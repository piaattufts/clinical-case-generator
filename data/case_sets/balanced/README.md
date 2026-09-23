# Balanced structured set (`CLINIPROOF_BALANCED_V4`)

**Status: active prospective validation set, pending human clinician validation.**

This directory is one of the two current prospective datasets. The other is [`../validation_seedcases_v3/`](../validation_seedcases_v3/README.md). `CLINIPROOF_TAXONOMY_V1` and the earlier balanced freezes are historical provenance and are not the current study set.

## Batch identity

| Item | Value |
| --- | --- |
| Batch code | `CLINIPROOF_BALANCED_V4` |
| Generation strategy | `balanced_structured` |
| VAL range | VAL-701–VAL-724 |
| Case count | 24 |
| Master seed | `20260925` |
| Sequences | 1401–1424 |
| Case seed | `{master_seed}:{sequence}:{scenario}:{clinical_profile}` |
| Status | Ready for human clinician validation. Not clinically validated. |

`CLINIPROOF_BALANCED_V4` supersedes the immutable predecessors `CLINIPROOF_BALANCED_V3` (VAL-501–VAL-524, [`../validation_balanced_v3/`](../validation_balanced_v3/README.md)) and `CLINIPROOF_BALANCED_V2` (VAL-301–VAL-324, [`../validation_balanced/`](../validation_balanced/README.md)). Those directories were not edited. This batch had not been sent for clinician ratings, so the final pre-validation chart QC was applied here in place. The batch code did not change. After clinician review starts, further clinical corrections should be a new batch code.

## Purpose

The balanced set asks whether a generator that starts from named clinical profiles, rather than from resident-authored examples, can produce charts that are diverse before any error is injected and that still contain exactly one assigned reconciliation problem. The distribution is a design grid. It is not a sample of hospital discharges and it is not prevalence-weighted.

## Generation method

Each assignment names a scenario family and a distinct clinical profile. The profile fixes the clinical structure: presentation, medication roles, relevant laboratories, hospital-course pattern, and follow-up. Demographics and numeric results are synthetic draws from the case seed. Medication concepts come from RxNorm. The administered dose, route, frequency, indication, and temporal state come from the curated regimen in [`../../data/bootstrap/medication_regimens.json`](../../data/bootstrap/medication_regimens.json), not from the product strength and not from a once-daily default.

The clean case is validated and fingerprinted before error injection. Exact duplicate fingerprints are rejected. Similarity of 0.85 or higher is rejected. Similarity from 0.70 to 0.85 is an investigator warning. Differences in age, sex, seed, or the planted error do not count as clinical uniqueness. After that audit, the batch plan injects one predetermined Family 1 or Family 2 discrepancy, or keeps the case as a control. Another category is not substituted if the assigned category is ineligible.

Resident-facing notes describe what happened in ordinary chart language. They do not say that a dose is correct, that a drug must be stopped at discharge, or that a medication is the hospital-only drug that reveals the answer. The investigator plan keeps `correct_discharge_state` and `decision_reason`.

## Batch composition

Counts below are the current manifest and coverage report, not a second hand-maintained key.

| Scenario family | Cases |
| --- | ---: |
| Inpatient heart failure (`HF_INPATIENT`) | 5 |
| Atrial fibrillation (`AF_ANTICOAGULATION`) | 5 |
| Hypertension (`HTN_INPATIENT`) | 5 |
| Type 2 diabetes (`T2DM_INPATIENT`) | 5 |
| Community-acquired pneumonia (`CAP_INPATIENT`) | 4 |

Each of the 24 rows uses a different clinical profile. Profile names and the one-case-per-profile grid are listed in [`diversity_report.md`](diversity_report.md) and [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md).

## Error and control composition

| Group | Cases |
| --- | ---: |
| Family 1 list discrepancies | 11 |
| Family 2 transition-of-care gaps | 9 |
| Clean controls | 4 |
| Total | 24 |

Family 1 in this batch: omission 3, commission 1, dose mismatch 3, route mismatch 1, frequency mismatch 2, therapeutic substitution 1.

Family 2 in this batch: monitoring not arranged 2, held medication without a restart plan 2, insufficient supply 2, hospital-only medication continued 1, inpatient substitution not reverted 1, pending-decision follow-up missing 1.

`f2_coprescription_omitted` is not implemented and is not in this batch. Category definitions are in [`../../docs/error_taxonomy.md`](../../docs/error_taxonomy.md). Do not read this README as an answer key for a particular VAL identifier.

## Diversity results

Evaluated on the clean case before error injection. Source: [`diversity_report.md`](diversity_report.md).

| Result | Value |
| --- | --- |
| Unique profiles | 24 |
| Exact duplicate fingerprints | 0 |
| Near-duplicate rejections (≥ 0.85) | 0 |
| Similarity warnings (0.70–0.85) | 1 |
| Closest pair | VAL-717 vs VAL-719, similarity 0.74 |

VAL-717 and VAL-719 share a scenario, specialty, diagnosis, and medication skeleton. They differ in clinical profile, symptoms, hospital-course pattern, and follow-up. The warning is recorded. It is not a rejection.

## Clinical QC

The checks in this section are automated internal review plus investigator inspection of the exported charts. They are not clinician validation.

Before this directory is used for human review, the freeze checks terminology identity, curated dose/route/frequency, beta-blocker formulation against frequency, temporal role, laboratory units, imaging timepoint wording, and error isolation. Isolation requires one intended discrepancy on error-bearing cases and zero on controls. The internal table is [`../clinical_qc_report.md`](../clinical_qc_report.md). Passing that table means the case is ready for human C1–C5 review. It does not mean the case is clinically validated.

Warfarin cases in this batch were checked against the answer key. VAL-703 and VAL-707 are `f2_monitoring_not_arranged`: warfarin remains at discharge, anticoagulation-clinic follow-up remains, and the structured INR monitoring task is absent. That split is the intended target. Laboratory monitoring is not the same thing as a clinic appointment. VAL-710 is a control and has both structured INR monitoring and anticoagulation-clinic follow-up.

## File index

| File | What it is | Who should open it |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Assignment source: VAL id, scenario, profile, sequence, whether to inject, and the error category | Developers regenerating the batch |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Blinded resident export | Residents and anyone building a blinded review |
| [`investigator_answer_key.json`](investigator_answer_key.json) | Concealed targets, clean expected state, and `decision_reason` | Investigators only |
| [`investigator_answer_key.md`](investigator_answer_key.md) | The same key in readable form | Investigators only |
| [`validation_manifest.json`](validation_manifest.json) | Batch identity, seeds, validation status, and terminology snapshot | Reproducibility checks |
| [`coverage_report.md`](coverage_report.md) | Scenario and category counts | Investigators |
| [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md) | Profile-by-category grid | Investigators |
| [`diversity_report.md`](diversity_report.md) | Clean-case uniqueness and similarity | Investigators |
| [`resident_review_worksheet.csv`](resident_review_worksheet.csv) | Empty rows for a later resident study | Study staff, after clinician acceptance |
| [`resident_review_schema.json`](resident_review_schema.json) | Fields for that later worksheet | Developers |
| [`readable/all_cases.md`](readable/all_cases.md) | Human-readable resident-safe charts | Residents |
| [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) | Charts plus the intended target for C1–C5 | Clinician reviewers |
| [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv) | Empty C1–C5 rating rows | Clinician reviewers |
| [`readable/validation_rubric.md`](readable/validation_rubric.md) | Rubric text without per-case answers | Reviewers |
| [`readable/README.md`](readable/README.md) | Index of the readable packet | Anyone opening `readable/` |

Do not send the answer key, the batch plan, or the clinician packet to residents who are supposed to find the problem themselves.

## Reviewer workflow

Residents start at [`readable/all_cases.md`](readable/all_cases.md) or the blinded JSON. They should infer reconciliation problems from the chart. The chart should not explain the answer.

Clinicians rating suitability start at [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md), record C1–C5 on [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv), and use [`../../docs/clinical_validation.md`](../../docs/clinical_validation.md). That review is one pass. It is not a resident study response.

Investigators use the answer key and [`../clinical_qc_report.md`](../clinical_qc_report.md). Developers use [`../../docs/developer_guide.md`](../../docs/developer_guide.md).

## Regeneration

Regenerate only while this batch is still pre-validation, and only from a bootstrapped database. Freeze reuses an existing VAL row when the identifier, case seed, and scenario still match, so a content change requires deleting the frozen rows for this batch code before freezing again. Do not delete archived batches.

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v4/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V4
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_BALANCED_V4 \
  --resident data/validation_balanced_v4/resident_validation_cases.json
```

There is no default batch. Pass `--plan` and `--batch-code` explicitly. The same commands with the seed-guided plan do not rebuild this directory.

## Reproducibility

The manifest records the master seed, the per-case seed, the generator version, and the terminology snapshot used at export. Clean-case fingerprints exclude the VAL identifier, the seed, demographics, numeric results, and the injected error. The answer key is written by the injector, not by a language model. Narrative on this freeze is template text. OpenAI is not called.

## Limitations and status

This batch is ready for human clinician validation. It is not clinically validated. The grid covers five scenario families by design. It does not estimate how often these problems occur in practice. Curated regimens avoid known distracting baselines for these profiles. They are not a general prescribing system. Template prose can still look regular across cases. Uniqueness scores do not by themselves prove that a teacher would call two charts distinct lessons.
