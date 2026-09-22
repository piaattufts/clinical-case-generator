"""Deterministic CliniProof error injection.

The assessment blueprint selects the target category before the case is mutated.
OpenAI is not used to choose the error. Unknown or ineligible categories fail
rather than falling back to another type.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cases import CaseAnswerKey, CaseMedication, ClinicalCase
from app.models.generation import CaseMedicationPlan
from app.models.reference import RefMedication
from app.repositories.cases import list_medications_for_case
from app.services.error_taxonomy import (
    F1_COMMISSION,
    F1_DOSE,
    F1_FREQUENCY,
    F1_OMISSION,
    F1_ROUTE,
    F1_SUBSTITUTION,
    F2_HELD_RESTART,
    F2_HOSPITAL_ONLY,
    F2_INPATIENT_SUB,
    F2_MONITORING,
    F2_PENDING_FOLLOWUP,
    F2_SUPPLY,
    FAMILY_FOR_CATEGORY,
    INJECTED_SUPPLY_DAYS,
    MONITORING_NEEDLE,
    NONE,
    RESTART_NEEDLE,
    REVERT_SUB_NEEDLE,
    CaseView,
    canonicalize_category,
    class_pairs_for_case,
    commission_targets,
    continue_discharge_targets,
    held_restart_targets,
    inpatient_substitution_clean_targets,
    is_hospital_only_plan,
    isolation_errors,
    load_case_view,
    medication_rxcui,
    monitoring_targets,
    parse_days,
    plan_rxcui,
    require_eligible,
)
from app.sources.exceptions import CaseValidationError
from app.utils.identifiers import CHILD_ID_PREFIXES, format_child_business_id

INJECTORS = {
    F1_OMISSION,
    F1_COMMISSION,
    F1_DOSE,
    F1_ROUTE,
    F1_FREQUENCY,
    F1_SUBSTITUTION,
    F2_MONITORING,
    F2_HELD_RESTART,
    F2_SUPPLY,
    F2_HOSPITAL_ONLY,
    F2_INPATIENT_SUB,
    F2_PENDING_FOLLOWUP,
}

# Backward-compatible alias used by older tests and docs.
SUPPORTED_ERROR_FAMILIES = frozenset(
    {
        "omission",
        "dose_mismatch",
        "frequency_mismatch",
        "incorrect_continuation",
        *INJECTORS,
    }
)


@dataclass
class InjectionResult:
    category: str
    family: str
    rxcui: str
    drug: str | None
    explanation: str
    seed: str
    changed_field: str | None = None
    trigger_meds: list[dict[str, Any]] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


def inject_reconciliation_error(
    session: Session,
    case: ClinicalCase,
    *,
    rng: random.Random,
    seed: str,
    preferred_category: str = F1_OMISSION,
) -> InjectionResult:
    """Plant exactly the requested category after a validated clean case."""
    requested = canonicalize_category(preferred_category)
    if requested == NONE:
        raise CaseValidationError(
            "error_injection",
            "inject_reconciliation_error was called for a clean control",
        )
    if requested not in INJECTORS:
        raise CaseValidationError(
            "error_injection",
            f"{requested} cannot be injected; no substitute category will be used",
        )
    require_eligible(session, case, requested)
    view = load_case_view(session, case)
    result = _dispatch(session, case, view, rng, seed, requested)
    if canonicalize_category(result.category) != requested:
        raise CaseValidationError(
            "error_injection",
            f"injector produced {result.category!r} instead of requested {requested!r}",
        )
    session.expire_all()
    extra_findings = isolation_errors(session, case, expected_category=requested)
    if extra_findings:
        raise CaseValidationError("error_isolation", extra_findings[0], extra_findings)
    return result


def _dispatch(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
    category: str,
) -> InjectionResult:
    if category == F1_OMISSION:
        return _inject_omission(session, case, view, rng, seed)
    if category == F1_DOSE:
        return _inject_field_mismatch(session, case, view, rng, seed, "dose")
    if category == F1_ROUTE:
        return _inject_field_mismatch(session, case, view, rng, seed, "route")
    if category == F1_FREQUENCY:
        return _inject_field_mismatch(session, case, view, rng, seed, "frequency")
    if category == F1_COMMISSION:
        return _inject_commission(session, case, view, rng, seed)
    if category == F1_SUBSTITUTION:
        return _inject_therapeutic_substitution(session, case, view, rng, seed)
    if category == F2_MONITORING:
        return _inject_monitoring_gap(session, case, view, rng, seed)
    if category == F2_HELD_RESTART:
        return _inject_held_restart_gap(session, case, view, rng, seed)
    if category == F2_SUPPLY:
        return _inject_insufficient_supply(session, case, view, rng, seed)
    if category == F2_HOSPITAL_ONLY:
        return _inject_hospital_only(session, case, view, rng, seed)
    if category == F2_INPATIENT_SUB:
        return _inject_inpatient_substitution(session, case, view, rng, seed)
    if category == F2_PENDING_FOLLOWUP:
        return _inject_pending_followup(session, case, view, rng, seed)
    raise CaseValidationError("error_injection", f"no injector for {category}")


def _inject_omission(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    targets = continue_discharge_targets(session, view)
    plan, medication = _choose(rng, targets)
    rxcui = plan_rxcui(session, plan) or ""
    session.delete(medication)
    plan.is_error_target = True
    extra = {
        "changed_field": "presence",
        "clean_expected_state": "present",
        "injected_state": "absent",
        "context": "discharge",
        "original_clean_state": _medication_snapshot(medication, rxcui),
        "post_injection_state": None,
        "evidence_required": (
            "Home/inpatient continuation of this medication with no stop rationale."
        ),
        "evidence_location": "home_medications,inpatient_medications,discharge_medications",
        "detectability_location": "discharge_medications",
    }
    explanation = (
        "A medication indicated at discharge was omitted from the discharge medication list."
    )
    return _finish(
        session,
        case,
        category=F1_OMISSION,
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action="Restore the omitted continued discharge medication.",
        changed_field="presence",
        plan_ids=[plan.id],
    )


def _inject_field_mismatch(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
    field_name: str,
) -> InjectionResult:
    targets = [
        item for item in continue_discharge_targets(session, view) if getattr(item[1], field_name)
    ]
    plan, medication = _choose(rng, targets)
    original = str(getattr(medication, field_name) or "")
    planted = _altered_value(field_name, original)
    setattr(medication, field_name, planted)
    plan.is_error_target = True
    rxcui = plan_rxcui(session, plan) or ""
    category = {"dose": F1_DOSE, "route": F1_ROUTE, "frequency": F1_FREQUENCY}[field_name]
    extra = {
        "changed_field": field_name,
        "clean_expected_state": original,
        "injected_state": planted,
        "expected_value": original,
        "planted_value": planted,
        "context": "discharge",
        "evidence_required": f"Intended {field_name} on the home/inpatient medication plan.",
        "evidence_location": "home_medications,discharge_medications",
        "detectability_location": "discharge_medications",
    }
    explanation = (
        f"The discharge {field_name} differs from the intended medication plan "
        "without a documented clinical rationale."
    )
    return _finish(
        session,
        case,
        category=category,
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action=f"Restore the correct continued discharge {field_name}.",
        changed_field=field_name,
        plan_ids=[plan.id],
    )


def _inject_commission(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    targets = commission_targets(session, view)
    plan, home = _choose(rng, targets)
    cloned = _clone_to_discharge(session, case, home)
    session.add(cloned)
    plan.is_error_target = True
    rxcui = plan_rxcui(session, plan) or ""
    extra = {
        "changed_field": "presence",
        "clean_expected_state": "absent",
        "injected_state": "present",
        "context": "discharge",
        "original_clean_state": None,
        "post_injection_state": _medication_snapshot(cloned, rxcui),
        "evidence_required": "Home medication was discontinued and should not appear at discharge.",
        "evidence_location": "home_medications,discharge_instructions,discharge_medications",
        "detectability_location": "discharge_medications",
    }
    explanation = (
        "A medication was prescribed at discharge without a clinical indication "
        "or intended discharge role."
    )
    return _finish(
        session,
        case,
        category=F1_COMMISSION,
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action="Remove the unindicated medication from the discharge list.",
        changed_field="presence",
        plan_ids=[plan.id],
    )


def _inject_therapeutic_substitution(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    pairs = class_pairs_for_case(session, view)
    pair = _choose(rng, pairs)
    targets = [
        item
        for item in continue_discharge_targets(session, view)
        if item[0].ref_medication_id == pair.source.id
    ]
    if not targets:
        raise CaseValidationError(
            "error_injection",
            "therapeutic substitution pair is no longer attached to a discharge medication",
        )
    plan, medication = targets[0]
    original = _medication_snapshot(medication, pair.source.rxcui)
    _replace_medication_identity(medication, pair.substitute)
    plan.is_error_target = True
    extra = {
        "changed_field": "drug",
        "clean_expected_state": original,
        "injected_state": _medication_snapshot(medication, pair.substitute.rxcui),
        "expected_value": pair.source.rxcui,
        "planted_value": pair.substitute.rxcui,
        "class_id": pair.class_id,
        "class_name": pair.class_name,
        "source_backed_class": True,
        "evidence_required": (
            f"RxClass {pair.class_id} ({pair.class_name}) relates the source and substitute."
        ),
        "evidence_location": "home_medications,inpatient_medications,discharge_medications",
        "detectability_location": "discharge_medications",
    }
    explanation = (
        "A different medication in the same therapeutic class was substituted at discharge "
        "without a documented clinical or formulary explanation."
    )
    return _finish(
        session,
        case,
        category=F1_SUBSTITUTION,
        rxcui=pair.source.rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action=(
            "Restore the original continued medication; do not leave an "
            "unexplained same-class substitute."
        ),
        changed_field="drug",
        plan_ids=[plan.id],
        trigger_meds=[
            {"rxcui": pair.source.rxcui, "drug": plan.drug, "role": "source"},
            {
                "rxcui": pair.substitute.rxcui,
                "drug": _med_label(pair.substitute),
                "role": "substitute",
            },
        ],
    )


def _inject_monitoring_gap(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    targets = monitoring_targets(session, view)
    medication, rule_code, lab = _choose(rng, targets)
    rxcui = medication_rxcui(session, medication) or ""
    removed_ids = [item.monitoring_id for item in view.monitoring]
    for row in view.monitoring:
        session.delete(row)
    original_monitoring = medication.monitoring
    medication.monitoring = None
    extra = {
        "changed_field": "monitoring",
        "clean_expected_state": {
            "medication_monitoring": original_monitoring,
            "case_monitoring_ids": removed_ids,
        },
        "injected_state": {"medication_monitoring": None, "case_monitoring": []},
        "rule_code": rule_code,
        "required_monitoring": lab,
        "evidence_required": (
            f"Trigger medication remains; source-backed rule {rule_code} requires {lab}."
        ),
        "evidence_location": "discharge_medications,CaseLab,CaseMonitoring",
        "detectability_location": "CaseMonitoring,discharge_medications.monitoring",
        "field_removed": "CaseMonitoring and CaseMedication.monitoring",
    }
    plan = _mark_plan(view, medication.ref_medication_id)
    explanation = (
        "A medication requiring outpatient laboratory or physiological monitoring "
        "was discharged without that monitoring being arranged."
    )
    return _finish(
        session,
        case,
        category=F2_MONITORING,
        rxcui=rxcui,
        drug=medication.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action="Arrange the required outpatient monitoring for the trigger medication.",
        changed_field="monitoring",
        plan_ids=[] if plan is None else [plan.id],
        trigger_meds=[{"rxcui": rxcui, "drug": medication.drug, "rule_code": rule_code}],
    )


def _inject_held_restart_gap(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    plans = held_restart_targets(view)
    plan = _choose(rng, plans)
    rxcui = plan_rxcui(session, plan) or ""
    removed: list[str | None] = []
    for instruction in view.instructions:
        if (
            instruction.instruction_text
            and RESTART_NEEDLE in instruction.instruction_text.casefold()
        ):
            removed.append(instruction.instruction_text)
            session.delete(instruction)
    cleared: list[str | None] = []
    for medication in view.medications:
        if medication.ref_medication_id != plan.ref_medication_id:
            continue
        if medication.target_or_goal:
            cleared.append(medication.target_or_goal)
            medication.target_or_goal = None
    plan.is_error_target = True
    extra = {
        "changed_field": "restart_plan",
        "clean_expected_state": {"instructions": removed, "target_or_goal": cleared},
        "injected_state": {"instructions": [], "target_or_goal": None},
        "held_reason_preserved": True,
        "evidence_required": (
            "The medication was held for a documented reason and needs a restart plan."
        ),
        "evidence_location": "home_medications,inpatient_medications,CaseInstruction",
        "detectability_location": "CaseInstruction,CaseMedication.target_or_goal",
    }
    explanation = (
        "A home medication legitimately held during hospitalization has no documented "
        "resumption criterion or timing at discharge."
    )
    return _finish(
        session,
        case,
        category=F2_HELD_RESTART,
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action=(
            "Document when and under what criteria the held medication should be restarted."
        ),
        changed_field="restart_plan",
        plan_ids=[plan.id],
    )


def _inject_insufficient_supply(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    followup_days = max(
        (parse_days(item.timing) or 0 for item in view.followups),
        default=0,
    )
    targets = [
        item
        for item in continue_discharge_targets(session, view)
        if parse_days(item[1].quantity_or_days) is not None
        and item[1].dose
        and item[1].frequency
        and (parse_days(item[1].quantity_or_days) or 0) >= followup_days
    ]
    plan, medication = _choose(rng, targets)
    original = medication.quantity_or_days
    medication.quantity_or_days = f"{INJECTED_SUPPLY_DAYS} days"
    plan.is_error_target = True
    rxcui = plan_rxcui(session, plan) or ""
    extra = {
        "changed_field": "quantity_or_days",
        "clean_expected_state": original,
        "injected_state": medication.quantity_or_days,
        "expected_value": original,
        "planted_value": medication.quantity_or_days,
        "followup_days": followup_days,
        "dose": medication.dose,
        "frequency": medication.frequency,
        "evidence_required": (
            "Days' supply must cover the scheduled follow-up or treatment endpoint."
        ),
        "evidence_location": "CaseFollowup,discharge_medications.quantity_or_days",
        "detectability_location": "discharge_medications.quantity_or_days",
    }
    explanation = (
        "The prescribed quantity or days' supply is insufficient to cover the patient "
        "until the planned follow-up."
    )
    return _finish(
        session,
        case,
        category=F2_SUPPLY,
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action=(
            "Increase days' supply so treatment continues through the planned follow-up."
        ),
        changed_field="quantity_or_days",
        plan_ids=[plan.id],
    )


def _inject_hospital_only(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    inpatient = [
        item
        for item in view.inpatient
        if item.ref_medication_id
        and item.ref_medication_id
        not in {row.ref_medication_id for row in view.discharge if row.ref_medication_id}
    ]
    candidates: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan in view.plans:
        if not is_hospital_only_plan(plan):
            continue
        match = next(
            (item for item in inpatient if item.ref_medication_id == plan.ref_medication_id),
            None,
        )
        if match is not None:
            candidates.append((plan, match))
    plan, source = _choose(rng, candidates)
    cloned = _clone_to_discharge(session, case, source)
    session.add(cloned)
    plan.is_error_target = True
    rxcui = plan_rxcui(session, plan) or ""
    extra = {
        "changed_field": "presence",
        "clean_expected_state": "absent",
        "injected_state": "present",
        "context": "discharge",
        "evidence_required": (
            "Medication was started in hospital for an inpatient-only indication and should stop."
        ),
        "evidence_location": (
            "home_medications,inpatient_medications,discharge_medications,plan.decision_reason"
        ),
        "detectability_location": "discharge_medications",
    }
    explanation = (
        "A medication started for an inpatient-only indication was erroneously continued "
        "at discharge despite no ongoing outpatient indication."
    )
    return _finish(
        session,
        case,
        category=F2_HOSPITAL_ONLY,
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action="Stop the hospital-only medication at discharge.",
        changed_field="presence",
        plan_ids=[plan.id],
    )


def _inject_inpatient_substitution(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    targets = inpatient_substitution_clean_targets(session, view)
    home_plan, sub_plan, class_id, class_name = _choose(rng, targets)
    discharge_home = next(
        (
            item
            for item in view.discharge
            if item.ref_medication_id == home_plan.ref_medication_id and item.status != "held"
        ),
        None,
    )
    inpatient_sub = next(
        (item for item in view.inpatient if item.ref_medication_id == sub_plan.ref_medication_id),
        None,
    )
    if discharge_home is None or inpatient_sub is None:
        raise CaseValidationError(
            "error_injection",
            "inpatient substitution clean structure is incomplete",
        )
    original = _medication_snapshot(discharge_home, plan_rxcui(session, home_plan))
    substitute = session.get(RefMedication, sub_plan.ref_medication_id)
    if substitute is None:
        raise CaseValidationError("error_injection", "substitute medication reference is missing")
    _replace_medication_identity(discharge_home, substitute)
    for instruction in view.instructions:
        if (
            instruction.instruction_text
            and REVERT_SUB_NEEDLE in instruction.instruction_text.casefold()
        ):
            session.delete(instruction)
    home_plan.is_error_target = True
    extra = {
        "changed_field": "discharge_medication",
        "clean_expected_state": original,
        "injected_state": _medication_snapshot(discharge_home, substitute.rxcui),
        "class_id": class_id,
        "class_name": class_name,
        "source_rxcui": plan_rxcui(session, home_plan),
        "substitute_rxcui": substitute.rxcui,
        "evidence_required": (
            "Home therapy was temporarily replaced inpatient and should be "
            "reverted or explicitly re-decided."
        ),
        "evidence_location": (
            "home_medications,inpatient_medications,discharge_medications,CaseInstruction"
        ),
        "detectability_location": "discharge_medications",
    }
    explanation = (
        "A home therapy temporarily replaced during hospitalization for formulary or protocol "
        "reasons was neither reverted nor explicitly re-decided at discharge."
    )
    return _finish(
        session,
        case,
        category=F2_INPATIENT_SUB,
        rxcui=plan_rxcui(session, home_plan) or "",
        drug=home_plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action=(
            "Revert to the home therapy or document an intentional decision "
            "to continue the inpatient substitute."
        ),
        changed_field="discharge_medication",
        plan_ids=[home_plan.id, sub_plan.id],
        trigger_meds=[
            {
                "rxcui": plan_rxcui(session, home_plan),
                "drug": home_plan.drug,
                "role": "home_therapy",
            },
            {
                "rxcui": substitute.rxcui,
                "drug": sub_plan.drug,
                "role": "inpatient_substitute",
            },
        ],
    )


def _inject_pending_followup(
    session: Session,
    case: ClinicalCase,
    view: CaseView,
    rng: random.Random,
    seed: str,
) -> InjectionResult:
    _ = rng
    removed = [
        {"item": item.item, "timing": item.timing, "with_service": item.with_service}
        for item in view.followups
    ]
    for followup in view.followups:
        session.delete(followup)
    extra = {
        "changed_field": "followup",
        "clean_expected_state": removed,
        "injected_state": [],
        "evidence_required": (
            "A pending therapeutic decision remains unresolved and requires scheduled follow-up."
        ),
        "evidence_location": "CaseInstruction,CaseFollowup",
        "detectability_location": "CaseFollowup",
    }
    explanation = (
        "Treatment continues after discharge while a pending therapeutic decision remains "
        "unresolved and no follow-up visit is arranged to resolve it."
    )
    plan = next((item for item in view.plans if item.correct_discharge_state == "continue"), None)
    if plan is not None:
        plan.is_error_target = True
    rxcui = plan_rxcui(session, plan) if plan is not None else ""
    return _finish(
        session,
        case,
        category=F2_PENDING_FOLLOWUP,
        rxcui=rxcui or "",
        drug=None if plan is None else plan.drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action="Arrange follow-up to resolve the pending therapeutic decision.",
        changed_field="followup",
        plan_ids=[] if plan is None else [plan.id],
    )


def _finish(
    session: Session,
    case: ClinicalCase,
    *,
    category: str,
    rxcui: str,
    drug: str | None,
    explanation: str,
    seed: str,
    extra: dict[str, Any],
    correct_action: str,
    changed_field: str | None,
    plan_ids: list[UUID],
    trigger_meds: list[dict[str, Any]] | None = None,
) -> InjectionResult:
    family = FAMILY_FOR_CATEGORY[category]
    triggers = trigger_meds or [{"rxcui": rxcui, "drug": drug}]
    for plan_id in plan_ids:
        plan = session.get(CaseMedicationPlan, plan_id)
        if plan is not None:
            plan.is_error_target = True
    _write_answer_key(
        session,
        case,
        family=family,
        category=category,
        rxcui=rxcui,
        drug=drug,
        explanation=explanation,
        seed=seed,
        extra=extra,
        correct_action=correct_action,
        changed_field=changed_field,
        trigger_meds=triggers,
    )
    case.clean_case = False
    case.case_status = "error_injected"
    session.flush()
    return InjectionResult(
        category=category,
        family=family,
        rxcui=rxcui,
        drug=drug,
        explanation=explanation,
        seed=seed,
        changed_field=changed_field,
        trigger_meds=triggers,
        extra=extra,
    )


def _write_answer_key(
    session: Session,
    case: ClinicalCase,
    *,
    family: str,
    category: str,
    rxcui: str,
    drug: str | None,
    explanation: str,
    seed: str,
    extra: dict[str, Any],
    correct_action: str,
    changed_field: str | None,
    trigger_meds: list[dict[str, Any]],
) -> CaseAnswerKey:
    answer = CaseAnswerKey(
        case_id=case.id,
        answer_id=format_child_business_id(CHILD_ID_PREFIXES["answer_key"], case.case_id_code, 1),
        error_family=family,
        error_category=category,
        error_description=explanation,
        trigger_meds=trigger_meds,
        detectability_location=str(extra.get("detectability_location") or "discharge_medications"),
        correct_action=correct_action,
        severity_ncc_merp=None,
        difficulty_a_priori=None,
        is_primary_error=True,
        intentional_changes=[
            {
                "kind": category,
                "error_family": family,
                "error_category": category,
                "rxcui": rxcui,
                "drug": drug,
                "seed": seed,
                "changed_field": changed_field,
                "clean_expected_state": extra.get("clean_expected_state"),
                "injected_state": extra.get("injected_state"),
                "evidence_required": extra.get("evidence_required"),
                "evidence_location": extra.get("evidence_location"),
                "source_backed_rationale": explanation,
                **{
                    key: value
                    for key, value in extra.items()
                    if key
                    not in {
                        "clean_expected_state",
                        "injected_state",
                        "evidence_required",
                        "evidence_location",
                        "detectability_location",
                    }
                },
            }
        ],
    )
    session.add(answer)
    session.flush()
    return answer


def _clone_to_discharge(
    session: Session, case: ClinicalCase, source: CaseMedication
) -> CaseMedication:
    existing = list_medications_for_case(session, case.id)
    next_index = len(existing) + 1
    return CaseMedication(
        case_id=case.id,
        medication_id=format_child_business_id(
            CHILD_ID_PREFIXES["medication"], case.case_id_code, next_index
        ),
        ref_medication_id=source.ref_medication_id,
        context="discharge",
        drug=source.drug,
        reported_name=source.reported_name,
        dose=source.dose,
        route=source.route,
        frequency=source.frequency,
        indication=source.indication,
        status="discharge",
        held_reason=None,
        verification_status=source.verification_status,
        verification_source=source.verification_source,
        target_or_goal=None,
        monitoring=source.monitoring
        if MONITORING_NEEDLE not in (source.monitoring or "").casefold()
        else source.monitoring,
        quantity_or_days=source.quantity_or_days,
        refills=None,
        source_type=source.source_type,
        source_file=None,
        source_reference=source.source_reference,
        notes=None,
    )


def _replace_medication_identity(medication: CaseMedication, replacement: RefMedication) -> None:
    label = _med_label(replacement)
    medication.ref_medication_id = replacement.id
    medication.drug = label
    medication.reported_name = label
    medication.source_reference = f"RXCUI:{replacement.rxcui}"


def _altered_value(field_name: str, original: str) -> str:
    if field_name == "dose":
        return _altered_dose(original)
    if field_name == "frequency":
        return "twice daily" if original != "twice daily" else "once daily"
    if field_name == "route":
        lowered = original.casefold()
        if "oral" in lowered:
            return "intravenous"
        if "intravenous" in lowered or lowered in {"iv", "i.v."}:
            return "oral"
        return "oral"
    raise CaseValidationError("error_injection", f"unsupported field {field_name}")


def _altered_dose(original: str) -> str:
    stripped = original.strip()
    if stripped.startswith("2"):
        return "1" + stripped[1:]
    if stripped[:1].isdigit():
        return "2" + stripped[1:]
    return f"2 tablets instead of {stripped}"


def _choose[T](rng: random.Random, targets: list[T]) -> T:
    if not targets:
        raise CaseValidationError(
            "error_injection",
            "no eligible target for the requested category; no substitute category will be used",
        )
    return rng.choice(targets)


def _mark_plan(view: CaseView, ref_id: Any) -> CaseMedicationPlan | None:
    for plan in view.plans:
        if plan.ref_medication_id == ref_id:
            plan.is_error_target = True
            return plan
    return None


def _medication_snapshot(medication: CaseMedication, rxcui: str | None) -> dict[str, Any]:
    return {
        "drug": medication.drug,
        "dose": medication.dose,
        "route": medication.route,
        "frequency": medication.frequency,
        "status": medication.status,
        "quantity_or_days": medication.quantity_or_days,
        "monitoring": medication.monitoring,
        "rxcui": rxcui,
    }


def _med_label(medication: RefMedication) -> str:
    return (
        medication.generic_name
        or medication.concept_name
        or medication.ingredient
        or medication.rxcui
    )
