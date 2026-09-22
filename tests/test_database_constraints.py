"""Constraint tests against PostgreSQL. Fixture identifiers use the TEST_ prefix only."""

from __future__ import annotations

import uuid

import pytest
from app.models.cases import CaseMedication, CaseSymptom, ClinicalCase
from app.models.reference import (
    DataSourceRegistry,
    RefClinicalDistribution,
    RefDiagnosis,
    RefLabTest,
    RefMedication,
)
from app.repositories.reference import (
    SOURCE_REGISTRY_ROWS,
    seed_data_source_registry,
)
from sqlalchemy import inspect, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

EXPECTED_TABLES = frozenset(
    {
        "data_source_registry",
        "ref_medications",
        "ref_drug_labels",
        "ref_diagnoses",
        "ref_symptoms",
        "ref_lab_tests",
        "ref_units",
        "ref_vitals",
        "ref_procedures",
        "ref_devices",
        "ref_microbiology",
        "ref_clinical_distributions",
        "clinical_cases",
        "case_presentations",
        "case_symptoms",
        "case_social_supports",
        "case_diagnoses",
        "case_problem_list",
        "case_notes",
        "case_vitals",
        "case_labs",
        "case_microbiology",
        "case_weights",
        "case_intake_outputs",
        "case_imaging",
        "case_procedures",
        "case_devices",
        "case_consults",
        "case_medications",
        "case_medication_reconciliations",
        "case_monitoring",
        "case_therapy_restrictions",
        "case_discharge_planning",
        "case_followups",
        "case_instructions",
        "case_return_precautions",
        "case_answer_keys",
        "case_blueprints",
        "case_generation_runs",
        "case_medication_plans",
        "clinical_rules",
        "validation_batch_cases",
        "ref_medication_classes",
    }
)

CREDENTIALED_SOURCES = frozenset({"LOINC", "SNOMED_CT", "MIMIC_IV"})


def test_migration_creates_every_table(engine: Engine) -> None:
    names = set(inspect(engine).get_table_names())
    assert EXPECTED_TABLES <= names
    assert "alembic_version" in names


def test_source_registry_metadata_and_no_clinical_rows(db_session: Session) -> None:
    rows = list(db_session.scalars(select(DataSourceRegistry)).all())
    by_code = {row.source_code: row for row in rows}
    assert set(by_code) == {row["source_code"] for row in SOURCE_REGISTRY_ROWS}
    for row in rows:
        assert row.records_imported == 0
        assert row.error_message is None
        assert row.last_sync_at is None
        if row.source_code in CREDENTIALED_SOURCES:
            assert row.enabled is False
            assert row.sync_status == "not_configured"
            assert row.requires_credentials is True
        else:
            assert row.enabled is True
            assert row.sync_status == "never_synced"
            assert row.requires_credentials is False

    for table_name in EXPECTED_TABLES - {"data_source_registry"}:
        count = db_session.scalar(text(f"SELECT COUNT(*) FROM {table_name}"))
        assert count == 0


def test_source_registry_seed_is_idempotent(db_session: Session) -> None:
    inserted = seed_data_source_registry(db_session)
    db_session.commit()
    assert inserted == 0
    total = db_session.scalar(text("SELECT COUNT(*) FROM data_source_registry"))
    assert total == len(SOURCE_REGISTRY_ROWS)


def test_ref_medication_rejects_duplicate_rxcui(db_session: Session) -> None:
    db_session.add(RefMedication(rxcui="TEST_RX_1", concept_name="Test Medication"))
    db_session.commit()
    db_session.add(RefMedication(rxcui="TEST_RX_1", concept_name="Test Medication Duplicate"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    db_session.execute(text("DELETE FROM ref_medications WHERE rxcui = 'TEST_RX_1'"))
    db_session.commit()


def test_ref_lab_test_rejects_duplicate_loinc_code(db_session: Session) -> None:
    db_session.add(RefLabTest(loinc_code="TEST_LOINC_1", long_common_name="Test Lab"))
    db_session.commit()
    db_session.add(RefLabTest(loinc_code="TEST_LOINC_1", long_common_name="Test Lab Duplicate"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    db_session.execute(text("DELETE FROM ref_lab_tests WHERE loinc_code = 'TEST_LOINC_1'"))
    db_session.commit()


def test_case_child_requires_existing_case(db_session: Session) -> None:
    db_session.add(CaseSymptom(case_id=uuid.uuid4(), symptom="TEST_symptom"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_ref_diagnosis_requires_snomed_or_icd(db_session: Session) -> None:
    db_session.add(RefDiagnosis(preferred_name="TEST_diagnosis_without_code"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_distribution_unique_index_treats_nulls_as_equal(db_session: Session) -> None:
    payload = {
        "source_dataset": "TEST_DS",
        "clinical_context": "TEST_CTX",
        "variable_code": "TEST_VAR",
        "age_min": None,
        "age_max": None,
        "sex": None,
        "care_setting": None,
        "timepoint": None,
    }
    db_session.add(RefClinicalDistribution(**payload))
    db_session.commit()
    db_session.add(RefClinicalDistribution(**payload))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    db_session.execute(
        text(
            "DELETE FROM ref_clinical_distributions "
            "WHERE source_dataset = 'TEST_DS' AND variable_code = 'TEST_VAR'"
        )
    )
    db_session.commit()


def test_distribution_rejects_raw_mimic_marker(db_session: Session) -> None:
    db_session.add(
        RefClinicalDistribution(
            source_dataset="MIMIC_IV_RAW",
            clinical_context="TEST_CTX",
            variable_code="TEST_VAR_RAW",
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_case_medication_context_is_constrained(db_session: Session) -> None:
    case = ClinicalCase(case_id_code="TEST_CASE_1")
    db_session.add(case)
    db_session.commit()
    db_session.add(CaseMedication(case_id=case.id, context="TEST_bad_context"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    db_session.execute(text("DELETE FROM clinical_cases WHERE case_id_code = 'TEST_CASE_1'"))
    db_session.commit()
