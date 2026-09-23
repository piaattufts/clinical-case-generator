"""Clean-case uniqueness, near-duplicate detection, and balanced batch-plan tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from app.models.cases import ClinicalCase
from app.models.reference import RefMedication
from app.services.bootstrap import _prefer_medication_row
from app.services.case_diversity import (
    NEAR_DUPLICATE_REJECT,
    NEAR_DUPLICATE_WARN,
    CleanCaseFingerprint,
    fingerprint_from_mapping,
    require_unique_clean_cases,
    similarity,
)
from app.services.generation import ClinicalProfile, generate_one_case, load_scenarios
from app.services.validation_batch import (
    freeze_validation_batch,
    load_batch_plan,
    parse_assignments,
)
from app.sources.exceptions import CaseValidationError, DuplicateClinicalCaseError
from app.utils.provenance import build_provenance
from sqlalchemy.orm import Session

from tests.test_generation_pipeline import _seed_generation_refs, _test_scenario

REPO = Path(__file__).resolve().parents[1]
V2_PLAN = REPO / "data" / "validation_balanced" / "batch_plan.json"
EXPECTED_V1_HASHES = {
    "batch_plan.json": "2a34f26326655c9c786263d32bcf87cbb99b9a90a9171fbd34758a62281f955d",
    "resident_validation_cases.json": (
        "90227220afcc2398c969f36a1cc27bc11a4a04de39c6a93b495cca649b2cfdec"
    ),
    "investigator_answer_key.json": (
        "6d82319ba48d1dfea6b0fe6fd6fd1d07f5fe970f907e44968193cc5aaa2ea07d"
    ),
    "investigator_answer_key.md": (
        "425cb79d7ace8c4c379ed5f1cdfeaf957c25c0f4d9e3a4960347885d11e81e0b"
    ),
    "validation_manifest.json": (
        "1b6a87d3c48bc31896ac5ac2629fa1ac68118504384bef36994940623f02feba"
    ),
    "coverage_report.md": "d399eb61010ba7c1643ae3dd0ec911c1aaecf360061fad40be2f3aa9f4bf15d2",
    "scenario_coverage_matrix.md": (
        "9a24b908d7d953e0d50770f75c6890db0b5015405a0c7c5a1ea6132cab7c7582"
    ),
    "resident_review_worksheet.csv": (
        "8178c07c5e85fd66d845472f498297c6a3f97c1dfda426efa706b3680ba694c1"
    ),
    "resident_review_schema.json": (
        "118edb2a716988aa2891c30c512af931d54957a49e6f77989542299bd40fc6c7"
    ),
}


def _fp(**overrides: Any) -> CleanCaseFingerprint:
    payload: dict[str, Any] = {
        "scenario": "HF_INPATIENT",
        "clinical_profile": "HF_VOLUME_OVERLOAD",
        "specialty": "cardiology",
        "diagnosis_codes": ["Heart failure"],
        "symptoms": ["dyspnea", "edema", "orthopnea"],
        "home_medications": ["RXCUI:1", "RXCUI:2", "RXCUI:3"],
        "inpatient_medications": ["RXCUI:1", "RXCUI:2", "RXCUI:3"],
        "lab_concepts": ["LOINC:K", "LOINC:CR"],
        "monitoring": [],
        "hospital_course_pattern": "multi_day_diuresis|several days|worsening",
        "followup": ["cardiology|Heart-failure clinic follow-up|7 days"],
        "disposition": "home|no_home_health",
    }
    payload.update(overrides)
    return fingerprint_from_mapping(payload)


def test_exact_duplicate_fingerprints_raise() -> None:
    left = _fp()
    right = _fp()
    assert left.digest() == right.digest()
    with pytest.raises(DuplicateClinicalCaseError, match="VAL-A and VAL-B"):
        require_unique_clean_cases([("VAL-A", left), ("VAL-B", right)])


def test_demographics_seed_and_error_do_not_create_uniqueness() -> None:
    clinical = {
        "scenario": "HF_INPATIENT",
        "clinical_profile": "HF_VOLUME_OVERLOAD",
        "specialty": "cardiology",
        "diagnosis_codes": ["Heart failure"],
        "symptoms": ["dyspnea", "edema"],
        "home_medications": ["RXCUI:furosemide", "RXCUI:lisinopril"],
        "inpatient_medications": ["RXCUI:furosemide", "RXCUI:lisinopril"],
        "lab_concepts": ["LOINC:K"],
        "monitoring": [],
        "hospital_course_pattern": "multi_day_diuresis|several days|worsening",
        "followup": ["cardiology|Heart-failure clinic follow-up|7 days"],
        "disposition": "home|no_home_health",
    }
    left = fingerprint_from_mapping(
        {
            **clinical,
            "age": 58,
            "sex": "Female",
            "seed": "1:1:HF_INPATIENT",
            "error_category": "f1_omission",
            "lab_values": [4.1],
            "vitals": {"hr": 98},
        }
    )
    right = fingerprint_from_mapping(
        {
            **clinical,
            "age": 81,
            "sex": "Male",
            "seed": "99:2:HF_INPATIENT",
            "error_category": "f2_monitoring_not_arranged",
            "lab_values": [3.3],
            "vitals": {"hr": 72},
        }
    )
    assert left.digest() == right.digest()
    assert similarity(left, right) == 1.0


def test_near_duplicate_is_rejected_above_threshold() -> None:
    left = _fp()
    right = _fp(followup=["primary care|Primary care follow-up|7 days"])
    score = similarity(left, right)
    assert score >= NEAR_DUPLICATE_REJECT
    with pytest.raises(Exception, match="near-duplicate"):
        require_unique_clean_cases([("VAL-A", left), ("VAL-B", right)])


def test_warning_band_is_reported_but_not_rejected() -> None:
    left = _fp()
    right = _fp(
        hospital_course_pattern="improving_after_treatment|one week|improving after treatment",
        followup=["cardiology|Heart-failure follow-up after diuresis|14 days"],
    )
    score = similarity(left, right)
    audit = require_unique_clean_cases([("VAL-A", left), ("VAL-B", right)])
    assert audit.duplicates == []
    assert audit.rejected_pairs == []
    assert NEAR_DUPLICATE_WARN <= score < NEAR_DUPLICATE_REJECT
    assert audit.warnings


def test_genuinely_distinct_cases_are_not_near_duplicates() -> None:
    left = _fp()
    right = _fp(
        scenario="CAP_INPATIENT",
        clinical_profile="CAP_TYPICAL_COUGH",
        specialty="pulmonology",
        diagnosis_codes=["Pneumonia"],
        symptoms=["cough"],
        home_medications=["RXCUI:azithromycin"],
        inpatient_medications=["RXCUI:azithromycin"],
        lab_concepts=["LOINC:NA"],
        hospital_course_pattern="antibiotic_course_inpatient|several days|persistent",
        followup=["pulmonology|Pneumonia follow-up|7 days"],
    )
    audit = require_unique_clean_cases([("VAL-A", left), ("VAL-B", right)])
    assert similarity(left, right) < NEAR_DUPLICATE_WARN
    assert audit.warnings == []
    assert audit.rejected_pairs == []


def test_same_profile_different_seed_is_duplicate(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    first = generate_one_case(
        db_session,
        sequence=31,
        seed=1,
        scenario=scenario,
        inject_error=False,
        use_openai=False,
    )
    second = generate_one_case(
        db_session,
        sequence=32,
        seed=99,
        scenario=scenario,
        inject_error=True,
        use_openai=False,
        error_category="f1_omission",
    )
    assert first.fingerprint is not None
    assert second.fingerprint is not None
    assert first.seed != second.seed
    case_a = db_session.get(ClinicalCase, first.case_id)
    case_b = db_session.get(ClinicalCase, second.case_id)
    assert case_a is not None and case_b is not None
    assert (case_a.patient_age, case_a.patient_gender) != (
        case_b.patient_age,
        case_b.patient_gender,
    ) or first.seed != second.seed
    with pytest.raises(DuplicateClinicalCaseError):
        require_unique_clean_cases(
            [("VAL-A", first.fingerprint), ("VAL-B", second.fingerprint)]
        )


def test_distinct_profiles_are_not_duplicates(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.profiles = [
        ClinicalProfile(
            code="PROFILE_A",
            symptom_queries=["TEST_symptom"],
            medication_required_queries=["TEST_med"],
            lab_queries=["TEST_lab"],
            hospital_course_pattern="day1_io_ready_home",
            followup_item="Primary care follow-up",
            followup_service="primary care",
            followup_timing="7 days",
        ),
        ClinicalProfile(
            code="PROFILE_B",
            symptom_queries=["TEST_symptom"],
            medication_required_queries=["TEST_ibuprofen"],
            lab_queries=["TEST_lab"],
            hospital_course_pattern="improving_after_treatment",
            followup_item="Cardiology follow-up",
            followup_service="cardiology",
            followup_timing="14 days",
            io_timepoint="hospital_day_3",
        ),
    ]
    first = generate_one_case(
        db_session,
        sequence=41,
        seed=7,
        scenario=scenario,
        inject_error=False,
        use_openai=False,
        profile_code="PROFILE_A",
    )
    second = generate_one_case(
        db_session,
        sequence=42,
        seed=7,
        scenario=scenario,
        inject_error=False,
        use_openai=False,
        profile_code="PROFILE_B",
    )
    assert first.fingerprint is not None and second.fingerprint is not None
    require_unique_clean_cases(
        [("VAL-A", first.fingerprint), ("VAL-B", second.fingerprint)]
    )
    assert first.fingerprint.digest() != second.fingerprint.digest()
    assert first.clinical_profile == "PROFILE_A"
    assert second.clinical_profile == "PROFILE_B"


def test_generation_is_reproducible_with_the_same_seed(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    first = generate_one_case(
        db_session, sequence=51, seed=8, scenario=scenario, inject_error=False, use_openai=False
    )
    digest = None if first.fingerprint is None else first.fingerprint.digest()
    second = generate_one_case(
        db_session, sequence=51, seed=8, scenario=scenario, inject_error=False, use_openai=False
    )
    assert second.fingerprint is not None
    assert second.fingerprint.digest() == digest
    assert second.seed == first.seed


def test_balanced_v2_plan_has_unique_profiles_and_families() -> None:
    plan = load_batch_plan(V2_PLAN)
    assignments = parse_assignments(plan)
    assert plan["batch_code"] == "CLINIPROOF_BALANCED_V2"
    assert len(assignments) == 24
    families = {item.scenario: 0 for item in assignments}
    for item in assignments:
        families[item.scenario] += 1
    assert families["HF_INPATIENT"] == 5
    assert families["AF_ANTICOAGULATION"] == 5
    assert families["HTN_INPATIENT"] == 5
    assert families["T2DM_INPATIENT"] == 5
    assert families["CAP_INPATIENT"] == 4
    profiles = [item.clinical_profile for item in assignments]
    assert None not in profiles
    assert len(set(profiles)) == 24
    controls = [item for item in assignments if not item.inject_error]
    assert len(controls) == 4
    categories = [item.error_category for item in assignments if item.inject_error]
    assert len(set(categories)) >= 10
    assert all(item.sequence >= 1001 for item in assignments)


def test_clinical_profiles_are_defined_for_each_family() -> None:
    scenarios = {item.code: item for item in load_scenarios()}
    assert set(scenarios) == {
        "HF_INPATIENT",
        "AF_ANTICOAGULATION",
        "HTN_INPATIENT",
        "T2DM_INPATIENT",
        "CAP_INPATIENT",
    }
    profile_codes = [profile.code for item in scenarios.values() for profile in item.profiles]
    assert len(profile_codes) == 24
    assert len(set(profile_codes)) == 24


def test_concentrated_plan_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "plan.json"
    cases = []
    for index in range(12):
        cases.append(
            {
                "validation_case_id": f"VAL-{index + 1:03d}",
                "scenario": "HF_INPATIENT",
                "clinical_profile": f"P{index}",
                "inject_error": False,
                "error_family": "none",
                "error_category": None,
                "sequence": 1100 + index,
            }
        )
    path.write_text(
        json.dumps(
            {
                "batch_code": "TEST_CONCENTRATED",
                "master_seed": 1,
                "require_balanced_scenarios": True,
                "cases": cases,
            }
        ),
        encoding="utf-8",
    )
    from app.services.validation_batch import _assert_scenario_balance

    plan = json.loads(path.read_text(encoding="utf-8"))
    with pytest.raises(CaseValidationError, match="batch_balance"):
        _assert_scenario_balance(plan, parse_assignments(plan))


def test_frozen_v1_files_were_not_altered() -> None:
    root = REPO / "data" / "validation"
    for name, expected in EXPECTED_V1_HASHES.items():
        digest = hashlib.sha256((root / name).read_bytes()).hexdigest()
        assert digest == expected, name


def test_tablet_formulation_outranks_oral_solution() -> None:
    rx = build_provenance("RXNORM", "TEST_FORM")
    solution = RefMedication(
        rxcui="100",
        concept_name="lisinopril Oral Solution",
        generic_name="lisinopril",
        ingredient="lisinopril",
        dose_form="Oral Solution",
        term_type="SCD",
        **rx,
    )
    tablet = RefMedication(
        rxcui="200",
        concept_name="lisinopril Oral Tablet",
        generic_name="lisinopril",
        ingredient="lisinopril",
        dose_form="Oral Tablet",
        term_type="SCD",
        **rx,
    )
    chosen = _prefer_medication_row([solution, tablet], "lisinopril")
    assert chosen is not None
    assert chosen.rxcui == "200"


def test_freeze_rejects_duplicate_clean_cases(
    db_session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.anticoagulant_mutex_queries = []
    monkeypatch.setattr("app.services.validation_batch.load_scenarios", lambda: [scenario])
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps(
            {
                "batch_code": "TEST_DUP",
                "master_seed": 11,
                "cases": [
                    {
                        "validation_case_id": "VAL-111",
                        "scenario": scenario.code,
                        "inject_error": False,
                        "error_family": "none",
                        "error_category": None,
                        "sequence": 81,
                    },
                    {
                        "validation_case_id": "VAL-112",
                        "scenario": scenario.code,
                        "inject_error": True,
                        "error_family": "family_1",
                        "error_category": "f1_omission",
                        "sequence": 82,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(DuplicateClinicalCaseError):
        freeze_validation_batch(
            db_session, plan_path=plan, use_openai=False, allow_test_identifiers=True
        )
