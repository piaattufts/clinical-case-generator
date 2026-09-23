"""Deterministic human-readable views of frozen CLINIPROOF_TAXONOMY_V1 cases.

Reads resident-visible JSON for clinical content and the investigator answer key
only for the investigator validation packet. Does not modify frozen source files.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from app.services.readable_docs import (
    ABOUT_CASE_DATA,
    ALL_CASES_HEADER,
    CLINICIAN_PACKET_HEADER,
    DEVELOPER_NOTES_MD,
    HOW_CLINIPROOF_WORKS_MD,
    READABLE_INDEX_MD,
    VALIDATION_RUBRIC_MD,
)

MISSING = "Not specified"
CASE_IDS = tuple(f"VAL-{index:03d}" for index in range(201, 225))
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESIDENT_PATH = REPO_ROOT / "data" / "validation" / "resident_validation_cases.json"
DEFAULT_INVESTIGATOR_PATH = REPO_ROOT / "data" / "validation" / "investigator_answer_key.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "validation" / "readable"

INTERNAL_MED_STATUS = frozenset({"home", "active", "discharge"})

CLINICAL_CATEGORY_LABELS = {
    "f1_omission": "Medication omitted at discharge",
    "f1_commission": "Medication inappropriately added or continued",
    "f1_dose_mismatch": "Unexplained dose discrepancy",
    "f1_route_mismatch": "Unexplained route discrepancy",
    "f1_frequency_mismatch": "Unexplained frequency discrepancy",
    "f1_therapeutic_substitution": "Unexplained therapeutic substitution",
    "f2_monitoring_not_arranged": "Required outpatient monitoring not arranged",
    "f2_held_med_no_restart_plan": "Held medication without a restart plan",
    "f2_insufficient_supply": "Insufficient medication supply",
    "f2_hospital_only_continued": "Hospital-only medication continued after discharge",
    "f2_inpatient_substitution_not_reverted": (
        "Temporary inpatient substitution not addressed at discharge"
    ),
    "f2_pending_decision_followup_missing": (
        "Follow-up missing for an unresolved treatment decision"
    ),
    "f2_coprescription_omitted": "Required companion medication omitted",
    "none": "No intentional assessment problem",
}

FAMILY_LABELS = {
    "family_1": "Family 1 — medication-list / transition discrepancy",
    "family_2": "Family 2 — transition-of-care gap",
    "none": "No planted assessment target (clean control)",
}

LOCATION_LABELS = {
    "discharge_medications": "Discharge medications",
    "home_medications": "Home medications",
    "inpatient_medications": "Medications during hospitalization",
    "CaseLab": "Laboratory results",
    "CaseMonitoring": "Scheduled monitoring",
    "CaseInstruction": "Discharge instructions",
    "CaseFollowup": "Follow-up appointments",
    "plan.decision_reason": "Medication plan / decision reason",
}

C1_TO_C5_FORM = """### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________
"""


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if isinstance(value, list | tuple | dict) and len(value) == 0:
        return True
    return False


def display(value: object) -> str:
    if _is_missing(value):
        return MISSING
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list | tuple):
        parts = [display(item) for item in value if not _is_missing(item)]
        return ", ".join(parts) if parts else MISSING
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text if text else MISSING


def _labelize(value: object) -> str:
    text = display(value)
    if text == MISSING:
        return text
    return text.replace("_", " ")


def _cell(value: object) -> str:
    return display(value).replace("|", "\\|").replace("\n", " ")


def _md_table(
    headers: Sequence[str],
    rows: Sequence[Sequence[object]],
    *,
    empty: str | None = None,
) -> str:
    usable = [row for row in rows if any(not _is_missing(cell) for cell in row)]
    if not usable:
        return empty or "No rows were specified for this table."
    header_line = "| " + " | ".join(headers) + " |"
    align = []
    for header in headers:
        align.append("| ---: " if header in {"Value", "Result", "Unit"} else "| --- ")
    sep = "".join(align) + "|"
    body = ["| " + " | ".join(_cell(cell) for cell in row) + " |" for row in usable]
    return "\n".join([header_line, sep, *body])


def _bullet_map(items: Sequence[tuple[str, object]]) -> str:
    lines = [f"- **{label}:** {display(value)}" for label, value in items if not _is_missing(value)]
    return "\n".join(lines) if lines else f"{MISSING}."


def _as_dict(value: object) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _as_list(value: object) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def _sort_maps(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    def sort_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key) or "") for key in keys)

    return sorted((_as_dict(row) for row in rows), key=sort_key)


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return payload


def _index_cases(
    payload: dict[str, Any],
    id_field: str,
    *,
    expected_ids: Sequence[str] | None = None,
) -> dict[str, dict[str, Any]]:
    rows = payload.get("cases")
    if not isinstance(rows, list) or not rows:
        raise ValueError("source document must contain a non-empty cases list")
    indexed: dict[str, dict[str, Any]] = {}
    for item in rows:
        if not isinstance(item, dict):
            continue
        key = str(item.get(id_field) or item.get("case_id_code") or "")
        indexed[key] = item
    required = tuple(expected_ids) if expected_ids is not None else CASE_IDS
    missing = [case_id for case_id in required if case_id not in indexed]
    if missing:
        raise ValueError(f"source document missing {missing}")
    extras = sorted(set(indexed) - set(required))
    if extras:
        raise ValueError(f"source document has unexpected ids {extras}")
    return indexed


def discover_case_ids(payload: dict[str, Any], id_field: str) -> tuple[str, ...]:
    rows = payload.get("cases")
    if not isinstance(rows, list) or not rows:
        raise ValueError("source document must contain a non-empty cases list")
    ids: list[str] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        key = str(item.get(id_field) or item.get("case_id_code") or "")
        if key:
            ids.append(key)
    return tuple(ids)


def _medication_note(row: Mapping[str, Any]) -> str:
    parts: list[str] = []
    status = row.get("status")
    if not _is_missing(status) and str(status) not in INTERNAL_MED_STATUS:
        parts.append(display(status))
    for key, label in (
        ("held_reason", "held reason"),
        ("indication", "indication"),
        ("monitoring", "monitoring"),
        ("quantity_or_days", "supply"),
        ("target_or_goal", "target"),
        ("notes", "note"),
    ):
        value = row.get(key)
        if _is_missing(value):
            continue
        parts.append(f"{label}: {display(value)}")
    return "; ".join(parts)


def _medication_table(rows: Sequence[Mapping[str, Any]], context: str) -> str:
    selected = [row for row in rows if str(row.get("context") or "") == context]
    ordered = _sort_maps(selected, ("drug", "dose", "route", "frequency", "status", "medication_id"))
    table_rows = [
        [
            row.get("drug") or row.get("reported_name"),
            row.get("dose"),
            row.get("route"),
            row.get("frequency"),
            _medication_note(row),
        ]
        for row in ordered
    ]
    return _md_table(
        ("Medication", "Dose", "Route", "Frequency", "Relevant note"),
        table_rows,
        empty="No medications were specified for this list.",
    )


def _vitals_table(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = _sort_maps(rows, ("timepoint", "vital_id"))
    measures: list[list[object]] = []
    for row in ordered:
        timepoint = _labelize(row.get("timepoint"))
        prefix = "" if timepoint == MISSING else f"{timepoint}: "
        if not _is_missing(row.get("temp_c")):
            measures.append([f"{prefix}Temperature", row.get("temp_c"), "°C"])
        if not _is_missing(row.get("bp_systolic")) or not _is_missing(row.get("bp_diastolic")):
            measures.append(
                [
                    f"{prefix}Blood pressure",
                    f"{display(row.get('bp_systolic'))}/{display(row.get('bp_diastolic'))}",
                    "mmHg",
                ]
            )
        if not _is_missing(row.get("heart_rate")):
            measures.append([f"{prefix}Heart rate", row.get("heart_rate"), "beats/min"])
        if not _is_missing(row.get("resp_rate")):
            measures.append([f"{prefix}Respiratory rate", row.get("resp_rate"), "breaths/min"])
        if not _is_missing(row.get("spo2_percent")):
            measures.append([f"{prefix}SpO2", row.get("spo2_percent"), "%"])
        if not _is_missing(row.get("oxygen_support")):
            measures.append([f"{prefix}Oxygen support", row.get("oxygen_support"), ""])
    return _md_table(
        ("Measure", "Value", "Unit"),
        measures,
        empty="No vital signs were specified in this case.",
    )


def _labs_table(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = _sort_maps(rows, ("timepoint", "test_name", "lab_id"))
    table_rows = []
    for row in ordered:
        result = row.get("value")
        if _is_missing(result):
            result = row.get("value_text")
        label = row.get("test_name")
        timepoint = row.get("timepoint")
        if not _is_missing(timepoint):
            label = f"{display(label)} ({_labelize(timepoint)})"
        table_rows.append([label, result, row.get("unit")])
    return _md_table(
        ("Test", "Result", "Unit"),
        table_rows,
        empty="No laboratory results were specified in this case.",
    )


def _diagnoses_table(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = _sort_maps(rows, ("diagnosis_type", "diagnosis", "diagnosis_id"))
    return _md_table(
        ("Diagnosis", "Type", "Status", "Context"),
        [
            [row.get("diagnosis"), row.get("diagnosis_type"), row.get("status"), row.get("context")]
            for row in ordered
        ],
        empty="No diagnoses were specified in this case.",
    )


def _problems_table(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = _sort_maps(rows, ("priority", "problem", "problem_id"))
    return _md_table(
        ("Problem", "Type", "Priority", "Status"),
        [
            [row.get("problem"), row.get("problem_type"), row.get("priority"), row.get("status")]
            for row in ordered
        ],
        empty="No problem-list entries were specified in this case.",
    )


def _named_rows(
    rows: Sequence[Mapping[str, Any]],
    label_key: str,
    extra: Sequence[str],
    *,
    empty: str | None = None,
) -> str:
    if not rows:
        return empty or "No items were specified for this list."
    ordered = _sort_maps(rows, (label_key, *extra))
    lines: list[str] = []
    for row in ordered:
        details = [
            f"{key.replace('_', ' ')}: {display(row.get(key))}"
            for key in extra
            if not _is_missing(row.get(key))
        ]
        head = display(row.get(label_key))
        if details:
            lines.append(f"- {head} ({'; '.join(details)})")
        else:
            lines.append(f"- {head}")
    return "\n".join(lines) if lines else (empty or "No items were specified for this list.")


def _hospital_course(clinical: Mapping[str, Any], case: Mapping[str, Any]) -> str:
    paragraphs: list[str] = []
    io_rows = _sort_maps(_as_list(case.get("CaseIntakeOutput")), ("timepoint", "io_id"))
    for row in io_rows:
        timepoint = _labelize(row.get("timepoint"))
        sentence = (
            f"On {timepoint}, intake was {display(row.get('intake_ml'))} mL and output was "
            f"{display(row.get('output_ml'))} mL (net {display(row.get('net_ml'))} mL)."
        )
        if not _is_missing(row.get("notes")):
            sentence += f" Note: {display(row.get('notes'))}"
        paragraphs.append(sentence)
    planning = _as_dict(clinical.get("discharge_planning"))
    plan_bits = []
    if not _is_missing(planning.get("disposition")):
        plan_bits.append(f"The planned disposition is {display(planning.get('disposition'))}.")
    if not _is_missing(planning.get("discharge_readiness")):
        plan_bits.append(
            f"Discharge readiness is recorded as {display(planning.get('discharge_readiness'))}."
        )
    if not _is_missing(planning.get("home_health_ordered")):
        ordered = planning.get("home_health_ordered")
        if ordered is False or str(ordered).strip().lower() in {"no", "false"}:
            plan_bits.append("Home health was not ordered.")
        else:
            plan_bits.append(f"Home health ordered: {display(ordered)}.")
    if not _is_missing(planning.get("barriers_to_discharge")):
        plan_bits.append(
            f"Barriers to discharge are recorded as {display(planning.get('barriers_to_discharge'))}."
        )
    plan_text = " ".join(bit for bit in plan_bits if bit)
    if plan_text:
        paragraphs.append(plan_text)
    return "\n\n".join(paragraphs) if paragraphs else "No hospital-course details were specified."


def _medrec_block(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "No medication-reconciliation documentation was specified."
    blocks: list[str] = []
    for row in _sort_maps(rows, ("medrec_id",)):
        items = [
            ("Best possible medication history source", _labelize(row.get("bpmh_source"))),
            ("Interviewer", row.get("bpmh_interviewer")),
            ("Date", row.get("bpmh_date")),
            ("Reconciliation status", _labelize(row.get("medrec_status"))),
            ("Patient able to participate", row.get("patient_able_to_participate")),
            ("Unverified medications present", row.get("unverified_medications_present")),
            ("Pharmacist review", row.get("pharmacist_review")),
            ("High-alert medications identified", row.get("high_alert_meds_identified")),
            ("Discrepancy types", row.get("discrepancy_types")),
        ]
        admission = _as_dict(row.get("reconciliation_admission"))
        discharge = _as_dict(row.get("reconciliation_discharge"))
        for prefix, payload in (
            ("Admission reconciliation", admission),
            ("Discharge reconciliation", discharge),
        ):
            if any(not _is_missing(payload.get(key)) for key in ("discrepancies_found", "resolved", "notes")):
                items.append(
                    (
                        prefix,
                        "; ".join(
                            f"{key.replace('_', ' ')}: {display(payload.get(key))}"
                            for key in ("discrepancies_found", "resolved", "notes")
                            if not _is_missing(payload.get(key))
                        ),
                    )
                )
        blocks.append(_bullet_map(items))
    return "\n\n".join(blocks)


def _other_visible(case: Mapping[str, Any], clinical: Mapping[str, Any]) -> str:
    sections: list[str] = []
    support = _as_dict(clinical.get("social_support"))
    support_text = _bullet_map(
        [
            ("Living situation", support.get("living_situation") or clinical.get("social_context")),
            ("Caregiver support", support.get("caregiver_support")),
            ("Transportation", support.get("transportation")),
            ("Financial barriers", support.get("financial_barriers")),
            ("Health literacy", support.get("health_literacy")),
            ("Language preference", support.get("language_preference")),
            ("Substance use", support.get("substance_use")),
            ("Advance directive", support.get("advance_directive")),
        ]
    )
    if support_text != f"{MISSING}.":
        sections.append("Social context:\n\n" + support_text)
    weights = _as_list(case.get("CaseWeight"))
    if weights:
        weight_lines = []
        for row in _sort_maps(weights, ("timepoint", "weight_id")):
            weight_lines.append(
                f"- {_labelize(row.get('timepoint'))}: {display(row.get('weight_kg'))} kg"
                + (
                    f" (dry weight {display(row.get('dry_weight_kg'))} kg)"
                    if not _is_missing(row.get("dry_weight_kg"))
                    else ""
                )
            )
        sections.append("Serial weights:\n\n" + "\n".join(weight_lines))
    imaging = _as_list(case.get("CaseImaging"))
    consults = _as_list(case.get("CaseConsult"))
    if imaging:
        sections.append("Imaging:\n\n" + display(imaging))
    else:
        sections.append("No imaging studies were specified in this case.")
    if consults:
        sections.append("Consultations:\n\n" + display(consults))
    else:
        sections.append("No consultations were specified in this case.")
    for label, key in (
        ("Procedures", "CaseProcedure"),
        ("Devices", "CaseDevice"),
        ("Therapy restrictions", "CaseTherapyRestriction"),
    ):
        rows = _as_list(case.get(key))
        if rows:
            sections.append(f"{label}:\n\n" + display(rows))
    return "\n\n".join(sections) if sections else "No additional clinical information was specified."


def render_resident_case(case: Mapping[str, Any]) -> str:
    clinical = _as_dict(case.get("ClinicalCase"))
    case_id = display(case.get("case_id_code") or clinical.get("case_id_code"))
    presentation = _as_dict(clinical.get("presentation"))
    notes = _as_list(case.get("CaseNote"))
    medications = _as_list(case.get("CaseMedication"))
    note_text = "\n\n".join(
        display(row.get("note_text"))
        for row in _sort_maps(notes, ("note_type", "note_id"))
        if not _is_missing(row.get("note_text"))
    )
    history_bits = []
    if not _is_missing(clinical.get("medical_history")):
        history_bits.append("**Past medical history:** " + display(clinical.get("medical_history")))
    if not _is_missing(clinical.get("allergies")):
        history_bits.append("**Allergies:** " + display(clinical.get("allergies")))
    diagnoses = _diagnoses_table(_as_list(case.get("CaseDiagnosis")))
    problems = _problems_table(_as_list(case.get("CaseProblemList")))
    history_body = (
        "\n\n".join(history_bits)
        if history_bits
        else "No additional past medical history or allergy fields were specified."
    )
    lines = [
        f"# {case_id}",
        "",
        "## Patient overview",
        "",
        "The following overview lists the demographic and admission facts stored for this synthetic patient.",
        "",
        _bullet_map(
            [
                ("Age", clinical.get("patient_age")),
                ("Sex/gender", clinical.get("patient_gender")),
                (
                    "Weight",
                    None
                    if _is_missing(clinical.get("weight_kg"))
                    else f"{display(clinical.get('weight_kg'))} kg",
                ),
                ("Clinical setting/specialty", clinical.get("specialty")),
                ("Admission diagnosis", clinical.get("admission_dx")),
                ("Disposition", clinical.get("disposition_status")),
                ("One-liner", clinical.get("one_liner")),
            ]
        ),
        "",
        "## Reason for hospitalization",
        "",
        "The following fields are the presenting complaint and history stored on the case.",
        "",
        _bullet_map(
            [
                (
                    "Chief complaint",
                    presentation.get("chief_complaint") or clinical.get("chief_complaint"),
                ),
                ("Symptoms", presentation.get("presenting_symptoms")),
                ("Symptom duration", presentation.get("symptom_duration")),
                ("Symptom course", presentation.get("symptom_course")),
                ("History of present illness", presentation.get("hpi")),
                ("Review of systems", presentation.get("review_of_systems")),
            ]
        ),
        "",
        "### Admission note",
        "",
        note_text if note_text else "No admission note was specified.",
        "",
        "## Relevant medical history",
        "",
        history_body,
        "",
        "The following table lists diagnoses stored on the case.",
        "",
        diagnoses,
        "",
        "The following table lists problem-list entries stored on the case.",
        "",
        problems,
        "",
        "## Hospital course",
        "",
        _hospital_course(clinical, case),
        "",
        "## Clinical status at discharge",
        "",
        "### Vital signs",
        "",
        "The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.",
        "",
        _vitals_table(_as_list(case.get("CaseVital"))),
        "",
        "### Laboratory results",
        "",
        "The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.",
        "",
        _labs_table(_as_list(case.get("CaseLab"))),
        "",
        "## Home medications",
        "",
        "The following table lists medications recorded as the home regimen.",
        "",
        _medication_table(medications, "home"),
        "",
        "## Medications during hospitalization",
        "",
        "The following table lists medications recorded as active during the hospital stay.",
        "",
        _medication_table(medications, "inpatient"),
        "",
        "## Discharge medications",
        "",
        "The following table lists medications recorded on the discharge list.",
        "",
        _medication_table(medications, "discharge"),
        "",
        "## Medication reconciliation",
        "",
        _medrec_block(_as_list(case.get("CaseMedicationReconciliation"))),
        "",
        "## Follow-up and monitoring",
        "",
        "The following items are scheduled monitoring tasks stored on the case.",
        "",
        _named_rows(
            _as_list(case.get("CaseMonitoring")),
            "parameter",
            ("frequency", "target", "trigger_for_action", "duration", "responsible_service"),
            empty="No scheduled monitoring was specified.",
        ),
        "",
        "The following items are follow-up appointments stored on the case.",
        "",
        _named_rows(
            _as_list(case.get("CaseFollowup")),
            "item",
            ("timing", "with_service"),
            empty="No follow-up appointments were specified.",
        ),
        "",
        "## Discharge instructions",
        "",
        _named_rows(
            _as_list(case.get("CaseInstruction")),
            "instruction_text",
            ("category",),
            empty="No discharge instructions were specified.",
        ),
        "",
        "## Other relevant clinical information",
        "",
        "The following items are return precautions stored on the case.",
        "",
        _named_rows(
            _as_list(case.get("CaseReturnPrecaution")),
            "symptom",
            ("reason", "action", "severity", "patient_instruction"),
            empty="No return precautions were specified.",
        ),
        "",
        _other_visible(case, clinical),
        "",
        ABOUT_CASE_DATA.rstrip(),
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _format_state(value: object) -> str:
    """Render clean/injected state. Empty collections are meaningful (absence)."""
    if value is None:
        return "none"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, int | float):
        return str(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return "none"
        if "SYN" in text and any(character.isdigit() for character in text):
            return "present"
        return text.replace("_", " ")
    if isinstance(value, list):
        if not value:
            return "none"
        return "; ".join(_format_state(item) for item in value)
    if isinstance(value, Mapping):
        if not value:
            return "none"
        bits = [
            f"{str(key).replace('_', ' ')}: {_format_state(item)}"
            for key, item in sorted(value.items())
        ]
        return "; ".join(bits) if bits else "none"
    return str(value)


def _trigger_lines(value: object) -> str:
    rows = value if isinstance(value, list) else []
    if not rows:
        return "No trigger medications were specified."
    lines: list[str] = []
    for row in rows:
        payload = _as_dict(row)
        drug = display(payload.get("drug"))
        extras = [
            f"{key}={display(payload.get(key))}"
            for key in ("role", "rxcui", "rule_code")
            if not _is_missing(payload.get(key))
        ]
        lines.append(f"- {drug}" + (f" ({'; '.join(extras)})" if extras else ""))
    return "\n".join(lines)


def _location_text(value: object) -> str:
    if _is_missing(value):
        return MISSING
    if isinstance(value, list | tuple):
        parts = [_location_text(item) for item in value if not _is_missing(item)]
        return ", ".join(parts) if parts else MISSING
    labels = []
    for token in str(value).split(","):
        token = token.strip()
        if not token:
            continue
        labels.append(LOCATION_LABELS.get(token, token.replace("_", " ")))
    return ", ".join(labels) if labels else MISSING


def render_investigator_spec(row: Mapping[str, Any]) -> str:
    error = _as_dict(row.get("error"))
    category = str(error.get("error_category") or "none")
    family = str(error.get("error_family") or row.get("control_error_status") or "none")
    control = str(
        row.get("control_error_status") or error.get("control_error_status") or ""
    )
    clinical_label = CLINICAL_CATEGORY_LABELS.get(category, _labelize(category))
    family_label = FAMILY_LABELS.get(family, _labelize(family))
    changes = error.get("injected_state")
    if _is_missing(changes):
        changes = error.get("intentional_changes")
    change_rows = changes if isinstance(changes, list) else []
    first = _as_dict(change_rows[0]) if change_rows else {}
    should_parts: list[str] = []
    description = error.get("error_description") or error.get("rationale")
    if not _is_missing(description):
        should_parts.append(display(description))
    if first:
        should_parts.append("Clean expected state: " + _format_state(first.get("clean_expected_state")))
    appears = _format_state(first.get("injected_state")) if first else MISSING
    should_occur = "\n\n".join(should_parts) if should_parts else MISSING
    if control == "clean_control" or category == "none":
        lines = [
            "## Intended assessment issue",
            "",
            "**Clinical category:**",
            "",
            "No intentional assessment problem (clean control)",
            "",
            "**CliniProof identifier:**",
            "",
            "`none`",
            "",
            "**Medication(s) involved:**",
            "",
            "No trigger medication is specified because this is a clean control.",
            "",
            "**What should have occurred clinically:**",
            "",
            "No planted medication-reconciliation discrepancy or transition-of-care gap.",
            "",
            "**What appears in the case:**",
            "",
            "The resident-visible chart is the clean expected state.",
            "",
            "**Where the relevant evidence appears:**",
            "",
            "Review the full chart; there is no concealed target.",
            "",
            "**Expected clinical action:**",
            "",
            "NO INTENTIONAL ERROR",
            "",
        ]
        return "\n".join(lines)
    lines = [
        "## Intended assessment issue",
        "",
        "**Clinical category:**",
        "",
        clinical_label,
        "",
        "**CliniProof identifier:**",
        "",
        f"`{category}`",
        "",
        f"**Family:** {family_label} (`{family}`)",
        "",
        "**Medication(s) involved:**",
        "",
        _trigger_lines(error.get("trigger_meds") or error.get("affected_medication")),
        "",
        "**What should have occurred clinically:**",
        "",
        should_occur,
        "",
        "**What appears in the case:**",
        "",
        appears,
        "",
        "**Where the relevant evidence appears:**",
        "",
        _location_text(error.get("evidence_location") or error.get("detectability_location")),
        "",
        "**Expected clinical action:**",
        "",
        display(error.get("correct_action")),
        "",
        "### Technical implementation",
        "",
        _bullet_map(
            [
                ("Changed field", first.get("changed_field") or error.get("changed_field")),
                ("Detectability location", _location_text(error.get("detectability_location"))),
                ("Evidence required", error.get("evidence_required")),
                ("Rationale", error.get("rationale") or error.get("error_description")),
            ]
        ),
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _join_pages(pages: Sequence[str]) -> str:
    return "\n---\n\n".join(page.rstrip() for page in pages) + "\n"


def render_all_cases(
    case_pages: Sequence[tuple[str, str]],
    *,
    batch_code: str = "CLINIPROOF_TAXONOMY_V1",
    case_ids: Sequence[str] | None = None,
) -> str:
    header = ALL_CASES_HEADER
    ids = tuple(case_ids) if case_ids is not None else CASE_IDS
    if batch_code != "CLINIPROOF_TAXONOMY_V1" or ids != CASE_IDS:
        first = ids[0] if ids else "VAL-001"
        last = ids[-1] if ids else "VAL-001"
        header = (
            "# CliniProof Clinical Case Set\n\n"
            f"## {batch_code}\n\n"
            "This document is intended for residents, clinicians, medical educators, "
            "pharmacists, and clinical informatics collaborators who want to review the "
            "clinical cases without reading the underlying JSON representation.\n\n"
            f"The set contains {len(ids)} cases, labeled {first} through {last}. "
            "Each case is a synthetic inpatient encounter assembled for "
            "medication-reconciliation review. The software has already checked "
            "structure, terminology provenance, and a limited set of implemented "
            "clinical rules. Those automated checks do not establish clinical validity. "
            "Until clinicians finish review, treat every record as a machine-validated "
            "synthetic resident-review case pending clinician validation.\n\n"
            "This file contains only the information a resident would see. It does not "
            "identify which cases contain an intended assessment problem, if any, and it "
            "does not include investigator answer keys.\n"
        )
    return header.rstrip() + "\n\n---\n\n" + _join_pages([page for _, page in case_pages])


def render_clinician_packet(
    case_pages: Sequence[tuple[str, str]],
    investigator_rows: Mapping[str, Mapping[str, Any]],
    *,
    batch_code: str = "CLINIPROOF_TAXONOMY_V1",
    case_ids: Sequence[str] | None = None,
) -> str:
    header = CLINICIAN_PACKET_HEADER
    ids = tuple(case_ids) if case_ids is not None else CASE_IDS
    if batch_code != "CLINIPROOF_TAXONOMY_V1" or ids != CASE_IDS:
        first = ids[0] if ids else "VAL-001"
        last = ids[-1] if ids else "VAL-001"
        header = CLINICIAN_PACKET_HEADER.replace("CLINIPROOF_TAXONOMY_V1", batch_code).replace(
            "VAL-201 through VAL-224", f"{first} through {last}"
        )
    blocks = [header.rstrip()]
    for case_id, page in case_pages:
        spec = render_investigator_spec(investigator_rows[case_id])
        blocks.append(
            page.rstrip()
            + "\n\n"
            + spec.rstrip()
            + "\n\n"
            + C1_TO_C5_FORM.rstrip()
        )
    return "\n\n---\n\n".join(blocks) + "\n"


WORKSHEET_COLUMNS = (
    "validation_case_id",
    "reviewer_id",
    "c1",
    "c2",
    "c3",
    "c4",
    "c5",
    "c4_additional_problem",
    "recommendation",
    "comments",
)

OBSOLETE_READABLE_FILES = (
    "plausibility_only_packet.md",
    "reviewer_protocol.md",
    "consensus_worksheet.csv",
)


def render_clinical_validation_worksheet(case_ids: Sequence[str] | None = None) -> str:
    header = ",".join(WORKSHEET_COLUMNS)
    rows = [header]
    empty = "," * (len(WORKSHEET_COLUMNS) - 1)
    for case_id in case_ids or CASE_IDS:
        rows.append(f"{case_id}{empty}")
    return "\n".join(rows) + "\n"


def _with_trailing_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def build_readable_packets(
    *,
    resident_path: Path = DEFAULT_RESIDENT_PATH,
    investigator_path: Path = DEFAULT_INVESTIGATOR_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    case_ids: Sequence[str] | None = None,
    batch_code: str = "CLINIPROOF_TAXONOMY_V1",
) -> dict[str, Path]:
    resident_doc = _load_json_object(resident_path)
    investigator_doc = _load_json_object(investigator_path)
    ids = tuple(case_ids) if case_ids is not None else CASE_IDS
    resident = _index_cases(resident_doc, "case_id_code", expected_ids=ids)
    investigator = _index_cases(investigator_doc, "validation_case_id", expected_ids=ids)
    case_dir = output_dir / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    pages: list[tuple[str, str]] = []
    written: dict[str, Path] = {}
    for case_id in ids:
        page = render_resident_case(resident[case_id])
        pages.append((case_id, page))
        path = case_dir / f"{case_id}.md"
        path.write_text(page, encoding="utf-8", newline="\n")
        written[case_id] = path
    files = {
        "readme": output_dir / "README.md",
        "all_cases": output_dir / "all_cases.md",
        "validation_rubric": output_dir / "validation_rubric.md",
        "clinician_validation_packet": output_dir / "clinician_validation_packet.md",
        "how_cliniproof_works": output_dir / "how_cliniproof_works.md",
        "developer_notes": output_dir / "developer_notes.md",
        "clinical_validation_worksheet": output_dir / "clinical_validation_worksheet.csv",
    }
    readme_text = READABLE_INDEX_MD
    if batch_code != "CLINIPROOF_TAXONOMY_V1" or ids != CASE_IDS:
        first = ids[0] if ids else "VAL-001"
        last = ids[-1] if ids else "VAL-001"
        readme_text = (
            "# Readable CliniProof review materials\n\n"
            f"This directory contains the human-readable review materials for "
            f"`{batch_code}`, cases {first} through {last}. Clinical validation uses "
            "a single review stage. Each clinician or resident reviews the complete "
            "case and assesses C1–C5 in one pass.\n\n"
            "Until clinicians finish review, treat every record as a machine-validated "
            "synthetic resident-review case pending clinician validation. Passing the "
            "clean-case diversity audit does not mean the cases are clinically validated.\n"
        )
    files["readme"].write_text(_with_trailing_newline(readme_text), encoding="utf-8", newline="\n")
    files["all_cases"].write_text(
        render_all_cases(pages, batch_code=batch_code, case_ids=ids),
        encoding="utf-8",
        newline="\n",
    )
    files["validation_rubric"].write_text(
        _with_trailing_newline(VALIDATION_RUBRIC_MD),
        encoding="utf-8",
        newline="\n",
    )
    files["clinician_validation_packet"].write_text(
        render_clinician_packet(
            pages, investigator, batch_code=batch_code, case_ids=ids
        ),
        encoding="utf-8",
        newline="\n",
    )
    files["how_cliniproof_works"].write_text(
        _with_trailing_newline(HOW_CLINIPROOF_WORKS_MD), encoding="utf-8", newline="\n"
    )
    files["developer_notes"].write_text(
        _with_trailing_newline(DEVELOPER_NOTES_MD), encoding="utf-8", newline="\n"
    )
    files["clinical_validation_worksheet"].write_text(
        render_clinical_validation_worksheet(ids), encoding="utf-8", newline="\n"
    )
    for obsolete_name in OBSOLETE_READABLE_FILES:
        obsolete_path = output_dir / obsolete_name
        if obsolete_path.exists():
            obsolete_path.unlink()
    written.update(files)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build human-readable CliniProof validation packets from frozen JSON."
    )
    parser.add_argument("--resident", type=Path, default=DEFAULT_RESIDENT_PATH)
    parser.add_argument("--investigator", type=Path, default=DEFAULT_INVESTIGATOR_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--batch-code", default="CLINIPROOF_TAXONOMY_V1")
    args = parser.parse_args(argv)
    resident_doc = _load_json_object(args.resident)
    case_ids = None
    if args.batch_code != "CLINIPROOF_TAXONOMY_V1" or args.resident != DEFAULT_RESIDENT_PATH:
        case_ids = discover_case_ids(resident_doc, "case_id_code")
    build_readable_packets(
        resident_path=args.resident,
        investigator_path=args.investigator,
        output_dir=args.output_dir,
        case_ids=case_ids,
        batch_code=args.batch_code,
    )
    return 0
