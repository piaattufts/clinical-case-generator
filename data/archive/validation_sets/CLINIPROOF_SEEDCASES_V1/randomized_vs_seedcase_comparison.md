# Randomized template batch versus resident-seed-guided batch

> Historical document. This compares superseded freezes `CLINIPROOF_TAXONOMY_V1` and `CLINIPROOF_SEEDCASES_V1`.
> Current comparison: [`../validation_comparison/active_batch_comparison.md`](../validation_comparison/active_batch_comparison.md).

machine-validated synthetic resident-review cases pending clinician validation

This comparison uses exported charts. It does not regenerate or modify
either frozen batch. Uniqueness is judged on clean-case structure
reconstructed from resident-facing fields plus investigator labels.
Age, sex, exact vitals, and exact laboratory numbers are excluded.

Left: `CLINIPROOF_TAXONOMY_V1` (`randomized_template` unless labeled).
Right: `CLINIPROOF_SEEDCASES_V1` (`resident_seed_guided` unless labeled).

| Measure | CLINIPROOF_TAXONOMY_V1 | CLINIPROOF_SEEDCASES_V1 |
| --- | ---: | ---: |
| Cases | 24 | 24 |
| Scenario / archetype families | 5 | 6 |
| Unique clinical profiles | 1 | 24 |
| Unique diagnoses | 5 | 6 |
| Unique symptom sets | 5 | 12 |
| Unique home-medication sets | 7 | 21 |
| Unique hospital-course profiles | 1 | 24 |
| Unique follow-up profiles | 3 | 21 |
| Exact duplicate fingerprints | 19 | 0 |
| Near-duplicate warnings | 0 | 7 |
| Closest-pair similarity | 1.0 | 0.79 |

## Families

### Left

- `AF_ANTICOAGULATION`: 3
- `CAP_INPATIENT`: 1
- `HF_INPATIENT`: 13
- `HTN_INPATIENT`: 4
- `T2DM_INPATIENT`: 3

### Right

- `GI_BLEED_ACUTE_CHANGE`: 4
- `HF_DECOMPENSATION`: 4
- `MEDREC_UNCERTAIN_HISTORY`: 4
- `OPAT_ENDOCARDITIS`: 4
- `POSTOP_ANTICOAGULATION`: 4
- `TRANSPLANT_CMV`: 4

## Error-category coverage

### Left

- `f1_commission`: 2
- `f1_dose_mismatch`: 2
- `f1_frequency_mismatch`: 2
- `f1_omission`: 3
- `f1_route_mismatch`: 1
- `f1_therapeutic_substitution`: 1
- `f2_held_med_no_restart_plan`: 2
- `f2_hospital_only_continued`: 1
- `f2_inpatient_substitution_not_reverted`: 1
- `f2_insufficient_supply`: 2
- `f2_monitoring_not_arranged`: 2
- `f2_pending_decision_followup_missing`: 1
- `none`: 4

### Right

- `f1_commission`: 1
- `f1_dose_mismatch`: 2
- `f1_omission`: 3
- `f1_therapeutic_substitution`: 1
- `f2_held_med_no_restart_plan`: 3
- `f2_hospital_only_continued`: 2
- `f2_insufficient_supply`: 3
- `f2_monitoring_not_arranged`: 1
- `f2_pending_decision_followup_missing`: 4
- `none`: 4

## Closest pairs

- Left closest pair: VAL-201 vs VAL-207 (1.0)
- Right closest pair: VAL-405 vs VAL-407 (0.79)

## Method note

`CLINIPROOF_TAXONOMY_V1` is generated from structured/randomized inpatient
scenario families. `CLINIPROOF_SEEDCASES_V1` is generated from resident-authored
seed archetypes plus named clinical profiles. Neither batch is declared the
study dataset by this report. Human clinician review is still required.
