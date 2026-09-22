# Internal scenario coverage matrix

Resolved from local source-backed reference rows. Hidden answer data is not included.

## HF_INPATIENT

- context: inpatient / cardiology
- diagnoses: Unspecified systolic (congestive) heart failure [I50.20]
- medications: lisinopril 1 MG/ML Oral Solution [1806884], furosemide 4 MG/ML Oral Solution [104220], metoprolol tartrate 37.5 MG Oral Tablet [1606347], spironolactone 1 MG/ML Oral Suspension [104230], atorvastatin 80 MG Oral Tablet [259255]
- labs: Potassium [Moles/volume] in Serum or Plasma [2823-3], Creatinine [Moles/volume] in Serum or Plasma [14682-9], INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Natriuretic peptide B [Mass/volume] in Serum or Plasma [30934-4]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: omission, dose_mismatch, frequency_mismatch, incorrect_continuation
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## AF_ANTICOAGULATION

- context: inpatient / cardiology
- diagnoses: Paroxysmal atrial fibrillation [I48.0]
- medications: metoprolol tartrate 37.5 MG Oral Tablet [1606347], atorvastatin 80 MG Oral Tablet [259255]
- labs: INR in Platelet poor plasma or blood by Coagulation assay [38875-1], Creatinine [Moles/volume] in Serum or Plasma [14682-9]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: omission, dose_mismatch, frequency_mismatch, incorrect_continuation
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## HTN_INPATIENT

- context: inpatient / general medicine
- diagnoses: Essential (primary) hypertension [I10]
- medications: lisinopril 1 MG/ML Oral Solution [1806884], amlodipine 5 MG Oral Tablet [197361], hydrochlorothiazide 50 MG Oral Tablet [197770], atorvastatin 80 MG Oral Tablet [259255]
- labs: Creatinine [Moles/volume] in Serum or Plasma [14682-9], Potassium [Moles/volume] in Serum or Plasma [2823-3], Sodium [Moles/volume] in Serum or Plasma [2951-2]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: omission, dose_mismatch, frequency_mismatch, incorrect_continuation
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## T2DM_INPATIENT

- context: inpatient / general medicine
- diagnoses: Type 2 diabetes mellitus with unspecified complications [E11.8]
- medications: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet [1807888], lisinopril 1 MG/ML Oral Solution [1806884], atorvastatin 80 MG Oral Tablet [259255]
- labs: Glucose [Moles/volume] in Serum or Plasma [14749-6], Creatinine [Moles/volume] in Serum or Plasma [14682-9], Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: omission, dose_mismatch, frequency_mismatch
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

## CAP_INPATIENT

- context: inpatient / pulmonology
- diagnoses: Lobar pneumonia, unspecified organism [J18.1]
- medications: azithromycin 250 MG Oral Capsule [141962], albuterol 0.4 MG Inhalation Powder [104514], pantoprazole 20 MG Delayed Release Oral Tablet [251872]
- labs: Hemoglobin [Mass/volume] in Blood by Oximetry [55782-7], Creatinine [Moles/volume] in Serum or Plasma [14682-9], Sodium [Moles/volume] in Serum or Plasma [2951-2]
- units: scenario uses UCUM-backed case units where present
- enabled rules in the local rule table: FUROSEMIDE_HF_INDICATION, NO_DUAL_ORAL_ANTICOAGULANT, WARFARIN_INR_MONITORING
- possible error types: omission, dose_mismatch, frequency_mismatch
- source support: RxNorm, ICD-10-CM, LOINC, UCUM, DailyMed/RxClass as stored

