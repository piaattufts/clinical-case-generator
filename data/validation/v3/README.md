# RESIDENT_VALIDATION_V3

Independent freeze of 24 machine-validated synthetic resident-review cases pending clinician validation. Same five inpatient families and error mix as V1. New master seed, sequences, and VAL IDs.

| Field | Value |
| --- | --- |
| Batch code | `RESIDENT_VALIDATION_V3` |
| Master seed | `20260924` |
| Case seed formula | `{master_seed}:{sequence}:{scenario}` |
| Internal case IDs | `SYN-000301`–`SYN-000324` |
| Frozen public IDs | `VAL-049`–`VAL-072` |
| OpenAI | **not used** (`freeze-validation-batch` hardcodes `use_openai=False`) |

Plan: [`batch_plan.json`](batch_plan.json). Export blinded resident JSON and investigator files into **this directory** (`--output-dir data/validation/v3`). Do not export into `data/validation/` (that overwrites V1).

```bash
clinical-case-generator freeze-validation-batch --plan data/validation/v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V3 --output-dir data/validation/v3
```

Give residents only `resident_validation_cases.json` and `resident_review_worksheet.csv`. Keep this README, the answer key, the manifest, the plan, and coverage files investigator-only.

Shared pipeline, sources, and planted-error mechanics: [`../README.md`](../README.md).
