# Clinician walkthrough

CliniProof cases are synthetic inpatient charts built to support medication-reconciliation and transition-of-care assessment. This walkthrough uses a teaching case to show how the chart is assembled and how clinicians should read it.

> The examples on this page are educational demonstrations only. They are not part of either prospective validation set.

## Current case sets

- [Balanced structured case set](../../data/case_sets/balanced/README.md) (CLINIPROOF_BALANCED_V4, VAL-701–VAL-724)
- [Resident-seed-guided case set](../../data/case_sets/seed_guided/README.md) (CLINIPROOF_SEEDCASES_V3, VAL-801–VAL-824)

Those two overviews are the charts under review. The heart-failure chart below is a separate teaching example, identified as TEACH-001 and TEACH-002.

## 1. What a CliniProof case looks like

### How a CliniProof case is structured

Every chart follows the same order. The headings below are the headings on the readable case.

```text
Patient overview
        ↓
Reason for hospitalization
        ↓
Relevant medical history
        ↓
Hospital course
        ↓
Admission status
        ↓
Discharge / most recent status
        ↓
Home medications
        ↓
Medications during hospitalization
        ↓
Discharge medications
        ↓
Medication reconciliation
        ↓
Follow-up and monitoring
        ↓
Discharge instructions
        ↓
Other relevant clinical information
```

| Section | What it contributes |
| --- | --- |
| Patient overview | Age, sex, weight, service, admission diagnosis, and disposition |
| Reason for hospitalization | Chief complaint, symptoms, duration, course, and the history of the present illness |
| Relevant medical history | Conditions already present that shape the regimen |
| Hospital course | What happened during the stay and whether the patient improved |
| Admission status | Vital signs and laboratory results at arrival |
| Discharge / most recent status | The same measures at the time of transition |
| Home medications | The regimen in use before admission |
| Medications during hospitalization | What was continued, started, held, substituted, or limited to the stay |
| Discharge medications | The outpatient list presented for review |
| Medication reconciliation | History source, patient participation, and pharmacist review |
| Follow-up and monitoring | Appointments and laboratory tasks that sit beside the medication list |
| Discharge instructions | What the patient is told to do with the regimen |
| Other relevant clinical information | Imaging, consultations, procedures, weights, and return precautions |

## 2. Walk through one clean case

The complete clean chart is [Heart failure (TEACH-001)](examples/clean_heart_failure_case.md). It uses the same sections as the study cases. No assessment problem was introduced.

TEACH-001 is a 77-year-old man admitted to cardiology with acute systolic heart failure and discharged home. Weight on admission is 92 kg.

### Presentation

The chart records dyspnea, edema, and orthopnea for several days, worsening. The history states that he was admitted for decompensated heart failure with volume overload. Past history is hypertension and mixed hyperlipidemia. Those diagnoses are why the home regimen contains both heart-failure therapy and an antihypertensive.

### Clinical trajectory

Admission and discharge findings are paired so a reader can see the course.

| | Admission | Discharge |
| --- | --- | --- |
| Heart rate | 96 beats/min | 79 beats/min |
| SpO2 | 94% | 98% |
| Creatinine | 1.1 mg/dL | 0.9 mg/dL |
| BNP | 963 pg/mL | 241 pg/mL |
| Potassium | 4.6 mmol/L | 3.6 mmol/L |
| Weight | 92 kg | 87 kg |

On hospital day 3, intake was 1566 mL and output was 2109 mL. The course describes diuresis over several days, with congestion improved enough for discharge. Discharge readiness is recorded as ready, and the disposition is home. A chest radiograph at admission shows pulmonary edema without focal consolidation. Inpatient cardiology consultation is recorded.

### Medication history

The home regimen is three oral medications, each once daily:

| Medication | Dose | Route | Frequency |
| --- | --- | --- | --- |
| Furosemide | 40 MG | oral | once daily |
| Lisinopril | 10 MG | oral | once daily |
| Spironolactone | 25 MG | oral | once daily |

On the chart, furosemide and spironolactone are listed for the heart-failure diagnosis. Lisinopril is listed for hypertension. The dose, route, and frequency come from the curated regimen for this heart-failure profile.

### Inpatient medication changes

During the stay, the same three medications remain active at the same dose, route, and frequency. This particular chart does not add a new start, a temporary hold, a substitution, or a hospital-only drug. Other cases use those roles. Section 5 shows how they are represented when they occur.

### Discharge regimen

On the clean chart, the discharge list is the same three medications, still 40 MG, 10 MG, and 25 MG, oral, once daily. The discharge instruction says to take the discharge medications as listed. That instruction belongs with the list. It is not a separate monitoring plan.

### Monitoring and follow-up

Follow-up and monitoring are their own section. TEACH-001 schedules heart-failure clinic follow-up in 7 days with cardiology. No separate laboratory monitoring task is stored. A clinic appointment and a laboratory task are different items. A return precaution for worsening dyspnea is stored with the other clinical information, not inside the medication table.

Medication reconciliation on this chart records a history from the patient and prior records, with the patient able to participate and a pharmacist review recorded. That block describes how the history was obtained. The medication tables are the regimen.

## 3. Where the information comes from

| Case element | Source |
| --- | --- |
| Medication identity | RxNorm-backed terminology |
| Laboratory identity | LOINC-backed terminology |
| Diagnosis identity | ICD-10-CM-backed terminology where used |
| Demographics | synthetic |
| Numeric vitals/labs | synthetic |
| Clinical profile | structured generator or resident-derived archetype |
| Medication regimen | curated clinical profile logic |
| Narrative wording | generated from structured clinical facts |
| Assessment problem | introduced after the clean case is constructed |

Terminology provenance confirms the identity of a clinical concept. It does not by itself establish that the complete case is clinically appropriate.

The balanced case set builds each chart from a structured clinical profile. The resident-seed-guided case set starts from an archetype taken from resident-authored cases. Both strategies then create a synthetic patient, findings, a medication transition, and follow-up. TEACH-001 uses a structured heart-failure profile: volume overload, multi-day diuresis, the three medications above, creatinine, BNP, potassium, and cardiology follow-up. Age, sex, weight, and the numeric results are synthetic draws for this teaching patient. They are not copied from a study case.

## 4. How a clean case is constructed

```text
Clinical scenario or archetype
        ↓
Clinical profile
        ↓
Synthetic patient
        ↓
Clinical findings
        ↓
Medication transitions
        ↓
Monitoring and follow-up
        ↓
CLEAN CASE
```

The clean case is constructed first. The hospitalization, the regimen, and the follow-up are assembled as a coherent chart. An assessment problem, when one is used, is introduced only after that chart exists. The chart is not written around an error.

TEACH-001 is that clean chart. TEACH-002, in the next section, is the same hospitalization after one change to the discharge list.

## 5. How the medication transition is represented

```text
Home regimen
      ↓
Hospitalization
      ├── continued
      ├── newly started
      ├── temporarily held
      ├── substituted
      ├── discontinued
      └── hospital-only
      ↓
Discharge regimen
      +
monitoring
      +
follow-up
      +
restart / pending decisions
```

Medication reconciliation is more than a comparison of two lists. The transition can also depend on:

- why a medication was held
- whether it should restart
- whether monitoring is required
- whether enough medication is supplied
- whether follow-up is arranged
- whether inpatient-only therapy is stopped at discharge

A held drug may still be appropriate if the chart gives a reason and a restart plan. A hospital-only drug may be appropriate during the stay and absent from the discharge list. A clinic appointment does not replace a required laboratory task. Supply is separate from the drug name: a correct medication can still run out before follow-up.

On TEACH-001, all three home medications are continued through the hospitalization and onto the discharge list. Monitoring and the heart-failure clinic visit are recorded beside that list.

## 6. A clean chart and a chart with one assessment problem

[TEACH-001](examples/clean_heart_failure_case.md) is the clean case. [TEACH-002](examples/heart_failure_omission_case.md) is the error-bearing form of that same case: the same patient, the same course, and the same home and inpatient lists, with one difference on the discharge list. The TEACH-002 chart is written as a clinical chart. It does not announce a problem.

### Clean discharge

Home, inpatient, and discharge:

- furosemide
- lisinopril
- spironolactone

### Medication-omission example

Home and inpatient:

- furosemide
- lisinopril
- spironolactone

Discharge:

- lisinopril
- spironolactone

In the second example, one clinically intended medication is absent from the discharge list. The resident-facing chart does not label this as an error. The investigator key records the intended target separately.

The missing discharge row is furosemide 40 MG oral once daily. Home and inpatient furosemide are unchanged. Lisinopril and spironolactone remain on every list. Nothing else in the hospitalization was changed.

### Investigator record

This teaching change is a medication omitted from the discharge list. The project records that class of problem as Family 1. The investigator record for TEACH-002 is stored with the technical source files and is separate from the chart. Study cases keep the same separation: the resident chart does not carry the answer, and the clinician validation packet does. This page does not identify the target on any VAL case.

## 7. Medication-list discrepancies and transition-of-care gaps

Assessment problems fall into two clinical groups. A case receives at most one introduced problem. Some study cases are clean controls, so a reviewer cannot assume that every chart contains a problem.

### Medication-list discrepancies

These involve the regimen itself. Examples:

- medication omitted
- unintended medication continued
- dose mismatch
- route mismatch
- frequency mismatch
- therapeutic substitution problem

The project records this group as Family 1. TEACH-002 is the omission example.

### Transition-of-care gaps

These involve actions around the medication plan. Examples:

- required monitoring missing
- restart plan missing
- medication supply inadequate
- hospital-only therapy continued
- substitution not reverted
- pending medication decision lacks appropriate follow-up

The project records this group as Family 2. A clinic appointment can be present while the laboratory task is the missing step. TEACH-001 and TEACH-002 do not demonstrate a Family 2 gap. The study sets include both groups. The case-set overviews describe them without naming which VAL case carries which target.

## 8. What the software checks

Before a case reaches clinicians, automated checks evaluate:

- required chart structure
- terminology consistency
- laboratory value/unit compatibility
- medication route/form compatibility
- supported dose/frequency rules
- consistency of medication temporal states
- clean-case uniqueness
- whether the intended experimental change was introduced as designed
- whether an obvious second mechanical discrepancy was created

These checks do not establish that the case is clinically believable or educationally fair.

A passed check means the chart is internally consistent with the rules the software implements. It leaves clinical plausibility, fairness, and competing interpretations to the reviewer.

## 9. What the clinician reviews

Clinician validation is one reading of the complete chart. The same reading produces five ratings. This review decides whether a chart is fit to use. It is separate from the later task in which a resident, who does not see the answer, says what is wrong.

### C1 — Clinical plausibility

Does the complete chart represent a believable inpatient encounter?

### C2 — Intended assessment problem

Is the intended medication-reconciliation or transition-of-care problem actually present?

### C3 — Detectability

Could an internal-medicine resident identify and resolve it using only the chart?

### C4 — Competing problems

Is there another clinically meaningful medication problem that could reasonably be interpreted as an alternative answer?

### C5 — Difficulty

How difficult is the case likely to be for an internal-medicine resident?

C5 is advisory. Observed difficulty comes later, from resident performance.

After those ratings, the decision is:

- **Accept.** The chart can be used for its assigned target, or as a clean control.
- **Revise.** The chart needs a specific correction before use. A correction is a new freeze, not a silent edit of a frozen set.
- **Exclude.** The chart should not be used, even if the software checks passed.

Until that review is finished, treat the study charts as machine-checked synthetic cases awaiting clinician validation.

## Continue to clinician review

- [Balanced clinician validation packet](../../data/case_sets/balanced/readable/clinician_validation_packet.md)
- [Seed-guided clinician validation packet](../../data/case_sets/seed_guided/readable/clinician_validation_packet.md)
- [Clinical validation methodology](../clinical_validation.md)

The packets include the intended target so a validator can rate the chart and the target together. The readable case pages do not.

## Technical source files

The structured source used to generate the teaching example is available here for technical reference.

- [Clean chart source (TEACH-001)](source_json/teach-001-clean.json)
- [Omission chart source (TEACH-002)](source_json/teach-002-omission.json)
- [Investigator record for TEACH-002](source_json/teach-002-investigator.json)
- [Index of source files](source_json/README.md)

Earlier generator snapshots are stored in that same technical folder. They are not the charts explained above.
