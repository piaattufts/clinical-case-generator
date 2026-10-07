# ruff: noqa: E501
"""Evidence-gated Round 2 copies for the six cases with Round 1 feedback.

Copies the recovered clean charts and applies only changes that have a reviewer
item and a source. It does not edit frozen files, the recovered export, or the
other 18 cases.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from docx.document import Document as WordDocument
from docx.shared import RGBColor

from app.services.clinical_revision_items import EVIDENCE_NOTES, LEDGER, REVIEW_ITEMS
from app.services.cycle2_split_casebooks import (
    _banner,
    _bordered_table,
    _chart,
    _round2_form,
)
from app.services.round1_six_case_review import (
    AMBIGUITY,
    completed_reviews,
    write_feedback_files,
)
from app.services.word_controls import finalize_word_form, prepare_form_document
from app.services.word_export import NAVY, _add_body, _add_heading, _new_document, _set_run_font

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "exports" / "clean_balanced_seed_set"
CASE_IDS = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")


def write_revision_package(feedback_dir: Path, case_dir: Path) -> Path:
    """Write the Round 1 extract, the revision record, the six cases, and the codebook."""
    feedback_dir.mkdir(parents=True, exist_ok=True)
    write_feedback_files(feedback_dir)
    (feedback_dir / "CLINICAL_REVISION_LOG.md").write_text(
        _clinical_revision_log(),
        encoding="utf-8",
    )
    (feedback_dir / "REVISION_DIFF.md").write_text(_revision_diff(), encoding="utf-8")
    (feedback_dir / "REVISION_EVIDENCE_LEDGER.md").write_text(_ledger(), encoding="utf-8")
    _evidence_gate()
    case_dir.mkdir(parents=True, exist_ok=True)
    for case_id in CASE_IDS:
        resident, evaluator = _build_case(case_id)
        if "reference_discharge_plan" in resident:
            raise ValueError(f"{case_id} resident chart contains the reference")
        (case_dir / f"{case_id}_resident.json").write_text(
            json.dumps(resident, indent=2) + "\n",
            encoding="utf-8",
        )
        (case_dir / f"{case_id}_evaluator.json").write_text(
            json.dumps(evaluator, indent=2) + "\n",
            encoding="utf-8",
        )
    document_path = _write_codebook(case_dir)
    (case_dir / "README.md").write_text(_readme(), encoding="utf-8")
    (case_dir / "MANIFEST.md").write_text(_manifest(), encoding="utf-8")
    return document_path


def _evidence_gate() -> None:
    """Every concern needs a decision, and every executed change needs evidence."""
    allowed = {
        "REVISED",
        "NOT_CHANGED",
        "SOURCE_SELECTION_AMBIGUITY",
        "NOT_COMPLETED_IN_ROUND_1",
        "REQUIRES_CLINICIAN_DECISION",
    }
    for item in REVIEW_ITEMS:
        if item["status"] not in allowed:
            raise ValueError(item["id"])
        for field in ("comment", "revision", "location", "old", "new", "reasoning", "evidence"):
            if not item[field].strip():
                raise ValueError(f"{item['id']} missing {field}")
        if item["status"] == "REVISED" and "[E" not in item["evidence"]:
            raise ValueError(f"{item['id']} has no evidence id")
    for row in LEDGER:
        if not row["source"] or not row["classification"]:
            raise ValueError(row["case"])


def _build_case(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    resident = json.loads((CLEAN / f"{case_id}_resident.json").read_text(encoding="utf-8"))
    evaluator = json.loads((CLEAN / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
    _NARRATIVE[case_id](resident)
    _NARRATIVE[case_id](evaluator)
    _REFERENCE[case_id](evaluator)
    resident.pop("reference_discharge_plan", None)
    return resident, evaluator


def _set_note(case: dict[str, Any], note_type: str, text: str) -> None:
    for note in case.get("CaseNote") or []:
        if note.get("note_type") == note_type:
            note["note_text"] = text
            return
    raise KeyError(note_type)


def _set_hpi(case: dict[str, Any], text: str) -> None:
    case["ClinicalCase"]["presentation"]["hpi"] = text


def _patch_801(case: dict[str, Any]) -> None:
    _set_hpi(
        case,
        "A 75-year-old Male is admitted with delirium after several days of confusion, "
        "fatigue, and poor oral intake. Mucous membranes are dry. The recorded supine "
        "blood pressure is 136/78 mmHg, and the orthostatic systolic pressure falls "
        "20 mmHg from that supine value. Home medicines are lisinopril, atorvastatin, "
        "metformin, and ibuprofen as needed. He could not give a reliable medication "
        "history at admission. A collateral list was verified later. Glucose is 163 mg/dL "
        "on admission and 103 mg/dL at discharge. Creatinine is 1.1 mg/dL then 1.0 mg/dL.",
    )
    _set_note(
        case,
        "admission",
        "Admission note for a 75-year-old Male with delirium. Poor oral intake, dry "
        "mucous membranes, and a 20 mmHg orthostatic fall from the supine pressure of "
        "136 mmHg are present. Home medicines are lisinopril, atorvastatin, metformin, "
        "and ibuprofen as needed. A collateral medication list was verified after admission.",
    )
    _set_note(
        case,
        "hospital_course",
        "Poor intake and volume depletion were treated with fluids and resumed oral "
        "intake. Confusion cleared as intake improved. Glucose is 163 mg/dL then "
        "103 mg/dL. Creatinine is 1.1 mg/dL then 1.0 mg/dL. Ibuprofen remains available "
        "for symptomatic analgesia. No bleeding and no kidney injury are recorded as a "
        "reason to stop it.",
    )
    for medication in case.get("CaseMedication") or []:
        if "ibuprofen" in str(medication.get("drug")):
            if medication.get("context") == "home":
                medication["status"] = "home"
            elif medication.get("context") == "inpatient":
                medication["status"] = "active"
            medication["held_reason"] = None


def _patch_802(case: dict[str, Any]) -> None:
    _set_hpi(
        case,
        "A 81-year-old Female is admitted with delirium after two days of confusion and "
        "poor oral intake. No other precipitant is recorded. Home medicines are lisinopril "
        "10 mg daily and atorvastatin 40 mg daily. Creatinine is 1.3 mg/dL on admission "
        "and 1.2 mg/dL at discharge. No creatinine from before this admission is recorded. "
        "Blood pressure is 138/69 mmHg then 124/68 mmHg.",
    )
    _set_note(
        case,
        "admission",
        "Admission note for a 81-year-old Female with delirium. Confusion and poor oral "
        "intake for two days. Home medicines are lisinopril and atorvastatin. No earlier "
        "creatinine is recorded.",
    )
    _set_note(
        case,
        "hospital_course",
        "Poor oral intake was the only precipitant recorded. Confusion improved as intake "
        "resumed. Creatinine is 1.3 mg/dL then 1.2 mg/dL. Blood pressure is 138/69 mmHg "
        "then 124/68 mmHg. Atorvastatin 40 mg daily is on the verified home list. No "
        "creatinine from before this admission is recorded.",
    )
    for reconciliation in case.get("CaseMedicationReconciliation") or []:
        reconciliation["notes"] = (
            "A pharmacy fill history was used to verify the home list after admission. "
            "Atorvastatin 40 mg daily is on that list."
        )


def _patch_803(case: dict[str, Any]) -> None:
    addition = (
        " No precipitant for the delirium is recorded. Creatinine is 1.0 mg/dL on "
        "admission and 1.2 mg/dL at discharge. Potassium is 4.4 mmol/L then 4.2 mmol/L. "
        "Hydrochlorothiazide, lisinopril, atorvastatin, and metformin are continued. "
        "No discharge medicine is stopped."
    )
    for note in case.get("CaseNote") or []:
        if note.get("note_type") == "hospital_course":
            text = str(note.get("note_text") or "")
            if "1.2 mg/dL" not in text:
                note["note_text"] = text.rstrip() + addition


def _patch_805(case: dict[str, Any]) -> None:
    course = (
        "Dyspnea, edema, and orthopnea were present for one week. The chest radiograph "
        "shows pulmonary edema without pneumonia. The only recorded furosemide order, at "
        "home and in the hospital, is 40 mg oral once daily. Weight is 81 kg on admission "
        "and 78 kg at discharge. Dry weight is 73 kg. One intake-and-output day is stored, "
        "hospital day 3, with intake 1418 mL, output 2463 mL, and net -1045 mL. Those "
        "weights do not show a return to dry weight. Creatinine is 1.7 mg/dL then "
        "0.9 mg/dL. Potassium is 4.7 mmol/L then 4.3 mmol/L. B-type natriuretic peptide "
        "is 1120 pg/mL then 369 pg/mL. Blood pressure is 109/82 mmHg then 110/84 mmHg. "
        "Oxygen saturation is 92 percent then 98 percent. No echocardiogram and no "
        "ejection fraction are recorded. Metoprolol succinate 25 mg daily is continued."
    )
    _set_note(case, "hospital_course", course)
    _set_hpi(
        case,
        "A 68-year-old Female is admitted with acute systolic heart failure. Dyspnea, "
        "edema, and orthopnea have been present for one week. Home medicines are oral "
        "furosemide 40 mg once daily, atorvastatin, and metoprolol succinate 25 mg once "
        "daily. The inpatient furosemide row is the same oral dose. Discharge weight is "
        "78 kg and the recorded dry weight is 73 kg.",
    )
    _set_note(
        case,
        "admission",
        "Admission note for a 68-year-old Female with acute systolic heart failure. "
        "Symptoms are dyspnea, edema, and orthopnea for one week. Home and inpatient "
        "furosemide are both oral 40 mg once daily. No echocardiogram is recorded.",
    )
    for consult in case.get("CaseConsult") or []:
        if consult.get("service") == "cardiology":
            consult["recommendation"] = (
                "No echocardiogram is recorded. This consultation does not record a "
                "specific medication change."
            )


def _patch_809(case: dict[str, Any]) -> None:
    text = (
        "A 82-year-old Male is admitted with infective endocarditis. The recorded symptom "
        "is fatigue for one week. Temperature is 36.80°C on admission and at discharge. "
        "Home medicines are lisinopril and atorvastatin. Ceftriaxone 2000 mg intravenously "
        "once daily was started during the admission. Transthoracic echocardiogram shows a "
        "mobile echodensity consistent with a vegetation and preserved ventricular function. "
        "Admission blood culture grew gram-positive cocci. A later culture showed no growth. "
        "Creatinine is 1.3 mg/dL on admission and 0.8 mg/dL at discharge. No creatinine "
        "from before this admission is recorded."
    )
    _set_hpi(case, text)
    _set_note(case, "admission", text)
    _set_note(
        case,
        "hospital_course",
        "Ceftriaxone 2000 mg intravenously once daily was given during the admission. "
        "The echocardiogram shows a vegetation with preserved ventricular function. "
        "Blood culture grew gram-positive cocci, and a later culture showed no growth. "
        "Creatinine is 1.3 mg/dL then 0.8 mg/dL. Lisinopril remains on the inpatient "
        "list. No baseline creatinine before this admission is recorded. Temperature "
        "remains 36.80°C.",
    )


def _patch_813(case: dict[str, Any]) -> None:
    case["CaseMedication"] = [
        medication
        for medication in case.get("CaseMedication") or []
        if not (
            medication.get("context") == "home" and "valganciclovir" in str(medication.get("drug"))
        )
    ]
    for medication in case.get("CaseMedication") or []:
        if "valganciclovir" in str(medication.get("drug")):
            medication["notes"] = (
                "Started after the admission viral-load result. Given as 450 MG tablets."
            )
    text = (
        "A 64-year-old Female with a kidney transplant is admitted with diarrhea for "
        "several days. Home medicines are tacrolimus 1 mg every 12 hours, amlodipine "
        "5 mg daily, and atorvastatin 40 mg daily. She was not taking valganciclovir "
        "before admission. The admission viral-load review detected CMV viral burden."
    )
    _set_hpi(case, text)
    _set_note(case, "admission", text)
    _set_note(
        case,
        "hospital_course",
        "The admission viral-load review detected CMV viral burden and supported "
        "antiviral treatment. Valganciclovir 900 mg orally twice daily, given as 450 mg "
        "tablets, was started after that result. A later review showed a lower viral "
        "burden. Tacrolimus 1 mg every 12 hours was continued. Diarrhea improved. "
        "Creatinine is 1.2 mg/dL then 1.0 mg/dL. Potassium is 4.7 mmol/L then 3.9 mmol/L. "
        "No cause for the potassium change is recorded.",
    )
    for consult in case.get("CaseConsult") or []:
        if consult.get("service") == "infectious disease":
            consult["recommendation"] = (
                "Antiviral treatment follows the admission viral-load result."
            )
        elif consult.get("service") == "transplant":
            consult["recommendation"] = (
                "Tacrolimus 1 mg every 12 hours is the recorded immunosuppressant. "
                "No antimetabolite is on the medication list."
            )


_NARRATIVE = {
    "VAL-801": _patch_801,
    "VAL-802": _patch_802,
    "VAL-803": _patch_803,
    "VAL-805": _patch_805,
    "VAL-809": _patch_809,
    "VAL-813": _patch_813,
}


def _set_alternative(
    evaluator: dict[str, Any], medication: str, action: str, rationale: str
) -> None:
    plan = evaluator["reference_discharge_plan"]
    plan["acceptable_alternatives"] = [
        {"medication": medication, "action": action, "rationale": rationale}
    ]


def _reference_801(evaluator: dict[str, Any]) -> None:
    for item in evaluator["reference_discharge_plan"]["medications"]:
        if "ibuprofen" in str(item.get("medication")):
            item["action"] = "continue"
            item["rationale"] = (
                "No stop indication is documented. Creatinine is 1.1 mg/dL then "
                "1.0 mg/dL. The reference continues ibuprofen rather than adding a bleed "
                "or an infection."
            )


def _reference_802(evaluator: dict[str, Any]) -> None:
    _set_alternative(
        evaluator,
        "lisinopril 10 MG Oral Tablet",
        "hold",
        "Hold is acceptable if creatinine 1.3 mg/dL is judged to be acute kidney injury. "
        "No baseline is recorded, so the reference does not require a hold.",
    )


def _reference_803(evaluator: dict[str, Any]) -> None:
    for item in evaluator["reference_discharge_plan"]["medications"]:
        if "lisinopril" in str(item.get("medication")):
            item["duration"] = "30 days"
            item["rationale"] = (
                "The reviewed case shortened this supply to 7 days. The preserved "
                "chart uses 30 days, the same duration as the other discharge "
                "medicines. Creatinine 1.0 mg/dL then 1.2 mg/dL does not change that supply."
            )


def _reference_805(evaluator: dict[str, Any]) -> None:
    for item in evaluator["reference_discharge_plan"]["medications"]:
        if "furosemide" in str(item.get("medication")):
            item["rationale"] = (
                "The recorded order remains 40 mg oral once daily. Discharge weight "
                "is 78 kg and dry weight is 73 kg, so the weights do not show a return "
                "to dry weight. No intravenous dose is stored in the project regimen."
            )
    _set_alternative(
        evaluator,
        "Additional systolic heart-failure therapy (ACE inhibitor, ARNI, SGLT2 inhibitor, or MRA)",
        "start",
        "An additional class is acceptable at discharge and is not required. Admission "
        "creatinine is 1.7 mg/dL and falls to 0.9 mg/dL. No ejection fraction is recorded.",
    )


def _reference_809(evaluator: dict[str, Any]) -> None:
    _set_alternative(
        evaluator,
        "lisinopril 10 MG Oral Tablet",
        "hold",
        "Hold while creatinine is 1.3 mg/dL is acceptable if that value is judged to be "
        "acute kidney injury. No prior baseline is recorded, so the reference continues lisinopril.",
    )


def _reference_813(evaluator: dict[str, Any]) -> None:
    for item in evaluator["reference_discharge_plan"]["medications"]:
        if "valganciclovir" in str(item.get("medication")):
            item["action"] = "start"
            item["rationale"] = (
                "Start 900 mg orally twice daily after the admission viral-load result. "
                "The 450 mg tablet is the product strength. Creatinine is 1.2 mg/dL then "
                "1.0 mg/dL, and the project regimen does not reduce this dose in that range."
            )
    _set_alternative(
        evaluator,
        "BX Rating tacrolimus 1 MG Oral Capsule",
        "modify",
        "A temporary reduction is acceptable if the transplant service documents one. "
        "No trough and no reduction are recorded, so the reference continues 1 mg every 12 hours.",
    )


_REFERENCE = {
    "VAL-801": _reference_801,
    "VAL-802": _reference_802,
    "VAL-803": _reference_803,
    "VAL-805": _reference_805,
    "VAL-809": _reference_809,
    "VAL-813": _reference_813,
}


def _cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ")


def _clinical_revision_log() -> str:
    lines = [
        "# Clinical revision log",
        "",
        "Each row is one clinical concern from the completed Round 1 review. "
        "The reasoning states why the original representation was or was not changed.",
        "",
        "| ID | Reviewer comment / finding | Revision | Location in case | Old representation | New representation | Clinical reasoning | Evidence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in REVIEW_ITEMS:
        cells = [
            item["id"],
            item["comment"],
            item["revision"],
            item["location"],
            item["old"],
            item["new"],
            item["reasoning"],
            item["evidence"] + " " + item["status"],
        ]
        lines.append("| " + " | ".join(_cell(cell) for cell in cells) + " |")
    lines.append("")
    return "\n".join(lines)


def _revision_diff() -> str:
    lines = [
        "# Revision diff",
        "",
        "Executed changes only. Items with no change in the represented fact are in the clinical revision log.",
        "",
        "| Case | Location | Old | New | Comment addressed | Clinical reasoning | Evidence |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in REVIEW_ITEMS:
        if item["status"] not in {"REVISED", "REQUIRES_CLINICIAN_DECISION"}:
            continue
        if item["old"] == item["new"]:
            continue
        cells = [
            item["case"],
            item["location"],
            item["old"],
            item["new"],
            item["comment"],
            item["reasoning"],
            item["evidence"],
        ]
        lines.append("| " + " | ".join(_cell(cell) for cell in cells) + " |")
    lines.append("")
    return "\n".join(lines)


def _ledger() -> str:
    lines = [
        "# Revision evidence ledger",
        "",
        "Literature supports a clinical relationship. It is not used as a measurement that was absent from the chart. "
        "A synthetic finding is labeled as such.",
        "",
        "| Case | Change | Old representation | New representation | Source | Classification |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in LEDGER:
        cells = [
            row["case"],
            row["change"],
            row["old"],
            row["new"],
            row["source"],
            row["classification"],
        ]
        lines.append("| " + " | ".join(_cell(cell) for cell in cells) + " |")
    lines.extend(["", "## Evidence notes", ""])
    for key, text in EVIDENCE_NOTES.items():
        lines.append(f"{key} {text}")
        lines.append("")
    return "\n".join(lines)


def _write_codebook(directory: Path) -> Path:
    document = _new_document("CliniProof Cycle 2  |  Set 1 revised cases, version 2")
    prepare_form_document(document)
    _add_heading(document, "CliniProof", 0)
    _add_body(document, "Clinical Revision Round 2, version 2")
    _add_heading(document, "SET 1", 1)
    _add_heading(document, "REVISED CASES FOLLOWING ROUND 1 CLINICIAN FEEDBACK", 2)
    _add_body(document, "Cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, VAL-813")
    _add_body(
        document,
        "Complete the blank Round 2 form before you read the historical Round 1 record "
        "or the clinical revision record. This file contains the six cases that received "
        "Round 1 feedback. The other eighteen cases are not in this file. Ready for "
        "clinician review does not mean clinically validated.",
    )
    reviews = completed_reviews()
    for case_id in CASE_IDS:
        resident, evaluator = _build_case(case_id)
        row = {"case_id": case_id, "resident": resident, "evaluator": evaluator}
        banner = document.add_paragraph()
        banner.paragraph_format.page_break_before = True
        banner.paragraph_format.keep_with_next = True
        _set_run_font(banner.add_run(f"CASE {case_id}"), size=16, bold=True, color=NAVY)
        _add_body(document, "Round 2 revised case, version 2")
        _add_heading(document, "CURRENT ROUND 2 CASE", 2)
        _chart(document, resident)
        _round2_form(document, row)
        _historical_section(document, reviews[case_id])
        _response_section(document, case_id)
    path = directory / "CliniProof_Cycle2_Revised_Cases_Validation.docx"
    document.save(str(path))
    finalize_word_form(path)
    return path


def _historical_section(document: WordDocument, review: dict[str, Any]) -> None:
    heading = document.add_paragraph()
    heading.paragraph_format.page_break_before = True
    heading.paragraph_format.keep_with_next = True
    _set_run_font(
        heading.add_run("ROUND 1 CLINICIAN FEEDBACK — HISTORICAL RECORD"),
        size=14,
        bold=True,
        color=NAVY,
    )
    _banner(
        document,
        "ROUND 1 CLINICIAN FEEDBACK — READ ONLY",
        fill="595959",
        font_color=RGBColor(0xFF, 0xFF, 0xFF),
    )
    _add_body(
        document,
        "This section reproduces the completed Round 1 form. Boxes are not editable. "
        "Blank items stay blank. If two boxes were selected, both are shown.",
    )
    rows = []
    for domain in review["c1"]["domains"]:
        marks = tuple("☒" if domain["scores"][str(score)] else "☐" for score in (1, 2, 3, 4))
        label = domain["domain"]
        if AMBIGUITY in domain["flags"]:
            label += " — source selected more than one score"
        rows.append((label, *marks))
    _bordered_table(
        document,
        ("Domain", "1", "2", "3", "4"),
        tuple(rows),
        (3.6, 0.8, 0.8, 0.8, 0.8),
        header=True,
        fill="F2F2F2",
    )
    _add_body(document, "C1 overall: " + _selection_line(review["c1"]["overall"], ("pass", "fail")))
    _quote(document, "C1 comments", review["c1"]["comment"])
    _add_body(document, "C2 question: " + review["c2"]["question"])
    _add_body(document, "C2: " + _selection_line(review["c2"]["selection"], ("pass", "fail")))
    _quote(document, "C2 comments", review["c2"]["comment"])
    _add_body(document, "C3 question: " + review["c3"]["question"])
    _add_body(document, "C3: " + _selection_line(review["c3"]["selection"], ("pass", "fail")))
    _quote(document, "C3 comments", review["c3"]["comment"])
    _add_body(document, "C4 question: " + review["c4"]["question"])
    _add_body(document, "C4: " + _selection_line(review["c4"]["selection"], ("pass", "fail")))
    _add_body(
        document,
        "C4 issue: " + (review["c4"]["medication_or_clinical_issue"] or "NOT COMPLETED IN ROUND 1"),
    )
    _add_body(
        document,
        "C4 location: " + (review["c4"]["where_it_appears"] or "NOT COMPLETED IN ROUND 1"),
    )
    _add_body(
        document,
        "C4 clinical meaning: "
        + (review["c4"]["why_clinically_meaningful"] or "NOT COMPLETED IN ROUND 1"),
    )
    _quote(document, "C4 comments", review["c4"]["comment"])
    _add_body(
        document,
        "C5: "
        + _selection_line(
            review["c5"]["selection"],
            ("easy", "moderate", "hard", "inappropriate_or_outlier"),
        ),
    )
    _quote(document, "C5 comments", review["c5"]["comment"])
    _add_body(
        document,
        "Overall recommendation: "
        + _selection_line(
            review["overall_recommendation"]["selection"],
            ("accept", "revise", "exclude"),
        ),
    )
    _quote(document, "Overall comments", review["overall_recommendation"]["comment"])
    reviewer = review["overall_recommendation"]["reviewer_code"] or "NOT COMPLETED IN ROUND 1"
    dated = review["overall_recommendation"]["date"] or "NOT COMPLETED IN ROUND 1"
    _add_body(document, f"Reviewer: {reviewer}. Date: {dated}.")


_SELECTION_LABELS = {
    "pass": "Pass",
    "fail": "Fail",
    "easy": "Easy",
    "moderate": "Moderate",
    "hard": "Hard",
    "inappropriate_or_outlier": "Inappropriate / outlier",
    "accept": "Accept",
    "revise": "Revise",
    "exclude": "Exclude",
}


def _selection_line(selection: dict[str, Any], names: tuple[str, ...]) -> str:
    if selection.get("pass") is None and "accept" not in selection and "easy" not in selection:
        return "NOT COMPLETED IN ROUND 1"
    chosen = [_SELECTION_LABELS[name] for name in names if selection.get(name)]
    if not chosen:
        return "NOT COMPLETED IN ROUND 1"
    text = ", ".join(chosen)
    if AMBIGUITY in selection.get("flags", []):
        text += ". Source document contains multiple selected responses; reproduced exactly."
    return text


def _quote(document: WordDocument, label: str, comment: str | None) -> None:
    _bordered_table(
        document,
        (label,),
        ((comment or "NOT COMPLETED IN ROUND 1",),),
        (6.8,),
        header=True,
        fill="F2F2F2",
    )


def _response_section(document: WordDocument, case_id: str) -> None:
    heading = document.add_paragraph()
    heading.paragraph_format.page_break_before = True
    heading.paragraph_format.keep_with_next = True
    _set_run_font(
        heading.add_run("CLINICAL REVISION RECORD"),
        size=14,
        bold=True,
        color=NAVY,
    )
    rows = tuple(
        (
            item["comment"],
            item["revision"],
            item["location"].replace("_", " ").replace("; ", "\n"),
            item["old"],
            item["new"],
            item["reasoning"] + " " + item["evidence"],
        )
        for item in REVIEW_ITEMS
        if item["case"] == case_id
    )
    _bordered_table(
        document,
        (
            "Round 1 comment",
            "Revision made",
            "Where the revision was made",
            "Old representation",
            "New representation",
            "Clinical reasoning and supporting evidence",
        ),
        rows,
        (1.15, 1.05, 0.95, 1.15, 1.15, 1.35),
        header=True,
        size=8,
    )
    _add_heading(document, "Evidence", 3)
    for key, text in EVIDENCE_NOTES.items():
        cited = any(
            key in item["evidence"] or key in item["reasoning"]
            for item in REVIEW_ITEMS
            if item["case"] == case_id
        )
        cited = cited or any(key in row["source"] for row in LEDGER if row["case"] == case_id)
        if cited:
            _add_body(document, f"{key} {text}")


def _readme() -> str:
    return "\n".join(
        [
            "# Set 1 revised cases, version 2",
            "",
            "Open [CliniProof_Cycle2_Revised_Cases_Validation.docx]"
            "(CliniProof_Cycle2_Revised_Cases_Validation.docx).",
            "",
            "This version contains VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and "
            "VAL-813 only. It does not replace the eighteen Set 2 cases, which remain under internal revision.",
            "",
            "Round 1 comments are reproduced after the blank Round 2 form. The clinical "
            "revision record follows that historical record. The revision log, the "
            "field-level diff, and the evidence ledger are in this directory.",
            "",
            "Ready for clinician review does not mean clinically validated.",
            "",
        ]
    )


def _manifest() -> str:
    lines = [
        "# Set 1 version 2 manifest",
        "",
        "| Case | Resident file | Evaluator file |",
        "| --- | --- | --- |",
    ]
    for case_id in CASE_IDS:
        lines.append(f"| {case_id} | `{case_id}_resident.json` | `{case_id}_evaluator.json` |")
    lines.append("")
    return "\n".join(lines)
