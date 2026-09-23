# Clean-case diversity report (`CLINIPROOF_BALANCED_V4`)

Case diversity is evaluated on the clean clinical case before error injection. Different seeds, demographics, numeric results, or planted error categories do not by themselves make two cases clinically unique.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

## Scenario distribution

| Family | Clinical profile | Count |
| --- | --- | ---: |
| `AF_ANTICOAGULATION` | `AF_HELD_NSAID` | 1 |
| `AF_ANTICOAGULATION` | `AF_POST_RATE_CONTROL` | 1 |
| `AF_ANTICOAGULATION` | `AF_RATE_CONTROL_APIXABAN` | 1 |
| `AF_ANTICOAGULATION` | `AF_WARFARIN_INR` | 1 |
| `AF_ANTICOAGULATION` | `AF_WITH_STATIN` | 1 |
| `CAP_INPATIENT` | `CAP_DYSPNEA_WHEEZE` | 1 |
| `CAP_INPATIENT` | `CAP_HOME_TRANSITION` | 1 |
| `CAP_INPATIENT` | `CAP_INPATIENT_ANTIBIOTIC` | 1 |
| `CAP_INPATIENT` | `CAP_TYPICAL_COUGH` | 1 |
| `HF_INPATIENT` | `HF_DISCHARGE_MONITORING` | 1 |
| `HF_INPATIENT` | `HF_MEDICATION_ADJUSTMENT` | 1 |
| `HF_INPATIENT` | `HF_POST_DIURESIS` | 1 |
| `HF_INPATIENT` | `HF_VOLUME_OVERLOAD` | 1 |
| `HF_INPATIENT` | `HF_WITH_WARFARIN` | 1 |
| `HTN_INPATIENT` | `HTN_ACE_CCB` | 1 |
| `HTN_INPATIENT` | `HTN_ACE_THIAZIDE` | 1 |
| `HTN_INPATIENT` | `HTN_CCB_STATIN` | 1 |
| `HTN_INPATIENT` | `HTN_NEW_DIAGNOSIS` | 1 |
| `HTN_INPATIENT` | `HTN_TRIPLE_THERAPY` | 1 |
| `T2DM_INPATIENT` | `T2DM_CONTROL` | 1 |
| `T2DM_INPATIENT` | `T2DM_GLYCEMIC_STABILIZATION` | 1 |
| `T2DM_INPATIENT` | `T2DM_METFORMIN_ACE` | 1 |
| `T2DM_INPATIENT` | `T2DM_METFORMIN_STATIN` | 1 |
| `T2DM_INPATIENT` | `T2DM_PENDING_DURATION` | 1 |

### Specialty and diagnosis

**Specialty**

- cardiology: 10 (41.7%)
- general medicine: 10 (41.7%)
- pulmonology: 4 (16.7%)

**Diagnosis**

- Acute systolic (congestive) heart failure|Essential (primary) hypertension|Mixed hyperlipidemia: 3 (12.5%)
- Acute systolic (congestive) heart failure|Essential (primary) hypertension|Paroxysmal atrial fibrillation: 1 (4.2%)
- Acute systolic (congestive) heart failure|Mixed hyperlipidemia|Paroxysmal atrial fibrillation: 1 (4.2%)
- Essential (primary) hypertension|Lobar pneumonia, unspecified organism: 1 (4.2%)
- Essential (primary) hypertension|Mixed hyperlipidemia: 5 (20.8%)
- Essential (primary) hypertension|Mixed hyperlipidemia|Paroxysmal atrial fibrillation: 4 (16.7%)
- Essential (primary) hypertension|Mixed hyperlipidemia|Type 2 diabetes mellitus with hyperglycemia: 3 (12.5%)
- Essential (primary) hypertension|Paroxysmal atrial fibrillation: 1 (4.2%)
- Gastro-esophageal reflux disease without esophagitis|Lobar pneumonia, unspecified organism: 2 (8.3%)
- Lobar pneumonia, unspecified organism: 1 (4.2%)
- Mixed hyperlipidemia|Type 2 diabetes mellitus with hyperglycemia: 2 (8.3%)

**Broad scenario family**

- AF_ANTICOAGULATION: 5 (20.8%)
- CAP_INPATIENT: 4 (16.7%)
- HF_INPATIENT: 5 (20.8%)
- HTN_INPATIENT: 5 (20.8%)
- T2DM_INPATIENT: 5 (20.8%)

## Clinical-feature diversity

- unique symptom sets: 14
- unique home-medication sets: 21
- unique hospital-course profiles: 24
- unique follow-up profiles: 24
- unique discharge dispositions: 2
- unique clinical profiles: 24

## Error distribution

- family_1: 11
- family_2: 9
- none: 4

- `f1_commission`: 1
- `f1_dose_mismatch`: 3
- `f1_frequency_mismatch`: 2
- `f1_omission`: 3
- `f1_route_mismatch`: 1
- `f1_therapeutic_substitution`: 1
- `f2_held_med_no_restart_plan`: 2
- `f2_hospital_only_continued`: 1
- `f2_inpatient_substitution_not_reverted`: 1
- `f2_insufficient_supply`: 2
- `f2_monitoring_not_arranged`: 2
- `f2_pending_decision_followup_missing`: 1
- `none`: 4

## Similarity audit

- closest pair: VAL-717 vs VAL-719
- similarity score: 0.74
- features shared: scenario, specialty, diagnosis, home_medications, inpatient_medications, disposition
- features different: clinical_profile, symptoms, hospital_course_pattern, followup

Pairs at or above the warning threshold:

- VAL-717 vs VAL-719: 0.74 (shared scenario, specialty, diagnosis, home_medications, inpatient_medications, disposition)

## Uniqueness conclusion

All clean cases passed the uniqueness requirement. Exact fingerprints are distinct and no pair met the near-duplicate rejection threshold.

- exact duplicate fingerprints: 0
- near-duplicate rejections: 0
- near-duplicate warnings: 1
