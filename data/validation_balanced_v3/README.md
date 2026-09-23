# Prospective balanced CliniProof set (`CLINIPROOF_BALANCED_V3`)

> Historical document. This batch was frozen before the final clinical-regimen QC and is preserved as provenance.
> Current prospective sets: [`CLINIPROOF_BALANCED_V4`](../validation_balanced_v4/README.md) and [`CLINIPROOF_SEEDCASES_V3`](../validation_seedcases_v3/README.md).

**Status: archived preclinical revision.** This freeze is **not** an active prospective study set.

This directory preserves `CLINIPROOF_BALANCED_V3`. Public identifiers are VAL-501 through VAL-524. `generation_strategy = balanced_structured`.

It does **not** replace archived `CLINIPROOF_TAXONOMY_V1` in [`data/validation/`](../validation/) or the preclinical-QC freeze `CLINIPROOF_BALANCED_V2` in [`data/validation_balanced/`](../validation_balanced/). The current balanced set is [`CLINIPROOF_BALANCED_V4`](../validation_balanced_v4/README.md).

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. Passing software checks does not mean the cases are clinically validated.

## Why this revision exists

`CLINIPROOF_BALANCED_V2` was merged as a frozen preclinical artifact. Clinical QC found lab value/unit mismatches, indication/PMH gaps, weak hospitalization context for some hypertension and diabetes profiles, and other chart-coherence problems. Those generator defects were fixed and this revision was frozen under new VAL identifiers rather than mutating V2 in place. A later regimen QC produced `CLINIPROOF_BALANCED_V4` without altering this directory.

## Planned mix

| Family | Count |
| --- | ---: |
| Heart failure (`HF_INPATIENT`) | 5 |
| Atrial fibrillation (`AF_ANTICOAGULATION`) | 5 |
| Hypertension (`HTN_INPATIENT`) | 5 |
| Type 2 diabetes (`T2DM_INPATIENT`) | 5 |
| Community-acquired pneumonia (`CAP_INPATIENT`) | 4 |

Four cases are clean controls. The remaining twenty cover the implemented Family 1 and Family 2 categories.

## Files

| File | Role |
| --- | --- |
| [`batch_plan.json`](batch_plan.json) | VAL id, scenario, clinical profile, family, category, sequence |
| `resident_validation_cases.json` | Blinded resident export (written by freeze/export) |
| `investigator_answer_key.json` | Concealed targets |
| `validation_manifest.json` | Seed and snapshot metadata |
| `coverage_report.md` | Terminology and error coverage |
| `diversity_report.md` | Clean-case uniqueness audit |
| `readable/` | One-stage clinician packet and worksheet |

## Freeze and export

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3 --output-dir data/validation_balanced_v3
python -m app.services.readable_packets --resident data/validation_balanced_v3/resident_validation_cases.json --investigator data/validation_balanced_v3/investigator_answer_key.json --output-dir data/validation_balanced_v3/readable --batch-code CLINIPROOF_BALANCED_V3
```

Master seed: `20260923`. Case seed: `{master_seed}:{sequence}:{scenario}:{clinical_profile}`.
