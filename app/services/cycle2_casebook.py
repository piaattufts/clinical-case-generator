"""Blank Cycle 2 clinician-validation casebook for VAL-801–VAL-824.

Reads the existing revised and clean-review exports. It does not regenerate
cases and does not write resident or evaluator JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from docx import Document

from app.services.word_controls import (
    append_checkbox,
    append_rich_text_field,
    finalize_word_form,
    prepare_form_document,
)

ROOT = Path(__file__).resolve().parents[2]
REVISED_DIR = ROOT / "exports" / "ko_revised_cases_v1"
CLEAN_DIR = ROOT / "exports" / "ko_clean_cases_for_review_v1"
REVISED_IDS = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")
CASE_IDS = tuple(f"VAL-{number}" for number in range(801, 825))

SPECIAL_QUESTIONS = {
    "VAL-805": (
        "Which additional HFrEF therapies should be required versus acceptable "
        "alternatives, given ejection fraction 30 percent, discharge systolic "
        "pressure 110 mmHg, creatinine 0.9 mg/dL, and potassium 4.3 mmol/L?"
    ),
    "VAL-806": (
        "Restart lisinopril versus continued hold, given creatinine 2.8 mg/dL "
        "falling to 1.6 mg/dL without a known baseline?"
    ),
    "VAL-813": (
        "Continue versus modify or temporarily hold mycophenolate, given the "
        "CMV disease and transplant context?"
    ),
    "VAL-814": "Restart versus continued hold of mycophenolate?",
    "VAL-820": (
        "Is enoxaparin VTE prophylaxis appropriate during concurrent warfarin "
        "therapy with the documented INR values?"
    ),
    "VAL-821": (
        "Restart apixaban at discharge versus continued hold pending "
        "gastroenterology follow-up?"
    ),
}


def write_cycle2_final_validation(directory: Path) -> Path:
    """Write the blank 24-case Word form, its README, and its manifest."""
    directory.mkdir(parents=True, exist_ok=True)
    rows = [_load(case_id) for case_id in CASE_IDS]
    document = Document()
    prepare_form_document(document)
    document.add_heading("CliniProof Cycle 2 clinician validation", 0)
    document.add_paragraph(
        "These 24 charts are clean cases ready for clinician review. "
        "Ready for clinician review does not mean clinically validated."
    )
    document.add_paragraph(
        "Read the resident-facing chart and answer C1 and C2 before the "
        "clinician validation reference. That reference is not shown to residents."
    )
    document.add_paragraph(
        "Historical validation design: the older error-injection casebooks are "
        "not this review package. All boxes below start blank."
    )
    for row in rows:
        _add_case(document, row)
    path = directory / "CliniProof_Cycle2_Final_Validation.docx"
    document.save(str(path))
    finalize_word_form(path)
    (directory / "README.md").write_text(_readme(), encoding="utf-8")
    (directory / "MANIFEST.md").write_text(_manifest(rows), encoding="utf-8")
    return path


def _load(case_id: str) -> dict[str, Any]:
    folder = REVISED_DIR if case_id in REVISED_IDS else CLEAN_DIR
    resident = json.loads((folder / f"{case_id}_resident.json").read_text(encoding="utf-8"))
    evaluator = json.loads((folder / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
    if "reference_discharge_plan" in resident:
        raise ValueError(f"{case_id} resident file contains the hidden reference")
    return {
        "case_id": case_id,
        "group": "revised" if case_id in REVISED_IDS else "internal revision",
        "folder": folder.name,
        "resident": resident,
        "evaluator": evaluator,
    }


def _add_case(document: Any, row: dict[str, Any]) -> None:
    case_id = row["case_id"]
    chart = row["resident"]
    clinical = chart["ClinicalCase"]
    document.add_heading(f"CASE {case_id}", 1)
    document.add_paragraph(clinical.get("one_liner") or "")
    document.add_heading("Resident-facing chart", 2)
    _chart(document, chart)
    document.add_heading("C1 — Clinical plausibility", 2)
    document.add_paragraph(
        "1 = implausible; 2 = substantial revision required; "
        "3 = plausible with minor concern; 4 = fully plausible."
    )
    for domain in (
        "presentation and demographics",
        "fit between presentation and diagnosis",
        "vital signs",
        "laboratory findings",
        "medication regimen",
        "hospital course",
        "chart consistency",
        "discharge context and follow-up",
    ):
        _choices(document, case_id, f"c1-{domain}", domain, ("1", "2", "3", "4"))
    _choices(document, case_id, "c1-overall", "C1 overall", ("Pass", "Fail"))
    document.add_heading("C2 — Sufficiency for resident decision-making", 2)
    document.add_paragraph(
        "Does the resident-facing chart contain enough clinical information for an "
        "internal-medicine resident to independently determine an appropriate "
        "discharge medication regimen?"
    )
    _choices(document, case_id, "c2", "C2", ("Pass", "Fail"))
    _comment(document, case_id, "c2-comment", "C2 comment")
    document.add_heading("CLINICIAN VALIDATION REFERENCE", 2)
    document.add_paragraph("Not shown to residents in the assessment study.")
    document.add_paragraph("Complete C1 and C2 before using this reference.")
    reference = row["evaluator"]["reference_discharge_plan"]
    for item in reference.get("medications") or []:
        document.add_paragraph(
            f"{item.get('action')}: {item.get('medication')} {item.get('dose')} "
            f"{item.get('route')} {item.get('frequency')}. "
            f"Indication: {item.get('indication')}. Rationale: {item.get('rationale')}.",
            style="List Bullet",
        )
    for item in reference.get("acceptable_alternatives") or []:
        document.add_paragraph(
            f"Acceptable alternative already recorded: {item.get('action')} "
            f"{item.get('medication')}. {item.get('rationale')}",
            style="List Bullet",
        )
    question = SPECIAL_QUESTIONS.get(case_id)
    if question:
        document.add_heading("Case-specific adjudication", 3)
        document.add_paragraph(question)
        _comment(document, case_id, "adjudication", "Case-specific adjudication")
    document.add_heading("C3 — Reference-plan validity", 2)
    document.add_paragraph(
        "Is the hidden reference discharge medication plan clinically defensible?"
    )
    _choices(document, case_id, "c3", "C3", ("Pass", "Fail"))
    _comment(
        document,
        case_id,
        "c3-dispute",
        "Disputed medication, current action, suggested action, and reason",
    )
    document.add_heading("C4 — Acceptable alternatives", 2)
    document.add_paragraph(
        "Could another discharge medication decision also reasonably be correct?"
    )
    _choices(document, case_id, "c4", "C4", ("No", "Yes"))
    _comment(document, case_id, "c4-alt-1", "Alternative 1: medication, action, and rationale")
    _comment(document, case_id, "c4-alt-2", "Alternative 2: medication, action, and rationale")
    document.add_heading("C5 — Missing, misleading, or competing issues", 2)
    document.add_paragraph(
        "Does the chart contain another clinically meaningful issue that could "
        "change the expected discharge plan?"
    )
    _choices(document, case_id, "c5-issue", "C5 competing issue", ("No", "Yes"))
    document.add_paragraph("Does any wording reveal the intended answer?")
    _choices(document, case_id, "c5-leak", "C5 answer reveal", ("No", "Yes"))
    _comment(document, case_id, "c5-comment", "C5 comment")
    document.add_heading("C6 — Expected learner difficulty", 2)
    _choices(
        document,
        case_id,
        "c6",
        "C6",
        ("Easy", "Moderate", "Hard", "Inappropriate or outlier"),
    )
    document.add_heading("Overall recommendation", 2)
    _choices(document, case_id, "overall", "Overall", ("Accept", "Revise", "Exclude"))
    _comment(document, case_id, "overall-comment", "Comments")


def _chart(document: Any, chart: dict[str, Any]) -> None:
    clinical = chart["ClinicalCase"]
    presentation = clinical.get("presentation") or {}
    document.add_paragraph(presentation.get("hpi") or "")
    document.add_paragraph(
        "Diagnoses: "
        + "; ".join(item.get("diagnosis") or "" for item in chart.get("CaseDiagnosis") or [])
    )
    for note in chart.get("CaseNote") or []:
        document.add_paragraph(f"{note.get('note_type')}: {note.get('note_text')}")
    document.add_paragraph("Home and inpatient medications:")
    for med in chart.get("CaseMedication") or []:
        document.add_paragraph(
            f"{med.get('context')}: {med.get('drug')} {med.get('dose')} "
            f"{med.get('route')} {med.get('frequency')}. "
            f"Indication: {med.get('indication') or 'none'}. "
            f"Held reason: {med.get('held_reason') or 'none'}.",
            style="List Bullet",
        )
    document.add_paragraph("Vital signs:")
    for vital in chart.get("CaseVital") or []:
        document.add_paragraph(
            f"{vital.get('timepoint')}: blood pressure {vital.get('bp_systolic')}/"
            f"{vital.get('bp_diastolic')}, heart rate {vital.get('heart_rate')}, "
            f"temperature {vital.get('temp_c')}, "
            f"oxygen saturation {vital.get('spo2_percent')}.",
            style="List Bullet",
        )
    document.add_paragraph("Laboratories:")
    for lab in chart.get("CaseLab") or []:
        document.add_paragraph(
            f"{lab.get('timepoint')}: {lab.get('test_name')} {lab.get('value')} {lab.get('unit')}.",
            style="List Bullet",
        )
    if chart.get("CaseWeight"):
        document.add_paragraph("Weights:")
        for weight in chart["CaseWeight"]:
            dry = weight.get("dry_weight_kg")
            suffix = f", dry weight {dry} kg" if dry else ""
            document.add_paragraph(
                f"{weight.get('timepoint')}: {weight.get('weight_kg')} kg{suffix}.",
                style="List Bullet",
            )
    if chart.get("CaseIntakeOutput"):
        document.add_paragraph("Intake and output:")
        for item in chart["CaseIntakeOutput"]:
            document.add_paragraph(
                f"{item.get('timepoint')}: intake {item.get('intake_ml')} mL, "
                f"output {item.get('output_ml')} mL, net {item.get('net_ml')} mL.",
                style="List Bullet",
            )
    for imaging in chart.get("CaseImaging") or []:
        document.add_paragraph(f"Imaging, {imaging.get('study_type')}: {imaging.get('finding')}")
    for consult in chart.get("CaseConsult") or []:
        document.add_paragraph(
            f"Consult, {consult.get('service')}: {consult.get('assessment')} "
            f"{consult.get('recommendation')}"
        )
    for procedure in chart.get("CaseProcedure") or []:
        document.add_paragraph(
            f"Procedure: {procedure.get('procedure_name')}. {procedure.get('findings') or ''}"
        )
    for item in chart.get("CaseFollowup") or []:
        document.add_paragraph(
            f"Follow-up: {item.get('item')} in {item.get('timing')} "
            f"with {item.get('with_service')}."
        )


def _choices(document: Any, case_id: str, code: str, label: str, choices: tuple[str, ...]) -> None:
    paragraph = document.add_paragraph(f"{label}: ")
    for choice in choices:
        paragraph.add_run(choice + " ")
        append_checkbox(
            paragraph,
            document,
            tag=f"{case_id}-{code}-{choice}",
            alias=f"{case_id} {code} {choice}",
        )


def _comment(document: Any, case_id: str, tag: str, label: str) -> None:
    document.add_paragraph(label)
    table = document.add_table(rows=1, cols=1)
    append_rich_text_field(
        table.cell(0, 0),
        document,
        tag=f"{case_id}-{tag}",
        alias=label,
        lines=3,
    )


def _readme() -> str:
    return "\n".join(
        [
            "# Cycle 2 combined casebook",
            "",
            "Combined investigator convenience copy. Not a clinician review assignment.",
            "",
            "Clinicians should review [Set 1, version 3]"
            "(../ko_cycle2_revised_validation_v3/"
            "CliniProof_Cycle2_Revised_Cases_Validation.docx) only. "
            "[Set 2](../ko_cycle2_clean_validation/"
            "CliniProof_Cycle2_Clean_Cases_Validation.docx) is still under "
            "internal correction and is not yet ready for clinician review.",
            "",
            "This file keeps all 24 cases in one document for investigators who want "
            "a single convenience copy. It is not a clinician review assignment.",
            "",
            "Open [CliniProof_Cycle2_Final_Validation.docx]"
            "(CliniProof_Cycle2_Final_Validation.docx) in desktop Microsoft Word.",
            "The checkboxes start blank. Ready for clinician review does not mean "
            "clinically validated.",
            "",
            "Each case shows the resident-facing chart, then C1 and C2, then the hidden "
            "reference, then C3 through C6 and Accept, Revise, or Exclude.",
            "",
            "The older error-injection casebooks are historical validation design. "
            "Do not use them as this review package.",
            "",
            "The cases were not regenerated. Archived pre-injection charts were the source. "
            "Original frozen VAL files are unchanged. These files are separate review artifacts.",
            "",
        ]
    )


def _manifest(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Cycle 2 validation manifest",
        "",
        "Each VAL-801–VAL-824 identifier appears once. None of these cases is "
        "clinically validated.",
        "",
        "| Case | Review group | Resident file | Evaluator file |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        case_id = row["case_id"]
        folder = row["folder"]
        lines.append(
            f"| {case_id} | {row['group']} | "
            f"`exports/{folder}/{case_id}_resident.json` | "
            f"`exports/{folder}/{case_id}_evaluator.json` |"
        )
    lines.extend(
        [
            "",
            "Case-specific adjudication questions are included for VAL-805, VAL-806, "
            "VAL-813, VAL-814, VAL-820, and VAL-821.",
            "",
        ]
    )
    return "\n".join(lines)
