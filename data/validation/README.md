# CLINIPROOF_TAXONOMY_V1

This directory is the **current** CliniProof clinician-validation batch. Batch code **`CLINIPROOF_TAXONOMY_V1`**. It is the frozen validation set generated using the canonical CliniProof `error_family` / `error_category` implementation.

`CLINIPROOF_TAXONOMY_V1` covers all **currently implemented** CliniProof error categories. That is **not** complete coverage of the full conceptual taxonomy. `f2_coprescription_omitted` remains specified by the conceptual taxonomy but is `not_yet_implementable` because a sufficiently source-backed deterministic companion-prescription rule has not yet been implemented.

Target `error_family` and `error_category` are specified in [`batch_plan.json`](batch_plan.json) **before** generation. The injector never asks an LLM which error to plant. If the requested category is unknown, ineligible, or `not_yet_implementable`, freeze **rejects** the assignment and aborts the batch instead of substituting another category.

All records remain **machine-validated synthetic resident-review cases pending clinician validation**.

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
- Unknown, ineligible, and `not_yet_implementable` categories **abort**. They do **not** silently substitute another category.
- For every error-bearing case, planned canonical category = injected `kind` = investigator answer-key category.
- Every error-bearing case has **exactly one** intended injected assessment target.
- Clean controls have **zero** injected targets.
- Freeze-time audit also recorded: eligibility passed, clean validation passed, post-injection assessment validation passed, no silent fallback.

Default operator commands (this directory is the default plan and export location):

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch
```

The committed JSON and Markdown files are the **study source of truth**. Do **not** re-run freeze expecting bit-identical live-API output.

## Family 1 versus Family 2

Do **not** read this batch as “every error-bearing case has exactly one medication-list discrepancy.” That is true of Family 1 list-transition errors. It is **not** true of Family 2.

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
- **Error-category distribution.** Several categories occur only once. This batch alone does **not** support stable category-specific psychometric estimates. It is primarily intended for clinician assessment of clinical plausibility, assessment-object integrity, error fidelity, detectability, and isolation.
- **Missing category.** `f2_coprescription_omitted` is intentionally absent (`not_yet_implementable`).
- **Terminology ranking.** Official source ranking can produce technically source-valid but clinically atypical formulations or units (RxNorm solutions/gels, SI laboratory units). Those are among the issues clinician plausibility review should detect.

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
| [`readable/`](readable/) | See below | Derived Markdown clinician-validation views |

## Human-readable clinician validation packets

These files are generated from the frozen JSON. They do **not** replace it.

**Where should I start?**

| If you are... | Start here |
| --- | --- |
| Resident or clinician reviewing cases | [`readable/all_cases.md`](readable/all_cases.md) |
| Clinician validating clinical plausibility | [`readable/plausibility_only_packet.md`](readable/plausibility_only_packet.md) |
| Investigator / expert validator | [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) |
| Medical educator reviewing the framework | [`readable/validation_rubric.md`](readable/validation_rubric.md) |
| Clinician or resident curious how CliniProof works | [`readable/how_cliniproof_works.md`](readable/how_cliniproof_works.md) |
| Clinical informatics / AI engineer | [`readable/developer_notes.md`](readable/developer_notes.md) |

**Safe for residents and plausibility-only review** (resident-visible content; no per-case planted-error answers):

- [`readable/all_cases.md`](readable/all_cases.md)
- [`readable/plausibility_only_packet.md`](readable/plausibility_only_packet.md)
- [`readable/cases/VAL-201.md`](readable/cases/VAL-201.md) through [`VAL-224.md`](readable/cases/VAL-224.md)
- [`readable/how_cliniproof_works.md`](readable/how_cliniproof_works.md) (mechanisms only; no per-case answers)
- [`readable/developer_notes.md`](readable/developer_notes.md) (generic implementation; no per-case answers)
- [`readable/validation_rubric.md`](readable/validation_rubric.md) (rubric only; no per-case answers)

**Investigator / validator only — do not distribute to resident participants:**

- [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md)

Index: [`readable/README.md`](readable/README.md). Regenerate with `python scripts/build_readable_validation_packets.py`.

Shared pipeline, official sources, and limitations: [`../../README.md`](../../README.md).

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
