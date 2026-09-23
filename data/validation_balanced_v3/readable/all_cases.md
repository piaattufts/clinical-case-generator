# CliniProof Clinical Case Set

## CLINIPROOF_BALANCED_V3

This document is intended for residents, clinicians, medical educators, pharmacists, and clinical informatics collaborators who want to review the clinical cases without reading the underlying JSON representation.

The set contains 24 cases, labeled VAL-501 through VAL-524. Each case is a synthetic inpatient encounter assembled for medication-reconciliation review. The software has already checked structure, terminology provenance, and a limited set of implemented clinical rules. Those automated checks do not establish clinical validity. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

This file contains only the information a resident would see. It does not identify which cases contain an intended assessment problem, if any, and it does not include investigator answer keys.

---

# VAL-501

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 76
- **Sex/gender:** Female
- **Weight:** 84.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 76-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Edema, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Edema, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 76-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Edema, Orthopnea, present for several days and worsening. Home medications include furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. Admitted for decompensated heart failure with volume overload. The hospital course focused on diuresis over several inpatient days. Intake and output were recorded, and congestion improved enough for discharge.

### Admission note

Admission note for a 76-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Edema, Orthopnea for several days (worsening). Medications continued from home: furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. Admitted for decompensated heart failure with volume overload. The hospital course focused on diuresis over several inpatient days. Intake and output were recorded, and congestion improved enough for discharge.

The hospital course focused on diuresis over several inpatient days. Intake and output were recorded, and congestion improved enough for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

On hospital day 3, intake was 1581 mL and output was 2034 mL (net -453 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 123/81 | mmHg |
| admission: Heart rate | 111 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.6 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 1321.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.2 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 127/85 | mmHg |
| discharge: Heart rate | 102 | beats/min |
| discharge: Respiratory rate | 23 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 352.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.1 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Heart-failure clinic follow-up (timing: 7 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 84.000 kg
- discharge: 81.000 kg (dry weight 79.000 kg)

Imaging:

{'study_id': 'STUDY-VAL501-001', 'case_id': 'VAL-501', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Pulmonary edema without focal consolidation.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL501-001', 'case_id': 'VAL-501', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-502

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 59
- **Sex/gender:** Male
- **Weight:** 81.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 59-year-old Male with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Fatigue in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Fatigue
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 59-year-old Male is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Fatigue, present for one week and improving after treatment. Home medications include furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet. Admitted for decompensated heart failure; congestion improved with diuresis. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 59-year-old Male with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Fatigue for one week (improving after treatment). Medications continued from home: furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet. Admitted for decompensated heart failure; congestion improved with diuresis. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

On hospital day 4, intake was 1556 mL and output was 2791 mL (net -1235 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 156/80 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.5 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 132/85 | mmHg |
| discharge: Heart rate | 89 | beats/min |
| discharge: Respiratory rate | 23 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.1 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.4 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Heart-failure follow-up after diuresis (timing: 14 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 81.000 kg
- discharge: 77.000 kg (dry weight 74.000 kg)

Imaging:

{'study_id': 'STUDY-VAL502-001', 'case_id': 'VAL-502', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Improving pulmonary edema compared with admission.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL502-001', 'case_id': 'VAL-502', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-503

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 72
- **Sex/gender:** Female
- **Weight:** 79.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 72-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chest pain in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Chest pain
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 72-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Chest pain, present for two days and acutely worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted for decompensated heart failure with atrial fibrillation. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

### Admission note

Admission note for a 72-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Chest pain for two days (acutely worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted for decompensated heart failure with atrial fibrillation. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |

## Hospital course

On hospital day 2, intake was 1557 mL and output was 2378 mL (net -821 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 115/69 | mmHg |
| admission: Heart rate | 103 | beats/min |
| admission: Respiratory rate | 26 | breaths/min |
| admission: SpO2 | 90.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.8 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.1 | {INR} |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.2 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 123/77 | mmHg |
| discharge: Heart rate | 72 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 94.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.5 | {INR} |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.1 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Outpatient INR follow-up (timing: 7 days; with service: anticoagulation clinic)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 79.000 kg
- discharge: 76.000 kg (dry weight 71.000 kg)

Imaging:

{'study_id': 'STUDY-VAL503-001', 'case_id': 'VAL-503', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Cardiomegaly without focal pneumonia.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL503-001', 'case_id': 'VAL-503', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-504

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 84
- **Sex/gender:** Female
- **Weight:** 108.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 84-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Edema, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Edema, Orthopnea
- **Symptom duration:** one day
- **Symptom course:** progressive
- **History of present illness:** A 84-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Edema, Orthopnea, present for one day and progressive. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, spironolactone 100 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. Admitted for decompensated heart failure requiring diuretic adjustment. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 84-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Edema, Orthopnea for one day (progressive). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, spironolactone 100 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. Admitted for decompensated heart failure requiring diuretic adjustment. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

On hospital day 3, intake was 1427 mL and output was 2651 mL (net -1224 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 134/77 | mmHg |
| admission: Heart rate | 108 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.0 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 426.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.3 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 146/96 | mmHg |
| discharge: Heart rate | 76 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 300.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.6 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Formulary substitution for metoprolol tartrate 37.5 MG Oral Tablet during admission (RxClass CV100 BETA BLOCKERS/RELATED). |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Volume and blood-pressure follow-up (timing: 3 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Edema (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 108.000 kg
- discharge: 104.000 kg (dry weight 100.000 kg)

Imaging:

{'study_id': 'STUDY-VAL504-001', 'case_id': 'VAL-504', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Mild pulmonary congestion.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL504-001', 'case_id': 'VAL-504', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-505

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 63
- **Sex/gender:** Male
- **Weight:** 65.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 63-year-old Male with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Orthopnea, Fatigue in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Orthopnea, Fatigue
- **Symptom duration:** one week
- **Symptom course:** persistent
- **History of present illness:** A 63-year-old Male is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Orthopnea, Fatigue, present for one week and persistent. Home medications include apixaban 2.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for decompensated heart failure with a planned home-health transition. The inpatient stay was brief. Symptoms and vital signs were observed, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 63-year-old Male with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Orthopnea, Fatigue for one week (persistent). Medications continued from home: apixaban 2.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for decompensated heart failure with a planned home-health transition. The inpatient stay was brief. Symptoms and vital signs were observed, and the patient was judged ready for discharge home.

The inpatient stay was brief. Symptoms and vital signs were observed, and the patient was judged ready for discharge home.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |

## Hospital course

On hospital day 1, intake was 1584 mL and output was 2747 mL (net -1163 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 142/92 | mmHg |
| admission: Heart rate | 102 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.1 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 1019.0 | pg/mL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 129/69 | mmHg |
| discharge: Heart rate | 106 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 93.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 407.0 | pg/mL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Heart-failure clinic with home-health support (timing: 10 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 65.000 kg
- discharge: 62.000 kg (dry weight 60.000 kg)

Imaging:

{'study_id': 'STUDY-VAL505-001', 'case_id': 'VAL-505', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Improving congestion.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL505-001', 'case_id': 'VAL-505', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-506

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Male
- **Weight:** 90.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 77-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Fatigue in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Fatigue
- **Symptom duration:** two days
- **Symptom course:** intermittent
- **History of present illness:** A 77-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Fatigue, present for two days and intermittent. Home medications include apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet. Admitted for symptomatic atrial fibrillation with rapid ventricular response. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

### Admission note

Admission note for a 77-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Fatigue for two days (intermittent). Medications continued from home: apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet. Admitted for symptomatic atrial fibrillation with rapid ventricular response. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 128/90 | mmHg |
| admission: Heart rate | 130 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.7 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 146/73 | mmHg |
| discharge: Heart rate | 104 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 92.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Rate-control follow-up (timing: 7 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 90.000 kg

Imaging:

{'study_id': 'STUDY-VAL506-001', 'case_id': 'VAL-506', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute pulmonary edema.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL506-001', 'case_id': 'VAL-506', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue rate control and the planned anticoagulation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-507

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 74
- **Sex/gender:** Female
- **Weight:** 103.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 74-year-old Female with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Chest pain in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Fatigue, Chest pain
- **Symptom duration:** one day
- **Symptom course:** acutely worsening
- **History of present illness:** A 74-year-old Female is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Fatigue, Chest pain, present for one day and acutely worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted for symptomatic atrial fibrillation requiring rate control and INR assessment. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 74-year-old Female with Paroxysmal atrial fibrillation. Symptoms: Fatigue, Chest pain for one day (acutely worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted for symptomatic atrial fibrillation requiring rate control and INR assessment. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 129/78 | mmHg |
| admission: Heart rate | 114 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.9 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.8 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 121/76 | mmHg |
| discharge: Heart rate | 108 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 94.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.9 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- INR monitoring follow-up (timing: 7 days; with service: anticoagulation clinic)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 103.000 kg

Imaging:

{'study_id': 'STUDY-VAL507-001', 'case_id': 'VAL-507', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute infiltrate.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL507-001', 'case_id': 'VAL-507', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue rate control and the planned anticoagulation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-508

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 88
- **Sex/gender:** Male
- **Weight:** 79.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 88-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 88-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Fatigue, present for several days and persistent. Home medications include apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic atrial fibrillation; rate control was restored. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 88-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Fatigue for several days (persistent). Medications continued from home: apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic atrial fibrillation; rate control was restored. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 141/68 | mmHg |
| admission: Heart rate | 91 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.8 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 122/82 | mmHg |
| discharge: Heart rate | 105 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 20 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Lipid and anticoagulation follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 79.000 kg

Imaging:

{'study_id': 'STUDY-VAL508-001', 'case_id': 'VAL-508', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute cardiopulmonary process.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL508-001', 'case_id': 'VAL-508', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue rate control and the planned anticoagulation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-509

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 66
- **Sex/gender:** Female
- **Weight:** 67.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 66-year-old Female with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chest pain, Fatigue in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Chest pain, Fatigue
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 66-year-old Female is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Chest pain, Fatigue, present for one week and progressive. Home medications include apixaban 2.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. carvedilol 6.25 MG Oral Tablet, ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for symptomatic atrial fibrillation with chest discomfort. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 66-year-old Female with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Chest pain, Fatigue for one week (progressive). Medications continued from home: apixaban 2.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. carvedilol 6.25 MG Oral Tablet, ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for symptomatic atrial fibrillation with chest discomfort. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 122/81 | mmHg |
| admission: Heart rate | 135 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.1 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 135/91 | mmHg |
| discharge: Heart rate | 106 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 93.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.4 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | held; held reason: Held inpatient for documented hypotension during rate control; intended to restart.; indication: Paroxysmal atrial fibrillation |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | held; held reason: Held inpatient for documented hypotension during rate control; intended to restart.; indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Cardiology follow-up after rate control (timing: 3 days; with service: cardiology)

## Discharge instructions

- Do not restart at discharge: ibuprofen 300 MG Oral Tablet was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 67.000 kg

Imaging:

{'study_id': 'STUDY-VAL509-001', 'case_id': 'VAL-509', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute pulmonary edema.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL509-001', 'case_id': 'VAL-509', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue rate control and the planned anticoagulation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-510

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 83
- **Sex/gender:** Female
- **Weight:** 67.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 83-year-old Female with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Fatigue
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 83-year-old Female is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Fatigue, present for two days and improving after treatment. Home medications include carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted for atrial fibrillation with rapid ventricular response, now rate-controlled. The inpatient stay was brief. Symptoms and vital signs were observed, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 83-year-old Female with Paroxysmal atrial fibrillation. Symptoms: Fatigue for two days (improving after treatment). Medications continued from home: carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted for atrial fibrillation with rapid ventricular response, now rate-controlled. The inpatient stay was brief. Symptoms and vital signs were observed, and the patient was judged ready for discharge home.

The inpatient stay was brief. Symptoms and vital signs were observed, and the patient was judged ready for discharge home.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 158/84 | mmHg |
| admission: Heart rate | 110 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.3 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.1 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 150/78 | mmHg |
| discharge: Heart rate | 77 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 92.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.7 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Anticoagulation clinic follow-up (timing: 10 days; with service: anticoagulation clinic)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 67.000 kg

Imaging:

{'study_id': 'STUDY-VAL510-001', 'case_id': 'VAL-510', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute infiltrate.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL510-001', 'case_id': 'VAL-510', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue rate control and the planned anticoagulation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-511

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 67
- **Sex/gender:** Female
- **Weight:** 64.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 67-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Chest pain in the setting of Essential (primary) hypertension
- **Symptoms:** Fatigue, Chest pain
- **Symptom duration:** one day
- **Symptom course:** persistent
- **History of present illness:** A 67-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Fatigue, Chest pain, present for one day and persistent. Home medications include amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for symptomatic hypertensive urgency with chest pain, observed for end-organ symptoms. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

### Admission note

Admission note for a 67-year-old Female with Essential (primary) hypertension. Symptoms: Fatigue, Chest pain for one day (persistent). Medications continued from home: amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for symptomatic hypertensive urgency with chest pain, observed for end-organ symptoms. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 203/114 | mmHg |
| admission: Heart rate | 95 | beats/min |
| admission: Respiratory rate | 14 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.8 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.7 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 142/80 | mmHg |
| discharge: Heart rate | 74 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.9 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Blood-pressure follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 300 MG Oral Tablet was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 64.000 kg

Imaging:

{'study_id': 'STUDY-VAL511-001', 'case_id': 'VAL-511', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute pulmonary edema or focal consolidation.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL511-001', 'case_id': 'VAL-511', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'No ST-elevation pattern was documented.', 'recommendation': 'Continue observed antihypertensive therapy after end-organ evaluation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-512

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 70
- **Sex/gender:** Male
- **Weight:** 78.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 70-year-old Male with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Essential (primary) hypertension
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** intermittent
- **History of present illness:** A 70-year-old Male is admitted with Essential (primary) hypertension. Presenting symptoms include Fatigue, present for several days and intermittent. Home medications include hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for symptomatic hypertensive urgency with marked blood-pressure elevation. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

### Admission note

Admission note for a 70-year-old Male with Essential (primary) hypertension. Symptoms: Fatigue for several days (intermittent). Medications continued from home: hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for symptomatic hypertensive urgency with marked blood-pressure elevation. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 185/111 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 99.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.1 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.3 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 140.0 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 152/72 | mmHg |
| discharge: Heart rate | 110 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.3 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (discharge) | 140.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 20 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Electrolyte and blood-pressure follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 78.000 kg

Imaging:

{'study_id': 'STUDY-VAL512-001', 'case_id': 'VAL-512', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No pulmonary edema.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-513

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 66
- **Sex/gender:** Female
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 66-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Essential (primary) hypertension
- **Symptoms:** Fatigue
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 66-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Fatigue, present for one week and improving after treatment. Home medications include amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hypertensive urgency after home readings remained severely elevated. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 66-year-old Female with Essential (primary) hypertension. Symptoms: Fatigue for one week (improving after treatment). Medications continued from home: amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hypertensive urgency after home readings remained severely elevated. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 196/102 | mmHg |
| admission: Heart rate | 73 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.1 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 142/90 | mmHg |
| discharge: Heart rate | 105 | beats/min |
| discharge: Respiratory rate | 23 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.1 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | intravenous | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care blood-pressure check (timing: 3 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 75.000 kg

Imaging:

{'study_id': 'STUDY-VAL513-001', 'case_id': 'VAL-513', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute cardiopulmonary process.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-514

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 65
- **Sex/gender:** Female
- **Weight:** 82.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 65-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Chest pain in the setting of Essential (primary) hypertension
- **Symptoms:** Fatigue, Chest pain
- **Symptom duration:** one week
- **Symptom course:** worsening
- **History of present illness:** A 65-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Fatigue, Chest pain, present for one week and worsening. Home medications include amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for symptomatic hypertensive urgency on triple oral therapy, observed for end-organ symptoms. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

### Admission note

Admission note for a 65-year-old Female with Essential (primary) hypertension. Symptoms: Fatigue, Chest pain for one week (worsening). Medications continued from home: amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for symptomatic hypertensive urgency on triple oral therapy, observed for end-organ symptoms. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 210/104 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.6 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 138.0 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 137/89 | mmHg |
| discharge: Heart rate | 109 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.6 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (discharge) | 139.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 20 MG Delayed Release Oral Tablet. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 20 MG Delayed Release Oral Tablet. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Hypertension specialty follow-up (timing: 7 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 82.000 kg

Imaging:

{'study_id': 'STUDY-VAL514-001', 'case_id': 'VAL-514', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No pulmonary edema.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL514-001', 'case_id': 'VAL-514', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue observed antihypertensive therapy after end-organ evaluation.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-515

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 65
- **Sex/gender:** Male
- **Weight:** 103.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 65-year-old Male with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Essential (primary) hypertension
- **Symptoms:** Fatigue
- **Symptom duration:** two days
- **Symptom course:** progressive
- **History of present illness:** A 65-year-old Male is admitted with Essential (primary) hypertension. Presenting symptoms include Fatigue, present for two days and progressive. Home medications include atorvastatin 80 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. Admitted for a first presentation of severe symptomatic hypertension requiring observed treatment. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

### Admission note

Admission note for a 65-year-old Male with Essential (primary) hypertension. Symptoms: Fatigue for two days (progressive). Medications continued from home: atorvastatin 80 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. Admitted for a first presentation of severe symptomatic hypertension requiring observed treatment. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 180/110 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.4 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 122/80 | mmHg |
| discharge: Heart rate | 79 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.1 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- New antihypertensive follow-up (timing: 10 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 103.000 kg

Imaging:

{'study_id': 'STUDY-VAL515-001', 'case_id': 'VAL-515', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'No acute infiltrate.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-516

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 53
- **Sex/gender:** Female
- **Weight:** 66.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with hyperglycemia
- **Disposition:** home
- **One-liner:** 53-year-old Female with Type 2 diabetes mellitus with hyperglycemia

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Fatigue in the setting of Type 2 diabetes mellitus with hyperglycemia
- **Symptoms:** Polyuria, Fatigue
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 53-year-old Female is admitted with Type 2 diabetes mellitus with hyperglycemia. Presenting symptoms include Polyuria, Fatigue, present for one week and progressive. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for symptomatic hyperglycemia with polyuria requiring supervised glucose and fluid management. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

### Admission note

Admission note for a 53-year-old Female with Type 2 diabetes mellitus with hyperglycemia. Symptoms: Polyuria, Fatigue for one week (progressive). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for symptomatic hyperglycemia with polyuria requiring supervised glucose and fluid management. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 136/71 | mmHg |
| admission: Heart rate | 77 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.1 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 369.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 137/71 | mmHg |
| discharge: Heart rate | 86 | beats/min |
| discharge: Respiratory rate | 23 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.4 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 111.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Diabetes and kidney follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 66.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-517

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 53
- **Sex/gender:** Male
- **Weight:** 100.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with hyperglycemia
- **Disposition:** home
- **One-liner:** 53-year-old Male with Type 2 diabetes mellitus with hyperglycemia

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Type 2 diabetes mellitus with hyperglycemia
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 53-year-old Male is admitted with Type 2 diabetes mellitus with hyperglycemia. Presenting symptoms include Fatigue, present for several days and persistent. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia requiring inpatient glucose stabilization. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

### Admission note

Admission note for a 53-year-old Male with Type 2 diabetes mellitus with hyperglycemia. Symptoms: Fatigue for several days (persistent). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia requiring inpatient glucose stabilization. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 126/70 | mmHg |
| admission: Heart rate | 73 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 99.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 362.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.0 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 142/95 | mmHg |
| discharge: Heart rate | 85 | beats/min |
| discharge: Respiratory rate | 24 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 160.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 12.3 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | twice daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Glycemic follow-up (timing: 14 days; with service: endocrinology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 100.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-518

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 49
- **Sex/gender:** Female
- **Weight:** 70.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with hyperglycemia
- **Disposition:** home
- **One-liner:** 49-year-old Female with Type 2 diabetes mellitus with hyperglycemia

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria in the setting of Type 2 diabetes mellitus with hyperglycemia
- **Symptoms:** Polyuria
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 49-year-old Female is admitted with Type 2 diabetes mellitus with hyperglycemia. Presenting symptoms include Polyuria, present for two days and acutely worsening. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia with volume depletion requiring supervised treatment. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 49-year-old Female with Type 2 diabetes mellitus with hyperglycemia. Symptoms: Polyuria for two days (acutely worsening). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia with volume depletion requiring supervised treatment. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 127/76 | mmHg |
| admission: Heart rate | 73 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.3 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 354.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.8 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 158/96 | mmHg |
| discharge: Heart rate | 91 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 113.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.2 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia; supply: 7 days |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia; supply: 30 days |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Diabetes medication-supply follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 70.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-519

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 54
- **Sex/gender:** Male
- **Weight:** 100.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with hyperglycemia
- **Disposition:** home
- **One-liner:** 54-year-old Male with Type 2 diabetes mellitus with hyperglycemia

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Fatigue in the setting of Type 2 diabetes mellitus with hyperglycemia
- **Symptoms:** Polyuria, Fatigue
- **Symptom duration:** one day
- **Symptom course:** intermittent
- **History of present illness:** A 54-year-old Male is admitted with Type 2 diabetes mellitus with hyperglycemia. Presenting symptoms include Polyuria, Fatigue, present for one day and intermittent. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia; a pending outpatient diabetes-therapy decision was recorded. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 54-year-old Male with Type 2 diabetes mellitus with hyperglycemia. Symptoms: Polyuria, Fatigue for one day (intermittent). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia; a pending outpatient diabetes-therapy decision was recorded. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 137/74 | mmHg |
| admission: Heart rate | 82 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 99.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 366.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 153/96 | mmHg |
| discharge: Heart rate | 77 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 140.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

No follow-up appointments were specified.

## Discharge instructions

- A pending therapeutic decision remains. The outpatient metformin dose after this hyperglycemic admission remains to be confirmed at endocrinology follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 100.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-520

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 65
- **Sex/gender:** Male
- **Weight:** 96.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with hyperglycemia
- **Disposition:** home
- **One-liner:** 65-year-old Male with Type 2 diabetes mellitus with hyperglycemia

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Type 2 diabetes mellitus with hyperglycemia
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 65-year-old Male is admitted with Type 2 diabetes mellitus with hyperglycemia. Presenting symptoms include Fatigue, present for several days and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia that improved with supervised inpatient management. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

### Admission note

Admission note for a 65-year-old Male with Type 2 diabetes mellitus with hyperglycemia. Symptoms: Fatigue for several days (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for symptomatic hyperglycemia that improved with supervised inpatient management. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with hyperglycemia | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 130/72 | mmHg |
| admission: Heart rate | 70 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 251.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.3 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 158/76 | mmHg |
| discharge: Heart rate | 83 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 158.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.0 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with hyperglycemia |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Routine diabetes follow-up (timing: 21 days; with service: endocrinology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 96.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-521

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 75
- **Sex/gender:** Female
- **Weight:** 76.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 75-year-old Female with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 75-year-old Female is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, present for several days and persistent. Home medications include albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule. Admitted for community-acquired pneumonia with hypoxia and a lobar infiltrate. Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

### Admission note

Admission note for a 75-year-old Female with Lobar pneumonia, unspecified organism. Symptoms: Cough for several days (persistent). Medications continued from home: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule. Admitted for community-acquired pneumonia with hypoxia and a lobar infiltrate. Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 121/77 | mmHg |
| admission: Heart rate | 118 | beats/min |
| admission: Respiratory rate | 26 | breaths/min |
| admission: SpO2 | 90.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.7 | mg/dL |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 134.0 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 133/91 | mmHg |
| discharge: Heart rate | 93 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Sodium [Moles/volume] in Serum or Plasma (discharge) | 140.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | twice daily | indication: Lobar pneumonia, unspecified organism |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Pneumonia follow-up (timing: 7 days; with service: pulmonology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Cough (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 76.000 kg

Imaging:

{'study_id': 'STUDY-VAL521-001', 'case_id': 'VAL-521', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Right lower-lobe infiltrate consistent with pneumonia.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL521-001', 'case_id': 'VAL-521', 'service': 'pulmonology', 'timepoint': 'inpatient', 'assessment': 'Community-acquired pneumonia.', 'recommendation': 'Continue the intended antimicrobial and respiratory plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-522

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 78.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 71-year-old Male with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Wheezing in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Dyspnea, Wheezing
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 71-year-old Male is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Dyspnea, Wheezing, present for two days and acutely worsening. Home medications include albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule. Admitted for hypoxic pneumonia with wheezing. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 71-year-old Male with Lobar pneumonia, unspecified organism. Symptoms: Dyspnea, Wheezing for two days (acutely worsening). Medications continued from home: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule. Admitted for hypoxic pneumonia with wheezing. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | diagnosis | high | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 128/64 | mmHg |
| admission: Heart rate | 105 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.8 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 9.2 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 118/96 | mmHg |
| discharge: Heart rate | 101 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 92.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.1 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 2 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Respiratory follow-up (timing: 3 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 78.000 kg

Imaging:

{'study_id': 'STUDY-VAL522-001', 'case_id': 'VAL-522', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Left lower-lobe infiltrate with no large effusion.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL522-001', 'case_id': 'VAL-522', 'service': 'pulmonology', 'timepoint': 'inpatient', 'assessment': 'Pneumonia with bronchospasm.', 'recommendation': 'Continue the intended antimicrobial and respiratory plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-523

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Male
- **Weight:** 88.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 64-year-old Male with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough, Dyspnea in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough, Dyspnea
- **Symptom duration:** one day
- **Symptom course:** progressive
- **History of present illness:** A 64-year-old Male is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, Dyspnea, present for one day and progressive. Home medications include azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. albuterol 0.4 MG Inhalation Powder was held on admission and is not intended for discharge continuation. Admitted for community-acquired pneumonia requiring inpatient antibiotics. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 64-year-old Male with Lobar pneumonia, unspecified organism. Symptoms: Cough, Dyspnea for one day (progressive). Medications continued from home: azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. albuterol 0.4 MG Inhalation Powder was held on admission and is not intended for discharge continuation. Admitted for community-acquired pneumonia requiring inpatient antibiotics. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

**Past medical history:** Gastro-esophageal reflux disease without esophagitis

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | admission | active | inpatient |
| Gastro-esophageal reflux disease without esophagitis | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | diagnosis | high | active |
| Gastro-esophageal reflux disease without esophagitis | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 134/75 | mmHg |
| admission: Heart rate | 104 | beats/min |
| admission: Respiratory rate | 27 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 10.9 | g/dL |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 143.0 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 135/74 | mmHg |
| discharge: Heart rate | 109 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 9.8 | g/dL |
| Sodium [Moles/volume] in Serum or Plasma (discharge) | 139.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Gastro-esophageal reflux disease without esophagitis |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | held; held reason: Scheduled inhaler doses were held overnight for documented tachycardia; intended to restart.; indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Gastro-esophageal reflux disease without esophagitis |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 inhalation | inhaled | once daily | held; held reason: Scheduled inhaler doses were held overnight for documented tachycardia; intended to restart.; indication: symptomatic bronchospasm; not a treatment for the admission diagnosis |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Gastro-esophageal reflux disease without esophagitis |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Pulmonary follow-up after antibiotic course (timing: 14 days; with service: pulmonology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Cough (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 88.000 kg

Imaging:

{'study_id': 'STUDY-VAL523-001', 'case_id': 'VAL-523', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Lobar infiltrate improving compared with admission.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-524

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 74
- **Sex/gender:** Male
- **Weight:** 97.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 74-year-old Male with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough, Wheezing in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough, Wheezing
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 74-year-old Male is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, Wheezing, present for one week and improving after treatment. Home medications include azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. Admitted for pneumonia; a remaining oral antibiotic course was arranged at discharge. Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

### Admission note

Admission note for a 74-year-old Male with Lobar pneumonia, unspecified organism. Symptoms: Cough, Wheezing for one week (improving after treatment). Medications continued from home: azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. Admitted for pneumonia; a remaining oral antibiotic course was arranged at discharge. Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

## Relevant medical history

**Past medical history:** Gastro-esophageal reflux disease without esophagitis

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | admission | active | inpatient |
| Gastro-esophageal reflux disease without esophagitis | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Lobar pneumonia, unspecified organism | diagnosis | high | active |
| Gastro-esophageal reflux disease without esophagitis | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 137/83 | mmHg |
| admission: Heart rate | 92 | beats/min |
| admission: Respiratory rate | 28 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.7 | mg/dL |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 140.0 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 123/81 | mmHg |
| discharge: Heart rate | 110 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.4 | mg/dL |
| Sodium [Moles/volume] in Serum or Plasma (discharge) | 133.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Gastro-esophageal reflux disease without esophagitis |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Gastro-esophageal reflux disease without esophagitis |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism; supply: 7 days |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Gastro-esophageal reflux disease without esophagitis; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Antibiotic supply and pneumonia follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Cough (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 97.000 kg

Imaging:

{'study_id': 'STUDY-VAL524-001', 'case_id': 'VAL-524', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Improving infiltrate.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
