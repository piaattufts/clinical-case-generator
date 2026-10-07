# ruff: noqa: E501
"""Canonical Set 1 for the six Round 1 cases.

Version 3 starts from the clean pre-injection charts. A version 1 or version 2
sentence is kept only when it has a source and does not tell the resident the
discharge action. Literature supports plausibility. It does not recover a
measurement that was not recorded.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from docx.document import Document as WordDocument
from docx.shared import RGBColor

from app.services.cycle2_split_casebooks import _chart, _round2_form
from app.services.cycle2_v2_cases import _historical_section
from app.services.round1_six_case_review import write_feedback_files
from app.services.word_controls import finalize_word_form, prepare_form_document
from app.services.word_export import NAVY, _add_body, _add_heading, _new_document, _set_run_font

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "exports" / "clean_balanced_seed_set"
V1 = ROOT / "exports" / "ko_revised_cases_v1"
V2 = ROOT / "exports" / "ko_cycle2_revised_validation_v2"
CASE_IDS = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")

LEAK_PATTERNS = (
    r"no reason to stop",
    r"verified list at discharge",
    r"use the verified",
    r"no discharge medicine is stopped",
    r"\bare continued\b",
    r"complete the planned",
    r"\bintended\b",
    r"continue after discharge",
    r"should continue",
    r"should stop",
    r"\brestart\b",
    r"\bresume\b",
    r"planned outpatient",
    r"planned antibiotic",
    r"correct medication",
    r"expected regimen",
    r"take exactly as listed",
    r"prepared for discharge",
    r"author response",
    r"planted error",
    r"injected error",
    r"assessment discrepancy",
    r"error family",
    r"\bf1_",
    r"\bf2_",
    r"find the error",
)

OLD_DESIGN_PATTERNS = (
    r"planted",
    r"injected error",
    r"assessment discrepancy",
    r"intended problem",
    r"expected error",
    r"detectability",
    r"find the error",
    r"what is wrong",
    r"error family",
    r"family 1",
    r"family 2",
    r"\bf1_",
    r"\bf2_",
    r"assessment target",
    r"error-bearing",
    r"clean control",
)

EVIDENCE_NOTES: dict[str, str] = {
    "[E1]": "Round 1 form in KO Casebook Validation.docx, reviewer KO, 10/5/2026. Supports the comment text and the blank or conflicting boxes. It does not by itself prove a medication change.",
    "[E2]": "Inouye SK, Westendorp RGJ, Saczynski JS. Delirium in elderly people. Lancet. 2014;383:911-922. doi:10.1016/S0140-6736(13)60688-1. Supports poor intake as a plausible delirium precipitant. It does not establish that this synthetic patient had that precipitant.",
    "[E3]": "Freeman R, Wieling W, Axelrod FB, et al. Consensus statement on the definition of orthostatic hypotension, neurally mediated syncope and the postural tachycardia syndrome. Clin Auton Res. 2011;21:69-72. doi:10.1007/s10286-011-0119-5. A fall of 20 mmHg in systolic pressure is the consensus threshold. The standing pressure of 116 mmHg is that threshold applied to the recorded supine pressure of 136 mmHg. It was not measured in the source chart.",
    "[E4]": "Clean pre-injection VAL-801 in exports/clean_balanced_seed_set. Glucose 163 mg/dL then 103 mg/dL. Creatinine 1.1 mg/dL then 1.0 mg/dL. Supine blood pressure 136/78 mmHg then 121/71 mmHg. Ibuprofen is on the medication list. No bleeding event is stored.",
    "[E5]": "Clean pre-injection VAL-802. Creatinine 1.3 mg/dL then 1.2 mg/dL. Blood pressure 138/69 mmHg then 124/68 mmHg. No creatinine from before the admission is stored. Atorvastatin is on the list. No potassium pair is stored.",
    "[E6]": "KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney Int Suppl. 2012;2:1-138. Supports reassessing ACE-inhibitor exposure when kidney function may be worse than baseline. It does not create a baseline that was not measured, and it does not set a creatinine threshold for this chart.",
    "[E7]": "Clean pre-injection VAL-803 evaluator. Lisinopril, hydrochlorothiazide, atorvastatin, and metformin each have a 30-day duration. Creatinine 1.0 mg/dL then 1.2 mg/dL. Potassium 4.4 mmol/L then 4.2 mmol/L. Glucose 149 mg/dL then 129 mg/dL. No sodium is stored. The reviewed readable case, data/case_sets/seed_guided/readable/cases/VAL-803.md, gave lisinopril a 7-day supply. That shortened supply is the earlier discrepancy, not the clean duration.",
    "[E8]": "Hydrochlorothiazide tablet labeling, DailyMed setid 9f0beacd-4c41-432d-b7d6-e779ae4c1b99, states that thiazides can cause hyponatremia and electrolyte imbalance.",
    "[E9]": "Clean pre-injection VAL-805. Furosemide 40 mg oral once daily at home and in the hospital. Weights 81 kg on admission, 78 kg at discharge, dry weight 73 kg. Hospital day 3 intake 1418 mL, output 2463 mL, net -1045 mL. Blood pressure 109/82 mmHg then 110/84 mmHg. Creatinine 1.7 mg/dL then 0.9 mg/dL. Potassium 4.7 mmol/L then 4.3 mmol/L. B-type natriuretic peptide 1120 pg/mL then 369 pg/mL. Oxygen saturation 92 percent then 98 percent. Chest radiograph shows pulmonary edema. No ejection fraction is stored.",
    "[E10]": "Heidenreich PA, Bozkurt B, Aguilar D, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 2022;145:e895-e1032. doi:10.1161/CIR.0000000000001063. Supports intravenous loop-diuretic treatment of congestion and the role of additional therapy in systolic heart failure. It was not used to invent an intravenous dose, a weight, or an ejection fraction.",
    "[E11]": "Repository regimen FUROSEMIDE_40_DAILY in data/bootstrap/medication_regimens.json. Dose 40 mg, route oral, frequency once daily. The entry excludes the injection product. DailyMed setid 571a52ed-5258-46d5-a0d2-9a984cf73895. This is the charted oral dose. It does not supply an intravenous order.",
    "[E12]": "Mullens W, Damman K, Harjola VP, et al. The use of diuretics in heart failure with congestion — a position statement from the Heart Failure Association of the ESC. Eur J Heart Fail. 2019;21:137-155. doi:10.1002/ejhf.1369. Supports judging decongestion with weight and urine output. It was not used to replace the recorded weights.",
    "[E13]": "Clean pre-injection VAL-809. Temperature 36.80°C on admission and at discharge. Presenting symptom fatigue. Blood culture with gram-positive cocci, later culture with no growth. Echocardiogram vegetation with preserved ventricular function. Creatinine 1.3 mg/dL then 0.8 mg/dL. Ceftriaxone 2000 mg intravenous once daily started during the admission. No valve history, dental history, murmur, or pre-admission creatinine is stored.",
    "[E14]": "Baddour LM, Wilson WR, Bayer AS, et al. Infective Endocarditis in Adults: Diagnosis, Antimicrobial Therapy, and Management of Complications. AHA Scientific Statement. Circulation. 2015;132:1435-1486. doi:10.1161/CIR.0000000000000296. Fever and a predisposing condition, including poor dentition, are part of the clinical picture of endocarditis. The statement was not used to replace the recorded temperature of 36.80°C, to add a prosthetic valve, or to rename gram-positive cocci.",
    "[E15]": "Repository regimen CEFTRIAXONE_ENDOCARDITIS_OPAT. Ceftriaxone 2000 mg intravenous once daily. Supports the dose already charted. It does not supply a remaining duration for this case.",
    "[E16]": "Clean pre-injection VAL-813. Admission viral-load review detected CMV viral burden and supported antiviral treatment. A later review was lower. Creatinine 1.2 mg/dL then 1.0 mg/dL. Potassium 4.7 mmol/L then 3.9 mmol/L. Home medicines are tacrolimus 1 mg every 12 hours, amlodipine, atorvastatin, and valganciclovir. Mycophenolate is not on the list. No tacrolimus trough is stored.",
    "[E17]": "Repository regimen VALGANCICLOVIR_CMV_TREATMENT. Dose 900 mg oral twice daily, given as 450 mg tablets, when renal function is in the range these profiles keep. DailyMed setid 89a934f0-85a3-44c1-82e5-d09d1738e08d. Supports the dose already charted. The dose was not taken from RxNorm.",
    "[E18]": "Kotton CN, Kumar D, Caliendo AM, et al. The Third International Consensus Guidelines on the Management of Cytomegalovirus in Solid-organ Transplantation. Transplantation. 2018;102:900-931. doi:10.1097/TP.0000000000002191. Supports starting treatment after laboratory evidence of CMV. It was not used to invent a viral-load number or an unrecorded immunosuppressant.",
    "[E19]": "RxNorm identifies valganciclovir. It was not used as evidence for the dose or the start time.",
    "[E20]": "CELLCEPT labeling, DailyMed setid 37241e87-4af4-4dc3-a1aa-ea6f20d8dc40, recommends 1 g orally twice daily for adult kidney transplantation. The source case has no mycophenolate row, so the labeled dose was not added.",
    "[E21]": "Spasovski G, Vanholder R, Allolio B, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol. 2014;170:G1-G47. doi:10.1530/EJE-13-1020. Thiazides are a recognized cause of hyponatremia, and hyponatremia can cause neurologic symptoms. This supports the plausibility of the added sodium pair. It does not show that those values were measured in the source chart.",
    "[E22]": "American Geriatrics Society Beers Criteria Update Expert Panel. American Geriatrics Society 2023 updated AGS Beers Criteria for potentially inappropriate medication use in older adults. J Am Geriatr Soc. 2023;71:2052-2081. doi:10.1111/jgs.18372. Supports treating a stop of an as-needed NSAID in an older adult as reasonable because of bleeding and kidney risk. It does not show that this patient bled or developed kidney injury.",
}

REVIEW_ITEMS: tuple[dict[str, str], ...] = (
    {
        "id": "VAL-801-C01",
        "case": "VAL-801",
        "comment": "C1 Fail. “The patient presents with delirium, but the cause is not revealed during the hospital course, we just learn that the delirium improves with treatment. There are no further details on why the patient was delirious or why he improved.” Overall: “Delirium due to known physiologic condition and then not elaborating on the physiologic condition doesn’t make sense.” The comment offered infection or gastrointestinal bleeding as examples.",
        "revision": "Poor oral intake, dry mucous membranes, and a standing systolic pressure are now on the chart. Infection and gastrointestinal bleeding were not added.",
        "location": "presentation; admission note; hospital course; vital signs",
        "old": "The clean course does not name a precipitant. The recorded supine pressure is 136/78 mmHg. No standing pressure is stored.",
        "new": "Poor oral intake and dry mucous membranes are described. The supine pressure remains 136/78 mmHg. A standing systolic pressure of 116 mmHg is a separate vital row. Confusion cleared as oral intake improved. Glucose is 163 mg/dL then 103 mg/dL.",
        "reasoning": "The review asked for a physiologic condition that explains the delirium and the improvement. Poor intake is a recognized precipitant, and the glucose fall fits restored intake. Infection and bleeding were examples, not findings in this chart, so they were not invented. The standing pressure uses the consensus 20 mmHg systolic threshold applied to the recorded supine pressure. It is labeled synthetic. The source supine vital is unchanged.",
        "evidence": "[E1] [E2] [E3] [E4]",
        "status": "REVISED",
    },
    {
        "id": "VAL-801-C02",
        "case": "VAL-801",
        "comment": "C2 Fail: “It wasn’t clear why ibuprofen should be stopped.” C4 Fail. Issue: “Ibuprofen stopped on admission.” Comment: “Not clear why ibuprofen was stopped.” C1 also says it is not clear why ibuprofen was stopped.",
        "revision": "The unexplained stop was removed from the resident chart. The reference continues ibuprofen. A stop is an acceptable alternative. The chart does not say which action to take.",
        "location": "home medications; inpatient medications; hospital course; reference_discharge_plan",
        "old": "Home and inpatient ibuprofen are marked stopped during the admission. The clean reference action is stop. No bleeding or kidney-injury event is stored.",
        "new": "Ibuprofen 400 mg every 8 hours as needed is on the home list and the inpatient list. Creatinine is 1.1 mg/dL then 1.0 mg/dL. No melena or hematemesis is recorded. The reference action is continue. Stop is an acceptable alternative.",
        "reasoning": "The stop the reviewer saw had no indication on the chart. Removing it follows the recorded list and the stable creatinine. Continuing an as-needed NSAID is not the only defensible plan in a 75-year-old with delirium, so a stop remains acceptable. The resident chart states the list and the negative bleeding history. It does not say that there is no reason to stop the drug.",
        "evidence": "[E1] [E4] [E22]",
        "status": "REVISED",
    },
    {
        "id": "VAL-801-C03",
        "case": "VAL-801",
        "comment": "C3 Pass and Fail are both selected. C3 comment is blank. C5 is Inappropriate / outlier: “Case is unclear.” Overall recommendation Revise: “This case could be usable if there was more complexity to the clinical case, i.e infection discovered and treated. Medication list should be clearer.”",
        "revision": "The double selection and the blank C3 comment are reproduced and were not resolved by guessing. No infection was added. The medication rows now agree with the notes.",
        "location": "Round 1 record; medication tables; notes",
        "old": "C3 has two selected results and no comment. The note says ibuprofen was stopped while giving no indication.",
        "new": "C3 remains Pass and Fail with no comment. The notes and the medication tables both show ibuprofen on the list. No infection was added.",
        "reasoning": "A blank comment and two selected boxes cannot be turned into one reviewer decision. Infection was an example of complexity, not a documented illness. The medication-list complaint is addressed by making the rows and the notes describe the same list.",
        "evidence": "[E1] [E4]",
        "status": "SOURCE_SELECTION_AMBIGUITY",
    },
    {
        "id": "VAL-802-C01",
        "case": "VAL-802",
        "comment": "C1 Fail. “delirium cause is not revealed (delirium due to known physiologic condition doesn’t make sense), it doesn’t appear that anything happened in the hospital course.” Hospital-course score is 1. Overall recommendation Exclude: “this case would need major revisions to be compatible with the goals of this project.”",
        "revision": "Poor oral intake is named as the only recorded precipitant, and the course states the creatinine and blood-pressure pairs. No other illness was added.",
        "location": "presentation; admission note; hospital course",
        "old": "The clean course does not name a precipitant or discuss the creatinine pair.",
        "new": "Confusion and poor oral intake for two days. No other precipitant is recorded. Confusion improved as oral intake improved. Creatinine is 1.3 mg/dL then 1.2 mg/dL. Blood pressure is 138/69 mmHg then 124/68 mmHg.",
        "reasoning": "The empty course is a fair description of the clean chart. Poor intake is a plausible precipitant and is labeled synthetic. Adding a second disease to answer Exclude would invent a case the source does not contain. Exclude remains the recorded recommendation.",
        "evidence": "[E1] [E2] [E5]",
        "status": "REVISED",
    },
    {
        "id": "VAL-802-C02",
        "case": "VAL-802",
        "comment": "C1: “lots of mention of the statin and it said that she was taking the statin, but this was not continued at discharge for no obvious reason.” C2 Fail: “Was the trainee supposed to continue the statin? Or recognize that it was not continued?”",
        "revision": "The note states that atorvastatin 40 mg daily is on the home list. It does not say whether to continue it at discharge. The reference continues it.",
        "location": "hospital course; medication reconciliation; reference_discharge_plan",
        "old": "The clean note talks about a collateral list and medicines that had been stopped, without a statin-specific discharge sentence. Atorvastatin is on the home and inpatient lists. The clean reference continues it.",
        "new": "The course says atorvastatin 40 mg daily is on the home list. The reference continues atorvastatin for hyperlipidemia. No stop was added.",
        "reasoning": "The reviewer was looking at a chart whose prose and discharge target did not say the same thing about the statin. The clean list contains atorvastatin, and no adverse effect is stored. The resident can see the list. The sentence does not instruct the discharge action.",
        "evidence": "[E1] [E5]",
        "status": "REVISED",
    },
    {
        "id": "VAL-802-C03",
        "case": "VAL-802",
        "comment": "C1: “creatinine was the only lab value and changed slightly, but it was not clear what the baseline creatinine was.” C4 Fail. Issue: “Creatinine elevated but patient continued on lisinopril.” Meaning recorded by the reviewer: if the creatinine represented acute kidney injury, lisinopril should be stopped. C3 Fail: the case lacks a reason for stopping the statin.",
        "revision": "No baseline creatinine was added. The reference continues lisinopril. Hold is an acceptable alternative.",
        "location": "laboratories; hospital course; reference_discharge_plan; acceptable alternatives",
        "old": "Creatinine is 1.3 mg/dL then 1.2 mg/dL. No earlier creatinine is stored. The clean reference continues lisinopril and records no alternative.",
        "new": "The same creatinine pair is stated, with an explicit statement that no earlier creatinine is recorded. The reference continues lisinopril. Hold is acceptable if 1.3 mg/dL is judged to be acute kidney injury.",
        "reasoning": "The comment says both that the change is slight and that the baseline is unknown, and that lisinopril should be stopped if the value is acute kidney injury. Those statements do not supply the missing baseline. Version 1’s creatinine of 1.2 mg/dL six weeks earlier is not in the clean chart and is not restored. KDIGO supports reassessment. It does not choose one action for this pair.",
        "evidence": "[E1] [E5] [E6]",
        "status": "REQUIRES_CLINICIAN_DECISION",
    },
    {
        "id": "VAL-803-C01",
        "case": "VAL-803",
        "comment": "C1 Fail. “delirium diagnosis is unclear (delirium due to known physiologic condition), cause is not revealed during the hospital course.” Fit between presentation and diagnosis is scored 1. Hospital course is scored 1.",
        "revision": "Sodium 128 mmol/L on admission and 135 mmol/L at discharge were added and labeled synthetic. The course does not state the discharge action.",
        "location": "laboratories; presentation; admission note; hospital course; inpatient medications",
        "old": "No sodium is stored. Hydrochlorothiazide is active at home and in the hospital. The course does not name a precipitant.",
        "new": "Admission sodium is 128 mmol/L and discharge sodium is 135 mmol/L. Hydrochlorothiazide is on the home list and the inpatient row is held after the admission sodium. Confusion cleared. The note does not say whether to restart the drug.",
        "reasoning": "The review asked for a cause. Hydrochlorothiazide is already on the list, and thiazide hyponatremia is a recognized cause of neurologic symptoms. The sodium pair is the version 1 pair, kept only as a labeled synthetic addition. It is not a recovered source laboratory. The inpatient hold is visible evidence. The discharge decision is left for the resident.",
        "evidence": "[E1] [E7] [E8] [E21]",
        "status": "REVISED",
    },
    {
        "id": "VAL-803-C02",
        "case": "VAL-803",
        "comment": "C1: “Medication list is fine but no changes that need to be made at discharge. Her creatinine changes so this might be considered clinically relevant or why the patient receives only 7 days of lisinopril.” C2 through the overall recommendation were not completed.",
        "revision": "The 7-day lisinopril supply was not restored. The reference duration remains 30 days. Holding lisinopril is an acceptable alternative. Later Round 1 items stay blank.",
        "location": "reference_discharge_plan; hospital course; Round 1 record",
        "old": "The reviewed readable case shortened lisinopril to 7 days. The clean evaluator duration is 30 days. Creatinine is 1.0 mg/dL then 1.2 mg/dL. C2 through the overall recommendation are blank.",
        "new": "The reference continues lisinopril for 30 days. The resident chart states the creatinine pair and does not state a day supply. Hold is an acceptable alternative. Blank Round 1 items remain NOT COMPLETED IN ROUND 1.",
        "reasoning": "The 7-day supply is the discrepancy the reviewer was shown, not the clean duration. A creatinine rise of 0.2 mg/dL does not by itself select a 7-day supply. The comment that no discharge change was needed described a chart with no precipitant. The sodium addition, which answers the missing-cause comment, is what makes a hydrochlorothiazide decision visible. Blank boxes were not filled in.",
        "evidence": "[E1] [E7]",
        "status": "NOT_COMPLETED_IN_ROUND_1",
    },
    {
        "id": "VAL-805-C01",
        "case": "VAL-805",
        "comment": "C1 Fail. “The weight should be closer to dry weight at the time of discharge.” C3 Fail: “The discharge weight not being close to the patient’s dry weight is confusing and suggests that the patient is not in fact ready for discharge.”",
        "revision": "The recorded weights were kept. The reference does not treat oral furosemide continuation as completed decongestion. Increasing the diuretic, without a fabricated dose, is an acceptable alternative.",
        "location": "weights; hospital course; reference_discharge_plan; acceptable alternatives",
        "old": "Admission weight 81 kg, discharge weight 78 kg, dry weight 73 kg. The clean reference continues furosemide 40 mg oral once daily with no alternative.",
        "new": "The same weights remain. The course states them. The reference still lists the recorded oral dose, and the action is clinically ambiguous. A dose increase with no numeric intravenous dose, and deferring discharge, are acceptable.",
        "reasoning": "Version 1 replaced these weights with 86 kg, 83 kg, and 80 kg and set dry weight to 80 kg. Those numbers are not in the source. The review is right that 78 kg is not 73 kg. Changing the reference claim is supported. Inventing a new weight series is not.",
        "evidence": "[E1] [E9] [E12]",
        "status": "REVISED",
    },
    {
        "id": "VAL-805-C02",
        "case": "VAL-805",
        "comment": "Medication-regimen scores 2 and 3 are both selected. “The medications during hospitalization would not be the same as the home regimen - the lasix would be given IV and increased.” Overall: “should not be the same as the patient’s home regimen.” “We need to add further details to the hospital course so there is a greater understanding of what diuresis the patient was receiving.”",
        "revision": "No intravenous dose was added. The course states that the only recorded order is 40 mg oral once daily. The increased dose is an acceptable alternative without a number.",
        "location": "inpatient medications; hospital course; reference_discharge_plan",
        "old": "Home and inpatient furosemide are 40 mg oral once daily.",
        "new": "The same oral order remains. The course says no other furosemide order is recorded. The reference does not invent an intravenous dose.",
        "reasoning": "Intravenous loop diuretic treatment is usual in congested heart failure. The project regimen FUROSEMIDE_40_DAILY is oral 40 mg once daily and excludes the injection product. No repository regimen encodes an intravenous dose for this case. Selecting 40 mg intravenous twice daily would repeat the version 1 invention. The dose increase therefore remains a clinician decision.",
        "evidence": "[E1] [E9] [E10] [E11]",
        "status": "REQUIRES_CLINICIAN_DECISION",
    },
    {
        "id": "VAL-805-C03",
        "case": "VAL-805",
        "comment": "“it would be more realistic to have several days of input and output data, as well as data on what medications the patient received during the hospitalization.”",
        "revision": "The single stored intake-and-output day was kept and written into the course. No additional days were created.",
        "location": "intake and output; hospital course",
        "old": "Hospital day 3 only: intake 1418 mL, output 2463 mL, net -1045 mL.",
        "new": "The same day is stated in the course. No hospital day 1 or day 2 balance was added.",
        "reasoning": "Version 1 replaced this day with three invented balances. The source has one day. A more realistic series is not a license to replace the recorded day.",
        "evidence": "[E1] [E9]",
        "status": "NOT_CHANGED",
    },
    {
        "id": "VAL-805-C04",
        "case": "VAL-805",
        "comment": "“It would be helpful to have either notes from cardiology or echocardiogram data and require the trainee to add additional medications to the patient’s regimen or adjust their dose of lasix.” Overall: “The trainee should have to make decisions on additional medications that should be added to the patient’s regimen – i.e. other GDMT such as ACE/ARB, SGLT2i, MRA.” C2 Pass, with no comment. C4 Pass, with no issue and no comment. C5 Moderate, with no comment. Overall Revise.",
        "revision": "No ejection fraction was added. The cardiology line no longer tells the resident to continue a plan. Additional therapy is an acceptable alternative and is not required. Blank comments stay blank.",
        "location": "consultations; imaging; reference_discharge_plan; acceptable alternatives",
        "old": "The cardiology recommendation says to continue the intended heart-failure and diuretic plan. No ejection fraction is stored.",
        "new": "The consultation does not record a medication order. No ejection fraction is on the chart. An ACE inhibitor, ARNI, SGLT2 inhibitor, or mineralocorticoid-receptor antagonist may be started and is not required.",
        "reasoning": "Guideline-directed therapy depends on systolic function that this chart does not record. Version 1’s ejection fraction of 30 percent is not restored, and the codebook does not ask about it. The resident still has a diuretic decision and an optional additional class, using the recorded creatinine, potassium, and blood pressure. Blank C2, C4, and C5 comments were not invented.",
        "evidence": "[E1] [E9] [E10]",
        "status": "REVISED",
    },
    {
        "id": "VAL-809-C01",
        "case": "VAL-809",
        "comment": "C1 Fail. “Presentation – requires more details, should present with fevers, have a history of mechanical valve or poor dentition that would predispose to endocarditis.” Overall: “Would have fevers/chills/predisposition to endocarditis.”",
        "revision": "A reported home temperature of 38.4°C and poor dentition were added and labeled synthetic. The recorded temperatures stay 36.80°C. No prosthetic valve, dental extraction, murmur, or species name was added.",
        "location": "presentation; admission note; hospital course; vital signs; microbiology",
        "old": "Temperature 36.80°C on admission and at discharge. Symptom fatigue. Organism gram-positive cocci. Vegetation present. No valve or dental history.",
        "new": "The vital table still shows 36.80°C at both time points. The history adds a reported home temperature of 38.4°C the evening before admission and poor dentition. No prosthetic valve is recorded. The organism remains gram-positive cocci.",
        "reasoning": "Fever and a predisposition are part of the endocarditis picture the reviewer asked for. Replacing 36.80°C with 38.6°C would erase a source vital. A mechanical valve was specifically not added. A dental extraction and viridans group streptococcus are version 1 inventions and are not restored. Poor dentition is the predisposition the comment allowed. Both additions are synthetic.",
        "evidence": "[E1] [E13] [E14]",
        "status": "REVISED",
    },
    {
        "id": "VAL-809-C02",
        "case": "VAL-809",
        "comment": "C1: “AKI was unexplained and lisinopril was continued despite AKI.” C2 Fail: “Lisinopril was continued despite the patient having an AKI.” C4 Fail. Issue: “Lisinopril - AKI.” Meaning: “Should not be continued.” Overall: “Lisinopril should be held if the patient has an AKI.”",
        "revision": "The creatinine pair is stated, including the absence of a pre-admission value. The reference continues lisinopril. Hold is an acceptable alternative.",
        "location": "laboratories; hospital course; reference_discharge_plan; acceptable alternatives",
        "old": "Creatinine 1.3 mg/dL then 0.8 mg/dL, not discussed as a baseline problem. The clean reference continues lisinopril.",
        "new": "The course states 1.3 mg/dL then 0.8 mg/dL and states that no earlier creatinine is recorded. Lisinopril remains on the inpatient list. Hold is acceptable if 1.3 mg/dL is judged to be acute kidney injury.",
        "reasoning": "The comment says to hold lisinopril if the patient has acute kidney injury. The chart shows a fall to 0.8 mg/dL and no creatinine from before admission. Treating 0.8 mg/dL as a known baseline would invent the version 1 history. The hold is acceptable. It is not required by a baseline the chart does not have.",
        "evidence": "[E1] [E6] [E13]",
        "status": "REQUIRES_CLINICIAN_DECISION",
    },
    {
        "id": "VAL-809-C03",
        "case": "VAL-809",
        "comment": "Overall: “Patient of this age would be very likely to have more than 2 home medications, would like to have more detail and complexity overall to this case.” C3 Pass, with no comment. C5 Inappropriate / outlier: “Error in the case as described above.” Overall Revise.",
        "revision": "No home medicine was added. The infectious-disease line no longer says to complete a planned course. Ceftriaxone remains the inpatient start, and the reference starts it without a fabricated duration.",
        "location": "home medications; consultations; hospital course; reference_discharge_plan",
        "old": "Home medicines are lisinopril and atorvastatin. The infectious-disease recommendation says to complete the planned parenteral course. The clean reference starts ceftriaxone with no duration.",
        "new": "The home list is unchanged. The consultation states the vegetation and the culture results and does not name a discharge duration. The reference starts ceftriaxone 2000 mg intravenous once daily with no duration.",
        "reasoning": "A longer home list would be an invented medication history. The antibiotic decision is supported by the vegetation, the culture, and the inpatient start. The source does not record how many days remain, and version 1’s four-week duration is not restored. Blank C3 and C4 comments stay blank.",
        "evidence": "[E1] [E13] [E15]",
        "status": "REQUIRES_CLINICIAN_DECISION",
    },
    {
        "id": "VAL-813-C01",
        "case": "VAL-813",
        "comment": "C1 Fail. “Patient is admitted for new diagnosis of CMV colitis, but was already on treatment for this (valganciclovir) prior to admission, which does not make sense. This medication would be started after diagnosis during the hospitalization.” C2 Fail: being on valganciclovir at admission “would make you think that you need to change to an alternative regimen.” C4 Fail. Issue: “Valganciclovir.” Meaning: “Should not be an admission medication.” Comment: “This is an error in the case that would be confusing.”",
        "revision": "Valganciclovir was removed from the home list and remains an inpatient start after the admission viral-load result. The reference action is start.",
        "location": "home medications; inpatient medications; presentation; hospital course; reference_discharge_plan",
        "old": "Valganciclovir 900 mg twice daily is a home medicine and an inpatient medicine. The clean note says outpatient continuation is the intended plan.",
        "new": "Home medicines are tacrolimus 1 mg every 12 hours, amlodipine 5 mg daily, and atorvastatin 40 mg daily. Valganciclovir 900 mg twice daily, given as 450 mg tablets, starts after the admission result that detected CMV viral burden. The reference action is start.",
        "reasoning": "The admission viral-load review is what supports antiviral treatment. A pre-admission valganciclovir row contradicts that sequence. The inpatient order and the project dose stay. Creatinine is 1.2 mg/dL then 1.0 mg/dL. The resident chart describes the inpatient start. It does not say to discharge on that list.",
        "evidence": "[E1] [E16] [E17] [E18] [E19]",
        "status": "REVISED",
    },
    {
        "id": "VAL-813-C02",
        "case": "VAL-813",
        "comment": "“The medications are much too simplified for a post transplant patient.”",
        "revision": "No additional immunosuppressant was added. The codebook does not ask about a drug that is not on the list. A temporary tacrolimus reduction is an acceptable alternative.",
        "location": "home medications; consultations; reference_discharge_plan; codebook adjudication",
        "old": "The only immunosuppressant on the clean list is tacrolimus 1 mg every 12 hours. Version 1 added mycophenolate. The earlier codebook asked about mycophenolate.",
        "new": "Tacrolimus remains the only immunosuppressant. The adjudication question asks about tacrolimus and the potassium pair. It does not name an absent drug.",
        "reasoning": "Labeling for mycophenolate supports a dose in kidney transplantation generally. It does not place that drug on this patient’s list. Adding it would invent a home medicine and then ask the resident to continue it. Whether the regimen is too narrow without it is left for the clinician. No trough is recorded, so a temporary tacrolimus reduction is acceptable and the reference continues 1 mg every 12 hours.",
        "evidence": "[E1] [E16] [E20]",
        "status": "REQUIRES_CLINICIAN_DECISION",
    },
    {
        "id": "VAL-813-C03",
        "case": "VAL-813",
        "comment": "“The labs are incomplete and the patient has a change in potassium without obvious cause or indication.” C5 Inappropriate / outlier, with no comment. Overall Exclude, with no comment. Reviewer KO. Date 10/5/2026.",
        "revision": "Potassium 4.7 mmol/L then 3.9 mmol/L is stated. No cause, blood count, or numeric viral load was added. The blank overall comment stays blank.",
        "location": "laboratories; hospital course; Round 1 record",
        "old": "Potassium 4.7 mmol/L then 3.9 mmol/L is stored and not discussed.",
        "new": "The course quotes those values and states that no cause is recorded. Exclude remains the recorded recommendation.",
        "reasoning": "The pair is a source result. Inventing a cause or a complete blood count would add data the case does not contain. The potassium change does not identify a medication to stop. The blank overall comment was not filled in.",
        "evidence": "[E1] [E16]",
        "status": "NOT_CHANGED",
    },
)

LEDGER: tuple[dict[str, str], ...] = (
    {
        "case": "VAL-801",
        "change": "Poor oral intake and dry mucous membranes added as the delirium precipitant.",
        "old": "No precipitant recorded.",
        "new": "Described in the history and the course. Confusion cleared as oral intake improved.",
        "source": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE. [E2]. Glucose 163 then 103 mg/dL is CASE_SOURCE [E4].",
        "classification": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE",
    },
    {
        "case": "VAL-801",
        "change": "Standing systolic pressure 116 mmHg added as its own vital row.",
        "old": "Supine 136/78 mmHg only.",
        "new": "Supine row unchanged. Standing systolic pressure 116 mmHg. Diastolic pressure, heart rate, and temperature were not copied onto that row.",
        "source": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE. [E3] applied to the CASE_SOURCE supine systolic pressure [E4].",
        "classification": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE",
    },
    {
        "case": "VAL-801",
        "change": "Ibuprofen stop removed. Stop kept as an acceptable alternative.",
        "old": "Chart and clean reference stop ibuprofen without a stored bleeding or kidney event.",
        "new": "Both medication rows list ibuprofen. Reference action continue. Alternative action stop.",
        "source": "CASE_SOURCE medication list [E4]. CLINICAL_LITERATURE [E22] supports the alternative and was not used to invent bleeding.",
        "classification": "CASE_SOURCE",
    },
    {
        "case": "VAL-802",
        "change": "Poor oral intake added. No baseline creatinine and no potassium pair added.",
        "old": "No precipitant. Creatinine 1.3 then 1.2 mg/dL. No earlier creatinine.",
        "new": "Poor oral intake is the only precipitant named. The creatinine pair and the absence of an earlier value are stated.",
        "source": "Precipitant is SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E2]. Creatinine pair is CASE_SOURCE [E5].",
        "classification": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE",
    },
    {
        "case": "VAL-803",
        "change": "Sodium 128 mmol/L then 135 mmol/L added. Inpatient hydrochlorothiazide held after the admission sodium.",
        "old": "No sodium. Hydrochlorothiazide active in the hospital. Clean reference continues it.",
        "new": "Sodium pair present. Inpatient row held. Reference action stop. Restart is an acceptable alternative. The resident note does not state the discharge action.",
        "source": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E8] [E21]. The numbers are the version 1 pair, not a source laboratory. CASE_SOURCE confirms hydrochlorothiazide and the creatinine pair [E7].",
        "classification": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE",
    },
    {
        "case": "VAL-803",
        "change": "Lisinopril duration left at 30 days.",
        "old": "Reviewed readable case used 7 days. Clean evaluator uses 30 days.",
        "new": "Reference duration 30 days. Resident chart does not state a day supply. Hold is an acceptable alternative.",
        "source": "CASE_SOURCE [E7]. The 7-day supply is the earlier discrepancy.",
        "classification": "CASE_SOURCE",
    },
    {
        "case": "VAL-805",
        "change": "Source weights, one intake-output day, and oral furosemide kept. Continuation marked ambiguous.",
        "old": "81 kg, 78 kg, dry weight 73 kg. Oral 40 mg once daily. One net of -1045 mL.",
        "new": "Same figures. No intravenous dose. No ejection fraction. Additional heart-failure therapy is optional.",
        "source": "CASE_SOURCE [E9]. DATABASE [E11]. CLINICAL_LITERATURE [E10] [E12] was not used to invent a dose or an ejection fraction.",
        "classification": "CASE_SOURCE",
    },
    {
        "case": "VAL-809",
        "change": "Reported home temperature 38.4°C and poor dentition added. Recorded temperatures kept.",
        "old": "36.80°C twice. Fatigue. Gram-positive cocci. No dental or valve history.",
        "new": "Vital rows remain 36.80°C. History distinguishes the reported home temperature and records poor dentition. No prosthetic valve.",
        "source": "Temperatures, organism, vegetation, and creatinine are CASE_SOURCE [E13]. The home temperature and poor dentition are SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E14].",
        "classification": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE",
    },
    {
        "case": "VAL-809",
        "change": "Planned-course sentence removed. Ceftriaxone duration not invented. Lisinopril hold is an alternative.",
        "old": "Consultation says to complete the planned parenteral course. Reference duration is empty.",
        "new": "Consultation states the vegetation and cultures. Reference starts ceftriaxone with no duration. Lisinopril continues, and hold is acceptable.",
        "source": "CASE_SOURCE [E13] [E15]. CLINICAL_LITERATURE [E6] for the alternative. No baseline creatinine was added.",
        "classification": "CASE_SOURCE",
    },
    {
        "case": "VAL-813",
        "change": "Valganciclovir removed from the home list and started after the admission viral-load result.",
        "old": "Valganciclovir is a home medicine. The note calls outpatient use the intended continuation.",
        "new": "Not a home medicine. Inpatient 900 mg twice daily after the admission result. Reference action start.",
        "source": "CASE_SOURCE procedure text [E16]. DATABASE [E17]. CLINICAL_LITERATURE [E18].",
        "classification": "CASE_SOURCE",
    },
    {
        "case": "VAL-813",
        "change": "Mycophenolate not added. Potassium cause not invented.",
        "old": "No mycophenolate. Potassium 4.7 then 3.9 mmol/L with no cause.",
        "new": "Still no mycophenolate. The potassium pair is stated. Tacrolimus reduction is an acceptable alternative. No trough was added.",
        "source": "CASE_SOURCE [E16]. Labeling [E20] was not used to add the drug.",
        "classification": "REQUIRES_CLINICIAN_DECISION",
    },
)

SPECIAL_QUESTIONS = {
    "VAL-801": (
        "Ibuprofen 400 mg every 8 hours as needed is on the home list and the inpatient list. "
        "No melena or hematemesis is recorded. Creatinine is 1.1 mg/dL then 1.0 mg/dL. "
        "Is continuation required, or is a stop also acceptable?"
    ),
    "VAL-802": (
        "Creatinine is 1.3 mg/dL then 1.2 mg/dL, and no creatinine from before this admission "
        "is recorded. Blood pressure is 138/69 mmHg then 124/68 mmHg. Should lisinopril be "
        "continued or held?"
    ),
    "VAL-803": (
        "Admission sodium is 128 mmol/L and discharge sodium is 135 mmol/L. "
        "Hydrochlorothiazide is on the home list and was not given after the admission sodium. "
        "Creatinine is 1.0 mg/dL then 1.2 mg/dL. Should hydrochlorothiazide be restarted, "
        "and should lisinopril be continued or held?"
    ),
    "VAL-805": (
        "Discharge weight is 78 kg and dry weight is 73 kg. The only recorded furosemide "
        "order is 40 mg oral once daily. Creatinine is 0.9 mg/dL, potassium is 4.3 mmol/L, "
        "and blood pressure is 110/84 mmHg. No ejection fraction is recorded. Should that "
        "oral dose be continued, increased, or should discharge wait? Are an ACE inhibitor, "
        "ARNI, SGLT2 inhibitor, or mineralocorticoid-receptor antagonist required, or only acceptable?"
    ),
    "VAL-809": (
        "Recorded temperatures are 36.80°C on admission and at discharge. A temperature of "
        "38.4°C was reported at home the evening before admission. Poor dentition is noted. "
        "No prosthetic valve is recorded. The culture grew gram-positive cocci. Creatinine "
        "is 1.3 mg/dL then 0.8 mg/dL, and no earlier creatinine is recorded. No remaining "
        "antibiotic duration is recorded. Should ceftriaxone be continued, and should "
        "lisinopril be continued or held?"
    ),
    "VAL-813": (
        "Valganciclovir was not a home medicine. It was started at 900 mg twice daily after "
        "the admission viral-load result. Creatinine is 1.2 mg/dL then 1.0 mg/dL. Tacrolimus "
        "is 1 mg every 12 hours, and no trough is recorded. Potassium is 4.7 mmol/L then "
        "3.9 mmol/L, and no cause is recorded. Should tacrolimus be continued or temporarily reduced?"
    ),
}

REFERENCE_EVIDENCE: tuple[dict[str, str], ...] = (
    {"case": "VAL-801", "medication": "atorvastatin 40 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hyperlipidemia is active. The drug is on the home and inpatient lists. No adverse effect is described."},
    {"case": "VAL-801", "medication": "lisinopril 10 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hypertension is active. Creatinine is 1.1 mg/dL then 1.0 mg/dL. Blood pressure is 136/78 mmHg then 121/71 mmHg."},
    {"case": "VAL-801", "medication": "metformin hydrochloride 500 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Diabetes is active. Glucose is 163 mg/dL then 103 mg/dL. Creatinine does not rise."},
    {"case": "VAL-801", "medication": "ibuprofen 400 MG Oral Tablet", "action": "continue", "classification": "CLINICALLY_AMBIGUOUS", "why": "The drug is on both lists, creatinine is stable, and no melena or hematemesis is recorded. Stopping an as-needed NSAID in a 75-year-old with delirium is also defensible. That alternative is encoded. The chart does not choose."},
    {"case": "VAL-802", "medication": "lisinopril 10 MG Oral Tablet", "action": "continue", "classification": "CLINICALLY_AMBIGUOUS", "why": "Creatinine is 1.3 mg/dL then 1.2 mg/dL and no pre-admission value is recorded. Hold is encoded."},
    {"case": "VAL-802", "medication": "atorvastatin 40 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hyperlipidemia. The drug is on the home list. The note does not say to continue it at discharge."},
    {"case": "VAL-803", "medication": "hydrochlorothiazide 25 MG Oral Tablet", "action": "stop", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Admission sodium is 128 mmol/L while hydrochlorothiazide is a home medicine. The inpatient row is held, and discharge sodium is 135 mmol/L. Confusion cleared. The note does not say to leave the drug stopped. Restart with sodium follow-up is encoded."},
    {"case": "VAL-803", "medication": "lisinopril 10 MG Oral Tablet", "action": "continue", "classification": "CLINICALLY_AMBIGUOUS", "why": "Creatinine rises from 1.0 mg/dL to 1.2 mg/dL. The clean duration is 30 days. Hold is encoded. The resident chart does not state a day supply."},
    {"case": "VAL-803", "medication": "atorvastatin 40 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hyperlipidemia and an active inpatient row. The sodium history does not implicate this drug."},
    {"case": "VAL-803", "medication": "metformin hydrochloride 500 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Diabetes. Glucose is 149 mg/dL then 129 mg/dL. Creatinine remains in a range that does not by itself stop metformin."},
    {"case": "VAL-805", "medication": "24 HR metoprolol succinate 25 MG Extended Release Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Systolic heart failure. The same dose is on the home and inpatient lists. Heart rate and blood pressure are recorded. The note identifies the dose and does not call it the discharge prescription."},
    {"case": "VAL-805", "medication": "atorvastatin 40 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hyperlipidemia and an active inpatient row."},
    {"case": "VAL-805", "medication": "furosemide 40 MG Oral Tablet", "action": "continue", "classification": "CLINICALLY_AMBIGUOUS", "why": "The only recorded order is 40 mg oral once daily. Oxygen saturation and natriuretic peptide improved, and one day of output was net negative. Discharge weight is 78 kg and dry weight is 73 kg, so continuation is not a claim that dry weight was reached. A dose increase without an invented number is encoded."},
    {"case": "VAL-805", "medication": "Additional systolic heart-failure therapy (ACE inhibitor, ARNI, SGLT2 inhibitor, or MRA)", "action": "start", "classification": "CLINICALLY_AMBIGUOUS", "why": "No ejection fraction is recorded. Discharge creatinine is 0.9 mg/dL and potassium is 4.3 mmol/L. Starting another class is acceptable and not required."},
    {"case": "VAL-809", "medication": "ceftriaxone 2000 MG Injection", "action": "start", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "A vegetation is present, the admission culture grew gram-positive cocci, a later culture showed no growth, and ceftriaxone was started in the hospital. The consultation does not say to complete a planned course. No remaining duration is stored, and none was added."},
    {"case": "VAL-809", "medication": "lisinopril 10 MG Oral Tablet", "action": "continue", "classification": "CLINICALLY_AMBIGUOUS", "why": "Creatinine falls from 1.3 mg/dL to 0.8 mg/dL. No pre-admission creatinine is recorded. Hold is encoded."},
    {"case": "VAL-809", "medication": "atorvastatin 40 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hyperlipidemia and an active inpatient row."},
    {"case": "VAL-813", "medication": "valganciclovir 450 MG Oral Tablet", "action": "start", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Not a home medicine. Started at 900 mg twice daily after the admission viral-load result. A later result was lower and diarrhea improved. Creatinine is 1.2 mg/dL then 1.0 mg/dL."},
    {"case": "VAL-813", "medication": "BX Rating tacrolimus 1 MG Oral Capsule", "action": "continue", "classification": "CLINICALLY_AMBIGUOUS", "why": "It is the recorded immunosuppressant and was given through the stay at 1 mg every 12 hours. No trough is recorded. A temporary reduction is encoded."},
    {"case": "VAL-813", "medication": "amlodipine 5 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hypertension. The drug is on the home and inpatient lists."},
    {"case": "VAL-813", "medication": "atorvastatin 40 MG Oral Tablet", "action": "continue", "classification": "SUFFICIENT_VISIBLE_EVIDENCE", "why": "Hyperlipidemia and an active inpatient row."},
)


def _set_note(case: dict[str, Any], note_type: str, text: str) -> None:
    for note in case.get("CaseNote") or []:
        if note.get("note_type") == note_type:
            note["note_text"] = text
            return
    raise KeyError(note_type)


def _set_hpi(case: dict[str, Any], text: str) -> None:
    presentation = case["ClinicalCase"]["presentation"]
    presentation["hpi"] = text
    presentation["symptom_course"] = "See the history of present illness."
    presentation["review_of_systems"] = "See the history of present illness."


def _set_followup(case: dict[str, Any], text: str) -> None:
    rows = case.get("CaseFollowup") or []
    if not rows:
        raise KeyError("followup")
    rows[0]["item"] = text


def _consult(case: dict[str, Any], service: str, recommendation: str, assessment: str) -> None:
    for consult in case.get("CaseConsult") or []:
        if consult.get("service") == service:
            consult["recommendation"] = recommendation
            consult["assessment"] = assessment
            return
    raise KeyError(service)


def _patch_801(case: dict[str, Any]) -> None:
    case["ClinicalCase"]["one_liner"] = (
        "75-year-old man admitted with confusion, fatigue, and poor oral intake."
    )
    _set_hpi(
        case,
        "A 75-year-old man is admitted with several days of confusion, fatigue, and poor "
        "oral intake. Mucous membranes are dry. Supine blood pressure on admission is "
        "136/78 mmHg. A standing systolic pressure of 116 mmHg is recorded at admission. "
        "Home medicines are lisinopril, atorvastatin, metformin, and ibuprofen as needed. "
        "He could not give a reliable medication history at admission. A collateral list "
        "was obtained later. Glucose is 163 mg/dL on admission and 103 mg/dL at discharge. "
        "Creatinine is 1.1 mg/dL then 1.0 mg/dL.",
    )
    case["ClinicalCase"]["presentation"]["presenting_symptoms"] = (
        "Confusion, fatigue, and poor oral intake."
    )
    _set_note(
        case,
        "admission",
        "Admission note for a 75-year-old man with delirium. Poor oral intake and dry "
        "mucous membranes are present. Supine blood pressure is 136/78 mmHg, and a "
        "standing systolic pressure of 116 mmHg is recorded. Home medicines are "
        "lisinopril, atorvastatin, metformin, and ibuprofen as needed. A collateral "
        "medication list was obtained after admission.",
    )
    _set_note(
        case,
        "hospital_course",
        "Poor oral intake was treated with fluids, and oral intake improved. Confusion "
        "cleared as oral intake improved. Glucose is 163 mg/dL then 103 mg/dL. "
        "Creatinine is 1.1 mg/dL then 1.0 mg/dL. Ibuprofen 400 mg every 8 hours as "
        "needed is on the home list and on the inpatient list. No melena or hematemesis "
        "is recorded.",
    )
    _consult(
        case,
        "geriatrics",
        "Collateral history was obtained after admission. No melena or hematemesis is described.",
        "Confusion cleared as oral intake improved.",
    )
    _set_followup(case, "Primary care follow-up")
    standing = None
    for vital in case.get("CaseVital") or []:
        if vital.get("timepoint") == "admission":
            standing = json.loads(json.dumps(vital))
            break
    if standing is None:
        raise KeyError("admission vital")
    standing.update(
        {
            "vital_id": "VIT-VAL801-STAND",
            "timepoint": "admission_standing",
            "bp_systolic": 116,
            "bp_diastolic": None,
            "heart_rate": None,
            "resp_rate": None,
            "temp_c": None,
            "spo2_percent": None,
            "oxygen_support": None,
            "source_reference": None,
        }
    )
    case["CaseVital"].append(standing)
    for medication in case.get("CaseMedication") or []:
        if "ibuprofen" in str(medication.get("drug")):
            medication["status"] = "home" if medication.get("context") == "home" else "active"
            medication["held_reason"] = None


def _patch_802(case: dict[str, Any]) -> None:
    case["ClinicalCase"]["one_liner"] = (
        "81-year-old woman admitted with confusion and poor oral intake."
    )
    _set_hpi(
        case,
        "An 81-year-old woman is admitted with delirium after two days of confusion and "
        "poor oral intake. No other precipitant is recorded. Home medicines are lisinopril "
        "10 mg daily and atorvastatin 40 mg daily. Creatinine is 1.3 mg/dL on admission "
        "and 1.2 mg/dL at discharge. No creatinine from before this admission is recorded. "
        "Blood pressure is 138/69 mmHg then 124/68 mmHg.",
    )
    case["ClinicalCase"]["presentation"]["presenting_symptoms"] = (
        "Confusion and poor oral intake for two days."
    )
    _set_note(
        case,
        "admission",
        "Admission note for an 81-year-old woman with delirium. Confusion and poor oral "
        "intake for two days. Home medicines are lisinopril and atorvastatin. No earlier "
        "creatinine is recorded.",
    )
    _set_note(
        case,
        "hospital_course",
        "Poor oral intake was the only precipitant recorded. Confusion improved as oral "
        "intake improved. Creatinine is 1.3 mg/dL then 1.2 mg/dL. Blood pressure is "
        "138/69 mmHg then 124/68 mmHg. Atorvastatin 40 mg daily is on the home list. "
        "No creatinine from before this admission is recorded.",
    )
    _set_followup(case, "Primary care follow-up")
    for reconciliation in case.get("CaseMedicationReconciliation") or []:
        reconciliation["notes"] = (
            "A pharmacy fill history was obtained after admission. Atorvastatin 40 mg "
            "daily is on that list."
        )


def _patch_803(case: dict[str, Any]) -> None:
    case["ClinicalCase"]["one_liner"] = (
        "71-year-old man admitted with fatigue, confusion, and serum sodium 128 mmol/L."
    )
    _set_hpi(
        case,
        "A 71-year-old man is admitted with one week of fatigue and confusion. Home "
        "medicines include hydrochlorothiazide 25 mg daily, lisinopril 10 mg daily, "
        "atorvastatin 40 mg daily, and metformin 500 mg twice daily. Admission sodium "
        "is 128 mmol/L. Creatinine is 1.0 mg/dL on admission and 1.2 mg/dL at discharge.",
    )
    case["ClinicalCase"]["presentation"]["presenting_symptoms"] = "Fatigue and confusion for one week."
    _set_note(
        case,
        "admission",
        "Admission note. Fatigue and confusion for one week. Hydrochlorothiazide is on "
        "the home list. Serum sodium on arrival is 128 mmol/L. Creatinine is 1.0 mg/dL.",
    )
    _set_note(
        case,
        "hospital_course",
        "Admission sodium is 128 mmol/L. Hydrochlorothiazide was not given after that "
        "result. Discharge sodium is 135 mmol/L. Confusion cleared. Creatinine is "
        "1.0 mg/dL then 1.2 mg/dL. Potassium is 4.4 mmol/L then 4.2 mmol/L. Glucose "
        "is 149 mg/dL then 129 mg/dL.",
    )
    _set_followup(case, "Primary care follow-up")
    template = dict(case["CaseLab"][0])
    for timepoint, value, lab_id in (
        ("admission", 128, "LAB-VAL803-NA1"),
        ("discharge", 135, "LAB-VAL803-NA2"),
    ):
        row = dict(template)
        row.update(
            {
                "lab_id": lab_id,
                "timepoint": timepoint,
                "test_name": "Sodium [Moles/volume] in Serum or Plasma",
                "value": value,
                "value_text": None,
                "unit": "mmol/L",
                "status": "final",
                "source_reference": "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE synthetic_v3",
            }
        )
        case["CaseLab"].append(row)
    for medication in case.get("CaseMedication") or []:
        if "hydrochlorothiazide" in str(medication.get("drug")) and medication.get("context") == "inpatient":
            medication["status"] = "held"
            medication["held_reason"] = "Admission serum sodium 128 mmol/L."


def _patch_805(case: dict[str, Any]) -> None:
    case["ClinicalCase"]["one_liner"] = (
        "68-year-old woman admitted with dyspnea, edema, and orthopnea."
    )
    _set_hpi(
        case,
        "A 68-year-old woman is admitted with acute systolic heart failure. Dyspnea, "
        "edema, and orthopnea have been present for one week. Home medicines are oral "
        "furosemide 40 mg once daily, atorvastatin, and metoprolol succinate 25 mg once "
        "daily. The inpatient furosemide order is the same oral dose. Weight is 81 kg "
        "on admission and 78 kg at discharge. Recorded dry weight is 73 kg.",
    )
    case["ClinicalCase"]["presentation"]["presenting_symptoms"] = "Dyspnea, edema, and orthopnea for one week."
    _set_note(
        case,
        "admission",
        "Admission note for a 68-year-old woman with acute systolic heart failure. "
        "Symptoms are dyspnea, edema, and orthopnea for one week. Home and inpatient "
        "furosemide orders are both oral 40 mg once daily. No echocardiogram is recorded.",
    )
    _set_note(
        case,
        "hospital_course",
        "Dyspnea, edema, and orthopnea were present for one week. The chest radiograph "
        "shows pulmonary edema without pneumonia. The only recorded furosemide order, "
        "at home and in the hospital, is 40 mg oral once daily. Weight is 81 kg on "
        "admission and 78 kg at discharge. Dry weight is 73 kg. One intake-and-output "
        "day is stored, hospital day 3, with intake 1418 mL, output 2463 mL, and net "
        "-1045 mL. Creatinine is 1.7 mg/dL then 0.9 mg/dL. Potassium is 4.7 mmol/L "
        "then 4.3 mmol/L. B-type natriuretic peptide is 1120 pg/mL then 369 pg/mL. "
        "Blood pressure is 109/82 mmHg then 110/84 mmHg. Oxygen saturation is 92 percent "
        "then 98 percent. No echocardiogram and no ejection fraction are recorded. "
        "Metoprolol succinate 25 mg daily is the recorded home and inpatient dose.",
    )
    _consult(
        case,
        "cardiology",
        "No echocardiogram is recorded. This consultation does not record a medication order.",
        "Pulmonary edema is present on the chest radiograph. No ejection fraction is recorded.",
    )
    _set_followup(case, "Heart-failure clinic follow-up")


def _patch_809(case: dict[str, Any]) -> None:
    case["ClinicalCase"]["one_liner"] = (
        "82-year-old man admitted with fatigue, a reported home fever, and a vegetation."
    )
    text = (
        "An 82-year-old man is admitted with infective endocarditis. Fatigue has been "
        "present for one week. He reported a temperature of 38.4°C at home the evening "
        "before admission. Recorded hospital temperatures are 36.80°C on admission and "
        "36.80°C at discharge. Poor dentition is noted. No prosthetic valve is recorded. "
        "Home medicines are lisinopril and atorvastatin. Ceftriaxone 2000 mg intravenously "
        "once daily was started during the admission. Transthoracic echocardiogram shows "
        "a mobile echodensity consistent with a vegetation and preserved ventricular "
        "function. Admission blood culture grew gram-positive cocci. A later culture "
        "showed no growth. Creatinine is 1.3 mg/dL on admission and 0.8 mg/dL at "
        "discharge. No creatinine from before this admission is recorded."
    )
    _set_hpi(case, text)
    case["ClinicalCase"]["presentation"]["presenting_symptoms"] = (
        "Fatigue for one week, with a reported home temperature of 38.4°C."
    )
    _set_note(case, "admission", text)
    _set_note(
        case,
        "hospital_course",
        "Ceftriaxone 2000 mg intravenously once daily was given during the admission. "
        "The echocardiogram shows a vegetation with preserved ventricular function. "
        "Blood culture grew gram-positive cocci, and a later culture showed no growth. "
        "A temperature of 38.4°C was reported at home the evening before admission. "
        "Recorded temperatures are 36.80°C on admission and at discharge. Poor dentition "
        "is noted. No prosthetic valve is recorded. Creatinine is 1.3 mg/dL then "
        "0.8 mg/dL. Lisinopril is on the inpatient list. No creatinine from before this "
        "admission is recorded.",
    )
    _consult(
        case,
        "infectious disease",
        "A vegetation is present. The admission blood culture grew gram-positive cocci. "
        "A later blood culture showed no growth.",
        "Fatigue, a reported home temperature, poor dentition, and a vegetation are recorded.",
    )
    _set_followup(case, "Infectious-disease follow-up")


def _patch_813(case: dict[str, Any]) -> None:
    case["ClinicalCase"]["one_liner"] = (
        "64-year-old woman with a kidney transplant admitted with diarrhea."
    )
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
        "A 64-year-old woman with a kidney transplant is admitted with diarrhea for "
        "several days. Home medicines are tacrolimus 1 mg every 12 hours, amlodipine "
        "5 mg daily, and atorvastatin 40 mg daily. She was not taking valganciclovir "
        "before admission. The admission viral-load review detected CMV viral burden."
    )
    _set_hpi(case, text)
    case["ClinicalCase"]["presentation"]["presenting_symptoms"] = "Diarrhea for several days."
    _set_note(case, "admission", text)
    _set_note(
        case,
        "hospital_course",
        "The admission viral-load review detected CMV viral burden. Valganciclovir "
        "900 mg orally twice daily, given as 450 mg tablets, was started after that "
        "result. A later review showed a lower viral burden. Diarrhea improved. "
        "Tacrolimus 1 mg every 12 hours was given through the stay at the same dose. "
        "Creatinine is 1.2 mg/dL then 1.0 mg/dL. Potassium is 4.7 mmol/L then "
        "3.9 mmol/L. No cause for the potassium change is recorded. No tacrolimus "
        "trough is recorded.",
    )
    _consult(
        case,
        "infectious disease",
        "The admission viral-load review detected CMV. Valganciclovir was started after that result.",
        "Diarrhea improved after the antiviral was started.",
    )
    _consult(
        case,
        "transplant",
        "Tacrolimus 1 mg every 12 hours is the recorded immunosuppressant. No other "
        "immunosuppressant is on the medication list. No trough is recorded.",
        "Kidney transplant. The recorded immunosuppressant dose was given through the stay.",
    )
    _set_followup(case, "Transplant clinic follow-up")


_NARRATIVE = {
    "VAL-801": _patch_801,
    "VAL-802": _patch_802,
    "VAL-803": _patch_803,
    "VAL-805": _patch_805,
    "VAL-809": _patch_809,
    "VAL-813": _patch_813,
}


def _add_alternative(plan: dict[str, Any], medication: str, action: str, rationale: str) -> None:
    plan.setdefault("acceptable_alternatives", [])
    plan["acceptable_alternatives"].append(
        {"medication": medication, "action": action, "rationale": rationale}
    )


def _retitle(plan: dict[str, Any], item_text: str) -> None:
    for row in plan.get("follow_up_requirements") or []:
        row["item"] = item_text


def _reference_801(evaluator: dict[str, Any]) -> None:
    plan = evaluator["reference_discharge_plan"]
    reasons = {
        "atorvastatin": "Hyperlipidemia is active. The drug is on the home and inpatient lists. No adverse effect is described.",
        "lisinopril": "Hypertension is active. Creatinine is 1.1 mg/dL then 1.0 mg/dL. Blood pressure is 136/78 mmHg then 121/71 mmHg.",
        "metformin": "Diabetes is active. Glucose is 163 mg/dL then 103 mg/dL.",
        "ibuprofen": "Ibuprofen is on the home and inpatient lists. No melena or hematemesis is recorded. Creatinine is 1.1 mg/dL then 1.0 mg/dL. A stop is also acceptable.",
    }
    for item in plan["medications"]:
        name = str(item.get("medication"))
        for key, rationale in reasons.items():
            if key in name:
                item["action"] = "continue"
                item["rationale"] = rationale
                item["evidence_class"] = next(
                    row["classification"]
                    for row in REFERENCE_EVIDENCE
                    if row["case"] == "VAL-801" and key in row["medication"]
                )
    _add_alternative(
        plan,
        "ibuprofen 400 MG Oral Tablet",
        "stop",
        "A stop is acceptable in a 75-year-old with delirium even though no bleeding and no creatinine rise are recorded.",
    )
    _retitle(plan, "Primary care follow-up")


def _reference_802(evaluator: dict[str, Any]) -> None:
    plan = evaluator["reference_discharge_plan"]
    for item in plan["medications"]:
        name = str(item.get("medication"))
        if "lisinopril" in name:
            item["rationale"] = (
                "Hypertension is active and blood pressure is 138/69 mmHg then 124/68 mmHg. "
                "Creatinine is 1.3 mg/dL then 1.2 mg/dL. No earlier creatinine is recorded, so a hold is also acceptable."
            )
            item["evidence_class"] = "CLINICALLY_AMBIGUOUS"
        elif "atorvastatin" in name:
            item["rationale"] = "Hyperlipidemia is active and atorvastatin is on the home list. No adverse effect is described."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
    _add_alternative(
        plan,
        "lisinopril 10 MG Oral Tablet",
        "hold",
        "Hold is acceptable if creatinine 1.3 mg/dL is judged to be acute kidney injury. No baseline is recorded, so the reference does not require a hold.",
    )
    _retitle(plan, "Primary care follow-up")


def _reference_803(evaluator: dict[str, Any]) -> None:
    plan = evaluator["reference_discharge_plan"]
    for item in plan["medications"]:
        name = str(item.get("medication"))
        if "hydrochlorothiazide" in name:
            item["action"] = "stop"
            item["duration"] = None
            item["rationale"] = (
                "Admission sodium is 128 mmol/L while hydrochlorothiazide is a home medicine. "
                "The inpatient row is held after that result. Discharge sodium is 135 mmol/L and confusion cleared. "
                "The sodium pair is a synthetic addition. Restart is acceptable only with planned sodium checks."
            )
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
        elif "lisinopril" in name:
            item["duration"] = "30 days"
            item["rationale"] = (
                "The clean chart uses 30 days. The reviewed 7-day supply is not restored. "
                "Creatinine is 1.0 mg/dL then 1.2 mg/dL. Hold is acceptable if that rise is judged to be acute kidney injury."
            )
            item["evidence_class"] = "CLINICALLY_AMBIGUOUS"
        elif "atorvastatin" in name:
            item["rationale"] = "Hyperlipidemia is active. The sodium history does not implicate this drug."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
        elif "metformin" in name:
            item["rationale"] = "Diabetes is active. Glucose is 149 mg/dL then 129 mg/dL."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
    _add_alternative(
        plan,
        "hydrochlorothiazide 25 MG Oral Tablet",
        "restart",
        "Restart is acceptable only with planned sodium checks if blood pressure is not controlled on lisinopril alone. The reference does not restart it.",
    )
    _add_alternative(
        plan,
        "lisinopril 10 MG Oral Tablet",
        "hold",
        "Hold is acceptable if the rise from 1.0 mg/dL to 1.2 mg/dL is judged to be acute kidney injury. The reference keeps the 30-day supply.",
    )
    _retitle(plan, "Primary care follow-up")


def _reference_805(evaluator: dict[str, Any]) -> None:
    plan = evaluator["reference_discharge_plan"]
    for item in plan["medications"]:
        name = str(item.get("medication"))
        if "furosemide" in name:
            item["action"] = "continue"
            item["route"] = "oral"
            item["dose"] = "40 MG"
            item["frequency"] = "once daily"
            item["rationale"] = (
                "The only recorded order is 40 mg oral once daily. Discharge weight is 78 kg and dry weight is 73 kg. "
                "Oxygen saturation and natriuretic peptide improved. Continuation is not a claim that dry weight was reached. "
                "No intravenous dose is stored in the project regimen."
            )
            item["evidence_class"] = "CLINICALLY_AMBIGUOUS"
        elif "metoprolol" in name:
            item["rationale"] = (
                "The same 25 mg daily dose is on the home and inpatient lists. "
                "Discharge blood pressure is 110/84 mmHg. No ejection fraction is recorded."
            )
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
        elif "atorvastatin" in name:
            item["rationale"] = "Hyperlipidemia is active and the inpatient row is active."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
    _add_alternative(
        plan,
        "furosemide 40 MG Oral Tablet",
        "modify",
        "Increasing the loop diuretic, or deferring discharge until weight is closer to 73 kg, is acceptable. No intravenous dose is stored, so no numeric intravenous dose is specified. REQUIRES_CLINICIAN_DECISION for the increased dose.",
    )
    _add_alternative(
        plan,
        "Additional systolic heart-failure therapy (ACE inhibitor, ARNI, SGLT2 inhibitor, or MRA)",
        "start",
        "An additional class is acceptable and is not required. Discharge creatinine is 0.9 mg/dL and potassium is 4.3 mmol/L. No ejection fraction is recorded.",
    )
    _retitle(plan, "Heart-failure clinic follow-up")


def _reference_809(evaluator: dict[str, Any]) -> None:
    plan = evaluator["reference_discharge_plan"]
    for item in plan["medications"]:
        name = str(item.get("medication"))
        if "ceftriaxone" in name:
            item["action"] = "start"
            item["duration"] = None
            item["rationale"] = (
                "Started during the admission. A vegetation is present. The admission culture grew gram-positive cocci, "
                "and a later culture showed no growth. The source chart does not record a remaining duration, so none is added."
            )
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
        elif "lisinopril" in name:
            item["action"] = "continue"
            item["rationale"] = (
                "Creatinine is 1.3 mg/dL then 0.8 mg/dL. No creatinine from before this admission is recorded. "
                "Hold is acceptable if 1.3 mg/dL is judged to be acute kidney injury."
            )
            item["evidence_class"] = "CLINICALLY_AMBIGUOUS"
        elif "atorvastatin" in name:
            item["rationale"] = "Hyperlipidemia is active and the inpatient row is active."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
    _add_alternative(
        plan,
        "lisinopril 10 MG Oral Tablet",
        "hold",
        "Hold is acceptable if creatinine 1.3 mg/dL is judged to be acute kidney injury. No prior baseline is recorded, so the reference does not require a hold.",
    )
    _retitle(plan, "Infectious-disease follow-up")


def _reference_813(evaluator: dict[str, Any]) -> None:
    plan = evaluator["reference_discharge_plan"]
    for item in plan["medications"]:
        name = str(item.get("medication"))
        if "valganciclovir" in name:
            item["action"] = "start"
            item["rationale"] = (
                "Start 900 mg orally twice daily after the admission viral-load result. "
                "The drug is not on the home list. Creatinine is 1.2 mg/dL then 1.0 mg/dL. "
                "The 450 mg tablet is the product strength."
            )
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
        elif "tacrolimus" in name:
            item["rationale"] = (
                "Tacrolimus 1 mg every 12 hours is the recorded immunosuppressant and was given through the stay. "
                "No trough is recorded. A temporary reduction is acceptable."
            )
            item["evidence_class"] = "CLINICALLY_AMBIGUOUS"
        elif "amlodipine" in name:
            item["rationale"] = "Hypertension is active and amlodipine is on the home and inpatient lists."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
        elif "atorvastatin" in name:
            item["rationale"] = "Hyperlipidemia is active and atorvastatin is on the home and inpatient lists."
            item["evidence_class"] = "SUFFICIENT_VISIBLE_EVIDENCE"
    _add_alternative(
        plan,
        "BX Rating tacrolimus 1 MG Oral Capsule",
        "modify",
        "A temporary reduction is acceptable if the transplant service documents one. No trough and no reduction are recorded, so the reference continues 1 mg every 12 hours.",
    )
    _retitle(plan, "Transplant clinic follow-up")


_REFERENCE = {
    "VAL-801": _reference_801,
    "VAL-802": _reference_802,
    "VAL-803": _reference_803,
    "VAL-805": _reference_805,
    "VAL-809": _reference_809,
    "VAL-813": _reference_813,
}


def build_case(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    resident = json.loads((CLEAN / f"{case_id}_resident.json").read_text(encoding="utf-8"))
    evaluator = json.loads((CLEAN / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
    _NARRATIVE[case_id](resident)
    _NARRATIVE[case_id](evaluator)
    _REFERENCE[case_id](evaluator)
    evaluator["clinician_review_status"] = "PREPARED_FOR_RE_REVIEW"
    resident.pop("reference_discharge_plan", None)
    resident.pop("clinician_review_status", None)
    return resident, evaluator


def leak_hits(resident: dict[str, Any]) -> list[str]:
    text = json.dumps(resident)
    return [pattern for pattern in LEAK_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]


def old_design_hits(resident: dict[str, Any]) -> list[str]:
    text = json.dumps(resident)
    return [pattern for pattern in OLD_DESIGN_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE)]


def _evidence_gate() -> None:
    allowed = {
        "REVISED",
        "NOT_CHANGED",
        "SOURCE_SELECTION_AMBIGUITY",
        "NOT_COMPLETED_IN_ROUND_1",
        "REQUIRES_CLINICIAN_DECISION",
    }
    classes = {
        "CASE_SOURCE",
        "REPOSITORY_SOURCE",
        "DATABASE",
        "CLINICAL_LITERATURE",
        "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE",
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
        if row["classification"] not in classes and row["classification"] != "REQUIRES_CLINICIAN_DECISION":
            raise ValueError(row["classification"])
        if not row["source"]:
            raise ValueError(row["case"])
    allowed_ref = {"SUFFICIENT_VISIBLE_EVIDENCE", "WEAK_VISIBLE_EVIDENCE", "CLINICALLY_AMBIGUOUS"}
    for row in REFERENCE_EVIDENCE:
        if row["classification"] not in allowed_ref:
            raise ValueError(row["medication"])


def _cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ")


def _clinical_revision_log() -> str:
    lines = [
        "# Clinical revision log",
        "",
        "Each row is one clinical concern from the Round 1 review. "
        "Version 3 is prepared for re-review. It is not clinically validated.",
        "",
        "| ID | COMMENT | REVISION | LOCATION | OLD | NEW | CLINICAL REASONING | EVIDENCE |",
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
        "Changes from the clean pre-injection chart. Items with no change in the represented fact are in the clinical revision log.",
        "",
        "| Case | Location | Old | New | Comment addressed | Clinical reasoning | Evidence |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in REVIEW_ITEMS:
        if item["old"] == item["new"]:
            continue
        if item["status"] == "NOT_COMPLETED_IN_ROUND_1" and "30 days" not in item["new"]:
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
        "Literature supports a clinical relationship. It is not a measurement that was absent from the chart. "
        "A synthetic finding is labeled as such.",
        "",
        "| Case | Change | Old representation | New representation | Source | Classification |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in LEDGER:
        cells = [row["case"], row["change"], row["old"], row["new"], row["source"], row["classification"]]
        lines.append("| " + " | ".join(_cell(cell) for cell in cells) + " |")
    lines.extend(["", "## Evidence notes", ""])
    for key, text in EVIDENCE_NOTES.items():
        lines.append(f"{key} {text}")
        lines.append("")
    return "\n".join(lines)


def _answer_leak_audit(cases: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Answer-leak audit, version 3",
        "",
        "Scope: resident JSON for VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. "
        "Historical Round 1 text in the codebook is not resident-chart text. "
        "The clinician adjudication questions sit after the hidden reference and are not resident text.",
        "",
        "Searched phrases: intended, intended at discharge, continue after discharge, should continue, "
        "should stop, restart, resume, planned outpatient regimen, planned antibiotic course, "
        "correct medication, expected regimen, take exactly as listed, no reason to stop, "
        "no discharge medicine is stopped, verified list at discharge, are continued, "
        "complete the planned parenteral course, use the verified list.",
        "",
        "| Case | Pattern | Severity |",
        "| --- | --- | --- |",
    ]
    total = 0
    for case_id in CASE_IDS:
        hits = leak_hits(cases[case_id])
        total += len(hits)
        if not hits:
            lines.append(f"| {case_id} | none | DIRECT_ANSWER_LEAK = 0 |")
        for hit in hits:
            lines.append(f"| {case_id} | {hit} | DIRECT_ANSWER_LEAK |")
    lines.extend(
        [
            "",
            f"DIRECT_ANSWER_LEAK count: {total}.",
            "",
            "Removed resident sentences from version 2: “No bleeding and no kidney injury are recorded as a reason to stop it.” "
            "“Use the verified collateral medication list at discharge.” "
            "“Hydrochlorothiazide, lisinopril, atorvastatin, and metformin are continued. No discharge medicine is stopped.” "
            "“Complete the planned parenteral course with laboratory follow-up.”",
            "",
        ]
    )
    return "\n".join(lines)


def _reference_audit(evaluators: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Reference-evidence audit, version 3",
        "",
        "Every hidden reference action is classified from the resident chart. "
        "Allowed classes are SUFFICIENT_VISIBLE_EVIDENCE, WEAK_VISIBLE_EVIDENCE, and CLINICALLY_AMBIGUOUS.",
        "",
        "| Case | Medication | Action | Classification | Why |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in REFERENCE_EVIDENCE:
        lines.append(
            "| "
            + " | ".join(
                _cell(row[key])
                for key in ("case", "medication", "action", "classification", "why")
            )
            + " |"
        )
    lines.extend(["", "## Agreement with evaluator files", ""])
    for row in REFERENCE_EVIDENCE:
        if row["action"] == "start" and "Additional systolic" in row["medication"]:
            alternatives = evaluators[row["case"]]["reference_discharge_plan"].get("acceptable_alternatives") or []
            found = any(row["action"] == item.get("action") and "Additional" in str(item.get("medication")) for item in alternatives)
        else:
            medications = evaluators[row["case"]]["reference_discharge_plan"]["medications"]
            found = any(
                item.get("medication") == row["medication"] and item.get("action") == row["action"]
                for item in medications
            )
            if not found:
                alternatives = evaluators[row["case"]]["reference_discharge_plan"].get("acceptable_alternatives") or []
                found = any(
                    item.get("medication") == row["medication"] and item.get("action") == row["action"]
                    for item in alternatives
                )
        lines.append(f"- {row['case']} {row['medication']} {row['action']}: {'matched' if found else 'MISSING'}")
    lines.extend(
        [
            "",
            "HIDDEN_REFERENCE_DEPENDENCY count: 0.",
            "CLINICALLY_INCONSISTENT count: 0.",
            "",
            "Ambiguous actions and their alternatives are on the reference plan and in the case-specific adjudication question.",
            "",
        ]
    )
    return "\n".join(lines)


def _snippet(value: str, limit: int = 360) -> str:
    text = " ".join(value.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _fields(case: dict[str, Any] | None) -> dict[str, str]:
    if case is None:
        return {}
    clinical = case["ClinicalCase"]
    fields = {
        "one_liner": str(clinical.get("one_liner") or ""),
        "hpi": str((clinical.get("presentation") or {}).get("hpi") or ""),
    }
    for note in case.get("CaseNote") or []:
        fields[f"note:{note.get('note_type')}"] = str(note.get("note_text") or "")
    for consult in case.get("CaseConsult") or []:
        fields[f"consult:{consult.get('service')}"] = str(consult.get("recommendation") or "")
    for follow in case.get("CaseFollowup") or []:
        fields["followup"] = str(follow.get("item") or "")
    for medication in case.get("CaseMedication") or []:
        key = f"med:{medication.get('context')}:{medication.get('drug')}"
        fields[key] = (
            f"status={medication.get('status')}; dose={medication.get('dose')}; "
            f"route={medication.get('route')}; frequency={medication.get('frequency')}; "
            f"held={medication.get('held_reason')}"
        )
    for lab in case.get("CaseLab") or []:
        fields[f"lab:{lab.get('timepoint')}:{lab.get('test_name')}"] = f"{lab.get('value')} {lab.get('unit')}"
    for vital in case.get("CaseVital") or []:
        fields[f"vital:{vital.get('timepoint')}"] = (
            f"temp={vital.get('temp_c')}; bp={vital.get('bp_systolic')}/{vital.get('bp_diastolic')}; "
            f"hr={vital.get('heart_rate')}"
        )
    for weight in case.get("CaseWeight") or []:
        fields[f"weight:{weight.get('timepoint')}"] = (
            f"{weight.get('weight_kg')} dry={weight.get('dry_weight_kg')}"
        )
    for io in case.get("CaseIntakeOutput") or []:
        fields[f"io:{io.get('timepoint')}"] = (
            f"in={io.get('intake_ml')} out={io.get('output_ml')} net={io.get('net_ml')}"
        )
    for micro in case.get("CaseMicrobiology") or []:
        fields[f"micro:{micro.get('timepoint')}"] = f"{micro.get('organism')} {micro.get('result')}"
    for image in case.get("CaseImaging") or []:
        fields[f"imaging:{image.get('study_type')}"] = str(image.get("finding") or "")
    plan = case.get("reference_discharge_plan") or {}
    for item in plan.get("medications") or []:
        fields[f"ref:{item.get('medication')}"] = (
            f"action={item.get('action')}; dose={item.get('dose')}; route={item.get('route')}; "
            f"frequency={item.get('frequency')}; duration={item.get('duration')}"
        )
    alternatives = plan.get("acceptable_alternatives") or []
    if alternatives:
        fields["ref:alternatives"] = "; ".join(
            f"{item.get('medication')}={item.get('action')}" for item in alternatives
        )
    else:
        fields["ref:alternatives"] = "none"
    return fields


def _provenance(version: str, case_id: str, value: str, clean_value: str | None) -> str:
    if clean_value is not None and value == clean_value:
        return f"CASE_SOURCE. Same text as exports/clean_balanced_seed_set/{case_id}."
    if version == "v1":
        return (
            "exports/ko_revised_cases_v1. This text is not the clean pre-injection chart. "
            "It comes from the first revision attempt."
        )
    return (
        "exports/ko_cycle2_revised_validation_v2, produced by app/services/cycle2_v2_cases.py "
        "from the clean chart. A wording change here is not a new measurement."
    )


def _judgment(case_id: str, field: str, v1: str, v2: str, clean: str | None) -> tuple[str, str]:
    if field.startswith("lab:") and "Sodium" in field and case_id == "VAL-803":
        return (
            "V1 numbers, relabeled",
            "The sodium pair is not a source laboratory. It is kept only as SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE because hydrochlorothiazide is on the list and the review asked for a cause. The version 1 discharge sentence is not kept.",
        )
    if case_id == "VAL-801" and field == "vital:admission_standing":
        return (
            "V3 addition",
            "Version 2 described a 20 mmHg fall that was not in the vital table. Version 3 puts 116 mmHg on its own row and leaves the source 136/78 mmHg row unchanged.",
        )
    if case_id == "VAL-809" and field in {"hpi", "note:admission", "note:hospital_course"}:
        return (
            "Neither version copied",
            "Version 1 replaces 36.80°C, names viridans group streptococcus, and adds a dental extraction. Version 2 keeps the source facts and still tells the resident to complete a planned course in the consultation. Version 3 keeps the source vitals and organism, adds a labeled home temperature and poor dentition, and does not state the discharge antibiotic plan.",
        )
    if case_id == "VAL-803" and field in {"hpi", "note:admission", "note:hospital_course"}:
        return (
            "Neither version copied",
            "Version 2 states that every medicine is continued and that no discharge medicine is stopped. Version 1 states that hydrochlorothiazide was held because the sodium was 128 mmol/L, which is the discharge conclusion written as a course sentence. Version 3 shows the sodium pair and the inpatient hold without stating the discharge action.",
        )
    if case_id == "VAL-801" and field in {"hpi", "note:hospital_course", "consult:geriatrics"}:
        return (
            "Neither version copied",
            "Version 2 says there is no reason to stop ibuprofen and tells the resident to use the verified list at discharge. Version 1 invents knee pain and states that no bleeding was found as the close of the argument. Version 3 keeps the poor-intake precipitant and the medication list without choosing the discharge action.",
        )
    if v1 == v2:
        if clean is not None and v1 == clean:
            return ("Either", "V1 and V2 match the clean chart. Version 3 starts from that recorded value.")
        return ("Either", "V1 and V2 agree with each other. Version 3 keeps the shared fact when the resident chart does not use it as a discharge order.")
    if clean is not None and v2 == clean and v1 != clean:
        return (
            "V2",
            "V2 matches the clean pre-injection chart. V1 changes a recorded fact without a source measurement. Version 3 starts from the recorded fact.",
        )
    if clean is not None and v1 == clean and v2 != clean:
        return (
            "V3 wording of the clean fact",
            "V2 changes the clean wording. Version 3 keeps the clean fact and drops any sentence that states the discharge action.",
        )
    return (
        "V3",
        "Neither version is copied as a block. Source measurements are kept. Invented measurements are not kept just because they make a fuller story.",
    )


def _reconciliation(built: dict[str, tuple[dict[str, Any], dict[str, Any]]]) -> str:
    lines = [
        "# Set 1 version reconciliation",
        "",
        "V1 is exports/ko_revised_cases_v1. V2 is exports/ko_cycle2_revised_validation_v2. "
        "The clean pre-injection charts are exports/clean_balanced_seed_set. "
        "A more detailed version is not preferred. A detail is a starting value for version 3 only with provenance and a clinical reason.",
        "",
        "## Why the two packages diverged",
        "",
        "Version 1 rewrote the six stories so that each Round 1 comment had a concrete finding: a dehydration examination, a baseline creatinine, a sodium pair and a thiazide hold, a new weight curve with intravenous furosemide and an ejection fraction of 30 percent, fever in place of the recorded temperature plus a dental extraction and viridans group streptococcus, and mycophenolate. Several of those details are not in the clean chart and are not in a repository dose file.",
        "",
        "Version 2 started again from the clean charts and refused those invented measurements. It kept the source weights, the single intake-and-output day, oral furosemide, the temperature 36.80°C, gram-positive cocci, and the transplant list without mycophenolate. It also left discharge-conclusion sentences in the resident chart, and the shared codebook still asked about an ejection fraction of 30 percent and about mycophenolate.",
        "",
        "Version 3 keeps a source measurement over a more detailed invented one. Synthetic additions are limited to the precipitant the review said was missing. They are labeled. They do not replace a recorded vital, and they do not state the discharge action.",
        "",
        "## Starting source for each case",
        "",
        "| Case | Starting source | What version 3 does not take from version 1 |",
        "| --- | --- | --- |",
        "| VAL-801 | Clean chart, plus the version 2 precipitant rewritten so it does not choose the ibuprofen action | Knee pain as an invented indication |",
        "| VAL-802 | Version 2 / clean laboratories. No baseline creatinine | Creatinine 1.2 mg/dL six weeks earlier, and the potassium pair |",
        "| VAL-803 | Clean chart. Sodium pair from version 1, relabeled synthetic. Discharge sentence from neither version | The sentence that hydrochlorothiazide was held as the completed discharge story |",
        "| VAL-805 | Clean / version 2 weights, intake and output, oral furosemide, and absent ejection fraction | 86 kg to 80 kg, dry weight 80 kg, intravenous 40 mg twice daily, ejection fraction 30 percent |",
        "| VAL-809 | Clean / version 2 vitals, organism, vegetation, and creatinine | Replacement of 36.80°C, dental extraction, viridans group streptococcus, invented baseline, mechanical valve |",
        "| VAL-813 | Version 2 chronology: valganciclovir is not a home medicine | Mycophenolate |",
        "",
        "## Field comparison",
        "",
        "Fields that are identical in V1, V2, and the clean chart are omitted. Every remaining clinical field is listed.",
        "",
        "| CASE | FIELD | V1 | V2 | SOURCE/PROVENANCE OF V1 | SOURCE/PROVENANCE OF V2 | WHICH IS CLINICALLY BETTER SUPPORTED | WHY | STARTING VALUE FOR V3 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for case_id in CASE_IDS:
        v1_case = json.loads((V1 / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
        v2_case = json.loads((V2 / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
        clean_case = json.loads((CLEAN / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
        resident, evaluator = built[case_id]
        v3_fields = _fields(resident)
        v3_fields.update({key: value for key, value in _fields(evaluator).items() if key.startswith("ref:")})
        f1, f2, clean_fields = _fields(v1_case), _fields(v2_case), _fields(clean_case)
        keys = sorted(set(f1) | set(f2) | set(v3_fields) | set(clean_fields))
        for key in keys:
            left, right, source, current = f1.get(key, ""), f2.get(key, ""), clean_fields.get(key), v3_fields.get(key, "")
            if left == right == (source or "") and current == left:
                continue
            if left == right and current == left and source is None:
                continue
            which, why = _judgment(case_id, key, left, right, source)
            cells = [
                case_id,
                key,
                _snippet(left or "—"),
                _snippet(right or "—"),
                _provenance("v1", case_id, left, source),
                _provenance("v2", case_id, right, source),
                which,
                why,
                _snippet(current or "—"),
            ]
            lines.append("| " + " | ".join(_cell(cell) for cell in cells) + " |")
    lines.append("")
    return "\n".join(lines)


def _katie_reaudit(cases: dict[str, dict[str, Any]], evaluators: dict[str, dict[str, Any]]) -> str:
    leak_total = sum(len(leak_hits(cases[case_id])) for case_id in CASE_IDS)
    design_total = sum(len(old_design_hits(cases[case_id])) for case_id in CASE_IDS)
    bad_class = [
        row["classification"]
        for row in REFERENCE_EVIDENCE
        if row["classification"] in {"HIDDEN_REFERENCE_DEPENDENCY", "CLINICALLY_INCONSISTENT"}
    ]
    absent = []
    for case_id, question in SPECIAL_QUESTIONS.items():
        if case_id == "VAL-805" and "30 percent" in question:
            absent.append(case_id)
        if case_id == "VAL-813" and "mycophenolate" in question.lower():
            absent.append(case_id)
        if "ejection fraction 30" in question.lower():
            absent.append(case_id)
    lines = [
        "# Katie re-audit, Set 1 version 3",
        "",
        "These six cases are prepared for re-review. They are not clinically validated.",
        "",
        "| Gate | Result |",
        "| --- | --- |",
        f"| Cases | {len(CASE_IDS)} |",
        f"| DIRECT_ANSWER_LEAK | {leak_total} |",
        f"| HIDDEN_REFERENCE_DEPENDENCY | {sum(1 for row in REFERENCE_EVIDENCE if row['classification'] == 'HIDDEN_REFERENCE_DEPENDENCY')} |",
        f"| CLINICALLY_INCONSISTENT | {sum(1 for row in REFERENCE_EVIDENCE if row['classification'] == 'CLINICALLY_INCONSISTENT')} |",
        f"| CODEBOOK REFERENCES ABSENT FACT | {len(absent)} |",
        "| README/V3 MISMATCH | see README_V3_FACT_CHECK.md after the documentation check |",
        f"| OLD ERROR-INJECTION LANGUAGE in resident charts | {design_total} |",
        "",
        "| Case | Round 1 problem addressed | Resident chart states the discharge action | Reference class outside the allowed set | Codebook cites an absent fact | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    summaries = {
        "VAL-801": "Partial. A precipitant is visible. Infection was not added. Ibuprofen is no longer stopped without a reason, and the chart does not choose the discharge action.",
        "VAL-802": "Partial. The course is readable and no baseline was invented. Lisinopril remains ambiguous, and the alternative is encoded. The recorded recommendation was Exclude.",
        "VAL-803": "Partial. A sodium precipitant was added and labeled synthetic. C2 through the overall recommendation were not completed and stay blank.",
        "VAL-805": "Partial. Source weights and the oral dose remain. No intravenous dose and no ejection fraction were invented. The diuretic action is ambiguous.",
        "VAL-809": "Partial. Source temperatures and the organism remain. A labeled home fever and poor dentition were added. No valve was added. The antibiotic duration is not invented.",
        "VAL-813": "Partial. Valganciclovir is no longer a home medicine. No extra immunosuppressant was added. Potassium still has no cause. The recorded recommendation was Exclude.",
    }
    for case_id in CASE_IDS:
        leaks = leak_hits(cases[case_id])
        outside = [
            row["classification"]
            for row in REFERENCE_EVIDENCE
            if row["case"] == case_id and row["classification"] not in {
                "SUFFICIENT_VISIBLE_EVIDENCE",
                "WEAK_VISIBLE_EVIDENCE",
                "CLINICALLY_AMBIGUOUS",
            }
        ]
        question_problem = "no" if case_id not in absent else "yes"
        lines.append(
            f"| {case_id} | {summaries[case_id]} | {'yes' if leaks else 'no'} | "
            f"{'yes' if outside else 'no'} | {question_problem} | Prepared for re-review |"
        )
    lines.extend(
        [
            "",
            "Set 2 was not re-audited and was not edited.",
            "",
            "Reference classes used:",
            "",
        ]
    )
    for row in REFERENCE_EVIDENCE:
        if row["case"] in evaluators:
            lines.append(f"- {row['case']} {row['medication']}: {row['classification']}")
    if bad_class:
        lines.append("")
        lines.append("Disallowed classes present: " + ", ".join(bad_class))
    lines.append("")
    return "\n".join(lines)


def readme_mismatches(readme: str, cases: dict[str, dict[str, Any]]) -> list[str]:
    """Compare the six current-case narratives with the version 3 resident charts."""
    errors: list[str] = []
    if "exports/ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx" not in readme:
        errors.append("README does not link the version 3 codebook")
    current = re.findall(
        r"\[[^\]]+\]\((exports/ko_cycle2_revised_validation_v2/[^)]+)\)",
        readme,
    )
    if current:
        errors.append("README still links version 2 as a current target: " + ", ".join(current))
    start = readme.find("#### VAL-801")
    end = readme.find("### Cases that needed narrower consistency corrections")
    if start < 0 or end < 0:
        return ["README is missing the six-case narrative block"]
    block = readme[start:end]
    parts = re.split(r"#### (VAL-80\d|VAL-81\d) —", block)
    sections: dict[str, str] = {}
    for index in range(1, len(parts), 2):
        sections[parts[index]] = parts[index + 1]
    banned = (
        "dental extraction",
        "viridans",
        "mycophenolate",
        "30 percent",
        "ejection fraction 30",
        "six weeks",
        "38.6",
        "86 kg",
        "intravenous 40",
        "40 mg twice",
        "baseline creatinine of 1.2",
        "1.2 mg/dL six weeks",
    )
    for case_id in CASE_IDS:
        section = sections.get(case_id, "")
        if not section:
            errors.append(f"{case_id} narrative missing")
            continue
        blob = json.dumps(cases[case_id]).lower()
        for phrase in banned:
            if phrase in section.lower() and phrase not in blob:
                errors.append(f"{case_id} README contains absent fact: {phrase}")
        if case_id == "VAL-803" and "128" not in section:
            errors.append("VAL-803 README omits the sodium value that is in the chart")
        if case_id == "VAL-805" and "73" not in section:
            errors.append("VAL-805 README omits dry weight 73 kg")
        if case_id == "VAL-809" and "36.80" not in section:
            errors.append("VAL-809 README omits recorded temperature 36.80")
        if case_id == "VAL-813" and "mycophenolate" in section.lower():
            errors.append("VAL-813 README mentions mycophenolate")
        if case_id == "VAL-802" and "six weeks" in section.lower():
            errors.append("VAL-802 README restores a baseline interval")
    return errors


def _response_section(document: WordDocument, case_id: str) -> None:
    heading = document.add_paragraph()
    heading.paragraph_format.page_break_before = True
    heading.paragraph_format.keep_with_next = True
    _set_run_font(heading.add_run("CLINICAL REVISION RECORD"), size=14, bold=True, color=NAVY)
    rows = tuple(
        (
            item["comment"],
            item["revision"],
            item["location"],
            item["old"],
            item["new"],
            item["reasoning"] + " " + item["evidence"],
        )
        for item in REVIEW_ITEMS
        if item["case"] == case_id
    )
    from app.services.cycle2_split_casebooks import _bordered_table

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
    _add_heading(document, "Evidence references", 3)
    for key, text in EVIDENCE_NOTES.items():
        cited = any(key in item["evidence"] or key in item["reasoning"] for item in REVIEW_ITEMS if item["case"] == case_id)
        cited = cited or any(key in row["source"] for row in LEDGER if row["case"] == case_id)
        if cited:
            _add_body(document, f"{key} {text}")


def _write_codebook(directory: Path, built: dict[str, tuple[dict[str, Any], dict[str, Any]]]) -> Path:
    from app.services.round1_six_case_review import completed_reviews

    document = _new_document("CliniProof Cycle 2  |  Set 1 revised cases, version 3")
    prepare_form_document(document)
    _add_heading(document, "CliniProof", 0)
    _add_body(document, "Clinical Revision Round 2, version 3")
    _add_heading(document, "SET 1", 1)
    _add_heading(document, "REVISED CASES FOLLOWING ROUND 1 CLINICIAN FEEDBACK", 2)
    _add_body(document, "Cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, VAL-813")
    _add_body(
        document,
        "Each case opens with the chart a resident would see. Complete the blank Round 2 form, "
        "including C1 and C2, before you read the hidden reference, the historical Round 1 record, "
        "or the clinical revision record. This file contains the six cases that received Round 1 "
        "feedback. The other eighteen cases are not in this file. Prepared for re-review does not "
        "mean clinically validated.",
    )
    reviews = completed_reviews()
    for case_id in CASE_IDS:
        resident, evaluator = built[case_id]
        row = {
            "case_id": case_id,
            "resident": resident,
            "evaluator": evaluator,
            "special_question": SPECIAL_QUESTIONS[case_id],
        }
        banner = document.add_paragraph()
        banner.paragraph_format.page_break_before = True
        banner.paragraph_format.keep_with_next = True
        _set_run_font(banner.add_run(f"CASE {case_id}"), size=16, bold=True, color=NAVY)
        _add_body(document, "Round 2 revised case, version 3. Prepared for re-review.")
        _add_heading(document, "RESIDENT-FACING CHART", 2)
        _add_body(
            document,
            "This opening chart is the same information the resident would see. It does not include the hidden reference.",
        )
        _chart(document, resident)
        _round2_form(document, row)
        _historical_section(document, reviews[case_id])
        _response_section(document, case_id)
    path = directory / "CliniProof_Cycle2_Revised_Cases_Validation.docx"
    document.save(str(path))
    finalize_word_form(path)
    return path


def _readme() -> str:
    return "\n".join(
        [
            "# Set 1 revised cases, version 3",
            "",
            "This is the current Set 1 package. Open "
            "[CliniProof_Cycle2_Revised_Cases_Validation.docx]"
            "(CliniProof_Cycle2_Revised_Cases_Validation.docx).",
            "",
            "The file contains VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. "
            "Each case opens with the resident-facing chart and a blank Round 2 form. "
            "The historical Round 1 ratings and comments follow that form. The clinical "
            "revision record and the evidence references follow the historical record. "
            "VAL-803 items that were blank in Round 1 remain marked not completed.",
            "",
            "Version 1 and version 2 are superseded revision attempts. They are not deleted.",
            "",
            "Prepared for re-review does not mean clinically validated.",
            "",
        ]
    )


def _manifest() -> str:
    lines = [
        "# Set 1 version 3 manifest",
        "",
        "Current Set 1 codebook: `CliniProof_Cycle2_Revised_Cases_Validation.docx`.",
        "",
        "| Case | Resident file | Evaluator file |",
        "| --- | --- | --- |",
    ]
    for case_id in CASE_IDS:
        lines.append(f"| {case_id} | `{case_id}_resident.json` | `{case_id}_evaluator.json` |")
    lines.append("")
    lines.append("Prepared for re-review. Not clinically validated.")
    lines.append("")
    return "\n".join(lines)


def write_revision_package(directory: Path) -> Path:
    """Write the six cases, the revision record, and the version 3 codebook."""
    _evidence_gate()
    directory.mkdir(parents=True, exist_ok=True)
    write_feedback_files(directory)
    built: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    residents: dict[str, dict[str, Any]] = {}
    evaluators: dict[str, dict[str, Any]] = {}
    for case_id in CASE_IDS:
        resident, evaluator = build_case(case_id)
        hits = leak_hits(resident)
        if hits:
            raise ValueError(f"{case_id} leak: {hits}")
        if old_design_hits(resident):
            raise ValueError(f"{case_id} old design language: {old_design_hits(resident)}")
        if "reference_discharge_plan" in resident:
            raise ValueError(case_id)
        built[case_id] = (resident, evaluator)
        residents[case_id] = resident
        evaluators[case_id] = evaluator
        (directory / f"{case_id}_resident.json").write_text(
            json.dumps(resident, indent=2) + "\n",
            encoding="utf-8",
        )
        (directory / f"{case_id}_evaluator.json").write_text(
            json.dumps(evaluator, indent=2) + "\n",
            encoding="utf-8",
        )
    (directory / "CLINICAL_REVISION_LOG.md").write_text(_clinical_revision_log(), encoding="utf-8")
    (directory / "REVISION_DIFF.md").write_text(_revision_diff(), encoding="utf-8")
    (directory / "REVISION_EVIDENCE_LEDGER.md").write_text(_ledger(), encoding="utf-8")
    (directory / "SET1_VERSION_RECONCILIATION.md").write_text(_reconciliation(built), encoding="utf-8")
    (directory / "ANSWER_LEAK_AUDIT.md").write_text(_answer_leak_audit(residents), encoding="utf-8")
    (directory / "REFERENCE_EVIDENCE_AUDIT.md").write_text(_reference_audit(evaluators), encoding="utf-8")
    (directory / "KATIE_REAUDIT.md").write_text(_katie_reaudit(residents, evaluators), encoding="utf-8")
    readme_path = ROOT / "README.md"
    mismatches = readme_mismatches(readme_path.read_text(encoding="utf-8"), residents) if readme_path.is_file() else ["README.md missing"]
    fact_lines = ["# README / version 3 fact check", ""]
    if mismatches:
        fact_lines.append(f"README/V3 MISMATCH = {len(mismatches)}.")
        fact_lines.extend(f"- {item}" for item in mismatches)
    else:
        fact_lines.append("README/V3 MISMATCH = 0.")
    fact_lines.append("")
    (directory / "README_V3_FACT_CHECK.md").write_text("\n".join(fact_lines), encoding="utf-8")
    (directory / "README.md").write_text(_readme(), encoding="utf-8")
    (directory / "MANIFEST.md").write_text(_manifest(), encoding="utf-8")
    for case_id, question in SPECIAL_QUESTIONS.items():
        if "30 percent" in question or "mycophenolate" in question.lower():
            raise ValueError(question)
    return _write_codebook(directory, built)


def label_superseded() -> None:
    note = "\n".join(
        [
            "# SUPERSEDED REVISION ATTEMPT",
            "",
            "This directory is not the current Set 1 package. The cases here were not deleted and were not rewritten.",
            "",
            "The current Set 1 codebook is "
            "[CliniProof_Cycle2_Revised_Cases_Validation.docx](../ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx).",
            "",
            "Prepared for re-review does not mean clinically validated.",
            "",
        ]
    )
    for folder in (V1, V2):
        (folder / "SUPERSEDED.md").write_text(note, encoding="utf-8")
    readme = V2 / "README.md"
    text = readme.read_text(encoding="utf-8")
    banner = (
        "SUPERSEDED REVISION ATTEMPT. This is not the current Set 1 package. "
        "The current codebook is "
        "[version 3](../ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx).\n\n"
    )
    if not text.startswith("SUPERSEDED"):
        readme.write_text(banner + text, encoding="utf-8")
