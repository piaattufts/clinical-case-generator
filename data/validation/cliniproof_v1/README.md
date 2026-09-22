# CLINIPROOF_TAXONOMY_V1

This directory is the study copy of batch **`CLINIPROOF_TAXONOMY_V1`**. It is a **new** validation set. It does **not** replace or rewrite `RESIDENT_VALIDATION_V1` (`VAL-001`–`VAL-024`) or `RESIDENT_VALIDATION_V2`–`V4`.

Target `error_family` and `error_category` are specified in [`batch_plan.json`](batch_plan.json) **before** generation. The injector never asks an LLM which error to plant. If the requested category is ineligible, freeze **rejects** the assignment and aborts the batch instead of substituting another category.

All records remain **machine-validated synthetic resident-review cases pending clinician validation**.

| Field | Value |
| --- | --- |
| Batch code | `CLINIPROOF_TAXONOMY_V1` |
| Public IDs | `VAL-201`–`VAL-224` |
| Internal sequences | `SYN-000801`–`SYN-000824` |
| Master seed | `20260922` |
| Case seed | `{master_seed}:{sequence}:{scenario}` |
| Mix | 4 clean controls (`VAL-213`, `VAL-216`, `VAL-220`, `VAL-223`), 20 error-bearing |
| OpenAI | not used |
| Export audit | passed |
| Exported at | `2026-09-22T15:40:14.870878+00:00` |
| Dataset status | `machine-validated synthetic resident-review cases pending clinician validation` |

Give residents only `resident_validation_cases.json` and `resident_review_worksheet.csv`. Keep the investigator key, manifest, coverage files, `batch_plan.json`, and this README off the resident packet.

## Commands

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation/cliniproof_v1/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_TAXONOMY_V1 --output-dir data/validation/cliniproof_v1
```

Export **must** use `--output-dir data/validation/cliniproof_v1`. The default export directory is `data/validation/` and would overwrite the frozen V1 resident file.

`f2_coprescription_omitted` is not assigned here; the repository has no source-backed companion-prescription rule. Manuscript examples (steroid/PPI, opioid/bowel regimen) are not hard-coded.

Machine validation means the requested category was injected as specified, structural/terminology constraints passed, implemented deterministic clinical rules passed, and no mechanically detectable extra discrepancy was found. Clinician review still evaluates clinical coherence, error fidelity, evidentiary sufficiency, error isolation, cue integrity, and educational appropriateness.

## Files in this directory

| File | Audience | Contents |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Investigators / operators | Canonical `error_family` + `error_category` chosen before generation |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Residents | Blinded dashboard-shaped cases, including `CaseMonitoring` |
| [`investigator_answer_key.json`](investigator_answer_key.json) / [`.md`](investigator_answer_key.md) | Investigators only | Seeds, SYN IDs, family, category, clean expected state |
| [`validation_manifest.json`](validation_manifest.json) | Investigators | Freeze metadata, source versions |
| [`coverage_report.md`](coverage_report.md) | Investigators | Mix counts |
| [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md) | Investigators | Resolved concepts per family |
| [`resident_review_worksheet.csv`](resident_review_worksheet.csv) | Residents / study staff | Empty capture rows |
| [`resident_review_schema.json`](resident_review_schema.json) | Study staff | Worksheet fields |

Shared pipeline, official sources, and limitations: [`../README.md`](../README.md).

## Assignment index (investigator only)

Do **not** distribute this table to residents.

| VAL | SYN | Scenario | Seed | Family | Category |
| --- | --- | --- | --- | --- | --- |
| VAL-201 | SYN-000801 | HF_INPATIENT | `20260922:801:HF_INPATIENT` | family_1 | `f1_omission` |
| VAL-202 | SYN-000802 | HF_INPATIENT | `20260922:802:HF_INPATIENT` | family_1 | `f1_commission` |
| VAL-203 | SYN-000803 | HF_INPATIENT | `20260922:803:HF_INPATIENT` | family_1 | `f1_dose_mismatch` |
| VAL-204 | SYN-000804 | HF_INPATIENT | `20260922:804:HF_INPATIENT` | family_1 | `f1_route_mismatch` |
| VAL-205 | SYN-000805 | HF_INPATIENT | `20260922:805:HF_INPATIENT` | family_1 | `f1_frequency_mismatch` |
| VAL-206 | SYN-000806 | HF_INPATIENT | `20260922:806:HF_INPATIENT` | family_1 | `f1_therapeutic_substitution` |
| VAL-207 | SYN-000807 | HF_INPATIENT | `20260922:807:HF_INPATIENT` | family_2 | `f2_monitoring_not_arranged` |
| VAL-208 | SYN-000808 | HF_INPATIENT | `20260922:808:HF_INPATIENT` | family_2 | `f2_held_med_no_restart_plan` |
| VAL-209 | SYN-000809 | HF_INPATIENT | `20260922:809:HF_INPATIENT` | family_2 | `f2_insufficient_supply` |
| VAL-210 | SYN-000810 | HF_INPATIENT | `20260922:810:HF_INPATIENT` | family_2 | `f2_hospital_only_continued` |
| VAL-211 | SYN-000811 | HF_INPATIENT | `20260922:811:HF_INPATIENT` | family_2 | `f2_inpatient_substitution_not_reverted` |
| VAL-212 | SYN-000812 | HF_INPATIENT | `20260922:812:HF_INPATIENT` | family_2 | `f2_pending_decision_followup_missing` |
| VAL-213 | SYN-000813 | HF_INPATIENT | `20260922:813:HF_INPATIENT` | none | **clean control** |
| VAL-214 | SYN-000814 | AF_ANTICOAGULATION | `20260922:814:AF_ANTICOAGULATION` | family_1 | `f1_omission` |
| VAL-215 | SYN-000815 | AF_ANTICOAGULATION | `20260922:815:AF_ANTICOAGULATION` | family_2 | `f2_monitoring_not_arranged` |
| VAL-216 | SYN-000816 | AF_ANTICOAGULATION | `20260922:816:AF_ANTICOAGULATION` | none | **clean control** |
| VAL-217 | SYN-000817 | HTN_INPATIENT | `20260922:817:HTN_INPATIENT` | family_1 | `f1_dose_mismatch` |
| VAL-218 | SYN-000818 | HTN_INPATIENT | `20260922:818:HTN_INPATIENT` | family_1 | `f1_commission` |
| VAL-219 | SYN-000819 | HTN_INPATIENT | `20260922:819:HTN_INPATIENT` | family_2 | `f2_held_med_no_restart_plan` |
| VAL-220 | SYN-000820 | HTN_INPATIENT | `20260922:820:HTN_INPATIENT` | none | **clean control** |
| VAL-221 | SYN-000821 | T2DM_INPATIENT | `20260922:821:T2DM_INPATIENT` | family_1 | `f1_omission` |
| VAL-222 | SYN-000822 | T2DM_INPATIENT | `20260922:822:T2DM_INPATIENT` | family_2 | `f2_insufficient_supply` |
| VAL-223 | SYN-000823 | T2DM_INPATIENT | `20260922:823:T2DM_INPATIENT` | none | **clean control** |
| VAL-224 | SYN-000824 | CAP_INPATIENT | `20260922:824:CAP_INPATIENT` | family_1 | `f1_frequency_mismatch` |

Family 1 is a discharge/plan mutation. Family 2 is generally an absence (monitoring, restart plan, supply, hospital-only stop, substitution revert, or follow-up) while the trigger medication remains visible. Clean controls keep the intended companion actions.
