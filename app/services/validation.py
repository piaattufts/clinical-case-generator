"""Deterministic validation layers for synthetic cases.

Layers: structural, terminology, clinical rules, and assessment consistency.
Family 1 checks medication-plan mutations. Family 2 checks trigger-plus-missing-action
gaps. External APIs are not called on ordinary case reads.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.orm import Session

from app.models.cases import (
    CaseDischargePlanning,
    CaseImaging,
    CaseMedication,
    CaseMicrobiology,
    CaseSocialSupport,
    ClinicalCase,
)
from app.models.generation import CaseMedicationPlan
from app.models.reference import RefDiagnosis, RefLabTest, RefMedication
from app.repositories.cases import (
    list_answer_keys_for_case,
    list_diagnoses_for_case,
    list_labs_for_case,
    list_medications_for_case,
    list_monitoring_for_case,
    list_plans_for_case,
)
from app.repositories.reference import (
    get_diagnosis_by_icd10cm,
    get_lab_test_by_loinc,
    get_medication_by_rxcui,
    get_unit_by_ucum,
)
from app.services.clinical_coherence import (
    dose_compatible_with_form,
    implausible_lab_errors,
    indication_matches_problems,
    resident_leak_hits,
    route_compatible_with_form,
)
from app.services.error_taxonomy import (
    F1_COMMISSION,
    F1_DOSE,
    F1_FREQUENCY,
    F1_ROUTE,
    F2_HOSPITAL_ONLY,
    F2_INPATIENT_SUB,
    NONE,
    canonicalize_category,
    detect_findings,
    isolation_errors,
)
from app.services.medication_regimens import (
    beta_blocker_frequency_conflicts,
    echo_course_statement,
    endocarditis_microbiology_conflicts,
    imaging_timepoint_conflict,
    living_disposition_conflict,
    regimen_field_conflicts,
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
    expected_category: str | None = None,
) -> ValidationReport:
    snapshot = snapshot_from_case(session, case)
    structural = _structural(session, case)
    terminology = _terminology(session, case)
    clinical = _clinical(session, snapshot)
    coherence = _clinical_coherence(
        session,
        case,
        expected_category=expected_category,
        expect_injected_error=expect_injected_error,
    )
    plan_layer = _assessment_consistency(
        session,
        case,
        expect_injected_error=expect_injected_error,
        expected_category=expected_category,
    )
    report = ValidationReport(
        case_id_code=case.case_id_code,
        layers=[structural, terminology, clinical, coherence, plan_layer],
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


def _clinical_coherence(
    session: Session,
    case: ClinicalCase,
    *,
    expected_category: str | None,
    expect_injected_error: bool,
) -> LayerResult:
    errors: list[str] = []
    problems = [
        item.diagnosis
        for item in list_diagnoses_for_case(session, case.id)
        if item.diagnosis
    ]
    planted_category = canonicalize_category(expected_category) if expected_category else NONE
    keys = list_answer_keys_for_case(session, case.id)
    if keys:
        planted_category = canonicalize_category(keys[0].error_category)
    for lab in list_labs_for_case(session, case.id):
        errors.extend(implausible_lab_errors(lab.test_name, lab.value, lab.unit))
    for medication in list_medications_for_case(session, case.id):
        med_row = (
            session.get(RefMedication, medication.ref_medication_id)
            if medication.ref_medication_id is not None
            else None
        )
        skip_route = (
            expect_injected_error
            and planted_category == F1_ROUTE
            and medication.context == "discharge"
        )
        skip_dose = (
            expect_injected_error
            and planted_category in {F1_DOSE, F1_ROUTE}
            and medication.context == "discharge"
        )
        if med_row is not None and not skip_route:
            if not route_compatible_with_form(medication.route, med_row):
                errors.append(
                    f"route {medication.route!r} is incompatible with "
                    f"{med_row.dose_form or med_row.concept_name}"
                )
            if not skip_dose and not dose_compatible_with_form(medication.dose, med_row):
                errors.append(
                    f"dose {medication.dose!r} is incompatible with "
                    f"{med_row.dose_form or med_row.concept_name}"
                )
        if medication.indication and problems:
            if not indication_matches_problems(medication.indication, problems):
                if "formulary substitution" not in (medication.indication or "").casefold():
                    if "inpatient-only" not in (medication.indication or "").casefold():
                        if "not a treatment for the admission diagnosis" not in (
                            medication.indication or ""
                        ).casefold():
                            errors.append(
                                f"indication {medication.indication!r} is not represented "
                                "on the case problem list"
                            )
    leak_fields = [
        case.chief_complaint,
        case.one_liner,
        case.admission_dx,
    ]
    leak_fields.extend(
        item.notes for item in list_medications_for_case(session, case.id) if item.notes
    )
    from sqlalchemy import select

    from app.models.cases import CaseInstruction, CaseNote, CasePresentation

    presentation = session.scalars(
        select(CasePresentation).where(CasePresentation.case_id == case.id)
    ).first()
    if presentation is not None:
        leak_fields.extend([presentation.chief_complaint, presentation.hpi])
    for note in session.scalars(select(CaseNote).where(CaseNote.case_id == case.id)):
        leak_fields.append(note.note_text)
    for instruction in session.scalars(
        select(CaseInstruction).where(CaseInstruction.case_id == case.id)
    ):
        leak_fields.append(instruction.instruction_text)
    blob = "\n".join(part for part in leak_fields if part)
    for hit in resident_leak_hits(blob):
        errors.append(f"resident-facing text leaked {hit!r}")
    inpatient_by_ref = {
        item.ref_medication_id: item
        for item in list_medications_for_case(session, case.id)
        if item.context == "inpatient" and item.ref_medication_id is not None
    }
    for medication in list_medications_for_case(session, case.id):
        ref_id = medication.ref_medication_id
        if ref_id is None:
            continue
        med_row = session.get(RefMedication, ref_id)
        if med_row is None:
            continue
        inpatient = inpatient_by_ref.get(ref_id)
        skip_dose = _planted_field_changed(
            medication, inpatient, planted_category, F1_DOSE, "dose"
        )
        skip_route = _planted_field_changed(
            medication, inpatient, planted_category, F1_ROUTE, "route"
        )
        skip_frequency = _planted_field_changed(
            medication, inpatient, planted_category, F1_FREQUENCY, "frequency"
        )
        for message in regimen_field_conflicts(
            med_row,
            dose=None if skip_dose else medication.dose,
            route=None if skip_route else medication.route,
            frequency=None if skip_frequency else medication.frequency,
        ):
            if skip_dose and message.startswith("dose "):
                continue
            if skip_route and message.startswith("route "):
                continue
            if skip_frequency and message.startswith("frequency "):
                continue
            errors.append(message)
        if not skip_frequency:
            conflicts = beta_blocker_frequency_conflicts(
                med_row.concept_name,
                medication.frequency,
            )
            for message in conflicts:
                errors.append(message)
    errors.extend(_temporal_role_errors(session, case, planted_category))
    errors.extend(_diagnostic_context_errors(session, case, problems))
    has_monitoring = bool(list_monitoring_for_case(session, case.id))
    if re.search(
        r"\b(?:scheduled laboratory monitoring|monitoring was arranged|"
        r"inr monitoring was arranged)\b",
        blob,
        flags=re.IGNORECASE,
    ) and not has_monitoring:
        errors.append(
            "narrative claims monitoring was arranged but no monitoring row is stored"
        )
    return LayerResult("clinical_coherence", passed=not errors, errors=errors)


def _clinical(session: Session, snapshot: CaseSnapshot) -> LayerResult:
    hits = evaluate_rules(session, snapshot)
    errors = [item.message for item in hard_violations(hits)]
    warnings = [item.message for item in hits if item.severity != "hard"]
    return LayerResult("clinical", passed=not errors, errors=errors, warnings=warnings)


def _assessment_consistency(
    session: Session,
    case: ClinicalCase,
    *,
    expect_injected_error: bool,
    expected_category: str | None,
) -> LayerResult:
    errors: list[str] = []
    warnings: list[str] = []
    keys = list_answer_keys_for_case(session, case.id)
    plans = list_plans_for_case(session, case.id)
    findings = detect_findings(session, case)
    if expect_injected_error:
        if len(keys) != 1:
            errors.append("expected exactly one answer key for an error-bearing case")
        else:
            if keys[0].is_primary_error is False:
                errors.append("answer key is not marked as the primary error")
            key_category = canonicalize_category(keys[0].error_category)
            if expected_category is not None:
                requested = canonicalize_category(expected_category)
                if key_category != requested:
                    errors.append(
                        f"answer-key category {key_category!r} != requested category {requested!r}"
                    )
            isolation = isolation_errors(
                session,
                case,
                expected_category=expected_category or (keys[0].error_category or NONE),
            )
            errors.extend(isolation)
            if keys[0].error_family is None:
                errors.append("answer key is missing error_family")
        targets = [plan for plan in plans if plan.is_error_target]
        if expected_category is not None and canonicalize_category(expected_category) == NONE:
            errors.append("error-bearing validation was requested for category none")
        elif len(targets) < 1:
            warnings.append("no medication plan marked as the error target")
        clinician = (
            "clinician validation still required for clinical coherence, "
            "error fidelity, evidentiary sufficiency, error isolation, "
            "cue integrity, and educational appropriateness"
        )
        warnings.append(clinician)
    else:
        if findings:
            errors.append(
                "clean case has mechanically detectable discrepancies before injection: "
                + "; ".join(f"{item.category}:{item.drug or item.rxcui}" for item in findings)
            )
        if keys:
            errors.append("clean case must not have an answer key")
        if any(plan.is_error_target for plan in plans):
            warnings.append("clean case plan has is_error_target set")
        if case.clean_case is False:
            errors.append("clean case flag is false before injection")
    return LayerResult("assessment", passed=not errors, errors=errors, warnings=warnings)


def _planted_field_changed(
    medication: CaseMedication,
    inpatient: CaseMedication | None,
    planted_category: str,
    category: str,
    field_name: str,
) -> bool:
    if medication.context != "discharge" or planted_category != category or inpatient is None:
        return False
    return (getattr(inpatient, field_name) or "") != (getattr(medication, field_name) or "")


_STARTED_HPI_RE = re.compile(
    r"Started during this admission:\s*([^.]+)\.",
    re.IGNORECASE,
)
_HOSPITAL_ONLY_HPI_RE = re.compile(
    r"(?:Used only in the hospital and stopped at discharge|"
    r"Started during the hospitalization):\s*([^.]+)\.",
    re.IGNORECASE,
)
_DISCONTINUED_HPI_RE = re.compile(
    r"([^.]+?) was (?:"
    r"discontinued and is not intended at discharge|"
    r"stopped during this admission"
    r")\.",
    re.IGNORECASE,
)


def _split_chart_names(blob: str) -> list[str]:
    return [part.strip() for part in blob.split(",") if part.strip()]


def _same_drug_name(left: str | None, right: str | None) -> bool:
    return bool(left and right and left.casefold().strip() == right.casefold().strip())


def _answer_rxcuis_for_role(session: Session, case: ClinicalCase, role: str | None) -> set[str]:
    found: set[str] = set()
    for key in list_answer_keys_for_case(session, case.id):
        triggers = key.trigger_meds if isinstance(key.trigger_meds, list) else []
        for item in triggers:
            if not isinstance(item, dict) or not item.get("rxcui"):
                continue
            if role is None or item.get("role") == role:
                found.add(str(item["rxcui"]))
        changes = key.intentional_changes if isinstance(key.intentional_changes, list) else []
        for item in changes:
            if role is not None:
                continue
            if isinstance(item, dict) and item.get("rxcui"):
                found.add(str(item["rxcui"]))
    return found


def _temporal_role_errors(
    session: Session, case: ClinicalCase, planted_category: str
) -> list[str]:
    errors: list[str] = []
    medications = list_medications_for_case(session, case.id)
    substitute_rxcuis = (
        _answer_rxcuis_for_role(session, case, "inpatient_substitute")
        if planted_category == F2_INPATIENT_SUB
        else set()
    )
    planted_rxcuis = _answer_rxcuis_for_role(session, case, None)
    for plan in list_plans_for_case(session, case.id):
        rows = [
            item
            for item in medications
            if item.ref_medication_id == plan.ref_medication_id
        ]
        home_rows = [item for item in rows if item.context == "home"]
        active_discharge = [
            item
            for item in rows
            if item.context == "discharge" and item.status != "held"
        ]
        if plan.home_state == "absent" and home_rows:
            errors.append(
                f"{plan.drug or 'medication'} is described as absent from home "
                "but a home medication row is present"
            )
        stopped_on_discharge = plan.correct_discharge_state == "stop" and bool(active_discharge)
        planted_explains = planted_category in {F2_HOSPITAL_ONLY, F1_COMMISSION}
        if stopped_on_discharge and planted_category == F2_INPATIENT_SUB:
            plan_rxcui = _rxcui_for_medication(session, active_discharge[0])
            planted_explains = bool(plan_rxcui and plan_rxcui in substitute_rxcuis)
        if stopped_on_discharge and not planted_explains:
            errors.append(
                f"{plan.drug or 'medication'} remains active at discharge after a stop plan"
            )
        for row in rows:
            note = (row.notes or "").casefold()
            if "started during this admission" in note and row.context == "home":
                errors.append(
                    f"{plan.drug or row.drug or 'medication'} was started during the admission "
                    "but is listed as a home medication"
                )
    errors.extend(
        _narrative_temporal_errors(
            session,
            case,
            medications,
            planted_category=planted_category,
            planted_rxcuis=planted_rxcuis,
        )
    )
    return errors


def _narrative_temporal_errors(
    session: Session,
    case: ClinicalCase,
    medications: list[CaseMedication],
    *,
    planted_category: str,
    planted_rxcuis: set[str],
) -> list[str]:
    from sqlalchemy import select

    from app.models.cases import CasePresentation

    presentation = session.scalars(
        select(CasePresentation).where(CasePresentation.case_id == case.id)
    ).first()
    hpi = presentation.hpi if presentation is not None else ""
    if not hpi:
        return []
    errors: list[str] = []
    home_rows = [item for item in medications if item.context == "home"]
    discharge_rows = [
        item
        for item in medications
        if item.context == "discharge" and item.status != "held"
    ]
    started_match = _STARTED_HPI_RE.search(hpi)
    if started_match:
        for name in _split_chart_names(started_match.group(1)):
            if any(_same_drug_name(name, item.drug) for item in home_rows):
                errors.append(
                    f"{name} was started during the admission but is listed as a home medication"
                )
    hospital_match = _HOSPITAL_ONLY_HPI_RE.search(hpi)
    if hospital_match:
        for name in _split_chart_names(hospital_match.group(1)):
            for item in discharge_rows:
                if not _same_drug_name(name, item.drug):
                    continue
                rxcui = _rxcui_for_medication(session, item)
                if planted_category == F2_HOSPITAL_ONLY and rxcui in planted_rxcuis:
                    continue
                errors.append(
                    f"{name} is described as hospital-only but remains on the discharge list"
                )
    stopped_match = _DISCONTINUED_HPI_RE.search(hpi)
    if stopped_match:
        for name in _split_chart_names(stopped_match.group(1)):
            for item in discharge_rows:
                if not _same_drug_name(name, item.drug):
                    continue
                rxcui = _rxcui_for_medication(session, item)
                if planted_category == F1_COMMISSION and rxcui in planted_rxcuis:
                    continue
                errors.append(
                    f"{name} was discontinued but remains an active discharge therapy"
                )
    return errors


def _diagnostic_context_errors(
    session: Session, case: ClinicalCase, problems: list[str]
) -> list[str]:
    from sqlalchemy import select

    errors: list[str] = []
    for image in session.scalars(select(CaseImaging).where(CaseImaging.case_id == case.id)):
        conflict = imaging_timepoint_conflict(image.timepoint, image.finding)
        if conflict:
            errors.append(conflict)
        study = (image.study_type or "").casefold()
        if "echo" in study and echo_course_statement(image.finding):
            errors.append(
                "echocardiogram finding states a treatment course instead of an imaging finding: "
                f"{image.finding}"
            )
    problem_blob = " ".join(problems).casefold()
    if "endocarditis" in problem_blob:
        micro_rows = [
            {
                "timepoint": item.timepoint or "",
                "result": item.result or "",
                "organism": item.organism or "",
                "status": item.status or "",
                "notes": item.notes or "",
            }
            for item in session.scalars(
                select(CaseMicrobiology).where(CaseMicrobiology.case_id == case.id)
            )
        ]
        errors.extend(endocarditis_microbiology_conflicts(micro_rows))
    social = session.scalars(
        select(CaseSocialSupport).where(CaseSocialSupport.case_id == case.id)
    ).first()
    planning = session.scalars(
        select(CaseDischargePlanning).where(CaseDischargePlanning.case_id == case.id)
    ).first()
    if social is not None and planning is not None:
        conflict = living_disposition_conflict(social.living_situation, planning.disposition)
        if conflict:
            errors.append(conflict)
    return errors


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
