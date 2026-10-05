"""Clean resident cases keep the discharge regimen hidden."""

from __future__ import annotations

from app.models.cases import ClinicalCase
from app.repositories.cases import list_answer_keys_for_case
from app.services.generation import DEFAULT_INJECT_ERROR, generate_one_case
from app.services.resident_case import (
    audit_active_validation_cases,
    evaluator_case_document,
    reference_discharge_plan,
    resident_case_document,
)
from app.services.validation import require_valid, validate_case
from sqlalchemy.orm import Session

from tests.test_generation_pipeline import _seed_generation_refs, _test_scenario


def test_clean_case_has_no_injected_error_and_hides_the_reference(db_session: Session) -> None:
    assert DEFAULT_INJECT_ERROR is False
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    first = generate_one_case(
        db_session,
        sequence=81,
        seed=11,
        scenario=scenario,
        use_openai=False,
    )
    assert first.injected is None
    case = db_session.get(ClinicalCase, first.case_id)
    assert case is not None
    assert list_answer_keys_for_case(db_session, case.id) == []
    report = validate_case(db_session, case, expect_injected_error=False)
    require_valid(report)

    resident = resident_case_document(db_session, case)
    reference = reference_discharge_plan(db_session, case)
    evaluator = evaluator_case_document(db_session, case)

    assert resident["medications"]
    assert all(item["context"] != "discharge" for item in resident["medications"])
    assert "reference_discharge_plan" not in resident
    assert reference["medications"]
    assert {item["action"] for item in reference["medications"]} <= {
        "continue",
        "start",
        "stop",
        "change",
    }
    assert evaluator["reference_discharge_plan"] == reference
    assert evaluator["medications"] == resident["medications"]

    again = generate_one_case(
        db_session,
        sequence=81,
        seed=11,
        scenario=scenario,
        use_openai=False,
    )
    again_case = db_session.get(ClinicalCase, again.case_id)
    assert again_case is not None
    assert reference_discharge_plan(db_session, again_case) == reference
    assert again.injected is None


def test_normal_generation_does_not_emit_an_error_bearing_twin(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    results = [
        generate_one_case(
            db_session,
            sequence=82,
            seed=12,
            scenario=_test_scenario(),
            use_openai=False,
        )
    ]
    assert len(results) == 1
    assert results[0].injected is None


def test_active_exports_still_need_regeneration() -> None:
    audit = audit_active_validation_cases()
    assert audit["needs_regeneration"] == 48
    assert audit["counts"]["CONTAINS_INJECTED_ERROR"] == 40
    assert audit["counts"]["REFERENCE_LEAKAGE"] == 8
    assert audit["counts"].get("CLEAN_AND_USABLE", 0) == 0
