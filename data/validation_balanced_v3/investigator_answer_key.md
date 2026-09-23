# Investigator answer key

machine-validated synthetic resident-review cases pending clinician validation

Batch: `CLINIPROOF_BALANCED_V3`

## VAL-501

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_VOLUME_OVERLOAD`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260923:1201:HF_INPATIENT:HF_VOLUME_OVERLOAD`

## VAL-502

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_POST_DIURESIS`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_therapeutic_substitution`
- Rationale: A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.
- Seed: `20260923:1202:HF_INPATIENT:HF_POST_DIURESIS`

## VAL-503

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_WITH_WARFARIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260923:1203:HF_INPATIENT:HF_WITH_WARFARIN`

## VAL-504

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_MEDICATION_ADJUSTMENT`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_inpatient_substitution_not_reverted`
- Rationale: A home therapy temporarily replaced during hospitalization for formulary or protocol reasons was neither reverted nor explicitly re-decided at discharge.
- Seed: `20260923:1204:HF_INPATIENT:HF_MEDICATION_ADJUSTMENT`

## VAL-505

- Scenario: `HF_INPATIENT`
- Clinical profile: `HF_DISCHARGE_MONITORING`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1205:HF_INPATIENT:HF_DISCHARGE_MONITORING`

## VAL-506

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_RATE_CONTROL_APIXABAN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260923:1206:AF_ANTICOAGULATION:AF_RATE_CONTROL_APIXABAN`

## VAL-507

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_WARFARIN_INR`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260923:1207:AF_ANTICOAGULATION:AF_WARFARIN_INR`

## VAL-508

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_WITH_STATIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1208:AF_ANTICOAGULATION:AF_WITH_STATIN`

## VAL-509

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_HELD_NSAID`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260923:1209:AF_ANTICOAGULATION:AF_HELD_NSAID`

## VAL-510

- Scenario: `AF_ANTICOAGULATION`
- Clinical profile: `AF_POST_RATE_CONTROL`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1210:AF_ANTICOAGULATION:AF_POST_RATE_CONTROL`

## VAL-511

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_ACE_CCB`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260923:1211:HTN_INPATIENT:HTN_ACE_CCB`

## VAL-512

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_ACE_THIAZIDE`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1212:HTN_INPATIENT:HTN_ACE_THIAZIDE`

## VAL-513

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_CCB_STATIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_route_mismatch`
- Rationale: The discharge route differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1213:HTN_INPATIENT:HTN_CCB_STATIN`

## VAL-514

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_TRIPLE_THERAPY`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260923:1214:HTN_INPATIENT:HTN_TRIPLE_THERAPY`

## VAL-515

- Scenario: `HTN_INPATIENT`
- Clinical profile: `HTN_NEW_DIAGNOSIS`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1215:HTN_INPATIENT:HTN_NEW_DIAGNOSIS`

## VAL-516

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_METFORMIN_ACE`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260923:1216:T2DM_INPATIENT:T2DM_METFORMIN_ACE`

## VAL-517

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_METFORMIN_STATIN`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1217:T2DM_INPATIENT:T2DM_METFORMIN_STATIN`

## VAL-518

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_GLYCEMIC_STABILIZATION`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260923:1218:T2DM_INPATIENT:T2DM_GLYCEMIC_STABILIZATION`

## VAL-519

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_PENDING_DURATION`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260923:1219:T2DM_INPATIENT:T2DM_PENDING_DURATION`

## VAL-520

- Scenario: `T2DM_INPATIENT`
- Clinical profile: `T2DM_CONTROL`
- Generation strategy: `balanced_structured`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260923:1220:T2DM_INPATIENT:T2DM_CONTROL`

## VAL-521

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_TYPICAL_COUGH`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1221:CAP_INPATIENT:CAP_TYPICAL_COUGH`

## VAL-522

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_DYSPNEA_WHEEZE`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260923:1222:CAP_INPATIENT:CAP_DYSPNEA_WHEEZE`

## VAL-523

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_INPATIENT_ANTIBIOTIC`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260923:1223:CAP_INPATIENT:CAP_INPATIENT_ANTIBIOTIC`

## VAL-524

- Scenario: `CAP_INPATIENT`
- Clinical profile: `CAP_HOME_TRANSITION`
- Generation strategy: `balanced_structured`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260923:1224:CAP_INPATIENT:CAP_HOME_TRANSITION`

