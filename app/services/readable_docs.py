"""Static Markdown for derived CliniProof clinician/technical packets.

These strings are copied into data/validation/readable/ by the generator.
They discuss mechanisms generically and must not map a VAL ID to a hidden target.
"""

from __future__ import annotations

ABOUT_CASE_DATA = """## About the case data

This is a synthetic case created for medication-reconciliation assessment.

Medication, diagnosis, and laboratory concepts are drawn from established clinical terminology sources. Patient-specific values and the clinical scenario are synthetic.

The case has undergone automated checks for structure, terminology consistency, and the implemented clinical constraints. These checks do not establish clinical validity.
"""

ALL_CASES_HEADER = """# CliniProof Clinical Case Set

## CLINIPROOF_TAXONOMY_V1

This document is intended for residents, clinicians, medical educators, and clinical informatics collaborators who want to review the clinical cases without reading the underlying JSON representation.

Status: machine-validated synthetic resident-review cases pending clinician validation.

Cases: VAL-201 through VAL-224

Total: 24

This file contains resident-visible clinical content only. It does not identify which cases contain an assessment problem, if any, and it does not include investigator answer keys.

## How these cases are created

These cases are synthetic rather than extracted from individual patient records.

Clinical concepts such as medication names, diagnoses, and laboratory tests are linked to established terminology sources. Patient-specific values such as age, vital signs, and laboratory results are synthetically generated.

The system first creates a structured case and checks its terminology, internal structure, and a limited set of predefined clinical rules. For assessment cases, a specific medication-reconciliation problem may then be introduced in a controlled way. Human clinician review is required because these automated checks cannot establish that a case is clinically realistic or educationally appropriate.

In outline:

1. A clinical scenario is selected (for example, an inpatient heart-failure or pneumonia theme).
2. Medication, diagnosis, and laboratory concepts are resolved against established terminology sources already stored locally.
3. A synthetic patient encounter is constructed (demographics, vitals, laboratory values, medication lists, notes, and follow-up).
4. Automated clinical and structural checks are applied to that “clean” case.
5. For assessment cases, a predefined medication-reconciliation problem may be introduced. Some cases are left unchanged as clean controls. This file does not say which is which.
6. The case is checked again after any assessment modification.
7. Resident-facing and investigator-facing versions are separated. Residents receive the chart. Investigators receive the concealed assessment target separately.
8. Clinicians review the resulting cases before educational use.

Medication reconciliation, in ordinary clinical terms, is the process of comparing what the patient was taking before admission, what was given in the hospital, and what is prescribed at discharge, then ensuring that intended continuations, holds, stops, and follow-up actions are explicit.

Review each case as you would a discharge chart: is the patient story coherent, and can you complete a careful medication-reconciliation review from the documents provided?
"""

PLAUSIBILITY_HEADER = """# CliniProof clinical-plausibility packet

## CLINIPROOF_TAXONOMY_V1

This packet is for an independent clinician assessing **clinical plausibility (C1)** without seeing the concealed assessment target.

It is intended for residents, attending physicians, and medical educators. It contains the resident-visible chart for each case, followed by the C1 form. It does **not** reveal whether a given case is a clean control, whether an assessment problem was introduced, which medication is involved, or what the expected action would be.

These cases are synthetic rather than extracted from individual patient records. Clinical concepts such as medication names, diagnoses, and laboratory tests are linked to established terminology sources. Patient-specific values such as age, vital signs, and laboratory results are synthetically generated.

The system first creates a structured case and checks its terminology, internal structure, and a limited set of predefined clinical rules. For assessment cases, a specific medication-reconciliation problem may then be introduced in a controlled way. Human clinician review is required because these automated checks cannot establish that a case is clinically realistic or educationally appropriate.

**How to rate C1.** Ask whether this chart could reasonably represent a patient encountered in the stated clinical setting. Clinical plausibility is not the same as optimal management or complete guideline concordance. Comment on the exact field or issue for any domain rated below 3.

Full criterion definitions: [`validation_rubric.md`](validation_rubric.md). Broader system explanation: [`how_cliniproof_works.md`](how_cliniproof_works.md).

Status: machine-validated synthetic resident-review cases pending clinician validation.
"""

INVESTIGATOR_HEADER = """# Investigator / Clinical Validator Copy

This document contains the intended assessment target for each case and must not be provided to resident participants.

**INVESTIGATOR / VALIDATOR ONLY — DO NOT DISTRIBUTE TO RESIDENT PARTICIPANTS**

Use this packet for primary expert raters completing the full CliniProof C1–C5 validation rubric. Each case appears as:

1. The resident-visible clinical chart (same content residents see).
2. The intended assessment issue, with a clinical label and the canonical CliniProof identifier.
3. The C1–C5 rating forms.

Rubric: [`validation_rubric.md`](validation_rubric.md). System overview: [`how_cliniproof_works.md`](how_cliniproof_works.md). Implementation notes: [`developer_notes.md`](developer_notes.md).

Status: machine-validated synthetic resident-review cases pending clinician validation.
"""

READABLE_INDEX_MD = """# Readable CliniProof review materials

These files are derived human-readable views of frozen `CLINIPROOF_TAXONOMY_V1` (`VAL-201`–`VAL-224`). They do **not** replace the frozen JSON. They were generated by `scripts/build_readable_validation_packets.py` from:

- [`../resident_validation_cases.json`](../resident_validation_cases.json) for all clinician-visible patient information
- [`../investigator_answer_key.json`](../investigator_answer_key.json) only for the investigator packet

Status: machine-validated synthetic resident-review cases pending clinician validation.

Regenerate (from the repository root; does not modify frozen JSON):

```bash
python scripts/build_readable_validation_packets.py
```

## Where should I start?

| If you are... | Start here |
| --- | --- |
| Resident or clinician reviewing cases | [`all_cases.md`](all_cases.md) |
| Clinician validating clinical plausibility | [`plausibility_only_packet.md`](plausibility_only_packet.md) |
| Investigator / expert validator | [`clinician_validation_packet.md`](clinician_validation_packet.md) |
| Medical educator reviewing the framework | [`validation_rubric.md`](validation_rubric.md) |
| Clinician or resident curious how CliniProof works | [`how_cliniproof_works.md`](how_cliniproof_works.md) |
| Clinical informatics / AI engineer | [`developer_notes.md`](developer_notes.md) |

## Safe for residents and plausibility-only review

These files contain resident-visible case content and generic explanations of how cases are made. They do **not** include planted-error family, category, trigger labels, control status, or per-case answer keys.

| File | Contents |
| --- | --- |
| [`all_cases.md`](all_cases.md) | All 24 readable cases, sequential |
| [`plausibility_only_packet.md`](plausibility_only_packet.md) | Each readable case followed by the C1 assessment form |
| [`cases/`](cases/) | One page per case, VAL-201 through VAL-224 |
| [`how_cliniproof_works.md`](how_cliniproof_works.md) | Clinical-to-technical overview (no per-case answers) |
| [`developer_notes.md`](developer_notes.md) | Informatics/engineering notes (generic mechanisms only) |
| [`validation_rubric.md`](validation_rubric.md) | C1–C5 rubric (no per-case answers) |

## Investigator / validator only

| File | Contents |
| --- | --- |
| [`clinician_validation_packet.md`](clinician_validation_packet.md) | Readable case + concealed target + C1–C5 forms |

**Do not provide `clinician_validation_packet.md` to resident study participants.**
"""

VALIDATION_RUBRIC_MD = """# CliniProof clinician-validation rubric

Status: machine-validated synthetic resident-review cases pending clinician validation.

This rubric is for clinician and investigator review of frozen `CLINIPROOF_TAXONOMY_V1` cases (`VAL-201`–`VAL-224`). The five criteria serve different purposes.

- **C1 (clinical plausibility)** can be completed from the resident-visible chart alone. It is *fixable*: a case that is implausible should be revised rather than scored as an assessment item.
- **C2–C4** are *hard gates*. They require the concealed assessment specification (investigator packet). A failure means the case cannot be used against its intended answer key until it is fixed or retired.
- **C5 (difficulty)** is *advisory*. It must not by itself reject a case.

`f2_coprescription_omitted` is not represented in this frozen batch and remains `not_yet_implementable`.

## Family-specific guidance for C2–C4

C2–C4 must account for different structures.

### Family 1 — medication-list / transition discrepancies

These generally involve comparing home, inpatient, and discharge medication lists.

#### Medication omitted at discharge

`f1_omission`

A medication intended to continue after hospitalization is absent from the discharge medication list without a documented reason.

#### Medication inappropriately added or continued

`f1_commission`

A medication that should not be on the discharge list (for example, one that was held or stopped) appears there without a documented decision to continue it.

#### Unexplained dose discrepancy

`f1_dose_mismatch`

The discharge dose differs from the intended continued dose without an explanation.

#### Unexplained route discrepancy

`f1_route_mismatch`

The discharge route differs from the intended continued route without an explanation.

#### Unexplained frequency discrepancy

`f1_frequency_mismatch`

The discharge frequency differs from the intended continued frequency without an explanation.

#### Unexplained therapeutic substitution

`f1_therapeutic_substitution`

The discharge list replaces an intended continued medication with another agent of the same class without documenting an intentional switch.

### Family 2 — transition-of-care gaps

These may involve absence of monitoring, follow-up, supply, restart planning, or another transition action. Do **not** identify Family 2 solely by comparing medication lists. For Family 2, the trigger or precondition must be visible, and the missing companion action is the specified target.

#### Required monitoring not arranged

`f2_monitoring_not_arranged`

**Clinical explanation.** Warfarin is continued at discharge, but outpatient INR monitoring has not been arranged.

**Technical concept.** In CliniProof this is classified as a Family 2 transition-of-care gap because the medication order itself remains unchanged; the missing element is the required follow-up action.

#### Held medication without a restart plan

`f2_held_med_no_restart_plan`

A home medication is intentionally held in the hospital for a legitimate temporary reason, but discharge documentation does not say when or under what conditions it should be resumed.

#### Insufficient medication supply

`f2_insufficient_supply`

Days’ supply at discharge is too short to last until the planned follow-up.

#### Hospital-only medication continued after discharge

`f2_hospital_only_continued`

A medication started for an inpatient-only indication is still on the discharge list.

#### Temporary inpatient substitution not addressed at discharge

`f2_inpatient_substitution_not_reverted`

A temporary inpatient substitute was used, but discharge does not revert to home therapy or document an intentional decision to continue the substitute.

#### Follow-up missing for an unresolved treatment decision

`f2_pending_decision_followup_missing`

A treatment decision was left pending, but no follow-up is arranged to resolve it.

#### Required companion medication omitted (not in this freeze)

`f2_coprescription_omitted`

Specified conceptually. Not currently implementable because no source-backed companion-prescription rule exists in this repository.

## Criterion 1 — Clinical plausibility — fixable

### Clinical question

“Apart from any intentionally planted reconciliation discrepancy, could this case reasonably represent a patient encountered in the stated clinical setting?”

### Reviewer should look for

Assess these domains independently:

1. Presentation and demographics
2. Diagnosis-presentation coherence
3. Vital signs
4. Laboratory findings
5. Medication regimen
6. Hospital course
7. Cross-document consistency
8. Discharge context and follow-up

Clinical plausibility is **not** synonymous with optimal management or complete guideline concordance. Unusual but source-backed formulations or units should be recorded if they undermine credibility; they should not be silently “corrected” in the frozen case.

### Scale (each domain)

- **4 — Fully plausible.** No clinically meaningful concern.
- **3 — Plausible with minor concern.** A minor issue is present but would not materially alter interpretation.
- **2 — Questionable.** A clinically meaningful inconsistency or implausibility is present and the case requires revision.
- **1 — Implausible.** A major contradiction or unrealistic feature prevents the case from representing a credible inpatient encounter.

### Result

Global judgment: Yes / No.

**C1 pass:** all clinically relevant domains ≥ 3 **and** global judgment = Yes.

**C1 revise:** any domain ≤ 2 **or** global judgment = No.

Require comments identifying the exact field or issue for any rating below 3.

### Technical interpretation

C1 is a clinical-realism gate on the resident-visible export. It does not inspect `error_family` / `error_category`. Software already checked schema, terminology identifiers, and implemented rules; C1 asks whether a physician still finds the chart coherent.

## Criterion 2 — Intended error present and correctly classified — hard gate

### Clinical question

“Is the intended medication-reconciliation problem actually present in this chart, and is it the problem the specification claims?”

### Reviewer should look for

- Is the intended discrepancy or gap actually present?
- Is it correctly classified (Family 1 list discrepancy versus Family 2 transition gap, and the specific category)?
- Does the investigator specification describe what is actually visible in the case?

### Result

Pass / Fail.

A failure means the case cannot be scored against its intended answer key.

### Technical interpretation

This is fidelity of the deterministic injection to the planned canonical category. Planned category, injected `kind`, and answer-key `error_category` must describe the same visible target.

## Criterion 3 — Detectability from documents alone — hard gate

### Clinical question

“Could a resident identify and resolve the intended problem using only the information available in this case?”

### Reviewer should look for

- required clinical evidence is present
- information is not contradictory
- no critical information is withheld
- wording does not accidentally reveal the answer (cueing)
- for Family 2: the trigger or precondition is visible and unambiguous

### Result

Pass / Fail.

Comment on evidence location, ambiguity, missing information, and cueing.

### Technical interpretation

This corresponds to evidentiary sufficiency and cue integrity in the CliniProof assessment model. The resident export must be sufficient without investigator fields.

## Criterion 4 — Absence of unintended errors — hard gate

### Clinical question

“Is there any additional clinically meaningful medication-reconciliation discrepancy or transition-of-care gap beyond the specified target?”

### Reviewer should look for

This must be assessed by **active hunt**. Do not merely record errors that happen to be noticed. List any additional possible error and its severity or importance.

### Result

Pass / Fail.

### Technical interpretation

Error isolation: exactly one intended assessment target on error-bearing cases, zero on clean controls. Unintended second targets make the answer key unusable.

## Criterion 5 — Difficulty for target learner — advisory

### Clinical question

“How difficult would this item be for an internal medicine resident?”

### Reviewer should look for

A provisional expert estimate: Easy / Moderate / Hard / Outlier / inappropriate.

### Result

Advisory only. Difficulty is ultimately an empirical property to be calibrated after resident administration. C5 alone should not reject a case.

### Technical interpretation

`difficulty_a_priori` in the answer key is optional metadata, not a software-computed score.

## Final disposition

- Accept
- Revise and re-rate
- Regenerate / retire
- Adjudication required
"""

HOW_CLINIPROOF_WORKS_MD = """# How CliniProof Builds and Validates a Case

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
"""

DEVELOPER_NOTES_MD = """# CliniProof Implementation Notes for Clinical Informatics and AI Engineering

This note assumes you understand software engineering and may not have a clinical training background. It translates the medical objective into the modules that implement it.

It explains **mechanisms**. It does **not** map any frozen `VAL-201`–`VAL-224` identifier to a hidden assessment target. That mapping exists only in investigator-only files.

Status: machine-validated synthetic resident-review cases pending clinician validation.

## Clinical objective

Hospitals reconcile medications at admission and discharge so that intended home therapy is neither dropped nor continued unsafely, and so that required monitoring and follow-up actually occur.

CliniProof builds **synthetic** inpatient charts for that task. Each assessment item has a **known target** chosen before generation, not discovered afterwards by a model. Residents see a chart. Investigators see the target. Human clinicians still decide whether the chart is believable enough to use.

## Why canonical vocabularies are used

If the case said only “a heart-failure pill,” reviewers could not tell which product was meant, and software could not check rules. Official vocabularies give citable identifiers:

- **RxNorm (RXCUI)** for medications
- **ICD-10-CM** for diagnoses
- **LOINC** for laboratory *tests*
- **UCUM** for units

Those identifiers are stored only after an official service returns them, with provenance (`source_system`, `source_version`, `retrieved_at`). The generator never invents a code. SNOMED CT is not ingested here; SNOMED fields stay empty rather than being fabricated.

## Source-backed versus synthetic

| Layer | Meaning |
| --- | --- |
| Source-backed concept | The *type* of thing (warfarin as an RXCUI, creatinine as a LOINC) came from an official terminology |
| Synthetic value | The *patient-specific number or story* (age 72, creatinine 1.3, the HPI sentences) was generated |
| Deterministic assessment change | After the clean chart passed checks, software applied one planned edit |

A source-backed warfarin concept is **not** evidence that a real patient was taking warfarin.

## Scenario structure

`data/bootstrap/scenarios.json` holds teaching skeletons: specialty, age band, search phrases for diagnoses, symptoms, medications, labs, and which canonical assessment categories are allowed. Matching happens against **already bootstrapped** `ref_*` rows (`app/services/bootstrap.py`), not against live free text.

## Clean-case concept

Generation (`app/services/generation.py`) first builds a **clean** structured encounter: demographics, presentation, medications in three contexts (home, inpatient, discharge), labs, vitals, notes, monitoring, follow-up, instructions. “Clean” means the chart should not already contain the assessment target that the plan might later introduce.

A small rules engine (`app/services/rules.py`) applies only conditionals that have attached DailyMed or RxClass evidence. There are few such rules. They are not a complete specialty guideline.

## Family 1 versus Family 2

Identifiers live in `app/services/error_taxonomy.py`.

**Family 1 (`family_1`)** — the discharge *list* is wrong relative to intended continuation.

| Clinical meaning | Identifier |
| --- | --- |
| Medication omitted at discharge | `f1_omission` |
| Medication inappropriately added or continued | `f1_commission` |
| Unexplained dose discrepancy | `f1_dose_mismatch` |
| Unexplained route discrepancy | `f1_route_mismatch` |
| Unexplained frequency discrepancy | `f1_frequency_mismatch` |
| Unexplained therapeutic substitution | `f1_therapeutic_substitution` |

**Family 2 (`family_2`)** — a required *transition action* is missing; the continued-drug identity may be unchanged.

| Clinical meaning | Identifier |
| --- | --- |
| Required monitoring not arranged | `f2_monitoring_not_arranged` |
| Held medication without a restart plan | `f2_held_med_no_restart_plan` |
| Insufficient medication supply | `f2_insufficient_supply` |
| Hospital-only medication continued after discharge | `f2_hospital_only_continued` |
| Temporary inpatient substitution not addressed at discharge | `f2_inpatient_substitution_not_reverted` |
| Follow-up missing for an unresolved treatment decision | `f2_pending_decision_followup_missing` |
| Required companion medication omitted | `f2_coprescription_omitted` (specified, `not_yet_implementable`) |

**Held medication without restart plan** means the original medication is intentionally stopped during hospitalization for a legitimate temporary reason, but the discharge documentation does not tell the patient or outpatient clinician when or under what conditions it should be resumed. That maps to `f2_held_med_no_restart_plan`.

**Required monitoring not arranged** means, for example, warfarin continues at discharge but outpatient INR monitoring was not scheduled. That maps to `f2_monitoring_not_arranged`. The medication row stays; the monitoring record is what changes.

Do not implement Family 2 detection as “diff the three medication lists.”

## Eligibility, injection, and no fallback

The freeze plan names `error_family` and `error_category` **before** generation (`data/validation/batch_plan.json`).

`app/services/error_taxonomy.py` decides whether the clean case is **eligible** for that category (for example, there is a continued discharge drug to omit, or a monitoring-dependency rule matches).

`app/services/error_injection.py` then applies the exact edit, or skips injection for a clean control (`none`).

If the category is unknown, ineligible, or `not_yet_implementable`, freeze **aborts**. It does not pick a different error. An LLM never chooses the category.

## Clean state and injected state

The investigator answer key stores both:

- **Clean expected state** — what the field was after clean validation (for example, the omitted drug `present` on the discharge list)
- **Injected state** — what residents see after the edit (for example, `absent`)

Residents must not receive these fields. The readable investigator packet is the human view of the same concealed specification.

## Machine validation

`app/services/validation.py` and freeze-time checks in `app/services/validation_batch.py` cover structure, terminology integrity, implemented rules, category eligibility, the expected state transition, answer-key consistency, isolation of a second target, and leak checks on the resident export.

They do **not** establish clinical validity.

## Resident blinding

The resident JSON omits answer-key objects, internal `SYN-*` generation identifiers, family/category fields, trigger metadata, and clean/injected state. Readable files `all_cases.md`, `plausibility_only_packet.md`, and `cases/VAL-*.md` are derived only from that blinded export.

## Freeze immutability and provenance

Frozen `CLINIPROOF_TAXONOMY_V1` files under `data/validation/` are the study source of truth. Regenerating live terminology from APIs is **not** expected to reproduce bit-identical JSON. Readable Markdown is allowed to be regenerated from those frozen files; the frozen files themselves must not be rewritten to “improve” clinical content.

Each frozen assignment records scenario, seed, family, category, source-version snapshots, and validation statuses in the investigator key and manifest.

## Optional narrative LLM

`app/openai/narrative.py` may reword admission prose from already chosen names. It is not a case generator. The committed freeze used templates only.

## Reproducing the pipeline (operators)

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch
python scripts/build_readable_validation_packets.py
```

Do not re-freeze expecting to replace `VAL-201`–`VAL-224`. To refresh clinician-facing Markdown only, run the readable-packet script.
"""
