# CliniProof clinician validation packet

## Purpose

The cases are synthetically generated clinical cases produced by CliniProof and are being reviewed for clinical validity. Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass.

The frozen set is `CLINIPROOF_SEEDCASES_V3`, containing 24 cases labeled VAL-801 through VAL-824. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. That sentence means the software has already checked structure, terminology, and a limited set of implemented rules, but a clinician has not yet accepted the case for educational use.

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

# VAL-801

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 75
- **Sex/gender:** Male
- **Weight:** 81.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 75-year-old Male with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion, Fatigue in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion, Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 75-year-old Male is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, Fatigue, present for several days and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. ibuprofen 400 MG Oral Tablet was discontinued and is not intended at discharge. Admitted for delirium with an initially incomplete medication history. The patient could not supply a reliable medication history at admission. A collateral home-medication list arrived later and was verified. Unknown names are not treated as discharge orders. Ibuprofen is documented as intentionally discontinued, not as an unknown item. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

### Admission note

Admission note for a 75-year-old Male with Delirium due to known physiological condition. Symptoms: Confusion, Fatigue for several days (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. ibuprofen 400 MG Oral Tablet was discontinued and is not intended at discharge. Admitted for delirium with an initially incomplete medication history. The patient could not supply a reliable medication history at admission. A collateral home-medication list arrived later and was verified. Unknown names are not treated as discharge orders. Ibuprofen is documented as intentionally discontinued, not as an unknown item. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

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

A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 136/78 | mmHg |
| admission: Heart rate | 85 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.1 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 163.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 121/71 | mmHg |
| discharge: Heart rate | 65 | beats/min |
| discharge: Respiratory rate | 20 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 103.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ibuprofen 400 MG Oral Tablet | 400 MG | oral | every 8 hours as needed | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ibuprofen 400 MG Oral Tablet | 400 MG | oral | every 8 hours as needed | held; held reason: Held on admission; not continued at discharge.; indication: symptomatic analgesia; not a treatment for the admission diagnosis |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

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

- Do not restart at discharge: ibuprofen 400 MG Oral Tablet was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Confusion (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 81.000 kg

Consultations:

- geriatrics (timepoint: inpatient; assessment: Delirium improved toward baseline.; recommendation: Use the verified collateral medication list at discharge.)

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

# VAL-802

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 81
- **Sex/gender:** Female
- **Weight:** 83.000 kg
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
- **History of present illness:** A 81-year-old Female is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, present for two days and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for delirium; a verified statin was confirmed from collateral sources. A later collateral list confirmed a continued statin. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

### Admission note

Admission note for a 81-year-old Female with Delirium due to known physiological condition. Symptoms: Confusion for two days (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for delirium; a verified statin was confirmed from collateral sources. A later collateral list confirmed a continued statin. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

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

A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 138/69 | mmHg |
| admission: Heart rate | 75 | beats/min |
| admission: Respiratory rate | 15 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.3 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 124/68 | mmHg |
| discharge: Heart rate | 74 | beats/min |
| discharge: Respiratory rate | 20 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 83.000 kg

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

- atorvastatin 40 MG Oral Tablet (rxcui=617311)

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

# VAL-803

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 97.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 71-year-old Male with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Fatigue, Confusion
- **Symptom duration:** one week
- **Symptom course:** persistent
- **History of present illness:** A 71-year-old Male is admitted with Delirium due to known physiological condition. Presenting symptoms include Fatigue, Confusion, present for one week and persistent. Home medications include hydrochlorothiazide 25 MG Oral Tablet, lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted for delirium with a later-verified home regimen and home-health needs. Discharge planning includes home services. The verified list is the collateral regimen, including a diuretic identified after admission. The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

### Admission note

Admission note for a 71-year-old Male with Delirium due to known physiological condition. Symptoms: Fatigue, Confusion for one week (persistent). Medications continued from home: hydrochlorothiazide 25 MG Oral Tablet, lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted for delirium with a later-verified home regimen and home-health needs. Discharge planning includes home services. The verified list is the collateral regimen, including a diuretic identified after admission. The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

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

The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/69 | mmHg |
| admission: Heart rate | 91 | beats/min |
| admission: Respiratory rate | 15 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.0 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 149.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.4 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 123/70 | mmHg |
| discharge: Heart rate | 67 | beats/min |
| discharge: Respiratory rate | 20 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 129.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.2 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| hydrochlorothiazide 25 MG Oral Tablet | 25 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| hydrochlorothiazide 25 MG Oral Tablet | 25 MG | oral | once daily | indication: Essential (primary) hypertension |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia; supply: 30 days |
| hydrochlorothiazide 25 MG Oral Tablet | 25 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 7 days |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications; supply: 30 days |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 97.000 kg

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

- lisinopril 10 MG Oral Tablet (rxcui=314076)

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

# VAL-804

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 70
- **Sex/gender:** Female
- **Weight:** 89.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 70-year-old Female with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 70-year-old Female is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, present for one day and improving after treatment. Home medications include atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted for resolving delirium; a pending outpatient cognitive-therapy decision was recorded. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented separately from unknown home medications. A new disease-modifying start was deferred to outpatient confirmation.

### Admission note

Admission note for a 70-year-old Female with Delirium due to known physiological condition. Symptoms: Confusion for one day (improving after treatment). Medications continued from home: atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted for resolving delirium; a pending outpatient cognitive-therapy decision was recorded. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented separately from unknown home medications. A new disease-modifying start was deferred to outpatient confirmation.

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

A new disease-modifying start was deferred to outpatient confirmation.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 130/79 | mmHg |
| admission: Heart rate | 75 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 155.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 125/67 | mmHg |
| discharge: Heart rate | 78 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 108.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 89.000 kg

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

- Not specified

**What should have occurred clinically:**

Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.

Clean expected state: item: Reassess pending therapeutic decision; timing: 14 days; with service: neurology

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

# VAL-805

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 68
- **Sex/gender:** Female
- **Weight:** 81.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 68-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Edema, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Edema, Orthopnea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 68-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Edema, Orthopnea, present for one week and improving after treatment. Home medications include furosemide 40 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. Admitted for acute heart-failure decompensation with congestion. Congestion improved with inpatient diuresis. Daily weights and intake/output were used to judge euvolemia before discharge. Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

### Admission note

Admission note for a 68-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Edema, Orthopnea for one week (improving after treatment). Medications continued from home: furosemide 40 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. Admitted for acute heart-failure decompensation with congestion. Congestion improved with inpatient diuresis. Daily weights and intake/output were used to judge euvolemia before discharge. Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

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

Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

On hospital day 3, intake was 1418 mL and output was 2463 mL (net -1045 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 109/82 | mmHg |
| admission: Heart rate | 93 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.7 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 1120.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.7 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 110/84 | mmHg |
| discharge: Heart rate | 69 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 369.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.3 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 81.000 kg
- discharge: 78.000 kg (dry weight 73.000 kg)

Imaging:

- Chest radiograph (timepoint: admission; body site: chest; finding: Pulmonary edema without pneumonia.)

Consultations:

- cardiology (timepoint: inpatient; assessment: Inpatient cardiology recommendations were recorded.; recommendation: Continue the intended heart-failure and diuretic plan.)

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

# VAL-806

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Female
- **Weight:** 78.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 82-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Edema in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Edema
- **Symptom duration:** several days
- **Symptom course:** progressive
- **History of present illness:** A 82-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Edema, present for several days and progressive. Home medications include furosemide 40 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. lisinopril 10 MG Oral Tablet was held during the admission (Held for rising creatinine during decongestion; intended to restart after renal recovery.). Admitted for decompensated heart failure with worsening renal function. Creatinine rose with congestion. Lisinopril was held during decongestion because of worsening renal function. Creatinine rose with congestion. Selected therapy was held.

### Admission note

Admission note for a 82-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Edema for several days (progressive). Medications continued from home: furosemide 40 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. lisinopril 10 MG Oral Tablet was held during the admission (Held for rising creatinine during decongestion; intended to restart after renal recovery.). Admitted for decompensated heart failure with worsening renal function. Creatinine rose with congestion. Lisinopril was held during decongestion because of worsening renal function. Creatinine rose with congestion. Selected therapy was held.

Creatinine rose with congestion. Selected therapy was held.

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

Creatinine rose with congestion. Selected therapy was held.

On hospital day 4, intake was 1307 mL and output was 2064 mL (net -757 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 124/72 | mmHg |
| admission: Heart rate | 107 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 89.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.8 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 116/72 | mmHg |
| discharge: Heart rate | 67 | beats/min |
| discharge: Respiratory rate | 14 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.6 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.5 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | held; held reason: Held for rising creatinine during decongestion; intended to restart after renal recovery.; indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | held; held reason: Held for rising creatinine during decongestion; intended to restart after renal recovery.; indication: Essential (primary) hypertension |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 78.000 kg
- discharge: 73.000 kg (dry weight 74.000 kg)

Imaging:

- Chest radiograph (timepoint: admission; body site: chest; finding: Congestion with small pleural effusions.)

Consultations:

- cardiology (timepoint: inpatient; assessment: Inpatient cardiology recommendations were recorded.; recommendation: Continue the intended heart-failure and diuretic plan.)

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

- lisinopril 10 MG Oral Tablet (rxcui=314076)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding lisinopril 10 MG Oral Tablet: Resume lisinopril when creatinine is falling toward the prior baseline.; target or goal: Resume lisinopril when creatinine is falling toward the prior baseline.; Resume lisinopril when creatinine is falling toward the prior baseline.

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

# VAL-807

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 60
- **Sex/gender:** Male
- **Weight:** 99.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 60-year-old Male with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Orthopnea
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 60-year-old Male is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Orthopnea, present for two days and acutely worsening. Home medications include furosemide 40 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. Admitted for decompensated heart failure with hypokalemia during diuresis. Diuresis was accompanied by potassium repletion. The intended outpatient diuretic dose is recorded. Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

### Admission note

Admission note for a 60-year-old Male with Acute systolic (congestive) heart failure. Symptoms: Dyspnea, Orthopnea for two days (acutely worsening). Medications continued from home: furosemide 40 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. Admitted for decompensated heart failure with hypokalemia during diuresis. Diuresis was accompanied by potassium repletion. The intended outpatient diuretic dose is recorded. Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

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

Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

On hospital day 3, intake was 1325 mL and output was 2417 mL (net -1092 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/70 | mmHg |
| admission: Heart rate | 102 | beats/min |
| admission: Respiratory rate | 26 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.2 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 836.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.5 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 137/77 | mmHg |
| discharge: Heart rate | 62 | beats/min |
| discharge: Respiratory rate | 15 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (discharge) | 585.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.8 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| furosemide 40 MG Oral Tablet | 20 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 99.000 kg
- discharge: 93.000 kg (dry weight 95.000 kg)

Imaging:

- Chest radiograph (timepoint: admission; body site: chest; finding: Pulmonary vascular congestion and interstitial edema.)
- Chest radiograph (timepoint: discharge; body site: chest; finding: Improved pulmonary edema compared with admission.)

Consultations:

- cardiology (timepoint: inpatient; assessment: Inpatient cardiology recommendations were recorded.; recommendation: Continue the intended heart-failure and diuretic plan.)

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

- furosemide 40 MG Oral Tablet (rxcui=313988)

**What should have occurred clinically:**

The discharge dose differs from the intended medication plan without a documented clinical rationale.

Clean expected state: 40 MG

**What appears in the case:**

20 MG

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

# VAL-808

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 66
- **Sex/gender:** Female
- **Weight:** 94.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Acute systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 66-year-old Female with Acute systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Edema, Orthopnea in the setting of Acute systolic (congestive) heart failure
- **Symptoms:** Edema, Orthopnea
- **Symptom duration:** one week
- **Symptom course:** worsening
- **History of present illness:** A 66-year-old Female is admitted with Acute systolic (congestive) heart failure. Presenting symptoms include Edema, Orthopnea, present for one week and worsening. Home medications include spironolactone 25 MG Oral Tablet, furosemide 40 MG Oral Tablet, lisinopril 10 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. Admitted for decompensated heart failure requiring diuretic adjustment. The outpatient diuretic plan was reviewed during the stay. The discharge list is the intended home regimen after that adjustment. The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

### Admission note

Admission note for a 66-year-old Female with Acute systolic (congestive) heart failure. Symptoms: Edema, Orthopnea for one week (worsening). Medications continued from home: spironolactone 25 MG Oral Tablet, furosemide 40 MG Oral Tablet, lisinopril 10 MG Oral Tablet, 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet. Admitted for decompensated heart failure requiring diuretic adjustment. The outpatient diuretic plan was reviewed during the stay. The discharge list is the intended home regimen after that adjustment. The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

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

The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

On hospital day 4, intake was 1569 mL and output was 2248 mL (net -679 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 139/82 | mmHg |
| admission: Heart rate | 70 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.9 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.4 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 142/64 | mmHg |
| discharge: Heart rate | 84 | beats/min |
| discharge: Respiratory rate | 15 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.7 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| spironolactone 25 MG Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure; note: Extended-release succinate taken once daily. |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| spironolactone 25 MG Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 6.25 MG | oral | twice daily | indication: Acute systolic (congestive) heart failure; note: Immediate-release carvedilol taken twice daily. |
| furosemide 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| spironolactone 25 MG Oral Tablet | 25 MG | oral | once daily | indication: Acute systolic (congestive) heart failure |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 94.000 kg
- discharge: 92.000 kg (dry weight 86.000 kg)

Imaging:

- Chest radiograph (timepoint: admission; body site: chest; finding: Residual mild congestion.)

Consultations:

- cardiology (timepoint: inpatient; assessment: Inpatient cardiology recommendations were recorded.; recommendation: Continue the intended heart-failure and diuretic plan.)

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

- 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet (role=source; rxcui=866427)
- carvedilol 6.25 MG Oral Tablet (role=substitute; rxcui=200031)

**What should have occurred clinically:**

A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.

Clean expected state: dose: 25 MG; drug: 24 HR metoprolol succinate 25 MG Extended Release Oral Tablet; frequency: once daily; monitoring: none; quantity or days: none; route: oral; rxcui: 866427; status: discharge

**What appears in the case:**

dose: 6.25 MG; drug: carvedilol 6.25 MG Oral Tablet; frequency: twice daily; monitoring: none; quantity or days: none; route: oral; rxcui: 200031; status: discharge

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

# VAL-809

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Male
- **Weight:** 70.000 kg
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
- **History of present illness:** A 82-year-old Male is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Fatigue, present for one week and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis and discharged on planned outpatient parenteral antimicrobial therapy. The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring. A seven-day supply was arranged to cover therapy until infectious-disease follow-up. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

### Admission note

Admission note for a 82-year-old Male with Acute and subacute infective endocarditis. Symptoms: Fatigue for one week (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis and discharged on planned outpatient parenteral antimicrobial therapy. The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring. A seven-day supply was arranged to cover therapy until infectious-disease follow-up. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

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

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/86 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.3 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 13.1 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 139/85 | mmHg |
| discharge: Heart rate | 80 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.8 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 12.9 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 70.000 kg

Imaging:

- Transthoracic echocardiogram (timepoint: inpatient; body site: heart; finding: Mobile echodensity consistent with a vegetation; ventricular function preserved.)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Complete the planned parenteral course with laboratory follow-up.)

Devices:

- PICC (site: right upper arm; status: in_place; care instructions: Line precautions and weekly dressing changes; removal plan: Remove after the planned parenteral course)

Microbiology:

- blood culture (timepoint: admission; specimen: blood; organism: gram-positive cocci; result: growth; status: final)
- blood culture (timepoint: inpatient; specimen: blood; result: no growth; status: final)

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

# VAL-810

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 83
- **Sex/gender:** Male
- **Weight:** 72.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 83-year-old Male with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea, Fatigue in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Nausea, Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 83-year-old Male is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Nausea, Fatigue, present for several days and improving after treatment. Home medications include atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis; remaining parenteral ceftriaxone is intended after discharge. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

### Admission note

Admission note for a 83-year-old Male with Acute and subacute infective endocarditis. Symptoms: Nausea, Fatigue for several days (improving after treatment). Medications continued from home: atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis; remaining parenteral ceftriaxone is intended after discharge. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

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

Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 125/82 | mmHg |
| admission: Heart rate | 106 | beats/min |
| admission: Respiratory rate | 26 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.3 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 176.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 137/81 | mmHg |
| discharge: Heart rate | 70 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 112.0 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 72.000 kg

Imaging:

- Transthoracic echocardiogram (timepoint: inpatient; body site: heart; finding: Mobile echodensity consistent with a vegetation; ventricular function preserved.)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Complete the planned parenteral course with laboratory follow-up.)

Devices:

- PICC (site: right upper arm; status: in_place; care instructions: Line precautions and weekly dressing changes; removal plan: Remove after the planned parenteral course)

Microbiology:

- blood culture (timepoint: admission; specimen: blood; organism: gram-positive cocci; result: growth; status: final)
- blood culture (timepoint: inpatient; specimen: blood; result: no growth; status: final)

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

- ceftriaxone 2000 MG Injection (rxcui=1665046)

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

# VAL-811

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 74
- **Sex/gender:** Male
- **Weight:** 87.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 74-year-old Male with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** persistent
- **History of present illness:** A 74-year-old Male is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Nausea, present for two days and persistent. Home medications include lisinopril 10 MG Oral Tablet, aspirin 81 MG Chewable Tablet, metformin hydrochloride 500 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis with a remaining outpatient parenteral course. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Infectious-disease follow-up is scheduled. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

### Admission note

Admission note for a 74-year-old Male with Acute and subacute infective endocarditis. Symptoms: Nausea for two days (persistent). Medications continued from home: lisinopril 10 MG Oral Tablet, aspirin 81 MG Chewable Tablet, metformin hydrochloride 500 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis with a remaining outpatient parenteral course. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Infectious-disease follow-up is scheduled. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

## Relevant medical history

**Past medical history:** Essential (primary) hypertension, Type 2 diabetes mellitus without complications, Atherosclerotic heart disease of native coronary artery without angina pectoris

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | admission | active | inpatient |
| Atherosclerotic heart disease of native coronary artery without angina pectoris | past_history | active | history |
| Essential (primary) hypertension | past_history | active | history |
| Type 2 diabetes mellitus without complications | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | diagnosis | high | active |
| Atherosclerotic heart disease of native coronary artery without angina pectoris | diagnosis | medium | active |
| Essential (primary) hypertension | diagnosis | medium | active |
| Type 2 diabetes mellitus without complications | diagnosis | medium | active |

## Hospital course

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 139/88 | mmHg |
| admission: Heart rate | 90 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.8 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 111.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 12.9 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 130/76 | mmHg |
| discharge: Heart rate | 67 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 137.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 12.4 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: Atherosclerotic heart disease of native coronary artery without angina pectoris |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: Atherosclerotic heart disease of native coronary artery without angina pectoris |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: Atherosclerotic heart disease of native coronary artery without angina pectoris; supply: 30 days |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; supply: 7 days; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications; supply: 30 days |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 87.000 kg

Imaging:

- Transthoracic echocardiogram (timepoint: inpatient; body site: heart; finding: Mobile echodensity consistent with a vegetation; ventricular function preserved.)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Complete the planned parenteral course with laboratory follow-up.)

Devices:

- PICC (site: right upper arm; status: in_place; care instructions: Line precautions and weekly dressing changes; removal plan: Remove after the planned parenteral course)

Microbiology:

- blood culture (timepoint: admission; specimen: blood; organism: gram-positive cocci; result: growth; status: final)
- blood culture (timepoint: inpatient; specimen: blood; result: no growth; status: final)

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

- ceftriaxone 2000 MG Injection (rxcui=1665046)

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

# VAL-812

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 75
- **Sex/gender:** Male
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Acute and subacute infective endocarditis
- **Disposition:** home
- **One-liner:** 75-year-old Male with Acute and subacute infective endocarditis

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Acute and subacute infective endocarditis
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 75-year-old Male is admitted with Acute and subacute infective endocarditis. Presenting symptoms include Fatigue, Nausea, present for one week and improving after treatment. Home medications include aspirin 81 MG Chewable Tablet, atorvastatin 40 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis; remaining parenteral duration is a pending outpatient decision. Duration of remaining parenteral ceftriaxone is to be confirmed at infectious-disease follow-up. Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

### Admission note

Admission note for a 75-year-old Male with Acute and subacute infective endocarditis. Symptoms: Fatigue, Nausea for one week (improving after treatment). Medications continued from home: aspirin 81 MG Chewable Tablet, atorvastatin 40 MG Oral Tablet. Started during this admission: ceftriaxone 2000 MG Injection. Admitted for endocarditis; remaining parenteral duration is a pending outpatient decision. Duration of remaining parenteral ceftriaxone is to be confirmed at infectious-disease follow-up. Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

## Relevant medical history

**Past medical history:** Mixed hyperlipidemia, Atherosclerotic heart disease of native coronary artery without angina pectoris

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | admission | active | inpatient |
| Atherosclerotic heart disease of native coronary artery without angina pectoris | past_history | active | history |
| Mixed hyperlipidemia | past_history | active | history |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Acute and subacute infective endocarditis | diagnosis | high | active |
| Atherosclerotic heart disease of native coronary artery without angina pectoris | diagnosis | medium | active |
| Mixed hyperlipidemia | diagnosis | medium | active |

## Hospital course

Cultures cleared on inpatient therapy. Remaining parenteral duration is to be confirmed as an outpatient decision.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 129/79 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 13.6 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 140/74 | mmHg |
| discharge: Heart rate | 74 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.9 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: Atherosclerotic heart disease of native coronary artery without angina pectoris |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: Atherosclerotic heart disease of native coronary artery without angina pectoris |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: Atherosclerotic heart disease of native coronary artery without angina pectoris |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| ceftriaxone 2000 MG Injection | 2000 MG | intravenous | once daily | indication: Acute and subacute infective endocarditis; note: Started during this admission for infective endocarditis and continued as intravenous outpatient therapy. |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 75.000 kg

Imaging:

- Transthoracic echocardiogram (timepoint: inpatient; body site: heart; finding: Mobile echodensity consistent with a vegetation; ventricular function preserved.)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Complete the planned parenteral course with laboratory follow-up.)

Devices:

- PICC (site: right upper arm; status: in_place; care instructions: Line precautions and weekly dressing changes; removal plan: Remove after the planned parenteral course)

Microbiology:

- blood culture (timepoint: admission; specimen: blood; organism: gram-positive cocci; result: growth; status: final)
- blood culture (timepoint: inpatient; specimen: blood; result: no growth; status: final)

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

- ceftriaxone 2000 MG Injection (rxcui=1665046)

**What should have occurred clinically:**

Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.

Clean expected state: item: Reassess pending therapeutic decision; timing: 14 days; with service: infectious disease

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

# VAL-813

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Female
- **Weight:** 68.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 64-year-old Female with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 64-year-old Female is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, present for several days and improving after treatment. Home medications include amlodipine 5 MG Oral Tablet, BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation. Gastrointestinal symptoms improved on antiviral therapy. Outpatient valganciclovir is the intended continuation. Kidney-transplant immunosuppression continues separately from CMV treatment. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

### Admission note

Admission note for a 64-year-old Female with Other cytomegaloviral diseases. Symptoms: Diarrhea for several days (improving after treatment). Medications continued from home: amlodipine 5 MG Oral Tablet, BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation. Gastrointestinal symptoms improved on antiviral therapy. Outpatient valganciclovir is the intended continuation. Kidney-transplant immunosuppression continues separately from CMV treatment. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

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

Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

On hospital day 5, intake was 1655 mL and output was 1812 mL (net -157 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 147/80 | mmHg |
| admission: Heart rate | 73 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.2 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.7 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 134/80 | mmHg |
| discharge: Heart rate | 84 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.0 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 3.9 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- tacrolimus trough and serum creatinine (frequency: as directed by the transplant service; responsible service: transplant)

The following items are follow-up appointments stored on the case.

- Transplant clinic follow-up after antiviral conversion (timing: 7 days; with service: transplant)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 68.000 kg
- discharge: 66.000 kg (dry weight 63.000 kg)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Continue antiviral therapy and infection-related monitoring as documented.)
- transplant (timepoint: inpatient; assessment: Transplant-service recommendations were recorded.; recommendation: Continue immunosuppression with infection-related adjustments as documented.)

Procedures:

- CMV viral-load review (time: admission; procedure type: diagnostic; findings: CMV viral burden was detected and supported antiviral treatment.)
- CMV viral-load review (time: inpatient; procedure type: diagnostic; findings: CMV viral burden was lower than the admission result.)

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

# VAL-814

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 90.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 71-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea, Nausea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea, Nausea
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 71-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, Nausea, present for one week and progressive. Home medications include amlodipine 5 MG Oral Tablet, BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet. mycophenolate mofetil 500 MG Oral Tablet was held during the admission (Held during active infection as an immunosuppression adjustment; intended to restart.). Admitted for cytomegalovirus disease after kidney transplantation with an infection-related mycophenolate hold. Mycophenolate was held during infection as an immunosuppression adjustment. Tacrolimus continues for transplant immunosuppression. Volume-related kidney injury led to temporary holds of selected immunosuppression.

### Admission note

Admission note for a 71-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea, Nausea for one week (progressive). Medications continued from home: amlodipine 5 MG Oral Tablet, BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet. mycophenolate mofetil 500 MG Oral Tablet was held during the admission (Held during active infection as an immunosuppression adjustment; intended to restart.). Admitted for cytomegalovirus disease after kidney transplantation with an infection-related mycophenolate hold. Mycophenolate was held during infection as an immunosuppression adjustment. Tacrolimus continues for transplant immunosuppression. Volume-related kidney injury led to temporary holds of selected immunosuppression.

Volume-related kidney injury led to temporary holds of selected immunosuppression.

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

Volume-related kidney injury led to temporary holds of selected immunosuppression.

On hospital day 4, intake was 1441 mL and output was 1515 mL (net -74 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 120/78 | mmHg |
| admission: Heart rate | 83 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 2.5 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 120/86 | mmHg |
| discharge: Heart rate | 78 | beats/min |
| discharge: Respiratory rate | 17 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.6 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| mycophenolate mofetil 500 MG Oral Tablet | 1000 MG | oral | twice daily | indication: Kidney transplant status |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| mycophenolate mofetil 500 MG Oral Tablet | 1000 MG | oral | twice daily | held; held reason: Held during active infection as an immunosuppression adjustment; intended to restart.; indication: Kidney transplant status |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| mycophenolate mofetil 500 MG Oral Tablet | 1000 MG | oral | twice daily | held; held reason: Held during active infection as an immunosuppression adjustment; intended to restart.; indication: Kidney transplant status |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- tacrolimus trough and serum creatinine (frequency: as directed by the transplant service; responsible service: transplant)

The following items are follow-up appointments stored on the case.

- Transplant follow-up to reassess held immunosuppression (timing: 5 days; with service: transplant)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 90.000 kg
- discharge: 84.000 kg (dry weight 85.000 kg)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Continue antiviral therapy and infection-related monitoring as documented.)
- transplant (timepoint: inpatient; assessment: Transplant-service recommendations were recorded.; recommendation: Continue immunosuppression with infection-related adjustments as documented.)

Procedures:

- CMV viral-load review (time: admission; procedure type: diagnostic; findings: CMV viral burden was detected and supported antiviral treatment.)
- CMV viral-load review (time: inpatient; procedure type: diagnostic; findings: CMV viral burden was lower than the admission result.)

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

- mycophenolate mofetil 500 MG Oral Tablet (rxcui=200060)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding mycophenolate mofetil 500 MG Oral Tablet: Resume mycophenolate when diarrhea has resolved and the transplant team confirms restart.; target or goal: Resume mycophenolate when diarrhea has resolved and the transplant team confirms restart.; Resume mycophenolate when diarrhea has resolved and the transplant team confirms restart.

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

# VAL-815

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 68
- **Sex/gender:** Female
- **Weight:** 74.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 68-year-old Female with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** intermittent
- **History of present illness:** A 68-year-old Female is admitted with Other cytomegaloviral diseases. Presenting symptoms include Nausea, present for two days and intermittent. Home medications include amlodipine 5 MG Oral Tablet, BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet, lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation with a tacrolimus dose adjustment. Tacrolimus was continued at the intended adjusted outpatient dose for transplant immunosuppression, not as treatment for CMV. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 68-year-old Female with Other cytomegaloviral diseases. Symptoms: Nausea for two days (intermittent). Medications continued from home: amlodipine 5 MG Oral Tablet, BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet, lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation with a tacrolimus dose adjustment. Tacrolimus was continued at the intended adjusted outpatient dose for transplant immunosuppression, not as treatment for CMV. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

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

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

On hospital day 3, intake was 1623 mL and output was 1966 mL (net -343 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 118/79 | mmHg |
| admission: Heart rate | 72 | beats/min |
| admission: Respiratory rate | 14 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.8 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.6 | mmol/L |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 138/80 | mmHg |
| discharge: Heart rate | 70 | beats/min |
| discharge: Respiratory rate | 14 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |
| Potassium [Moles/volume] in Serum or Plasma (discharge) | 4.5 | mmol/L |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 2 MG | oral | every 12 hours | indication: Kidney transplant status |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Essential (primary) hypertension |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- tacrolimus trough and serum creatinine (frequency: as directed by the transplant service; responsible service: transplant)

The following items are follow-up appointments stored on the case.

- Transplant medication-dose follow-up (timing: 7 days; with service: transplant)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 74.000 kg
- discharge: 68.000 kg (dry weight 70.000 kg)

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Continue antiviral therapy and infection-related monitoring as documented.)
- transplant (timepoint: inpatient; assessment: Transplant-service recommendations were recorded.; recommendation: Continue immunosuppression with infection-related adjustments as documented.)

Procedures:

- CMV viral-load review (time: admission; procedure type: diagnostic; findings: CMV viral burden was detected and supported antiviral treatment.)
- CMV viral-load review (time: inpatient; procedure type: diagnostic; findings: CMV viral burden was lower than the admission result.)

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

- BX Rating tacrolimus 1 MG Oral Capsule (rxcui=2665162)

**What should have occurred clinically:**

The discharge dose differs from the intended medication plan without a documented clinical rationale.

Clean expected state: 1 MG

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

# VAL-816

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 57
- **Sex/gender:** Male
- **Weight:** 102.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 57-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea, Fatigue in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea, Fatigue
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 57-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, Fatigue, present for one day and improving after treatment. Home medications include BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation; antiviral duration remains pending. Antiviral duration after conversion remains a pending outpatient decision. Tacrolimus continues for immunosuppression. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

### Admission note

Admission note for a 57-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea, Fatigue for one day (improving after treatment). Medications continued from home: BX Rating tacrolimus 1 MG Oral Capsule, valganciclovir 450 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. Admitted for cytomegalovirus disease after kidney transplantation; antiviral duration remains pending. Antiviral duration after conversion remains a pending outpatient decision. Tacrolimus continues for immunosuppression. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

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

Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 147/81 | mmHg |
| admission: Heart rate | 73 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.0 | mg/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 125/70 | mmHg |
| discharge: Heart rate | 76 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 0.9 | mg/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| BX Rating tacrolimus 1 MG Oral Capsule | 1 MG | oral | every 12 hours | indication: Kidney transplant status; note: Charted maintenance for an adult already taking therapy. The dose is individualized to the trough and is not the labeled weight-based starting dose. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| valganciclovir 450 MG Oral Tablet | 900 MG | oral | twice daily | indication: Other cytomegaloviral diseases; note: CMV treatment dose of 900 MG twice daily with preserved renal function, given as 450 MG tablets. This is not prophylaxis. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- tacrolimus trough and serum creatinine (frequency: as directed by the transplant service; responsible service: transplant)

The following items are follow-up appointments stored on the case.

No follow-up appointments were specified.

## Discharge instructions

- A pending therapeutic decision remains. Remaining duration of valganciclovir is to be confirmed at infectious-disease follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 102.000 kg

Consultations:

- infectious disease (timepoint: inpatient; assessment: Infectious-disease recommendations were recorded.; recommendation: Confirm remaining antiviral duration as an outpatient decision.)
- transplant (timepoint: inpatient; assessment: Transplant-service recommendations were recorded.; recommendation: Continue immunosuppression with infection-related adjustments as documented.)

Procedures:

- CMV viral-load review (time: admission; procedure type: diagnostic; findings: CMV viral burden was detected and supported antiviral treatment.)
- CMV viral-load review (time: inpatient; procedure type: diagnostic; findings: CMV viral burden was lower than the admission result.)

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

- valganciclovir 450 MG Oral Tablet (rxcui=313566)

**What should have occurred clinically:**

Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.

Clean expected state: item: Reassess pending therapeutic decision; timing: 14 days; with service: infectious disease

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

# VAL-817

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 87
- **Sex/gender:** Male
- **Weight:** 90.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 87-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 87-year-old Male is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Fatigue, present for several days and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted after operative repair of a femoral-neck fracture with planned warfarin resumption. Warfarin was interrupted for surgery and then resumed. The inpatient enoxaparin injection stops at discharge in this profile. Anticoagulation was interrupted for surgery and then resumed.

### Admission note

Admission note for a 87-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Fatigue for several days (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted after operative repair of a femoral-neck fracture with planned warfarin resumption. Warfarin was interrupted for surgery and then resumed. The inpatient enoxaparin injection stops at discharge in this profile. Anticoagulation was interrupted for surgery and then resumed.

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

Anticoagulation was interrupted for surgery and then resumed.

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 123/72 | mmHg |
| admission: Heart rate | 85 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 127.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 9.0 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.6 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 136/73 | mmHg |
| discharge: Heart rate | 71 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 98.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 113.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 10.1 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.6 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 90.000 kg

Consultations:

- orthopedics (timepoint: inpatient; assessment: Orthopedic postoperative recommendations were recorded.; recommendation: Protective weight bearing and rehabilitation as documented.)

Procedures:

- Open reduction and internal fixation of femoral neck fracture (time: inpatient; procedure type: operative; findings: Fracture reduced and internally fixed.)

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

- warfarin sodium 5 MG Oral Tablet (rxcui=855332; rule_code=WARFARIN_INR_MONITORING)

**What should have occurred clinically:**

A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.

Clean expected state: case monitoring ids: present; medication monitoring: INR laboratory monitoring is separate from the clinic appointment.

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

# VAL-818

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 79
- **Sex/gender:** Male
- **Weight:** 103.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 79-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea, Fatigue in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Nausea, Fatigue
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 79-year-old Male is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Nausea, Fatigue, present for one day and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted after hip-fracture surgery; anticoagulation is intended at discharge. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

### Admission note

Admission note for a 79-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Nausea, Fatigue for one day (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted after hip-fracture surgery; anticoagulation is intended at discharge. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

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

Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 120/81 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 15 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 7.9 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.3 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 124/74 | mmHg |
| discharge: Heart rate | 76 | beats/min |
| discharge: Respiratory rate | 15 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 10.3 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.9 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: within 7 days, then by the INR result; trigger for action: Repeat INR sooner if bleeding or a new interacting medicine occurs; responsible service: laboratory monitoring)

The following items are follow-up appointments stored on the case.

- Orthopedic and anticoagulation follow-up (timing: 14 days; with service: orthopedics)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 103.000 kg

Consultations:

- orthopedics (timepoint: inpatient; assessment: Orthopedic postoperative recommendations were recorded.; recommendation: Protective weight bearing and rehabilitation as documented.)

Procedures:

- Open reduction and internal fixation of femoral neck fracture (time: inpatient; procedure type: operative; findings: Fracture reduced and internally fixed.)

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

- warfarin sodium 5 MG Oral Tablet (rxcui=855332)

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

# VAL-819

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 70
- **Sex/gender:** Female
- **Weight:** 100.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 70-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** persistent
- **History of present illness:** A 70-year-old Female is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Nausea, present for two days and persistent. Home medications include lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet. Admitted after hip-fracture surgery with planned anticoagulation follow-up. Warfarin was resumed. An anticoagulation-clinic INR visit is scheduled. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed.

### Admission note

Admission note for a 70-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Nausea for two days (persistent). Medications continued from home: lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet. Admitted after hip-fracture surgery with planned anticoagulation follow-up. Warfarin was resumed. An anticoagulation-clinic INR visit is scheduled. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed.

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

Anticoagulation was interrupted for surgery and then resumed.

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 133/84 | mmHg |
| admission: Heart rate | 71 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.9 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.5 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 127/81 | mmHg |
| discharge: Heart rate | 88 | beats/min |
| discharge: Respiratory rate | 18 | breaths/min |
| discharge: SpO2 | 97.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.1 | mg/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.6 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension; supply: 30 days |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: INR laboratory monitoring is separate from the clinic appointment.; supply: 7 days; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: within 7 days, then by the INR result; trigger for action: Repeat INR sooner if bleeding or a new interacting medicine occurs; responsible service: laboratory monitoring)

The following items are follow-up appointments stored on the case.

- Anticoagulation supply and INR follow-up (timing: 14 days; with service: anticoagulation clinic)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Nausea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 100.000 kg

Consultations:

- orthopedics (timepoint: inpatient; assessment: Orthopedic postoperative recommendations were recorded.; recommendation: Protective weight bearing and rehabilitation as documented.)

Procedures:

- Open reduction and internal fixation of femoral neck fracture (time: inpatient; procedure type: operative; findings: Fracture reduced and internally fixed.)

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

- warfarin sodium 5 MG Oral Tablet (rxcui=855332)

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

# VAL-820

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Female
- **Weight:** 98.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** rehab
- **One-liner:** 82-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 82-year-old Female is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Fatigue, Nausea, present for one week and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Used only in the hospital and stopped at discharge: 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe. Admitted after hip-fracture surgery with inpatient bridging anticoagulation only. Enoxaparin was used as inpatient bridging and is not intended to continue once warfarin is resumed. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

### Admission note

Admission note for a 82-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Fatigue, Nausea for one week (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, warfarin sodium 5 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Used only in the hospital and stopped at discharge: 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe. Admitted after hip-fracture surgery with inpatient bridging anticoagulation only. Enoxaparin was used as inpatient bridging and is not intended to continue once warfarin is resumed. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

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

Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

The planned disposition is rehab. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 138/72 | mmHg |
| admission: Heart rate | 83 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 124.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.3 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.2 | {INR} |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 114/77 | mmHg |
| discharge: Heart rate | 74 | beats/min |
| discharge: Respiratory rate | 16 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 119.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 11.1 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (discharge) | 2.0 | {INR} |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe | 40 MG | subcutaneous | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe.; note: Hospital-only prophylaxis: 40 MG from the 0.4 mL syringe (100 MG/mL), subcutaneous once daily, stopped at discharge. |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe | 40 MG | subcutaneous | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe.; note: Hospital-only prophylaxis: 40 MG from the 0.4 mL syringe (100 MG/mL), subcutaneous once daily, stopped at discharge. |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| warfarin sodium 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Paroxysmal atrial fibrillation; monitoring: INR laboratory monitoring is separate from the clinic appointment.; note: Charted maintenance dose for this course. The dose is adjusted to the INR and is not a universal dose. |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

- INR in Platelet poor plasma or blood by Coagulation assay (frequency: within 7 days, then by the INR result; trigger for action: Repeat INR sooner if bleeding or a new interacting medicine occurs; responsible service: laboratory monitoring)

The following items are follow-up appointments stored on the case.

- Orthopedic rehabilitation follow-up (timing: 10 days; with service: orthopedics)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 98.000 kg

Consultations:

- orthopedics (timepoint: inpatient; assessment: Orthopedic postoperative recommendations were recorded.; recommendation: Protective weight bearing and rehabilitation as documented.)

Procedures:

- Open reduction and internal fixation of femoral neck fracture (time: inpatient; procedure type: operative; findings: Fracture reduced and internally fixed.)

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

- 0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe (rxcui=854235)

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

# VAL-821

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 78
- **Sex/gender:** Female
- **Weight:** 83.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 78-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 78-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, present for two days and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. apixaban 5 MG Oral Tablet was held during the admission (Held for gastrointestinal bleeding; intended to restart after hemoglobin stability.). Admitted for gastrointestinal bleeding with held anticoagulation. Bleeding settled and hemoglobin was stable. Apixaban was held. The patient is discharge-ready. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held.

### Admission note

Admission note for a 78-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue for two days (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet. apixaban 5 MG Oral Tablet was held during the admission (Held for gastrointestinal bleeding; intended to restart after hemoglobin stability.). Admitted for gastrointestinal bleeding with held anticoagulation. Bleeding settled and hemoglobin was stable. Apixaban was held. The patient is discharge-ready. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held.

Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held.

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

Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 138/70 | mmHg |
| admission: Heart rate | 69 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 0.9 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.7 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 140/79 | mmHg |
| discharge: Heart rate | 88 | beats/min |
| discharge: Respiratory rate | 19 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 10.9 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 5 MG Oral Tablet | 5 MG | oral | twice daily | indication: Paroxysmal atrial fibrillation |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 5 MG Oral Tablet | 5 MG | oral | twice daily | held; held reason: Held for gastrointestinal bleeding; intended to restart after hemoglobin stability.; indication: Paroxysmal atrial fibrillation |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 5 MG Oral Tablet | 5 MG | oral | twice daily | held; held reason: Held for gastrointestinal bleeding; intended to restart after hemoglobin stability.; indication: Paroxysmal atrial fibrillation |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 83.000 kg

Consultations:

- gastroenterology (timepoint: inpatient; assessment: Gastroenterology recommendations were recorded.; recommendation: Hold anticoagulation while hemoglobin remains stable, then reassess.)

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

- apixaban 5 MG Oral Tablet (rxcui=1364445)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding apixaban 5 MG Oral Tablet: Resume apixaban if hemoglobin remains stable for 48 hours and bleeding has not recurred.; target or goal: Resume apixaban if hemoglobin remains stable for 48 hours and bleeding has not recurred.; Resume apixaban if hemoglobin remains stable for 48 hours and bleeding has not recurred.

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

# VAL-822

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 79
- **Sex/gender:** Female
- **Weight:** 100.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 79-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 79-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, Nausea, present for one day and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Used only in the hospital and stopped at discharge: pantoprazole 40 MG Delayed Release Oral Tablet. Admitted for gastrointestinal bleeding treated with inpatient acid suppression. Inpatient acid suppression was used for the bleed and is not intended to continue at discharge unless later prescribed. Gastrointestinal bleeding was observed with serial hemoglobin checks. Inpatient acid suppression was used while the patient stabilized for discharge.

### Admission note

Admission note for a 79-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue, Nausea for one day (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Used only in the hospital and stopped at discharge: pantoprazole 40 MG Delayed Release Oral Tablet. Admitted for gastrointestinal bleeding treated with inpatient acid suppression. Inpatient acid suppression was used for the bleed and is not intended to continue at discharge unless later prescribed. Gastrointestinal bleeding was observed with serial hemoglobin checks. Inpatient acid suppression was used while the patient stabilized for discharge.

Gastrointestinal bleeding was observed with serial hemoglobin checks. Inpatient acid suppression was used while the patient stabilized for discharge.

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

Gastrointestinal bleeding was observed with serial hemoglobin checks. Inpatient acid suppression was used while the patient stabilized for discharge.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 144/71 | mmHg |
| admission: Heart rate | 83 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 153.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 8.5 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 128/78 | mmHg |
| discharge: Heart rate | 73 | beats/min |
| discharge: Respiratory rate | 15 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 126.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 10.7 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| pantoprazole 40 MG Delayed Release Oral Tablet | 40 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 40 MG Delayed Release Oral Tablet. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |
| pantoprazole 40 MG Delayed Release Oral Tablet | 40 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 40 MG Delayed Release Oral Tablet. |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 100.000 kg

Consultations:

- gastroenterology (timepoint: inpatient; assessment: Gastroenterology recommendations were recorded.; recommendation: Continue inpatient acid suppression and observe serial hemoglobin until stability.)

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

- pantoprazole 40 MG Delayed Release Oral Tablet (rxcui=314200)

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

# VAL-823

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 109.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 71-year-old Male with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 71-year-old Male is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, present for several days and persistent. Home medications include apixaban 5 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted for gastrointestinal bleeding with a pending anticoagulation decision. Restart versus continued hold of anticoagulation is a pending outpatient decision. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

### Admission note

Admission note for a 71-year-old Male with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue for several days (persistent). Medications continued from home: apixaban 5 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. Admitted for gastrointestinal bleeding with a pending anticoagulation decision. Restart versus continued hold of anticoagulation is a pending outpatient decision. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

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

Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/72 | mmHg |
| admission: Heart rate | 68 | beats/min |
| admission: Respiratory rate | 14 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (admission) | 1.1 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (admission) | 116.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 9.0 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 127/70 | mmHg |
| discharge: Heart rate | 76 | beats/min |
| discharge: Respiratory rate | 14 | breaths/min |
| discharge: SpO2 | 96.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Mass/volume] in Serum or Plasma (discharge) | 1.2 | mg/dL |
| Fasting glucose [Mass/volume] in Serum or Plasma (discharge) | 104.0 | mg/dL |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 10.2 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 5 MG Oral Tablet | 5 MG | oral | twice daily | indication: Paroxysmal atrial fibrillation; note: Standard labeled dose for nonvalvular atrial fibrillation. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 5 MG Oral Tablet | 5 MG | oral | twice daily | indication: Paroxysmal atrial fibrillation; note: Standard labeled dose for nonvalvular atrial fibrillation. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 5 MG Oral Tablet | 5 MG | oral | twice daily | indication: Paroxysmal atrial fibrillation; note: Standard labeled dose for nonvalvular atrial fibrillation. |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

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

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 109.000 kg

Consultations:

- gastroenterology (timepoint: inpatient; assessment: Gastroenterology recommendations were recorded.; recommendation: Hold anticoagulation while hemoglobin remains stable, then reassess.)

Procedures:

- Upper endoscopy (time: inpatient; procedure type: endoscopic; findings: Bleeding source evaluated; no ongoing active bleeding at discharge planning.)

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

- apixaban 5 MG Oral Tablet (rxcui=1364445)

**What should have occurred clinically:**

Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.

Clean expected state: item: Reassess pending therapeutic decision; timing: 7 days; with service: cardiology

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

# VAL-824

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Female
- **Weight:** 97.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 77-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Fatigue, Nausea in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Fatigue, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 77-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Fatigue, Nausea, present for one week and improving after treatment. Home medications include lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. aspirin 81 MG Chewable Tablet was discontinued and is not intended at discharge. Admitted for gastrointestinal bleeding with intentional aspirin discontinuation. Aspirin used for primary prevention was intentionally stopped after the bleed. That discontinuation is documented and is distinct from an omitted intended medication. Gastrointestinal bleeding settled and hemoglobin was stable. Aspirin used for primary prevention was stopped.

### Admission note

Admission note for a 77-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Fatigue, Nausea for one week (improving after treatment). Medications continued from home: lisinopril 10 MG Oral Tablet, atorvastatin 40 MG Oral Tablet, metformin hydrochloride 500 MG Oral Tablet. aspirin 81 MG Chewable Tablet was discontinued and is not intended at discharge. Admitted for gastrointestinal bleeding with intentional aspirin discontinuation. Aspirin used for primary prevention was intentionally stopped after the bleed. That discontinuation is documented and is distinct from an omitted intended medication. Gastrointestinal bleeding settled and hemoglobin was stable. Aspirin used for primary prevention was stopped.

Gastrointestinal bleeding settled and hemoglobin was stable. Aspirin used for primary prevention was stopped.

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

Gastrointestinal bleeding settled and hemoglobin was stable. Aspirin used for primary prevention was stopped.

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Admission status

### Vital signs

The following table lists admission vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 147/87 | mmHg |
| admission: Heart rate | 77 | beats/min |
| admission: Respiratory rate | 16 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists admission laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 7.8 | g/dL |

## Discharge / most recent status

The following table lists discharge or most-recent vital signs stored on the case.

| Measure | Value | Unit |
| --- | ---: | ---: |
| discharge: Temperature | 36.80 | °C |
| discharge: Blood pressure | 130/74 | mmHg |
| discharge: Heart rate | 75 | beats/min |
| discharge: Respiratory rate | 14 | breaths/min |
| discharge: SpO2 | 95.00 | % |

The following table lists discharge or most-recent laboratory tests stored on the case.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (discharge) | 9.3 | g/dL |

Discharge disposition and follow-up below should be read with the discharge-timepoint vitals and laboratories above.

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: antiplatelet therapy; not a treatment for the admission diagnosis |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: antiplatelet therapy; not a treatment for the admission diagnosis |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 81 MG Chewable Tablet | 81 MG | oral | once daily | indication: antiplatelet therapy; not a treatment for the admission diagnosis |
| atorvastatin 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Mixed hyperlipidemia |
| lisinopril 10 MG Oral Tablet | 10 MG | oral | once daily | indication: Essential (primary) hypertension |
| metformin hydrochloride 500 MG Oral Tablet | 500 MG | oral | twice daily | indication: Type 2 diabetes mellitus without complications |

## Medication reconciliation

- **Best possible medication history source:** patient and prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Primary care follow-up (timing: 10 days; with service: primary care)

## Discharge instructions

- Do not restart at discharge: aspirin 81 MG Chewable Tablet was discontinued and has no outpatient role. (category: medications)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Fatigue (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Baseline living situation: lives at home
- **Language preference:** English

Serial weights:

- admission: 97.000 kg

Consultations:

- gastroenterology (timepoint: inpatient; assessment: Gastroenterology recommendations were recorded.; recommendation: Hold anticoagulation while hemoglobin remains stable, then reassess.)

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

- aspirin 81 MG Chewable Tablet (rxcui=318272)

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
