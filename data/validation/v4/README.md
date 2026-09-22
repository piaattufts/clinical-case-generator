# RESIDENT_VALIDATION_V4

Fourth independent freeze of 24 machine-validated synthetic resident-review cases pending clinician validation. Same five inpatient families and error mix as V1. New master seed, sequences, and VAL IDs. These records are **not clinically validated** until residents complete review.

This freeze stores the historical injector names (`omission`, `dose_mismatch`, `frequency_mismatch`, `incorrect_continuation`). They map to `f1_omission`, `f1_dose_mismatch`, `f1_frequency_mismatch`, and `f1_commission`. They are **not rewritten**. Canonical-ID cases are [`../cliniproof_v1/`](../cliniproof_v1/).

The committed JSON in this folder is the **study source of truth** for this batch. Shared pipeline, official sources, planted-error mechanics, and limitations: [`../README.md`](../README.md).

---

## Dataset identity (this freeze)

| Field | Value |
| --- | --- |
| Batch code | `RESIDENT_VALIDATION_V4` |
| Generator | `clinical-case-generator` `0.1.0` |
| Master seed | `20260925` |
| Case seed formula | `{master_seed}:{sequence}:{scenario}` |
| Internal case IDs | `SYN-000401`–`SYN-000424` |
| Frozen public IDs | `VAL-073`–`VAL-096` |
| Frozen at | `2026-09-22T14:19:32.678881+00:00` |
| Exported at | `2026-09-22T14:19:46.240896+00:00` |
| Cases | 24 frozen, 0 rejected |
| Clean controls | 5 (`VAL-077`, `VAL-082`, `VAL-087`, `VAL-092`, `VAL-096`) |
| Error-bearing | 19 (exactly one planted medication-reconciliation error each) |
| OpenAI | **not used** (`freeze-validation-batch` hardcodes `use_openai=False`) |
| Dataset status string | `machine-validated synthetic resident-review cases pending clinician validation` |
| Leak audit | `audit_passed: true` |

Sequences **401–424** keep this freeze away from smoke cases `SYN-000001`–`SYN-000003` and from the other resident-validation batches.

Official source versions recorded on this freeze:

| Source | Version | Rows imported | Last successful sync |
| --- | --- | --- | --- |
| RXNORM | `08-Sep-2026` | 16 | `2026-09-22T14:18:57.947304+00:00` |
| LOINC | `2.83` | 7 | `2026-09-22T14:19:12.743784+00:00` |
| UCUM | `2.2` | 16 | `2026-09-22T14:18:58.828843+00:00` |
| ICD10CM | none supplied by API | 5 | `2026-09-22T14:18:58.224692+00:00` |
| DAILYMED | none supplied by API | 10 | `2026-09-22T14:19:17.058217+00:00` |

---

## Files in this directory

| File | Audience | Contents |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Investigators / operators | Master seed, VAL IDs, scenarios, inject flags, error categories, sequences |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Residents | Blinded dashboard-shaped cases. **Give this file to reviewers.** |
| [`investigator_answer_key.json`](investigator_answer_key.json) | Investigators only | Seeds, SYN IDs, error category, affected RXCUI, clean expected state |
| [`investigator_answer_key.md`](investigator_answer_key.md) | Investigators only | Human-readable answer key |
| [`validation_manifest.json`](validation_manifest.json) | Investigators | Per-VAL freeze metadata, source versions, enabled rules |
| [`coverage_report.md`](coverage_report.md) | Investigators | Scenario, error, terminology, and rule counts |
| [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md) | Investigators | Resolved diagnoses, meds, labs, and allowed error types per family |
| [`resident_review_worksheet.csv`](resident_review_worksheet.csv) | Residents / study staff | Empty capture rows; no fabricated ratings |
| [`resident_review_schema.json`](resident_review_schema.json) | Study staff | Field definitions for the worksheet |

Do **not** give residents this README, the investigator key, the manifest, `batch_plan.json`, or the coverage files.

```bash
clinical-case-generator freeze-validation-batch --plan data/validation/v4/batch_plan.json
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V4 --output-dir data/validation/v4
```

Do not omit `--plan` / `--output-dir`. The CLI defaults would reuse or overwrite V1.

---

## Assignment index

| VAL | SYN | Scenario | Seed | Age / sex | Status | Error | Affected medication (RXCUI) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-073 | SYN-000401 | HF_INPATIENT | `20260925:401:HF_INPATIENT` | 71 F | error | omission | furosemide 4 MG/ML Oral Solution (`104220`) |
| VAL-074 | SYN-000402 | HF_INPATIENT | `20260925:402:HF_INPATIENT` | 57 M | error | dose_mismatch | spironolactone 1 MG/ML Oral Suspension (`104230`) — discharge **2 tablet** vs home `1 tablet` |
| VAL-075 | SYN-000403 | HF_INPATIENT | `20260925:403:HF_INPATIENT` | 77 F | error | frequency_mismatch | warfarin sodium 1 MG Oral Tablet (`855288`) — discharge **twice daily** |
| VAL-076 | SYN-000404 | HF_INPATIENT | `20260925:404:HF_INPATIENT` | 70 M | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-077 | SYN-000405 | HF_INPATIENT | `20260925:405:HF_INPATIENT` | 75 F | **clean control** | — | — |
| VAL-078 | SYN-000406 | AF_ANTICOAGULATION | `20260925:406:AF_ANTICOAGULATION` | 88 F | error | omission | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) |
| VAL-079 | SYN-000407 | AF_ANTICOAGULATION | `20260925:407:AF_ANTICOAGULATION` | 80 M | error | dose_mismatch | apixaban 2.5 MG Oral Tablet (`1364435`) — discharge **1.5 MG** vs home `2.5 MG` |
| VAL-080 | SYN-000408 | AF_ANTICOAGULATION | `20260925:408:AF_ANTICOAGULATION` | 76 M | error | frequency_mismatch | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) — discharge **twice daily** |
| VAL-081 | SYN-000409 | AF_ANTICOAGULATION | `20260925:409:AF_ANTICOAGULATION` | 70 F | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-082 | SYN-000410 | AF_ANTICOAGULATION | `20260925:410:AF_ANTICOAGULATION` | 60 F | **clean control** | — | — |
| VAL-083 | SYN-000411 | HTN_INPATIENT | `20260925:411:HTN_INPATIENT` | 61 F | error | omission | hydrochlorothiazide 50 MG Oral Tablet (`197770`) |
| VAL-084 | SYN-000412 | HTN_INPATIENT | `20260925:412:HTN_INPATIENT` | 68 M | error | dose_mismatch | lisinopril 1 MG/ML Oral Solution (`1806884`) — discharge **2 MG/ML** vs home `1 MG/ML` |
| VAL-085 | SYN-000413 | HTN_INPATIENT | `20260925:413:HTN_INPATIENT` | 61 F | error | frequency_mismatch | hydrochlorothiazide 50 MG Oral Tablet (`197770`) — discharge **twice daily** |
| VAL-086 | SYN-000414 | HTN_INPATIENT | `20260925:414:HTN_INPATIENT` | 73 M | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-087 | SYN-000415 | HTN_INPATIENT | `20260925:415:HTN_INPATIENT` | 70 F | **clean control** | — | — |
| VAL-088 | SYN-000416 | T2DM_INPATIENT | `20260925:416:T2DM_INPATIENT` | 50 M | error | omission | atorvastatin 80 MG Oral Tablet (`259255`) |
| VAL-089 | SYN-000417 | T2DM_INPATIENT | `20260925:417:T2DM_INPATIENT` | 79 M | error | dose_mismatch | atorvastatin 80 MG Oral Tablet (`259255`) — discharge **20 MG** vs home `80 MG` |
| VAL-090 | SYN-000418 | T2DM_INPATIENT | `20260925:418:T2DM_INPATIENT` | 66 M | error | frequency_mismatch | Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet (`1807888`) — discharge **twice daily** |
| VAL-091 | SYN-000419 | T2DM_INPATIENT | `20260925:419:T2DM_INPATIENT` | 77 F | error | omission | lisinopril 1 MG/ML Oral Solution (`1806884`) |
| VAL-092 | SYN-000420 | T2DM_INPATIENT | `20260925:420:T2DM_INPATIENT` | 45 M | **clean control** | — | — |
| VAL-093 | SYN-000421 | CAP_INPATIENT | `20260925:421:CAP_INPATIENT` | 64 M | error | omission | pantoprazole 20 MG Delayed Release Oral Tablet (`251872`) |
| VAL-094 | SYN-000422 | CAP_INPATIENT | `20260925:422:CAP_INPATIENT` | 57 M | error | dose_mismatch | pantoprazole 20 MG Delayed Release Oral Tablet (`251872`) — discharge **10 MG** vs home `20 MG` |
| VAL-095 | SYN-000423 | CAP_INPATIENT | `20260925:423:CAP_INPATIENT` | 80 F | error | frequency_mismatch | azithromycin 250 MG Oral Capsule (`141962`) — discharge **twice daily** |
| VAL-096 | SYN-000424 | CAP_INPATIENT | `20260925:424:CAP_INPATIENT` | 67 M | **clean control** | — | — |

Clean expected discharge lists **never** include ibuprofen. Clean controls still list ibuprofen on home and inpatient with an explicit hold when the scenario has a stop medication. Error-bearing `incorrect_continuation` cases are the only ones with ibuprofen on discharge.

---

## Per-case catalog

Each block is the frozen case as exported. Lab/vital numbers are synthetic. Continue vs stop is the **correct** reconciliation plan (investigator view). Discharge-list mutations are listed under “Planted error”.

### `HF_INPATIENT` — I50.20, Unspecified systolic (congestive) heart failure

Symptoms (as stored on this freeze): Dyspnea, Anasarca, Orthopnea. Specialty: cardiology.
Correct continue meds on the clean plan: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet.
Held stop med: ibuprofen 0.05 MG/MG Topical Gel.
Labs: Cr `14682-9`, K `2823-3`, BNP `30934-4`, INR `38875-1`.

#### VAL-073 (`SYN-000401`) — omission

- Seed `20260925:401:HF_INPATIENT`. 71-year-old Female, 64 kg. Vitals: BP 135/77, HR 77, RR 21, SpO2 93.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.1 umol/L, K 4.1 mmol/L, BNP 219 pg/mL, INR 2.4.
- Planted error: furosemide 4 MG/ML Oral Solution (`104220`) omitted from discharge (present home + inpatient).

#### VAL-074 (`SYN-000402`) — dose_mismatch

- Seed `20260925:402:HF_INPATIENT`. 57-year-old Male, 83 kg. Vitals: BP 148/77, HR 72, RR 22, SpO2 97.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 0.8 umol/L, K 4.7 mmol/L, BNP 606 pg/mL, INR 2.2.
- Planted error: discharge spironolactone 1 MG/ML Oral Suspension (`104230`) dose **2 tablet** (home/inpatient remain `1 tablet`).

#### VAL-075 (`SYN-000403`) — frequency_mismatch

- Seed `20260925:403:HF_INPATIENT`. 77-year-old Female, 74 kg. Vitals: BP 150/79, HR 109, RR 22, SpO2 95.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 1.6 umol/L, K 3.6 mmol/L, BNP 574 pg/mL, INR 2.9.
- Planted error: discharge warfarin sodium 1 MG Oral Tablet (`855288`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-076 (`SYN-000404`) — incorrect_continuation

- Seed `20260925:404:HF_INPATIENT`. 70-year-old Male, 62 kg. Vitals: BP 122/82, HR 73, RR 23, SpO2 97.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.1 umol/L, K 3.6 mmol/L, BNP 570 pg/mL, INR 3.1.
- Planted error: ibuprofen 0.05 MG/MG Topical Gel (`141997`) **continued on discharge** (correct plan is stop).

#### VAL-077 (`SYN-000405`) — clean control

- Seed `20260925:405:HF_INPATIENT`. 75-year-old Female, 96 kg. Vitals: BP 153/87, HR 73, RR 17, SpO2 93.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 1.2 umol/L, K 3.5 mmol/L, BNP 660 pg/mL, INR 2.6.
- Discharge list: atorvastatin 80 MG Oral Tablet, furosemide 4 MG/ML Oral Solution, lisinopril 1 MG/ML Oral Solution, metoprolol tartrate 37.5 MG Oral Tablet, spironolactone 1 MG/ML Oral Suspension, warfarin sodium 1 MG Oral Tablet. No planted error.

### `AF_ANTICOAGULATION` — I48.0, Paroxysmal atrial fibrillation

Symptoms (as stored on this freeze): Dyspnea, Chronic fatigue syndrome. Specialty: cardiology.
Shared continue meds: metoprolol, atorvastatin, plus exactly one of warfarin or apixaban (mutex pick from the seed).
Held stop med: ibuprofen 0.05 MG/MG Topical Gel.
Labs: Cr `14682-9`, INR `38875-1`.

#### VAL-078 (`SYN-000406`) — omission

- Seed `20260925:406:AF_ANTICOAGULATION`. 88-year-old Female, 76 kg. Vitals: BP 152/94, HR 103, RR 24, SpO2 91.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 0.8 umol/L, INR 2.
- Planted error: metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) omitted from discharge (present home + inpatient).

#### VAL-079 (`SYN-000407`) — dose_mismatch

- Seed `20260925:407:AF_ANTICOAGULATION`. 80-year-old Male, 75 kg. Vitals: BP 122/71, HR 110, RR 17, SpO2 92.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.3 umol/L, INR 2.2.
- Planted error: discharge apixaban 2.5 MG Oral Tablet (`1364435`) dose **1.5 MG** (home/inpatient remain `2.5 MG`).

#### VAL-080 (`SYN-000408`) — frequency_mismatch

- Seed `20260925:408:AF_ANTICOAGULATION`. 76-year-old Male, 65 kg. Vitals: BP 142/91, HR 80, RR 24, SpO2 98.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 1.2 umol/L, INR 2.1.
- Planted error: discharge metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-081 (`SYN-000409`) — incorrect_continuation

- Seed `20260925:409:AF_ANTICOAGULATION`. 70-year-old Female, 85 kg. Vitals: BP 139/85, HR 105, RR 20, SpO2 97.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.2 umol/L, INR 1.8.
- Planted error: ibuprofen 0.05 MG/MG Topical Gel (`141997`) **continued on discharge** (correct plan is stop).

#### VAL-082 (`SYN-000410`) — clean control

- Seed `20260925:410:AF_ANTICOAGULATION`. 60-year-old Female, 64 kg. Vitals: BP 135/79, HR 97, RR 21, SpO2 94.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 1.1 umol/L, INR 3.2.
- Discharge list: atorvastatin 80 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, warfarin sodium 1 MG Oral Tablet. No planted error.

### `HTN_INPATIENT` — I10, Essential (primary) hypertension

Symptoms (as stored on this freeze): Chronic fatigue syndrome. Specialty: general medicine.
Correct continue meds on the clean plan: lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet.
Held stop med: ibuprofen 0.05 MG/MG Topical Gel.
Labs: Cr `14682-9`, K `2823-3`, Na `2951-2`.

#### VAL-083 (`SYN-000411`) — omission

- Seed `20260925:411:HTN_INPATIENT`. 61-year-old Female, 68 kg. Vitals: BP 137/96, HR 91, RR 23, SpO2 91.
- Labs: Cr 1.2 umol/L, K 4.1 mmol/L, Na 138 mmol/L.
- Planted error: hydrochlorothiazide 50 MG Oral Tablet (`197770`) omitted from discharge (present home + inpatient).

#### VAL-084 (`SYN-000412`) — dose_mismatch

- Seed `20260925:412:HTN_INPATIENT`. 68-year-old Male, 68 kg. Vitals: BP 127/95, HR 72, RR 18, SpO2 94.
- Labs: Cr 1 umol/L, K 4.2 mmol/L, Na 138 mmol/L.
- Planted error: discharge lisinopril 1 MG/ML Oral Solution (`1806884`) dose **2 MG/ML** (home/inpatient remain `1 MG/ML`).

#### VAL-085 (`SYN-000413`) — frequency_mismatch

- Seed `20260925:413:HTN_INPATIENT`. 61-year-old Female, 92 kg. Vitals: BP 131/82, HR 88, RR 16, SpO2 98.
- Labs: Cr 1.1 umol/L, K 3.7 mmol/L, Na 134 mmol/L.
- Planted error: discharge hydrochlorothiazide 50 MG Oral Tablet (`197770`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-086 (`SYN-000414`) — incorrect_continuation

- Seed `20260925:414:HTN_INPATIENT`. 73-year-old Male, 88 kg. Vitals: BP 130/87, HR 79, RR 18, SpO2 97.
- Labs: Cr 0.9 umol/L, K 4.7 mmol/L, Na 135 mmol/L.
- Planted error: ibuprofen 0.05 MG/MG Topical Gel (`141997`) **continued on discharge** (correct plan is stop).

#### VAL-087 (`SYN-000415`) — clean control

- Seed `20260925:415:HTN_INPATIENT`. 70-year-old Female, 65 kg. Vitals: BP 121/74, HR 99, RR 21, SpO2 91.
- Labs: Cr 1 umol/L, K 4 mmol/L, Na 138 mmol/L.
- Discharge list: amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution. No planted error.

### `T2DM_INPATIENT` — E11.8, Type 2 diabetes mellitus with unspecified complications

Symptoms (as stored on this freeze): Polyuria, Chronic fatigue syndrome. Specialty: general medicine.
Correct continue meds on the clean plan: lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.
Labs: Cr `14682-9`, glucose `14749-6`, Hb `55782-7`.

#### VAL-088 (`SYN-000416`) — omission

- Seed `20260925:416:T2DM_INPATIENT`. 50-year-old Male, 61 kg. Vitals: BP 146/83, HR 90, RR 18, SpO2 94.
- Labs: Cr 1.3 umol/L, glucose 156 mmol/L, Hb 10.5 g/dL.
- Planted error: atorvastatin 80 MG Oral Tablet (`259255`) omitted from discharge (present home + inpatient).

#### VAL-089 (`SYN-000417`) — dose_mismatch

- Seed `20260925:417:T2DM_INPATIENT`. 79-year-old Male, 104 kg. Vitals: BP 149/80, HR 108, RR 16, SpO2 96.
- Labs: Cr 1.6 umol/L, glucose 174 mmol/L, Hb 11.3 g/dL.
- Planted error: discharge atorvastatin 80 MG Oral Tablet (`259255`) dose **20 MG** (home/inpatient remain `80 MG`).

#### VAL-090 (`SYN-000418`) — frequency_mismatch

- Seed `20260925:418:T2DM_INPATIENT`. 66-year-old Male, 109 kg. Vitals: BP 155/79, HR 80, RR 20, SpO2 94.
- Labs: Cr 1 umol/L, glucose 131 mmol/L, Hb 10.6 g/dL.
- Planted error: discharge Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet (`1807888`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-091 (`SYN-000419`) — omission

- Seed `20260925:419:T2DM_INPATIENT`. 77-year-old Female, 107 kg. Vitals: BP 145/88, HR 98, RR 16, SpO2 98.
- Labs: Cr 1.6 umol/L, glucose 140 mmol/L, Hb 13.3 g/dL.
- Planted error: lisinopril 1 MG/ML Oral Solution (`1806884`) omitted from discharge (present home + inpatient).

#### VAL-092 (`SYN-000420`) — clean control

- Seed `20260925:420:T2DM_INPATIENT`. 45-year-old Male, 104 kg. Vitals: BP 146/74, HR 102, RR 20, SpO2 96.
- Labs: Cr 0.8 umol/L, glucose 143 mmol/L, Hb 12.2 g/dL.
- Discharge list: atorvastatin 80 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet. No planted error.

### `CAP_INPATIENT` — J18.1, Lobar pneumonia, unspecified organism

Symptoms (as stored on this freeze): Cough, Dyspnea, Wheezing. Specialty: pulmonology.
Correct continue meds on the clean plan: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet.
Labs: Cr `14682-9`, Na `2951-2`, Hb `55782-7`.

#### VAL-093 (`SYN-000421`) — omission

- Seed `20260925:421:CAP_INPATIENT`. 64-year-old Male, 91 kg. Vitals: BP 155/82, HR 80, RR 23, SpO2 91.
- Labs: Cr 1.1 umol/L, Na 136 mmol/L, Hb 14.2 g/dL.
- Planted error: pantoprazole 20 MG Delayed Release Oral Tablet (`251872`) omitted from discharge (present home + inpatient).

#### VAL-094 (`SYN-000422`) — dose_mismatch

- Seed `20260925:422:CAP_INPATIENT`. 57-year-old Male, 71 kg. Vitals: BP 130/84, HR 76, RR 21, SpO2 93.
- Labs: Cr 1.6 umol/L, Na 143 mmol/L, Hb 13.5 g/dL.
- Planted error: discharge pantoprazole 20 MG Delayed Release Oral Tablet (`251872`) dose **10 MG** (home/inpatient remain `20 MG`).

#### VAL-095 (`SYN-000423`) — frequency_mismatch

- Seed `20260925:423:CAP_INPATIENT`. 80-year-old Female, 78 kg. Vitals: BP 122/71, HR 110, RR 20, SpO2 94.
- Labs: Cr 1 umol/L, Na 140 mmol/L, Hb 11.5 g/dL.
- Planted error: discharge azithromycin 250 MG Oral Capsule (`141962`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-096 (`SYN-000424`) — clean control

- Seed `20260925:424:CAP_INPATIENT`. 67-year-old Male, 68 kg. Vitals: BP 148/76, HR 96, RR 18, SpO2 93.
- Labs: Cr 0.8 umol/L, Na 144 mmol/L, Hb 12.7 g/dL.
- Discharge list: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. No planted error.

---

## Repeatability

**Bit-identical study reprint:** use the committed files in this directory.

A second `freeze-validation-batch` on this plan reuses immutable VAL IDs and does not rewrite cases. Live API re-bootstrap is not guaranteed bit-identical. If ranking drifts, keep this freeze and start a new `batch_code` rather than editing JSON to substitute a “more typical” RXCUI or unit.

