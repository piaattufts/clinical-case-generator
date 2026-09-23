# Internal scenario coverage matrix

Resolved from local source-backed reference rows. Hidden answer data is not included.

## MEDREC_UNCERTAIN_HISTORY

- context: inpatient / general medicine
- generation_strategy: resident_seed_guided
- seed_source_filename: `Bad_Med_Rec_Case.docx`
- diagnoses: Delirium due to known physiological condition [F05]
- medications: lisinopril 40 MG Oral Tablet [197884], Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet [1807888], atorvastatin 80 MG Oral Tablet [259255]
- labs: Creatinine [Mass/volume] in Serum or Plasma [2160-0], Potassium [Moles/volume] in Serum or Plasma [2823-3], Fasting glucose [Mass/volume] in Serum or Plasma [1558-6]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f2_insufficient_supply, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## HF_DECOMPENSATION

- context: inpatient / cardiology
- generation_strategy: resident_seed_guided
- seed_source_filename: `Heart_Failure_Case.docx`
- diagnoses: Acute systolic (congestive) heart failure [I50.21]
- medications: furosemide 80 MG Oral Tablet [197732], metoprolol tartrate 37.5 MG Oral Tablet [1606347], lisinopril 40 MG Oral Tablet [197884], atorvastatin 80 MG Oral Tablet [259255]
- labs: Potassium [Moles/volume] in Serum or Plasma [2823-3], Creatinine [Mass/volume] in Serum or Plasma [2160-0], Natriuretic peptide B [Mass/volume] in Serum or Plasma [30934-4]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_dose_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## OPAT_ENDOCARDITIS

- context: inpatient / infectious disease
- generation_strategy: resident_seed_guided
- seed_source_filename: `OPAT_Case.docx`
- diagnoses: Acute and subacute infective endocarditis [I33.0]
- medications: ceftriaxone 500 MG Injection [1665005], lisinopril 40 MG Oral Tablet [197884], atorvastatin 80 MG Oral Tablet [259255], Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet [1807888]
- labs: Creatinine [Mass/volume] in Serum or Plasma [2160-0], Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7], Fasting glucose [Mass/volume] in Serum or Plasma [1558-6]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f2_insufficient_supply, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## TRANSPLANT_CMV

- context: inpatient / nephrology
- generation_strategy: resident_seed_guided
- seed_source_filename: `Post_transplant_case.docx`
- diagnoses: Other cytomegaloviral diseases [B25.8]
- medications: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule [1431971], mycophenolate mofetil 250 MG Oral Capsule [199058], amlodipine 5 MG Oral Tablet [197361], atorvastatin 80 MG Oral Tablet [259255]
- labs: Creatinine [Mass/volume] in Serum or Plasma [2160-0], Potassium [Moles/volume] in Serum or Plasma [2823-3]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_dose_mismatch, f2_held_med_no_restart_plan, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## POSTOP_ANTICOAGULATION

- context: inpatient / orthopedics
- generation_strategy: resident_seed_guided
- seed_source_filename: `Post-Op_Case.docx`
- diagnoses: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture [S72.001A]
- medications: warfarin sodium 1 MG Oral Tablet [855288], lisinopril 40 MG Oral Tablet [197884], Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet [1807888]
- labs: INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7], Creatinine [Mass/volume] in Serum or Plasma [2160-0], Fasting glucose [Mass/volume] in Serum or Plasma [1558-6]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f2_monitoring_not_arranged, f2_insufficient_supply, f2_hospital_only_continued
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## GI_BLEED_ACUTE_CHANGE

- context: inpatient / general medicine
- generation_strategy: resident_seed_guided
- seed_source_filename: `Sepsis_AMA_Case.docx`
- diagnoses: Gastrointestinal hemorrhage, unspecified [K92.2]
- medications: apixaban 2.5 MG Oral Tablet [1364435], atorvastatin 80 MG Oral Tablet [259255], lisinopril 40 MG Oral Tablet [197884], Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet [1807888]
- labs: Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7], Creatinine [Mass/volume] in Serum or Plasma [2160-0], Fasting glucose [Mass/volume] in Serum or Plasma [1558-6]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f2_held_med_no_restart_plan, f2_hospital_only_continued, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

