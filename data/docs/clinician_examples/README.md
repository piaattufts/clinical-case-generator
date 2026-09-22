# Educational demonstration cases (not the resident-validation study)

These snapshots support the clinician walkthrough in the root [`README.md`](../../README.md). They were generated with the same pipeline as the study cases (`app/services/generation.py`, `use_openai=False` because `OPENAI_API_KEY` was empty) using sequences **901–904** and seed **20260926**. Those identifiers are **not** `VAL-*` study IDs and are **not** part of `RESIDENT_VALIDATION_V1` (or later batches).

| File | Internal id | Scenario | Error injection | Audience |
| --- | --- | --- | --- | --- |
| [`syn-000901.json`](syn-000901.json) | `SYN-000901` | `HF_INPATIENT` | none (clean) | Clinician teaching |
| [`syn-000902.json`](syn-000902.json) | `SYN-000902` | `AF_ANTICOAGULATION` | none (clean) | Clinician teaching |
| [`syn-000903.json`](syn-000903.json) | `SYN-000903` | `CAP_INPATIENT` | none (clean) | Clinician teaching |
| [`syn-000904.json`](syn-000904.json) | `SYN-000904` | `HF_INPATIENT` | one `omission` | **Investigator-only teaching** |

`SYN-000904.json` includes the planted-error answer key. Do **not** give that file, or the investigator-only README section that quotes it, to resident study participants. It is not a `VAL-*` case, but it teaches the injection method.

Commands used (after `db-init` and `bootstrap-reference-data`):

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 20260926 --start-index 901 --scenario HF_INPATIENT --no-inject-error
clinical-case-generator generate-synthetic-cases --count 1 --seed 20260926 --start-index 902 --scenario AF_ANTICOAGULATION --no-inject-error
clinical-case-generator generate-synthetic-cases --count 1 --seed 20260926 --start-index 903 --scenario CAP_INPATIENT --no-inject-error
clinical-case-generator generate-synthetic-cases --count 1 --seed 20260926 --start-index 904 --scenario HF_INPATIENT --inject-error
```

Case seed formula: `{seed}:{sequence}:{scenario}` (example: `20260926:901:HF_INPATIENT`).

Status language: machine-validated synthetic records pending clinician validation.
