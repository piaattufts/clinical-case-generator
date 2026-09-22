"""CliniProof reconciliation-error taxonomy.

Canonical identifiers, deterministic eligibility, and mechanical finding
detection. An LLM never chooses the planted error. Unknown or obsolete names
raise rather than being translated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cases import (
    CaseFollowup,
    CaseInstruction,
    CaseMedication,
    CaseMonitoring,
    ClinicalCase,
)
from app.models.generation import CaseMedicationPlan
from app.models.reference import RefLabTest, RefMedication
from app.repositories.cases import (
    list_followups_for_case,
    list_instructions_for_case,
    list_labs_for_case,
    list_medications_for_case,
    list_monitoring_for_case,
    list_plans_for_case,
)
from app.repositories.reference import (
    list_enabled_rules,
    list_medication_classes_for_rxcui,
    list_medications_sharing_class,
)
from app.services.rules import CaseSnapshot, evaluate_rules, hard_violations
from app.sources.exceptions import CaseValidationError

FAMILY_1 = "family_1"
FAMILY_2 = "family_2"
FAMILY_NONE = "none"

F1_OMISSION = "f1_omission"
F1_COMMISSION = "f1_commission"
F1_DOSE = "f1_dose_mismatch"
F1_ROUTE = "f1_route_mismatch"
F1_FREQUENCY = "f1_frequency_mismatch"
F1_SUBSTITUTION = "f1_therapeutic_substitution"
F2_COPRESCRIPTION = "f2_coprescription_omitted"
F2_MONITORING = "f2_monitoring_not_arranged"
F2_HELD_RESTART = "f2_held_med_no_restart_plan"
F2_SUPPLY = "f2_insufficient_supply"
F2_HOSPITAL_ONLY = "f2_hospital_only_continued"
F2_INPATIENT_SUB = "f2_inpatient_substitution_not_reverted"
F2_PENDING_FOLLOWUP = "f2_pending_decision_followup_missing"
NONE = "none"

CANONICAL_CATEGORIES = frozenset(
    {
        F1_OMISSION,
        F1_COMMISSION,
        F1_DOSE,
        F1_ROUTE,
        F1_FREQUENCY,
        F1_SUBSTITUTION,
        F2_COPRESCRIPTION,
        F2_MONITORING,
        F2_HELD_RESTART,
        F2_SUPPLY,
        F2_HOSPITAL_ONLY,
        F2_INPATIENT_SUB,
        F2_PENDING_FOLLOWUP,
        NONE,
    }
)

FAMILY_FOR_CATEGORY = {
    F1_OMISSION: FAMILY_1,
    F1_COMMISSION: FAMILY_1,
    F1_DOSE: FAMILY_1,
    F1_ROUTE: FAMILY_1,
    F1_FREQUENCY: FAMILY_1,
    F1_SUBSTITUTION: FAMILY_1,
    F2_COPRESCRIPTION: FAMILY_2,
    F2_MONITORING: FAMILY_2,
    F2_HELD_RESTART: FAMILY_2,
    F2_SUPPLY: FAMILY_2,
    F2_HOSPITAL_ONLY: FAMILY_2,
    F2_INPATIENT_SUB: FAMILY_2,
    F2_PENDING_FOLLOWUP: FAMILY_2,
    NONE: FAMILY_NONE,
}

NOT_YET_IMPLEMENTABLE = {
    F2_COPRESCRIPTION: (
        "no source-backed companion-prescription rule exists; steroid/opioid examples "
        "from the manuscript are not hard-coded"
    ),
}

IMPLEMENTABLE_CATEGORIES = CANONICAL_CATEGORIES - set(NOT_YET_IMPLEMENTABLE)

RESTART_NEEDLE = "resume when"
DO_NOT_RESTART_NEEDLE = "do not restart at discharge"
PENDING_DECISION_NEEDLE = "pending therapeutic decision"
HOSPITAL_ONLY_NEEDLE = "inpatient-only indication"
FORMULARY_SUB_NEEDLE = "formulary substitution for"
REVERT_SUB_NEEDLE = "resume home therapy"
MONITORING_NEEDLE = "outpatient monitoring arranged"
CLEAN_SUPPLY_DAYS = 30
FOLLOWUP_DAYS_FOR_SUPPLY = 14
INJECTED_SUPPLY_DAYS = 7

# Same-class substitution uses RxClass membership, not name similarity.
# Anatomical/super-classes are too broad for CliniProof F1.4 / F2.6.
SUBSTITUTION_CLASS_TYPES = frozenset({"EPC", "ATC1-4", "VA"})
BROAD_CLASS_NAME_NEEDLES = (
    "cardiovascular agent",
    "central nervous system agent",
    "cns agent",
    "anti-infective",
    "antiinfective",
    "gastrointestinal agent",
    "respiratory tract agent",
    "hormone/hormone modifier",
    "medical device",
    "dietary product",
)

_DAYS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:day|days|d)\b", re.IGNORECASE)
_INT_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*$")


@dataclass(frozen=True)
class CategorySpec:
    category: str
    family: str
    implementable: bool
    blocked_reason: str | None
    preconditions: str


@dataclass
class CaseView:
    case: ClinicalCase
    plans: list[CaseMedicationPlan]
    medications: list[CaseMedication]
    home: list[CaseMedication]
    inpatient: list[CaseMedication]
    discharge: list[CaseMedication]
    monitoring: list[CaseMonitoring]
    followups: list[CaseFollowup]
    instructions: list[CaseInstruction]


@dataclass(frozen=True)
class Finding:
    category: str
    rxcui: str | None
    drug: str | None
    changed_field: str | None
    detail: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ClassPair:
    source: RefMedication
    substitute: RefMedication
    class_id: str
    class_name: str


def category_specs() -> dict[str, CategorySpec]:
    return {
        F1_OMISSION: CategorySpec(
            F1_OMISSION,
            FAMILY_1,
            True,
            None,
            "At least one medication intended to continue is present on the clean discharge list.",
        ),
        F1_COMMISSION: CategorySpec(
            F1_COMMISSION,
            FAMILY_1,
            True,
            None,
            (
                "A home medication is documented as discontinued/not for discharge "
                "and is absent from the clean discharge list."
            ),
        ),
        F1_DOSE: CategorySpec(
            F1_DOSE,
            FAMILY_1,
            True,
            None,
            "A continued discharge medication has an unambiguous clean dose.",
        ),
        F1_ROUTE: CategorySpec(
            F1_ROUTE,
            FAMILY_1,
            True,
            None,
            "A continued discharge medication has an unambiguous clean route.",
        ),
        F1_FREQUENCY: CategorySpec(
            F1_FREQUENCY,
            FAMILY_1,
            True,
            None,
            "A continued discharge medication has an unambiguous clean frequency.",
        ),
        F1_SUBSTITUTION: CategorySpec(
            F1_SUBSTITUTION,
            FAMILY_1,
            True,
            None,
            (
                "A continued medication has a source-backed same-class substitute "
                "that is not already on the case and does not violate a hard rule."
            ),
        ),
        F2_COPRESCRIPTION: CategorySpec(
            F2_COPRESCRIPTION,
            FAMILY_2,
            False,
            NOT_YET_IMPLEMENTABLE[F2_COPRESCRIPTION],
            "A source-backed companion-prescription rule must exist for the trigger medication.",
        ),
        F2_MONITORING: CategorySpec(
            F2_MONITORING,
            FAMILY_2,
            True,
            None,
            (
                "A discharge medication matches an enabled monitoring_dependency "
                "rule and the clean case contains the required monitoring arrangement."
            ),
        ),
        F2_HELD_RESTART: CategorySpec(
            F2_HELD_RESTART,
            FAMILY_2,
            True,
            None,
            (
                "A home medication is held inpatient with a documented reason "
                "and a restart/resumption plan is present."
            ),
        ),
        F2_SUPPLY: CategorySpec(
            F2_SUPPLY,
            FAMILY_2,
            True,
            None,
            (
                "Dose, frequency, days' supply, and follow-up interval are all "
                "parseable, and clean supply covers follow-up."
            ),
        ),
        F2_HOSPITAL_ONLY: CategorySpec(
            F2_HOSPITAL_ONLY,
            FAMILY_2,
            True,
            None,
            (
                "An inpatient-only medication is documented with a stop-at-discharge "
                "plan and is absent from the clean discharge list."
            ),
        ),
        F2_INPATIENT_SUB: CategorySpec(
            F2_INPATIENT_SUB,
            FAMILY_2,
            True,
            None,
            (
                "Home therapy A is replaced inpatient by same-class B for a "
                "documented formulary reason, and clean discharge reverts to A."
            ),
        ),
        F2_PENDING_FOLLOWUP: CategorySpec(
            F2_PENDING_FOLLOWUP,
            FAMILY_2,
            True,
            None,
            (
                "A pending therapeutic decision is documented and a follow-up "
                "visit is scheduled to resolve it."
            ),
        ),
        NONE: CategorySpec(
            NONE,
            FAMILY_NONE,
            True,
            None,
            "No planted error. Intentional documented medication changes may still be present.",
        ),
    }


def canonicalize_category(value: str | None) -> str:
    if value is None or str(value).strip() == "":
        return NONE
    raw = str(value).strip()
    lowered = raw.casefold()
    if raw in CANONICAL_CATEGORIES:
        return raw
    if lowered in CANONICAL_CATEGORIES:
        return lowered
    raise CaseValidationError(
        "error_taxonomy",
        f"unknown error category {value!r}; refusing to substitute another category",
    )


def canonicalize_family(value: str | None, *, category: str | None = None) -> str:
    if category is not None:
        resolved = canonicalize_category(category)
        expected = FAMILY_FOR_CATEGORY[resolved]
        if value is None or str(value).strip() == "":
            return expected
        raw = str(value).strip().casefold()
        allowed = {FAMILY_1, FAMILY_2, FAMILY_NONE}
        if raw not in allowed:
            raise CaseValidationError("error_taxonomy", f"unknown error family {value!r}")
        if raw != expected:
            raise CaseValidationError(
                "error_taxonomy",
                f"error_family {value!r} does not match error_category {resolved}",
            )
        return expected
    if value is None or str(value).strip() == "":
        return FAMILY_NONE
    raw = str(value).strip().casefold()
    if raw in {FAMILY_1, FAMILY_2, FAMILY_NONE}:
        return raw
    raise CaseValidationError("error_taxonomy", f"unknown error family {value!r}")


def categories_equal(left: str | None, right: str | None) -> bool:
    try:
        return canonicalize_category(left) == canonicalize_category(right)
    except CaseValidationError:
        return False


def assert_implementable(category: str) -> None:
    canonical = canonicalize_category(category)
    if canonical in NOT_YET_IMPLEMENTABLE:
        raise CaseValidationError(
            "error_taxonomy",
            f"{canonical} is not_yet_implementable: {NOT_YET_IMPLEMENTABLE[canonical]}",
        )


def resolve_requested_category(
    *,
    inject_error: bool,
    error_category: str | None,
    scenario_target: str | None,
) -> str:
    if not inject_error:
        if error_category not in (None, "", NONE):
            raise CaseValidationError(
                "error_taxonomy",
                "clean control requested but error_category is not none",
            )
        return NONE
    requested = error_category if error_category not in (None, "") else scenario_target
    canonical = canonicalize_category(requested)
    if canonical == NONE:
        raise CaseValidationError(
            "error_taxonomy",
            "error-bearing case requested but error_category is none",
        )
    assert_implementable(canonical)
    return canonical


def load_case_view(session: Session, case: ClinicalCase) -> CaseView:
    medications = list_medications_for_case(session, case.id)
    return CaseView(
        case=case,
        plans=list_plans_for_case(session, case.id),
        medications=medications,
        home=[item for item in medications if item.context == "home"],
        inpatient=[item for item in medications if item.context == "inpatient"],
        discharge=[item for item in medications if item.context == "discharge"],
        monitoring=list_monitoring_for_case(session, case.id),
        followups=list_followups_for_case(session, case.id),
        instructions=list_instructions_for_case(session, case.id),
    )


def plan_rxcui(session: Session, plan: CaseMedicationPlan) -> str | None:
    if plan.ref_medication_id is None:
        return None
    row = session.get(RefMedication, plan.ref_medication_id)
    return row.rxcui if row is not None else None


def medication_rxcui(session: Session, medication: CaseMedication) -> str | None:
    if medication.ref_medication_id is None:
        return None
    row = session.get(RefMedication, medication.ref_medication_id)
    return row.rxcui if row is not None else None


def parse_days(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if text == "":
        return None
    matched = _DAYS_RE.search(text)
    if matched:
        return float(matched.group(1))
    matched = _INT_RE.match(text)
    if matched:
        return float(matched.group(1))
    return None


def contains_needle(value: str | None, needle: str) -> bool:
    if value is None:
        return False
    return needle in value.casefold()


def eligible_errors(session: Session, case: ClinicalCase) -> list[str]:
    """Return canonical categories whose deterministic preconditions hold.

    Unknown or unimplemented categories are never substituted in.
    """
    view = load_case_view(session, case)
    found: list[str] = [NONE]
    if _eligible_omission(session, view):
        found.append(F1_OMISSION)
    if _eligible_commission(session, view):
        found.append(F1_COMMISSION)
    if _eligible_field(session, view, "dose"):
        found.append(F1_DOSE)
    if _eligible_field(session, view, "route"):
        found.append(F1_ROUTE)
    if _eligible_field(session, view, "frequency"):
        found.append(F1_FREQUENCY)
    if class_pairs_for_case(session, view):
        found.append(F1_SUBSTITUTION)
    if _eligible_monitoring(session, view):
        found.append(F2_MONITORING)
    if _eligible_held_restart(view):
        found.append(F2_HELD_RESTART)
    if _eligible_supply(view):
        found.append(F2_SUPPLY)
    if _eligible_hospital_only(session, view):
        found.append(F2_HOSPITAL_ONLY)
    if _eligible_inpatient_substitution(session, view):
        found.append(F2_INPATIENT_SUB)
    if _eligible_pending_followup(view):
        found.append(F2_PENDING_FOLLOWUP)
    return found


def require_eligible(session: Session, case: ClinicalCase, category: str) -> None:
    canonical = canonicalize_category(category)
    if canonical == NONE:
        return
    assert_implementable(canonical)
    allowed = eligible_errors(session, case)
    if canonical not in allowed:
        spec = category_specs()[canonical]
        raise CaseValidationError(
            "error_eligibility",
            f"requested category {canonical} is not eligible for this case; "
            f"precondition: {spec.preconditions}. No substitute category will be injected.",
        )


def detect_findings(session: Session, case: ClinicalCase) -> list[Finding]:
    view = load_case_view(session, case)
    findings: list[Finding] = []
    consumed_plans: set[UUID] = set()
    consumed_discharge: set[UUID] = set()

    findings.extend(
        _find_inpatient_substitutions(session, view, consumed_plans, consumed_discharge)
    )
    findings.extend(
        _find_therapeutic_substitutions(session, view, consumed_plans, consumed_discharge)
    )
    findings.extend(_find_hospital_only(session, view, consumed_plans, consumed_discharge))
    findings.extend(_find_family1_plan_gaps(session, view, consumed_plans, consumed_discharge))
    findings.extend(_find_monitoring_gaps(session, view))
    findings.extend(_find_held_restart_gaps(session, view))
    findings.extend(_find_supply_gaps(view))
    findings.extend(_find_pending_followup_gaps(view))
    return findings


def isolation_errors(
    session: Session,
    case: ClinicalCase,
    *,
    expected_category: str,
) -> list[str]:
    canonical = canonicalize_category(expected_category)
    findings = detect_findings(session, case)
    errors = _duplicate_discharge_errors(session, load_case_view(session, case))
    if canonical == NONE:
        if findings:
            errors.append(
                "clean control has mechanically detectable extra discrepancy: "
                + "; ".join(_finding_label(item) for item in findings)
            )
        return errors
    matching = [item for item in findings if item.category == canonical]
    extra = [item for item in findings if item.category != canonical]
    if len(matching) != 1:
        errors.append(
            f"expected exactly one {canonical} finding, found {len(matching)} "
            f"({', '.join(_finding_label(item) for item in matching) or 'none'})"
        )
    if extra:
        errors.append(
            "mechanically detectable extra discrepancy besides the target: "
            + "; ".join(_finding_label(item) for item in extra)
        )
    return errors


def class_usable_for_substitution(
    *, class_type: str | None, class_id: str, class_name: str
) -> bool:
    """True when RxClass membership is specific enough for therapeutic substitution."""
    ctype = (class_type or "").strip()
    if ctype not in SUBSTITUTION_CLASS_TYPES:
        return False
    if ctype == "ATC1-4" and len(class_id.strip()) < 3:
        return False
    lowered = class_name.casefold()
    return not any(needle in lowered for needle in BROAD_CLASS_NAME_NEEDLES)


def class_pairs_for_case(session: Session, view: CaseView) -> list[ClassPair]:
    case_rxcuis = _case_rxcuis(session, view)
    pairs: list[ClassPair] = []
    seen: set[tuple[str, str]] = set()
    for plan, medication in _continue_discharge_targets(session, view):
        source = (
            session.get(RefMedication, plan.ref_medication_id) if plan.ref_medication_id else None
        )
        if source is None:
            continue
        for hit in _substitutes_for(session, source, case_rxcuis):
            key = (source.rxcui, hit.substitute.rxcui)
            if key in seen:
                continue
            if _pair_violates_hard_rule(session, view, source.rxcui, hit.substitute.rxcui):
                continue
            seen.add(key)
            pairs.append(hit)
        _ = medication
    pairs.sort(key=lambda item: (item.source.rxcui, item.substitute.rxcui, item.class_id))
    return pairs


def _substitutes_for(
    session: Session, source: RefMedication, excluded: set[str]
) -> list[ClassPair]:
    pairs: list[ClassPair] = []
    seen: set[tuple[str, str]] = set()
    classes = list_medication_classes_for_rxcui(session, source.rxcui)
    for membership in classes:
        if not class_usable_for_substitution(
            class_type=membership.class_type,
            class_id=membership.class_id,
            class_name=membership.class_name,
        ):
            continue
        for sibling in list_medications_sharing_class(
            session, membership.class_id, exclude_rxcui=source.rxcui
        ):
            if sibling.rxcui in excluded:
                continue
            key = (sibling.rxcui, membership.class_id)
            if key in seen:
                continue
            seen.add(key)
            pairs.append(ClassPair(source, sibling, membership.class_id, membership.class_name))
    pairs.sort(key=lambda item: (item.substitute.rxcui, item.class_id))
    return pairs


def _eligible_omission(session: Session, view: CaseView) -> bool:
    return bool(_continue_discharge_targets(session, view))


def _eligible_commission(session: Session, view: CaseView) -> bool:
    return bool(_commission_targets(session, view))


def _eligible_field(session: Session, view: CaseView, field_name: str) -> bool:
    for _plan, medication in _continue_discharge_targets(session, view):
        if getattr(medication, field_name):
            return True
    return False


def _eligible_monitoring(session: Session, view: CaseView) -> bool:
    return bool(_monitoring_targets(session, view))


def _eligible_held_restart(view: CaseView) -> bool:
    return bool(_held_restart_targets(view))


def _eligible_supply(view: CaseView) -> bool:
    followup_days = _followup_days(view)
    if followup_days is None:
        return False
    for medication in view.discharge:
        if medication.status == "held":
            continue
        supply = parse_days(medication.quantity_or_days)
        if supply is None or medication.dose is None or medication.frequency is None:
            continue
        if supply >= followup_days:
            return True
    return False


def _eligible_hospital_only(session: Session, view: CaseView) -> bool:
    discharge_ids = {item.ref_medication_id for item in view.discharge if item.ref_medication_id}
    for plan in view.plans:
        if not _is_hospital_only_plan(plan):
            continue
        if plan.ref_medication_id in discharge_ids:
            continue
        if _plan_has_inpatient(session, view, plan):
            return True
    return False


def _eligible_inpatient_substitution(session: Session, view: CaseView) -> bool:
    return bool(_inpatient_substitution_clean_targets(session, view))


def _eligible_pending_followup(view: CaseView) -> bool:
    return _has_pending_decision(view) and bool(view.followups)


def _continue_discharge_targets(
    session: Session, view: CaseView
) -> list[tuple[CaseMedicationPlan, CaseMedication]]:
    by_ref = {
        item.ref_medication_id: item
        for item in view.discharge
        if item.ref_medication_id is not None and item.status != "held"
    }
    found: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan in view.plans:
        if plan.correct_discharge_state != "continue":
            continue
        if plan.ref_medication_id is None:
            continue
        medication = by_ref.get(plan.ref_medication_id)
        if medication is None:
            continue
        found.append((plan, medication))
    found.sort(key=lambda item: (plan_rxcui(session, item[0]) or "", item[0].plan_id or ""))
    return found


def _commission_targets(
    session: Session, view: CaseView
) -> list[tuple[CaseMedicationPlan, CaseMedication]]:
    discharge_ids = {
        item.ref_medication_id
        for item in view.discharge
        if item.ref_medication_id and item.status != "held"
    }
    by_home = {item.ref_medication_id: item for item in view.home if item.ref_medication_id}
    found: list[tuple[CaseMedicationPlan, CaseMedication]] = []
    for plan in view.plans:
        if _is_hospital_only_plan(plan):
            continue
        if plan.decision != "stop" or plan.correct_discharge_state != "stop":
            continue
        if plan.ref_medication_id is None or plan.ref_medication_id in discharge_ids:
            continue
        home_row = by_home.get(plan.ref_medication_id)
        if home_row is None:
            continue
        found.append((plan, home_row))
    found.sort(key=lambda item: (plan_rxcui(session, item[0]) or "", item[1].drug or ""))
    return found


def _monitoring_targets(session: Session, view: CaseView) -> list[tuple[CaseMedication, str, str]]:
    discharge_rxcuis = {
        medication_rxcui(session, item): item
        for item in view.discharge
        if medication_rxcui(session, item) and item.status != "held"
    }
    found: list[tuple[CaseMedication, str, str]] = []
    for rule in list_enabled_rules(session):
        constraint = rule.constraint_json if isinstance(rule.constraint_json, dict) else {}
        if str(constraint.get("action") or "") != "require_lab":
            continue
        if not rule.input_rxcui or rule.input_rxcui not in discharge_rxcuis:
            continue
        medication = discharge_rxcuis[rule.input_rxcui]
        if not _monitoring_present(view, medication):
            continue
        lab = rule.input_loinc_code or str(constraint.get("loinc_code") or "")
        found.append((medication, rule.rule_code, lab))
    return found


def _held_restart_targets(view: CaseView) -> list[CaseMedicationPlan]:
    found: list[CaseMedicationPlan] = []
    for plan in view.plans:
        if plan.decision != "restart":
            continue
        if not _held_evidence(view, plan):
            continue
        if not _restart_plan_present(view, plan):
            continue
        found.append(plan)
    return found


def _inpatient_substitution_clean_targets(
    session: Session, view: CaseView
) -> list[tuple[CaseMedicationPlan, CaseMedicationPlan, str, str]]:
    found: list[tuple[CaseMedicationPlan, CaseMedicationPlan, str, str]] = []
    home_ids = {item.ref_medication_id for item in view.home if item.ref_medication_id}
    inpatient_ids = {item.ref_medication_id for item in view.inpatient if item.ref_medication_id}
    discharge_ids = {
        item.ref_medication_id
        for item in view.discharge
        if item.ref_medication_id and item.status != "held"
    }
    for home_plan in view.plans:
        if home_plan.correct_discharge_state != "continue" or home_plan.ref_medication_id is None:
            continue
        if home_plan.ref_medication_id not in home_ids:
            continue
        if home_plan.ref_medication_id not in discharge_ids:
            continue
        if home_plan.ref_medication_id in inpatient_ids:
            continue
        for sub_plan in view.plans:
            if sub_plan.id == home_plan.id or sub_plan.ref_medication_id is None:
                continue
            if sub_plan.correct_discharge_state != "stop":
                continue
            if sub_plan.ref_medication_id not in inpatient_ids:
                continue
            if sub_plan.ref_medication_id in discharge_ids:
                continue
            if not _has_formulary_reason(view, sub_plan):
                continue
            if not _has_revert_instruction(view):
                continue
            source = session.get(RefMedication, home_plan.ref_medication_id)
            substitute = session.get(RefMedication, sub_plan.ref_medication_id)
            if source is None or substitute is None:
                continue
            shared = _shared_class(session, source.rxcui, substitute.rxcui)
            if shared is None:
                continue
            found.append((home_plan, sub_plan, shared[0], shared[1]))
    return found


def _find_inpatient_substitutions(
    session: Session,
    view: CaseView,
    consumed_plans: set[UUID],
    consumed_discharge: set[UUID],
) -> list[Finding]:
    findings: list[Finding] = []
    home_ids = {item.ref_medication_id for item in view.home if item.ref_medication_id}
    inpatient_by_ref = {
        item.ref_medication_id: item for item in view.inpatient if item.ref_medication_id
    }
    discharge_by_ref = {
        item.ref_medication_id: item
        for item in view.discharge
        if item.ref_medication_id and item.status != "held"
    }
    for home_plan in view.plans:
        if home_plan.id in consumed_plans or home_plan.ref_medication_id is None:
            continue
        if home_plan.correct_discharge_state != "continue":
            continue
        if home_plan.ref_medication_id not in home_ids:
            continue
        if home_plan.ref_medication_id in inpatient_by_ref:
            continue
        if home_plan.ref_medication_id in discharge_by_ref:
            continue
        for sub_plan in view.plans:
            if sub_plan.id in consumed_plans or sub_plan.ref_medication_id is None:
                continue
            listed = discharge_by_ref.get(sub_plan.ref_medication_id)
            if listed is None or listed.id in consumed_discharge:
                continue
            if sub_plan.ref_medication_id not in inpatient_by_ref:
                continue
            if _has_revert_instruction(view):
                continue
            source = session.get(RefMedication, home_plan.ref_medication_id)
            substitute = session.get(RefMedication, sub_plan.ref_medication_id)
            if source is None or substitute is None:
                continue
            shared = _shared_class(session, source.rxcui, substitute.rxcui)
            if shared is None:
                continue
            consumed_plans.add(home_plan.id)
            consumed_plans.add(sub_plan.id)
            consumed_discharge.add(listed.id)
            findings.append(
                Finding(
                    F2_INPATIENT_SUB,
                    source.rxcui,
                    home_plan.drug,
                    "discharge_medication",
                    "Inpatient substitute remains at discharge without a documented revert.",
                    {
                        "source_rxcui": source.rxcui,
                        "substitute_rxcui": substitute.rxcui,
                        "class_id": shared[0],
                        "class_name": shared[1],
                    },
                )
            )
    return findings


def _find_therapeutic_substitutions(
    session: Session,
    view: CaseView,
    consumed_plans: set[UUID],
    consumed_discharge: set[UUID],
) -> list[Finding]:
    findings: list[Finding] = []
    planned_ids = {plan.ref_medication_id for plan in view.plans if plan.ref_medication_id}
    discharge_unplanned = [
        item
        for item in view.discharge
        if item.ref_medication_id is not None
        and item.status != "held"
        and item.id not in consumed_discharge
        and item.ref_medication_id not in planned_ids
    ]
    inpatient_ids = {item.ref_medication_id for item in view.inpatient if item.ref_medication_id}
    for plan in view.plans:
        if plan.id in consumed_plans or plan.correct_discharge_state != "continue":
            continue
        if plan.ref_medication_id is None:
            continue
        if any(
            item.ref_medication_id == plan.ref_medication_id and item.status != "held"
            for item in view.discharge
        ):
            continue
        if plan.ref_medication_id not in inpatient_ids:
            continue
        source = session.get(RefMedication, plan.ref_medication_id)
        if source is None:
            continue
        for listed in discharge_unplanned:
            if listed.id in consumed_discharge:
                continue
            substitute = session.get(RefMedication, listed.ref_medication_id)
            if substitute is None:
                continue
            shared = _shared_class(session, source.rxcui, substitute.rxcui)
            if shared is None:
                continue
            consumed_plans.add(plan.id)
            consumed_discharge.add(listed.id)
            findings.append(
                Finding(
                    F1_SUBSTITUTION,
                    source.rxcui,
                    plan.drug,
                    "drug",
                    "Discharge lists a same-class substitute without a documented explanation.",
                    {
                        "expected_rxcui": source.rxcui,
                        "planted_rxcui": substitute.rxcui,
                        "class_id": shared[0],
                        "class_name": shared[1],
                    },
                )
            )
            break
    return findings


def _find_hospital_only(
    session: Session,
    view: CaseView,
    consumed_plans: set[UUID],
    consumed_discharge: set[UUID],
) -> list[Finding]:
    findings: list[Finding] = []
    by_discharge = {
        item.ref_medication_id: item
        for item in view.discharge
        if item.ref_medication_id and item.status != "held"
    }
    for plan in view.plans:
        if plan.id in consumed_plans or not _is_hospital_only_plan(plan):
            continue
        ref_id = plan.ref_medication_id
        if ref_id is None:
            continue
        listed = by_discharge.get(ref_id)
        if listed is None or listed.id in consumed_discharge:
            continue
        consumed_plans.add(plan.id)
        consumed_discharge.add(listed.id)
        findings.append(
            Finding(
                F2_HOSPITAL_ONLY,
                plan_rxcui(session, plan),
                plan.drug,
                "discharge_medication",
                "Hospital-only medication was continued at discharge.",
            )
        )
    return findings


def _find_family1_plan_gaps(
    session: Session,
    view: CaseView,
    consumed_plans: set[UUID],
    consumed_discharge: set[UUID],
) -> list[Finding]:
    findings: list[Finding] = []
    home_by_ref = {item.ref_medication_id: item for item in view.home if item.ref_medication_id}
    discharge_by_ref = {
        item.ref_medication_id: item
        for item in view.discharge
        if item.ref_medication_id is not None and item.status != "held"
    }
    for plan in view.plans:
        if plan.id in consumed_plans or plan.ref_medication_id is None:
            continue
        listed = discharge_by_ref.get(plan.ref_medication_id)
        if listed is not None and listed.id in consumed_discharge:
            continue
        if plan.correct_discharge_state == "continue" and listed is None:
            if plan.decision == "restart":
                continue
            findings.append(
                Finding(
                    F1_OMISSION,
                    plan_rxcui(session, plan),
                    plan.drug,
                    "presence",
                    "Intended discharge medication is absent from the discharge list.",
                )
            )
            consumed_plans.add(plan.id)
            continue
        if (
            plan.correct_discharge_state == "stop"
            and listed is not None
            and not _is_hospital_only_plan(plan)
        ):
            findings.append(
                Finding(
                    F1_COMMISSION,
                    plan_rxcui(session, plan),
                    plan.drug,
                    "presence",
                    "Unindicated medication appears on the discharge list.",
                )
            )
            consumed_plans.add(plan.id)
            consumed_discharge.add(listed.id)
            continue
        if plan.correct_discharge_state != "continue" or listed is None:
            continue
        home = home_by_ref.get(plan.ref_medication_id)
        if home is None:
            continue
        if (home.dose or "") != (listed.dose or ""):
            findings.append(
                Finding(
                    F1_DOSE,
                    plan_rxcui(session, plan),
                    plan.drug,
                    "dose",
                    "Discharge dose differs from the intended plan.",
                    {"expected": home.dose, "planted": listed.dose},
                )
            )
            consumed_plans.add(plan.id)
        elif (home.route or "") != (listed.route or ""):
            findings.append(
                Finding(
                    F1_ROUTE,
                    plan_rxcui(session, plan),
                    plan.drug,
                    "route",
                    "Discharge route differs from the intended plan.",
                    {"expected": home.route, "planted": listed.route},
                )
            )
            consumed_plans.add(plan.id)
        elif (home.frequency or "") != (listed.frequency or ""):
            findings.append(
                Finding(
                    F1_FREQUENCY,
                    plan_rxcui(session, plan),
                    plan.drug,
                    "frequency",
                    "Discharge frequency differs from the intended plan.",
                    {"expected": home.frequency, "planted": listed.frequency},
                )
            )
            consumed_plans.add(plan.id)
    return findings


def _find_monitoring_gaps(session: Session, view: CaseView) -> list[Finding]:
    findings: list[Finding] = []
    discharge_rxcuis = {
        medication_rxcui(session, item): item
        for item in view.discharge
        if medication_rxcui(session, item) and item.status != "held"
    }
    for rule in list_enabled_rules(session):
        constraint = rule.constraint_json if isinstance(rule.constraint_json, dict) else {}
        if str(constraint.get("action") or "") != "require_lab":
            continue
        if not rule.input_rxcui or rule.input_rxcui not in discharge_rxcuis:
            continue
        medication = discharge_rxcuis[rule.input_rxcui]
        if _monitoring_present(view, medication):
            continue
        lab = rule.input_loinc_code or str(constraint.get("loinc_code") or "")
        findings.append(
            Finding(
                F2_MONITORING,
                rule.input_rxcui,
                medication.drug,
                "monitoring",
                "Required outpatient monitoring is not arranged.",
                {"rule_code": rule.rule_code, "required_lab": lab},
            )
        )
    return findings


def _find_held_restart_gaps(session: Session, view: CaseView) -> list[Finding]:
    findings: list[Finding] = []
    for plan in view.plans:
        if plan.decision != "restart":
            continue
        if not _held_evidence(view, plan):
            continue
        if _restart_plan_present(view, plan):
            continue
        findings.append(
            Finding(
                F2_HELD_RESTART,
                plan_rxcui(session, plan),
                plan.drug,
                "restart_plan",
                "Held medication has no documented resumption criterion or timing.",
            )
        )
    return findings


def _find_supply_gaps(view: CaseView) -> list[Finding]:
    followup_days = _followup_days(view)
    if followup_days is None:
        return []
    findings: list[Finding] = []
    for medication in view.discharge:
        if medication.status == "held":
            continue
        supply = parse_days(medication.quantity_or_days)
        if supply is None:
            continue
        if medication.dose is None or medication.frequency is None:
            continue
        if supply < followup_days:
            findings.append(
                Finding(
                    F2_SUPPLY,
                    None,
                    medication.drug,
                    "quantity_or_days",
                    "Days' supply does not cover the planned follow-up interval.",
                    {
                        "supply_days": supply,
                        "followup_days": followup_days,
                        "dose": medication.dose,
                        "frequency": medication.frequency,
                    },
                )
            )
    return findings


def _find_pending_followup_gaps(view: CaseView) -> list[Finding]:
    if not _has_pending_decision(view):
        return []
    if view.followups:
        return []
    return [
        Finding(
            F2_PENDING_FOLLOWUP,
            None,
            None,
            "followup",
            "Pending therapeutic decision has no follow-up arranged.",
        )
    ]


def _monitoring_present(view: CaseView, medication: CaseMedication) -> bool:
    if contains_needle(medication.monitoring, MONITORING_NEEDLE):
        return True
    return bool(view.monitoring)


def _held_evidence(view: CaseView, plan: CaseMedicationPlan) -> bool:
    rows = [
        item
        for item in view.medications
        if item.ref_medication_id == plan.ref_medication_id
        and item.context in {"home", "inpatient", "discharge"}
    ]
    return any(item.status == "held" and item.held_reason for item in rows)


def _restart_plan_present(view: CaseView, plan: CaseMedicationPlan) -> bool:
    for instruction in view.instructions:
        if contains_needle(instruction.instruction_text, RESTART_NEEDLE):
            return True
    for medication in view.medications:
        if medication.ref_medication_id != plan.ref_medication_id:
            continue
        if contains_needle(medication.target_or_goal, RESTART_NEEDLE):
            return True
    return False


def _has_pending_decision(view: CaseView) -> bool:
    return any(
        contains_needle(item.instruction_text, PENDING_DECISION_NEEDLE)
        for item in view.instructions
    )


def _has_revert_instruction(view: CaseView) -> bool:
    return any(
        contains_needle(item.instruction_text, REVERT_SUB_NEEDLE) for item in view.instructions
    )


def _has_formulary_reason(view: CaseView, plan: CaseMedicationPlan) -> bool:
    if contains_needle(plan.decision_reason, FORMULARY_SUB_NEEDLE):
        return True
    return any(
        contains_needle(item.indication, FORMULARY_SUB_NEEDLE)
        for item in view.medications
        if item.ref_medication_id == plan.ref_medication_id
    )


def _is_hospital_only_plan(plan: CaseMedicationPlan) -> bool:
    if plan.home_state not in {None, "absent"}:
        return False
    if plan.inpatient_state not in {"new_start", "continue"}:
        return False
    return plan.correct_discharge_state == "stop" and contains_needle(
        plan.decision_reason, HOSPITAL_ONLY_NEEDLE
    )


def _plan_has_inpatient(session: Session, view: CaseView, plan: CaseMedicationPlan) -> bool:
    _ = session
    return any(
        item.ref_medication_id == plan.ref_medication_id and item.context == "inpatient"
        for item in view.medications
    )


def _followup_days(view: CaseView) -> float | None:
    values = [parse_days(item.timing) for item in view.followups]
    numeric = [item for item in values if item is not None]
    if not numeric:
        return None
    return max(numeric)


def _shared_class(session: Session, left: str, right: str) -> tuple[str, str] | None:
    left_classes = {
        (item.class_id, item.class_name)
        for item in list_medication_classes_for_rxcui(session, left)
        if class_usable_for_substitution(
            class_type=item.class_type, class_id=item.class_id, class_name=item.class_name
        )
    }
    right_ids = {
        item.class_id
        for item in list_medication_classes_for_rxcui(session, right)
        if class_usable_for_substitution(
            class_type=item.class_type, class_id=item.class_id, class_name=item.class_name
        )
    }
    shared = sorted(item for item in left_classes if item[0] in right_ids)
    if not shared:
        return None
    return shared[0]


def _duplicate_discharge_errors(session: Session, view: CaseView) -> list[str]:
    seen: dict[str, str] = {}
    for item in view.discharge:
        if item.status == "held":
            continue
        rxcui = medication_rxcui(session, item)
        if not rxcui:
            continue
        if rxcui in seen:
            return [
                f"duplicate discharge medication {rxcui} was introduced in addition to the target"
            ]
        seen[rxcui] = item.drug or rxcui
    return []


def _case_rxcuis(session: Session, view: CaseView) -> set[str]:
    found: set[str] = set()
    for medication in view.medications:
        rxcui = medication_rxcui(session, medication)
        if rxcui:
            found.add(rxcui)
    return found


def _pair_violates_hard_rule(
    session: Session, view: CaseView, source_rxcui: str, substitute_rxcui: str
) -> bool:
    rxcuis = _case_rxcuis(session, view)
    rxcuis.add(substitute_rxcui)
    rxcuis.add(source_rxcui)
    loinc_codes: set[str] = set()
    for lab in list_labs_for_case(session, view.case.id):
        if lab.ref_lab_id is None:
            continue
        lab_row = session.get(RefLabTest, lab.ref_lab_id)
        if lab_row is not None:
            loinc_codes.add(lab_row.loinc_code)
    snapshot = CaseSnapshot(
        age=view.case.patient_age,
        sex=view.case.patient_gender,
        care_context="inpatient",
        icd10cm_codes=frozenset(),
        rxcuis=frozenset(rxcuis),
        loinc_codes=frozenset(loinc_codes),
    )
    return bool(hard_violations(evaluate_rules(session, snapshot)))


def _finding_label(item: Finding) -> str:
    target = item.drug or item.rxcui or "unknown"
    return f"{item.category}:{target}"


continue_discharge_targets = _continue_discharge_targets
commission_targets = _commission_targets
monitoring_targets = _monitoring_targets
held_restart_targets = _held_restart_targets
inpatient_substitution_clean_targets = _inpatient_substitution_clean_targets
is_hospital_only_plan = _is_hospital_only_plan
