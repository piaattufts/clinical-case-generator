# Resident validation coverage

machine-validated synthetic resident-review cases pending clinician validation

TOTAL CASES: 24

## SCENARIOS

- AF_ANTICOAGULATION → 5
- CAP_INPATIENT → 4
- HF_INPATIENT → 5
- HTN_INPATIENT → 5
- T2DM_INPATIENT → 5

## CONTROL STATUS

- clean controls → 5
- error-bearing → 19

## ERROR TYPES

- dose_mismatch → 5
- frequency_mismatch → 5
- incorrect_continuation → 3
- omission → 6

## TERMINOLOGY COVERAGE

- unique medications: 14
- unique RXCUIs: 14
- unique diagnoses: 5
- unique ICD codes: 5
- unique labs: 7
- unique LOINC codes: 7
- unique UCUM units: 5

## LOINC COVERAGE

- cases with LOINC-backed labs: 24
- LOINC concepts used: 14682-9, 14749-6, 2823-3, 2951-2, 30934-4, 38875-1, 55782-7

## RULE COVERAGE

- FUROSEMIDE_HF_INDICATION (soft, enabled, source=RXCLASS): 5 cases
- NO_DUAL_ORAL_ANTICOAGULANT (hard, enabled, source=DAILYMED): 5 cases
- WARFARIN_INR_MONITORING (hard, enabled, source=DAILYMED): 5 cases

## VALIDATION

- clean cases passed: 24
- final frozen cases: 24
- cases with exactly one intended error: 19
- unexpected-error count: 0
