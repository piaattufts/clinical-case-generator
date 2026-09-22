# Investigator answer key

machine-validated synthetic resident-review cases pending clinician validation

Batch: `CLINIPROOF_TAXONOMY_V1`

## VAL-201

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260922:801:HF_INPATIENT`

## VAL-202

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260922:802:HF_INPATIENT`

## VAL-203

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260922:803:HF_INPATIENT`

## VAL-204

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_route_mismatch`
- Rationale: The discharge route differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260922:804:HF_INPATIENT`

## VAL-205

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260922:805:HF_INPATIENT`

## VAL-206

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_therapeutic_substitution`
- Rationale: A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.
- Seed: `20260922:806:HF_INPATIENT`

## VAL-207

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260922:807:HF_INPATIENT`

## VAL-208

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260922:808:HF_INPATIENT`

## VAL-209

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260922:809:HF_INPATIENT`

## VAL-210

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260922:810:HF_INPATIENT`

## VAL-211

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_inpatient_substitution_not_reverted`
- Rationale: A home therapy temporarily replaced during hospitalization for formulary or protocol reasons was neither reverted nor explicitly re-decided at discharge.
- Seed: `20260922:811:HF_INPATIENT`

## VAL-212

- Scenario: `HF_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260922:812:HF_INPATIENT`

## VAL-213

- Scenario: `HF_INPATIENT`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260922:813:HF_INPATIENT`

## VAL-214

- Scenario: `AF_ANTICOAGULATION`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260922:814:AF_ANTICOAGULATION`

## VAL-215

- Scenario: `AF_ANTICOAGULATION`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260922:815:AF_ANTICOAGULATION`

## VAL-216

- Scenario: `AF_ANTICOAGULATION`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260922:816:AF_ANTICOAGULATION`

## VAL-217

- Scenario: `HTN_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260922:817:HTN_INPATIENT`

## VAL-218

- Scenario: `HTN_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260922:818:HTN_INPATIENT`

## VAL-219

- Scenario: `HTN_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260922:819:HTN_INPATIENT`

## VAL-220

- Scenario: `HTN_INPATIENT`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260922:820:HTN_INPATIENT`

## VAL-221

- Scenario: `T2DM_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260922:821:T2DM_INPATIENT`

## VAL-222

- Scenario: `T2DM_INPATIENT`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260922:822:T2DM_INPATIENT`

## VAL-223

- Scenario: `T2DM_INPATIENT`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260922:823:T2DM_INPATIENT`

## VAL-224

- Scenario: `CAP_INPATIENT`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_frequency_mismatch`
- Rationale: The discharge frequency differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260922:824:CAP_INPATIENT`

