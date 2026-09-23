# CliniProof clinician validation packet

## Purpose

The cases are synthetically generated clinical cases produced by CliniProof and are being reviewed for clinical validity. Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass.

The frozen set is `CLINIPROOF_SEEDCASES_V1`, containing twenty-four cases labeled VAL-401 through VAL-424. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. That sentence means the software has already checked structure, terminology, and a limited set of implemented rules, but a clinician has not yet accepted the case for educational use.

## Reviewer task

For each case:

1. Read the complete case.
2. Assess C1–C5 using the forms that follow the case.
3. Record ratings in [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv).
4. Add comments where a problem is identified.

Do not split these ratings across separate review stages. Complete all five criteria during this one review.

C1 asks whether the chart could reasonably represent a patient in the stated inpatient setting. C2 asks whether the intended medication-reconciliation or transition-of-care problem is actually present. C3 asks whether an internal medicine resident could detect and resolve that problem from the case documents. C4 asks whether another unintended clinically meaningful problem is also present. C5 is an expert estimate of expected learner difficulty.

This packet includes the intended assessment issue for each case so that C2 through C5 can be completed in the same pass as C1. Full criterion definitions are in [`validation_rubric.md`](validation_rubric.md).

These charts were generated from expert/resident-authored clinical archetypes and remain synthetic. The specific source archetype is not shown to blinded resident participants.

---

# VAL-401

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 72
- **Sex/gender:** Male
- **Weight:** 89.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 72-year-old Male with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion, Chronic fatigue syndrome in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 72-year-old Male is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, Chronic fatigue syndrome, present for several days and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. The patient could not supply a reliable medication history at admission. A collateral home-medication list arrived later and was verified. Unknown names are not treated as discharge orders. Ibuprofen is documented as intentionally discontinued, not as an unknown item. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

### Admission note

Admission note for a 72-year-old Male with Delirium due to known physiological condition. Symptoms: Confusion, Chronic fatigue syndrome for several days (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. ibuprofen 300 MG Oral Tablet was held on admission and is not intended for discharge continuation. The patient could not supply a reliable medication history at admission. A collateral home-medication list arrived later and was verified. Unknown names are not treated as discharge orders. Ibuprofen is documented as intentionally discontinued, not as an unknown item. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1243 mL and output was 1443 mL (net -200 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 140/76 | mmHg |
| admission: Heart rate | 106 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 156.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| ibuprofen 300 MG Oral Tablet | 300 MG | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
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

- admission: 89.000 kg

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

# VAL-402

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 76
- **Sex/gender:** Male
- **Weight:** 102.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 76-year-old Male with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 76-year-old Male is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, present for two days and improving after treatment. Home medications include lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. A later collateral list confirmed a continued statin. Incomplete information at admission is not itself the planted error. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

### Admission note

Admission note for a 76-year-old Male with Delirium due to known physiological condition. Symptoms: Confusion for two days (improving after treatment). Medications continued from home: lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. A later collateral list confirmed a continued statin. Incomplete information at admission is not itself the planted error. A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

A collateral medication list was obtained after admission and verified. Unknown names were not converted into discharge orders. Intentionally discontinued therapy was documented separately from incomplete information.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1507 mL and output was 1485 mL (net 22 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 142/79 | mmHg |
| admission: Heart rate | 87 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
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

- admission: 102.000 kg

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

- atorvastatin 80 MG Oral Tablet (rxcui=259255)

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

# VAL-403

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 80
- **Sex/gender:** Male
- **Weight:** 63.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 80-year-old Male with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Chronic fatigue syndrome, Confusion
- **Symptom duration:** one week
- **Symptom course:** persistent
- **History of present illness:** A 80-year-old Male is admitted with Delirium due to known physiological condition. Presenting symptoms include Chronic fatigue syndrome, Confusion, present for one week and persistent. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Discharge planning includes home services. The clean list is the verified collateral regimen, including a diuretic identified after admission. The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

### Admission note

Admission note for a 80-year-old Male with Delirium due to known physiological condition. Symptoms: Chronic fatigue syndrome, Confusion for one week (persistent). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Discharge planning includes home services. The clean list is the verified collateral regimen, including a diuretic identified after admission. The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

The patient returned to cognitive baseline. Home services were arranged and the verified medication list was prepared for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |

## Hospital course

On hospital day 4, intake was 1965 mL and output was 1536 mL (net 429 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 127/69 | mmHg |
| admission: Heart rate | 99 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 91.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 165.0 | mmol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.6 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Delirium due to known physiological condition |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition; supply: 30 days |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition; supply: 30 days |
| hydrochlorothiazide 50 MG Oral Tablet | 50 MG | oral | once daily | indication: Delirium due to known physiological condition; supply: 7 days |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Delirium due to known physiological condition; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

- hydrochlorothiazide 50 MG Oral Tablet (rxcui=197770)

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

# VAL-404

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 84
- **Sex/gender:** Male
- **Weight:** 82.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Delirium due to known physiological condition
- **Disposition:** home
- **One-liner:** 84-year-old Male with Delirium due to known physiological condition

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Confusion in the setting of Delirium due to known physiological condition
- **Symptoms:** Confusion
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 84-year-old Male is admitted with Delirium due to known physiological condition. Presenting symptoms include Confusion, present for one day and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented on the clean case and is distinct from an unknown home medication. A new disease-modifying start was deferred to outpatient confirmation. That pending decision is recorded on the clean discharge plan.

### Admission note

Admission note for a 84-year-old Male with Delirium due to known physiological condition. Symptoms: Confusion for one day (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. A cognitive-enhancer start is deferred to outpatient confirmation. That pending decision is documented on the clean case and is distinct from an unknown home medication. A new disease-modifying start was deferred to outpatient confirmation. That pending decision is recorded on the clean discharge plan.

A new disease-modifying start was deferred to outpatient confirmation. That pending decision is recorded on the clean discharge plan.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Delirium due to known physiological condition | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 2016 mL and output was 1740 mL (net 276 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 133/80 | mmHg |
| admission: Heart rate | 97 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 174.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Delirium due to known physiological condition |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Delirium due to known physiological condition |

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

- Confusion (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

Follow-up missing for an unresolved treatment decision

**CliniProof identifier:**

`f2_pending_decision_followup_missing`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet (rxcui=1807888)

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

# VAL-405

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 63
- **Sex/gender:** Female
- **Weight:** 61.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 63-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca, Orthopnea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 63-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, Orthopnea, present for one week and improving after treatment. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Congestion improved with inpatient diuresis. Daily weights and intake/output were used to judge euvolemia before discharge. Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

### Admission note

Admission note for a 63-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca, Orthopnea for one week (improving after treatment). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Congestion improved with inpatient diuresis. Daily weights and intake/output were used to judge euvolemia before discharge. Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

Congestion was treated with inpatient diuresis. Serial weights and intake/output were used to judge readiness for discharge.

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

On hospital day 3, intake was 1718 mL and output was 1744 mL (net -26 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 125/82 | mmHg |
| admission: Heart rate | 111 | beats/min |
| admission: Respiratory rate | 26 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 786.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.6 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 61.000 kg

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

# VAL-406

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 82
- **Sex/gender:** Female
- **Weight:** 84.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 82-year-old Female with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Anasarca in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Anasarca
- **Symptom duration:** several days
- **Symptom course:** progressive
- **History of present illness:** A 82-year-old Female is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Anasarca, present for several days and progressive. Home medications include furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. metoprolol tartrate 37.5 MG Oral Tablet was held on admission and is not intended for discharge continuation. Creatinine rose with congestion. Selected disease-modifying therapy was held with an explicit plan to reassess restart, separate from any planted error. Creatinine rose with congestion. Selected therapy was held with a plan to reassess restart after renal recovery.

### Admission note

Admission note for a 82-year-old Female with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Anasarca for several days (progressive). Medications continued from home: furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. metoprolol tartrate 37.5 MG Oral Tablet was held on admission and is not intended for discharge continuation. Creatinine rose with congestion. Selected disease-modifying therapy was held with an explicit plan to reassess restart, separate from any planted error. Creatinine rose with congestion. Selected therapy was held with a plan to reassess restart after renal recovery.

Creatinine rose with congestion. Selected therapy was held with a plan to reassess restart after renal recovery.

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

On hospital day 4, intake was 1967 mL and output was 873 mL (net 1094 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 110/65 | mmHg |
| admission: Heart rate | 101 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.3 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.2 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 84.000 kg

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

- metoprolol tartrate 37.5 MG Oral Tablet (rxcui=1606347)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding metoprolol tartrate 37.5 MG Oral Tablet: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; target or goal: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; Resume when systolic blood pressure remains above 100 mmHg for 24 hours.

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

# VAL-407

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Male
- **Weight:** 96.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 77-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Dyspnea, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Dyspnea, Orthopnea
- **Symptom duration:** two days
- **Symptom course:** acutely worsening
- **History of present illness:** A 77-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Dyspnea, Orthopnea, present for two days and acutely worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Diuresis was complicated by hypokalemia requiring repletion. The clean discharge diuretic dose is the intended outpatient dose. Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

### Admission note

Admission note for a 77-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Dyspnea, Orthopnea for two days (acutely worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Diuresis was complicated by hypokalemia requiring repletion. The clean discharge diuretic dose is the intended outpatient dose. Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

Diuresis was accompanied by potassium repletion. Electrolytes were trending toward a range acceptable for discharge.

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

On hospital day 3, intake was 1543 mL and output was 1178 mL (net 365 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 124/64 | mmHg |
| admission: Heart rate | 118 | beats/min |
| admission: Respiratory rate | 20 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.4 | umol/L |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma (admission) | 183.0 | pg/mL |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.8 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 27.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 96.000 kg

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

- metoprolol tartrate 37.5 MG Oral Tablet (rxcui=1606347)

**What should have occurred clinically:**

The discharge dose differs from the intended medication plan without a documented clinical rationale.

Clean expected state: 37.5 MG

**What appears in the case:**

27.5 MG

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

# VAL-408

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 72
- **Sex/gender:** Male
- **Weight:** 67.000 kg
- **Clinical setting/specialty:** cardiology
- **Admission diagnosis:** Unspecified systolic (congestive) heart failure
- **Disposition:** home
- **One-liner:** 72-year-old Male with Unspecified systolic (congestive) heart failure

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure
- **Symptoms:** Anasarca, Orthopnea
- **Symptom duration:** one week
- **Symptom course:** worsening
- **History of present illness:** A 72-year-old Male is admitted with Unspecified systolic (congestive) heart failure. Presenting symptoms include Anasarca, Orthopnea, present for one week and worsening. Home medications include metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. The outpatient diuretic plan was reviewed during the stay. The clean list is the intended home regimen after that adjustment. The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

### Admission note

Admission note for a 72-year-old Male with Unspecified systolic (congestive) heart failure. Symptoms: Anasarca, Orthopnea for one week (worsening). Medications continued from home: metoprolol tartrate 37.5 MG Oral Tablet, furosemide 80 MG Oral Tablet, lisinopril 40 MG Oral Tablet, spironolactone 100 MG Oral Tablet. The outpatient diuretic plan was reviewed during the stay. The clean list is the intended home regimen after that adjustment. The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

The outpatient diuretic plan was adjusted during the stay after the inpatient response to therapy was observed.

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

On hospital day 4, intake was 1625 mL and output was 1336 mL (net 289 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 156/77 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 95.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.3 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 4.4 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| metoprolol tartrate 37.5 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| spironolactone 100 MG Oral Tablet | 100 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| carvedilol 6.25 MG Oral Tablet | 37.5 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
| furosemide 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Unspecified systolic (congestive) heart failure |
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

- Primary care volume follow-up after diuretic adjustment (timing: 7 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Anasarca (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

Social context:

- **Living situation:** Lives at home
- **Language preference:** English

Serial weights:

- admission: 67.000 kg

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

# VAL-409

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 81
- **Sex/gender:** Female
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Endocarditis, valve unspecified
- **Disposition:** home
- **One-liner:** 81-year-old Female with Endocarditis, valve unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Endocarditis, valve unspecified
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 81-year-old Female is admitted with Endocarditis, valve unspecified. Presenting symptoms include Chronic fatigue syndrome, present for one week and improving after treatment. Home medications include ceftriaxone 500 MG Injection, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring. Those transition tasks are part of the clean case. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

### Admission note

Admission note for a 81-year-old Female with Endocarditis, valve unspecified. Symptoms: Chronic fatigue syndrome for one week (improving after treatment). Medications continued from home: ceftriaxone 500 MG Injection, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring. Those transition tasks are part of the clean case. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | diagnosis | high | active |

## Hospital course

On hospital day 4, intake was 1216 mL and output was 1191 mL (net 25 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 133/85 | mmHg |
| admission: Heart rate | 72 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 13.8 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

The following items are follow-up appointments stored on the case.

- Infectious-disease follow-up with parenteral-therapy laboratory monitoring (timing: 14 days; with service: infectious disease)

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

# VAL-410

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 64
- **Sex/gender:** Male
- **Weight:** 81.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Endocarditis, valve unspecified
- **Disposition:** home
- **One-liner:** 64-year-old Male with Endocarditis, valve unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea, Chronic fatigue syndrome in the setting of Endocarditis, valve unspecified
- **Symptoms:** Nausea, Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 64-year-old Male is admitted with Endocarditis, valve unspecified. Presenting symptoms include Nausea, Chronic fatigue syndrome, present for several days and improving after treatment. Home medications include ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

### Admission note

Admission note for a 64-year-old Male with Endocarditis, valve unspecified. Symptoms: Nausea, Chronic fatigue syndrome for several days (improving after treatment). Medications continued from home: ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Parenteral ceftriaxone is intended to continue after discharge until the planned end date. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 2100 mL and output was 841 mL (net 1259 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 38.20 | °C |
| admission: Blood pressure | 115/81 | mmHg |
| admission: Heart rate | 95 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 0.9 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 170.0 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

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

- Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet (rxcui=1807888)

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

# VAL-411

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 70
- **Sex/gender:** Female
- **Weight:** 82.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Endocarditis, valve unspecified
- **Disposition:** home
- **One-liner:** 70-year-old Female with Endocarditis, valve unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Endocarditis, valve unspecified
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** persistent
- **History of present illness:** A 70-year-old Female is admitted with Endocarditis, valve unspecified. Presenting symptoms include Nausea, present for two days and persistent. Home medications include aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. The clean case documents enough supply to cover the remaining parenteral course until infectious-disease follow-up. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

### Admission note

Admission note for a 70-year-old Female with Endocarditis, valve unspecified. Symptoms: Nausea for two days (persistent). Medications continued from home: aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet. The clean case documents enough supply to cover the remaining parenteral course until infectious-disease follow-up. Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

Parenteral antimicrobial therapy was continued with a specified remaining duration, laboratory monitoring, and line precautions for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | diagnosis | high | active |

## Hospital course

On hospital day 5, intake was 1569 mL and output was 1603 mL (net -34 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 151/71 | mmHg |
| admission: Heart rate | 85 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 135.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.0 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Endocarditis, valve unspecified; supply: 30 days |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Endocarditis, valve unspecified; supply: 30 days |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified; supply: 7 days |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Endocarditis, valve unspecified; supply: 30 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
- **Reconciliation status:** complete
- **Patient able to participate:** Yes
- **Pharmacist review:** Yes

## Follow-up and monitoring

The following items are scheduled monitoring tasks stored on the case.

No scheduled monitoring was specified.

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

- admission: 82.000 kg

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

- ceftriaxone 500 MG Injection (rxcui=1665005)

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

# VAL-412

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 62
- **Sex/gender:** Male
- **Weight:** 106.000 kg
- **Clinical setting/specialty:** infectious disease
- **Admission diagnosis:** Endocarditis, valve unspecified
- **Disposition:** home
- **One-liner:** 62-year-old Male with Endocarditis, valve unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Nausea in the setting of Endocarditis, valve unspecified
- **Symptoms:** Chronic fatigue syndrome, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 62-year-old Male is admitted with Endocarditis, valve unspecified. Presenting symptoms include Chronic fatigue syndrome, Nausea, present for one week and improving after treatment. Home medications include aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, atorvastatin 80 MG Oral Tablet. Duration of remaining parenteral therapy is to be confirmed at infectious-disease follow-up. The clean case records that pending decision. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

### Admission note

Admission note for a 62-year-old Male with Endocarditis, valve unspecified. Symptoms: Chronic fatigue syndrome, Nausea for one week (improving after treatment). Medications continued from home: aspirin 75 MG Delayed Release Oral Tablet, ceftriaxone 500 MG Injection, atorvastatin 80 MG Oral Tablet. Duration of remaining parenteral therapy is to be confirmed at infectious-disease follow-up. The clean case records that pending decision. Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

Cultures cleared on inpatient therapy. The remaining parenteral course and infectious-disease follow-up were arranged before discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Endocarditis, valve unspecified | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 2166 mL and output was 1255 mL (net 911 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 135/76 | mmHg |
| admission: Heart rate | 84 | beats/min |
| admission: Respiratory rate | 24 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.8 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Endocarditis, valve unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Endocarditis, valve unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Endocarditis, valve unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Endocarditis, valve unspecified |
| ceftriaxone 500 MG Injection | 500 MG | oral | once daily | indication: Endocarditis, valve unspecified |

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

- Pending therapeutic decision: duration of aspirin 75 MG Delayed Release Oral Tablet remains uncertain and will be determined at the scheduled follow-up. (category: followup)
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

Follow-up missing for an unresolved treatment decision

**CliniProof identifier:**

`f2_pending_decision_followup_missing`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- aspirin 75 MG Delayed Release Oral Tablet (rxcui=103954)

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

# VAL-413

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 67
- **Sex/gender:** Male
- **Weight:** 101.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 67-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 67-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, present for several days and improving after treatment. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Gastrointestinal symptoms improved on antiviral therapy. Outpatient valganciclovir is the intended continuation. No unsupported transplant dosing rule is encoded. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent without encoding unsupported dosing rules.

### Admission note

Admission note for a 67-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea for several days (improving after treatment). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Gastrointestinal symptoms improved on antiviral therapy. Outpatient valganciclovir is the intended continuation. No unsupported transplant dosing rule is encoded. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent without encoding unsupported dosing rules.

Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent without encoding unsupported dosing rules.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |

## Hospital course

On hospital day 5, intake was 1825 mL and output was 1640 mL (net 185 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 139/82 | mmHg |
| admission: Heart rate | 88 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| Potassium [Moles/volume] in Serum or Plasma (admission) | 3.5 | mmol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 101.000 kg

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

# VAL-414

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 59
- **Sex/gender:** Male
- **Weight:** 63.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 59-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea, Nausea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea, Nausea
- **Symptom duration:** one week
- **Symptom course:** progressive
- **History of present illness:** A 59-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, Nausea, present for one week and progressive. Home medications include amlodipine 5 MG Oral Tablet, mycophenolate mofetil 250 MG Oral Capsule. 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule was held on admission and is not intended for discharge continuation. Mycophenolate was held during infection with a documented plan to reassess restart. That hold is a clinical decision on the clean case. Volume-related kidney injury led to temporary holds. Restart plans were documented separately from any planted reconciliation error.

### Admission note

Admission note for a 59-year-old Male with Other cytomegaloviral diseases. Symptoms: Diarrhea, Nausea for one week (progressive). Medications continued from home: amlodipine 5 MG Oral Tablet, mycophenolate mofetil 250 MG Oral Capsule. 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule was held on admission and is not intended for discharge continuation. Mycophenolate was held during infection with a documented plan to reassess restart. That hold is a clinical decision on the clean case. Volume-related kidney injury led to temporary holds. Restart plans were documented separately from any planted reconciliation error.

Volume-related kidney injury led to temporary holds. Restart plans were documented separately from any planted reconciliation error.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |

## Hospital course

On hospital day 4, intake was 1899 mL and output was 1084 mL (net 815 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 154/89 | mmHg |
| admission: Heart rate | 96 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.5 | umol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| mycophenolate mofetil 250 MG Oral Capsule | 250 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| mycophenolate mofetil 250 MG Oral Capsule | 250 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| mycophenolate mofetil 250 MG Oral Capsule | 250 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 63.000 kg

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

- 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule (rxcui=1431971)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; target or goal: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; Resume when systolic blood pressure remains above 100 mmHg for 24 hours.

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

# VAL-415

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 72
- **Sex/gender:** Male
- **Weight:** 92.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 72-year-old Male with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Other cytomegaloviral diseases
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** intermittent
- **History of present illness:** A 72-year-old Male is admitted with Other cytomegaloviral diseases. Presenting symptoms include Nausea, present for two days and intermittent. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Tacrolimus was continued at the intended adjusted outpatient dose. Numeric target ranges from the seed document are not encoded as software rules. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

### Admission note

Admission note for a 72-year-old Male with Other cytomegaloviral diseases. Symptoms: Nausea for two days (intermittent). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, amlodipine 5 MG Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Tacrolimus was continued at the intended adjusted outpatient dose. Numeric target ranges from the seed document are not encoded as software rules. Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

Home therapy was reviewed and adjusted during the stay. The discharge list reflects the intended outpatient regimen.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1544 mL and output was 1220 mL (net 324 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 139/72 | mmHg |
| admission: Heart rate | 105 | beats/min |
| admission: Respiratory rate | 18 | breaths/min |
| admission: SpO2 | 92.00 | % |

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
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| amlodipine 5 MG Oral Tablet | 5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 20 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- atorvastatin 80 MG Oral Tablet (rxcui=259255)

**What should have occurred clinically:**

The discharge dose differs from the intended medication plan without a documented clinical rationale.

Clean expected state: 80 MG

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

# VAL-416

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 65
- **Sex/gender:** Female
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** nephrology
- **Admission diagnosis:** Other cytomegaloviral diseases
- **Disposition:** home
- **One-liner:** 65-year-old Female with Other cytomegaloviral diseases

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Diarrhea, Chronic fatigue syndrome in the setting of Other cytomegaloviral diseases
- **Symptoms:** Diarrhea, Chronic fatigue syndrome
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 65-year-old Female is admitted with Other cytomegaloviral diseases. Presenting symptoms include Diarrhea, Chronic fatigue syndrome, present for one day and improving after treatment. Home medications include 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Antiviral duration after conversion remains a pending outpatient decision documented on the clean case. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent without encoding unsupported dosing rules.

### Admission note

Admission note for a 65-year-old Female with Other cytomegaloviral diseases. Symptoms: Diarrhea, Chronic fatigue syndrome for one day (improving after treatment). Medications continued from home: 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule, atorvastatin 80 MG Oral Tablet, valganciclovir 450 MG Oral Tablet. Antiviral duration after conversion remains a pending outpatient decision documented on the clean case. Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent without encoding unsupported dosing rules.

Infectious symptoms improved. Inpatient antiviral therapy was converted to the intended outpatient agent without encoding unsupported dosing rules.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Other cytomegaloviral diseases | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1399 mL and output was 1715 mL (net -316 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 154/76 | mmHg |
| admission: Heart rate | 95 | beats/min |
| admission: Respiratory rate | 23 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.2 | umol/L |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule | 0.5 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Other cytomegaloviral diseases |
| valganciclovir 450 MG Oral Tablet | 450 MG | oral | once daily | indication: Other cytomegaloviral diseases |

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

- Pending therapeutic decision: duration of 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule remains uncertain and will be determined at the scheduled follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Diarrhea (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Follow-up missing for an unresolved treatment decision

**CliniProof identifier:**

`f2_pending_decision_followup_missing`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- 24 HR tacrolimus 0.5 MG Extended Release Oral Capsule (rxcui=1431971)

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

# VAL-417

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 97.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** home
- **One-liner:** 71-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** improving after treatment
- **History of present illness:** A 71-year-old Male is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Chronic fatigue syndrome, present for several days and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Warfarin was interrupted for surgery and then resumed. The clean case arranges INR monitoring. Bridging injection is not continued at discharge in this profile. Anticoagulation was interrupted for surgery and then resumed. INR monitoring was arranged as part of the clean discharge plan.

### Admission note

Admission note for a 71-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Chronic fatigue syndrome for several days (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Warfarin was interrupted for surgery and then resumed. The clean case arranges INR monitoring. Bridging injection is not continued at discharge in this profile. Anticoagulation was interrupted for surgery and then resumed. INR monitoring was arranged as part of the clean discharge plan.

Anticoagulation was interrupted for surgery and then resumed. INR monitoring was arranged as part of the clean discharge plan.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1686 mL and output was 1103 mL (net 583 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 125/75 | mmHg |
| admission: Heart rate | 74 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 167.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.0 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 3.1 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

# VAL-418

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 86
- **Sex/gender:** Female
- **Weight:** 100.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** home
- **One-liner:** 86-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea, Chronic fatigue syndrome in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Nausea, Chronic fatigue syndrome
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 86-year-old Female is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Nausea, Chronic fatigue syndrome, present for one day and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

### Admission note

Admission note for a 86-year-old Female with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Nausea, Chronic fatigue syndrome for one day (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Postoperative hemoglobin was observed. Warfarin is intended to continue at discharge. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |

## Hospital course

On hospital day 4, intake was 1614 mL and output was 1007 mL (net 607 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 145/68 | mmHg |
| admission: Heart rate | 82 | beats/min |
| admission: Respiratory rate | 22 | breaths/min |
| admission: SpO2 | 96.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 14.2 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.6 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 100.000 kg

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

- warfarin sodium 1 MG Oral Tablet (rxcui=855288)

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

# VAL-419

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 77
- **Sex/gender:** Male
- **Weight:** 86.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** home
- **One-liner:** 77-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Nausea in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Nausea
- **Symptom duration:** two days
- **Symptom course:** persistent
- **History of present illness:** A 77-year-old Male is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Nausea, present for two days and persistent. Home medications include lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Discharge includes enough warfarin supply to reach the scheduled INR visit. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed. INR monitoring was arranged as part of the clean discharge plan.

### Admission note

Admission note for a 77-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Nausea for two days (persistent). Medications continued from home: lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Discharge includes enough warfarin supply to reach the scheduled INR visit. Home therapy support is arranged. Anticoagulation was interrupted for surgery and then resumed. INR monitoring was arranged as part of the clean discharge plan.

Anticoagulation was interrupted for surgery and then resumed. INR monitoring was arranged as part of the clean discharge plan.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 1398 mL and output was 1131 mL (net 267 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health ordered: Yes.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 145/69 | mmHg |
| admission: Heart rate | 109 | beats/min |
| admission: Respiratory rate | 17 | breaths/min |
| admission: SpO2 | 93.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.0 | umol/L |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 1.8 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; supply: 30 days |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged.; supply: 7 days |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

- admission: 86.000 kg

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

- warfarin sodium 1 MG Oral Tablet (rxcui=855288)

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

# VAL-420

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 71
- **Sex/gender:** Male
- **Weight:** 104.000 kg
- **Clinical setting/specialty:** orthopedics
- **Admission diagnosis:** Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Disposition:** home
- **One-liner:** 71-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Nausea in the setting of Fracture of unspecified part of neck of right femur, initial encounter for closed fracture
- **Symptoms:** Chronic fatigue syndrome, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 71-year-old Male is admitted with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Presenting symptoms include Chronic fatigue syndrome, Nausea, present for one week and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Enoxaparin was used as inpatient bridging and is not intended to continue once warfarin is resumed. The clean case stops that hospital-only anticoagulant. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

### Admission note

Admission note for a 71-year-old Male with Fracture of unspecified part of neck of right femur, initial encounter for closed fracture. Symptoms: Chronic fatigue syndrome, Nausea for one week (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. Enoxaparin was used as inpatient bridging and is not intended to continue once warfarin is resumed. The clean case stops that hospital-only anticoagulant. Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

Postoperative hemoglobin was observed without transfusion. Rehabilitation and anticoagulation follow-up were planned.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1209 mL and output was 1748 mL (net -539 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 143/73 | mmHg |
| admission: Heart rate | 83 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 92.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 176.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 14.3 | g/dL |
| INR in Platelet poor plasma or blood by Coagulation assay (admission) | 2.1 | {INR} |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe | 100 MG/ML | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe. |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe | 100 MG/ML | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe. |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture |
| warfarin sodium 1 MG Oral Tablet | 1 MG | oral | once daily | indication: Fracture of unspecified part of neck of right femur, initial encounter for closed fracture; monitoring: Outpatient monitoring arranged. |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

## Intended assessment issue

**Clinical category:**

Hospital-only medication continued after discharge

**CliniProof identifier:**

`f2_hospital_only_continued`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- 0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe (rxcui=854228)

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

# VAL-421

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 80
- **Sex/gender:** Male
- **Weight:** 83.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 80-year-old Male with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** two days
- **Symptom course:** improving after treatment
- **History of present illness:** A 80-year-old Male is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Chronic fatigue syndrome, present for two days and improving after treatment. Home medications include lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. apixaban 2.5 MG Oral Tablet was held on admission and is not intended for discharge continuation. Bleeding settled and hemoglobin was stable. Apixaban was held with a documented restart plan. The patient is discharge-ready. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

### Admission note

Admission note for a 80-year-old Male with Gastrointestinal hemorrhage, unspecified. Symptoms: Chronic fatigue syndrome for two days (improving after treatment). Medications continued from home: lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. apixaban 2.5 MG Oral Tablet was held on admission and is not intended for discharge continuation. Bleeding settled and hemoglobin was stable. Apixaban was held with a documented restart plan. The patient is discharge-ready. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 1764 mL and output was 1316 mL (net 448 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 119/72 | mmHg |
| admission: Heart rate | 107 | beats/min |
| admission: Respiratory rate | 19 | breaths/min |
| admission: SpO2 | 97.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.6 | umol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.4 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | held; held reason: Held inpatient for documented in-hospital hypotension; intended to restart.; indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

Held medication without a restart plan

**CliniProof identifier:**

`f2_held_med_no_restart_plan`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- apixaban 2.5 MG Oral Tablet (rxcui=1364435)

**What should have occurred clinically:**

A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.

Clean expected state: instructions: Resume when holding apixaban 2.5 MG Oral Tablet: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; target or goal: Resume when systolic blood pressure remains above 100 mmHg for 24 hours.; Resume when systolic blood pressure remains above 100 mmHg for 24 hours.

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

# VAL-422

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 84
- **Sex/gender:** Male
- **Weight:** 71.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 84-year-old Male with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Nausea in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Chronic fatigue syndrome, Nausea
- **Symptom duration:** one day
- **Symptom course:** improving after treatment
- **History of present illness:** A 84-year-old Male is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Chronic fatigue syndrome, Nausea, present for one day and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Inpatient acid suppression was used for the bleed. The clean case does not continue that hospital-only proton-pump inhibitor unless a clinician later decides it is needed. The patient was observed until vital signs and symptoms stabilized enough for discharge.

### Admission note

Admission note for a 84-year-old Male with Gastrointestinal hemorrhage, unspecified. Symptoms: Chronic fatigue syndrome, Nausea for one day (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. Inpatient acid suppression was used for the bleed. The clean case does not continue that hospital-only proton-pump inhibitor unless a clinician later decides it is needed. The patient was observed until vital signs and symptoms stabilized enough for discharge.

The patient was observed until vital signs and symptoms stabilized enough for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |

## Hospital course

On hospital day 2, intake was 2027 mL and output was 1354 mL (net 673 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 137/84 | mmHg |
| admission: Heart rate | 85 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 169.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.3 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| pantoprazole 20 MG Delayed Release Oral Tablet | 20 MG | oral | once daily | indication: Started in hospital for an inpatient-only indication; stop at discharge. No outpatient continuation of pantoprazole 20 MG Delayed Release Oral Tablet. |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
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

- Primary care follow-up after gastrointestinal bleed (timing: 5 days; with service: primary care)

## Discharge instructions

- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

# VAL-423

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 81
- **Sex/gender:** Male
- **Weight:** 99.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 81-year-old Male with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Chronic fatigue syndrome
- **Symptom duration:** several days
- **Symptom course:** persistent
- **History of present illness:** A 81-year-old Male is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Chronic fatigue syndrome, present for several days and persistent. Home medications include apixaban 2.5 MG Oral Tablet, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Restart versus continued hold of anticoagulation is a pending outpatient decision. The clean case records that follow-up. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

### Admission note

Admission note for a 81-year-old Male with Gastrointestinal hemorrhage, unspecified. Symptoms: Chronic fatigue syndrome for several days (persistent). Medications continued from home: apixaban 2.5 MG Oral Tablet, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet. Restart versus continued hold of anticoagulation is a pending outpatient decision. The clean case records that follow-up. The patient is discharge-ready, not in shock. Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

Restart versus continued hold of anticoagulation remains a pending outpatient decision. The patient is otherwise ready for discharge.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |

## Hospital course

On hospital day 3, intake was 2090 mL and output was 1094 mL (net 996 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 143/85 | mmHg |
| admission: Heart rate | 89 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 94.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Creatinine [Moles/volume] in Serum or Plasma (admission) | 1.4 | umol/L |
| Glucose [Moles/volume] in Serum or Plasma (admission) | 157.0 | mmol/L |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.3 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| apixaban 2.5 MG Oral Tablet | 2.5 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

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

- Pending therapeutic decision: duration of apixaban 2.5 MG Oral Tablet remains uncertain and will be determined at the scheduled follow-up. (category: followup)
- Take discharge medications exactly as listed. (category: medications)

## Other relevant clinical information

The following items are return precautions stored on the case.

- Chronic fatigue syndrome (reason: Worsening of the presenting symptom; action: Seek urgent evaluation; severity: urgent)

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

## Intended assessment issue

**Clinical category:**

Follow-up missing for an unresolved treatment decision

**CliniProof identifier:**

`f2_pending_decision_followup_missing`

**Family:** Family 2 — transition-of-care gap (`family_2`)

**Medication(s) involved:**

- apixaban 2.5 MG Oral Tablet (rxcui=1364435)

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

# VAL-424

## Patient overview

The following overview lists the demographic and admission facts stored for this synthetic patient.

- **Age:** 75
- **Sex/gender:** Female
- **Weight:** 75.000 kg
- **Clinical setting/specialty:** general medicine
- **Admission diagnosis:** Gastrointestinal hemorrhage, unspecified
- **Disposition:** home
- **One-liner:** 75-year-old Female with Gastrointestinal hemorrhage, unspecified

## Reason for hospitalization

The following fields are the presenting complaint and history stored on the case.

- **Chief complaint:** Chronic fatigue syndrome, Nausea in the setting of Gastrointestinal hemorrhage, unspecified
- **Symptoms:** Chronic fatigue syndrome, Nausea
- **Symptom duration:** one week
- **Symptom course:** improving after treatment
- **History of present illness:** A 75-year-old Female is admitted with Gastrointestinal hemorrhage, unspecified. Presenting symptoms include Chronic fatigue syndrome, Nausea, present for one week and improving after treatment. Home medications include Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. aspirin 75 MG Delayed Release Oral Tablet was held on admission and is not intended for discharge continuation. Aspirin used for primary prevention was intentionally stopped after the bleed. That discontinuation is not an unknown medication and is not the same as a planted list error. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

### Admission note

Admission note for a 75-year-old Female with Gastrointestinal hemorrhage, unspecified. Symptoms: Chronic fatigue syndrome, Nausea for one week (improving after treatment). Medications continued from home: Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, lisinopril 40 MG Oral Tablet, atorvastatin 80 MG Oral Tablet. aspirin 75 MG Delayed Release Oral Tablet was held on admission and is not intended for discharge continuation. Aspirin used for primary prevention was intentionally stopped after the bleed. That discontinuation is not an unknown medication and is not the same as a planted list error. Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

Gastrointestinal bleeding settled and hemoglobin was stable. Anticoagulation was held with a documented restart plan in a discharge-ready patient.

## Relevant medical history

No additional past medical history or allergy fields were specified.

The following table lists diagnoses stored on the case.

| Diagnosis | Type | Status | Context |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | admission | active | inpatient |

The following table lists problem-list entries stored on the case.

| Problem | Type | Priority | Status |
| --- | --- | --- | --- |
| Gastrointestinal hemorrhage, unspecified | diagnosis | high | active |

## Hospital course

On hospital day 4, intake was 1666 mL and output was 1178 mL (net 488 mL).

The planned disposition is home. Discharge readiness is recorded as ready. Home health was not ordered.

## Clinical status at discharge

### Vital signs

The following table lists vital signs stored on the case. These numbers are synthetic patient-specific values, not measurements from a real record.

| Measure | Value | Unit |
| --- | ---: | ---: |
| admission: Temperature | 36.80 | °C |
| admission: Blood pressure | 122/79 | mmHg |
| admission: Heart rate | 79 | beats/min |
| admission: Respiratory rate | 21 | breaths/min |
| admission: SpO2 | 98.00 | % |

### Laboratory results

The following table lists laboratory tests stored on the case. The test identity comes from LOINC. The numeric result is synthetic.

| Test | Result | Unit |
| --- | ---: | ---: |
| Hemoglobin [Mass/volume] in Blood by Oximetry (admission) | 11.1 | g/dL |

## Home medications

The following table lists medications recorded as the home regimen.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Medications during hospitalization

The following table lists medications recorded as active during the hospital stay.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | held; held reason: Held on admission; not continued at discharge.; indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Discharge medications

The following table lists medications recorded on the discharge list.

| Medication | Dose | Route | Frequency | Relevant note |
| --- | --- | --- | --- | --- |
| Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | 1000 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| aspirin 75 MG Delayed Release Oral Tablet | 1 tablet | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| atorvastatin 80 MG Oral Tablet | 80 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |
| lisinopril 40 MG Oral Tablet | 40 MG | oral | once daily | indication: Gastrointestinal hemorrhage, unspecified |

## Medication reconciliation

- **Best possible medication history source:** prior records
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

## Intended assessment issue

**Clinical category:**

Medication inappropriately added or continued

**CliniProof identifier:**

`f1_commission`

**Family:** Family 1 — medication-list / transition discrepancy (`family_1`)

**Medication(s) involved:**

- aspirin 75 MG Delayed Release Oral Tablet (rxcui=103954)

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
