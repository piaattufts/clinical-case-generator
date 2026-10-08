"""Apply the frozen revision framework to the twenty clean cases.

Does not modify CLEAN_BASE, the four overlap revisions, or revision_framework.md.
"""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
from typing import Any

from app.services.validation_casebook import (
    PreparedCase,
    _start_case_section,
    _write_validation,
)
from app.services.word_controls import finalize_word_form, prepare_form_document
from app.services.word_export import _add_body, _add_heading, _new_document, _render_case

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "case_sets" / "seed_guided" / "CLEAN_BASE"
OUT = ROOT / "data" / "case_sets" / "seed_guided" / "REVISED" / "remaining_20"
CODEBOOK = ROOT / "docs" / "validation" / "CliniProof_Revised_Remaining20_Codebook.docx"
CSV_PATH = ROOT / "docs" / "revision" / "revision_framework_application.csv"
LOG_PATH = ROOT / "docs" / "revision" / "remaining_20_revision_log.md"
NO_COMMENT = "Framework-guided investigator revision; no case-specific clinician feedback."
REVIEWER_PLUS = (
    "Framework-guided investigator revision, plus Reviewer 1 case-specific comments "
    "recorded separately."
)
STATUS = "FRAMEWORK-REVISED AND READY FOR CLINICIAN REVIEW"
DOMAINS = (
    "presentation_diagnosis_coherence",
    "causal_context",
    "diagnostic_workup",
    "treatment_trajectory",
    "laboratory_vital_trend",
    "hospital_course_completeness",
    "medication_decision_support",
    "discharge_stability_chronology",
    "internal_consistency",
    "unsupported_hidden_reference_action",
)


class Finding:
    def __init__(self, problem: bool, evidence: str, revision: str = "none") -> None:
        self.problem = problem
        self.evidence = evidence
        self.revision = revision if problem else "none"

    @property
    def required(self) -> bool:
        return self.problem


def _load(case_id: str) -> dict[str, Any]:
    payload: Any = json.loads((CLEAN / f"{case_id}_resident.json").read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(case_id)
    return payload


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _med(case: dict[str, Any], drug_name: str, context: str) -> dict[str, Any]:
    needle = drug_name.casefold()
    for row in case["CaseMedication"]:
        if isinstance(row, dict) and row.get("context") == context and needle in str(row.get("drug")).casefold():
            return row
    raise KeyError(f"{case['case_id_code']} missing {context} {drug_name}")


def _drop_med(case: dict[str, Any], drug_name: str, context: str) -> None:
    needle = drug_name.casefold()
    case["CaseMedication"] = [
        row
        for row in case["CaseMedication"]
        if not (
            isinstance(row, dict)
            and row.get("context") == context
            and needle in str(row.get("drug")).casefold()
        )
    ]


def _add_med(case: dict[str, Any], template: dict[str, Any], **changes: Any) -> dict[str, Any]:
    row = copy.deepcopy(template)
    row.update(changes)
    case["CaseMedication"].append(row)
    return row


def _add_lab(
    case: dict[str, Any],
    *,
    lab_id: str,
    timepoint: str,
    test_name: str,
    value: float | None,
    unit: str | None,
    value_text: str | None = None,
) -> None:
    template = copy.deepcopy(case["CaseLab"][0]) if case["CaseLab"] else {
        "lab_id": lab_id,
        "case_id": case["case_id_code"],
        "status": "final",
        "source_reference": None,
    }
    template.update(
        {
            "lab_id": lab_id,
            "case_id": case["case_id_code"],
            "timepoint": timepoint,
            "test_name": test_name,
            "value": value,
            "value_text": value_text,
            "unit": unit,
            "status": "final",
            "source_reference": None,
        }
    )
    case["CaseLab"].append(template)


def _set_lab(case: dict[str, Any], timepoint: str, test_start: str, value: float) -> None:
    for row in case["CaseLab"]:
        if row.get("timepoint") == timepoint and str(row.get("test_name")).startswith(test_start):
            row["value"] = value
            return
    raise KeyError(f"{case['case_id_code']} {timepoint} {test_start}")


def _vital(case: dict[str, Any], timepoint: str) -> dict[str, Any]:
    for row in case["CaseVital"]:
        if isinstance(row, dict) and row.get("timepoint") == timepoint:
            return row
    raise KeyError(timepoint)


def _story(
    case: dict[str, Any],
    *,
    one_liner: str,
    complaint: str,
    admission_dx: str,
    hpi: str,
    admission_note: str,
    course: str,
) -> None:
    clinical = case["ClinicalCase"]
    clinical["one_liner"] = one_liner
    clinical["chief_complaint"] = complaint
    clinical["admission_dx"] = admission_dx
    clinical["presentation"]["chief_complaint"] = complaint
    clinical["presentation"]["hpi"] = hpi
    case["CaseNote"][0]["note_text"] = admission_note
    case["CaseNote"][-1]["note_text"] = course


def _consult(
    case: dict[str, Any],
    service: str,
    assessment: str,
    recommendation: str,
    consult_id: str,
) -> None:
    for row in case["CaseConsult"]:
        if str(row.get("service")) == service:
            row["assessment"] = assessment
            row["recommendation"] = recommendation
            return
    case["CaseConsult"].append(
        {
            "consult_id": consult_id,
            "case_id": case["case_id_code"],
            "service": service,
            "timepoint": "inpatient",
            "assessment": assessment,
            "recommendation": recommendation,
            "source_reference": None,
        }
    )


def _imaging(case: dict[str, Any], study_id: str, study_type: str, finding: str, body: str) -> None:
    row: dict[str, Any] = {
        "study_id": study_id,
        "case_id": case["case_id_code"],
        "timepoint": "inpatient",
        "study_type": study_type,
        "body_site": body,
        "finding": finding,
        "source_reference": None,
    }
    if case["CaseImaging"]:
        case["CaseImaging"][0].update(
            {"study_type": study_type, "finding": finding, "body_site": body, "study_id": study_id}
        )
    else:
        case["CaseImaging"] = [row]


def _ref(
    medication: str,
    action: str,
    dose: str,
    frequency: str,
    indication: str,
    rationale: str,
    *,
    route: str | None = None,
) -> dict[str, Any]:
    inferred = route
    if inferred is None:
        lowered = medication.casefold()
        inferred = "intravenous" if "injection" in lowered else "subcutaneous" if "enoxaparin" in lowered else "oral"
    return {
        "medication": medication,
        "action": action,
        "dose": dose,
        "route": inferred,
        "frequency": frequency,
        "duration": None,
        "indication": indication,
        "rationale": rationale,
        "monitoring": None,
    }


def _wrap(
    resident: dict[str, Any],
    reference: dict[str, Any],
    facts: list[dict[str, str]],
    *,
    statement: str,
    reviewer_note: str | None,
) -> dict[str, Any]:
    evaluator = copy.deepcopy(resident)
    evaluator["reference_discharge_plan"] = reference
    evaluator["revision_provenance"] = {
        "status": STATUS,
        "clinically_validated": False,
        "framework": "docs/revision/revision_framework.md",
        "baseline": f"data/case_sets/seed_guided/CLEAN_BASE/{resident['case_id_code']}_resident.json",
        "statement": statement,
        "reviewer_1_comment": reviewer_note,
        "synthetic_facts": facts,
    }
    return evaluator


def _fail(evidence: str, revision: str) -> Finding:
    return Finding(True, evidence, revision)


def _pass(evidence: str) -> Finding:
    return Finding(False, evidence)


def _delirium_baseline(case: dict[str, Any], diagnosis_id: str) -> None:
    history = list(case["ClinicalCase"]["medical_history"])
    if "Mild major neurocognitive disorder" not in history:
        history.insert(0, "Mild major neurocognitive disorder")
    case["ClinicalCase"]["medical_history"] = history
    case["CaseDiagnosis"].append(
        {
            **case["CaseDiagnosis"][0],
            "diagnosis_id": diagnosis_id,
            "diagnosis": "Mild major neurocognitive disorder",
            "diagnosis_type": "past_history",
            "status": "active",
            "context": "baseline",
        }
    )
    case["CaseDiagnosis"][0]["diagnosis"] = "Acute delirium, a change from the caregiver-reported baseline"


def revise_802(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _delirium_baseline(case, "DX-VAL802-005")
    _story(
        case,
        one_liner="81-year-old woman with acute delirium from a urinary infection, now back to baseline",
        complaint="New confusion, worse than baseline",
        admission_dx="Acute delirium, a change from baseline",
        hpi=(
            "An 81-year-old woman with mild major neurocognitive disorder is admitted for two days "
            "of confusion that her caregiver says is worse than baseline. At baseline she recognizes "
            "family. Temperature is 37.9 C. Urinalysis shows leukocyte esterase, and the urine culture "
            "grows Escherichia coli. She finishes five days of nitrofurantoin 100 mg orally twice daily "
            "before discharge. Outpatient creatinine is 1.1 mg/dL, admission creatinine is 1.3 mg/dL, "
            "and discharge creatinine is 1.2 mg/dL. That small change is not treated as acute kidney "
            "injury. A pharmacy list confirms lisinopril 10 mg daily and atorvastatin 40 mg daily. "
            "Neither is stopped. There is no statin adverse effect on the chart. Confusion is back "
            "to the caregiver's baseline at discharge, and she is afebrile."
        ),
        admission_note=(
            "Acute confusion above the caregiver's baseline. Temperature 37.9 C. Creatinine 1.3 mg/dL "
            "against an outpatient value of 1.1 mg/dL. Lisinopril and atorvastatin are continued."
        ),
        course=(
            "Escherichia coli urinary infection. Nitrofurantoin 100 mg twice daily for five days "
            "was completed in the hospital and is not continued. The verified statin and lisinopril "
            "stay active. Creatinine at discharge is 1.2 mg/dL."
        ),
    )
    _vital(case, "admission")["temp_c"] = "37.90"
    _add_lab(case, lab_id="LAB-VAL802-003", timepoint="outpatient_baseline", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=1.1, unit="mg/dL")
    _add_lab(case, lab_id="LAB-VAL802-004", timepoint="admission", test_name="Urinalysis", value=None, unit=None, value_text="Leukocyte esterase positive.")
    case["CaseMicrobiology"] = [{
        "micro_id": "MICRO-VAL802-001", "case_id": "VAL-802", "timepoint": "admission",
        "specimen": "urine", "test": "urine culture", "organism": "Escherichia coli",
        "result": "growth", "quantity": None, "status": "final",
        "notes": "Treated with a completed five-day nitrofurantoin course.", "source_reference": None,
    }]
    _add_med(
        case, _med(case, "atorvastatin", "inpatient"),
        medication_id="MED-VAL802-005", context="inpatient", drug="nitrofurantoin 100 MG Oral Capsule",
        reported_name="nitrofurantoin 100 MG Oral Capsule", dose="100 MG", route="oral",
        frequency="twice daily", indication="Urinary tract infection", status="discontinued",
        notes="Five days completed before discharge. Not a discharge medicine.",
    )
    _consult(
        case, "geriatrics",
        "Acute delirium has returned to the caregiver-reported baseline.",
        "Continue the verified lisinopril and atorvastatin. Do not prescribe nitrofurantoin after discharge.",
        "CON-VAL802-001",
    )
    findings = {
        "presentation_diagnosis_coherence": _fail("Arrival label was delirium due to a known physiological condition, with no baseline.", "Added a caregiver-reported baseline and named the admission as a change from it."),
        "causal_context": _fail("The course said confusion improved and named no precipitant.", "Added a urinary infection with fever, pyuria, and Escherichia coli."),
        "diagnostic_workup": _fail("No urinalysis or culture was on the chart.", "Added both."),
        "treatment_trajectory": _fail("No acute treatment was recorded.", "Added a five-day nitrofurantoin course that finishes before discharge."),
        "laboratory_vital_trend": _fail("Creatinine moved from 1.3 to 1.2 mg/dL with no baseline.", "Added an outpatient creatinine of 1.1 mg/dL so the change is small."),
        "hospital_course_completeness": _fail("Reviewer 1 noted that nothing appeared to happen during the stay.", "The course now records the culture, the completed antibiotic, and the return to baseline."),
        "medication_decision_support": _fail("The statin was discussed without a visible continue-or-stop decision.", "The pharmacy list confirms atorvastatin and lisinopril, and neither is stopped."),
        "discharge_stability_chronology": _fail("Recovery was asserted without a baseline to recover to.", "Discharge is afebrile and back to the stated baseline, after the antibiotic has finished."),
        "internal_consistency": _pass("Home and inpatient rows already listed both chronic medicines as active. The new sentences match those rows."),
        "unsupported_hidden_reference_action": _fail("A continue action for the statin was not readable as a decision.", "The reference still continues both chronic medicines, now because the chart says they were verified and not stopped. Nitrofurantoin is stopped because the course is complete."),
    }
    reference = {
        "medications": [
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Verified on the pharmacy list. Creatinine 1.2 mg/dL is close to the 1.1 mg/dL baseline. The geriatrics note says to continue it."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "The collateral pharmacy list confirms it. No adverse effect is described. The note says it was not stopped."),
            _ref("nitrofurantoin 100 MG Oral Capsule", "stop", "100 MG", "twice daily", "Urinary tract infection", "Five days were completed before discharge."),
        ],
        "monitoring_requirements": [],
        "follow_up_requirements": [{"item": "Primary care medication-list follow-up", "timing": "5 days", "with_service": "primary care"}],
    }
    facts = [
        {"fact": "Caregiver-reported cognitive baseline and a temperature of 37.9 C.", "why": "Delirium was not shown as a change from baseline.", "evidence": "DSM-5-TR defines delirium as a change from baseline."},
        {"fact": "Pyuria, Escherichia coli, and nitrofurantoin 100 mg orally twice daily for five completed days.", "why": "No precipitant or hospital treatment was visible.", "evidence": "Gupta K et al. Clin Infect Dis. 2011;52:e103-e120. IDSA lists nitrofurantoin 100 mg twice daily for five days for uncomplicated cystitis. Estimated creatinine clearance from the chart's age, weight, and creatinine is above 30 mL/min."},
        {"fact": "Outpatient creatinine 1.1 mg/dL.", "why": "Reviewer 1 said the baseline creatinine was missing.", "evidence": "The admission and discharge values were already on the clean chart."},
    ]
    note = (
        "Reviewer 1 said the delirium label was not coherent, the cause was missing, little happened "
        "in the hospital, baseline creatinine was missing, and the statin seemed not to be continued. "
        "The clean chart had no seven-day statin stop. The revision makes continuation explicit rather "
        "than adding a stop."
    )
    return _wrap(case, reference, facts, statement=REVIEWER_PLUS, reviewer_note=note), findings, (
        "VAL-802 was the same empty delirium label as VAL-801, with Reviewer 1's additional points "
        "about baseline creatinine and the statin. The infection and the creatinine baseline were added. "
        "The statin and lisinopril continue because the verified list and the small creatinine change support that."
    )


def revise_803(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _delirium_baseline(case, "DX-VAL803-007")
    _story(
        case,
        one_liner="71-year-old man with acute delirium and a creatinine rise on hydrochlorothiazide",
        complaint="New confusion, worse than baseline",
        admission_dx="Acute delirium, a change from baseline",
        hpi=(
            "A 71-year-old man with mild major neurocognitive disorder is admitted for a week of "
            "fatigue and confusion that his family says is new. Fever is 38.0 C. Urine culture grows "
            "Escherichia coli. He completes seven days of ceftriaxone 1 g intravenously once daily "
            "before discharge and leaves on no antibiotic. Outpatient creatinine is 1.0 mg/dL and "
            "discharge creatinine is 1.2 mg/dL while he is on hydrochlorothiazide and lisinopril and "
            "has been eating poorly. Potassium stays 4.2 to 4.4 mmol/L. Blood pressure at discharge "
            "is 123/70 mm Hg. Hydrochlorothiazide is stopped at discharge because of the creatinine "
            "rise and poor intake. Lisinopril is continued. Metformin and atorvastatin are continued. "
            "He is back to his family's reported baseline and afebrile."
        ),
        admission_note="New confusion. Temperature 38.0 C. Creatinine 1.0 mg/dL at baseline and 1.2 mg/dL now. Hydrochlorothiazide is the drug paired with that rise.",
        course="The urinary infection was treated to completion. Hydrochlorothiazide is not restarted. Lisinopril continues, with a creatinine check at follow-up.",
    )
    _vital(case, "admission")["temp_c"] = "38.00"
    _add_lab(case, lab_id="LAB-VAL803-007", timepoint="outpatient_baseline", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=1.0, unit="mg/dL")
    _set_lab(case, "admission", "Creatinine", 1.0)
    _set_lab(case, "discharge", "Creatinine", 1.2)
    case["CaseMicrobiology"] = [{
        "micro_id": "MICRO-VAL803-001", "case_id": "VAL-803", "timepoint": "admission",
        "specimen": "urine", "test": "urine culture", "organism": "Escherichia coli",
        "result": "growth", "quantity": None, "status": "final", "notes": None, "source_reference": None,
    }]
    hctz = _med(case, "hydrochlorothiazide", "inpatient")
    hctz["status"] = "discontinued"
    hctz["held_reason"] = "Stopped because creatinine rose from 1.0 to 1.2 mg/dL during poor intake."
    _add_med(
        case, _med(case, "lisinopril", "inpatient"),
        medication_id="MED-VAL803-009", context="inpatient", drug="ceftriaxone 1000 MG Injection",
        reported_name="ceftriaxone 1000 MG Injection", dose="1000 MG", route="intravenous",
        frequency="once daily", indication="Urinary tract infection", status="discontinued",
        notes="Seven days completed before discharge.",
    )
    _consult(
        case, "geriatrics",
        "Delirium has cleared to the reported baseline. Creatinine rose on a thiazide.",
        "Do not restart hydrochlorothiazide at discharge. Continue lisinopril and recheck creatinine. The antibiotic course is finished.",
        "CON-VAL803-001",
    )
    findings = {
        "presentation_diagnosis_coherence": _fail("The admission label was delirium due to a known physiological condition.", "Named a baseline and an acute change."),
        "causal_context": _fail("No cause was stated.", "Added a urinary infection."),
        "diagnostic_workup": _fail("No culture was recorded.", "Added a urine culture."),
        "treatment_trajectory": _fail("No acute treatment was recorded.", "Added a completed seven-day ceftriaxone course."),
        "laboratory_vital_trend": _fail("Creatinine rose from 1.0 to 1.2 mg/dL and was not tied to a medicine.", "The rise is now the reason hydrochlorothiazide stops. A separate outpatient baseline of 1.0 mg/dL matches the admission value already stored."),
        "hospital_course_completeness": _fail("The course said he returned to baseline without saying from what.", "The course now includes the infection and the diuretic stop."),
        "medication_decision_support": _fail("Reviewer 1 said the medication list required no decision.", "Stopping hydrochlorothiazide is the decision. Lisinopril is not given a seven-day limit, because that limit is not on the clean chart."),
        "discharge_stability_chronology": _fail("Baseline cognition was missing.", "Discharge is afebrile and back to the stated baseline."),
        "internal_consistency": _pass("Potassium and blood pressure were already stable and still support continuing lisinopril."),
        "unsupported_hidden_reference_action": _fail("The clean reference continued hydrochlorothiazide despite the creatinine rise Reviewer 1 flagged.", "The reference now stops hydrochlorothiazide and continues lisinopril, metformin, and atorvastatin."),
    }
    reference = {
        "medications": [
            _ref("hydrochlorothiazide 25 MG Oral Tablet", "stop", "25 MG", "once daily", "Hypertension", "Creatinine rose from 1.0 to 1.2 mg/dL during poor intake. The geriatrics note says not to restart it."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Blood pressure is 123/70 mm Hg and potassium is 4.2 mmol/L. The rise in creatinine is attributed to the thiazide and poor intake. No seven-day supply limit is on the chart."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Glucose fell from 149 to 129 mg/dL and he is eating. Creatinine 1.2 mg/dL does not by itself stop it on this chart."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued through the stay. No adverse effect is described."),
            _ref("ceftriaxone 1000 MG Injection", "stop", "1000 MG", "once daily", "Urinary tract infection", "Seven days were completed before discharge."),
        ],
        "monitoring_requirements": [{"parameter": "serum creatinine", "frequency": "at primary care within 14 days", "target": None, "duration": "after the thiazide stop"}],
        "follow_up_requirements": [{"item": "Home-health and primary care medication-supply follow-up, including creatinine", "timing": "14 days", "with_service": "primary care"}],
    }
    facts = [
        {"fact": "Cognitive baseline, temperature 38.0 C, urine culture, and a completed ceftriaxone course.", "why": "The delirium label and the missing cause are the same defect as VAL-801, and this patient is a man, so a short nitrofurantoin course was not used.", "evidence": "Ceftriaxone labeling lists 1 to 2 g once daily. DSM-5-TR requires a change from baseline."},
        {"fact": "The decision to stop hydrochlorothiazide because creatinine rose from 1.0 to 1.2 mg/dL.", "why": "Reviewer 1 said the creatinine change might be the clinically relevant medication issue, and that the list otherwise had no decision.", "evidence": "The two creatinine values were already on the clean chart."},
    ]
    note = (
        "Reviewer 1 said the delirium label and cause were unclear, the list posed no discharge change, "
        "and asked why lisinopril would be limited to seven days. The clean chart has no seven-day "
        "lisinopril supply. That limit was not added. The creatinine rise was used as the real decision."
    )
    return _wrap(case, reference, facts, statement=REVIEWER_PLUS, reviewer_note=note), findings, (
        "VAL-803 keeps the verified chronic list and uses the existing creatinine rise to stop hydrochlorothiazide. "
        "The infection supplies the missing cause of delirium. Lisinopril is not restricted to seven days."
    )


def revise_804(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _delirium_baseline(case, "DX-VAL804-005")
    _story(
        case,
        one_liner="70-year-old woman whose acute delirium cleared after hyponatremia was corrected",
        complaint="One day of confusion, worse than baseline",
        admission_dx="Acute delirium, a change from baseline",
        hpi=(
            "A 70-year-old woman with mild major neurocognitive disorder is admitted after one day "
            "of confusion her family says is new. She had been eating and drinking poorly. Sodium is "
            "128 mmol/L on arrival and 136 mmol/L at discharge after intravenous fluid. Glucose falls "
            "from 155 to 108 mg/dL. No infection is found on the urinalysis. Confusion returns to "
            "baseline. Atorvastatin and metformin are continued. A cognitive-enhancer is not started. "
            "Neurology will reconsider that start in 14 days. The discharge list does not add one."
        ),
        admission_note="Acute confusion. Sodium 128 mmol/L. Urinalysis without leukocyte esterase.",
        course="Sodium corrected to 136 mmol/L and attention returned to baseline. No cognitive enhancer was started.",
    )
    _add_lab(case, lab_id="LAB-VAL804-003", timepoint="admission", test_name="Sodium [Moles/volume] in Serum or Plasma", value=128.0, unit="mmol/L")
    _add_lab(case, lab_id="LAB-VAL804-004", timepoint="discharge", test_name="Sodium [Moles/volume] in Serum or Plasma", value=136.0, unit="mmol/L")
    _add_lab(case, lab_id="LAB-VAL804-005", timepoint="admission", test_name="Urinalysis", value=None, unit=None, value_text="Leukocyte esterase negative.")
    _consult(
        case, "neurology",
        "Delirium has cleared after the sodium was corrected. Baseline is a mild major neurocognitive disorder.",
        "Do not start a cognitive enhancer at discharge. Reassess that question in clinic in 14 days. Continue metformin and atorvastatin.",
        "CON-VAL804-001",
    )
    case["CaseFollowup"][0]["item"] = "Reassess whether a cognitive enhancer should be started"
    findings = {
        "presentation_diagnosis_coherence": _fail("The chart used the non-specific delirium label and no baseline.", "Added the baseline and called the admission a change from it."),
        "causal_context": _fail("A pending cognitive-therapy sentence was not a cause of the confusion.", "Hyponatremia from poor intake is the precipitant, and it corrected."),
        "diagnostic_workup": _fail("No study explained the confusion.", "Added sodium values and a negative urinalysis."),
        "treatment_trajectory": _fail("No corrective treatment was shown.", "Intravenous fluid is the treatment, and the sodium rose."),
        "laboratory_vital_trend": _fail("Glucose was the only laboratory pair.", "Added the sodium pair that carries the decision."),
        "hospital_course_completeness": _fail("The course said a start was deferred and did not say what happened to the confusion.", "The course now ends at baseline after the sodium correction."),
        "medication_decision_support": _fail("The deferred cognitive enhancer was not separated from the medicines that should continue.", "Neurology says not to start an enhancer now, and to continue metformin and atorvastatin."),
        "discharge_stability_chronology": _fail("Discharge readiness was not tied to a corrected value.", "Sodium is 136 mmol/L and confusion has cleared."),
        "internal_consistency": _pass("The two home medicines were already active in both contexts."),
        "unsupported_hidden_reference_action": _pass("Continuing atorvastatin and metformin was already supported by active inpatient rows and is restated. No enhancer is added to the reference."),
    }
    reference = {
        "medications": [
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued during the stay. Neurology says to continue it."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Glucose fell from 155 to 108 mg/dL. Neurology says to continue it."),
        ],
        "monitoring_requirements": [],
        "follow_up_requirements": [{"item": "Reassess whether a cognitive enhancer should be started", "timing": "14 days", "with_service": "neurology"}],
    }
    facts = [{
        "fact": "Sodium 128 mmol/L corrected to 136 mmol/L, a negative urinalysis, and a decision not to start a cognitive enhancer.",
        "why": "The clean chart deferred a new medicine without explaining the delirium.",
        "evidence": "Acute hyponatremia is a recognized precipitant of delirium. The enhancer is not started because the chart assigns that decision to the upcoming visit.",
    }]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, (
        "VAL-804 keeps the pending neurology decision and supplies the missing cause of the delirium. "
        "No cognitive enhancer is placed on the discharge reference."
    )


def _hf_ischemia_negative(case: dict[str, Any], prefix: str) -> None:
    _add_lab(case, lab_id=f"LAB-{prefix}-T1", timepoint="admission", test_name="Troponin I.cardiac [Mass/volume] in Serum or Plasma", value=14.0, unit="ng/L")
    _add_lab(case, lab_id=f"LAB-{prefix}-T2", timepoint="six_hours_later", test_name="Troponin I.cardiac [Mass/volume] in Serum or Plasma", value=12.0, unit="ng/L")
    case["CaseImaging"].append({
        "study_id": f"STUDY-{prefix}-ECG",
        "case_id": case["case_id_code"],
        "timepoint": "admission",
        "study_type": "Electrocardiogram",
        "body_site": "heart",
        "finding": "Sinus rhythm. No ischemic ST-segment change.",
        "source_reference": None,
    })
    case["CaseImaging"].append({
        "study_id": f"STUDY-{prefix}-ECHO",
        "case_id": case["case_id_code"],
        "timepoint": "inpatient",
        "study_type": "Transthoracic echocardiogram",
        "body_site": "heart",
        "finding": "Left ventricular ejection fraction 30 percent. No new severe valvular lesion.",
        "source_reference": None,
    })


def revise_806(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hf_ischemia_negative(case, "VAL806")
    _story(
        case,
        one_liner="82-year-old woman with heart-failure congestion and a creatinine rise; lisinopril stays held",
        complaint="Dyspnea and edema",
        admission_dx="Acute systolic heart failure",
        hpi=(
            "An 82-year-old woman with systolic heart failure is admitted with several days of dyspnea "
            "and edema after missing three days of furosemide. She has no chest pain. Troponin does not "
            "rise and the electrocardiogram shows no ischemic change. Ejection fraction is 30 percent. "
            "Admission oxygen saturation is 89 percent on 2 L/min nasal cannula and is 96 percent on "
            "room air at discharge. Outpatient creatinine is 1.4 mg/dL, admission creatinine is 2.8 mg/dL, "
            "and discharge creatinine is 1.6 mg/dL. Lisinopril was held on admission and is still held "
            "because creatinine has not returned to baseline. Furosemide 40 mg was given intravenously "
            "twice daily until weight fell from 78 kg to 73 kg, at a dry weight of 74 kg, and the "
            "intravenous doses have stopped. Resume furosemide 40 mg orally once daily. Continue "
            "metoprolol succinate and atorvastatin. Do not restart lisinopril today."
        ),
        admission_note="Congestion after missed diuretic doses. Creatinine 2.8 mg/dL, baseline 1.4 mg/dL. Lisinopril held. Oxygen 2 L/min.",
        course="Intravenous diuresis reached dry weight. Creatinine improved only to 1.6 mg/dL. Lisinopril remains held for the visit in 3 days.",
    )
    _vital(case, "admission")["oxygen_support"] = "2 L/min nasal cannula"
    _vital(case, "discharge")["oxygen_support"] = "room air"
    _add_lab(case, lab_id="LAB-VAL806-005", timepoint="outpatient_baseline", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=1.4, unit="mg/dL")
    furosemide = _med(case, "furosemide", "inpatient")
    furosemide["drug"] = "furosemide 40 MG Injection"
    furosemide["dose"] = "40 MG"
    furosemide["route"] = "intravenous"
    furosemide["frequency"] = "twice daily"
    furosemide["status"] = "discontinued"
    furosemide["notes"] = "Stopped once weight was 73 kg, at the 74 kg dry weight."
    _consult(
        case, "cardiology",
        "Congestion after missed oral furosemide. Ischemia is not supported. Creatinine has not returned to 1.4 mg/dL.",
        "Resume furosemide 40 mg orally once daily. Do not restart lisinopril until creatinine is nearer the outpatient baseline. Continue metoprolol succinate and atorvastatin.",
        "CON-VAL806-001",
    )
    findings = {
        "presentation_diagnosis_coherence": _pass("Acute systolic heart failure matches the dyspnea, edema, and chest radiograph already on the chart."),
        "causal_context": _fail("The chart said creatinine rose with congestion and did not say why the congestion started.", "Three missed days of furosemide are the precipitant. Ischemia was looked for and not found."),
        "diagnostic_workup": _fail("No electrocardiogram, troponin, or ejection fraction was recorded.", "Added a flat troponin pair, a non-ischemic electrocardiogram, and an ejection fraction of 30 percent."),
        "treatment_trajectory": _fail("Inpatient furosemide was the same oral dose as the home medicine.", "Intravenous furosemide was given until dry weight and then stopped."),
        "laboratory_vital_trend": _fail("Lisinopril was to be restarted after renal recovery, but discharge creatinine was 1.6 mg/dL with no baseline.", "Baseline is 1.4 mg/dL. Discharge creatinine is still above it, so the hold continues."),
        "hospital_course_completeness": _fail("Only one intake-and-output day was listed, and hypoxia had no oxygen device.", "The weight pair already showed the diuresis. Oxygen support is now recorded. The single net-negative day is kept."),
        "medication_decision_support": _fail("Restarting lisinopril was not supported by the discharge creatinine.", "Cardiology says not to restart it today and to resume oral furosemide."),
        "discharge_stability_chronology": _pass("Discharge weight 73 kg is at the recorded dry weight of 74 kg, and oxygen saturation is 96 percent on room air."),
        "internal_consistency": _fail("The narrative promised a restart after recovery while the discharge creatinine was still high.", "The narrative and the reference now both keep lisinopril held."),
        "unsupported_hidden_reference_action": _fail("The clean reference restarted lisinopril.", "The reference now holds lisinopril and continues the other three home medicines."),
    }
    reference = {
        "medications": [
            _ref("furosemide 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Systolic heart failure", "Intravenous doses have stopped at dry weight. Cardiology says to resume 40 mg orally once daily. The precipitant was missed doses."),
            _ref("lisinopril 10 MG Oral Tablet", "hold", "10 MG", "once daily", "Hypertension and systolic heart failure", "Held because creatinine is 1.6 mg/dL against a baseline of 1.4 mg/dL. Cardiology says not to restart it today."),
            _ref("24 HR metoprolol succinate 25 MG Extended Release Oral Tablet", "continue", "25 MG", "once daily", "Systolic heart failure", "Continued through the stay. Heart rate at discharge is 67. Cardiology says to continue it."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued. Cardiology says to continue it."),
        ],
        "monitoring_requirements": [{"parameter": "serum creatinine", "frequency": "at the cardiology visit in 3 days", "target": "near the 1.4 mg/dL baseline before lisinopril restarts", "duration": None}],
        "follow_up_requirements": [{"item": "Cardiology follow-up to reassess held lisinopril", "timing": "3 days", "with_service": "cardiology"}],
    }
    facts = [
        {"fact": "Three missed furosemide days, a flat troponin, and an ejection fraction of 30 percent.", "why": "The decompensation had no cause and no ischemic evaluation.", "evidence": "Heidenreich PA et al. Circulation. 2022;145:e895-e1032."},
        {"fact": "Intravenous furosemide until dry weight, and a baseline creatinine of 1.4 mg/dL.", "why": "The oral dose had been copied into the hospital, and the restart lacked a baseline.", "evidence": "The same guideline recommends intravenous loop diuretic for admitted fluid overload. The hold follows the discharge creatinine still being above baseline."},
    ]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, (
        "VAL-806 keeps lisinopril held. The discharge creatinine has not returned to baseline, so the clean reference's restart was not kept."
    )


def revise_807(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hf_ischemia_negative(case, "VAL807")
    _story(
        case,
        one_liner="60-year-old man with heart-failure diuresis and a transient fall in potassium",
        complaint="Dyspnea and orthopnea",
        admission_dx="Acute systolic heart failure",
        hpi=(
            "A 60-year-old man with systolic heart failure is admitted with two days of dyspnea and "
            "orthopnea after missing two doses of furosemide. There is no chest pain. Troponin does "
            "not rise. Ejection fraction is 30 percent. Weight is 99 kg on admission and the dry weight "
            "is 95 kg. Furosemide 40 mg intravenously twice daily is given until the weight is 95 kg, "
            "then stopped. Potassium is 3.5 mmol/L on admission, 3.2 mmol/L on hospital day 2, and "
            "3.8 mmol/L at discharge after one 40 mEq oral potassium chloride dose. That dose is not "
            "continued. Creatinine stays 1.2 mg/dL. Resume furosemide 40 mg orally once daily. "
            "Continue metoprolol succinate and atorvastatin. He is on room air at discharge."
        ),
        admission_note="Congestion after two missed diuretic doses. Weight 99 kg, dry weight 95 kg. Potassium 3.5 mmol/L.",
        course="Intravenous diuresis reached dry weight. One potassium replacement was given for 3.2 mmol/L. Discharge potassium is 3.8 mmol/L.",
    )
    _vital(case, "admission")["oxygen_support"] = "2 L/min nasal cannula"
    _vital(case, "discharge")["oxygen_support"] = "room air"
    case["CaseWeight"][1]["weight_kg"] = "95.000"
    case["CaseWeight"][1]["dry_weight_kg"] = "95.000"
    _add_lab(case, lab_id="LAB-VAL807-007", timepoint="hospital_day_2", test_name="Potassium [Moles/volume] in Serum or Plasma", value=3.2, unit="mmol/L")
    furosemide = _med(case, "furosemide", "inpatient")
    furosemide.update({"drug": "furosemide 40 MG Injection", "route": "intravenous", "frequency": "twice daily", "status": "discontinued", "notes": "Stopped at the 95 kg dry weight."})
    _add_med(
        case, _med(case, "furosemide", "home"),
        medication_id="MED-VAL807-008", context="inpatient", drug="potassium chloride",
        reported_name="potassium chloride", dose="40 MEQ", route="oral", frequency="once",
        indication="Potassium 3.2 mmol/L", status="discontinued",
        notes="Single replacement. Not continued after potassium was 3.8 mmol/L.",
    )
    _consult(
        case, "cardiology",
        "Diuresis reached dry weight. The low potassium was replaced once.",
        "Resume furosemide 40 mg orally once daily. Do not continue standing potassium. Continue metoprolol succinate and atorvastatin.",
        "CON-VAL807-001",
    )
    findings = {
        "presentation_diagnosis_coherence": _pass("Dyspnea, orthopnea, and pulmonary edema already matched acute systolic heart failure."),
        "causal_context": _fail("Hypokalemia during diuresis was described without a reason for the decompensation.", "Two missed furosemide doses are the precipitant."),
        "diagnostic_workup": _fail("No ischemic evaluation or ejection fraction was on the chart.", "Added a flat troponin, an electrocardiogram, and an ejection fraction of 30 percent."),
        "treatment_trajectory": _fail("Inpatient furosemide copied the home oral dose, and potassium replacement had no dose.", "Intravenous diuresis was used until dry weight. One 40 mEq potassium dose is recorded and stopped."),
        "laboratory_vital_trend": _fail("The note said hypokalemia while the stored potassium was 3.5 then 3.8 mmol/L, and discharge weight was below dry weight.", "Added a hospital-day-2 potassium of 3.2 mmol/L and set the discharge weight equal to the 95 kg dry weight."),
        "hospital_course_completeness": _fail("One intake-and-output row did not show the potassium event.", "The potassium value and the single replacement are the course the discharge decision uses."),
        "medication_decision_support": _fail("The intended outpatient diuretic was mentioned and not specified.", "Cardiology says to resume 40 mg orally once daily and not to continue potassium."),
        "discharge_stability_chronology": _fail("Discharge weight was 93 kg against a dry weight of 95 kg.", "Discharge weight is now the dry weight, on room air, with potassium 3.8 mmol/L."),
        "internal_consistency": _fail("The repletion sentence and the potassium values did not match.", "The low value, the dose, and the discharge value now agree."),
        "unsupported_hidden_reference_action": _pass("Continuing oral furosemide 40 mg daily is the action the missed-dose precipitant supports. No standing potassium is added."),
    }
    reference = {
        "medications": [
            _ref("furosemide 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Systolic heart failure", "Missed doses precipitated the stay. Intravenous therapy has stopped at dry weight. Cardiology says to resume 40 mg orally once daily."),
            _ref("24 HR metoprolol succinate 25 MG Extended Release Oral Tablet", "continue", "25 MG", "once daily", "Systolic heart failure", "Continued. Discharge heart rate is 62."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued. No adverse effect is described."),
            _ref("potassium chloride", "stop", "40 MEQ", "once", "Transient potassium of 3.2 mmol/L", "One dose was given. Discharge potassium is 3.8 mmol/L."),
        ],
        "monitoring_requirements": [{"parameter": "potassium and weight", "frequency": "at primary care in 5 days", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Electrolyte and heart-failure follow-up", "timing": "5 days", "with_service": "primary care"}],
    }
    facts = [{
        "fact": "Missed diuretic doses, intravenous diuresis to a 95 kg dry weight, potassium 3.2 mmol/L, and one 40 mEq replacement.",
        "why": "The clean chart asserted hypokalemia and a diuretic plan without the values or the order.",
        "evidence": "Heidenreich PA et al. Circulation. 2022;145:e895-e1032. A single replacement is not continued after the potassium is 3.8 mmol/L.",
    }]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, (
        "VAL-807 makes the potassium fall and the dry-weight target visible. Oral furosemide 40 mg daily is resumed because the precipitant was missed doses, and standing potassium is not continued."
    )


def revise_808(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hf_ischemia_negative(case, "VAL808")
    _story(
        case,
        one_liner="66-year-old woman whose congestion did not reach dry weight on furosemide 40 mg daily",
        complaint="Edema and orthopnea",
        admission_dx="Acute systolic heart failure",
        hpi=(
            "A 66-year-old woman with systolic heart failure is admitted with a week of edema and "
            "orthopnea. She took furosemide 40 mg orally once daily and still gained fluid. Ejection "
            "fraction is 30 percent. Troponin does not rise. Dry weight is 86 kg. Admission weight is "
            "94 kg. Furosemide 40 mg intravenously twice daily is given, and weight falls only to 90 kg. "
            "The chest radiograph still shows residual congestion. Creatinine stays 0.9 mg/dL and "
            "potassium rises from 3.4 to 3.7 mmol/L on spironolactone. Blood pressure is 142/64 mm Hg. "
            "Cardiology recommends furosemide 40 mg orally twice daily at discharge because 40 mg once "
            "daily did not reach dry weight. Furosemide 80 mg once daily is a reasonable alternative "
            "total daily dose and is not the primary plan. Continue lisinopril, spironolactone, and "
            "metoprolol succinate."
        ),
        admission_note="Congestion despite home furosemide 40 mg daily. Weight 94 kg, dry weight 86 kg.",
        course="Intravenous diuresis lowered the weight to 90 kg. Residual congestion remains. The oral dose is increased.",
    )
    case["CaseWeight"][1]["weight_kg"] = "90.000"
    case["CaseWeight"][1]["dry_weight_kg"] = "86.000"
    furosemide = _med(case, "furosemide", "inpatient")
    furosemide.update({"drug": "furosemide 40 MG Injection", "route": "intravenous", "frequency": "twice daily", "status": "discontinued", "notes": "Acute course. Dry weight was not reached."})
    _consult(
        case, "cardiology",
        "Home furosemide 40 mg daily did not prevent this admission, and dry weight was not reached.",
        "Discharge on furosemide 40 mg orally twice daily. Continue lisinopril, spironolactone, and metoprolol succinate.",
        "CON-VAL808-001",
    )
    findings = {
        "presentation_diagnosis_coherence": _pass("Edema, orthopnea, and residual congestion match acute systolic heart failure."),
        "causal_context": _fail("The chart said the diuretic was adjusted and did not say why the patient was congested on the home dose.", "The home dose itself failed: fluid gained despite 40 mg daily, and dry weight was not reached."),
        "diagnostic_workup": _fail("No ejection fraction or ischemic check was recorded.", "Added both. The troponin does not rise."),
        "treatment_trajectory": _fail("Inpatient furosemide was still 40 mg orally once daily while the note said the dose was adjusted.", "Intravenous twice-daily furosemide is the acute treatment, and the discharge dose is 40 mg orally twice daily."),
        "laboratory_vital_trend": _pass("Creatinine stays 0.9 mg/dL and potassium moves from 3.4 to 3.7 mmol/L, which still allows spironolactone and lisinopril."),
        "hospital_course_completeness": _fail("One net-negative day and a discharge weight 6 kg above dry weight were the whole diuretic story.", "The course now ends at 90 kg with residual congestion, which is why the dose changes."),
        "medication_decision_support": _fail("No adjusted dose was written.", "Cardiology names 40 mg orally twice daily. Eighty milligrams once daily is recorded only as an alternative."),
        "discharge_stability_chronology": _fail("Discharge was called ready at a weight far above dry weight without a plan for that gap.", "The gap is now the reason for the higher oral dose, and the radiograph's residual congestion is acknowledged."),
        "internal_consistency": _fail("The adjustment sentence and the unchanged 40 mg rows disagreed.", "The intravenous course and the recommended oral dose now agree with that sentence."),
        "unsupported_hidden_reference_action": _fail("The clean reference continued 40 mg once daily.", "The reference changes furosemide to 40 mg twice daily and continues the other heart-failure medicines."),
    }
    reference = {
        "medications": [
            _ref("furosemide 40 MG Oral Tablet", "change", "40 MG", "twice daily", "Systolic heart failure", "Forty milligrams once daily did not reach the 86 kg dry weight. Cardiology recommends 40 mg orally twice daily. Furosemide 80 mg once daily is a reasonable alternative total daily dose."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension and systolic heart failure", "Creatinine is 0.9 mg/dL, potassium is 3.7 mmol/L, and systolic blood pressure is 142 mm Hg."),
            _ref("spironolactone 25 MG Oral Tablet", "continue", "25 MG", "once daily", "Systolic heart failure", "Potassium rose only to 3.7 mmol/L. Creatinine is stable."),
            _ref("24 HR metoprolol succinate 25 MG Extended Release Oral Tablet", "continue", "25 MG", "once daily", "Systolic heart failure", "Continued through the stay."),
        ],
        "monitoring_requirements": [{"parameter": "weight, creatinine, and potassium", "frequency": "at primary care in 7 days", "target": "move toward the 86 kg dry weight", "duration": None}],
        "follow_up_requirements": [{"item": "Primary care volume follow-up after the diuretic increase", "timing": "7 days", "with_service": "primary care"}],
    }
    facts = [{
        "fact": "Failure of furosemide 40 mg daily, intravenous diuresis, a discharge weight of 90 kg against a dry weight of 86 kg, and a recommendation for 40 mg twice daily.",
        "why": "The clean chart announced a diuretic adjustment and did not show one, while discharge weight remained well above dry weight.",
        "evidence": "Furosemide labeling lists a usual adult oral dose of 20 to 80 mg, which can be repeated. Heidenreich PA et al. Circulation. 2022;145:e895-e1032.",
    }]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, (
        "VAL-808 changes the furosemide plan because the home dose did not reach dry weight. The other heart-failure medicines stay, and their laboratory values still support them."
    )


EARLY = (
    ("VAL-802", revise_802),
    ("VAL-803", revise_803),
    ("VAL-804", revise_804),
    ("VAL-806", revise_806),
    ("VAL-807", revise_807),
    ("VAL-808", revise_808),
)


def _write_codebook(residents: list[dict[str, Any]]) -> None:
    document = _new_document("CliniProof framework-revised cases")
    prepare_form_document(document)
    _add_heading(document, "CliniProof cases revised with the frozen framework", 0)
    _add_body(
        document,
        "These twenty charts were revised from the clean base by applying the frozen "
        "framework in docs/revision/revision_framework.md. This was not a new clinician review. "
        "The charts are ready for clinician review. They are not clinically validated.",
    )
    _add_body(
        document,
        "The coding instrument is unchanged: C1 through C5, then Accept, Revise, or Exclude. "
        "There is no deliberately introduced medication-reconciliation discrepancy in these charts.",
    )
    for resident in residents:
        case_id = str(resident["case_id_code"])
        _start_case_section(document, "Framework-revised clean-case review", case_id)
        _render_case(document, resident, page_break=False, heading_text=f"CASE {case_id}")
        prepared = PreparedCase(
            case_id,
            resident,
            {"control_error_status": "NO INTENTIONAL ERROR", "error": {"error_category": "none"}},
            {},
        )
        _write_validation(document, prepared)
    CODEBOOK.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(CODEBOOK))
    finalize_word_form(CODEBOOK)


def _write_outputs(
    rows: list[dict[str, str]],
    narratives: list[tuple[str, str, dict[str, Finding]]],
) -> None:
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_id",
                "framework_domain",
                "problem_present",
                "evidence",
                "revision_required",
                "revision",
                "provenance",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Framework application for the remaining twenty clean cases",
        "",
        "Status: framework-revised and ready for clinician review. These cases are not clinically validated.",
        "",
        "The framework in `docs/revision/revision_framework.md` was frozen before these charts were edited. "
        "It was not changed to make a difficult case fit. VAL-802 and VAL-803 also use Reviewer 1's "
        "case-specific comments. Those comments are separate rows in the application table. "
        "The other eighteen cases had no case-specific clinician comments.",
        "",
        "The hidden reference was written again from the revised chart. Where the old action was not "
        "defensible, it was changed. Reasonable alternatives are named in the reference rationale "
        "when more than one action would follow from the same facts.",
        "",
    ]
    for case_id, blurb, findings in narratives:
        lines.append(f"## {case_id}")
        lines.append("")
        lines.append(blurb)
        lines.append("")
        for domain in DOMAINS:
            item = findings[domain]
            state = "Revised" if item.problem else "Pass"
            lines.append(f"- {domain}: {state}. {item.evidence}")
        lines.append("")
    lines.append("Case-level rows are in `docs/revision/revision_framework_application.csv`.")
    lines.append("")
    LOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    from scripts.remaining20_later import LATER

    OUT.mkdir(parents=True, exist_ok=True)
    residents: list[dict[str, Any]] = []
    rows: list[dict[str, str]] = []
    narratives: list[tuple[str, str, dict[str, Finding]]] = []
    for case_id, reviser in (*EARLY, *LATER):
        resident = _load(case_id)
        evaluator, findings, blurb = reviser(resident)
        missing = [name for name in DOMAINS if name not in findings]
        if missing:
            raise SystemExit(f"{case_id} missing domains {missing}")
        blob = json.dumps(resident)
        for banned in ("reference_discharge_plan", "revision_provenance", "synthetic_facts"):
            if banned in blob:
                raise SystemExit(f"{case_id} resident contains {banned}")
        if any(row.get("context") == "discharge" for row in resident["CaseMedication"]):
            raise SystemExit(f"{case_id} has a discharge medication row")
        provenance = evaluator["revision_provenance"]
        if case_id in {"VAL-802", "VAL-803"}:
            if not provenance["reviewer_1_comment"]:
                raise SystemExit(case_id)
            rows.append(
                {
                    "case_id": case_id,
                    "framework_domain": "reviewer_1_case_comment",
                    "problem_present": "yes",
                    "evidence": provenance["reviewer_1_comment"],
                    "revision_required": "yes",
                    "revision": "Applied beside the framework. See the case narrative.",
                    "provenance": "Reviewer 1 case-specific comment. Not a new framework domain.",
                }
            )
        elif provenance["statement"] != NO_COMMENT:
            raise SystemExit(f"{case_id} provenance statement")
        for domain in DOMAINS:
            item = findings[domain]
            rows.append(
                {
                    "case_id": case_id,
                    "framework_domain": domain,
                    "problem_present": "yes" if item.problem else "no",
                    "evidence": item.evidence,
                    "revision_required": "yes" if item.required else "no",
                    "revision": item.revision,
                    "provenance": provenance["statement"],
                }
            )
        (OUT / f"{case_id}_resident.json").write_text(_dump(resident), encoding="utf-8")
        (OUT / f"{case_id}_evaluator.json").write_text(_dump(evaluator), encoding="utf-8")
        residents.append(resident)
        narratives.append((case_id, blurb, findings))
    _write_outputs(rows, narratives)
    _write_codebook(residents)


if __name__ == "__main__":
    main()
