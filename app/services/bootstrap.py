"""Bounded reference bootstrap from a checked-in human-readable manifest.

Identifiers are taken only from official source responses. Unresolved requests are
reported. A second run upserts and does not duplicate canonical identifiers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reference import RefDiagnosis, RefDrugLabel, RefLabTest, RefMedication, RefUnit
from app.repositories.reference import (
    get_data_source,
    list_medications,
    mark_source_sync_error,
    mark_source_sync_success,
    search_diagnoses,
    search_lab_tests,
    search_medications,
    upsert_drug_label,
    upsert_symptom,
    upsert_unit,
)
from app.services.reference_sync import (
    DEFAULT_SYNC_LIMIT,
    sync_icd10cm,
    sync_loinc,
    sync_rxnorm,
)
from app.sources.conditions import ConditionsClient
from app.sources.dailymed import DailyMedClient, DailyMedLabel
from app.sources.exceptions import SourceNotConfigured
from app.sources.icd10cm import Icd10CmClient
from app.sources.loinc import LoincClient
from app.sources.rxclass import RxClassClient
from app.sources.rxnorm import RxNormClient, RxNormConcept
from app.sources.ucum import UcumClient
from app.utils.provenance import build_provenance

BOOTSTRAP_DIR = Path(__file__).resolve().parents[2] / "data" / "bootstrap"
DEFAULT_MANIFEST_PATH = BOOTSTRAP_DIR / "manifest.json"
DEFAULT_RULE_TEMPLATE_PATH = BOOTSTRAP_DIR / "rule_templates.json"
DEFAULT_SCENARIO_PATH = BOOTSTRAP_DIR / "scenarios.json"

TTY_PRIORITY = {
    "IN": 0,
    "PIN": 1,
    "MIN": 2,
    "SCD": 3,
    "SBD": 4,
    "BN": 5,
}


@dataclass
class UnresolvedRequest:
    kind: str
    request: str
    reason: str


@dataclass
class BootstrapResult:
    upserted: dict[str, list[str]] = field(default_factory=dict)
    unresolved: list[UnresolvedRequest] = field(default_factory=list)
    skipped: list[UnresolvedRequest] = field(default_factory=list)
    rules_enabled: list[str] = field(default_factory=list)


@dataclass
class SourceClients:
    rxnorm: RxNormClient | None = None
    icd10cm: Icd10CmClient | None = None
    ucum: UcumClient | None = None
    loinc: LoincClient | None = None
    conditions: ConditionsClient | None = None
    dailymed: DailyMedClient | None = None
    rxclass: RxClassClient | None = None


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def load_manifest(path: Path | None = None) -> dict[str, list[str]]:
    raw = load_json_object(path or DEFAULT_MANIFEST_PATH)
    result: dict[str, list[str]] = {}
    for key in ("medications", "diagnoses", "symptoms", "labs", "units"):
        values = raw.get(key, [])
        if not isinstance(values, list):
            raise ValueError(f"manifest.{key} must be a list of search strings")
        cleaned: list[str] = []
        for item in values:
            text = str(item).strip()
            if text == "":
                continue
            cleaned.append(text)
        result[key] = cleaned
    return result


def bootstrap_reference_data(
    session: Session,
    *,
    manifest_path: Path | None = None,
    clients: SourceClients | None = None,
    sync_labels: bool = True,
    sync_rules: bool = True,
    rule_template_path: Path | None = None,
) -> BootstrapResult:
    """Resolve manifest names through official APIs and upsert source-backed rows."""
    from app.services.rules import enable_rules_from_templates

    manifest = load_manifest(manifest_path)
    bundle = clients or SourceClients()
    owned: list[Any] = []
    result = BootstrapResult(
        upserted={
            "medications": [],
            "diagnoses": [],
            "symptoms": [],
            "labs": [],
            "units": [],
            "labels": [],
        }
    )
    try:
        rxnorm = bundle.rxnorm or RxNormClient()
        if bundle.rxnorm is None:
            owned.append(rxnorm)
        icd = bundle.icd10cm or Icd10CmClient()
        if bundle.icd10cm is None:
            owned.append(icd)
        ucum = bundle.ucum or UcumClient()
        if bundle.ucum is None:
            owned.append(ucum)
        conditions = bundle.conditions or ConditionsClient()
        if bundle.conditions is None:
            owned.append(conditions)
        dailymed = bundle.dailymed or DailyMedClient()
        if bundle.dailymed is None:
            owned.append(dailymed)
        rxclass = bundle.rxclass or RxClassClient()
        if bundle.rxclass is None:
            owned.append(rxclass)

        _bootstrap_medications(session, rxnorm, manifest["medications"], result)
        _bootstrap_diagnoses(session, icd, manifest["diagnoses"], result)
        _bootstrap_symptoms(session, conditions, manifest["symptoms"], result)
        _bootstrap_units(session, ucum, manifest["units"], result)
        _bootstrap_labs(session, bundle.loinc, manifest["labs"], result)
        if sync_labels:
            _bootstrap_labels(session, dailymed, result)
        if sync_rules:
            result.rules_enabled = enable_rules_from_templates(
                session,
                dailymed=dailymed,
                rxclass=rxclass,
                template_path=rule_template_path,
            )
        _refresh_registry_counts(session)
        return result
    finally:
        for client in owned:
            if hasattr(client, "close"):
                client.close()


def match_medication(session: Session, query: str) -> RefMedication | None:
    rows, _ = search_medications(session, query, limit=50, offset=0)
    return _prefer_medication_row(list(rows), query)


def match_diagnosis(session: Session, query: str) -> RefDiagnosis | None:
    rows, _ = search_diagnoses(session, query, limit=50, offset=0)
    ranked = sorted(
        rows,
        key=lambda row: (
            0 if _contains(row.preferred_name, query) else 1,
            0 if _contains(row.icd10cm_code, query) else 1,
            (row.icd10cm_code or ""),
        ),
    )
    return ranked[0] if ranked else None


def match_lab(session: Session, query: str) -> RefLabTest | None:
    rows, _ = search_lab_tests(session, query, limit=50, offset=0)
    ranked = sorted(
        rows,
        key=lambda row: (
            0 if _contains(row.long_common_name, query) or _contains(row.component, query) else 1,
            row.loinc_code,
        ),
    )
    return ranked[0] if ranked else None


def _bootstrap_medications(
    session: Session,
    client: RxNormClient,
    names: list[str],
    result: BootstrapResult,
) -> None:
    for name in names:
        try:
            concepts = sorted(
                client.search_by_name(name),
                key=lambda item: (TTY_PRIORITY.get(item.tty or "", 9), item.rxcui),
            )
            chosen = _prefer_rxnorm_concept(concepts, name)
            if chosen is None:
                result.unresolved.append(
                    UnresolvedRequest("medication", name, "RxNorm returned no concept")
                )
                continue
            sync = sync_rxnorm(session, rxcui=chosen.rxcui, client=client)
            result.upserted["medications"].extend(sync.identifiers)
        except Exception as exc:
            result.unresolved.append(UnresolvedRequest("medication", name, str(exc)))


def _bootstrap_diagnoses(
    session: Session,
    client: Icd10CmClient,
    names: list[str],
    result: BootstrapResult,
) -> None:
    for name in names:
        try:
            hits = client.search(name, count=DEFAULT_SYNC_LIMIT, offset=0)
            chosen = _prefer_icd_concept(hits, name)
            if chosen is None:
                result.unresolved.append(
                    UnresolvedRequest("diagnosis", name, "ICD-10-CM returned no concept")
                )
                continue
            sync = sync_icd10cm(session, code=chosen.icd10cm_code, client=client)
            result.upserted["diagnoses"].extend(sync.identifiers)
        except Exception as exc:
            result.unresolved.append(UnresolvedRequest("diagnosis", name, str(exc)))


def _bootstrap_symptoms(
    session: Session,
    client: ConditionsClient,
    names: list[str],
    result: BootstrapResult,
) -> None:
    for name in names:
        try:
            hits = sorted(client.search(name, count=DEFAULT_SYNC_LIMIT), key=lambda item: item.name)
            chosen = next((item for item in hits if _contains(item.name, name)), None)
            if chosen is None and hits:
                chosen = hits[0]
            if chosen is None:
                result.unresolved.append(
                    UnresolvedRequest("symptom", name, "NLM conditions returned no concept")
                )
                continue
            provenance = build_provenance("NLM_CONDITIONS")
            row = upsert_symptom(
                session,
                {
                    "snomed_code": None,
                    "preferred_name": chosen.name,
                    "synonyms": chosen.synonyms or None,
                    "body_system": None,
                    "semantic_category": "symptom",
                    "active": True,
                    "source_system": provenance["source_system"],
                    "source_version": provenance["source_version"],
                    "retrieved_at": provenance["retrieved_at"],
                },
            )
            result.upserted["symptoms"].append(row.preferred_name or chosen.name)
        except Exception as exc:
            result.unresolved.append(UnresolvedRequest("symptom", name, str(exc)))


def _bootstrap_units(
    session: Session,
    client: UcumClient,
    names: list[str],
    result: BootstrapResult,
) -> None:
    try:
        xml_text = client.fetch_essence_xml()
    except Exception as exc:
        for name in names:
            result.unresolved.append(UnresolvedRequest("unit", name, str(exc)))
        return
    retrieved_at: datetime | None = None
    version: str | None = None
    identifiers: list[str] = []
    try:
        for name in names:
            units = client.search_units(name, xml_text=xml_text)[:DEFAULT_SYNC_LIMIT]
            if not units:
                result.unresolved.append(
                    UnresolvedRequest("unit", name, "UCUM essence had no match")
                )
                continue
            for unit in units:
                provenance = build_provenance("UCUM", unit.source_version)
                retrieved_at = _as_datetime(provenance["retrieved_at"])
                version = unit.source_version or version
                upsert_unit(session, _unit_row(unit, provenance))
                identifiers.append(unit.ucum_code)
        result.upserted["units"].extend(identifiers)
        if identifiers:
            mark_source_sync_success(
                session,
                "UCUM",
                records_imported=len(set(identifiers)),
                source_version=version,
                retrieved_at=retrieved_at or _as_datetime(build_provenance("UCUM")["retrieved_at"]),
            )
    except Exception as exc:
        when = _as_datetime(build_provenance("UCUM")["retrieved_at"])
        mark_source_sync_error(session, "UCUM", message=str(exc), retrieved_at=when)
        raise


def _unit_row(unit: Any, provenance: dict[str, Any]) -> dict[str, Any]:
    return {
        "ucum_code": unit.ucum_code,
        "display_name": unit.display_name,
        "quantity_type": unit.quantity_type,
        "canonical_unit": unit.canonical_unit,
        "conversion_factor": unit.conversion_factor,
        "active": unit.active,
        "source_system": provenance["source_system"],
        "source_version": provenance["source_version"] or unit.source_version,
        "retrieved_at": provenance["retrieved_at"],
    }


def _bootstrap_labs(
    session: Session,
    supplied: LoincClient | None,
    names: list[str],
    result: BootstrapResult,
) -> None:
    if not names:
        return
    owned = False
    client = supplied
    try:
        if client is None:
            client = LoincClient()
            owned = True
    except SourceNotConfigured as exc:
        for name in names:
            result.skipped.append(UnresolvedRequest("lab", name, str(exc)))
        when = _as_datetime(build_provenance("LOINC")["retrieved_at"])
        mark_source_sync_error(
            session,
            "LOINC",
            message=str(exc),
            retrieved_at=when,
            not_configured=True,
        )
        return
    try:
        for name in names:
            try:
                sync = sync_loinc(session, query=name, client=client)
                if not sync.identifiers:
                    result.unresolved.append(
                        UnresolvedRequest("lab", name, "LOINC returned no concept")
                    )
                    continue
                result.upserted["labs"].extend(sync.identifiers)
            except Exception as exc:
                result.unresolved.append(UnresolvedRequest("lab", name, str(exc)))
    finally:
        if owned and client is not None:
            client.close()


def _bootstrap_labels(session: Session, client: DailyMedClient, result: BootstrapResult) -> None:
    retrieved_at: datetime | None = None
    for medication in list_medications(session):
        try:
            labels = client.labels_for_rxcui(medication.rxcui, limit=1)
        except Exception as exc:
            result.unresolved.append(UnresolvedRequest("label", medication.rxcui, str(exc)))
            continue
        for label in labels:
            provenance = build_provenance("DAILYMED")
            retrieved_at = _as_datetime(provenance["retrieved_at"])
            upsert_drug_label(session, _label_values(label, provenance))
            result.upserted["labels"].append(label.set_id)
    if retrieved_at is not None:
        mark_source_sync_success(
            session,
            "DAILYMED",
            records_imported=len(result.upserted["labels"]),
            source_version=None,
            retrieved_at=retrieved_at,
        )


def _label_values(label: DailyMedLabel, provenance: dict[str, Any]) -> dict[str, Any]:
    return {
        "set_id": label.set_id,
        "rxcui": label.rxcui,
        "drug_name": label.title,
        "active_ingredient": label.active_ingredient,
        "indication_text": label.indication_text,
        "dosage_text": label.dosage_text,
        "route": None,
        "contraindications_text": label.contraindications_text,
        "warnings_text": label.warnings_text,
        "renal_impairment_text": None,
        "hepatic_impairment_text": None,
        "geriatric_use_text": None,
        "source_system": provenance["source_system"],
        "source_version": provenance["source_version"],
        "retrieved_at": provenance["retrieved_at"],
    }


def _prefer_rxnorm_concept(concepts: list[RxNormConcept], query: str) -> RxNormConcept | None:
    if not concepts:
        return None
    ranked = sorted(
        concepts,
        key=lambda item: (
            0 if _contains(item.name, query) else 1,
            TTY_PRIORITY.get(item.tty or "", 9),
            item.rxcui,
        ),
    )
    return ranked[0]


def _prefer_icd_concept(concepts: Any, query: str) -> Any | None:
    ranked = sorted(
        list(concepts),
        key=lambda item: (
            0 if _contains(item.description, query) else 1,
            len(item.icd10cm_code),
            item.icd10cm_code,
        ),
    )
    return ranked[0] if ranked else None


def _prefer_medication_row(rows: list[RefMedication], query: str) -> RefMedication | None:
    ranked = sorted(
        rows,
        key=lambda row: (
            0
            if _contains(row.ingredient, query)
            or _contains(row.generic_name, query)
            or _contains(row.concept_name, query)
            else 1,
            TTY_PRIORITY.get(row.term_type or "", 9),
            row.rxcui,
        ),
    )
    return ranked[0] if ranked else None


def _refresh_registry_counts(session: Session) -> None:
    now = _as_datetime(build_provenance("RXNORM")["retrieved_at"])
    counts = {
        "RXNORM": int(session.scalar(select(func.count()).select_from(RefMedication)) or 0),
        "ICD10CM": int(session.scalar(select(func.count()).select_from(RefDiagnosis)) or 0),
        "LOINC": int(session.scalar(select(func.count()).select_from(RefLabTest)) or 0),
        "UCUM": int(session.scalar(select(func.count()).select_from(RefUnit)) or 0),
        "DAILYMED": int(session.scalar(select(func.count()).select_from(RefDrugLabel)) or 0),
    }
    for source_code, total in counts.items():
        row = get_data_source(session, source_code)
        if row is None or total <= 0:
            continue
        row.records_imported = total
        if row.last_successful_sync_at is None:
            row.last_successful_sync_at = now
        row.last_sync_at = now
        row.sync_status = "synced"
        row.error_message = None
    session.flush()


def _contains(value: str | None, query: str) -> bool:
    if value is None:
        return False
    return query.casefold() in value.casefold()


def _as_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return value
    raise TypeError("retrieved_at must be a datetime")
