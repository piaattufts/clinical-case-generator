# CliniProof Resident-Seed-Guided Case Set

Batch: `CLINIPROOF_SEEDCASES_V3`
Cases: VAL-801–VAL-824
Number of cases: 24
Status: Pending human clinician validation
Generation approach: Resident-seed-guided generation

## Start reviewing

- [Read all cases](readable/all_cases.md)
- [Open the clinician validation packet](readable/clinician_validation_packet.md)
- [Open the validation worksheet](readable/clinical_validation_worksheet.csv)

## What this case set is

This set starts from six resident-authored clinical examples. Each example
was abstracted into an archetype: the workflow a discharging clinician has
to get right. Four synthetic profiles were then written for each archetype
so the charts differ before any assessment problem is introduced.

The resident-authored source cases are used as clinical design references.
The study cases are newly synthesized encounters, not copies of the source cases.
Six examples do not estimate how often these problems occur, which drugs
are most common, or which errors are most common. The [source documents](../../seed_cases/README.md) are preserved separately and are not the charts
under review.

The other current set, the [balanced structured cases](../balanced/README.md),
starts from a predefined scenario grid rather than from these examples.

## At a glance

| Resident-derived archetype | Cases | Core clinical workflow represented |
| --- | ---: | --- |
| Medication history uncertainty | 4 | Incomplete history, collateral reconciliation, and discharge-list verification |
| Acute heart-failure decompensation | 4 | Diuresis, renal or electrolyte changes, and medication holds or adjustment |
| Outpatient parenteral antibiotic therapy after endocarditis | 4 | Intravenous antibiotics, line care, monitoring, and infectious-diseases follow-up |
| Post-kidney-transplant infectious complication | 4 | Antiviral treatment, immunosuppression management, and monitoring |
| Postoperative anticoagulation after hip fracture | 4 | Surgery, interruption or resumption of anticoagulation, and rehabilitation |
| Gastrointestinal bleed with anticoagulation decisions | 4 | Bleeding stabilization, medication holds, and restart decisions |

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
| VAL-801 | Medication history uncertainty | Delirium due to known physiological condition | Collateral verified | The patient could not supply a reliable medication history at admission |
| VAL-802 | Medication history uncertainty | Delirium due to known physiological condition | Verified statin continued | A later collateral list confirmed a continued statin |
| VAL-803 | Medication history uncertainty | Delirium due to known physiological condition | Home services supply | Discharge planning includes home services |
| VAL-804 | Medication history uncertainty | Delirium due to known physiological condition | Pending cognitive therapy | A cognitive-enhancer start is deferred to outpatient confirmation |
| VAL-805 | Acute heart-failure decompensation | Acute systolic (congestive) heart failure | Uncomplicated diuresis | Congestion improved with inpatient diuresis |
| VAL-806 | Acute heart-failure decompensation | Acute systolic (congestive) heart failure | AKI holds | Creatinine rose with congestion |
| VAL-807 | Acute heart-failure decompensation | Acute systolic (congestive) heart failure | Potassium replacement | Diuresis was accompanied by potassium repletion |
| VAL-808 | Acute heart-failure decompensation | Acute systolic (congestive) heart failure | Diuretic adjustment | The outpatient diuretic plan was reviewed during the stay |
| VAL-809 | Outpatient parenteral antibiotic therapy after endocarditis | Acute and subacute infective endocarditis | Stable completion plan | The patient is leaving with a planned parenteral antibiotic course, line precautions, and scheduled laboratory monitoring |
| VAL-810 | Outpatient parenteral antibiotic therapy after endocarditis | Acute and subacute infective endocarditis | Parenteral antibiotic course | Admitted for endocarditis |
| VAL-811 | Outpatient parenteral antibiotic therapy after endocarditis | Acute and subacute infective endocarditis | Short antibiotic supply | Admitted for endocarditis with a remaining outpatient parenteral course |
| VAL-812 | Outpatient parenteral antibiotic therapy after endocarditis | Acute and subacute infective endocarditis | Infectious-diseases follow-up | Duration of remaining parenteral ceftriaxone is to be confirmed at infectious-disease follow-up |
| VAL-813 | Post-kidney-transplant infectious complication | Other cytomegaloviral diseases | CMV improving | Gastrointestinal symptoms improved on antiviral therapy |
| VAL-814 | Post-kidney-transplant infectious complication | Other cytomegaloviral diseases | MMF hold restart | Mycophenolate was held during infection as an immunosuppression adjustment |
| VAL-815 | Post-kidney-transplant infectious complication | Other cytomegaloviral diseases | Tacrolimus adjustment | Admitted for cytomegalovirus disease after kidney transplantation with a tacrolimus dose adjustment |
| VAL-816 | Post-kidney-transplant infectious complication | Other cytomegaloviral diseases | Pending antiviral duration | Antiviral duration after conversion remains a pending outpatient decision |
| VAL-817 | Postoperative anticoagulation after hip fracture | Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | Warfarin monitoring | Warfarin was interrupted for surgery and then resumed |
| VAL-818 | Postoperative anticoagulation after hip fracture | Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | Anticoagulation | Postoperative hemoglobin was observed |
| VAL-819 | Postoperative anticoagulation after hip fracture | Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | Anticoag supply | Anticoagulation supply and INR follow-up |
| VAL-820 | Postoperative anticoagulation after hip fracture | Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | Bridge hospital only | Enoxaparin was used for inpatient venous-thromboembolism prophylaxis |
| VAL-821 | Gastrointestinal bleed with anticoagulation decisions | Gastrointestinal hemorrhage, unspecified | Ac held restart | Bleeding settled and hemoglobin was stable |
| VAL-822 | Gastrointestinal bleed with anticoagulation decisions | Gastrointestinal hemorrhage, unspecified | PPI hospital only | Pantoprazole was initiated during the hospitalization for acute gastrointestinal management |
| VAL-823 | Gastrointestinal bleed with anticoagulation decisions | Gastrointestinal hemorrhage, unspecified | Pending ac decision | Restart versus continued hold of anticoagulation is a pending outpatient decision |
| VAL-824 | Gastrointestinal bleed with anticoagulation decisions | Gastrointestinal hemorrhage, unspecified | Aspirin not restarted | Aspirin used for primary prevention was stopped after the bleed |

## Dataset composition

- 24 cases
- 24 distinct clinical profiles
- 0 exact clean-case duplicates
- Highest clean-case similarity: 0.79 (VAL-805 vs VAL-807)
- Near-duplicate warnings: 7

Similarity is measured on the clean clinical case before any discrepancy is introduced.
A warning means two charts share clinical structure. It is not a rejection.

### Clinical families

| Item | Cases |
| --- | ---: |
| Acute heart-failure decompensation | 4 |
| Gastrointestinal bleed with anticoagulation decisions | 4 |
| Medication history uncertainty | 4 |
| Outpatient parenteral antibiotic therapy after endocarditis | 4 |
| Post-kidney-transplant infectious complication | 4 |
| Postoperative anticoagulation after hip fracture | 4 |

### Admission diagnoses

| Item | Cases |
| --- | ---: |
| Acute and subacute infective endocarditis | 4 |
| Acute systolic (congestive) heart failure | 4 |
| Delirium due to known physiological condition | 4 |
| Fracture of unspecified part of neck of right femur, initial encounter for closed fracture | 4 |
| Gastrointestinal hemorrhage, unspecified | 4 |
| Other cytomegaloviral diseases | 4 |

### Clinical services

| Item | Cases |
| --- | ---: |
| general medicine | 8 |
| cardiology | 4 |
| infectious disease | 4 |
| nephrology | 4 |
| orthopedics | 4 |

### Discharge disposition

| Item | Cases |
| --- | ---: |
| home | 20 |
| rehab | 4 |

### Medication-transition patterns in the clean profiles

These counts describe the clinical situation designed into each profile.
They are not the injected assessment targets.

| Pattern designed into the profile | Cases |
| --- | ---: |
| Home regimen continued into the hospitalization | 24 |
| A hold or a stop is part of the profile | 5 |
| Hospital-only therapy is part of the profile | 2 |
| A pending outpatient medication decision is part of the profile | 3 |

## Investigator / technical material

Clinicians rating cases do not need these files to start.

- [Manifest](validation_manifest.json)
- [Diversity report](diversity_report.md)
- [Answer key](investigator_answer_key.md) — investigators only
- [Batch plan](batch_plan.json)
- [Coverage report](coverage_report.md)
- [Internal QC report](../investigator/clinical_qc_report.md)
- [Resident-authored source notes](../../seed_cases/README.md)

Regenerate this overview from the manifest and archetypes with
`python -m app.services.case_set_overview`.
