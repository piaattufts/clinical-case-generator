"""Upsert official terminology rows. Identifiers are taken from source clients only."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.reference import (
    mark_source_sync_error,
    mark_source_sync_success,
    upsert_diagnosis_icd10cm,
    upsert_lab_test,
    upsert_medication,
    upsert_unit,
)
from app.sources.exceptions import SourceNotConfigured
from app.sources.icd10cm import Icd10CmClient, Icd10CmConcept
from app.sources.loinc import LoincClient, LoincConcept
from app.sources.rxnorm import (
    BRAND_TTY,
    PRESCRIBABLE_TTY,
    RELATED_TTY,
    RxNormClient,
    RxNormConcept,
)
from app.sources.ucum import UcumClient, UcumUnit
from app.utils.provenance import build_provenance

DEFAULT_SYNC_LIMIT = 20
MAX_SYNC_LIMIT = 100


def _retrieved_at(provenance: dict[str, Any]) -> datetime:
    value = provenance["retrieved_at"]
    if isinstance(value, datetime):
        return value
    raise TypeError("retrieved_at must be a datetime")


@dataclass
class SyncResult:
    source_code: str
    upserted: int
    identifiers: list[str] = field(default_factory=list)
    source_version: str | None = None


def _clamp_limit(limit: int) -> int:
    if limit < 1:
        raise ValueError("limit must be a positive integer")
    return min(limit, MAX_SYNC_LIMIT)


def sync_rxnorm(
    session: Session,
    *,
    name: str | None = None,
    rxcui: str | None = None,
    limit: int = DEFAULT_SYNC_LIMIT,
    client: RxNormClient | None = None,
) -> SyncResult:
    """Fetch named or RXCUI-selected RxNorm concepts and upsert by RXCUI.

    A full RxNorm import is not performed.
    """
    name_text = name.strip() if name is not None else ""
    rxcui_text = rxcui.strip() if rxcui is not None else ""
    if name_text == "" and rxcui_text == "":
        raise ValueError("Provide a name or RXCUI. Full RxNorm import is not run by default.")
    capped = _clamp_limit(limit)
    owns_client = client is None
    rxnav = client or RxNormClient()
    retrieved_at: datetime | None = None
    try:
        version = rxnav.version()
        if rxcui_text != "":
            concept = rxnav.lookup_by_rxcui(rxcui_text)
            selected = [concept] if concept is not None else []
        else:
            selected = rxnav.search_by_name(name_text)[:capped]
        identifiers: list[str] = []
        for concept in selected:
            extra = rxnav.properties(concept.rxcui)
            related = rxnav.related_concepts(concept.rxcui, tty=RELATED_TTY)
            provenance = build_provenance("RXNORM", version)
            retrieved_at = _retrieved_at(provenance)
            values = _medication_values(concept, extra, related, provenance)
            upsert_medication(session, values)
            identifiers.append(concept.rxcui)
        retrieved = (
            retrieved_at
            if retrieved_at is not None
            else _retrieved_at(build_provenance("RXNORM", version))
        )
        mark_source_sync_success(
            session,
            "RXNORM",
            records_imported=len(identifiers),
            source_version=version,
            retrieved_at=retrieved,
        )
        return SyncResult(
            source_code="RXNORM",
            upserted=len(identifiers),
            identifiers=identifiers,
            source_version=version,
        )
    except Exception as exc:
        when = _retrieved_at(build_provenance("RXNORM"))
        mark_source_sync_error(session, "RXNORM", message=str(exc), retrieved_at=when)
        raise
    finally:
        if owns_client:
            rxnav.close()


def sync_loinc(
    session: Session,
    *,
    query: str | None = None,
    code: str | None = None,
    limit: int = DEFAULT_SYNC_LIMIT,
    client: LoincClient | None = None,
) -> SyncResult:
    """Fetch LOINC terms by code or filtered search. There is no generated fallback."""
    query_text = query.strip() if query is not None else ""
    code_text = code.strip() if code is not None else ""
    if query_text == "" and code_text == "":
        raise ValueError("Provide --query or --code. Full LOINC import is not run by default.")
    capped = _clamp_limit(limit)
    owns_client = client is None
    loinc: LoincClient | None = client
    try:
        if loinc is None:
            loinc = LoincClient()
        if code_text != "":
            looked_up = loinc.lookup_by_code(code_text)
            selected = [looked_up] if looked_up is not None else []
        else:
            selected = []
            for hit in loinc.search_by_name(query_text, count=capped):
                detailed = loinc.lookup_by_code(hit.loinc_code)
                selected.append(detailed if detailed is not None else hit)
        version: str | None = None
        identifiers: list[str] = []
        retrieved_at: datetime | None = None
        for concept in selected:
            version = concept.version or version
            provenance = build_provenance("LOINC", version)
            retrieved_at = _retrieved_at(provenance)
            upsert_lab_test(session, _lab_values(concept, provenance))
            identifiers.append(concept.loinc_code)
        retrieved = (
            retrieved_at
            if retrieved_at is not None
            else _retrieved_at(build_provenance("LOINC", version))
        )
        mark_source_sync_success(
            session,
            "LOINC",
            records_imported=len(identifiers),
            source_version=version,
            retrieved_at=retrieved,
        )
        return SyncResult(
            source_code="LOINC",
            upserted=len(identifiers),
            identifiers=identifiers,
            source_version=version,
        )
    except Exception as exc:
        when = _retrieved_at(build_provenance("LOINC"))
        mark_source_sync_error(
            session,
            "LOINC",
            message=str(exc),
            retrieved_at=when,
            not_configured=isinstance(exc, SourceNotConfigured),
        )
        raise
    finally:
        if owns_client and loinc is not None:
            loinc.close()


def sync_ucum(
    session: Session,
    *,
    query: str | None = None,
    code: str | None = None,
    import_all: bool = False,
    limit: int = DEFAULT_SYNC_LIMIT,
    client: UcumClient | None = None,
) -> SyncResult:
    """Import units from official UCUM essence XML.

    Conversion factors are copied, never invented.
    """
    query_text = query.strip() if query is not None else ""
    code_text = code.strip() if code is not None else ""
    if not import_all and query_text == "" and code_text == "":
        raise ValueError(
            "Provide --query, --code, or --all. Full UCUM import is not run by default."
        )
    capped = _clamp_limit(limit)
    owns_client = client is None
    ucum = client or UcumClient()
    try:
        xml_text = ucum.fetch_essence_xml()
        if import_all:
            selected = ucum.list_units(xml_text)
        elif code_text != "":
            selected = [unit for unit in ucum.list_units(xml_text) if unit.ucum_code == code_text]
        else:
            selected = ucum.search_units(query_text, xml_text=xml_text)[:capped]
        version = selected[0].source_version if selected else None
        if version is None:
            parsed_all = ucum.list_units(xml_text)
            version = parsed_all[0].source_version if parsed_all else None
        identifiers: list[str] = []
        retrieved_at: datetime | None = None
        for unit in selected:
            provenance = build_provenance("UCUM", unit.source_version or version)
            retrieved_at = _retrieved_at(provenance)
            upsert_unit(session, _unit_values(unit, provenance))
            identifiers.append(unit.ucum_code)
        retrieved = (
            retrieved_at
            if retrieved_at is not None
            else _retrieved_at(build_provenance("UCUM", version))
        )
        mark_source_sync_success(
            session,
            "UCUM",
            records_imported=len(identifiers),
            source_version=version,
            retrieved_at=retrieved,
        )
        return SyncResult(
            source_code="UCUM",
            upserted=len(identifiers),
            identifiers=identifiers,
            source_version=version,
        )
    except Exception as exc:
        when = _retrieved_at(build_provenance("UCUM"))
        mark_source_sync_error(session, "UCUM", message=str(exc), retrieved_at=when)
        raise
    finally:
        if owns_client:
            ucum.close()


def sync_icd10cm(
    session: Session,
    *,
    query: str | None = None,
    code: str | None = None,
    limit: int = DEFAULT_SYNC_LIMIT,
    client: Icd10CmClient | None = None,
) -> SyncResult:
    """Store ICD-10-CM code and exact official description. No model-generated codes."""
    query_text = query.strip() if query is not None else ""
    code_text = code.strip() if code is not None else ""
    if query_text == "" and code_text == "":
        raise ValueError("Provide --query or --code. Full ICD-10-CM import is not run by default.")
    capped = _clamp_limit(limit)
    owns_client = client is None
    icd = client or Icd10CmClient()
    try:
        selected: list[Icd10CmConcept]
        if code_text != "":
            looked_up = icd.lookup_by_code(code_text)
            selected = [looked_up] if looked_up is not None else []
        else:
            selected = icd.search(query_text, count=capped, offset=0)
        identifiers: list[str] = []
        retrieved_at: datetime | None = None
        for concept in selected:
            provenance = build_provenance("ICD10CM")
            retrieved_at = _retrieved_at(provenance)
            upsert_diagnosis_icd10cm(session, _diagnosis_values(concept, provenance))
            identifiers.append(concept.icd10cm_code)
        retrieved = (
            retrieved_at if retrieved_at is not None else _retrieved_at(build_provenance("ICD10CM"))
        )
        mark_source_sync_success(
            session,
            "ICD10CM",
            records_imported=len(identifiers),
            source_version=None,
            retrieved_at=retrieved,
        )
        return SyncResult(
            source_code="ICD10CM",
            upserted=len(identifiers),
            identifiers=identifiers,
            source_version=None,
        )
    except Exception as exc:
        when = _retrieved_at(build_provenance("ICD10CM"))
        mark_source_sync_error(session, "ICD10CM", message=str(exc), retrieved_at=when)
        raise
    finally:
        if owns_client:
            icd.close()


def _medication_values(
    concept: RxNormConcept,
    extra: dict[str, str],
    related: list[RxNormConcept],
    provenance: dict[str, Any],
) -> dict[str, Any]:
    tty = concept.tty
    related_by_tty = _index_related(related)
    ingredient = _first_name(related_by_tty.get("IN"))
    brand_name = _first_name(related_by_tty.get("BN"))
    dose_form = _first_name(related_by_tty.get("DF"))
    generic_name = concept.name if tty in {"IN", "PIN", "SCD", "SCDC", "SCDG", "GPCK"} else None
    if generic_name is None:
        generic_name = ingredient or _first_name(related_by_tty.get("SCD"))
    if tty in BRAND_TTY and brand_name is None:
        brand_name = concept.synonym or concept.name
    strength = extra.get("AVAILABLE_STRENGTH") or extra.get("STRENGTH")
    return {
        "rxcui": concept.rxcui,
        "concept_name": concept.name,
        "generic_name": generic_name,
        "brand_name": brand_name,
        "ingredient": ingredient,
        "strength": strength,
        "strength_value": None,
        "strength_unit": None,
        "dose_form": dose_form,
        "route": extra.get("ROUTE"),
        "term_type": tty,
        "is_brand": tty in BRAND_TTY if tty is not None else None,
        "is_current": None if concept.suppress is None else concept.suppress.upper() != "Y",
        "prescribable": tty in PRESCRIBABLE_TTY if tty is not None else None,
        "source_concept_id": concept.rxcui,
        "source_system": provenance["source_system"],
        "source_version": provenance["source_version"],
        "retrieved_at": provenance["retrieved_at"],
    }


def _lab_values(concept: LoincConcept, provenance: dict[str, Any]) -> dict[str, Any]:
    return {
        "loinc_code": concept.loinc_code,
        "long_common_name": concept.long_common_name,
        "short_name": concept.short_name,
        "component": concept.component,
        "property": concept.property_code,
        "time_aspect": concept.time_aspect,
        "system_specimen": concept.system_specimen,
        "scale": concept.scale,
        "method": concept.method,
        "class_name": concept.class_name,
        "status": concept.status,
        "example_ucum_units": concept.example_ucum_units,
        "source_system": provenance["source_system"],
        "source_version": provenance["source_version"] or concept.version,
        "retrieved_at": provenance["retrieved_at"],
    }


def _unit_values(unit: UcumUnit, provenance: dict[str, Any]) -> dict[str, Any]:
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


def _diagnosis_values(concept: Icd10CmConcept, provenance: dict[str, Any]) -> dict[str, Any]:
    return {
        "snomed_code": None,
        "icd10cm_code": concept.icd10cm_code,
        "preferred_name": concept.description,
        "synonyms": None,
        "semantic_category": None,
        "parent_concept_id": None,
        "active": True,
        "source_system": provenance["source_system"],
        "source_version": provenance["source_version"],
        "retrieved_at": provenance["retrieved_at"],
    }


def _index_related(related: list[RxNormConcept]) -> dict[str, list[RxNormConcept]]:
    grouped: dict[str, list[RxNormConcept]] = {}
    for concept in related:
        if concept.tty is None:
            continue
        grouped.setdefault(concept.tty, []).append(concept)
    return grouped


def _first_name(concepts: list[RxNormConcept] | None) -> str | None:
    if not concepts:
        return None
    for concept in concepts:
        if concept.name is not None and concept.name.strip() != "":
            return concept.name
    return None
