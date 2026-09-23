# Investigator answer key

machine-validated synthetic resident-review cases pending clinician validation

Batch: `CLINIPROOF_BALANCED_V4`

## VAL-701

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_VOLUME_OVERLOAD`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260925:1401:HF_INPATIENT:HF_VOLUME_OVERLOAD`

## VAL-702

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_POST_DIURESIS`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_therapeutic_substitution`
- Rationale: A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.
- Seed: `20260925:1402:HF_INPATIENT:HF_POST_DIURESIS`

## VAL-703

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_WITH_WARFARIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260925:1403:HF_INPATIENT:HF_WITH_WARFARIN`

## VAL-704

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_MEDICATION_ADJUSTMENT`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_inpatient_substitution_not_reverted`
- Rationale: A home therapy temporarily replaced during hospitalization for formulary or protocol reasons was neither reverted nor explicitly re-decided at discharge.
- Seed: `20260925:1404:HF_INPATIENT:HF_MEDICATION_ADJUSTMENT`

## VAL-705

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_DISCHARGE_MONITORING`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260925:1405:HF_INPATIENT:HF_DISCHARGE_MONITORING`

## VAL-706

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_RATE_CONTROL_APIXABAN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260925:1406:AF_ANTICOAGULATION:AF_RATE_CONTROL_APIXABAN`

## VAL-707

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_WARFARIN_INR`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260925:1407:AF_ANTICOAGULATION:AF_WARFARIN_INR`

## VAL-708

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_WITH_STATIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260925:1408:AF_ANTICOAGULATION:AF_WITH_STATIN`

## VAL-709

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_HELD_NSAID`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260925:1409:AF_ANTICOAGULATION:AF_HELD_NSAID`

## VAL-710

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_POST_RATE_CONTROL`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260925:1410:AF_ANTICOAGULATION:AF_POST_RATE_CONTROL`

## VAL-711

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_ACE_CCB`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260925:1411:HTN_INPATIENT:HTN_ACE_CCB`

## VAL-712

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_ACE_THIAZIDE`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260925:1412:HTN_INPATIENT:HTN_ACE_THIAZIDE`

## VAL-713

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_CCB_STATIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_route_mismatch`
- Rationale: The discharge route differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260925:1413:HTN_INPATIENT:HTN_CCB_STATIN`

## VAL-714

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_TRIPLE_THERAPY`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260925:1414:HTN_INPATIENT:HTN_TRIPLE_THERAPY`

## VAL-715

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_NEW_DIAGNOSIS`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260925:1415:HTN_INPATIENT:HTN_NEW_DIAGNOSIS`

## VAL-716

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_METFORMIN_ACE`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260925:1416:T2DM_INPATIENT:T2DM_METFORMIN_ACE`

## VAL-717

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_METFORMIN_STATIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260925:1417:T2DM_INPATIENT:T2DM_METFORMIN_STATIN`

## VAL-718

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_GLYCEMIC_STABILIZATION`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260925:1418:T2DM_INPATIENT:T2DM_GLYCEMIC_STABILIZATION`

## VAL-719

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_PENDING_DURATION`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: A pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260925:1419:T2DM_INPATIENT:T2DM_PENDING_DURATION`

## VAL-720

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_CONTROL`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260925:1420:T2DM_INPATIENT:T2DM_CONTROL`

## VAL-721

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_TYPICAL_COUGH`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260925:1421:CAP_INPATIENT:CAP_TYPICAL_COUGH`

## VAL-722

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_DYSPNEA_WHEEZE`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260925:1422:CAP_INPATIENT:CAP_DYSPNEA_WHEEZE`

## VAL-723

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_INPATIENT_ANTIBIOTIC`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260925:1423:CAP_INPATIENT:CAP_INPATIENT_ANTIBIOTIC`

## VAL-724

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_HOME_TRANSITION`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260925:1424:CAP_INPATIENT:CAP_HOME_TRANSITION`

