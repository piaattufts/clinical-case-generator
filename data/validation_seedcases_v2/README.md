# Prospective seed-guided CliniProof set (`CLINIPROOF_SEEDCASES_V2`)

**Status: active prospective validation set.**

This directory holds one of the two active CliniProof batches. Public identifiers are VAL-601 through VAL-624. `generation_strategy = resident_seed_guided`.

Resident-authored seed documents in [`data/seed_cases/resident_authored/`](../seed_cases/resident_authored/) are immutable design references. They are not copied into these charts.

The preclinical-QC freeze `CLINIPROOF_SEEDCASES_V1` remains in [`data/validation_seedcases/`](../validation_seedcases/). Archived `CLINIPROOF_TAXONOMY_V1` remains in [`data/validation/`](../validation/). The other active set is [`CLINIPROOF_BALANCED_V3`](../validation_balanced_v3/).

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

## Archetypes

Four profiles are generated from each of six resident-derived archetypes:

1. Medication-history uncertainty / delirium
2. Acute heart-failure decompensation
3. Outpatient parenteral antimicrobial therapy / endocarditis
4. Kidney-transplant infection and immunosuppression transitions
5. Postoperative anticoagulation after hip fracture
6. Gastrointestinal bleeding with anticoagulation or discharge-transition decisions

## Freeze and export

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v2/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2 --output-dir data/validation_seedcases_v2
python -m app.services.readable_packets --resident data/validation_seedcases_v2/resident_validation_cases.json --investigator data/validation_seedcases_v2/investigator_answer_key.json --output-dir data/validation_seedcases_v2/readable --batch-code CLINIPROOF_SEEDCASES_V2
```

Master seed: `20260924`.
