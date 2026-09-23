# Generator field classification

This note classifies fields on the synthetic chart so diversity is introduced only where it is clinically meaningful. It is not a clinical guideline.

## 1. Clinically meaningful and should vary

These fields are part of the clean-case fingerprint when they are categorical (sets, patterns, coded concepts), not when they are exact numeric draws.

| Field | How it varies |
| --- | --- |
| Scenario family | Balanced across HF, AF, hypertension, diabetes, and pneumonia |
| Clinical profile | One named variant per case |
| Symptom set | Profile-specific subset of source-backed HPO/symptom rows |
| Symptom duration and course | Profile values such as one day, two days, several days, one week, with progressive, intermittent, persistent, acutely worsening, or improving after treatment |
| Medication subset | Required medications, optional includes, mutually exclusive anticoagulants, and profile-specific held or hospital-only drugs |
| Laboratory concept set | Profile subset; warfarin cases still include INR |
| Hospital-course pattern | Several concise inpatient patterns (diuresis, rate control, antibiotic course, glycemic stabilization, and others) |
| Follow-up service, item, and timing | Primary care, specialty, or anticoagulation clinic at clinically relevant intervals |
| Home health | Ordered only on selected discharge-support profiles |
| Vital-sign *pattern* | Congestive, hypertensive, tachycardic, febrile, or standard ranges |

Formulation selection prefers tablet or capsule RxNorm rows over oral solutions, suspensions, and gels when both exist locally. Identifiers are never invented.

## 2. Study-controlled and intentionally constant

| Field | Why it stays constant |
| --- | --- |
| Language preference | English. Language is not an assessment factor in this study. |
| Living situation | Lives at home. Housing variation is not an assessment factor. |
| Medication-reconciliation status on the clean case | `complete_clean`, pharmacist review true, patient able to participate. These describe the study’s clean starting state, not clinical diversity. |
| Narrative source on the freeze | Template wording (`use_openai=False`) so wording cannot become a hidden source of difference. |
| Care context | Inpatient for every currently implemented family. |
| Dataset status sentence | Machine-validated synthetic resident-review cases pending clinician validation. |

## 3. Irrelevant to this study and left empty rather than randomized

Empty or omitted on purpose: ethnicity, caregiver support, transportation, financial barriers, health literacy, advance directives, imaging, consults, devices, procedures, and therapy restrictions. Filling them with random values would look like diversity without supporting the medication-reconciliation task.

Exact age, sex, weight, vital numbers, and laboratory numbers are generated from the seed so cases remain reproducible. They are **excluded** from the uniqueness fingerprint. Changing only those values must not make two otherwise identical charts count as distinct.
