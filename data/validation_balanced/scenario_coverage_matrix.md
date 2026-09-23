# Internal scenario coverage matrix

Resolved from local source-backed reference rows. Hidden answer data is not included.

## HF_INPATIENT

- context: inpatient / cardiology
- diagnoses: Unspecified systolic (congestive) heart failure [I50.20]
- medications: lisinopril 40 MG Oral Tablet [197884], furosemide 80 MG Oral Tablet [197732], metoprolol tartrate 37.5 MG Oral Tablet [1606347], spironolactone 100 MG Oral Tablet [198222], atorvastatin 80 MG Oral Tablet [259255]
- labs: Potassium [Moles/volume] in Serum or Plasma [2823-3], Creatinine [Moles/volume] in Serum or Plasma [14682-9], INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Natriuretic peptide B [Mass/volume] in Serum or Plasma [30934-4]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_monitoring_not_arranged, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_inpatient_substitution_not_reverted, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## AF_ANTICOAGULATION

- context: inpatient / cardiology
- diagnoses: Paroxysmal atrial fibrillation [I48.0]
- medications: metoprolol tartrate 37.5 MG Oral Tablet [1606347], atorvastatin 80 MG Oral Tablet [259255]
- labs: INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Creatinine [Moles/volume] in Serum or Plasma [14682-9]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_monitoring_not_arranged, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_inpatient_substitution_not_reverted, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## HTN_INPATIENT

- context: inpatient / general medicine
- diagnoses: Essential (primary) hypertension [I10]
- medications: lisinopril 40 MG Oral Tablet [197884], amlodipine 5 MG Oral Tablet [197361], hydrochlorothiazide 50 MG Oral Tablet [197770], atorvastatin 80 MG Oral Tablet [259255]
- labs: Creatinine [Moles/volume] in Serum or Plasma [14682-9], Potassium [Moles/volume] in Serum or Plasma [2823-3], Sodium [Moles/volume] in Serum or Plasma [2951-2]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_commission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_inpatient_substitution_not_reverted, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## T2DM_INPATIENT

- context: inpatient / general medicine
- diagnoses: Type 2 diabetes mellitus with unspecified complications [E11.8]
- medications: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet [1807888], lisinopril 40 MG Oral Tablet [197884], atorvastatin 80 MG Oral Tablet [259255]
- labs: Glucose [Moles/volume] in Serum or Plasma [14749-6], Creatinine [Moles/volume] in Serum or Plasma [14682-9], Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## CAP_INPATIENT

- context: inpatient / pulmonology
- diagnoses: Lobar pneumonia, unspecified organism [J18.1]
- medications: azithromycin 250 MG Oral Capsule [141962], albuterol 4 MG Extended Release Oral Capsule [153741], pantoprazole 20 MG Delayed Release Oral Tablet [251872]
- labs: Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7], Creatinine [Moles/volume] in Serum or Plasma [14682-9], Sodium [Moles/volume] in Serum or Plasma [2951-2]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: f1_omission, f1_dose_mismatch, f1_route_mismatch, f1_frequency_mismatch, f1_therapeutic_substitution, f2_held_med_no_restart_plan, f2_insufficient_supply, f2_hospital_only_continued, f2_pending_decision_followup_missing
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

