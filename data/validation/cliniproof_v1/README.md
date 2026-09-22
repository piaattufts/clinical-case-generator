# CLINIPROOF_TAXONOMY_V1

This directory is the study copy of batch **`CLINIPROOF_TAXONOMY_V1`**. It is a **new** validation set. It does **not** replace or rewrite `RESIDENT_VALIDATION_V1` (`VAL-001`–`VAL-024`).

Target `error_family` and `error_category` are specified in [`batch_plan.json`](batch_plan.json) **before** generation. The injector never asks an LLM which error to plant. If the requested category is ineligible, freeze **rejects** the assignment and aborts the batch instead of substituting another category.

| Field | Value |
| --- | --- |
| Batch code | `CLINIPROOF_TAXONOMY_V1` |
| Public IDs | `VAL-201`–`VAL-224` |
| Internal sequences | `SYN-000801`–`SYN-000824` |
| Master seed | `20260922` |
| Case seed | `{master_seed}:{sequence}:{scenario}` |
| Mix | 4 clean controls, 20 error-bearing |
| OpenAI | not used |
| Export audit | passed |
| Exported at | `2026-09-22T15:40:14.870878+00:00` |
| Dataset status | `machine-validated synthetic resident-review cases pending clinician validation` |

Give residents only `resident_validation_cases.json` and `resident_review_worksheet.csv`. Keep the investigator key, manifest, coverage files, and this README off the resident packet.

## Commands

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation/cliniproof_v1/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_TAXONOMY_V1 --output-dir data/validation/cliniproof_v1
```

Export **must** use `--output-dir data/validation/cliniproof_v1`. The default export directory is `data/validation/` and would overwrite the frozen V1 resident file.

`f2_coprescription_omitted` is not assigned here; the repository has no source-backed companion-prescription rule.

Machine validation means the requested category was injected as specified, structural/terminology constraints passed, implemented deterministic clinical rules passed, and no mechanically detectable extra discrepancy was found. Clinician review still evaluates clinical coherence, error fidelity, evidentiary sufficiency, error isolation, cue integrity, and educational appropriateness.
