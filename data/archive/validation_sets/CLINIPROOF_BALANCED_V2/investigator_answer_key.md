# Investigator answer key

machine-validated synthetic resident-review cases pending clinician validation

Batch: `CLINIPROOF_BALANCED_V2`

## VAL-301

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_VOLUME_OVERLOAD`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260923:1001:HF_INPATIENT:HF_VOLUME_OVERLOAD`

## VAL-302

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_POST_DIURESIS`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_therapeutic_substitution`
- Rationale: A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.
- Seed: `20260923:1002:HF_INPATIENT:HF_POST_DIURESIS`

## VAL-303

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_WITH_WARFARIN`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260923:1003:HF_INPATIENT:HF_WITH_WARFARIN`

## VAL-304

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_MEDICATION_ADJUSTMENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_inpatient_substitution_not_reverted`
- Rationale: A home therapy temporarily replaced during hospitalization for formulary or protocol reasons was neither reverted nor explicitly re-decided at discharge.
- Seed: `20260923:1004:HF_INPATIENT:HF_MEDICATION_ADJUSTMENT`

## VAL-305

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_DISCHARGE_MONITORING`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1005:HF_INPATIENT:HF_DISCHARGE_MONITORING`

## VAL-306

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_RATE_CONTROL_APIXABAN`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260923:1006:AF_ANTICOAGULATION:AF_RATE_CONTROL_APIXABAN`

## VAL-307

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_WARFARIN_INR`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260923:1007:AF_ANTICOAGULATION:AF_WARFARIN_INR`

## VAL-308

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_WITH_STATIN`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1008:AF_ANTICOAGULATION:AF_WITH_STATIN`

## VAL-309

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_HELD_NSAID`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260923:1009:AF_ANTICOAGULATION:AF_HELD_NSAID`

## VAL-310

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_POST_RATE_CONTROL`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1010:AF_ANTICOAGULATION:AF_POST_RATE_CONTROL`

## VAL-311

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_ACE_CCB`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260923:1011:HTN_INPATIENT:HTN_ACE_CCB`

## VAL-312

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_ACE_THIAZIDE`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1012:HTN_INPATIENT:HTN_ACE_THIAZIDE`

## VAL-313

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_CCB_STATIN`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_route_mismatch`
- Rationale: The discharge route differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1013:HTN_INPATIENT:HTN_CCB_STATIN`

## VAL-314

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_TRIPLE_THERAPY`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260923:1014:HTN_INPATIENT:HTN_TRIPLE_THERAPY`

## VAL-315

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_NEW_DIAGNOSIS`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1015:HTN_INPATIENT:HTN_NEW_DIAGNOSIS`

## VAL-316

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_METFORMIN_ACE`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260923:1016:T2DM_INPATIENT:T2DM_METFORMIN_ACE`

## VAL-317

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_METFORMIN_STATIN`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1017:T2DM_INPATIENT:T2DM_METFORMIN_STATIN`

## VAL-318

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_GLYCEMIC_STABILIZATION`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260923:1018:T2DM_INPATIENT:T2DM_GLYCEMIC_STABILIZATION`

## VAL-319

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_PENDING_DURATION`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260923:1019:T2DM_INPATIENT:T2DM_PENDING_DURATION`

## VAL-320

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_CONTROL`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1020:T2DM_INPATIENT:T2DM_CONTROL`

## VAL-321

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_TYPICAL_COUGH`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1021:CAP_INPATIENT:CAP_TYPICAL_COUGH`

## VAL-322

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_DYSPNEA_WHEEZE`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1022:CAP_INPATIENT:CAP_DYSPNEA_WHEEZE`

## VAL-323

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_INPATIENT_ANTIBIOTIC`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260923:1023:CAP_INPATIENT:CAP_INPATIENT_ANTIBIOTIC`

## VAL-324

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_HOME_TRANSITION`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260923:1024:CAP_INPATIENT:CAP_HOME_TRANSITION`

