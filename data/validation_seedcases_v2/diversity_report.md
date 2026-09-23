# Clean-case diversity report (`CLINIPROOF_SEEDCASES_V2`)

Case diversity is evaluated on the clean clinical case before error injection. Different seeds, demographics, numeric results, or planted error categories do not by themselves make two cases clinically unique.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

## Scenario distribution

| Family | Clinical profile | Count |
| --- | --- | ---: |
| `GI_BLEED_ACUTE_CHANGE` | `GI_BLEED_AC_HELD_RESTART` | 1 |
| `GI_BLEED_ACUTE_CHANGE` | `GI_BLEED_ASPIRIN_NOT_RESTARTED` | 1 |
| `GI_BLEED_ACUTE_CHANGE` | `GI_BLEED_PENDING_AC_DECISION` | 1 |
| `GI_BLEED_ACUTE_CHANGE` | `GI_BLEED_PPI_HOSPITAL_ONLY` | 1 |
| `HF_DECOMPENSATION` | `HF_DECOMP_AKI_HOLDS` | 1 |
| `HF_DECOMPENSATION` | `HF_DECOMP_DIURETIC_ADJUSTMENT` | 1 |
| `HF_DECOMPENSATION` | `HF_DECOMP_POTASSIUM_REPLACEMENT` | 1 |
| `HF_DECOMPENSATION` | `HF_DECOMP_UNCOMPLICATED_DIURESIS` | 1 |
| `MEDREC_UNCERTAIN_HISTORY` | `MEDREC_COLLATERAL_VERIFIED` | 1 |
| `MEDREC_UNCERTAIN_HISTORY` | `MEDREC_HOME_SERVICES_SUPPLY` | 1 |
| `MEDREC_UNCERTAIN_HISTORY` | `MEDREC_PENDING_COGNITIVE_THERAPY` | 1 |
| `MEDREC_UNCERTAIN_HISTORY` | `MEDREC_VERIFIED_STATIN_CONTINUED` | 1 |
| `OPAT_ENDOCARDITIS` | `OPAT_MISSING_ID_FOLLOWUP` | 1 |
| `OPAT_ENDOCARDITIS` | `OPAT_OMITTED_PARENTERAL_THERAPY` | 1 |
| `OPAT_ENDOCARDITIS` | `OPAT_SHORT_ANTIBIOTIC_SUPPLY` | 1 |
| `OPAT_ENDOCARDITIS` | `OPAT_STABLE_COMPLETION_PLAN` | 1 |
| `POSTOP_ANTICOAGULATION` | `POSTOP_ANTICOAG_SUPPLY` | 1 |
| `POSTOP_ANTICOAGULATION` | `POSTOP_BRIDGE_HOSPITAL_ONLY` | 1 |
| `POSTOP_ANTICOAGULATION` | `POSTOP_OMITTED_ANTICOAGULATION` | 1 |
| `POSTOP_ANTICOAGULATION` | `POSTOP_WARFARIN_MONITORING` | 1 |
| `TRANSPLANT_CMV` | `TRANSPLANT_CMV_IMPROVING` | 1 |
| `TRANSPLANT_CMV` | `TRANSPLANT_MMF_HOLD_RESTART` | 1 |
| `TRANSPLANT_CMV` | `TRANSPLANT_PENDING_ANTIVIRAL_DURATION` | 1 |
| `TRANSPLANT_CMV` | `TRANSPLANT_TACROLIMUS_ADJUSTMENT` | 1 |

### Specialty and diagnosis

**Specialty**

- cardiology: 4 (16.7%)
- general medicine: 8 (33.3%)
- infectious disease: 4 (16.7%)
- nephrology: 4 (16.7%)
- orthopedics: 4 (16.7%)

**Diagnosis**

- Acute and subacute infective endocarditis|Essential (primary) hypertension|Mixed hyperlipidemia: 1 (4.2%)
- Acute and subacute infective endocarditis|Essential (primary) hypertension|Type 2 diabetes mellitus without complications: 1 (4.2%)
- Acute and subacute infective endocarditis|Mixed hyperlipidemia: 1 (4.2%)
- Acute and subacute infective endocarditis|Mixed hyperlipidemia|Type 2 diabetes mellitus without complications: 1 (4.2%)
- Acute systolic (congestive) heart failure|Essential (primary) hypertension: 1 (4.2%)
- Acute systolic (congestive) heart failure|Essential (primary) hypertension|Mixed hyperlipidemia: 3 (12.5%)
- Delirium due to known physiological condition|Essential (primary) hypertension|Mixed hyperlipidemia: 1 (4.2%)
- Delirium due to known physiological condition|Essential (primary) hypertension|Mixed hyperlipidemia|Type 2 diabetes mellitus without complications: 2 (8.3%)
- Delirium due to known physiological condition|Mixed hyperlipidemia|Type 2 diabetes mellitus without complications: 1 (4.2%)
- Essential (primary) hypertension|Fracture of unspecified part of neck of right femur, initial encounter for closed fracture|Paroxysmal atrial fibrillation: 1 (4.2%)
- Essential (primary) hypertension|Fracture of unspecified part of neck of right femur, initial encounter for closed fracture|Paroxysmal atrial fibrillation|Type 2 diabetes mellitus without complications: 3 (12.5%)
- Essential (primary) hypertension|Gastrointestinal hemorrhage, unspecified|Mixed hyperlipidemia|Paroxysmal atrial fibrillation: 1 (4.2%)
- Essential (primary) hypertension|Gastrointestinal hemorrhage, unspecified|Mixed hyperlipidemia|Type 2 diabetes mellitus without complications: 2 (8.3%)
- Essential (primary) hypertension|Kidney transplant status|Mixed hyperlipidemia|Other cytomegaloviral diseases: 2 (8.3%)
- Essential (primary) hypertension|Kidney transplant status|Other cytomegaloviral diseases: 1 (4.2%)
- Gastrointestinal hemorrhage, unspecified|Mixed hyperlipidemia|Paroxysmal atrial fibrillation|Type 2 diabetes mellitus without complications: 1 (4.2%)
- Kidney transplant status|Mixed hyperlipidemia|Other cytomegaloviral diseases: 1 (4.2%)

**Broad scenario family**

- GI_BLEED_ACUTE_CHANGE: 4 (16.7%)
- HF_DECOMPENSATION: 4 (16.7%)
- MEDREC_UNCERTAIN_HISTORY: 4 (16.7%)
- OPAT_ENDOCARDITIS: 4 (16.7%)
- POSTOP_ANTICOAGULATION: 4 (16.7%)
- TRANSPLANT_CMV: 4 (16.7%)

## Clinical-feature diversity

- unique symptom sets: 12
- unique home-medication sets: 21
- unique hospital-course profiles: 24
- unique follow-up profiles: 23
- unique discharge dispositions: 4
- unique clinical profiles: 24

## Error distribution

- family_1: 7
- family_2: 13
- none: 4

- `f1_commission`: 1
- `f1_dose_mismatch`: 2
- `f1_omission`: 3
- `f1_therapeutic_substitution`: 1
- `f2_held_med_no_restart_plan`: 3
- `f2_hospital_only_continued`: 2
- `f2_insufficient_supply`: 3
- `f2_monitoring_not_arranged`: 1
- `f2_pending_decision_followup_missing`: 4
- `none`: 4

## Similarity audit

- closest pair: VAL-605 vs VAL-607
- similarity score: 0.79
- features shared: scenario, specialty, diagnosis, home_medications, inpatient_medications, lab_concepts, disposition
- features different: clinical_profile, symptoms, hospital_course_pattern, followup

Pairs at or above the warning threshold:

- VAL-601 vs VAL-603: 0.72 (shared scenario, specialty, diagnosis, symptoms, disposition)
- VAL-605 vs VAL-606: 0.71 (shared scenario, specialty, diagnosis, disposition)
- VAL-605 vs VAL-607: 0.79 (shared scenario, specialty, diagnosis, home_medications, inpatient_medications, lab_concepts, disposition)
- VAL-617 vs VAL-618: 0.75 (shared scenario, specialty, diagnosis, home_medications, inpatient_medications, disposition)
- VAL-617 vs VAL-620: 0.70 (shared scenario, specialty, diagnosis, home_medications, lab_concepts, disposition)
- VAL-618 vs VAL-620: 0.76 (shared scenario, specialty, diagnosis, symptoms, home_medications, disposition)
- VAL-622 vs VAL-624: 0.71 (shared scenario, specialty, diagnosis, symptoms, disposition)

## Uniqueness conclusion

All clean cases passed the uniqueness requirement. Exact fingerprints are distinct and no pair met the near-duplicate rejection threshold.

- exact duplicate fingerprints: 0
- near-duplicate rejections: 0
- near-duplicate warnings: 7
