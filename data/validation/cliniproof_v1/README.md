# CLINIPROOF_TAXONOMY_V1

This directory is the study copy of batch **`CLINIPROOF_TAXONOMY_V1`**. It is a **new** validation set. It does **not** replace or rewrite `RESIDENT_VALIDATION_V1` (`VAL-001`–`VAL-024`).

Target `error_family` and `error_category` are specified in [`batch_plan.json`](batch_plan.json) **before** generation. The injector never asks an LLM which error to plant. If the requested category is ineligible, freeze **rejects** the assignment instead of substituting another category.

Public IDs: `VAL-201`–`VAL-224`. Internal sequences: `SYN-000801`–`SYN-000824`.

Dataset status: `machine-validated synthetic resident-review cases pending clinician validation`.

## Commands

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation/cliniproof_v1/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_TAXONOMY_V1 --output-dir data/validation/cliniproof_v1
```

Export **must** use `--output-dir data/validation/cliniproof_v1`. The default export directory is `data/validation/` and would overwrite the frozen V1 resident file.

`f2_coprescription_omitted` is not assigned here; the repository has no source-backed companion-prescription rule.
