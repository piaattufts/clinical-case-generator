"""CliniProof taxonomy eligibility, injection, isolation, and no-fallback tests."""

from __future__ import annotations

import inspect
import json
import random
from pathlib import Path
from typing import Any

import pytest
from app.models.cases import ClinicalCase
from app.models.generation import ValidationBatchCase
from app.models.reference import ClinicalRule, RefLabTest, RefMedication, RefMedicationClass
from app.repositories.cases import (
    list_answer_keys_for_case,
    list_followups_for_case,
    list_instructions_for_case,
    list_medications_for_case,
    list_monitoring_for_case,
    list_plans_for_case,
)
from app.services.error_injection import inject_reconciliation_error
from app.services.error_taxonomy import (
    F1_COMMISSION,
    F1_DOSE,
    F1_FREQUENCY,
    F1_OMISSION,
    F1_ROUTE,
    F1_SUBSTITUTION,
    F2_COPRESCRIPTION,
    F2_HELD_RESTART,
    F2_HOSPITAL_ONLY,
    F2_INPATIENT_SUB,
    F2_MONITORING,
    F2_PENDING_FOLLOWUP,
    F2_SUPPLY,
    FAMILY_FOR_CATEGORY,
    IMPLEMENTABLE_CATEGORIES,
    NONE,
    canonicalize_category,
    canonicalize_family,
    class_usable_for_substitution,
    detect_findings,
    eligible_errors,
)
from app.services.generation import GeneratedCaseResult, Scenario, generate_one_case
from app.services.validation import require_valid, validate_case
from app.services.validation_batch import (
    DEFAULT_BATCH_CODE,
    LEAK_MARKERS,
    _investigator_payload,
    _resident_payload,
    freeze_validation_batch,
)
from app.sources.exceptions import CaseValidationError, ReferenceResolutionError
from app.utils.provenance import build_provenance
from sqlalchemy.orm import Session

from tests.source_fixtures import TEST_RXCUI, TEST_RXCUI_IBU, TEST_RXCUI_WARFARIN
from tests.test_generation_pipeline import _seed_generation_refs, _test_scenario

TEST_RXCUI_ALT = "TEST_RXCUI_ALT"
TEST_RXCUI_HOSP = "TEST_RXCUI_HOSP"
TEST_LOINC_INR = "TEST_LOINC_INR"
TEST_CLASS_BETA = "TEST_CLASS_BETA"


def _collect_test_identifiers(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, str) and value.startswith("TEST_"):
        found.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(_collect_test_identifiers(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_collect_test_identifiers(item))
    return found


def _seed_taxonomy_refs(session: Session) -> None:
    _seed_generation_refs(session)
    rx = build_provenance("RXNORM", "TEST_RXNORM_VERSION")
    loinc = build_provenance("LOINC", "TEST_LOINC_VERSION")
    rxclass = build_provenance("RXCLASS")
    session.add(
        RefMedication(
            rxcui=TEST_RXCUI_ALT,
            concept_name="TEST_alt branded product",
            generic_name="TEST_alt",
            ingredient="TEST_alt",
            strength="5 mg",
            route="oral",
            **rx,
        )
    )
    session.add(
        RefMedication(
            rxcui=TEST_RXCUI_HOSP,
            concept_name="TEST_hosp branded product",
            generic_name="TEST_hosp",
            ingredient="TEST_hosp",
            strength="40 mg",
            route="oral",
            **rx,
        )
    )
    session.add(
        RefLabTest(
            loinc_code=TEST_LOINC_INR,
            long_common_name="TEST_INR in Platelet poor plasma",
            component="TEST_INR",
            example_ucum_units=["{INR}"],
            **loinc,
        )
    )
    session.add(
        RefMedicationClass(
            rxcui=TEST_RXCUI,
            class_id=TEST_CLASS_BETA,
            class_name="TEST beta blockers",
            class_type="ATC1-4",
            rela="has_ATC",
            **rxclass,
        )
    )
    session.add(
        RefMedicationClass(
            rxcui=TEST_RXCUI_ALT,
            class_id=TEST_CLASS_BETA,
            class_name="TEST beta blockers",
            class_type="ATC1-4",
            rela="has_ATC",
            **rxclass,
        )
    )
    session.add(
        ClinicalRule(
            rule_code="TEST_WARFARIN_INR",
            rule_type="monitoring_dependency",
            severity="hard",
            enabled=True,
            input_rxcui=TEST_RXCUI_WARFARIN,
            input_loinc_code=TEST_LOINC_INR,
            constraint_json={"action": "require_lab"},
            source_identifier="TEST_SET_1",
            **build_provenance("DAILYMED"),
        )
    )
    session.flush()


def _scenario() -> Scenario:
    scenario = _test_scenario()
    scenario.medication_queries = ["TEST_med"]
    scenario.stop_medication_queries = ["ibuprofen"]
    scenario.hospital_only_medication_queries = ["TEST_hosp"]
    scenario.lab_queries = ["TEST_lab", "TEST_INR"]
    scenario.anticoagulant_mutex_queries = ["warfarin"]
    return scenario


def _generate(
    session: Session, sequence: int, category: str | None, inject: bool = True
) -> GeneratedCaseResult:
    return generate_one_case(
        session,
        sequence=sequence,
        seed=11,
        scenario=_scenario(),
        inject_error=inject,
        use_openai=False,
        error_category=category,
    )


def _payloads(
    session: Session, result: GeneratedCaseResult, category: str | None
) -> tuple[ClinicalCase, dict[str, Any], dict[str, Any]]:
    case = session.get(ClinicalCase, result.case_id)
    assert case is not None
    val_id = f"VAL-{int(result.case_id_code.rsplit('-', 1)[-1]):03d}"
    canonical = NONE if category in {None, NONE} else canonicalize_category(category)
    frozen = ValidationBatchCase(
        validation_case_id=val_id,
        batch_code="TEST_TAXONOMY",
        case_id=case.id,
        scenario_code="TEST_HF",
        master_seed=11,
        case_seed=result.seed,
        is_clean_control=canonical == NONE,
        error_family=FAMILY_FOR_CATEGORY[canonical],
        error_category=canonical,
        generator_version="0.1.0",
        clean_validation=result.clean_validation,
        final_validation=result.validation,
        clean_state=result.clean_state,
        immutable=True,
    )
    session.add(frozen)
    session.flush()
    return (
        case,
        _resident_payload(session, case, frozen),
        _investigator_payload(session, case, frozen),
    )


def test_obsolete_identifiers_are_rejected_not_translated() -> None:
    for obsolete in (
        "omission",
        "dose_mismatch",
        "frequency_mismatch",
        "incorrect_continuation",
        "commission",
        "route_mismatch",
        "medication_reconciliation",
    ):
        with pytest.raises(CaseValidationError, match="unknown error category"):
            canonicalize_category(obsolete)
    with pytest.raises(CaseValidationError, match="unknown error family"):
        canonicalize_family("medication_reconciliation")
    assert canonicalize_category(F1_OMISSION) == F1_OMISSION
    assert canonicalize_family("family_1", category=F1_OMISSION) == "family_1"


def test_unknown_category_is_rejected_not_replaced(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    with pytest.raises(CaseValidationError, match="unknown error category"):
        _generate(db_session, 40, "not_a_real_error")


def test_coprescription_is_not_yet_implementable(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    with pytest.raises(CaseValidationError, match="not_yet_implementable"):
        _generate(db_session, 41, F2_COPRESCRIPTION)


def test_ineligible_commission_does_not_fallback(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    scenario = _scenario()
    scenario.stop_medication_queries = []
    with pytest.raises((CaseValidationError, ReferenceResolutionError)):
        generate_one_case(
            db_session,
            sequence=42,
            seed=11,
            scenario=scenario,
            inject_error=True,
            use_openai=False,
            error_category=F1_COMMISSION,
        )


def test_clean_control(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _generate(db_session, 43, None, inject=False)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    assert case.clean_case is True
    assert result.injected is None
    assert detect_findings(db_session, case) == []
    assert NONE in eligible_errors(db_session, case)
    keys = list_answer_keys_for_case(db_session, case.id)
    assert keys == []
    report = validate_case(db_session, case, expect_injected_error=False, expected_category=NONE)
    require_valid(report)
    case, resident, investigator = _payloads(db_session, result, None)
    blob = json.dumps(resident).casefold()
    assert "f1_" not in blob
    assert "answer_key" not in blob
    assert investigator["error"]["error_category"] == NONE


def _assert_category_case(session: Session, sequence: int, category: str) -> GeneratedCaseResult:
    first = _generate(session, sequence, category)
    assert first.injected is not None
    assert first.injected.category == category
    case = session.get(ClinicalCase, first.case_id)
    assert case is not None
    keys = list_answer_keys_for_case(session, case.id)
    assert len(keys) == 1
    assert keys[0].error_category == category
    assert keys[0].error_family is not None
    assert keys[0].is_primary_error is True
    assert keys[0].correct_action
    assert keys[0].intentional_changes
    change = keys[0].intentional_changes[0]
    assert change["error_category"] == category
    assert "clean_expected_state" in change
    assert "injected_state" in change
    findings = detect_findings(session, case)
    assert [item.category for item in findings] == [category]
    report = validate_case(session, case, expect_injected_error=True, expected_category=category)
    require_valid(report)
    second = _generate(session, sequence, category)
    assert second.injected is not None
    assert second.injected.category == category
    assert second.injected.rxcui == first.injected.rxcui
    _, resident, investigator = _payloads(session, second, category)
    blob = json.dumps(resident).casefold()
    assert category not in blob
    assert "answer_key" not in blob
    assert "error_family" not in blob
    error = investigator["error"]
    assert error["error_category"] == category
    assert error["error_family"] == FAMILY_FOR_CATEGORY[category]
    assert error["correct_action"]
    assert error["clean_expected_state"] is not None
    assert error["trigger_meds"]
    assert error["detectability_location"]
    assert error["changed_field"]
    assert error["evidence_required"]
    assert error["evidence_location"]
    assert error["intentional_changes"]
    return second


def test_f1_omission_injection(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 44, F1_OMISSION)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    home = [
        item for item in list_medications_for_case(db_session, case.id) if item.context == "home"
    ]
    discharge = [
        item
        for item in list_medications_for_case(db_session, case.id)
        if item.context == "discharge" and item.status != "held"
    ]
    assert len(home) > len(discharge)


def test_f1_commission_injection(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 45, F1_COMMISSION)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    assert any(
        linked.rxcui == TEST_RXCUI_IBU
        for item in list_medications_for_case(db_session, case.id)
        if item.context == "discharge" and item.ref_medication_id is not None
        for linked in [db_session.get(RefMedication, item.ref_medication_id)]
        if linked is not None
    )


def test_f1_dose_route_frequency(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    dose = _assert_category_case(db_session, 46, F1_DOSE)
    _assert_category_case(db_session, 47, F1_ROUTE)
    _assert_category_case(db_session, 48, F1_FREQUENCY)
    case = db_session.get(ClinicalCase, dose.case_id)
    assert case is not None
    home_by = {
        item.ref_medication_id: item
        for item in list_medications_for_case(db_session, case.id)
        if item.context == "home"
    }
    changed = 0
    for item in list_medications_for_case(db_session, case.id):
        if item.context != "discharge" or item.ref_medication_id not in home_by:
            continue
        home = home_by[item.ref_medication_id]
        if (home.dose or "") != (item.dose or ""):
            changed += 1
            assert (home.route or "") == (item.route or "")
            assert (home.frequency or "") == (item.frequency or "")
    assert changed == 1


def test_f1_therapeutic_substitution(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 49, F1_SUBSTITUTION)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    discharge_rxcuis = set()
    home_rxcuis = set()
    for item in list_medications_for_case(db_session, case.id):
        if item.ref_medication_id is None:
            continue
        row = db_session.get(RefMedication, item.ref_medication_id)
        if row is None:
            continue
        if item.context == "discharge" and item.status != "held":
            discharge_rxcuis.add(row.rxcui)
        if item.context == "home":
            home_rxcuis.add(row.rxcui)
    assert TEST_RXCUI in home_rxcuis
    assert TEST_RXCUI_ALT in discharge_rxcuis
    assert TEST_RXCUI not in discharge_rxcuis


def test_f2_monitoring_not_arranged(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 50, F2_MONITORING)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    assert list_monitoring_for_case(db_session, case.id) == []
    warfarin_rows = []
    for item in list_medications_for_case(db_session, case.id):
        if item.ref_medication_id is None:
            continue
        row = db_session.get(RefMedication, item.ref_medication_id)
        if row is not None and row.rxcui == TEST_RXCUI_WARFARIN:
            warfarin_rows.append(item)
            if item.context == "discharge":
                assert not item.monitoring
    assert warfarin_rows
    home_w = [item for item in warfarin_rows if item.context == "home"]
    discharge_w = [item for item in warfarin_rows if item.context == "discharge"]
    assert home_w and discharge_w
    assert home_w[0].dose == discharge_w[0].dose
    assert home_w[0].route == discharge_w[0].route
    assert home_w[0].frequency == discharge_w[0].frequency
    assert home_w[0].ref_medication_id == discharge_w[0].ref_medication_id


def test_f2_held_med_no_restart_plan(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 51, F2_HELD_RESTART)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    assert not any(
        item.instruction_text and "resume when" in item.instruction_text.casefold()
        for item in list_instructions_for_case(db_session, case.id)
    )
    held = [
        item
        for item in list_medications_for_case(db_session, case.id)
        if item.status == "held" and item.held_reason
    ]
    assert held
    assert all(item.target_or_goal is None for item in held)


def test_f2_insufficient_supply(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 52, F2_SUPPLY)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    short = [
        item
        for item in list_medications_for_case(db_session, case.id)
        if item.context == "discharge" and item.quantity_or_days == "7 days"
    ]
    assert len(short) == 1
    followups = list_followups_for_case(db_session, case.id)
    assert followups
    assert followups[0].timing == "14 days"


def test_f2_hospital_only_continued(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 53, F2_HOSPITAL_ONLY)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    discharge_rxcuis = set()
    home_rxcuis = set()
    for item in list_medications_for_case(db_session, case.id):
        if item.ref_medication_id is None:
            continue
        row = db_session.get(RefMedication, item.ref_medication_id)
        if row is None:
            continue
        if item.context == "home":
            home_rxcuis.add(row.rxcui)
        if item.context == "discharge" and item.status != "held":
            discharge_rxcuis.add(row.rxcui)
    assert TEST_RXCUI_HOSP in discharge_rxcuis
    assert TEST_RXCUI_HOSP not in home_rxcuis


def test_f2_inpatient_substitution_not_reverted(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 54, F2_INPATIENT_SUB)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    by_context: dict[str, set[str]] = {"home": set(), "inpatient": set(), "discharge": set()}
    for item in list_medications_for_case(db_session, case.id):
        if item.ref_medication_id is None or item.status == "held":
            continue
        row = db_session.get(RefMedication, item.ref_medication_id)
        if row is None or item.context not in by_context:
            continue
        by_context[item.context].add(row.rxcui)
    assert TEST_RXCUI in by_context["home"]
    assert TEST_RXCUI_ALT in by_context["inpatient"]
    assert TEST_RXCUI_ALT in by_context["discharge"]
    assert TEST_RXCUI not in by_context["discharge"]
    assert not any(
        item.instruction_text and "resume home therapy" in item.instruction_text.casefold()
        for item in list_instructions_for_case(db_session, case.id)
    )


def test_f2_pending_decision_followup_missing(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _assert_category_case(db_session, 55, F2_PENDING_FOLLOWUP)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    assert list_followups_for_case(db_session, case.id) == []
    assert any(
        item.instruction_text and "pending therapeutic decision" in item.instruction_text.casefold()
        for item in list_instructions_for_case(db_session, case.id)
    )


def test_requested_category_is_never_silently_replaced(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _generate(db_session, 56, F1_DOSE)
    assert result.injected is not None
    assert result.injected.category == F1_DOSE
    assert result.injected.category != F1_OMISSION
    findings = detect_findings(
        db_session,
        db_session.get(ClinicalCase, result.case_id),  # type: ignore[arg-type]
    )
    assert [item.category for item in findings] == [F1_DOSE]


def test_plans_mark_exactly_the_intended_target(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _generate(db_session, 57, F1_FREQUENCY)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    targets = [plan for plan in list_plans_for_case(db_session, case.id) if plan.is_error_target]
    assert len(targets) == 1


def test_family_mismatch_is_rejected() -> None:
    with pytest.raises(CaseValidationError, match="does not match"):
        canonicalize_family("family_2", category=F1_OMISSION)


def test_broad_rxclass_is_not_used_for_substitution() -> None:
    assert class_usable_for_substitution(
        class_type="ATC1-4", class_id="TEST_CLASS_BETA", class_name="TEST beta blockers"
    )
    assert not class_usable_for_substitution(
        class_type="ATC1-4", class_id="C", class_name="CARDIOVASCULAR SYSTEM"
    )
    assert not class_usable_for_substitution(
        class_type="VA", class_id="CV000", class_name="CARDIOVASCULAR AGENTS"
    )


def test_ineligible_substitution_does_not_fallback(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _scenario()
    scenario.lab_queries = ["TEST_lab"]
    with pytest.raises(CaseValidationError, match="same-class substitute"):
        generate_one_case(
            db_session,
            sequence=58,
            seed=11,
            scenario=scenario,
            inject_error=True,
            use_openai=False,
            error_category=F1_SUBSTITUTION,
        )


def test_coprescription_never_appears_in_eligible_errors(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _generate(db_session, 60, None, inject=False)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    allowed = eligible_errors(db_session, case)
    assert F2_COPRESCRIPTION not in allowed
    assert NONE in allowed


def test_current_validation_plan_is_cliniproof_taxonomy_v1() -> None:
    plan = json.loads(Path("data/validation/batch_plan.json").read_text(encoding="utf-8"))
    assert plan["batch_code"] == "CLINIPROOF_TAXONOMY_V1"
    assert plan["cases"][0]["validation_case_id"] == "VAL-201"
    assert plan["cases"][0]["error_category"] == F1_OMISSION
    assert plan["cases"][0]["error_family"] == "family_1"
    assert plan["cases"][-1]["validation_case_id"] == "VAL-224"
    assert len(plan["cases"]) == 24
    assert [row["validation_case_id"] for row in plan["cases"]] == [
        f"VAL-{index:03d}" for index in range(201, 225)
    ]
    assert [row["sequence"] for row in plan["cases"]] == list(range(801, 825))
    categories = {row.get("error_category") for row in plan["cases"]}
    assert "omission" not in categories
    assert "incorrect_continuation" not in categories
    assert not Path("data/validation/cliniproof_v1").exists()
    assert not Path("data/validation/legacy_pre_taxonomy").exists()


def test_committed_cliniproof_export_is_canonical_and_blinded() -> None:
    validation_dir = Path("data/validation")
    plan = json.loads((validation_dir / "batch_plan.json").read_text(encoding="utf-8"))
    resident = json.loads(
        (validation_dir / "resident_validation_cases.json").read_text(encoding="utf-8")
    )
    investigator = json.loads(
        (validation_dir / "investigator_answer_key.json").read_text(encoding="utf-8")
    )
    worksheet = (validation_dir / "resident_review_worksheet.csv").read_text(encoding="utf-8")
    assert resident["batch_code"] == DEFAULT_BATCH_CODE
    assert investigator["batch_code"] == DEFAULT_BATCH_CODE
    assert len(resident["cases"]) == 24
    assert len(investigator["cases"]) == 24
    resident_ids = [row["case_id_code"] for row in resident["cases"]]
    investigator_ids = [row["validation_case_id"] for row in investigator["cases"]]
    planned_ids = [row["validation_case_id"] for row in plan["cases"]]
    assert resident_ids == planned_ids == investigator_ids
    assert "VAL-001" not in resident_ids
    blob = json.dumps(resident).casefold()
    leaked = [marker for marker in ("caseanswerkey", "syn-000", *LEAK_MARKERS) if marker in blob]
    assert leaked == []
    assert _collect_test_identifiers(resident) == []
    for planned, exported in zip(plan["cases"], investigator["cases"], strict=True):
        planned_category = planned.get("error_category") or NONE
        exported_category = exported["error"]["error_category"]
        assert canonicalize_category(exported_category) == canonicalize_category(planned_category)
        if planned.get("inject_error"):
            assert exported["control_error_status"] == "error_bearing"
            assert exported["error"]["error_family"] in {"family_1", "family_2"}
            assert len(exported["error"].get("trigger_meds") or []) >= 1
        else:
            assert exported["control_error_status"] == "NO INTENTIONAL ERROR"
            assert exported["error"]["error_category"] == NONE
    assert worksheet.splitlines()[1].startswith("VAL-201,")
    assert worksheet.splitlines()[-1].startswith("VAL-224,")
    for line in worksheet.splitlines()[1:]:
        fields = line.split(",")
        assert fields[0].startswith("VAL-")
        assert all(field == "" for field in fields[1:])


def test_obsolete_error_category_is_rejected_by_generation(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    with pytest.raises(CaseValidationError, match="unknown error category"):
        _generate(db_session, 39, "omission")


def test_ineligible_monitoring_does_not_fallback(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _scenario()
    scenario.anticoagulant_mutex_queries = []
    scenario.lab_queries = ["TEST_lab"]
    with pytest.raises(CaseValidationError, match="no substitute"):
        generate_one_case(
            db_session,
            sequence=59,
            seed=11,
            scenario=scenario,
            inject_error=True,
            use_openai=False,
            error_category=F2_MONITORING,
        )


def test_freeze_persists_canonical_ids(
    db_session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_taxonomy_refs(db_session)
    scenario = _scenario()
    monkeypatch.setattr("app.services.validation_batch.load_scenarios", lambda: [scenario])
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps(
            {
                "batch_code": "TEST_CANON",
                "master_seed": 11,
                "cases": [
                    {
                        "validation_case_id": "VAL-101",
                        "scenario": scenario.code,
                        "inject_error": True,
                        "error_family": "family_1",
                        "error_category": F1_OMISSION,
                        "sequence": 71,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result = freeze_validation_batch(
        db_session, plan_path=plan, use_openai=False, allow_test_identifiers=True
    )
    assert result.rejected == []
    assert result.frozen[0].error_category == F1_OMISSION
    assert result.frozen[0].error_family == "family_1"


def test_freeze_does_not_substitute_ineligible_category(
    db_session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_generation_refs(db_session)
    scenario = _scenario()
    scenario.lab_queries = ["TEST_lab"]
    monkeypatch.setattr("app.services.validation_batch.load_scenarios", lambda: [scenario])
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps(
            {
                "batch_code": "TEST_NO_FALLBACK",
                "master_seed": 11,
                "cases": [
                    {
                        "validation_case_id": "VAL-102",
                        "scenario": scenario.code,
                        "inject_error": True,
                        "error_family": "family_1",
                        "error_category": F1_SUBSTITUTION,
                        "sequence": 72,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CaseValidationError, match="rejected assignments|same-class substitute"):
        freeze_validation_batch(
            db_session, plan_path=plan, use_openai=False, allow_test_identifiers=True
        )


def test_freeze_rejects_category_not_allowed_for_scenario(
    db_session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_taxonomy_refs(db_session)
    scenario = _scenario()
    scenario.allowed_error_categories = [F1_OMISSION]
    monkeypatch.setattr("app.services.validation_batch.load_scenarios", lambda: [scenario])
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps(
            {
                "batch_code": "TEST_ALLOWED",
                "master_seed": 11,
                "cases": [
                    {
                        "validation_case_id": "VAL-103",
                        "scenario": scenario.code,
                        "inject_error": True,
                        "error_family": "family_1",
                        "error_category": F1_DOSE,
                        "sequence": 73,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CaseValidationError, match="not allowed for scenario"):
        freeze_validation_batch(
            db_session, plan_path=plan, use_openai=False, allow_test_identifiers=True
        )


def test_ineligible_categories_on_a_plain_clean_case_do_not_fallback(
    db_session: Session,
) -> None:
    _seed_taxonomy_refs(db_session)
    result = _generate(db_session, 81, None, inject=False)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    allowed = set(eligible_errors(db_session, case))
    assert NONE in allowed
    assert F2_COPRESCRIPTION not in allowed
    rng = random.Random("no-fallback")
    rejected: list[str] = []
    for category in sorted(IMPLEMENTABLE_CATEGORIES - {NONE}):
        if category in allowed:
            continue
        with pytest.raises(
            CaseValidationError, match="not eligible|no substitute|cannot be injected"
        ):
            inject_reconciliation_error(
                db_session,
                case,
                rng=rng,
                seed="ineligible",
                preferred_category=category,
            )
        rejected.append(category)
        assert detect_findings(db_session, case) == []
    assert F2_HOSPITAL_ONLY in rejected
    assert F2_HELD_RESTART in rejected
    assert F2_SUPPLY in rejected
    assert F2_PENDING_FOLLOWUP in rejected
    assert F2_INPATIENT_SUB in rejected


def test_clearing_dose_makes_dose_mismatch_ineligible(db_session: Session) -> None:
    _seed_taxonomy_refs(db_session)
    result = _generate(db_session, 82, None, inject=False)
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    for item in list_medications_for_case(db_session, case.id):
        item.dose = None
    db_session.flush()
    db_session.expire_all()
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    assert F1_DOSE not in eligible_errors(db_session, case)
    with pytest.raises(CaseValidationError, match="not eligible"):
        inject_reconciliation_error(
            db_session,
            case,
            rng=random.Random("dose"),
            seed="ineligible-dose",
            preferred_category=F1_DOSE,
        )


def test_default_batch_code_and_plan_are_cliniproof_taxonomy_v1() -> None:
    from app.cli import export_validation_batch_cmd, freeze_validation_batch_cmd
    from app.services.validation_batch import DEFAULT_BATCH_PLAN_PATH

    assert DEFAULT_BATCH_CODE == "CLINIPROOF_TAXONOMY_V1"
    assert DEFAULT_BATCH_PLAN_PATH == Path("data/validation/batch_plan.json").resolve()
    plan = json.loads(DEFAULT_BATCH_PLAN_PATH.read_text(encoding="utf-8"))
    assert plan["batch_code"] == DEFAULT_BATCH_CODE
    export_default = inspect.signature(export_validation_batch_cmd).parameters["batch_code"].default
    assert export_default == DEFAULT_BATCH_CODE
    freeze_default = inspect.signature(freeze_validation_batch_cmd).parameters["plan"].default
    assert freeze_default is None
