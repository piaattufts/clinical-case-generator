"""Clinician-review packages for the recovered VAL-801–VAL-824 clean charts.

Set A revises six cases from clinician feedback. Set B packages the other
eighteen recovered charts without a clinical rewrite. Neither set reads the
historical injected charts, and neither overwrites the frozen VAL files.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from docx import Document

from app.services.word_controls import (
    append_checkbox,
    append_rich_text_field,
    finalize_word_form,
    prepare_form_document,
)

SOURCE_DIR = Path(__file__).resolve().parents[2] / "exports" / "clean_balanced_seed_set"
FROZEN_RESIDENT = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "case_sets"
    / "seed_guided"
    / "resident_validation_cases.json"
)

REVISED_IDS = (
    "VAL-801",
    "VAL-802",
    "VAL-803",
    "VAL-805",
    "VAL-809",
    "VAL-813",
)
REMAINING_IDS = (
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

Revision = tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], str]

SUFFICIENT = "SUFFICIENT_EVIDENCE"
WEAK = "WEAK_EVIDENCE"
HIDDEN = "HIDDEN_ANSWER_DEPENDENCY"
INCONSISTENT = "CLINICALLY_INCONSISTENT"
READY_REVIEW = "READY_FOR_CLINICIAN_REVIEW"
NOT_READY = "NOT_READY"
FRESH = "READY_FOR_FRESH_REVIEW"
NEEDS_FIX = "NEEDS_PRE_REVIEW_FIX"

_LEAKS = (
    "reference_discharge_plan",
    "exactly as listed",
    "clean_expected_state",
    "error_category",
    "error_family",
    "planted",
    "f1_",
    "f2_",
)


def write_ko_review_sets(revised_dir: Path, remaining_dir: Path) -> dict[str, Any]:
    """Write both review directories from the recovered clean export."""
    revised_dir.mkdir(parents=True, exist_ok=True)
    remaining_dir.mkdir(parents=True, exist_ok=True)
    revised_rows = [_write_revised(case_id, revised_dir) for case_id in REVISED_IDS]
    remaining_rows = [_write_remaining(case_id, remaining_dir) for case_id in REMAINING_IDS]
    _write_docx(
        revised_dir / "KO_REVISED_CASES_REVIEW.docx",
        "Revised cases for clinician review",
        revised_rows,
    )
    _write_docx(
        remaining_dir / "KO_REMAINING_CLEAN_CASES_REVIEW.docx",
        "Remaining clean cases for clinician review",
        remaining_rows,
    )
    (revised_dir / "AUDIT.md").write_text(_revised_audit(revised_rows), encoding="utf-8")
    (remaining_dir / "AUDIT.md").write_text(_remaining_audit(remaining_rows), encoding="utf-8")
    return {
        "revised": [row["case_id"] for row in revised_rows],
        "remaining": [row["case_id"] for row in remaining_rows],
        "revised_status": {row["case_id"]: row["status"] for row in revised_rows},
        "remaining_status": {row["case_id"]: row["status"] for row in remaining_rows},
    }


def _load_pair(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    resident = json.loads((SOURCE_DIR / f"{case_id}_resident.json").read_text(encoding="utf-8"))
    evaluator = json.loads(
        (SOURCE_DIR / f"{case_id}_evaluator.json").read_text(encoding="utf-8")
    )
    return resident, evaluator


def _write_revised(case_id: str, directory: Path) -> dict[str, Any]:
    resident, _evaluator = _load_pair(case_id)
    revised, reference, trace, summary = _REVISIONS[case_id](deepcopy(resident))
    _strip_resident_answers(revised)
    classes = [item["evidence_class"] for item in trace]
    status = READY_REVIEW
    if any(item in {HIDDEN, INCONSISTENT} for item in classes):
        status = NOT_READY
    evaluator = deepcopy(revised)
    evaluator["reference_discharge_plan"] = reference
    evaluator["evidence_trace"] = trace
    evaluator["clinician_review_status"] = status
    evaluator["revision_summary"] = summary
    _dump(directory, case_id, revised, evaluator)
    return {
        "case_id": case_id,
        "resident": revised,
        "evaluator": evaluator,
        "summary": summary,
        "status": status,
        "classes": classes,
    }


def _write_remaining(case_id: str, directory: Path) -> dict[str, Any]:
    resident, evaluator = _load_pair(case_id)
    resident = deepcopy(resident)
    evaluator = deepcopy(evaluator)
    _strip_resident_answers(resident)
    finding = _precheck(resident, evaluator)
    status = _remaining_status(finding)
    evaluator.pop("reference_discharge_plan", None)
    # Keep the recovered reference; do not rebuild it.
    source_eval = json.loads(
        (SOURCE_DIR / f"{case_id}_evaluator.json").read_text(encoding="utf-8")
    )
    evaluator = deepcopy(resident)
    evaluator["reference_discharge_plan"] = source_eval["reference_discharge_plan"]
    evaluator["clinician_review_status"] = status
    evaluator["precheck_finding"] = finding
    _dump(directory, case_id, resident, evaluator)
    return {
        "case_id": case_id,
        "resident": resident,
        "evaluator": evaluator,
        "finding": finding,
        "status": status,
        "summary": finding,
        "classes": [],
    }


def _dump(
    directory: Path,
    case_id: str,
    resident: dict[str, Any],
    evaluator: dict[str, Any],
) -> None:
    (directory / f"{case_id}_resident.json").write_text(
        json.dumps(resident, indent=2) + "\n",
        encoding="utf-8",
    )
    (directory / f"{case_id}_evaluator.json").write_text(
        json.dumps(evaluator, indent=2) + "\n",
        encoding="utf-8",
    )


def _strip_resident_answers(chart: dict[str, Any]) -> None:
    chart.pop("reference_discharge_plan", None)
    chart.pop("evidence_trace", None)
    chart.pop("clinician_review_status", None)
    chart.pop("revision_summary", None)
    chart.pop("precheck_finding", None)
    chart["CaseMedication"] = [
        row for row in chart.get("CaseMedication") or [] if row.get("context") != "discharge"
    ]
    chart["CaseInstruction"] = [
        row
        for row in chart.get("CaseInstruction") or []
        if "exactly as listed" not in (row.get("instruction_text") or "").casefold()
        and "was stopped during this admission"
        not in (row.get("instruction_text") or "").casefold()
    ]


def _precheck(resident: dict[str, Any], evaluator: dict[str, Any]) -> str:
    """Flag objective defects. Do not rewrite the chart to make them pass."""
    findings: list[str] = []
    blob = json.dumps(resident).casefold()
    for needle in _LEAKS:
        if needle in blob:
            findings.append(f"answer leakage:{needle}")
    if "reference_discharge_plan" not in evaluator:
        findings.append("unsupported:evaluator is missing the hidden reference plan")
    if "in this profile" in blob or "the discharge list is the intended" in blob:
        findings.append("answer leakage:resident narrative states an intended discharge list")
    if "resume when holding" in blob:
        findings.append(
            "answer leakage:an instruction directs the resident to resume a held medicine"
        )
    diagnoses = " ".join(
        (item.get("diagnosis") or "") for item in resident.get("CaseDiagnosis") or []
    ).casefold()
    admission = (resident.get("ClinicalCase") or {}).get("admission_dx") or ""
    medications = resident.get("CaseMedication") or []
    _precheck_stops(findings, medications, diagnoses)
    _precheck_volume(findings, resident, diagnoses)
    _precheck_regimen_claims(findings, blob, medications)
    _precheck_monitoring(findings, resident, medications)
    if "cytomegalo" in admission.casefold() and "prophylaxis" not in blob:
        if any(
            "valganciclovir" in (row.get("drug") or "").casefold() and row.get("context") == "home"
            for row in medications
        ):
            findings.append(
                "contradictory timeline:valganciclovir is already a home medicine while the "
                "admission is for CMV disease, and the chart does not describe prophylaxis"
            )
    if not findings:
        return "none"
    return "; ".join(dict.fromkeys(findings))


def _precheck_stops(
    findings: list[str],
    medications: list[dict[str, Any]],
    diagnoses: str,
) -> None:
    for row in medications:
        reason = (row.get("held_reason") or "").casefold()
        if reason != "stopped during this admission.":
            continue
        if any(token in diagnoses for token in ("bleed", "hemorrhage")):
            continue
        findings.append(f"unexplained stop:{row.get('drug')} has no clinical reason")


def _precheck_volume(
    findings: list[str],
    resident: dict[str, Any],
    diagnoses: str,
) -> None:
    if "heart failure" not in diagnoses:
        return
    for weight in resident.get("CaseWeight") or []:
        if not weight.get("dry_weight_kg") or weight.get("weight_kg") is None:
            continue
        actual = float(weight["weight_kg"])
        dry = float(weight["dry_weight_kg"])
        if actual > dry + 2:
            findings.append(
                f"inconsistent:discharge weight {actual:.0f} kg remains above "
                f"dry weight {dry:.0f} kg"
            )


def _named(
    medications: list[dict[str, Any]],
    token: str,
    context: str,
) -> dict[str, Any] | None:
    return next(
        (
            row
            for row in medications
            if token in (row.get("drug") or "").casefold() and row.get("context") == context
        ),
        None,
    )


def _same_regimen(left: dict[str, Any] | None, right: dict[str, Any] | None) -> bool:
    if left is None or right is None:
        return False
    return all(left.get(key) == right.get(key) for key in ("dose", "route", "frequency"))


def _precheck_regimen_claims(
    findings: list[str],
    blob: str,
    medications: list[dict[str, Any]],
) -> None:
    if "potassium repletion" in blob and not any(
        "potassium" in (row.get("drug") or "").casefold() for row in medications
    ):
        findings.append(
            "unsupported:hospital course describes potassium repletion but no potassium "
            "medication is listed"
        )
    if "diuretic plan was adjusted" in blob:
        if _same_regimen(
            _named(medications, "furosemide", "home"),
            _named(medications, "furosemide", "inpatient"),
        ):
            findings.append(
                "contradictory timeline:narrative says the diuretic plan was adjusted but "
                "the home and inpatient loop-diuretic regimens match"
            )
    if "tacrolimus" in blob and "dose adjustment" in blob:
        if _same_regimen(
            _named(medications, "tacrolimus", "home"),
            _named(medications, "tacrolimus", "inpatient"),
        ):
            findings.append(
                "contradictory timeline:narrative describes a tacrolimus dose adjustment "
                "but the home and inpatient doses match"
            )
    if "enoxaparin" in blob and _named(medications, "enoxaparin", "inpatient") is None:
        findings.append(
            "contradictory timeline:narrative describes enoxaparin but it is not on "
            "the medication list"
        )
    if "prior baseline" in blob and "baseline of" not in blob:
        findings.append(
            "unsupported:a restart instruction refers to a creatinine baseline that is "
            "not in the chart"
        )
    enoxaparin = _named(medications, "enoxaparin", "inpatient")
    if (
        enoxaparin is not None
        and "fibrillation" in (enoxaparin.get("indication") or "").casefold()
        and "prophylaxis" in blob
    ):
        findings.append(
            "indication mismatch:enoxaparin is labeled for atrial fibrillation while the "
            "narrative describes venous-thromboembolism prophylaxis"
        )


def _precheck_monitoring(
    findings: list[str],
    resident: dict[str, Any],
    medications: list[dict[str, Any]],
) -> None:
    warfarin = any("warfarin" in (row.get("drug") or "").casefold() for row in medications)
    inr_lab = any(
        "inr" in (row.get("test_name") or "").casefold() for row in resident.get("CaseLab") or []
    )
    inr_task = any(
        "inr" in (row.get("parameter") or "").casefold()
        for row in resident.get("CaseMonitoring") or []
    )
    if warfarin and not inr_lab:
        findings.append("inconsistent monitoring:warfarin is present without an INR result")
    if inr_task and not warfarin:
        findings.append("inconsistent monitoring:INR monitoring is present without warfarin")


def _remaining_status(finding: str) -> str:
    if finding == "none":
        return FRESH
    parts = [item.strip() for item in finding.split(";")]
    serious = (
        "inconsistent:",
        "contradictory timeline:",
        "unexplained",
        "inconsistent monitoring:",
    )
    if any(part.startswith(serious) for part in parts):
        return INCONSISTENT
    return NEEDS_FIX


def _set_text(chart: dict[str, Any], *, hpi: str, admission: str, course: str) -> None:
    chart["ClinicalCase"]["presentation"]["hpi"] = hpi
    chart["ClinicalCase"]["chief_complaint"] = chart["ClinicalCase"].get("chief_complaint")
    for note in chart.get("CaseNote") or []:
        if note.get("note_type") == "admission":
            note["note_text"] = admission
        elif note.get("note_type") == "hospital_course":
            note["note_text"] = course


def _meds(chart: dict[str, Any], drug_prefix: str) -> list[dict[str, Any]]:
    return [
        row
        for row in chart.get("CaseMedication") or []
        if (row.get("drug") or "").startswith(drug_prefix)
    ]


def _decision(
    chart: dict[str, Any],
    *,
    medication: str,
    action: str,
    indication: str,
    rationale: str,
    diagnosis: str,
    event: str,
    labs: str,
    vitals: str,
    history: str,
    location: str,
    phrases: list[str],
    dose: str | None = None,
    route: str | None = None,
    frequency: str | None = None,
    duration: str | None = None,
    monitoring: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    source: dict[str, Any] = next(
        (
            row
            for row in chart.get("CaseMedication") or []
            if row.get("drug") == medication and row.get("context") in {"inpatient", "home"}
        ),
        {},
    )
    plan = {
        "medication": medication,
        "action": action,
        "dose": dose if dose is not None else source.get("dose"),
        "route": route if route is not None else source.get("route"),
        "frequency": frequency if frequency is not None else source.get("frequency"),
        "duration": duration,
        "indication": indication,
        "rationale": rationale,
        "monitoring": monitoring,
        "required": action in {"continue", "start", "change", "restart"},
    }
    visible = json.dumps(
        {key: value for key, value in chart.items() if key != "reference_discharge_plan"}
    ).casefold()
    missing = [phrase for phrase in phrases if phrase.casefold() not in visible]
    if missing:
        evidence_class = HIDDEN
    else:
        evidence_class = SUFFICIENT
    trace = {
        "medication": medication,
        "action": action,
        "indication": indication,
        "supporting_diagnosis": diagnosis,
        "supporting_hospital_event": event,
        "supporting_labs": labs,
        "supporting_vitals": vitals,
        "supporting_medication_history": history,
        "rationale": rationale,
        "resident_visible_evidence_location": location,
        "evidence_class": evidence_class,
    }
    return plan, trace


def _plan_bundle(
    plans: list[dict[str, Any]],
    followups: list[dict[str, Any]],
    monitoring: list[dict[str, Any]] | None = None,
    alternatives: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "medications": plans,
        "medications_to_stop": [
            item["medication"] for item in plans if item["action"] == "stop"
        ],
        "acceptable_alternatives": alternatives or [],
        "contraindications": [],
        "monitoring_requirements": monitoring or [],
        "follow_up_requirements": [
            {
                "item": item.get("item"),
                "timing": item.get("timing"),
                "with_service": item.get("with_service"),
            }
            for item in followups
        ],
    }


def _revise_801(chart: dict[str, Any]) -> Revision:
    hpi = (
        "A 75-year-old man with diabetes, hypertension, and hyperlipidemia is admitted "
        "with confusion and fatigue for several days. He had been eating and drinking poorly. "
        "Home medicines are lisinopril, atorvastatin, metformin, and ibuprofen as needed for "
        "knee pain. There is no gastrointestinal bleeding, melena, or recent kidney injury."
    )
    admission = (
        "Admission note. Confusion and fatigue for several days, with poor oral intake. "
        "Mucous membranes are dry, and the orthostatic systolic pressure falls 20 mmHg from "
        "the recorded supine pressure of 136 mmHg. Collateral history later confirmed the "
        "home medication list, including ibuprofen for knee pain. No bleeding symptoms."
    )
    course = (
        "Delirium was attributed to dehydration from poor oral intake. Intravenous fluids "
        "and nutrition were given. Glucose fell from 163 mg/dL to 103 mg/dL as eating resumed; "
        "this was not a hyperosmolar state. Creatinine stayed 1.1 mg/dL then 1.0 mg/dL. "
        "Confusion cleared as intake improved. Knee pain was still present. No bleeding was "
        "found, and kidney function stayed stable."
    )
    _set_text(chart, hpi=hpi, admission=admission, course=course)
    for row in _meds(chart, "ibuprofen"):
        row["status"] = "home" if row.get("context") == "home" else "active"
        row["held_reason"] = None
        row["indication"] = "knee pain; not a treatment for the admission diagnosis"
    consults = chart.get("CaseConsult") or []
    if consults:
        consults[0]["assessment"] = (
            "Delirium improved after rehydration and the glucose fell from 163 mg/dL to 103 mg/dL."
        )
        consults[0]["recommendation"] = (
            "The collateral medication list was verified. No bleeding or kidney injury was found."
        )
    plans: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    specs: list[tuple[str, str, str, str, str, str, str, str, str, list[str]]] = [
        (
            "atorvastatin 40 MG Oral Tablet",
            "continue",
            "Mixed hyperlipidemia",
            "Hyperlipidemia is active and there is no statin intolerance.",
            "atorvastatin was confirmed on the collateral home list",
            "none required for this continuation",
            "none",
            "Home atorvastatin for mixed hyperlipidemia",
            "diagnoses; home medications",
            ["mixed hyperlipidemia", "atorvastatin"],
        ),
        (
            "lisinopril 10 MG Oral Tablet",
            "continue",
            "Essential (primary) hypertension",
            "Blood pressure remained adequate and creatinine did not rise.",
            "Confusion cleared as intake and glucose improved.",
            "creatinine stayed 1.1 mg/dL then 1.0 mg/dL",
            "discharge systolic blood pressure 121 mmHg",
            "Home lisinopril",
            "diagnoses; labs; vitals",
            ["lisinopril", "1.0", "hypertension"],
        ),
        (
            "metformin hydrochloride 500 MG Oral Tablet",
            "continue",
            "Type 2 diabetes mellitus without complications",
            "Glucose improved and kidney function remained stable.",
            "Glucose improved with fluids and nutrition.",
            "glucose fell from 163 mg/dL to 103 mg/dL",
            "none",
            "Home metformin",
            "diagnoses; labs",
            ["metformin", "103", "diabetes"],
        ),
        (
            "ibuprofen 400 MG Oral Tablet",
            "continue",
            "knee pain; not a treatment for the admission diagnosis",
            "No bleeding and stable creatinine, so the as-needed analgesic remains.",
            "no gastrointestinal bleeding",
            "creatinine 1.0 mg/dL",
            "none",
            "Home ibuprofen for knee pain",
            "history of present illness; hospital course; labs",
            ["ibuprofen", "knee pain", "no gastrointestinal bleeding"],
        ),
    ]
    for spec in specs:
        plan, trace = _decision(
            chart,
            medication=spec[0],
            action=spec[1],
            indication=spec[2],
            rationale=spec[3],
            diagnosis=spec[2],
            event=spec[4],
            labs=spec[5],
            vitals=spec[6],
            history=spec[7],
            location=spec[8],
            phrases=spec[9],
            duration=None,
        )
        plans.append(plan)
        traces.append(trace)
    reference = _plan_bundle(plans, chart.get("CaseFollowup") or [])
    summary = (
        "Delirium is attributed to dehydration from poor oral intake, with dry mucous "
        "membranes and an orthostatic drop. Glucose fell from 163 to 103 mg/dL as intake "
        "resumed and is not treated as the cause. Ibuprofen is continued for knee pain "
        "because the chart shows no bleeding and creatinine stays 1.1 then 1.0 mg/dL."
    )
    return chart, reference, traces, summary


def _add_lab(
    chart: dict[str, Any],
    *,
    lab_id: str,
    timepoint: str,
    test_name: str,
    value: float,
    unit: str,
) -> None:
    chart.setdefault("CaseLab", []).append(
        {
            "lab_id": lab_id,
            "case_id": chart["case_id_code"],
            "timepoint": timepoint,
            "test_name": test_name,
            "value": value,
            "value_text": None,
            "unit": unit,
            "status": "final",
            "source_reference": None,
        }
    )


def _revise_802(chart: dict[str, Any]) -> Revision:
    _add_lab(
        chart,
        lab_id="LAB-VAL802-K1",
        timepoint="admission",
        test_name="Potassium [Moles/volume] in Serum or Plasma",
        value=4.2,
        unit="mmol/L",
    )
    _add_lab(
        chart,
        lab_id="LAB-VAL802-K2",
        timepoint="discharge",
        test_name="Potassium [Moles/volume] in Serum or Plasma",
        value=4.1,
        unit="mmol/L",
    )
    hpi = (
        "An 81-year-old woman with hypertension and hyperlipidemia is admitted with two days "
        "of confusion. She had been drinking poorly. A clinic creatinine six weeks earlier was "
        "1.2 mg/dL. Home medicines are lisinopril and atorvastatin. There is no focal weakness."
    )
    admission = (
        "Admission note. Confusion for two days with poor oral intake. Outpatient creatinine "
        "was 1.2 mg/dL six weeks earlier. Home lisinopril and atorvastatin were confirmed "
        "from a collateral list."
    )
    course = (
        "Delirium was attributed to dehydration from poor oral intake. Intravenous fluids "
        "were given. Creatinine was 1.3 mg/dL on admission and 1.2 mg/dL at discharge, matching "
        "the recent baseline of 1.2 mg/dL. Potassium was 4.2 mmol/L then 4.1 mmol/L. Systolic "
        "blood pressure was 138 mmHg on admission and 124 mmHg at discharge. Confusion cleared "
        "after rehydration. Kidney function and potassium were back at the recent baseline, "
        "and the discharge systolic pressure was 124 mmHg."
    )
    _set_text(chart, hpi=hpi, admission=admission, course=course)
    plans = []
    traces = []
    for medication, indication, phrases, rationale, labs, vitals in (
        (
            "lisinopril 10 MG Oral Tablet",
            "Essential (primary) hypertension",
            ["lisinopril", "1.2 mg/dl", "4.1", "124"],
            "Creatinine returned to the documented baseline and potassium "
            "and blood pressure were acceptable.",
            "creatinine 1.3 then 1.2 mg/dL; potassium 4.2 then 4.1 mmol/L",
            "systolic blood pressure 124 mmHg at discharge",
        ),
        (
            "atorvastatin 40 MG Oral Tablet",
            "Mixed hyperlipidemia",
            ["atorvastatin", "hyperlipidemia"],
            "Hyperlipidemia remains active and no statin adverse effect is described.",
            "none required",
            "none",
        ),
    ):
        plan, trace = _decision(
            chart,
            medication=medication,
            action="continue",
            indication=indication,
            rationale=rationale,
            diagnosis=indication,
            event="Confusion cleared after rehydration.",
            labs=labs,
            vitals=vitals,
            history=f"Home {medication.split()[0]}",
            location="hospital course; labs; vitals; diagnoses",
            phrases=phrases,
        )
        plans.append(plan)
        traces.append(trace)
    summary = (
        "Delirium is attributed to poor intake and dehydration. Creatinine is interpreted "
        "against a stated baseline of 1.2 mg/dL, with potassium 4.1 mmol/L and discharge "
        "systolic pressure 124 mmHg. Lisinopril and atorvastatin stay on the reference "
        "plan. Atorvastatin was already on the recovered chart and is not re-omitted."
    )
    return chart, _plan_bundle(plans, chart.get("CaseFollowup") or []), traces, summary


def _revise_803(chart: dict[str, Any]) -> Revision:
    sodium = "Sodium [Moles/volume] in Serum or Plasma"
    _add_lab(
        chart,
        lab_id="LAB-VAL803-NA1",
        timepoint="admission",
        test_name=sodium,
        value=128,
        unit="mmol/L",
    )
    _add_lab(
        chart,
        lab_id="LAB-VAL803-NA2",
        timepoint="discharge",
        test_name=sodium,
        value=135,
        unit="mmol/L",
    )
    hpi = (
        "A 71-year-old man with hypertension, diabetes, and hyperlipidemia is admitted with "
        "one week of fatigue and confusion. Home medicines include hydrochlorothiazide, "
        "lisinopril, atorvastatin, and metformin. He has been drinking more water than usual "
        "and has no focal weakness."
    )
    admission = (
        "Admission note. Subacute confusion and fatigue. Hydrochlorothiazide is on the home "
        "list. Serum sodium on arrival is 128 mmol/L."
    )
    course = (
        "Delirium was attributed to thiazide-associated hyponatremia. Hydrochlorothiazide was "
        "held because the serum sodium was 128 mmol/L. Isotonic fluid was given. Sodium rose "
        "to 135 mmol/L and confusion cleared. Creatinine was 1.0 mg/dL then 1.2 mg/dL and "
        "potassium was 4.4 mmol/L then 4.2 mmol/L."
    )
    _set_text(chart, hpi=hpi, admission=admission, course=course)
    for row in _meds(chart, "hydrochlorothiazide"):
        row["status"] = "held"
        row["held_reason"] = (
            "Serum sodium 128 mmol/L on admission while taking hydrochlorothiazide."
        )
    plans = []
    traces = []
    stop_plan, stop_trace = _decision(
        chart,
        medication="hydrochlorothiazide 25 MG Oral Tablet",
        action="stop",
        indication="Essential (primary) hypertension",
        rationale="Sodium was 128 mmol/L on the thiazide and rose to 135 mmol/L after it was held.",
        diagnosis="Essential (primary) hypertension",
        event="Hydrochlorothiazide was held because the serum sodium was 128 mmol/L.",
        labs="sodium 128 mmol/L then 135 mmol/L",
        vitals="none",
        history="Home hydrochlorothiazide",
        location="hospital course; labs",
        phrases=["128 mmol/l", "135 mmol/l", "hydrochlorothiazide"],
    )
    plans.append(stop_plan)
    traces.append(stop_trace)
    for medication, indication, phrases in (
        (
            "lisinopril 10 MG Oral Tablet",
            "Essential (primary) hypertension",
            ["lisinopril", "4.2", "1.2"],
        ),
        (
            "atorvastatin 40 MG Oral Tablet",
            "Mixed hyperlipidemia",
            ["atorvastatin", "hyperlipidemia"],
        ),
        (
            "metformin hydrochloride 500 MG Oral Tablet",
            "Type 2 diabetes mellitus without complications",
            ["metformin", "diabetes"],
        ),
    ):
        plan, trace = _decision(
            chart,
            medication=medication,
            action="continue",
            indication=indication,
            rationale=(
                "This medicine was not implicated in the hyponatremia, and glucose, "
                "creatinine, and potassium remained acceptable."
            ),
            diagnosis=indication,
            event="Confusion cleared as the sodium rose to 135 mmol/L.",
            labs="creatinine 1.2 mg/dL; potassium 4.2 mmol/L",
            vitals="none",
            history=f"Home {medication.split()[0]}",
            location="diagnoses; hospital course; labs",
            phrases=phrases,
            duration="30 days",
        )
        plans.append(plan)
        traces.append(trace)
    summary = (
        "Delirium is attributed to thiazide-associated hyponatremia (sodium 128 mmol/L, "
        "later 135 mmol/L). Hydrochlorothiazide is stopped. Lisinopril supply stays the "
        "recovered 30-day clean value, not the old 7-day injected supply."
    )
    return chart, _plan_bundle(plans, chart.get("CaseFollowup") or []), traces, summary


def _revise_805(chart: dict[str, Any]) -> Revision:
    chart["CaseWeight"] = [
        {
            "weight_id": "WT-VAL805-001",
            "case_id": "VAL-805",
            "timepoint": "admission",
            "weight_kg": "86.000",
            "dry_weight_kg": None,
            "source_reference": None,
        },
        {
            "weight_id": "WT-VAL805-002",
            "case_id": "VAL-805",
            "timepoint": "hospital_day_2",
            "weight_kg": "83.000",
            "dry_weight_kg": None,
            "source_reference": None,
        },
        {
            "weight_id": "WT-VAL805-003",
            "case_id": "VAL-805",
            "timepoint": "discharge",
            "weight_kg": "80.000",
            "dry_weight_kg": "80.000",
            "source_reference": None,
        },
    ]
    chart["CaseIntakeOutput"] = [
        {
            "io_id": f"IO-VAL805-00{index}",
            "case_id": "VAL-805",
            "timepoint": f"hospital_day_{index}",
            "intake_ml": intake,
            "output_ml": output,
            "net_ml": intake - output,
            "notes": None,
            "source_reference": None,
        }
        for index, intake, output in ((1, 1100, 2800), (2, 1300, 2600), (3, 1500, 1900))
    ]
    chart.setdefault("CaseImaging", []).append(
        {
            "study_id": "IMG-VAL805-ECHO",
            "case_id": "VAL-805",
            "timepoint": "admission",
            "study_type": "Transthoracic echocardiogram",
            "body_site": "heart",
            "finding": "Left ventricular ejection fraction 30 percent. No valvular vegetation.",
            "source_reference": None,
        }
    )
    for row in _meds(chart, "furosemide"):
        if row.get("context") == "inpatient":
            row["route"] = "intravenous"
            row["frequency"] = "twice daily"
            row["notes"] = (
                "Intravenous furosemide 40 MG twice daily during volume overload. "
                "The home regimen was 40 MG orally once daily."
            )
    hpi = (
        "A 68-year-old woman with systolic heart failure and hyperlipidemia is admitted with "
        "one week of dyspnea, edema, and orthopnea. Home medicines are oral furosemide 40 MG "
        "once daily, metoprolol succinate 25 MG once daily, and atorvastatin. She is hypoxic "
        "and volume overloaded. Dry weight is 80 kg."
    )
    admission = (
        "Admission note. Acute decompensated heart failure. Weight 86 kg, above a dry weight "
        "of 80 kg. Oxygen saturation 92 percent. Home oral furosemide is not the inpatient dose."
    )
    course = (
        "Pulmonary edema was treated with intravenous furosemide 40 MG twice daily, which is "
        "distinct from the home oral 40 MG once daily. Intake and output were net negative on "
        "hospital days 1, 2, and 3. Weight fell from 86 kg to 83 kg and then to 80 kg, equal "
        "to the dry weight. Creatinine fell from 1.7 mg/dL to 0.9 mg/dL and potassium from "
        "4.7 mmol/L to 4.3 mmol/L. B-type natriuretic peptide fell from 1120 pg/mL to 369 pg/mL. "
        "Discharge systolic blood pressure was 110 mmHg and heart rate 69. Oxygen saturation "
        "was 92 percent on admission and 98 percent at discharge. Ejection fraction was 30 "
        "percent. The home list is oral furosemide, metoprolol succinate, and atorvastatin."
    )
    _set_text(chart, hpi=hpi, admission=admission, course=course)
    consults = chart.get("CaseConsult") or []
    if consults:
        consults[0]["assessment"] = (
            "Volume overload responded to intravenous diuresis. Ejection fraction is 30 percent. "
            "Discharge weight equals the 80 kg dry weight."
        )
        consults[0]["recommendation"] = (
            "Blood pressure at discharge is 110 mmHg systolic. Kidney function improved."
        )
    plans = []
    traces = []
    for medication, indication, phrases, rationale, event, labs, vitals in (
        (
            "furosemide 40 MG Oral Tablet",
            "Acute systolic (congestive) heart failure",
            ["intravenous furosemide", "80 kg", "dry weight"],
            "Congestion resolved and weight returned to the 80 kg dry weight, "
            "so the home oral 40 MG daily dose is resumed.",
            "Intravenous furosemide 40 MG twice daily, distinct from home oral therapy.",
            "creatinine 1.7 to 0.9 mg/dL; natriuretic peptide 1120 to 369 pg/mL",
            "oxygen saturation 98 percent at discharge",
        ),
        (
            "24 HR metoprolol succinate 25 MG Extended Release Oral Tablet",
            "Acute systolic (congestive) heart failure",
            ["ejection fraction 30", "110 mmhg", "heart rate 69"],
            "Ejection fraction is 30 percent, discharge heart rate is 69, "
            "and systolic pressure is 110 mmHg.",
            "Beta blocker was continued through diuresis.",
            "potassium 4.3 mmol/L",
            "systolic blood pressure 110 mmHg; heart rate 69",
        ),
        (
            "atorvastatin 40 MG Oral Tablet",
            "Mixed hyperlipidemia",
            ["atorvastatin", "hyperlipidemia"],
            "Hyperlipidemia is a separate active problem and no statin intolerance is described.",
            "none",
            "none",
            "none",
        ),
    ):
        plan, trace = _decision(
            chart,
            medication=medication,
            action="continue",
            indication=indication,
            rationale=rationale,
            diagnosis=indication,
            event=event,
            labs=labs,
            vitals=vitals,
            history=f"Home {medication.split()[0]}",
            location="hospital course; weights; labs; imaging",
            phrases=phrases,
            route="oral",
            frequency="once daily",
        )
        plans.append(plan)
        traces.append(trace)
    summary = (
        "The hospitalization is diuresis with intravenous furosemide, serial weights from "
        "86 kg to an 80 kg dry weight, and three days of negative intake and output. "
        "The reference plan resumes the home oral diuretic and beta blocker. No new "
        "guideline-directed class was added at a systolic pressure of 110 mmHg; a low-dose "
        "ACE inhibitor, ARB, or SGLT2 inhibitor is recorded only as an acceptable alternative."
    )
    alternatives = [
        {
            "medication": "ACE inhibitor, ARB, or SGLT2 inhibitor",
            "action": "start",
            "rationale": (
                "Ejection fraction is 30 percent and creatinine recovered to 0.9 mg/dL. "
                "The reference plan does not start one of these classes because none was "
                "a home medicine and the discharge systolic pressure is 110 mmHg. A reviewer "
                "may still accept a low-dose start."
            ),
        }
    ]
    return (
        chart,
        _plan_bundle(plans, chart.get("CaseFollowup") or [], alternatives=alternatives),
        traces,
        summary,
    )


def _revise_809(chart: dict[str, Any]) -> Revision:
    for vital in chart.get("CaseVital") or []:
        if vital.get("timepoint") == "admission":
            vital["temp_c"] = "38.60"
            vital["heart_rate"] = 104
            vital["resp_rate"] = 22
            vital["bp_systolic"] = 128
        elif vital.get("timepoint") == "discharge":
            vital["temp_c"] = "36.80"
            vital["heart_rate"] = 76
            vital["bp_systolic"] = 118
    _add_lab(
        chart,
        lab_id="LAB-VAL809-CR3",
        timepoint="hospital_day_3",
        test_name="Creatinine [Mass/volume] in Serum or Plasma",
        value=1.0,
        unit="mg/dL",
    )
    for row in chart.get("CaseMicrobiology") or []:
        if row.get("result") == "growth":
            row["organism"] = "Viridans group streptococcus"
            row["notes"] = (
                "Identified from the admission blood culture after a dental "
                "extraction three weeks earlier."
            )
    hpi = (
        "An 82-year-old man with hypertension and hyperlipidemia is admitted with one week of "
        "fever and fatigue. He had a dental extraction three weeks earlier. A new murmur is "
        "present. Home medicines are lisinopril and atorvastatin. Outpatient creatinine last "
        "month was 0.8 mg/dL."
    )
    admission = (
        "Admission note. Fever 38.6 C, heart rate 104, and a new murmur after a recent dental "
        "extraction. Blood cultures grew gram-positive cocci. Creatinine is 1.3 mg/dL, above "
        "the 0.8 mg/dL baseline."
    )
    course = (
        "Blood cultures grew Viridans group streptococcus. A transthoracic echocardiogram showed "
        "a vegetation. Ceftriaxone 2000 MG intravenously once daily was started. Later blood "
        "cultures showed no growth, and fever resolved. Acute kidney injury was attributed to "
        "the infection: creatinine 1.3 mg/dL on admission, 1.0 mg/dL on hospital day 3, and "
        "0.8 mg/dL at discharge. Lisinopril was held while creatinine was 1.3 mg/dL. At "
        "discharge the creatinine is 0.8 mg/dL and the systolic blood pressure is 118 mmHg."
    )
    _set_text(chart, hpi=hpi, admission=admission, course=course)
    for row in _meds(chart, "lisinopril"):
        if row.get("context") == "inpatient":
            row["status"] = "held"
            row["held_reason"] = "Held while creatinine was 1.3 mg/dL."
    consults = chart.get("CaseConsult") or []
    if consults:
        consults[0]["assessment"] = (
            "Endocarditis with a vegetation and Viridans group streptococcus bacteremia after "
            "a dental extraction. Fever has resolved and follow-up cultures show no growth."
        )
        consults[0]["recommendation"] = (
            "Four weeks of intravenous ceftriaxone is the planned course for viridans "
            "endocarditis with a vegetation. Kidney function has returned to the "
            "0.8 mg/dL baseline."
        )
    plans = []
    traces = []
    for medication, action, indication, phrases, rationale, event, labs, vitals in (
        (
            "ceftriaxone 2000 MG Injection",
            "start",
            "Acute and subacute infective endocarditis",
            ["ceftriaxone", "vegetation", "viridans"],
            "Started for endocarditis after a vegetation and streptococcal "
            "bacteremia were documented.",
            "Ceftriaxone was started during the admission.",
            "none",
            "fever resolved",
        ),
        (
            "lisinopril 10 MG Oral Tablet",
            "restart",
            "Essential (primary) hypertension",
            ["lisinopril was held", "0.8 mg/dl", "118"],
            "Held during the creatinine rise and restarted after creatinine returned to 0.8 mg/dL.",
            "Held while creatinine was 1.3 mg/dL.",
            "creatinine 1.3, then 1.0, then 0.8 mg/dL",
            "systolic blood pressure 118 mmHg",
        ),
        (
            "atorvastatin 40 MG Oral Tablet",
            "continue",
            "Mixed hyperlipidemia",
            ["atorvastatin", "hyperlipidemia"],
            "Hyperlipidemia is unchanged and no statin adverse effect is described.",
            "none",
            "none",
            "none",
        ),
    ):
        plan, trace = _decision(
            chart,
            medication=medication,
            action=action,
            indication=indication,
            rationale=rationale,
            diagnosis=indication,
            event=event,
            labs=labs,
            vitals=vitals,
            history="Home lisinopril and atorvastatin; ceftriaxone was not a home medicine",
            location="history of present illness; hospital course; labs; microbiology; imaging",
            phrases=phrases,
            duration="4 weeks" if medication.startswith("ceftriaxone") else None,
        )
        plans.append(plan)
        traces.append(trace)
    summary = (
        "Endocarditis is supported by fever, a recent dental extraction, viridans bacteremia, "
        "and a vegetation. Lisinopril was held at creatinine 1.3 mg/dL and restarted at 0.8 mg/dL."
    )
    monitoring = chart.get("CaseMonitoring") or []
    return chart, _plan_bundle(plans, chart.get("CaseFollowup") or [], monitoring), traces, summary


def _revise_813(chart: dict[str, Any]) -> Revision:
    tacrolimus = next(
        row for row in _meds(chart, "BX Rating tacrolimus") if row.get("context") == "home"
    )
    mycophenolate_home = deepcopy(tacrolimus)
    mycophenolate_home.update(
        {
            "medication_id": "MED-VAL813-MMF-H",
            "drug": "mycophenolate mofetil 500 MG Oral Tablet",
            "reported_name": "mycophenolate mofetil 500 MG Oral Tablet",
            "dose": "1000 MG",
            "route": "oral",
            "frequency": "twice daily",
            "indication": "Kidney transplant status",
            "status": "home",
            "context": "home",
            "notes": "Given as 500 MG tablets.",
            "held_reason": None,
        }
    )
    mycophenolate_inpatient = deepcopy(mycophenolate_home)
    mycophenolate_inpatient.update(
        {
            "medication_id": "MED-VAL813-MMF-I",
            "context": "inpatient",
            "status": "active",
        }
    )
    kept = []
    for row in chart.get("CaseMedication") or []:
        drug = (row.get("drug") or "").casefold()
        if "valganciclovir" in drug and row.get("context") == "home":
            continue
        kept.append(row)
    for row in kept:
        if "valganciclovir" in (row.get("drug") or "").casefold():
            row["notes"] = (
                "Started after the CMV viral load was detected during this admission. "
                "Given as 450 MG tablets. Not a pre-admission medicine."
            )
            row["indication"] = "Other cytomegaloviral diseases"
    chart["CaseMedication"] = [mycophenolate_home, mycophenolate_inpatient, *kept]
    hpi = (
        "A 64-year-old woman with a kidney transplant is admitted with several days of diarrhea. "
        "Maintenance immunosuppression is tacrolimus and mycophenolate. She also takes amlodipine "
        "for hypertension and atorvastatin for hyperlipidemia. She was not taking valganciclovir "
        "before this admission."
    )
    admission = (
        "Admission note. Diarrhea after kidney transplantation. Home immunosuppression is "
        "tacrolimus and mycophenolate. Valganciclovir is not a home medicine."
    )
    course = (
        "CMV viral load drawn after admission was detected, and valganciclovir was started "
        "only after that result, 900 MG twice daily given as 450 MG tablets. Diarrhea then "
        "improved, and a later viral-load review was lower than the admission result. "
        "Creatinine was 1.2 mg/dL then 1.0 mg/dL and potassium was 4.7 mmol/L then 3.9 mmol/L. "
        "Tacrolimus, mycophenolate, amlodipine, and atorvastatin were continued."
    )
    _set_text(chart, hpi=hpi, admission=admission, course=course)
    for consult in chart.get("CaseConsult") or []:
        if consult.get("service") == "infectious disease":
            consult["assessment"] = (
                "CMV viral load was detected after admission in a transplant "
                "recipient with diarrhea."
            )
            consult["recommendation"] = (
                "Antiviral therapy was begun after the viral-load result. Symptoms improved."
            )
        if consult.get("service") == "transplant":
            consult["assessment"] = (
                "Kidney transplant maintained on tacrolimus and mycophenolate."
            )
            consult["recommendation"] = (
                "Immunosuppression was kept active while the new antiviral was started."
            )
    plans = []
    traces = []
    start_plan, start_trace = _decision(
        chart,
        medication="valganciclovir 450 MG Oral Tablet",
        action="start",
        dose="900 MG",
        frequency="twice daily",
        indication="Other cytomegaloviral diseases",
        rationale="Started only after CMV viral load was detected during the admission.",
        diagnosis="Other cytomegaloviral diseases",
        event="Valganciclovir was started after the CMV viral load was detected.",
        labs="creatinine 1.0 mg/dL at discharge supports the labeled dose",
        vitals="none",
        history="Not a home medicine",
        location="history of present illness; hospital course; procedures",
        phrases=["not taking valganciclovir", "viral load", "started"],
    )
    plans.append(start_plan)
    traces.append(start_trace)
    for medication, indication, phrases in (
        (
            "BX Rating tacrolimus 1 MG Oral Capsule",
            "Kidney transplant status",
            ["tacrolimus", "transplant"],
        ),
        (
            "mycophenolate mofetil 500 MG Oral Tablet",
            "Kidney transplant status",
            ["mycophenolate", "transplant"],
        ),
        (
            "amlodipine 5 MG Oral Tablet",
            "Essential (primary) hypertension",
            ["amlodipine", "hypertension"],
        ),
        (
            "atorvastatin 40 MG Oral Tablet",
            "Mixed hyperlipidemia",
            ["atorvastatin", "hyperlipidemia"],
        ),
    ):
        plan, trace = _decision(
            chart,
            medication=medication,
            action="continue",
            indication=indication,
            rationale=(
                "This pre-admission medicine matches an active diagnosis "
                "and was not the new antiviral."
            ),
            diagnosis=indication,
            event="Immunosuppression and cardiovascular medicines were kept active.",
            labs="creatinine 1.2 then 1.0 mg/dL; potassium 3.9 mmol/L",
            vitals="discharge systolic blood pressure 134 mmHg",
            history=f"Home {medication.split()[0]}",
            location="diagnoses; history of present illness; labs",
            phrases=phrases,
        )
        plans.append(plan)
        traces.append(trace)
    summary = (
        "Chronology is corrected inside the same transplant/CMV scenario: diarrhea on "
        "tacrolimus and mycophenolate, CMV diagnosed after admission, and valganciclovir "
        "started only after the viral load. Not marked REPLACE_WITH_MATCHED_CASE."
    )
    return chart, _plan_bundle(plans, chart.get("CaseFollowup") or []), traces, summary


_REVISIONS = {
    "VAL-801": _revise_801,
    "VAL-802": _revise_802,
    "VAL-803": _revise_803,
    "VAL-805": _revise_805,
    "VAL-809": _revise_809,
    "VAL-813": _revise_813,
}


def _write_docx(path: Path, title: str, rows: list[dict[str, Any]]) -> None:
    document = Document()
    prepare_form_document(document)
    document.add_heading(title, 0)
    document.add_paragraph(
        "Read the resident-facing chart and complete the ratings before the clinician "
        "validation reference. That reference is not shown to residents."
    )
    document.add_paragraph(
        "These charts are clean clinical cases. The resident determines the discharge "
        "medication regimen from the chart."
    )
    for row in rows:
        _add_case(document, row)
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(path))
    finalize_word_form(path)


def _add_case(document: Any, row: dict[str, Any]) -> None:
    case_id = row["case_id"]
    chart = row["resident"]
    clinical = chart["ClinicalCase"]
    document.add_heading(f"CASE {case_id}", 1)
    document.add_paragraph(clinical.get("one_liner") or "")
    document.add_heading("Resident-facing chart", 2)
    presentation = clinical.get("presentation") or {}
    document.add_paragraph(presentation.get("hpi") or "")
    document.add_paragraph("Diagnoses: " + "; ".join(
        item.get("diagnosis") or "" for item in chart.get("CaseDiagnosis") or []
    ))
    for note in chart.get("CaseNote") or []:
        document.add_paragraph(f"{note.get('note_type')}: {note.get('note_text')}")
    document.add_paragraph("Medications (home and inpatient only):")
    for med in chart.get("CaseMedication") or []:
        document.add_paragraph(
            f"{med.get('context')}: {med.get('drug')} {med.get('dose')} {med.get('route')} "
            f"{med.get('frequency')}. Indication: {med.get('indication') or 'none'}. "
            f"Held reason: {med.get('held_reason') or 'none'}. "
            f"Notes: {med.get('notes') or 'none'}.",
            style="List Bullet",
        )
    document.add_paragraph("Vital signs:")
    for vital in chart.get("CaseVital") or []:
        document.add_paragraph(
            f"{vital.get('timepoint')}: blood pressure {vital.get('bp_systolic')}/"
            f"{vital.get('bp_diastolic')}, heart rate {vital.get('heart_rate')}, "
            f"respiratory rate {vital.get('resp_rate')}, temperature {vital.get('temp_c')}, "
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
            document.add_paragraph(
                f"{weight.get('timepoint')}: {weight.get('weight_kg')} kg"
                + (
                    f", dry weight {weight.get('dry_weight_kg')} kg"
                    if weight.get("dry_weight_kg")
                    else ""
                ),
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
        document.add_paragraph(
            f"Imaging, {imaging.get('study_type')}: {imaging.get('finding')}"
        )
    for consult in chart.get("CaseConsult") or []:
        document.add_paragraph(
            f"Consult, {consult.get('service')}: {consult.get('assessment')} "
            f"{consult.get('recommendation')}"
        )
    for micro in chart.get("CaseMicrobiology") or []:
        document.add_paragraph(
            f"Microbiology: {micro.get('test')} {micro.get('result')} "
            f"{micro.get('organism') or ''} "
            f"{micro.get('notes') or ''}"
        )
    for procedure in chart.get("CaseProcedure") or []:
        document.add_paragraph(
            f"Procedure, {procedure.get('time') or procedure.get('timepoint')}: "
            f"{procedure.get('procedure_name')}. {procedure.get('findings') or ''}"
        )
    for item in chart.get("CaseMonitoring") or []:
        document.add_paragraph(
            f"Monitoring: {item.get('parameter')} ({item.get('frequency')}), "
            f"{item.get('responsible_service') or ''}."
        )
    for item in chart.get("CaseInstruction") or []:
        document.add_paragraph(f"Instruction: {item.get('instruction_text')}")
    for follow in chart.get("CaseFollowup") or []:
        document.add_paragraph(
            f"Follow-up: {follow.get('item')} in {follow.get('timing')} "
            f"with {follow.get('with_service')}."
        )
    document.add_heading("Clinician ratings", 2)
    document.add_paragraph("Complete these ratings before reading the validation reference.")
    _c1(document, case_id)
    _yes_no(document, case_id, "C2", "Decision sufficiency", ("Pass", "Fail"))
    _comment(document, case_id, "c2-comment", "C2 comment if Fail")
    _yes_no(document, case_id, "C3", "Reference-plan validity", ("Pass", "Fail"))
    document.add_paragraph("Disputed medication, if any:")
    _comment(
        document,
        case_id,
        "c3-medication",
        "Disputed medication, action, suggested action, and reason",
    )
    _yes_no(
        document,
        case_id,
        "C4",
        "Alternative acceptable answers",
        ("No", "Yes"),
    )
    document.add_paragraph("Could another discharge regimen also reasonably be correct?")
    _comment(document, case_id, "c4-alternatives", "Acceptable alternatives if Yes")
    document.add_heading("C5 — Missing or misleading information", 3)
    document.add_paragraph(
        "Note missing information, contradictions, misleading statements, unrealistic "
        "medication behavior, inappropriate monitoring, or implausible hospital-course details."
    )
    _comment(document, case_id, "c5-comment", "C5 comments")
    _yes_no(
        document,
        case_id,
        "C6",
        "Resident-level appropriateness",
        (
            "Too easy",
            "Appropriate",
            "Challenging but appropriate",
            "Too difficult or inappropriate",
        ),
    )
    _yes_no(document, case_id, "overall", "Overall recommendation", ("Accept", "Revise", "Exclude"))
    _comment(document, case_id, "overall-comment", "Revision comments")
    document.add_heading("CLINICIAN VALIDATION REFERENCE", 2)
    document.add_paragraph("Not shown to residents in the assessment study.")
    document.add_paragraph("Complete the ratings above before using this reference.")
    reference = row["evaluator"]["reference_discharge_plan"]
    for item in reference.get("medications") or []:
        document.add_paragraph(
            f"{item.get('action')}: {item.get('medication')} {item.get('dose')} "
            f"{item.get('route')} {item.get('frequency')}. "
            f"Duration: {item.get('duration') or 'not specified'}. "
            f"Indication: {item.get('indication')}. Rationale: {item.get('rationale')}. "
            f"Monitoring: {item.get('monitoring') or 'see chart'}.",
            style="List Bullet",
        )
    for item in reference.get("acceptable_alternatives") or []:
        document.add_paragraph(
            f"Acceptable alternative: {item.get('action')} {item.get('medication')}. "
            f"{item.get('rationale')}",
            style="List Bullet",
        )
    for item in reference.get("follow_up_requirements") or []:
        document.add_paragraph(
            f"Reference follow-up: {item.get('item')} in {item.get('timing')} "
            f"with {item.get('with_service')}.",
            style="List Bullet",
        )
    for item in row["evaluator"].get("evidence_trace") or []:
        document.add_paragraph(
            f"Evidence for {item.get('medication')}: {item.get('evidence_class')}. "
            f"{item.get('supporting_hospital_event')} {item.get('supporting_labs')} "
            f"Visible in {item.get('resident_visible_evidence_location')}.",
            style="List Bullet",
        )


def _c1(document: Any, case_id: str) -> None:
    document.add_heading("C1 — Clinical plausibility", 3)
    document.add_paragraph(
        "1 = implausible; 2 = substantial revision required; 3 = plausible with minor concern; "
        "4 = fully plausible."
    )
    domains = (
        "presentation",
        "diagnosis",
        "hospital course",
        "laboratory findings",
        "vital signs",
        "medication history",
        "inpatient treatment",
        "discharge context",
        "overall consistency",
    )
    for domain in domains:
        paragraph = document.add_paragraph(f"{domain}: ")
        for score in ("1", "2", "3", "4"):
            paragraph.add_run(f" {score} ")
            append_checkbox(
                paragraph,
                document,
                tag=f"{case_id}-c1-{domain}-{score}",
                alias=f"{case_id} C1 {domain} {score}",
            )


def _yes_no(document: Any, case_id: str, code: str, prompt: str, choices: tuple[str, ...]) -> None:
    document.add_heading(f"{code} — {prompt}", 3)
    paragraph = document.add_paragraph()
    for choice in choices:
        paragraph.add_run(choice + " ")
        append_checkbox(
            paragraph,
            document,
            tag=f"{case_id}-{code}-{choice}",
            alias=f"{case_id} {code} {choice}",
        )


def _comment(document: Any, case_id: str, tag: str, label: str) -> None:
    table = document.add_table(rows=1, cols=1)
    append_rich_text_field(
        table.cell(0, 0),
        document,
        tag=f"{case_id}-{tag}",
        alias=label,
        lines=3,
    )


def _revised_audit(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Revised seed-guided cases",
        "",
        "Built from the recovered clean charts. Historical frozen files were not edited.",
        "",
        "| Case | Original issue | Revision made | Reference plan rebuilt | "
        "Evidence sufficient | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    issues = {
        "VAL-801": "Delirium unexplained; ibuprofen stopped without a reason",
        "VAL-802": "Delirium unexplained; creatinine and lisinopril hard to interpret",
        "VAL-803": "Delirium unexplained; little discharge decision-making",
        "VAL-805": "Heart-failure course too thin for a diuretic and GDMT decision",
        "VAL-809": "Endocarditis and AKI not convincing; lisinopril continued through AKI",
        "VAL-813": "Valganciclovir already a home medicine before CMV was diagnosed",
    }
    for row in rows:
        sufficient = (
            "yes"
            if row["classes"] and all(item == SUFFICIENT for item in row["classes"])
            else "no"
        )
        lines.append(
            "| {case} | {issue} | {revision} | yes | {sufficient} | {status} |".format(
                case=row["case_id"],
                issue=issues[row["case_id"]],
                revision=row["summary"].replace("|", "/"),
                sufficient=sufficient,
                status=row["status"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def _remaining_audit(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Remaining recovered clean cases",
        "",
        "These charts were not rewritten. Each file starts from the recovered clean export.",
        "",
        "| Case | Clean source recovered | Error mutation absent | "
        "Answer leakage absent | Precheck finding | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        resident = row["resident"]
        blob = json.dumps(resident).casefold()
        mutation_absent = (
            "no"
            if "exactly as listed" in blob
            or any(
                item.get("context") == "discharge" for item in resident.get("CaseMedication") or []
            )
            else "yes"
        )
        leakage_absent = "no" if "answer leakage" in row["finding"] else "yes"
        lines.append(
            f"| {row['case_id']} | yes | {mutation_absent} | {leakage_absent} | "
            f"{row['finding'].replace('|', '/')} | {row['status']} |"
        )
    lines.append("")
    return "\n".join(lines)
