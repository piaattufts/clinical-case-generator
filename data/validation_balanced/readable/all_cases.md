# CliniProof Clinical Case Set

## CLINIPROOF_BALANCED_V2

This document is intended for residents, clinicians, medical educators, pharmacists, and clinical informatics collaborators who want to review the clinical cases without reading the underlying JSON representation.

The set contains 24 cases, labeled VAL-301 through VAL-324. Each case is a synthetic inpatient encounter assembled for medication-reconciliation review. The software has already checked structure, terminology provenance, and a limited set of implemented clinical rules. Those automated checks do not establish clinical validity. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

This file contains only the information a resident would see. It does not identify which cases contain an intended assessment problem, if any, and it does not include investigator answer keys.

---

# VAL-301

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 73
- **Sex/gender:** Male
- **Weight:** 107.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 73-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 73-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea, present for several days and worsening. Home medications include furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. The hospital course focused on diuresis over several inpatient days. Intake and output were recorded, and congestion improved enough for discharge.

### Admission note

Admission note for a 73-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea for several days (worsening). Medications continued from home: furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. The hospital course focused on diuresis over several inpatient days. Intake and output were recorded, and congestion improved enough for discharge.

The hospital course focused on diuresis over several inpatient days. Intake and output were recorded, and congestion improved enough for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 2149 mL and output was 1543 mL (net 606 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 133/87 | mmHg |
| admission: Heart rate | 103 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 89.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 872.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.3 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 107.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-302

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 58
- **Sex/gender:** Male
- **Weight:** 96.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 58-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chronic fatigue syndrome in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Chronic fatigue syndrome
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 58-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Chronic fatigue syndrome, present for one week and improving after treatment. Home medications include furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 58-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Chronic fatigue syndrome for one week (improving after treatment). Medications continued from home: furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | diagnosis | high | active |

## Hospital course

On hospital day 4, intake was 1610 mL and output was 1453 mL (net 157 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/69 | mmHg |
| admission: Heart rate | 101 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.3 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.7 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| enalapril maleate 2.5 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 96.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-303

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 63
- **Sex/gender:** Male
- **Weight:** 99.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 63-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Angina pectoris in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Angina pectoris
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 63-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Angina pectoris, present for two days and acutely worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

### Admission note

Admission note for a 63-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Angina pectoris for two days (acutely worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 2099 mL and output was 957 mL (net 1142 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/73 | mmHg |
| admission: Heart rate | 91 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.5 | {INR} |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.9 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 99.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-304

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Female
- **Weight:** 63.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 71-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Anasarca, Orthopnea
- **Symptom duration:** one day
- **Symptom course:** progressive
- **History of present illness:** A 71-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Anasarca, Orthopnea, present for one day and progressive. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, spironolactone 100 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 71-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Anasarca, Orthopnea for one day (progressive). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, spironolactone 100 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1902 mL and output was 1738 mL (net 164 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 120/81 | mmHg |
| admission: Heart rate | 99 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 851.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.6 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Formulary substitution for metoprolol tartrate 37.5 MG Oral Tablet during admission (RxClass CV100 BETA BLOCKERS/RELATED). |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Anasarca (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 63.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-305

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 55
- **Sex/gender:** Male
- **Weight:** 106.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 55-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Orthopnea, Chronic fatigue syndrome in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Orthopnea, Chronic fatigue syndrome
- **Symptom duration:** one week
- **Symptom course:** persistent
- **History of present illness:** A 55-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Orthopnea, Chronic fatigue syndrome, present for one week and persistent. Home medications include apixaban 2.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 55-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Orthopnea, Chronic fatigue syndrome for one week (persistent). Medications continued from home: apixaban 2.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Unspecified systolic (congestive) heart failure | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 2199 mL and output was 1449 mL (net 750 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 138/95 | mmHg |
| admission: Heart rate | 107 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 462.0 | pg/mL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 106.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-306

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 76
- **Sex/gender:** Female
- **Weight:** 76.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 76-year-old Female with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Chronic fatigue syndrome
- **Symptom duration:** two days
- **Symptom course:** intermittent
- **History of present illness:** A 76-year-old Female is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Chronic fatigue syndrome, present for two days and intermittent. Home medications include apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

### Admission note

Admission note for a 76-year-old Female with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Chronic fatigue syndrome for two days (intermittent). Medications continued from home: apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet. Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

Heart rate was observed and treated during the stay. The patient was discharged once rate control was clinically acceptable.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1826 mL and output was 949 mL (net 877 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 123/78 | mmHg |
| admission: Heart rate | 126 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |

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

- **Best possible medication history source:** prior records
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

- admission: 76.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-307

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 80
- **Sex/gender:** Male
- **Weight:** 77.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 80-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Angina pectoris in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Chronic fatigue syndrome, Angina pectoris
- **Symptom duration:** one day
- **Symptom course:** acutely worsening
- **History of present illness:** A 80-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Chronic fatigue syndrome, Angina pectoris, present for one day and acutely worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 80-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Chronic fatigue syndrome, Angina pectoris for one day (acutely worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 1865 mL and output was 1520 mL (net 345 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 123/84 | mmHg |
| admission: Heart rate | 137 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 1.8 | {INR} |

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

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 77.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-308

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Female
- **Weight:** 65.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 64-year-old Female with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 64-year-old Female is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Chronic fatigue syndrome, present for several days and persistent. Home medications include apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 64-year-old Female with Paroxysmal atrial fibrillation. Symptoms: Chronic fatigue syndrome for several days (persistent). Medications continued from home: apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 2018 mL and output was 1640 mL (net 378 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 128/72 | mmHg |
| admission: Heart rate | 101 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.4 | umol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 20 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 65.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-309

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 73
- **Sex/gender:** Male
- **Weight:** 108.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 73-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Angina pectoris, Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Angina pectoris, Chronic fatigue syndrome
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 73-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Angina pectoris, Chronic fatigue syndrome, present for one week and progressive. Home medications include carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. apixaban 2.5 MG Oral Tablet, ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 73-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Angina pectoris, Chronic fatigue syndrome for one week (progressive). Medications continued from home: carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. apixaban 2.5 MG Oral Tablet, ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1816 mL and output was 1413 mL (net 403 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 138/82 | mmHg |
| admission: Heart rate | 133 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.8 | umol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 108.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-310

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Male
- **Weight:** 62.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 64-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 64-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Chronic fatigue syndrome, present for two days and improving after treatment. Home medications include carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 64-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Chronic fatigue syndrome for two days (improving after treatment). Medications continued from home: carvedilol 6.25 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Paroxysmal atrial fibrillation | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 1321 mL and output was 1100 mL (net 221 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 123/69 | mmHg |
| admission: Heart rate | 78 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.5 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 62.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-311

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 52
- **Sex/gender:** Female
- **Weight:** 74.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 52-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Angina pectoris in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome, Angina pectoris
- **Symptom duration:** one day
- **Symptom course:** persistent
- **History of present illness:** A 52-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome, Angina pectoris, present for one day and persistent. Home medications include amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

### Admission note

Admission note for a 52-year-old Female with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome, Angina pectoris for one day (persistent). Medications continued from home: amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

Blood pressure was treated and observed in hospital. The discharge plan continues the selected antihypertensive regimen.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 1427 mL and output was 1710 mL (net -283 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 174/93 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 99.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.3 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.6 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 74.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-312

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 69
- **Sex/gender:** Male
- **Weight:** 104.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 69-year-old Male with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** intermittent
- **History of present illness:** A 69-year-old Male is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome, present for several days and intermittent. Home medications include hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 69-year-old Male with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome for several days (intermittent). Medications continued from home: hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 2152 mL and output was 1752 mL (net 400 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 169/99 | mmHg |
| admission: Heart rate | 81 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 143.0 | mmol/L |

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
| hydrochlorothiazide 50 MG Oral Tablet | 20 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 104.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-313

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 78
- **Sex/gender:** Female
- **Weight:** 72.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 78-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 78-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome, present for one week and improving after treatment. Home medications include amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 78-year-old Female with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome for one week (improving after treatment). Medications continued from home: amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1568 mL and output was 1799 mL (net -231 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/96 | mmHg |
| admission: Heart rate | 96 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | intravenous | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 72.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-314

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 74
- **Sex/gender:** Male
- **Weight:** 77.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 74-year-old Male with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Angina pectoris in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome, Angina pectoris
- **Symptom duration:** one week
- **Symptom course:** worsening
- **History of present illness:** A 74-year-old Male is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome, Angina pectoris, present for one week and worsening. Home medications include amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 74-year-old Male with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome, Angina pectoris for one week (worsening). Medications continued from home: amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1222 mL and output was 1274 mL (net -52 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 151/98 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.1 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.0 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 134.0 | mmol/L |

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

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 77.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-315

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 53
- **Sex/gender:** Female
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 53-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** two days
- **Symptom course:** progressive
- **History of present illness:** A 53-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome, present for two days and progressive. Home medications include atorvastatin 80 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 53-year-old Female with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome for two days (progressive). Medications continued from home: atorvastatin 80 MG Oral Tablet, enalapril maleate 2.5 MG Oral Tablet. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Essential (primary) hypertension | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Essential (primary) hypertension | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1215 mL and output was 1294 mL (net -79 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.70 | °C |
| admission: Blood pressure | 150/98 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 14 | breaths/min |
| admission: SpO2 | 99.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.4 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| enalapril maleate 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 75.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-316

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 55
- **Sex/gender:** Female
- **Weight:** 93.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 55-year-old Female with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Polyuria, Chronic fatigue syndrome
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 55-year-old Female is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Polyuria, Chronic fatigue syndrome, present for one week and progressive. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

### Admission note

Admission note for a 55-year-old Female with Type 2 diabetes mellitus with unspecified complications. Symptoms: Polyuria, Chronic fatigue syndrome for one week (progressive). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1563 mL and output was 1370 mL (net 193 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 138/84 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 15 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 175.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 93.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-317

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 78
- **Sex/gender:** Male
- **Weight:** 66.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 78-year-old Male with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 78-year-old Male is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Chronic fatigue syndrome, present for several days and persistent. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 78-year-old Male with Type 2 diabetes mellitus with unspecified complications. Symptoms: Chronic fatigue syndrome for several days (persistent). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 1656 mL and output was 1598 mL (net 58 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 120/71 | mmHg |
| admission: Heart rate | 86 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 128.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 12.5 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | twice daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 66.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-318

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 52
- **Sex/gender:** Female
- **Weight:** 88.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 52-year-old Female with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Polyuria
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 52-year-old Female is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Polyuria, present for two days and acutely worsening. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 52-year-old Female with Type 2 diabetes mellitus with unspecified complications. Symptoms: Polyuria for two days (acutely worsening). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 2112 mL and output was 1605 mL (net 507 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 118/85 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.8 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 127.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 13.6 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications; supply: 30 days |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications; supply: 30 days |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications; supply: 7 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 88.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-319

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 50
- **Sex/gender:** Female
- **Weight:** 109.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 50-year-old Female with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Polyuria, Chronic fatigue syndrome
- **Symptom duration:** one day
- **Symptom course:** intermittent
- **History of present illness:** A 50-year-old Female is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Polyuria, Chronic fatigue syndrome, present for one day and intermittent. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 50-year-old Female with Type 2 diabetes mellitus with unspecified complications. Symptoms: Polyuria, Chronic fatigue syndrome for one day (intermittent). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1485 mL and output was 1017 mL (net 468 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.60 | °C |
| admission: Blood pressure | 125/83 | mmHg |
| admission: Heart rate | 86 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 171.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

No follow-up appointments were specified.

## Discharge instructions

- Pending therapeutic decision: duration of Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet remains uncertain and will be determined at the scheduled follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 109.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-320

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 79
- **Sex/gender:** Male
- **Weight:** 91.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 79-year-old Male with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 79-year-old Male is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Chronic fatigue syndrome, present for several days and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

### Admission note

Admission note for a 79-year-old Male with Type 2 diabetes mellitus with unspecified complications. Symptoms: Chronic fatigue syndrome for several days (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

Glucose was monitored and diabetes therapy was continued while the inpatient team prepared a discharge plan.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Type 2 diabetes mellitus with unspecified complications | diagnosis | high | active |

## Hospital course

On hospital day 1, intake was 1885 mL and output was 1030 mL (net 855 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 130/91 | mmHg |
| admission: Heart rate | 93 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 153.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 13.5 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 91.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-321

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 83.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 71-year-old Male with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 71-year-old Male is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, present for several days and persistent. Home medications include azithromycin 250 MG Oral Capsule, albuterol 4 MG Extended Release Oral Capsule. Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

### Admission note

Admission note for a 71-year-old Male with Lobar pneumonia, unspecified organism. Symptoms: Cough for several days (persistent). Medications continued from home: azithromycin 250 MG Oral Capsule, albuterol 4 MG Extended Release Oral Capsule. Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

Inpatient antimicrobial therapy was administered and respiratory symptoms were monitored until the patient was ready for discharge.

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

On hospital day 2, intake was 2182 mL and output was 1164 mL (net 1018 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 138/77 | mmHg |
| admission: Heart rate | 96 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 140.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | twice daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 83.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-322

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 78
- **Sex/gender:** Female
- **Weight:** 95.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 78-year-old Female with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Wheezing in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Dyspnea, Wheezing
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 78-year-old Female is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Dyspnea, Wheezing, present for two days and acutely worsening. Home medications include azithromycin 250 MG Oral Capsule, albuterol 4 MG Extended Release Oral Capsule. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

### Admission note

Admission note for a 78-year-old Female with Lobar pneumonia, unspecified organism. Symptoms: Dyspnea, Wheezing for two days (acutely worsening). Medications continued from home: azithromycin 250 MG Oral Capsule, albuterol 4 MG Extended Release Oral Capsule. Symptoms improved after inpatient treatment. The patient was observed until discharge readiness was documented.

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

On hospital day 3, intake was 2127 mL and output was 882 mL (net 1245 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 121/84 | mmHg |
| admission: Heart rate | 104 | beats/min |
| admission: Respiratory rate | 28 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.3 | umol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.7 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 2 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 95.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-323

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 63
- **Sex/gender:** Female
- **Weight:** 63.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 63-year-old Female with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough, Dyspnea in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough, Dyspnea
- **Symptom duration:** one day
- **Symptom course:** progressive
- **History of present illness:** A 63-year-old Female is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, Dyspnea, present for one day and progressive. Home medications include albuterol 4 MG Extended Release Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. azithromycin 250 MG Oral Capsule was held on admission and is not intended for discharge continuation. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 63-year-old Female with Lobar pneumonia, unspecified organism. Symptoms: Cough, Dyspnea for one day (progressive). Medications continued from home: albuterol 4 MG Extended Release Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. azithromycin 250 MG Oral Capsule was held on admission and is not intended for discharge continuation. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

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

On hospital day 2, intake was 1218 mL and output was 1354 mL (net -136 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 133/68 | mmHg |
| admission: Heart rate | 101 | beats/min |
| admission: Respiratory rate | 27 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.7 | g/dL |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 136.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 4 MG Extended Release Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 63.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
---

# VAL-324

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Male
- **Weight:** 101.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 82-year-old Male with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough, Wheezing in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough, Wheezing
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 82-year-old Male is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, Wheezing, present for one week and improving after treatment. Home medications include azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

### Admission note

Admission note for a 82-year-old Male with Lobar pneumonia, unspecified organism. Symptoms: Cough, Wheezing for one week (improving after treatment). Medications continued from home: azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

The inpatient stay was brief. Intake and output were recorded, and the patient was judged ready for discharge home.

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

On hospital day 1, intake was 1240 mL and output was 1708 mL (net -468 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 158/73 | mmHg |
| admission: Heart rate | 107 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.4 | umol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 140.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism; supply: 7 days |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 101.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.
