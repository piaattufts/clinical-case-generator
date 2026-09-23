# CliniProof Balanced Structured Case Set

Batch: `CLINIPROOF_BALANCED_V4`
Cases: VAL-701–VAL-724
Number of cases: 24
Status: Pending human clinician validation
Generation approach: Balanced structured generation

## Start reviewing

- [Read all cases](readable/all_cases.md)
- [Open the clinician validation packet](readable/clinician_validation_packet.md)
- [Open the validation worksheet](readable/clinical_validation_worksheet.csv)

## What this case set is

This set was designed to cover a range of common inpatient problems
under a controlled study plan. Each case is a new synthetic encounter
built from a named clinical profile: a specified presentation, medication
role, hospital course, and follow-up. The profiles were chosen so that
the 24 charts differ in clinical structure before any assessment problem
is introduced.

The other current set, the [resident-seed-guided cases](../seed_guided/README.md), starts from resident-authored clinical examples
instead of this scenario grid. The two sets ask different design questions.
They are not two versions of the same batch.

## At a glance

| Clinical family | Number of cases | Typical clinical context |
| --- | ---: | --- |
| Heart failure | 5 | Decompensation, diuresis, and medication adjustment |
| Atrial fibrillation | 5 | Rate control and anticoagulation |
| Hypertension | 5 | Symptomatic or severe hypertension and medication transitions |
| Type 2 diabetes | 5 | Inpatient hyperglycemia and discharge therapy |
| Pneumonia | 4 | Acute infection and short-course medication transitions |

The distribution is intentionally balanced for study design and is not
intended to reproduce disease prevalence in clinical practice.

## How each case is structured

Every case is written as a hospital chart, in this order:

```text
Patient overview
        ↓
Reason for hospitalization
        ↓
Relevant medical history / problem list
        ↓
Hospital course
        ↓
Admission vitals and laboratories
        ↓
Discharge / most-recent clinical status
        ↓
Home medications
        ↓
Medications used during hospitalization
        ↓
Discharge medications
        ↓
Medication reconciliation
        ↓
Monitoring and follow-up
        ↓
Discharge instructions
        ↓
Imaging / consultations / procedures / other context
```

| Case section | What the clinician should learn from it |
| --- | --- |
| Patient overview | Demographic and admission context |
| Reason for hospitalization | Why hospital-level care occurred |
| Relevant medical history | Comorbidities needed to interpret the medications |
| Hospital course | Clinical trajectory and treatment decisions |
| Admission vs discharge status | Whether the transition is clinically coherent |
| Home medications | Pre-admission regimen |
| Inpatient medications | Continuation, starts, substitutions, holds, and hospital-only therapy |
| Discharge medications | Outpatient regimen as presented to the resident |
| Medication reconciliation | History source, participation, and pharmacist review |
| Monitoring and follow-up | Transition-of-care requirements |
| Other clinical information | Imaging, procedures, consultations, and return precautions |

## How medication transitions are represented

```text
Home regimen
    ↓
Hospitalization
    ├── continued
    ├── temporarily held
    ├── substituted
    ├── discontinued
    ├── newly started
    └── hospital-only therapy
    ↓
Discharge regimen
    +
monitoring
    +
follow-up
    +
restart / pending decisions
```

A problem can sit in the medication list itself, or in the plan around that list.
Monitoring, supply, a restart, follow-up, or a drug that should stay in the
hospital can each be the issue. A list that looks complete can still hide a
missing transition step.

## What varies across cases

Cases differ in the clinical situation, not only in the identifier:

- diagnosis or archetype
- presentation and symptoms
- clinical trajectory
- relevant past history
- medication regimen
- inpatient medication changes
- laboratory findings
- imaging, procedures, or consultations
- discharge clinical status
- monitoring and follow-up
- disposition, when the profile calls for a change from the patient's baseline living situation

## What does not count as meaningful case diversity

Two cases are not treated as clinically distinct merely because they differ in:

- age
- sex
- random seed
- an exact laboratory number
- an exact vital sign
- the case identifier
- which discrepancy was later introduced

The diversity audit ignores those fields and compares the clean clinical structure.

## Medication-reconciliation problems represented

Each error-bearing case is built around one medication-reconciliation or
transition-of-care problem. Clean controls, with no introduced problem, are
included so a reviewer cannot assume every chart is wrong. This page does not
say which case is which.

### Family 1 — the regimen itself

The discharge regimen does not match the intended plan. Examples:

- a medication that should continue is missing
- a medication that should have stopped is still listed
- the dose does not match the rest of the chart
- the route does not match the formulation
- the frequency does not match the regimen
- a same-class substitute appears without a documented reason

### Family 2 — the transition around the list

The medication list can look plausible while a required transition step is missing. Examples:

- required laboratory monitoring is not arranged
- a held medication has no restart plan
- the supply will not last until follow-up
- a hospital-only medication is still on the discharge list
- a temporary inpatient substitute was not changed back
- a pending medication decision has no follow-up

A clinic appointment is not the same thing as the laboratory task.
An anticoagulation clinic visit can be present while the INR check itself
is the missing step.

## How clinicians should review these cases

Review is one reading of the complete case. Record all five ratings in that
same pass. There is no separate plausibility stage and no second consensus
stage. This review decides whether a chart is fit to use. It is not the later
task in which a resident, blinded to the answer, says what is wrong.

### C1 — Clinical plausibility

Could this reasonably be an inpatient encounter? Consider the presentation,
the diagnosis, the vital signs, the laboratories, the regimen, the hospital
course, internal consistency, and the discharge plan.

### C2 — Intended assessment problem

Is the intended medication-reconciliation or transition-of-care problem
actually present, and does it match its category? A control should contain none.

### C3 — Detectability

Could an internal-medicine resident identify the problem from the visible
chart and say what should change, without the chart announcing the answer?

### C4 — No unintended competing problem

Is there another clinically meaningful medication problem that could
reasonably be read as a different answer? A second dose, frequency, route,
hold, or monitoring problem can make the case unusable.

### C5 — Difficulty

How difficult is the case likely to be for the intended learner?
This rating is advisory. Actual difficulty will later be estimated from
resident performance.

Recommendations:

- **Accept.** The chart can be used for its assigned purpose, or as a control.
- **Revise.** The chart needs a stated correction before use.
  Do not silently edit a case after review has started.
- **Exclude.** The chart should not be used, even if software checks passed.

C1 through C4 need to be acceptable before a case is used against its answer key.

## Case map

Each row is one synthetic encounter. This table does not say which cases
contain a discrepancy or what that discrepancy is.

| Case | Clinical family | Admission diagnosis | Profile / clinical context | Main distinguishing feature |
| --- | --- | --- | --- | --- |
| VAL-701 | Heart failure | Acute systolic (congestive) heart failure | Volume overload | Admitted for decompensated heart failure with volume overload |
| VAL-702 | Heart failure | Acute systolic (congestive) heart failure | Post diuresis | Admitted for decompensated heart failure; congestion improved with diuresis |
| VAL-703 | Heart failure | Acute systolic (congestive) heart failure | With warfarin | Admitted for decompensated heart failure with atrial fibrillation |
| VAL-704 | Heart failure | Acute systolic (congestive) heart failure | Medication adjustment | Admitted for decompensated heart failure requiring diuretic adjustment |
| VAL-705 | Heart failure | Acute systolic (congestive) heart failure | Discharge monitoring | Admitted for decompensated heart failure with a planned home-health transition |
| VAL-706 | Atrial fibrillation | Paroxysmal atrial fibrillation | Rate control apixaban | Admitted for symptomatic atrial fibrillation with rapid ventricular response |
| VAL-707 | Atrial fibrillation | Paroxysmal atrial fibrillation | Warfarin INR | Admitted for symptomatic atrial fibrillation requiring rate control and INR assessment |
| VAL-708 | Atrial fibrillation | Paroxysmal atrial fibrillation | With statin | Admitted for symptomatic atrial fibrillation; rate control was restored |
| VAL-709 | Atrial fibrillation | Paroxysmal atrial fibrillation | Held nsaid | Admitted for symptomatic atrial fibrillation with chest discomfort |
| VAL-710 | Atrial fibrillation | Paroxysmal atrial fibrillation | Post rate control | Admitted for atrial fibrillation with rapid ventricular response, now rate-controlled |
| VAL-711 | Hypertension | Essential (primary) hypertension | ACE CCB | Admitted for symptomatic hypertensive urgency with chest pain, observed for end-organ symptoms |
| VAL-712 | Hypertension | Essential (primary) hypertension | ACE thiazide | Admitted for symptomatic hypertensive urgency with marked blood-pressure elevation |
| VAL-713 | Hypertension | Essential (primary) hypertension | CCB statin | Admitted for symptomatic hypertensive urgency after home readings remained severely elevated |
| VAL-714 | Hypertension | Essential (primary) hypertension | Triple therapy | Admitted for symptomatic hypertensive urgency on triple oral therapy, observed for end-organ symptoms |
| VAL-715 | Hypertension | Essential (primary) hypertension | New diagnosis | Admitted for a first presentation of severe symptomatic hypertension requiring observed treatment |
| VAL-716 | Type 2 diabetes | Type 2 diabetes mellitus with hyperglycemia | Metformin ACE | Admitted for symptomatic hyperglycemia with polyuria requiring supervised glucose and fluid management |
| VAL-717 | Type 2 diabetes | Type 2 diabetes mellitus with hyperglycemia | Metformin statin | Admitted for symptomatic hyperglycemia requiring inpatient glucose stabilization |
| VAL-718 | Type 2 diabetes | Type 2 diabetes mellitus with hyperglycemia | Glycemic stabilization | Admitted for symptomatic hyperglycemia with volume depletion requiring supervised treatment |
| VAL-719 | Type 2 diabetes | Type 2 diabetes mellitus with hyperglycemia | Pending duration | Admitted for symptomatic hyperglycemia; a pending outpatient diabetes-therapy decision was recorded |
| VAL-720 | Type 2 diabetes | Type 2 diabetes mellitus with hyperglycemia | Uncomplicated course | Admitted for symptomatic hyperglycemia that improved with supervised inpatient management |
| VAL-721 | Pneumonia | Lobar pneumonia, unspecified organism | Typical cough | Admitted for community-acquired pneumonia with hypoxia and a lobar infiltrate |
| VAL-722 | Pneumonia | Lobar pneumonia, unspecified organism | Dyspnea wheeze | Admitted for hypoxic pneumonia with wheezing |
| VAL-723 | Pneumonia | Lobar pneumonia, unspecified organism | Inpatient antibiotic | Admitted for community-acquired pneumonia requiring inpatient antibiotics |
| VAL-724 | Pneumonia | Lobar pneumonia, unspecified organism | Home transition | Admitted for pneumonia; a remaining oral antibiotic course was arranged at discharge |

## Dataset composition

- 24 cases
- 24 distinct clinical profiles
- 0 exact clean-case duplicates
- Highest clean-case similarity: 0.74 (VAL-717 vs VAL-719)
- Near-duplicate warnings: 1

Similarity is measured on the clean clinical case before any discrepancy is introduced.
A warning means two charts share clinical structure. It is not a rejection.

### Clinical families

| Item | Cases |
| --- | ---: |
| Atrial fibrillation | 5 |
| Heart failure | 5 |
| Hypertension | 5 |
| Type 2 diabetes | 5 |
| Pneumonia | 4 |

### Admission diagnoses

| Item | Cases |
| --- | ---: |
| Acute systolic (congestive) heart failure | 5 |
| Essential (primary) hypertension | 5 |
| Paroxysmal atrial fibrillation | 5 |
| Type 2 diabetes mellitus with hyperglycemia | 5 |
| Lobar pneumonia, unspecified organism | 4 |

### Clinical services

| Item | Cases |
| --- | ---: |
| cardiology | 10 |
| general medicine | 10 |
| pulmonology | 4 |

### Discharge disposition

| Item | Cases |
| --- | ---: |
| home | 24 |

### Medication-transition patterns in the clean profiles

These counts describe the clinical situation designed into each profile.
They are not the injected assessment targets.

| Pattern designed into the profile | Cases |
| --- | ---: |
| Home regimen continued into the hospitalization | 24 |
| A hold or a stop is part of the profile | 3 |
| Hospital-only therapy is part of the profile | 6 |
| A pending outpatient medication decision is part of the profile | 1 |

## Investigator / technical material

Clinicians rating cases do not need these files to start. Investigators
and developers use them to see how the set was frozen.

- [Manifest](validation_manifest.json)
- [Diversity report](diversity_report.md)
- [Answer key](investigator_answer_key.md) — investigators only
- [Batch plan](batch_plan.json)
- [Coverage report](coverage_report.md)
- [Internal QC report](../investigator/clinical_qc_report.md)

Regenerate this overview from the manifest and profiles with
`python -m app.services.case_set_overview`.
