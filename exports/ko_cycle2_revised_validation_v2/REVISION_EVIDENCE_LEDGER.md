# Revision evidence ledger

Literature supports a clinical relationship. It is not used as a measurement that was absent from the chart. A synthetic finding is labeled as such.

| Case | Change | Old representation | New representation | Source | Classification |
| --- | --- | --- | --- | --- | --- |
| VAL-801 | Poor oral intake, dry mucous membranes, and a 20 mmHg orthostatic fall were added to the history and examination. | Not recorded. | Recorded in the admission note and hospital course. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE. [E2] [E3]. Supine blood pressure 136/78 mmHg is CASE_SOURCE [E4]. The orthostatic fall was not measured in the source chart. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-801 | Ibuprofen stop removed. | Reference action stop. | Reference action continue, symptomatic analgesia. | CASE_SOURCE [E4]. No bleeding or kidney-injury indication is stored. | CASE_SOURCE |
| VAL-802 | Poor oral intake added as the delirium precipitant. | No precipitant recorded. | Poor oral intake for two days. No other precipitant recorded. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE [E2]. No new laboratory value was added. | SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE |
| VAL-802 | No baseline creatinine added. | 1.3 mg/dL then 1.2 mg/dL. | 1.3 mg/dL then 1.2 mg/dL. | CASE_SOURCE [E5]. | NOT_CHANGED |
| VAL-802 | Answer-key statin sentence removed. | The note said the statin should be continued. | The medicine remains on the list without that instruction. | CASE_SOURCE medication row [E5]. The sentence was an answer leak. | CASE_SOURCE |
| VAL-803 | Lisinopril duration restored to 30 days. | Injected reference duration 7 days. | 30 days. | CASE_SOURCE [E7]. | CASE_SOURCE |
| VAL-803 | No sodium series added. | No sodium stored. | No sodium stored. | CASE_SOURCE [E7]. Labeling [E8] was not used to invent a value. | NOT_CHANGED |
| VAL-805 | Intravenous furosemide not charted. | 40 mg oral once daily. | 40 mg oral once daily. | CASE_SOURCE [E9] and DATABASE [E11]. LITERATURE [E10] supports IV treatment in principle and was not used to invent a dose. | REQUIRES_CLINICIAN_DECISION |
| VAL-805 | Weights and the single intake/output day retained. The euvolemia sentence was removed. | 81 kg, dry weight 73 kg, discharge 78 kg; hospital day 3 intake 1418 mL, output 2463 mL, net -1045 mL. Course claimed euvolemia. | Same measurements. Course states that discharge weight remains above dry weight. | CASE_SOURCE [E9]. LITERATURE [E12] supports using those observations and was not used to replace them. | CASE_SOURCE |
| VAL-805 | No ejection fraction added. | Systolic heart-failure diagnosis, no numeric EF. | Same. | CASE_SOURCE [E9]. | NOT_CHANGED |
| VAL-809 | Recorded endocarditis evidence moved into the course. Temperature, valve history, and microbiology were not replaced. | Temperature 36.80°C. Gram-positive cocci. Vegetation. | Same facts, now stated in the course. | CASE_SOURCE [E13]. LITERATURE [E14] supports the disease representation. | CASE_SOURCE |
| VAL-809 | Lisinopril hold is an acceptable alternative, not a required stop. | Continued. | Continued, with hold acceptable. | CASE_SOURCE creatinine pair [E13]. LITERATURE [E6]. No baseline creatinine was invented. | REQUIRES_CLINICIAN_DECISION |
| VAL-813 | Valganciclovir removed from the home list and started after the admission viral-load result. | Home and inpatient, 900 mg twice daily. | Inpatient start after the recorded detection. Dose unchanged. | CASE_SOURCE procedure text and diagnosis [E16]. The home row was removed because it contradicted that sequence. | CASE_SOURCE |
| VAL-813 | Dose left at 900 mg twice daily. | 900 mg twice daily, 450 mg tablets. | 900 mg twice daily, 450 mg tablets. | DATABASE [E17]. Creatinine 1.2 then 1.0 mg/dL is CASE_SOURCE [E16]. RxNorm was not used to set the dose [E19]. | DATABASE |
| VAL-813 | Mycophenolate not added. | Not on the list. | Not on the list. | CASE_SOURCE [E16]. Labeling [E20] was not used to add the drug. | REQUIRES_CLINICIAN_DECISION |

## Evidence notes

[E1] Round 1 form in KO Casebook Validation.docx, reviewer KO, 10/5/2026. Supports the comment text and the blank or conflicting boxes. It does not by itself prove a medication change.

[E2] Inouye SK, Westendorp RGJ, Saczynski JS. Delirium in elderly people. Lancet. 2014;383:911-922. doi:10.1016/S0140-6736(13)60688-1. Supports treating the precipitant of delirium. It does not establish which precipitant this synthetic patient had.

[E3] Freeman R, Wieling W, Axelrod FB, et al. Consensus statement on the definition of orthostatic hypotension, neurally mediated syncope and the postural tachycardia syndrome. Clin Auton Res. 2011;21:69-72. doi:10.1007/s10286-011-0119-5. Supports the 20 mmHg systolic threshold used for the synthetic orthostatic finding. It does not show that this patient had that finding.

[E4] Clean pre-injection VAL-801. Glucose 163 mg/dL then 103 mg/dL, creatinine 1.1 mg/dL then 1.0 mg/dL, supine blood pressure 136/78 mmHg, and ibuprofen on the verified list. No bleeding or kidney-injury indication for stopping ibuprofen is stored.

[E5] Clean pre-injection VAL-802. Creatinine 1.3 mg/dL then 1.2 mg/dL. No creatinine from before the admission is stored. Atorvastatin is on the verified list.

[E6] KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney Int Suppl. 2012;2:1-138. Supports reassessing ACE-inhibitor exposure when kidney function worsens. It does not create a baseline creatinine that was not measured.

[E7] Clean pre-injection VAL-803 evaluator. Lisinopril duration 30 days. Creatinine 1.0 mg/dL on admission and 1.2 mg/dL at discharge. Hydrochlorothiazide 25 mg daily is on the list. No sodium is stored. The reviewed readable case, data/case_sets/seed_guided/readable/cases/VAL-803.md, gave lisinopril a 7-day supply.

[E8] Hydrochlorothiazide tablet labeling, DailyMed setid 9f0beacd-4c41-432d-b7d6-e779ae4c1b99. Thiazides can cause hyponatremia. That fact was not used to add a sodium value or to stop the drug.

[E9] Clean pre-injection VAL-805. Furosemide 40 mg oral once daily at home and in the hospital. Weights 81 kg on admission, 78 kg at discharge, dry weight 73 kg. Hospital day 3 intake 1418 mL, output 2463 mL, net -1045 mL. Blood pressure 109/82 mmHg then 110/84 mmHg. Creatinine 1.7 mg/dL then 0.9 mg/dL. Potassium 4.7 mmol/L then 4.3 mmol/L. B-type natriuretic peptide 1120 pg/mL then 369 pg/mL. Oxygen saturation 92 percent then 98 percent. Chest radiograph shows pulmonary edema. No ejection fraction is stored.

[E10] Heidenreich PA, Bozkurt B, Aguilar D, et al. 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure. Circulation. 2022;145:e895-e1032. doi:10.1161/CIR.0000000000001063. Supports intravenous loop diuretic treatment of congestion and the components of therapy for systolic heart failure. It was not used to invent an intravenous dose, a weight, or an ejection fraction.

[E11] Repository regimen FUROSEMIDE_40_DAILY in data/bootstrap/medication_regimens.json. Dose 40 mg, route oral, frequency once daily. The entry excludes the injection product. DailyMed setid 571a52ed-5258-46d5-a0d2-9a984cf73895. Supports the charted oral dose. It does not supply an intravenous order.

[E12] Mullens W, Damman K, Harjola VP, et al. The use of diuretics in heart failure with congestion — a position statement from the Heart Failure Association of the ESC. Eur J Heart Fail. 2019;21:137-155. doi:10.1002/ejhf.1369. Supports using weight and urine output to judge decongestion. It was not used to replace the recorded weights.

[E13] Clean pre-injection VAL-809. Temperature 36.80°C on admission and at discharge. The stored presenting symptom is fatigue. Blood culture with gram-positive cocci, later culture with no growth. Echocardiogram vegetation with preserved ventricular function. Creatinine 1.3 mg/dL then 0.8 mg/dL. No valve or dental history.

[E14] Baddour LM, Wilson WR, Bayer AS, et al. Infective Endocarditis in Adults: Diagnosis, Antimicrobial Therapy, and Management of Complications. AHA Scientific Statement. Circulation. 2015;132:1435-1486. doi:10.1161/CIR.0000000000000296. Supports using bacteremia, echocardiography, and antimicrobial therapy in the case representation. It was not used to add a valve, a dental procedure, or a fever that replaces 36.80°C.

[E15] Repository regimen CEFTRIAXONE_ENDOCARDITIS_OPAT. Ceftriaxone 2000 mg intravenous once daily. Supports the dose already charted.

[E16] Clean pre-injection VAL-813. Admission diagnosis of CMV disease. Procedure text: admission viral burden detected and supported antiviral treatment; later burden lower. Creatinine 1.2 mg/dL then 1.0 mg/dL. Potassium 4.7 mmol/L then 3.9 mmol/L. Home medicines include tacrolimus 1 mg every 12 hours, amlodipine, atorvastatin, and valganciclovir.

[E17] Repository regimen VALGANCICLOVIR_CMV_TREATMENT. Dose 900 mg oral twice daily, given as 450 mg tablets, when renal function is in the range these profiles keep. DailyMed setid 89a934f0-85a3-44c1-82e5-d09d1738e08d. Supports the dose. The dose was not taken from RxNorm.

[E18] Kotton CN, Kumar D, Caliendo AM, et al. The Third International Consensus Guidelines on the Management of Cytomegalovirus in Solid-organ Transplantation. Transplantation. 2018;102:900-931. doi:10.1097/TP.0000000000002191. Supports starting treatment after laboratory evidence of CMV and adjusting the dose for renal function. It was not used to invent a viral-load number.

[E19] RxNorm identifies valganciclovir. It was not used as evidence for the dose or the start time.

[E20] CELLCEPT labeling, DailyMed setid 37241e87-4af4-4dc3-a1aa-ea6f20d8dc40, recommends 1 g orally twice daily for adult kidney transplantation. The source case has no mycophenolate row, so the labeled dose was not added.
