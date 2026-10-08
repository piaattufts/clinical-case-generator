# Diversity

Fingerprints exclude the medication-signature string so that a second patient with the same variant is treated as a structural duplicate.
Pairs at or above 0.85 similarity were rejected before final selection.

## MED_HISTORY_UNCERTAINTY
- G2-001 delirium_uti: precipitant=urinary_tract_infection; pathway=urinalysis_culture_then_diagnosis; disposition=home
- G2-002 delirium_dehydration: precipitant=poor_intake_and_dehydration; pathway=exam_chemistry_cognitive_baseline; disposition=home
- G2-003 hyponatremia_hctz: precipitant=thiazide_associated_hyponatremia; pathway=serial_sodium_medication_review; disposition=home
- G2-004 delirium_pneumonia: precipitant=lobar_pneumonia; pathway=radiograph_then_antibiotic; disposition=home
- similarity G2-001 vs G2-002: 0.45
- similarity G2-001 vs G2-003: 0.33
- similarity G2-001 vs G2-004: 0.23
- similarity G2-002 vs G2-003: 0.33
- similarity G2-002 vs G2-004: 0.23
- similarity G2-003 vs G2-004: 0.33

## HF_DECOMPENSATION
- G2-005 nonadherence_cost: precipitant=medication_nonadherence; pathway=radiograph_bnp_echo_adherence_history; disposition=home
- G2-006 dietary_sodium_missed_diuretic: precipitant=dietary_sodium_and_missed_diuretic; pathway=radiograph_bnp_echo_troponin; disposition=home
- G2-007 new_atrial_fibrillation: precipitant=new_atrial_fibrillation_with_rapid_rate; pathway=telemetry_radiograph_bnp_echo; disposition=home
- G2-008 hypertensive_surge: precipitant=missed_antihypertensive_and_pressure_surge; pathway=blood_pressure_radiograph_bnp_echo; disposition=home
- similarity G2-005 vs G2-006: 0.29
- similarity G2-005 vs G2-007: 0.50
- similarity G2-005 vs G2-008: 0.50
- similarity G2-006 vs G2-007: 0.29
- similarity G2-006 vs G2-008: 0.29
- similarity G2-007 vs G2-008: 0.50

## ENDOCARDITIS_OPAT
- G2-009 dental_mitral: precipitant=recent_dental_extraction; pathway=cultures_then_mitral_echo; disposition=home
- G2-010 no_source_aortic: precipitant=no_source_after_directed_evaluation; pathway=cultures_then_aortic_echo_negative_source_search; disposition=home
- G2-011 bicuspid_predisposition: precipitant=bicuspid_aortic_valve; pathway=cultures_and_echo_showing_bicuspid_valve; disposition=home
- G2-012 opat_home_infusion: precipitant=dental_cleaning; pathway=cultures_echo_home_infusion_assessment; disposition=home
- similarity G2-009 vs G2-010: 0.33
- similarity G2-009 vs G2-011: 0.45
- similarity G2-009 vs G2-012: 0.45
- similarity G2-010 vs G2-011: 0.33
- similarity G2-010 vs G2-012: 0.33
- similarity G2-011 vs G2-012: 0.45

## TRANSPLANT_CMV
- G2-013 cdiff_excluded: precipitant=diarrhea_after_negative_c_difficile; pathway=c_difficile_negative_then_pcr_and_biopsy; disposition=home
- G2-014 volume_loss: precipitant=high_volume_diarrhea; pathway=volume_exam_chemistry_pcr_biopsy; disposition=home
- G2-015 prophylaxis_breakthrough: precipitant=breakthrough_during_scenario_prophylaxis; pathway=pcr_on_prophylaxis_then_induction; disposition=home
- G2-016 transplant_clinic_followup: precipitant=subacute_diarrhea; pathway=pcr_biopsy_transplant_clinic_plan; disposition=home
- similarity G2-013 vs G2-014: 0.50
- similarity G2-013 vs G2-015: 0.12
- similarity G2-013 vs G2-016: 0.38
- similarity G2-014 vs G2-015: 0.12
- similarity G2-014 vs G2-016: 0.38
- similarity G2-015 vs G2-016: 0.20

## HIP_FRACTURE_ANTICOAGULATION
- G2-017 snf_after_orif: precipitant=fall_from_standing; pathway=xray_inr_orif_therapy_recommendation; disposition=skilled nursing facility
- G2-018 delayed_mobilization_snf: precipitant=fall_with_slow_mobilization; pathway=xray_orif_physical_therapy; disposition=skilled nursing facility
- G2-019 af_early_hemostasis: precipitant=fall_with_prompt_hemostasis; pathway=xray_orif_day2_hemostasis; disposition=home
- G2-020 inr_delay_home: precipitant=ground_level_fall; pathway=xray_inr_then_orif; disposition=home
- similarity G2-017 vs G2-018: 0.50
- similarity G2-017 vs G2-019: 0.38
- similarity G2-017 vs G2-020: 0.38
- similarity G2-018 vs G2-019: 0.38
- similarity G2-018 vs G2-020: 0.38
- similarity G2-019 vs G2-020: 0.50

## GI_BLEED_ANTICOAGULATION
- G2-021 duodenal_ulcer_restart: precipitant=melena; pathway=egd_duodenal_ulcer; disposition=home
- G2-022 esophagitis: precipitant=melena_and_reflux; pathway=egd_esophagitis; disposition=home
- G2-023 diverticular_hold: precipitant=hematochezia; pathway=colonoscopy_diverticular_bleed; disposition=home
- G2-024 defer_restart: precipitant=hematochezia; pathway=colonoscopy_then_unresolved_restart_timing; disposition=home
- similarity G2-021 vs G2-022: 0.38
- similarity G2-021 vs G2-023: 0.29
- similarity G2-021 vs G2-024: 0.29
- similarity G2-022 vs G2-023: 0.29
- similarity G2-022 vs G2-024: 0.29
- similarity G2-023 vs G2-024: 0.64
