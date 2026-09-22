# RESIDENT_VALIDATION_V3

Third independent freeze of 24 machine-validated synthetic resident-review cases pending clinician validation. Same five inpatient families and error mix as V1. New master seed, sequences, and VAL IDs. These records are **not clinically validated** until residents complete review.

This freeze stores the historical injector names (`omission`, `dose_mismatch`, `frequency_mismatch`, `incorrect_continuation`). They map to `f1_omission`, `f1_dose_mismatch`, `f1_frequency_mismatch`, and `f1_commission`. They are **not rewritten**. Canonical-ID cases are [`../cliniproof_v1/`](../cliniproof_v1/).

The committed JSON in this folder is the **study source of truth** for this batch. Shared pipeline, official sources, planted-error mechanics, and limitations: [`../README.md`](../README.md).

---

## Dataset identity (this freeze)

| Field | Value |
| --- | --- |
| Batch code | `RESIDENT_VALIDATION_V3` |
| Generator | `clinical-case-generator` `0.1.0` |
| Master seed | `20260924` |
| Case seed formula | `{master_seed}:{sequence}:{scenario}` |
| Internal case IDs | `SYN-000301`–`SYN-000324` |
| Frozen public IDs | `VAL-049`–`VAL-072` |
| Frozen at | `2026-09-22T14:19:30.181131+00:00` |
| Exported at | `2026-09-22T14:19:44.051450+00:00` |
| Cases | 24 frozen, 0 rejected |
| Clean controls | 5 (`VAL-053`, `VAL-058`, `VAL-063`, `VAL-068`, `VAL-072`) |
| Error-bearing | 19 (exactly one planted medication-reconciliation error each) |
| OpenAI | **not used** (`freeze-validation-batch` hardcodes `use_openai=False`) |
| Dataset status string | `machine-validated synthetic resident-review cases pending clinician validation` |
| Leak audit | `audit_passed: true` |

Sequences **301–324** keep this freeze away from smoke cases `SYN-000001`–`SYN-000003` and from the other resident-validation batches.

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
clinical-case-generator freeze-validation-batch --plan data/validation/v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V3 --output-dir data/validation/v3
```

Do not omit `--plan` / `--output-dir`. The CLI defaults would reuse or overwrite V1.

---

## Assignment index

| VAL | SYN | Scenario | Seed | Age / sex | Status | Error | Affected medication (RXCUI) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-049 | SYN-000301 | HF_INPATIENT | `20260924:301:HF_INPATIENT` | 72 F | error | omission | lisinopril 1 MG/ML Oral Solution (`1806884`) |
| VAL-050 | SYN-000302 | HF_INPATIENT | `20260924:302:HF_INPATIENT` | 55 M | error | dose_mismatch | lisinopril 1 MG/ML Oral Solution (`1806884`) — discharge **2 MG/ML** vs home `1 MG/ML` |
| VAL-051 | SYN-000303 | HF_INPATIENT | `20260924:303:HF_INPATIENT` | 72 M | error | frequency_mismatch | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) — discharge **twice daily** |
| VAL-052 | SYN-000304 | HF_INPATIENT | `20260924:304:HF_INPATIENT` | 61 M | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-053 | SYN-000305 | HF_INPATIENT | `20260924:305:HF_INPATIENT` | 59 F | **clean control** | — | — |
| VAL-054 | SYN-000306 | AF_ANTICOAGULATION | `20260924:306:AF_ANTICOAGULATION` | 84 F | error | omission | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) |
| VAL-055 | SYN-000307 | AF_ANTICOAGULATION | `20260924:307:AF_ANTICOAGULATION` | 69 M | error | dose_mismatch | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) — discharge **27.5 MG** vs home `37.5 MG` |
| VAL-056 | SYN-000308 | AF_ANTICOAGULATION | `20260924:308:AF_ANTICOAGULATION` | 67 M | error | frequency_mismatch | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) — discharge **twice daily** |
| VAL-057 | SYN-000309 | AF_ANTICOAGULATION | `20260924:309:AF_ANTICOAGULATION` | 63 M | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-058 | SYN-000310 | AF_ANTICOAGULATION | `20260924:310:AF_ANTICOAGULATION` | 82 M | **clean control** | — | — |
| VAL-059 | SYN-000311 | HTN_INPATIENT | `20260924:311:HTN_INPATIENT` | 70 F | error | omission | amlodipine 5 MG Oral Tablet (`197361`) |
| VAL-060 | SYN-000312 | HTN_INPATIENT | `20260924:312:HTN_INPATIENT` | 71 F | error | dose_mismatch | amlodipine 5 MG Oral Tablet (`197361`) — discharge **2 MG** vs home `5 MG` |
| VAL-061 | SYN-000313 | HTN_INPATIENT | `20260924:313:HTN_INPATIENT` | 60 F | error | frequency_mismatch | lisinopril 1 MG/ML Oral Solution (`1806884`) — discharge **twice daily** |
| VAL-062 | SYN-000314 | HTN_INPATIENT | `20260924:314:HTN_INPATIENT` | 71 F | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-063 | SYN-000315 | HTN_INPATIENT | `20260924:315:HTN_INPATIENT` | 77 F | **clean control** | — | — |
| VAL-064 | SYN-000316 | T2DM_INPATIENT | `20260924:316:T2DM_INPATIENT` | 49 M | error | omission | atorvastatin 80 MG Oral Tablet (`259255`) |
| VAL-065 | SYN-000317 | T2DM_INPATIENT | `20260924:317:T2DM_INPATIENT` | 63 M | error | dose_mismatch | lisinopril 1 MG/ML Oral Solution (`1806884`) — discharge **2 MG/ML** vs home `1 MG/ML` |
| VAL-066 | SYN-000318 | T2DM_INPATIENT | `20260924:318:T2DM_INPATIENT` | 52 F | error | frequency_mismatch | lisinopril 1 MG/ML Oral Solution (`1806884`) — discharge **twice daily** |
| VAL-067 | SYN-000319 | T2DM_INPATIENT | `20260924:319:T2DM_INPATIENT` | 64 F | error | omission | lisinopril 1 MG/ML Oral Solution (`1806884`) |
| VAL-068 | SYN-000320 | T2DM_INPATIENT | `20260924:320:T2DM_INPATIENT` | 68 M | **clean control** | — | — |
| VAL-069 | SYN-000321 | CAP_INPATIENT | `20260924:321:CAP_INPATIENT` | 70 F | error | omission | azithromycin 250 MG Oral Capsule (`141962`) |
| VAL-070 | SYN-000322 | CAP_INPATIENT | `20260924:322:CAP_INPATIENT` | 52 M | error | dose_mismatch | pantoprazole 20 MG Delayed Release Oral Tablet (`251872`) — discharge **10 MG** vs home `20 MG` |
| VAL-071 | SYN-000323 | CAP_INPATIENT | `20260924:323:CAP_INPATIENT` | 74 M | error | frequency_mismatch | azithromycin 250 MG Oral Capsule (`141962`) — discharge **twice daily** |
| VAL-072 | SYN-000324 | CAP_INPATIENT | `20260924:324:CAP_INPATIENT` | 49 M | **clean control** | — | — |

Clean expected discharge lists **never** include ibuprofen. Clean controls still list ibuprofen on home and inpatient with an explicit hold when the scenario has a stop medication. Error-bearing `incorrect_continuation` cases are the only ones with ibuprofen on discharge.

---

## Per-case catalog

Each block is the frozen case as exported. Lab/vital numbers are synthetic. Continue vs stop is the **correct** reconciliation plan (investigator view). Discharge-list mutations are listed under “Planted error”.

### `HF_INPATIENT` — I50.20, Unspecified systolic (congestive) heart failure

Symptoms (as stored on this freeze): Dyspnea, Anasarca, Orthopnea. Specialty: cardiology.
Correct continue meds on the clean plan: furosemide 4 MG/ML Oral Solution, spironolactone 1 MG/ML Oral Suspension, apixaban 2.5 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, atorvastatin 80 MG Oral Tablet.
Held stop med: ibuprofen 0.05 MG/MG Topical Gel.
Labs: Cr `14682-9`, K `2823-3`, BNP `30934-4`, INR `38875-1`.

#### VAL-049 (`SYN-000301`) — omission

- Seed `20260924:301:HF_INPATIENT`. 72-year-old Female, 71 kg. Vitals: BP 144/79, HR 107, RR 23, SpO2 98.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 0.9 umol/L, K 4.7 mmol/L, BNP 652 pg/mL, INR 3.1.
- Planted error: lisinopril 1 MG/ML Oral Solution (`1806884`) omitted from discharge (present home + inpatient).

#### VAL-050 (`SYN-000302`) — dose_mismatch

- Seed `20260924:302:HF_INPATIENT`. 55-year-old Male, 102 kg. Vitals: BP 133/80, HR 90, RR 16, SpO2 93.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 1 umol/L, K 4.4 mmol/L, BNP 811 pg/mL, INR 2.2.
- Planted error: discharge lisinopril 1 MG/ML Oral Solution (`1806884`) dose **2 MG/ML** (home/inpatient remain `1 MG/ML`).

#### VAL-051 (`SYN-000303`) — frequency_mismatch

- Seed `20260924:303:HF_INPATIENT`. 72-year-old Male, 76 kg. Vitals: BP 155/82, HR 78, RR 19, SpO2 94.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 0.8 umol/L, K 4.2 mmol/L, BNP 473 pg/mL, INR 2.3.
- Planted error: discharge metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-052 (`SYN-000304`) — incorrect_continuation

- Seed `20260924:304:HF_INPATIENT`. 61-year-old Male, 63 kg. Vitals: BP 122/79, HR 96, RR 23, SpO2 95.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.2 umol/L, K 4.6 mmol/L, BNP 280 pg/mL, INR 2.5.
- Planted error: ibuprofen 0.05 MG/MG Topical Gel (`141997`) **continued on discharge** (correct plan is stop).

#### VAL-053 (`SYN-000305`) — clean control

- Seed `20260924:305:HF_INPATIENT`. 59-year-old Female, 104 kg. Vitals: BP 157/76, HR 73, RR 23, SpO2 98.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.5 umol/L, K 3.8 mmol/L, BNP 261 pg/mL, INR 1.9.
- Discharge list: apixaban 2.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, furosemide 4 MG/ML Oral Solution, lisinopril 1 MG/ML Oral Solution, metoprolol tartrate 37.5 MG Oral Tablet, spironolactone 1 MG/ML Oral Suspension. No planted error.

### `AF_ANTICOAGULATION` — I48.0, Paroxysmal atrial fibrillation

Symptoms (as stored on this freeze): Dyspnea, Chronic fatigue syndrome. Specialty: cardiology.
Shared continue meds: metoprolol, atorvastatin, plus exactly one of warfarin or apixaban (mutex pick from the seed).
Held stop med: ibuprofen 0.05 MG/MG Topical Gel.
Labs: Cr `14682-9`, INR `38875-1`.

#### VAL-054 (`SYN-000306`) — omission

- Seed `20260924:306:AF_ANTICOAGULATION`. 84-year-old Female, 73 kg. Vitals: BP 127/94, HR 89, RR 22, SpO2 97.
- Anticoagulant: **warfarin sodium 1 MG Oral Tablet**.
- Labs: Cr 1.3 umol/L, INR 2.5.
- Planted error: metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) omitted from discharge (present home + inpatient).

#### VAL-055 (`SYN-000307`) — dose_mismatch

- Seed `20260924:307:AF_ANTICOAGULATION`. 69-year-old Male, 85 kg. Vitals: BP 135/93, HR 103, RR 20, SpO2 95.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.4 umol/L, INR 2.1.
- Planted error: discharge metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) dose **27.5 MG** (home/inpatient remain `37.5 MG`).

#### VAL-056 (`SYN-000308`) — frequency_mismatch

- Seed `20260924:308:AF_ANTICOAGULATION`. 67-year-old Male, 72 kg. Vitals: BP 155/75, HR 99, RR 17, SpO2 95.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.4 umol/L, INR 2.9.
- Planted error: discharge metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-057 (`SYN-000309`) — incorrect_continuation

- Seed `20260924:309:AF_ANTICOAGULATION`. 63-year-old Male, 100 kg. Vitals: BP 128/85, HR 109, RR 24, SpO2 95.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.6 umol/L, INR 2.3.
- Planted error: ibuprofen 0.05 MG/MG Topical Gel (`141997`) **continued on discharge** (correct plan is stop).

#### VAL-058 (`SYN-000310`) — clean control

- Seed `20260924:310:AF_ANTICOAGULATION`. 82-year-old Male, 110 kg. Vitals: BP 158/86, HR 85, RR 18, SpO2 94.
- Anticoagulant: **apixaban 2.5 MG Oral Tablet**.
- Labs: Cr 1.4 umol/L, INR 2.2.
- Discharge list: apixaban 2.5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, metoprolol tartrate 37.5 MG Oral Tablet. No planted error.

### `HTN_INPATIENT` — I10, Essential (primary) hypertension

Symptoms (as stored on this freeze): Chronic fatigue syndrome. Specialty: general medicine.
Correct continue meds on the clean plan: lisinopril 1 MG/ML Oral Solution, amlodipine 5 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, atorvastatin 80 MG Oral Tablet.
Held stop med: ibuprofen 0.05 MG/MG Topical Gel.
Labs: Cr `14682-9`, K `2823-3`, Na `2951-2`.

#### VAL-059 (`SYN-000311`) — omission

- Seed `20260924:311:HTN_INPATIENT`. 70-year-old Female, 109 kg. Vitals: BP 119/83, HR 98, RR 18, SpO2 91.
- Labs: Cr 0.9 umol/L, K 4.6 mmol/L, Na 134 mmol/L.
- Planted error: amlodipine 5 MG Oral Tablet (`197361`) omitted from discharge (present home + inpatient).

#### VAL-060 (`SYN-000312`) — dose_mismatch

- Seed `20260924:312:HTN_INPATIENT`. 71-year-old Female, 109 kg. Vitals: BP 148/88, HR 82, RR 17, SpO2 94.
- Labs: Cr 0.9 umol/L, K 3.8 mmol/L, Na 142 mmol/L.
- Planted error: discharge amlodipine 5 MG Oral Tablet (`197361`) dose **2 MG** (home/inpatient remain `5 MG`).

#### VAL-061 (`SYN-000313`) — frequency_mismatch

- Seed `20260924:313:HTN_INPATIENT`. 60-year-old Female, 79 kg. Vitals: BP 124/89, HR 105, RR 17, SpO2 94.
- Labs: Cr 0.8 umol/L, K 4.7 mmol/L, Na 140 mmol/L.
- Planted error: discharge lisinopril 1 MG/ML Oral Solution (`1806884`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-062 (`SYN-000314`) — incorrect_continuation

- Seed `20260924:314:HTN_INPATIENT`. 71-year-old Female, 92 kg. Vitals: BP 150/86, HR 110, RR 17, SpO2 92.
- Labs: Cr 1 umol/L, K 3.7 mmol/L, Na 136 mmol/L.
- Planted error: ibuprofen 0.05 MG/MG Topical Gel (`141997`) **continued on discharge** (correct plan is stop).

#### VAL-063 (`SYN-000315`) — clean control

- Seed `20260924:315:HTN_INPATIENT`. 77-year-old Female, 64 kg. Vitals: BP 133/70, HR 109, RR 23, SpO2 94.
- Labs: Cr 1.5 umol/L, K 3.7 mmol/L, Na 134 mmol/L.
- Discharge list: amlodipine 5 MG Oral Tablet, atorvastatin 80 MG Oral Tablet, hydrochlorothiazide 50 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution. No planted error.

### `T2DM_INPATIENT` — E11.8, Type 2 diabetes mellitus with unspecified complications

Symptoms (as stored on this freeze): Polyuria, Chronic fatigue syndrome. Specialty: general medicine.
Correct continue meds on the clean plan: lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet, atorvastatin 80 MG Oral Tablet.
Labs: Cr `14682-9`, glucose `14749-6`, Hb `55782-7`.

#### VAL-064 (`SYN-000316`) — omission

- Seed `20260924:316:T2DM_INPATIENT`. 49-year-old Male, 77 kg. Vitals: BP 146/83, HR 82, RR 24, SpO2 95.
- Labs: Cr 1.4 umol/L, glucose 171 mmol/L, Hb 13.1 g/dL.
- Planted error: atorvastatin 80 MG Oral Tablet (`259255`) omitted from discharge (present home + inpatient).

#### VAL-065 (`SYN-000317`) — dose_mismatch

- Seed `20260924:317:T2DM_INPATIENT`. 63-year-old Male, 91 kg. Vitals: BP 130/91, HR 83, RR 23, SpO2 97.
- Labs: Cr 1.3 umol/L, glucose 154 mmol/L, Hb 12.9 g/dL.
- Planted error: discharge lisinopril 1 MG/ML Oral Solution (`1806884`) dose **2 MG/ML** (home/inpatient remain `1 MG/ML`).

#### VAL-066 (`SYN-000318`) — frequency_mismatch

- Seed `20260924:318:T2DM_INPATIENT`. 52-year-old Female, 97 kg. Vitals: BP 148/72, HR 78, RR 24, SpO2 96.
- Labs: Cr 0.8 umol/L, glucose 152 mmol/L, Hb 14.1 g/dL.
- Planted error: discharge lisinopril 1 MG/ML Oral Solution (`1806884`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-067 (`SYN-000319`) — omission

- Seed `20260924:319:T2DM_INPATIENT`. 64-year-old Female, 108 kg. Vitals: BP 137/77, HR 81, RR 23, SpO2 92.
- Labs: Cr 1 umol/L, glucose 128 mmol/L, Hb 14.5 g/dL.
- Planted error: lisinopril 1 MG/ML Oral Solution (`1806884`) omitted from discharge (present home + inpatient).

#### VAL-068 (`SYN-000320`) — clean control

- Seed `20260924:320:T2DM_INPATIENT`. 68-year-old Male, 85 kg. Vitals: BP 146/89, HR 96, RR 21, SpO2 95.
- Labs: Cr 1.5 umol/L, glucose 134 mmol/L, Hb 13.8 g/dL.
- Discharge list: atorvastatin 80 MG Oral Tablet, lisinopril 1 MG/ML Oral Solution, Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet. No planted error.

### `CAP_INPATIENT` — J18.1, Lobar pneumonia, unspecified organism

Symptoms (as stored on this freeze): Cough, Dyspnea, Wheezing. Specialty: pulmonology.
Correct continue meds on the clean plan: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet.
Labs: Cr `14682-9`, Na `2951-2`, Hb `55782-7`.

#### VAL-069 (`SYN-000321`) — omission

- Seed `20260924:321:CAP_INPATIENT`. 70-year-old Female, 69 kg. Vitals: BP 150/69, HR 85, RR 24, SpO2 91.
- Labs: Cr 1 umol/L, Na 142 mmol/L, Hb 14.3 g/dL.
- Planted error: azithromycin 250 MG Oral Capsule (`141962`) omitted from discharge (present home + inpatient).

#### VAL-070 (`SYN-000322`) — dose_mismatch

- Seed `20260924:322:CAP_INPATIENT`. 52-year-old Male, 98 kg. Vitals: BP 133/78, HR 85, RR 22, SpO2 95.
- Labs: Cr 1.2 umol/L, Na 134 mmol/L, Hb 13.3 g/dL.
- Planted error: discharge pantoprazole 20 MG Delayed Release Oral Tablet (`251872`) dose **10 MG** (home/inpatient remain `20 MG`).

#### VAL-071 (`SYN-000323`) — frequency_mismatch

- Seed `20260924:323:CAP_INPATIENT`. 74-year-old Male, 100 kg. Vitals: BP 134/68, HR 74, RR 23, SpO2 94.
- Labs: Cr 1 umol/L, Na 141 mmol/L, Hb 11.3 g/dL.
- Planted error: discharge azithromycin 250 MG Oral Capsule (`141962`) frequency **twice daily** (home/inpatient remain `once daily`).

#### VAL-072 (`SYN-000324`) — clean control

- Seed `20260924:324:CAP_INPATIENT`. 49-year-old Male, 81 kg. Vitals: BP 132/69, HR 83, RR 22, SpO2 95.
- Labs: Cr 1.6 umol/L, Na 137 mmol/L, Hb 13.4 g/dL.
- Discharge list: albuterol 0.4 MG Inhalation Powder, azithromycin 250 MG Oral Capsule, pantoprazole 20 MG Delayed Release Oral Tablet. No planted error.

---

## Repeatability

**Bit-identical study reprint:** use the committed files in this directory.

A second `freeze-validation-batch` on this plan reuses immutable VAL IDs and does not rewrite cases. Live API re-bootstrap is not guaranteed bit-identical. If ranking drifts, keep this freeze and start a new `batch_code` rather than editing JSON to substitute a “more typical” RXCUI or unit.

