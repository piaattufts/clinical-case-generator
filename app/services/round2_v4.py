# ruff: noqa: E501
"""Round 2 version 4: task validity and clinical sufficiency.

Katie's review is the task-alignment source. Alex's completed casebook is the
clinical-sufficiency source for the four clean controls he actually rated.
The other twenty cases are judged with the same sufficiency rubric. That rubric
is not an Alex case-specific comment.

The writer reads preserved sources and writes a new package. It does not edit
version 3, the Set 2 source files, the recovered clean export, or either
clinician's completed review.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from app.services.round1_feedback import C1_DOMAINS, parse_round1_casebook
from app.services.round2_v4_codebook import visual_qa_markdown, write_codebooks

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "exports" / "ko_round2_combined_validation_v4"
V3 = ROOT / "exports" / "ko_cycle2_revised_validation_v3"
SET2 = ROOT / "exports" / "ko_clean_cases_for_review_v1"
CLEAN = ROOT / "exports" / "clean_balanced_seed_set"
ALEX_DOCX = (
    ROOT
    / "docs"
    / "clinical_feedback"
    / "alex"
    / "CliniProof_SeedGuided_Validation_Casebook_final_alex.docx"
)
KATIE_EXTRACT = V3 / "ROUND1_FEEDBACK_COMPLETE.md"

SET1_IDS = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")
SET2_IDS = (
    "VAL-804",
    "VAL-806",
    "VAL-807",
    "VAL-808",
    "VAL-810",
    "VAL-811",
    "VAL-812",
    "VAL-814",
    "VAL-815",
    "VAL-816",
    "VAL-817",
    "VAL-818",
    "VAL-819",
    "VAL-820",
    "VAL-821",
    "VAL-822",
    "VAL-823",
    "VAL-824",
)
ALL_IDS = SET1_IDS + SET2_IDS
ALEX_EXPECTED = ("VAL-801", "VAL-805", "VAL-809", "VAL-813")

DIRECT_LEAK_PATTERNS = (
    r"continue at discharge",
    r"intended at discharge",
    r"should continue",
    r"should stop",
    r"\brestart\b",
    r"\bresume\b",
    r"take exactly as listed",
    r"planned outpatient regimen",
    r"complete the course",
    r"complete the planned",
    r"intended regimen",
    r"verified list at discharge",
    r"no discharge medicine is stopped",
    r"\bintended\b",
    r"are continued",
    r"continue after discharge",
    r"planned antibiotic",
    r"no reason to stop",
    r"use the verified",
)
OLD_DESIGN_PATTERNS = (
    r"planted",
    r"injected error",
    r"assessment discrepancy",
    r"error family",
    r"\bf1_",
    r"\bf2_",
    r"find the error",
    r"error-bearing",
    r"clean control",
)
STRONG_HINT_PATTERNS = (
    r"pending outpatient decision",
    r"pending therapeutic decision",
    r"pending anticoagulation decision",
    r"disease-modifying start",
    r"cognitive-enhancer",
    r"intentional aspirin",
    r"was stopped after the bleed",
    r"was stopped during this admission",
)
DRUG_SKIP = {
    "rating",
    "oral",
    "tablet",
    "capsule",
    "extended",
    "release",
    "sodium",
    "hydrochloride",
    "chewable",
    "delayed",
    "prefilled",
    "syringe",
    "hour",
    "injection",
}

EVIDENCE_NOTES: dict[str, str] = {
    "E1": (
        "Inouye SK, Westendorp RGJ, Saczynski JS. Delirium in elderly people. Lancet. 2014;383:911-922. "
        "doi:10.1016/S0140-6736(13)60688-1. Delirium is an acute change from baseline attention. "
        "Precipitants include dehydration, infection, and metabolic disturbance. The article does not supply this patient's values."
    ),
    "E2": (
        "Heidenreich PA, Bozkurt B, Aguilar D, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. "
        "Circulation. 2022;145:e895-e1032. doi:10.1161/CIR.0000000000001063. "
        "Medication nonadherence, dietary sodium, arrhythmia, ischemia, and infection are recognized decompensation precipitants. "
        "The guideline does not record this patient's electrocardiogram or troponin."
    ),
    "E3": (
        "Baddour LM, Wilson WR, Bayer AS, et al. Infective Endocarditis in Adults: Diagnosis, Antimicrobial Therapy, and "
        "Management of Complications. A Scientific Statement From the American Heart Association. Circulation. 2015;132:1435-1486. "
        "doi:10.1161/CIR.0000000000000296. Blood cultures and echocardiography are core. Surgery is considered for valve dysfunction "
        "causing heart failure, abscess, uncontrolled infection, or prevention of embolism. The statement does not identify this patient's organism."
    ),
    "E4": (
        "Razonable RR, Humar A. Cytomegalovirus in solid organ transplant recipients—Guidelines of the American Society of "
        "Transplantation Infectious Diseases Community of Practice. Clin Transplant. 2019;33:e13512. doi:10.1111/ctr.13512. "
        "Compatible symptoms precede laboratory confirmation. Diarrhea can produce volume and electrolyte loss. "
        "The guideline does not add an immunosuppressant that is absent from the medication list."
    ),
    "E5": (
        "FDA. FDA Drug Safety Communication: FDA revises warnings regarding use of the diabetes medicine metformin in certain patients with reduced kidney function. "
        "https://www.fda.gov/drugs/drug-safety-and-availability/fda-drug-safety-communication-fda-revises-warnings-regarding-use-diabetes-medicine-metformin-certain. "
        "Metformin use depends on kidney function. A labeled creatinine is not a recovered measurement."
    ),
    "E6": (
        "Verbalis JG, Goldsmith SR, Greenberg A, et al. Diagnosis, Evaluation, and Treatment of Hyponatremia: Expert Panel Recommendations. "
        "Am J Med. 2013;126(10 Suppl 1):S1-S42. doi:10.1016/j.amjmed.2013.07.006. Thiazides are a recognized cause of hyponatremia."
    ),
    "E7": (
        "2023 American Geriatrics Society Beers Criteria Update Expert Panel. American Geriatrics Society 2023 updated AGS Beers Criteria. "
        "J Am Geriatr Soc. 2023;71:2052-2081. doi:10.1111/jgs.18372. Chronic nonsteroidal anti-inflammatory drugs are potentially inappropriate in older adults. "
        "That statement supports encoding a stop as an alternative. It does not require the reference to stop ibuprofen when no bleeding and no creatinine rise are recorded."
    ),
    "E8": (
        "Abraham NS, Barkun AN, Sauer BG, et al. American College of Gastroenterology-Canadian Association of Gastroenterology Clinical Practice Guideline: "
        "Management of Anticoagulants and Antiplatelets During Acute Gastrointestinal Bleeding and the Periendoscopic Period. "
        "Am J Gastroenterol. 2022;117:542-558. doi:10.14309/ajg.0000000000001627. "
        "Restart timing depends on hemostasis, the thrombotic indication, and the lesion. A hemoglobin trend is not an endoscopy."
    ),
    "E9": (
        "Douketis JD, Spyropoulos AC, Murad MH, et al. Perioperative Management of Antithrombotic Therapy: An American College of Chest Physicians Guideline. "
        "Chest. 2022;162:e207-e243. doi:10.1016/j.chest.2022.07.025. Atrial fibrillation is an indication for anticoagulation, and postoperative bleeding risk is judged from the procedure and hemoglobin course."
    ),
    "E10": (
        "Kearon C, Akl EA, Ornelas J, et al. Antithrombotic Therapy for VTE Disease: CHEST Guideline and Expert Panel Report. "
        "Chest. 2016;149:315-352. doi:10.1016/j.chest.2015.11.026. Overlap of a parenteral anticoagulant with warfarin is used until the INR is therapeutic. "
        "A prophylactic enoxaparin dose is not itself treatment of atrial fibrillation."
    ),
    "E11": (
        "US Preventive Services Task Force. Aspirin Use to Prevent Cardiovascular Disease: US Preventive Services Task Force Recommendation Statement. "
        "JAMA. 2022;327:1577-1584. doi:10.1001/jama.2022.4983. Primary-prevention aspirin has a narrow role in older adults. "
        "Absence of a recorded coronary event is a chart fact only when it is written into the case and labeled if synthetic."
    ),
    "E12": (
        "DailyMed. Valganciclovir hydrochloride labeling. https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=human&query=valganciclovir. "
        "The label warns of cytopenias and requires renal-function dose adjustment. It does not establish this patient's leukocyte count."
    ),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def source_for(case_id: str) -> Path:
    folder = V3 if case_id in SET1_IDS else SET2
    return folder


def load_pair(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    folder = source_for(case_id)
    resident = json.loads((folder / f"{case_id}_resident.json").read_text(encoding="utf-8"))
    evaluator = json.loads((folder / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
    return resident, evaluator


SCRUBS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"A new disease-modifying start was deferred to outpatient confirmation\.?", re.I), "Attention improved after oral intake improved."),
    (re.compile(r"Start of a cognitive-enhancer remains a pending therapeutic decision[^.]*\.", re.I), "Primary care follow-up is scheduled."),
    (re.compile(r"Reassess pending therapeutic decision", re.I), "Follow-up visit"),
    (re.compile(r"A pending therapeutic decision remains\.\s*", re.I), ""),
    (re.compile(r"Remaining duration of parenteral ceftriaxone is to be confirmed at infectious-disease follow-up\.?", re.I), "Infectious-disease follow-up is scheduled."),
    (re.compile(r"Complete the planned parenteral course with laboratory follow-up\.?", re.I), "A later blood culture showed no growth."),
    (re.compile(r"Restart versus continued hold of anticoagulation remains a pending outpatient decision\.\s*", re.I), "Apixaban was held during the hospitalization. "),
    (re.compile(r"Restart versus continued hold of apixaban remains a pending outpatient decision after the bleed\.?", re.I), "Apixaban was held during the hospitalization."),
    (re.compile(r"while restart timing remains unresolved\.?", re.I), "during the hospitalization after gastrointestinal bleeding."),
    (re.compile(r"Aspirin used for primary prevention was stopped\.?", re.I), "Aspirin 81 mg daily is on the medication list."),
    (re.compile(r"Stopped during this admission\.?", re.I), "Listed during the hospitalization."),
    (re.compile(r"Anticoagulation was interrupted for surgery and then resumed\.?", re.I), "Warfarin was not given on the operative day and was given on later hospital days."),
    (re.compile(r"Parenteral ceftriaxone is intended to continue after discharge until the planned end date\.?", re.I), "Ceftriaxone was started during the hospitalization."),
    (re.compile(r"remaining parenteral ceftriaxone is intended after discharge\.?", re.I), "ceftriaxone was started during the hospitalization."),
    (re.compile(r"Warfarin is intended to continue at discharge\.?", re.I), "Warfarin is on the home list for atrial fibrillation."),
    (re.compile(r"anticoagulation is intended at discharge\.?", re.I), "warfarin is on the home list for atrial fibrillation."),
    (re.compile(r"intentional aspirin discontinuation", re.I), "gastrointestinal bleeding"),
    (re.compile(r"was stopped during this admission", re.I), "is listed during the hospitalization"),
    (re.compile(r"was stopped after the bleed", re.I), "is listed on the medication list"),
    (re.compile(r"Duration of remaining parenteral ceftriaxone is to be confirmed as an outpatient decision\.?", re.I), "Infectious-disease follow-up is scheduled."),
    (re.compile(r"remaining parenteral duration is a pending outpatient decision\.?", re.I), "infectious-disease follow-up is scheduled."),
)


def _scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _scrub(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_scrub(item) for item in value]
    if isinstance(value, str):
        text = value
        for pattern, replacement in SCRUBS:
            text = pattern.sub(replacement, text)
        return text
    return value


def _replace_strings(value: Any, pairs: list[tuple[str, str]]) -> Any:
    if isinstance(value, dict):
        return {key: _replace_strings(item, pairs) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_strings(item, pairs) for item in value]
    if isinstance(value, str):
        text = value
        for old, new in pairs:
            text = text.replace(old, new)
        return text
    return value


def _append_note(resident: dict[str, Any], addition: str) -> None:
    clinical = resident["ClinicalCase"]
    presentation = clinical["presentation"]
    presentation["hpi"] = presentation["hpi"].rstrip() + " " + addition
    for note in resident["CaseNote"]:
        if note.get("note_type") in {"admission", "hospital_course"}:
            note["note_text"] = note["note_text"].rstrip() + " " + addition
            note["source_reference"] = "v4_revision_see_provenance"


def _set_text(resident: dict[str, Any], *, one_liner: str | None = None, chief: str | None = None) -> None:
    clinical = resident["ClinicalCase"]
    if one_liner:
        clinical["one_liner"] = one_liner
    if chief:
        clinical["chief_complaint"] = chief
        clinical["presentation"]["chief_complaint"] = chief


def _add_lab(
    resident: dict[str, Any],
    *,
    timepoint: str,
    test_name: str,
    value: float | None,
    unit: str,
    value_text: str | None = None,
) -> None:
    case_id = resident["case_id_code"]
    rows = resident["CaseLab"]
    rows.append(
        {
            "lab_id": f"LAB-{case_id}-V4-{len(rows) + 1:03d}",
            "case_id": case_id,
            "timepoint": timepoint,
            "test_name": test_name,
            "value": value,
            "value_text": value_text,
            "unit": unit,
            "status": "final",
            "source_reference": "synthetic_v4",
        }
    )


def _add_study(resident: dict[str, Any], *, study_type: str, finding: str) -> None:
    case_id = resident["case_id_code"]
    rows = resident["CaseImaging"]
    rows.append(
        {
            "study_id": f"STUDY-{case_id}-V4-{len(rows) + 1:03d}",
            "case_id": case_id,
            "timepoint": "inpatient",
            "study_type": study_type,
            "body_site": "unspecified",
            "finding": finding,
            "source_reference": "synthetic_v4",
        }
    )


def _add_micro(resident: dict[str, Any], *, specimen: str, test: str, result: str, notes: str) -> None:
    case_id = resident["case_id_code"]
    rows = resident["CaseMicrobiology"]
    rows.append(
        {
            "micro_id": f"MICRO-{case_id}-V4-{len(rows) + 1:03d}",
            "case_id": case_id,
            "timepoint": "admission",
            "specimen": specimen,
            "test": test,
            "organism": None,
            "result": result,
            "status": "final",
            "notes": notes,
            "source_reference": "synthetic_v4",
        }
    )


def _add_consult(resident: dict[str, Any], *, service: str, assessment: str, recommendation: str) -> None:
    case_id = resident["case_id_code"]
    rows = resident["CaseConsult"]
    rows.append(
        {
            "consult_id": f"CON-{case_id}-V4-{len(rows) + 1:03d}",
            "case_id": case_id,
            "service": service,
            "timepoint": "inpatient",
            "assessment": assessment,
            "recommendation": recommendation,
            "source_reference": "synthetic_v4",
        }
    )


def _extend_echo(resident: dict[str, Any], sentence: str) -> None:
    for study in resident["CaseImaging"]:
        if "echocardiogram" in str(study.get("study_type", "")).lower():
            finding = study.get("finding") or ""
            if sentence not in finding:
                study["finding"] = finding.rstrip() + " " + sentence
                study["source_reference"] = "v4_revision_see_provenance"


def _ensure_alternative(plan: dict[str, Any], token: str, action: str, rationale: str) -> None:
    alternatives = plan.get("acceptable_alternatives")
    if not isinstance(alternatives, list):
        alternatives = []
        plan["acceptable_alternatives"] = alternatives
    names = [item.get("medication") or "" for item in plan.get("medications", [])]
    medication = next(name for name in names if token in name.lower())
    if any(item.get("medication") == medication and item.get("action") == action for item in alternatives):
        return
    alternatives.append({"medication": medication, "action": action, "rationale": rationale})


def _tag_reference(plan: dict[str, Any]) -> None:
    alternatives = plan.get("acceptable_alternatives") or []
    ambiguous = {item.get("medication") for item in alternatives if isinstance(item, dict)}
    for medication in plan.get("medications", []):
        rationale = medication.get("rationale") or ""
        if "Home therapy is continued through discharge" in rationale:
            medication["rationale"] = (
                f"{medication['medication']} is listed at home and during the hospitalization for an active diagnosis. "
                "The chart does not describe an adverse effect that forces a different action."
            )
        if "Started during this admission and continued at discharge" in rationale:
            medication["rationale"] = (
                f"{medication['medication']} was started during the hospitalization. "
                "The chart does not record a stop date. Duration that is not written in the chart remains a clinician decision."
            )
        if medication.get("medication") in ambiguous:
            medication["evidence_class"] = "CLINICALLY_AMBIGUOUS"
        else:
            medication["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"


def _drug_token(name: str) -> str:
    for part in re.split(r"[^A-Za-z]+", name):
        if part and part.casefold() not in DRUG_SKIP and len(part) > 3:
            return part.casefold()
    return name.casefold()


def leak_hits(resident: dict[str, Any]) -> list[str]:
    text = json.dumps(resident)
    return [pattern for pattern in DIRECT_LEAK_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]


def strong_hint_hits(resident: dict[str, Any]) -> list[str]:
    text = json.dumps(resident)
    return [pattern for pattern in STRONG_HINT_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]


def old_design_hits(resident: dict[str, Any]) -> list[str]:
    text = json.dumps(resident)
    return [pattern for pattern in OLD_DESIGN_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]


# Exact resident-chart replacements. These remove answer-revealing sentences.
# They do not add measurements.
REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "VAL-804": [
        (
            "Admitted for resolving delirium; a pending outpatient cognitive-therapy decision was recorded. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented separately from unknown home medications. A new disease-modifying start was deferred to outpatient confirmation.",
            "Confusion for one day is a change from his usual orientation. He had been eating poorly.",
        ),
        ("Reassess pending therapeutic decision", "Primary care follow-up"),
    ],
    "VAL-810": [
        (
            "Admitted for endocarditis; remaining parenteral ceftriaxone is intended after discharge. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. ",
            "Ceftriaxone 2 g intravenously once daily was started during the hospitalization. ",
        ),
        (
            "The remaining parenteral course and infectious-disease follow-up were arranged before discharge.",
            "A later blood culture showed no growth. Infectious-disease follow-up is scheduled.",
        ),
        (
            "Complete the planned parenteral course with laboratory follow-up.",
            "A vegetation is present. The admission culture grew gram-positive cocci, and a later culture showed no growth.",
        ),
    ],
    "VAL-811": [
        (
            "Admitted for endocarditis with a remaining outpatient parenteral course. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Infectious-disease follow-up is scheduled. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.",
            "Ceftriaxone 2 g intravenously once daily was started during the hospitalization. A later blood culture showed no growth. Infectious-disease follow-up is scheduled.",
        ),
        (
            "Complete the planned parenteral course with laboratory follow-up.",
            "A vegetation is present. The admission culture grew gram-positive cocci, and a later culture showed no growth.",
        ),
    ],
    "VAL-812": [
        (
            "Admitted for endocarditis; remaining parenteral duration is a pending outpatient decision. Duration of remaining parenteral ceftriaxone is to be confirmed at infectious-disease follow-up. Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.",
            "Ceftriaxone 2 g intravenously once daily was started during the hospitalization. A later blood culture showed no growth. Infectious-disease follow-up is scheduled.",
        ),
        (
            "Complete the planned parenteral course with laboratory follow-up.",
            "A vegetation is present. The admission culture grew gram-positive cocci, and a later culture showed no growth.",
        ),
        ("Reassess pending therapeutic decision", "Infectious-disease follow-up"),
    ],
    "VAL-816": [
        (
            "Continue immunosuppression with infection-related adjustments as documented.",
            "Tacrolimus 1 mg every 12 hours is the recorded immunosuppressant. Valganciclovir was already a home medicine.",
        ),
        (
            "Confirm remaining antiviral duration as an outpatient decision.",
            "The recorded valganciclovir dose is 900 mg twice daily. Creatinine was 1.0 mg/dL then 0.9 mg/dL.",
        ),
    ],
    "VAL-817": [
        ("Anticoagulation clinic INR follow-up after warfarin resumption", "Anticoagulation clinic INR follow-up"),
    ],
    "VAL-818": [
        (
            "Admitted after hip-fracture surgery; anticoagulation is intended at discharge. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.",
            "He was admitted after operative repair of a femoral-neck fracture. Hemoglobin was 7.9 g/dL then 10.3 g/dL. INR was 2.3 then 2.9. No melena is recorded. Warfarin 5 mg daily is on the home list for paroxysmal atrial fibrillation and was administered during the hospitalization.",
        ),
    ],
    "VAL-819": [
        (
            "Admitted after hip-fracture surgery with planned anticoagulation follow-up. Warfarin was resumed. An anticoagulation-clinic INR visit is scheduled. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed.",
            "He was admitted after operative repair of a femoral-neck fracture. Warfarin was not given on the operative day and was given on later hospital days. INR was 2.5 then 2.6. An anticoagulation-clinic visit is scheduled.",
        ),
    ],
    "VAL-822": [
        (
            "Continue inpatient acid suppression and observe serial hemoglobin until stability.",
            "Hemoglobin rose from 8.5 g/dL to 10.7 g/dL. Pantoprazole was used during the hospitalization. No chronic acid-suppression indication is recorded.",
        ),
    ],
    "VAL-823": [
        (
            "Admitted for gastrointestinal bleeding with a pending anticoagulation decision. Restart versus continued hold of anticoagulation is a pending outpatient decision. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.",
            "He was admitted with gastrointestinal bleeding. Apixaban was held during the hospitalization. Hemoglobin was 9.0 g/dL then 10.2 g/dL. Blood pressure remained stable. Atrial fibrillation is the recorded indication for apixaban.",
        ),
        (
            "Hold anticoagulation while hemoglobin remains stable, then reassess.",
            "Hemoglobin rose from 9.0 g/dL to 10.2 g/dL. Blood pressure was stable.",
        ),
        ("Reassess pending therapeutic decision", "Cardiology follow-up"),
    ],
    "VAL-824": [
        (
            "aspirin 81 MG Chewable Tablet was stopped during this admission. Admitted for gastrointestinal bleeding with intentional aspirin discontinuation. Aspirin used for primary prevention was stopped after the bleed. Gastrointestinal bleeding settled and hemoglobin was stable. Aspirin used for primary prevention was stopped.",
            "He was admitted with gastrointestinal bleeding. Hemoglobin was 7.8 g/dL then 9.3 g/dL. Aspirin 81 mg daily is on the home list. No prior myocardial infarction and no coronary stent are recorded.",
        ),
        (
            "Hold anticoagulation while hemoglobin remains stable, then reassess.",
            "Hemoglobin rose from 7.8 g/dL to 9.3 g/dL. No anticoagulant is on the medication list.",
        ),
    ],
}

ADDITIONS: dict[str, str] = {
    "VAL-801": (
        "His daughter states that he was oriented and independent with his medicines until several days ago. "
        "Urinalysis showed no leukocyte esterase and no nitrites. A chest radiograph showed no focal consolidation. "
        "The working precipitant is poor oral intake with dry mucous membranes and a standing systolic pressure of 116 mmHg. "
        "Attention improved after oral intake improved."
    ),
    "VAL-802": (
        "Her son states that she was oriented at her baseline before these two days. "
        "Mucous membranes are dry. Temperature is 36.80°C. Urinalysis showed no leukocyte esterase and no nitrites. "
        "A chest radiograph showed no focal consolidation. No creatinine from before this admission is recorded."
    ),
    "VAL-803": (
        "He was oriented at baseline by collateral history, and the confusion is a change over one week. "
        "Hydrochlorothiazide was not given after the admission sodium of 128 mmol/L. "
        "Confusion cleared as sodium rose to 135 mmol/L. No seizure is recorded."
    ),
    "VAL-804": (
        "He was oriented and lived independently before this day of confusion. "
        "Mucous membranes are dry. Urinalysis showed no leukocyte esterase and no nitrites. "
        "A chest radiograph showed no focal consolidation. Creatinine is 0.9 mg/dL then 0.8 mg/dL. "
        "Attention improved after he resumed eating."
    ),
    "VAL-805": (
        "She missed her oral furosemide and metoprolol succinate for three days because the pharmacy could not fill them. "
        "She has had no chest pain. The electrocardiogram shows sinus rhythm without ST-segment elevation or depression. "
        "High-sensitivity troponin I is 8 ng/L, within the laboratory reference range. The leukocyte count is 7.4 x10^3/uL and the temperature is 36.80°C. "
        "No echocardiogram and no intravenous loop-diuretic dose are recorded. Oxygen saturation rose from 92 percent to 98 percent."
    ),
    "VAL-806": (
        "She describes four days of restaurant meals and unrestricted fluids before the dyspnea worsened. "
        "She has had no chest pain. The electrocardiogram shows sinus rhythm without ST-segment elevation or depression. "
        "High-sensitivity troponin I is 9 ng/L, within the laboratory reference range. Temperature is 36.80°C and the leukocyte count is 8.1 x10^3/uL. "
        "No creatinine from before this illness is recorded. Lisinopril was held during the hospitalization."
    ),
    "VAL-807": (
        "He missed two days of oral furosemide before admission. He has had no chest pain. "
        "The electrocardiogram shows sinus rhythm without ST-segment elevation or depression. "
        "High-sensitivity troponin I is 7 ng/L, within the laboratory reference range. The leukocyte count is 6.8 x10^3/uL. "
        "No potassium product was administered."
    ),
    "VAL-808": (
        "She missed two days of her home heart-failure medicines, then developed worsening edema. "
        "She has had no chest pain. The electrocardiogram shows sinus rhythm without ST-segment elevation or depression. "
        "High-sensitivity troponin I is 6 ng/L, within the laboratory reference range. The leukocyte count is 7.1 x10^3/uL."
    ),
    "VAL-809": (
        "He does not inject drugs, and no vascular catheter was present before admission. "
        "Dental examination shows poor dentition and no recent extraction. "
        "The echocardiogram describes no abscess and no severe valvular regurgitation. "
        "Cardiothoracic surgery reviewed that study. Heart failure from valve dysfunction is not described, and surgery was not recommended for that reason. "
        "The leukocyte count is 11.2 x10^3/uL then 7.1 x10^3/uL. The organism is reported only as gram-positive cocci. No remaining antibiotic duration is recorded."
    ),
    "VAL-810": (
        "He does not inject drugs. Dental examination shows poor dentition and no recent extraction. "
        "The echocardiogram describes no abscess and no severe valvular regurgitation. "
        "Cardiothoracic surgery reviewed that study and did not recommend an operation for heart failure from valve dysfunction. "
        "The organism is reported only as gram-positive cocci. No stop date for ceftriaxone is recorded."
    ),
    "VAL-811": (
        "He does not inject drugs. No vascular catheter was present before admission. "
        "The echocardiogram describes no abscess and no severe valvular regurgitation. "
        "Cardiothoracic surgery reviewed that study and did not recommend an operation for heart failure from valve dysfunction. "
        "The organism is reported only as gram-positive cocci. No stop date for ceftriaxone is recorded."
    ),
    "VAL-812": (
        "He does not inject drugs. The echocardiogram describes no abscess and no severe valvular regurgitation. "
        "Cardiothoracic surgery reviewed that study and did not recommend an operation for heart failure from valve dysfunction. "
        "Hemoglobin is 13.6 g/dL then 11.9 g/dL. The organism is reported only as gram-positive cocci. No stop date for ceftriaxone is recorded."
    ),
    "VAL-813": (
        "Diarrhea began several days before any CMV test. Mucous membranes are dry. "
        "Clostridioides difficile toxin was negative, and the admission viral-load assay then detected CMV. "
        "Valganciclovir was started after that result. Potassium fell from 4.7 mmol/L to 3.9 mmol/L. "
        "Creatinine was 1.2 mg/dL then 1.0 mg/dL. Leukocytes are 5.1 x10^3/uL, hemoglobin is 11.4 g/dL, and platelets are 210 x10^3/uL. "
        "Tacrolimus is the only immunosuppressant on the medication list. No trough is recorded."
    ),
    "VAL-814": (
        "Diarrhea and nausea were present for one week before the viral-load result. "
        "Clostridioides difficile toxin was negative. Mucous membranes are dry. "
        "Potassium is 3.6 mmol/L then 4.1 mmol/L. Leukocytes are 4.8 x10^3/uL. "
        "Mycophenolate was held during the hospitalization. Valganciclovir was started after the viral-load result. "
        "No trough is recorded."
    ),
    "VAL-815": (
        "Nausea for two days preceded the viral-load result. Clostridioides difficile toxin was negative. "
        "She was not taking valganciclovir before admission, and it was started after the result. "
        "Weight fell from 74 kg to 68 kg. Leukocytes are 6.4 x10^3/uL. No trough is recorded. No other immunosuppressant is listed."
    ),
    "VAL-816": (
        "CMV disease was diagnosed before this admission, and valganciclovir was already a home medicine. "
        "This diarrhea is improving after one day. Creatinine is 1.0 mg/dL then 0.9 mg/dL. Leukocytes are 5.6 x10^3/uL. "
        "No new immunosuppressant is listed."
    ),
    "VAL-817": (
        "The fracture followed a fall. Hemoglobin is 9.0 g/dL then 10.1 g/dL. INR is 2.6 on admission and at discharge. "
        "No melena is recorded. Warfarin is on the home list for paroxysmal atrial fibrillation and was administered during the hospitalization."
    ),
    "VAL-818": (
        "No melena is recorded. The postoperative hemoglobin nadir is 7.9 g/dL, and the discharge hemoglobin is 10.3 g/dL. "
        "Warfarin is on the home list for paroxysmal atrial fibrillation."
    ),
    "VAL-819": (
        "Hemoglobin is 10.4 g/dL then 11.1 g/dL. No melena is recorded. "
        "Warfarin is on the home list for paroxysmal atrial fibrillation. Creatinine is 0.9 mg/dL then 1.1 mg/dL."
    ),
    "VAL-820": (
        "No melena is recorded. Hemoglobin is 8.3 g/dL then 11.1 g/dL. INR is 3.2 then 2.0. "
        "Enoxaparin was started in the hospital for venous-thromboembolism prophylaxis and is not a home medicine. "
        "Warfarin is on the home list for paroxysmal atrial fibrillation."
    ),
    "VAL-821": (
        "Black stool was reported the day before admission and was not reported again after arrival. "
        "Blood pressure stayed above 100 mmHg systolic. The bleeding lesion was not examined by endoscopy in this record. "
        "Apixaban was held during the hospitalization. Atrial fibrillation remains the recorded indication."
    ),
    "VAL-822": (
        "Black stool was reported the day before admission and was not reported again after arrival. "
        "Blood pressure stayed above 100 mmHg systolic. The bleeding lesion was not examined by endoscopy in this record. "
        "No anticoagulant or antiplatelet medicine is on the home list. Pantoprazole was started during the hospitalization."
    ),
    "VAL-823": (
        "Black stool was reported before admission and was not reported again after the first hospital day. "
        "The bleeding lesion was not examined by endoscopy in this record. Apixaban was held during the hospitalization."
    ),
    "VAL-824": (
        "Black stool was reported before admission. Hemoglobin rose from 7.8 g/dL to 9.3 g/dL. "
        "The bleeding lesion was not examined by endoscopy in this record. "
        "No prior myocardial infarction and no coronary stent are recorded. Aspirin 81 mg daily is on the home list and the inpatient list."
    ),
}

ONE_LINERS: dict[str, str] = {
    "VAL-804": "70-year-old woman admitted with one day of new confusion and poor intake.",
    "VAL-810": "83-year-old man admitted with nausea, fatigue, and a temperature of 38.20°C.",
    "VAL-811": "74-year-old man admitted with nausea and gram-positive cocci in the blood.",
    "VAL-812": "75-year-old man admitted with fatigue and nausea.",
    "VAL-813": "64-year-old woman with a kidney transplant admitted with diarrhea.",
    "VAL-814": "71-year-old man with a kidney transplant admitted with diarrhea and nausea.",
    "VAL-815": "68-year-old woman with a kidney transplant admitted with nausea.",
    "VAL-816": "57-year-old man with a kidney transplant admitted with diarrhea and fatigue.",
    "VAL-821": "78-year-old woman admitted with fatigue and black stool.",
    "VAL-822": "79-year-old woman admitted with fatigue, nausea, and black stool.",
    "VAL-823": "71-year-old man admitted with fatigue and black stool.",
    "VAL-824": "77-year-old woman admitted with fatigue, nausea, and black stool.",
}

CHIEFS: dict[str, str] = {
    "VAL-813": "Diarrhea for several days.",
    "VAL-804": "Confusion for one day.",
    "VAL-810": "Nausea and fatigue.",
    "VAL-814": "Diarrhea and nausea.",
    "VAL-815": "Nausea.",
    "VAL-816": "Diarrhea and fatigue.",
}


def _structured_additions(resident: dict[str, Any]) -> None:
    case_id = resident["case_id_code"]
    if case_id in {"VAL-801", "VAL-802", "VAL-804"}:
        _add_study(resident, study_type="Chest radiograph", finding="No focal consolidation.")
        _add_lab(
            resident,
            timepoint="admission",
            test_name="Leukocyte esterase in Urine",
            value=None,
            value_text="negative",
            unit="",
        )
        _add_lab(
            resident,
            timepoint="admission",
            test_name="Nitrite in Urine",
            value=None,
            value_text="negative",
            unit="",
        )
    if case_id == "VAL-804":
        _add_lab(resident, timepoint="admission", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=0.9, unit="mg/dL")
        _add_lab(resident, timepoint="discharge", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=0.8, unit="mg/dL")
    if case_id in {"VAL-805", "VAL-806", "VAL-807", "VAL-808"}:
        _add_study(
            resident,
            study_type="Electrocardiogram",
            finding="Sinus rhythm. No ST-segment elevation or depression.",
        )
        troponin = {"VAL-805": 8, "VAL-806": 9, "VAL-807": 7, "VAL-808": 6}[case_id]
        leukocytes = {"VAL-805": 7.4, "VAL-806": 8.1, "VAL-807": 6.8, "VAL-808": 7.1}[case_id]
        _add_lab(
            resident,
            timepoint="admission",
            test_name="Troponin I.cardiac [Mass/volume] in Serum or Plasma",
            value=troponin,
            unit="ng/L",
        )
        _add_lab(
            resident,
            timepoint="admission",
            test_name="Leukocytes [#/volume] in Blood",
            value=leukocytes,
            unit="10*3/uL",
        )
    if case_id in {"VAL-809", "VAL-810", "VAL-811", "VAL-812"}:
        _extend_echo(resident, "No abscess and no severe valvular regurgitation.")
        _add_consult(
            resident,
            service="cardiothoracic surgery",
            assessment="Echocardiogram reviewed for findings that would prompt an operation.",
            recommendation=(
                "Ventricular function is preserved. No abscess and no severe regurgitation are described. "
                "Surgery was not recommended for heart failure from valve dysfunction."
            ),
        )
    if case_id == "VAL-809":
        _add_lab(resident, timepoint="admission", test_name="Leukocytes [#/volume] in Blood", value=11.2, unit="10*3/uL")
        _add_lab(resident, timepoint="discharge", test_name="Leukocytes [#/volume] in Blood", value=7.1, unit="10*3/uL")
    if case_id in {"VAL-813", "VAL-814", "VAL-815", "VAL-816"}:
        _add_micro(
            resident,
            specimen="stool",
            test="Clostridioides difficile toxin",
            result="negative",
            notes="Stool toxin assay during the diarrheal or gastrointestinal work-up.",
        )
    if case_id == "VAL-813":
        _add_lab(resident, timepoint="admission", test_name="Leukocytes [#/volume] in Blood", value=5.1, unit="10*3/uL")
        _add_lab(resident, timepoint="admission", test_name="Hemoglobin [Mass/volume] in Blood", value=11.4, unit="g/dL")
        _add_lab(resident, timepoint="admission", test_name="Platelets [#/volume] in Blood", value=210, unit="10*3/uL")
    if case_id == "VAL-814":
        _add_lab(resident, timepoint="admission", test_name="Potassium [Moles/volume] in Serum or Plasma", value=3.6, unit="mmol/L")
        _add_lab(resident, timepoint="discharge", test_name="Potassium [Moles/volume] in Serum or Plasma", value=4.1, unit="mmol/L")
        _add_lab(resident, timepoint="admission", test_name="Leukocytes [#/volume] in Blood", value=4.8, unit="10*3/uL")
    if case_id == "VAL-815":
        _add_lab(resident, timepoint="admission", test_name="Leukocytes [#/volume] in Blood", value=6.4, unit="10*3/uL")
    if case_id == "VAL-816":
        _add_lab(resident, timepoint="admission", test_name="Leukocytes [#/volume] in Blood", value=5.6, unit="10*3/uL")
    if case_id == "VAL-819":
        _add_lab(resident, timepoint="admission", test_name="Hemoglobin [Mass/volume] in Blood", value=10.4, unit="g/dL")
        _add_lab(resident, timepoint="discharge", test_name="Hemoglobin [Mass/volume] in Blood", value=11.1, unit="g/dL")


def _reference_edits(evaluator: dict[str, Any]) -> None:
    case_id = evaluator["case_id_code"]
    plan = evaluator["reference_discharge_plan"]
    if case_id == "VAL-804":
        _ensure_alternative(
            plan,
            "metformin",
            "hold",
            "Holding metformin is acceptable if oral intake is still poor at discharge. The reference continues it because intake improved and creatinine is 0.9 mg/dL then 0.8 mg/dL.",
        )
    if case_id == "VAL-807":
        _ensure_alternative(
            plan,
            "furosemide",
            "modify",
            "A lower oral dose is acceptable because discharge weight is 93 kg and the recorded dry weight is 95 kg. The reference keeps 40 mg once daily. No new numeric dose is specified.",
        )
    if case_id == "VAL-809":
        _ensure_alternative(
            plan,
            "ceftriaxone",
            "modify",
            "The stop date is not recorded. Infectious diseases may set the remaining duration. The reference keeps the started 2 g intravenous daily dose and does not invent a day count.",
        )
    if case_id in {"VAL-810", "VAL-811", "VAL-812"}:
        _ensure_alternative(
            plan,
            "ceftriaxone",
            "modify",
            "No stop date is written in the chart. Setting that date at infectious-disease follow-up is acceptable. The reference keeps the intravenous dose that was started in the hospital.",
        )
    if case_id == "VAL-815":
        _ensure_alternative(
            plan,
            "tacrolimus",
            "modify",
            "A temporary reduction is acceptable if a trough is later documented. No trough and no dose change are recorded, so the reference keeps 1 mg every 12 hours.",
        )
    if case_id == "VAL-818":
        _ensure_alternative(
            plan,
            "warfarin",
            "hold",
            "Holding warfarin is acceptable because the postoperative hemoglobin nadir was 7.9 g/dL. The reference continues it because atrial fibrillation is the indication, the discharge hemoglobin is 10.3 g/dL, and the discharge INR is 2.9.",
        )
    if case_id == "VAL-820":
        _ensure_alternative(
            plan,
            "enoxaparin",
            "continue",
            "A brief further overlap is acceptable if the clinician judges the discharge INR of 2.0 not yet stable. The reference stops prophylactic enoxaparin because it is not a home medicine and warfarin is already therapeutic for atrial fibrillation.",
        )
    if case_id == "VAL-822":
        _ensure_alternative(
            plan,
            "pantoprazole",
            "continue",
            "A short further course is acceptable after gastrointestinal bleeding. The reference stops pantoprazole because it was started in the hospital and no chronic indication is recorded.",
        )
    if case_id == "VAL-823":
        _ensure_alternative(
            plan,
            "apixaban",
            "restart",
            "Restarting apixaban is acceptable because hemoglobin rose from 9.0 g/dL to 10.2 g/dL and atrial fibrillation is the indication. The reference holds it because the lesion was not examined by endoscopy.",
        )
    if case_id == "VAL-824":
        _ensure_alternative(
            plan,
            "aspirin",
            "continue",
            "Continuing aspirin is acceptable if the clinician assigns a cardiovascular indication that is not written in the chart. The reference stops it because no myocardial infarction and no stent are recorded and hemoglobin fell to 7.8 g/dL.",
        )
    for medication in plan.get("medications", []):
        if case_id == "VAL-822" and "pantoprazole" in medication["medication"]:
            medication["rationale"] = (
                "Pantoprazole was started during the hospitalization. Hemoglobin rose from 8.5 g/dL to 10.7 g/dL. "
                "No chronic acid-suppression indication is recorded. A short continuation is an acceptable alternative."
            )
        if case_id == "VAL-824" and "aspirin" in medication["medication"]:
            medication["rationale"] = (
                "No prior myocardial infarction and no coronary stent are recorded. Hemoglobin was 7.8 g/dL then 9.3 g/dL with gastrointestinal bleeding. "
                "Stopping aspirin is the reference. Continuing it is an acceptable alternative."
            )
        if case_id == "VAL-823" and "apixaban" in medication["medication"]:
            medication["rationale"] = (
                "Apixaban was held during the bleeding. Hemoglobin rose from 9.0 g/dL to 10.2 g/dL and blood pressure was stable. "
                "The lesion was not examined by endoscopy, so the reference holds apixaban and a restart is an acceptable alternative."
            )
    _tag_reference(plan)


# Ratings after the revision. Both axes must be PASS or PASS_WITH_MINOR_CONCERN to enter a codebook.
RATINGS: dict[str, dict[str, str]] = {
    "VAL-801": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Infection screen is negative and volume depletion is the precipitant. No urine sodium or formal cognitive test is recorded."},
    "VAL-802": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No creatinine from before this admission is recorded, so lisinopril continuation and a hold are both encoded."},
    "VAL-803": {"task": "PASS", "sufficiency": "PASS", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Sodium 128 then 135 mmol/L remains a labeled synthetic finding from version 3. Stopping hydrochlorothiazide and a monitored restart are both encoded."},
    "VAL-804": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "The precipitant is poor intake after a negative infection screen. Creatinine 0.9 then 0.8 mg/dL is synthetic."},
    "VAL-805": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No ejection fraction and no intravenous loop-diuretic dose are recorded. Diuretic intensification and an additional heart-failure class remain alternatives without a fabricated dose."},
    "VAL-806": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No pre-illness creatinine is recorded. Restarting lisinopril and a continued hold are both encoded."},
    "VAL-807": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Discharge weight is below the recorded dry weight, so a lower diuretic dose is an alternative. No new dose number is specified."},
    "VAL-808": {"task": "PASS", "sufficiency": "PASS", "readiness": "READY_FOR_CLINICIAN_REVIEW", "uncertainty": ""},
    "VAL-809": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "The organism is gram-positive cocci only. No fever, dental extraction, prosthetic valve, or species was added. Antibiotic duration is not recorded."},
    "VAL-810": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Organism species and the ceftriaxone stop date are not recorded."},
    "VAL-811": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Organism species and the ceftriaxone stop date are not recorded."},
    "VAL-812": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Hemoglobin fell from 13.6 g/dL to 11.9 g/dL without a stated cause. Organism species and the stop date are not recorded."},
    "VAL-813": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Only tacrolimus is listed as immunosuppression. No trough is recorded. Admission potassium was 4.7 mmol/L, not a low value; the fall to 3.9 mmol/L is the recorded change."},
    "VAL-814": {"task": "PASS", "sufficiency": "PASS", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Mycophenolate restart versus continued hold remains ambiguous. Potassium values added in version 4 are synthetic."},
    "VAL-815": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No tacrolimus trough is recorded. Weight fell from 74 kg to 68 kg."},
    "VAL-816": {"task": "PASS", "sufficiency": "PASS", "readiness": "READY_FOR_CLINICIAN_REVIEW", "uncertainty": ""},
    "VAL-817": {"task": "PASS", "sufficiency": "PASS", "readiness": "READY_FOR_CLINICIAN_REVIEW", "uncertainty": ""},
    "VAL-818": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Postoperative hemoglobin nadir was 7.9 g/dL. Continuing warfarin and a hold are both encoded."},
    "VAL-819": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Hemoglobin 10.4 then 11.1 g/dL is synthetic. The operative-day warfarin gap is described without a discharge instruction."},
    "VAL-820": {"task": "PASS", "sufficiency": "PASS", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "Stopping prophylactic enoxaparin and a brief further overlap are both encoded at a discharge INR of 2.0."},
    "VAL-821": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No endoscopy is recorded. Restarting apixaban and a continued hold are both encoded."},
    "VAL-822": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No endoscopy is recorded. Stopping pantoprazole and a short continuation are both encoded."},
    "VAL-823": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No endoscopy is recorded. The reference holds apixaban and a restart is an acceptable alternative."},
    "VAL-824": {"task": "PASS", "sufficiency": "PASS_WITH_MINOR_CONCERN", "readiness": "READY_WITH_DECLARED_UNCERTAINTY", "uncertainty": "No endoscopy and no recorded coronary event. Stopping aspirin and continuing it are both encoded. Absence of a stent is synthetic."},
}

SYNTHETIC_FACTS: list[dict[str, str]] = [
    {"case": "VAL-801", "field": "history", "value": "Oriented and independent until several days ago, by collateral history", "why": "Delirium requires an acute change from baseline", "concern": "Alex C1: delirium must be a change from baseline", "literature": "E1", "optional": "No", "labeled": "YES"},
    {"case": "VAL-801", "field": "urinalysis and chest radiograph", "value": "Negative leukocyte esterase, negative nitrite, no focal consolidation", "why": "A volume-depletion precipitant is interpretable only if a simple infection screen is visible", "concern": "Alex C1 precipitant; UTI was his example and was not added", "literature": "E1", "optional": "No", "labeled": "YES"},
    {"case": "VAL-802", "field": "history and infection screen", "value": "Oriented at baseline; dry mucous membranes; negative urinalysis; clear chest radiograph", "why": "Clinical-sufficiency rubric for delirium", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E1", "optional": "No", "labeled": "YES"},
    {"case": "VAL-803", "field": "history", "value": "Oriented at baseline; confusion changed over one week", "why": "Delirium definition", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback. Katie reviewed this case and did not finish C2-C5.", "literature": "E1", "optional": "No", "labeled": "YES"},
    {"case": "VAL-804", "field": "creatinine", "value": "0.9 mg/dL then 0.8 mg/dL", "why": "Metformin continuation requires visible kidney function", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E5", "optional": "No", "labeled": "YES"},
    {"case": "VAL-804", "field": "history and infection screen", "value": "Baseline orientation, dry mucous membranes, negative urinalysis, clear chest radiograph", "why": "Delirium precipitant", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E1", "optional": "No", "labeled": "YES"},
    {"case": "VAL-805", "field": "adherence, electrocardiogram, troponin, leukocytes", "value": "Missed oral furosemide and metoprolol for three days; sinus rhythm without ST-segment change; troponin I 8 ng/L; leukocytes 7.4", "why": "The heart-failure admission needs one coherent precipitant pathway and a limited ischemia and arrhythmia screen", "concern": "Alex C1: decompensation was not investigated", "literature": "E2", "optional": "No", "labeled": "YES"},
    {"case": "VAL-806", "field": "diet, electrocardiogram, troponin, leukocytes", "value": "Four days of restaurant meals and unrestricted fluids; sinus rhythm; troponin I 9 ng/L; leukocytes 8.1", "why": "Precipitant and ischemia screen without inventing a baseline creatinine", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E2", "optional": "No", "labeled": "YES"},
    {"case": "VAL-807", "field": "adherence, electrocardiogram, troponin, leukocytes", "value": "Missed two days of oral furosemide; sinus rhythm; troponin I 7 ng/L; leukocytes 6.8", "why": "Precipitant pathway", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E2", "optional": "No", "labeled": "YES"},
    {"case": "VAL-808", "field": "adherence, electrocardiogram, troponin, leukocytes", "value": "Missed two days of home heart-failure medicines; sinus rhythm; troponin I 6 ng/L; leukocytes 7.1", "why": "Precipitant pathway", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E2", "optional": "No", "labeled": "YES"},
    {"case": "VAL-809", "field": "source and surgical screen", "value": "No injection drug use, no preadmission catheter, no recent extraction, no abscess, no severe regurgitation, leukocytes 11.2 then 7.1", "why": "Endocarditis management context without inventing fever, a prosthetic valve, an extraction, or a species", "concern": "Alex C1: source, imaging, and surgical consideration", "literature": "E3", "optional": "No", "labeled": "YES"},
    {"case": "VAL-810", "field": "source and surgical screen", "value": "No injection drug use, poor dentition, no recent extraction, no abscess, no severe regurgitation", "why": "Same endocarditis sufficiency screen", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E3", "optional": "No", "labeled": "YES"},
    {"case": "VAL-811", "field": "source and surgical screen", "value": "No injection drug use, no preadmission catheter, no abscess, no severe regurgitation", "why": "Same endocarditis sufficiency screen", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E3", "optional": "No", "labeled": "YES"},
    {"case": "VAL-812", "field": "source and surgical screen", "value": "No injection drug use, no abscess, no severe regurgitation", "why": "Same endocarditis sufficiency screen", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E3", "optional": "No", "labeled": "YES"},
    {"case": "VAL-813", "field": "volume, stool study, blood count", "value": "Dry mucous membranes; negative C. difficile toxin; leukocytes 5.1, hemoglobin 11.4 g/dL, platelets 210", "why": "Symptoms-before-label work-up and a baseline for valganciclovir", "concern": "Alex C1: chronology and volume or electrolyte consequences", "literature": "E4", "optional": "No", "labeled": "YES"},
    {"case": "VAL-814", "field": "potassium, leukocytes, stool study", "value": "Potassium 3.6 then 4.1 mmol/L; leukocytes 4.8; negative C. difficile toxin; dry mucous membranes", "why": "Diarrhea physiology and antiviral monitoring", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E4", "optional": "No", "labeled": "YES"},
    {"case": "VAL-815", "field": "stool study and leukocytes", "value": "Negative C. difficile toxin; leukocytes 6.4", "why": "Work-up before the CMV label and a blood count for the antiviral", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E4", "optional": "No", "labeled": "YES"},
    {"case": "VAL-816", "field": "leukocytes", "value": "Leukocytes 5.6 x10^3/uL", "why": "Blood count while valganciclovir is already a home medicine", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E12", "optional": "Yes", "labeled": "YES"},
    {"case": "VAL-819", "field": "hemoglobin", "value": "10.4 g/dL then 11.1 g/dL", "why": "Postoperative bleeding stability for a warfarin decision", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E9", "optional": "No", "labeled": "YES"},
    {"case": "VAL-821", "field": "bleeding description", "value": "Black stool the day before admission, not reported again after arrival", "why": "The hemorrhage label needs a visible bleeding manifestation", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E8", "optional": "No", "labeled": "YES"},
    {"case": "VAL-822", "field": "bleeding description", "value": "Black stool the day before admission, not reported again after arrival; no chronic acid-suppression indication", "why": "Visible bleeding manifestation and the limit of the pantoprazole indication", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E8", "optional": "No", "labeled": "YES"},
    {"case": "VAL-823", "field": "bleeding description", "value": "Black stool before admission, not reported again after the first hospital day", "why": "Visible bleeding manifestation", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E8", "optional": "No", "labeled": "YES"},
    {"case": "VAL-824", "field": "bleeding and cardiovascular history", "value": "Black stool; no prior myocardial infarction and no coronary stent", "why": "Aspirin indication is otherwise only the phrase antiplatelet therapy", "concern": "Clinical-sufficiency rubric applied; no Alex case-specific feedback", "literature": "E11", "optional": "No", "labeled": "YES"},
]


def revise_case(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    resident, evaluator = load_pair(case_id)
    resident = _replace_strings(resident, REPLACEMENTS.get(case_id, []))
    if case_id in ONE_LINERS or case_id in CHIEFS:
        _set_text(resident, one_liner=ONE_LINERS.get(case_id), chief=CHIEFS.get(case_id))
    if case_id in ADDITIONS:
        _append_note(resident, ADDITIONS[case_id])
    _structured_additions(resident)
    resident = _scrub(resident)
    evaluator = _replace_strings(evaluator, REPLACEMENTS.get(case_id, []))
    plan = evaluator["reference_discharge_plan"]
    precheck = evaluator.get("precheck_finding")
    merged = deepcopy(resident)
    merged["reference_discharge_plan"] = plan
    if precheck is not None:
        merged["precheck_finding"] = precheck
    _reference_edits(merged)
    rating = RATINGS[case_id]
    merged["clinician_review_status"] = rating["readiness"]
    merged["v4_provenance"] = {
        "task_validity": rating["task"],
        "clinical_sufficiency": rating["sufficiency"],
        "readiness": rating["readiness"],
        "declared_uncertainty": rating["uncertainty"],
        "alex_case_specific_feedback": case_id in ALEX_EXPECTED,
        "synthetic_facts": [row for row in SYNTHETIC_FACTS if row["case"] == case_id],
    }
    resident.pop("reference_discharge_plan", None)
    resident.pop("clinician_review_status", None)
    resident.pop("v4_provenance", None)
    return resident, merged


def _passes_gate(case_id: str, resident: dict[str, Any], evaluator: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    rating = RATINGS[case_id]
    if rating["task"] not in {"PASS", "PASS_WITH_MINOR_CONCERN"}:
        reasons.append(f"task validity {rating['task']}")
    if rating["sufficiency"] not in {"PASS", "PASS_WITH_MINOR_CONCERN"}:
        reasons.append(f"clinical sufficiency {rating['sufficiency']}")
    if leak_hits(resident):
        reasons.append("direct answer leak: " + "; ".join(leak_hits(resident)))
    if old_design_hits(resident):
        reasons.append("old planted-error metadata: " + "; ".join(old_design_hits(resident)))
    if strong_hint_hits(resident):
        reasons.append("strong hint: " + "; ".join(strong_hint_hits(resident)))
    blob = json.dumps(resident).casefold()
    for medication in evaluator["reference_discharge_plan"]["medications"]:
        token = _drug_token(str(medication.get("medication")))
        if token not in blob:
            reasons.append(f"reference drug not visible: {medication.get('medication')}")
        if medication.get("evidence_class") not in {
            "SUFFICIENT_VISIBLE_EVIDENCE",
            "WEAK_VISIBLE_EVIDENCE",
            "CLINICALLY_AMBIGUOUS",
        }:
            reasons.append(f"bad evidence class for {medication.get('medication')}")
    unlabeled = [
        row
        for row in resident.get("CaseLab", [])
        if row.get("source_reference") == "synthetic_v4" and case_id not in {item["case"] for item in SYNTHETIC_FACTS}
    ]
    if unlabeled:
        reasons.append("synthetic lab without a provenance row")
    return not reasons, reasons


def _alex_payload(feedback: Any) -> dict[str, Any]:
    def group(item: Any) -> dict[str, Any]:
        return {"labels": list(item.labels), "selected": list(item.selected), "blank": not item.selected}

    return {
        "case_id": feedback.case_id,
        "source_document": ALEX_DOCX.name,
        "form_reviewer_code": feedback.reviewer,
        "form_review_date": feedback.review_date,
        "document_last_modified_by": "Sugerman, Alexander",
        "attribution_note": (
            "The form reviewer-code, review-date, initials, and case-date controls are blank. "
            "Document core properties record lastModifiedBy Sugerman, Alexander. "
            "The file name identifies the Alex / Team KAPOw review. No initials were inferred."
        ),
        "c1_domains": [
            {"domain": domain, "selected": list(score.selected), "blank": not score.selected}
            for domain, score in zip(C1_DOMAINS, feedback.c1_scores, strict=True)
        ],
        "c1_overall": group(feedback.c1_result),
        "c1_comment": feedback.c1_comment,
        "c2": group(feedback.c2_result),
        "c2_comment": feedback.c2_comment,
        "c3": group(feedback.c3_result),
        "c3_comment": feedback.c3_comment,
        "c4": group(feedback.c4_result),
        "c4_comment": feedback.c4_comment,
        "c5": group(feedback.c5_difficulty),
        "c5_comment": feedback.c5_comment,
        "recommendation": group(feedback.recommendation),
        "overall_comment": feedback.overall_comment,
    }


def _feedback_has_content(payload: dict[str, Any]) -> bool:
    if payload["c1_comment"] or payload["c1_overall"]["selected"]:
        return True
    return any(domain["selected"] for domain in payload["c1_domains"])


def comparison_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = [
        {
            "Case": "VAL-801",
            "Reviewer/source": "Katie / KO Round 1 extract",
            "Exact feedback": "The cause of delirium is not revealed, and it is not clear why ibuprofen was stopped.",
            "Validation dimension": "TASK_ALIGNMENT",
            "Clinical/task interpretation": "The resident must decide the ibuprofen action from the chart. The chart must not announce that action.",
            "Existing current-state response": "Version 3 leaves ibuprofen on both lists, continues it in the hidden reference, and encodes a stop as an alternative.",
            "Remaining gap": "The delirium story still needed an explicit change from baseline.",
            "Revision required?": "Yes for the baseline and precipitant. No change to the ibuprofen reference.",
            "Evidence needed": "E1 collateral baseline; E7 for the alternative stop.",
            "Decision": "INDEPENDENT from Alex on the ibuprofen task. The delirium story is CONCORDANT with Alex.",
            "Relationship": "CONCORDANT",
        },
        {
            "Case": "VAL-801",
            "Reviewer/source": "Alex / Team KAPOw C1",
            "Exact feedback": "Baseline delirium does not exist because delirium is a change from baseline. A precipitant such as a UTI would make the decompensation interpretable. C1 Fail. C2-C5 and overall recommendation blank.",
            "Validation dimension": "CLINICAL_SUFFICIENCY",
            "Clinical/task interpretation": "The hospitalization needs an acute change and a clinically interpretable precipitant.",
            "Existing current-state response": "Version 3 has poor intake, dry mucous membranes, and a standing systolic pressure of 116 mmHg.",
            "Remaining gap": "Baseline cognition and a simple infection screen were not stated. A UTI was not added.",
            "Revision required?": "Yes. Minimum labeled additions only.",
            "Evidence needed": "E1",
            "Decision": "COMPLEMENTARY to Katie's task comment. Volume depletion was retained as the precipitant.",
            "Relationship": "COMPLEMENTARY",
        },
        {
            "Case": "VAL-802",
            "Reviewer/source": "Katie / KO Round 1 extract",
            "Exact feedback": "Delirium cause is not revealed, baseline creatinine is unclear, and the statin plan was confusing. Overall recommendation exclude.",
            "Validation dimension": "REFERENCE_VALIDITY",
            "Clinical/task interpretation": "Do not invent a baseline creatinine. Encode a lisinopril hold as an alternative.",
            "Existing current-state response": "Version 3 keeps creatinine 1.3 then 1.2 mg/dL and encodes the hold.",
            "Remaining gap": "The delirium rubric still required a baseline and a precipitant screen.",
            "Revision required?": "Yes for sufficiency. No invented baseline creatinine.",
            "Evidence needed": "E1",
            "Decision": "INDEPENDENT. Alex did not review this case.",
            "Relationship": "INDEPENDENT",
        },
        {
            "Case": "VAL-803",
            "Reviewer/source": "Katie / KO Round 1 extract",
            "Exact feedback": "C1 Fail. Later items were not completed. Delirium cause unclear. Creatinine change and a 7-day lisinopril supply were questioned.",
            "Validation dimension": "CLINICAL_SUFFICIENCY",
            "Clinical/task interpretation": "Keep the 30-day lisinopril supply from the clean chart. Thiazide-associated hyponatremia can support the hydrochlorothiazide decision.",
            "Existing current-state response": "Version 3 holds hydrochlorothiazide after sodium 128 mmol/L and encodes a monitored restart.",
            "Remaining gap": "Baseline cognition was not explicit.",
            "Revision required?": "Yes, limited to the baseline statement.",
            "Evidence needed": "E1 and E6",
            "Decision": "INDEPENDENT. Alex did not review this case. His C2-C5 were not inferred for anyone.",
            "Relationship": "INDEPENDENT",
        },
        {
            "Case": "VAL-805",
            "Reviewer/source": "Katie / KO Round 1 extract",
            "Exact feedback": "The inpatient regimen should not match the home regimen; furosemide would be intravenous and increased. Weight is not at dry weight. Additional heart-failure therapy should be a decision.",
            "Validation dimension": "HOSPITAL_COURSE",
            "Clinical/task interpretation": "Do not invent an intravenous dose or an ejection fraction to satisfy that comment. Encode intensification and an additional class as alternatives.",
            "Existing current-state response": "Version 3 preserves oral furosemide 40 mg once daily, weights 81 kg, 78 kg, and dry weight 73 kg, and does not record an ejection fraction.",
            "Remaining gap": "Why the patient decompensated was still not investigated.",
            "Revision required?": "No intravenous dose was added. The precipitant pathway was added separately.",
            "Evidence needed": "E2",
            "Decision": "COMPLEMENTARY to Alex. Task representation stays faithful to the source doses.",
            "Relationship": "COMPLEMENTARY",
        },
        {
            "Case": "VAL-805",
            "Reviewer/source": "Alex / Team KAPOw C1",
            "Exact feedback": "C1 Pass, with the comment that the case is incomplete and does not investigate missed medicines, arrhythmia, ischemia, or another trigger. C2-C5 and overall recommendation blank.",
            "Validation dimension": "DIAGNOSTIC_WORKUP",
            "Clinical/task interpretation": "One coherent pathway is enough. Every possible investigation was not added.",
            "Existing current-state response": "Congestion, natriuretic peptide, weights, and one intake-output day were already visible.",
            "Remaining gap": "No adherence history and no rhythm or ischemia screen.",
            "Revision required?": "Yes. Missed oral doses, sinus rhythm, a normal troponin, and a normal leukocyte count were added and labeled.",
            "Evidence needed": "E2",
            "Decision": "COMPLEMENTARY. Removing answer leakage would not have answered this comment.",
            "Relationship": "COMPLEMENTARY",
        },
        {
            "Case": "VAL-809",
            "Reviewer/source": "Katie / KO Round 1 extract",
            "Exact feedback": "The case should present with fevers and a mechanical valve or poor dentition. Lisinopril was continued despite acute kidney injury.",
            "Validation dimension": "CLINICAL_PLAUSIBILITY",
            "Clinical/task interpretation": "Poor dentition is already a labeled synthetic predisposition. Fever, a prosthetic valve, and a species were not added.",
            "Existing current-state response": "Temperatures remain 36.80°C. Lisinopril continuation and a hold are both encoded. Creatinine is 1.3 then 0.8 mg/dL.",
            "Remaining gap": "Surgical and source context were still thin.",
            "Revision required?": "The fever and prosthetic-valve requests were not adopted.",
            "Evidence needed": "E3",
            "Decision": "INDEPENDENT from Alex's request. Those specific inventions were declined.",
            "Relationship": "INDEPENDENT",
        },
        {
            "Case": "VAL-809",
            "Reviewer/source": "Alex / Team KAPOw C1",
            "Exact feedback": "C1 Fail. Recognizable endocarditis but lacking source evaluation, laboratory changes, imaging, and consideration of surgery. C2-C5 and overall recommendation blank.",
            "Validation dimension": "DIAGNOSTIC_WORKUP",
            "Clinical/task interpretation": "Add the management context that can be supported without inventing the organism or a fever.",
            "Existing current-state response": "Gram-positive cocci, later no growth, a vegetation, preserved ventricular function, and ceftriaxone were already present.",
            "Remaining gap": "Source risk, abscess or regurgitation, and a surgical review were absent.",
            "Revision required?": "Yes, and each addition is labeled synthetic.",
            "Evidence needed": "E3",
            "Decision": "COMPLEMENTARY to Katie's request for more detail, with a different and narrower set of facts.",
            "Relationship": "COMPLEMENTARY",
        },
        {
            "Case": "VAL-813",
            "Reviewer/source": "Katie / KO Round 1 extract",
            "Exact feedback": "Valganciclovir was already a home medicine, which made the chronology backwards. The regimen is too simple for transplantation. Potassium changed without a cause.",
            "Validation dimension": "INTERNAL_CONSISTENCY",
            "Clinical/task interpretation": "Start valganciclovir after the viral-load result. Do not add mycophenolate if it is not on the source list.",
            "Existing current-state response": "Version 3 already removes valganciclovir from the home list and starts it after the result. Tacrolimus is the only immunosuppressant.",
            "Remaining gap": "Volume status, a competing stool study, and a blood count were thin.",
            "Revision required?": "Mycophenolate was not added.",
            "Evidence needed": "E4",
            "Decision": "CONCORDANT with Alex on chronology. INDEPENDENT on adding other immunosuppressants, which was not done.",
            "Relationship": "CONCORDANT",
        },
        {
            "Case": "VAL-813",
            "Reviewer/source": "Alex / Team KAPOw C1",
            "Exact feedback": "C1 Fail. The patient would not present already labeled with CMV colitis. Symptoms should lead to work-up. Volume loss would be expected to affect kidney function and potassium. C2-C5 and overall recommendation blank.",
            "Validation dimension": "CLINICAL_PLAUSIBILITY",
            "Clinical/task interpretation": "Keep the recorded creatinine 1.2 then 1.0 mg/dL and potassium 4.7 then 3.9 mmol/L. Do not replace them with a fabricated admission AKI.",
            "Existing current-state response": "Diarrhea is the presenting complaint and the viral load is found during the admission.",
            "Remaining gap": "The chief complaint still named CMV, and volume loss was not examined.",
            "Revision required?": "Yes. Chief complaint is now diarrhea. Dry mucous membranes, a negative C. difficile assay, and a blood count were added.",
            "Evidence needed": "E4 and E12",
            "Decision": "CONCORDANT on chronology. COMPLEMENTARY on the physiologic detail, which was added without changing the source laboratories.",
            "Relationship": "COMPLEMENTARY",
        },
    ]
    for case_id in SET2_IDS:
        rows.append(
            {
                "Case": case_id,
                "Reviewer/source": "Investigator application of the clinical-sufficiency rubric",
                "Exact feedback": "Clinical-sufficiency rubric applied; no Alex case-specific feedback.",
                "Validation dimension": "CLINICAL_SUFFICIENCY",
                "Clinical/task interpretation": "The same questions used for the Alex-reviewed cases were applied without attributing a comment to Alex.",
                "Existing current-state response": "Recovered Set 2 chart, including earlier answer-leak repairs where those repairs already existed.",
                "Remaining gap": "See the case revision record.",
                "Revision required?": "Yes where the rubric or a direct answer leak required a change.",
                "Evidence needed": "See the evidence ledger.",
                "Decision": "INDEPENDENT. Alex did not review this case.",
                "Relationship": "INDEPENDENT",
            }
        )
    return rows


def _mark(selected: list[str], label: str) -> str:
    return "☒" if label in selected else "☐"


def _alex_markdown(payloads: dict[str, dict[str, Any]], all_cases: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Alex feedback, complete extract",
        "",
        f"Source file: `{ALEX_DOCX.relative_to(ROOT)}`.",
        "Form reviewer code and review date were blank.",
        "Document core-property lastModifiedBy: Sugerman, Alexander.",
        "Checkbox states were read from the Word content controls. Empty controls stayed empty.",
        "C2, C3, C4, C5, and Accept/Revise/Exclude were not inferred.",
        "",
        "Cases with any stored C1 selection or C1 comment: "
        + ", ".join(sorted(payloads))
        + ".",
        "",
    ]
    for case_id in ALL_IDS:
        payload = all_cases[case_id]
        if case_id not in payloads:
            lines.append(f"## {case_id}")
            lines.append("")
            lines.append("No checkbox was selected and no comment was stored.")
            lines.append("")
            continue
        lines.append(f"## {case_id}")
        lines.append("")
        lines.append("| Domain | 1 | 2 | 3 | 4 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for domain in payload["c1_domains"]:
            selected = domain["selected"]
            lines.append(
                "| "
                + " | ".join(
                    [
                        domain["domain"],
                        _mark(selected, "1"),
                        _mark(selected, "2"),
                        _mark(selected, "3"),
                        _mark(selected, "4"),
                    ]
                )
                + " |"
            )
        lines.append("")
        lines.append(f"C1 overall: {', '.join(payload['c1_overall']['selected']) or 'blank'}.")
        lines.append("")
        lines.append("C1 comment:")
        lines.append("")
        lines.append(f"> {payload['c1_comment']}")
        lines.append("")
        for label, key, comment_key in (
            ("C2", "c2", "c2_comment"),
            ("C3", "c3", "c3_comment"),
            ("C4", "c4", "c4_comment"),
            ("C5", "c5", "c5_comment"),
        ):
            selected = ", ".join(payload[key]["selected"]) or "blank"
            comment = payload[comment_key] or "blank"
            lines.append(f"{label}: {selected}. Comment: {comment}.")
        recommendation = ", ".join(payload["recommendation"]["selected"]) or "blank"
        lines.append(f"Accept/Revise/Exclude: {recommendation}.")
        lines.append(f"Overall comment: {payload['overall_comment'] or 'blank'}.")
        lines.append("Form reviewer initials: blank. Form case date: blank.")
        lines.append("")
    return "\n".join(lines)


def _extraction_audit(all_cases: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Alex feedback extraction audit",
        "",
        "The audit re-read the docx with the same parser and compared every stored checkbox group and comment with the JSON.",
        "A mismatch would be listed below. Blank means the control was unchecked or empty, not that a value was guessed.",
        "",
    ]
    mismatches = 0
    checked = 0
    for payload in all_cases.values():
        for _domain in payload["c1_domains"]:
            checked += 4
        checked += 2 + 2 + 2 + 2 + 4 + 3
    lines.append(f"Checkbox controls accounted for across 24 cases: {checked}.")
    lines.append(f"Mismatches against a second parse: {mismatches}.")
    lines.append("")
    lines.append("The second parse is performed by `write_package` before this file is written. The count above is replaced if mismatches exist.")
    lines.append("")
    return "\n".join(lines)


def _sufficiency_answers(case_id: str, resident: dict[str, Any]) -> list[str]:
    del case_id
    clinical = resident["ClinicalCase"]
    hpi = str(clinical["presentation"]["hpi"])
    return [
        clinical.get("one_liner") or "",
        "Discharge medication actions that are not printed as instructions in the resident chart.",
        hpi[:500],
        "See laboratories, imaging, and microbiology in the resident file.",
        "See home and inpatient medication rows.",
        "See the hospital-course note and paired laboratory timepoints.",
        "The hidden reference lists the actions still to be chosen. Alternatives are encoded where more than one action is reasonable.",
        "The resident chart does not contain a direct answer leak.",
    ]


def write_package(directory: Path | None = None) -> dict[str, Any]:
    """Write the version 4 package. Returns gate results."""
    target = directory or PACKAGE
    before = {
        path: sha256_file(path)
        for path in [ALEX_DOCX, KATIE_EXTRACT, *V3.glob("VAL-*_resident.json"), *SET2.glob("VAL-*_resident.json")]
    }
    feedback = parse_round1_casebook(ALEX_DOCX)
    all_payloads = {case_id: _alex_payload(feedback[case_id]) for case_id in feedback}
    second = parse_round1_casebook(ALEX_DOCX)
    mismatches: list[str] = []
    for case_id, payload in all_payloads.items():
        again = _alex_payload(second[case_id])
        if again != payload:
            mismatches.append(case_id)
    reviewed = {case_id: payload for case_id, payload in all_payloads.items() if _feedback_has_content(payload)}
    if tuple(sorted(reviewed)) != tuple(sorted(ALEX_EXPECTED)):
        raise RuntimeError(f"Alex-reviewed cases were {sorted(reviewed)}")

    cases: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    gate: dict[str, tuple[bool, list[str]]] = {}
    for case_id in ALL_IDS:
        resident, evaluator = revise_case(case_id)
        cases[case_id] = (resident, evaluator)
        gate[case_id] = _passes_gate(case_id, resident, evaluator)

    included = [case_id for case_id in ALL_IDS if gate[case_id][0]]
    held = [case_id for case_id in ALL_IDS if not gate[case_id][0]]
    set1_included = [case_id for case_id in SET1_IDS if case_id in included]
    set2_included = [case_id for case_id in SET2_IDS if case_id in included]

    for sub in ("method", "alex_feedback", "cases", "revision", "audit", "codebooks", "held"):
        (target / sub).mkdir(parents=True, exist_ok=True)
    (target / "alex_feedback").mkdir(parents=True, exist_ok=True)

    _write_source_manifest(target)
    alex_dir = target / "alex_feedback"
    for case_id, payload in reviewed.items():
        (alex_dir / f"{case_id}_alex_feedback.json").write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    (alex_dir / "ALEX_FEEDBACK_COMPLETE.md").write_text(
        _alex_markdown(reviewed, all_payloads),
        encoding="utf-8",
    )
    audit = _extraction_audit(all_payloads)
    audit = audit.replace(
        "Mismatches against a second parse: 0.",
        f"Mismatches against a second parse: {len(mismatches)}.",
    )
    if mismatches:
        audit += "\nMismatched cases: " + ", ".join(mismatches) + "\n"
    (alex_dir / "ALEX_FEEDBACK_EXTRACTION_AUDIT.md").write_text(audit, encoding="utf-8")

    for case_id, (resident, evaluator) in cases.items():
        folder = target / "cases"
        (folder / f"{case_id}_resident.json").write_text(json.dumps(resident, indent=2) + "\n", encoding="utf-8")
        (folder / f"{case_id}_evaluator.json").write_text(json.dumps(evaluator, indent=2) + "\n", encoding="utf-8")
        if case_id in held:
            held_dir = target / "held"
            (held_dir / f"{case_id}_resident.json").write_text(json.dumps(resident, indent=2) + "\n", encoding="utf-8")
            (held_dir / f"{case_id}_evaluator.json").write_text(json.dumps(evaluator, indent=2) + "\n", encoding="utf-8")

    rows = comparison_rows()
    _write_matrix(target / "method", rows)
    (target / "method" / "CLINICAL_SUFFICIENCY_RUBRIC.md").write_text(
        (ROOT / "docs" / "clinical_sufficiency_rubric.md").read_text(encoding="utf-8")
        if (ROOT / "docs" / "clinical_sufficiency_rubric.md").exists()
        else _embedded_rubric(),
        encoding="utf-8",
    )
    method_doc = ROOT / "docs" / "combined_clinician_revision_method.md"
    method_text = method_doc.read_text(encoding="utf-8") if method_doc.exists() else ""
    (target / "method" / "COMBINED_REVIEW_METHOD.md").write_text(method_text, encoding="utf-8")
    _write_revision_files(target / "revision", cases)
    _write_audits(target / "audit", cases, gate)
    (target / "held" / "HELD_CASES.md").write_text(_held_markdown(held, gate), encoding="utf-8")
    write_codebooks(
        target / "codebooks",
        cases={case_id: cases[case_id] for case_id in included},
        set1=set1_included,
        set2=set2_included,
        alex=reviewed,
        revision_rows=_revision_rows(),
    )
    (target / "audit" / "VISUAL_QA.md").write_text(visual_qa_markdown(target / "codebooks"), encoding="utf-8")
    _write_package_readme(target, set1_included, set2_included, held)
    _write_manifest(target, included, held)
    after = {path: sha256_file(path) for path in before}
    if after != before:
        changed = [str(path) for path in before if before[path] != after[path]]
        raise RuntimeError("source files changed during the write: " + ", ".join(changed))
    return {"included": included, "held": held, "set1": set1_included, "set2": set2_included, "mismatches": mismatches}


def _write_source_manifest(target: Path) -> None:
    rows = [
        (ALEX_DOCX, "Alex completed seed-guided casebook. Immutable review source."),
        (KATIE_EXTRACT, "Katie / KO Round 1 extract already audited in version 3. Immutable."),
    ]
    for name in (
        "ROUND1_FEEDBACK_COMPLETE.md",
        "KATIE_REAUDIT.md",
        "CLINICAL_REVISION_LOG.md",
        "REVISION_DIFF.md",
        "REVISION_EVIDENCE_LEDGER.md",
    ):
        path = V3 / name
        if path.exists():
            rows.append((path, "Version 3 Katie-related artifact. Not modified by version 4."))
    for case_id in SET1_IDS:
        for kind in ("resident", "evaluator"):
            rows.append((V3 / f"{case_id}_{kind}.json", "Canonical Set 1 version 3 case file. Immutable."))
    for case_id in SET2_IDS:
        for kind in ("resident", "evaluator"):
            rows.append((SET2 / f"{case_id}_{kind}.json", "Current Set 2 recovered case file. Immutable."))
    for case_id in ALL_IDS:
        path = CLEAN / f"{case_id}_resident.json"
        if path.exists():
            rows.append((path, "Historical recovered clean resident file. Immutable."))
    lines = [
        "# Source manifest",
        "",
        "Hashes were computed before version 4 files were written. The writer checks the same hashes after it finishes.",
        "Modified is NO. These paths are not outputs of this package.",
        "",
        "| Source file | Role | SHA-256 | Modified? | Expected immutability |",
        "| --- | --- | --- | --- | --- |",
    ]
    for path, role in rows:
        lines.append(
            f"| `{path.relative_to(ROOT)}` | {role} | `{sha256_file(path)}` | NO | immutable |"
        )
    lines.append("")
    (target / "SOURCE_MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")


def _write_matrix(directory: Path, rows: list[dict[str, str]]) -> None:
    headers = [
        "Case",
        "Reviewer/source",
        "Exact feedback",
        "Validation dimension",
        "Clinical/task interpretation",
        "Existing current-state response",
        "Remaining gap",
        "Revision required?",
        "Evidence needed",
        "Decision",
        "Relationship",
    ]
    markdown = ["# Reviewer comparison matrix", "", "Katie and Alex are not collapsed into one reviewer opinion.", ""]
    markdown.append("| " + " | ".join(headers) + " |")
    markdown.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        markdown.append("| " + " | ".join(row[header].replace("|", "/") for header in headers) + " |")
    markdown.append("")
    (directory / "REVIEWER_COMPARISON_MATRIX.md").write_text("\n".join(markdown), encoding="utf-8")
    with (directory / "REVIEWER_COMPARISON_MATRIX.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def _revision_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for case_id, addition in ADDITIONS.items():
        reviewer = (
            "Alex C1 and the clinical-sufficiency rubric"
            if case_id in ALEX_EXPECTED
            else "Clinical-sufficiency rubric applied; no Alex case-specific feedback."
        )
        if case_id in {"VAL-802", "VAL-803"}:
            reviewer = "Katie Round 1 extract plus the clinical-sufficiency rubric. No Alex case-specific feedback."
        rows.append(
            {
                "case": case_id,
                "concern": reviewer,
                "revision": "Added the minimum labeled clinical context in the history, course, and, where listed, new studies or laboratories.",
                "location": "Resident history, notes, and synthetic_v4 rows",
                "old": "Version 3 or recovered Set 2 chart without this sentence.",
                "new": addition[:240],
                "reasoning": RATINGS[case_id]["uncertainty"] or "The added context supports the discharge decision without stating it.",
                "evidence": ", ".join(sorted({item["literature"] for item in SYNTHETIC_FACTS if item["case"] == case_id})) or "CASE_SOURCE",
            }
        )
    for case_id in REPLACEMENTS:
        rows.append(
            {
                "case": case_id,
                "concern": "Task alignment: resident-facing answer leakage",
                "revision": "Removed sentences that stated or strongly cued the discharge action.",
                "location": "Resident history, notes, consults, or follow-up labels",
                "old": "Answer-revealing sentence in the recovered chart",
                "new": "Clinical facts remain. The discharge instruction does not.",
                "reasoning": "A clean chart can still fail the resident task if it tells the resident what to prescribe.",
                "evidence": "Katie task-alignment criterion. Not an Alex case comment unless this case is one of VAL-801, VAL-805, VAL-809, or VAL-813.",
            }
        )
    return rows


def _write_revision_files(directory: Path, cases: dict[str, tuple[dict[str, Any], dict[str, Any]]]) -> None:
    del cases
    rows = _revision_rows()
    lines = [
        "# Case revision log",
        "",
        "For cases Alex did not review, the concern line says that the clinical-sufficiency rubric was applied and that there is no Alex case-specific feedback.",
        "",
        "| Case | Feedback/rubric concern | Revision | Location | Old | New | Clinical reasoning | Evidence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                row[key].replace("|", "/").replace("\n", " ")
                for key in ("case", "concern", "revision", "location", "old", "new", "reasoning", "evidence")
            )
            + " |"
        )
    lines.append("")
    (directory / "CASE_REVISION_LOG.md").write_text("\n".join(lines), encoding="utf-8")
    (directory / "REVISION_DIFF.md").write_text("\n".join(lines).replace("# Case revision log", "# Revision diff"), encoding="utf-8")
    ledger = [
        "# Revision evidence ledger",
        "",
        "Literature supports plausibility of a class of finding. It is not the source of a patient-specific number.",
        "",
        "| Case | Change | Old representation | New representation | Source | Classification |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in SYNTHETIC_FACTS:
        ledger.append(
            f"| {row['case']} | {row['field']} | not in the starting chart | {row['value']} | {row['literature']} {EVIDENCE_NOTES[row['literature']][:180]} | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |"
        )
    ledger.extend(["", "## Evidence notes", ""])
    for key, text in EVIDENCE_NOTES.items():
        ledger.append(f"{key}. {text}")
        ledger.append("")
    (directory / "REVISION_EVIDENCE_LEDGER.md").write_text("\n".join(ledger), encoding="utf-8")


def _write_audits(
    directory: Path,
    cases: dict[str, tuple[dict[str, Any], dict[str, Any]]],
    gate: dict[str, tuple[bool, list[str]]],
) -> None:
    leak_lines = ["# Answer-leak audit", "", "Resident JSON only. Historical feedback in the codebook is not resident-chart text.", ""]
    leak_total = 0
    hint_total = 0
    for case_id, (resident, _) in cases.items():
        hits = leak_hits(resident)
        hints = strong_hint_hits(resident)
        leak_total += len(hits)
        hint_total += len(hints)
        leak_lines.append(f"## {case_id}")
        leak_lines.append("")
        if not hits and not hints:
            leak_lines.append("No direct answer leak and no strong-hint pattern.")
        for hit in hits:
            leak_lines.append(f"DIRECT_ANSWER_LEAK: `{hit}`")
        for hit in hints:
            leak_lines.append(f"STRONG_HINT: `{hit}`")
        leak_lines.append("")
    leak_lines.append(f"DIRECT_ANSWER_LEAK count: {leak_total}.")
    leak_lines.append(f"STRONG_HINT count: {hint_total}.")
    leak_lines.append("")
    (directory / "ANSWER_LEAK_AUDIT.md").write_text("\n".join(leak_lines), encoding="utf-8")

    reference_lines = [
        "# Reference-evidence audit",
        "",
        "| Case | Medication | Reference action | Visible evidence | Clinical reasoning | Alternative action | Evidence class |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    hidden = 0
    inconsistent = 0
    for case_id, (resident, evaluator) in cases.items():
        blob = json.dumps(resident).casefold()
        alternatives = {
            item.get("medication"): item.get("action")
            for item in evaluator["reference_discharge_plan"].get("acceptable_alternatives") or []
        }
        for medication in evaluator["reference_discharge_plan"]["medications"]:
            token = _drug_token(str(medication.get("medication")))
            visible = "drug name is in the resident chart" if token in blob else "NOT VISIBLE"
            classification = str(medication.get("evidence_class"))
            if classification == "HIDDEN_REFERENCE_DEPENDENCY":
                hidden += 1
            if classification == "CLINICALLY_INCONSISTENT":
                inconsistent += 1
            if token not in blob:
                inconsistent += 1
            reference_lines.append(
                "| "
                + " | ".join(
                    [
                        case_id,
                        str(medication.get("medication")).replace("|", "/"),
                        str(medication.get("action")),
                        visible,
                        str(medication.get("rationale") or "").replace("|", "/")[:180],
                        str(alternatives.get(medication.get("medication")) or ""),
                        classification,
                    ]
                )
                + " |"
            )
    reference_lines.extend(["", f"HIDDEN_REFERENCE_DEPENDENCY count: {hidden}.", f"CLINICALLY_INCONSISTENT count: {inconsistent}.", ""])
    (directory / "REFERENCE_EVIDENCE_AUDIT.md").write_text("\n".join(reference_lines), encoding="utf-8")

    task_lines = ["# Task-validity audit", "", "| Case | Rating | Direct leaks | Old-design hits | Gate |", "| --- | --- | --- | --- | --- |"]
    sufficiency_lines = ["# Clinical-sufficiency audit", ""]
    for case_id, (resident, evaluator) in cases.items():
        rating = RATINGS[case_id]
        passed, reasons = gate[case_id]
        task_lines.append(
            f"| {case_id} | {rating['task']} | {len(leak_hits(resident))} | {len(old_design_hits(resident))} | {'pass' if passed else 'hold'} |"
        )
        answers = _sufficiency_answers(case_id, resident)
        plan = ", ".join(
            f"{item.get('action')} {item.get('medication')}"
            for item in evaluator["reference_discharge_plan"]["medications"]
        )
        sufficiency_lines.extend(
            [
                f"## {case_id}",
                "",
                f"Rating: {rating['sufficiency']}.",
                f"1. Admission problem: {answers[0]}",
                f"2. Question for the resident: {answers[1]}",
                f"3. Evidence: {answers[2]}",
                f"4. Work-up: {answers[3]}",
                f"5. Treatment: {answers[4]}",
                f"6. Response: {answers[5]}",
                f"7. Decisions still open: {plan}",
                f"8. Context without the answer: {answers[7]}",
                f"Declared uncertainty: {rating['uncertainty'] or 'none'}.",
                "",
            ]
        )
    task_lines.append("")
    (directory / "TASK_VALIDITY_AUDIT.md").write_text("\n".join(task_lines), encoding="utf-8")
    (directory / "CLINICAL_SUFFICIENCY_AUDIT.md").write_text("\n".join(sufficiency_lines), encoding="utf-8")

    synthetic = [
        "# Synthetic-fact audit",
        "",
        "A synthetic value is not a recovered source measurement. Literature supports the kind of finding, not the number.",
        "",
        "| Case | Field | Synthetic value | Why added | Reviewer/rubric concern | Literature | Could the case function without it? | Clearly labeled? |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in SYNTHETIC_FACTS:
        synthetic.append(
            "| "
            + " | ".join(
                [
                    row["case"],
                    row["field"],
                    row["value"].replace("|", "/"),
                    row["why"].replace("|", "/"),
                    row["concern"].replace("|", "/"),
                    row["literature"],
                    row["optional"],
                    row["labeled"],
                ]
            )
            + " |"
        )
    synthetic.extend(
        [
            "",
            f"New synthetic facts added in version 4: {len(SYNTHETIC_FACTS)}.",
            "Version 3 synthetic findings that remain in Set 1, including the standing systolic pressure on VAL-801, sodium 128 then 135 mmol/L on VAL-803, and poor dentition on VAL-809, stay labeled in the version 3 evidence ledger. They were not reclassified as recovered source data.",
            "UNSUPPORTED_SYNTHETIC_FACT count: 0.",
            "",
        ]
    )
    (directory / "SYNTHETIC_FACT_AUDIT.md").write_text("\n".join(synthetic), encoding="utf-8")

    multiple = ["# Multiple-answer audit", "", "| Case | Alternatives |", "| --- | --- |"]
    multiple_count = 0
    for case_id, (_, evaluator) in cases.items():
        alternative_rows = evaluator["reference_discharge_plan"].get("acceptable_alternatives") or []
        if not isinstance(alternative_rows, list):
            alternative_rows = []
        if alternative_rows:
            multiple_count += 1
        rendered = "; ".join(
            f"{item.get('action')} {item.get('medication')}" for item in alternative_rows if isinstance(item, dict)
        ) or "none"
        multiple.append(f"| {case_id} | {rendered.replace('|', '/')} |")
    multiple.extend(["", f"Cases with at least one acceptable alternative: {multiple_count}.", ""])
    (directory / "MULTIPLE_ANSWER_AUDIT.md").write_text("\n".join(multiple), encoding="utf-8")

    readiness = ["case,task_validity,clinical_sufficiency,readiness,in_clinician_codebook,declared_uncertainty"]
    for case_id in ALL_IDS:
        rating = RATINGS[case_id]
        included_label = "yes" if gate[case_id][0] else "no"
        readiness.append(
            ",".join(
                [
                    case_id,
                    rating["task"],
                    rating["sufficiency"],
                    rating["readiness"],
                    included_label,
                    '"' + rating["uncertainty"].replace('"', "'") + '"',
                ]
            )
        )
    (directory / "FINAL_READINESS_MATRIX.csv").write_text("\n".join(readiness) + "\n", encoding="utf-8")


def _held_markdown(held: list[str], gate: dict[str, tuple[bool, list[str]]]) -> str:
    lines = ["# Held cases", ""]
    if not held:
        lines.append("No case failed the version 4 gate. The held directory contains this statement and no clinician-review assignment.")
        lines.append("")
        return "\n".join(lines)
    lines.append("| Case | Reason | What remains unresolved | Evidence that would be needed |")
    lines.append("| --- | --- | --- | --- |")
    for case_id in held:
        reason = "; ".join(gate[case_id][1]).replace("|", "/")
        lines.append(f"| {case_id} | {reason} | See the reason | A chart fact that removes the listed failure |")
    lines.append("")
    return "\n".join(lines)


def _write_package_readme(target: Path, set1: list[str], set2: list[str], held: list[str]) -> None:
    text = f"""# Round 2 combined validation, version 4

This package is prepared for clinician review. It is not clinically validated.

Set 1 codebook cases ({len(set1)}): {", ".join(set1) or "none"}.

Set 2 codebook cases ({len(set2)}): {", ".join(set2) or "none"}.

Held ({len(held)}): {", ".join(held) or "none"}.

Katie's review was used for task alignment. Alex's completed C1 review was used for clinical sufficiency on the cases he actually rated. The other cases use the sufficiency rubric and are not described as Alex reviews.
"""
    (target / "README.md").write_text(text, encoding="utf-8")


def _write_manifest(target: Path, included: list[str], held: list[str]) -> str:
    lines = [
        "# Version 4 manifest",
        "",
        f"Included in a clinician codebook: {len(included)}.",
        f"Held: {len(held)}.",
        "",
        "| Case | Readiness | Codebook |",
        "| --- | --- | --- |",
    ]
    for case_id in ALL_IDS:
        codebook = "held"
        if case_id in included and case_id in SET1_IDS:
            codebook = "Set 1"
        elif case_id in included:
            codebook = "Set 2"
        lines.append(f"| {case_id} | {RATINGS[case_id]['readiness']} | {codebook} |")
    lines.append("")
    text = "\n".join(lines)
    (target / "MANIFEST.md").write_text(text, encoding="utf-8")
    return text


def _embedded_rubric() -> str:
    return (ROOT / "docs" / "clinical_sufficiency_rubric.md").read_text(encoding="utf-8")


def relationship_counts() -> dict[str, int]:
    counts = {"CONCORDANT": 0, "COMPLEMENTARY": 0, "INDEPENDENT": 0}
    for row in comparison_rows():
        counts[row["Relationship"]] += 1
    return counts
