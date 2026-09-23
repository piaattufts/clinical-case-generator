# Investigator answer key

machine-validated synthetic resident-review cases pending clinician validation

Batch: `CLINIPROOF_SEEDCASES_V2`

## VAL-601

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_COLLATERAL_VERIFIED`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1301:MEDREC_UNCERTAIN_HISTORY:MEDREC_COLLATERAL_VERIFIED`

## VAL-602

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_VERIFIED_STATIN_CONTINUED`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260924:1302:MEDREC_UNCERTAIN_HISTORY:MEDREC_VERIFIED_STATIN_CONTINUED`

## VAL-603

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_HOME_SERVICES_SUPPLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260924:1303:MEDREC_UNCERTAIN_HISTORY:MEDREC_HOME_SERVICES_SUPPLY`

## VAL-604

- Scenario: `MEDREC_UNCERTAIN_HISTORY`
- Clinical profile: `MEDREC_PENDING_COGNITIVE_THERAPY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `MEDREC_UNCERTAIN_HISTORY`
- Seed source file: `Bad_Med_Rec_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1304:MEDREC_UNCERTAIN_HISTORY:MEDREC_PENDING_COGNITIVE_THERAPY`

## VAL-605

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_UNCOMPLICATED_DIURESIS`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1305:HF_DECOMPENSATION:HF_DECOMP_UNCOMPLICATED_DIURESIS`

## VAL-606

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_AKI_HOLDS`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260924:1306:HF_DECOMPENSATION:HF_DECOMP_AKI_HOLDS`

## VAL-607

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_POTASSIUM_REPLACEMENT`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260924:1307:HF_DECOMPENSATION:HF_DECOMP_POTASSIUM_REPLACEMENT`

## VAL-608

- Scenario: `HF_DECOMPENSATION`
- Clinical profile: `HF_DECOMP_DIURETIC_ADJUSTMENT`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `HF_DECOMPENSATION`
- Seed source file: `Heart_Failure_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_therapeutic_substitution`
- Rationale: A different medication in the same therapeutic class was substituted at discharge without a documented clinical or formulary explanation.
- Seed: `20260924:1308:HF_DECOMPENSATION:HF_DECOMP_DIURETIC_ADJUSTMENT`

## VAL-609

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_STABLE_COMPLETION_PLAN`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1309:OPAT_ENDOCARDITIS:OPAT_STABLE_COMPLETION_PLAN`

## VAL-610

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_OMITTED_PARENTERAL_THERAPY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260924:1310:OPAT_ENDOCARDITIS:OPAT_OMITTED_PARENTERAL_THERAPY`

## VAL-611

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_SHORT_ANTIBIOTIC_SUPPLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260924:1311:OPAT_ENDOCARDITIS:OPAT_SHORT_ANTIBIOTIC_SUPPLY`

## VAL-612

- Scenario: `OPAT_ENDOCARDITIS`
- Clinical profile: `OPAT_MISSING_ID_FOLLOWUP`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `OPAT_ENDOCARDITIS`
- Seed source file: `OPAT_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1312:OPAT_ENDOCARDITIS:OPAT_MISSING_ID_FOLLOWUP`

## VAL-613

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_CMV_IMPROVING`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: NO INTENTIONAL ERROR
- NO INTENTIONAL ERROR
- Seed: `20260924:1313:TRANSPLANT_CMV:TRANSPLANT_CMV_IMPROVING`

## VAL-614

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_MMF_HOLD_RESTART`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260924:1314:TRANSPLANT_CMV:TRANSPLANT_MMF_HOLD_RESTART`

## VAL-615

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_TACROLIMUS_ADJUSTMENT`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_dose_mismatch`
- Rationale: The discharge dose differs from the intended medication plan without a documented clinical rationale.
- Seed: `20260924:1315:TRANSPLANT_CMV:TRANSPLANT_TACROLIMUS_ADJUSTMENT`

## VAL-616

- Scenario: `TRANSPLANT_CMV`
- Clinical profile: `TRANSPLANT_PENDING_ANTIVIRAL_DURATION`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `TRANSPLANT_CMV`
- Seed source file: `Post_transplant_case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1316:TRANSPLANT_CMV:TRANSPLANT_PENDING_ANTIVIRAL_DURATION`

## VAL-617

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_WARFARIN_MONITORING`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_monitoring_not_arranged`
- Rationale: A medication requiring outpatient laboratory or physiological monitoring was discharged without that monitoring being arranged.
- Seed: `20260924:1317:POSTOP_ANTICOAGULATION:POSTOP_WARFARIN_MONITORING`

## VAL-618

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_OMITTED_ANTICOAGULATION`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_omission`
- Rationale: A medication indicated at discharge was omitted from the discharge medication list.
- Seed: `20260924:1318:POSTOP_ANTICOAGULATION:POSTOP_OMITTED_ANTICOAGULATION`

## VAL-619

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_ANTICOAG_SUPPLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_insufficient_supply`
- Rationale: The prescribed quantity or days' supply is insufficient to cover the patient until the planned follow-up.
- Seed: `20260924:1319:POSTOP_ANTICOAGULATION:POSTOP_ANTICOAG_SUPPLY`

## VAL-620

- Scenario: `POSTOP_ANTICOAGULATION`
- Clinical profile: `POSTOP_BRIDGE_HOSPITAL_ONLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `POSTOP_ANTICOAGULATION`
- Seed source file: `Post-Op_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260924:1320:POSTOP_ANTICOAGULATION:POSTOP_BRIDGE_HOSPITAL_ONLY`

## VAL-621

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_AC_HELD_RESTART`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_held_med_no_restart_plan`
- Rationale: A home medication legitimately held during hospitalization has no documented resumption criterion or timing at discharge.
- Seed: `20260924:1321:GI_BLEED_ACUTE_CHANGE:GI_BLEED_AC_HELD_RESTART`

## VAL-622

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_PPI_HOSPITAL_ONLY`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_hospital_only_continued`
- Rationale: A medication started for an inpatient-only indication was erroneously continued at discharge despite no ongoing outpatient indication.
- Seed: `20260924:1322:GI_BLEED_ACUTE_CHANGE:GI_BLEED_PPI_HOSPITAL_ONLY`

## VAL-623

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_PENDING_AC_DECISION`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_2`
- Error category: `f2_pending_decision_followup_missing`
- Rationale: Treatment continues after discharge while a pending therapeutic decision remains unresolved and no follow-up visit is arranged to resolve it.
- Seed: `20260924:1323:GI_BLEED_ACUTE_CHANGE:GI_BLEED_PENDING_AC_DECISION`

## VAL-624

- Scenario: `GI_BLEED_ACUTE_CHANGE`
- Clinical profile: `GI_BLEED_ASPIRIN_NOT_RESTARTED`
- Generation strategy: `resident_seed_guided`
- Seed archetype: `GI_BLEED_ACUTE_CHANGE`
- Seed source file: `Sepsis_AMA_Case.docx`
- Status: error_bearing
- Error family: `family_1`
- Error category: `f1_commission`
- Rationale: A medication was prescribed at discharge without a clinical indication or intended discharge role.
- Seed: `20260924:1324:GI_BLEED_ACUTE_CHANGE:GI_BLEED_ASPIRIN_NOT_RESTARTED`

