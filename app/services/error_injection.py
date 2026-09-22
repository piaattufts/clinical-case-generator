"""Deterministic medication-reconciliation error injection.

The clean case must already have passed validation. Exactly one error is planted.
OpenAI is not used to choose the error.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.models.cases import CaseAnswerKey, CaseMedication, ClinicalCase
from app.models.generation import CaseMedicationPlan
from app.models.reference import RefMedication
from app.repositories.cases import list_medications_for_case, list_plans_for_case
from app.sources.exceptions import CaseValidationError
from app.utils.identifiers import CHILD_ID_PREFIXES, format_child_business_id

SUPPORTED_ERROR_FAMILIES = frozenset(
    {
        "omission",
        "dose_mismatch",
        "frequency_mismatch",
        "incorrect_continuation",
    }
)


@dataclass
class InjectionResult:
    category: str
    rxcui: str
    drug: str | None
    explanation: str
    seed: str


def inject_reconciliation_error(
    session: Session,
    case: ClinicalCase,
    *,
    rng: random.Random,
    seed: str,
    preferred_category: str = "omission",
) -> InjectionResult:
    """Plant exactly one discharge-list error after a validated clean case."""
    plans = list_plans_for_case(session, case.id)
    medications = list_medications_for_case(session, case.id)
    discharge = [item for item in medications if item.context == "discharge"]
    home = [item for item in medications if item.context == "home"]
    category = (
        preferred_category if preferred_category in SUPPORTED_ERROR_FAMILIES else "omission"
    )
    if category == "dose_mismatch":
        dose_targets = _eligible_dose_targets(session, plans, discharge)
        if not dose_targets:
            raise CaseValidationError(
                "error_injection",
                "no eligible medication for a dose_mismatch reconciliation error",
            )
        return _inject_dose_mismatch(session, case, rng, seed, dose_targets)
    if category == "frequency_mismatch":
        freq_targets = _eligible_frequency_targets(session, plans, discharge)
        if not freq_targets:
            raise CaseValidationError(
                "error_injection",
                "no eligible medication for a frequency_mismatch reconciliation error",
            )
        return _inject_frequency_mismatch(session, case, rng, seed, freq_targets)
    if category == "incorrect_continuation":
        stop_targets = _eligible_incorrect_continuation_targets(session, plans, home, discharge)
        if not stop_targets:
            raise CaseValidationError(
                "error_injection",
                "no eligible medication for an incorrect_continuation reconciliation error",
            )
        return _inject_incorrect_continuation(session, case, rng, seed, stop_targets)
    eligible = _eligible_omission_targets(session, plans, discharge)
    if not eligible:
        raise CaseValidationError(
            "error_injection",
            "no eligible medication for a single reconciliation error",
        )
    eligible.sort(key=lambda item: (_plan_rxcui(session, item[0]) or "", item[0].plan_id or ""))
    plan, medication = rng.choice(eligible)
    rxcui = _plan_rxcui(session, plan) or ""
    session.delete(medication)
    plan.is_error_target = True
    session.flush()
    explanation = (
        "The correct discharge medication list includes this continued home medication; "
        "it was intentionally omitted from the discharge list."
    )
    _write_answer_key(
        session,
        case,
        category="omission",
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra={"clean_state": "present", "injected_state": "absent", "context": "discharge"},
    )
    case.clean_case = False
    case.case_status = "error_injected"
    session.flush()
    return InjectionResult(
        category="omission",
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
    )


def _eligible_omission_targets(
    session: Session,
    plans: list[CaseMedicationPlan],
    discharge: list[CaseMedication],
) -> list[tuple[CaseMedicationPlan, CaseMedication]]:
    by_ref = {
        item.ref_medication_id: item for item in discharge if item.ref_medication_id is not None
    }
    eligible: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan in plans:
        if plan.decision != "continue" or plan.correct_discharge_state != "continue":
            continue
        if plan.ref_medication_id is None:
            continue
        medication = by_ref.get(plan.ref_medication_id)
        if medication is None:
            continue
        eligible.append((plan, medication))
    return eligible


def _eligible_dose_targets(
    session: Session,
    plans: list[CaseMedicationPlan],
    discharge: list[CaseMedication],
) -> list[tuple[CaseMedicationPlan, CaseMedication]]:
    found: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan, medication in _eligible_omission_targets(session, plans, discharge):
        if medication.dose:
            found.append((plan, medication))
    return found


def _eligible_frequency_targets(
    session: Session,
    plans: list[CaseMedicationPlan],
    discharge: list[CaseMedication],
) -> list[tuple[CaseMedicationPlan, CaseMedication]]:
    found: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan, medication in _eligible_omission_targets(session, plans, discharge):
        if medication.frequency:
            found.append((plan, medication))
    return found


def _eligible_incorrect_continuation_targets(
    session: Session,
    plans: list[CaseMedicationPlan],
    home: list[CaseMedication],
    discharge: list[CaseMedication],
) -> list[tuple[CaseMedicationPlan, CaseMedication]]:
    discharge_ids = {item.ref_medication_id for item in discharge if item.ref_medication_id}
    by_home = {item.ref_medication_id: item for item in home if item.ref_medication_id is not None}
    found: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan in plans:
        if plan.decision != "stop" or plan.correct_discharge_state != "stop":
            continue
        if plan.ref_medication_id is None or plan.ref_medication_id in discharge_ids:
            continue
        home_row = by_home.get(plan.ref_medication_id)
        if home_row is None:
            continue
        found.append((plan, home_row))
    return found


def _inject_dose_mismatch(
    session: Session,
    case: ClinicalCase,
    rng: random.Random,
    seed: str,
    targets: list[tuple[CaseMedicationPlan, CaseMedication]],
) -> InjectionResult:
    targets.sort(key=lambda item: (_plan_rxcui(session, item[0]) or "", item[1].dose or ""))
    plan, medication = rng.choice(targets)
    original = medication.dose or ""
    medication.dose = _altered_dose(original)
    plan.is_error_target = True
    rxcui = _plan_rxcui(session, plan) or ""
    explanation = "The discharge dose was intentionally changed from the correct continued dose."
    _write_answer_key(
        session,
        case,
        category="dose_mismatch",
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra={"clean_dose": original, "injected_dose": medication.dose, "context": "discharge"},
    )
    case.clean_case = False
    case.case_status = "error_injected"
    session.flush()
    return InjectionResult("dose_mismatch", rxcui, plan.drug, explanation, seed)


def _inject_frequency_mismatch(
    session: Session,
    case: ClinicalCase,
    rng: random.Random,
    seed: str,
    targets: list[tuple[CaseMedicationPlan, CaseMedication]],
) -> InjectionResult:
    targets.sort(key=lambda item: (_plan_rxcui(session, item[0]) or "", item[1].frequency or ""))
    plan, medication = rng.choice(targets)
    original = medication.frequency or ""
    medication.frequency = "twice daily" if original != "twice daily" else "once daily"
    plan.is_error_target = True
    rxcui = _plan_rxcui(session, plan) or ""
    explanation = "The discharge frequency was intentionally changed from the correct frequency."
    _write_answer_key(
        session,
        case,
        category="frequency_mismatch",
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra={
            "clean_frequency": original,
            "injected_frequency": medication.frequency,
            "context": "discharge",
        },
    )
    case.clean_case = False
    case.case_status = "error_injected"
    session.flush()
    return InjectionResult("frequency_mismatch", rxcui, plan.drug, explanation, seed)


def _inject_incorrect_continuation(
    session: Session,
    case: ClinicalCase,
    rng: random.Random,
    seed: str,
    targets: list[tuple[CaseMedicationPlan, CaseMedication]],
) -> InjectionResult:
    targets.sort(key=lambda item: (_plan_rxcui(session, item[0]) or "", item[1].drug or ""))
    plan, home = rng.choice(targets)
    existing = list_medications_for_case(session, case.id)
    next_index = len(existing) + 1
    cloned = CaseMedication(
        case_id=case.id,
        medication_id=format_child_business_id(
            CHILD_ID_PREFIXES["medication"], case.case_id_code, next_index
        ),
        ref_medication_id=home.ref_medication_id,
        context="discharge",
        drug=home.drug,
        reported_name=home.reported_name,
        dose=home.dose,
        route=home.route,
        frequency=home.frequency,
        indication=home.indication,
        status="discharge",
        held_reason=None,
        verification_status=home.verification_status,
        verification_source=home.verification_source,
        target_or_goal=None,
        monitoring=None,
        quantity_or_days=None,
        refills=None,
        source_type=home.source_type,
        source_file=None,
        source_reference=home.source_reference,
        notes=None,
    )
    session.add(cloned)
    plan.is_error_target = True
    rxcui = _plan_rxcui(session, plan) or ""
    explanation = (
        "This home medication was correctly held and should not appear on the discharge list; "
        "it was intentionally continued at discharge."
    )
    _write_answer_key(
        session,
        case,
        category="incorrect_continuation",
        rxcui=rxcui,
        drug=plan.drug,
        explanation=explanation,
        seed=seed,
        extra={"clean_state": "absent", "injected_state": "present", "context": "discharge"},
    )
    case.clean_case = False
    case.case_status = "error_injected"
    session.flush()
    return InjectionResult("incorrect_continuation", rxcui, plan.drug, explanation, seed)


def _altered_dose(original: str) -> str:
    stripped = original.strip()
    if stripped.startswith("2"):
        return "1" + stripped[1:]
    if stripped[:1].isdigit():
        return "2" + stripped[1:]
    return f"2 tablets instead of {stripped}"


def _write_answer_key(
    session: Session,
    case: ClinicalCase,
    *,
    category: str,
    rxcui: str,
    drug: str | None,
    explanation: str,
    seed: str,
    extra: dict[str, Any],
) -> CaseAnswerKey:
    answer = CaseAnswerKey(
        case_id=case.id,
        answer_id=format_child_business_id(CHILD_ID_PREFIXES["answer_key"], case.case_id_code, 1),
        error_family="medication_reconciliation",
        error_category=category,
        error_description=explanation,
        trigger_meds=[{"rxcui": rxcui, "drug": drug}],
        detectability_location="discharge_medications",
        correct_action=_correct_action(category),
        severity_ncc_merp=None,
        difficulty_a_priori=None,
        is_primary_error=True,
        intentional_changes=[
            {
                "kind": category,
                "rxcui": rxcui,
                "drug": drug,
                "seed": seed,
                "source_backed_rationale": explanation,
                **extra,
            }
        ],
    )
    session.add(answer)
    session.flush()
    return answer


def _correct_action(category: str) -> str:
    if category == "omission":
        return "Restore the omitted continued discharge medication from the medication plan."
    if category == "dose_mismatch":
        return "Restore the correct continued discharge dose from the medication plan."
    if category == "frequency_mismatch":
        return "Restore the correct continued discharge frequency from the medication plan."
    if category == "incorrect_continuation":
        return "Remove the held medication from the discharge list."
    return "Restore the correct discharge medication plan."


def _plan_rxcui(session: Session, plan: CaseMedicationPlan) -> str | None:
    if plan.ref_medication_id is None:
        return None
    row = session.get(RefMedication, plan.ref_medication_id)
    return row.rxcui if row is not None else None
