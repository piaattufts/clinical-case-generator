"""Match each revised Generation 1 case to an independent Generation 2 episode.

The match is on reasoning family and decision complexity. Generation 2 cases
are built from Synthea patients and the episode engine. Generation 1 charts
are not copied, and the Generation 1 reference plan is not a template.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from app.services.discharge_episode import build_episode, variant_supported, variants_for
from app.services.g2_audit import round1_row
from app.services.g2_cohort import _retag
from app.services.synthea_eligibility import evaluate_patient
from app.sources.synthea import LongitudinalPatient

ROOT = Path(__file__).resolve().parents[2]
REVISED = ROOT / "data" / "case_sets" / "seed_guided" / "REVISED"
MIN_ATTEMPTS = 4

PAIRS: tuple[tuple[str, str], ...] = tuple(
    (f"VAL-{index}", f"G2-{index - 800:03d}") for index in range(801, 825)
)

FAMILY_BY_VAL = {
    **{f"VAL-{index}": "MED_HISTORY_UNCERTAINTY" for index in range(801, 805)},
    **{f"VAL-{index}": "HF_DECOMPENSATION" for index in range(805, 809)},
    **{f"VAL-{index}": "ENDOCARDITIS_OPAT" for index in range(809, 813)},
    **{f"VAL-{index}": "TRANSPLANT_CMV" for index in range(813, 817)},
    **{f"VAL-{index}": "HIP_FRACTURE_ANTICOAGULATION" for index in range(817, 821)},
    **{f"VAL-{index}": "GI_BLEED_ANTICOAGULATION" for index in range(821, 825)},
}

FAMILY_LABEL = {
    "MED_HISTORY_UNCERTAINTY": "Medication history uncertainty",
    "HF_DECOMPENSATION": "Acute heart-failure decompensation",
    "ENDOCARDITIS_OPAT": "Outpatient parenteral antibiotic therapy after endocarditis",
    "TRANSPLANT_CMV": "Post-kidney-transplant infectious complication",
    "HIP_FRACTURE_ANTICOAGULATION": "Postoperative anticoagulation after hip fracture",
    "GI_BLEED_ANTICOAGULATION": "Gastrointestinal bleed with anticoagulation decisions",
}

REASONING_TARGET = {
    "MED_HISTORY_UNCERTAINTY": (
        "Interpret an acute change and decide which outpatient medicines continue, stop, or restart"
    ),
    "HF_DECOMPENSATION": (
        "Discharge heart-failure therapy after decompensation, diuresis, and renal review"
    ),
    "ENDOCARDITIS_OPAT": (
        "Choose outpatient parenteral antibiotic therapy after endocarditis is established in hospital"
    ),
    "TRANSPLANT_CMV": (
        "Start or adjust cytomegalovirus therapy and immunosuppression after a diagnostic work-up"
    ),
    "HIP_FRACTURE_ANTICOAGULATION": (
        "Time anticoagulation around hip-fracture repair and decide the postoperative restart"
    ),
    "GI_BLEED_ANTICOAGULATION": (
        "Hold antithrombotic therapy for bleeding and decide restart, stop, or acid suppression"
    ),
}

PREFERRED_VARIANTS: dict[str, tuple[str, ...]] = {
    "VAL-801": ("delirium_uti", "delirium_dehydration", "nsaid_dyspepsia", "lisinopril_hold_aki"),
    "VAL-802": ("delirium_uti", "delirium_pneumonia", "pharmacy_confirmation", "delirium_dehydration"),
    "VAL-803": ("delirium_dehydration", "hyponatremia_hctz", "orthostasis_hctz", "lisinopril_hold_aki"),
    "VAL-804": ("hyponatremia_hctz", "pharmacy_confirmation", "orthostasis_hctz", "delirium_pneumonia"),
    "VAL-805": (
        "nonadherence_cost",
        "dietary_sodium_missed_diuretic",
        "no_clear_precipitant",
        "ischemia_evaluated_negative",
    ),
    "VAL-806": (
        "dietary_sodium_missed_diuretic",
        "recent_nsaid",
        "pulmonary_infection",
        "hypertensive_surge",
    ),
    "VAL-807": (
        "no_clear_precipitant",
        "ischemia_evaluated_negative",
        "nonadherence_cost",
        "new_atrial_fibrillation",
    ),
    "VAL-808": (
        "hypertensive_surge",
        "pulmonary_infection",
        "new_atrial_fibrillation",
        "recent_nsaid",
    ),
    "VAL-809": ("dental_mitral", "opat_home_infusion", "skin_source", "bicuspid_predisposition"),
    "VAL-810": (
        "no_source_aortic",
        "surgery_consult_no_indication",
        "dental_mitral",
        "skin_source",
    ),
    "VAL-811": (
        "gi_source_evaluated",
        "opat_skilled_nursing",
        "bicuspid_predisposition",
        "no_source_aortic",
    ),
    "VAL-812": (
        "opat_skilled_nursing",
        "surgery_consult_no_indication",
        "gi_source_evaluated",
        "opat_home_infusion",
    ),
    "VAL-813": ("colitis_biopsy", "cdiff_excluded", "volume_loss", "transplant_clinic_followup"),
    "VAL-814": ("volume_loss", "cdiff_excluded", "colitis_biopsy", "leukopenia_recovered"),
    "VAL-815": ("prophylaxis_breakthrough", "leukopenia_recovered", "pcr_syndrome", "id_clinic_followup"),
    "VAL-816": ("transplant_clinic_followup", "pcr_syndrome", "id_clinic_followup", "colitis_biopsy"),
    "VAL-817": ("snf_after_orif", "inr_delay_home", "af_early_hemostasis", "delayed_mobilization_snf"),
    "VAL-818": ("inr_delay_home", "af_early_hemostasis", "snf_after_orif", "delayed_mobilization_snf"),
    "VAL-819": ("af_early_hemostasis", "delayed_mobilization_snf", "inr_delay_home", "snf_after_orif"),
    "VAL-820": (
        "delayed_mobilization_snf",
        "snf_after_orif",
        "supratherapeutic_inr",
        "inr_delay_home",
    ),
    "VAL-821": ("duodenal_ulcer_restart", "stable_no_transfusion", "gastric_ulcer_inr", "esophagitis"),
    "VAL-822": ("esophagitis", "stable_no_transfusion", "duodenal_ulcer_restart", "gastric_ulcer_inr"),
    "VAL-823": ("diverticular_hold", "defer_restart", "duodenal_ulcer_restart", "nsaid_and_warfarin"),
    "VAL-824": ("nsaid_and_warfarin", "defer_restart", "diverticular_hold", "esophagitis"),
}

DUAL_REVIEW = {"VAL-801", "VAL-805", "VAL-809", "VAL-813"}
REVIEWER1_SPECIFIC = {"VAL-802", "VAL-803"}
MONITOR_BAND = {"limited": 0, "routine": 1, "intensive": 2}
DIFFICULTY_BAND = {"low": 0, "moderate": 1, "high": 2}


def revised_resident_path(case_id: str) -> Path:
    for folder in ("overlap_4", "remaining_20"):
        path = REVISED / folder / f"{case_id}_resident.json"
        if path.is_file():
            return path
    raise FileNotFoundError(case_id)


def revised_evaluator_path(case_id: str) -> Path:
    return revised_resident_path(case_id).with_name(f"{case_id}_evaluator.json")


def _stem(drug: str) -> str:
    return (drug or "").casefold().split()[0]


def _monitoring_label(parameters: list[str], follow_items: list[str]) -> str:
    blob = " ".join(parameters + follow_items).casefold()
    if any(token in blob for token in ("weekly", "inr", "trough", "parenteral", "cytomegalovirus")):
        return "intensive"
    if parameters or any(token in blob for token in ("creatinine", "electrolyte", "chemistry", "weight", "hemoglobin")):
        return "routine"
    return "limited"


def _difficulty(decision_count: int, monitoring: str) -> str:
    points = decision_count + MONITOR_BAND[monitoring]
    if points <= 2:
        return "low"
    if points <= 5:
        return "moderate"
    return "high"


def _g1_decisions(resident: dict[str, Any]) -> list[str]:
    home = {
        _stem(str(row.get("drug") or ""))
        for row in resident.get("CaseMedication") or []
        if isinstance(row, dict) and row.get("context") == "home"
    }
    decisions: list[str] = []
    for row in resident.get("CaseMedication") or []:
        if not isinstance(row, dict) or row.get("context") != "inpatient":
            continue
        status = str(row.get("status") or "")
        notes = f"{row.get('notes') or ''} {row.get('held_reason') or ''}".casefold()
        drug = _stem(str(row.get("drug") or ""))
        if status == "discontinued":
            decisions.append("stop")
        elif status == "held":
            decisions.append("restart" if "restarted" in notes else "hold")
        elif drug not in home:
            decisions.append("new_start")
    return decisions


def profile_resident(case_id: str) -> dict[str, Any]:
    resident = json.loads(revised_resident_path(case_id).read_text(encoding="utf-8"))
    family = FAMILY_BY_VAL[case_id]
    home = [
        row
        for row in resident.get("CaseMedication") or []
        if isinstance(row, dict) and row.get("context") == "home"
    ]
    inpatient = [
        row
        for row in resident.get("CaseMedication") or []
        if isinstance(row, dict) and row.get("context") == "inpatient"
    ]
    decisions = _g1_decisions(resident)
    follow = [str(row.get("item") or "") for row in resident.get("CaseFollowup") or [] if isinstance(row, dict)]
    monitors = [
        str(row.get("parameter") or "")
        for row in resident.get("CaseMonitoring") or []
        if isinstance(row, dict)
    ]
    monitoring = _monitoring_label(monitors, follow)
    diagnoses = [
        str(row.get("diagnosis") or "")
        for row in resident.get("CaseDiagnosis") or []
        if isinstance(row, dict) and row.get("diagnosis_type") in {"admission", "hospital"}
    ]
    disposition = str((resident.get("ClinicalCase") or {}).get("disposition_status") or "")
    return {
        "generation1_case_id": case_id,
        "scenario_family": family,
        "family_label": FAMILY_LABEL[family],
        "primary_reasoning_target": REASONING_TARGET[family],
        "secondary_reasoning_targets": sorted(set(decisions)),
        "number_of_home_medications": len(home),
        "number_of_clinically_relevant_medications": len({_stem(str(row.get("drug") or "")) for row in inpatient}),
        "number_of_major_discharge_decisions": len(decisions),
        "decision_types": decisions,
        "important_monitoring_requirements": monitors or follow[:2],
        "important_followup_requirements": follow,
        "major_diagnostic_workup": diagnoses[:4],
        "approximate_difficulty": _difficulty(len(decisions), monitoring),
        "monitoring_complexity": monitoring,
        "followup_count": len(follow),
        "major_causal_dependencies": [
            "baseline before the acute change",
            "a precipitant or an evaluation for one",
            "work-up before a newly established diagnosis",
            "treatment before the recorded response",
        ],
        "disposition": disposition,
        "clinician_input_into_generation2_case": "none",
    }


def _g2_actions(episode: dict[str, Any]) -> list[dict[str, Any]]:
    plan = episode.get("reference_discharge_plan") or {}
    return [row for row in plan.get("actions") or [] if isinstance(row, dict)]


def profile_episode(episode: dict[str, Any]) -> dict[str, Any]:
    resident = episode["resident"]
    actions = _g2_actions(episode)
    consequential = [str(row.get("action")) for row in actions if row.get("action") != "continue"]
    follow = [str(row.get("item") or "") for row in resident.get("CaseFollowup") or [] if isinstance(row, dict)]
    monitors = [
        str(row.get("parameter") or "")
        for row in resident.get("CaseMonitoring") or []
        if isinstance(row, dict)
    ]
    monitoring = _monitoring_label(monitors, follow)
    return {
        "scenario_family": episode.get("scenario_code"),
        "decision_types": consequential,
        "decision_count": len(consequential),
        "monitoring_complexity": monitoring,
        "followup_count": len(follow),
        "approximate_difficulty": _difficulty(len(consequential), monitoring),
        "disposition": str((resident.get("ClinicalCase") or {}).get("disposition_status") or ""),
        "home_medications": sum(
            1
            for row in resident.get("CaseMedication") or []
            if isinstance(row, dict) and row.get("context") == "home"
        ),
    }


def _band_distance(left: str, right: str, scale: dict[str, int]) -> int:
    return abs(scale[left] - scale[right])


def _disposition_compatible(g1: str, g2: str) -> bool:
    g1_facility = g1.casefold() in {"rehab", "snf", "skilled nursing facility"}
    g2_facility = "skill" in g2.casefold() or g2.casefold() in {"rehab", "snf"}
    return g1_facility == g2_facility


def match_score(
    g1_profile: dict[str, Any],
    episode: dict[str, Any],
    *,
    variant_id: str,
    used_variants: set[str],
) -> int:
    g2_profile = profile_episode(episode)
    if g2_profile["scenario_family"] != g1_profile["scenario_family"]:
        return -1000
    decision_gap = abs(int(g1_profile["number_of_major_discharge_decisions"]) - int(g2_profile["decision_count"]))
    monitor_gap = _band_distance(
        str(g1_profile["monitoring_complexity"]),
        str(g2_profile["monitoring_complexity"]),
        MONITOR_BAND,
    )
    difficulty_gap = _band_distance(
        str(g1_profile["approximate_difficulty"]),
        str(g2_profile["approximate_difficulty"]),
        DIFFICULTY_BAND,
    )
    preferred = PREFERRED_VARIANTS[str(g1_profile["generation1_case_id"])]
    preference = 2 if variant_id == preferred[0] else 1 if variant_id in preferred else 0
    score = 80 - (12 * decision_gap) - (8 * monitor_gap) - (6 * difficulty_gap) + preference
    if _disposition_compatible(str(g1_profile["disposition"]), str(g2_profile["disposition"])):
        score += 4
    if variant_id in used_variants:
        score -= 10
    return score


def _passes_core(g1_profile: dict[str, Any], episode: dict[str, Any], audit: dict[str, Any]) -> bool:
    g2_profile = profile_episode(episode)
    if g2_profile["scenario_family"] != g1_profile["scenario_family"]:
        return False
    if abs(int(g1_profile["number_of_major_discharge_decisions"]) - int(g2_profile["decision_count"])) > 2:
        return False
    if _band_distance(
        str(g1_profile["monitoring_complexity"]),
        str(g2_profile["monitoring_complexity"]),
        MONITOR_BAND,
    ) > 1:
        return False
    if _band_distance(
        str(g1_profile["approximate_difficulty"]),
        str(g2_profile["approximate_difficulty"]),
        DIFFICULTY_BAND,
    ) > 1:
        return False
    return bool(audit["overall_pass"])


def _variant_order(case_id: str, scenario: str) -> list[dict[str, Any]]:
    catalog = {str(item["variant_id"]): item for item in variants_for(scenario)}
    ordered: list[dict[str, Any]] = []
    for variant_id in PREFERRED_VARIANTS[case_id]:
        item = catalog.get(variant_id)
        if item is not None:
            ordered.append(item)
    for item in variants_for(scenario):
        if item not in ordered:
            ordered.append(item)
    return ordered


def _reference_signature(payload: dict[str, Any]) -> tuple[tuple[str, str, str], ...]:
    actions = payload.get("reference_discharge_plan")
    rows: list[dict[str, Any]]
    if isinstance(actions, dict):
        rows = [row for row in actions.get("actions") or [] if isinstance(row, dict)]
    elif isinstance(actions, list):
        rows = [row for row in actions if isinstance(row, dict)]
    else:
        rows = []
    return tuple(
        sorted(
            (
                str(row.get("action") or row.get("discharge_action") or ""),
                _stem(str(row.get("medication") or row.get("drug") or "")),
                str(row.get("dose") or ""),
            )
            for row in rows
        )
    )


def _copied_reference(case_id: str, episode: dict[str, Any]) -> bool:
    evaluator = json.loads(revised_evaluator_path(case_id).read_text(encoding="utf-8"))
    g1_sig = _reference_signature(evaluator)
    g2_sig = _reference_signature(episode)
    return bool(g1_sig) and g1_sig == g2_sig


def _copied_facts(case_id: str, episode: dict[str, Any]) -> bool:
    g1 = json.loads(revised_resident_path(case_id).read_text(encoding="utf-8"))
    g2 = episode["resident"]
    g1_line = str((g1.get("ClinicalCase") or {}).get("one_liner") or "")
    g2_line = str((g2.get("ClinicalCase") or {}).get("one_liner") or "")
    if g1_line and g1_line == g2_line:
        return True
    g1_labs = {
        (str(row.get("test_name")), str(row.get("value")))
        for row in g1.get("CaseLab") or []
        if isinstance(row, dict) and row.get("value") is not None
    }
    g2_labs = {
        (str(row.get("test_name")), str(row.get("value")))
        for row in g2.get("CaseLab") or []
        if isinstance(row, dict) and row.get("value") is not None
    }
    return len(g1_labs & g2_labs) >= 4


def build_matched_cohort(
    patients: list[LongitudinalPatient],
    meta: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[str, list[LongitudinalPatient]] = {code: [] for code in FAMILY_LABEL}
    for patient in patients:
        decisions = evaluate_patient(patient)
        for code, decision in decisions.items():
            if decision.eligible:
                grouped[code].append(patient)
    for rows in grouped.values():
        rows.sort(key=lambda item: item.synthea_patient_id)
    used_patients: set[str] = set()
    used_variants: dict[str, set[str]] = {code: set() for code in FAMILY_LABEL}
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    attempts_out: list[dict[str, Any]] = []
    for case_id, g2_id in PAIRS:
        g1_profile = profile_resident(case_id)
        scenario = str(g1_profile["scenario_family"])
        pool = [item for item in grouped[scenario] if item.synthea_patient_id not in used_patients]
        if len(pool) < MIN_ATTEMPTS:
            pool = list(grouped[scenario])
        passing: list[tuple[int, str, LongitudinalPatient, dict[str, Any]]] = []
        attempt_count = 0
        tried: set[tuple[str, str]] = set()
        variant_cycle = _variant_order(case_id, scenario)
        cursor = 0
        while attempt_count < MIN_ATTEMPTS and cursor < len(variant_cycle) * max(len(pool), 1):
            variant = variant_cycle[cursor % len(variant_cycle)]
            cursor += 1
            candidate_patient = next(
                (
                    item
                    for item in pool
                    if (item.synthea_patient_id, str(variant["variant_id"])) not in tried
                    and variant_supported(item, scenario, variant)
                ),
                None,
            )
            if candidate_patient is None:
                continue
            tried.add((candidate_patient.synthea_patient_id, str(variant["variant_id"])))
            episode = build_episode(candidate_patient, scenario, variant, meta)
            audit = round1_row(episode, "")
            attempt_count += 1
            score = match_score(
                g1_profile,
                episode,
                variant_id=str(variant["variant_id"]),
                used_variants=used_variants[scenario],
            )
            record = {
                "generation1_case_id": case_id,
                "scenario": scenario,
                "variant_id": variant["variant_id"],
                "synthea_patient_id": candidate_patient.synthea_patient_id,
                "eligibility_tier": episode["eligibility_tier"],
                "score": score,
                "audit_pass": bool(audit["overall_pass"]),
            }
            if not audit["overall_pass"] or _copied_reference(case_id, episode) or _copied_facts(case_id, episode):
                rejected.append({**record, "reason": audit["notes"] or "copied_or_failed", "episode": None})
                attempts_out.append({**record, "status": "rejected"})
                continue
            if not _passes_core(g1_profile, episode, audit):
                rejected.append({**record, "reason": "match_tolerance", "episode": None})
                attempts_out.append({**record, "status": "rejected_match"})
                continue
            passing.append((score, str(variant["variant_id"]), candidate_patient, episode))
            attempts_out.append({**record, "status": "candidate"})
        if not passing:
            raise RuntimeError(f"{case_id} has no passing Generation 2 candidate")
        passing.sort(key=lambda item: (-item[0], item[1], item[2].synthea_patient_id))
        _score, variant_id, patient, episode = passing[0]
        _finalize(episode, g2_id, case_id)
        used_patients.add(patient.synthea_patient_id)
        used_variants[scenario].add(variant_id)
        selected.append(
            {
                "case_id": g2_id,
                "generation1_case_id": case_id,
                "scenario": scenario,
                "variant_id": variant_id,
                "synthea_patient_id": patient.synthea_patient_id,
                "eligibility_tier": episode["eligibility_tier"],
                "episode": episode,
                "match_score": _score,
                "attempt_count": attempt_count,
            }
        )
        for row in attempts_out:
            if row["generation1_case_id"] == case_id and row["status"] == "candidate":
                row["selected"] = row["variant_id"] == variant_id and row["synthea_patient_id"] == patient.synthea_patient_id
    return selected, rejected, attempts_out


def _finalize(episode: dict[str, Any], case_id: str, generation1_case_id: str) -> None:
    resident = episode["resident"]
    resident["case_id_code"] = case_id
    clinical = resident["ClinicalCase"]
    clinical["case_id_code"] = case_id
    clinical["title"] = str(clinical.get("one_liner") or "Inpatient discharge-reasoning case")
    clinical["patient_name"] = "Synthetic patient"
    _retag(resident, case_id)
    episode["case_id"] = case_id
    neutral = f"M-{generation1_case_id.removeprefix('VAL-')}"
    provenance = episode.setdefault("provenance", {})
    provenance["matched_generation1_case_id"] = generation1_case_id
    provenance["neutral_study_id"] = neutral
    provenance["blinding"] = {
        "generation_method_hidden_from_narrative": True,
        "neutral_study_id": neutral,
    }
    _scrub_narrative(resident)


def _scrub_narrative(resident: dict[str, Any]) -> None:
    banned = ("synthea", "generation 1", "generation 2")

    def clean(value: object) -> object:
        if isinstance(value, str):
            text = value
            for token in banned:
                lowered = text.casefold()
                while token in lowered:
                    start = lowered.index(token)
                    text = text[:start] + text[start + len(token) :]
                    lowered = text.casefold()
            return " ".join(text.split())
        if isinstance(value, list):
            return [clean(item) for item in value]
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items()}
        return value

    for key in ("CaseNote", "CaseInstruction", "CaseMedication"):
        resident[key] = clean(resident.get(key))
    clinical = resident.get("ClinicalCase")
    if isinstance(clinical, dict) and isinstance(clinical.get("presentation"), dict):
        clinical["presentation"] = clean(clinical["presentation"])
        clinical["one_liner"] = clean(clinical.get("one_liner"))


def write_matching_artifacts(
    root: Path,
    selected: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
) -> None:
    profile_dir = root / "matching_profiles"
    profile_dir.mkdir(parents=True, exist_ok=True)
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    pair_rows: list[dict[str, str]] = []
    audit_rows: list[dict[str, str]] = []
    blinding: dict[str, str] = {}
    for item in selected:
        case_id = str(item["generation1_case_id"])
        g1_profile = profile_resident(case_id)
        episode = item["episode"]
        g2_profile = profile_episode(episode)
        audit = round1_row(episode, str(item["case_id"]))
        (profile_dir / f"{case_id}.json").write_text(
            json.dumps(g1_profile, indent=2) + "\n",
            encoding="utf-8",
        )
        notes = (
            "Independent hospitalization matched on reasoning family and decision complexity. "
            "Patient-specific facts and the reference plan were generated for this episode."
        )
        if case_id in DUAL_REVIEW:
            notes += " Round 1 sufficiency rules are generator gates for this pair."
        elif case_id in REVIEWER1_SPECIFIC:
            notes += " Reviewer 1 comments informed only the Generation 1 revision, not this episode."
        else:
            notes += " No case-specific clinician input was applied to this episode."
        pair_rows.append(
            {
                "generation1_case_id": case_id,
                "generation2_case_id": str(item["case_id"]),
                "scenario_family": str(g1_profile["scenario_family"]),
                "reasoning_target": str(g1_profile["primary_reasoning_target"]),
                "important_medication_decisions_g1": ", ".join(g1_profile["decision_types"]) or "continue",
                "important_medication_decisions_g2": ", ".join(g2_profile["decision_types"]) or "continue",
                "approximate_difficulty_g1": str(g1_profile["approximate_difficulty"]),
                "target_difficulty_g2": str(g2_profile["approximate_difficulty"]),
                "monitoring_complexity_g1": str(g1_profile["monitoring_complexity"]),
                "monitoring_complexity_g2": str(g2_profile["monitoring_complexity"]),
                "matching_notes": notes,
            }
        )
        same_family = g1_profile["scenario_family"] == g2_profile["scenario_family"]
        decision_gap = abs(int(g1_profile["number_of_major_discharge_decisions"]) - int(g2_profile["decision_count"]))
        monitor_gap = _band_distance(
            str(g1_profile["monitoring_complexity"]),
            str(g2_profile["monitoring_complexity"]),
            MONITOR_BAND,
        )
        difficulty_gap = _band_distance(
            str(g1_profile["approximate_difficulty"]),
            str(g2_profile["approximate_difficulty"]),
            DIFFICULTY_BAND,
        )
        copied_facts = _copied_facts(case_id, episode)
        copied_reference = _copied_reference(case_id, episode)
        core = (
            same_family
            and decision_gap <= 2
            and monitor_gap <= 1
            and difficulty_gap <= 1
            and not copied_facts
            and not copied_reference
            and bool(audit["overall_pass"])
        )
        audit_rows.append(
            {
                "generation1_case_id": case_id,
                "generation2_case_id": str(item["case_id"]),
                "same_scenario_family": "YES" if same_family else "NO",
                "same_broad_reasoning_target": "YES" if same_family else "NO",
                "similar_medication_decision_complexity": "YES" if decision_gap <= 2 else "NO",
                "similar_monitoring_complexity": "YES" if monitor_gap <= 1 else "NO",
                "similar_approximate_difficulty": "YES" if difficulty_gap <= 1 else "NO",
                "g2_independently_generated": "YES",
                "patient_specific_facts_copied_from_g1": "YES" if copied_facts else "NO",
                "hidden_reference_copied_from_g1": "YES" if copied_reference else "NO",
                "round1_failure_mode_prevented": "YES" if audit["overall_pass"] else "NO",
                "clinically_sufficient": "YES" if audit["overall_pass"] else "NO",
                "core_pass": "YES" if core else "NO",
                "attempts": str(item.get("attempt_count") or ""),
            }
        )
        neutral = f"M-{case_id.removeprefix('VAL-')}"
        blinding[case_id] = neutral
        blinding[str(item["case_id"])] = neutral
    _write_csv(
        root / "matched_pairs.csv",
        [
            "generation1_case_id",
            "generation2_case_id",
            "scenario_family",
            "reasoning_target",
            "important_medication_decisions_g1",
            "important_medication_decisions_g2",
            "approximate_difficulty_g1",
            "target_difficulty_g2",
            "monitoring_complexity_g1",
            "monitoring_complexity_g2",
            "matching_notes",
        ],
        pair_rows,
    )
    _write_csv(
        reports / "matched_pair_audit.csv",
        list(audit_rows[0].keys()) if audit_rows else ["generation1_case_id"],
        audit_rows,
    )
    (reports / "matched_pair_audit.md").write_text(_audit_md(audit_rows), encoding="utf-8")
    (root / "blinding_map.json").write_text(
        json.dumps(
            {
                "purpose": "Neutral pair identifiers for a later blinded clinician comparison. This file is not a case narrative.",
                "study_conducted": False,
                "neutral_study_id_by_case": blinding,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (reports / "matching_attempts.csv").write_text(_attempts_csv(attempts), encoding="utf-8")
    if any(row["core_pass"] != "YES" for row in audit_rows):
        failed = [row["generation1_case_id"] for row in audit_rows if row["core_pass"] != "YES"]
        raise RuntimeError("matched pair audit failed for " + ", ".join(failed))


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _attempts_csv(attempts: list[dict[str, Any]]) -> str:
    fields = [
        "generation1_case_id",
        "scenario",
        "variant_id",
        "synthea_patient_id",
        "score",
        "audit_pass",
        "status",
        "selected",
    ]
    lines = [",".join(fields)]
    for row in attempts:
        lines.append(
            ",".join(str(row.get(field, "")) for field in fields)
        )
    return "\n".join(lines) + "\n"


def _audit_md(rows: list[dict[str, str]]) -> str:
    passed = sum(1 for row in rows if row["core_pass"] == "YES")
    lines = [
        "# Matched pair audit",
        "",
        "Each Generation 2 case was chosen from multiple episode attempts after a Generation 1 matching profile was fixed.",
        "The match is the reasoning family and approximate decision complexity.",
        "The hospitalization and the reference plan are independent.",
        "",
        f"Pairs: {len(rows)}. Core pass: {passed}/{len(rows)}.",
        "",
        "A later comparison can ask whether the Synthea-grounded method produces clinically stronger cases than the revised archetype method when pairs are judged with the same instrument. This audit does not answer that question.",
        "",
    ]
    for row in rows:
        lines.append(
            f"- {row['generation1_case_id']} / {row['generation2_case_id']}: "
            f"family {row['same_scenario_family']}, "
            f"decisions {row['similar_medication_decision_complexity']}, "
            f"monitoring {row['similar_monitoring_complexity']}, "
            f"difficulty {row['similar_approximate_difficulty']}, "
            f"copied facts {row['patient_specific_facts_copied_from_g1']}, "
            f"copied reference {row['hidden_reference_copied_from_g1']}, "
            f"core {row['core_pass']}"
        )
    return "\n".join(lines) + "\n"


def pair_table_markdown() -> str:
    lines = [
        "| Generation 1 | Generation 2 | Family |",
        "| --- | --- | --- |",
    ]
    for case_id, g2_id in PAIRS:
        family = FAMILY_LABEL[FAMILY_BY_VAL[case_id]]
        lines.append(f"| {case_id} | {g2_id} | {family} |")
    return "\n".join(lines)
