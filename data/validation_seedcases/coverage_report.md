# Resident validation coverage

machine-validated synthetic resident-review cases pending clinician validation

TOTAL CASES: 24

## SCENARIOS

- GI_BLEED_ACUTE_CHANGE → 4
- HF_DECOMPENSATION → 4
- MEDREC_UNCERTAIN_HISTORY → 4
- OPAT_ENDOCARDITIS → 4
- POSTOP_ANTICOAGULATION → 4
- TRANSPLANT_CMV → 4

## CONTROL STATUS

- clean controls → 4
- error-bearing → 20

## ERROR TYPES

- f1_commission → 1
- f1_dose_mismatch → 2
- f1_omission → 3
- f1_therapeutic_substitution → 1
- f2_held_med_no_restart_plan → 3
- f2_hospital_only_continued → 2
- f2_insufficient_supply → 3
- f2_monitoring_not_arranged → 1
- f2_pending_decision_followup_missing → 4

## TERMINOLOGY COVERAGE

- unique medications: 19
- unique RXCUIs: 19
- unique diagnoses: 6
- unique ICD codes: 6
- unique labs: 6
- unique LOINC codes: 6
- unique UCUM units: 5

## LOINC COVERAGE

- cases with LOINC-backed labs: 24
- LOINC concepts used: 14682-9, 14749-6, 2823-3, 30934-4, 38875-1, 55782-7

## RULE COVERAGE

- FUROSEMIDE_HF_INDICATION (soft, enabled, source=RXCLASS): 4 cases
- NO_DUAL_ORAL_ANTICOAGULANT (hard, enabled, source=DAILYMED): 4 cases
- WARFARIN_INR_MONITORING (hard, enabled, source=DAILYMED): 4 cases

## VALIDATION

- clean cases passed: 24
- final frozen cases: 24
- cases with exactly one intended error: 20
- unexpected-error count: 0
