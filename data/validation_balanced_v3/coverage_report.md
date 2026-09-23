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

- clean controls → 4
- error-bearing → 20

## ERROR TYPES

- f1_commission → 1
- f1_dose_mismatch → 3
- f1_frequency_mismatch → 2
- f1_omission → 3
- f1_route_mismatch → 1
- f1_therapeutic_substitution → 1
- f2_held_med_no_restart_plan → 2
- f2_hospital_only_continued → 1
- f2_inpatient_substitution_not_reverted → 1
- f2_insufficient_supply → 2
- f2_monitoring_not_arranged → 2
- f2_pending_decision_followup_missing → 1

## TERMINOLOGY COVERAGE

- unique medications: 16
- unique RXCUIs: 16
- unique diagnoses: 7
- unique ICD codes: 7
- unique labs: 7
- unique LOINC codes: 7
- unique UCUM units: 5

## LOINC COVERAGE

- cases with LOINC-backed labs: 24
- LOINC concepts used: 1558-6, 2160-0, 2823-3, 2951-2, 30934-4, 38875-1, 55782-7

## RULE COVERAGE

- FUROSEMIDE_HF_INDICATION (soft, enabled, source=RXCLASS): 4 cases
- NO_DUAL_ORAL_ANTICOAGULANT (hard, enabled, source=DAILYMED): 3 cases
- WARFARIN_INR_MONITORING (hard, enabled, source=DAILYMED): 3 cases

## VALIDATION

- clean cases passed: 24
- final frozen cases: 24
- cases with exactly one intended error: 20
- unexpected-error count: 0
