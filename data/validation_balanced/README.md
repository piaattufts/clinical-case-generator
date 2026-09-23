# Prospective balanced CliniProof set (`CLINIPROOF_BALANCED_V2`)

**Status: active prospective validation set.**

This directory holds one of the two active CliniProof batches. Public identifiers are VAL-301 through VAL-324. `generation_strategy = balanced_structured`.

It does **not** replace or regenerate archived `CLINIPROOF_TAXONOMY_V1` in [`data/validation/`](../validation/). The other active set is [`CLINIPROOF_SEEDCASES_V1`](../validation_seedcases/).

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. Passing the clean-case diversity audit does not mean the cases are clinically validated.

## Why this batch exists

The V1 freeze reused one heart-failure skeleton for thirteen of twenty-four cases. Those charts shared the same admission diagnosis, the same three symptoms, the same “several days / worsening” course, nearly the same medication list, the same home disposition, and the same seven-day primary-care follow-up. The planted CliniProof error was the main visible difference. That is not clinical uniqueness.

This batch specifies a distinct clinical profile **before** error injection. Generation order is:

1. Choose a broad scenario family.
2. Choose a named clinical profile.
3. Construct a clean patient from that profile.
4. Validate the clean case.
5. Confirm eligibility for the assigned category.
6. Inject that category, or skip it for a control.
7. Validate again and freeze.

## Planned mix

| Family | Count |
| --- | ---: |
| Heart failure (`HF_INPATIENT`) | 5 |
| Atrial fibrillation (`AF_ANTICOAGULATION`) | 5 |
| Hypertension (`HTN_INPATIENT`) | 5 |
| Type 2 diabetes (`T2DM_INPATIENT`) | 5 |
| Community-acquired pneumonia (`CAP_INPATIENT`) | 4 |

Four cases are clean controls. The remaining twenty cover the implemented Family 1 and Family 2 categories. No category is permanently tied to one diagnosis except where eligibility requires it (for example warfarin plus INR for `f2_monitoring_not_arranged`).

## Files

| File | Role |
| --- | --- |
| [`batch_plan.json`](batch_plan.json) | VAL id, scenario, clinical profile, family, category, sequence |
| [`field_classification.md`](field_classification.md) | Which generator fields vary, stay constant, or are omitted |
| `resident_validation_cases.json` | Blinded resident export (written by freeze/export) |
| `investigator_answer_key.json` | Concealed targets |
| `validation_manifest.json` | Seed and snapshot metadata |
| `coverage_report.md` | Terminology and error coverage |
| `diversity_report.md` | Clean-case uniqueness audit |
| `readable/` | One-stage clinician packet and worksheet |

## Freeze and export

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V2 --output-dir data/validation_balanced
python -m app.services.readable_packets --resident data/validation_balanced/resident_validation_cases.json --investigator data/validation_balanced/investigator_answer_key.json --output-dir data/validation_balanced/readable --batch-code CLINIPROOF_BALANCED_V2
```

Master seed: `20260923`. Case seed: `{master_seed}:{sequence}:{scenario}:{clinical_profile}`.
