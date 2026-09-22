# Resident-validation dataset and full generation pipeline

This directory holds the frozen resident-review study copies. All batches are **machine-validated synthetic resident-review cases pending clinician validation**. Software checks terminology, structure, and the three implemented source-backed rules. These records are **not clinically validated** until residents complete review.

| Batch | Public IDs | Internal IDs | Master seed | Plan / exports |
| --- | --- | --- | --- | --- |
| `RESIDENT_VALIDATION_V1` | `VAL-001`–`VAL-024` | `SYN-000101`–`SYN-000124` | `20260922` | this folder ([`batch_plan.json`](batch_plan.json)) |
| `RESIDENT_VALIDATION_V2` | `VAL-025`–`VAL-048` | `SYN-000201`–`SYN-000224` | `20260923` | [`v2/`](v2/) |
| `RESIDENT_VALIDATION_V3` | `VAL-049`–`VAL-072` | `SYN-000301`–`SYN-000324` | `20260924` | [`v3/`](v3/) |
| `RESIDENT_VALIDATION_V4` | `VAL-073`–`VAL-096` | `SYN-000401`–`SYN-000424` | `20260925` | [`v4/`](v4/) |

Each later batch uses the **same five inpatient families and error mix** as V1, with a new `batch_code`, new VAL IDs, new sequences, and a new master seed. VAL IDs are globally unique and immutable. Do not freeze V2–V4 with the default plan (that would try to reuse `VAL-001`–`VAL-024`). Do not export V2–V4 into this folder (that would overwrite the V1 study files).

```bash
clinical-case-generator freeze-validation-batch --plan data/validation/v2/batch_plan.json
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V2 --output-dir data/validation/v2
# repeat for v3 / v4 and RESIDENT_VALIDATION_V3 / V4
```

The remainder of this README is the investigator catalog for **`RESIDENT_VALIDATION_V1`**. Investigator catalogs for V2–V4 live in the corresponding subdirectory README.

The committed JSON and Markdown files are the **study source of truth**. Regenerating against live terminology APIs can change RxNorm or LOINC ranking even with the same seeds. Use the committed files to score, reprint, or reload a frozen batch; do not treat a new live freeze as bit-identical unless the exports match.

---

## Dataset identity (this freeze)

| Field | Value |
| --- | --- |
| Batch code | `RESIDENT_VALIDATION_V1` |
| Generator | `clinical-case-generator` `0.1.0` |
| Master seed | `20260922` |
| Case seed formula | `{master_seed}:{sequence}:{scenario}` (example: `20260922:101:HF_INPATIENT`) |
| Internal case IDs | `SYN-000101`–`SYN-000124` |
| Frozen public IDs | `VAL-001`–`VAL-024` |
| Frozen at | `2026-09-22T12:30:18.503185+00:00` |
| Exported at | `2026-09-22T12:31:06.013739+00:00` |
| Cases | 24 frozen, 0 rejected |
| Clean controls | 5 (`VAL-005`, `VAL-010`, `VAL-015`, `VAL-020`, `VAL-024`) |
| Error-bearing | 19 (exactly one planted medication-reconciliation error each) |
| OpenAI | **not used** (`freeze-validation-batch` hardcodes `use_openai=False`) |
| Dataset status string | `machine-validated synthetic resident-review cases pending clinician validation` |

Sequences **101–124** are intentional. They keep this freeze away from earlier smoke cases `SYN-000001`–`SYN-000003`.

---

## Files in this directory

| File | Audience | Contents |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Investigators / operators | Master seed, VAL IDs, scenarios, inject flags, error categories, sequences |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Residents | Blinded dashboard-shaped cases. **Give this file to reviewers.** |
| [`investigator_answer_key.json`](investigator_answer_key.json) | Investigators only | Seeds, SYN IDs, error category, affected RXCUI, clean expected state, rule/reference snapshots |
| [`investigator_answer_key.md`](investigator_answer_key.md) | Investigators only | Human-readable answer key |
| [`validation_manifest.json`](validation_manifest.json) | Investigators | Per-VAL freeze metadata, source versions, enabled rules |
| [`coverage_report.md`](coverage_report.md) | Investigators | Scenario, error, terminology, and rule counts |
| [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md) | Investigators | Resolved diagnoses, meds, labs, and allowed error types per family |
| [`resident_review_worksheet.csv`](resident_review_worksheet.csv) | Residents / study staff | Empty capture rows for VAL-001–024; no fabricated ratings |
| [`resident_review_schema.json`](resident_review_schema.json) | Study staff | Field definitions for the worksheet |

Do **not** give residents the investigator key, the manifest, this README’s planted-error tables, `batch_plan.json`, or the coverage files. Those leak control status, seeds, and intended errors.

`data/exports/**` is gitignored. Tracked study artifacts live only under `data/validation/` (V1 in this folder; V2–V4 in `v2/`, `v3/`, `v4/`).

| Folder | Audience | Contents |
| --- | --- | --- |
| [`v2/`](v2/) | Investigators / residents (split files as in this folder) | `RESIDENT_VALIDATION_V2` plan, freeze exports, investigator catalog |
| [`v3/`](v3/) | same split | `RESIDENT_VALIDATION_V3` |
| [`v4/`](v4/) | same split | `RESIDENT_VALIDATION_V4` |

---

## Who receives which file

**Residents** receive:

- `resident_validation_cases.json`
- `resident_review_worksheet.csv` (and optionally the schema)

The resident JSON follows the dashboard case template: nested `ClinicalCase` (presentation, social_support, discharge_planning) plus `CaseDiagnosis`, `CaseNote`, `CaseVital`, `CaseLab`, `CaseImaging`, `CaseConsult`, `CaseMedication`, `CaseFollowup`, `CaseInstruction`, and the other dashboard arrays. It **omits** `CaseAnswerKey`. Titles and child business IDs use `VAL-*` (`DX-VAL001-001`, `MED-VAL001-001`, …), not `SYN-*`. RXCUI `source_reference`, error category, seeds, rule names, and the clean-control flag are redacted. Patient display names are `VAL Patient 001`, not `SYN Patient 101`.

**Investigators** keep:

- this README
- `investigator_answer_key.json` / `.md`
- `validation_manifest.json`
- `batch_plan.json`
- coverage files

---

## End-to-end pipeline

```text
.env + PostgreSQL
        │
        ▼
   db-init                    Alembic head + data_source_registry rows
        │                     (no clinical concepts)
        ▼
bootstrap-reference-data      official APIs → ref_* rows + rule enablement
        │                     manifest.json / scenarios.json / rule_templates.json
        ▼
freeze-validation-batch       per VAL assignment:
        │                       generate clean case from local ref_*
        │                       validate (structural / terminology / clinical / plan)
        │                       optionally inject exactly one recon error
        │                       re-validate
        │                       assign immutable VAL-* if audit passes
        ▼
export-validation-batch       blinded resident JSON + investigator key
                              + manifest + coverage + empty worksheet
                              + leak audit
        ▼
resident review               worksheet ratings (human)
        ▼
clinician validation          not performed by this software
```

### 0. Prerequisites

Python 3.12, PostgreSQL 16, and a virtualenv:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Required for this freeze:

| Variable | Role |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy URL. Default `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `LOINC_USERNAME` / `LOINC_PASSWORD` | Regenstrief FHIR Terminology Service. Empty values raise `SourceNotConfigured`; labs are not invented |

Leave `OPENAI_API_KEY` empty to match this freeze. The freeze CLI does not call OpenAI even if a key is present. Ad-hoc `generate-synthetic-cases` **will** word narratives with OpenAI when a key is set; that path is not how `RESIDENT_VALIDATION_V1` was built.

`.env` is gitignored. Never commit LOINC credentials.

SNOMED CT and MIMIC stay disabled. `snomed_code` remains null rather than invented.

### 1. Database

```bash
docker compose up -d
clinical-case-generator db-init
```

`db-init` runs `alembic upgrade head` and seeds eight `data_source_registry` metadata rows. It does not load RxNorm, LOINC, or diagnoses.

Alembic ancestry that must remain intact:

- `1c236aeaadc7` — Phase 1 clinical schema (do not rewrite)
- `7b9e4c21d6a0` — `clinical_rules`
- `c3f8a91b2e47` — `validation_batch_cases` (immutable VAL-* assignments)

### 2. Bounded reference bootstrap

```bash
clinical-case-generator bootstrap-reference-data
```

This reads human-readable **search requests** from [`data/bootstrap/manifest.json`](../bootstrap/manifest.json), not fabricated codes. For each request it calls official APIs, upserts only identifiers the source returned, stores DailyMed SPL labels for resolved RXCUIs, and enables curated rules only when DailyMed or RxClass evidence is present.

A second bootstrap does not duplicate canonical identifiers. Unresolved requests are reported and skipped.

What bootstrap does **not** do:

- invent RXCUI, LOINC, ICD-10-CM, UCUM, or SNOMED identifiers
- store LOINC Parts (`LP`), answers (`LA`), or groups (`LG`) as labs
- select RxNorm combination products (`name / name`, TTY `MIN`, or more than one related ingredient) unless the request itself is a combination
- write HPO `HP:` identifiers into `snomed_code` (HPO is source metadata / synonyms only)
- invent a numeric conversion factor for composed UCUM units such as `kg` when the official essence file does not supply one

Targeted one-off sync (not required if bootstrap already resolved the concept):

```bash
clinical-case-generator sync-rxnorm --name <medication-name>
clinical-case-generator sync-loinc --query <lab-name>
clinical-case-generator sync-ucum --query <unit-text>
clinical-case-generator sync-icd10 --query <diagnosis-text>
clinical-case-generator reference-search medications --query <text>
```

### 3. Freeze the VAL-* batch

```bash
clinical-case-generator freeze-validation-batch
```

Default plan: [`batch_plan.json`](batch_plan.json). Optional: `--plan path/to/plan.json`.

For each assignment the freeze:

1. Builds `case_seed = f"{master_seed}:{sequence}:{scenario}"`.
2. Reuses the existing row if that VAL ID is already immutable **and** the stored seed/scenario match the plan.
3. Otherwise generates `SYN-{sequence:06d}` from local `ref_*` rows only.
4. Validates the clean case (four layers: structural, terminology, clinical rules, medication plan).
5. Injects the planned error category when `inject_error` is true, using Python `random.Random(case_seed)` — not an LLM.
6. Validates again. Post-injection validation is expected to pass the implemented rule engine; planted discharge-list discrepancies are the intended study signal, not unexpected failures.
7. Rejects the assignment instead of freezing if generation, resolution, or audit fails. This freeze had **zero** rejections.
8. Persists an immutable `validation_batch_cases` row: VAL ID, SYN ID, seed, scenario, control status, snapshots.

VAL IDs are **not overwritten**. A second freeze of the same plan reprints `reused: ["VAL-001", …]` and leaves cases unchanged. To build a different batch, use a new `batch_code` and new VAL IDs.

### 4. Export blinded and investigator files

```bash
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

Default output directory is this folder. Export regenerates the resident payload from the frozen case (it does not trust a stale in-memory resident snapshot) and runs a leak audit before writing.

Audit fails the export if the resident file contains:

- `SYN-` identifiers
- `TEST_` identifier **values** (the JSON key `test_name` is allowed; a bare `test_` substring is not used as a leak marker because it would false-positive on `test_name`)
- answer-key fields, seeds, rule codes, or clean-control flags

This freeze export reported `audit_passed: true`.

### 5. Optional ad-hoc generation (not this freeze)

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator validate-cases --case-id SYN-000001
```

That path is for development. It is not how `VAL-001`–`VAL-024` were assigned. Do not mix `TEST_` fixture IDs into a resident-validation batch.

### 6. Checks

```bash
pytest
ruff check .
mypy
```

HTTP is mocked in pytest. Live bootstrap/freeze is a separate operator step and needs LOINC credentials.

---

## Official sources used at freeze time

| Source | Official URL | Version recorded in this freeze | Rows imported (approx.) |
| --- | --- | --- | --- |
| RxNorm (RxNav) | `https://rxnav.nlm.nih.gov/REST` | `08-Sep-2026` | 16 medications |
| LOINC FHIR TS | `https://fhir.loinc.org` | `2.83` | 7 lab terms |
| LOINC valueset | `http://loinc.org?fhir_vs` (implicit CodeSystem valueset; `http://loinc.org/vs` 404s) | — | — |
| UCUM essence XML | `https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml` | `2.2` | 16 units |
| ICD-10-CM | `https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search` | none supplied by API | 5 diagnoses |
| DailyMed | `https://dailymed.nlm.nih.gov/dailymed/services/v2` | none supplied by API | 10 labels |
| NLM conditions | `https://clinicaltables.nlm.nih.gov/api/conditions/v3/search` | — | symptoms (token match) |
| NLM HPO | `https://clinicaltables.nlm.nih.gov/api/hpo/v3/search` | — | Orthopnea fallback |
| RxClass | `https://rxnav.nlm.nih.gov/REST/rxclass` | — | furosemide/edema class |

Provenance columns `source_system`, `source_version`, and timezone-aware `retrieved_at` are stored on every real reference row.

Last successful sync timestamps from the freeze-time snapshot:

- RxNorm `2026-09-22T12:29:57.737695+00:00`
- ICD-10-CM `2026-09-22T12:29:58.025713+00:00`
- UCUM `2026-09-22T12:29:58.463277+00:00`
- LOINC `2026-09-22T12:30:12.174574+00:00`
- DailyMed `2026-09-22T12:30:16.289246+00:00`

---

## Bootstrap inputs that define the case families

Three checked-in files drive generation. Changing them changes **future** batches; it does not mutate this freeze.

### `data/bootstrap/manifest.json` (v2)

Human-readable requests: 16 medication names, 5 diagnoses, 8 symptoms, 7 labs, 9 unit texts. Codes are filled in only after the official APIs answer.

Aspirin and carvedilol were bootstrapped and stored in `ref_medications`. They are **not used** in any of the 24 frozen cases.

### `data/bootstrap/scenarios.json` (v2)

Five inpatient families (within the 5–6 family bound):

| Code | Specialty | Age | Diagnosis query | Meds | Stop med | Anticoagulant mutex (exactly one) | Labs | Allowed errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HF_INPATIENT` | cardiology | 55–85 | heart failure | lisinopril, furosemide, metoprolol, spironolactone, atorvastatin | ibuprofen | warfarin **or** apixaban | K, Cr, INR, natriuretic peptide | omission, dose, frequency, incorrect_continuation |
| `AF_ANTICOAGULATION` | cardiology | 60–88 | atrial fibrillation | metoprolol, atorvastatin | ibuprofen | warfarin **or** apixaban | INR, Cr | same four |
| `HTN_INPATIENT` | general medicine | 50–80 | essential (primary) hypertension | lisinopril, amlodipine, hydrochlorothiazide, atorvastatin | ibuprofen | (none) | Cr, K, Na | same four |
| `T2DM_INPATIENT` | general medicine | 45–80 | type 2 diabetes mellitus | metformin, lisinopril, atorvastatin | (none) | (none) | glucose, Cr, hemoglobin | omission, dose, frequency |
| `CAP_INPATIENT` | pulmonology | 45–85 | pneumonia | azithromycin, albuterol, pantoprazole | (none) | (none) | hemoglobin, Cr, Na | omission, dose, frequency |

`T2DM_INPATIENT` and `CAP_INPATIENT` have no stop medication, so `incorrect_continuation` is not assigned. VAL-019 is a second omission in T2DM (there is no fourth allowed family). VAL-021–024 are four CAP cases (one clean control).

Ibuprofen is a **held** home/inpatient medication with plan decision `stop`. There is no hard “NSAID + heart failure” rule. Snapshot-from-case includes home meds, so a hard prohibit would reject the clean case.

### `data/bootstrap/rule_templates.json`

Rules stay disabled until evidence is attached. This freeze enabled all three:

| Rule | Type | Severity | Evidence |
| --- | --- | --- | --- |
| `NO_DUAL_ORAL_ANTICOAGULANT` | medication_incompatibility | hard | DailyMed SPL `a454cd24-0c6d-46e8-b1e4-197388606175` (needles: anticoagulant + concomitant) |
| `WARFARIN_INR_MONITORING` | monitoring_dependency | hard | DailyMed SPL `724b0061-f42a-4008-a078-09c800ee9785` **and** LOINC `38875-1`. Needles INR **or** prothrombin (`evidence_mode: any`) because this warfarin SPL monitoring text uses INR and does not say “prothrombin” |
| `FUROSEMIDE_HF_INDICATION` | medication_diagnosis_allow | soft | RxClass class `Edema` (not DailyMed-only) |

Coverage of rule **application** on frozen cases (from `coverage_report.md`): furosemide/HF on 5 HF cases; dual-anticoagulant and warfarin/INR rules on the 4 cases that actually carry warfarin (`VAL-001`, `003`, `005`, `010`). Investigator snapshots list all three enabled rules for every case because they were enabled in the local rule table at freeze time.

No additional rules were invented. OpenAI is never used to write or enable rules.

---

## How one case is generated (repeatable mechanics)

Implementation: `app/services/generation.py`, `error_injection.py`, `validation.py`, `validation_batch.py`, `bootstrap.py`.

For assignment `{validation_case_id, scenario, inject_error, error_category, sequence}`:

1. **Seed.** `case_seed = f"{master_seed}:{sequence}:{scenario.code}"`. `rng = random.Random(case_seed)` (Python 3.12 `random`).
2. **Internal ID.** `SYN-{sequence:06d}`. Child IDs use prefixes in `app/utils/identifiers.py` (`DX-`, `MED-`, `LAB-`, `PLAN-`, …). After freeze, the resident export rewrites those prefixes onto `VAL-NNN`.
3. **Diagnosis.** First local `ref_diagnoses` row matching the scenario query (already ICD-10-CM-backed).
4. **Symptoms.** Local `ref_symptoms` matching scenario queries. NLM conditions token match can return a more specific official name than the query (this freeze: `edema` → **Anasarca**, `fatigue` → **Chronic fatigue syndrome**). `orthopnea` failed conditions token match and resolved through NLM HPO (`HP:0012764` class); `snomed_code` is null.
5. **Medications.** Each scenario medication query is matched to one local RxNorm row. Combination SCDs are excluded at bootstrap. Anticoagulant mutex queries are sorted by RXCUI, then `rng.choice` picks **exactly one** of warfarin or apixaban. Selected meds are then sorted by RXCUI for stable insert order.
6. **Stop medications.** Ibuprofen when the scenario lists it. Plan decision `stop`; present on home and inpatient lists; absent from the clean discharge list.
7. **Labs.** Every scenario lab query must resolve to a stored official LOINC **term** code (`^\d{1,5}-\d$`). Missing labs reject the case. Ranking during bootstrap prefers serum/plasma/blood base analytes and deprioritizes panels, calibrators, dialysis, timed `--` names, ratios, and Parts.
8. **Hard rules.** A snapshot of ICD + RXCUIs + LOINCs is evaluated. Dual oral anticoagulants are never co-selected (mutex). Warfarin cases always include INR `38875-1`.
9. **Demographics and vitals (RNG, synthetic).** Age in the scenario band; sex `Female`/`Male`; hospital day 2–6; weight 60–110 kg; BP/HR/RR/SpO2 from integer ranges; temperature fixed `36.8`. Numeric labs/vitals are labeled `synthetic_model_generated` in the database; they are **not** MIMIC empirical draws.
10. **Dose / frequency.** Frequency is always `once daily` on the clean case. Dose is the RxNorm `strength` string when present, otherwise the synthetic fallback `1 tablet` (oral solutions, topical gel, albuterol powder, azithromycin capsule in this freeze).
11. **Narrative.** Template wording from already-selected names. Freeze does not call OpenAI. Allowed-name checks would reject model text that introduces unknown drugs or codes if OpenAI were enabled on the ad-hoc path.
12. **Clean validation.** Must pass before injection.
13. **Error injection** (if planned). See next section. The answer key is written by the injector from the planted mutation, not by an LLM.
14. **Freeze audit.** No `TEST_` IDs; canonical codes present; control status matches the plan; exactly one intended error when `inject_error` is true.

Lab value draws (still from `rng`, not clinical truth):

| Analyte (name match) | Draw |
| --- | --- |
| INR | `randint(18, 32) / 10` |
| potassium | `randint(35, 48) / 10` |
| creatinine | `randint(8, 16) / 10` |
| sodium | `randint(134, 144)` |
| glucose | `randint(110, 180)` |
| hemoglobin | `randint(105, 145) / 10` |
| natriuretic / BNP | `randint(180, 900)` |

Units on the case are the first example UCUM unit stored on the lab row (SI moles/volume for electrolytes/creatinine/glucose in this freeze).

---

## Planted error families

Exactly one family per error-bearing case. If the assigned family has no eligible target, freeze **rejects** the case rather than silently falling back.

| Category | Clean precondition | Mutation | How the altered value is chosen |
| --- | --- | --- | --- |
| `omission` | Plan `continue` with a discharge row | Delete that discharge row | Eligible continue meds sorted by RXCUI; `rng.choice` |
| `dose_mismatch` | Continue med with a parseable dose | Replace discharge dose | First character: if original starts with `2` → `1…`; else if it starts with a digit → `2…`; else `2 tablets instead of {original}` |
| `frequency_mismatch` | Continue med with a frequency | Flip `once daily` ↔ `twice daily` | Same RNG choice over eligible continue meds |
| `incorrect_continuation` | Stop med on home, **not** on clean discharge | Copy it onto the discharge list | Requires a scenario `stop_medication_queries` hit (ibuprofen in this freeze) |

Home and inpatient lists stay internally consistent with the clean plan. Residents should reconcile **discharge** against home/inpatient/held meds.

---

## Repeatability contract

**Bit-identical study reprint:** use the committed files in this directory. That is the intended repeatability path.

**Deterministic regeneration of the same VAL IDs from the same local `ref_*` rows:** same Python 3.12 `random.Random` seed string, same bootstrap ranking, `use_openai=False`. A second `freeze-validation-batch` on this plan will **reuse** immutable rows and will not rewrite cases.

**Live API re-bootstrap is not guaranteed bit-identical.** RxNav and LOINC search ranking can change. The same query (`lisinopril`, `hemoglobin`, `edema`) can resolve to a different official concept tomorrow. If that happens, keep this freeze as the dataset and start a new `batch_code` for any replacement.

**Do not** hand-edit frozen JSON to “fix” formulation or unit realism. Those are resident-review limitations, not license to invent a more typical tablet RXCUI or a conventional US lab unit that the source did not return.

---

## Resolved terminology used in VAL-001–024

### Diagnoses (ICD-10-CM)

| ICD-10-CM | Preferred name | Families |
| --- | --- | --- |
| I50.20 | Unspecified systolic (congestive) heart failure | HF |
| I48.0 | Paroxysmal atrial fibrillation | AF |
| I10 | Essential (primary) hypertension | HTN |
| E11.8 | Type 2 diabetes mellitus with unspecified complications | T2DM |
| J18.1 | Lobar pneumonia, unspecified organism | CAP |

### Medications (RxNorm)

| RXCUI | RxNav name | Role in freeze |
| --- | --- | --- |
| 1806884 | lisinopril 1 MG/ML Oral Solution | HF, HTN, T2DM |
| 104220 | furosemide 4 MG/ML Oral Solution | HF |
| 1606347 | metoprolol tartrate 37.5 MG Oral Tablet | HF, AF |
| 104230 | spironolactone 1 MG/ML Oral Suspension | HF |
| 259255 | atorvastatin 80 MG Oral Tablet | HF, AF, HTN, T2DM |
| 855288 | warfarin sodium 1 MG Oral Tablet | mutex pick on some HF/AF cases |
| 1364435 | apixaban 2.5 MG Oral Tablet | mutex pick on remaining HF/AF cases |
| 141997 | ibuprofen 0.05 MG/MG Topical Gel | held stop med (HF, AF, HTN) |
| 197361 | amlodipine 5 MG Oral Tablet | HTN |
| 197770 | hydrochlorothiazide 50 MG Oral Tablet | HTN |
| 1807888 | Modified 24 HR metformin hydrochloride 1000 MG Extended Release Oral Tablet | T2DM |
| 141962 | azithromycin 250 MG Oral Capsule | CAP |
| 104514 | albuterol 0.4 MG Inhalation Powder | CAP |
| 251872 | pantoprazole 20 MG Delayed Release Oral Tablet | CAP |

Warfarin vs apixaban is the only per-case medication branch inside a family; it is determined by `rng.choice` on the mutex list after sorting by RXCUI.

### Labs (LOINC 2.83)

| LOINC | Long common name | Unit on cases | Families |
| --- | --- | --- | --- |
| 2823-3 | Potassium [Moles/volume] in Serum or Plasma | mmol/L | HF, HTN |
| 14682-9 | Creatinine [Moles/volume] in Serum or Plasma | umol/L | all |
| 38875-1 | INR in Platelet poor plasma or blood by Coagulation assay | {INR} | HF, AF |
| 30934-4 | Natriuretic peptide B [Mass/volume] in Serum or Plasma | pg/mL | HF |
| 2951-2 | Sodium [Moles/volume] in Serum or Plasma | mmol/L | HTN, CAP |
| 14749-6 | Glucose [Moles/volume] in Serum or Plasma | mmol/L | T2DM |
| 55782-7 | Hemoglobin [Mass/volume] in Blood by Oximetry | g/dL | T2DM, CAP |

### Symptoms as stored (NLM / HPO names, not the bootstrap query text)

| Query | Stored preferred name | Notes |
| --- | --- | --- |
| dyspnea | Dyspnea | NLM conditions |
| edema | Anasarca | NLM token match; not generic “edema” |
| orthopnea | Orthopnea | HPO fallback; SNOMED null |
| fatigue | Chronic fatigue syndrome | NLM token match |
| polyuria | Polyuria | |
| cough | Cough | |
| wheezing | Wheezing | |

---

## Assignment index

| VAL | SYN | Scenario | Seed | Age / sex | Status | Error | Affected medication (RXCUI) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-001 | SYN-000101 | HF_INPATIENT | `20260922:101:HF_INPATIENT` | 73 M | error | omission | warfarin sodium 1 MG Oral Tablet (`855288`) |
| VAL-002 | SYN-000102 | HF_INPATIENT | `20260922:102:HF_INPATIENT` | 68 F | error | dose_mismatch | apixaban 2.5 MG Oral Tablet (`1364435`) — discharge **1.5 MG** vs home 2.5 MG |
| VAL-003 | SYN-000103 | HF_INPATIENT | `20260922:103:HF_INPATIENT` | 57 M | error | frequency_mismatch | lisinopril 1 MG/ML Oral Solution (`1806884`) — discharge **twice daily** |
| VAL-004 | SYN-000104 | HF_INPATIENT | `20260922:104:HF_INPATIENT` | 62 F | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) appears on discharge |
| VAL-005 | SYN-000105 | HF_INPATIENT | `20260922:105:HF_INPATIENT` | 74 F | **clean control** | — | — |
| VAL-006 | SYN-000106 | AF_ANTICOAGULATION | `20260922:106:AF_ANTICOAGULATION` | 81 F | error | omission | apixaban 2.5 MG Oral Tablet (`1364435`) |
| VAL-007 | SYN-000107 | AF_ANTICOAGULATION | `20260922:107:AF_ANTICOAGULATION` | 69 M | error | dose_mismatch | atorvastatin 80 MG Oral Tablet (`259255`) — discharge **20 MG** |
| VAL-008 | SYN-000108 | AF_ANTICOAGULATION | `20260922:108:AF_ANTICOAGULATION` | 68 F | error | frequency_mismatch | metoprolol tartrate 37.5 MG Oral Tablet (`1606347`) — discharge **twice daily** |
| VAL-009 | SYN-000109 | AF_ANTICOAGULATION | `20260922:109:AF_ANTICOAGULATION` | 74 M | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) on discharge |
| VAL-010 | SYN-000110 | AF_ANTICOAGULATION | `20260922:110:AF_ANTICOAGULATION` | 74 F | **clean control** | — | — |
| VAL-011 | SYN-000111 | HTN_INPATIENT | `20260922:111:HTN_INPATIENT` | 64 F | error | omission | hydrochlorothiazide 50 MG Oral Tablet (`197770`) |
| VAL-012 | SYN-000112 | HTN_INPATIENT | `20260922:112:HTN_INPATIENT` | 63 M | error | dose_mismatch | amlodipine 5 MG Oral Tablet (`197361`) — discharge **2 MG** |
| VAL-013 | SYN-000113 | HTN_INPATIENT | `20260922:113:HTN_INPATIENT` | 60 F | error | frequency_mismatch | atorvastatin 80 MG Oral Tablet (`259255`) — discharge **twice daily** |
| VAL-014 | SYN-000114 | HTN_INPATIENT | `20260922:114:HTN_INPATIENT` | 58 M | error | incorrect_continuation | ibuprofen 0.05 MG/MG Topical Gel (`141997`) on discharge |
| VAL-015 | SYN-000115 | HTN_INPATIENT | `20260922:115:HTN_INPATIENT` | 61 F | **clean control** | — | — |
| VAL-016 | SYN-000116 | T2DM_INPATIENT | `20260922:116:T2DM_INPATIENT` | 55 F | error | omission | metformin ER 1000 MG (`1807888`) |
| VAL-017 | SYN-000117 | T2DM_INPATIENT | `20260922:117:T2DM_INPATIENT` | 70 M | error | dose_mismatch | atorvastatin 80 MG Oral Tablet (`259255`) — discharge **20 MG** |
| VAL-018 | SYN-000118 | T2DM_INPATIENT | `20260922:118:T2DM_INPATIENT` | 48 F | error | frequency_mismatch | metformin ER 1000 MG (`1807888`) — discharge **twice daily** |
| VAL-019 | SYN-000119 | T2DM_INPATIENT | `20260922:119:T2DM_INPATIENT` | 48 F | error | omission | lisinopril 1 MG/ML Oral Solution (`1806884`) |
| VAL-020 | SYN-000120 | T2DM_INPATIENT | `20260922:120:T2DM_INPATIENT` | 72 M | **clean control** | — | — |
| VAL-021 | SYN-000121 | CAP_INPATIENT | `20260922:121:CAP_INPATIENT` | 53 F | error | omission | azithromycin 250 MG Oral Capsule (`141962`) |
| VAL-022 | SYN-000122 | CAP_INPATIENT | `20260922:122:CAP_INPATIENT` | 75 F | error | dose_mismatch | azithromycin 250 MG Oral Capsule (`141962`) — discharge **2 tablet** vs home `1 tablet` |
| VAL-023 | SYN-000123 | CAP_INPATIENT | `20260922:123:CAP_INPATIENT` | 62 M | error | frequency_mismatch | albuterol 0.4 MG Inhalation Powder (`104514`) — discharge **twice daily** |
| VAL-024 | SYN-000124 | CAP_INPATIENT | `20260922:124:CAP_INPATIENT` | 75 M | **clean control** | — | — |

Clean expected discharge lists **never** include ibuprofen. Clean controls still list ibuprofen on home and inpatient with an explicit hold. Error-bearing `incorrect_continuation` cases are the only ones with ibuprofen on discharge.

---

## Per-case catalog

Each block is the frozen case as exported. Lab/vital numbers are synthetic. Continue vs stop is the **correct** reconciliation plan (investigator view). Discharge-list mutations are listed under “Planted error”.

### HF_INPATIENT — I50.20, symptoms Dyspnea / Anasarca / Orthopnea

Shared continue meds: furosemide `104220`, spironolactone `104230`, metoprolol `1606347`, lisinopril `1806884`, atorvastatin `259255`, plus exactly one of warfarin `855288` or apixaban `1364435`. Shared labs: Cr `14682-9`, K `2823-3`, BNP `30934-4`, INR `38875-1`. Held: ibuprofen `141997`. Specialty cardiology.

#### VAL-001 (`SYN-000101`) — omission

- Seed `20260922:101:HF_INPATIENT`. 73-year-old Male, 97 kg. Vitals: BP 150/74, HR 90, RR 17, SpO2 94.
- Anticoagulant: **warfarin** 1 MG once daily.
- Labs: Cr 1.6 umol/L, K 4.4 mmol/L, BNP 324 pg/mL, INR 2.1.
- Planted error: warfarin omitted from discharge (present home + inpatient).
- Rules in play: all three (includes warfarin + INR + furosemide/HF).

#### VAL-002 (`SYN-000102`) — dose_mismatch

- Seed `20260922:102:HF_INPATIENT`. 68-year-old Female, 80 kg. Vitals: BP 155/80, HR 101, RR 24, SpO2 95.
- Anticoagulant: **apixaban** 2.5 MG once daily.
- Labs: Cr 1.4 umol/L, K 4.3 mmol/L, BNP 286 pg/mL, INR 3.0.
- Planted error: discharge apixaban dose **1.5 MG** (home/inpatient remain 2.5 MG).

#### VAL-003 (`SYN-000103`) — frequency_mismatch

- Seed `20260922:103:HF_INPATIENT`. 57-year-old Male, 70 kg. Vitals: BP 153/87, HR 75, RR 24, SpO2 93.
- Anticoagulant: **warfarin** 1 MG once daily.
- Labs: Cr 1.2 umol/L, K 3.5 mmol/L, BNP 561 pg/mL, INR 2.8.
- Planted error: discharge lisinopril frequency **twice daily** (home/inpatient remain once daily).

#### VAL-004 (`SYN-000104`) — incorrect_continuation

- Seed `20260922:104:HF_INPATIENT`. 62-year-old Female, 92 kg. Vitals: BP 146/94, HR 104, RR 16, SpO2 96.
- Anticoagulant: **apixaban** 2.5 MG once daily.
- Labs: Cr 0.9 umol/L, K 4.7 mmol/L, BNP 397 pg/mL, INR 2.0.
- Planted error: ibuprofen topical gel **continued on discharge** (correct plan is stop).

#### VAL-005 (`SYN-000105`) — clean control

- Seed `20260922:105:HF_INPATIENT`. 74-year-old Female, 108 kg. Vitals: BP 149/96, HR 73, RR 21, SpO2 97.
- Anticoagulant: **warfarin** 1 MG once daily.
- Labs: Cr 1.4 umol/L, K 4.0 mmol/L, BNP 464 pg/mL, INR 3.1.
- Discharge continue list: atorvastatin, furosemide, lisinopril, metoprolol, spironolactone, warfarin. Ibuprofen held. No planted error.

### AF_ANTICOAGULATION — I48.0, symptoms Dyspnea / Chronic fatigue syndrome

Shared continue meds: metoprolol `1606347`, atorvastatin `259255`, plus warfarin or apixaban. Labs: INR `38875-1`, Cr `14682-9`. Held: ibuprofen. Specialty cardiology.

#### VAL-006 (`SYN-000106`) — omission

- Seed `20260922:106:AF_ANTICOAGULATION`. 81-year-old Female, 84 kg. Vitals: BP 132/80, HR 98, RR 23, SpO2 94.
- Anticoagulant: **apixaban** 2.5 MG.
- Labs: Cr 0.9 umol/L, INR 2.0.
- Planted error: apixaban omitted from discharge.

#### VAL-007 (`SYN-000107`) — dose_mismatch

- Seed `20260922:107:AF_ANTICOAGULATION`. 69-year-old Male, 89 kg. Vitals: BP 122/79, HR 87, RR 19, SpO2 97.
- Anticoagulant: **apixaban** 2.5 MG.
- Labs: Cr 1.5 umol/L, INR 3.0.
- Planted error: discharge atorvastatin **20 MG** (home/inpatient 80 MG).

#### VAL-008 (`SYN-000108`) — frequency_mismatch

- Seed `20260922:108:AF_ANTICOAGULATION`. 68-year-old Female, 75 kg. Vitals: BP 135/86, HR 104, RR 18, SpO2 98.
- Anticoagulant: **apixaban** 2.5 MG.
- Labs: Cr 1.3 umol/L, INR 3.1.
- Planted error: discharge metoprolol **twice daily**.

#### VAL-009 (`SYN-000109`) — incorrect_continuation

- Seed `20260922:109:AF_ANTICOAGULATION`. 74-year-old Male, 80 kg. Vitals: BP 153/94, HR 89, RR 18, SpO2 98.
- Anticoagulant: **apixaban** 2.5 MG.
- Labs: Cr 1.0 umol/L, INR 2.1.
- Planted error: ibuprofen on discharge.

#### VAL-010 (`SYN-000110`) — clean control

- Seed `20260922:110:AF_ANTICOAGULATION`. 74-year-old Female, 104 kg. Vitals: BP 134/84, HR 90, RR 18, SpO2 92.
- Anticoagulant: **warfarin** 1 MG (the AF mutex pick on this seed).
- Labs: Cr 1.3 umol/L, INR 2.0.
- Discharge continue list: atorvastatin, metoprolol, warfarin. Ibuprofen held. No planted error.

### HTN_INPATIENT — I10, symptom Chronic fatigue syndrome

Shared continue meds: lisinopril `1806884`, amlodipine `197361`, hydrochlorothiazide `197770`, atorvastatin `259255`. Labs: Cr `14682-9`, K `2823-3`, Na `2951-2`. Held: ibuprofen. Specialty general medicine.

#### VAL-011 (`SYN-000111`) — omission

- Seed `20260922:111:HTN_INPATIENT`. 64-year-old Female, 85 kg. Vitals: BP 153/84, HR 109, RR 16, SpO2 97.
- Labs: Cr 1.4 umol/L, K 4.5 mmol/L, Na 141 mmol/L.
- Planted error: hydrochlorothiazide omitted from discharge.

#### VAL-012 (`SYN-000112`) — dose_mismatch

- Seed `20260922:112:HTN_INPATIENT`. 63-year-old Male, 106 kg. Vitals: BP 125/84, HR 90, RR 24, SpO2 93.
- Labs: Cr 0.8 umol/L, K 4.3 mmol/L, Na 143 mmol/L.
- Planted error: discharge amlodipine **2 MG** (home/inpatient 5 MG).

#### VAL-013 (`SYN-000113`) — frequency_mismatch

- Seed `20260922:113:HTN_INPATIENT`. 60-year-old Female, 85 kg. Vitals: BP 129/94, HR 90, RR 21, SpO2 97.
- Labs: Cr 1.6 umol/L, K 4.2 mmol/L, Na 140 mmol/L.
- Planted error: discharge atorvastatin **twice daily**.

#### VAL-014 (`SYN-000114`) — incorrect_continuation

- Seed `20260922:114:HTN_INPATIENT`. 58-year-old Male, 77 kg. Vitals: BP 123/69, HR 98, RR 19, SpO2 93.
- Labs: Cr 1.2 umol/L, K 4.6 mmol/L, Na 143 mmol/L.
- Planted error: ibuprofen on discharge.

#### VAL-015 (`SYN-000115`) — clean control

- Seed `20260922:115:HTN_INPATIENT`. 61-year-old Female, 99 kg. Vitals: BP 143/76, HR 74, RR 19, SpO2 95.
- Labs: Cr 1.4 umol/L, K 3.8 mmol/L, Na 137 mmol/L.
- Discharge continue list: amlodipine, atorvastatin, hydrochlorothiazide, lisinopril. Ibuprofen held. No planted error.

### T2DM_INPATIENT — E11.8, symptoms Polyuria / Chronic fatigue syndrome

Shared continue meds: metformin ER `1807888`, lisinopril `1806884`, atorvastatin `259255`. Labs: glucose `14749-6`, Cr `14682-9`, Hb `55782-7`. No stop medication. Specialty general medicine.

#### VAL-016 (`SYN-000116`) — omission

- Seed `20260922:116:T2DM_INPATIENT`. 55-year-old Female, 75 kg. Vitals: BP 119/85, HR 105, RR 19, SpO2 95.
- Labs: Cr 0.8 umol/L, glucose 154 mmol/L, Hb 11.4 g/dL.
- Planted error: metformin ER omitted from discharge.

#### VAL-017 (`SYN-000117`) — dose_mismatch

- Seed `20260922:117:T2DM_INPATIENT`. 70-year-old Male, 101 kg. Vitals: BP 131/73, HR 78, RR 20, SpO2 94.
- Labs: Cr 0.9 umol/L, glucose 174 mmol/L, Hb 13.6 g/dL.
- Planted error: discharge atorvastatin **20 MG**.

#### VAL-018 (`SYN-000118`) — frequency_mismatch

- Seed `20260922:118:T2DM_INPATIENT`. 48-year-old Female, 77 kg. Vitals: BP 125/96, HR 110, RR 19, SpO2 96.
- Labs: Cr 1.5 umol/L, glucose 149 mmol/L, Hb 13.1 g/dL.
- Planted error: discharge metformin ER **twice daily**.

#### VAL-019 (`SYN-000119`) — omission (second T2DM omission; no continuation family)

- Seed `20260922:119:T2DM_INPATIENT`. 48-year-old Female, 96 kg. Vitals: BP 142/91, HR 98, RR 22, SpO2 94.
- Labs: Cr 1.3 umol/L, glucose 139 mmol/L, Hb 11.7 g/dL.
- Planted error: lisinopril omitted from discharge.

#### VAL-020 (`SYN-000120`) — clean control

- Seed `20260922:120:T2DM_INPATIENT`. 72-year-old Male, 66 kg. Vitals: BP 127/80, HR 108, RR 24, SpO2 97.
- Labs: Cr 1.6 umol/L, glucose 138 mmol/L, Hb 12.9 g/dL.
- Discharge continue list: metformin ER, atorvastatin, lisinopril. No planted error.

### CAP_INPATIENT — J18.1, symptoms Cough / Dyspnea / Wheezing

Shared continue meds: azithromycin `141962`, albuterol `104514`, pantoprazole `251872`. Labs: Hb `55782-7`, Cr `14682-9`, Na `2951-2`. No stop medication. Specialty pulmonology.

#### VAL-021 (`SYN-000121`) — omission

- Seed `20260922:121:CAP_INPATIENT`. 53-year-old Female, 110 kg. Vitals: BP 118/70, HR 79, RR 21, SpO2 94.
- Labs: Cr 1.4 umol/L, Na 134 mmol/L, Hb 13.8 g/dL.
- Planted error: azithromycin omitted from discharge (home/inpatient keep `1 tablet` once daily because this SCD has no strength string).

#### VAL-022 (`SYN-000122`) — dose_mismatch

- Seed `20260922:122:CAP_INPATIENT`. 75-year-old Female, 94 kg. Vitals: BP 119/72, HR 89, RR 23, SpO2 92.
- Labs: Cr 1.2 umol/L, Na 141 mmol/L, Hb 14.4 g/dL.
- Planted error: discharge azithromycin **2 tablet** (home/inpatient `1 tablet`).

#### VAL-023 (`SYN-000123`) — frequency_mismatch

- Seed `20260922:123:CAP_INPATIENT`. 62-year-old Male, 85 kg. Vitals: BP 123/81, HR 102, RR 17, SpO2 97.
- Labs: Cr 0.8 umol/L, Na 143 mmol/L, Hb 12.1 g/dL.
- Planted error: discharge albuterol **twice daily**.

#### VAL-024 (`SYN-000124`) — clean control

- Seed `20260922:124:CAP_INPATIENT`. 75-year-old Male, 70 kg. Vitals: BP 130/96, HR 80, RR 17, SpO2 93.
- Labs: Cr 1.6 umol/L, Na 140 mmol/L, Hb 11.6 g/dL.
- Discharge continue list: albuterol, azithromycin, pantoprazole. No planted error.

---

## Resident review capture

[`resident_review_worksheet.csv`](resident_review_worksheet.csv) has one empty row per VAL ID. Columns (see [`resident_review_schema.json`](resident_review_schema.json)):

- `validation_case_id`
- `reviewer_id` (pseudonymous)
- `clinical_realism_rating` (1–5)
- `medication_reconciliation_correctness_rating` (1–5)
- `case_clarity_rating` (1–5)
- `identified_error_type`
- `identified_affected_medication`
- `confidence_rating` (1–5)
- `free_text_comments`
- `overall_acceptability`
- `revision_recommendation`

Do not pre-fill ratings. Scoring against the investigator key is a separate, unblinded step.

---

## Limitations reviewers should judge (not silently “fixed”)

These are properties of the official-source ranking and the generator, documented so the study is reproducible:

- **Formulation realism.** RxNav SCD ranking produced oral solutions (lisinopril, furosemide), spironolactone oral suspension, ibuprofen **topical gel**, albuterol inhalation powder, azithromycin capsule. Typical adult tablets were not substituted.
- **Synthetic fallback dose `1 tablet`** when RxNorm `strength` is empty (ibuprofen gel, azithromycin, albuterol, furosemide solution, spironolactone suspension).
- **SI lab units** (`mmol/L`, `umol/L`) and creatinine values drawn on a 0.8–1.6 scale that does not match a typical US mg/dL creatinine, because the stored example unit is moles/volume.
- **Glucose** LOINC 14749-6 is moles/volume; values 138–174 are labeled `mmol/L` from the source example unit (not a conventional mg/dL fingerstick range).
- **Hemoglobin** is LOINC **55782-7** (oximetry method), not a methodless mass/volume term.
- **NLM names** Anasarca and Chronic fatigue syndrome are what the conditions API returned for `edema` and `fatigue`.
- **Only four** reconciliation-error families exist. Duplicate therapy, missing co-prescription, contraindicated restart, and failure-to-restart are not generated.
- **INR** is still generated on apixaban HF/AF cases because the HF/AF lab list always includes the INR query; warfarin-specific monitoring is a hard rule only when warfarin is selected.
- Numeric vitals/labs are synthetic, not empirical MIMIC distributions. Raw MIMIC rows are never sent to OpenAI (and OpenAI was not used here).

---

## Operator checklist to reprint this freeze

On a database that already contains the frozen rows:

```bash
clinical-case-generator freeze-validation-batch
# expected: reused VAL-001 … VAL-024, rejected []
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

Compare the new export to git. The study dataset is unchanged if the JSON matches.

On a **empty** database, to rebuild local `ref_*` and then freeze:

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data   # live APIs; ranking may drift
clinical-case-generator freeze-validation-batch    # will create new SYN/VAL rows only if VAL IDs are absent
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

If live ranking differs, **stop** and keep the committed `data/validation/*.json` as the dataset. Do not overwrite git with a drifted export unless the study team explicitly starts a new batch.

---

## Code map

| Stage | Module |
| --- | --- |
| Official HTTP clients | `app/sources/` (`rxnorm`, `loinc`, `ucum`, `icd10cm`, `conditions`, `hpo`, `dailymed`, `rxclass`) |
| Bounded import + rule enablement | `app/services/bootstrap.py` |
| Concept selection + case persist | `app/services/generation.py` |
| Clinical IF/THEN | `app/services/rules.py` |
| Four-layer validation | `app/services/validation.py` |
| Reconciliation mutation | `app/services/error_injection.py` |
| VAL freeze / blinded export / leak audit | `app/services/validation_batch.py` |
| CLI | `app/cli/__init__.py` (`db-init`, `bootstrap-reference-data`, `freeze-validation-batch`, `export-validation-batch`) |
| LOINC term-code shape | `app/utils/loinc_codes.py` |
