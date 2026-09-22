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

MISSING = "Not documented"
CASE_IDS = tuple(f"VAL-{index:03d}" for index in range(201, 225))
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESIDENT_PATH = REPO_ROOT / "data" / "validation" / "resident_validation_cases.json"
DEFAULT_INVESTIGATOR_PATH = REPO_ROOT / "data" / "validation" / "investigator_answer_key.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "validation" / "readable"

C1_FORM = """### C1 Clinical plausibility

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation/demographics | ☐ | ☐ | ☐ | ☐ |
| Diagnosis-presentation coherence | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Cross-document consistency | ☐ | ☐ | ☐ | ☐ |
| Discharge context/follow-up | ☐ | ☐ | ☐ | ☐ |

Global plausibility:

☐ Yes

☐ No

Specific concerns / fields requiring correction:

____________________________________

Overall C1:

☐ Pass

☐ Revise
"""

C2_TO_C5_FORM = """### C2 Intended error present and correctly classified

☐ Pass

☐ Fail

Comments:

### C3 Detectability from documents alone

☐ Pass

☐ Fail

Evidence reviewed:

Ambiguity / cueing concerns:

### C4 Absence of unintended errors

☐ Pass

☐ Fail

Additional possible discrepancies/gaps found:

Severity / importance:

### C5 Difficulty for internal medicine resident

☐ Easy

☐ Moderate

☐ Hard

☐ Outlier / inappropriate

Comments:

### Final case disposition

☐ Accept

☐ Revise and re-rate

☐ Regenerate / retire

☐ Adjudication required

Overall comments:
"""

VALIDATION_RUBRIC_MD = """# CliniProof clinician-validation rubric

Status: machine-validated synthetic resident-review cases pending clinician validation.

This rubric is for clinician review of frozen `CLINIPROOF_TAXONOMY_V1` cases (`VAL-201`–`VAL-224`). The five criteria serve different purposes. C1 can be completed from resident-visible documents alone. C2–C5 require the concealed assessment specification and belong on the investigator packet.

`CLINIPROOF_TAXONOMY_V1` covers all currently implemented CliniProof error categories. `f2_coprescription_omitted` is not represented in this frozen batch and remains `not_yet_implementable`.

## Family-specific guidance for C2–C4

**Family 1** categories are medication-list / transition discrepancies:

- `f1_omission`
- `f1_commission`
- `f1_dose_mismatch`
- `f1_route_mismatch`
- `f1_frequency_mismatch`
- `f1_therapeutic_substitution`

**Family 2** categories are transition-of-care gaps. They may occur without changing the medication list:

- `f2_monitoring_not_arranged`
- `f2_held_med_no_restart_plan`
- `f2_insufficient_supply`
- `f2_hospital_only_continued`
- `f2_inpatient_substitution_not_reverted`
- `f2_pending_decision_followup_missing`

Do **not** identify Family 2 solely by comparing home versus discharge medication lists. For Family 2, confirm that the trigger or precondition is visible and that the missing companion action (monitoring, restart plan, supply, hospital-only stop, substitution revert, or follow-up) is the specified target.

## C1. Clinical plausibility — fixable

Definition: the resident-visible case forms a coherent and clinically credible inpatient encounter.

Assess the following domains independently:

1. Presentation and demographics
2. Diagnosis-presentation coherence
3. Vital signs
4. Laboratory findings
5. Medication regimen
6. Hospital course
7. Cross-document consistency
8. Discharge context and follow-up

Scale for each domain:

- **4 — Fully plausible.** No clinically meaningful concern.
- **3 — Plausible with minor concern.** A minor issue is present but would not materially alter interpretation.
- **2 — Questionable.** A clinically meaningful inconsistency or implausibility is present and the case requires revision.
- **1 — Implausible.** A major contradiction or unrealistic feature prevents the case from representing a credible inpatient encounter.

Global question:

“Apart from the intentionally planted reconciliation discrepancy, could this case reasonably represent a patient encountered in the stated clinical setting?”

Yes / No

**C1 pass:** all clinically relevant domains ≥ 3 **and** global judgment = Yes.

**C1 revise:** any domain ≤ 2 **or** global judgment = No.

Require comments identifying the exact field or issue for any rating below 3.

Clinical plausibility is **not** synonymous with optimal management or complete guideline concordance.

## C2. Intended error present and correctly classified — hard gate

Standard: the planted error is actually present and matches the specified CliniProof family/category.

Response: Pass / Fail

Questions:

- Is the intended discrepancy/gap actually present?
- Is it correctly classified?
- Does the investigator specification describe what is actually visible in the case?

A failure means the case cannot be scored against its intended answer key.

## C3. Detectability from documents alone — hard gate

Standard: the target is recoverable from the resident-visible case alone. The resident should not require withheld clinical information. The error must also not be artificially disclosed by formatting or wording.

For Family 2: the trigger/precondition must be visible and unambiguous.

Response: Pass / Fail

Require comments on evidence location, ambiguity, missing information, and cueing.

## C4. Absence of unintended errors — hard gate

Standard: no additional clinically meaningful medication-reconciliation discrepancy or transition-of-care gap exists beyond the specified target.

This must be assessed by **active hunt**. Do not merely record errors that happen to be noticed.

Ask raters to list any additional possible error and its severity/importance.

Response: Pass / Fail

## C5. Difficulty for target learner — advisory

Target learner: internal medicine resident.

Rating: Easy / Moderate / Hard / Outlier / inappropriate

This is an expert provisional estimate only. Difficulty is ultimately an empirical property to be calibrated after resident administration.

C5 alone should not reject a case.

## Final disposition

- Accept
- Revise and re-rate
- Regenerate / retire
- Adjudication required
"""

READABLE_INDEX_MD = """# Readable clinician-validation packets

These files are derived human-readable views of frozen `CLINIPROOF_TAXONOMY_V1` (`VAL-201`–`VAL-224`). They do **not** replace the frozen JSON. They were generated by `scripts/build_readable_validation_packets.py` from:

- [`../resident_validation_cases.json`](../resident_validation_cases.json) for all clinician-visible patient information
- [`../investigator_answer_key.json`](../investigator_answer_key.json) only for the investigator packet

Status: machine-validated synthetic resident-review cases pending clinician validation.

Regenerate (from the repository root; does not modify frozen JSON):

```bash
python scripts/build_readable_validation_packets.py
```

## Safe for plausibility-only review

These files contain resident-visible case content plus, where noted, the C1 form. They do **not** include planted-error family, category, trigger labels, control status, or answer keys.

| File | Contents |
| --- | --- |
| [`all_cases.md`](all_cases.md) | All 24 readable cases, sequential |
| [`plausibility_only_packet.md`](plausibility_only_packet.md) | Each readable case followed by the C1 assessment form |
| [`cases/VAL-201.md`](cases/VAL-201.md) … [`VAL-224.md`](cases/VAL-224.md) | One readable case per page |
| [`validation_rubric.md`](validation_rubric.md) | C1–C5 rubric (no per-case answers) |

## Investigator / validator only

| File | Contents |
| --- | --- |
| [`clinician_validation_packet.md`](clinician_validation_packet.md) | Readable case + concealed target specification + C1–C5 forms |

**Do not provide `clinician_validation_packet.md` to resident study participants.**
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


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    usable = [row for row in rows if any(not _is_missing(cell) for cell in row)]
    if not usable:
        return f"{MISSING}."
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


def _index_cases(payload: dict[str, Any], id_field: str) -> dict[str, dict[str, Any]]:
    rows = payload.get("cases")
    if not isinstance(rows, list) or not rows:
        raise ValueError("source document must contain a non-empty cases list")
    indexed: dict[str, dict[str, Any]] = {}
    for item in rows:
        if not isinstance(item, dict):
            continue
        key = str(item.get(id_field) or item.get("case_id_code") or "")
        indexed[key] = item
    missing = [case_id for case_id in CASE_IDS if case_id not in indexed]
    if missing:
        raise ValueError(f"source document missing {missing}")
    extras = sorted(set(indexed) - set(CASE_IDS))
    if extras:
        raise ValueError(f"source document has unexpected ids {extras}")
    return indexed


def _medication_note(row: Mapping[str, Any]) -> str:
    parts: list[str] = []
    for key in ("status", "held_reason", "monitoring", "quantity_or_days", "notes"):
        value = row.get(key)
        if _is_missing(value):
            continue
        if key == "quantity_or_days":
            parts.append(f"supply: {display(value)}")
        elif key == "status":
            parts.append(display(value))
        else:
            parts.append(f"{key.replace('_', ' ')}: {display(value)}")
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
        ("Medication", "Dose", "Route", "Frequency", "Status / note"),
        table_rows,
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
            measures.append([f"{prefix}Oxygen support", row.get("oxygen_support"), MISSING])
    return _md_table(("Measure", "Value", "Unit"), measures)


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
    return _md_table(("Test", "Result", "Unit"), table_rows)


def _diagnoses_table(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = _sort_maps(rows, ("diagnosis_type", "diagnosis", "diagnosis_id"))
    return _md_table(
        ("Diagnosis", "Type", "Status", "Context"),
        [
            [row.get("diagnosis"), row.get("diagnosis_type"), row.get("status"), row.get("context")]
            for row in ordered
        ],
    )


def _problems_table(rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = _sort_maps(rows, ("priority", "problem", "problem_id"))
    return _md_table(
        ("Problem", "Type", "Priority", "Status"),
        [
            [row.get("problem"), row.get("problem_type"), row.get("priority"), row.get("status")]
            for row in ordered
        ],
    )


def _named_rows(rows: Sequence[Mapping[str, Any]], label_key: str, extra: Sequence[str]) -> str:
    if not rows:
        return f"{MISSING}."
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
    return "\n".join(lines) if lines else f"{MISSING}."


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
    plan_bits = [
        f"Disposition {display(planning.get('disposition'))}."
        if not _is_missing(planning.get("disposition"))
        else "",
        f"Discharge readiness: {display(planning.get('discharge_readiness'))}."
        if not _is_missing(planning.get("discharge_readiness"))
        else "",
        f"Home health ordered: {display(planning.get('home_health_ordered'))}."
        if not _is_missing(planning.get("home_health_ordered"))
        else "",
        f"Barriers to discharge: {display(planning.get('barriers_to_discharge'))}."
        if not _is_missing(planning.get("barriers_to_discharge"))
        else "",
    ]
    plan_text = " ".join(bit for bit in plan_bits if bit)
    if plan_text:
        paragraphs.append(plan_text)
    inpatient = [
        row
        for row in _as_list(case.get("CaseMedication"))
        if str(row.get("context") or "") == "inpatient"
    ]
    if inpatient:
        names = display(
            [
                row.get("drug") or row.get("reported_name")
                for row in _sort_maps(inpatient, ("drug", "medication_id"))
            ]
        )
        paragraphs.append(f"Inpatient medications documented: {names}.")
    return "\n\n".join(paragraphs) if paragraphs else f"{MISSING}."


def _medrec_block(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return f"{MISSING}."
    blocks: list[str] = []
    for row in _sort_maps(rows, ("medrec_id",)):
        items = [
            ("Best possible medication history source", row.get("bpmh_source")),
            ("Interviewer", row.get("bpmh_interviewer")),
            ("Date", row.get("bpmh_date")),
            ("Reconciliation status", row.get("medrec_status")),
            ("Patient able to participate", row.get("patient_able_to_participate")),
            ("Unverified medications present", row.get("unverified_medications_present")),
            ("Pharmacist review", row.get("pharmacist_review")),
            ("High-alert medications identified", row.get("high_alert_meds_identified")),
            ("Discrepancy types", row.get("discrepancy_types")),
        ]
        admission = _as_dict(row.get("reconciliation_admission"))
        discharge = _as_dict(row.get("reconciliation_discharge"))
        for prefix, payload in (("Admission reconciliation", admission), ("Discharge reconciliation", discharge)):
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
    if not _is_missing(clinical.get("allergies")):
        sections.append("Allergies: " + display(clinical.get("allergies")))
    if not _is_missing(clinical.get("medical_history")):
        sections.append("Medical history: " + display(clinical.get("medical_history")))
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
    for label, key in (
        ("Procedures", "CaseProcedure"),
        ("Devices", "CaseDevice"),
        ("Therapy restrictions", "CaseTherapyRestriction"),
    ):
        rows = _as_list(case.get(key))
        if rows:
            sections.append(f"{label}:\n\n" + display(rows))
    return "\n\n".join(sections) if sections else f"{MISSING}."


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
    symptoms = presentation.get("presenting_symptoms")
    lines = [
        f"# {case_id}",
        "",
        "## Patient summary",
        "",
        _bullet_map(
            [
                ("Age", clinical.get("patient_age")),
                ("Sex/gender", clinical.get("patient_gender")),
                ("Weight", None if _is_missing(clinical.get("weight_kg")) else f"{display(clinical.get('weight_kg'))} kg"),
                ("Clinical setting/specialty", clinical.get("specialty")),
                ("Admission diagnosis", clinical.get("admission_dx")),
                ("Disposition", clinical.get("disposition_status")),
                ("One-liner", clinical.get("one_liner")),
            ]
        ),
        "",
        "## Presentation",
        "",
        _bullet_map(
            [
                ("Chief complaint", presentation.get("chief_complaint") or clinical.get("chief_complaint")),
                ("Symptoms", symptoms),
                ("Symptom duration", presentation.get("symptom_duration")),
                ("Symptom course", presentation.get("symptom_course")),
                ("History of present illness", presentation.get("hpi")),
                ("Review of systems", presentation.get("review_of_systems")),
            ]
        ),
        "",
        "### H&P / admission note",
        "",
        note_text if note_text else f"{MISSING}.",
        "",
        "## Hospital course",
        "",
        _hospital_course(clinical, case),
        "",
        "## Diagnoses / problem list",
        "",
        _diagnoses_table(_as_list(case.get("CaseDiagnosis"))),
        "",
        _problems_table(_as_list(case.get("CaseProblemList"))),
        "",
        "## Vitals",
        "",
        _vitals_table(_as_list(case.get("CaseVital"))),
        "",
        "## Laboratory results",
        "",
        _labs_table(_as_list(case.get("CaseLab"))),
        "",
        "## Imaging",
        "",
        f"{MISSING}." if not _as_list(case.get("CaseImaging")) else display(case.get("CaseImaging")),
        "",
        "## Consultations",
        "",
        f"{MISSING}." if not _as_list(case.get("CaseConsult")) else display(case.get("CaseConsult")),
        "",
        "## Home medications",
        "",
        _medication_table(medications, "home"),
        "",
        "## Inpatient medications",
        "",
        _medication_table(medications, "inpatient"),
        "",
        "## Discharge medications",
        "",
        _medication_table(medications, "discharge"),
        "",
        "## Medication reconciliation / relevant transition information",
        "",
        _medrec_block(_as_list(case.get("CaseMedicationReconciliation"))),
        "",
        "## Monitoring / follow-up",
        "",
        "Scheduled monitoring:",
        "",
        _named_rows(
            _as_list(case.get("CaseMonitoring")),
            "parameter",
            ("frequency", "target", "trigger_for_action", "duration", "responsible_service"),
        ),
        "",
        "Appointments / follow-up plan:",
        "",
        _named_rows(
            _as_list(case.get("CaseFollowup")),
            "item",
            ("timing", "with_service"),
        ),
        "",
        "## Discharge instructions",
        "",
        _named_rows(_as_list(case.get("CaseInstruction")), "instruction_text", ("category",)),
        "",
        "## Return precautions",
        "",
        _named_rows(
            _as_list(case.get("CaseReturnPrecaution")),
            "symptom",
            ("reason", "action", "severity", "patient_instruction"),
        ),
        "",
        "## Other resident-visible information",
        "",
        _other_visible(case, clinical),
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _format_nested(value: object) -> str:
    if _is_missing(value):
        return MISSING
    if isinstance(value, bool | int | float | str):
        return display(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2)


def _trigger_lines(value: object) -> str:
    rows = value if isinstance(value, list) else []
    if not rows:
        return f"{MISSING}."
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


def render_investigator_spec(row: Mapping[str, Any]) -> str:
    error = _as_dict(row.get("error"))
    changes = error.get("injected_state")
    if _is_missing(changes):
        changes = error.get("intentional_changes")
    change_rows = changes if isinstance(changes, list) else []
    change_blocks: list[str] = []
    for index, item in enumerate(change_rows, start=1):
        payload = _as_dict(item)
        skip = {
            "seed",
            "kind",
            "error_family",
            "error_category",
            "source_backed_rationale",
        }
        fields = [
            (key.replace("_", " "), payload.get(key))
            for key in sorted(payload)
            if key not in skip
        ]
        change_blocks.append(f"Change {index}:\n\n" + "\n".join(f"- **{label}:** {_format_nested(value)}" for label, value in fields if not _is_missing(value)))
    change_text = "\n\n".join(change_blocks) if change_blocks else f"{MISSING}."
    lines = [
        "## Investigator specification",
        "",
        _bullet_map(
            [
                ("Error family", error.get("error_family")),
                ("Error category", error.get("error_category")),
                ("Control / error status", row.get("control_error_status") or error.get("control_error_status")),
                ("Detectability location", error.get("detectability_location")),
                ("Evidence location", error.get("evidence_location")),
                ("Evidence required", error.get("evidence_required")),
                ("Correct action", error.get("correct_action")),
                ("Changed field", error.get("changed_field")),
                ("Rationale", error.get("rationale") or error.get("error_description")),
            ]
        ),
        "",
        "Trigger medication(s):",
        "",
        _trigger_lines(error.get("trigger_meds") or error.get("affected_medication")),
        "",
        "Intended clean state / injected state:",
        "",
        change_text,
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _join_pages(pages: Sequence[str]) -> str:
    return "\n---\n\n".join(page.rstrip() for page in pages) + "\n"


def render_all_cases(case_pages: Sequence[tuple[str, str]]) -> str:
    header = """# CLINIPROOF_TAXONOMY_V1 — Readable Case Set

Status:

Machine-validated synthetic resident-review cases pending clinician validation.

Cases:

VAL-201 through VAL-224

Total:

24

This file contains resident-visible case content only.
"""
    return header.rstrip() + "\n\n---\n\n" + _join_pages([page for _, page in case_pages])


def render_plausibility_packet(case_pages: Sequence[tuple[str, str]]) -> str:
    header = """# CLINIPROOF_TAXONOMY_V1 — Plausibility-only packet

This packet is for an independent clinician assessing **C1 clinical plausibility**.

It contains resident-visible case information only. It does **not** reveal planted error, error family, error category, trigger medication, correct action, clean versus error-bearing status, or investigator answer keys.

Complete the C1 form after each case. Rubric: [`validation_rubric.md`](validation_rubric.md).

Status: machine-validated synthetic resident-review cases pending clinician validation.
"""
    blocks = [header.rstrip()]
    for _, page in case_pages:
        blocks.append(page.rstrip() + "\n\n" + C1_FORM.rstrip())
    return "\n\n---\n\n".join(blocks) + "\n"


def render_investigator_packet(
    case_pages: Sequence[tuple[str, str]], investigator_rows: Mapping[str, Mapping[str, Any]]
) -> str:
    header = """# INVESTIGATOR / VALIDATOR ONLY

This file contains the concealed assessment specification.

**Do not provide it to resident study participants.**

Use this packet for primary expert raters completing the full CliniProof C1–C5 validation rubric. Rubric: [`validation_rubric.md`](validation_rubric.md).

Status: machine-validated synthetic resident-review cases pending clinician validation.
"""
    blocks = [header.rstrip()]
    for case_id, page in case_pages:
        spec = render_investigator_spec(investigator_rows[case_id])
        blocks.append(
            page.rstrip()
            + "\n\n"
            + spec.rstrip()
            + "\n\n"
            + C1_FORM.rstrip()
            + "\n\n"
            + C2_TO_C5_FORM.rstrip()
        )
    return "\n\n---\n\n".join(blocks) + "\n"


def _with_trailing_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def build_readable_packets(
    *,
    resident_path: Path = DEFAULT_RESIDENT_PATH,
    investigator_path: Path = DEFAULT_INVESTIGATOR_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Path]:
    resident = _index_cases(_load_json_object(resident_path), "case_id_code")
    investigator = _index_cases(_load_json_object(investigator_path), "validation_case_id")
    case_dir = output_dir / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    pages: list[tuple[str, str]] = []
    written: dict[str, Path] = {}
    for case_id in CASE_IDS:
        page = render_resident_case(resident[case_id])
        pages.append((case_id, page))
        path = case_dir / f"{case_id}.md"
        path.write_text(page, encoding="utf-8", newline="\n")
        written[case_id] = path
    files = {
        "readme": output_dir / "README.md",
        "all_cases": output_dir / "all_cases.md",
        "validation_rubric": output_dir / "validation_rubric.md",
        "plausibility_only_packet": output_dir / "plausibility_only_packet.md",
        "clinician_validation_packet": output_dir / "clinician_validation_packet.md",
    }
    files["readme"].write_text(
        _with_trailing_newline(READABLE_INDEX_MD), encoding="utf-8", newline="\n"
    )
    files["all_cases"].write_text(render_all_cases(pages), encoding="utf-8", newline="\n")
    files["validation_rubric"].write_text(
        _with_trailing_newline(VALIDATION_RUBRIC_MD),
        encoding="utf-8",
        newline="\n",
    )
    files["plausibility_only_packet"].write_text(
        render_plausibility_packet(pages), encoding="utf-8", newline="\n"
    )
    files["clinician_validation_packet"].write_text(
        render_investigator_packet(pages, investigator), encoding="utf-8", newline="\n"
    )
    written.update(files)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build human-readable CliniProof validation packets from frozen JSON."
    )
    parser.add_argument("--resident", type=Path, default=DEFAULT_RESIDENT_PATH)
    parser.add_argument("--investigator", type=Path, default=DEFAULT_INVESTIGATOR_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    build_readable_packets(
        resident_path=args.resident,
        investigator_path=args.investigator,
        output_dir=args.output_dir,
    )
    return 0
