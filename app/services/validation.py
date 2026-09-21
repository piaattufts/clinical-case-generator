"""Deterministic validation layers for synthetic cases.

Layers: structural, terminology, clinical rules, and medication-plan consistency.
External APIs are not called on ordinary case reads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.orm import Session

from app.models.cases import CaseMedication, ClinicalCase
from app.models.generation import CaseMedicationPlan
from app.models.reference import RefDiagnosis, RefLabTest, RefMedication
from app.repositories.cases import (
    list_answer_keys_for_case,
    list_diagnoses_for_case,
    list_labs_for_case,
    list_medications_for_case,
    list_plans_for_case,
)
from app.repositories.reference import (
    get_diagnosis_by_icd10cm,
    get_lab_test_by_loinc,
    get_medication_by_rxcui,
    get_unit_by_ucum,
)
from app.services.rules import CaseSnapshot, RuleViolation, evaluate_rules, hard_violations
from app.sources.exceptions import CaseValidationError
from app.utils.identifiers import CASE_CODE_RE

MEDICATION_CONTEXTS = frozenset({"home", "inpatient", "inpatient_history", "discharge"})
MEDICATION_STATUSES = frozenset({"home", "active", "held", "discontinued", "discharge"})
PLAN_DECISIONS = frozenset({"continue", "stop", "restart", "hold", "dose_change", "new_start"})


@dataclass
class LayerResult:
    layer: str
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    case_id_code: str
    layers: list[LayerResult]
    rules: list[RuleViolation] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(layer.passed for layer in self.layers)

    def errors(self) -> list[str]:
        found: list[str] = []
        for layer in self.layers:
            found.extend(f"{layer.layer}: {item}" for item in layer.errors)
        return found


def validate_case(
    session: Session,
    case: ClinicalCase,
    *,
    expect_injected_error: bool = False,
) -> ValidationReport:
    snapshot = snapshot_from_case(session, case)
    structural = _structural(session, case)
    terminology = _terminology(session, case)
    clinical = _clinical(session, snapshot)
    plan_layer = _plan_consistency(session, case, expect_injected_error=expect_injected_error)
    report = ValidationReport(
        case_id_code=case.case_id_code,
        layers=[structural, terminology, clinical, plan_layer],
        rules=evaluate_rules(session, snapshot),
    )
    return report


def require_valid(report: ValidationReport) -> None:
    if report.passed:
        return
    details = report.errors()
    raise CaseValidationError("case", details[0] if details else "validation failed", details)


def snapshot_from_case(session: Session, case: ClinicalCase) -> CaseSnapshot:
    rxcuis: set[str] = set()
    for medication in list_medications_for_case(session, case.id):
        rxcui = _rxcui_for_medication(session, medication)
        if rxcui is not None:
            rxcuis.add(rxcui)
    icd_codes: set[str] = set()
    for diagnosis in list_diagnoses_for_case(session, case.id):
        if diagnosis.ref_diagnosis_id is None:
            continue
        dx_row = session.get(RefDiagnosis, diagnosis.ref_diagnosis_id)
        if dx_row is not None and dx_row.icd10cm_code:
            icd_codes.add(dx_row.icd10cm_code)
    loinc_codes: set[str] = set()
    for lab in list_labs_for_case(session, case.id):
        if lab.ref_lab_id is None:
            continue
        lab_ref = session.get(RefLabTest, lab.ref_lab_id)
        if lab_ref is not None:
            loinc_codes.add(lab_ref.loinc_code)
    return CaseSnapshot(
        age=case.patient_age,
        sex=case.patient_gender,
        care_context="inpatient",
        icd10cm_codes=frozenset(icd_codes),
        rxcuis=frozenset(rxcuis),
        loinc_codes=frozenset(loinc_codes),
    )


def _structural(session: Session, case: ClinicalCase) -> LayerResult:
    errors: list[str] = []
    if CASE_CODE_RE.fullmatch(case.case_id_code) is None:
        errors.append(f"case_id_code {case.case_id_code!r} is not SYN-000001 format")
    for medication in list_medications_for_case(session, case.id):
        if medication.context is not None and medication.context not in MEDICATION_CONTEXTS:
            errors.append(f"invalid medication context {medication.context!r}")
        if medication.status is not None and medication.status not in MEDICATION_STATUSES:
            errors.append(f"invalid medication status {medication.status!r}")
        if medication.case_id != case.id:
            errors.append("medication case_id does not match parent case")
    for plan in list_plans_for_case(session, case.id):
        if plan.decision is not None and plan.decision not in PLAN_DECISIONS:
            errors.append(f"invalid plan decision {plan.decision!r}")
    if not list_diagnoses_for_case(session, case.id):
        errors.append("case has no diagnosis row")
    return LayerResult("structural", passed=not errors, errors=errors)


def _terminology(session: Session, case: ClinicalCase) -> LayerResult:
    errors: list[str] = []
    for medication in list_medications_for_case(session, case.id):
        if medication.ref_medication_id is None:
            errors.append(f"medication {medication.drug!r} is missing a reference link")
            continue
        med_row = session.get(RefMedication, medication.ref_medication_id)
        if med_row is None:
            errors.append("medication reference id does not resolve")
            continue
        if _looks_invented(med_row.rxcui) and not med_row.rxcui.startswith("TEST_"):
            errors.append(f"unsupported invented identifier {med_row.rxcui!r}")
        if med_row.source_system is None:
            errors.append(f"RXCUI {med_row.rxcui} has no source provenance")
        claimed = _claimed_rxcui(medication)
        if claimed is not None and get_medication_by_rxcui(session, claimed) is None:
            errors.append(f"RXCUI {claimed} is not present in local RxNorm reference data")
    for diagnosis in list_diagnoses_for_case(session, case.id):
        if diagnosis.ref_diagnosis_id is None:
            errors.append("diagnosis is missing a reference link")
            continue
        dx_row = session.get(RefDiagnosis, diagnosis.ref_diagnosis_id)
        if dx_row is None:
            errors.append("diagnosis reference id does not resolve")
            continue
        if dx_row.icd10cm_code and get_diagnosis_by_icd10cm(session, dx_row.icd10cm_code) is None:
            errors.append(f"ICD-10-CM {dx_row.icd10cm_code} is not in local reference data")
        if dx_row.source_system is None:
            errors.append("diagnosis row has no source provenance")
        code = dx_row.icd10cm_code
        if code and _looks_invented(code) and not code.startswith("TEST_"):
            errors.append(f"unsupported invented identifier {code!r}")
    for lab in list_labs_for_case(session, case.id):
        if lab.ref_lab_id is None:
            errors.append(f"lab {lab.test_name!r} is missing a reference link")
            continue
        lab_row = session.get(RefLabTest, lab.ref_lab_id)
        if lab_row is None:
            errors.append("lab reference id does not resolve")
            continue
        if get_lab_test_by_loinc(session, lab_row.loinc_code) is None:
            errors.append(f"LOINC {lab_row.loinc_code} is not in local reference data")
        if lab_row.source_system is None:
            errors.append(f"LOINC {lab_row.loinc_code} has no source provenance")
        if lab.unit:
            allowed_examples = {
                str(item) for item in (lab_row.example_ucum_units or []) if item is not None
            }
            unit_row = get_unit_by_ucum(session, lab.unit)
            if unit_row is None and lab.unit not in allowed_examples:
                errors.append(
                    f"unit {lab.unit!r} is not a source-backed UCUM or LOINC example unit"
                )
            if unit_row is not None and unit_row.source_system is None:
                errors.append(f"UCUM {lab.unit} has no source provenance")
    return LayerResult("terminology", passed=not errors, errors=errors)


def _clinical(session: Session, snapshot: CaseSnapshot) -> LayerResult:
    hits = evaluate_rules(session, snapshot)
    errors = [item.message for item in hard_violations(hits)]
    warnings = [item.message for item in hits if item.severity != "hard"]
    return LayerResult("clinical", passed=not errors, errors=errors, warnings=warnings)


def _plan_consistency(
    session: Session,
    case: ClinicalCase,
    *,
    expect_injected_error: bool,
) -> LayerResult:
    errors: list[str] = []
    warnings: list[str] = []
    plans = list_plans_for_case(session, case.id)
    discharge = [
        item for item in list_medications_for_case(session, case.id) if item.context == "discharge"
    ]
    discharge_ids = {item.ref_medication_id for item in discharge if item.ref_medication_id}
    discrepancies = 0
    for plan in plans:
        should_be_present = plan.correct_discharge_state == "continue"
        present = plan.ref_medication_id in discharge_ids
        if should_be_present and not present:
            discrepancies += 1
        if present and plan.correct_discharge_state == "stop":
            discrepancies += 1
    keys = list_answer_keys_for_case(session, case.id)
    if expect_injected_error:
        if discrepancies != 1:
            errors.append(
                f"expected exactly one medication-reconciliation discrepancy, found {discrepancies}"
            )
        if len(keys) != 1:
            errors.append("expected exactly one answer key for an error-bearing case")
        if keys and keys[0].is_primary_error is False:
            errors.append("answer key is not marked as the primary error")
        targets = [plan for plan in plans if plan.is_error_target]
        if len(targets) != 1:
            errors.append("expected exactly one medication plan marked as the error target")
    else:
        if discrepancies != 0:
            errors.append(
                f"clean case has {discrepancies} medication-plan discrepancies before injection"
            )
        if keys:
            errors.append("clean case must not have an answer key")
        if any(plan.is_error_target for plan in plans):
            warnings.append("clean case plan has is_error_target set")
    return LayerResult("medication_plan", passed=not errors, errors=errors, warnings=warnings)


def _rxcui_for_medication(session: Session, medication: CaseMedication) -> str | None:
    if medication.ref_medication_id is None:
        return _claimed_rxcui(medication)
    row = session.get(RefMedication, medication.ref_medication_id)
    return row.rxcui if row is not None else _claimed_rxcui(medication)


def _claimed_rxcui(medication: CaseMedication) -> str | None:
    text = medication.source_reference
    if text is None:
        return None
    prefix = "RXCUI:"
    if text.startswith(prefix):
        code = text[len(prefix) :].strip()
        return code or None
    return None


def _looks_invented(value: str) -> bool:
    lowered = value.casefold()
    return lowered.startswith("fake_") or lowered.startswith("invented_")


def serialize_report(report: ValidationReport) -> dict[str, Any]:
    return {
        "case_id_code": report.case_id_code,
        "passed": report.passed,
        "errors": report.errors(),
        "layers": [
            {
                "layer": layer.layer,
                "passed": layer.passed,
                "errors": layer.errors,
                "warnings": layer.warnings,
            }
            for layer in report.layers
        ],
        "rules": [
            {
                "rule_code": item.rule_code,
                "severity": item.severity,
                "message": item.message,
            }
            for item in report.rules
        ],
    }


def plan_for_rxcui(session: Session, plan: CaseMedicationPlan) -> str | None:
    if plan.ref_medication_id is None:
        return None
    row = session.get(RefMedication, plan.ref_medication_id)
    return row.rxcui if row is not None else None
