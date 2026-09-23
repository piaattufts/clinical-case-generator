# Investigator answer key

machine-validated synthetic resident-review cases pending clinician validation

Batch: `CLINIPROOF_SEEDCASES_V1`

## VAL-401

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_COLLATERAL_VERIFIED`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1101:MEDREC_UNCERTAIN_HISTORY:MEDREC_COLLATERAL_VERIFIED`

## VAL-402

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_VERIFIED_STATIN_CONTINUED`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260924:1102:MEDREC_UNCERTAIN_HISTORY:MEDREC_VERIFIED_STATIN_CONTINUED`

## VAL-403

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_HOME_SERVICES_SUPPLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260924:1103:MEDREC_UNCERTAIN_HISTORY:MEDREC_HOME_SERVICES_SUPPLY`

## VAL-404

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_PENDING_COGNITIVE_THERAPY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1104:MEDREC_UNCERTAIN_HISTORY:MEDREC_PENDING_COGNITIVE_THERAPY`

## VAL-405

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_UNCOMPLICATED_DIURESIS`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1105:HF_DECOMPENSATION:HF_DECOMP_UNCOMPLICATED_DIURESIS`

## VAL-406

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_AKI_HOLDS`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260924:1106:HF_DECOMPENSATION:HF_DECOMP_AKI_HOLDS`

## VAL-407

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_POTASSIUM_REPLACEMENT`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260924:1107:HF_DECOMPENSATION:HF_DECOMP_POTASSIUM_REPLACEMENT`

## VAL-408

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_DIURETIC_ADJUSTMENT`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_therapeutic_substitution`
- Rationale: A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.
- Seed: `20260924:1108:HF_DECOMPENSATION:HF_DECOMP_DIURETIC_ADJUSTMENT`

## VAL-409

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_STABLE_COMPLETION_PLAN`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1109:OPAT_ENDOCARDITIS:OPAT_STABLE_COMPLETION_PLAN`

## VAL-410

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_OMITTED_PARENTERAL_THERAPY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260924:1110:OPAT_ENDOCARDITIS:OPAT_OMITTED_PARENTERAL_THERAPY`

## VAL-411

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_SHORT_ANTIBIOTIC_SUPPLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260924:1111:OPAT_ENDOCARDITIS:OPAT_SHORT_ANTIBIOTIC_SUPPLY`

## VAL-412

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_MISSING_ID_FOLLOWUP`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1112:OPAT_ENDOCARDITIS:OPAT_MISSING_ID_FOLLOWUP`

## VAL-413

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_CMV_IMPROVING`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1113:TRANSPLANT_CMV:TRANSPLANT_CMV_IMPROVING`

## VAL-414

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_MMF_HOLD_RESTART`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260924:1114:TRANSPLANT_CMV:TRANSPLANT_MMF_HOLD_RESTART`

## VAL-415

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_TACROLIMUS_ADJUSTMENT`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260924:1115:TRANSPLANT_CMV:TRANSPLANT_TACROLIMUS_ADJUSTMENT`

## VAL-416

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_PENDING_ANTIVIRAL_DURATION`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1116:TRANSPLANT_CMV:TRANSPLANT_PENDING_ANTIVIRAL_DURATION`

## VAL-417

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_WARFARIN_MONITORING`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260924:1117:POSTOP_ANTICOAGULATION:POSTOP_WARFARIN_MONITORING`

## VAL-418

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_OMITTED_ANTICOAGULATION`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260924:1118:POSTOP_ANTICOAGULATION:POSTOP_OMITTED_ANTICOAGULATION`

## VAL-419

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_ANTICOAG_SUPPLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260924:1119:POSTOP_ANTICOAGULATION:POSTOP_ANTICOAG_SUPPLY`

## VAL-420

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_BRIDGE_HOSPITAL_ONLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260924:1120:POSTOP_ANTICOAGULATION:POSTOP_BRIDGE_HOSPITAL_ONLY`

## VAL-421

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_AC_HELD_RESTART`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260924:1121:GI_BLEED_ACUTE_CHANGE:GI_BLEED_AC_HELD_RESTART`

## VAL-422

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_PPI_HOSPITAL_ONLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260924:1122:GI_BLEED_ACUTE_CHANGE:GI_BLEED_PPI_HOSPITAL_ONLY`

## VAL-423

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_PENDING_AC_DECISION`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1123:GI_BLEED_ACUTE_CHANGE:GI_BLEED_PENDING_AC_DECISION`

## VAL-424

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_ASPIRIN_NOT_RESTARTED`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260924:1124:GI_BLEED_ACUTE_CHANGE:GI_BLEED_ASPIRIN_NOT_RESTARTED`

