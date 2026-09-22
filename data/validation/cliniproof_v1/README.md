# CLINIPROOF_TAXONOMY_V1

This directory is the **current post-taxonomy clinician-validation batch**. Batch code **`CLINIPROOF_TAXONOMY_V1`**. It is the first frozen validation set generated using the canonical CliniProof `error_family` / `error_category` implementation.

It is a **new** set with a new `batch_code` and new VAL IDs. It does **not** replace or rewrite `RESIDENT_VALIDATION_V1` (`VAL-001`–`VAL-024`). Pre-taxonomy `RESIDENT_VALIDATION_V2`–`V4` are archived under [`../legacy_pre_taxonomy/`](../legacy_pre_taxonomy/) for provenance only. They are **not** current resident packets, **not** taxonomy-compliant validation batches, and **not** evidence of Family 2 implementation.

`CLINIPROOF_TAXONOMY_V1` covers all **currently implemented** CliniProof error categories. That is **not** complete coverage of the full conceptual taxonomy. `f2_coprescription_omitted` remains specified by the conceptual taxonomy but is `not_yet_implementable` because a sufficiently source-backed deterministic companion-prescription rule has not yet been implemented.

Target `error_family` and `error_category` are specified in [`batch_plan.json`](batch_plan.json) **before** generation. The injector never asks an LLM which error to plant. If the requested category is ineligible or `not_yet_implementable`, freeze **rejects** the assignment and aborts the batch instead of substituting another category.

All records remain **machine-validated synthetic resident-review cases pending clinician validation**.

| Field | Value |
| --- | --- |
| Batch code | `CLINIPROOF_TAXONOMY_V1` |
| Role | Current post-taxonomy clinician-validation batch |
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
| Freeze commit on PR #6 | `db6832a47135bdb66a21d005095a14ba2de539d5` (`Freeze and export CLINIPROOF_TAXONOMY_V1 without rewriting V1.`) |
| Dataset status | `machine-validated synthetic resident-review cases pending clinician validation` |

Give residents only `resident_validation_cases.json` and `resident_review_worksheet.csv`. Keep the investigator key, manifest, coverage files, `batch_plan.json`, and this README off the resident packet.

## Audited coverage

A read-only integrity audit of these frozen files (no regeneration) found **no defect** on `VAL-201`–`VAL-224`.

| Bucket | Count |
| --- | --- |
| Clean controls | **4** |
| Family 1 total | **11** |
| `f1_omission` | 3 |
| `f1_commission` | 2 |
| `f1_dose_mismatch` | 2 |
| `f1_frequency_mismatch` | 2 |
| `f1_route_mismatch` | 1 |
| `f1_therapeutic_substitution` | 1 |
| Family 2 implemented total | **9** |
| `f2_monitoring_not_arranged` | 2 |
| `f2_held_med_no_restart_plan` | 2 |
| `f2_insufficient_supply` | 2 |
| `f2_hospital_only_continued` | 1 |
| `f2_inpatient_substitution_not_reverted` | 1 |
| `f2_pending_decision_followup_missing` | 1 |
| not_yet_implementable `f2_coprescription_omitted` | **0** |

Scenario composition (not prevalence-weighted): `HF_INPATIENT` 13/24, `HTN_INPATIENT` 4/24, `AF_ANTICOAGULATION` 3/24, `T2DM_INPATIENT` 3/24, `CAP_INPATIENT` 1/24.

## Implemented generation process

This freeze was **not** produced by asking an LLM to invent a clinical case and then find an error. The implemented pipeline is:

1. Assessment / batch specification (`batch_plan.json`: VAL ID, scenario, `inject_error`, `error_family`, canonical `error_category`, sequence)
2. Scenario selected from `data/bootstrap/scenarios.json`
3. Canonical terminology resolved from local authoritative `ref_*` tables
4. Deterministic structured **clean** case generated (`use_openai=False`)
5. Source-backed clinical rules applied
6. Clean case machine-validated (structural, terminology, clinical, assessment)
7. Requested canonical error category eligibility checked
8. Exact requested error injected deterministically (or skipped for clean controls)
9. Hidden assessment / answer-key state recorded (`clean_expected_state` and `injected_state` as implemented)
10. Post-injection category-aware validation
11. Freeze under an immutable VAL ID
12. Blinded resident export + investigator export

Behavior on this batch:

- The requested error category is selected **prospectively**.
- Ineligible categories **abort**. They do **not** silently substitute another category.
- For every error-bearing case, planned canonical category = injected `kind` = investigator answer-key category.
- Every error-bearing case has **exactly one** intended injected assessment target.
- Clean controls have **zero** injected targets.
- Freeze-time audit also recorded: eligibility passed, clean validation passed, post-injection assessment validation passed, no silent fallback.

## Family 1 versus Family 2

Do **not** read this batch as “every error-bearing case has exactly one medication-list discrepancy.” That is true of historical V1 Family 1 names; it is **not** true of Family 2.

**Family 1** errors are medication-reconciliation / list-transition discrepancies: omission, commission, dose mismatch, route mismatch, frequency mismatch, therapeutic substitution.

**Family 2** errors are transition-of-care gaps that may leave the medication list itself unchanged. Implemented categories here: monitoring not arranged; held medication with no restart plan; insufficient supply; hospital-only medication continued; inpatient substitution not reverted; missing follow-up for a pending therapeutic decision.

Validation is **category-aware**. For Family 2 the freeze checks that the trigger/precondition is present, the expected companion action exists in the clean state, the specified action is absent or incorrect after injection, resident-visible evidence needed for detection remains present, and no unintended second assessment target was introduced.

## Resident blinding

The audited resident export contains:

- no `CaseAnswerKey`
- no `SYN-*` identifiers
- no `TEST_*` identifiers
- no `LEAK_MARKERS` (`app/services/validation_batch.py`)
- no planted-error category or error-family field
- no target-medication metadata
- no `clean_expected_state` / `injected_state` / correct-action answer

The resident worksheet retains **empty** rating/response fields. Do not pre-populate resident judgments.

## Machine validation versus clinician validation

Machine validation on this freeze establishes only what the code checks: schema/structure, terminology/reference integrity, deterministic rule constraints, category eligibility, expected deterministic state transition, answer-key consistency, implemented error-isolation checks, and resident-export leak checks.

It does **not** establish overall clinical realism, guideline completeness, optimal therapy, educational appropriateness, clinical validity, or calibrated learner difficulty. Those remain part of clinician/resident validation.

## Provenance

Per-assignment reproducibility fields are in [`batch_plan.json`](batch_plan.json) (VAL ID, scenario, family, category, sequence, inject flag), [`validation_manifest.json`](validation_manifest.json) (seed, control status, source snapshots, rule snapshots, validation statuses), and [`investigator_answer_key.json`](investigator_answer_key.json) (SYN ID, family, category, clean expected state, injected state).

Terminology versions recorded on this freeze (from the manifest; do not invent missing versions):

| Source | Version on this freeze |
| --- | --- |
| RXNORM | `08-Sep-2026` |
| LOINC | `2.83` |
| UCUM | `2.2` |
| ICD10CM | none supplied by API (`null`) |
| RXCLASS | none supplied by API (`null`) |
| DAILYMED | none supplied by API (`null`) |

## Limitations

- **Clinical distribution.** This set is not a prevalence-weighted or representative sample of inpatient medicine (`HF_INPATIENT` 13/24; `CAP_INPATIENT` 1/24).
- **Error-category distribution.** Several categories occur only once. This batch alone does **not** support stable category-specific psychometric estimates. Its immediate purpose is clinician validation of case quality and assessment-object integrity.
- **Missing category.** `f2_coprescription_omitted` is intentionally absent (`not_yet_implementable`).
- **Terminology ranking.** Official source ranking can produce technically source-valid but clinically atypical formulations or units (RxNorm solutions/gels, SI laboratory units). Those are among the issues clinician plausibility review should detect.

## Commands

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation/cliniproof_v1/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_TAXONOMY_V1 --output-dir data/validation/cliniproof_v1
```

Export **must** use `--output-dir data/validation/cliniproof_v1`. The default export directory is `data/validation/` and would overwrite the frozen V1 resident file. Do **not** re-run freeze expecting bit-identical live-API output; the committed files are the study source of truth.

`f2_coprescription_omitted` is not assigned here. Manuscript examples (steroid/PPI, opioid/bowel regimen) are not hard-coded.

## Files in this directory

| File | Audience | Contents |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Investigators / operators | Canonical `error_family` + `error_category` chosen before generation |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Residents | Blinded dashboard-shaped cases, including `CaseMonitoring` |
| [`investigator_answer_key.json`](investigator_answer_key.json) / [`.md`](investigator_answer_key.md) | Investigators only | Seeds, SYN IDs, family, category, clean expected state, injected state |
| [`validation_manifest.json`](validation_manifest.json) | Investigators | Freeze metadata, source versions |
| [`coverage_report.md`](coverage_report.md) | Investigators | Mix counts written at export |
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
