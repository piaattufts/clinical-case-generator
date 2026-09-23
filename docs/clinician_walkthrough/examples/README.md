# Teaching snapshots

These four JSON files support the [clinician walkthrough](../README.md). They are not `VAL-*` study cases. They are not members of the current prospective sets `CLINIPROOF_BALANCED_V4` (VAL-701–VAL-724) or `CLINIPROOF_SEEDCASES_V3` (VAL-801–VAL-824).

They were generated with an earlier code path, template wording, sequences 901–904, and seed 20260926, without calling OpenAI. Some doses copy product strength or fall back to once daily. Current study charts use the curated regimen layer instead.

| File | Internal id | Scenario | Error injection | Audience |
| --- | --- | --- | --- | --- |
| [`syn-000901.json`](syn-000901.json) | `SYN-000901` | Heart-failure inpatient | none (clean) | Clinician teaching |
| [`syn-000902.json`](syn-000902.json) | `SYN-000902` | Atrial fibrillation | none (clean) | Clinician teaching |
| [`syn-000903.json`](syn-000903.json) | `SYN-000903` | Pneumonia | none (clean) | Clinician teaching |
| [`syn-000904.json`](syn-000904.json) | `SYN-000904` | Heart-failure inpatient | one medication omitted at discharge | **Investigator-only teaching** |

`SYN-000904.json` includes the answer key. Do not give that file to resident study participants.

Each case seed is `{seed}:{sequence}:{scenario}`. The heart-failure teaching case uses `20260926:901:HF_INPATIENT`.

Until a clinician finishes review, treat these records as machine-validated synthetic cases pending clinician validation.
