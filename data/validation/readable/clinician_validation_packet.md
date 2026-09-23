# CliniProof clinician validation packet

## Purpose

The cases are synthetically generated clinical cases produced by CliniProof and are being reviewed for clinical validity. Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass.

The frozen set is `CLINIPROOF_TAXONOMY_V1`, containing twenty-four cases labeled VAL-201 through VAL-224. That freeze is archived historical provenance and is not an active prospective study set. New reviewers should start at [`../../active_validation_sets.md`](../../active_validation_sets.md). Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. That sentence means the software has already checked structure, terminology, and a limited set of implemented rules, but a clinician has not yet accepted the case for educational use.

## Reviewer task

For each case:

1. Read the complete case.
2. Assess C1–C5 using the forms that follow the case.
3. Record ratings in [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv).
4. Add comments where a problem is identified.

Do not split these ratings across separate review stages. Complete all five criteria during this one review.

C1 asks whether the chart could reasonably represent a patient in the stated inpatient setting. C2 asks whether the intended medication-reconciliation or transition-of-care problem is actually present. C3 asks whether an internal medicine resident could detect and resolve that problem from the case documents. C4 asks whether another unintended clinically meaningful problem is also present. C5 is an expert estimate of expected learner difficulty.

This packet includes the intended assessment issue for each case so that C2 through C5 can be completed in the same pass as C1. Full criterion definitions are in [`validation_rubric.md`](validation_rubric.md).

---

# VAL-201

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 78
- **Sex/gender:** Male
- **Weight:** 104.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 78-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 78-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 78-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1927 mL and output was 1119 mL (net 808 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 155/94 | mmHg |
| admission: Heart rate | 80 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 1.8 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 872.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.1 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Medication omitted at discharge

**CliniProof identifier:**

`f1_omission`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- lisinopril 1 MG/ML Oral Solution (rxcui=1806884)

**What should have occurred clinically:**

A medication indicated at discharge was omitted from the discharge medication list.

Clean expected state: present

**What appears in the case:**

absent

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge medications

**Expected clinical action:**

Restore the omitted continued discharge medication.

### Technical implementation

- **Changed field:** presence
- **Detectability location:** Discharge medications
- **Evidence required:** Home/inpatient continuation of this medication with no stop rationale.
- **Rationale:** A medication indicated at discharge was omitted from the discharge medication list.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-202

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 60
- **Sex/gender:** Male
- **Weight:** 81.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 60-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 60-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 60-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1751 mL and output was 1598 mL (net 153 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 147/81 | mmHg |
| admission: Heart rate | 107 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.3 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.1 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 889.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 81.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Medication inappropriately added or continued

**CliniProof identifier:**

`f1_commission`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- ibuprofen 0.05 MG/MG Topical Gel (rxcui=141997)

**What should have occurred clinically:**

A medication was prescribed at discharge without a clinical indication or intended discharge role.

Clean expected state: absent

**What appears in the case:**

present

**Where the relevant evidence appears:**

Home medications, discharge instructions, Discharge medications

**Expected clinical action:**

Remove the unindicated medication from the discharge list.

### Technical implementation

- **Changed field:** presence
- **Detectability location:** Discharge medications
- **Evidence required:** Home medication was discontinued and should not appear at discharge.
- **Rationale:** A medication was prescribed at discharge without a clinical indication or intended discharge role.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-203

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 57
- **Sex/gender:** Female
- **Weight:** 92.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 57-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 57-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 57-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1577 mL and output was 1621 mL (net -44 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 132/87 | mmHg |
| admission: Heart rate | 103 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.3 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 654.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.7 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 2 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 92.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Unexplained dose discrepancy

**CliniProof identifier:**

`f1_dose_mismatch`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- furosemide 4 MG/ML Oral Solution (rxcui=104220)

**What should have occurred clinically:**

The discharge dose differs from the intended medication plan without a documented clinical rationale.

Clean expected state: 1 tablet

**What appears in the case:**

2 tablet

**Where the relevant evidence appears:**

Home medications, Discharge medications

**Expected clinical action:**

Restore the correct continued discharge dose.

### Technical implementation

- **Changed field:** dose
- **Detectability location:** Discharge medications
- **Evidence required:** Intended dose on the home/inpatient medication plan.
- **Rationale:** The discharge dose differs from the intended medication plan without a documented clinical rationale.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-204

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 79
- **Sex/gender:** Female
- **Weight:** 109.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 79-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 79-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 79-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1609 mL and output was 1491 mL (net 118 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 136/76 | mmHg |
| admission: Heart rate | 104 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.8 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 399.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | intravenous | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Unexplained route discrepancy

**CliniProof identifier:**

`f1_route_mismatch`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- lisinopril 1 MG/ML Oral Solution (rxcui=1806884)

**What should have occurred clinically:**

The discharge route differs from the intended medication plan without a documented clinical rationale.

Clean expected state: oral

**What appears in the case:**

intravenous

**Where the relevant evidence appears:**

Home medications, Discharge medications

**Expected clinical action:**

Restore the correct continued discharge route.

### Technical implementation

- **Changed field:** route
- **Detectability location:** Discharge medications
- **Evidence required:** Intended route on the home/inpatient medication plan.
- **Rationale:** The discharge route differs from the intended medication plan without a documented clinical rationale.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-205

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 85
- **Sex/gender:** Male
- **Weight:** 71.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 85-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 85-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 85-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 2032 mL and output was 1169 mL (net 863 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 122/93 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.9 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 336.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.6 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | twice daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 71.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Unexplained frequency discrepancy

**CliniProof identifier:**

`f1_frequency_mismatch`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- lisinopril 1 MG/ML Oral Solution (rxcui=1806884)

**What should have occurred clinically:**

The discharge frequency differs from the intended medication plan without a documented clinical rationale.

Clean expected state: once daily

**What appears in the case:**

twice daily

**Where the relevant evidence appears:**

Home medications, Discharge medications

**Expected clinical action:**

Restore the correct continued discharge frequency.

### Technical implementation

- **Changed field:** frequency
- **Detectability location:** Discharge medications
- **Evidence required:** Intended frequency on the home/inpatient medication plan.
- **Rationale:** The discharge frequency differs from the intended medication plan without a documented clinical rationale.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-206

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 55
- **Sex/gender:** Male
- **Weight:** 98.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 55-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 55-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 55-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1578 mL and output was 959 mL (net 619 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 149/87 | mmHg |
| admission: Heart rate | 96 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.1 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.0 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 539.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.1 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| carvedilol 6.25 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 98.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Unexplained therapeutic substitution

**CliniProof identifier:**

`f1_therapeutic_substitution`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- metoprolol tartrate 37.5 MG Oral Tablet (role=source; rxcui=1606347)
- carvedilol 6.25 MG Oral Tablet (role=substitute; rxcui=200031)

**What should have occurred clinically:**

A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.

Clean expected state: dose: 37.5 MG; drug: metoprolol tartrate 37.5 MG Oral Tablet; frequency: once daily; monitoring: none; quantity or days: none; route: oral; rxcui: 1606347; status: discharge

**What appears in the case:**

dose: 37.5 MG; drug: carvedilol 6.25 MG Oral Tablet; frequency: once daily; monitoring: none; quantity or days: none; route: oral; rxcui: 200031; status: discharge

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge medications

**Expected clinical action:**

Restore the original continued medication; do not leave an unexplained same-class substitute.

### Technical implementation

- **Changed field:** drug
- **Detectability location:** Discharge medications
- **Evidence required:** RxClass CV100 (BETA BLOCKERS/RELATED) relates the source and substitute.
- **Rationale:** A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-207

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 68
- **Sex/gender:** Male
- **Weight:** 97.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 68-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 68-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 68-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 2080 mL and output was 1294 mL (net 786 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/74 | mmHg |
| admission: Heart rate | 107 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.1 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.8 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 690.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.9 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
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

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 97.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Required outpatient monitoring not arranged

**CliniProof identifier:**

`f2_monitoring_not_arranged`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- warfarin sodium 1 MG Oral Tablet (rxcui=855288; rule_code=WARFARIN_INR_MONITORING)

**What should have occurred clinically:**

A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.

Clean expected state: case monitoring ids: present; medication monitoring: Outpatient monitoring arranged.

**What appears in the case:**

case monitoring: none; medication monitoring: none

**Where the relevant evidence appears:**

Discharge medications, Laboratory results, Scheduled monitoring

**Expected clinical action:**

Arrange the required outpatient monitoring for the trigger medication.

### Technical implementation

- **Changed field:** monitoring
- **Detectability location:** Scheduled monitoring, discharge medications.monitoring
- **Evidence required:** Trigger medication remains; source-backed rule WARFARIN_INR_MONITORING requires 38875-1.
- **Rationale:** A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-208

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 59
- **Sex/gender:** Female
- **Weight:** 92.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 59-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 59-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. furosemide 4 MG/ML Oral Solution, ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 59-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. furosemide 4 MG/ML Oral Solution, ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1510 mL and output was 1049 mL (net 461 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 141/74 | mmHg |
| admission: Heart rate | 92 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.1 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.1 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 712.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.5 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 92.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Held medication without a restart plan

**CliniProof identifier:**

`f2_held_med_no_restart_plan`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- furosemide 4 MG/ML Oral Solution (rxcui=104220)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding furosemide 4 MG/ML Oral Solution: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; target or goal: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; Resume when systolic blood pressure remains above 100 mmHg for 24 hours.

**What appears in the case:**

instructions: none; target or goal: none

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge instructions

**Expected clinical action:**

Document when and under what criteria the held medication should be restarted.

### Technical implementation

- **Changed field:** restart_plan
- **Detectability location:** Discharge instructions, CaseMedication.target or goal
- **Evidence required:** The medication was held for a documented reason and needs a restart plan.
- **Rationale:** A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-209

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 62
- **Sex/gender:** Male
- **Weight:** 63.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 62-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 62-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 62-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1547 mL and output was 1368 mL (net 179 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 122/91 | mmHg |
| admission: Heart rate | 104 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.0 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 413.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.3 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; supply: 30 days |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; supply: 30 days |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure; supply: 7 days |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure; supply: 30 days |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; supply: 30 days |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Insufficient medication supply

**CliniProof identifier:**

`f2_insufficient_supply`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- furosemide 4 MG/ML Oral Solution (rxcui=104220)

**What should have occurred clinically:**

The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.

Clean expected state: 30 days

**What appears in the case:**

7 days

**Where the relevant evidence appears:**

Follow-up appointments, discharge medications.quantity or days

**Expected clinical action:**

Increase days' supply so treatment continues through the planned follow-up.

### Technical implementation

- **Changed field:** quantity_or_days
- **Detectability location:** discharge medications.quantity or days
- **Evidence required:** Days' supply must cover the scheduled follow-up or treatment endpoint.
- **Rationale:** The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-210

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Female
- **Weight:** 74.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 71-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 71-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 71-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1487 mL and output was 1482 mL (net 5 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 144/71 | mmHg |
| admission: Heart rate | 100 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.0 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 236.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.2 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 20 MG Delayed Release Oral Tablet. |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 20 MG Delayed Release Oral Tablet. |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Hospital-only medication continued after discharge

**CliniProof identifier:**

`f2_hospital_only_continued`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- pantoprazole 20 MG Delayed Release Oral Tablet (rxcui=251872)

**What should have occurred clinically:**

A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.

Clean expected state: absent

**What appears in the case:**

present

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge medications, Medication plan / decision reason

**Expected clinical action:**

Stop the hospital-only medication at discharge.

### Technical implementation

- **Changed field:** presence
- **Detectability location:** Discharge medications
- **Evidence required:** Medication was started in hospital for an inpatient-only indication and should stop.
- **Rationale:** A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-211

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Male
- **Weight:** 60.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 77-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 77-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 77-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1532 mL and output was 973 mL (net 559 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 121/75 | mmHg |
| admission: Heart rate | 98 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.1 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 629.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | once daily | indication: Formulary substitution for metoprolol tartrate 37.5 MG Oral Tablet during admission (RxClass CV100 BETA BLOCKERS/RELATED). |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| carvedilol 6.25 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 60.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Temporary inpatient substitution not addressed at discharge

**CliniProof identifier:**

`f2_inpatient_substitution_not_reverted`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- metoprolol tartrate 37.5 MG Oral Tablet (role=home_therapy; rxcui=1606347)
- carvedilol 6.25 MG Oral Tablet (role=inpatient_substitute; rxcui=200031)

**What should have occurred clinically:**

A home therapy temporarily replaced during hospitalization for formulary or protocol reasons was neither reverted nor explicitly re-decided at discharge.

Clean expected state: dose: 37.5 MG; drug: metoprolol tartrate 37.5 MG Oral Tablet; frequency: once daily; monitoring: none; quantity or days: none; route: oral; rxcui: 1606347; status: discharge

**What appears in the case:**

dose: 37.5 MG; drug: carvedilol 6.25 MG Oral Tablet; frequency: once daily; monitoring: none; quantity or days: none; route: oral; rxcui: 200031; status: discharge

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge medications, Discharge instructions

**Expected clinical action:**

Revert to the home therapy or document an intentional decision to continue the inpatient substitute.

### Technical implementation

- **Changed field:** discharge_medication
- **Detectability location:** Discharge medications
- **Evidence required:** Home therapy was temporarily replaced inpatient and should be reverted or explicitly re-decided.
- **Rationale:** A home therapy temporarily replaced during hospitalization for formulary or protocol reasons was neither reverted nor explicitly re-decided at discharge.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-212

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 66
- **Sex/gender:** Male
- **Weight:** 79.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 66-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 66-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 66-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 2115 mL and output was 1763 mL (net 352 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 149/96 | mmHg |
| admission: Heart rate | 82 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.0 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 427.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.5 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: as labeled; responsible service: outpatient anticoagulation)

The following items are follow-up appointments stored on the case.

No follow-up appointments were specified.

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Pending therapeutic decision: duration of furosemide 4 MG/ML Oral Solution remains uncertain and will be determined at the scheduled follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 79.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Follow-up missing for an unresolved treatment decision

**CliniProof identifier:**

`f2_pending_decision_followup_missing`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- furosemide 4 MG/ML Oral Solution (rxcui=104220)

**What should have occurred clinically:**

Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.

Clean expected state: item: Reassess pending therapeutic decision; timing: 7 days; with service: primary care

**What appears in the case:**

none

**Where the relevant evidence appears:**

Discharge instructions, Follow-up appointments

**Expected clinical action:**

Arrange follow-up to resolve the pending therapeutic decision.

### Technical implementation

- **Changed field:** followup
- **Detectability location:** Follow-up appointments
- **Evidence required:** A pending therapeutic decision remains unresolved and requires scheduled follow-up.
- **Rationale:** Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-213

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 81
- **Sex/gender:** Female
- **Weight:** 63.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 81-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 81-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea. Home medications include furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 81-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea. Medications continued from home: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1743 mL and output was 1291 mL (net 452 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 143/79 | mmHg |
| admission: Heart rate | 87 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.7 | {INR} |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 530.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.4 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 4 MG/ML Oral Solution | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 1 MG/ML Oral Suspension | 1 tablet | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

No intentional assessment problem (clean control)

**CliniProof identifier:**

`none`

**Medication(s) involved:**

No trigger medication is specified because this is a clean control.

**What should have occurred clinically:**

No planted medication-reconciliation discrepancy or transition-of-care gap.

**What appears in the case:**

The resident-visible chart is the clean expected state.

**Where the relevant evidence appears:**

Review the full chart; there is no concealed target.

**Expected clinical action:**

NO INTENTIONAL ERROR

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-214

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 88
- **Sex/gender:** Male
- **Weight:** 89.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 88-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 88-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Chronic fatigue syndrome. Home medications include apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 88-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Chronic fatigue syndrome. Medications continued from home: apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 2139 mL and output was 1397 mL (net 742 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 123/79 | mmHg |
| admission: Heart rate | 110 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.0 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
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

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 89.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Medication omitted at discharge

**CliniProof identifier:**

`f1_omission`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- apixaban 2.5 MG Oral Tablet (rxcui=1364435)

**What should have occurred clinically:**

A medication indicated at discharge was omitted from the discharge medication list.

Clean expected state: present

**What appears in the case:**

absent

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge medications

**Expected clinical action:**

Restore the omitted continued discharge medication.

### Technical implementation

- **Changed field:** presence
- **Detectability location:** Discharge medications
- **Evidence required:** Home/inpatient continuation of this medication with no stop rationale.
- **Rationale:** A medication indicated at discharge was omitted from the discharge medication list.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-215

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Female
- **Weight:** 72.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 82-year-old Female with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 82-year-old Female is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Chronic fatigue syndrome. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 82-year-old Female with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Chronic fatigue syndrome. Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 2197 mL and output was 1316 mL (net 881 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/95 | mmHg |
| admission: Heart rate | 87 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.1 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.0 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
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

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Required outpatient monitoring not arranged

**CliniProof identifier:**

`f2_monitoring_not_arranged`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- warfarin sodium 1 MG Oral Tablet (rxcui=855288; rule_code=WARFARIN_INR_MONITORING)

**What should have occurred clinically:**

A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.

Clean expected state: case monitoring ids: present; medication monitoring: Outpatient monitoring arranged.

**What appears in the case:**

case monitoring: none; medication monitoring: none

**Where the relevant evidence appears:**

Discharge medications, Laboratory results, Scheduled monitoring

**Expected clinical action:**

Arrange the required outpatient monitoring for the trigger medication.

### Technical implementation

- **Changed field:** monitoring
- **Detectability location:** Scheduled monitoring, discharge medications.monitoring
- **Evidence required:** Trigger medication remains; source-backed rule WARFARIN_INR_MONITORING requires 38875-1.
- **Rationale:** A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-216

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Male
- **Weight:** 110.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Paroxysmal atrial fibrillation
- **Disposition:** home
- **One-liner:** 64-year-old Male with Paroxysmal atrial fibrillation

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Chronic fatigue syndrome in the setting of Paroxysmal atrial fibrillation
- **Symptoms:** Dyspnea, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 64-year-old Male is admitted with Paroxysmal atrial fibrillation. Presenting symptoms include Dyspnea, Chronic fatigue syndrome. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 64-year-old Male with Paroxysmal atrial fibrillation. Symptoms: Dyspnea, Chronic fatigue syndrome. Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1213 mL and output was 1459 mL (net -246 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 138/93 | mmHg |
| admission: Heart rate | 77 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.6 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation |
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

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Dyspnea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 110.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

No intentional assessment problem (clean control)

**CliniProof identifier:**

`none`

**Medication(s) involved:**

No trigger medication is specified because this is a clean control.

**What should have occurred clinically:**

No planted medication-reconciliation discrepancy or transition-of-care gap.

**What appears in the case:**

The resident-visible chart is the clean expected state.

**Where the relevant evidence appears:**

Review the full chart; there is no concealed target.

**Expected clinical action:**

NO INTENTIONAL ERROR

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-217

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 53
- **Sex/gender:** Male
- **Weight:** 72.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 53-year-old Male with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 53-year-old Male is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome. Home medications include lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 53-year-old Male with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome. Medications continued from home: lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1969 mL and output was 849 mL (net 1120 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/96 | mmHg |
| admission: Heart rate | 99 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.2 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 134.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 2 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
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

## Intended assessment issue

**Clinical category:**

Unexplained dose discrepancy

**CliniProof identifier:**

`f1_dose_mismatch`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- amlodipine 5 MG Oral Tablet (rxcui=197361)

**What should have occurred clinically:**

The discharge dose differs from the intended medication plan without a documented clinical rationale.

Clean expected state: 5 MG

**What appears in the case:**

2 MG

**Where the relevant evidence appears:**

Home medications, Discharge medications

**Expected clinical action:**

Restore the correct continued discharge dose.

### Technical implementation

- **Changed field:** dose
- **Detectability location:** Discharge medications
- **Evidence required:** Intended dose on the home/inpatient medication plan.
- **Rationale:** The discharge dose differs from the intended medication plan without a documented clinical rationale.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-218

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 51
- **Sex/gender:** Male
- **Weight:** 109.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 51-year-old Male with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 51-year-old Male is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome. Home medications include lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 51-year-old Male with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome. Medications continued from home: lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1977 mL and output was 942 mL (net 1035 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 149/92 | mmHg |
| admission: Heart rate | 108 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.4 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.6 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 136.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Medication inappropriately added or continued

**CliniProof identifier:**

`f1_commission`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- ibuprofen 0.05 MG/MG Topical Gel (rxcui=141997)

**What should have occurred clinically:**

A medication was prescribed at discharge without a clinical indication or intended discharge role.

Clean expected state: absent

**What appears in the case:**

present

**Where the relevant evidence appears:**

Home medications, discharge instructions, Discharge medications

**Expected clinical action:**

Remove the unindicated medication from the discharge list.

### Technical implementation

- **Changed field:** presence
- **Detectability location:** Discharge medications
- **Evidence required:** Home medication was discontinued and should not appear at discharge.
- **Rationale:** A medication was prescribed at discharge without a clinical indication or intended discharge role.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-219

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 58
- **Sex/gender:** Female
- **Weight:** 106.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 58-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 58-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome. Home medications include amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. lisinopril 1 MG/ML Oral Solution, ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 58-year-old Female with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome. Medications continued from home: amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. lisinopril 1 MG/ML Oral Solution, ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1877 mL and output was 884 mL (net 993 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 154/76 | mmHg |
| admission: Heart rate | 76 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.1 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 138.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Held medication without a restart plan

**CliniProof identifier:**

`f2_held_med_no_restart_plan`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- lisinopril 1 MG/ML Oral Solution (rxcui=1806884)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding lisinopril 1 MG/ML Oral Solution: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; target or goal: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; Resume when systolic blood pressure remains above 100 mmHg for 24 hours.

**What appears in the case:**

instructions: none; target or goal: none

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge instructions

**Expected clinical action:**

Document when and under what criteria the held medication should be restarted.

### Technical implementation

- **Changed field:** restart_plan
- **Detectability location:** Discharge instructions, CaseMedication.target or goal
- **Evidence required:** The medication was held for a documented reason and needs a restart plan.
- **Rationale:** A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-220

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 52
- **Sex/gender:** Female
- **Weight:** 83.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Essential (primary) hypertension
- **Disposition:** home
- **One-liner:** 52-year-old Female with Essential (primary) hypertension

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Essential (primary) hypertension
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 52-year-old Female is admitted with Essential (primary) hypertension. Presenting symptoms include Chronic fatigue syndrome. Home medications include lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

### Admission note

Admission note for a 52-year-old Female with Essential (primary) hypertension. Symptoms: Chronic fatigue syndrome. Medications continued from home: lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 0.05 MG/MG Topical Gel was held on admission and is not intended for discharge continuation.

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

On hospital day 1, intake was 1688 mL and output was 811 mL (net 877 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 126/89 | mmHg |
| admission: Heart rate | 102 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 142.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| ibuprofen 0.05 MG/MG Topical Gel | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Essential (primary) hypertension |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Essential (primary) hypertension |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: ibuprofen 0.05 MG/MG Topical Gel was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

No intentional assessment problem (clean control)

**CliniProof identifier:**

`none`

**Medication(s) involved:**

No trigger medication is specified because this is a clean control.

**What should have occurred clinically:**

No planted medication-reconciliation discrepancy or transition-of-care gap.

**What appears in the case:**

The resident-visible chart is the clean expected state.

**Where the relevant evidence appears:**

Review the full chart; there is no concealed target.

**Expected clinical action:**

NO INTENTIONAL ERROR

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-221

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Female
- **Weight:** 95.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 77-year-old Female with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Polyuria, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 77-year-old Female is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Polyuria, Chronic fatigue syndrome. Home medications include lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.

### Admission note

Admission note for a 77-year-old Female with Type 2 diabetes mellitus with unspecified complications. Symptoms: Polyuria, Chronic fatigue syndrome. Medications continued from home: lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.

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

On hospital day 1, intake was 1814 mL and output was 1179 mL (net 635 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 132/83 | mmHg |
| admission: Heart rate | 103 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 138.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 12.9 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

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

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Medication omitted at discharge

**CliniProof identifier:**

`f1_omission`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- lisinopril 1 MG/ML Oral Solution (rxcui=1806884)

**What should have occurred clinically:**

A medication indicated at discharge was omitted from the discharge medication list.

Clean expected state: present

**What appears in the case:**

absent

**Where the relevant evidence appears:**

Home medications, Medications during hospitalization, Discharge medications

**Expected clinical action:**

Restore the omitted continued discharge medication.

### Technical implementation

- **Changed field:** presence
- **Detectability location:** Discharge medications
- **Evidence required:** Home/inpatient continuation of this medication with no stop rationale.
- **Rationale:** A medication indicated at discharge was omitted from the discharge medication list.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-222

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 53
- **Sex/gender:** Female
- **Weight:** 85.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 53-year-old Female with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Polyuria, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 53-year-old Female is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Polyuria, Chronic fatigue syndrome. Home medications include lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.

### Admission note

Admission note for a 53-year-old Female with Type 2 diabetes mellitus with unspecified complications. Symptoms: Polyuria, Chronic fatigue syndrome. Medications continued from home: lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.

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

On hospital day 1, intake was 1644 mL and output was 940 mL (net 704 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 140/68 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 174.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.3 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications; supply: 7 days |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications; supply: 30 days |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 14 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 85.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

Insufficient medication supply

**CliniProof identifier:**

`f2_insufficient_supply`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet (rxcui=1807888)

**What should have occurred clinically:**

The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.

Clean expected state: 30 days

**What appears in the case:**

7 days

**Where the relevant evidence appears:**

Follow-up appointments, discharge medications.quantity or days

**Expected clinical action:**

Increase days' supply so treatment continues through the planned follow-up.

### Technical implementation

- **Changed field:** quantity_or_days
- **Detectability location:** discharge medications.quantity or days
- **Evidence required:** Days' supply must cover the scheduled follow-up or treatment endpoint.
- **Rationale:** The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-223

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 60
- **Sex/gender:** Female
- **Weight:** 82.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Type 2 diabetes mellitus with unspecified complications
- **Disposition:** home
- **One-liner:** 60-year-old Female with Type 2 diabetes mellitus with unspecified complications

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Polyuria, Chronic fatigue syndrome in the setting of Type 2 diabetes mellitus with unspecified complications
- **Symptoms:** Polyuria, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 60-year-old Female is admitted with Type 2 diabetes mellitus with unspecified complications. Presenting symptoms include Polyuria, Chronic fatigue syndrome. Home medications include lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.

### Admission note

Admission note for a 60-year-old Female with Type 2 diabetes mellitus with unspecified complications. Symptoms: Polyuria, Chronic fatigue syndrome. Medications continued from home: lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.

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

On hospital day 1, intake was 1452 mL and output was 1089 mL (net 363 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 139/69 | mmHg |
| admission: Heart rate | 78 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 146.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 12.8 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |
| lisinopril 1 MG/ML Oral Solution | 1 MG/ML | oral | once daily | indication: Type 2 diabetes mellitus with unspecified complications |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 7 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Polyuria (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 82.000 kg

No imaging studies were specified in this case.

No consultations were specified in this case.

## About the case data

This is a synthetic case created for medication-reconciliation assessment. It is not an extract from an individual patient’s medical record.

Medication names, diagnoses, and laboratory tests are drawn from established clinical terminology sources so that the concepts can be cited. Patient-specific values such as age, vital signs, and numeric laboratory results, and the surrounding clinical scenario, are generated by the software.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. Those checks can detect technical inconsistencies, but they do not establish that the case is clinically realistic, educationally appropriate, or ready for use without clinician review.

## Intended assessment issue

**Clinical category:**

No intentional assessment problem (clean control)

**CliniProof identifier:**

`none`

**Medication(s) involved:**

No trigger medication is specified because this is a clean control.

**What should have occurred clinically:**

No planted medication-reconciliation discrepancy or transition-of-care gap.

**What appears in the case:**

The resident-visible chart is the clean expected state.

**Where the relevant evidence appears:**

Review the full chart; there is no concealed target.

**Expected clinical action:**

NO INTENTIONAL ERROR

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________

---

# VAL-224

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 55
- **Sex/gender:** Male
- **Weight:** 101.000 kg
- **Clinical setting/specialty:** pulmonology
- **Admission diagnosis:** Lobar pneumonia, unspecified organism
- **Disposition:** home
- **One-liner:** 55-year-old Male with Lobar pneumonia, unspecified organism

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Cough, Dyspnea, Wheezing in the setting of Lobar pneumonia, unspecified organism
- **Symptoms:** Cough, Dyspnea, Wheezing
- **Symptom duration:** several days
- **Symptom course:** worsening
- **History of present illness:** A 55-year-old Male is admitted with Lobar pneumonia, unspecified organism. Presenting symptoms include Cough, Dyspnea, Wheezing. Home medications include albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet.

### Admission note

Admission note for a 55-year-old Male with Lobar pneumonia, unspecified organism. Symptoms: Cough, Dyspnea, Wheezing. Medications continued from home: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet.

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

On hospital day 1, intake was 2029 mL and output was 888 mL (net 1141 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 124/78 | mmHg |
| admission: Heart rate | 76 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 13.0 | g/dL |
| Sodium [Moles/volume] in Serum or Plasma (admission) | 138.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Lobar pneumonia, unspecified organism |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 1 tablet | oral | once daily | indication: Lobar pneumonia, unspecified organism |
| azithromycin 250 MG Oral Capsule | 1 tablet | oral | twice daily | indication: Lobar pneumonia, unspecified organism |
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

- Primary care follow-up (timing: 7 days; with service: primary care)

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

## Intended assessment issue

**Clinical category:**

Unexplained frequency discrepancy

**CliniProof identifier:**

`f1_frequency_mismatch`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- azithromycin 250 MG Oral Capsule (rxcui=141962)

**What should have occurred clinically:**

The discharge frequency differs from the intended medication plan without a documented clinical rationale.

Clean expected state: once daily

**What appears in the case:**

twice daily

**Where the relevant evidence appears:**

Home medications, Discharge medications

**Expected clinical action:**

Restore the correct continued discharge frequency.

### Technical implementation

- **Changed field:** frequency
- **Detectability location:** Discharge medications
- **Evidence required:** Intended frequency on the home/inpatient medication plan.
- **Rationale:** The discharge frequency differs from the intended medication plan without a documented clinical rationale.

### C1 Clinical plausibility

Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Rate each domain independently. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

| Domain | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Presentation and demographics | ☐ | ☐ | ☐ | ☐ |
| Fit between presentation and diagnosis | ☐ | ☐ | ☐ | ☐ |
| Vital signs | ☐ | ☐ | ☐ | ☐ |
| Laboratory findings | ☐ | ☐ | ☐ | ☐ |
| Medication regimen | ☐ | ☐ | ☐ | ☐ |
| Hospital course | ☐ | ☐ | ☐ | ☐ |
| Consistency across the chart | ☐ | ☐ | ☐ | ☐ |
| Discharge plan and follow-up | ☐ | ☐ | ☐ | ☐ |

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

☐ Yes

☐ No

Written explanation for any domain rated 1 or 2:

____________________________________

### C2 Intended assessment problem

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess? Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case. C2 is a hard requirement: if it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C3 Detectability

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case? Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. C3 is a hard requirement. A written explanation is required for a failure.

☐ Pass

☐ Fail

Written explanation if Fail:

### C4 Absence of unintended problems

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem? After reviewing the complete case, actively search for another discrepancy that a reasonable resident could interpret as an assessment target. Do not merely record problems that happen to be noticed. C4 is a hard requirement.

☐ Pass

☐ Fail

If Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful:

### C5 Expected learner difficulty

How difficult would this case likely be for an internal medicine resident? This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance. C5 is advisory and should not by itself cause a case to fail validation.

☐ Easy

☐ Moderate

☐ Hard

☐ Inappropriate / outlier

Comments:

## Reviewer recommendation

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

Recommended revisions are required whenever Revise is selected. Comments are recommendations for the study team. Do not modify the frozen case files from this form.

### Recommended revisions, if any

____________________________________
