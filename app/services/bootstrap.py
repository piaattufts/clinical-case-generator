"""Bounded reference bootstrap from a checked-in human-readable manifest.

Identifiers are taken only from official source responses. Unresolved requests are
reported. A second run upserts and does not duplicate canonical identifiers.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reference import (
    RefDiagnosis,
    RefDrugLabel,
    RefLabTest,
    RefMedication,
    RefSymptom,
    RefUnit,
)
from app.repositories.reference import (
    get_data_source,
    list_medications,
    mark_source_sync_error,
    mark_source_sync_success,
    search_diagnoses,
    search_lab_tests,
    search_medications,
    upsert_drug_label,
    upsert_medication_class,
    upsert_symptom,
    upsert_unit,
)
from app.services.clinical_coherence import (
    formulation_preference_rank,
    formulation_preference_rank_blob,
    is_symptom_level_concept,
    lab_unit_rank,
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
from app.sources.hpo import HpoClient
from app.sources.icd10cm import Icd10CmClient
from app.sources.loinc import LoincClient, LoincConcept
from app.sources.rxclass import RxClassClient
from app.sources.rxnorm import RxNormClient, RxNormConcept
from app.sources.ucum import UcumClient
from app.utils.loinc_codes import is_storeable_lab_code
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
_FORMULATION_PREFER = ("tablet", "capsule")
_FORMULATION_DEPRIORITIZE = (
    "solution",
    "suspension",
    "syrup",
    "elixir",
    "gel",
    "cream",
    "ointment",
    "injectable",
    "injection",
    "intravenous",
    "powder",
)
LOINC_RANK_LOOKUPS = 8
_LOINC_DEPRIORITIZE = (
    "panel",
    "calibrator",
    "control",
    "challenge",
    "deprecated",
    "hedis",
    "value set",
    "days in therapeutic",
    "adjusted for egfr",
    "dialysis",
    " --",
    "fetus",
    "blood product",
    "free hemoglobin",
)
_DIAGNOSIS_DEPRIORITIZE = (
    "neonatal",
    "newborn",
    "perinatal",
    "fetal",
    "in diseases classified elsewhere",
    "unspecified complications",
)
_PEDIATRIC_CHAPTER_PREFIXES = ("P", "O")
_LOINC_PREFERRED_SPECIMEN = (
    "serum or plasma",
    "platelet poor plasma",
)
_LOINC_PREFERRED_SPECIMEN_SECONDARY = (" in blood",)
_LOINC_DEPRIORITIZE_SPECIMEN = ("urine", "stool", "hair", "csf", "cord blood")


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
    hpo: HpoClient | None = None
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
        hpo = bundle.hpo or HpoClient()
        if bundle.hpo is None:
            owned.append(hpo)
        dailymed = bundle.dailymed or DailyMedClient()
        if bundle.dailymed is None:
            owned.append(dailymed)
        rxclass = bundle.rxclass or RxClassClient()
        if bundle.rxclass is None:
            owned.append(rxclass)

        _bootstrap_medications(session, rxnorm, manifest["medications"], result)
        _bootstrap_medication_classes(session, rxclass, result)
        _bootstrap_diagnoses(session, icd, manifest["diagnoses"], result)
        _bootstrap_symptoms(session, conditions, hpo, manifest["symptoms"], result)
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
        key=lambda row: _diagnosis_rank_key(row.preferred_name, row.icd10cm_code, query),
    )
    return ranked[0] if ranked else None


def match_lab(session: Session, query: str) -> RefLabTest | None:
    rows, _ = search_lab_tests(session, query, limit=50, offset=0)
    usable = [row for row in rows if is_storeable_lab_code(row.loinc_code)]
    ranked = sorted(usable, key=lambda row: _loinc_rank_key(_concept_from_lab_row(row), query))
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
            chosen = _prefer_rxnorm_concept(concepts, name, client=client)
            if chosen is None:
                result.unresolved.append(
                    UnresolvedRequest("medication", name, "RxNorm returned no concept")
                )
                continue
            sync = sync_rxnorm(session, rxcui=chosen.rxcui, client=client)
            result.upserted["medications"].extend(sync.identifiers)
        except Exception as exc:
            result.unresolved.append(UnresolvedRequest("medication", name, str(exc)))


def _bootstrap_medication_classes(
    session: Session,
    client: RxClassClient,
    result: BootstrapResult,
) -> None:
    imported = 0
    for medication in list_medications(session):
        try:
            hits = client.classes_for_rxcui(medication.rxcui)
        except Exception as exc:
            result.unresolved.append(
                UnresolvedRequest("medication_class", medication.rxcui, str(exc))
            )
            continue
        for hit in hits:
            if hit.class_id.strip() == "" or hit.class_name.strip() == "":
                continue
            provenance = build_provenance("RXCLASS")
            upsert_medication_class(
                session,
                {
                    "rxcui": hit.rxcui or medication.rxcui,
                    "class_id": hit.class_id,
                    "class_name": hit.class_name,
                    "class_type": hit.class_type,
                    "rela": hit.rela,
                    **provenance,
                },
            )
            imported += 1
    if imported:
        mark_source_sync_success(
            session,
            "RXCLASS",
            records_imported=imported,
            source_version=None,
            retrieved_at=datetime.now(UTC),
        )


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
    hpo: HpoClient | None,
    names: list[str],
    result: BootstrapResult,
) -> None:
    for name in names:
        try:
            hits = sorted(client.search(name, count=DEFAULT_SYNC_LIMIT), key=lambda item: item.name)
            ranked = sorted(
                (
                    item
                    for item in hits
                    if is_symptom_level_concept(item.name, name)
                    or any(is_symptom_level_concept(synonym, name) for synonym in item.synonyms)
                ),
                key=lambda item: (
                    0 if (item.name or "").casefold() == name.casefold() else 1,
                    item.name or "",
                ),
            )
            chosen = ranked[0] if ranked else None
            if chosen is not None:
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
                continue
            hpo_row = _bootstrap_hpo_symptom(session, hpo, name) if hpo is not None else None
            if hpo_row is not None:
                result.upserted["symptoms"].append(hpo_row.preferred_name or name)
                continue
            result.unresolved.append(
                UnresolvedRequest(
                    "symptom",
                    name,
                    "NLM conditions and HPO returned no token-matched concept",
                )
            )
        except Exception as exc:
            result.unresolved.append(UnresolvedRequest("symptom", name, str(exc)))


def _bootstrap_hpo_symptom(session: Session, client: HpoClient, name: str) -> RefSymptom | None:
    hits = sorted(client.search(name, count=DEFAULT_SYNC_LIMIT), key=lambda item: item.hpo_id)
    chosen = next(
        (
            item
            for item in hits
            if is_symptom_level_concept(item.name, name)
            or any(is_symptom_level_concept(synonym, name) for synonym in item.synonyms)
        ),
        None,
    )
    if chosen is None:
        return None
    provenance = build_provenance("NLM_HPO")
    synonyms = [chosen.hpo_id, *chosen.synonyms]
    return upsert_symptom(
        session,
        {
            "snomed_code": None,
            "preferred_name": chosen.name,
            "synonyms": synonyms,
            "body_system": None,
            "semantic_category": "symptom",
            "active": True,
            "source_system": provenance["source_system"],
            "source_version": provenance["source_version"],
            "retrieved_at": provenance["retrieved_at"],
        },
    )


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
                hits = _collect_loinc_term_hits(client, name)
                preview = sorted(
                    hits,
                    key=lambda item: _loinc_rank_key(item, name),
                )
                detailed: list[LoincConcept] = []
                for hit in preview[:LOINC_RANK_LOOKUPS]:
                    looked = client.lookup_by_code(hit.loinc_code)
                    detailed.append(looked if looked is not None else hit)
                chosen = prefer_loinc_concept(detailed, name)
                if chosen is None or not is_storeable_lab_code(chosen.loinc_code):
                    result.unresolved.append(
                        UnresolvedRequest("lab", name, "LOINC returned no observation concept")
                    )
                    continue
                sync = sync_loinc(session, code=chosen.loinc_code, client=client)
                if not sync.identifiers:
                    result.unresolved.append(
                        UnresolvedRequest("lab", name, "LOINC lookup returned no concept")
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


def _prefer_rxnorm_concept(
    concepts: list[RxNormConcept],
    query: str,
    *,
    client: RxNormClient | None = None,
) -> RxNormConcept | None:
    if not concepts:
        return None
    filtered = [
        item for item in concepts if not is_unintended_combination(item, query, client=client)
    ]
    ranked = sorted(
        filtered or [],
        key=lambda item: (
            formulation_preference_rank_blob(
                " ".join(part for part in (item.name, item.synonym) if part),
                query,
            ),
            _ugly_product_rank(item.name),
            0 if _contains(item.name, query) else 1,
            TTY_PRIORITY.get(item.tty or "", 9),
            item.rxcui,
        ),
    )
    return ranked[0] if ranked else None


def prefer_loinc_concept(concepts: list[LoincConcept], query: str) -> LoincConcept | None:
    usable = [item for item in concepts if is_storeable_lab_code(item.loinc_code)]
    ranked = sorted(usable, key=lambda item: _loinc_rank_key(item, query))
    return ranked[0] if ranked else None


def _collect_loinc_term_hits(client: LoincClient, name: str) -> list[LoincConcept]:
    seen: set[str] = set()
    collected: list[LoincConcept] = []
    for query in _loinc_search_queries(name):
        hits = client.search_by_name(query, count=DEFAULT_SYNC_LIMIT)
        for hit in hits:
            if hit.loinc_code in seen or not is_storeable_lab_code(hit.loinc_code):
                continue
            seen.add(hit.loinc_code)
            collected.append(hit)
    return collected


def _loinc_search_queries(name: str) -> list[str]:
    queries: list[str] = []
    lowered = name.casefold()
    if not any(token in lowered for token in ("serum", "plasma", "blood")):
        queries.append(f"{name} in serum or plasma")
        queries.append(f"{name} in blood")
    if "[" not in name:
        queries.append(f"{name} [Mass/volume]")
        queries.append(f"{name} [Moles/volume]")
    queries.append(name)
    return queries


def _loinc_rank_key(
    item: LoincConcept, query: str
) -> tuple[int, int, int, int, int, int, int, int, int, str]:
    return (
        0 if _loinc_text_matches(item, query) else 1,
        _loinc_analyte_rank(item, query),
        0 if (item.status or "ACTIVE").upper() == "ACTIVE" else 1,
        1 if _loinc_deprioritized(item) else 0,
        _loinc_specimen_rank(item),
        1 if _loinc_deprioritized_specimen(item) else 0,
        lab_unit_rank(item, query),
        0 if item.example_ucum_units else 1,
        0 if item.long_common_name and "[" in item.long_common_name else 1,
        item.loinc_code,
    )


def _loinc_text_matches(item: LoincConcept, query: str) -> bool:
    return (
        _contains(item.long_common_name, query)
        or _contains(item.short_name, query)
        or _contains(item.component, query)
    )


def _loinc_analyte_rank(item: LoincConcept, query: str) -> int:
    name = (item.long_common_name or "").casefold()
    needle = re.escape(query.casefold().strip())
    if re.search(rf"{needle}(?: \[[^\]]+\]| in )", name) is not None:
        return 0
    return 1


def _loinc_deprioritized(item: LoincConcept) -> bool:
    blob = _loinc_blob(item)
    if any(token in blob for token in _LOINC_DEPRIORITIZE):
        return True
    return _loinc_ratio_outside_property(item.long_common_name)


def _loinc_ratio_outside_property(name: str | None) -> bool:
    if not name:
        return False
    stripped = re.sub(r"\[[^\]]*\]", "", name)
    return "/" in stripped


def _loinc_preferred_specimen(item: LoincConcept) -> bool:
    return _loinc_specimen_rank(item) == 0


def _loinc_specimen_rank(item: LoincConcept) -> int:
    blob = _loinc_blob(item)
    if any(token in blob for token in _LOINC_PREFERRED_SPECIMEN):
        return 0
    if any(token in blob for token in _LOINC_PREFERRED_SPECIMEN_SECONDARY):
        return 1
    return 2


def _loinc_deprioritized_specimen(item: LoincConcept) -> bool:
    blob = _loinc_blob(item)
    return any(token in blob for token in _LOINC_DEPRIORITIZE_SPECIMEN)


def _loinc_blob(item: LoincConcept) -> str:
    return " ".join(
        part
        for part in (item.long_common_name, item.short_name, item.component, item.class_name)
        if part
    ).casefold()


def _concept_from_lab_row(row: RefLabTest) -> LoincConcept:
    units = row.example_ucum_units if isinstance(row.example_ucum_units, list) else None
    return LoincConcept(
        loinc_code=row.loinc_code,
        long_common_name=row.long_common_name,
        short_name=row.short_name,
        component=row.component,
        class_name=row.class_name,
        status=row.status,
        example_ucum_units=[str(item) for item in units] if units else None,
    )


def _prefer_icd_concept(concepts: Any, query: str) -> Any | None:
    ranked = sorted(
        list(concepts),
        key=lambda item: _diagnosis_rank_key(item.description, item.icd10cm_code, query),
    )
    return ranked[0] if ranked else None


def _diagnosis_rank_key(
    name: str | None, code: str | None, query: str
) -> tuple[int, int, int, int, str]:
    lowered = (name or "").casefold()
    code_text = code or ""
    query_cf = query.casefold()
    pediatric_query = any(
        token in query_cf for token in ("neonatal", "newborn", "perinatal", "fetal")
    )
    deprioritize = 0
    if not pediatric_query:
        if any(token in lowered for token in _DIAGNOSIS_DEPRIORITIZE):
            deprioritize = 2
        if "candidal" in lowered or "candida" in lowered:
            deprioritize = max(deprioritize, 2)
        if code_text[:1].upper() in _PEDIATRIC_CHAPTER_PREFIXES:
            deprioritize = max(deprioritize, 2)
    unspecified = (
        2
        if "unspecified complications" in lowered
        else 1
        if "unspecified" in lowered
        else 0
    )
    return (
        0 if _contains(name, query) or _contains(code, query) else 1,
        deprioritize,
        unspecified,
        len(code_text),
        code_text,
    )


def _prefer_medication_row(rows: list[RefMedication], query: str) -> RefMedication | None:
    filtered = [
        row
        for row in rows
        if not looks_like_combination_name(row.concept_name)
        and not looks_like_combination_name(row.generic_name)
        and (row.term_type or "") != "MIN"
    ]
    ranked = sorted(
        filtered,
        key=lambda row: (
            0
            if _contains(row.ingredient, query)
            or _contains(row.generic_name, query)
            or _contains(row.concept_name, query)
            else 1,
            formulation_preference_rank(row, query),
            _ugly_product_rank(row.concept_name),
            _formulation_rank(row),
            TTY_PRIORITY.get(row.term_type or "", 9),
            row.rxcui,
        ),
    )
    return ranked[0] if ranked else None


def _formulation_rank(row: RefMedication) -> int:
    blob = " ".join(
        part
        for part in (row.dose_form, row.concept_name, row.generic_name, row.route)
        if part
    )
    return _formulation_rank_text(blob)


def _formulation_rank_text(blob: str) -> int:
    lowered = blob.casefold()
    if any(token in lowered for token in _FORMULATION_PREFER):
        return 0
    if any(token in lowered for token in _FORMULATION_DEPRIORITIZE):
        return 2
    return 1


def is_unintended_combination(
    concept: RxNormConcept,
    query: str,
    *,
    client: RxNormClient | None = None,
) -> bool:
    """True when a search hit is a multi-ingredient product the query did not request."""
    if query_allows_combination(query):
        return False
    if (concept.tty or "") == "MIN":
        return True
    if looks_like_combination_name(concept.name) or looks_like_combination_name(concept.synonym):
        return True
    if client is None or (concept.tty or "") not in {"SCD", "SBD", "GPCK", "BPCK", "SBDC"}:
        return False
    try:
        related = client.related_concepts(concept.rxcui, tty="IN")
    except Exception:
        return False
    ingredients = [item for item in related if (item.tty or "") == "IN"]
    return len(ingredients) > 1


def looks_like_combination_name(value: str | None) -> bool:
    if value is None:
        return False
    return " / " in value


def query_allows_combination(query: str) -> bool:
    text = query.strip().casefold()
    return " / " in text or " and " in text


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


def token_match(value: str | None, query: str) -> bool:
    """True when query appears as a whole token, not as a substring of another word."""
    if value is None:
        return False
    needle = query.strip()
    if needle == "":
        return False
    pattern = r"(?<![a-z0-9])" + re.escape(needle.casefold()) + r"(?![a-z0-9])"
    return re.search(pattern, value.casefold()) is not None


def _ugly_product_rank(name: str | None) -> int:
    lowered = (name or "").casefold()
    if lowered.startswith("nda") or " nda" in lowered:
        return 1
    return 0


def _contains(value: str | None, query: str) -> bool:
    if value is None:
        return False
    return query.casefold() in value.casefold()


def _as_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return value
    raise TypeError("retrieved_at must be a datetime")
