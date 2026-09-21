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

SUPPORTED_ERROR_FAMILIES = frozenset({"omission", "dose_mismatch", "frequency_mismatch"})


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
    discharge = [
        item for item in list_medications_for_case(session, case.id) if item.context == "discharge"
    ]
    category = preferred_category if preferred_category in SUPPORTED_ERROR_FAMILIES else "omission"
    eligible = _eligible_omission_targets(session, plans, discharge)
    if category != "omission" or not eligible:
        dose_targets = _eligible_dose_targets(session, plans, discharge)
        if category == "dose_mismatch" and dose_targets:
            return _inject_dose_mismatch(session, case, rng, seed, dose_targets)
        if category == "frequency_mismatch":
            freq_targets = _eligible_frequency_targets(discharge)
            if freq_targets:
                return _inject_frequency_mismatch(session, case, rng, seed, freq_targets)
        if not eligible:
            raise CaseValidationError(
                "error_injection",
                "no eligible medication for a single reconciliation error",
            )
        category = "omission"
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


def _eligible_frequency_targets(discharge: list[CaseMedication]) -> list[CaseMedication]:
    return [item for item in discharge if item.frequency]


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
    targets: list[CaseMedication],
) -> InjectionResult:
    targets.sort(key=lambda item: (item.drug or "", item.frequency or ""))
    medication = rng.choice(targets)
    original = medication.frequency or ""
    medication.frequency = "twice daily" if original != "twice daily" else "once daily"
    rxcui = ""
    if medication.ref_medication_id is not None:
        row = session.get(RefMedication, medication.ref_medication_id)
        rxcui = row.rxcui if row is not None else ""
    plans = [
        plan
        for plan in list_plans_for_case(session, case.id)
        if plan.ref_medication_id == medication.ref_medication_id
    ]
    if plans:
        plans[0].is_error_target = True
    explanation = "The discharge frequency was intentionally changed from the correct frequency."
    _write_answer_key(
        session,
        case,
        category="frequency_mismatch",
        rxcui=rxcui,
        drug=medication.drug,
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
    return InjectionResult("frequency_mismatch", rxcui, medication.drug, explanation, seed)


def _altered_dose(original: str) -> str:
    stripped = original.strip()
    if stripped.startswith("2"):
        return "1" + stripped[1:]
    if stripped[:1].isdigit():
        return "2" + stripped[1:]
    return f"{stripped} (altered)"


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
        correct_action=(
            "Restore the correct continued discharge medication from the medication plan."
        ),
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


def _plan_rxcui(session: Session, plan: CaseMedicationPlan) -> str | None:
    if plan.ref_medication_id is None:
        return None
    row = session.get(RefMedication, plan.ref_medication_id)
    return row.rxcui if row is not None else None
