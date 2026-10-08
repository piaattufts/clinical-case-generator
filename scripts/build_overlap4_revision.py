"""Build the four-case clinical revision from the clean base.

The clean-base files are read and never written. New facts are recorded on the
evaluator file and in docs/revision/overlap_4_revision_log.md.
"""

from __future__ import annotations

import copy
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
OUT = ROOT / "data" / "case_sets" / "seed_guided" / "REVISED" / "overlap_4"
CODEBOOK = ROOT / "docs" / "validation" / "CliniProof_Revised_Overlap4_Codebook.docx"
CASE_IDS = ("VAL-801", "VAL-805", "VAL-809", "VAL-813")


def _load(case_id: str) -> dict[str, Any]:
    path = CLEAN / f"{case_id}_resident.json"
    payload: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(case_id)
    return payload


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _med(case: dict[str, Any], drug_name: str, context: str) -> dict[str, Any]:
    needle = drug_name.casefold()
    for row in case["CaseMedication"]:
        if row["context"] == context and needle in str(row["drug"]).casefold():
            if not isinstance(row, dict):
                raise TypeError(drug_name)
            return row
    raise KeyError(f"{case['case_id_code']} missing {context} {drug_name}")


def _drop_med(case: dict[str, Any], drug_name: str, context: str) -> None:
    needle = drug_name.casefold()
    case["CaseMedication"] = [
        row
        for row in case["CaseMedication"]
        if not (row["context"] == context and needle in str(row["drug"]).casefold())
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
    template = copy.deepcopy(case["CaseLab"][0])
    template.update(
        {
            "lab_id": lab_id,
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
        if row["timepoint"] == timepoint and str(row["test_name"]).startswith(test_start):
            row["value"] = value
            return
    raise KeyError(f"{case['case_id_code']} lab {timepoint} {test_start}")


def _add_vital(case: dict[str, Any], **changes: Any) -> None:
    row = copy.deepcopy(case["CaseVital"][0])
    row.update(changes)
    case["CaseVital"].append(row)


def _vital(case: dict[str, Any], timepoint: str) -> dict[str, Any]:
    for row in case["CaseVital"]:
        if row["timepoint"] == timepoint:
            if not isinstance(row, dict):
                raise TypeError(timepoint)
            return row
    raise KeyError(timepoint)


def revise_801(case: dict[str, Any]) -> dict[str, Any]:
    clinical = case["ClinicalCase"]
    clinical["one_liner"] = (
        "75-year-old man with mild major neurocognitive disorder and acute delirium "
        "during a urinary tract infection"
    )
    clinical["admission_dx"] = "Acute delirium, a change from baseline"
    clinical["chief_complaint"] = "New confusion, worse than baseline"
    clinical["medical_history"] = [
        "Mild major neurocognitive disorder",
        "Essential (primary) hypertension",
        "Type 2 diabetes mellitus without complications",
        "Mixed hyperlipidemia",
    ]
    clinical["social_context"] = (
        "Lives at home. A family caregiver reports his baseline: he recognizes family "
        "and holds a simple conversation."
    )
    hpi = (
        "A 75-year-old man with mild major neurocognitive disorder is admitted because "
        "a family caregiver reports two days of new confusion. At baseline he recognizes "
        "family and converses at home. On arrival he was disoriented, and that change "
        "is the delirium. Oral intake had been poor. He had been taking ibuprofen for "
        "knee pain. After his attention improved, a collateral list from the caregiver "
        "and the pharmacy was verified: lisinopril 10 mg daily, atorvastatin 40 mg daily, "
        "and metformin 500 mg twice daily. Ibuprofen 400 mg orally every 8 hours as "
        "needed was on that list. Fever and a urinalysis with leukocyte esterase led to "
        "a urine culture that grew Escherichia coli. He completed seven days of "
        "ceftriaxone 1 g intravenously once daily before discharge and is not taking an "
        "antibiotic at discharge. Outpatient creatinine was 1.0 mg/dL. Admission "
        "creatinine was 1.5 mg/dL. Ibuprofen was stopped and was not restarted. "
        "Lisinopril and metformin were held while creatinine was above baseline and "
        "intake was poor, then restarted when creatinine returned to 1.0 mg/dL and he "
        "was eating. Atorvastatin was continued. Confusion returned to the caregiver's "
        "reported baseline."
    )
    clinical["presentation"]["chief_complaint"] = "New confusion, worse than baseline"
    clinical["presentation"]["hpi"] = hpi
    clinical["presentation"]["presenting_symptoms"] = ["Confusion", "Fatigue"]
    clinical["presentation"]["symptom_duration"] = "two days"
    clinical["presentation"]["symptom_course"] = "returned to the reported baseline"
    clinical["social_support"]["living_situation"] = (
        "Lives at home with a family caregiver who can describe his cognitive baseline"
    )
    clinical["discharge_planning"]["discharge_readiness"] = "ready"
    case["CaseNote"] = [
        {
            **case["CaseNote"][0],
            "note_type": "admission",
            "note_text": (
                "Admission note. Acute confusion is a change from a known mild major "
                "neurocognitive disorder. Temperature 38.2 C. Urinalysis shows leukocyte "
                "esterase. Outpatient creatinine 1.0 mg/dL; admission creatinine 1.5 mg/dL. "
                "Ibuprofen, lisinopril, and metformin are held. Atorvastatin is continued."
            ),
        },
        {
            **case["CaseNote"][-1],
            "note_type": "hospital_course",
            "note_text": (
                "Urine culture grew Escherichia coli. Ceftriaxone 1 g intravenously once "
                "daily was given for seven days and the course finished before discharge. "
                "Fever resolved and attention returned to the caregiver's reported baseline. "
                "Creatinine returned to 1.0 mg/dL. Lisinopril 10 mg daily and metformin "
                "500 mg twice daily were restarted. Ibuprofen was not restarted. The "
                "collateral medication list was verified with the caregiver and the pharmacy. "
                "No antibiotic is planned after discharge."
            ),
        },
    ]
    case["CaseDiagnosis"] = [
        {
            **case["CaseDiagnosis"][0],
            "diagnosis": "Acute delirium, a change from baseline cognitive function",
            "diagnosis_type": "admission",
        },
        {
            **case["CaseDiagnosis"][0],
            "diagnosis_id": "DX-VAL801-005",
            "diagnosis": "Urinary tract infection",
            "diagnosis_type": "admission",
            "status": "resolved",
            "context": "inpatient",
        },
        {
            **case["CaseDiagnosis"][1],
            "diagnosis_id": "DX-VAL801-006",
            "diagnosis": "Mild major neurocognitive disorder",
            "diagnosis_type": "past_history",
        },
        *[
            row
            for row in case["CaseDiagnosis"]
            if row["diagnosis_type"] == "past_history"
        ],
    ]
    case["CaseProblemList"] = [
        {
            **case["CaseProblemList"][0],
            "problem_id": "PROB-VAL801-005",
            "problem": "Acute delirium on mild major neurocognitive disorder",
            "assessment": "New confusion, not his baseline. It cleared as the infection was treated.",
            "plan": "Discharge at the caregiver's reported baseline. No standing sedative was added.",
        },
        {
            **case["CaseProblemList"][0],
            "problem_id": "PROB-VAL801-006",
            "problem": "Urinary tract infection",
            "assessment": "Fever, pyuria, and Escherichia coli in the urine.",
            "plan": "Seven days of ceftriaxone were completed in the hospital. No discharge antibiotic.",
        },
        *[
            row
            for row in case["CaseProblemList"]
            if row["problem"] != "Delirium due to known physiological condition"
        ],
    ]
    _vital(case, "admission")["temp_c"] = "38.20"
    _vital(case, "admission")["heart_rate"] = 98
    _vital(case, "discharge")["temp_c"] = "36.70"
    _set_lab(case, "admission", "Creatinine", 1.5)
    _set_lab(case, "discharge", "Creatinine", 1.0)
    _add_lab(
        case,
        lab_id="LAB-VAL801-005",
        timepoint="outpatient_baseline",
        test_name="Creatinine [Mass/volume] in Serum or Plasma",
        value=1.0,
        unit="mg/dL",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL801-006",
        timepoint="admission",
        test_name="Urinalysis",
        value=None,
        unit=None,
        value_text="Leukocyte esterase positive. Nitrite positive. Bacteria present.",
    )
    case["CaseMicrobiology"] = [
        {
            "micro_id": "MICRO-VAL801-001",
            "case_id": "VAL-801",
            "timepoint": "admission",
            "specimen": "urine",
            "test": "urine culture",
            "organism": "Escherichia coli",
            "result": "growth",
            "quantity": None,
            "status": "final",
            "notes": "Susceptible to ceftriaxone.",
            "source_reference": None,
        }
    ]
    ibuprofen_home = _med(case, "ibuprofen", "home")
    ibuprofen_home["held_reason"] = (
        "Stopped on admission because creatinine was above the outpatient baseline "
        "while he was taking an NSAID and eating poorly. Not restarted."
    )
    ibuprofen_inpatient = _med(case, "ibuprofen", "inpatient")
    ibuprofen_inpatient["status"] = "discontinued"
    ibuprofen_inpatient["held_reason"] = ibuprofen_home["held_reason"]
    for name in ("lisinopril", "metformin"):
        row = _med(case, name, "inpatient")
        row["status"] = "active"
        row["notes"] = (
            "Held on admission while creatinine was 1.5 mg/dL and intake was poor. "
            "Restarted after creatinine returned to 1.0 mg/dL and he was eating."
        )
    ceftriaxone = _add_med(
        case,
        _med(case, "lisinopril", "inpatient"),
        medication_id="MED-VAL801-009",
        context="inpatient",
        drug="ceftriaxone 1000 MG Injection",
        reported_name="ceftriaxone 1000 MG Injection",
        dose="1000 MG",
        route="intravenous",
        frequency="once daily",
        indication="Urinary tract infection",
        status="discontinued",
        held_reason=None,
        notes="Seven daily doses were completed before discharge. Not continued after discharge.",
        verification_status="verified",
        verification_source="inpatient administration",
    )
    del ceftriaxone
    case["CaseConsult"] = [
        {
            **case["CaseConsult"][0],
            "assessment": (
                "Acute delirium on a known mild major neurocognitive disorder. "
                "Attention has returned to the caregiver's reported baseline."
            ),
            "recommendation": (
                "Use the verified collateral medication list. Do not restart ibuprofen. "
                "Lisinopril and metformin may be restarted now that creatinine is at the "
                "outpatient baseline and he is eating."
            ),
        }
    ]
    case["CaseMedicationReconciliation"][0]["notes"] = (
        "He could not give a medication history while delirious. A caregiver and pharmacy "
        "list was verified after his attention improved. Ibuprofen was confirmed and stopped. "
        "No unverified name was turned into a discharge medicine."
    )
    case["CaseFollowup"][0]["item"] = (
        "Primary care follow-up, including a creatinine check after the ACE inhibitor restart"
    )
    facts = [
        {
            "fact": "Mild major neurocognitive disorder with a caregiver-reported conversational baseline.",
            "why": "Delirium is an acute change from baseline. The prior chart had neither a baseline nor a cause.",
            "evidence": "American Psychiatric Association. DSM-5-TR. Delirium is a disturbance that develops over a short period and is a change from baseline attention and awareness.",
        },
        {
            "fact": "Fever, pyuria, and Escherichia coli urinary infection treated with ceftriaxone 1 g intravenously once daily for seven completed days.",
            "why": "Both reviewers asked for a precipitant that explains the acute confusion and the recovery.",
            "evidence": "Gupta K et al. Clin Infect Dis. 2011;52:e103-e120. IDSA pyelonephritis guidance includes an initial intravenous dose of ceftriaxone 1 g. Ceftriaxone labeling lists 1 to 2 g once daily for serious infections. A seven-day intravenous course was completed before discharge so the discharge list does not depend on an unfinished antibiotic.",
        },
        {
            "fact": "Outpatient creatinine 1.0 mg/dL, admission creatinine 1.5 mg/dL, discharge creatinine 1.0 mg/dL. Ibuprofen stopped. Lisinopril and metformin held, then restarted.",
            "why": "The ibuprofen stop had no visible reason. An ACE inhibitor and metformin also needed a visible relationship to kidney function and intake.",
            "evidence": "2019 AGS Beers Criteria. J Am Geriatr Soc. 2019;67:674-694. NSAIDs are listed for kidney-function risk in older adults. Restarting lisinopril and metformin is tied on the chart to return of creatinine to the outpatient baseline and resumed eating.",
        },
    ]
    return _evaluator(case, _reference_801(), facts)


def _reference_801() -> dict[str, Any]:
    return {
        "medications": [
            _ref(
                "lisinopril 10 MG Oral Tablet",
                "restart",
                "10 MG",
                "once daily",
                "Essential (primary) hypertension",
                "Held while creatinine was 1.5 mg/dL. Restarted after creatinine returned to the outpatient baseline of 1.0 mg/dL. The geriatrics note says it may be restarted.",
            ),
            _ref(
                "metformin hydrochloride 500 MG Oral Tablet",
                "restart",
                "500 MG",
                "twice daily",
                "Type 2 diabetes mellitus without complications",
                "Held while intake was poor and creatinine was above baseline. Restarted after he was eating and creatinine was 1.0 mg/dL.",
            ),
            _ref(
                "atorvastatin 40 MG Oral Tablet",
                "continue",
                "40 MG",
                "once daily",
                "Mixed hyperlipidemia",
                "Continued through the admission on the verified collateral list. No new contraindication is described.",
            ),
            _ref(
                "ibuprofen 400 MG Oral Tablet",
                "stop",
                "400 MG",
                "every 8 hours as needed",
                "Prior symptomatic analgesia",
                "Stopped because creatinine rose above the outpatient baseline during NSAID use and poor intake. The chart says it was not restarted.",
            ),
            _ref(
                "ceftriaxone 1000 MG Injection",
                "stop",
                "1000 MG",
                "once daily",
                "Urinary tract infection",
                "Seven daily doses were completed before discharge. The chart says no antibiotic is planned after discharge.",
            ),
        ],
        "monitoring_requirements": [
            {
                "parameter": "serum creatinine",
                "frequency": "at the primary-care visit in 7 days",
                "target": None,
                "duration": "after ACE-inhibitor restart",
            }
        ],
        "follow_up_requirements": [
            {
                "item": "Primary care follow-up, including a creatinine check after the ACE inhibitor restart",
                "timing": "7 days",
                "with_service": "primary care",
            }
        ],
    }


def revise_805(case: dict[str, Any]) -> dict[str, Any]:
    clinical = case["ClinicalCase"]
    clinical["weight_kg"] = "84.000"
    clinical["one_liner"] = (
        "68-year-old woman with acute heart-failure decompensation after missed diuretic doses"
    )
    clinical["chief_complaint"] = "Dyspnea, orthopnea, and edema"
    hpi = (
        "A 68-year-old woman with known systolic heart failure is admitted with one week "
        "of worsening dyspnea, orthopnea, and edema. She ran out of furosemide and missed "
        "four days of her 40 mg oral daily dose. She has no chest pain. Home medicines are "
        "furosemide 40 mg oral once daily, metoprolol succinate 25 mg oral once daily, and "
        "atorvastatin 40 mg oral once daily. She is not taking an ACE inhibitor, ARB, or "
        "ARNI. Admission weight is 84 kg. Her recorded dry weight is 78 kg. A chest "
        "radiograph shows pulmonary edema. Electrocardiogram shows sinus rhythm without "
        "ischemic ST-segment change. Troponin I was 18 ng/L and 16 ng/L six hours later, "
        "without a rise. Echocardiography shows a left ventricular ejection fraction of "
        "30 percent and no new severe valvular lesion. Furosemide 40 mg was given "
        "intravenously twice daily on hospital days 1 through 3, which is not the home "
        "oral regimen. Weight fell to 81 kg and then to 78 kg. Intake and output were net "
        "negative on each of those three days. Creatinine fell from 1.7 mg/dL to 0.9 mg/dL. "
        "Potassium remained 4.1 to 4.7 mmol/L. Oxygen by nasal cannula was weaned to room "
        "air. At discharge she is at dry weight, warm, and breathing room air."
    )
    clinical["presentation"]["chief_complaint"] = "Dyspnea, orthopnea, and edema"
    clinical["presentation"]["hpi"] = hpi
    clinical["presentation"]["symptom_course"] = "improved after intravenous diuresis"
    case["CaseNote"] = [
        {
            **case["CaseNote"][0],
            "note_text": (
                "Admission note. Congestion after four missed days of furosemide 40 mg oral "
                "daily. No chest pain. Weight 84 kg, dry weight 78 kg, oxygen saturation 92 "
                "percent on 2 L/min nasal cannula."
            ),
        },
        {
            **case["CaseNote"][-1],
            "note_text": (
                "Hospital days 1 through 3: furosemide 40 mg intravenously twice daily. "
                "Net negative intake and output each day. Weight 84 kg, then 81 kg, then "
                "78 kg at the recorded dry weight. Troponin did not rise. She is on room air."
            ),
        },
    ]
    _vital(case, "admission")["spo2_percent"] = "92.00"
    _vital(case, "admission")["oxygen_support"] = "2 L/min nasal cannula"
    _vital(case, "discharge")["spo2_percent"] = "98.00"
    _vital(case, "discharge")["oxygen_support"] = "room air"
    _vital(case, "discharge")["bp_systolic"] = 110
    case["CaseWeight"] = [
        {
            **case["CaseWeight"][0],
            "timepoint": "admission",
            "weight_kg": "84.000",
            "dry_weight_kg": "78.000",
        },
        {
            **case["CaseWeight"][0],
            "weight_id": "WT-VAL805-003",
            "timepoint": "hospital_day_2",
            "weight_kg": "81.000",
            "dry_weight_kg": "78.000",
        },
        {
            **case["CaseWeight"][1],
            "timepoint": "discharge",
            "weight_kg": "78.000",
            "dry_weight_kg": "78.000",
        },
    ]
    case["CaseIntakeOutput"] = [
        _io(case, "IO-VAL805-001", "hospital_day_1", 1100, 2900),
        _io(case, "IO-VAL805-002", "hospital_day_2", 1300, 2500),
        _io(case, "IO-VAL805-003", "hospital_day_3", 1500, 2000),
    ]
    _add_lab(
        case,
        lab_id="LAB-VAL805-007",
        timepoint="admission",
        test_name="Troponin I.cardiac [Mass/volume] in Serum or Plasma",
        value=18.0,
        unit="ng/L",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL805-008",
        timepoint="six_hours_later",
        test_name="Troponin I.cardiac [Mass/volume] in Serum or Plasma",
        value=16.0,
        unit="ng/L",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL805-009",
        timepoint="hospital_day_2",
        test_name="Potassium [Moles/volume] in Serum or Plasma",
        value=4.1,
        unit="mmol/L",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL805-010",
        timepoint="hospital_day_2",
        test_name="Creatinine [Mass/volume] in Serum or Plasma",
        value=1.2,
        unit="mg/dL",
    )
    furosemide = _med(case, "furosemide", "inpatient")
    furosemide["drug"] = "furosemide 40 MG Injection"
    furosemide["reported_name"] = "furosemide 40 MG Injection"
    furosemide["dose"] = "40 MG"
    furosemide["route"] = "intravenous"
    furosemide["frequency"] = "twice daily"
    furosemide["status"] = "discontinued"
    furosemide["notes"] = (
        "Hospital days 1 through 3 only. Stopped once weight reached the 78 kg dry weight. "
        "This is not the home oral dose."
    )
    case["CaseImaging"] = [
        case["CaseImaging"][0],
        {
            **case["CaseImaging"][0],
            "study_id": "STUDY-VAL805-002",
            "study_type": "Transthoracic echocardiogram",
            "body_site": "heart",
            "finding": (
                "Left ventricular ejection fraction 30 percent. No new severe valvular lesion."
            ),
        },
        {
            **case["CaseImaging"][0],
            "study_id": "STUDY-VAL805-003",
            "study_type": "Electrocardiogram",
            "body_site": "heart",
            "finding": "Sinus rhythm. No ischemic ST-segment change.",
        },
    ]
    case["CaseConsult"] = [
        {
            **case["CaseConsult"][0],
            "assessment": (
                "Congestion followed four missed days of oral furosemide. Ischemia is not "
                "supported by the history, electrocardiogram, or troponin. Ejection fraction "
                "is 30 percent. Dry weight of 78 kg was reached with intravenous furosemide."
            ),
            "recommendation": (
                "Resume furosemide 40 mg orally once daily. The missed doses explain the "
                "accumulation, and the intravenous course has been stopped at dry weight. "
                "Start enalapril 5 mg orally twice daily for systolic heart failure. "
                "Creatinine is 0.9 mg/dL, potassium is 4.3 mmol/L, and systolic blood "
                "pressure is 110 mm Hg. Continue metoprolol succinate 25 mg daily and "
                "atorvastatin 40 mg daily. The ACE inhibitor has not yet been given."
            ),
        }
    ]
    case["CaseMedicationReconciliation"][0]["notes"] = (
        "She missed four days of furosemide because the supply ran out. The other home "
        "medicines were continued. She has no ACE inhibitor, ARB, or ARNI at home."
    )
    case["CaseFollowup"][0]["item"] = (
        "Heart-failure clinic after diuresis, with a plan to obtain furosemide so doses are not missed"
    )
    facts = [
        {
            "fact": "Four missed days of home furosemide, a flat troponin, sinus electrocardiogram, and echocardiographic ejection fraction of 30 percent.",
            "why": "The prior chart did not say why heart failure decompensated.",
            "evidence": "Heidenreich PA et al. 2022 AHA/ACC/HFSA heart failure guideline. Circulation. 2022;145:e895-e1032. Precipitants, including missed medication, are part of the admission assessment. Ischemia was looked for and not supported by the values on this chart.",
        },
        {
            "fact": "Furosemide 40 mg intravenously twice daily for three days; weights 84 kg, 81 kg, and 78 kg; dry weight 78 kg; three days of net-negative intake and output; oxygen weaned to room air.",
            "why": "The home oral dose was repeated as the inpatient dose, and discharge weight was not at dry weight.",
            "evidence": "Heidenreich PA et al. Circulation. 2022;145:e895-e1032. Patients admitted with fluid overload should receive intravenous loop diuretic therapy, initially at a dose that equals or exceeds the chronic oral dose.",
        },
        {
            "fact": "Cardiology recommendation to resume oral furosemide 40 mg once daily and to start enalapril 5 mg twice daily, which has not yet been administered.",
            "why": "The discharge diuretic decision has to follow the missed-dose precipitant, and systolic heart failure with ejection fraction 30 percent has no ACE inhibitor on the home list.",
            "evidence": "Heidenreich PA et al. Circulation. 2022;145:e895-e1032. An ACE inhibitor is indicated for HFrEF when ARNI is not used. The enalapril dose is the curated regimen ENALAPRIL_5_BID, 5 mg orally twice daily. SOLVD used enalapril for systolic heart failure. N Engl J Med. 1991;325:293-302.",
        },
    ]
    return _evaluator(case, _reference_805(), facts)


def _io(case: dict[str, Any], io_id: str, timepoint: str, intake: int, output: int) -> dict[str, Any]:
    template = {
        "io_id": io_id,
        "case_id": case["case_id_code"],
        "timepoint": timepoint,
        "intake_ml": intake,
        "output_ml": output,
        "net_ml": intake - output,
        "notes": None,
        "source_reference": None,
    }
    return template


def _reference_805() -> dict[str, Any]:
    return {
        "medications": [
            _ref(
                "furosemide 40 MG Oral Tablet",
                "continue",
                "40 MG",
                "once daily",
                "Systolic heart failure",
                "The accumulation followed four missed doses. Intravenous diuresis has stopped at the 78 kg dry weight. Cardiology says to resume 40 mg orally once daily, not to start a higher maintenance dose.",
                monitoring="Obtain a supply so doses are not missed. Recheck weight and creatinine at the heart-failure visit.",
            ),
            _ref(
                "enalapril 5 MG Oral Tablet",
                "start",
                "5 MG",
                "twice daily",
                "Systolic heart failure with ejection fraction 30 percent",
                "There is no ACE inhibitor, ARB, or ARNI on the home list. Cardiology recommends starting enalapril 5 mg orally twice daily. It has not been given yet. Creatinine is 0.9 mg/dL, potassium is 4.3 mmol/L, and systolic blood pressure is 110 mm Hg.",
                monitoring="Creatinine and potassium at the follow-up visit.",
            ),
            _ref(
                "24 HR metoprolol succinate 25 MG Extended Release Oral Tablet",
                "continue",
                "25 MG",
                "once daily",
                "Systolic heart failure",
                "Continued through the admission. Heart rate at discharge is 69 beats per minute. Cardiology says to continue it.",
            ),
            _ref(
                "atorvastatin 40 MG Oral Tablet",
                "continue",
                "40 MG",
                "once daily",
                "Mixed hyperlipidemia",
                "Home medicine continued through the admission, and cardiology says to continue it.",
            ),
        ],
        "monitoring_requirements": [
            {
                "parameter": "weight, creatinine, and potassium",
                "frequency": "at the heart-failure visit in 7 days, sooner if dyspnea or lightheadedness returns",
                "target": "remain near the 78 kg dry weight",
                "duration": None,
            }
        ],
        "follow_up_requirements": [
            {
                "item": "Heart-failure clinic after diuresis, with a plan to obtain furosemide so doses are not missed",
                "timing": "7 days",
                "with_service": "cardiology",
            }
        ],
    }


def revise_809(case: dict[str, Any]) -> dict[str, Any]:
    clinical = case["ClinicalCase"]
    clinical["one_liner"] = (
        "82-year-old man with fever, dental disease, and mitral-valve endocarditis"
    )
    clinical["chief_complaint"] = "Fever and fatigue"
    clinical["medical_history"] = [
        "Essential (primary) hypertension",
        "Mixed hyperlipidemia",
        "Chronic periodontitis and several dental caries",
    ]
    hpi = (
        "An 82-year-old man is admitted with one week of fever and fatigue. He has no "
        "prosthetic valve. A dental examination shows several caries and periodontal "
        "disease. Home medicines are lisinopril 10 mg daily and atorvastatin 40 mg daily. "
        "Admission temperature is 38.8 C. Two blood-culture sets drawn before antibiotics "
        "grew Streptococcus mitis group, reported susceptible to penicillin. Ceftriaxone "
        "2 g intravenously once daily was started after those cultures were drawn. "
        "Creatinine was 1.6 mg/dL on hospital day 1, above an outpatient baseline of "
        "0.9 mg/dL, while he was febrile and eating poorly. Lisinopril was held that day. "
        "Repeat blood cultures on hospital day 3 showed no growth. A transesophageal "
        "echocardiogram shows an 8 mm mitral vegetation, mild mitral regurgitation, no "
        "abscess, and a left ventricular ejection fraction of 55 percent. Cardiac surgery "
        "found no current indication for an operation: he has no heart-failure symptoms "
        "from the valve lesion, no abscess, and the bacteremia has cleared. Ceftriaxone "
        "2 g intravenously once daily is planned for four weeks counted from the first "
        "negative blood culture. Discharge creatinine is 0.8 mg/dL. Lisinopril 10 mg "
        "daily was restarted the day before discharge and the blood pressure remained "
        "in the 130s systolic. A peripherally inserted central catheter is in place for "
        "the remaining intravenous doses. Weekly blood count and creatinine are arranged."
    )
    clinical["presentation"]["chief_complaint"] = "Fever and fatigue"
    clinical["presentation"]["presenting_symptoms"] = ["Fever", "Fatigue"]
    clinical["presentation"]["hpi"] = hpi
    clinical["presentation"]["symptom_course"] = "fever resolved after antibiotics"
    case["CaseNote"] = [
        {
            **case["CaseNote"][0],
            "note_text": (
                "Admission note. Fever to 38.8 C and fatigue for one week. Poor dentition. "
                "No prosthetic valve. Blood cultures drawn before antibiotics. Outpatient "
                "creatinine 0.9 mg/dL. Lisinopril held."
            ),
        },
        {
            **case["CaseNote"][-1],
            "note_text": (
                "Streptococcus mitis group bacteremia, penicillin susceptible. Cleared on "
                "hospital day 3. Transesophageal echocardiogram with an 8 mm mitral "
                "vegetation and no abscess. Surgery is not indicated now. Ceftriaxone 2 g "
                "intravenously once daily for four weeks from the first negative culture. "
                "Lisinopril restarted after creatinine returned to 0.8 mg/dL."
            ),
        },
    ]
    _vital(case, "admission")["temp_c"] = "38.80"
    _vital(case, "admission")["heart_rate"] = 102
    _vital(case, "discharge")["temp_c"] = "36.70"
    _vital(case, "discharge")["bp_systolic"] = 132
    _vital(case, "discharge")["heart_rate"] = 78
    _set_lab(case, "admission", "Creatinine", 1.6)
    _set_lab(case, "discharge", "Creatinine", 0.8)
    _add_lab(
        case,
        lab_id="LAB-VAL809-005",
        timepoint="outpatient_baseline",
        test_name="Creatinine [Mass/volume] in Serum or Plasma",
        value=0.9,
        unit="mg/dL",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL809-006",
        timepoint="admission",
        test_name="Leukocytes [#/volume] in Blood",
        value=14.2,
        unit="10*3/uL",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL809-007",
        timepoint="discharge",
        test_name="Leukocytes [#/volume] in Blood",
        value=7.4,
        unit="10*3/uL",
    )
    case["CaseMicrobiology"] = [
        {
            "micro_id": "MICRO-VAL809-001",
            "case_id": "VAL-809",
            "timepoint": "admission",
            "specimen": "blood",
            "test": "blood culture",
            "organism": "Streptococcus mitis group",
            "result": "growth",
            "quantity": "2 of 2 sets",
            "status": "final",
            "notes": "Drawn before antibiotics. Reported susceptible to penicillin.",
            "source_reference": None,
        },
        {
            "micro_id": "MICRO-VAL809-002",
            "case_id": "VAL-809",
            "timepoint": "hospital_day_3",
            "specimen": "blood",
            "test": "blood culture",
            "organism": None,
            "result": "no growth",
            "quantity": "2 of 2 sets",
            "status": "final",
            "notes": "First negative cultures. The four-week ceftriaxone course is counted from this day.",
            "source_reference": None,
        },
    ]
    case["CaseImaging"] = [
        {
            **case["CaseImaging"][0],
            "study_type": "Transesophageal echocardiogram",
            "finding": (
                "8 mm mitral vegetation. Mild mitral regurgitation. No abscess. "
                "Left ventricular ejection fraction 55 percent."
            ),
        }
    ]
    case["CaseDevice"] = [
        {
            "device_id": "DEV-VAL809-001",
            "case_id": "VAL-809",
            "device_type": "peripherally inserted central catheter",
            "site": "right arm",
            "placement_timepoint": "inpatient",
            "status": "in place",
            "tip_location_or_confirmation": "Tip position confirmed. Site without erythema or drainage.",
            "care_instructions": "Standard line care during the remaining ceftriaxone course.",
            "removal_plan": "Remove when the four-week intravenous course is complete.",
            "source_reference": None,
        }
    ]
    lisinopril = _med(case, "lisinopril", "inpatient")
    lisinopril["notes"] = (
        "Held on hospital day 1 when creatinine was 1.6 mg/dL. Restarted the day before "
        "discharge after creatinine was 0.8 mg/dL."
    )
    ceftriaxone = _med(case, "ceftriaxone", "inpatient")
    ceftriaxone["notes"] = (
        "2 g intravenously once daily. Four weeks counted from the first negative blood "
        "culture on hospital day 3. Continues after discharge through the catheter."
    )
    case["CaseConsult"] = [
        {
            **case["CaseConsult"][0],
            "assessment": (
                "Penicillin-susceptible Streptococcus mitis group endocarditis on a native "
                "mitral valve. Bacteremia cleared on hospital day 3. No abscess."
            ),
            "recommendation": (
                "Continue ceftriaxone 2 g intravenously once daily to complete four weeks "
                "from the first negative culture. Weekly complete blood count and creatinine. "
                "Infectious-diseases follow-up in 7 days."
            ),
        },
        {
            **case["CaseConsult"][0],
            "consult_id": "CON-VAL809-002",
            "service": "cardiac surgery",
            "assessment": (
                "Mitral vegetation without abscess, severe regurgitation, heart failure, "
                "or uncontrolled infection."
            ),
            "recommendation": "No indication for valve surgery during this admission.",
        },
    ]
    case["CaseFollowup"][0]["timing"] = "7 days"
    case["CaseFollowup"].append(
        {
            **case["CaseFollowup"][0],
            "followup_id": "FU-VAL809-002",
            "item": "Dental follow-up for caries and periodontal disease",
            "timing": "2 weeks",
            "with_service": "dentistry",
        }
    )
    facts = [
        {
            "fact": "Fever of 38.8 C, periodontal disease and caries, and no prosthetic valve.",
            "why": "The prior chart was afebrile and gave no predisposition for endocarditis.",
            "evidence": "Baddour LM et al. Circulation. 2015;132:1435-1486. Fever and a predisposing condition are clinical features of infective endocarditis. Dental infection is a recognized source of viridans-group streptococcal bacteremia.",
        },
        {
            "fact": "Penicillin-susceptible Streptococcus mitis group in two blood-culture sets, clearance on hospital day 3, and a transesophageal echocardiogram showing an 8 mm mitral vegetation without abscess.",
            "why": "The organism, the imaging, and the response to treatment were not specific enough to support a treatment duration or a surgical decision.",
            "evidence": "Baddour LM et al. Circulation. 2015;132:1435-1486. Ceftriaxone 2 g intravenously every 24 hours for four weeks is an accepted regimen for native-valve endocarditis due to highly penicillin-susceptible viridans-group streptococci. Early surgery is recommended for valve dysfunction causing heart failure, uncontrolled infection, or an indication such as abscess; none of those is present on this chart.",
        },
        {
            "fact": "Creatinine 0.9 mg/dL at baseline, 1.6 mg/dL on hospital day 1, and 0.8 mg/dL at discharge, with lisinopril held and then restarted.",
            "why": "The creatinine rise was unexplained and lisinopril appeared to continue through it.",
            "evidence": "KDIGO AKI guideline. Kidney Int Suppl. 2012;2:1-138. Hemodynamically active drugs are reviewed when kidney function falls. The chart restarts lisinopril only after creatinine has returned to baseline.",
        },
    ]
    return _evaluator(case, _reference_809(), facts)


def _reference_809() -> dict[str, Any]:
    return {
        "medications": [
            _ref(
                "ceftriaxone 2000 MG Injection",
                "continue",
                "2000 MG",
                "once daily",
                "Native mitral-valve endocarditis due to penicillin-susceptible Streptococcus mitis group",
                "Started in the hospital after cultures were drawn. Infectious diseases recommends completing four weeks from the first negative culture on hospital day 3. The catheter is in place.",
                monitoring="Weekly complete blood count and creatinine.",
            ),
            _ref(
                "lisinopril 10 MG Oral Tablet",
                "restart",
                "10 MG",
                "once daily",
                "Essential (primary) hypertension",
                "Held when creatinine was 1.6 mg/dL. Restarted the day before discharge after creatinine was 0.8 mg/dL, and systolic blood pressure stayed in the 130s.",
            ),
            _ref(
                "atorvastatin 40 MG Oral Tablet",
                "continue",
                "40 MG",
                "once daily",
                "Mixed hyperlipidemia",
                "Home medicine continued through the admission. No new contraindication is described.",
            ),
        ],
        "monitoring_requirements": [
            {
                "parameter": "weekly complete blood count and creatinine during parenteral therapy",
                "frequency": "weekly",
                "target": None,
                "duration": "for the remaining ceftriaxone course",
            }
        ],
        "follow_up_requirements": [
            {
                "item": "Infectious-disease follow-up with parenteral-therapy laboratory monitoring",
                "timing": "7 days",
                "with_service": "infectious disease",
            },
            {
                "item": "Dental follow-up for caries and periodontal disease",
                "timing": "2 weeks",
                "with_service": "dentistry",
            },
        ],
    }


def revise_813(case: dict[str, Any]) -> dict[str, Any]:
    clinical = case["ClinicalCase"]
    clinical["weight_kg"] = "64.000"
    clinical["one_liner"] = (
        "64-year-old woman with diarrhea after kidney transplant, found to have cytomegalovirus colitis"
    )
    clinical["admission_dx"] = "Diarrhea after kidney transplant"
    clinical["chief_complaint"] = "Diarrhea and poor intake"
    clinical["medical_history"] = [
        "Kidney transplant status",
        "Essential (primary) hypertension",
        "Mixed hyperlipidemia",
    ]
    case["CaseDiagnosis"] = [
        {
            **case["CaseDiagnosis"][0],
            "diagnosis": "Diarrhea after kidney transplant",
            "diagnosis_type": "admission",
            "status": "improving",
        },
        {
            **case["CaseDiagnosis"][0],
            "diagnosis_id": "DX-VAL813-005",
            "diagnosis": "Cytomegalovirus colitis",
            "diagnosis_type": "established_during_admission",
            "status": "active",
            "context": "Found on hospital day 2 by colonoscopic biopsy. Not the admitting label.",
        },
        *[row for row in case["CaseDiagnosis"] if row["diagnosis_type"] == "past_history"],
    ]
    case["CaseProblemList"] = [
        {
            **case["CaseProblemList"][0],
            "problem": "Diarrhea after kidney transplant",
            "assessment": "The admitting problem. Bacterial stool studies did not explain it.",
            "plan": "Volume repletion. The cause was established by biopsy.",
        },
        {
            **case["CaseProblemList"][-1],
            "problem_id": "PROB-VAL813-005",
            "problem": "Cytomegalovirus colitis",
            "assessment": "Established on hospital day 2. It was not known at admission.",
            "plan": "Antiviral induction. Mycophenolate remains held.",
        },
        *[
            row
            for row in case["CaseProblemList"]
            if row["problem"] != "Other cytomegaloviral diseases"
        ],
    ]
    hpi = (
        "A 64-year-old woman with a remote kidney transplant is admitted for several days "
        "of watery diarrhea and poor intake. She is not admitted with a diagnosis of "
        "cytomegalovirus colitis. Home immunosuppression is tacrolimus 1 mg orally every "
        "12 hours, mycophenolate mofetil 1000 mg orally twice daily, and prednisone 5 mg "
        "orally once daily. She also takes amlodipine 5 mg daily and atorvastatin 40 mg "
        "daily. Valganciclovir is not a home medicine. Admission weight is 64 kg. Blood "
        "pressure is 100/62 mm Hg and heart rate is 110 beats per minute. Creatinine is "
        "1.8 mg/dL, above an outpatient baseline of 1.0 mg/dL. Potassium is 3.2 mmol/L. "
        "Stool culture did not grow a bacterial pathogen, and Clostridioides difficile "
        "toxin is negative. On hospital day 2, colonoscopy shows colitis and the biopsy "
        "immunohistochemistry is positive for cytomegalovirus. Plasma cytomegalovirus DNA "
        "is 8500 IU/mL. Mycophenolate is held. Ganciclovir 5 mg/kg intravenously every "
        "12 hours is started after the biopsy; at 66 kg that dose is 330 mg. Potassium "
        "chloride, 40 mEq orally, is given for the admission potassium. Diarrhea slows "
        "to one or two formed stools a day. Discharge weight is 66 kg, creatinine is "
        "0.9 mg/dL, and potassium is 4.0 mmol/L. The transplant pharmacist records "
        "creatinine clearance above 60 mL/min from the discharge age, weight, and "
        "creatinine. Intravenous ganciclovir is stopped and valganciclovir 900 mg orally "
        "twice daily, given as 450 mg tablets, is started. Tacrolimus 1 mg every 12 hours "
        "continues; a discharge trough is 6.5 ng/mL and the transplant target on the "
        "chart is 5 to 8 ng/mL. Prednisone 5 mg daily continues. Mycophenolate stays "
        "held. Transplant clinic in 7 days will decide whether to restart it. No standing "
        "potassium is prescribed because the potassium is 4.0 mmol/L and the diarrhea "
        "has slowed."
    )
    clinical["presentation"]["chief_complaint"] = "Diarrhea and poor intake"
    clinical["presentation"]["hpi"] = hpi
    clinical["presentation"]["presenting_symptoms"] = ["Diarrhea"]
    clinical["presentation"]["symptom_course"] = (
        "diarrhea slowed after volume repletion and antiviral treatment"
    )
    case["CaseNote"] = [
        {
            **case["CaseNote"][0],
            "note_text": (
                "Admission note for diarrhea and poor intake after kidney transplant. "
                "The cause is not yet known. Creatinine 1.8 mg/dL, potassium 3.2 mmol/L, "
                "baseline creatinine 1.0 mg/dL. Mycophenolate is held. Valganciclovir is "
                "not a home medicine."
            ),
        },
        {
            **case["CaseNote"][-1],
            "note_text": (
                "Bacterial stool studies and Clostridioides difficile toxin are negative. "
                "Colonoscopic biopsy is positive for cytomegalovirus. Plasma cytomegalovirus "
                "DNA is 8500 IU/mL. Ganciclovir was given intravenously, then changed to "
                "valganciclovir 900 mg orally twice daily after creatinine clearance was "
                "above 60 mL/min. Mycophenolate remains held for the transplant visit."
            ),
        },
    ]
    _vital(case, "admission").update(
        {
            "temp_c": "37.40",
            "bp_systolic": 100,
            "bp_diastolic": 62,
            "heart_rate": 110,
        }
    )
    _vital(case, "discharge").update(
        {
            "temp_c": "36.80",
            "bp_systolic": 128,
            "bp_diastolic": 76,
            "heart_rate": 76,
        }
    )
    case["CaseWeight"] = [
        {
            **case["CaseWeight"][0],
            "timepoint": "admission",
            "weight_kg": "64.000",
            "dry_weight_kg": None,
        },
        {
            **case["CaseWeight"][1],
            "timepoint": "discharge",
            "weight_kg": "66.000",
            "dry_weight_kg": None,
        },
    ]
    _set_lab(case, "admission", "Creatinine", 1.8)
    _set_lab(case, "discharge", "Creatinine", 0.9)
    _set_lab(case, "admission", "Potassium", 3.2)
    _set_lab(case, "discharge", "Potassium", 4.0)
    _add_lab(
        case,
        lab_id="LAB-VAL813-005",
        timepoint="outpatient_baseline",
        test_name="Creatinine [Mass/volume] in Serum or Plasma",
        value=1.0,
        unit="mg/dL",
    )
    _add_lab(
        case,
        lab_id="LAB-VAL813-006",
        timepoint="inpatient",
        test_name="Cytomegalovirus DNA [#/volume] in Serum or Plasma by NAA with probe detection",
        value=8500.0,
        unit="IU/mL",
    )
    case["CaseMicrobiology"] = [
        {
            "micro_id": "MICRO-VAL813-001",
            "case_id": "VAL-813",
            "timepoint": "admission",
            "specimen": "stool",
            "test": "stool culture",
            "organism": None,
            "result": "no growth",
            "quantity": None,
            "status": "final",
            "notes": "No bacterial pathogen.",
            "source_reference": None,
        },
        {
            "micro_id": "MICRO-VAL813-002",
            "case_id": "VAL-813",
            "timepoint": "admission",
            "specimen": "stool",
            "test": "Clostridioides difficile toxin",
            "organism": None,
            "result": "negative",
            "quantity": None,
            "status": "final",
            "notes": None,
            "source_reference": None,
        },
    ]
    case["CaseProcedure"] = [
        {
            "procedure_id": "PROC-VAL813-001",
            "case_id": "VAL-813",
            "procedure_name": "Colonoscopy with biopsy",
            "procedure_type": "diagnostic",
            "date": None,
            "timepoint": "hospital_day_2",
            "performed_by": "gastroenterology",
            "anesthesia_type": None,
            "findings": "Colitis. Biopsy immunohistochemistry positive for cytomegalovirus.",
            "complications": None,
            "duration_minutes": None,
            "laterality": None,
            "source_reference": None,
        }
    ]
    _drop_med(case, "valganciclovir", "home")
    mmf_template = _med(case, "tacrolimus", "home")
    _add_med(
        case,
        mmf_template,
        medication_id="MED-VAL813-009",
        context="home",
        drug="mycophenolate mofetil 500 MG Oral Tablet",
        reported_name="mycophenolate mofetil 500 MG Oral Tablet",
        dose="1000 MG",
        route="oral",
        frequency="twice daily",
        indication="Kidney transplant status",
        status="home",
        notes="Given as 500 MG tablets.",
    )
    _add_med(
        case,
        mmf_template,
        medication_id="MED-VAL813-010",
        context="home",
        drug="prednisone 5 MG Oral Tablet",
        reported_name="prednisone 5 MG Oral Tablet",
        dose="5 MG",
        route="oral",
        frequency="once daily",
        indication="Kidney transplant status",
        status="home",
        notes=None,
    )
    _add_med(
        case,
        _med(case, "tacrolimus", "inpatient"),
        medication_id="MED-VAL813-011",
        context="inpatient",
        drug="mycophenolate mofetil 500 MG Oral Tablet",
        reported_name="mycophenolate mofetil 500 MG Oral Tablet",
        dose="1000 MG",
        route="oral",
        frequency="twice daily",
        indication="Kidney transplant status",
        status="held",
        held_reason=(
            "Held after cytomegalovirus colitis was established. Transplant says not to "
            "restart it at discharge. Reassess at the visit in 7 days."
        ),
        notes="Given as 500 MG tablets.",
    )
    _add_med(
        case,
        _med(case, "tacrolimus", "inpatient"),
        medication_id="MED-VAL813-012",
        context="inpatient",
        drug="prednisone 5 MG Oral Tablet",
        reported_name="prednisone 5 MG Oral Tablet",
        dose="5 MG",
        route="oral",
        frequency="once daily",
        indication="Kidney transplant status",
        status="active",
        notes="Maintenance corticosteroid continued.",
    )
    _add_med(
        case,
        _med(case, "tacrolimus", "inpatient"),
        medication_id="MED-VAL813-013",
        context="inpatient",
        drug="ganciclovir injection",
        reported_name="ganciclovir injection",
        dose="330 MG",
        route="intravenous",
        frequency="every 12 hours",
        indication="Cytomegalovirus colitis",
        status="discontinued",
        notes=(
            "5 mg/kg at 66 kg, started after the biopsy. Stopped when oral valganciclovir "
            "was begun. Not a discharge medicine."
        ),
    )
    valg = _med(case, "valganciclovir", "inpatient")
    valg["status"] = "active"
    valg["notes"] = (
        "Not a home medicine. Started after intravenous ganciclovir, once creatinine "
        "clearance was above 60 mL/min. Induction dose 900 mg orally twice daily, given "
        "as 450 mg tablets."
    )
    tac = _med(case, "tacrolimus", "inpatient")
    tac["notes"] = (
        "Discharge trough 6.5 ng/mL. Transplant target written on the chart is 5 to 8 ng/mL."
    )
    case["CaseConsult"] = [
        {
            **case["CaseConsult"][0],
            "service": "transplant",
            "assessment": (
                "Cytomegalovirus colitis after the biopsy. Volume depletion on admission "
                "has improved. Tacrolimus trough is in the stated target range."
            ),
            "recommendation": (
                "Continue tacrolimus 1 mg every 12 hours and prednisone 5 mg daily. "
                "Do not restart mycophenolate at discharge. Reassess that hold in clinic "
                "in 7 days."
            ),
        },
        {
            **case["CaseConsult"][1],
            "assessment": (
                "Tissue-proven cytomegalovirus colitis. Bacterial stool studies and "
                "Clostridioides difficile toxin are negative."
            ),
            "recommendation": (
                "Induction valganciclovir 900 mg orally twice daily now that creatinine "
                "clearance is above 60 mL/min. Recheck the viral load, blood count, and "
                "creatinine. Duration extends at least through the early follow-up and "
                "depends on symptom resolution and the viral load."
            ),
        },
    ]
    case["CaseMonitoring"] = [
        {
            **case["CaseMonitoring"][0],
            "parameter": "tacrolimus trough, serum creatinine, complete blood count, and plasma cytomegalovirus DNA",
            "frequency": "at the transplant visit in 7 days, sooner if diarrhea or fever returns",
            "responsible_service": "transplant",
        }
    ]
    case["CaseFollowup"][0]["item"] = (
        "Transplant clinic to review antiviral induction and whether mycophenolate can restart"
    )
    case["CaseIntakeOutput"] = [
        {
            "io_id": "IO-VAL813-001",
            "case_id": "VAL-813",
            "timepoint": "hospital_day_1",
            "intake_ml": 2800,
            "output_ml": 1600,
            "net_ml": 1200,
            "notes": "Intravenous volume repletion while diarrhea was still frequent.",
            "source_reference": None,
        }
    ]
    facts = [
        {
            "fact": "Admission for diarrhea before any cytomegalovirus label; negative bacterial stool studies and a negative Clostridioides difficile toxin; colonoscopy with biopsy immunohistochemistry positive for cytomegalovirus; plasma cytomegalovirus DNA 8500 IU/mL.",
            "why": "The prior chart presented an already labeled cytomegalovirus illness and listed valganciclovir as a home medicine.",
            "evidence": "Kotton CN et al. Transplantation. 2018;102:900-931. Gastrointestinal cytomegalovirus disease is established from symptoms plus tissue findings, not from a discharge label alone. Valganciclovir labeling uses 900 mg twice daily for induction when creatinine clearance is at least 60 mL/min.",
        },
        {
            "fact": "Admission creatinine 1.8 mg/dL and potassium 3.2 mmol/L, baseline creatinine 1.0 mg/dL, discharge creatinine 0.9 mg/dL and potassium 4.0 mmol/L after volume repletion and 40 mEq of potassium chloride. Weights 64 kg then 66 kg.",
            "why": "The prior potassium change had no cause, and the admission laboratories were not the low potassium and reduced kidney function expected from diarrheal volume loss.",
            "evidence": "Diarrhea and poor intake produce prerenal azotemia and potassium loss. Gennari FJ. Hypokalemia. N Engl J Med. 1998;339:451-458. The potassium chloride dose is a one-time replacement for a measured value of 3.2 mmol/L and is not continued after the repeat value is 4.0 mmol/L.",
        },
        {
            "fact": "Home regimen of tacrolimus, mycophenolate mofetil 1000 mg twice daily, and prednisone 5 mg daily. Mycophenolate held and not restarted at discharge. Intravenous ganciclovir 5 mg/kg, then oral valganciclovir induction.",
            "why": "The prior transplant regimen was only tacrolimus plus medicines for blood pressure and cholesterol, and the antiviral was already a home drug.",
            "evidence": "Kidney Disease: Improving Global Outcomes Transplant Work Group. Am J Transplant. 2009;9(Suppl 3):S1-S155. Maintenance immunosuppression is combination therapy and commonly includes a glucocorticoid. CellCept labeling recommends 1 g orally twice daily for adult kidney transplants. Kotton CN et al. Transplantation. 2018;102:900-931. Immunosuppression is reduced when possible during cytomegalovirus disease. Ganciclovir labeling uses 5 mg/kg every 12 hours for induction.",
        },
    ]
    return _evaluator(case, _reference_813(), facts)


def _reference_813() -> dict[str, Any]:
    return {
        "medications": [
            _ref(
                "valganciclovir 450 MG Oral Tablet",
                "start",
                "900 MG",
                "twice daily",
                "Cytomegalovirus colitis, after a positive biopsy",
                "Not a home medicine. Started after intravenous ganciclovir once the pharmacist recorded creatinine clearance above 60 mL/min. Induction dose, given as 450 mg tablets. Duration is rechecked with the viral load; it is not a completed course at discharge.",
                monitoring="Blood count, creatinine, and plasma cytomegalovirus DNA.",
            ),
            _ref(
                "mycophenolate mofetil 500 MG Oral Tablet",
                "hold",
                "1000 MG",
                "twice daily",
                "Kidney transplant status",
                "Held after the biopsy established cytomegalovirus colitis. The transplant note says not to restart it at discharge and to reassess in 7 days.",
            ),
            _ref(
                "BX Rating tacrolimus 1 MG Oral Capsule",
                "continue",
                "1 MG",
                "every 12 hours",
                "Kidney transplant status",
                "Discharge trough 6.5 ng/mL is inside the 5 to 8 ng/mL target written by transplant. The note says to continue 1 mg every 12 hours.",
            ),
            _ref(
                "prednisone 5 MG Oral Tablet",
                "continue",
                "5 MG",
                "once daily",
                "Kidney transplant status",
                "Home maintenance corticosteroid. Transplant says to continue it.",
            ),
            _ref(
                "amlodipine 5 MG Oral Tablet",
                "continue",
                "5 MG",
                "once daily",
                "Essential (primary) hypertension",
                "Home medicine continued. Discharge blood pressure is 128/76 mm Hg.",
            ),
            _ref(
                "atorvastatin 40 MG Oral Tablet",
                "continue",
                "40 MG",
                "once daily",
                "Mixed hyperlipidemia",
                "Home medicine continued. No new contraindication is described.",
            ),
            _ref(
                "ganciclovir injection",
                "stop",
                "330 MG",
                "every 12 hours",
                "Cytomegalovirus colitis",
                "Intravenous induction was stopped when oral valganciclovir began. It is not a discharge medicine.",
            ),
            _ref(
                "potassium chloride",
                "stop",
                "40 MEQ",
                "once",
                "Admission potassium 3.2 mmol/L",
                "One replacement dose is described. Discharge potassium is 4.0 mmol/L and diarrhea has slowed, so no standing potassium is indicated.",
            ),
        ],
        "monitoring_requirements": [
            {
                "parameter": "tacrolimus trough, serum creatinine, complete blood count, and plasma cytomegalovirus DNA",
                "frequency": "at the transplant visit in 7 days, sooner if diarrhea or fever returns",
                "target": "tacrolimus trough 5 to 8 ng/mL",
                "duration": "through antiviral induction",
            }
        ],
        "follow_up_requirements": [
            {
                "item": "Transplant clinic to review antiviral induction and whether mycophenolate can restart",
                "timing": "7 days",
                "with_service": "transplant",
            }
        ],
    }


def _ref(
    medication: str,
    action: str,
    dose: str,
    frequency: str,
    indication: str,
    rationale: str,
    *,
    route: str | None = None,
    monitoring: str | None = None,
) -> dict[str, Any]:
    inferred_route = route
    if inferred_route is None:
        inferred_route = "intravenous" if "Injection" in medication or medication.endswith("injection") else "oral"
    return {
        "medication": medication,
        "action": action,
        "dose": dose,
        "route": inferred_route,
        "frequency": frequency,
        "duration": None,
        "indication": indication,
        "rationale": rationale,
        "monitoring": monitoring,
    }


def _evaluator(
    resident: dict[str, Any], reference: dict[str, Any], facts: list[dict[str, str]]
) -> dict[str, Any]:
    evaluator = copy.deepcopy(resident)
    evaluator["reference_discharge_plan"] = reference
    evaluator["revision_provenance"] = {
        "status": "READY FOR NEXT CLINICIAN REVIEW",
        "clinically_validated": False,
        "baseline": f"data/case_sets/seed_guided/CLEAN_BASE/{resident['case_id_code']}_resident.json",
        "method": (
            "Reviewer concerns were turned into missing clinical information. "
            "The hidden reference was written again from the revised chart."
        ),
        "synthetic_facts": facts,
    }
    return evaluator


def _assert_resident_safe(resident: dict[str, Any]) -> None:
    blob = json.dumps(resident)
    for banned in (
        "reference_discharge_plan",
        "revision_provenance",
        "answer_key",
        "error_category",
        "synthetic_facts",
    ):
        if banned in blob:
            raise SystemExit(f"{resident['case_id_code']} resident contains {banned}")
    for row in resident["CaseMedication"]:
        if row.get("context") == "discharge":
            raise SystemExit(f"{resident['case_id_code']} has a discharge medication row")


def _write_codebook(residents: list[dict[str, Any]]) -> None:
    document = _new_document("CliniProof revised overlap cases")
    prepare_form_document(document)
    _add_heading(document, "CliniProof revised cases for the next clinician review", 0)
    _add_body(
        document,
        "These four charts were revised from the clean base after both clinicians "
        "had commented on them. They are ready for the next clinician review. "
        "They are not clinically validated.",
    )
    _add_body(
        document,
        "The coding instrument is unchanged: C1 through C5, then an overall "
        "recommendation of Accept, Revise, or Exclude. Blank fields stay blank. "
        "There is no deliberately introduced medication-reconciliation discrepancy "
        "in these charts.",
    )
    _add_body(document, "Cases: VAL-801, VAL-805, VAL-809, and VAL-813.")
    for resident in residents:
        case_id = str(resident["case_id_code"])
        _start_case_section(document, "Revised clean-case review", case_id)
        _render_case(
            document,
            resident,
            page_break=False,
            heading_text=f"CASE {case_id}",
        )
        prepared = PreparedCase(
            case_id,
            resident,
            {
                "control_error_status": "NO INTENTIONAL ERROR",
                "error": {"error_category": "none", "error_family": "none"},
            },
            {},
        )
        _write_validation(document, prepared)
    CODEBOOK.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(CODEBOOK))
    finalize_word_form(CODEBOOK)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    residents = []
    for case_id, reviser in (
        ("VAL-801", revise_801),
        ("VAL-805", revise_805),
        ("VAL-809", revise_809),
        ("VAL-813", revise_813),
    ):
        resident = _load(case_id)
        evaluator = reviser(resident)
        _assert_resident_safe(resident)
        (OUT / f"{case_id}_resident.json").write_text(_dump(resident), encoding="utf-8")
        (OUT / f"{case_id}_evaluator.json").write_text(_dump(evaluator), encoding="utf-8")
        residents.append(resident)
    _write_codebook(residents)


if __name__ == "__main__":
    main()
