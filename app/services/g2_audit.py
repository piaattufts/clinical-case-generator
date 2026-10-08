"""Independent audits for Generation 2 candidates.

The checks read the structured episode. They do not add clinical facts.
"""

from __future__ import annotations

import json
from typing import Any

from app.services.g2_terminology import ALLOWED_ACTIONS, ICD10, LOINC, TIME_RANK, UCUM_UNITS

REQUIRED_FACT_DOMAINS = (
    "baseline",
    "acute_change",
    "precipitant",
    "workup",
    "diagnosis",
    "treatment",
    "response",
    "physiology",
    "medication_decision",
    "discharge_readiness",
    "followup",
)

REQUIRED_EVENT_TYPES = (
    "baseline",
    "acute_change",
    "precipitant",
    "presentation",
    "workup",
    "diagnosis",
    "treatment",
    "response",
    "discharge",
)

LEAK_TOKENS = (
    "reference_discharge_plan",
    "investigator_derived_reference",
    "acceptable_alternatives",
    "planted error",
    "error_category",
    "intentional_changes",
    "scoring label",
    "clinically_validated",
    "baseline delirium",
)

ROUND1_COLUMNS = (
    "baseline_visible",
    "acute_change_clear",
    "precipitant_sufficient",
    "diagnostic_workup_sufficient",
    "hospital_course_sufficient",
    "treatment_visible",
    "response_visible",
    "physiology_coherent",
    "medication_decisions_supported",
    "chronology_valid",
    "discharge_readiness_supported",
    "monitoring_followup_sufficient",
)


_HIDDEN_FROM_RESIDENT = {
    "reference_discharge_plan",
    "facts",
    "timeline",
    "medication_decisions",
    "fingerprint",
    "physiology_expectations",
    "visible_fact_ids",
    "source_rxcuis",
    "source_snomed",
    "provenance",
    "scenario_code",
    "scenario_version",
    "variant_id",
    "eligibility_tier",
    "synthea_patient_id",
    "episode_generation_seed",
    "control_error_status",
    "ready_for_clinician_review",
    "clinically_validated",
    "resident",
}


def chart_of(episode: dict[str, Any]) -> dict[str, Any]:
    resident = episode.get("resident")
    if isinstance(resident, dict) and "CaseLab" in resident:
        return resident
    return {
        key: value
        for key, value in episode.items()
        if key not in _HIDDEN_FROM_RESIDENT
    }


def _facts(episode: dict[str, Any]) -> list[dict[str, Any]]:
    rows = episode.get("facts")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _events(episode: dict[str, Any]) -> list[dict[str, Any]]:
    rows = episode.get("timeline")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _decisions(episode: dict[str, Any]) -> list[dict[str, Any]]:
    rows = episode.get("medication_decisions")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def domain_present(episode: dict[str, Any], domain: str) -> bool:
    return any(
        item.get("resident_visible") and domain in (item.get("domains") or [])
        for item in _facts(episode)
    )


def chronology_errors(episode: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    events = sorted(_events(episode), key=lambda item: int(item.get("time_order") or 0))
    orders = [int(item.get("time_order") or 0) for item in events]
    if orders != sorted(orders):
        errors.append("timeline orders are not sorted")
    if any(right - left < 0 for left, right in zip(orders, orders[1:], strict=False)):
        errors.append("negative timeline interval")
    types = {str(item.get("event_type")) for item in events}
    for required in REQUIRED_EVENT_TYPES:
        if required not in types and not (
            required == "precipitant" and "precipitant_evaluation" in types
        ):
            errors.append(f"missing timeline event {required}")

    def first(event_type: str) -> int | None:
        matches = [
            int(item["time_order"]) for item in events if item.get("event_type") == event_type
        ]
        return min(matches) if matches else None

    presentation = first("presentation")
    diagnosis = first("diagnosis")
    workup = first("workup")
    treatment_orders = [
        item for item in events if item.get("event_type") == "treatment"
    ]
    response = first("response")
    discharge = first("discharge")
    if presentation is None or diagnosis is None or presentation >= diagnosis:
        errors.append("presentation does not precede the newly established diagnosis")
    if workup is None or diagnosis is None or workup >= diagnosis:
        errors.append("work-up does not precede the diagnosis")
    for item in treatment_orders:
        order = int(item["time_order"])
        if item.get("empiric"):
            if workup is None or order <= workup:
                errors.append("empiric treatment does not follow the preceding work-up")
        elif diagnosis is None or order <= diagnosis:
            errors.append("targeted treatment precedes the diagnosis")
    if response is None or not treatment_orders or response <= min(
        int(item["time_order"]) for item in treatment_orders
    ):
        errors.append("response does not follow treatment")
    if discharge is None or response is None or discharge <= response:
        errors.append("discharge does not follow stabilization")
    if any(order < 0 for order in orders):
        errors.append("negative time order")
    for med in _decisions(episode):
        held = [
            int(item["time_order"])
            for item in med.get("states") or []
            if isinstance(item, dict) and item.get("state") == "held"
        ]
        restarted = [
            int(item["time_order"])
            for item in med.get("states") or []
            if isinstance(item, dict) and item.get("state") == "restarted"
        ]
        if held and restarted and min(held) >= min(restarted):
            errors.append(f"{med.get('drug')} restarts before it is held")
    chart = chart_of(episode)
    by_test: dict[str, list[int]] = {}
    for lab in chart.get("CaseLab") or []:
        if not isinstance(lab, dict):
            continue
        rank = TIME_RANK.get(str(lab.get("timepoint")))
        if rank is None:
            errors.append(f"unknown lab timepoint {lab.get('timepoint')}")
            continue
        by_test.setdefault(str(lab.get("test_name")), []).append(rank)
    for name, ranks in by_test.items():
        if ranks != sorted(ranks):
            errors.append(f"{name} timepoints are out of order")
    return errors


def physiology_errors(episode: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    chart = chart_of(episode)
    series: dict[tuple[str, str], float] = {}
    for lab in chart.get("CaseLab") or []:
        if not isinstance(lab, dict):
            continue
        unit = lab.get("unit")
        if unit not in UCUM_UNITS and unit not in {None, ""}:
            errors.append(f"unit {unit} is not a permitted UCUM unit")
        loinc = lab.get("loinc_code")
        if loinc not in LOINC:
            errors.append(f"LOINC {loinc} is not in the verified table")
        value = lab.get("value")
        if isinstance(value, int | float):
            if value < 0:
                errors.append(f"negative lab {lab.get('test_name')}")
            series[(str(loinc), str(lab.get("timepoint")))] = float(value)
    for vital in chart.get("CaseVital") or []:
        if not isinstance(vital, dict):
            continue
        systolic = vital.get("bp_systolic")
        diastolic = vital.get("bp_diastolic")
        if isinstance(systolic, int) and isinstance(diastolic, int) and systolic <= diastolic:
            errors.append("blood pressure systolic is not above diastolic")
        for key, low, high in (
            ("heart_rate", 30, 180),
            ("resp_rate", 8, 50),
            ("temp_c", 35, 41),
            ("spo2_percent", 70, 100),
        ):
            raw = vital.get(key)
            if isinstance(raw, int | float) and not low <= float(raw) <= high:
                errors.append(f"{key} {raw} is outside a survivable range")
    expectations = episode.get("physiology_expectations") or []
    creat = {when: value for (code, when), value in series.items() if code == "2160-0"}
    potassium = {when: value for (code, when), value in series.items() if code == "2823-3"}
    hemoglobin = {when: value for (code, when), value in series.items() if code == "718-7"}
    inr = {when: value for (code, when), value in series.items() if code == "6301-6"}
    if "aki_recovered" in expectations:
        base = creat.get("baseline", creat.get("admission"))
        peak = creat.get("peak", creat.get("admission"))
        end = creat.get("discharge")
        if base is None or peak is None or end is None or not (peak >= base and end <= peak):
            errors.append("AKI creatinine trajectory is not peak-then-recovery")
    if "bleed_hemoglobin" in expectations:
        start = hemoglobin.get("admission", hemoglobin.get("baseline"))
        nadir = hemoglobin.get("nadir", hemoglobin.get("intermediate"))
        end = hemoglobin.get("discharge")
        if start is None or nadir is None or end is None or not (nadir <= start and end >= nadir):
            errors.append("hemoglobin does not fall and then stabilize")
    if "inr_down" in expectations:
        if inr.get("discharge", 99) > inr.get("admission", 0):
            errors.append("INR rose after the anticoagulant was held")
    weights = {}
    for row in chart.get("CaseWeight") or []:
        if isinstance(row, dict) and isinstance(row.get("weight_kg"), int | float):
            weights[str(row.get("timepoint"))] = float(row["weight_kg"])
    if "diuresis_weight_down" in expectations:
        if weights.get("discharge", 0) >= weights.get("admission", 0):
            errors.append("weight did not fall after diuresis")
    for value in potassium.values():
        if not 2.5 <= value <= 6.0:
            errors.append(f"potassium {value} is not coherent")
    return errors


def medication_errors(episode: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    visible = set(episode.get("visible_fact_ids") or [])
    if not visible:
        visible = {
            str(item["fact_id"])
            for item in _facts(episode)
            if item.get("resident_visible") and item.get("fact_id")
        }
    for med in _decisions(episode):
        action = str(med.get("discharge_action") or "")
        drug = str(med.get("drug") or "")
        if action not in ALLOWED_ACTIONS:
            errors.append(f"{drug} has no allowed discharge action")
        evidence = [str(item) for item in med.get("evidence_ids") or []]
        if not evidence or any(item not in visible for item in evidence):
            errors.append(f"{drug} {action} is not tied to resident-visible evidence")
        if not str(med.get("rationale") or "").strip():
            errors.append(f"{drug} has no rationale")
        states = [item for item in med.get("states") or [] if isinstance(item, dict)]
        state_names = [str(item.get("state")) for item in states]
        if "held" in state_names and action == "continue" and "restarted" not in state_names:
            errors.append(f"{drug} was held and has no restart or other final disposition")
        if med.get("hospital_only") and action != "stop":
            errors.append(f"hospital-only {drug} is not stopped")
        if action in {"stop", "restart", "hold", "dose_change", "new_start"}:
            triggers = [str(item.get("trigger") or "") for item in states]
            if not any(triggers):
                errors.append(f"{drug} changes without a trigger")
        for alternative in med.get("acceptable_alternatives") or []:
            if not isinstance(alternative, dict):
                errors.append(f"{drug} alternative is malformed")
                continue
            if alternative.get("alternative_action") not in ALLOWED_ACTIONS:
                errors.append(f"{drug} alternative action is missing")
            if not alternative.get("conditions") or not alternative.get("rationale"):
                errors.append(f"{drug} alternative has no condition or rationale")
    return errors


def provenance_errors(episode: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed = {
        "synthea_longitudinal",
        "cliniproof_episode_generated",
        "reference_terminology",
        "investigator_derived_reference",
    }
    source_rx = set(episode.get("source_rxcuis") or [])
    source_snomed = set(episode.get("source_snomed") or [])
    for fact in _facts(episode):
        provenance = str(fact.get("provenance") or "")
        if provenance not in allowed:
            errors.append(f"fact {fact.get('fact_id')} has no provenance class")
        text = str(fact.get("text") or "").casefold()
        if provenance == "synthea_longitudinal" and (
            "hospital day" in text or "this admission" in text or "during the hospitalization" in text
        ):
            errors.append(f"Synthea fact {fact.get('fact_id')} describes the inpatient episode")
        if provenance == "cliniproof_episode_generated" and "synthea recorded this inpatient" in text:
            errors.append("episode fact is mislabeled as Synthea")
    chart = chart_of(episode)
    for lab in chart.get("CaseLab") or []:
        if isinstance(lab, dict) and lab.get("provenance") not in allowed:
            errors.append("lab missing provenance")
    for diagnosis in chart.get("CaseDiagnosis") or []:
        if not isinstance(diagnosis, dict):
            continue
        code = diagnosis.get("icd10cm")
        if code is not None and code not in ICD10:
            errors.append(f"invented ICD-10-CM {code}")
        snomed = diagnosis.get("snomed_code")
        if snomed is not None and snomed not in source_snomed:
            errors.append(f"SNOMED {snomed} was not copied from the Synthea patient")
        if diagnosis.get("provenance") not in allowed:
            errors.append("diagnosis missing provenance")
    for med in _decisions(episode):
        rxcui = med.get("rxcui")
        if rxcui is not None and rxcui not in source_rx:
            errors.append(f"RxCUI {rxcui} was not copied from Synthea")
        if med.get("identity_provenance") not in allowed:
            errors.append(f"{med.get('drug')} identity has no provenance")
    for action in (episode.get("reference_discharge_plan") or {}).get("actions") or []:
        if isinstance(action, dict) and action.get("provenance") != "investigator_derived_reference":
            errors.append("reference action is not investigator-derived")
    return errors


def leak_errors(episode: dict[str, Any]) -> list[str]:
    resident = chart_of(episode)
    text = json.dumps(resident).casefold()
    return [token for token in LEAK_TOKENS if token.casefold() in text]


def monitoring_ok(episode: dict[str, Any]) -> bool:
    chart = chart_of(episode)
    return bool(chart.get("CaseMonitoring")) and bool(chart.get("CaseFollowup"))


def round1_row(episode: dict[str, Any], case_id: str) -> dict[str, Any]:
    chrono = chronology_errors(episode)
    phys = physiology_errors(episode)
    meds = medication_errors(episode)
    leaks = leak_errors(episode)
    provenance = provenance_errors(episode)
    course = ""
    for note in chart_of(episode).get("CaseNote") or []:
        if isinstance(note, dict) and note.get("note_type") == "hospital_course":
            course = str(note.get("note_text") or "")
    flags = {
        "baseline_visible": domain_present(episode, "baseline"),
        "acute_change_clear": domain_present(episode, "acute_change"),
        "precipitant_sufficient": domain_present(episode, "precipitant"),
        "diagnostic_workup_sufficient": domain_present(episode, "workup")
        and domain_present(episode, "diagnosis"),
        "hospital_course_sufficient": len(course) > 400
        and domain_present(episode, "treatment")
        and domain_present(episode, "response"),
        "treatment_visible": domain_present(episode, "treatment"),
        "response_visible": domain_present(episode, "response"),
        "physiology_coherent": not phys and domain_present(episode, "physiology"),
        "medication_decisions_supported": not meds and domain_present(episode, "medication_decision"),
        "chronology_valid": not chrono,
        "discharge_readiness_supported": domain_present(episode, "discharge_readiness"),
        "monitoring_followup_sufficient": monitoring_ok(episode) and domain_present(episode, "followup"),
    }
    notes = chrono + phys + meds + leaks + provenance
    overall = all(flags.values()) and not leaks and not provenance
    return {
        "case_id": case_id,
        "scenario": episode.get("scenario_code"),
        "variant_id": episode.get("variant_id"),
        **flags,
        "answer_leak": not leaks,
        "provenance": not provenance,
        "overall_pass": overall,
        "notes": "; ".join(notes),
    }


def audit_passes(episode: dict[str, Any]) -> bool:
    row = round1_row(episode, str(episode.get("case_id") or ""))
    return bool(row["overall_pass"])
