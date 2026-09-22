"""Freeze a resident-validation batch and export blinded plus investigator files.

VAL-* identifiers are immutable after freeze. OpenAI is not used to choose errors
or write answer keys. Cases are machine-validated synthetic records pending
clinician validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import __version__
from app.models.cases import (
    CaseConsult,
    CaseDevice,
    CaseDischargePlanning,
    CaseFollowup,
    CaseImaging,
    CaseInstruction,
    CaseIntakeOutput,
    CaseMedicationReconciliation,
    CaseMonitoring,
    CaseNote,
    CasePresentation,
    CaseProblemList,
    CaseProcedure,
    CaseReturnPrecaution,
    CaseSocialSupport,
    CaseTherapyRestriction,
    CaseVital,
    CaseWeight,
    ClinicalCase,
)
from app.models.generation import ValidationBatchCase
from app.models.reference import RefDiagnosis, RefLabTest, RefMedication, RefSymptom
from app.repositories.cases import (
    get_frozen_case_by_validation_id,
    list_answer_keys_for_case,
    list_diagnoses_for_case,
    list_frozen_batch,
    list_labs_for_case,
    list_medications_for_case,
    list_symptoms_for_case,
)
from app.repositories.reference import (
    get_data_source,
    get_diagnosis_by_icd10cm,
    get_lab_test_by_loinc,
    get_medication_by_rxcui,
    get_unit_by_ucum,
    list_enabled_rules,
    list_rules,
)
from app.services.bootstrap import load_json_object, match_diagnosis, match_lab, match_medication
from app.services.error_taxonomy import (
    FAMILY_NONE,
    NONE,
    canonicalize_category,
    canonicalize_family,
    categories_equal,
)
from app.services.generation import (
    GENERATOR_NAME,
    GeneratedCaseResult,
    generate_one_case,
    load_scenarios,
)
from app.services.validation import validate_case
from app.sources.exceptions import FrozenValidationCaseError
from app.utils.identifiers import VALIDATION_CASE_RE, format_validation_child_id
from app.utils.jsonio import dumps_json, loads_json

VALIDATION_DIR = Path(__file__).resolve().parents[2] / "data" / "validation"
DEFAULT_BATCH_PLAN_PATH = VALIDATION_DIR / "batch_plan.json"
DEFAULT_EXPORT_DIR = VALIDATION_DIR
DATASET_STATUS = "machine-validated synthetic resident-review cases pending clinician validation"
LEAK_MARKERS = (
    "intentional error",
    "error_injected",
    "is_error_target",
    "is_clean_control",
    "no intentional error",
    "answer_key",
    "random_seed",
    "generator_version",
    "source_system",
    "retrieved_at",
    "rxcui:",
    "syn-000",
    "error_family",
    "error_category",
    "detectability_location",
    "correct_action",
    "clean_expected_state",
    "injected_state",
    "evidence_required",
    "difficulty_a_priori",
    "severity_ncc_merp",
    "intentional_changes",
    "trigger_meds",
    "is_primary_error",
)


@dataclass
class Assignment:
    validation_case_id: str
    scenario: str
    inject_error: bool
    error_category: str | None
    sequence: int
    error_family: str | None = None


@dataclass
class Rejection:
    validation_case_id: str
    scenario: str
    reason: str


@dataclass
class FreezeResult:
    batch_code: str
    master_seed: int
    frozen: list[ValidationBatchCase] = field(default_factory=list)
    rejected: list[Rejection] = field(default_factory=list)
    reused: list[str] = field(default_factory=list)


@dataclass
class ExportResult:
    resident_path: Path
    investigator_path: Path
    investigator_markdown_path: Path
    manifest_path: Path
    coverage_path: Path
    worksheet_path: Path
    schema_path: Path
    audit: dict[str, Any]


def load_batch_plan(path: Path | None = None) -> dict[str, Any]:
    return load_json_object(path or DEFAULT_BATCH_PLAN_PATH)


def parse_assignments(plan: dict[str, Any]) -> list[Assignment]:
    rows = plan.get("cases")
    if not isinstance(rows, list) or not rows:
        raise ValueError("batch plan must contain a non-empty cases list")
    assignments: list[Assignment] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        validation_case_id = str(item.get("validation_case_id") or "")
        if VALIDATION_CASE_RE.fullmatch(validation_case_id) is None:
            raise ValueError(f"invalid validation_case_id {validation_case_id!r}")
        assignments.append(
            Assignment(
                validation_case_id=validation_case_id,
                scenario=str(item.get("scenario") or ""),
                inject_error=bool(item.get("inject_error")),
                error_family=(
                    None
                    if item.get("error_family") in (None, "")
                    else str(item.get("error_family"))
                ),
                error_category=(
                    None
                    if item.get("error_category") in (None, "")
                    else str(item.get("error_category"))
                ),
                sequence=int(item["sequence"]),
            )
        )
    return assignments


def freeze_validation_batch(
    session: Session,
    *,
    plan_path: Path | None = None,
    use_openai: bool = False,
    allow_test_identifiers: bool = False,
) -> FreezeResult:
    plan = load_batch_plan(plan_path)
    batch_code = str(plan.get("batch_code") or "RESIDENT_VALIDATION_V1")
    master_seed = int(plan.get("master_seed") or 0)
    scenarios = {item.code: item for item in load_scenarios()}
    result = FreezeResult(batch_code=batch_code, master_seed=master_seed)
    for assignment in parse_assignments(plan):
        case_seed = f"{master_seed}:{assignment.sequence}:{assignment.scenario}"
        existing = get_frozen_case_by_validation_id(session, assignment.validation_case_id)
        if existing is not None and existing.immutable:
            if existing.case_seed == case_seed and existing.scenario_code == assignment.scenario:
                result.frozen.append(existing)
                result.reused.append(assignment.validation_case_id)
                continue
            raise FrozenValidationCaseError(
                assignment.validation_case_id,
                "existing frozen assignment does not match this plan",
            )
        scenario = scenarios.get(assignment.scenario)
        if scenario is None:
            result.rejected.append(
                Rejection(assignment.validation_case_id, assignment.scenario, "unknown scenario")
            )
            continue
        try:
            if assignment.inject_error:
                requested = canonicalize_category(assignment.error_category)
                canonicalize_family(assignment.error_family, category=requested)
            elif assignment.error_category not in (None, "", NONE):
                raise ValueError("clean control must use error_category none")
            generated = generate_one_case(
                session,
                sequence=assignment.sequence,
                seed=master_seed,
                scenario=scenario,
                inject_error=assignment.inject_error,
                use_openai=use_openai,
                error_category=assignment.error_category,
            )
        except Exception as exc:
            result.rejected.append(
                Rejection(assignment.validation_case_id, assignment.scenario, str(exc))
            )
            continue
        case = session.get(ClinicalCase, generated.case_id)
        if case is None:
            result.rejected.append(
                Rejection(assignment.validation_case_id, assignment.scenario, "case row missing")
            )
            continue
        audit_errors = _audit_generated(
            session,
            case,
            generated,
            assignment,
            allow_test_identifiers=allow_test_identifiers,
        )
        if audit_errors:
            result.rejected.append(
                Rejection(
                    assignment.validation_case_id,
                    assignment.scenario,
                    "; ".join(audit_errors),
                )
            )
            continue
        frozen = _persist_frozen_row(
            session,
            case=case,
            generated=generated,
            assignment=assignment,
            batch_code=batch_code,
            master_seed=master_seed,
            case_seed=case_seed,
        )
        result.frozen.append(frozen)
    session.flush()
    return result


def export_validation_batch(
    session: Session,
    *,
    batch_code: str,
    output_dir: Path | None = None,
    allow_test_identifiers: bool = False,
) -> ExportResult:
    output = output_dir or DEFAULT_EXPORT_DIR
    output.mkdir(parents=True, exist_ok=True)
    rows = list_frozen_batch(session, batch_code)
    if not rows:
        raise ValueError(f"no frozen cases for batch {batch_code}")
    resident_cases: list[dict[str, Any]] = []
    investigator_cases: list[dict[str, Any]] = []
    manifest_cases: list[dict[str, Any]] = []
    for frozen in rows:
        case = session.get(ClinicalCase, frozen.case_id)
        if case is None:
            continue
        resident = _resident_payload(session, case, frozen)
        frozen.resident_state = resident
        investigator = _investigator_payload(session, case, frozen)
        resident_cases.append(resident)
        investigator_cases.append(investigator)
        manifest_cases.append(
            {
                "validation_case_id": frozen.validation_case_id,
                "scenario": frozen.scenario_code,
                "seed": frozen.case_seed,
                "control_error_status": (
                    "clean_control" if frozen.is_clean_control else "error_bearing"
                ),
                "error_category": frozen.error_category,
                "clean_validation_status": _passed_flag(frozen.clean_validation),
                "post_injection_validation_status": _passed_flag(frozen.final_validation),
                "reference_snapshot": frozen.reference_snapshot,
                "rule_snapshot": frozen.rule_snapshot,
            }
        )
    audit = audit_frozen_batch(session, batch_code, allow_test_identifiers=allow_test_identifiers)
    coverage = build_coverage_report(session, batch_code, audit)
    resident_doc = {
        "dataset_status": DATASET_STATUS,
        "batch_code": batch_code,
        "description": (
            "Resident-facing synthetic cases for medication-reconciliation review. "
            + DATASET_STATUS
        ),
        "cases": resident_cases,
    }
    investigator_doc = {
        "dataset_status": DATASET_STATUS,
        "batch_code": batch_code,
        "cases": investigator_cases,
    }
    manifest_doc = {
        "dataset_status": DATASET_STATUS,
        "batch_code": batch_code,
        "generator_version": __version__,
        "exported_at": datetime.now(UTC).isoformat(),
        "cases": manifest_cases,
    }
    resident_path = output / "resident_validation_cases.json"
    investigator_path = output / "investigator_answer_key.json"
    investigator_md = output / "investigator_answer_key.md"
    manifest_path = output / "validation_manifest.json"
    coverage_path = output / "coverage_report.md"
    worksheet_path = output / "resident_review_worksheet.csv"
    schema_path = output / "resident_review_schema.json"
    resident_path.write_text(dumps_json(resident_doc), encoding="utf-8")
    investigator_path.write_text(dumps_json(investigator_doc), encoding="utf-8")
    investigator_md.write_text(_investigator_markdown(investigator_doc), encoding="utf-8")
    manifest_path.write_text(dumps_json(manifest_doc), encoding="utf-8")
    coverage_path.write_text(_coverage_markdown(coverage), encoding="utf-8")
    worksheet_path.write_text(_worksheet_csv(rows), encoding="utf-8")
    schema_path.write_text(dumps_json(_review_schema()), encoding="utf-8")
    (output / "scenario_coverage_matrix.md").write_text(
        _scenario_matrix_markdown(session),
        encoding="utf-8",
    )
    return ExportResult(
        resident_path=resident_path,
        investigator_path=investigator_path,
        investigator_markdown_path=investigator_md,
        manifest_path=manifest_path,
        coverage_path=coverage_path,
        worksheet_path=worksheet_path,
        schema_path=schema_path,
        audit=audit,
    )


def audit_frozen_batch(
    session: Session,
    batch_code: str,
    *,
    allow_test_identifiers: bool = False,
) -> dict[str, Any]:
    rows = list_frozen_batch(session, batch_code)
    errors: list[str] = []
    unexpected_errors = 0
    intended_one = 0
    clean_passed = 0
    loinc_cases = 0
    for frozen in rows:
        case = session.get(ClinicalCase, frozen.case_id)
        if case is None:
            errors.append(f"{frozen.validation_case_id}: missing clinical case")
            continue
        if frozen.clean_validation and frozen.clean_validation.get("passed"):
            clean_passed += 1
        else:
            errors.append(f"{frozen.validation_case_id}: clean validation did not pass")
        report = validate_case(
            session,
            case,
            expect_injected_error=not frozen.is_clean_control,
            expected_category=None if frozen.is_clean_control else frozen.error_category,
        )
        if not report.passed:
            unexpected_errors += 1
            errors.append(
                f"{frozen.validation_case_id}: post-freeze validation failed: "
                + "; ".join(report.errors())
            )
        keys = list_answer_keys_for_case(session, case.id)
        if frozen.is_clean_control:
            if keys:
                errors.append(f"{frozen.validation_case_id}: clean control has an answer key")
            if case.clean_case is False:
                errors.append(f"{frozen.validation_case_id}: clean control marked error-injected")
        else:
            if len(keys) != 1:
                errors.append(f"{frozen.validation_case_id}: expected one answer key")
            else:
                intended_one += 1
                if not categories_equal(keys[0].error_category, frozen.error_category):
                    errors.append(
                        f"{frozen.validation_case_id}: answer key category "
                        f"{keys[0].error_category!r} != {frozen.error_category!r}"
                    )
        errors.extend(
            _terminology_audit(
                session,
                case,
                frozen.validation_case_id,
                allow_test_identifiers=allow_test_identifiers,
            )
        )
        resident = _resident_payload(session, case, frozen)
        blob = dumps_json(resident).casefold()
        for marker in LEAK_MARKERS:
            if marker in blob:
                errors.append(f"{frozen.validation_case_id}: resident export leaked {marker!r}")
        if not allow_test_identifiers and _json_has_test_identifier(resident):
            errors.append(f"{frozen.validation_case_id}: resident export leaked TEST_ identifier")
        labs = list_labs_for_case(session, case.id)
        if labs:
            loinc_cases += 1
    return {
        "passed": not errors,
        "errors": errors,
        "frozen_count": len(rows),
        "clean_passed": clean_passed,
        "exactly_one_intended_error": intended_one,
        "unexpected_additional_errors": unexpected_errors,
        "loinc_backed_lab_cases": loinc_cases,
    }


def build_coverage_report(
    session: Session, batch_code: str, audit: dict[str, Any] | None = None
) -> dict[str, Any]:
    rows = list_frozen_batch(session, batch_code)
    scenarios: dict[str, int] = {}
    error_types: dict[str, int] = {}
    clean_controls = 0
    error_bearing = 0
    meds: set[str] = set()
    rxcuis: set[str] = set()
    diagnoses: set[str] = set()
    icds: set[str] = set()
    labs: set[str] = set()
    loincs: set[str] = set()
    units: set[str] = set()
    loinc_cases = 0
    rule_use: dict[str, int] = {}
    for frozen in rows:
        scenarios[frozen.scenario_code] = scenarios.get(frozen.scenario_code, 0) + 1
        if frozen.is_clean_control:
            clean_controls += 1
        else:
            error_bearing += 1
            if frozen.error_category:
                error_types[frozen.error_category] = error_types.get(frozen.error_category, 0) + 1
        case = session.get(ClinicalCase, frozen.case_id)
        if case is None:
            continue
        case_rxcuis: set[str] = set()
        for medication in list_medications_for_case(session, case.id):
            if medication.drug:
                meds.add(medication.drug)
            if medication.ref_medication_id is not None:
                med_row = session.get(RefMedication, medication.ref_medication_id)
                if med_row is not None:
                    rxcuis.add(med_row.rxcui)
                    case_rxcuis.add(med_row.rxcui)
        for diagnosis in list_diagnoses_for_case(session, case.id):
            if diagnosis.diagnosis:
                diagnoses.add(diagnosis.diagnosis)
            if diagnosis.ref_diagnosis_id is not None:
                dx_row = session.get(RefDiagnosis, diagnosis.ref_diagnosis_id)
                if dx_row is not None and dx_row.icd10cm_code:
                    icds.add(dx_row.icd10cm_code)
        case_labs = list_labs_for_case(session, case.id)
        if case_labs:
            loinc_cases += 1
        for lab in case_labs:
            if lab.test_name:
                labs.add(lab.test_name)
            if lab.unit:
                units.add(lab.unit)
            if lab.ref_lab_id is not None:
                lab_row = session.get(RefLabTest, lab.ref_lab_id)
                if lab_row is not None:
                    loincs.add(lab_row.loinc_code)
        enabled = {rule.rule_code: rule for rule in list_enabled_rules(session)}
        for rule in enabled.values():
            if rule.input_rxcui and rule.input_rxcui in case_rxcuis:
                rule_use[rule.rule_code] = rule_use.get(rule.rule_code, 0) + 1
    audit_doc = audit or {}
    return {
        "dataset_status": DATASET_STATUS,
        "total_cases": len(rows),
        "scenarios": scenarios,
        "clean_controls": clean_controls,
        "error_bearing": error_bearing,
        "error_types": error_types,
        "unique_medications": sorted(meds),
        "unique_rxcuis": sorted(rxcuis),
        "unique_diagnoses": sorted(diagnoses),
        "unique_icd_codes": sorted(icds),
        "unique_labs": sorted(labs),
        "unique_loinc_codes": sorted(loincs),
        "unique_ucum_units": sorted(units),
        "loinc_backed_lab_cases": loinc_cases,
        "rule_coverage": rule_use,
        "rules": [
            {
                "rule_code": rule.rule_code,
                "severity": rule.severity,
                "enabled": rule.enabled,
                "source_system": rule.source_system,
                "source_identifier": rule.source_identifier,
            }
            for rule in list_rules(session)
        ],
        "validation": audit_doc,
    }


def _persist_frozen_row(
    session: Session,
    *,
    case: ClinicalCase,
    generated: GeneratedCaseResult,
    assignment: Assignment,
    batch_code: str,
    master_seed: int,
    case_seed: str,
) -> ValidationBatchCase:
    keys = list_answer_keys_for_case(session, case.id)
    answer = None
    if keys:
        key = keys[0]
        answer = {
            "answer_id": key.answer_id,
            "error_family": key.error_family,
            "error_category": key.error_category,
            "error_description": key.error_description,
            "trigger_meds": key.trigger_meds,
            "correct_action": key.correct_action,
            "is_primary_error": key.is_primary_error,
            "intentional_changes": key.intentional_changes,
        }
    frozen = ValidationBatchCase(
        validation_case_id=assignment.validation_case_id,
        batch_code=batch_code,
        case_id=case.id,
        scenario_code=assignment.scenario,
        master_seed=master_seed,
        case_seed=case_seed,
        is_clean_control=not assignment.inject_error,
        error_family=(
            FAMILY_NONE
            if not assignment.inject_error
            else canonicalize_family(
                assignment.error_family,
                category=canonicalize_category(assignment.error_category),
            )
        ),
        error_category=(
            None
            if not assignment.inject_error
            else canonicalize_category(assignment.error_category)
        ),
        generator_version=__version__,
        reference_snapshot=_reference_snapshot(session),
        rule_snapshot=_rule_snapshot(session),
        clean_validation=generated.clean_validation,
        final_validation=generated.validation,
        clean_state=generated.clean_state,
        resident_state=None,
        answer_key_payload=answer,
        immutable=True,
    )
    session.add(frozen)
    session.flush()
    frozen.resident_state = _resident_payload(session, case, frozen)
    session.flush()
    return frozen


def _audit_generated(
    session: Session,
    case: ClinicalCase,
    generated: GeneratedCaseResult,
    assignment: Assignment,
    *,
    allow_test_identifiers: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not generated.clean_passed:
        errors.append("clean validation failed")
    if not allow_test_identifiers and "TEST_" in dumps_json(generated.clean_state):
        errors.append("TEST_ identifier present in clean state")
    if assignment.inject_error:
        if generated.injected is None:
            errors.append("expected an injected error")
        elif assignment.error_category and not categories_equal(
            generated.injected.category, assignment.error_category
        ):
            errors.append(
                "injected category "
                f"{generated.injected.category!r} != {assignment.error_category!r}"
            )
        elif assignment.error_family:
            try:
                canonicalize_family(assignment.error_family, category=generated.injected.category)
            except Exception as exc:
                errors.append(str(exc))
    elif generated.injected is not None:
        errors.append("clean control received an injected error")
    errors.extend(
        _terminology_audit(
            session,
            case,
            assignment.validation_case_id,
            allow_test_identifiers=allow_test_identifiers,
        )
    )
    return errors


def _terminology_audit(
    session: Session,
    case: ClinicalCase,
    label: str,
    *,
    allow_test_identifiers: bool = False,
) -> list[str]:
    errors: list[str] = []
    for medication in list_medications_for_case(session, case.id):
        if medication.ref_medication_id is None:
            errors.append(f"{label}: medication missing reference")
            continue
        med_row = session.get(RefMedication, medication.ref_medication_id)
        if med_row is None or get_medication_by_rxcui(session, med_row.rxcui) is None:
            errors.append(f"{label}: unresolved RXCUI")
            continue
        if med_row.source_system is None:
            errors.append(f"{label}: medication {med_row.rxcui} is not source-backed")
        if med_row.rxcui.startswith("TEST_") and not allow_test_identifiers:
            errors.append(f"{label}: medication {med_row.rxcui} is not source-backed")
    for diagnosis in list_diagnoses_for_case(session, case.id):
        if diagnosis.ref_diagnosis_id is None:
            errors.append(f"{label}: diagnosis missing reference")
            continue
        dx_row = session.get(RefDiagnosis, diagnosis.ref_diagnosis_id)
        if dx_row is None or not dx_row.icd10cm_code:
            errors.append(f"{label}: unresolved diagnosis")
            continue
        if (
            get_diagnosis_by_icd10cm(session, dx_row.icd10cm_code) is None
            or dx_row.source_system is None
        ):
            errors.append(f"{label}: diagnosis {dx_row.icd10cm_code} is not source-backed")
        if dx_row.icd10cm_code.startswith("TEST_") and not allow_test_identifiers:
            errors.append(f"{label}: TEST_ diagnosis code")
    for lab in list_labs_for_case(session, case.id):
        if lab.ref_lab_id is None:
            errors.append(f"{label}: lab missing reference")
            continue
        lab_row = session.get(RefLabTest, lab.ref_lab_id)
        if lab_row is None or get_lab_test_by_loinc(session, lab_row.loinc_code) is None:
            errors.append(f"{label}: unresolved LOINC")
            continue
        if lab_row.source_system is None:
            errors.append(f"{label}: lab {lab_row.loinc_code} is not source-backed")
        if lab_row.loinc_code.startswith("TEST_") and not allow_test_identifiers:
            errors.append(f"{label}: lab {lab_row.loinc_code} is not source-backed")
        if lab.unit:
            unit_row = get_unit_by_ucum(session, lab.unit)
            allowed = {str(item) for item in (lab_row.example_ucum_units or []) if item is not None}
            if unit_row is None and lab.unit not in allowed:
                errors.append(f"{label}: unsupported unit {lab.unit!r}")
    for symptom in list_symptoms_for_case(session, case.id):
        if symptom.ref_symptom_id is None:
            errors.append(f"{label}: symptom missing reference")
            continue
        symptom_row = session.get(RefSymptom, symptom.ref_symptom_id)
        if symptom_row is None or symptom_row.source_system is None:
            errors.append(f"{label}: symptom is not source-backed")
        snomed = None if symptom_row is None else symptom_row.snomed_code
        if snomed and snomed.startswith("HP:"):
            errors.append(f"{label}: HPO identifier stored as snomed_code")
    return errors


def _resident_payload(
    session: Session, case: ClinicalCase, frozen: ValidationBatchCase
) -> dict[str, Any]:
    val_id = frozen.validation_case_id
    presentation = session.scalar(
        select(CasePresentation).where(CasePresentation.case_id == case.id)
    )
    social = session.scalar(select(CaseSocialSupport).where(CaseSocialSupport.case_id == case.id))
    discharge = session.scalar(
        select(CaseDischargePlanning).where(CaseDischargePlanning.case_id == case.id)
    )
    symptoms = list_symptoms_for_case(session, case.id)
    weight = session.scalar(select(CaseWeight).where(CaseWeight.case_id == case.id))
    payload = {
        "case_id_code": val_id,
        "ClinicalCase": {
            "title": _resident_title(case, val_id),
            "case_id_code": val_id,
            "case_status": "review",
            "generation_source": "synthetic",
            "one_liner": case.one_liner,
            "admission_dx": case.admission_dx,
            "disposition_status": case.disposition_status,
            "chief_complaint": case.chief_complaint,
            "patient_name": f"VAL Patient {val_id.removeprefix('VAL-')}",
            "patient_age": case.patient_age,
            "patient_gender": case.patient_gender,
            "ethnicity": case.ethnicity,
            "weight_kg": None if weight is None else weight.weight_kg,
            "social_context": None if social is None else social.living_situation,
            "is_active": True,
            "difficulty": case.difficulty,
            "specialty": case.specialty,
            "allergies": [],
            "medical_history": [],
            "source_type": "authored_scenario",
            "source_file": None,
            "presentation": {
                "chief_complaint": None if presentation is None else presentation.chief_complaint,
                "hpi": None if presentation is None else presentation.hpi,
                "review_of_systems": (
                    None if presentation is None else presentation.review_of_systems
                ),
                "presenting_symptoms": [item.symptom for item in symptoms if item.symptom],
                "symptom_duration": None if presentation is None else presentation.symptom_duration,
                "symptom_course": None if presentation is None else presentation.symptom_course,
            },
            "social_support": None
            if social is None
            else {
                "living_situation": social.living_situation,
                "caregiver_support": social.caregiver_support,
                "transportation": social.transportation,
                "financial_barriers": social.financial_barriers,
                "health_literacy": social.health_literacy,
                "language_preference": social.language_preference,
                "substance_use": social.substance_use,
                "advance_directive": social.advance_directive,
            },
            "discharge_planning": None
            if discharge is None
            else {
                "disposition": discharge.disposition,
                "disposition_detail": discharge.disposition_detail,
                "transportation_needed": discharge.transportation_needed,
                "barriers_to_discharge": discharge.barriers_to_discharge or [],
                "discharge_readiness": discharge.discharge_readiness,
                "anticipated_discharge_date": discharge.anticipated_discharge_date,
                "medicaid_pending": None,
                "home_health_ordered": discharge.home_health_ordered,
                "dme_needed": discharge.dme_needed or [],
            },
        },
        "CaseDiagnosis": [
            {
                "diagnosis_id": _child_id("DX", val_id, index),
                "case_id": val_id,
                "diagnosis": item.diagnosis,
                "diagnosis_type": item.diagnosis_type,
                "status": item.status,
                "context": item.context,
                "source_type": "authored_scenario",
                "source_reference": None,
            }
            for index, item in enumerate(list_diagnoses_for_case(session, case.id), start=1)
        ],
        "CaseNote": [
            {
                "note_id": _child_id("NOTE", val_id, index),
                "case_id": val_id,
                "note_type": item.note_type,
                "note_text": item.note_text,
                "source_type": "authored_scenario",
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseNote, case.id, CaseNote.note_id), start=1
            )
        ],
        "CaseVital": [
            {
                "vital_id": _child_id("VIT", val_id, index),
                "case_id": val_id,
                "timepoint": item.timepoint,
                "temp_c": item.temp_c,
                "bp_systolic": item.bp_systolic,
                "bp_diastolic": item.bp_diastolic,
                "heart_rate": item.heart_rate,
                "resp_rate": item.resp_rate,
                "spo2_percent": item.spo2_percent,
                "oxygen_support": item.oxygen_support,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseVital, case.id, CaseVital.vital_id), start=1
            )
        ],
        "CaseLab": [
            {
                "lab_id": _child_id("LAB", val_id, index),
                "case_id": val_id,
                "timepoint": item.timepoint,
                "test_name": item.test_name,
                "value": item.value,
                "value_text": item.value_text,
                "unit": item.unit,
                "status": item.status,
                "source_reference": None,
            }
            for index, item in enumerate(list_labs_for_case(session, case.id), start=1)
        ],
        "CaseImaging": [
            {
                "study_id": _child_id("STUDY", val_id, index),
                "case_id": val_id,
                "timepoint": item.timepoint,
                "study_type": item.study_type,
                "body_site": item.body_site,
                "finding": item.finding,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseImaging, case.id, CaseImaging.study_id), start=1
            )
        ],
        "CaseConsult": [
            {
                "consult_id": _child_id("CON", val_id, index),
                "case_id": val_id,
                "service": item.service,
                "recommendation": item.recommendation,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseConsult, case.id, CaseConsult.consult_id), start=1
            )
        ],
        "CaseMedication": [
            {
                "medication_id": _child_id("MED", val_id, index),
                "case_id": val_id,
                "context": item.context,
                "drug": item.drug,
                "reported_name": item.reported_name,
                "dose": item.dose,
                "route": item.route,
                "frequency": item.frequency,
                "indication": item.indication,
                "status": item.status,
                "held_reason": item.held_reason,
                "verification_status": "verified",
                "verification_source": "prior_records",
                "target_or_goal": item.target_or_goal,
                "monitoring": item.monitoring,
                "quantity_or_days": item.quantity_or_days,
                "refills": item.refills,
                "source_type": "authored_scenario",
                "source_file": None,
                "source_reference": None,
                "notes": None,
            }
            for index, item in enumerate(list_medications_for_case(session, case.id), start=1)
        ],
        "CaseFollowup": [
            {
                "followup_id": _child_id("FU", val_id, index),
                "case_id": val_id,
                "item": item.item,
                "timing": item.timing,
                "with_service": item.with_service,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseFollowup, case.id, CaseFollowup.followup_id), start=1
            )
        ],
        "CaseInstruction": [
            {
                "instruction_id": _child_id("INS", val_id, index),
                "case_id": val_id,
                "category": item.category,
                "instruction_text": item.instruction_text,
                "source_type": "authored_scenario",
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseInstruction, case.id, CaseInstruction.instruction_id), start=1
            )
        ],
        "CaseMonitoring": [
            {
                "monitoring_id": _child_id("MON", val_id, index),
                "case_id": val_id,
                "parameter": item.parameter,
                "frequency": item.frequency,
                "target": item.target,
                "trigger_for_action": item.trigger_for_action,
                "duration": item.duration,
                "responsible_service": item.responsible_service,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseMonitoring, case.id, CaseMonitoring.monitoring_id), start=1
            )
        ],
        "CaseProblemList": [
            {
                "problem_id": _child_id("PROB", val_id, index),
                "case_id": val_id,
                "problem": item.problem,
                "problem_type": item.problem_type,
                "onset_date": None,
                "priority": item.priority,
                "status": item.status,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseProblemList, case.id, CaseProblemList.problem_id), start=1
            )
        ],
        "CaseProcedure": [
            {
                "procedure_id": _child_id("PROC", val_id, index),
                "case_id": val_id,
                "procedure_name": item.procedure_name,
                "procedure_type": item.procedure_type,
                "date": item.date,
                "time": item.timepoint,
                "performed_by": item.performed_by,
                "anesthesia_type": item.anesthesia_type,
                "findings": item.findings,
                "complications": item.complications,
                "duration_minutes": item.duration_minutes,
                "laterality": item.laterality,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseProcedure, case.id, CaseProcedure.procedure_id), start=1
            )
        ],
        "CaseTherapyRestriction": [
            {
                "therapy_id": _child_id("THER", val_id, index),
                "case_id": val_id,
                "category": item.category,
                "item": item.item,
                "order_detail": item.order_detail,
                "start_date": item.start_date,
                "end_date": item.end_date,
                "status": item.status,
                "ordered_by": item.ordered_by,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseTherapyRestriction, case.id, CaseTherapyRestriction.therapy_id),
                start=1,
            )
        ],
        "CaseReturnPrecaution": [
            {
                "precaution_id": _child_id("RP", val_id, index),
                "case_id": val_id,
                "symptom": item.symptom,
                "reason": item.reason,
                "action": item.action,
                "severity": item.severity,
                "patient_instruction": item.patient_instruction,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseReturnPrecaution, case.id, CaseReturnPrecaution.precaution_id),
                start=1,
            )
        ],
        "CaseMedicationReconciliation": [
            {
                "medrec_id": _child_id("MR", val_id, index),
                "case_id": val_id,
                "bpmh_source": "prior_records",
                "bpmh_interviewer": None,
                "bpmh_date": item.bpmh_date,
                "medrec_status": "complete",
                "patient_able_to_participate": item.patient_able_to_participate,
                "unverified_medications_present": None,
                "reconciliation_admission": {
                    "discrepancies_found": None,
                    "resolved": None,
                    "notes": None,
                },
                "reconciliation_discharge": {
                    "discrepancies_found": None,
                    "resolved": None,
                    "notes": None,
                },
                "discrepancy_types": [],
                "pharmacist_review": item.pharmacist_review,
                "high_alert_meds_identified": [],
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(
                    session,
                    CaseMedicationReconciliation,
                    case.id,
                    CaseMedicationReconciliation.medrec_id,
                ),
                start=1,
            )
        ],
        "CaseWeight": [
            {
                "weight_id": _child_id("WT", val_id, index),
                "case_id": val_id,
                "timepoint": item.timepoint,
                "weight_kg": item.weight_kg,
                "dry_weight_kg": item.dry_weight_kg,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseWeight, case.id, CaseWeight.weight_id), start=1
            )
        ],
        "CaseIntakeOutput": [
            {
                "io_id": _child_id("IO", val_id, index),
                "case_id": val_id,
                "timepoint": item.timepoint,
                "intake_ml": item.intake_ml,
                "output_ml": item.output_ml,
                "net_ml": item.net_ml,
                "notes": None,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseIntakeOutput, case.id, CaseIntakeOutput.io_id), start=1
            )
        ],
        "CaseDevice": [
            {
                "device_id": _child_id("DEV", val_id, index),
                "case_id": val_id,
                "device_type": item.device_type,
                "site": item.site,
                "placement_timepoint": item.placement_timepoint,
                "status": item.status,
                "tip_location_or_confirmation": item.tip_location_or_confirmation,
                "care_instructions": item.care_instructions,
                "removal_plan": item.removal_plan,
                "source_reference": None,
            }
            for index, item in enumerate(
                _list(session, CaseDevice, case.id, CaseDevice.device_id), start=1
            )
        ],
    }
    return _json_object(payload)


def _investigator_payload(
    session: Session, case: ClinicalCase, frozen: ValidationBatchCase
) -> dict[str, Any]:
    keys = list_answer_keys_for_case(session, case.id)
    if frozen.is_clean_control:
        status = "NO INTENTIONAL ERROR"
        error_block: dict[str, Any] = {
            "control_error_status": "clean_control",
            "error_family": FAMILY_NONE,
            "error_category": NONE,
            "statement": "NO INTENTIONAL ERROR",
        }
    else:
        status = "error_bearing"
        key = keys[0] if keys else None
        changes = None if key is None else key.intentional_changes
        first_change = changes[0] if isinstance(changes, list) and changes else {}
        error_block = {
            "control_error_status": "error_bearing",
            "error_family": frozen.error_family or (None if key is None else key.error_family),
            "error_category": frozen.error_category,
            "error_description": None if key is None else key.error_description,
            "trigger_meds": None if key is None else key.trigger_meds,
            "detectability_location": None if key is None else key.detectability_location,
            "correct_action": None if key is None else key.correct_action,
            "clean_expected_state": frozen.clean_state,
            "injected_state": changes,
            "changed_field": first_change.get("changed_field")
            if isinstance(first_change, dict)
            else None,
            "evidence_required": first_change.get("evidence_required")
            if isinstance(first_change, dict)
            else None,
            "evidence_location": first_change.get("evidence_location")
            if isinstance(first_change, dict)
            else None,
            "severity_ncc_merp": None if key is None else key.severity_ncc_merp,
            "intentional_changes": changes,
            "difficulty_a_priori": None if key is None else key.difficulty_a_priori,
            "affected_medication": None if key is None else key.trigger_meds,
            "rationale": None if key is None else key.error_description,
        }
    return _json_object(
        {
            "validation_case_id": frozen.validation_case_id,
            "internal_case_id_code": case.case_id_code,
            "scenario": frozen.scenario_code,
            "control_error_status": status,
            "error": error_block,
            "supporting_clinical_rules": frozen.rule_snapshot,
            "canonical_identifiers": {
                "rxcuis": sorted(
                    {
                        med_row.rxcui
                        for item in list_medications_for_case(session, case.id)
                        if item.ref_medication_id is not None
                        for med_row in [session.get(RefMedication, item.ref_medication_id)]
                        if med_row is not None
                    }
                ),
                "icd10cm_codes": sorted(
                    {
                        dx_row.icd10cm_code
                        for item in list_diagnoses_for_case(session, case.id)
                        if item.ref_diagnosis_id is not None
                        for dx_row in [session.get(RefDiagnosis, item.ref_diagnosis_id)]
                        if dx_row is not None and dx_row.icd10cm_code
                    }
                ),
                "loinc_codes": sorted(
                    {
                        lab_row.loinc_code
                        for item in list_labs_for_case(session, case.id)
                        if item.ref_lab_id is not None
                        for lab_row in [session.get(RefLabTest, item.ref_lab_id)]
                        if lab_row is not None
                    }
                ),
            },
            "generation_seed": frozen.case_seed,
            "master_seed": frozen.master_seed,
            "generator_version": frozen.generator_version,
            "generator_name": GENERATOR_NAME,
            "reference_snapshot": frozen.reference_snapshot,
            "rule_snapshot": frozen.rule_snapshot,
            "clean_validation": frozen.clean_validation,
            "post_injection_validation": frozen.final_validation,
            "frozen_at": frozen.frozen_at,
            "dataset_status": DATASET_STATUS,
        }
    )


def _reference_snapshot(session: Session) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for code in ("RXNORM", "ICD10CM", "LOINC", "UCUM", "DAILYMED", "RXCLASS"):
        row = get_data_source(session, code)
        payload[code] = (
            None
            if row is None
            else {
                "version": row.version,
                "records_imported": row.records_imported,
                "last_successful_sync_at": row.last_successful_sync_at,
                "sync_status": row.sync_status,
            }
        )
    return _json_object(payload)


def _rule_snapshot(session: Session) -> list[dict[str, Any]]:
    return [
        {
            "rule_code": rule.rule_code,
            "rule_type": rule.rule_type,
            "severity": rule.severity,
            "enabled": rule.enabled,
            "source_system": rule.source_system,
            "source_identifier": rule.source_identifier,
            "source_url": rule.source_url,
        }
        for rule in list_rules(session)
    ]


def _list(session: Session, model: Any, case_id: UUID, order_column: Any) -> list[Any]:
    rows = session.scalars(
        select(model).where(model.case_id == case_id).order_by(order_column.nulls_last())
    ).all()
    return list(rows)


def _json_object(payload: object) -> dict[str, Any]:
    loaded = loads_json(dumps_json(payload))
    if not isinstance(loaded, dict):
        raise TypeError("expected a JSON object")
    return loaded


def _resident_title(case: ClinicalCase, val_id: str) -> str:
    title = case.title or f"{case.specialty or 'inpatient'} case {val_id}"
    if case.case_id_code:
        title = title.replace(case.case_id_code, val_id)
    return title


def _json_has_test_identifier(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_json_has_test_identifier(item) for item in value.values())
    if isinstance(value, list):
        return any(_json_has_test_identifier(item) for item in value)
    if isinstance(value, str):
        return "TEST_" in value
    return False


def _child_id(prefix: str, validation_case_id: str, sequence: int) -> str:
    return format_validation_child_id(prefix, validation_case_id, sequence)


def _passed_flag(payload: dict[str, Any] | None) -> str:
    if payload and payload.get("passed"):
        return "passed"
    return "failed"


def _investigator_markdown(doc: dict[str, Any]) -> str:
    lines = [
        "# Investigator answer key",
        "",
        doc["dataset_status"],
        "",
        f"Batch: `{doc['batch_code']}`",
        "",
    ]
    for item in doc["cases"]:
        lines.append(f"## {item['validation_case_id']}")
        lines.append("")
        lines.append(f"- Scenario: `{item['scenario']}`")
        lines.append(f"- Status: {item['control_error_status']}")
        error = item.get("error") or {}
        if item["control_error_status"] == "NO INTENTIONAL ERROR":
            lines.append("- NO INTENTIONAL ERROR")
        else:
            lines.append(f"- Error family: `{error.get('error_family')}`")
            lines.append(f"- Error category: `{error.get('error_category')}`")
            lines.append(f"- Rationale: {error.get('rationale')}")
        lines.append(f"- Seed: `{item['generation_seed']}`")
        lines.append("")
    return "\n".join(lines) + "\n"


def _coverage_markdown(coverage: dict[str, Any]) -> str:
    lines = [
        "# Resident validation coverage",
        "",
        coverage["dataset_status"],
        "",
        f"TOTAL CASES: {coverage['total_cases']}",
        "",
        "## SCENARIOS",
        "",
    ]
    for name, count in sorted(coverage["scenarios"].items()):
        lines.append(f"- {name} → {count}")
    lines.extend(
        [
            "",
            "## CONTROL STATUS",
            "",
            f"- clean controls → {coverage['clean_controls']}",
            f"- error-bearing → {coverage['error_bearing']}",
            "",
            "## ERROR TYPES",
            "",
        ]
    )
    for name, count in sorted(coverage["error_types"].items()):
        lines.append(f"- {name} → {count}")
    if not coverage["error_types"]:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## TERMINOLOGY COVERAGE",
            "",
            f"- unique medications: {len(coverage['unique_medications'])}",
            f"- unique RXCUIs: {len(coverage['unique_rxcuis'])}",
            f"- unique diagnoses: {len(coverage['unique_diagnoses'])}",
            f"- unique ICD codes: {len(coverage['unique_icd_codes'])}",
            f"- unique labs: {len(coverage['unique_labs'])}",
            f"- unique LOINC codes: {len(coverage['unique_loinc_codes'])}",
            f"- unique UCUM units: {len(coverage['unique_ucum_units'])}",
            "",
            "## LOINC COVERAGE",
            "",
            f"- cases with LOINC-backed labs: {coverage['loinc_backed_lab_cases']}",
            f"- LOINC concepts used: {', '.join(coverage['unique_loinc_codes']) or '(none)'}",
            "",
            "## RULE COVERAGE",
            "",
        ]
    )
    for rule in coverage["rules"]:
        exercised = coverage["rule_coverage"].get(rule["rule_code"], 0)
        state = "enabled" if rule["enabled"] else "disabled"
        lines.append(
            f"- {rule['rule_code']} ({rule['severity']}, {state}, "
            f"source={rule['source_system'] or 'none'}): {exercised} cases"
        )
    validation = coverage.get("validation") or {}
    lines.extend(
        [
            "",
            "## VALIDATION",
            "",
            f"- clean cases passed: {validation.get('clean_passed')}",
            f"- final frozen cases: {validation.get('frozen_count')}",
            (
                "- cases with exactly one intended error: "
                f"{validation.get('exactly_one_intended_error')}"
            ),
            f"- unexpected-error count: {validation.get('unexpected_additional_errors')}",
            "",
        ]
    )
    return "\n".join(lines)


def _scenario_matrix_markdown(session: Session) -> str:
    lines = [
        "# Internal scenario coverage matrix",
        "",
        "Resolved from local source-backed reference rows. Hidden answer data is not included.",
        "",
    ]
    for scenario in load_scenarios():
        diagnoses = [
            _resolved_label(match_diagnosis(session, query), "preferred_name", "icd10cm_code")
            for query in scenario.diagnosis_queries
        ]
        medications = [
            _resolved_label(match_medication(session, query), "concept_name", "rxcui")
            for query in scenario.medication_queries
        ]
        labs = [
            _resolved_label(match_lab(session, query), "long_common_name", "loinc_code")
            for query in scenario.lab_queries
        ]
        enabled = [rule.rule_code for rule in list_enabled_rules(session)]
        error_types = scenario.allowed_error_categories or [scenario.target_error_category]
        lines.extend(
            [
                f"## {scenario.code}",
                "",
                f"- context: {scenario.care_context} / {scenario.specialty}",
                f"- diagnoses: {', '.join(diagnoses) or '(unresolved)'}",
                f"- medications: {', '.join(medications) or '(unresolved)'}",
                f"- labs: {', '.join(labs) or '(none)'}",
                "- units: scenario uses UCUM-backed case units where present",
                (
                    "- enabled rules in the local rule table: "
                    + (", ".join(enabled) or "(none enabled)")
                ),
                f"- possible error types: {', '.join(error_types)}",
                "- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def _resolved_label(row: Any, name_attr: str, code_attr: str) -> str:
    if row is None:
        return "(unresolved)"
    name = getattr(row, name_attr, None) or "(unnamed)"
    code = getattr(row, code_attr, None) or "(no code)"
    return f"{name} [{code}]"


def _worksheet_csv(rows: list[ValidationBatchCase]) -> str:
    header = (
        "validation_case_id,reviewer_id,clinical_realism_rating,"
        "medication_reconciliation_correctness_rating,case_clarity_rating,"
        "identified_error_type,identified_affected_medication,confidence_rating,"
        "free_text_comments,overall_acceptability,revision_recommendation"
    )
    lines = [header]
    for row in rows:
        lines.append(f"{row.validation_case_id},,,,,,,,,,")
    return "\n".join(lines) + "\n"


def _review_schema() -> dict[str, Any]:
    return {
        "title": "Resident review worksheet",
        "description": (
            "Capture clinician ratings for machine-validated synthetic cases. "
            "Do not collect identifying personal information unless a study protocol requires it."
        ),
        "fields": [
            {"name": "validation_case_id", "type": "string"},
            {"name": "reviewer_id", "type": "string", "description": "pseudonymous reviewer code"},
            {"name": "clinical_realism_rating", "type": "integer", "range": [1, 5]},
            {
                "name": "medication_reconciliation_correctness_rating",
                "type": "integer",
                "range": [1, 5],
            },
            {"name": "case_clarity_rating", "type": "integer", "range": [1, 5]},
            {"name": "identified_error_type", "type": "string"},
            {"name": "identified_affected_medication", "type": "string"},
            {"name": "confidence_rating", "type": "integer", "range": [1, 5]},
            {"name": "free_text_comments", "type": "string"},
            {"name": "overall_acceptability", "type": "string"},
            {"name": "revision_recommendation", "type": "string"},
        ],
    }
