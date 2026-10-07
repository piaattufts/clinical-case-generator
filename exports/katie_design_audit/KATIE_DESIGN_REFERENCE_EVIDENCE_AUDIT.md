# Reference-evidence audit

Question for every hidden reference action: could a resident reach that action from the resident-facing chart alone?

Labels: `SUFFICIENT_VISIBLE_EVIDENCE`, `WEAK_VISIBLE_EVIDENCE`, `HIDDEN_REFERENCE_DEPENDENCY`, `CLINICALLY_AMBIGUOUS`, `CLINICALLY_INCONSISTENT`.

"It was a home medicine" and "it was started in the hospital" are not treated as enough by themselves. A visible indication, a response, or a reason for a hold has to support the action.

Acceptable alternatives are noted. If a second action is clinically defensible and absent from `acceptable_alternatives`, that is recorded.

## Set 1 — version 2 revised charts

### VAL-801

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hyperlipidemia is on the problem list. The drug is active at home and in the hospital. No adverse effect is described. |
| Lisinopril 10 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hypertension is active. Creatinine is 1.1 then 1.0 mg/dL. Blood pressure falls from 136/78 to 121/71 mmHg. |
| Metformin 500 mg twice daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Diabetes is active. Fasting glucose falls from 163 to 103 mg/dL. |
| Ibuprofen 400 mg every 8 hours as needed | continue | WEAK_VISIBLE_EVIDENCE | No bleeding is described, and creatinine is stable, but the chart also says there is no reason to stop it. That sentence does the reasoning for the resident. Delirium in a 75-year-old is a setting in which stopping an as-needed NSAID is also defensible. That alternative is not encoded. |

Direction: the orthostatic finding and dry mucous membranes were added so the delirium would have a precipitant. They are not in the vital-sign table. The reference continue actions mostly follow the medication list. The ibuprofen sentence was written to match the reference.

### VAL-802

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Lisinopril 10 mg daily | continue | CLINICALLY_AMBIGUOUS | Creatinine is 1.3 then 1.2 mg/dL. No pre-admission value exists. Hold is an encoded alternative. |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | It is on the verified list for hyperlipidemia. The chart no longer says it must be continued. |

Direction: `CASE_DRIVES_REFERENCE` for the statin. The lisinopril action is explicitly not forced.

### VAL-803

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Hydrochlorothiazide 25 mg daily | continue | HIDDEN_REFERENCE_DEPENDENCY | The course says it is continued, but no physiological cause of the delirium is shown. A resident who takes the diagnosis seriously cannot tell whether the thiazide should stop. Sodium is not in the chart. |
| Lisinopril 10 mg daily, 30 days | continue | WEAK_VISIBLE_EVIDENCE | Creatinine rises from 1.0 to 1.2 mg/dL. The 30-day duration exists only on the evaluator plan. The resident chart does not show a day supply. |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hyperlipidemia and an active inpatient row. |
| Metformin 500 mg twice daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Diabetes. Glucose falls from 149 to 129 mg/dL. |

Direction: `REFERENCE_APPEARS_TO_DRIVE_CASE` for the sentence that lists every continue action. The missing precipitant means the chart does not support an independent decision.

### VAL-805

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Furosemide 40 mg oral daily | continue | CLINICALLY_INCONSISTENT | Discharge weight is 78 kg and dry weight is 73 kg. One intake/output day is net −1045 mL. The home and inpatient orders are the same oral dose. Continuing that dose as a completed decongestion plan does not follow from the weights. Increasing the diuretic, or not calling the patient ready, is a reasonable alternative and is not encoded. |
| Metoprolol succinate 25 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Systolic heart failure, heart rate 93 then 69, blood pressure about 110 mmHg. |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hyperlipidemia, active inpatient row. |
| Additional ACE inhibitor, ARNI, SGLT2 inhibitor, or MRA | start, acceptable only | CLINICALLY_AMBIGUOUS | No ejection fraction is stored. Admission creatinine is 1.7 mg/dL and falls to 0.9 mg/dL. Potassium is 4.7 then 4.3 mmol/L. Starting another class is optional in the reference, which is appropriate. The codebook question cites an ejection fraction of 30 percent that the chart does not contain. |

Direction: `CASE_DRIVES_REFERENCE` for the three continued drugs, and the case is too thin for the decision the heart-failure scenario is supposed to pose.

### VAL-809

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Ceftriaxone 2 g IV daily | start | SUFFICIENT_VISIBLE_EVIDENCE | Vegetation, gram-positive cocci, later culture with no growth, and an inpatient start. The consult then tells the resident to complete the course, so the decision is not left open. Duration is null on the reference. |
| Lisinopril 10 mg daily | continue | CLINICALLY_AMBIGUOUS | Creatinine falls from 1.3 to 0.8 mg/dL with no pre-admission baseline. Hold is encoded. |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hyperlipidemia, active row. |

Direction: the endocarditis facts are the source chart, restated. They are not a full presenting illness. Temperature remains 36.80°C.

### VAL-813

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Valganciclovir 900 mg twice daily | start | SUFFICIENT_VISIBLE_EVIDENCE | Not a home medicine. The admission viral-load review detected CMV, a later review was lower, and diarrhea improved. Creatinine is 1.2 then 1.0 mg/dL. |
| Tacrolimus 1 mg every 12 hours | continue | SUFFICIENT_VISIBLE_EVIDENCE | It is the recorded immunosuppressant and was given through the stay. A temporary reduction is an encoded alternative. No trough is shown. |
| Amlodipine 5 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hypertension. Blood pressure 147/80 then 134/80 mmHg. |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hyperlipidemia. |
| Mycophenolate | not on the plan | CLINICALLY_AMBIGUOUS | A typical kidney-transplant regimen includes an antimetabolite. None is charted, so a resident cannot decide to continue, reduce, or hold it. The codebook still asks that question. |

Direction: removing home valganciclovir was done so the start action would match a new-diagnosis reading. The remaining reference follows the revised chart. Potassium 4.7 then 3.9 mmol/L has no cause and does not drive a drug change.

## Set 2 — fresh-review charts

### VAL-804

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Atorvastatin 40 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hyperlipidemia. |
| Metformin 500 mg twice daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Diabetes. Glucose 155 then 108 mg/dL. |
| Cognitive enhancer | not on the plan | HIDDEN_REFERENCE_DEPENDENCY | The chart says a start was deferred. The reference does not contain that decision, so the resident is asked about a drug the scoring plan ignores. Delirium still has no physiological cause. |

### VAL-806

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Lisinopril 10 mg daily | restart | WEAK_VISIBLE_EVIDENCE | Held for creatinine 2.8 mg/dL. Discharge creatinine is still 1.6 mg/dL. No baseline. Potassium 4.5 mmol/L and systolic pressure 116 mmHg are visible. Continued hold is encoded. |
| Furosemide, atorvastatin, metoprolol succinate | continue | SUFFICIENT_VISIBLE_EVIDENCE | Heart failure and hyperlipidemia. Furosemide matches congestion. They were not the held drug. |

Direction: `CASE_DRIVES_REFERENCE`. This is one of the clearer open decisions.

### VAL-807

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Furosemide 40 mg oral daily | continue | WEAK_VISIBLE_EVIDENCE | Weight falls from 99 kg to 93 kg. Dry weight is 95 kg, so discharge weight is below dry weight. Reducing the diuretic is a reasonable alternative and is not encoded. |
| Atorvastatin and metoprolol | continue | SUFFICIENT_VISIBLE_EVIDENCE | Matching diagnoses, stable creatinine 1.2 mg/dL, potassium 3.5 then 3.8 mmol/L. No potassium product is present, and the chart says so without prescribing one. |

### VAL-808

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Furosemide 40 mg oral daily | continue | WEAK_VISIBLE_EVIDENCE | Home and inpatient doses match. Weight falls only from 94 kg to 92 kg, and dry weight is set to 92 kg. Net intake/output is −679 mL. The follow-up title says "after diuretic adjustment," which the reference does not do. |
| Spironolactone, lisinopril, metoprolol | continue | SUFFICIENT_VISIBLE_EVIDENCE | Systolic heart failure and hypertension. Creatinine 0.9 mg/dL. Potassium 3.4 then 3.7 mmol/L. Discharge systolic pressure 142 mmHg. |

### VAL-810

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Ceftriaxone 2 g IV daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Fever 38.2°C then 36.8°C, vegetation, gram-positive bacteremia that clears. The chart also says the drug is intended after discharge, so the resident is not deciding. |
| Atorvastatin and metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Matching chronic diagnoses. Glucose 176 then 112 mg/dL. |

Direction: `REFERENCE_APPEARS_TO_DRIVE_CASE`. The intended-discharge sentence is the archetype's predetermined answer.

### VAL-811

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Ceftriaxone 2 g IV daily, 30 days | continue | WEAK_VISIBLE_EVIDENCE | Vegetation and bacteremia are present. Temperature is 36.80°C. The 30-day duration is only on the reference. The prose says the drug is intended after discharge until a planned end date that the resident cannot see. |
| Lisinopril, aspirin, metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. Creatinine 0.8 then 0.9 mg/dL. |

Direction: `REFERENCE_APPEARS_TO_DRIVE_CASE`.

### VAL-812

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Ceftriaxone 2 g IV daily | continue | CLINICALLY_AMBIGUOUS | The narrative says the remaining duration is an outpatient decision. The consult says to complete the planned course. The reference continues the drug with no duration. A resident cannot tell which instruction is the case. |
| Aspirin and atorvastatin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. |

### VAL-814

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Valganciclovir 450 mg twice daily | start | SUFFICIENT_VISIBLE_EVIDENCE | Not a home medicine. Started after an in-hospital viral load. Dose moved from 450 mg daily at creatinine 2.5 mg/dL to 450 mg twice daily at creatinine 1.6 mg/dL. |
| Mycophenolate 1000 mg twice daily | restart | CLINICALLY_AMBIGUOUS | Held for CMV diarrhea. Viral burden is later lower and diarrhea was improving, but the virus is not described as cleared. Continued hold is encoded. |
| Tacrolimus and amlodipine | continue | SUFFICIENT_VISIBLE_EVIDENCE | Unchanged home immunosuppression and blood pressure. |

Direction: `CASE_DRIVES_REFERENCE`.

### VAL-815

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Valganciclovir 900 mg twice daily | start | SUFFICIENT_VISIBLE_EVIDENCE | Not a home medicine. Started after detection. Creatinine 0.8 then 0.9 mg/dL. |
| Tacrolimus 1 mg every 12 hours | continue | SUFFICIENT_VISIBLE_EVIDENCE | Same dose at home and in hospital. Creatinine and potassium are stable. The chart repeats that there was no dose change. |
| Amlodipine, lisinopril, atorvastatin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications and stable labs. |

### VAL-816

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Valganciclovir 900 mg twice daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | The chart establishes established CMV disease already under treatment, improving symptoms, and creatinine 1.0 then 0.9 mg/dL. Remaining duration is left to follow-up. |
| Tacrolimus and atorvastatin | continue | SUFFICIENT_VISIBLE_EVIDENCE | The consult says to continue immunosuppression, which removes the decision. |

A temporary reduction of tacrolimus during CMV is a reasonable alternative and is not encoded.

### VAL-817

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Warfarin 5 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Home warfarin for atrial fibrillation, active again on the inpatient list, discharge INR 2.6, hemoglobin 9.0 then 10.1 g/dL. |
| Lisinopril and metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hypertension and diabetes. Glucose 127 then 113 mg/dL. |

Direction: `CASE_DRIVES_REFERENCE`. The follow-up title assumes resumption has occurred.

### VAL-818

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Warfarin 5 mg daily | continue | CLINICALLY_AMBIGUOUS | The chart says warfarin is intended at discharge. Hemoglobin was 7.9 g/dL on admission and 10.3 g/dL at discharge. INR is 2.3 then 2.9. Holding or reducing warfarin after a hemoglobin of 7.9 g/dL is reasonable and is not encoded. |
| Lisinopril and metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. No glucose is stored for the metformin decision. |

Direction: `REFERENCE_APPEARS_TO_DRIVE_CASE`.

### VAL-819

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Warfarin 5 mg daily, 30 days | continue | WEAK_VISIBLE_EVIDENCE | The chart says anticoagulation was already resumed. INR is 2.5 then 2.6. Creatinine 0.9 then 1.1 mg/dL. The resident is confirming a completed action. A longer hold after hip surgery is also defensible and is not encoded. |
| Lisinopril 10 mg daily, 30 days | continue | SUFFICIENT_VISIBLE_EVIDENCE | Hypertension. |

### VAL-820

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Enoxaparin 40 mg subcutaneous daily | stop | SUFFICIENT_VISIBLE_EVIDENCE | Started in hospital for prophylaxis, not a home medicine, not the atrial-fibrillation drug. |
| Warfarin 5 mg daily | continue | SUFFICIENT_VISIBLE_EVIDENCE | Atrial fibrillation. INR 3.2 then 2.0. Hemoglobin 8.3 then 11.1 g/dL. |
| Lisinopril and metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. Glucose 124 then 119 mg/dL. |

A short overlap of prophylactic enoxaparin with warfarin is a reasonable alternative and is not encoded. The codebook asks the reviewer that question. The evaluator file does not store the alternative.

Direction: `CASE_DRIVES_REFERENCE`.

### VAL-821

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Apixaban 5 mg twice daily | restart | CLINICALLY_AMBIGUOUS | Held for gastrointestinal bleeding. Hemoglobin rises from 8.7 to 10.9 g/dL. Atrial fibrillation remains. Gastroenterology follow-up is in 7 days. Continued hold is encoded. The chart does not say to resume it. |
| Lisinopril and atorvastatin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Not the held anticoagulant. |

Direction: `CASE_DRIVES_REFERENCE`.

### VAL-822

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Pantoprazole 40 mg daily | stop | CLINICALLY_INCONSISTENT | Started for gastrointestinal bleeding. Hemoglobin rises from 8.5 to 10.7 g/dL. Gastroenterology says to continue acid suppression. Stopping a PPI at the moment of discharge is not supported by the visible consult. Continuing it is a reasonable alternative and is not encoded. |
| Lisinopril, atorvastatin, metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. Glucose 153 then 126 mg/dL. |

Direction: the stop reads like a hospital-only rule applied to the reference, not like a decision that follows the consult.

### VAL-823

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Apixaban 5 mg twice daily | hold | CLINICALLY_AMBIGUOUS | Held after bleeding. Hemoglobin 9.0 then 10.2 g/dL. Endoscopy shows no ongoing bleeding. The chart and the consult say to hold and reassess. Restart at discharge is also defensible and is not encoded. |
| Atorvastatin and metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. Glucose 116 then 104 mg/dL. |

### VAL-824

| Medication | Action | Classification | Why |
| --- | --- | --- | --- |
| Aspirin 81 mg daily | stop | SUFFICIENT_VISIBLE_EVIDENCE | Gastrointestinal bleeding, hemoglobin 7.8 then 9.3 g/dL, and the indication is primary prevention. The chart states the stop instead of leaving it open. Restarting aspirin for primary prevention would be hard to defend. |
| Lisinopril, atorvastatin, metformin | continue | SUFFICIENT_VISIBLE_EVIDENCE | Chronic indications. No glucose is stored. |

The gastroenterology consult says to hold anticoagulation. There is no anticoagulant on this list. That sentence does not belong to this hospitalization.

Direction: `REFERENCE_APPEARS_TO_DRIVE_CASE` for the repeated "intentional discontinuation" wording.
