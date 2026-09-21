"""Lookups for reference tables. No clinical concepts are inserted except source metadata."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.reference import DataSourceRegistry, RefLabTest, RefMedication, RefUnit

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
        "license_or_terms": (
            "LOINC requires a Regenstrief account. LOINC content is not bundled."
        ),
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
