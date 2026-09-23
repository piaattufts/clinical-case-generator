# Internal scenario coverage matrix

Resolved from local source-backed reference rows. Hidden answer data is not included.

## HF_INPATIENT

- context: inpatient / cardiology
- diagnoses: Acute systolic (congestive) heart failure [I50.21]
- medications: lisinopril 10 MG Oral Tablet [314076], furosemide 40 MG Oral Tablet [313988], 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet [866427], spironolactone 25 MG Oral Tablet [313096], atorvastatin 40 MG Oral Tablet [617311]
- labs: Potassium [Moles/volume] in Serum or Plasma [2823-3], Creatinine [Mass/volume] in Serum or Plasma [2160-0], INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Natriuretic peptide B [Mass/volume] in Serum or Plasma [30934-4]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_monitoring_not_arranged, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_inpatient_substitution_not_reverted, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## AF_ANTICOAGULATION

- context: inpatient / cardiology
- diagnoses: Paroxysmal atrial fibrillation [I48.0]
- medications: 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet [866427], atorvastatin 40 MG Oral Tablet [617311]
- labs: INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Creatinine [Mass/volume] in Serum or Plasma [2160-0]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_monitoring_not_arranged, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_inpatient_substitution_not_reverted, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## HTN_INPATIENT

- context: inpatient / general medicine
- diagnoses: Essential (primary) hypertension [I10]
- medications: lisinopril 10 MG Oral Tablet [314076], amlodipine 5 MG Oral Tablet [197361], hydrochlorothiazide 25 MG Oral Tablet [310798], atorvastatin 40 MG Oral Tablet [617311]
- labs: Creatinine [Mass/volume] in Serum or Plasma [2160-0], Potassium [Moles/volume] in Serum or Plasma [2823-3], Sodium [Moles/volume] in Serum or Plasma [2951-2]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_inpatient_substitution_not_reverted, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## T2DM_INPATIENT

- context: inpatient / general medicine
- diagnoses: Type 2 diabetes mellitus with hyperglycemia [E11.65], Type 2 diabetes mellitus without complications [E11.9]
- medications: metformin hydrochloride 500 MG Oral Tablet [861007], lisinopril 10 MG Oral Tablet [314076], atorvastatin 40 MG Oral Tablet [617311]
- labs: Fasting glucose [Mass/volume] in Serum or Plasma [1558-6], Creatinine [Mass/volume] in Serum or Plasma [2160-0], Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## CAP_INPATIENT

- context: inpatient / pulmonology
- diagnoses: Lobar pneumonia, unspecified organism [J18.1]
- medications: azithromycin 250 MG Oral Tablet [308460], albuterol 0.1 MG Inhalation Powder [252298], pantoprazole 40 MG Delayed Release Oral Tablet [314200]
- labs: Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7], Creatinine [Mass/volume] in Serum or Plasma [2160-0], Sodium [Moles/volume] in Serum or Plasma [2951-2]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

