# Generation 2 methodology

Generation 2 is a new experimental way to build clean discharge-reconciliation cases. Generation 1, the resident-archetype series VAL-801–VAL-824, stays in place. This note does not replace [methodology.md](methodology.md). It does not report a comparison result, and it does not say that Generation 2 is better.

## Why Synthea is being used

Generation 1 starts from six resident-authored workflows and writes a hospitalization around each profile. Round 1 review found that a recognizable diagnosis was sometimes not enough for a discharge decision: the baseline was thin, the reason for deterioration was missing, the work-up that established a diagnosis was missing, and medication changes were not always supported by visible facts.

Generation 2 asks a different construction question. Start with a longitudinal synthetic patient who already has an age, a sex, chronic conditions, and outpatient medicines. Then build one inpatient episode whose causal chain is complete enough for an internal-medicine resident to decide the discharge medication plan. The later comparison this makes possible is clinical plausibility, information sufficiency, internal consistency, diagnostic and work-up sufficiency, medication-decision sufficiency, reference-plan defensibility, expected difficulty, and whether revision is required. That comparison is not performed here.

## What each system contributes

Synthea contributes the longitudinal patient substrate: demographics, chronic and prior diagnoses, outpatient medication products, recent encounters, selected observations, procedures, and care-plan titles when those resources are present. The pinned upstream commit, seed, population size, geography, and FHIR R4 export are recorded in [config/synthea.yml](../config/synthea.yml). Bulk FHIR stays outside Git.

CliniProof contributes the controlled inpatient episode. Synthea is not treated as a complete inpatient reasoning simulator. Acute precipitants, hospital laboratories, imaging interpretations, medication holds, and responses are `cliniproof_episode_generated` unless a value was actually present in the extract.

## Pipeline

```text
Synthea population
        ↓
eligible longitudinal patient
        ↓
CliniProof scenario
        ↓
causal inpatient trajectory
        ↓
Round-1-informed clinical sufficiency gate
        ↓
medication-decision evidence audit
        ↓
clean resident-facing case
        ↓
hidden evidence-backed reference
        ↓
candidate selection
        ↓
clinician validation
```

The resident task is: given this hospitalization, determine the appropriate discharge medication plan. Phase 1 therefore builds clean cases only. It does not inject a medication error, plant an omission, or show a finished discharge list, an error label, or a scoring label.

## Eligibility

A population of 1000 living patients is generated with seed `20261008` and reference date `20261008` in Massachusetts. Deceased exports are excluded. Each family has an explicit rule in `app/services/synthea_eligibility.py` and in [discharge_scenarios_g2.json](../data/bootstrap/discharge_scenarios_g2.json).

Heart-failure eligibility prefers an active Synthea heart-failure condition. That living-adult pool is small, because many Synthea heart-failure lives have already ended. The scenario also accepts a compatible cardiovascular history plus a curated cardiovascular medicine. The inpatient episode then establishes acute heart failure during the stay and does not relabel the patient as having had Synthea heart failure.

Endocarditis was not present in this Synthea population. Eligibility is baseline context only. The infection is episode-generated.

Transplant eligibility requires a Synthea renal-transplant history and extended-release tacrolimus that matches a curated once-daily regimen. Mycophenolate is not added because it is common. Valganciclovir is not a home medicine unless a variant explicitly includes prior prophylaxis, and that prophylaxis is labeled episode-generated.

Gastrointestinal bleeding and hip fracture require curated warfarin plus a longitudinal anticoagulation indication. Hip fracture also requires age 65 or older. Other anticoagulants are not relabeled as warfarin.

If a family cannot fill four passing cases, the build stops. Constraints are not silently loosened.

## Inpatient trajectory

Every episode is a chain: baseline, acute change, precipitant or an evaluation that did not find one, presentation, work-up, diagnosis, treatment, physiologic response, medication consequences, discharge readiness, and an unsigned discharge-medication question. Important diagnoses are named after the test that establishes them. Endocarditis and cytomegalovirus disease are not the presenting labels.

Laboratories and vital signs are trajectories. A diuresis case must lose weight. An acute-kidney-injury case must show a peak and a later value no higher than that peak. A bleeding case must show a hemoglobin nadir and a later value at or above it. An infection is not required to have fever.

Medication state is temporal: home, continued, held, hospital-only, new, restarted, or discontinued. A change stores a trigger, the decision, the visible evidence, and the final state. Hospital-only medicines stop. A held medicine has a final disposition. Doses come from [medication_regimens.json](../data/bootstrap/medication_regimens.json). A Synthea product is charted only when the curated dose is the strength named on that product. Product strength is not otherwise copied into the dose. RxNorm codes are copied from the bundle. LOINC and ICD-10-CM codes used for episode facts are limited to a table checked against NLM Clinical Tables.

## Round 1 design requirements

The first clinician review is the source of the gates, not an endorsement of Generation 2. The gates require a visible baseline, a clear acute change, a sufficient precipitant, a diagnostic work-up, a hospital course, visible treatment, a visible response, coherent physiology, supported medication decisions, valid chronology, discharge readiness, and monitoring with follow-up. A failure rejects or blocks the candidate. It does not add a cosmetic sentence after the fact.

The concrete Generation 1 patterns those gates are meant to prevent are a delirium story without baseline cognition, a heart-failure story that is only “exacerbation, diuresis, improved,” an endocarditis label without cultures and echocardiography, and a cytomegalovirus colitis label that appears before the work-up. New patients are not copies of VAL-801–VAL-824.

## Hidden reference

The reference is derived after the resident chart exists. For each relevant medicine the question is what discharge action the visible case supports: continue, stop, restart, hold, dose change, or new start. Each action stores the regimen, the rationale, resident-visible fact identifiers, monitoring, and follow-up. When more than one action is defensible, `acceptable_alternatives` records the other action, the condition, and the reason. A reasonable alternative is not marked wrong because the generator preferred another action.

Terminology codes do not establish that a decision is appropriate. Guidelines cited in the scenario file constrain the shape of the work-up and the monitoring. They are not the source of a patient’s creatinine.

## Selection

At least eight candidate episodes are attempted in each family, using distinct variants and, when the pool allows, a second patient per variant. Exact or high-similarity structural fingerprints are rejected. Different age or sex alone is not treated as diversity. The final pilot keeps four variants per family, 24 cases. Automated checks can set `ready_for_clinician_review`. They cannot set clinical validation. The casebook uses the same C1–C5 clean-case instrument as Generation 1 and states that clinician review is still required.

## What this phase does not do

It does not call OpenAI. It does not send Synthea records or Generation 2 charts to a language model. It does not use MIMIC. It does not assign VAL identifiers. It does not merge itself.
