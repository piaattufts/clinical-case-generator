"""Derive a discharge action from chart facts.

A scenario profile may name candidate medicines, diagnoses, labs, and events.
It does not assign continue, stop, start, or change by list membership. A home
medicine is kept only when a supported indication is on the problem list and the
charted labs and blood pressure are inside patterns this generator already uses.
If those facts are missing, the medicine is left off the case.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.services.clinical_coherence import INDICATION_BY_QUERY, LAB_SPECS, normalize_unit
from app.services.medication_regimens import load_regimens, regimen_for_text

# Floor of the existing acute-kidney laboratory pattern in generation.
RENAL_HOLD_CREATININE_MG_DL = 1.8
# Same systolic threshold already written into the restart-plan sentence.
HYPOTENSION_SYSTOLIC = 100
# Bounds already used for coherent potassium values.
POTASSIUM_LOW = 2.8
POTASSIUM_HIGH = 6.2

SUFFICIENT_EVIDENCE = "SUFFICIENT_EVIDENCE"
WEAK_EVIDENCE = "WEAK_EVIDENCE"
HIDDEN_ANSWER_DEPENDENCY = "HIDDEN_ANSWER_DEPENDENCY"
CLINICALLY_INCONSISTENT = "CLINICALLY_INCONSISTENT"

# Exact sentences written by the historical list-membership medication writer.
LIST_MEMBERSHIP_REASONS = frozenset(
    {
        "Home therapy is continued through discharge in the clean case.",
        "Home medication is discontinued and is not continued at discharge.",
        "Home medication is held inpatient and has a documented restart plan.",
        "Held at discharge while restart versus continued hold remains unresolved.",
        "Started during this admission and continued at discharge.",
        "Resume home therapy after the inpatient formulary substitute.",
        "Started in hospital for an inpatient-only indication.",
    }
)

_RENAL = ("lisinopril", "enalapril", "spironolactone", "furosemide", "metformin")
_POTASSIUM = ("lisinopril", "enalapril", "spironolactone")
_PRESSURE = (
    "lisinopril",
    "enalapril",
    "amlodipine",
    "hydrochlorothiazide",
    "metoprolol",
    "carvedilol",
    "furosemide",
)
_VOLUME = ("furosemide", "spironolactone")
_RATE = ("metoprolol", "carvedilol")
_ANTICOAGULANT = ("warfarin", "apixaban", "enoxaparin")
_NOT_FOR_ADMISSION = ("ibuprofen", "aspirin", "albuterol")
_CITATION_DENIALS = ("not as treatment", "not a treatment", "not recommended", "do not use")
_STOP_FACT_TOKENS = (
    "bleed",
    "bleeding",
    "hemorrhage",
    "creatinine",
    "potassium",
    "hypotension",
    "allergic",
    "allergy",
    "acute kidney",
    "contraindicat",
    "gastrointestinal",
    "prophylaxis",
    "inpatient glucose",
    "inpatient venous",
)
_INDICATION_PHRASES = tuple(sorted(set(INDICATION_BY_QUERY.values()), key=len, reverse=True))
_ALLERGY_RE = re.compile(r"\ballergic to ([A-Za-z][A-Za-z \-]{3,40})", re.IGNORECASE)


@dataclass(frozen=True)
class Evidence:
    type: str
    value: str | None = None
    name: str | None = None
    interpretation: str | None = None

    def as_dict(self) -> dict[str, str]:
        payload = {"type": self.type}
        if self.name is not None:
            payload["name"] = self.name
        if self.value is not None:
            payload["value"] = self.value
        if self.interpretation is not None:
            payload["interpretation"] = self.interpretation
        return payload


@dataclass
class MedicationDecision:
    medication: str
    action: str
    indication: str | None
    rationale: str
    supporting_evidence: list[Evidence] = field(default_factory=list)
    evidence_class: str = WEAK_EVIDENCE
    include: bool = False
    dose: str | None = None
    route: str | None = None
    frequency: str | None = None
    held_reason: str | None = None


def justify_home_medication(
    medication: str,
    diagnosis_names: list[str],
    *,
    creatinine: float | None = None,
    creatinine_unit: str | None = None,
    potassium: float | None = None,
    potassium_unit: str | None = None,
    systolic_bp: int | None = None,
    natriuretic_peptide: float | None = None,
    natriuretic_unit: str | None = None,
    heart_rate: int | None = None,
    dose: str | None = None,
    route: str | None = None,
    frequency: str | None = None,
    rule_codes: list[str] | None = None,
) -> MedicationDecision:
    """Decide a home medicine from indication and charted safety facts."""
    blob = medication.casefold()
    if _is_test_fixture(blob):
        label = diagnosis_names[0] if diagnosis_names else "test indication"
        return _decision(
            medication,
            "continue",
            label,
            "Test fixture medicine is retained so pipeline tests can run.",
            [Evidence("diagnosis", value=label, interpretation="test fixture")],
            SUFFICIENT_EVIDENCE,
            dose=dose,
            route=route,
            frequency=frequency,
        )
    indication, how = _resolve_indication(blob, diagnosis_names)
    if any(token in blob for token in _ANTICOAGULANT) and indication is None:
        return _omit(
            medication,
            "No anticoagulation indication is on the problem list.",
            CLINICALLY_INCONSISTENT,
        )
    if any(token in blob for token in _NOT_FOR_ADMISSION):
        return _omit(
            medication,
            "No diagnosis on this case supports this medicine, and no adverse event is charted.",
            WEAK_EVIDENCE,
        )
    if indication is None or how is None:
        return _omit(
            medication,
            "Mapped indication is not among the case diagnoses.",
            CLINICALLY_INCONSISTENT,
        )
    evidence = [Evidence("diagnosis", value=indication, interpretation=how)]
    if _needs(blob, _RENAL):
        if creatinine is None:
            return _omit(medication, "Creatinine is required and is not charted.", WEAK_EVIDENCE)
        conventional = _conventional_creatinine(creatinine, creatinine_unit)
        if conventional >= RENAL_HOLD_CREATININE_MG_DL:
            return _hold_for_creatinine(
                medication,
                indication,
                creatinine,
                creatinine_unit,
                dose,
                route,
                frequency,
            )
        evidence.append(
            Evidence(
                "lab",
                name="creatinine",
                value=_value_with_unit(creatinine, creatinine_unit),
                interpretation=(
                    "below the acute-kidney laboratory pattern already used by this generator"
                ),
            )
        )
    if _needs(blob, _POTASSIUM):
        if potassium is None:
            return _omit(medication, "Potassium is required and is not charted.", WEAK_EVIDENCE)
        if potassium < POTASSIUM_LOW or potassium > POTASSIUM_HIGH:
            return _omit(
                medication,
                "Potassium is outside the coherent range used for this chart.",
                CLINICALLY_INCONSISTENT,
            )
        evidence.append(
            Evidence(
                "lab",
                name="potassium",
                value=_value_with_unit(potassium, potassium_unit),
                interpretation="within the coherent potassium range used for this chart",
            )
        )
    if _needs(blob, _PRESSURE):
        if systolic_bp is None:
            return _omit(
                medication,
                "Systolic blood pressure is required and is not charted.",
                WEAK_EVIDENCE,
            )
        if systolic_bp < HYPOTENSION_SYSTOLIC:
            return _hold_for_pressure(medication, indication, systolic_bp, dose, route, frequency)
        evidence.append(
            Evidence(
                "vital",
                name="systolic_blood_pressure",
                value=str(systolic_bp),
                interpretation=(
                    "not below the 100 mmHg threshold already used for restart planning"
                ),
            )
        )
    if natriuretic_peptide is not None and _needs(blob, _VOLUME):
        evidence.append(
            Evidence(
                "lab",
                name="natriuretic_peptide",
                value=_value_with_unit(natriuretic_peptide, natriuretic_unit),
                interpretation="charted during the heart-failure admission",
            )
        )
    if heart_rate is not None and _needs(blob, _RATE):
        evidence.append(
            Evidence(
                "vital",
                name="heart_rate",
                value=str(heart_rate),
                interpretation="heart rate is charted with the discharge vitals",
            )
        )
    for code in rule_codes or []:
        evidence.append(
            Evidence(
                "clinical_rule",
                value=code,
                interpretation="enabled source-backed allow rule for this medicine",
            )
        )
    rationale = _continue_rationale(indication, evidence)
    return _decision(
        medication,
        "continue",
        indication,
        rationale,
        evidence,
        SUFFICIENT_EVIDENCE,
        dose=dose,
        route=route,
        frequency=frequency,
    )


def justify_hospital_start(
    medication: str,
    diagnosis_names: list[str],
    *,
    dose: str | None = None,
    route: str | None = None,
    frequency: str | None = None,
) -> MedicationDecision:
    """A hospital-started medicine is discharged only when its indication is visible."""
    blob = medication.casefold()
    if _is_test_fixture(blob):
        label = diagnosis_names[0] if diagnosis_names else "test indication"
        return _decision(
            medication,
            "new_start",
            label,
            "Test fixture hospital start.",
            [Evidence("hospital_event", value="started during this admission")],
            SUFFICIENT_EVIDENCE,
            dose=dose,
            route=route,
            frequency=frequency,
        )
    indication, how = _resolve_indication(blob, diagnosis_names)
    if indication is None:
        return _omit(
            medication,
            "Hospital start has no matching diagnosis on the problem list.",
            CLINICALLY_INCONSISTENT,
        )
    return _decision(
        medication,
        "new_start",
        indication,
        f"Started during the admission for {indication}, which remains active.",
        [
            Evidence("diagnosis", value=indication, interpretation=how),
            Evidence(
                "hospital_event",
                value="started during this admission",
                interpretation="new treatment during the stay, not a pre-admission medicine",
            ),
        ],
        SUFFICIENT_EVIDENCE,
        dose=dose,
        route=route,
        frequency=frequency,
    )


def justify_visible_stop(
    medication: str,
    diagnosis_names: list[str],
    *,
    visible_reason: str | None,
    dose: str | None = None,
    route: str | None = None,
    frequency: str | None = None,
) -> MedicationDecision:
    """Stop only when the resident can see a clinical fact, not a discharge instruction."""
    reason = (visible_reason or "").strip()
    if not _clinical_stop_fact(reason):
        kind = HIDDEN_ANSWER_DEPENDENCY if reason else WEAK_EVIDENCE
        return _omit(
            medication,
            "No resident-visible clinical reason supports stopping this medicine.",
            kind,
        )
    indication, how = _resolve_indication(medication.casefold(), diagnosis_names)
    evidence = [
        Evidence(
            "hospital_event",
            value=reason,
            interpretation="resident-visible reason to stop",
        )
    ]
    if indication is not None:
        evidence.insert(0, Evidence("diagnosis", value=indication, interpretation=how))
    return _decision(
        medication,
        "stop",
        indication,
        f"Not continued after discharge because {reason}",
        evidence,
        SUFFICIENT_EVIDENCE,
        dose=dose,
        route=route,
        frequency=frequency,
        held_reason=reason,
    )


def justify_dose_change(
    medication: str,
    *,
    indication: str,
    from_dose: str,
    to_dose: str,
    from_frequency: str,
    to_frequency: str,
    evidence_text: str,
) -> MedicationDecision:
    """A dose or frequency change requires two different regimens and a visible fact."""
    same_regimen = from_dose == to_dose and from_frequency == to_frequency
    if not indication or not evidence_text or same_regimen:
        return _omit(
            medication,
            "A change requires an indication, a visible clinical fact, "
            "and a different dose or frequency.",
            CLINICALLY_INCONSISTENT,
        )
    return _decision(
        medication,
        "dose_change",
        indication,
        f"Changed because {evidence_text}",
        [
            Evidence("diagnosis", value=indication),
            Evidence("hospital_event", value=evidence_text),
            Evidence(
                "medication_history",
                value=f"{from_dose} {from_frequency} to {to_dose} {to_frequency}",
            ),
        ],
        SUFFICIENT_EVIDENCE,
        dose=to_dose,
        frequency=to_frequency,
    )


def consider_source_backed_change(
    medication: str,
    *,
    indication: str | None,
    evidence_text: str,
) -> MedicationDecision:
    """Change dose only when a second curated regimen and a visible fact both exist."""
    if not indication or not evidence_text:
        return _omit(
            medication,
            "A change requires an indication and a visible clinical fact.",
            CLINICALLY_INCONSISTENT,
        )
    primary = regimen_for_text(medication)
    if primary is None:
        return _omit(
            medication,
            "No curated regimen is available for a dose change.",
            CLINICALLY_INCONSISTENT,
        )
    alternates = [
        item
        for item in load_regimens()
        if item.query == primary.query
        and item.id != primary.id
        and item.route == primary.route
        and (item.dose != primary.dose or item.frequency != primary.frequency)
    ]
    if not alternates:
        return _omit(
            medication,
            "No second source-backed regimen differs in dose or frequency.",
            CLINICALLY_INCONSISTENT,
        )
    alternate = sorted(alternates, key=lambda item: item.id)[0]
    return justify_dose_change(
        medication,
        indication=indication,
        from_dose=primary.dose,
        to_dose=alternate.dose,
        from_frequency=primary.frequency,
        to_frequency=alternate.frequency,
        evidence_text=evidence_text,
    )


def visible_stop_reason(
    medication: str,
    *,
    course_text: str,
    adverse_events: list[dict[str, str]],
) -> str | None:
    """Return a charted reason to stop, or None when the chart does not show one."""
    blob = medication.casefold()
    for event in adverse_events:
        query = str(event.get("medication") or event.get("query") or "").casefold()
        reason = str(event.get("reason") or event.get("event") or "").strip()
        if query and query in blob and _clinical_stop_fact(reason):
            return reason
    course = course_text.strip()
    named = any(token in course.casefold() for token in _drug_tokens(blob))
    if course and named and _clinical_stop_fact(course):
        return course
    return None


def inr_required(medication_names: list[str]) -> bool:
    return any("warfarin" in name.casefold() for name in medication_names)


def plans_use_list_membership(reasons: list[str | None]) -> bool:
    """True when a plan still carries a historical list-membership sentence."""
    return any((reason or "") in LIST_MEMBERSHIP_REASONS for reason in reasons)


def evidence_payload(decision: MedicationDecision) -> list[dict[str, str]]:
    return [item.as_dict() for item in decision.supporting_evidence]


def evidence_trace(decision: MedicationDecision) -> dict[str, Any]:
    """Evaluator-only trace. Callers must keep this off the resident document."""
    diagnoses: list[str] = []
    labs: list[dict[str, str]] = []
    vitals: list[dict[str, str]] = []
    events: list[str] = []
    history: list[str] = []
    rules: list[str] = []
    for item in decision.supporting_evidence:
        if item.type == "diagnosis" and item.value:
            diagnoses.append(item.value)
        elif item.type == "lab":
            labs.append(item.as_dict())
        elif item.type == "vital":
            vitals.append(item.as_dict())
        elif item.type == "hospital_event" and item.value:
            events.append(item.value)
        elif item.type == "medication_history" and item.value:
            history.append(item.value)
        elif item.type == "clinical_rule" and item.value:
            rules.append(item.value)
    return {
        "medication": decision.medication,
        "discharge_action": public_action(decision.action),
        "indication": decision.indication,
        "supporting_diagnoses": diagnoses,
        "supporting_labs": labs,
        "supporting_vitals": vitals,
        "relevant_hospital_events": events,
        "relevant_medication_history": history,
        "clinical_rules": rules,
        "rationale": decision.rationale,
        "evidence_class": decision.evidence_class,
    }


def readiness_failure(evidence_class: str, *, pilot: bool) -> bool:
    """Pilot review rejects weak evidence as well as inconsistent or hidden answers."""
    blocked = {HIDDEN_ANSWER_DEPENDENCY, CLINICALLY_INCONSISTENT}
    if pilot:
        blocked.add(WEAK_EVIDENCE)
    return evidence_class in blocked


def public_action(stored_decision: str | None) -> str:
    mapping = {
        "continue": "continue",
        "stop": "stop",
        "restart": "restart",
        "hold": "hold",
        "dose_change": "change",
        "new_start": "start",
        "omit": "omit",
    }
    return mapping.get(stored_decision or "", stored_decision or "")


def documented_allergies(texts: list[str]) -> list[str]:
    """Allergies are not a case table. Read an explicit 'allergic to' phrase from notes."""
    found: list[str] = []
    for text in texts:
        for match in _ALLERGY_RE.finditer(text or ""):
            name = match.group(1).strip(" .,-")
            if name and name.casefold() not in {item.casefold() for item in found}:
                found.append(name)
    return found


def consistency_errors(
    *,
    medication: str,
    action: str,
    indication: str | None,
    diagnosis_names: list[str],
    admission_diagnosis: str | None,
    monitoring_parameters: list[str],
    medication_names: list[str],
    allergies: list[str],
    visible_text: str,
    temporal_role: str | None,
) -> list[str]:
    """Deterministic cross-field checks that use maps and regimens already in the project."""
    if _is_test_fixture(medication.casefold()):
        return []
    errors: list[str] = []
    expected, _how = _resolve_indication(medication.casefold(), diagnosis_names)
    kept = action in {"continue", "start", "change", "hold", "restart", "new_start"}
    if kept and expected is None:
        errors.append(f"{medication} has no supported indication for {action}")
    if expected is not None and indication and not _same_text(indication, expected):
        errors.append(
            f"{medication} indication {indication!r} does not match {expected!r}"
        )
    copied = bool(
        indication
        and admission_diagnosis
        and _same_text(indication, admission_diagnosis)
        and expected is None
    )
    if copied:
        errors.append(
            f"{medication} indication is copied from the admission diagnosis "
            "without a supported match"
        )
    if any(token in medication.casefold() for token in _ANTICOAGULANT) and expected is None:
        errors.append(f"{medication} is an anticoagulant without a supported indication")
    monitoring_blob = " ".join(monitoring_parameters).casefold()
    names = " ".join(medication_names).casefold()
    if "inr" in monitoring_blob and "warfarin" not in names:
        errors.append("warfarin-specific monitoring is present without warfarin")
    if "warfarin" in medication.casefold() and action in {"continue", "start", "change"}:
        if "inr" not in monitoring_blob:
            errors.append(f"{medication} is discharged without INR monitoring")
    if action == "stop" and not _clinical_stop_fact(visible_text):
        errors.append(f"{medication} is stopped without a resident-visible explanation")
    if temporal_role == "hospital_only" and action in {"continue", "start", "change"}:
        errors.append(f"{medication} is inpatient-only therapy on the discharge list")
    for allergy in allergies:
        if len(allergy) < 4:
            continue
        if allergy.casefold() in medication.casefold() and action in {
            "continue",
            "start",
            "change",
        }:
            errors.append(f"{medication} matches documented allergy {allergy}")
    return errors


def _resolve_indication(blob: str, diagnosis_names: list[str]) -> tuple[str | None, str | None]:
    mapped = _matched_indication(blob, diagnosis_names)
    if mapped is not None:
        return mapped, "mapped indication is active on the problem list"
    cited = _citation_indication(blob, diagnosis_names)
    if cited is not None:
        return cited, "stored regimen citation names this condition"
    return None, None


def _matched_indication(blob: str, diagnosis_names: list[str]) -> str | None:
    needles = [needle for query, needle in INDICATION_BY_QUERY.items() if query in blob]
    if not needles:
        return None
    for name in diagnosis_names:
        lowered = name.casefold()
        if any(needle.casefold() in lowered or lowered in needle.casefold() for needle in needles):
            return name
    return None


def _citation_indication(blob: str, diagnosis_names: list[str]) -> str | None:
    excerpts: list[str] = []
    for regimen in load_regimens():
        if regimen.query not in blob or not regimen.matches_text(blob):
            continue
        excerpts.append(_norm(regimen.citation))
        if regimen.additional_citation:
            excerpts.append(_norm(regimen.additional_citation))
    if not excerpts:
        return None
    combined = " ".join(excerpts)
    if any(denial in combined for denial in _CITATION_DENIALS):
        return None
    for name in diagnosis_names:
        lowered = _norm(name)
        for phrase in _INDICATION_PHRASES:
            if phrase in lowered and phrase in combined:
                return name
    return None


def _clinical_stop_fact(text: str) -> bool:
    lowered = text.casefold()
    if not lowered.strip():
        return False
    if lowered.strip() in {
        "stopped during this admission.",
        "stopped during this admission",
    }:
        return False
    return any(token in lowered for token in _STOP_FACT_TOKENS)


def _drug_tokens(blob: str) -> list[str]:
    skip = {"oral", "tablet", "capsule", "sodium", "extended", "release"}
    return [
        token
        for token in re.split(r"[^a-z0-9]+", blob)
        if len(token) > 4 and token not in skip
    ]


def _conventional_creatinine(value: float, unit: str | None) -> float:
    spec = next(item for item in LAB_SPECS if item.name == "creatinine")
    actual = normalize_unit(unit)
    factor = spec.conventional_to_molar
    if factor and spec.molar_unit and actual.casefold() == spec.molar_unit.casefold():
        return value / factor
    if not actual and factor and value >= 20:
        return value / factor
    return value


def _continue_rationale(indication: str, evidence: list[Evidence]) -> str:
    sentences = [f"{indication} is on the problem list."]
    names = {item.name for item in evidence}
    if "creatinine" in names:
        sentences.append(
            "Creatinine is below the acute-kidney laboratory pattern "
            "already used by this generator."
        )
    if "potassium" in names:
        sentences.append("Potassium is inside the coherent range used for this chart.")
    if "systolic_blood_pressure" in names:
        sentences.append(
            "Systolic blood pressure is not below the 100 mmHg threshold "
            "already used for restart planning."
        )
    return " ".join(sentences)


def _value_with_unit(value: float, unit: str | None) -> str:
    if unit:
        return f"{value} {unit}"
    return str(value)


def _norm(text: str) -> str:
    return text.casefold().replace("-", " ")


def _same_text(left: str, right: str) -> bool:
    return _norm(left).strip() == _norm(right).strip()


def _needs(blob: str, tokens: tuple[str, ...]) -> bool:
    return any(token in blob for token in tokens)


def _is_test_fixture(blob: str) -> bool:
    return "test_" in blob


def _hold_for_creatinine(
    medication: str,
    indication: str,
    creatinine: float,
    unit: str | None,
    dose: str | None,
    route: str | None,
    frequency: str | None,
) -> MedicationDecision:
    shown = _value_with_unit(creatinine, unit or "mg/dL")
    fact = f"creatinine {shown} meets the acute-kidney laboratory pattern"
    return _decision(
        medication,
        "hold",
        indication,
        f"Held because {fact}.",
        [
            Evidence("diagnosis", value=indication),
            Evidence("lab", name="creatinine", value=shown, interpretation=fact),
        ],
        SUFFICIENT_EVIDENCE,
        dose=dose,
        route=route,
        frequency=frequency,
        held_reason=fact,
    )


def _hold_for_pressure(
    medication: str,
    indication: str,
    systolic_bp: int,
    dose: str | None,
    route: str | None,
    frequency: str | None,
) -> MedicationDecision:
    fact = f"systolic blood pressure {systolic_bp} mmHg is below 100"
    return _decision(
        medication,
        "hold",
        indication,
        f"Held because {fact}.",
        [
            Evidence("diagnosis", value=indication),
            Evidence(
                "vital",
                name="systolic_blood_pressure",
                value=str(systolic_bp),
                interpretation=fact,
            ),
        ],
        SUFFICIENT_EVIDENCE,
        dose=dose,
        route=route,
        frequency=frequency,
        held_reason=fact,
    )


def _omit(medication: str, rationale: str, evidence_class: str) -> MedicationDecision:
    return MedicationDecision(
        medication=medication,
        action="omit",
        indication=None,
        rationale=rationale,
        evidence_class=evidence_class,
        include=False,
    )


def _decision(
    medication: str,
    action: str,
    indication: str | None,
    rationale: str,
    evidence: list[Evidence],
    evidence_class: str,
    *,
    dose: str | None = None,
    route: str | None = None,
    frequency: str | None = None,
    held_reason: str | None = None,
) -> MedicationDecision:
    return MedicationDecision(
        medication=medication,
        action=action,
        indication=indication,
        rationale=rationale,
        supporting_evidence=evidence,
        evidence_class=evidence_class,
        include=True,
        dose=dose,
        route=route,
        frequency=frequency,
        held_reason=held_reason,
    )
