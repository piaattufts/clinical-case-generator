# Revision evidence ledger

Literature supports a clinical relationship. It is not a measurement that was absent from the chart. A synthetic finding is labeled as such.

| Case | Change | Old representation | New representation | Source | Classification |
| --- | --- | --- | --- | --- | --- |
| VAL-801 | Poor oral intake and dry mucous membranes added as the delirium precipitant. | No precipitant recorded. | Described in the history and the course. Confusion cleared as oral intake improved. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE. [E2]. Glucose 163 then 103 mg/dL is CASE_SOURCE [E4]. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-801 | Standing systolic pressure 116 mmHg added as its own vital row. | Supine 136/78 mmHg only. | Supine row unchanged. Standing systolic pressure 116 mmHg. Diastolic pressure, heart rate, and temperature were not copied onto that row. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE. [E3] applied to the CASE_SOURCE supine systolic pressure [E4]. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-801 | Ibuprofen stop removed. Stop kept as an acceptable alternative. | Chart and clean reference stop ibuprofen without a stored bleeding or kidney event. | Both medication rows list ibuprofen. Reference action continue. Alternative action stop. | CASE_SOURCE medication list [E4]. CLINICAL_LITERATURE [E22] supports the alternative and was not used to invent bleeding. | CASE_SOURCE |
| VAL-802 | Poor oral intake added. No baseline creatinine and no potassium pair added. | No precipitant. Creatinine 1.3 then 1.2 mg/dL. No earlier creatinine. | Poor oral intake is the only precipitant named. The creatinine pair and the absence of an earlier value are stated. | Precipitant is SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E2]. Creatinine pair is CASE_SOURCE [E5]. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-803 | Sodium 128 mmol/L then 135 mmol/L added. Inpatient hydrochlorothiazide held after the admission sodium. | No sodium. Hydrochlorothiazide active in the hospital. Clean reference continues it. | Sodium pair present. Inpatient row held. Reference action stop. Restart is an acceptable alternative. The resident note does not state the discharge action. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E8] [E21]. The numbers are the version 1 pair, not a source laboratory. CASE_SOURCE confirms hydrochlorothiazide and the creatinine pair [E7]. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-803 | Lisinopril duration left at 30 days. | Reviewed readable case used 7 days. Clean evaluator uses 30 days. | Reference duration 30 days. Resident chart does not state a day supply. Hold is an acceptable alternative. | CASE_SOURCE [E7]. The 7-day supply is the earlier discrepancy. | CASE_SOURCE |
| VAL-805 | Source weights, one intake-output day, and oral furosemide kept. Continuation marked ambiguous. | 81 kg, 78 kg, dry weight 73 kg. Oral 40 mg once daily. One net of -1045 mL. | Same figures. No intravenous dose. No ejection fraction. Additional heart-failure therapy is optional. | CASE_SOURCE [E9]. DATABASE [E11]. CLINICAL_LITERATURE [E10] [E12] was not used to invent a dose or an ejection fraction. | CASE_SOURCE |
| VAL-809 | Poor dentition added. Recorded temperatures kept. No home fever added. | 36.80°C twice. Fatigue. Gram-positive cocci. No dental or valve history. | Vital rows remain 36.80°C. History records poor dentition. No prosthetic valve and no home temperature. | Temperatures, organism, vegetation, and creatinine are CASE_SOURCE [E13]. Poor dentition is SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E14]. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-809 | Planned-course sentence removed. Ceftriaxone duration not invented. Lisinopril hold is an alternative. | Consultation says to complete the planned parenteral course. Reference duration is empty. | Consultation states the vegetation and cultures. Reference starts ceftriaxone with no duration. Lisinopril continues, and hold is acceptable. | CASE_SOURCE [E13] [E15]. CLINICAL_LITERATURE [E6] for the alternative. No baseline creatinine was added. | CASE_SOURCE |
| VAL-813 | Valganciclovir removed from the home list and started after the admission viral-load result. | Valganciclovir is a home medicine. The note calls outpatient use the intended continuation. | Not a home medicine. Inpatient 900 mg twice daily after the admission result. Reference action start. | CASE_SOURCE procedure text [E16]. DATABASE [E17]. CLINICAL_LITERATURE [E18]. | CASE_SOURCE |
| VAL-813 | Mycophenolate not added. Potassium cause not invented. | No mycophenolate. Potassium 4.7 then 3.9 mmol/L with no cause. | Still no mycophenolate. The potassium pair is stated. Tacrolimus reduction is an acceptable alternative. No trough was added. | CASE_SOURCE [E16]. Labeling [E20] was not used to add the drug. | REQUIRES_CLINICIAN_DECISION |

## Evidence notes

[E1] Round 1 form in KO Casebook Validation.docx, reviewer KO, 10/5/2026. Supports the comment text and the blank or conflicting boxes. It does not by itself prove a medication change.

[E2] Inouye SK, Westendorp RGJ, Saczynski JS. Delirium in elderly people. Lancet. 2014;383:911-922. doi:10.1016/S0140-6736(13)60688-1. Supports poor intake as a plausible delirium precipitant. It does not establish that this synthetic patient had that precipitant.

[E3] Freeman R, Wieling W, Axelrod FB, et al. Consensus statement on the definition of orthostatic hypotension, neurally mediated syncope and the postural tachycardia syndrome. Clin Auton Res. 2011;21:69-72. doi:10.1007/s10286-011-0119-5. A fall of 20 mmHg in systolic pressure is the consensus threshold. The standing pressure of 116 mmHg is that threshold applied to the recorded supine pressure of 136 mmHg. It was not measured in the source chart.

[E4] Clean pre-injection VAL-801 in exports/clean_balanced_seed_set. Glucose 163 mg/dL then 103 mg/dL. Creatinine 1.1 mg/dL then 1.0 mg/dL. Supine blood pressure 136/78 mmHg then 121/71 mmHg. Ibuprofen is on the medication list. No bleeding event is stored.

[E5] Clean pre-injection VAL-802. Creatinine 1.3 mg/dL then 1.2 mg/dL. Blood pressure 138/69 mmHg then 124/68 mmHg. No creatinine from before the admission is stored. Atorvastatin is on the list. No potassium pair is stored.

[E6] KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney Int Suppl. 2012;2:1-138. Supports reassessing ACE-inhibitor exposure when kidney function may be worse than baseline. It does not create a baseline that was not measured, and it does not set a creatinine threshold for this chart.

[E7] Clean pre-injection VAL-803 evaluator. Lisinopril, hydrochlorothiazide, atorvastatin, and metformin each have a 30-day duration. Creatinine 1.0 mg/dL then 1.2 mg/dL. Potassium 4.4 mmol/L then 4.2 mmol/L. Glucose 149 mg/dL then 129 mg/dL. No sodium is stored. The reviewed readable case, data/case_sets/seed_guided/readable/cases/VAL-803.md, gave lisinopril a 7-day supply. That shortened supply is the earlier discrepancy, not the clean duration.

[E8] Hydrochlorothiazide tablet labeling, DailyMed setid 9f0beacd-4c41-432d-b7d6-e779ae4c1b99, states that thiazides can cause hyponatremia and electrolyte imbalance.

[E9] Clean pre-injection VAL-805. Furosemide 40 mg oral once daily at home and in the hospital. Weights 81 kg on admission, 78 kg at discharge, dry weight 73 kg. Hospital day 3 intake 1418 mL, output 2463 mL, net -1045 mL. Blood pressure 109/82 mmHg then 110/84 mmHg. Creatinine 1.7 mg/dL then 0.9 mg/dL. Potassium 4.7 mmol/L then 4.3 mmol/L. B-type natriuretic peptide 1120 pg/mL then 369 pg/mL. Oxygen saturation 92 percent then 98 percent. Chest radiograph shows pulmonary edema. No ejection fraction is stored.

[E10] Heidenreich PA, Bozkurt B, Aguilar D, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 2022;145:e895-e1032. doi:10.1161/CIR.0000000000001063. Supports intravenous loop-diuretic treatment of congestion and the role of additional therapy in systolic heart failure. It was not used to invent an intravenous dose, a weight, or an ejection fraction.

[E11] Repository regimen FUROSEMIDE_40_DAILY in data/bootstrap/medication_regimens.json. Dose 40 mg, route oral, frequency once daily. The entry excludes the injection product. DailyMed setid 571a52ed-5258-46d5-a0d2-9a984cf73895. This is the charted oral dose. It does not supply an intravenous order.

[E12] Mullens W, Damman K, Harjola VP, et al. The use of diuretics in heart failure with congestion — a position statement from the Heart Failure Association of the ESC. Eur J Heart Fail. 2019;21:137-155. doi:10.1002/ejhf.1369. Supports judging decongestion with weight and urine output. It was not used to replace the recorded weights.

[E13] Clean pre-injection VAL-809. Temperature 36.80°C on admission and at discharge. Presenting symptom fatigue. Blood culture with gram-positive cocci, later culture with no growth. Echocardiogram vegetation with preserved ventricular function. Creatinine 1.3 mg/dL then 0.8 mg/dL. Ceftriaxone 2000 mg intravenous once daily started during the admission. No valve history, dental history, murmur, or pre-admission creatinine is stored.

[E14] Baddour LM, Wilson WR, Bayer AS, et al. Infective Endocarditis in Adults: Diagnosis, Antimicrobial Therapy, and Management of Complications. AHA Scientific Statement. Circulation. 2015;132:1435-1486. doi:10.1161/CIR.0000000000000296. Fever and a predisposing condition, including poor dentition, are part of the clinical picture of endocarditis. The statement was not used to replace the recorded temperature of 36.80°C, to add a prosthetic valve, or to rename gram-positive cocci.

[E15] Repository regimen CEFTRIAXONE_ENDOCARDITIS_OPAT. Ceftriaxone 2000 mg intravenous once daily. Supports the dose already charted. It does not supply a remaining duration for this case.

[E16] Clean pre-injection VAL-813. Admission viral-load review detected CMV viral burden and supported antiviral treatment. A later review was lower. Creatinine 1.2 mg/dL then 1.0 mg/dL. Potassium 4.7 mmol/L then 3.9 mmol/L. Home medicines are tacrolimus 1 mg every 12 hours, amlodipine, atorvastatin, and valganciclovir. Mycophenolate is not on the list. No tacrolimus trough is stored.

[E17] Repository regimen VALGANCICLOVIR_CMV_TREATMENT. Dose 900 mg oral twice daily, given as 450 mg tablets, when renal function is in the range these profiles keep. DailyMed setid 89a934f0-85a3-44c1-82e5-d09d1738e08d. Supports the dose already charted. The dose was not taken from RxNorm.

[E18] Kotton CN, Kumar D, Caliendo AM, et al. The Third International Consensus Guidelines on the Management of Cytomegalovirus in Solid-organ Transplantation. Transplantation. 2018;102:900-931. doi:10.1097/TP.0000000000002191. Supports starting treatment after laboratory evidence of CMV. It was not used to invent a viral-load number or an unrecorded immunosuppressant.

[E19] RxNorm identifies valganciclovir. It was not used as evidence for the dose or the start time.

[E20] CELLCEPT labeling, DailyMed setid 37241e87-4af4-4dc3-a1aa-ea6f20d8dc40, recommends 1 g orally twice daily for adult kidney transplantation. The source case has no mycophenolate row, so the labeled dose was not added.

[E21] Spasovski G, Vanholder R, Allolio B, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol. 2014;170:G1-G47. doi:10.1530/EJE-13-1020. Thiazides are a recognized cause of hyponatremia, and hyponatremia can cause neurologic symptoms. This supports the plausibility of the added sodium pair. It does not show that those values were measured in the source chart.

[E22] American Geriatrics Society Beers Criteria Update Expert Panel. American Geriatrics Society 2023 updated AGS Beers Criteria for potentially inappropriate medication use in older adults. J Am Geriatr Soc. 2023;71:2052-2081. doi:10.1111/jgs.18372. Supports treating a stop of an as-needed NSAID in an older adult as reasonable because of bleeding and kidney risk. It does not show that this patient bled or developed kidney injury.
