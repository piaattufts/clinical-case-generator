# CliniProof Implementation Notes for Clinical Informatics and AI Engineering

This note assumes you understand software engineering and may not have a clinical training background. It translates the medical objective into the modules that implement it.

It explains mechanisms. It does not map any frozen identifier to a hidden assessment target. That mapping exists only in investigator-only files.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

## Clinical objective

Hospitals reconcile medications at admission and discharge so that intended home therapy is neither dropped nor continued unsafely, and so that required monitoring and follow-up actually occur.

CliniProof builds synthetic inpatient charts for that task. Each assessment item has a known target chosen before generation, not discovered afterwards by a model. Residents see a chart. Investigators see the target. Human clinicians still decide whether the chart is believable enough to use.

## Why canonical vocabularies are used

If the case said only “a heart-failure pill,” reviewers could not tell which product was meant, and software could not check rules. Official vocabularies give citable identifiers. RxNorm identifiers (RXCUI) name medications. ICD-10-CM codes name diagnoses. LOINC codes name laboratory tests. UCUM codes name units.

Those identifiers are stored only after an official service returns them, together with provenance fields for the source system, source version, and retrieval time. The generator never invents a code. SNOMED CT is not ingested here; SNOMED fields stay empty rather than being fabricated.

## Source-backed versus synthetic

The table below is the same distinction clinicians need, restated for engineers. A source-backed warfarin concept is not evidence that a real patient was taking warfarin.

| Layer | Meaning |
| --- | --- |
| Source-backed concept | The type of thing, such as warfarin as an RxNorm identifier or creatinine as a LOINC test, came from an official terminology |
| Synthetic value | The patient-specific number or story, such as age 72, creatinine 1.3, or the history-of-present-illness sentences, was generated |
| Deterministic assessment change | After the clean chart passed checks, software applied one planned edit |

## Scenario structure

The file `data/bootstrap/scenarios.json` holds teaching skeletons: specialty, age band, search phrases for diagnoses, symptoms, medications, and labs, and which standardized assessment categories are allowed. Matching happens against already bootstrapped reference rows in `app/services/bootstrap.py`, not against live free text.

## Clean-case concept

Generation in `app/services/generation.py` first builds a clean structured encounter: demographics, presentation, medications in three contexts (home, inpatient, and discharge), labs, vitals, notes, monitoring, follow-up, and instructions. Clean means the chart should not already contain the assessment target that the plan might later introduce.

A small rules engine in `app/services/rules.py` applies only conditionals that have attached DailyMed or RxClass evidence. There are few such rules. They are not a complete specialty guideline.

## Family 1 versus Family 2

Identifiers live in `app/services/error_taxonomy.py`.

Family 1 (`family_1`) means the discharge list is wrong relative to intended continuation. The following table lists the clinical meaning first and the software identifier second.

| Clinical meaning | Identifier |
| --- | --- |
| Medication omitted at discharge | `f1_omission` |
| Medication inappropriately added or continued | `f1_commission` |
| Unexplained dose discrepancy | `f1_dose_mismatch` |
| Unexplained route discrepancy | `f1_route_mismatch` |
| Unexplained frequency discrepancy | `f1_frequency_mismatch` |
| Unexplained therapeutic substitution | `f1_therapeutic_substitution` |

Family 2 (`family_2`) means a required transition action is missing; the continued-drug identity may be unchanged.

| Clinical meaning | Identifier |
| --- | --- |
| Required outpatient monitoring not arranged | `f2_monitoring_not_arranged` |
| Held medication without a restart plan | `f2_held_med_no_restart_plan` |
| Insufficient medication supply | `f2_insufficient_supply` |
| Hospital-only medication continued after discharge | `f2_hospital_only_continued` |
| Temporary inpatient substitution not addressed at discharge | `f2_inpatient_substitution_not_reverted` |
| Follow-up missing for an unresolved treatment decision | `f2_pending_decision_followup_missing` |
| Required companion medication omitted | `f2_coprescription_omitted` |

Held medication without a restart plan means the original medication is intentionally stopped during hospitalization for a legitimate temporary reason, but the discharge documentation does not tell the patient or outpatient clinician when or under what conditions it should be resumed. That maps to `f2_held_med_no_restart_plan`.

Required outpatient monitoring not arranged means, for example, warfarin continues at discharge but outpatient INR monitoring was not scheduled. That maps to `f2_monitoring_not_arranged`. The medication row stays; the monitoring record is what changes.

The taxonomy also defines required companion medication omitted (`f2_coprescription_omitted`). This category is not included in the current validation sets because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing, freeze currently rejects this category.

Do not implement Family 2 detection as a simple difference of the three medication lists.

## Eligibility, injection, and no fallback

The freeze plan names the error family and error category before generation in that batch’s `batch_plan.json`.

The taxonomy module in `app/services/error_taxonomy.py` decides whether the clean case is eligible for that category. For example, there must be a continued discharge drug to omit, or a monitoring-dependency rule must match.

The injector in `app/services/error_injection.py` then applies the exact edit, or skips injection for a clean control whose category is `none`.

If the category is unknown, ineligible, or marked `not_yet_implementable`, freeze aborts. It does not pick a different error. A language model never chooses the category.

## Clean state and injected state

The investigator answer key stores both states. The clean expected state is what the field was after clean validation, for example the omitted drug present on the discharge list. The injected state is what residents see after the edit, for example absent.

Residents must not receive these fields. The readable investigator packet is the human view of the same concealed specification.

## Machine validation

Validation in `app/services/validation.py` and freeze-time checks in `app/services/validation_batch.py` cover structure, terminology integrity, implemented rules, category eligibility, the expected state transition, answer-key consistency, isolation of a second target, and leak checks on the resident export.

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians.

## Resident blinding

The resident JSON omits answer-key objects, internal generation identifiers, family and category fields, trigger metadata, and clean or injected state. Readable files `all_cases.md` and the individual case pages are derived only from that blinded export.

## Human clinician validation

Human validation of the frozen set uses a single review stage. A clinician or resident reads the complete case in `clinician_validation_packet.md` and assesses C1–C5 in one pass. Ratings are stored on `clinical_validation_worksheet.csv`. Reviewer comments do not rewrite frozen JSON.

Case generation and automated checks remain unchanged. Software checks structure, terminology, implemented rules, and the intended assessment manipulation. Those checks do not replace this human review.

## Freeze immutability and provenance

Frozen files for batch `CLINIPROOF_TAXONOMY_V1` under `data/validation/` are archived historical provenance. Regenerating live terminology from APIs is not expected to reproduce bit-identical JSON. Readable Markdown is allowed to be regenerated from those frozen files; the frozen files themselves must not be rewritten to improve clinical content.

Each frozen assignment records scenario, seed, family, category, source-version snapshots, and validation statuses in the investigator key and manifest.

## Optional narrative language model

The module `app/openai/narrative.py` may reword admission prose from already chosen names. It is not a case generator. OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. It does not choose diagnoses, medications, terminology codes, error categories, clinical rules, or answer-key content. The committed freeze used templates only.

## Reproducing the pipeline

Operators who already have a database and terminology bootstrap can run the following commands. Pass an explicit `--plan` and `--batch-code`. Do not re-freeze expecting to replace archived VAL-201 through VAL-224. To refresh clinician-facing Markdown only, run the readable-packet script with `--batch-code`.

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
python -m app.services.readable_packets --batch-code CLINIPROOF_BALANCED_V3 --resident data/validation_balanced_v3/resident_validation_cases.json
```
