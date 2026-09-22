# How CliniProof Builds and Validates a Case

This overview is for residents who are curious about the technology, physicians, medical educators, informatics staff, and AI engineers. It explains the system in clinical language first, then names the software pieces.

It discusses **how** cases are made. It does **not** reveal which frozen `VAL-201`–`VAL-224` case contains which assessment target.

Status: machine-validated synthetic resident-review cases pending clinician validation.

## A. Clinical overview

CliniProof creates synthetic inpatient medication-reconciliation cases with a known assessment target.

**Medication reconciliation** is the clinical work of making a best-possible medication history, comparing it with inpatient orders and the discharge list, and ensuring that holds, stops, continuations, substitutions, supplies, monitoring, and follow-up are explicit and safe.

Some cases are **clean controls**: the chart is left without an intentionally planted assessment problem, so reviewers and residents can also see an intact reconciliation. Other cases receive **exactly one** planned problem after the clean chart has already passed automated checks.

**Family 1** problems are discrepancies on the medication lists themselves (a drug missing at discharge, an extra drug, or an unexplained change in dose, route, frequency, or product).

**Family 2** problems are transition-of-care gaps. The discharge medication identity may be unchanged; what is missing is a required companion action such as INR monitoring, a restart plan for a held drug, enough days’ supply, stopping a hospital-only drug, reverting a temporary substitute, or arranging follow-up for an unresolved decision.

Do not identify Family 2 solely by comparing home versus discharge lists.

### Implemented categories

Each category has a clinical name and a canonical identifier used in software and investigator materials.

#### Family 1

##### Medication omitted at discharge

`f1_omission`

**Clinical explanation.** A medication intended to continue after hospitalization is absent from the discharge medication list without a documented reason.

**Technical concept.** This is a Family 1 medication-transition discrepancy. The clean expected discharge medication is present before assessment modification and removed from the final discharge list.

##### Medication inappropriately added or continued

`f1_commission`

**Clinical explanation.** A medication that should not continue (for example, one held or stopped) appears on the discharge list.

**Technical concept.** The injector adds or retains a discharge-list entry that the clean case had omitted for a documented reason.

##### Unexplained dose discrepancy

`f1_dose_mismatch`

The discharge dose differs from the intended continued dose without explanation. The injector changes only that field on the discharge entry.

##### Unexplained route discrepancy

`f1_route_mismatch`

The discharge route differs from the intended continued route without explanation.

##### Unexplained frequency discrepancy

`f1_frequency_mismatch`

The discharge frequency differs from the intended continued frequency without explanation.

##### Unexplained therapeutic substitution

`f1_therapeutic_substitution`

The discharge list shows a same-class substitute instead of the intended continued product, without documenting an intentional switch.

#### Family 2

##### Required monitoring not arranged

`f2_monitoring_not_arranged`

**Clinical explanation.** Warfarin is continued at discharge, but outpatient INR monitoring has not been arranged.

**Technical concept.** In CliniProof this is classified as a Family 2 transition-of-care gap because the medication order itself remains unchanged; the missing element is the required follow-up action.

**Technical implementation.** Canonical category: `f2_monitoring_not_arranged`. The injector removes the expected monitoring record after the clean case passes validation. The medication itself remains unchanged.

##### Held medication without a restart plan

`f2_held_med_no_restart_plan`

The original medication is intentionally stopped during hospitalization for a legitimate temporary reason, but the discharge documentation does not tell the patient or outpatient clinician when or under what conditions it should be resumed.

##### Insufficient medication supply

`f2_insufficient_supply`

Days’ supply is shortened so that treatment cannot last until planned follow-up.

##### Hospital-only medication continued after discharge

`f2_hospital_only_continued`

A drug started for an inpatient-only indication remains on the discharge list.

##### Temporary inpatient substitution not addressed at discharge

`f2_inpatient_substitution_not_reverted`

A temporary inpatient substitute is left in place without reverting to home therapy or documenting an intentional decision.

##### Follow-up missing for an unresolved treatment decision

`f2_pending_decision_followup_missing`

A pending therapeutic decision has no arranged follow-up.

##### Required companion medication omitted (not implemented)

`f2_coprescription_omitted`

Specified conceptually. This freeze does not include it (`not_yet_implementable`).

## B. Source-backed versus synthetic information

**Source-backed concept ≠ real patient data.** An RXCUI for warfarin means the *concept* came from RxNorm, not that a real patient was taking warfarin.

| Type of information | Example | How it is obtained |
| --- | --- | --- |
| Medication concept | Warfarin | RxNorm-backed |
| Diagnosis concept | Heart failure | ICD-10-CM-backed |
| Laboratory test | Creatinine | LOINC-backed |
| Unit | mmol/L | UCUM/LOINC-backed |
| Age | 72 | Synthetic |
| Blood pressure | 128/74 | Synthetic |
| Lab result | Creatinine 1.3 | Synthetic patient value |
| Clinical narrative | HPI | Template or optional LLM wording |
| Assessment discrepancy | Missing monitoring | Deterministically introduced |

Official source ranking can yield technically valid but clinically atypical formulations or units (for example, a solution or gel, or an SI laboratory unit). Those oddities are left visible for clinician review. They are not silently rewritten.

## C. Generation pipeline

```
Clinical scenario
→ terminology resolution
→ clean synthetic patient
→ rule checks
→ clean validation
→ assessment target eligibility
→ controlled error introduction
→ post-error validation
→ blinded resident export
→ clinician validation
```

**Clinical scenario.** An operator chooses an inpatient teaching skeleton (specialty, age band, diagnosis and medication search phrases, allowed assessment categories).

**Terminology resolution.** Search phrases are matched to identifiers already stored from official services (RxNorm, ICD-10-CM, LOINC, UCUM, and related sources). The generator does not invent codes.

**Clean synthetic patient.** Demographics, vitals, laboratory *values*, medication lists, notes, and follow-up are assembled into a structured chart that is internally consistent with the scenario and the stored concepts.

**Rule checks.** A small set of source-backed IF/THEN constraints (only those with attached DailyMed or RxClass evidence) is applied. This is not a complete clinical guideline.

**Clean validation.** Software checks structure, that every coded concept exists in local reference tables, that hard rules hold, and that the clean chart does not already contain the assessment target that would later be planted.

**Assessment target eligibility.** If the plan requests a category, the case must actually be eligible for that category. If not, generation **stops**. Another category is not silently substituted.

**Controlled error introduction.** For assessment cases, exactly one planned change is applied. Clean controls skip this step.

**Post-error validation.** Software checks that the intended target is now present, that required evidence remains visible, and that a second assessment target was not introduced.

**Blinded resident export.** Residents receive the chart without family, category, trigger metadata, or answer keys.

**Clinician validation.** Humans apply C1–C5. Automated checks cannot certify realism or educational appropriateness.

## D. What OpenAI does

OpenAI is **optional**.

It may word narrative text (chief complaint, HPI, admission note) from **already selected** clinical facts (age, sex, diagnosis name, symptom names, medication names, and a template seed).

It does **not** choose diagnoses, drugs, terminology codes, clinical rules, error categories, or answer keys.

The current frozen validation set uses **template narrative rather than OpenAI** (`freeze-validation-batch` sets `use_openai=False`).

Raw patient-source rows are never sent to a language model.

## E. Why machine validation is not clinical validation

Software can verify:

- JSON/schema structure and required sections
- that coded medications, diagnoses, and labs exist in local terminology tables
- a limited set of implemented source-backed rules
- that the requested assessment category was eligible and that the injected state matches it
- that the resident export does not contain answer-key fields

Software cannot verify:

- whether the chart is clinically realistic
- whether therapy is complete or guideline-concordant
- whether the item is educationally appropriate
- how difficult residents will find it in practice

Until clinicians finish review, every generated record remains: **machine-validated synthetic resident-review cases pending clinician validation**.

## F. Technical implementation

Physicians can stop here. The table below is for engineers and informatics staff.

| Function | Implementation |
| --- | --- |
| Scenario definitions | `data/bootstrap/scenarios.json` |
| Terminology bootstrap | `app/services/bootstrap.py` |
| Case generation | `app/services/generation.py` |
| Error taxonomy | `app/services/error_taxonomy.py` |
| Error injection | `app/services/error_injection.py` |
| Validation | `app/services/validation.py` |
| Freeze/export | `app/services/validation_batch.py` |
| Optional narrative LLM | `app/openai/narrative.py` |
| Readable Markdown views | `app/services/readable_packets.py` |

Canonical families are `family_1`, `family_2`, and `none` (clean control). Canonical categories are the `f1_*` and `f2_*` identifiers listed above. Unknown names fail rather than being aliased.

Readable packets are regenerated with `python scripts/build_readable_validation_packets.py` and do not rewrite frozen JSON.
