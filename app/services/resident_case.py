"""Resident-facing charts versus the hidden discharge reference.

The resident task is to decide the discharge regimen from the clinical chart.
The correct discharge plan stays on CaseMedicationPlan and discharge medication
rows. Those rows are not part of the resident-facing document.

Deliberate chart errors belong to a later AI-intervention experiment. They are
not part of this representation.
"""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cases import (
    CaseDiagnosis,
    CaseDischargePlanning,
    CaseLab,
    CaseMedication,
    CaseNote,
    CasePresentation,
    CaseVital,
    ClinicalCase,
)
from app.models.generation import CaseMedicationPlan
from app.models.reference import RefMedication
from app.repositories.cases import (
    list_followups_for_case,
    list_instructions_for_case,
    list_medications_for_case,
    list_monitoring_for_case,
    list_plans_for_case,
)
from app.repositories.reference import list_enabled_rules
from app.services.medication_decisions import (
    CLINICALLY_INCONSISTENT,
    consider_source_backed_change,
    consistency_errors,
    documented_allergies,
    evidence_payload,
    evidence_trace,
    justify_home_medication,
    justify_hospital_start,
    justify_visible_stop,
    public_action,
)
from app.services.medication_regimens import regimen_for_text
from app.services.validation_registry import all_batch_specs
from app.utils.jsonio import dumps_json

_REQUIRED_ACTIONS = frozenset({"continue", "start", "change", "restart"})
_STORED_DECISIONS = frozenset(
    {"continue", "stop", "restart", "hold", "dose_change", "new_start"}
)
_RESIDENT_CONTEXTS = frozenset({"home", "inpatient", "inpatient_history"})
_ANSWER_KEYS = frozenset(
    {
        "reference_discharge_plan",
        "correct_discharge_state",
        "decision_reason",
        "is_error_target",
        "answer_key",
        "intentional_changes",
        "injected_state",
        "error_category",
        "error_family",
        "correct_action",
    }
)
_LISTED_DISCHARGE_INSTRUCTION = "exactly as listed"


def reference_discharge_plan(session: Session, case: ClinicalCase) -> dict[str, Any]:
    """Build the hidden scoring standard from the stored clean plan."""
    plans = list_plans_for_case(session, case.id)
    rows = list_medications_for_case(session, case.id)
    by_ref = _rows_by_reference(rows)
    diagnosis_names = [item.diagnosis for item in _diagnoses(session, case) if item.diagnosis]
    creatinine, creatinine_unit = _named_lab(session, case, "creatinine")
    potassium, potassium_unit = _named_lab(session, case, "potassium")
    peptide, peptide_unit = _named_lab(session, case, "natriuretic")
    systolic = _named_systolic(session, case)
    heart_rate = _named_heart_rate(session, case)
    monitoring = [
        {
            "parameter": item.parameter,
            "frequency": item.frequency,
            "target": item.target,
            "duration": item.duration,
        }
        for item in list_monitoring_for_case(session, case.id)
    ]
    visible = _resident_visible_text(session, case)
    allergies = documented_allergies([visible])
    names = [plan.drug or "" for plan in plans]
    medications: list[dict[str, Any]] = []
    to_stop: list[str] = []
    for plan in plans:
        action = public_action(plan.decision)
        source = _source_row(plan, by_ref)
        name = plan.drug or (None if source is None else source.drug) or ""
        explained = _explain_plan(
            name,
            plan.decision,
            diagnosis_names,
            creatinine=creatinine,
            creatinine_unit=creatinine_unit,
            potassium=potassium,
            potassium_unit=potassium_unit,
            systolic_bp=systolic,
            natriuretic_peptide=peptide,
            natriuretic_unit=peptide_unit,
            heart_rate=heart_rate,
            dose=None if source is None else source.dose,
            route=None if source is None else source.route,
            frequency=None if source is None else source.frequency,
            visible_reason=None if source is None else source.held_reason,
            course_text=_hospital_course(session, case),
            rule_codes=_allow_rule_codes(session, plan.ref_medication_id),
        )
        trace = evidence_trace(explained)
        evidence_class = explained.evidence_class
        if explained.include and trace["discharge_action"] != action:
            evidence_class = CLINICALLY_INCONSISTENT
        elif not explained.include and action not in {"", "omit"}:
            evidence_class = explained.evidence_class
        problems = consistency_errors(
            medication=name,
            action=action,
            indication=None if source is None else source.indication,
            diagnosis_names=diagnosis_names,
            admission_diagnosis=case.admission_dx,
            monitoring_parameters=[str(item.get("parameter") or "") for item in monitoring],
            medication_names=names,
            allergies=allergies,
            visible_text=visible,
            temporal_role=_temporal_role(name),
        )
        if problems and evidence_class == "SUFFICIENT_EVIDENCE":
            evidence_class = CLINICALLY_INCONSISTENT
        trace["evidence_class"] = evidence_class
        trace["discharge_action"] = action
        entry = {
            "medication": name,
            "action": action,
            "dose": None if source is None else source.dose,
            "route": None if source is None else source.route,
            "frequency": None if source is None else source.frequency,
            "duration": None if source is None else source.quantity_or_days,
            "indication": None if source is None else source.indication,
            "rationale": plan.decision_reason,
            "required": action in _REQUIRED_ACTIONS,
            "evidence_class": evidence_class,
            "supporting_evidence": evidence_payload(explained),
            "evidence_trace": trace,
            "consistency_errors": problems,
        }
        medications.append(entry)
        if action == "stop" and name:
            to_stop.append(name)
    return {
        "medications": medications,
        "medications_to_stop": to_stop,
        "acceptable_alternatives": [],
        "contraindications": [],
        "monitoring_requirements": monitoring,
        "follow_up_requirements": [
            {"item": item.item, "timing": item.timing, "with_service": item.with_service}
            for item in list_followups_for_case(session, case.id)
        ],
    }


def resident_case_document(session: Session, case: ClinicalCase) -> dict[str, Any]:
    """Clinical chart for the resident. The discharge regimen is omitted."""
    presentation = session.scalar(
        select(CasePresentation).where(CasePresentation.case_id == case.id)
    )
    discharge = session.scalar(
        select(CaseDischargePlanning).where(CaseDischargePlanning.case_id == case.id)
    )
    notes = list(
        session.scalars(select(CaseNote).where(CaseNote.case_id == case.id)).all()
    )
    diagnoses = list(
        session.scalars(select(CaseDiagnosis).where(CaseDiagnosis.case_id == case.id)).all()
    )
    vitals = list(session.scalars(select(CaseVital).where(CaseVital.case_id == case.id)).all())
    labs = list(session.scalars(select(CaseLab).where(CaseLab.case_id == case.id)).all())
    medications = [
        item
        for item in list_medications_for_case(session, case.id)
        if item.context in _RESIDENT_CONTEXTS
    ]
    instructions = [
        item
        for item in list_instructions_for_case(session, case.id)
        if _LISTED_DISCHARGE_INSTRUCTION not in (item.instruction_text or "").casefold()
    ]
    return {
        "case_id_code": case.case_id_code,
        "presentation": {
            "chief_complaint": case.chief_complaint
            if presentation is None
            else presentation.chief_complaint,
            "history_of_present_illness": None if presentation is None else presentation.hpi,
            "one_liner": case.one_liner,
            "admission_diagnosis": case.admission_dx,
        },
        "diagnoses": [
            {
                "diagnosis": item.diagnosis,
                "diagnosis_type": item.diagnosis_type,
                "status": item.status,
            }
            for item in diagnoses
        ],
        "hospital_course": [
            {"note_type": item.note_type, "note_text": item.note_text} for item in notes
        ],
        "vitals": [
            {
                "timepoint": item.timepoint,
                "bp_systolic": item.bp_systolic,
                "bp_diastolic": item.bp_diastolic,
                "heart_rate": item.heart_rate,
                "resp_rate": item.resp_rate,
                "spo2_percent": _plain_number(item.spo2_percent),
            }
            for item in vitals
        ],
        "labs": [
            {
                "timepoint": item.timepoint,
                "test_name": item.test_name,
                "value": _plain_number(item.value),
                "value_text": item.value_text,
                "unit": item.unit,
            }
            for item in labs
        ],
        "medications": [_medication_fact(item) for item in medications],
        "instructions": [
            {"category": item.category, "instruction_text": item.instruction_text}
            for item in instructions
        ],
        "discharge_status": None
        if discharge is None
        else {
            "disposition": discharge.disposition,
            "discharge_readiness": discharge.discharge_readiness,
        },
        "follow_up_considerations": [
            {"item": item.item, "timing": item.timing, "with_service": item.with_service}
            for item in list_followups_for_case(session, case.id)
        ],
    }


def evaluator_case_document(session: Session, case: ClinicalCase) -> dict[str, Any]:
    """Resident chart plus the hidden reference discharge plan."""
    document = resident_case_document(session, case)
    document["reference_discharge_plan"] = reference_discharge_plan(session, case)
    return document


def reference_plan_errors(session: Session, case: ClinicalCase) -> list[str]:
    """Structural checks for a clean case's hidden discharge standard."""
    errors: list[str] = []
    plans = list_plans_for_case(session, case.id)
    if not plans:
        errors.append("clean case is missing a reference discharge plan")
        return errors
    rows = list_medications_for_case(session, case.id)
    by_ref = _rows_by_reference(rows)
    for plan in plans:
        if plan.decision not in _STORED_DECISIONS:
            errors.append(f"reference plan {plan.drug or plan.plan_id} has no supported decision")
            continue
        action = public_action(plan.decision)
        if not plan.decision_reason:
            errors.append(f"reference plan {plan.drug or plan.plan_id} has no rationale")
        if action not in _REQUIRED_ACTIONS:
            continue
        source = _source_row(plan, by_ref)
        if source is None or not source.dose:
            errors.append(f"reference medication {plan.drug or plan.plan_id} has no dose")
        if source is None or not (source.indication or plan.decision_reason):
            errors.append(f"reference medication {plan.drug or plan.plan_id} has no indication")
    return errors


def resident_leak_errors(session: Session, case: ClinicalCase) -> list[str]:
    """The resident document must not carry the hidden discharge standard."""
    document = resident_case_document(session, case)
    errors: list[str] = []
    for medication in document["medications"]:
        if medication.get("context") not in _RESIDENT_CONTEXTS:
            errors.append("resident-facing case includes a discharge medication")
    leaked = _nested_keys(document) & _ANSWER_KEYS
    for key in sorted(leaked):
        errors.append(f"resident-facing case includes hidden field {key}")
    blob = dumps_json(document).casefold()
    if _LISTED_DISCHARGE_INSTRUCTION in blob:
        errors.append("resident-facing case tells the reader the discharge list is already written")
    if not document["medications"] and not document["diagnoses"]:
        errors.append("resident-facing case does not contain evidence for a discharge decision")
    return errors


def classify_resident_export(case: dict[str, Any], *, inject_error: bool | None) -> str:
    """Label one exported resident case against the clean-case contract."""
    medications = case.get("CaseMedication")
    if not isinstance(case, dict) or not isinstance(medications, list):
        return "OTHER_SCHEMA_PROBLEM"
    if inject_error:
        return "CONTAINS_INJECTED_ERROR"
    discharge = [
        item
        for item in medications
        if isinstance(item, dict) and item.get("context") == "discharge"
    ]
    if discharge or "reference_discharge_plan" in case:
        return "REFERENCE_LEAKAGE"
    return "CLEAN_AND_USABLE"


def audit_active_validation_cases() -> dict[str, Any]:
    """Classify the current on-disk resident exports. Does not rewrite them."""
    counts: dict[str, int] = {}
    needs_regeneration = 0
    cases: list[dict[str, str]] = []
    for spec in all_batch_specs().values():
        if not spec.is_active:
            continue
        resident_path = spec.directory / "resident_validation_cases.json"
        plan_path = spec.plan_path
        resident_doc = json.loads(resident_path.read_text(encoding="utf-8"))
        plan_doc = json.loads(plan_path.read_text(encoding="utf-8"))
        plan_rows = plan_doc.get("cases") if isinstance(plan_doc, dict) else None
        inject_by_id = {
            str(item.get("validation_case_id")): bool(item.get("inject_error"))
            for item in plan_rows or []
            if isinstance(item, dict)
        }
        exported = resident_doc.get("cases") if isinstance(resident_doc, dict) else None
        for case in exported or []:
            if not isinstance(case, dict):
                label = "OTHER_SCHEMA_PROBLEM"
                case_id = "unknown"
            else:
                case_id = str(case.get("case_id_code") or "")
                label = classify_resident_export(case, inject_error=inject_by_id.get(case_id))
            counts[label] = counts.get(label, 0) + 1
            if label != "CLEAN_AND_USABLE":
                needs_regeneration += 1
            cases.append({"case_id": case_id, "batch": spec.code, "classification": label})
    return {
        "counts": counts,
        "needs_regeneration": needs_regeneration,
        "cases": cases,
    }


def _plain_number(value: Decimal | float | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _explain_plan(
    name: str,
    stored_decision: str | None,
    diagnosis_names: list[str],
    *,
    creatinine: float | None,
    creatinine_unit: str | None,
    potassium: float | None,
    potassium_unit: str | None,
    systolic_bp: int | None,
    natriuretic_peptide: float | None,
    natriuretic_unit: str | None,
    heart_rate: int | None,
    dose: str | None,
    route: str | None,
    frequency: str | None,
    visible_reason: str | None,
    course_text: str,
    rule_codes: list[str],
) -> Any:
    if stored_decision == "new_start":
        return justify_hospital_start(
            name, diagnosis_names, dose=dose, route=route, frequency=frequency
        )
    if stored_decision == "stop":
        return justify_visible_stop(
            name,
            diagnosis_names,
            visible_reason=visible_reason,
            dose=dose,
            route=route,
            frequency=frequency,
        )
    if stored_decision == "dose_change":
        return consider_source_backed_change(
            name,
            indication=diagnosis_names[0] if diagnosis_names else None,
            evidence_text=course_text,
        )
    return justify_home_medication(
        name,
        diagnosis_names,
        creatinine=creatinine,
        creatinine_unit=creatinine_unit,
        potassium=potassium,
        potassium_unit=potassium_unit,
        systolic_bp=systolic_bp,
        natriuretic_peptide=natriuretic_peptide,
        natriuretic_unit=natriuretic_unit,
        heart_rate=heart_rate,
        dose=dose,
        route=route,
        frequency=frequency,
        rule_codes=rule_codes,
    )


def _hospital_course(session: Session, case: ClinicalCase) -> str:
    notes = session.scalars(
        select(CaseNote).where(
            CaseNote.case_id == case.id,
            CaseNote.note_type == "hospital_course",
        )
    ).all()
    return "\n".join(note.note_text or "" for note in notes)


def _allow_rule_codes(session: Session, ref_medication_id: Any) -> list[str]:
    if ref_medication_id is None:
        return []
    medication = session.get(RefMedication, ref_medication_id)
    if medication is None:
        return []
    codes: list[str] = []
    for rule in list_enabled_rules(session):
        constraint = rule.constraint_json if isinstance(rule.constraint_json, dict) else {}
        if str(constraint.get("action") or "") != "allow_with_diagnosis":
            continue
        if rule.input_rxcui and rule.input_rxcui == medication.rxcui:
            codes.append(rule.rule_code)
    return codes


def _diagnoses(session: Session, case: ClinicalCase) -> list[CaseDiagnosis]:
    return list(
        session.scalars(select(CaseDiagnosis).where(CaseDiagnosis.case_id == case.id)).all()
    )


def _named_lab(
    session: Session, case: ClinicalCase, needle: str
) -> tuple[float | None, str | None]:
    rows = list(session.scalars(select(CaseLab).where(CaseLab.case_id == case.id)).all())
    matches = [
        row
        for row in rows
        if needle in (row.test_name or "").casefold() and row.value is not None
    ]
    discharge = [row for row in matches if row.timepoint == "discharge"]
    chosen = discharge[-1] if discharge else (matches[-1] if matches else None)
    if chosen is None or chosen.value is None:
        return None, None
    return float(chosen.value), chosen.unit


def _named_systolic(session: Session, case: ClinicalCase) -> int | None:
    rows = list(session.scalars(select(CaseVital).where(CaseVital.case_id == case.id)).all())
    discharge = [row for row in rows if row.timepoint == "discharge" and row.bp_systolic]
    chosen = discharge[-1] if discharge else None
    if chosen is None:
        admitted = [row for row in rows if row.bp_systolic]
        chosen = admitted[-1] if admitted else None
    systolic = None if chosen is None else chosen.bp_systolic
    return None if systolic is None else int(systolic)


def _named_heart_rate(session: Session, case: ClinicalCase) -> int | None:
    rows = list(session.scalars(select(CaseVital).where(CaseVital.case_id == case.id)).all())
    discharge = [row for row in rows if row.timepoint == "discharge" and row.heart_rate is not None]
    chosen = discharge[-1] if discharge else None
    if chosen is None:
        admitted = [row for row in rows if row.heart_rate is not None]
        chosen = admitted[-1] if admitted else None
    rate = None if chosen is None else chosen.heart_rate
    return None if rate is None else int(rate)


def _resident_visible_text(session: Session, case: ClinicalCase) -> str:
    parts = [
        case.chief_complaint or "",
        case.one_liner or "",
        case.admission_dx or "",
    ]
    presentation = session.scalar(
        select(CasePresentation).where(CasePresentation.case_id == case.id)
    )
    if presentation is not None:
        parts.extend([presentation.hpi or "", presentation.chief_complaint or ""])
    for note in session.scalars(select(CaseNote).where(CaseNote.case_id == case.id)):
        parts.append(note.note_text or "")
    for item in list_medications_for_case(session, case.id):
        if item.context not in _RESIDENT_CONTEXTS:
            continue
        parts.extend(
            [
                item.drug or "",
                item.indication or "",
                item.held_reason or "",
                item.notes or "",
            ]
        )
    for instruction in list_instructions_for_case(session, case.id):
        text = instruction.instruction_text or ""
        if _LISTED_DISCHARGE_INSTRUCTION in text.casefold():
            continue
        parts.append(text)
    return "\n".join(parts)


def _temporal_role(name: str) -> str | None:
    regimen = regimen_for_text(name)
    return None if regimen is None else regimen.temporal_role


def _medication_fact(item: CaseMedication) -> dict[str, Any]:
    return {
        "medication": item.drug or item.reported_name,
        "context": item.context,
        "dose": item.dose,
        "route": item.route,
        "frequency": item.frequency,
        "indication": item.indication,
        "status": item.status,
        "held_reason": item.held_reason,
    }


def _rows_by_reference(
    rows: list[CaseMedication],
) -> dict[str, dict[Any, CaseMedication]]:
    grouped: dict[str, dict[Any, CaseMedication]] = {
        "discharge": {},
        "inpatient": {},
        "home": {},
    }
    for item in rows:
        if item.context in grouped and item.ref_medication_id is not None:
            grouped[item.context][item.ref_medication_id] = item
    return grouped


def _source_row(
    plan: CaseMedicationPlan,
    by_ref: dict[str, dict[Any, CaseMedication]],
) -> CaseMedication | None:
    if plan.ref_medication_id is None:
        return None
    for context in ("discharge", "inpatient", "home"):
        found = by_ref[context].get(plan.ref_medication_id)
        if found is not None:
            return found
    return None


def _nested_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        found.update(str(key) for key in value)
        for child in value.values():
            found.update(_nested_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_nested_keys(child))
    return found
