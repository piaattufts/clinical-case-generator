# CliniProof

CliniProof is a research framework for creating and validating synthetic inpatient cases for studying discharge-medication reasoning.

Each case describes a synthetic hospitalization: why the patient was admitted, what happened during the hospital stay, relevant laboratory and vital-sign changes, home medications, inpatient medications, and follow-up context.

The eventual resident task is to review that clinical information and decide which medications should be prescribed at discharge.

Residents are not shown the correct discharge plan. A separate clinician-validated reference plan is kept by the research team for later comparison and scoring. A scoring program for that comparison is not built yet.

The repository has gone through two clinician-validation rounds.

- **Round 2 is the current review set.**
- **Round 1 is retained because its clinician feedback led directly to the Round 2 redesign.**

## What this repository contains

Synthetic hospital cases, the Word forms clinicians use to judge those cases, and the software that builds them. The cases are not extracts from a medical record. Medication, diagnosis, and laboratory names are tied to standard terminologies. Ages, vital signs, and laboratory numbers are synthetic.

## Start here — current clinician review

If you are a clinician reviewing the current cases, use the Round 2 casebook. It is one Word file with all 24 cases and a blank form for each case.

**Round 2 clinician validation casebook**

- [Round 2 clinician validation casebook](exports/ko_cycle2_final_validation/CliniProof_Cycle2_Final_Validation.docx)
- [Round 2 package notes](exports/ko_cycle2_final_validation/README.md)
- [Round 2 case manifest](exports/ko_cycle2_final_validation/MANIFEST.md)

Cases: VAL-801–VAL-824  
Number of cases: 24  
Status: ready for clinician review; not yet clinically validated

Passing automated validation does not establish clinical validity.

## Round 2 — Current clean-case clinician validation

Round 2, also referred to in the repository as Clinical Revision Cycle 2, is the current clinician-validation round for VAL-801–VAL-824.

### What Round 2 is

Round 2 contains 24 clean synthetic inpatient cases.

The clinician is reviewing whether:

1. the clinical story is plausible;
2. the chart contains enough information for a resident to decide what should happen to each medication at discharge;
3. the hidden reference discharge plan is clinically defensible;
4. other discharge plans should also be accepted as reasonable;
5. any information is missing, contradictory, or unintentionally revealing the answer.

A clean case does not contain a deliberately planted medication error.

The resident sees the clinical evidence but not the reference discharge plan. The phrase “ready for clinician review” means the case has passed the repository’s internal checks and is ready to be evaluated by a clinician. Internally that status is sometimes labeled `READY_FOR_CLINICIAN_REVIEW`. It is not clinical approval.

### What the clinician is reviewing

The same kind of chart a resident would later see: the admission, the hospital course, laboratory and vital-sign changes, medicines taken at home, medicines used in the hospital, and follow-up plans. The study’s proposed discharge plan is withheld until the clinician has read that chart.

### What is in the Round 2 codebook

The current Word casebook contains all 24 cases, VAL-801 through VAL-824.

For each case the clinician first reads the same clean chart that a resident would see.

The clinician then completes:

- C1 — clinical plausibility
- C2 — whether the chart contains enough information for a resident to make the discharge decision
- C3 — whether the hidden reference plan is clinically defensible
- C4 — whether other answers should also be accepted
- C5 — whether there are missing, misleading, or competing clinical issues
- C6 — expected learner difficulty
- Accept / Revise / Exclude

The hidden reference plan appears only after the clinician has assessed the resident-facing chart. Accept. Revise. Exclude. are the overall recommendations on that form. They do not mean a case has already been accepted.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word.

### Cases included in Round 2

Round 2 contains 24 cases.

Six cases were revised directly in response to clinician comments from Round 1:

- VAL-801
- VAL-802
- VAL-803
- VAL-805
- VAL-809
- VAL-813

The other 18 recovered clean cases are undergoing their first review under the corrected clean-case protocol:

- VAL-804
- VAL-806
- VAL-807
- VAL-808
- VAL-810
- VAL-811
- VAL-812
- VAL-814
- VAL-815
- VAL-816
- VAL-817
- VAL-818
- VAL-819
- VAL-820
- VAL-821
- VAL-822
- VAL-823
- VAL-824

Nine of the 18 required narrow consistency corrections before review. These corrections removed contradictions or answer-revealing wording; they were not clinician validation. The case-by-case notes are in [Round 2 detailed revision log](#round-2-detailed-revision-log).

### Download the Round 2 codebook

- [Download the Round 2 clinician validation casebook](exports/ko_cycle2_final_validation/CliniProof_Cycle2_Final_Validation.docx)
- [Round 2 package notes](exports/ko_cycle2_final_validation/README.md)
- [Round 2 case manifest](exports/ko_cycle2_final_validation/MANIFEST.md)

### How Round 2 was produced

Round 2 was not generated as a new population of cases.

The project already had VAL-801–VAL-824 from the first validation round.

For Round 1, many of those cases had been intentionally modified to contain a medication-reconciliation problem. The clean version that existed before that modification had been preserved. We refer to this as the archived clean or pre-injection source.

For Round 2:

1. the original clean, pre-modification charts were recovered;
2. the clinician comments from Round 1 were reviewed;
3. cases with underlying clinical weaknesses were revised;
4. the remaining clean cases were checked for contradictions or answer-revealing language;
5. resident-facing charts were separated from hidden evaluator reference plans;
6. the resulting 24 cases were assembled into a new blank clinician-validation casebook.

```text
Round 1 case
    ↓
recover original clean chart
    ↓
apply relevant clinician feedback
    ↓
remove remaining inconsistencies / answer leakage
    ↓
Round 2 clean case
    ↓
new clinician validation
```

The original Round 1 files were not overwritten. No new 24-case population was generated.

### What happens after clinician review

A clinician Accept, Revise, or Exclude decision is still required before any case is treated as validated. After that review, residents would receive only the clean chart and would write their own discharge medication plan. The clinician-validated reference would stay with the research team for later comparison. Collecting resident confidence, written reasoning, or a response to later computer-generated advice is part of the planned study. Those collection tools are not implemented in this repository.

## Round 1 — Initial validation and what we learned

### What Round 1 tested

Round 1 used a different validation design.

Some cases were left unchanged as clean controls. Other cases were given one deliberately introduced medication-reconciliation or transition-of-care problem.

The clinician was asked to judge whether:

- the chart was clinically plausible;
- the intended problem was actually present;
- a resident could detect it;
- another unintended clinical problem competed with the intended answer;
- the case was appropriate in difficulty.

That design tested the error-injection framework.

It is no longer the active resident-study design.

### Download the Round 1 codebook

The Round 1 review of VAL-801–VAL-824 is the seed-guided validation casebook. The balanced casebook is the separate Round 1 review of VAL-701–VAL-724. Instructions for those historical forms are on the Round 1 review-package page.

### Round 1 validation materials

- [Round 1 VAL-801–VAL-824 clinician validation casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx)
- [Round 1 validation instructions](docs/resident_review_package/README.md)
- [Round 1 balanced VAL-701–VAL-724 casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx)

### Why the design changed

Round 1 clinician feedback exposed a mismatch between the validation task and the intended resident study.

The intended resident task was not to inspect a supplied discharge list and find a planted error. The intended task was for the resident to determine the discharge medication plan from the clinical case.

```text
Round 1
clinical chart + supplied discharge regimen
        ↓
find / validate a planted problem

became

Round 2
clean clinical chart
        ↓
resident determines discharge regimen
        ↓
compare with hidden clinician-validated reference
```

This change is why Round 2 uses clean resident-facing cases and hidden reference plans.

### How Round 1 led to Round 2

Round 1 feedback did two things. It showed that the validation task itself used the wrong study model. It also showed that some of the underlying clinical stories were too thin or internally inconsistent, even after the planted problem was set aside. Round 2 keeps the same VAL-801–VAL-824 study slots, starts again from the preserved clean charts, and asks clinicians to judge those charts under the corrected task.

## Relationship between Round 1 and Round 2

| | Round 1 | Round 2 |
| --- | --- | --- |
| Status | Historical validation round | Current validation round |
| Cases | VAL-801–VAL-824 | VAL-801–VAL-824 |
| Resident-facing concept | Supplied medication transition with possible planted discrepancy | Clean chart; resident constructs discharge plan |
| Deliberate planted error | Yes for many cases | No |
| Clean controls | Yes | Not part of the design |
| Clinician validates | Plausibility and intended discrepancy | Plausibility, evidence sufficiency, reference plan and acceptable alternatives |
| Reference | Intended planted problem | Hidden discharge medication plan |
| Current use | Provenance / earlier methodology | Active clinician validation |

**Current:** [Open Round 2 casebook](exports/ko_cycle2_final_validation/CliniProof_Cycle2_Final_Validation.docx)

**Previous:** [Open Round 1 casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx)

The balanced Round 1 set, VAL-701–VAL-724, was not rebuilt in Round 2. Its casebook remains [the balanced Round 1 casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx).

## How the same case IDs relate across rounds

VAL-801–VAL-824 identify the same study slots across the two rounds, but the Round 2 review files are not simply the Round 1 documents with the error labels removed.

Round 2 begins from the archived clean pre-injection chart. Some cases were then revised using clinician feedback or repaired for internal consistency.

```text
Round 1 VAL-805
= historical validation version

Round 2 VAL-805
= clean recovered case + clinician-driven clinical revision
```

The frozen Round 1 file was not overwritten. Round 2 files live in separate folders.

## Where to find the case files

| What you want | Location |
| --- | --- |
| Current Round 2 clinician Word casebook | [Round 2 casebook](exports/ko_cycle2_final_validation/CliniProof_Cycle2_Final_Validation.docx) |
| Round 2 revised-case package | [Revised cases](exports/ko_revised_cases_v1/AUDIT.md) |
| Round 2 clean/fresh-review package | [Clean cases for review](exports/ko_clean_cases_for_review_v1/AUDIT.md) |
| Round 2 manifest | [Manifest](exports/ko_cycle2_final_validation/MANIFEST.md) |
| Historical Round 1 seed-guided casebook | [VAL-801–VAL-824 casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx) |
| Historical Round 1 balanced casebook | [VAL-701–VAL-724 casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx) |
| Recovered clean source export | [Recovered 48-case audit](exports/clean_balanced_seed_set/AUDIT.md) |
| Frozen historical source cases | [Seed-guided source, `CLINIPROOF_SEEDCASES_V3`](data/case_sets/seed_guided/README.md) and [balanced source, `CLINIPROOF_BALANCED_V4`](data/case_sets/balanced/README.md) |

## Case provenance

Round 2 was assembled from preserved clean versions of the earlier cases, not from a new generator run. Original seeds, clinical scenarios, and profile assignments were kept. The frozen historical files under `data/case_sets/` remain the Round 1 record.

## Study workflow

```text
synthetic clinical case
        ↓
clean resident-facing chart
        ↓
resident independently chooses discharge medication plan
        ↓
resident reasoning / confidence may also be collected
        ↓
hidden clinician-validated reference discharge plan
        ↓
comparison / scoring
```


## Round 2 detailed revision log

The summaries above are enough to start a review. The notes below, and the audit files, record the case-by-case changes. They are not clinician approval.

Case-by-case audits: [revised-case audit](exports/ko_revised_cases_v1/AUDIT.md) and [clean-case audit](exports/ko_clean_cases_for_review_v1/AUDIT.md).

### Cases revised from Round 1 clinician feedback

#### VAL-801 — Delirium / dehydration

Delirium is attributed to dehydration from poor intake. Dry mucous membranes and a 20 mmHg orthostatic blood-pressure drop support that account. Glucose improves from 163 to 103 mg/dL with restored intake. Confusion resolves as intake improves. Ibuprofen remains available for knee pain. The unsupported ibuprofen discontinuation was removed. Creatinine remains stable at 1.1 then 1.0 mg/dL.

Reference plan: continue atorvastatin, continue lisinopril, continue metformin, continue ibuprofen.

#### VAL-802 — Delirium / dehydration with renal context

Delirium is attributed to poor intake and dehydration. A creatinine of 1.2 mg/dL six weeks earlier is the renal baseline. Creatinine is 1.3 mg/dL on admission and 1.2 mg/dL at discharge. Potassium is 4.2 then 4.1 mmol/L. Systolic blood pressure is 138 then 124 mmHg. Atorvastatin remains present for hyperlipidemia.

Reference plan: continue lisinopril, continue atorvastatin.

#### VAL-803 — Thiazide-associated hyponatremia

Delirium is attributed to thiazide-associated hyponatremia. Sodium is 128 mmol/L while the patient is taking hydrochlorothiazide. Hydrochlorothiazide is held. Sodium improves to 135 mmol/L and confusion clears. Creatinine is 1.0 then 1.2 mg/dL. Potassium is 4.4 then 4.2 mmol/L. The recovered lisinopril supply remains 30 days.

Reference plan: stop hydrochlorothiazide, continue lisinopril, continue atorvastatin, continue metformin.

#### VAL-805 — Acute systolic heart failure

The chart now has a realistic inpatient decongestion course. Weight changes 86, then 83, then 80 kg. 80 kg is the documented dry weight. Intake and output are net negative on hospital days 1–3. Inpatient furosemide is intravenous 40 mg twice daily, distinct from the home oral regimen. Creatinine improves from 1.7 to 0.9 mg/dL. Potassium improves from 4.7 to 4.3 mmol/L. Natriuretic peptide improves from 1120 to 369 pg/mL. Discharge systolic blood pressure is 110 mmHg, heart rate is 69, and oxygen saturation is 98 percent. Ejection fraction is 30 percent.

Current reference plan: continue oral furosemide 40 mg daily, continue metoprolol succinate 25 mg daily, continue atorvastatin. A low-dose ACE inhibitor, ARB, or SGLT2 inhibitor is recorded as an acceptable alternative, not as a required reference medication.

Cycle 2 clinician review specifically asks whether additional HFrEF therapies should be considered required versus acceptable alternatives.

#### VAL-809 — Infective endocarditis

The chart now includes fever of 38.6°C, heart rate 104, a recent dental extraction, a new murmur, viridans group streptococcus, and a documented vegetation. Later cultures show no growth and the fever resolves. Creatinine improves from 1.3 to 1.0 to 0.8 mg/dL. The prior baseline is 0.8 mg/dL. Lisinopril is held during the creatinine elevation. Discharge systolic blood pressure is 118 mmHg.

Reference plan: start ceftriaxone 2 g intravenously daily for four weeks, restart lisinopril, continue atorvastatin.

#### VAL-813 — Transplant / CMV

The patient presents with diarrhea while taking tacrolimus and mycophenolate. Valganciclovir is no longer a home medication. CMV viral load is detected after admission, and valganciclovir 900 mg twice daily begins after that detection. Creatinine is 1.2 then 1.0 mg/dL. The transplant/CMV scenario was retained rather than replaced.

Reference plan: start valganciclovir, continue tacrolimus, continue mycophenolate, continue amlodipine, continue atorvastatin.

Cycle 2 clinician review explicitly asks whether continuing mycophenolate at discharge is appropriate in the presented CMV and transplant context.

### Pre-review consistency repair

The first Cycle 2 precheck found nine recovered clean cases that should not go to clinicians until obvious inconsistencies were corrected:

- VAL-806
- VAL-807
- VAL-808
- VAL-814
- VAL-815
- VAL-816
- VAL-817
- VAL-820
- VAL-821

These cases were not regenerated. Each repair is a traceable copy of the recovered clean source. The copies that passed the evidence audit are in the fresh-review package. None of the nine remains held.

**VAL-806.** No prior creatinine existed in the source data, so none was invented. The instruction that told the resident to restart lisinopril was removed. Visible data are creatinine 2.8 then 1.6 mg/dL, potassium 4.5 mmol/L, and systolic pressure 116 mmHg. The hidden reference restarts lisinopril from that visible course. The decision is flagged `WEAK_EVIDENCE` because creatinine is still elevated and no baseline is known. Continued hold is an acceptable alternative.

**VAL-807.** The potassium-repletion claim was removed because no potassium product existed in the medication data. The measured potassium, 3.5 then 3.8 mmol/L, remains. The answer-revealing “intended outpatient diuretic dose” wording was removed.

**VAL-808.** Answer-revealing “intended regimen” wording was removed. The source home and inpatient loop-diuretic doses are the same, oral furosemide 40 mg once daily, so no adjustment was added. Discharge weight stays 92 kg. The 86 kg dry weight was the unsupported field and is corrected to 92 kg, which matches the observed 2 kg loss. The reference continues oral furosemide 40 mg once daily.

**VAL-814.** Valganciclovir was removed from the home list. Treatment begins after the in-hospital viral-load result. The inpatient dose is renal-adjusted: 450 mg once daily while creatinine is 2.5 mg/dL, then 450 mg twice daily at creatinine 1.6 mg/dL. The direct mycophenolate restart instruction was removed. The reference starts valganciclovir and restarts mycophenolate. A continued mycophenolate hold is an acceptable alternative.

**VAL-815.** The unsupported tacrolimus dose-adjustment narrative was removed. Home and inpatient tacrolimus remain 1 mg every 12 hours, with creatinine 0.8 then 0.9 mg/dL and potassium 4.6 then 4.5 mmol/L. CMV uses the same chronology as VAL-813: valganciclovir is not a home medicine and starts after the in-hospital viral load, at 900 mg twice daily.

**VAL-816.** The admission is framed as established CMV disease already under treatment. The answer-like pending-decision instruction was removed. Infectious-disease follow-up is the review context instead.

**VAL-817.** Implementation wording such as “in this profile” was removed. The enoxaparin narrative was removed because enoxaparin was not in the source medication record. INR remains 2.6 on warfarin.

**VAL-820.** The enoxaparin indication is inpatient VTE prophylaxis. Warfarin remains the medication associated with atrial fibrillation. INR is 3.2 then 2.0.

Review whether pharmacologic VTE prophylaxis with enoxaparin is clinically appropriate in the presence of concurrent warfarin therapy and the documented INR values.

**VAL-821.** The direct instruction to resume apixaban was removed. The resident sees the gastrointestinal bleed, hemoglobin 8.7 then 10.9 g/dL, atrial fibrillation, creatinine 1.2 mg/dL, and gastroenterology follow-up in seven days. The hidden reference recommends restarting apixaban. A continued hold until gastroenterology review is an acceptable alternative.

These nine repairs are not clinician-approved fixes. They are pre-review consistency corrections. The following items still require clinician judgment:

| Case | Judgment still required |
| --- | --- |
| VAL-806 | Lisinopril restart is `WEAK_EVIDENCE`. Continued hold is an acceptable alternative because no renal baseline is known. |
| VAL-814 | Restart versus continued hold of mycophenolate. |
| VAL-820 | Whether separate enoxaparin VTE prophylaxis is appropriate while the patient is receiving warfarin at the documented INR values. |
| VAL-821 | Restart versus continued hold of apixaban after gastrointestinal bleeding. |

### Repair principle

Revision Cycle 2 did not preserve an existing reference answer at all costs. When an existing medication decision could not be supported by resident-visible evidence, either the clinical representation or the hidden reference decision was corrected. Clinical facts determine the reference plan. Facts are not invented merely to justify a pre-existing answer.

```text
clinical facts
    ↓
hospital course / labs / treatment response
    ↓
medication decision
    ↓
hidden reference plan
```

### Evidence-sufficiency audit

Every reference medication decision is checked against information visible in the resident chart.

Current internal evidence classifications are `SUFFICIENT_EVIDENCE`, `WEAK_EVIDENCE`, `HIDDEN_ANSWER_DEPENDENCY`, and `CLINICALLY_INCONSISTENT`.

For the current VAL-801–VAL-824 Cycle 2 packages, all 24 cases are prepared for clinician review. Every reference decision in those packages passed the current evidence-sufficiency audit. No current case is held for `HIDDEN_ANSWER_DEPENDENCY` or `CLINICALLY_INCONSISTENT`. Evaluator files for the six revised cases and the nine repairs use `READY_FOR_CLINICIAN_REVIEW`. The nine recovered charts that were not rewritten use `READY_FOR_FRESH_REVIEW`. Both labels mean the case is ready to enter review.

This is an automated/internal readiness check. It does not establish that the reference plan is clinically correct. Clinician reviewers determine that.

### Cycle 2 provenance

```text
original frozen VAL case
        ↓
archived pre-injection clean source
        ↓
clean-source recovery
        ↓
Cycle 1 clinician feedback
        ↓
Cycle 2 revision / pre-review consistency audit
        ↓
resident + evaluator representations
        ↓
Cycle 2 clinician review
```

Historical frozen files remain available for provenance. Cycle 2 does not overwrite them. Corrected and revised files live in the export directories above. VAL-701–VAL-724 were not part of this cycle. Their recovered charts, including the three inconsistent balanced cases, are unchanged.


## Core principle

> The clinical case and the scoring reference are deliberately separated. Residents see the clinical evidence needed to make a discharge decision, but they do not see the intended discharge medication plan. The hidden reference plan is used only for evaluation.

## Developer view of the study sequence

```text
source-backed clinical data
        ↓
clinically coherent case
        ↓
resident-facing clean chart
        ↓
resident determines discharge medication plan
        ↓
hidden reference discharge plan
        ↓
resident response compared with reference
        ↓
errors / agreement / reasoning can be evaluated
```

The same sequence, drawn as the study steps:

```text
Clinical case
    ↓
Resident-facing chart
    ↓
Resident proposes discharge medications
    ↓
Hidden reference discharge plan
    ↓
Comparison / scoring
```

A later experiment may insert an AI recommendation between the resident's first decision and a revised decision. That recommendation is not part of the base case.

```text
Resident initial decision
    ↓
AI recommendation
    ↓
Resident accepts / rejects / revises
    ↓
Final decision
```

Any manipulated AI recommendation is a separate experimental intervention. It is not written into the clinical chart the resident reads first.

## Resident and evaluator views

Two files can describe the same underlying case. They do not expose the same information.

### What each resident-facing case contains

```text
Patient overview
        ↓
Reason for hospitalization
        ↓
History / relevant diagnoses
        ↓
Hospital course
        ↓
Admission and discharge clinical status
        ↓
Home medications
        ↓
Medications used during hospitalization
        ↓
Monitoring / follow-up context
        ↓
Discharge disposition and relevant instructions
        ↓
Resident determines discharge medication plan
```

There is no `Discharge medications` section that hands the resident the answer.

### Resident-facing case

The resident-facing representation includes clinical evidence. It may contain:

- presentation
- diagnoses and history
- hospital course
- home medications
- inpatient medications
- labs and vitals
- relevant treatments
- discharge disposition
- instructions that do not reveal the regimen
- follow-up context

It must not contain:

- a correct discharge medication list
- `reference_discharge_plan`
- expected medication actions
- hidden rationale
- scoring labels
- planted-error metadata

Home and inpatient medication lists are clinical evidence. They are not the answer. The resident still has to decide what should happen at discharge.

### Evaluator representation

The evaluator file is the resident chart plus `reference_discharge_plan`. It is not for study participants.

Where the recovered cases have the information, each reference medication includes the medicine, the action (`continue`, `start`, `stop`, `change`, `hold`, or `restart`), dose, route, frequency, duration, indication, rationale, and any monitoring note stored on that row. The plan also lists monitoring requirements and follow-up requirements when those rows exist.

Newly generated cases, built by `app/services/resident_case.py`, add evaluator-only fields: `required`, `evidence_class`, `supporting_evidence`, `evidence_trace`, and `consistency_errors`. Those fields are not in the recovered 48-case files. `acceptable_alternatives` and `contraindications` exist on newly generated plans and are currently empty lists. `medications_to_stop` is filled only when a reference action is `stop`.

## `reference_discharge_plan`

This object is the hidden reference standard. The example below is the recovered plan for VAL-701, a synthetic heart-failure chart. It is not a real patient.

```json
{
  "medications": [
    {
      "medication": "lisinopril 10 MG Oral Tablet",
      "action": "continue",
      "dose": "10 MG",
      "route": "oral",
      "frequency": "once daily",
      "duration": null,
      "indication": "Essential (primary) hypertension",
      "rationale": "Home therapy is continued through discharge in the clean case.",
      "monitoring": null
    }
  ],
  "monitoring_requirements": [],
  "follow_up_requirements": [
    {
      "item": "Heart-failure clinic follow-up",
      "timing": "7 days",
      "with_service": "cardiology"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `medication` | Drug name as charted |
| `action` | Intended discharge action |
| `dose`, `route`, `frequency` | Intended administration |
| `duration` | Days' supply or course length when the clean chart stored one. Often null |
| `indication` | Diagnosis or purpose stored on the medication row |
| `rationale` | Why the reference records that action. On the recovered set this is often the original generator sentence, not a new narrative |
| `monitoring` | Monitoring text stored on that medication row, or null |
| `monitoring_requirements` | Case-level monitoring tasks. Empty when the clean chart had none |
| `follow_up_requirements` | Follow-up item, timing, and service |

`required`, `medications_to_stop`, `acceptable_alternatives`, and `contraindications` are part of the generator's evaluator document. They are not fields in the recovered VAL-701 file above. Do not assume every export fills them.

The full VAL-701 evaluator file is [exports/clean_balanced_seed_set/VAL-701_evaluator.json](exports/clean_balanced_seed_set/VAL-701_evaluator.json). The matching resident file omits `reference_discharge_plan`.

## Frozen source batches

The registry still lists two active prospective validation datasets. They are the frozen originals that the recovery read. They are not the files to give a resident.

| Case set | Cases | Generation approach | Frozen files |
| --- | ---: | --- | --- |
| [Balanced structured set](data/case_sets/balanced/README.md) | 24 | Balanced structured generation from predefined profiles | `CLINIPROOF_BALANCED_V4`, VAL-701–VAL-724 |
| [Resident-seed-guided set](data/case_sets/seed_guided/README.md) | 24 | Resident-seed-guided generation from six resident-authored archetypes | `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824 |

`CLINIPROOF_BALANCED_V4`, VAL-701 through VAL-724, uses predefined structured clinical profiles: heart failure, atrial fibrillation, hypertension, type 2 diabetes, and pneumonia. Each of the 24 assignments uses a different profile. The counts are a study-design choice. The set is not prevalence-weighted.

`CLINIPROOF_SEEDCASES_V3`, VAL-801 through VAL-824, starts from six resident-provided cases abstracted into archetypes. The VAL charts are not copies of those documents. The six workflows are medication-history uncertainty, acute heart-failure decompensation, endocarditis treated with outpatient parenteral antibiotics, kidney transplant with cytomegalovirus treatment, hip fracture with interruption and resumption of anticoagulation, and gastrointestinal bleeding with anticoagulation holds and restart decisions.

Readable Markdown for the frozen charts remains at [data/case_sets/balanced/readable/all_cases.md](data/case_sets/balanced/readable/all_cases.md) and [data/case_sets/seed_guided/readable/all_cases.md](data/case_sets/seed_guided/readable/all_cases.md). Those pages still show the historical charts, including discharge lists and, where injected, the planted discrepancy. Do not use them as the current resident-facing study set.

Historical validation artifacts are retained for provenance and reproducibility. They should not be used as the current resident-facing study set.

## What this repository studies

CliniProof creates structured synthetic inpatient cases in which residents must use the clinical presentation, hospital course, medication history, laboratory data, treatment response, monitoring needs, and follow-up context to determine an appropriate discharge medication plan.

The central validation question is not whether a planted error can be detected. It is whether the chart contains sufficient and coherent clinical evidence for a resident to make a defensible discharge decision, and whether the hidden reference plan itself is clinically defensible.

The resident reviews the clean inpatient case and independently determines the appropriate discharge medication plan.

The frozen source registry lists two prospective batches, 48 cases in all. The recovered resident-facing export of those same 48 slots is [exports/clean_balanced_seed_set/](exports/clean_balanced_seed_set/AUDIT.md). The recovery audit labels 44 of those files ready for expert review and 4 clinically inconsistent. That count describes the recovered export only. It is not clinician approval, and it is not the Cycle 2 status of VAL-801–VAL-824. None of the 48 recovered files is clinically approved. Cycle 2 is a separate review preparation for the seed-guided identifiers.

OpenAI is optional. It may only reword narrative from facts the structured generator has already chosen. It does not choose diagnoses, medications, doses, or the reference plan. The committed study cases used template wording.

Neither set is a prevalence-weighted sample of hospital discharges. Passing automated validation does not establish clinical validity. Human clinician validation remains required.

## How a clean case is constructed

```text
clinical scenario / resident-derived archetype
        ↓
structured clinical profile
        ↓
synthetic patient encounter
        ↓
clinical course, labs, treatment and medication history
        ↓
clean resident-facing chart
        ↓
internal consistency / evidence-sufficiency checks
        ↓
hidden reference discharge plan
        ↓
clinician validation
        ↓
accepted case
        ↓
later resident assessment
```

Default generation writes one clean case. It does not inject a medication error and does not write a second case.

The historical frozen batches were built differently. After the clean chart passed, the batch plan introduced one discrepancy for most cases and left four controls in each set of 24 unchanged. That step is experimental / legacy / optional and not part of the default resident case pipeline. See [Experimental error injection](#experimental-error-injection).

Balanced structured generation and resident-seed-guided generation are the two labels for how the frozen profiles were chosen. They share terminology, regimens, and validation. They are not two versions of the same batch.

## Generation

The default command generates clean cases. No medication error is injected. No second corrupted case is written. The hidden reference plan is retained on the case for an evaluator export. Pass `--scenario` when you want a family other than the first scenario in `data/bootstrap/scenarios.json` (currently `HF_INPATIENT`).

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --scenario HF_INPATIENT
```

Validate one persisted case:

```bash
clinical-case-generator validate-cases --case-id SYN-000001
```

The generator does not treat product strength as the administered dose and does not assume once daily. Curated regimens live in [data/bootstrap/medication_regimens.json](data/bootstrap/medication_regimens.json). If a real medication has no curated regimen, generation fails rather than inventing a dose.

## Historical error-injection framework

> Earlier validation work used clean controls and deliberately injected medication-reconciliation discrepancies to test the error-injection framework. That design is retained for provenance and experimental tooling, but it is not the current resident-facing study workflow.

### Historical clean controls

The frozen batches mixed unchanged charts, called clean controls, with charts that each received one injected discrepancy. The current resident study does not depend on a clean-control versus error-bearing distinction.

`--inject-error` is experimental / legacy / optional and not part of the default resident case pipeline. Do not use it to generate the resident study set.

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 42 --inject-error --error-category f1_omission
```

It is retained for future experimental work and for the historical validation batches. The flag does not add an error label beside an otherwise clean chart. It changes the chart: a dose, a route, a frequency, a supply, a monitoring task, a follow-up, a restart instruction, or which drug is present at discharge. Restoring a clean case requires the pre-injection source. Deleting metadata is not enough.

The historical categories are documented in [docs/error_taxonomy.md](docs/error_taxonomy.md). Family 1 changes the regimen itself (`f1_omission`, `f1_commission`, `f1_dose_mismatch`, `f1_route_mismatch`, `f1_frequency_mismatch`, `f1_therapeutic_substitution`). Family 2 changes the transition around the list (`f2_monitoring_not_arranged`, `f2_held_med_no_restart_plan`, `f2_insufficient_supply`, `f2_hospital_only_continued`, `f2_inpatient_substitution_not_reverted`, `f2_pending_decision_followup_missing`). A required companion medication omitted (`f2_coprescription_omitted`) is defined conceptually and is not implemented.

### C1 — Clinical plausibility

### C2 — Intended assessment problem

### C3 — Detectability

### C4 — No unintended clinically meaningful problem

### C5 — Difficulty

Those five headings are the ratings printed in the historical Word casebooks for the frozen charts. C1 asks whether the encounter is believable. C2 asks whether a predetermined discrepancy, when one was injected, is actually present. A control should contain none. C3 asks whether a resident could see that historical problem. C4 asks whether a second problem could be mistaken for the answer. C5 is advisory. Accept. Revise. Exclude. are the recommendations in that casebook. They are not a claim that the recovered clean cases have been through that review.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word. The historical casebooks are [the balanced casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx) and [the seed-guided casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx). Do not give those casebooks to a resident. Each one prints a validation reference after C1.

## Recovered balanced study set

[exports/clean_balanced_seed_set/](exports/clean_balanced_seed_set/AUDIT.md) is the current resident-facing export of the original 48 case slots.

- 48 original case slots were recovered.
- No cases were regenerated.
- Original seeds were preserved.
- Original scenarios were preserved.
- Original profiles were preserved.
- The original frozen VAL files were not overwritten.
- Error-bearing cases were recovered from their archived pre-injection clean source.
- Clean controls used their original clean chart.

This table is the recovery audit of `exports/clean_balanced_seed_set/`. It is not the Cycle 2 count for VAL-801–VAL-824, and it is not clinician approval.

| Status | Count |
| --- | ---: |
| Recovered from clean source | 48 |
| Reconstructed from seed | 0 |
| Minor cleanup | 3 |
| Clinically inconsistent | 4 |
| Unrecoverable | 0 |
| Ready for expert review | 44 |

Ready for expert review, in this recovery table, means the injected chart change and the discharge-answer wording are gone, and the automated clinical pass did not find a blocking inconsistency. It does not mean an expert has approved the case.

The full row-by-row record is [exports/clean_balanced_seed_set/AUDIT.md](exports/clean_balanced_seed_set/AUDIT.md).

### Four cases that are not validated study cases in the recovered export

These four remain labeled `CLINICALLY_INCONSISTENT` inside `exports/clean_balanced_seed_set/`. They were not rewritten there, and no replacement was generated. VAL-801 in that export is still the unrepaired chart. The Cycle 2 revision of VAL-801 is a separate file under `exports/ko_revised_cases_v1/`. VAL-709, VAL-711, and VAL-714 were not part of Cycle 2.

| Case | Problem |
| --- | --- |
| VAL-709 | Ibuprofen is stopped without a visible clinical reason |
| VAL-711 | Ibuprofen is stopped without a visible clinical reason |
| VAL-714 | Pantoprazole is associated with hypertension, which is not a supported indication on that chart |
| VAL-801 | Ibuprofen is stopped without a visible clinical reason |

### Three traceable monitoring restorations

VAL-703, VAL-707, and VAL-817 lost the INR monitoring row when historical error injection removed it. The body of that row was not archived. Recovery restored it from two stored facts: the case's own INR laboratory name, and the warfarin-monitoring frequency, trigger, and service text that the generator writes and that remains on the untouched clean control VAL-710. This did not add a new clinical fact. It put back the monitoring task the clean chart had before injection.

## Output directory

```text
exports/clean_balanced_seed_set/
```

| File | Role |
| --- | --- |
| `AUDIT.md` | Seed, scenario, recovery source, cleanup, and final status for each of the 48 cases |
| `VAL-701_resident.json` | Resident-facing chart. No reference plan |
| `VAL-701_evaluator.json` | Same chart plus `reference_discharge_plan` |

The same pair exists for every identifier from VAL-701 through VAL-724 and from VAL-801 through VAL-824. Resident and evaluator files are the same underlying case with different exposure. Do not show the evaluator file to a participant.

## Provenance of a recovered case

```text
original generated clean case
        ↓
archived pre-injection snapshot
        ↓
historical injected variant
        ↓
recovery uses archived clean source
        ↓
resident/evaluator split
```

The recovered set does not come from rerunning the generator. Seeds in `AUDIT.md` are the original assignment seeds. Re-running generation with today's code would not reproduce these files, because the default decision path has changed and because recovery refuses to draw a new case.

A source-backed terminology concept is not automatically a clinically appropriate choice for a particular synthetic patient. Provenance detail is in [docs/provenance.md](docs/provenance.md).

## Case lifecycle

```text
generated
validated
frozen
optionally error-injected for historical experiments
recovered from clean source
resident/evaluator export
expert review
```

Error injection is not required. The default lifecycle stops at a clean case, a hidden reference, and expert review. The optional injection step describes only the historical batches and future experiments.

## Structural validation and clinical validation

### Structural validation

Automated checks can confirm schema completeness, terminology consistency, medication timeline consistency, answer leakage, whether the clinical evidence for a reference decision is visible in the resident chart, evidence sufficiency, and resident/evaluator separation. `tests/test_clean_set_recovery.py` checks that recovery does not modify the frozen resident export.

Those checks do not establish clinical correctness, whether a medicine should actually be restarted, whether an alternative should be accepted, educational appropriateness, or actual learner difficulty. Those require clinician review.

### Clinical validation

A clinician still has to judge whether each medicine has an appropriate indication, whether the discharge action is justified by the chart, whether labs and monitoring fit the medicines, and whether the hidden reference is defensible. More than one regimen can be reasonable. Missing information, contradictions, inappropriate monitoring, and unsafe recommendations are reasons to exclude a case.

> Passing automated tests does not mean a case has passed clinician review.

The recovery audit's "ready for expert review" label on 44 of the 48 recovered files means the injected chart change and the discharge-answer wording are gone, and the automated pass did not find a blocking inconsistency. It does not mean an expert has approved the case. Cycle 2 status for VAL-801–VAL-824 is separate and is not clinical approval either.

## What residents see later

After clinician validation, residents receive the clean resident-facing chart without the hidden discharge reference.

They use the available clinical information to construct their own discharge medication plan.

The hidden clinician-validated plan remains investigator-only and can later support comparison/scoring.

The resident is not asked to locate a deliberately planted chart error.

The study may also collect rationale, confidence, reasoning structure, and a response to later AI advice. Those collection tools are not implemented in this repository. A scoring engine is not implemented here.

## Active validation artifacts

| Artifact | User | Hidden reference? |
| --- | --- | --- |
| [Cycle 2 clinician validation casebook](exports/ko_cycle2_final_validation/CliniProof_Cycle2_Final_Validation.docx) | clinician validator | Yes, after the initial chart assessment |
| Resident-facing case JSON | resident study / developer | No |
| Evaluator case JSON | investigator / scoring | Yes |
| [Cycle 2 audit and manifest](exports/ko_cycle2_final_validation/MANIFEST.md) | investigator | Yes |
| [Historical balanced casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx) | provenance only | Yes |
| [Historical seed-guided casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx) | provenance only | Yes |

Historical validation design — do not use the older casebooks as the active Cycle 2 review package.

## Using the cases in a study

1. Show the resident the clean chart (`*_resident.json`), not the evaluator file.
2. Collect the resident's discharge medication decisions.
3. Optionally collect confidence and reasoning.
4. Compare the response with `reference_discharge_plan` in the evaluator file.
5. Classify differences. A scoring engine for that comparison is not implemented here.
6. Optionally, in a later experiment, introduce an AI recommendation that is not part of the base chart.
7. Collect a revised decision.
8. Analyze changes in accuracy, reliance, confidence, or reasoning.

## Clinician review

Review the recovered resident chart and, separately, the hidden reference. Do not stop at whether the file parses.

Assess:

- clinical coherence and realism
- whether the chart contains enough information to decide
- medication indications
- whether the hidden reference action is defensible
- whether more than one answer could reasonably be accepted
- missing information and contradictions
- inappropriate monitoring
- unsafe recommendations

The four inconsistent cases above should be reviewed as problems, not as cases that already passed.

## Repository structure

```text
app/services/generation.py           default clean-case generator
app/services/resident_case.py       resident chart versus hidden reference plan
app/services/validation.py           structural and coherence checks
app/services/error_injection.py      experimental chart discrepancies; not the default path
app/services/clean_set_recovery.py   rebuilds the 48 resident/evaluator files from frozen sources
app/services/ko_review_sets.py       Cycle 2 review copies for VAL-801–VAL-824
app/services/validation_batch.py     freeze and export of historical VAL batches
tests/test_clean_resident_case.py    clean generation hides the reference and does not inject an error
tests/test_clean_set_recovery.py     recovery leaves frozen files unchanged and restores known clean facts
tests/test_ko_review_sets.py         Cycle 2 packages hide the reference and leave frozen files unchanged
exports/clean_balanced_seed_set/     recovered 48-slot export; not overwritten by Cycle 2
exports/ko_revised_cases_v1/         six cases revised after first-round clinician feedback
    KO_REVISED_CASES_REVIEW.docx
    AUDIT.md
exports/ko_clean_cases_for_review_v1/ clean cases ready for clinician review
    KO_CLEAN_CASES_REVIEW.docx
    AUDIT.md
exports/ko_held_cases_v1/            held audit; currently records zero held cases
    KO_HELD_CASES_AUDIT.md
exports/ko_cycle2_final_validation/   active 24-case clinician validation casebook
    CliniProof_Cycle2_Final_Validation.docx
```

Methods and the directory map are also in [docs/methods.md](docs/methods.md) and [docs/repository_structure.md](docs/repository_structure.md).

## Testing

```bash
pytest
pytest tests/test_clean_resident_case.py
pytest tests/test_clean_set_recovery.py
```

`pytest` runs the full suite. It rebuilds the database schema and will wipe local case rows.

`tests/test_clean_resident_case.py` checks that a default generated case has no injected error, that the resident document omits discharge-context medications and `reference_discharge_plan`, and that the evaluator document still has the reference.

`tests/test_clean_set_recovery.py` checks that the original resident export is unchanged, that pre-injection content is restored (VAL-701 lisinopril remains a continue at 10 MG), that a known injected dose change is reversed (VAL-708 atorvastatin is 40 MG, not the planted 20 MG), and that recovered files are written to a separate directory.

Also used before a code change is considered complete:

```bash
ruff check .
mypy app
python scripts/check_docs.py
```

## LOINC

Laboratory import uses the LOINC FHIR value set at `http://loinc.org/vs`. The older URL `http://loinc.org?fhir_vs` returns 404 and is not the active endpoint. The FHIR base is `https://fhir.loinc.org`.

`LOINC_USERNAME` and `LOINC_PASSWORD` are read from the environment or from a local `.env` file. `.env` is gitignored. Do not commit credentials. Empty LOINC credentials stop laboratory import. They do not stop a checkout of the frozen or recovered cases.

## Environment

Copy `.env.example` to `.env`. The settings the application reads are:

| Variable | Role |
| --- | --- |
| `DATABASE_URL` | PostgreSQL URL. Default in code: `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `LOINC_USERNAME` | LOINC account name. Required for laboratory import |
| `LOINC_PASSWORD` | LOINC account password. Required for laboratory import. Never commit it |
| `OPENAI_API_KEY` | Optional. Empty means template narrative |
| `OPENAI_MODEL` | Optional model name. Default `gpt-5` |
| `SNOMED_BASE_URL` | Unused until a SNOMED ingestion path exists. Leave empty |
| `SNOMED_API_TOKEN` | Unused until a SNOMED ingestion path exists. Leave empty |
| `MIMIC_LOCAL_PATH` | Unused. MIMIC-IV is not ingested. Leave empty |

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
```

`db-init` applies migrations. It does not rewrite committed case files.

## Historical datasets and provenance

Earlier frozen batches are retained under [data/archive/validation_sets/](data/archive/validation_sets/README.md) for reproducibility and provenance. They are not the current study set.

| Historical batch | Archive directory | Historical identifiers |
| --- | --- | --- |
| `CLINIPROOF_TAXONOMY_V1` | `data/archive/validation_sets/CLINIPROOF_TAXONOMY_V1` | historical VAL-201–VAL-224 |
| `CLINIPROOF_BALANCED_V2` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V2` | historical VAL-301–VAL-324 |
| `CLINIPROOF_BALANCED_V3` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V3` | historical VAL-501–VAL-524 |
| `CLINIPROOF_SEEDCASES_V1` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V1` | historical VAL-401–VAL-424 |
| `CLINIPROOF_SEEDCASES_V2` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V2` | historical VAL-601–VAL-624 |

The frozen `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3` directories under `data/case_sets/` are also retained. They are the source of the recovery, not the current resident-facing export.

Teaching charts that are not study cases are in [docs/clinician_walkthrough/README.md](docs/clinician_walkthrough/README.md). TEACH-002 shows one historical injected omission. It is not a recovered study case.

## Limitations

- The cases are synthetic.
- The scenario list is a bounded teaching set.
- Neither original batch is prevalence-weighted.
- A terminology code does not prove a dose is appropriate.
- Companion-drug omission is not implemented.
- Regimens are curated for these profiles. They are not a universal prescribing engine.
- There is no resident-review application and no finished scoring engine in this repository.
- SNOMED CT and MIMIC-IV are not ingested.
- The four inconsistent files inside the recovered 48-slot export are not ready for use as study cases. Cycle 2 does not change those files. Its revised VAL-801 copy is a separate export.

## Licensing

Terminology content is not bundled. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license. LOINC requires a Regenstrief account.
