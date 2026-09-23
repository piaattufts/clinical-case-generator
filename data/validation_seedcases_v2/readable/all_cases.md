# CliniProof Clinical Case Set

## CLINIPROOF_SEEDCASES_V2

This document is intended for residents, clinicians, medical educators, pharmacists, and clinical informatics collaborators who want to review the clinical cases without reading the underlying JSON representation.

The set contains 24 cases, labeled VAL-601 through VAL-624. Each case is a synthetic inpatient encounter assembled for medication-reconciliation review. The software has already checked structure, terminology provenance, and a limited set of implemented clinical rules. Those automated checks do not establish clinical validity. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

This file contains only the information a resident would see. It does not identify which cases contain an intended assessment problem, if any, and it does not include investigator answer keys.

---

# VAL-601

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Female
- **Weight:** 78.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 77-year-old Female with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion, Fatigue in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion, Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 77-year-old Female is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, Fatigue, present for several days and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for delirium with an initially incomplete medication history. The patient could not supply a reliable medication history at admission. A collateral home-medication list arrived later and was verified. Unknown names are not treated as discharge orders. Ibuprofen is documented as intentionally discontinued, not as an unknown item. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

### Admission note

Admission note for a 77-year-old Female with Delirium due to known physiological condition. Symptoms: Confusion, Fatigue for several days (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for delirium with an initially incomplete medication history. The patient could not supply a reliable medication history at admission. A collateral home-medication list arrived later and was verified. Unknown names are not treated as discharge orders. Ibuprofen is documented as intentionally discontinued, not as an unknown item. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Type 2 diabetes mellitus without complications, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/78 | mmHg |
| admission: Heart rate | 101 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 244.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 141/96 | mmHg |
| discharge: Heart rate | 95 | beats/min |
| discharge: Respiratory rate | 20 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 148.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** caregiver and pharmacy
- **Reconciliation status:** complete
- **Patient able to participate:** No
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up after collateral medication verification (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 300 MG Oral Tablet was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Confusion (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 78.000 kg

Consultations:

{'consult_id': 'CON-VAL601-001', 'case_id': 'VAL-601', 'service': 'geriatrics', 'timepoint': 'inpatient', 'assessment': 'Delirium improved toward baseline.', 'recommendation': 'Use the verified collateral medication list at discharge.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-602

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 81
- **Sex/gender:** Female
- **Weight:** 73.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 81-year-old Female with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 81-year-old Female is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, present for two days and improving after treatment. Home medications include lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for delirium; a verified statin was confirmed from collateral sources. A later collateral list confirmed a continued statin. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

### Admission note

Admission note for a 81-year-old Female with Delirium due to known physiological condition. Symptoms: Confusion for two days (improving after treatment). Medications continued from home: lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for delirium; a verified statin was confirmed from collateral sources. A later collateral list confirmed a continued statin. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |
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
| admission: Blood pressure | 130/72 | mmHg |
| admission: Heart rate | 108 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.2 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 139/76 | mmHg |
| discharge: Heart rate | 94 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.1 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** pharmacy fill history
- **Reconciliation status:** complete
- **Patient able to participate:** No
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care medication-list follow-up (timing: 5 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Confusion (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 73.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-603

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Female
- **Weight:** 90.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 82-year-old Female with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Fatigue, Confusion
- **Symptom duration:** one week
- **Symptom course:** persistent
- **History of present illness:** A 82-year-old Female is admitted with Delirium due to known physiological condition. Presenting symptoms include Fatigue, Confusion, present for one week and persistent. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for delirium with a later-verified home regimen and home-health needs. Discharge planning includes home services. The verified list is the collateral regimen, including a diuretic identified after admission. The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

### Admission note

Admission note for a 82-year-old Female with Delirium due to known physiological condition. Symptoms: Fatigue, Confusion for one week (persistent). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for delirium with a later-verified home regimen and home-health needs. Discharge planning includes home services. The verified list is the collateral regimen, including a diuretic identified after admission. The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Type 2 diabetes mellitus without complications, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 158/95 | mmHg |
| admission: Heart rate | 76 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 355.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.7 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 145/90 | mmHg |
| discharge: Heart rate | 101 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 152.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.6 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications; supply: 30 days |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia; supply: 30 days |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 7 days |

## Medication reconciliation

- **Best possible medication history source:** caregiver and pharmacy
- **Reconciliation status:** complete
- **Patient able to participate:** No
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Home-health and primary care medication-supply follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 90.000 kg

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-604

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 76
- **Sex/gender:** Female
- **Weight:** 66.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 76-year-old Female with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 76-year-old Female is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, present for one day and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for resolving delirium; a pending outpatient cognitive-therapy decision was recorded. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented separately from unknown home medications. A new disease-modifying start was deferred to outpatient confirmation.

### Admission note

Admission note for a 76-year-old Female with Delirium due to known physiological condition. Symptoms: Confusion for one day (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for resolving delirium; a pending outpatient cognitive-therapy decision was recorded. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented separately from unknown home medications. A new disease-modifying start was deferred to outpatient confirmation.

A new disease-modifying start was deferred to outpatient confirmation.

## Relevant medical history

**Past medical history:** Type 2 diabetes mellitus without complications, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 131/81 | mmHg |
| admission: Heart rate | 79 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 299.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 149/89 | mmHg |
| discharge: Heart rate | 110 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 117.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medication reconciliation

- **Best possible medication history source:** family collateral
- **Reconciliation status:** complete
- **Patient able to participate:** No
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

No follow-up appointments were specified.

## Discharge instructions

- Start of a cognitive-enhancer remains a pending therapeutic decision for memory-clinic confirmation and is not an unknown home medication. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Confusion (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

# VAL-605

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 74
- **Sex/gender:** Male
- **Weight:** 64.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 74-year-old Male with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Edema, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Edema, Orthopnea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 74-year-old Male is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Edema, Orthopnea, present for one week and improving after treatment. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for acute heart-failure decompensation with congestion. Congestion improved with inpatient diuresis. Daily weights and intake/output were used to judge euvolemia before discharge. Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

### Admission note

Admission note for a 74-year-old Male with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Edema, Orthopnea for one week (improving after treatment). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for acute heart-failure decompensation with congestion. Congestion improved with inpatient diuresis. Daily weights and intake/output were used to judge euvolemia before discharge. Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

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

On hospital day 3, intake was 1588 mL and output was 1869 mL (net -281 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 115/70 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.0 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 1344.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.6 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 123/84 | mmHg |
| discharge: Heart rate | 104 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 92.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 295.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
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

- Heart-failure clinic after diuresis (timing: 7 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 64.000 kg
- discharge: 58.000 kg (dry weight 60.000 kg)

Imaging:

{'study_id': 'STUDY-VAL605-001', 'case_id': 'VAL-605', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Pulmonary edema without pneumonia.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL605-001', 'case_id': 'VAL-605', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-606

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 67
- **Sex/gender:** Male
- **Weight:** 103.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 67-year-old Male with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Edema in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Edema
- **Symptom duration:** several days
- **Symptom course:** progressive
- **History of present illness:** A 67-year-old Male is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Edema, present for several days and progressive. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. lisinopril 40 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for decompensated heart failure with worsening renal function. Creatinine rose with congestion. Lisinopril was held with an explicit plan to reassess restart after renal recovery. Creatinine rose with congestion. Selected therapy was held with a plan to reassess restart after renal recovery.

### Admission note

Admission note for a 67-year-old Male with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Edema for several days (progressive). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. lisinopril 40 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for decompensated heart failure with worsening renal function. Creatinine rose with congestion. Lisinopril was held with an explicit plan to reassess restart after renal recovery. Creatinine rose with congestion. Selected therapy was held with a plan to reassess restart after renal recovery.

Creatinine rose with congestion. Selected therapy was held with a plan to reassess restart after renal recovery.

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

On hospital day 4, intake was 1446 mL and output was 2165 mL (net -719 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 133/71 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.5 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.7 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 158/88 | mmHg |
| discharge: Heart rate | 87 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.8 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | held; held reason: Held for rising creatinine during decongestion; intended to restart after renal recovery.; indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | held; held reason: Held for rising creatinine during decongestion; intended to restart after renal recovery.; indication: Essential (primary) hypertension |
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

- Cardiology follow-up to reassess held therapy (timing: 3 days; with service: cardiology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 103.000 kg
- discharge: 100.000 kg (dry weight 96.000 kg)

Imaging:

{'study_id': 'STUDY-VAL606-001', 'case_id': 'VAL-606', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Congestion with small pleural effusions.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL606-001', 'case_id': 'VAL-606', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-607

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 76
- **Sex/gender:** Male
- **Weight:** 108.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 76-year-old Male with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Orthopnea
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 76-year-old Male is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Orthopnea, present for two days and acutely worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for decompensated heart failure with hypokalemia during diuresis. Diuresis was accompanied by potassium repletion. The intended outpatient diuretic dose is recorded. Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

### Admission note

Admission note for a 76-year-old Male with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Orthopnea for two days (acutely worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for decompensated heart failure with hypokalemia during diuresis. Diuresis was accompanied by potassium repletion. The intended outpatient diuretic dose is recorded. Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

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

On hospital day 3, intake was 1457 mL and output was 2054 mL (net -597 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 121/71 | mmHg |
| admission: Heart rate | 99 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.7 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 1310.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.2 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 155/83 | mmHg |
| discharge: Heart rate | 100 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.1 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 411.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.0 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 80 MG Oral Tablet | 20 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
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

- Electrolyte and heart-failure follow-up (timing: 5 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 108.000 kg
- discharge: 103.000 kg (dry weight 101.000 kg)

Imaging:

{'study_id': 'STUDY-VAL607-001', 'case_id': 'VAL-607', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Improving pulmonary edema.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL607-001', 'case_id': 'VAL-607', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-608

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 69
- **Sex/gender:** Female
- **Weight:** 73.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 69-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Edema, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Edema, Orthopnea
- **Symptom duration:** one week
- **Symptom course:** worsening
- **History of present illness:** A 69-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Edema, Orthopnea, present for one week and worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. Admitted for decompensated heart failure requiring diuretic adjustment. The outpatient diuretic plan was reviewed during the stay. The discharge list is the intended home regimen after that adjustment. The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

### Admission note

Admission note for a 69-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Edema, Orthopnea for one week (worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. Admitted for decompensated heart failure requiring diuretic adjustment. The outpatient diuretic plan was reviewed during the stay. The discharge list is the intended home regimen after that adjustment. The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute systolic (congestive) heart failure | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |

## Hospital course

On hospital day 4, intake was 1520 mL and output was 2684 mL (net -1164 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 139/92 | mmHg |
| admission: Heart rate | 77 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.7 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.3 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 131/89 | mmHg |
| discharge: Heart rate | 89 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.3 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.8 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
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

- Primary care volume follow-up after diuretic adjustment (timing: 7 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Edema (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 73.000 kg
- discharge: 68.000 kg (dry weight 65.000 kg)

Imaging:

{'study_id': 'STUDY-VAL608-001', 'case_id': 'VAL-608', 'timepoint': 'admission', 'study_type': 'Chest radiograph', 'body_site': 'chest', 'finding': 'Residual mild congestion.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL608-001', 'case_id': 'VAL-608', 'service': 'cardiology', 'timepoint': 'inpatient', 'assessment': 'Inpatient cardiology recommendations were recorded.', 'recommendation': 'Continue the intended heart-failure and diuretic plan.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-609

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Male
- **Weight:** 110.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 82-year-old Male with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Fatigue
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 82-year-old Male is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Fatigue, present for one week and improving after treatment. Home medications include ceftriaxone 500 MG Injection, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for endocarditis and discharged on planned outpatient parenteral antimicrobial therapy. The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring. A seven-day supply was arranged to cover therapy until infectious-disease follow-up. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

### Admission note

Admission note for a 82-year-old Male with Acute and subacute infective endocarditis. Symptoms: Fatigue for one week (improving after treatment). Medications continued from home: ceftriaxone 500 MG Injection, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for endocarditis and discharged on planned outpatient parenteral antimicrobial therapy. The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring. A seven-day supply was arranged to cover therapy until infectious-disease follow-up. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | diagnosis | high | active |
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
| admission: Blood pressure | 126/73 | mmHg |
| admission: Heart rate | 73 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.1 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 147/69 | mmHg |
| discharge: Heart rate | 104 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 93.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.4 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 12.2 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- weekly complete blood count and creatinine during parenteral therapy (frequency: weekly; responsible service: infectious disease)

The following items are follow-up appointments stored on the case.

- Infectious-disease follow-up with parenteral-therapy laboratory monitoring (timing: 14 days; with service: infectious disease)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 110.000 kg

Imaging:

{'study_id': 'STUDY-VAL609-001', 'case_id': 'VAL-609', 'timepoint': 'inpatient', 'study_type': 'Transthoracic echocardiogram', 'body_site': 'heart', 'finding': 'Vegetation treatment course in progress; ventricular function preserved.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL609-001', 'case_id': 'VAL-609', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Complete the planned parenteral course with laboratory follow-up.', 'source_reference': None}

Devices:

{'device_id': 'DEV-VAL609-001', 'case_id': 'VAL-609', 'device_type': 'PICC', 'site': 'right upper arm', 'placement_timepoint': 'inpatient', 'status': 'in_place', 'tip_location_or_confirmation': 'Tip position confirmed on chest radiograph', 'care_instructions': 'Line precautions and weekly dressing changes', 'removal_plan': 'Remove after the planned parenteral course', 'source_reference': None}

Microbiology:

{'micro_id': 'MICRO-VAL609-001', 'case_id': 'VAL-609', 'timepoint': 'admission', 'specimen': 'blood', 'test': 'blood culture', 'organism': None, 'result': 'no growth after 48 hours', 'status': 'final', 'notes': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-610

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 75
- **Sex/gender:** Female
- **Weight:** 81.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 75-year-old Female with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea, Fatigue in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Nausea, Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 75-year-old Female is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Nausea, Fatigue, present for several days and improving after treatment. Home medications include ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for endocarditis; remaining parenteral ceftriaxone is intended after discharge. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

### Admission note

Admission note for a 75-year-old Female with Acute and subacute infective endocarditis. Symptoms: Nausea, Fatigue for several days (improving after treatment). Medications continued from home: ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for endocarditis; remaining parenteral ceftriaxone is intended after discharge. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

## Relevant medical history

**Past medical history:** Type 2 diabetes mellitus without complications, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 133/70 | mmHg |
| admission: Heart rate | 106 | beats/min |
| admission: Respiratory rate | 26 | breaths/min |
| admission: SpO2 | 90.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 289.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 120/84 | mmHg |
| discharge: Heart rate | 100 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 145.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- weekly complete blood count and creatinine during parenteral therapy (frequency: weekly; responsible service: infectious disease)

The following items are follow-up appointments stored on the case.

- Infectious-disease clinic follow-up (timing: 7 days; with service: infectious disease)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 81.000 kg

Imaging:

{'study_id': 'STUDY-VAL610-001', 'case_id': 'VAL-610', 'timepoint': 'inpatient', 'study_type': 'Transthoracic echocardiogram', 'body_site': 'heart', 'finding': 'Treated endocarditis with improving clinical stability.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL610-001', 'case_id': 'VAL-610', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Complete the planned parenteral course with laboratory follow-up.', 'source_reference': None}

Devices:

{'device_id': 'DEV-VAL610-001', 'case_id': 'VAL-610', 'device_type': 'PICC', 'site': 'right upper arm', 'placement_timepoint': 'inpatient', 'status': 'in_place', 'tip_location_or_confirmation': 'Tip position confirmed on chest radiograph', 'care_instructions': 'Line precautions and weekly dressing changes', 'removal_plan': 'Remove after the planned parenteral course', 'source_reference': None}

Microbiology:

{'micro_id': 'MICRO-VAL610-001', 'case_id': 'VAL-610', 'timepoint': 'admission', 'specimen': 'blood', 'test': 'blood culture', 'organism': None, 'result': 'no growth after 48 hours', 'status': 'final', 'notes': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-611

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 83
- **Sex/gender:** Female
- **Weight:** 89.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 83-year-old Female with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** persistent
- **History of present illness:** A 83-year-old Female is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Nausea, present for two days and persistent. Home medications include aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for endocarditis with a remaining outpatient parenteral course. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Infectious-disease follow-up is scheduled. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

### Admission note

Admission note for a 83-year-old Female with Acute and subacute infective endocarditis. Symptoms: Nausea for two days (persistent). Medications continued from home: aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. Admitted for endocarditis with a remaining outpatient parenteral course. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Infectious-disease follow-up is scheduled. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 120/79 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.9 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 284.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.1 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 132/75 | mmHg |
| discharge: Heart rate | 95 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 94.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 138.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 9.3 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications; supply: 30 days |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis; supply: 30 days |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; supply: 7 days |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- weekly complete blood count and creatinine during parenteral therapy (frequency: weekly; responsible service: infectious disease)

The following items are follow-up appointments stored on the case.

- Infectious-disease follow-up for remaining antibiotic duration (timing: 14 days; with service: infectious disease)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 89.000 kg

Imaging:

{'study_id': 'STUDY-VAL611-001', 'case_id': 'VAL-611', 'timepoint': 'inpatient', 'study_type': 'Transthoracic echocardiogram', 'body_site': 'heart', 'finding': 'Endocarditis under treatment; patient clinically stable.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL611-001', 'case_id': 'VAL-611', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Complete the planned parenteral course with laboratory follow-up.', 'source_reference': None}

Devices:

{'device_id': 'DEV-VAL611-001', 'case_id': 'VAL-611', 'device_type': 'PICC', 'site': 'right upper arm', 'placement_timepoint': 'inpatient', 'status': 'in_place', 'tip_location_or_confirmation': 'Tip position confirmed on chest radiograph', 'care_instructions': 'Line precautions and weekly dressing changes', 'removal_plan': 'Remove after the planned parenteral course', 'source_reference': None}

Microbiology:

{'micro_id': 'MICRO-VAL611-001', 'case_id': 'VAL-611', 'timepoint': 'admission', 'specimen': 'blood', 'test': 'blood culture', 'organism': None, 'result': 'no growth after 48 hours', 'status': 'final', 'notes': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-612

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 70
- **Sex/gender:** Female
- **Weight:** 62.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 70-year-old Female with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 70-year-old Female is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Fatigue, Nausea, present for one week and improving after treatment. Home medications include aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, atorvastatin 80 MG Oral Tablet. Admitted for endocarditis; remaining parenteral duration is a pending outpatient decision. Duration of remaining parenteral ceftriaxone is to be confirmed at infectious-disease follow-up. Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

### Admission note

Admission note for a 70-year-old Female with Acute and subacute infective endocarditis. Symptoms: Fatigue, Nausea for one week (improving after treatment). Medications continued from home: aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, atorvastatin 80 MG Oral Tablet. Admitted for endocarditis; remaining parenteral duration is a pending outpatient decision. Duration of remaining parenteral ceftriaxone is to be confirmed at infectious-disease follow-up. Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 128/84 | mmHg |
| admission: Heart rate | 96 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 7.3 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 131/89 | mmHg |
| discharge: Heart rate | 110 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.4 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 500 MG Injection | 500 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- weekly complete blood count and creatinine during parenteral therapy (frequency: weekly; responsible service: infectious disease)

The following items are follow-up appointments stored on the case.

No follow-up appointments were specified.

## Discharge instructions

- A pending therapeutic decision remains. Remaining duration of parenteral ceftriaxone is to be confirmed at infectious-disease follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 62.000 kg

Imaging:

{'study_id': 'STUDY-VAL612-001', 'case_id': 'VAL-612', 'timepoint': 'inpatient', 'study_type': 'Transthoracic echocardiogram', 'body_site': 'heart', 'finding': 'Treated endocarditis awaiting confirmation of remaining duration.', 'source_reference': None}

Consultations:

{'consult_id': 'CON-VAL612-001', 'case_id': 'VAL-612', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Complete the planned parenteral course with laboratory follow-up.', 'source_reference': None}

Devices:

{'device_id': 'DEV-VAL612-001', 'case_id': 'VAL-612', 'device_type': 'PICC', 'site': 'right upper arm', 'placement_timepoint': 'inpatient', 'status': 'in_place', 'tip_location_or_confirmation': 'Tip position confirmed on chest radiograph', 'care_instructions': 'Line precautions and weekly dressing changes', 'removal_plan': 'Remove after the planned parenteral course', 'source_reference': None}

Microbiology:

{'micro_id': 'MICRO-VAL612-001', 'case_id': 'VAL-612', 'timepoint': 'admission', 'specimen': 'blood', 'test': 'blood culture', 'organism': None, 'result': 'no growth after 48 hours', 'status': 'final', 'notes': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-613

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 51
- **Sex/gender:** Male
- **Weight:** 62.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 51-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 51-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, present for several days and improving after treatment. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation. Gastrointestinal symptoms improved on antiviral therapy. Outpatient valganciclovir is the intended continuation. Kidney-transplant immunosuppression continues separately from CMV treatment. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

### Admission note

Admission note for a 51-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea for several days (improving after treatment). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation. Gastrointestinal symptoms improved on antiviral therapy. Outpatient valganciclovir is the intended continuation. Kidney-transplant immunosuppression continues separately from CMV treatment. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

## Relevant medical history

**Past medical history:** Kidney transplant status, Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Kidney transplant status | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Kidney transplant status | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

On hospital day 5, intake was 1665 mL and output was 1911 mL (net -246 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 137/90 | mmHg |
| admission: Heart rate | 92 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.2 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.6 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 144/78 | mmHg |
| discharge: Heart rate | 93 | beats/min |
| discharge: Respiratory rate | 24 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.6 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Transplant clinic follow-up after antiviral conversion (timing: 7 days; with service: transplant)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 62.000 kg
- discharge: 58.000 kg (dry weight 55.000 kg)

Consultations:

{'consult_id': 'CON-VAL613-001', 'case_id': 'VAL-613', 'service': 'transplant', 'timepoint': 'inpatient', 'assessment': 'Transplant-service recommendations were recorded.', 'recommendation': 'Continue immunosuppression with infection-related adjustments as documented.', 'source_reference': None}, {'consult_id': 'CON-VAL613-002', 'case_id': 'VAL-613', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Complete the planned parenteral course with laboratory follow-up.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-614

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Male
- **Weight:** 69.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 64-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea, Nausea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea, Nausea
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 64-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, Nausea, present for one week and progressive. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet. mycophenolate mofetil 250 MG Oral Capsule was held on admission and is not intended for discharge continuation. Admitted for cytomegalovirus disease after kidney transplantation with an infection-related mycophenolate hold. Mycophenolate was held during infection with a documented plan to reassess restart. Tacrolimus continues for transplant immunosuppression. Volume-related kidney injury led to temporary holds. Restart plans were documented for the held immunosuppression.

### Admission note

Admission note for a 64-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea, Nausea for one week (progressive). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet. mycophenolate mofetil 250 MG Oral Capsule was held on admission and is not intended for discharge continuation. Admitted for cytomegalovirus disease after kidney transplantation with an infection-related mycophenolate hold. Mycophenolate was held during infection with a documented plan to reassess restart. Tacrolimus continues for transplant immunosuppression. Volume-related kidney injury led to temporary holds. Restart plans were documented for the held immunosuppression.

Volume-related kidney injury led to temporary holds. Restart plans were documented for the held immunosuppression.

## Relevant medical history

**Past medical history:** Kidney transplant status, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Kidney transplant status | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Kidney transplant status | diagnosis | medium | active |

## Hospital course

On hospital day 4, intake was 1767 mL and output was 1978 mL (net -211 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/95 | mmHg |
| admission: Heart rate | 84 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 92.00 | % |

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
| discharge: Blood pressure | 127/82 | mmHg |
| discharge: Heart rate | 85 | beats/min |
| discharge: Respiratory rate | 20 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| mycophenolate mofetil 250 MG Oral Capsule | 250 MG | oral | once daily | indication: Kidney transplant status |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| mycophenolate mofetil 250 MG Oral Capsule | 250 MG | oral | once daily | held; held reason: Held during active infection as an immunosuppression adjustment; intended to restart.; indication: Kidney transplant status |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| mycophenolate mofetil 250 MG Oral Capsule | 250 MG | oral | once daily | held; held reason: Held during active infection as an immunosuppression adjustment; intended to restart.; indication: Kidney transplant status |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Transplant follow-up to reassess held immunosuppression (timing: 5 days; with service: transplant)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 69.000 kg
- discharge: 64.000 kg (dry weight 64.000 kg)

Consultations:

{'consult_id': 'CON-VAL614-001', 'case_id': 'VAL-614', 'service': 'transplant', 'timepoint': 'inpatient', 'assessment': 'Transplant-service recommendations were recorded.', 'recommendation': 'Continue immunosuppression with infection-related adjustments as documented.', 'source_reference': None}, {'consult_id': 'CON-VAL614-002', 'case_id': 'VAL-614', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Complete the planned parenteral course with laboratory follow-up.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-615

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 51
- **Sex/gender:** Female
- **Weight:** 80.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 51-year-old Female with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** intermittent
- **History of present illness:** A 51-year-old Female is admitted with Other cytomegaloviral diseases. Presenting symptoms include Nausea, present for two days and intermittent. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation with a tacrolimus dose adjustment. Tacrolimus was continued at the intended adjusted outpatient dose for transplant immunosuppression, not as treatment for CMV. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 51-year-old Female with Other cytomegaloviral diseases. Symptoms: Nausea for two days (intermittent). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation with a tacrolimus dose adjustment. Tacrolimus was continued at the intended adjusted outpatient dose for transplant immunosuppression, not as treatment for CMV. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

**Past medical history:** Kidney transplant status, Essential (primary) hypertension, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Kidney transplant status | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Kidney transplant status | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

On hospital day 3, intake was 1630 mL and output was 1721 mL (net -91 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 124/85 | mmHg |
| admission: Heart rate | 78 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.4 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.6 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 147/70 | mmHg |
| discharge: Heart rate | 82 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.3 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.6 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 2.5 MG | oral | once daily | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
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

- Transplant medication-dose follow-up (timing: 7 days; with service: transplant)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 80.000 kg
- discharge: 75.000 kg (dry weight 72.000 kg)

Consultations:

{'consult_id': 'CON-VAL615-001', 'case_id': 'VAL-615', 'service': 'transplant', 'timepoint': 'inpatient', 'assessment': 'Transplant-service recommendations were recorded.', 'recommendation': 'Continue immunosuppression with infection-related adjustments as documented.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-616

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 49
- **Sex/gender:** Male
- **Weight:** 78.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 49-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea, Fatigue in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea, Fatigue
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 49-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, Fatigue, present for one day and improving after treatment. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation; antiviral duration remains pending. Antiviral duration after conversion remains a pending outpatient decision. Tacrolimus continues for immunosuppression. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

### Admission note

Admission note for a 49-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea, Fatigue for one day (improving after treatment). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation; antiviral duration remains pending. Antiviral duration after conversion remains a pending outpatient decision. Tacrolimus continues for immunosuppression. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

## Relevant medical history

**Past medical history:** Kidney transplant status, Mixed hyperlipidemia

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |
| Kidney transplant status | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |
| Kidney transplant status | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 125/94 | mmHg |
| admission: Heart rate | 99 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.4 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 119/71 | mmHg |
| discharge: Heart rate | 91 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.4 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Kidney transplant status |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

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

- A pending therapeutic decision remains. Remaining duration of valganciclovir is to be confirmed at infectious-disease follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 78.000 kg

Consultations:

{'consult_id': 'CON-VAL616-001', 'case_id': 'VAL-616', 'service': 'transplant', 'timepoint': 'inpatient', 'assessment': 'Transplant-service recommendations were recorded.', 'recommendation': 'Continue immunosuppression with infection-related adjustments as documented.', 'source_reference': None}, {'consult_id': 'CON-VAL616-002', 'case_id': 'VAL-616', 'service': 'infectious disease', 'timepoint': 'inpatient', 'assessment': 'Infectious-disease recommendations were recorded.', 'recommendation': 'Confirm remaining antiviral duration as an outpatient decision.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-617

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 74
- **Sex/gender:** Female
- **Weight:** 61.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 74-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 74-year-old Female is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Fatigue, present for several days and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after operative repair of a femoral-neck fracture with planned warfarin resumption. Warfarin was interrupted for surgery and then resumed. Bridging injection is not continued at discharge in this profile. Anticoagulation was interrupted for surgery and then resumed.

### Admission note

Admission note for a 74-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Fatigue for several days (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after operative repair of a femoral-neck fracture with planned warfarin resumption. Warfarin was interrupted for surgery and then resumed. Bridging injection is not continued at discharge in this profile. Anticoagulation was interrupted for surgery and then resumed.

Anticoagulation was interrupted for surgery and then resumed.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Essential (primary) hypertension, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/88 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 275.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 9.5 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.0 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 130/77 | mmHg |
| discharge: Heart rate | 78 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 120.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.4 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.9 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
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

- Anticoagulation clinic INR follow-up after warfarin resumption (timing: 7 days; with service: anticoagulation clinic)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 61.000 kg

Consultations:

{'consult_id': 'CON-VAL617-001', 'case_id': 'VAL-617', 'service': 'orthopedics', 'timepoint': 'inpatient', 'assessment': 'Orthopedic postoperative recommendations were recorded.', 'recommendation': 'Protective weight bearing and rehabilitation as documented.', 'source_reference': None}

Procedures:

{'procedure_id': 'PROC-VAL617-001', 'case_id': 'VAL-617', 'procedure_name': 'Open reduction and internal fixation of femoral neck fracture', 'procedure_type': 'operative', 'date': None, 'time': 'inpatient', 'performed_by': None, 'anesthesia_type': None, 'findings': 'Fracture reduced and internally fixed.', 'complications': None, 'duration_minutes': None, 'laterality': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-618

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 88
- **Sex/gender:** Male
- **Weight:** 110.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 88-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea, Fatigue in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Nausea, Fatigue
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 88-year-old Male is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Nausea, Fatigue, present for one day and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after hip-fracture surgery; anticoagulation is intended at discharge. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

### Admission note

Admission note for a 88-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Nausea, Fatigue for one day (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after hip-fracture surgery; anticoagulation is intended at discharge. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Essential (primary) hypertension, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 128/92 | mmHg |
| admission: Heart rate | 82 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.9 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.7 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 153/93 | mmHg |
| discharge: Heart rate | 90 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.5 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.2 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Orthopedic and anticoagulation follow-up (timing: 14 days; with service: orthopedics)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 110.000 kg

Consultations:

{'consult_id': 'CON-VAL618-001', 'case_id': 'VAL-618', 'service': 'orthopedics', 'timepoint': 'inpatient', 'assessment': 'Orthopedic postoperative recommendations were recorded.', 'recommendation': 'Protective weight bearing and rehabilitation as documented.', 'source_reference': None}

Procedures:

{'procedure_id': 'PROC-VAL618-001', 'case_id': 'VAL-618', 'procedure_name': 'Open reduction and internal fixation of femoral neck fracture', 'procedure_type': 'operative', 'date': None, 'time': 'inpatient', 'performed_by': None, 'anesthesia_type': None, 'findings': 'Fracture reduced and internally fixed.', 'complications': None, 'duration_minutes': None, 'laterality': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-619

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 79
- **Sex/gender:** Female
- **Weight:** 101.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 79-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** persistent
- **History of present illness:** A 79-year-old Female is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Nausea, present for two days and persistent. Home medications include lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after hip-fracture surgery with planned anticoagulation follow-up. Warfarin was resumed. An anticoagulation-clinic INR visit is scheduled. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed.

### Admission note

Admission note for a 79-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Nausea for two days (persistent). Medications continued from home: lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after hip-fracture surgery with planned anticoagulation follow-up. Warfarin was resumed. An anticoagulation-clinic INR visit is scheduled. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed.

Anticoagulation was interrupted for surgery and then resumed.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |

## Hospital course

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 141/92 | mmHg |
| admission: Heart rate | 97 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.2 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.1 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 157/80 | mmHg |
| discharge: Heart rate | 96 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.3 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged.; supply: 7 days |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Anticoagulation supply and INR follow-up (timing: 14 days; with service: anticoagulation clinic)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 101.000 kg

Consultations:

{'consult_id': 'CON-VAL619-001', 'case_id': 'VAL-619', 'service': 'orthopedics', 'timepoint': 'inpatient', 'assessment': 'Orthopedic postoperative recommendations were recorded.', 'recommendation': 'Protective weight bearing and rehabilitation as documented.', 'source_reference': None}

Procedures:

{'procedure_id': 'PROC-VAL619-001', 'case_id': 'VAL-619', 'procedure_name': 'Open reduction and internal fixation of femoral neck fracture', 'procedure_type': 'operative', 'date': None, 'time': 'inpatient', 'performed_by': None, 'anesthesia_type': None, 'findings': 'Fracture reduced and internally fixed.', 'complications': None, 'duration_minutes': None, 'laterality': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-620

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 75
- **Sex/gender:** Female
- **Weight:** 71.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 75-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 75-year-old Female is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Fatigue, Nausea, present for one week and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after hip-fracture surgery with inpatient bridging anticoagulation only. Enoxaparin was used as inpatient bridging and is not intended to continue once warfarin is resumed. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

### Admission note

Admission note for a 75-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Fatigue, Nausea for one week (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Admitted after hip-fracture surgery with inpatient bridging anticoagulation only. Enoxaparin was used as inpatient bridging and is not intended to continue once warfarin is resumed. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Essential (primary) hypertension, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 124/81 | mmHg |
| admission: Heart rate | 93 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 250.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 7.7 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.0 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 127/74 | mmHg |
| discharge: Heart rate | 98 | beats/min |
| discharge: Respiratory rate | 22 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 140.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 9.4 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.0 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe | 100 MG/ML | intravenous | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe. |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe | 100 MG/ML | intravenous | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe. |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
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

- Orthopedic rehabilitation follow-up (timing: 10 days; with service: orthopedics)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 71.000 kg

Consultations:

{'consult_id': 'CON-VAL620-001', 'case_id': 'VAL-620', 'service': 'orthopedics', 'timepoint': 'inpatient', 'assessment': 'Orthopedic postoperative recommendations were recorded.', 'recommendation': 'Protective weight bearing and rehabilitation as documented.', 'source_reference': None}

Procedures:

{'procedure_id': 'PROC-VAL620-001', 'case_id': 'VAL-620', 'procedure_name': 'Open reduction and internal fixation of femoral neck fracture', 'procedure_type': 'operative', 'date': None, 'time': 'inpatient', 'performed_by': None, 'anesthesia_type': None, 'findings': 'Fracture reduced and internally fixed.', 'complications': None, 'duration_minutes': None, 'laterality': None, 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-621

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 73
- **Sex/gender:** Female
- **Weight:** 64.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 73-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 73-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, present for two days and improving after treatment. Home medications include lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. apixaban 2.5 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for gastrointestinal bleeding with held anticoagulation and a documented restart plan. Bleeding settled and hemoglobin was stable. Apixaban was held with a documented restart plan. The patient is discharge-ready. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

### Admission note

Admission note for a 73-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue for two days (improving after treatment). Medications continued from home: lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. apixaban 2.5 MG Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for gastrointestinal bleeding with held anticoagulation and a documented restart plan. Bleeding settled and hemoglobin was stable. Apixaban was held with a documented restart plan. The patient is discharge-ready. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Mixed hyperlipidemia, Essential (primary) hypertension

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 150/86 | mmHg |
| admission: Heart rate | 109 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 10.0 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 154/79 | mmHg |
| discharge: Heart rate | 105 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 94.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 10.1 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | held; held reason: Held for gastrointestinal bleeding; intended to restart after hemoglobin stability.; indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | held; held reason: Held for gastrointestinal bleeding; intended to restart after hemoglobin stability.; indication: Paroxysmal atrial fibrillation |
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

- Gastroenterology follow-up after held anticoagulation (timing: 7 days; with service: gastroenterology)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 64.000 kg

Consultations:

{'consult_id': 'CON-VAL621-001', 'case_id': 'VAL-621', 'service': 'gastroenterology', 'timepoint': 'inpatient', 'assessment': 'Gastroenterology recommendations were recorded.', 'recommendation': 'Hold anticoagulation while hemoglobin remains stable, then reassess.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-622

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 83
- **Sex/gender:** Female
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 83-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 83-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, Nausea, present for one day and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for gastrointestinal bleeding treated with inpatient acid suppression. Inpatient acid suppression was used for the bleed and is not intended to continue at discharge unless later prescribed. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 83-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue, Nausea for one day (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for gastrointestinal bleeding treated with inpatient acid suppression. Inpatient acid suppression was used for the bleed and is not intended to continue at discharge unless later prescribed. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Essential (primary) hypertension, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 152/77 | mmHg |
| admission: Heart rate | 103 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 270.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 9.3 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 149/96 | mmHg |
| discharge: Heart rate | 90 | beats/min |
| discharge: Respiratory rate | 21 | breaths/min |
| discharge: SpO2 | 93.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 134.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.5 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 20 MG Delayed Release Oral Tablet. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
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

- Primary care follow-up after gastrointestinal bleed (timing: 5 days; with service: primary care)

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

Consultations:

{'consult_id': 'CON-VAL622-001', 'case_id': 'VAL-622', 'service': 'gastroenterology', 'timepoint': 'inpatient', 'assessment': 'Gastroenterology recommendations were recorded.', 'recommendation': 'Hold anticoagulation while hemoglobin remains stable, then reassess.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-623

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 73
- **Sex/gender:** Male
- **Weight:** 82.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 73-year-old Male with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 73-year-old Male is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, present for several days and persistent. Home medications include apixaban 2.5 MG Oral Tablet, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for gastrointestinal bleeding with a pending anticoagulation decision. Restart versus continued hold of anticoagulation is a pending outpatient decision. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

### Admission note

Admission note for a 73-year-old Male with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue for several days (persistent). Medications continued from home: apixaban 2.5 MG Oral Tablet, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Admitted for gastrointestinal bleeding with a pending anticoagulation decision. Restart versus continued hold of anticoagulation is a pending outpatient decision. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

## Relevant medical history

**Past medical history:** Paroxysmal atrial fibrillation, Mixed hyperlipidemia, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |
| Mixed hyperlipidemia | past_history | active | history |
| Paroxysmal atrial fibrillation | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Paroxysmal atrial fibrillation | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 150/95 | mmHg |
| admission: Heart rate | 98 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.1 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 332.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 7.5 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 158/81 | mmHg |
| discharge: Heart rate | 102 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 92.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 136.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 9.1 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
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

- A pending therapeutic decision remains. Restart versus continued hold of apixaban remains a pending outpatient decision after the bleed. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 82.000 kg

Consultations:

{'consult_id': 'CON-VAL623-001', 'case_id': 'VAL-623', 'service': 'gastroenterology', 'timepoint': 'inpatient', 'assessment': 'Gastroenterology recommendations were recorded.', 'recommendation': 'Hold anticoagulation while hemoglobin remains stable, then reassess.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-624

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 69
- **Sex/gender:** Female
- **Weight:** 72.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 69-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 69-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, Nausea, present for one week and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. aspirin 75 MG Delayed Release Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for gastrointestinal bleeding with intentional aspirin discontinuation. Aspirin used for primary prevention was intentionally stopped after the bleed. That discontinuation is documented and is distinct from an omitted intended medication. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

### Admission note

Admission note for a 69-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue, Nausea for one week (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. aspirin 75 MG Delayed Release Oral Tablet was held on admission and is not intended for discharge continuation. Admitted for gastrointestinal bleeding with intentional aspirin discontinuation. Aspirin used for primary prevention was intentionally stopped after the bleed. That discontinuation is documented and is distinct from an omitted intended medication. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Essential (primary) hypertension, Type 2 diabetes mellitus without complications

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |
| Essential (primary) hypertension | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 129/81 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.1 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 128/94 | mmHg |
| discharge: Heart rate | 75 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 91.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 9.5 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus without complications |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: symptomatic analgesia; not a treatment for the admission diagnosis |
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

- Primary care follow-up after intentional aspirin discontinuation (timing: 10 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: aspirin 75 MG Delayed Release Oral Tablet was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 72.000 kg

Consultations:

{'consult_id': 'CON-VAL624-001', 'case_id': 'VAL-624', 'service': 'gastroenterology', 'timepoint': 'inpatient', 'assessment': 'Gastroenterology recommendations were recorded.', 'recommendation': 'Hold anticoagulation while hemoglobin remains stable, then reassess.', 'source_reference': None}

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
