# Frozen CliniProof validation set (`CLINIPROOF_TAXONOMY_V1`)

This directory holds the current frozen CliniProof clinician-validation set. The batch code `CLINIPROOF_TAXONOMY_V1` identifies that freeze. It was generated using the standardized CliniProof taxonomy, in which each assessment category has both a clinical meaning and a software identifier such as `f1_omission` for a medication that is unintentionally absent at discharge.

The freeze covers every CliniProof error category that the software can currently implement. That is not the same as complete coverage of the full conceptual taxonomy. The taxonomy also defines required companion medication omitted (`f2_coprescription_omitted`), which represents a situation in which a clinically required companion medication is missing. This category is not included in the current validation set because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category.

The intended family and category for each assignment are specified in [`batch_plan.json`](batch_plan.json) before generation. The injector never asks a language model which error to plant. If the requested category is unknown, ineligible, or marked `not_yet_implementable`, freeze rejects the assignment and aborts the batch instead of substituting another category.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

The table below is a compact identity card for the freeze. The sentences after the table explain what those fields mean for study operations.

| Field | Value |
| --- | --- |
| Batch code | `CLINIPROOF_TAXONOMY_V1` |
| Public IDs | `VAL-201`–`VAL-224` |
| Internal sequences | `SYN-000801`–`SYN-000824` (sequences 801–824) |
| Master seed | `20260922` |
| Case seed | `{master_seed}:{sequence}:{scenario}` |
| Cases | 24 |
| Mix | 4 clean controls, 20 error-bearing |
| Clean controls | `VAL-213`, `VAL-216`, `VAL-220`, `VAL-223` |
| OpenAI | not used (`freeze-validation-batch` sets `use_openai=False`) |
| Generator version | `0.1.0` |
| Export audit | passed |
| Exported at | `2026-09-22T15:40:14.870878+00:00` |
| Dataset status | `machine-validated synthetic resident-review cases pending clinician validation` |

There are twenty-four public case identifiers, VAL-201 through VAL-224. Four of the twenty-four cases are clean controls (`VAL-213`, `VAL-216`, `VAL-220`, and `VAL-223`). These cases do not contain an intentionally introduced medication-reconciliation problem and are included so that residents cannot assume that every case necessarily contains an error. The remaining twenty cases each contain exactly one intended assessment problem.

OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. It does not choose diagnoses, medications, terminology codes, error categories, clinical rules, or answer-key content. This freeze did not call OpenAI.

Give residents only [`resident_validation_cases.json`](resident_validation_cases.json) and [`resident_review_worksheet.csv`](resident_review_worksheet.csv), or the resident-safe readable Markdown under [`readable/`](readable/). Keep the investigator key, manifest, coverage files, `batch_plan.json`, this README, and the investigator validation packet off the resident packet.

## Audited coverage

A read-only integrity audit of these frozen files, without regeneration, found no defect on VAL-201 through VAL-224. The table lists counts by category. Clinical names are shown first, with the software identifier in parentheses. The paragraphs after the table state the same facts in clinical language.

| Bucket | Count |
| --- | --- |
| Clean controls | **4** |
| Family 1 medication-list discrepancies, total | **11** |
| Medication omitted at discharge (`f1_omission`) | 3 |
| Medication inappropriately added or continued (`f1_commission`) | 2 |
| Unexplained dose discrepancy (`f1_dose_mismatch`) | 2 |
| Unexplained frequency discrepancy (`f1_frequency_mismatch`) | 2 |
| Unexplained route discrepancy (`f1_route_mismatch`) | 1 |
| Unexplained therapeutic substitution (`f1_therapeutic_substitution`) | 1 |
| Family 2 transition-of-care gaps, implemented total | **9** |
| Required outpatient monitoring not arranged (`f2_monitoring_not_arranged`) | 2 |
| Held medication without a restart plan (`f2_held_med_no_restart_plan`) | 2 |
| Insufficient medication supply (`f2_insufficient_supply`) | 2 |
| Hospital-only medication continued after discharge (`f2_hospital_only_continued`) | 1 |
| Temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`) | 1 |
| Follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`) | 1 |
| Required companion medication omitted (`f2_coprescription_omitted`), not yet implementable | **0** |

Of the twenty cases containing an intended assessment problem, eleven represent Family 1 medication-reconciliation discrepancies, in which the medication regimen itself differs across the transition to discharge. The remaining nine represent Family 2 transition-of-care gaps, in which the medication order may be correct but an important action such as monitoring, medication supply, restart instructions, or follow-up is missing.

The scenario mix is not prevalence-weighted. Thirteen cases use the heart-failure inpatient skeleton, four use hypertension, three use atrial fibrillation with anticoagulation, three use type 2 diabetes, and one uses community-acquired pneumonia. This distribution is a teaching mix, not a sample of inpatient medicine.

## Implemented generation process

This freeze was not produced by asking a language model to invent a clinical case and then find an error. The implemented pipeline is as follows.

1. An assessment specification is written in `batch_plan.json`, including the public VAL identifier, scenario, whether to inject an error, the family, the standardized category, and the internal sequence.
2. A clinical scenario is selected from `data/bootstrap/scenarios.json`.
3. Canonical terminology is resolved from local authoritative reference tables.
4. A deterministic structured clean case is generated without OpenAI.
5. Source-backed clinical rules are applied.
6. The clean case is machine-validated for structure, terminology, implemented clinical rules, and assessment consistency.
7. Eligibility for the requested standardized error category is checked.
8. The exact requested error is injected deterministically, or skipped for clean controls.
9. Hidden assessment and answer-key state is recorded, including the clean expected state and the injected state.
10. Post-injection validation that is aware of the category is applied.
11. The case is frozen under an immutable VAL identifier.
12. A blinded resident export and an investigator export are written.

The requested error category is selected prospectively. Unknown, ineligible, and `not_yet_implementable` categories abort. They do not silently substitute another category. For every error-bearing case, the planned standardized category, the injected kind, and the investigator answer-key category agree. Every error-bearing case has exactly one intended injected assessment target. Clean controls have zero injected targets. Freeze-time audit also recorded that eligibility passed, clean validation passed, post-injection assessment validation passed, and no silent fallback occurred.

Default operator commands, with this directory as the default plan and export location, are:

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch
```

The committed JSON and Markdown files are the study source of truth. Do not re-run freeze expecting bit-identical output from live terminology APIs.

## Family 1 versus Family 2

Do not read this batch as if every error-bearing case had exactly one medication-list discrepancy. That statement is true of Family 1 list-transition errors. It is not true of Family 2.

Family 1 errors are medication-reconciliation and list-transition discrepancies: a medication omitted at discharge (`f1_omission`), a medication inappropriately added or continued (`f1_commission`), an unexplained dose discrepancy (`f1_dose_mismatch`), an unexplained route discrepancy (`f1_route_mismatch`), an unexplained frequency discrepancy (`f1_frequency_mismatch`), or an unexplained therapeutic substitution (`f1_therapeutic_substitution`).

Family 2 errors are transition-of-care gaps that may leave the medication list itself unchanged. Implemented categories in this freeze are required outpatient monitoring not arranged (`f2_monitoring_not_arranged`), held medication without a restart plan (`f2_held_med_no_restart_plan`), insufficient medication supply (`f2_insufficient_supply`), hospital-only medication continued after discharge (`f2_hospital_only_continued`), temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`), and follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`).

Validation is category-aware. For Family 2 the freeze checks that the trigger or precondition is present, that the expected companion action exists in the clean state, that the specified action is absent or incorrect after injection, that resident-visible evidence needed for detection remains present, and that no unintended second assessment target was introduced.

## Resident blinding

The audited resident export contains no answer-key object, no internal generation identifiers, no test identifiers, no leak-marker strings defined in `app/services/validation_batch.py`, no planted-error category or error-family field, no target-medication metadata, and no clean-expected-state, injected-state, or correct-action answer.

The resident worksheet retains empty rating and response fields. Do not pre-populate resident judgments.

## Machine validation versus clinician validation

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians. They also do not establish guideline completeness, optimal therapy, or calibrated learner difficulty.

## How clinical review will be conducted

Two clinical reviewers will independently assess every case. They will first evaluate clinical plausibility without seeing the intended assessment target. After those ratings have been submitted, they will receive the investigator version of the case and evaluate whether the intended problem is present, detectable, and isolated from other unintended clinical problems.

The study method is independent dual expert review with structured consensus resolution. It is not a Delphi process. Original independent ratings are preserved. Cases with important disagreements undergo structured consensus review, and the consensus outcome is recorded separately. Reviewers may request specific revisions. If consensus cannot be reached, the case remains unresolved and is not considered clinically validated.

The Stage 1 packet is [`readable/plausibility_only_packet.md`](readable/plausibility_only_packet.md). The Stage 2 packet is [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md). Criterion definitions are in [`readable/validation_rubric.md`](readable/validation_rubric.md). The two-reviewer workflow is in [`readable/reviewer_protocol.md`](readable/reviewer_protocol.md). Independent ratings are recorded on the empty [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv). Consensus outcomes are recorded separately on the empty [`readable/consensus_worksheet.csv`](readable/consensus_worksheet.csv).

## Provenance

Per-assignment reproducibility fields are stored in three investigator files. [`batch_plan.json`](batch_plan.json) records the public identifier, scenario, family, category, sequence, and inject flag. [`validation_manifest.json`](validation_manifest.json) records seed, control status, source snapshots, rule snapshots, and validation statuses. [`investigator_answer_key.json`](investigator_answer_key.json) records the internal identifier, family, category, clean expected state, and injected state.

Terminology versions recorded on this freeze come from the manifest. Do not invent missing versions. The table lists what the freeze actually stored.

| Source | Version on this freeze |
| --- | --- |
| RXNORM | `08-Sep-2026` |
| LOINC | `2.83` |
| UCUM | `2.2` |
| ICD10CM | none supplied by API (`null`) |
| RXCLASS | none supplied by API (`null`) |
| DAILYMED | none supplied by API (`null`) |

## Limitations

This set is not a prevalence-weighted or representative sample of inpatient medicine. Heart-failure cases predominate, and community-acquired pneumonia appears only once.

Several error categories occur only once. This batch alone does not support stable category-specific psychometric estimates. It is primarily intended for clinician assessment of clinical plausibility, assessment-object integrity, error fidelity, detectability, and isolation.

Required companion medication omitted (`f2_coprescription_omitted`) is intentionally absent because it is `not_yet_implementable`. Manuscript examples such as a steroid without a proton-pump inhibitor, or an opioid without a bowel regimen, are not hard-coded.

Official source ranking can produce technically source-valid but clinically atypical formulations or units, such as RxNorm solutions or gels, or SI laboratory units. Those are among the issues clinician plausibility review should detect.

## Files in this directory

The table below says who may receive each file. Residents should not receive investigator catalogs.

| File | Audience | Contents |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Investigators / operators | Family and category chosen before generation |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Residents | Blinded dashboard-shaped cases, including monitoring rows |
| [`investigator_answer_key.json`](investigator_answer_key.json) / [`.md`](investigator_answer_key.md) | Investigators only | Seeds, internal identifiers, family, category, clean expected state, injected state |
| [`validation_manifest.json`](validation_manifest.json) | Investigators | Freeze metadata and source versions |
| [`coverage_report.md`](coverage_report.md) | Investigators | Mix counts written at export |
| [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md) | Investigators | Resolved concepts per family |
| [`resident_review_worksheet.csv`](resident_review_worksheet.csv) | Residents / study staff | Empty capture rows |
| [`resident_review_schema.json`](resident_review_schema.json) | Study staff | Worksheet fields |
| [`readable/`](readable/) | See below | Derived Markdown clinician-validation views |

## Human-readable clinician validation packets

These files are generated from the frozen JSON. They do not replace it, and they do not regenerate the underlying VAL cases.

Use the following table to choose a starting file. Residents and independent plausibility reviewers should stay on the resident-safe documents. Only investigators and expert validators should open the concealed-target packet.

| If you are... | Start here |
| --- | --- |
| Resident or clinician reviewing cases | [`readable/all_cases.md`](readable/all_cases.md) |
| Clinical reviewer completing Stage 1 (blinded C1) | [`readable/plausibility_only_packet.md`](readable/plausibility_only_packet.md) |
| Clinical reviewer completing Stage 2 (C2–C5) | [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) |
| Clinical reviewer reading the two-reviewer protocol | [`readable/reviewer_protocol.md`](readable/reviewer_protocol.md) |
| Medical educator reviewing the framework | [`readable/validation_rubric.md`](readable/validation_rubric.md) |
| Recording independent ratings (empty template) | [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv) |
| Recording consensus (empty template) | [`readable/consensus_worksheet.csv`](readable/consensus_worksheet.csv) |
| Clinician or resident curious how CliniProof works | [`readable/how_cliniproof_works.md`](readable/how_cliniproof_works.md) |
| Clinical informatics / AI engineer | [`readable/developer_notes.md`](readable/developer_notes.md) |

The following files are safe for residents and for plausibility-only review. They contain resident-visible content and generic explanations. They do not include per-case planted-error answers.

- [`readable/all_cases.md`](readable/all_cases.md)
- [`readable/plausibility_only_packet.md`](readable/plausibility_only_packet.md)
- [`readable/cases/VAL-201.md`](readable/cases/VAL-201.md) through [`VAL-224.md`](readable/cases/VAL-224.md)
- [`readable/how_cliniproof_works.md`](readable/how_cliniproof_works.md), which describes mechanisms only
- [`readable/developer_notes.md`](readable/developer_notes.md), which describes generic implementation only
- [`readable/validation_rubric.md`](readable/validation_rubric.md), which is the rubric without per-case answers
- [`readable/reviewer_protocol.md`](readable/reviewer_protocol.md), which describes the two-reviewer workflow
- [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv), an empty independent-rating template
- [`readable/consensus_worksheet.csv`](readable/consensus_worksheet.csv), an empty consensus template stored separately from independent ratings

The investigator and clinical-validator packet must not be distributed to resident participants. Reviewers should complete Stage 1 C1 before opening it:

- [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md)

The packet index is [`readable/README.md`](readable/README.md). Regenerate the Markdown with `python scripts/build_readable_validation_packets.py`. Shared pipeline, official sources, and limitations are in [`../../README.md`](../../README.md).

## Assignment index (investigator only)

Do not distribute this table to residents. It maps each public VAL identifier to its internal generation identifier, scenario, seed, family, and category. Family 1 is a discharge or plan mutation. Family 2 is generally an absence of monitoring, restart plan, supply, hospital-only stop, substitution revert, or follow-up while the trigger medication remains visible. Clean controls keep the intended companion actions. Clinical names are shown first, with software identifiers in parentheses.

| VAL | SYN | Scenario | Seed | Family | Clinical category |
| --- | --- | --- | --- | --- | --- |
| VAL-201 | SYN-000801 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:801:HF_INPATIENT` | Family 1 (`family_1`) | Medication omitted at discharge (`f1_omission`) |
| VAL-202 | SYN-000802 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:802:HF_INPATIENT` | Family 1 (`family_1`) | Medication inappropriately added or continued (`f1_commission`) |
| VAL-203 | SYN-000803 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:803:HF_INPATIENT` | Family 1 (`family_1`) | Unexplained dose discrepancy (`f1_dose_mismatch`) |
| VAL-204 | SYN-000804 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:804:HF_INPATIENT` | Family 1 (`family_1`) | Unexplained route discrepancy (`f1_route_mismatch`) |
| VAL-205 | SYN-000805 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:805:HF_INPATIENT` | Family 1 (`family_1`) | Unexplained frequency discrepancy (`f1_frequency_mismatch`) |
| VAL-206 | SYN-000806 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:806:HF_INPATIENT` | Family 1 (`family_1`) | Unexplained therapeutic substitution (`f1_therapeutic_substitution`) |
| VAL-207 | SYN-000807 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:807:HF_INPATIENT` | Family 2 (`family_2`) | Required outpatient monitoring not arranged (`f2_monitoring_not_arranged`) |
| VAL-208 | SYN-000808 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:808:HF_INPATIENT` | Family 2 (`family_2`) | Held medication without a restart plan (`f2_held_med_no_restart_plan`) |
| VAL-209 | SYN-000809 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:809:HF_INPATIENT` | Family 2 (`family_2`) | Insufficient medication supply (`f2_insufficient_supply`) |
| VAL-210 | SYN-000810 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:810:HF_INPATIENT` | Family 2 (`family_2`) | Hospital-only medication continued after discharge (`f2_hospital_only_continued`) |
| VAL-211 | SYN-000811 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:811:HF_INPATIENT` | Family 2 (`family_2`) | Temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`) |
| VAL-212 | SYN-000812 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:812:HF_INPATIENT` | Family 2 (`family_2`) | Follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`) |
| VAL-213 | SYN-000813 | Heart-failure inpatient (`HF_INPATIENT`) | `20260922:813:HF_INPATIENT` | No planted target (`none`) | Clean control |
| VAL-214 | SYN-000814 | Atrial fibrillation with anticoagulation (`AF_ANTICOAGULATION`) | `20260922:814:AF_ANTICOAGULATION` | Family 1 (`family_1`) | Medication omitted at discharge (`f1_omission`) |
| VAL-215 | SYN-000815 | Atrial fibrillation with anticoagulation (`AF_ANTICOAGULATION`) | `20260922:815:AF_ANTICOAGULATION` | Family 2 (`family_2`) | Required outpatient monitoring not arranged (`f2_monitoring_not_arranged`) |
| VAL-216 | SYN-000816 | Atrial fibrillation with anticoagulation (`AF_ANTICOAGULATION`) | `20260922:816:AF_ANTICOAGULATION` | No planted target (`none`) | Clean control |
| VAL-217 | SYN-000817 | Hypertension inpatient (`HTN_INPATIENT`) | `20260922:817:HTN_INPATIENT` | Family 1 (`family_1`) | Unexplained dose discrepancy (`f1_dose_mismatch`) |
| VAL-218 | SYN-000818 | Hypertension inpatient (`HTN_INPATIENT`) | `20260922:818:HTN_INPATIENT` | Family 1 (`family_1`) | Medication inappropriately added or continued (`f1_commission`) |
| VAL-219 | SYN-000819 | Hypertension inpatient (`HTN_INPATIENT`) | `20260922:819:HTN_INPATIENT` | Family 2 (`family_2`) | Held medication without a restart plan (`f2_held_med_no_restart_plan`) |
| VAL-220 | SYN-000820 | Hypertension inpatient (`HTN_INPATIENT`) | `20260922:820:HTN_INPATIENT` | No planted target (`none`) | Clean control |
| VAL-221 | SYN-000821 | Type 2 diabetes inpatient (`T2DM_INPATIENT`) | `20260922:821:T2DM_INPATIENT` | Family 1 (`family_1`) | Medication omitted at discharge (`f1_omission`) |
| VAL-222 | SYN-000822 | Type 2 diabetes inpatient (`T2DM_INPATIENT`) | `20260922:822:T2DM_INPATIENT` | Family 2 (`family_2`) | Insufficient medication supply (`f2_insufficient_supply`) |
| VAL-223 | SYN-000823 | Type 2 diabetes inpatient (`T2DM_INPATIENT`) | `20260922:823:T2DM_INPATIENT` | No planted target (`none`) | Clean control |
| VAL-224 | SYN-000824 | Community-acquired pneumonia inpatient (`CAP_INPATIENT`) | `20260922:824:CAP_INPATIENT` | Family 1 (`family_1`) | Unexplained frequency discrepancy (`f1_frequency_mismatch`) |
