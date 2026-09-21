"""Lookups for reference tables. No clinical concepts are invented here."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from sqlalchemy import Select, String, cast, func, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from app.models.reference import (
    ClinicalRule,
    DataSourceRegistry,
    RefDiagnosis,
    RefDrugLabel,
    RefLabTest,
    RefMedication,
    RefSymptom,
    RefUnit,
)

SYNC_NEVER_SYNCED = "never_synced"
SYNC_NOT_CONFIGURED = "not_configured"

# Metadata only. records_imported stays 0. No terminology rows are created from this list.
SOURCE_REGISTRY_ROWS: tuple[dict[str, Any], ...] = (
    {
        "source_code": "RXNORM",
        "source_name": "RxNorm",
        "provider": "U.S. National Library of Medicine",
        "source_category": "medication",
        "access_type": "public",
        "requires_credentials": False,
        "enabled": True,
        "sync_status": SYNC_NEVER_SYNCED,
        "records_imported": 0,
        "license_or_terms": (
            "NLM RxNorm terms apply. Terminology content is not bundled with this application."
        ),
        "metadata": {"required_env": []},
    },
    {
        "source_code": "DAILYMED",
        "source_name": "DailyMed",
        "provider": "U.S. National Library of Medicine",
        "source_category": "medication_label",
        "access_type": "public",
        "requires_credentials": False,
        "enabled": True,
        "sync_status": SYNC_NEVER_SYNCED,
        "records_imported": 0,
        "license_or_terms": (
            "DailyMed label text is not bundled. NLM and FDA terms apply when it is retrieved."
        ),
        "metadata": {"required_env": []},
    },
    {
        "source_code": "LOINC",
        "source_name": "LOINC",
        "provider": "Regenstrief Institute",
        "source_category": "laboratory",
        "access_type": "credentialed",
        "requires_credentials": True,
        "enabled": False,
        "sync_status": SYNC_NOT_CONFIGURED,
        "records_imported": 0,
        "license_or_terms": ("LOINC requires a Regenstrief account. LOINC content is not bundled."),
        "metadata": {"required_env": ["LOINC_USERNAME", "LOINC_PASSWORD"]},
    },
    {
        "source_code": "UCUM",
        "source_name": "UCUM",
        "provider": "Regenstrief Institute",
        "source_category": "units",
        "access_type": "public",
        "requires_credentials": False,
        "enabled": True,
        "sync_status": SYNC_NEVER_SYNCED,
        "records_imported": 0,
        "license_or_terms": "UCUM content is not bundled. Regenstrief UCUM terms apply.",
        "metadata": {"required_env": []},
    },
    {
        "source_code": "ICD10CM",
        "source_name": "ICD-10-CM",
        "provider": "Centers for Disease Control and Prevention",
        "source_category": "diagnosis",
        "access_type": "public",
        "requires_credentials": False,
        "enabled": True,
        "sync_status": SYNC_NEVER_SYNCED,
        "records_imported": 0,
        "license_or_terms": "ICD-10-CM content is not bundled. CDC and CMS terms apply.",
        "metadata": {"required_env": []},
    },
    {
        "source_code": "SNOMED_CT",
        "source_name": "SNOMED CT",
        "provider": "SNOMED International",
        "source_category": "terminology",
        "access_type": "credentialed",
        "requires_credentials": True,
        "enabled": False,
        "sync_status": SYNC_NOT_CONFIGURED,
        "records_imported": 0,
        "license_or_terms": (
            "SNOMED CT requires an affiliate license. SNOMED CT content is not bundled."
        ),
        "metadata": {"required_env": ["SNOMED_BASE_URL", "SNOMED_API_TOKEN"]},
    },
    {
        "source_code": "ACCESS_GUDID",
        "source_name": "AccessGUDID",
        "provider": "U.S. Food and Drug Administration",
        "source_category": "device",
        "access_type": "public",
        "requires_credentials": False,
        "enabled": True,
        "sync_status": SYNC_NEVER_SYNCED,
        "records_imported": 0,
        "license_or_terms": "AccessGUDID device records are not bundled. FDA terms apply.",
        "metadata": {"required_env": []},
    },
    {
        "source_code": "MIMIC_IV",
        "source_name": "MIMIC-IV",
        "provider": "PhysioNet",
        "source_category": "clinical_dataset",
        "access_type": "local_credentialed",
        "requires_credentials": True,
        "enabled": False,
        "sync_status": SYNC_NOT_CONFIGURED,
        "records_imported": 0,
        "license_or_terms": (
            "MIMIC-IV requires PhysioNet credentialed access and a local copy. "
            "Raw patient rows are never stored as reference concepts and are never sent to OpenAI."
        ),
        "metadata": {"required_env": ["MIMIC_LOCAL_PATH"], "allows_raw_rows_in_openai": False},
    },
)


def seed_data_source_registry(session: Session) -> int:
    """Insert missing source-registry metadata rows. Existing rows are left unchanged.

    Returns the number of rows inserted. Does not insert clinical concepts.
    """
    before = session.scalar(select(func.count()).select_from(DataSourceRegistry)) or 0
    payload: list[dict[str, Any]] = []
    for row in SOURCE_REGISTRY_ROWS:
        item = dict(row)
        item["id"] = uuid.uuid4()
        item["metadata_json"] = item.pop("metadata")
        payload.append(item)
    statement = insert(DataSourceRegistry).values(payload)
    statement = statement.on_conflict_do_nothing(index_elements=["source_code"])
    session.execute(statement)
    after = session.scalar(select(func.count()).select_from(DataSourceRegistry)) or 0
    return int(after - before)


def get_data_source(session: Session, source_code: str) -> DataSourceRegistry | None:
    return session.scalar(
        select(DataSourceRegistry).where(DataSourceRegistry.source_code == source_code)
    )


def list_data_sources(session: Session) -> list[DataSourceRegistry]:
    rows = session.scalars(
        select(DataSourceRegistry).order_by(DataSourceRegistry.source_code)
    ).all()
    return list(rows)


def get_medication_by_rxcui(session: Session, rxcui: str) -> RefMedication | None:
    return session.scalar(select(RefMedication).where(RefMedication.rxcui == rxcui))


def get_lab_test_by_loinc(session: Session, loinc_code: str) -> RefLabTest | None:
    return session.scalar(select(RefLabTest).where(RefLabTest.loinc_code == loinc_code))


def get_unit_by_ucum(session: Session, ucum_code: str) -> RefUnit | None:
    return session.scalar(select(RefUnit).where(RefUnit.ucum_code == ucum_code))


def get_diagnosis_by_icd10cm(session: Session, icd10cm_code: str) -> RefDiagnosis | None:
    """Return an existing ICD-10-CM row. Prefer a row that does not also carry SNOMED."""
    return session.scalar(
        select(RefDiagnosis)
        .where(RefDiagnosis.icd10cm_code == icd10cm_code)
        .order_by(
            RefDiagnosis.snomed_code.is_not(None),
            RefDiagnosis.retrieved_at.desc().nulls_last(),
        )
        .limit(1)
    )


def get_symptom_by_name(session: Session, preferred_name: str) -> RefSymptom | None:
    return session.scalar(
        select(RefSymptom).where(RefSymptom.preferred_name == preferred_name).limit(1)
    )


def get_label_by_set_id(session: Session, set_id: str) -> RefDrugLabel | None:
    return session.scalar(select(RefDrugLabel).where(RefDrugLabel.set_id == set_id).limit(1))


def get_rule_by_code(session: Session, rule_code: str) -> ClinicalRule | None:
    return session.scalar(select(ClinicalRule).where(ClinicalRule.rule_code == rule_code))


def upsert_symptom(session: Session, values: dict[str, Any]) -> RefSymptom:
    name = str(values["preferred_name"])
    row = get_symptom_by_name(session, name)
    return _upsert_row(session, row, RefSymptom, values, identity_keys=("preferred_name",))


def upsert_drug_label(session: Session, values: dict[str, Any]) -> RefDrugLabel:
    set_id = str(values["set_id"])
    row = get_label_by_set_id(session, set_id)
    return _upsert_row(session, row, RefDrugLabel, values, identity_keys=("set_id",))


def upsert_rule(session: Session, values: dict[str, Any]) -> ClinicalRule:
    code = str(values["rule_code"])
    row = get_rule_by_code(session, code)
    return _upsert_row(session, row, ClinicalRule, values, identity_keys=("rule_code",))


def list_enabled_rules(session: Session) -> list[ClinicalRule]:
    rows = session.scalars(
        select(ClinicalRule).where(ClinicalRule.enabled.is_(True)).order_by(ClinicalRule.rule_code)
    ).all()
    return list(rows)


def list_medications(session: Session) -> list[RefMedication]:
    rows = session.scalars(select(RefMedication).order_by(RefMedication.rxcui)).all()
    return list(rows)


def list_diagnoses(session: Session) -> list[RefDiagnosis]:
    rows = session.scalars(
        select(RefDiagnosis).order_by(RefDiagnosis.icd10cm_code.nulls_last())
    ).all()
    return list(rows)


def list_lab_tests(session: Session) -> list[RefLabTest]:
    rows = session.scalars(select(RefLabTest).order_by(RefLabTest.loinc_code)).all()
    return list(rows)


def list_units(session: Session) -> list[RefUnit]:
    rows = session.scalars(select(RefUnit).order_by(RefUnit.ucum_code)).all()
    return list(rows)


def list_symptoms(session: Session) -> list[RefSymptom]:
    rows = session.scalars(
        select(RefSymptom).order_by(RefSymptom.preferred_name.nulls_last())
    ).all()
    return list(rows)


def upsert_medication(session: Session, values: dict[str, Any]) -> RefMedication:
    rxcui = str(values["rxcui"])
    row = get_medication_by_rxcui(session, rxcui)
    return _upsert_row(session, row, RefMedication, values, identity_keys=("rxcui",))


def upsert_lab_test(session: Session, values: dict[str, Any]) -> RefLabTest:
    loinc_code = str(values["loinc_code"])
    row = get_lab_test_by_loinc(session, loinc_code)
    return _upsert_row(session, row, RefLabTest, values, identity_keys=("loinc_code",))


def upsert_unit(session: Session, values: dict[str, Any]) -> RefUnit:
    ucum_code = str(values["ucum_code"])
    row = get_unit_by_ucum(session, ucum_code)
    return _upsert_row(session, row, RefUnit, values, identity_keys=("ucum_code",))


def upsert_diagnosis_icd10cm(session: Session, values: dict[str, Any]) -> RefDiagnosis:
    code = str(values["icd10cm_code"])
    row = get_diagnosis_by_icd10cm(session, code)
    return _upsert_row(session, row, RefDiagnosis, values, identity_keys=("icd10cm_code",))


def search_medications(
    session: Session, query: str, *, limit: int, offset: int
) -> tuple[list[RefMedication], int]:
    pattern = _ilike_pattern(query)
    filters: list[ColumnElement[bool]] = []
    if pattern is not None:
        filters.append(
            or_(
                RefMedication.rxcui.ilike(pattern, escape="\\"),
                RefMedication.concept_name.ilike(pattern, escape="\\"),
                RefMedication.generic_name.ilike(pattern, escape="\\"),
                RefMedication.brand_name.ilike(pattern, escape="\\"),
                RefMedication.ingredient.ilike(pattern, escape="\\"),
            )
        )
    stmt = select(RefMedication)
    if filters:
        stmt = stmt.where(*filters)
    total = _count(session, stmt)
    rows = session.scalars(
        stmt.order_by(
            RefMedication.concept_name.nulls_last(),
            RefMedication.rxcui,
        )
        .limit(limit)
        .offset(offset)
    ).all()
    return list(rows), total


def search_lab_tests(
    session: Session, query: str, *, limit: int, offset: int
) -> tuple[list[RefLabTest], int]:
    pattern = _ilike_pattern(query)
    filters: list[ColumnElement[bool]] = []
    if pattern is not None:
        filters.append(
            or_(
                RefLabTest.loinc_code.ilike(pattern, escape="\\"),
                RefLabTest.long_common_name.ilike(pattern, escape="\\"),
                RefLabTest.short_name.ilike(pattern, escape="\\"),
                RefLabTest.component.ilike(pattern, escape="\\"),
            )
        )
    stmt = select(RefLabTest)
    if filters:
        stmt = stmt.where(*filters)
    total = _count(session, stmt)
    rows = session.scalars(
        stmt.order_by(RefLabTest.long_common_name.nulls_last(), RefLabTest.loinc_code)
        .limit(limit)
        .offset(offset)
    ).all()
    return list(rows), total


def search_diagnoses(
    session: Session, query: str, *, limit: int, offset: int
) -> tuple[list[RefDiagnosis], int]:
    pattern = _ilike_pattern(query)
    filters: list[ColumnElement[bool]] = []
    if pattern is not None:
        filters.append(
            or_(
                RefDiagnosis.icd10cm_code.ilike(pattern, escape="\\"),
                RefDiagnosis.snomed_code.ilike(pattern, escape="\\"),
                RefDiagnosis.preferred_name.ilike(pattern, escape="\\"),
            )
        )
    stmt = select(RefDiagnosis)
    if filters:
        stmt = stmt.where(*filters)
    total = _count(session, stmt)
    rows = session.scalars(
        stmt.order_by(
            RefDiagnosis.preferred_name.nulls_last(),
            RefDiagnosis.icd10cm_code.nulls_last(),
        )
        .limit(limit)
        .offset(offset)
    ).all()
    return list(rows), total


def search_symptoms(
    session: Session, query: str, *, limit: int, offset: int
) -> tuple[list[RefSymptom], int]:
    pattern = _ilike_pattern(query)
    filters: list[ColumnElement[bool]] = []
    if pattern is not None:
        filters.append(
            or_(
                RefSymptom.snomed_code.ilike(pattern, escape="\\"),
                RefSymptom.preferred_name.ilike(pattern, escape="\\"),
                RefSymptom.body_system.ilike(pattern, escape="\\"),
                cast(RefSymptom.synonyms, String).ilike(pattern, escape="\\"),
            )
        )
    stmt = select(RefSymptom)
    if filters:
        stmt = stmt.where(*filters)
    total = _count(session, stmt)
    rows = session.scalars(
        stmt.order_by(RefSymptom.preferred_name.nulls_last(), RefSymptom.snomed_code.nulls_last())
        .limit(limit)
        .offset(offset)
    ).all()
    return list(rows), total


def mark_source_sync_success(
    session: Session,
    source_code: str,
    *,
    records_imported: int,
    source_version: str | None,
    retrieved_at: datetime,
) -> DataSourceRegistry | None:
    row = get_data_source(session, source_code)
    if row is None:
        return None
    row.last_sync_at = retrieved_at
    row.last_successful_sync_at = retrieved_at
    row.sync_status = "synced"
    row.records_imported = records_imported
    row.error_message = None
    row.enabled = True
    if source_version is not None:
        row.version = source_version
    session.flush()
    return row


def mark_source_sync_error(
    session: Session,
    source_code: str,
    *,
    message: str,
    retrieved_at: datetime,
    not_configured: bool = False,
) -> DataSourceRegistry | None:
    row = get_data_source(session, source_code)
    if row is None:
        return None
    row.last_sync_at = retrieved_at
    row.error_message = message
    if not_configured:
        row.sync_status = "not_configured"
        row.enabled = False
    else:
        row.sync_status = "error"
    session.flush()
    return row


def _upsert_row[TModel](
    session: Session,
    row: TModel | None,
    model: type[TModel],
    values: dict[str, Any],
    *,
    identity_keys: Sequence[str],
) -> TModel:
    if row is None:
        created = model(**values)
        session.add(created)
        session.flush()
        return created
    for key, value in values.items():
        if key in identity_keys or key == "id":
            continue
        setattr(row, key, value)
    session.flush()
    return row


def _count(session: Session, stmt: Select[Any]) -> int:
    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    return int(session.scalar(count_stmt) or 0)


def _ilike_pattern(query: str) -> str | None:
    text = query.strip()
    if text == "":
        return None
    escaped = text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"
