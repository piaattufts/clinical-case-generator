"""Frozen VAL-* batch, blinded export, and immutability tests. HTTP is mocked."""

from __future__ import annotations

import json
from pathlib import Path

from app.models.cases import ClinicalCase
from app.models.generation import ValidationBatchCase
from app.repositories.cases import get_frozen_case_by_validation_id, list_answer_keys_for_case
from app.services.generation import generate_one_case
from app.services.validation_batch import (
    DATASET_STATUS,
    export_validation_batch,
)
from app.sources.exceptions import FrozenValidationCaseError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tests.test_generation_pipeline import _seed_generation_refs, _test_scenario


def _write_plan(path: Path, *, inject: bool, category: str | None, sequence: int) -> Path:
    path.write_text(
        json.dumps(
            {
                "batch_code": "TEST_BATCH",
                "master_seed": 9,
                "cases": [
                    {
                        "validation_case_id": "VAL-001",
                        "scenario": "TEST_HF",
                        "inject_error": inject,
                        "error_category": category,
                        "sequence": sequence,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_freeze_is_immutable_and_export_is_blinded(db_session: Session, tmp_path: Path) -> None:
    _seed_generation_refs(db_session)
    plan = _write_plan(tmp_path / "plan.json", inject=True, category="omission", sequence=21)
    # Patch load_scenarios by writing through generate_one_case first so the case exists,
    # then freeze using a plan that points at an already generated sequence after we
    # intercept unknown scenario by generating with the test scenario directly.
    generated = generate_one_case(
        db_session,
        sequence=21,
        seed=9,
        scenario=_test_scenario(),
        inject_error=True,
        use_openai=False,
        error_category="omission",
    )
    case = db_session.get(ClinicalCase, generated.case_id)
    assert case is not None
    frozen = ValidationBatchCase(
        validation_case_id="VAL-001",
        batch_code="TEST_BATCH",
        case_id=case.id,
        scenario_code="TEST_HF",
        master_seed=9,
        case_seed=generated.seed,
        is_clean_control=False,
        error_category="omission",
        generator_version="0.1.0",
        reference_snapshot={},
        rule_snapshot=[],
        clean_validation=generated.clean_validation,
        final_validation=generated.validation,
        clean_state=generated.clean_state,
        resident_state=None,
        answer_key_payload=None,
        immutable=True,
    )
    db_session.add(frozen)
    db_session.flush()
    again = get_frozen_case_by_validation_id(db_session, "VAL-001")
    assert again is not None
    assert again.immutable is True
    try:
        generate_one_case(
            db_session,
            sequence=21,
            seed=9,
            scenario=_test_scenario(),
            inject_error=True,
            use_openai=False,
        )
        raised = False
    except FrozenValidationCaseError:
        raised = True
    assert raised is True
    from app.services.validation_batch import _investigator_payload, _resident_payload

    resident = _resident_payload(db_session, case, frozen)
    investigator = _investigator_payload(db_session, case, frozen)
    blob = json.dumps(resident).casefold()
    assert "val-001" in blob
    assert "caseanswerkey" not in blob
    assert "omission" not in blob
    assert "is_clean_control" not in blob
    assert "rxcui:" not in blob
    assert "random_seed" not in blob
    assert investigator["control_error_status"] == "error_bearing"
    assert investigator["error"]["error_category"] == "omission"
    assert DATASET_STATUS in investigator["dataset_status"]
    keys = list_answer_keys_for_case(db_session, case.id)
    assert len(keys) == 1
    export_dir = tmp_path / "out"
    exported = export_validation_batch(
        db_session,
        batch_code="TEST_BATCH",
        output_dir=export_dir,
        allow_test_identifiers=True,
    )
    assert exported.resident_path.exists()
    resident_doc = json.loads(exported.resident_path.read_text(encoding="utf-8"))
    assert "CaseAnswerKey" not in json.dumps(resident_doc)
    key_doc = json.loads(exported.investigator_path.read_text(encoding="utf-8"))
    assert key_doc["cases"][0]["validation_case_id"] == "VAL-001"
    _ = plan


def test_clean_control_answer_key_states_no_intentional_error(
    db_session: Session, tmp_path: Path
) -> None:
    _seed_generation_refs(db_session)
    generated = generate_one_case(
        db_session,
        sequence=22,
        seed=9,
        scenario=_test_scenario(),
        inject_error=False,
        use_openai=False,
    )
    case = db_session.get(ClinicalCase, generated.case_id)
    assert case is not None
    frozen = ValidationBatchCase(
        validation_case_id="VAL-002",
        batch_code="TEST_CLEAN",
        case_id=case.id,
        scenario_code="TEST_HF",
        master_seed=9,
        case_seed=generated.seed,
        is_clean_control=True,
        error_category=None,
        generator_version="0.1.0",
        clean_validation=generated.clean_validation,
        final_validation=generated.validation,
        clean_state=generated.clean_state,
        immutable=True,
    )
    db_session.add(frozen)
    db_session.flush()
    from app.services.validation_batch import _investigator_payload, _resident_payload

    investigator = _investigator_payload(db_session, case, frozen)
    assert investigator["control_error_status"] == "NO INTENTIONAL ERROR"
    resident = _resident_payload(db_session, case, frozen)
    assert "NO INTENTIONAL ERROR" not in json.dumps(resident)
    assert int(db_session.scalar(select(func.count()).select_from(ValidationBatchCase)) or 0) >= 1
    _ = tmp_path
