# Prospective seed-guided CliniProof set (`CLINIPROOF_SEEDCASES_V1`)

**Status: active prospective validation set.**

This directory holds one of the two active CliniProof batches. Public identifiers are VAL-401 through VAL-424. `generation_strategy = resident_seed_guided`.

It does **not** replace or regenerate:

- archived `CLINIPROOF_TAXONOMY_V1` in [`data/validation/`](../validation/)
- active `CLINIPROOF_BALANCED_V2` in [`data/validation_balanced/`](../validation_balanced/)

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. Passing the diversity audit does not mean the cases are clinically validated.

## Origin

Clinical structure comes from abstracted archetypes in [`data/seed_cases/`](../seed_cases/). Resident-authored DOCX files are not copied. Patient identifiers, source wording, and exact source laboratory sequences are not reproduced. Canonical codes continue to come from RxNorm, ICD-10-CM, LOINC, and UCUM.

## Freeze and export

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V1 --output-dir data/validation_seedcases
python scripts/build_readable_validation_packets.py --resident data/validation_seedcases/resident_validation_cases.json --investigator data/validation_seedcases/investigator_answer_key.json --output-dir data/validation_seedcases/readable --batch-code CLINIPROOF_SEEDCASES_V1
```

Master seed: `20260924`. Case seed: `{master_seed}:{sequence}:{archetype}:{clinical_profile}`.
