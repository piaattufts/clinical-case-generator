# Active prospective validation batches

machine-validated synthetic resident-review cases pending clinician validation

This investigator-facing comparison is descriptive. It does not rank one
generation strategy as better than the other. It does not regenerate or
modify either frozen batch. Uniqueness is judged on clean-case structure
reconstructed from resident-facing fields plus investigator labels.
Age, sex, exact vitals, and exact laboratory numbers are excluded.

Left: `CLINIPROOF_BALANCED_V3` (`balanced_structured`).
Right: `CLINIPROOF_SEEDCASES_V2` (`resident_seed_guided`).

The archived original freeze `CLINIPROOF_TAXONOMY_V1` is excluded.

| Measure | CLINIPROOF_BALANCED_V3 | CLINIPROOF_SEEDCASES_V2 |
| --- | ---: | ---: |
| Cases | 24 | 24 |
| Generation strategy | balanced_structured | resident_seed_guided |
| Scenario / archetype families | 5 | 6 |
| Unique clinical profiles | 24 | 24 |
| Unique diagnoses | 5 | 6 |
| Unique specialties | 3 | 5 |
| Unique symptom sets | 14 | 12 |
| Unique home-medication sets | 21 | 21 |
| Unique hospital-course profiles | 24 | 24 |
| Unique follow-up profiles | 24 | 21 |
| Unique imaging sets | 2 | 3 |
| Unique consult sets | 3 | 7 |
| Exact duplicate fingerprints | 0 | 0 |
| Near-duplicate warnings | 2 | 7 |
| Closest-pair similarity | 0.7567 | 0.79 |
| Family 1 count | 11 | 7 |
| Family 2 count | 9 | 13 |
| Clean-control count | 4 | 4 |

## Scenario / archetype distribution

### Left

- `AF_ANTICOAGULATION`: 5
- `CAP_INPATIENT`: 4
- `HF_INPATIENT`: 5
- `HTN_INPATIENT`: 5
- `T2DM_INPATIENT`: 5

### Right

- `GI_BLEED_ACUTE_CHANGE`: 4
- `HF_DECOMPENSATION`: 4
- `MEDREC_UNCERTAIN_HISTORY`: 4
- `OPAT_ENDOCARDITIS`: 4
- `POSTOP_ANTICOAGULATION`: 4
- `TRANSPLANT_CMV`: 4

## Diagnosis distribution

### Left

- Acute systolic (congestive) heart failure: 5
- Essential (primary) hypertension: 5
- Lobar pneumonia, unspecified organism: 4
- Paroxysmal atrial fibrillation: 5
- Type 2 diabetes mellitus with hyperglycemia: 5

### Right

- Acute and subacute infective endocarditis: 4
- Acute systolic (congestive) heart failure: 4
- Delirium due to known physiological condition: 4
- Fracture of unspecified part of neck of right femur, initial encounter for closed fracture: 4
- Gastrointestinal hemorrhage, unspecified: 4
- Other cytomegaloviral diseases: 4

## Specialty distribution

### Left

- cardiology: 10
- general medicine: 10
- pulmonology: 4

### Right

- cardiology: 4
- general medicine: 8
- infectious disease: 4
- nephrology: 4
- orthopedics: 4

## Closest pairs

- Left closest pair: VAL-517 vs VAL-520 (0.7567)
- Right closest pair: VAL-605 vs VAL-607 (0.79)

## Method note

`CLINIPROOF_BALANCED_V3` uses named clinical profiles inside the five
template inpatient families. `CLINIPROOF_SEEDCASES_V2` uses resident-authored
seed archetypes plus named profiles. Both are active prospective sets after
clinical-coherence QC. `CLINIPROOF_BALANCED_V2` and `CLINIPROOF_SEEDCASES_V1`
remain preclinical-QC archives. `CLINIPROOF_TAXONOMY_V1` remains archived
historical provenance. Human clinician review is still required.
