# Revision evidence ledger

| Case | Change | Old | New | Evidence class |
| --- | --- | --- | --- | --- |
| VAL-801 | Poor intake, dry mucous membranes, and a 20 mmHg orthostatic fall. | Not in the source chart. Supine pressure 136/78 mmHg is stored. | Described in the note. Not added as a second vital-sign row. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E2] [E3]. Supine pressure is CASE_SOURCE [E4]. |
| VAL-801 | Ibuprofen hold removed. | Status held. Reference stop. | Status active. Reference continue. No discharge instruction in the resident chart. | CASE_SOURCE [E4]. |
| VAL-802 | Poor oral intake added. Baseline creatinine not added. | No precipitant. Creatinine 1.3 then 1.2 mg/dL only. | Poor intake named. Same creatinine pair. Version 1 baseline 1.2 mg/dL was not restored. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE for the intake history [E2]. Creatinine is CASE_SOURCE [E5]. |
| VAL-803 | Sodium 128 then 135 mmol/L and inpatient hydrochlorothiazide hold. | No sodium. Hydrochlorothiazide active. | Synthetic sodium course. Inpatient row held. Reference stop, with hold acceptable. Resident chart does not state the discharge action. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E8]. Hydrochlorothiazide presence is CASE_SOURCE [E7]. |
| VAL-805 | Furosemide reference frequency twice daily. Source dose and weights kept. | 40 mg oral once daily. Weights 81 / 78 / dry 73 kg. | Same charted order and weights. Reference 40 mg oral twice daily. Continue once daily is acceptable. No intravenous dose and no ejection fraction. | CASE_SOURCE [E9]. CLINICAL_LITERATURE [E10] [E11] [E12]. Version 1 intravenous dose and 86-to-80 kg series were not used. |
| VAL-809 | Antibiotic consult no longer states the discharge plan. Source temperature and organism kept. | Temperature 36.80°C. Gram-positive cocci. Consult said to complete the planned course. | Same temperature and organism. Consult lists findings and follow-up. Lisinopril hold is an alternative. | CASE_SOURCE [E13]. CLINICAL_LITERATURE [E14]. Version 1 fever, dental extraction, and viridans label were not used. |
| VAL-813 | Home valganciclovir removed. Mycophenolate not added. | Valganciclovir on the home list. No mycophenolate. | Valganciclovir starts after the viral-load result at 900 mg twice daily. Mycophenolate remains absent. The adjudication question does not mention it. | CASE_SOURCE procedure text [E16]. REPOSITORY_SOURCE dose [E17]. Labeling [E20] was not used to add mycophenolate. |

## Evidence notes

[E1] KO Casebook Validation.docx, reviewer KO, 10/5/2026. Supports the comment text, the double selections, and the items left blank. It does not by itself prove a medication change.

[E2] Inouye SK, Westendorp RGJ, Saczynski JS. Delirium in elderly people. Lancet. 2014;383:911-922. doi:10.1016/S0140-6736(13)60688-1. Supports treating a precipitant of delirium, including metabolic precipitants. It does not establish which precipitant this synthetic patient had.

[E3] Freeman R, Wieling W, Axelrod FB, et al. Consensus statement on the definition of orthostatic hypotension. Clin Auton Res. 2011;21:69-72. doi:10.1007/s10286-011-0119-5. Supports the 20 mmHg systolic threshold used for the synthetic orthostatic finding. It does not show that this patient had that finding.

[E4] Clean pre-injection VAL-801. Glucose 163 mg/dL then 103 mg/dL. Creatinine 1.1 mg/dL then 1.0 mg/dL. Supine blood pressure 136/78 mmHg. Ibuprofen is on the verified list. No bleeding diagnosis is stored.

[E5] Clean pre-injection VAL-802. Creatinine 1.3 mg/dL then 1.2 mg/dL. Blood pressure 138/69 mmHg then 124/68 mmHg. No earlier creatinine and no potassium series are stored. Atorvastatin is on the verified list.

[E6] KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney Int Suppl. 2012;2:1-138. Supports reviewing ACE-inhibitor exposure when kidney function may have worsened. It does not create a baseline creatinine.

[E7] Clean pre-injection VAL-803. Hydrochlorothiazide 25 mg daily is on the list. Creatinine 1.0 mg/dL then 1.2 mg/dL. Potassium 4.4 mmol/L then 4.2 mmol/L. No sodium is stored. Evaluator lisinopril duration is 30 days. The reviewed readable case gave lisinopril 7 days.

[E8] Liamis G, Milionis H, Elisaf M. A review of drug-induced hyponatremia. Am J Kidney Dis. 2008;52:144-153. doi:10.1053/j.ajkd.2008.03.004. Thiazides are a common cause of hyponatremia. Hydrochlorothiazide labeling, DailyMed setid 9f0beacd-4c41-432d-b7d6-e779ae4c1b99. The citations support plausibility of the synthetic sodium course. They do not show that those sodium values were recovered from a source chart.

[E9] Clean pre-injection VAL-805. Furosemide 40 mg oral once daily at home and in the hospital. Weights 81 kg, 78 kg, dry weight 73 kg. Hospital day 3 intake 1418 mL, output 2463 mL, net -1045 mL. Creatinine 1.7 then 0.9 mg/dL. Potassium 4.7 then 4.3 mmol/L. Natriuretic peptide 1120 then 369 pg/mL. Blood pressure 109/82 then 110/84 mmHg. No ejection fraction.

[E10] Heidenreich PA, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 2022;145:e895-e1032. doi:10.1161/CIR.0000000000001063. Supports using congestion, kidney function, potassium, and blood pressure when judging diuretic and other heart-failure therapy. It was not used to invent a weight or an ejection fraction.

[E11] Repository regimen FUROSEMIDE_40_DAILY in data/bootstrap/medication_regimens.json. Oral 40 mg once daily. The entry excludes the injection product. Furosemide tablet labeling, DailyMed setid 571a52ed-5258-46d5-a0d2-9a984cf73895: the usual initial dose is 20 to 80 mg, and the same dose may be repeated 6 to 8 hours later. Supports the charted oral dose and a twice-daily reference frequency. It does not supply an intravenous order.

[E12] Mullens W, et al. The use of diuretics in heart failure with congestion. Eur J Heart Fail. 2019;21:137-155. doi:10.1002/ejhf.1369. Supports judging decongestion with weight and urine output. It was not used to replace the recorded weights.

[E13] Clean pre-injection VAL-809. Temperature 36.80°C on admission and at discharge. Symptom: fatigue. Gram-positive cocci, later no growth. Vegetation with preserved ventricular function. Creatinine 1.3 then 0.8 mg/dL. Ceftriaxone 2 g IV daily. PICC present. No valve or dental history.

[E14] Baddour LM, et al. Infective Endocarditis in Adults. Circulation. 2015;132:1435-1486. doi:10.1161/CIR.0000000000000296. Supports using bacteremia, echocardiography, and antimicrobial therapy in the representation. It was not used to add a valve, a dental procedure, a fever, or a species the culture does not name.

[E15] Repository regimen CEFTRIAXONE_ENDOCARDITIS_OPAT. Ceftriaxone 2000 mg intravenous once daily. Supports the dose already charted.

[E16] Clean pre-injection VAL-813. Procedure text: admission viral burden detected and supported antiviral treatment; later burden lower. Creatinine 1.2 then 1.0 mg/dL. Potassium 4.7 then 3.9 mmol/L. Home list includes tacrolimus, amlodipine, atorvastatin, and valganciclovir. No mycophenolate row.

[E17] Repository regimen VALGANCICLOVIR_CMV_TREATMENT. 900 mg oral twice daily, given as 450 mg tablets, when creatinine is in the range these profiles keep. DailyMed setid 89a934f0-85a3-44c1-82e5-d09d1738e08d. The dose was not taken from RxNorm.

[E18] Kotton CN, et al. The Third International Consensus Guidelines on the Management of Cytomegalovirus in Solid-organ Transplantation. Transplantation. 2018;102:900-931. doi:10.1097/TP.0000000000002191. Supports starting treatment after laboratory evidence of CMV and considering the intensity of immunosuppression. It was not used to invent a viral-load number or a mycophenolate row.

[E20] CELLCEPT labeling, DailyMed setid 37241e87-4af4-4dc3-a1aa-ea6f20d8dc40, recommends 1 g orally twice daily for adult kidney transplantation. The source case has no mycophenolate row, so the labeled dose was not added.
