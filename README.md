# Clinical Case Generator

Clinical Case Generator is a Python application that loads **official clinical terminology** into PostgreSQL, applies **source-backed IF/THEN rules**, and generates **constrained synthetic inpatient cases** for medication-reconciliation review.

It does **not** invent RxNorm, LOINC, SNOMED CT, ICD-10-CM, UCUM, or device identifiers. It does **not** send raw MIMIC patient rows, notes, identifiers, or events to OpenAI. Generated cases are **machine-validated synthetic records pending clinician validation**. Software checks terminology, structure, and the implemented source-backed rules. That is not the same as clinical validity.

The frozen resident-review batch `RESIDENT_VALIDATION_V1` (`VAL-001`–`VAL-024`), per-case seeds, official source versions, and the investigator catalog are in [`data/validation/README.md`](data/validation/README.md). Treat that file as **investigator-only**: it describes planted errors.

---

## Contents

1. [Project overview](#1-project-overview)
2. [Quick start](#2-quick-start)
3. [Architecture and repository layout](#3-architecture-and-repository-layout)
4. [Prerequisites](#4-prerequisites)
5. [Clone and initial setup](#5-clone-and-initial-setup)
6. [Environment configuration](#6-environment-configuration)
7. [Start PostgreSQL](#7-start-postgresql)
8. [Initialize the database](#8-initialize-the-database)
9. [Reference terminology](#9-reference-terminology)
10. [Bootstrap reference data](#10-bootstrap-reference-data)
11. [Individual terminology sync commands](#11-individual-terminology-sync-commands)
12. [Clinical rules](#12-clinical-rules)
13. [Generate synthetic cases](#13-generate-synthetic-cases)
14. [OpenAI usage](#14-openai-usage)
15. [Validate generated cases](#15-validate-generated-cases)
16. [Resident-validation workflow](#16-resident-validation-workflow)
17. [Resident-validation output files](#17-resident-validation-output-files)
18. [How to give cases to residents](#18-how-to-give-cases-to-residents)
19. [Reproducing the frozen validation batch](#19-reproducing-the-frozen-validation-batch)
20. [API](#20-api)
21. [Testing and code quality](#21-testing-and-code-quality)
22. [Common workflows](#22-common-workflows)
23. [Troubleshooting](#23-troubleshooting)
24. [Data provenance and safety constraints](#24-data-provenance-and-safety-constraints)
25. [Database and schema notes](#25-database-and-schema-notes)
26. [Current limitations](#26-current-limitations)
27. [Licensing](#27-licensing)

---

## 1. Project overview

### What this repository does

The application:

1. Talks to official terminology services (RxNav, LOINC FHIR, UCUM essence XML, NLM ICD-10-CM, NLM conditions, NLM HPO, DailyMed, RxClass).
2. Stores only identifiers and text those sources return, with provenance (`source_system`, `source_version`, `retrieved_at`).
3. Enables curated clinical conditionals only when DailyMed or RxClass evidence is attached.
4. Builds synthetic inpatient cases from **already stored** `ref_*` rows.
5. Validates each case (structural, terminology, hard clinical rules, medication-plan consistency).
6. Optionally plants exactly one medication-reconciliation error.
7. Freezes a resident-review batch as immutable `VAL-*` IDs and exports a **blinded** resident JSON plus an **investigator** answer key.

CLI entry point (from `pyproject.toml`): `clinical-case-generator = "app.cli:main"`.

### Problem it solves

Medication-reconciliation review studies need realistic-looking cases with known (hidden) discharge-list errors, using **canonical codes that can be cited**. This tool generates those cases from official vocabularies instead of free-text invention, then blinds the answer key for residents.

### Three data classes

**Authoritative reference data.** RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, and AccessGUDID *concepts* live in `ref_*` tables. Every real reference row keeps `source_system`, `source_version`, and a timezone-aware `retrieved_at`. Targeted sync and `bootstrap-reference-data` upsert **only** identifiers returned by official sources. DailyMed labels are stored when an RXCUI is already validated through RxNorm. SNOMED CT fields remain null rather than invented; there is **no SNOMED ingestion client** in this repository even if SNOMED environment variables are set. AccessGUDID and MIMIC ingestion are not implemented.

**Empirical aggregate data.** `ref_clinical_distributions` is for statistics calculated locally from a permitted dataset. Aggregates are not patient rows. A check constraint rejects `source_dataset = 'MIMIC_IV_RAW'`. This pipeline inserts no distribution rows and does not invent empirical distributions.

**Synthetic patient data.** `clinical_cases` and child tables hold generated cases. Unknown scalars are `NULL`, not empty strings. Dashboard business ids are assigned in Python after structured generation (`SYN-000001`, `DX-SYN000001-001`, and the other prefixes in `app/utils/identifiers.py`). Canonical concepts on a case must already exist in local reference tables. Numeric vital and laboratory values are synthetic and labeled `synthetic_model_generated`; they are not MIMIC empirical draws.

### What OpenAI is and is not used for

OpenAI is **optional** and is used only to **word** admission narrative text (chief complaint, HPI, note) from **already selected** structured facts (age, sex, diagnosis name, symptom names, medication names, and a template chief-complaint seed). See [OpenAI usage](#14-openai-usage).

OpenAI is **not** used to choose or invent diagnoses, medications, laboratory codes, units, clinical rules, error families, or answer keys. Raw MIMIC and other patient-source rows are never sent.

`freeze-validation-batch` hardcodes `use_openai=False`, so the committed `RESIDENT_VALIDATION_V1` freeze used template narrative only.

### Clinical validation

Machine validation ≠ clinical validation. Cases remain **machine-validated synthetic resident-review cases pending clinician validation** until humans complete review.

---

## 2. Quick start

Shortest path if Git, Python 3.12+, Docker, and (for labs) a Regenstrief LOINC account are already available.

**macOS/Linux**

```bash
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
# Edit .env: set LOINC_USERNAME and LOINC_PASSWORD for lab import.
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator validate-cases --case-id SYN-000001
```

**Windows PowerShell**

```powershell
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
# Edit .env: set LOINC_USERNAME and LOINC_PASSWORD for lab import.
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator validate-cases --case-id SYN-000001
```

To **use the committed resident-review files** without regenerating: give reviewers [`data/validation/resident_validation_cases.json`](data/validation/resident_validation_cases.json) and the empty worksheet. Do not send the investigator key. Details: [How to give cases to residents](#18-how-to-give-cases-to-residents).

To **rebuild the frozen batch in a local database** (after bootstrap):

```bash
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

`freeze-validation-batch` generates, validates, and freezes internally. A prior `validate-cases` run is not a prerequisite. See [Resident-validation workflow](#16-resident-validation-workflow).

---

## 3. Architecture and repository layout

```text
Official terminology sources
        ↓
Local reference tables (ref_*)
        ↓
Clinical rules (enabled only with DailyMed / RxClass evidence)
        ↓
Case generation (local ref_* only)
        ↓
Machine validation (structural / terminology / hard rules / medication plan)
        ↓
Optional error injection (exactly one reconciliation error)
        ↓
Freeze resident-validation batch (immutable VAL-* IDs)
        ↓
Resident export + investigator answer key
```

This matches `app/cli/__init__.py` and `app/services/validation_batch.py`. There is no AccessGUDID, SNOMED, or MIMIC stage in the running pipeline.

| Path | Role |
| --- | --- |
| `app/models` | SQLAlchemy 2 tables (`reference.py`, `cases.py`, `generation.py`) |
| `app/schemas` | Pydantic v2 models matching those tables |
| `app/repositories` | Lookups, upserts by official identifiers, `data_source_registry` seed |
| `app/sources` | HTTP clients: RxNav, LOINC FHIR, UCUM essence XML, NLM ICD-10-CM, NLM conditions, NLM HPO, DailyMed, RxClass |
| `app/services` | Sync, bootstrap, local search, rules, generation, validation, error injection, freeze/export |
| `app/cli` | Typer CLI (`clinical-case-generator`) |
| `app/api` | `GET /reference/medications`, `/labs`, `/diagnoses`, `/symptoms` |
| `app/main.py` | FastAPI app plus `GET /health` |
| `app/openai` | Optional narrative wording after canonical concepts are selected |
| `app/config.py` | Settings from `.env` |
| `app/database.py` | Engine, sessions, `ProvenanceMixin`, `CaseChildMixin` |
| `data/bootstrap` | `manifest.json`, `rule_templates.json`, `scenarios.json` |
| `data/validation` | Frozen batch plan, blinded/investigator exports, [pipeline catalog](data/validation/README.md) |
| `data/exports` | Gitignored local export directory (placeholder `.gitkeep` only) |
| `data/imports`, `data/aggregates`, `data/mimic` | Gitignored placeholders; this pipeline does not read them |
| `alembic/versions` | Migrations |
| `tests` | pytest; HTTP mocked with `httpx.MockTransport` |
| `docker-compose.yml` | Local PostgreSQL 16 |

`CaseGenerationRun.blueprint_id` is the UUID foreign key to `case_blueprints.id`. Optional links to reference rows use `ON DELETE RESTRICT`. Case children use `ON DELETE CASCADE` on `case_id`. Frozen `validation_batch_cases.case_id` uses `ON DELETE RESTRICT`.

Alembic:

- `1c236aeaadc7` — Phase 1 clinical schema (do not rewrite)
- `7b9e4c21d6a0` — `clinical_rules` (revises `1c236aeaadc7`)
- `c3f8a91b2e47` — `validation_batch_cases` (revises `7b9e4c21d6a0`; current head)

---

## 4. Prerequisites

| Requirement | Detail |
| --- | --- |
| Git | To clone the repository |
| Python | **3.12 or newer** (`requires-python = ">=3.12"` in `pyproject.toml`; Ruff/mypy target 3.12) |
| PostgreSQL | **16**, via the provided Compose file (`image: postgres:16`) or an equivalent local server |
| Docker Engine + Compose v2 | For the documented `docker compose` database |
| Regenstrief LOINC account | **Required** to import labs (`sync-loinc` and bootstrap lab rows) |
| OpenAI API key | **Optional**; narrative wording only |
| Network access | Official source hosts listed in [Reference terminology](#9-reference-terminology) |

**Required vs optional credentials**

| Credential | Required? |
| --- | --- |
| PostgreSQL (Compose defaults or `DATABASE_URL`) | Required to run CLI commands that use the database |
| `LOINC_USERNAME` / `LOINC_PASSWORD` | Required for LOINC. Empty values raise `SourceNotConfigured`. Bootstrap **skips** lab requests and continues; `sync-loinc` **exits 2**. Generation that needs labs then fails resolution. |
| `OPENAI_API_KEY` | Optional. Empty → template narrative. |
| `SNOMED_BASE_URL` / `SNOMED_API_TOKEN` | Unused. No SNOMED client. |
| `MIMIC_LOCAL_PATH` | Unused. No MIMIC reader. |

There is no resident-review web UI in this repository.

---

## 5. Clone and initial setup

Repository URL from `git remote`: `https://github.com/piaattufts/clinical-case-generator`.

### 1. Clone

**macOS/Linux** and **Windows PowerShell** (same):

```bash
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
```

### 2. Create and activate a virtual environment

The package is installed **editable** with development extras (`pytest`, `ruff`, `mypy`).

**macOS/Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation (`running scripts is disabled`), for this process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Confirm the CLI is on `PATH` (venv must be active):

```bash
clinical-case-generator --help
```

You should see commands including `db-init`, `sync-rxnorm`, `sync-loinc`, `sync-ucum`, `sync-icd10`, `reference-search`, `bootstrap-reference-data`, `generate-synthetic-cases`, `validate-cases`, `freeze-validation-batch`, and `export-validation-batch`. There is **no** `sync-all` command.

### 3. Create `.env`

**macOS/Linux**

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

`.env` is gitignored. Fill LOINC fields before lab import. Do not commit credentials.

---

## 6. Environment configuration

Settings are defined in `app/config.py` (`pydantic-settings`, `env_file=".env"`, `extra="ignore"`). Missing values fall back to empty strings or the local database URL.

| Variable | Required? | Purpose | Example / default |
| --- | --- | --- | --- |
| `DATABASE_URL` | Yes, for DB-backed commands | SQLAlchemy URL used by the app and Alembic (`alembic/env.py` copies it; `alembic.ini` has an empty `sqlalchemy.url`) | `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `OPENAI_API_KEY` | No | If non-empty, `assemble_narrative` may call OpenAI. If empty, it returns `None` and generation uses a template. | empty in `.env.example` |
| `OPENAI_MODEL` | No | Model name passed to `client.responses.parse(...)` | `gpt-5` |
| `LOINC_USERNAME` | For LOINC | HTTP Basic user for `https://fhir.loinc.org` | empty |
| `LOINC_PASSWORD` | For LOINC | HTTP Basic password | empty |
| `SNOMED_BASE_URL` | Unused | Loaded into settings only. No client reads it. | empty |
| `SNOMED_API_TOKEN` | Unused | Loaded into settings only. No client reads it. | empty |
| `MIMIC_LOCAL_PATH` | Unused | Loaded into settings only. No MIMIC files are read. | empty |

`.env.example` comment on LOINC: empty values raise `SourceNotConfigured`; there is no generated fallback.

Compose database user/password/name (`postgres` / `postgres` / `clinical_cases` on port `5432`) match that default URL. They are local development values, not production secrets.

---

## 7. Start PostgreSQL

`docker-compose.yml` defines one service:

| Item | Value |
| --- | --- |
| Service name | `postgres` |
| Image | `postgres:16` |
| Database | `clinical_cases` |
| User / password | `postgres` / `postgres` |
| Host port | `5432` |
| Volume | named volume `clinical_cases_pg` |
| Healthcheck | `pg_isready -U postgres -d clinical_cases` |

**macOS/Linux** and **Windows PowerShell**:

```bash
docker compose up -d
```

### Confirm it is running

```bash
docker compose ps
docker compose exec postgres pg_isready -U postgres -d clinical_cases
```

`pg_isready` should exit 0 and report that the server is accepting connections.

### Stop (data kept)

```bash
docker compose stop
```

### Start again

```bash
docker compose start
```

or `docker compose up -d`.

### Restart

```bash
docker compose restart postgres
```

### Reset the development database (destructive)

This **deletes** the named volume `clinical_cases_pg` (all tables, reference rows, generated cases, and freeze rows in that Docker database).

```bash
docker compose down -v
```

Then `docker compose up -d` and `clinical-case-generator db-init` again. Committed files under `data/validation/` are not deleted by this command.

`docker compose down` **without** `-v` stops containers and keeps the volume.

---

## 8. Initialize the database

```bash
clinical-case-generator db-init
```

What it does (`app/cli/__init__.py`):

1. `alembic upgrade head` using `alembic.ini` (URL from application settings).
2. `seed_data_source_registry(session)` — inserts the eight `data_source_registry` metadata rows if missing (`on_conflict_do_nothing` on `source_code`). Existing rows are unchanged.

It does **not** load RxNorm, LOINC, diagnoses, or other clinical concepts.

Printed message (exact template):

```text
Schema is at Alembic head. DataSourceRegistry metadata rows inserted this call: <n>. No clinical reference rows were loaded.
```

First run typically inserts `8`. Later runs insert `0`.

### Verify

1. The command exits 0 and prints the message above.
2. Optional SQL (Compose credentials):

```bash
docker compose exec postgres psql -U postgres -d clinical_cases -c "SELECT source_code, enabled, sync_status, records_imported FROM data_source_registry ORDER BY source_code;"
```

Expected source codes: `ACCESS_GUDID`, `DAILYMED`, `ICD10CM`, `LOINC`, `MIMIC_IV`, `RXNORM`, `SNOMED_CT`, `UCUM`.

3. Optional Alembic:

```bash
alembic current
```

Head revision is `c3f8a91b2e47`.

---

## 9. Reference terminology

Official base URLs are in `app/sources/http.py` (`SOURCE_BASE_URLS`) and the matching client modules.

| Source | Status | Used for | Official URL / notes |
| --- | --- | --- | --- |
| RxNorm | **Implemented** (public) | Medications (`ref_medications`) | `https://rxnav.nlm.nih.gov/REST` |
| DailyMed | **Implemented** (public) | SPL labels (`ref_drug_labels`); rule evidence | `https://dailymed.nlm.nih.gov/dailymed/services/v2` |
| LOINC | **Implemented, credential-dependent** | Labs (`ref_lab_tests`) | `https://fhir.loinc.org`. Search valueset `http://loinc.org?fhir_vs`. Only official term codes matching `^\d{1,5}-\d$` are stored as labs. Parts (`LP`), answers (`LA`), and groups (`LG`) are excluded. |
| UCUM | **Implemented** (public file) | Units (`ref_units`) | `https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml`. Conversion factors are copied from the file, never invented. Composed units such as `kg` keep a null factor when the essence file does not supply one. |
| ICD-10-CM | **Implemented** (public) | Diagnoses (`ref_diagnoses`) | `https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search` |
| NLM conditions | **Implemented** (public) | Symptom names during bootstrap | `https://clinicaltables.nlm.nih.gov/api/conditions/v3/search` |
| NLM HPO | **Implemented** (public) | Symptom fallback if conditions token-match fails | `https://clinicaltables.nlm.nih.gov/api/hpo/v3/search`. HPO `HP:` ids are source metadata/synonyms, **not** written to `snomed_code`. |
| RxClass | **Implemented** (public) | Rule evidence when DailyMed needles do not match | `https://rxnav.nlm.nih.gov/REST/rxclass` |
| SNOMED CT | **Registered, not implemented** | Registry row only (`enabled=False`, `sync_status=not_configured`) | No client. `SNOMED_*` env vars are unused. |
| AccessGUDID | **Registered, not implemented** | Registry row only (`enabled=True` in metadata, `never_synced`) | No client, no CLI sync. |
| MIMIC-IV | **Registered, disabled, not implemented** | Registry row only | No reader. `MIMIC_LOCAL_PATH` unused. Raw rows must never be stored as reference concepts and are never sent to OpenAI. |

HTTP helpers use User-Agent `clinical-case-generator/0.1.0 (terminology-sync; no-patient-data)` and retry on 429/502/503/504 (two retries). This is not an OpenAI call and does not transmit patient rows.

---

## 10. Bootstrap reference data

```bash
clinical-case-generator bootstrap-reference-data
```

Optional: `--manifest PATH` (default `data/bootstrap/manifest.json`).

This is a **bounded** import of names listed in the manifest, not a full vocabulary download.

### What `data/bootstrap/manifest.json` contains

Version 2. Keys are lists of **human-readable search strings**, not fabricated codes:

- `medications`, `diagnoses`, `symptoms`, `labs`, `units`

Empty strings are skipped.

Related files (not passed as CLI flags except rules via bootstrap internals):

- `data/bootstrap/scenarios.json` — generation families (used at generate/freeze time)
- `data/bootstrap/rule_templates.json` — curated rules (enabled during bootstrap)

### How names are resolved

`app/services/bootstrap.py`:

1. **Medications** — RxNav name search; combination products (`name / name`, TTY `MIN`, or more than one related ingredient) are not selected unless the request itself is a combination.
2. **Diagnoses** — NLM ICD-10-CM search; stored description is the official text; `snomed_code` stays null.
3. **Symptoms** — NLM conditions token match; if that fails, NLM HPO. `snomed_code` is not filled with `HP:` ids.
4. **Units** — official UCUM essence XML search / compose.
5. **Labs** — LOINC FHIR search with ranking (prefer serum/plasma/blood term codes). Missing LOINC credentials: each lab request is **skipped** with `SourceNotConfigured`, registry marked `not_configured`, and bootstrap **continues**.
6. **Labels** — DailyMed SPL XML for resolved RXCUIs.
7. **Rules** — `enable_rules_from_templates` (see [Clinical rules](#12-clinical-rules)).
8. Registry `records_imported` counts are refreshed.

### Provenance

Upserted rows get `source_system`, `source_version` when the source supplied one, and timezone-aware `retrieved_at` (`app/utils/provenance.py`). ICD-10-CM and DailyMed APIs often do not supply a version string; version may be null.

### Unresolved vs skipped

JSON printed by the CLI (`upserted`, `unresolved`, `skipped`, `rules_enabled`):

- `unresolved` — source was queried; no acceptable concept (or similar).
- `skipped` — not attempted; currently used for labs when LOINC is not configured.
- A second run **upserts** and does not duplicate canonical identifiers (unique RXCUI, LOINC, UCUM, ICD-10-CM, rule_code, label set_id).

### Verify

```bash
clinical-case-generator reference-search medications --query lisinopril
clinical-case-generator reference-search labs --query potassium
clinical-case-generator reference-search diagnoses --query "heart failure"
clinical-case-generator reference-search symptoms --query dyspnea
```

Each prints JSON with `kind`, `query`, `total`, `limit`, `offset`, `items` (row UUIDs), and `codes` (RXCUI / LOINC / ICD-10-CM / `snomed_code`, which may be `null` for symptoms).

If labs were skipped, `labs` search `total` stays `0` until LOINC credentials are set and bootstrap (or `sync-loinc`) is run.

---

## 11. Individual terminology sync commands

These call official APIs or the UCUM file and upsert what they return. They are **not** a full import. Limit is 1–100 (default 20). Exit code **2** on `ValueError` or `SourceNotConfigured`.

There is no `sync-dailymed`, `sync-snomed`, `sync-gudid`, or `sync-all` command. DailyMed/RxClass/HPO/conditions run as part of bootstrap.

### `sync-rxnorm`

**Purpose.** Upsert RxNorm concepts by RXCUI from NLM RxNav.

**Syntax.** `--name` and/or `--rxcui` required (at least one non-empty). `--limit` default 20.

**Examples**

```bash
clinical-case-generator sync-rxnorm --name lisinopril
clinical-case-generator sync-rxnorm --rxcui 1806884
```

(`1806884` is the RXCUI stored for lisinopril in the committed `RESIDENT_VALIDATION_V1` freeze, not a code invented by this repo.)

Running with neither selector prints: `Provide a name or RXCUI. Full RxNorm import is not run by default.` and exits 2.

**Expected result.** `RXNORM upserted N row(s): <rxcui>, ...` (or `(none)`).

### `sync-loinc`

**Purpose.** Upsert official LOINC **term** codes from the FHIR Terminology Service. Requires credentials.

**Syntax.** `--query` / `-q` or `--code` required. `--limit` default 20.

**Examples**

```bash
clinical-case-generator sync-loinc --query potassium
clinical-case-generator sync-loinc --code 2823-3
```

**Expected result.** `LOINC upserted N row(s): ...`. Missing credentials: `LOINC is not configured. Missing LOINC_USERNAME, LOINC_PASSWORD. No generated fallback is used.`

### `sync-ucum`

**Purpose.** Import units from official UCUM essence XML. Conversion factors are never invented.

**Syntax.** `--query` / `-q`, `--code`, or `--all` required.

**Examples**

```bash
clinical-case-generator sync-ucum --query gram
clinical-case-generator sync-ucum --all
```

**Expected result.** `UCUM upserted N row(s): ...`. `--all` imports every unit parsed from the essence file (not limited to `--limit`). Search without `--all` applies `--limit`.

### `sync-icd10`

**Purpose.** Store ICD-10-CM codes and the **exact official description**. No model-generated codes.

**Syntax.** `--query` / `-q` or `--code` required.

**Examples**

```bash
clinical-case-generator sync-icd10 --query "heart failure"
clinical-case-generator sync-icd10 --code I50.20
```

**Expected result.** `ICD10CM upserted N row(s): ...`.

### `reference-search`

**Purpose.** Search **locally stored** rows. Does not call terminology APIs or OpenAI.

**Syntax.** Argument `kind` is required: `medications`, `labs`, `diagnoses`, or `symptoms`. `--query` / `-q` default `""`. `--limit` default 20 (1–100). `--offset` default 0.

**Example**

```bash
clinical-case-generator reference-search medications --query lisinopril --limit 20 --offset 0
```

Unknown kind: `kind must be medications, labs, diagnoses, or symptoms.` (exit 2).

**Expected result.** Compact JSON (`separators=(",", ":")`) with `items` (UUIDs) and `codes`.

---

## 12. Clinical rules

**Where they live**

- Templates: `data/bootstrap/rule_templates.json`
- Database: `clinical_rules` (`app/models/reference.py` `ClinicalRule`)
- Enablement: `app/services/rules.py` `enable_rules_from_templates` (called from bootstrap)
- Evaluation: `evaluate_rules` / `hard_violations`

**IF/THEN structure**

Each template has `rule_code`, `rule_type`, `severity` (`hard` or `soft`; other values stored as `soft`), medication/diagnosis/lab **names** (resolved against local `ref_*`), `evidence_needles`, optional `evidence_mode` (`all` default, or `any`), and `constraint.action`:

| Action | Meaning when enabled |
| --- | --- |
| `prohibit_coadministration` | Snapshot must not contain both `input_rxcui` and `related_rxcui` |
| `require_lab` | If the medication RXCUI is present, `input_loinc_code` must be present |
| `allow_with_diagnosis` | If the medication RXCUI is present, `input_icd10cm_code` must be present |

**Provenance vs lookup**

Terminology lookup **alone does not enable** a rule. Enablement requires DailyMed label text and/or RxClass class names matching the needles, plus the resolved identifiers the action needs. Until then the row can be stored with `enabled=false` and `source_system` null.

Current templates (all enabled in the committed freeze after evidence attached):

| Rule | Type | Severity | Evidence in freeze |
| --- | --- | --- | --- |
| `NO_DUAL_ORAL_ANTICOAGULANT` | medication_incompatibility | hard | DailyMed |
| `WARFARIN_INR_MONITORING` | monitoring_dependency | hard | DailyMed INR language **or** “prothrombin” (`evidence_mode: any`) plus LOINC INR |
| `FUROSEMIDE_HF_INDICATION` | medication_diagnosis_allow | soft | RxClass class matching edema/heart-failure needles |

**How generation uses them**

Before persist, generation evaluates **hard** violations on the planned ICD + RXCUI + LOINC snapshot and aborts on a hit. Validation’s `clinical` layer fails the case on hard violations; soft hits are **warnings** and do not fail the layer.

No LLM writes or enables rules.

---

## 13. Generate synthetic cases

```bash
clinical-case-generator generate-synthetic-cases [OPTIONS]
```

Implemented flags (`generate-synthetic-cases --help`):

| Flag | Default | Notes |
| --- | --- | --- |
| `--count` | `3` | Integer 1–100 |
| `--seed` | `42` | Integer; combined with sequence and scenario into the case seed |
| `--start-index` | `1` | Integer ≥ 1; becomes `SYN-{index:06d}` |
| `--scenario` | omitted | Must match a `code` in `data/bootstrap/scenarios.json`. If omitted, the **first** scenario in that file is used (`HF_INPATIENT`). |
| `--inject-error` / `--no-inject-error` | `--inject-error` | Exactly one reconciliation error after a clean, validated case |

There is **no** `--use-openai` flag. The service default is `use_openai=True`; OpenAI is still skipped when the key is empty. Freeze is the path that forces `use_openai=False`.

Unknown `--scenario` raises `unknown scenario '...'` (exit 2).

### Examples

Three cases, default scenario, with injection:

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

Creates/replaces `SYN-000001`, `SYN-000002`, `SYN-000003` unless those underlying rows are frozen.

Without injection:

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --no-inject-error
```

One atrial-fibrillation family case at sequence 10:

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 42 --start-index 10 --scenario AF_ANTICOAGULATION --no-inject-error
```

Scenario codes in `data/bootstrap/scenarios.json`: `HF_INPATIENT`, `AF_ANTICOAGULATION`, `HTN_INPATIENT`, `T2DM_INPATIENT`, `CAP_INPATIENT`.

### Lifecycle

```text
Load scenario
  → resolve diagnosis, symptoms, meds, stop meds, labs from local ref_*
  → hard-rule check
  → persist clean case (IDs, vitals, labs, plans)
  → optional OpenAI wording of already-selected names (or template)
  → validate clean case (must pass)
  → optional inject exactly one error; write answer key in Python
  → validate again (expects exactly one plan discrepancy if injected)
```

Case seed: `f"{seed}:{sequence}:{scenario.code}"` (Python `random.Random`). Example: `42:1:HF_INPATIENT`.

If `SYN-000001` already exists and is **not** frozen, it is deleted and regenerated. If it is frozen as a `VAL-*` assignment, `generate_one_case` raises `FrozenValidationCaseError` (`Frozen validation case VAL-… cannot be overwritten: underlying case SYN-… is frozen`). The `generate-synthetic-cases` CLI does not catch that exception class (the freeze CLI does), so the process exits with a traceback instead of the usual exit code 2.

### Fields that are synthetic / model-generated

- Demographics in the scenario age band; sex `Female`/`Male`; weight; BP/HR/RR/SpO2 ranges; hospital day 2–6
- Laboratory numeric values (`NUMERIC_ORIGIN = "synthetic_model_generated"`)
- Dose = RxNorm `strength` when present, else `"1 tablet"`; clean frequency default `"once daily"`
- Narrative: template, or OpenAI wording of the same facts
- `generation_source` = `clinical-case-generator`; `source_type` on the case = `synthetic`

Not synthetic: RXCUI, LOINC, ICD-10-CM, UCUM codes (must already exist in `ref_*`).

### Expected CLI JSON

A list of objects with `case_id_code`, `seed`, `clean_passed`, `narrative_source` (`template` or `openai`), `error_category`, `error_rxcui`, `validation_passed`. Compact JSON (no extra spaces).

If local labs/meds/diagnoses are missing: `Could not resolve ... from an authoritative source` (exit 2).

---

## 14. OpenAI usage

**Only module:** `app/openai/narrative.py` (`assemble_narrative`). Generation calls it after concept selection. `tests/test_cli_phase2.py` asserts that `app/sources`, `app/services`, `app/api`, and `app/cli` do not import the `openai` package (`from openai import OpenAI` lives inside `assemble_narrative`).

**When the key is absent.** `openai_api_key.strip() == ""` → return `None` immediately. Generation uses `_template_narrative` and `narrative_source="template"`.

**When the key is present.** Lazy-import `OpenAI`. Request:

- `client.responses.parse`
- `model=settings.openai_model` (default `gpt-5`)
- `store=False`
- system instructions: write admission narrative from structured facts only; do not add diagnoses, medications, labs, units, doses, frequencies, procedures, devices, or identifiers that are not listed; do not invent reference ranges or label facts
- user content: `str({age, sex, diagnosis, symptoms, medications, chief_complaint_seed})`
- `text_format=CaseNarrative` (`chief_complaint`, `hpi`, `note_text`)

**On any exception** (including missing SDK or HTTP failure): return `None` → template fallback. There is no retry UI and no raised OpenAI error on the generate CLI path.

**After a successful parse.** Generation rejects the narrative and falls back to template if none of the allowed names appear in the text (`_narrative_rejected`).

**Freeze.** `freeze_validation_batch(..., use_openai=False)` so OpenAI is not called for `RESIDENT_VALIDATION_V1` even if a key is set.

**What OpenAI cannot do here:** invent or choose diagnoses, RXCUIs, LOINC, units, rules, error category, or answer-key content. Raw MIMIC rows are not in the payload.

This documents what the code sends. It is not a broader privacy certification.

---

## 15. Validate generated cases

```bash
clinical-case-generator validate-cases
clinical-case-generator validate-cases --case-id SYN-000001
```

`--case-id` is a `SYN-######` business id (help text: “Validate one SYN-000001 case id.”).

Without `--case-id`, every row in `clinical_cases` is validated, ordered by `case_id_code`. If the table is empty, the command prints `[]` and exits 0.

If `--case-id` is missing in the database: `case validation failed: case SYN-... was not found` (exit 2).

The first failing case raises `CaseValidationError` and stops the rest (exit 2). On success, prints a JSON list of reports:

- `case_id_code`, `passed`, `errors`
- `layers`: `structural`, `terminology`, `clinical`, `medication_plan` (each with `passed`, `errors`, `warnings`)
- `rules`: enabled-rule hits (`rule_code`, `severity`, `message`)

**What it checks** (`app/services/validation.py`)

| Layer | Passes when |
| --- | --- |
| structural | Case id matches `SYN-######`; medication context/status and plan decisions are in allowed sets; at least one diagnosis |
| terminology | Meds/diagnoses/labs link to `ref_*` with provenance; units are stored UCUM or LOINC example units; invented `fake_` / `invented_` ids rejected (`TEST_` fixtures allowed in tests) |
| clinical | No **hard** rule violations (soft → warnings) |
| medication_plan | Clean case: zero discharge/plan discrepancies and no answer key. Error-bearing (`clinical_cases.clean_case` is false): exactly one discrepancy, one answer key, one `is_error_target` plan |

**What it does not establish:** clinical realism, guideline completeness, or resident-review quality. It does not call external terminology APIs on ordinary reads.

---

## 16. Resident-validation workflow

This is how the **fixed resident-review set** is created. Ad-hoc `generate-synthetic-cases` (sequences 1+) is a separate development path.

### Prerequisites

1. Database initialized ([§8](#8-initialize-the-database)).
2. `bootstrap-reference-data` completed with LOINC credentials so every scenario lab query resolves.
3. Leave `OPENAI_API_KEY` empty if you want template narrative matching the committed freeze. Freeze does not call OpenAI regardless.

`validate-cases` is **not** required before freeze. Freeze generates each assignment, validates the clean case, injects if planned, validates again, then writes `validation_batch_cases`.

Recommended operator order:

```bash
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

Optional inspection of persisted `SYN-*` rows (including freeze sequences 101–124):

```bash
clinical-case-generator validate-cases
clinical-case-generator validate-cases --case-id SYN-000101
```

### `batch_plan.json`

Default plan: `data/validation/batch_plan.json` (`--plan` overrides).

Controls:

- `batch_code` (committed value `RESIDENT_VALIDATION_V1`)
- `master_seed` (`20260922`)
- `cases[]`: `validation_case_id` (`VAL-###`), `scenario`, `inject_error`, `error_category`, `sequence`

Case seed: `{master_seed}:{sequence}:{scenario}`. Sequences **101–124** avoid smoke ids `SYN-000001`–`SYN-000003`.

### Immutable `VAL-*` IDs

After a successful freeze, `validation_batch_cases.immutable` is true (default). A second freeze **reuses** matching VAL IDs (same seed and scenario) and will not overwrite them. If an existing frozen row disagrees with the plan, the CLI raises:

```text
Frozen validation case VAL-00N cannot be overwritten: existing frozen assignment does not match this plan
```

Rejected assignments (generation/audit failure) appear in the `rejected` list and are not frozen. The committed freeze had zero rejections.

### Current batch `RESIDENT_VALIDATION_V1`

| Item | Value |
| --- | --- |
| Public IDs | `VAL-001`–`VAL-024` |
| Internal IDs | `SYN-000101`–`SYN-000124` |
| Families | `HF_INPATIENT` (5), `AF_ANTICOAGULATION` (5), `HTN_INPATIENT` (5), `T2DM_INPATIENT` (5), `CAP_INPATIENT` (4) |
| Mix | 5 clean controls, 19 error-bearing (exactly one planted reconciliation error each) |
| Error families used | `omission`, `dose_mismatch`, `frequency_mismatch`, `incorrect_continuation` |
| Dataset status | `machine-validated synthetic resident-review cases pending clinician validation` |

**How controls vs planted errors work (do not tell residents which is which):**

- **Clean control** (`inject_error: false`): discharge list matches the correct plan. A held “stop” medication (when the scenario has one) stays off the discharge list.
- **Error-bearing**: after the clean case passes validation, Python plants one of: omit a continue-med from discharge; change discharge dose; flip frequency `once daily` ↔ `twice daily`; or copy a held stop-med onto discharge (`incorrect_continuation`). The answer key is written by that injector.

Residents should review every case as if the discharge list might be wrong. Investigators score against [`data/validation/investigator_answer_key.md`](data/validation/investigator_answer_key.md) and the catalog in [`data/validation/README.md`](data/validation/README.md)—not in resident packets.

### Freeze CLI output

```text
{"batch_code":"RESIDENT_VALIDATION_V1","master_seed":20260922,"frozen":["VAL-001",...],"reused":[...],"rejected":[...]}
```

### Export CLI

```bash
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

`--output-dir` defaults to `data/validation/`. Requires frozen rows **in the local database**. If none: `no frozen cases for batch RESIDENT_VALIDATION_V1` (exit 2).

Export regenerates blinded payloads, writes files listed in [§17](#17-resident-validation-output-files), and runs a leak audit (fails `audit_passed` if resident JSON contains markers such as `syn-000`, `answer_key`, `is_clean_control`, `rxcui:`, or `TEST_` identifier values).

Printed paths: `resident_path`, `investigator_path`, `manifest_path`, `coverage_path`, `worksheet_path`, `schema_path`, plus `audit_passed` / `audit_errors`.

---

## 17. Resident-validation output files

Directory: `data/validation/`. Tracked study artifacts live here (`data/exports/**` is gitignored).

| File | Purpose | Who should see it | Blinded? | Contains answer key? | Give to residents? |
| --- | --- | --- | --- | --- | --- |
| [`resident_validation_cases.json`](data/validation/resident_validation_cases.json) | Dashboard-shaped cases (`VAL-*` ids, nested `ClinicalCase`, child arrays). Omits `CaseAnswerKey`. Titles use `VAL-*`. | Residents | Yes | No | **Yes — this is the case file** |
| [`resident_review_worksheet.csv`](data/validation/resident_review_worksheet.csv) | Empty capture rows, one per VAL ID | Residents / study staff | Yes (no answers) | No | **Yes** |
| [`resident_review_schema.json`](data/validation/resident_review_schema.json) | Worksheet field definitions (ratings 1–5, identified error type, comments, …) | Study staff; optional for residents | Yes | No | Optional |
| [`investigator_answer_key.json`](data/validation/investigator_answer_key.json) | Seeds, `SYN-*`, error category, affected RXCUI, clean expected state, snapshots | Investigators | No | **Yes** | **No** |
| [`investigator_answer_key.md`](data/validation/investigator_answer_key.md) | Human-readable key | Investigators | No | **Yes** | **No** |
| [`validation_manifest.json`](data/validation/validation_manifest.json) | Freeze metadata, source versions, control status | Investigators | No | Control/error status | **No** |
| [`batch_plan.json`](data/validation/batch_plan.json) | Planned VAL IDs, scenarios, inject flags, error categories | Operators / investigators | No | Planned errors | **No** |
| [`coverage_report.md`](data/validation/coverage_report.md) | Counts by scenario/error/terminology | Investigators | No | Mix summary | **No** |
| [`scenario_coverage_matrix.md`](data/validation/scenario_coverage_matrix.md) | Resolved meds/labs/diagnoses per family | Investigators | No | Not per-case answers | **No** |
| [`README.md`](data/validation/README.md) | Full pipeline + **per-case planted-error catalog** | Investigators | No | **Yes (catalog)** | **No** |

Resident vs investigator split is enforced in export code (`LEAK_MARKERS` in `app/services/validation_batch.py`). Do not “fix” blinding by editing resident JSON to add codes or keys.

---

## 18. How to give cases to residents

This repository **does not contain a resident review UI**, dashboard importer, or scoring app. The HTTP API only searches local reference rows and serves `/health`. Delivery is a file handoff into whatever review process the study already uses.

1. **Send / import for review:** [`data/validation/resident_validation_cases.json`](data/validation/resident_validation_cases.json). Each element has `case_id_code` (`VAL-001` …) and dashboard-style arrays (`CaseMedication`, `CaseLab`, `CaseDiagnosis`, …).
2. **Keep investigator-only:** answer keys, `batch_plan.json`, `validation_manifest.json`, coverage files, and [`data/validation/README.md`](data/validation/README.md).
3. **Capture responses** in [`resident_review_worksheet.csv`](data/validation/resident_review_worksheet.csv) (or an equivalent form that uses [`resident_review_schema.json`](data/validation/resident_review_schema.json)). Do not pre-fill ratings.
4. **Worksheet ↔ cases:** `validation_case_id` on each CSV row matches `case_id_code` in the resident JSON.
5. **“Clinically validated” in this project** means a clinician/resident review concluded the case is acceptable for the study protocol. Until that happens, use the dataset-status sentence: machine-validated synthetic resident-review cases pending clinician validation.
6. **Machine validation is not clinical validity.** Passing `validate-cases` / freeze audit does not certify realism of formulations, units, or narratives.

Do not tell residents which cases are clean controls.

---

## 19. Reproducing the frozen validation batch

**Study source of truth:** the committed JSON/Markdown under `data/validation/`, not a later live API run.

Why live bootstrap can differ: RxNav and LOINC ranking can change. The same string (`lisinopril`, `hemoglobin`, `edema`) may resolve to a different official concept. Seeds do not freeze upstream search order.

**Reprint without mutating VAL IDs** (database already has this freeze):

```bash
clinical-case-generator freeze-validation-batch
# reused should list VAL-001 … VAL-024; rejected should be []
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

Compare export files to git. If they match, the study dataset is unchanged.

**Empty database rebuild** (may **not** bit-match if APIs drifted):

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

If ranking differs, keep the committed files as the dataset. Start a new `batch_code` and new VAL IDs for any replacement study set. Do not hand-edit frozen JSON to substitute a “more typical” tablet RXCUI or conventional US lab unit the source did not return.

Freeze-time identity, seeds, RXCUIs, LOINC, and per-case planted errors: [`data/validation/README.md`](data/validation/README.md).

Generator version: `0.1.0` (`app/__init__.py` / `pyproject.toml`).

---

## 20. API

Start the process (venv active). `uvicorn` is a project dependency. Host and port below match the command used in this repository’s documentation; they are not FastAPI defaults.

**macOS/Linux** and **Windows PowerShell**:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

App: `app.main:app` (`title="Clinical Case Generator"`, `version="0.1.0"`). FastAPI also serves interactive docs at `http://127.0.0.1:8765/docs` (framework default, not a custom route).

No route calls OpenAI or external terminology services. Reference routes read PostgreSQL via `app.api.deps.get_session`.

### `GET /health`

Process liveness. **Does not** check the database.

**macOS/Linux**

```bash
curl -s http://127.0.0.1:8765/health
```

**Windows PowerShell**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8765/health
```

Response: `{"status":"ok"}` (HTTP 200).

### `GET /reference/medications` | `/labs` | `/diagnoses` | `/symptoms`

Query parameters (`app/api/reference.py`):

| Name | Type | Default | Constraints |
| --- | --- | --- | --- |
| `query` | string | `""` | Local substring search |
| `limit` | int | `20` | 1–100 |
| `offset` | int | `0` | ≥ 0 |

**macOS/Linux**

```bash
curl -s "http://127.0.0.1:8765/reference/medications?query=lisinopril&limit=20&offset=0"
```

**Windows PowerShell**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8765/reference/medications?query=lisinopril&limit=20&offset=0"
```

Response shape (`MedicationSearchPage` and siblings): `items` (full reference objects), `total`, `limit`, `offset`, `query`. Medication items include `rxcui`, names, provenance fields, and `id`. Lab items include `loinc_code`. Diagnosis items include `icd10cm_code` / `snomed_code`. Symptom items include `preferred_name` and possibly null `snomed_code`.

These endpoints require a reachable `DATABASE_URL`. `/health` does not.

---

## 21. Testing and code quality

From the repo root, venv active, PostgreSQL reachable at `DATABASE_URL` for the full suite:

```bash
pytest
ruff check .
mypy
```

Configuration:

- pytest: `testpaths = ["tests"]`, `asyncio_mode = auto`
- ruff: `target-version = py312`, `line-length = 100`, lint `E,F,I,UP,B,W`
- mypy: `python_version = 3.12`, `strict = true`, `files = ["app", "tests"]`, `exclude = ["alembic/"]`

### PostgreSQL and destructive migrations

`tests/conftest.py` session fixture runs `alembic upgrade head`, then **`downgrade base`**, then `upgrade head` on `DATABASE_URL`. That **drops and recreates** application tables.

Do **not** point `pytest` at a database whose frozen `VAL-*` rows you need to keep, unless you can re-run freeze afterward. `/health` tests do not need the database, but `pytest` with no arguments runs the whole suite, including constraint, sync, bootstrap, generation, API, and freeze tests.

### HTTP

Client tests use `httpx.MockTransport`. They do not use live LOINC credentials. Fixture identifiers use the `TEST_` prefix only. `TEST_` ids must not appear in the resident-validation dataset.

### Before opening a PR

1. Venv active; `ruff check .` and `mypy` clean.
2. PostgreSQL up; understand that `pytest` will migrate `DATABASE_URL` through `base`.
3. `pytest` green.
4. Do not rewrite `alembic/versions/1c236aeaadc7_phase_1_clinical_schema.py`.
5. Do not commit `.env` or credentials.
6. Do not add `TEST_` identifiers to resident exports.
7. Do not claim cases are clinically validated.

---

## 22. Common workflows

Commands below assume the venv is active and `.env` exists. Where the shell differs, both variants are shown.

### A. First-time setup

**macOS/Linux**

```bash
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
# Set LOINC_USERNAME and LOINC_PASSWORD in .env for labs.
docker compose up -d
clinical-case-generator db-init
```

**Windows PowerShell**

```powershell
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
# Set LOINC_USERNAME and LOINC_PASSWORD in .env for labs.
docker compose up -d
clinical-case-generator db-init
```

### B. Refresh terminology

```bash
clinical-case-generator bootstrap-reference-data
```

Optional targeted sync (examples):

```bash
clinical-case-generator sync-rxnorm --name metoprolol
clinical-case-generator sync-loinc --query creatinine
clinical-case-generator sync-ucum --query milligram
clinical-case-generator sync-icd10 --query "atrial fibrillation"
```

### C. Generate three test cases

Requires bootstrap (including labs if the scenario lists labs).

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

Default scenario: `HF_INPATIENT`. IDs: `SYN-000001`–`SYN-000003`.

### D. Generate without injected errors

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --no-inject-error
```

### E. Validate a specific case

```bash
clinical-case-generator validate-cases --case-id SYN-000001
```

### F. Rebuild / export resident validation batch

```bash
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

**Warnings:** VAL IDs are immutable; freeze reuses existing matching rows. Export overwrites files in `data/validation/` (or `--output-dir`). Live APIs may change ranking. `pytest` can wipe the same database. Sequences 101–124; do not generate ad-hoc cases onto those ids if they are frozen.

### G. Run the API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

### H. Run all checks

```bash
pytest
ruff check .
mypy
```

---

## 23. Troubleshooting

### `clinical-case-generator: command not found` (or PowerShell “not recognized”)

**Cause.** Virtualenv not active, or package not installed.  
**Fix.** Activate `.venv` ([§5](#5-clone-and-initial-setup)), then `python -m pip install -e ".[dev]"`. Confirm with `clinical-case-generator --help`.

### Connection refused / database errors talking to port 5432

**Cause.** Postgres not running, wrong port, or `DATABASE_URL` host/user/password mismatch.  
**Fix.** `docker compose up -d` then `docker compose exec postgres pg_isready -U postgres -d clinical_cases`. Confirm `DATABASE_URL` matches Compose (`postgres:postgres@localhost:5432/clinical_cases`) unless you intend a different server.

### Missing `.env`

**Cause.** Settings fall back to defaults (`app/config.py`); LOINC and OpenAI stay empty.  
**Fix.** Copy `.env.example` to `.env`. Alembic still uses `get_settings().database_url`.

### `LOINC is not configured. Missing LOINC_USERNAME, LOINC_PASSWORD. No generated fallback is used.`

**Cause.** `SourceNotConfigured` from `LoincClient`.  
**Fix.** Set both variables in `.env`. `sync-loinc` exits 2. Bootstrap **skips** labs (`skipped` in JSON) and continues. Generation that requires labs then fails resolution.

### `Could not resolve lab request '...' from an authoritative source`

**Cause.** `ReferenceResolutionError` — scenario lab query not in `ref_lab_tests` (often because LOINC was skipped).  
**Fix.** Configure LOINC, re-run `bootstrap-reference-data`, confirm `reference-search labs`.

### Unresolved medication / diagnosis / symptom during bootstrap

**Cause.** Official search returned nothing acceptable (combination filter, token match, ranking).  
**Fix.** Inspect `unresolved` in bootstrap JSON. Do not invent a code. Adjust the **search string** in the manifest only if you still query the official API.

### Duplicate / idempotent bootstrap or `db-init`

**Cause.** Unique identifiers; registry `on_conflict_do_nothing`.  
**Fix.** None required. `db-init` reports `inserted this call: 0`. Bootstrap upserts the same RXCUI/LOINC again.

### Alembic / migration problems

**Cause.** Database not empty of conflicting objects, or URL missing.  
**Fix.** Confirm `alembic current` and `DATABASE_URL`. Do not edit `1c236aeaadc7`. Destructive last resort on **dev Docker only**: `docker compose down -v`, then up and `db-init`.

### OpenAI key missing

**Cause.** Empty `OPENAI_API_KEY`.  
**Fix.** None if template narrative is acceptable. Generate still runs; `narrative_source` is `template`.

### OpenAI request failure

**Cause.** `assemble_narrative` catches all exceptions and returns `None`.  
**Fix.** Generation continues with the template. Check key/model/network if you expected `"openai"` in CLI output.

### `case validation failed: ...`

**Cause.** A validation layer failed; CLI prints the first error and exits 2.  
**Fix.** Read the `layer:` prefix. Clean cases must have zero plan discrepancies; error-bearing cases must have exactly one. Hard dual-anticoagulant or missing INR (when warfarin is selected) fails `clinical`.

### `Frozen validation case VAL-00N cannot be overwritten`

**Cause.** Immutable freeze row; seed/scenario mismatch, or `generate-synthetic-cases` targeting a frozen `SYN-000101`–`SYN-000124`.  
**Fix.** Do not overwrite. Use a new batch/VAL IDs, or reuse via freeze when the plan matches.

### `no frozen cases for batch RESIDENT_VALIDATION_V1`

**Cause.** Export ran before freeze, or pytest/downgrade wiped rows, or wrong database.  
**Fix.** Run `freeze-validation-batch` on this `DATABASE_URL`, or use committed JSON without export.

### Port 5432 or 8765 already in use

**Cause.** Another Postgres or an old uvicorn.  
**Fix.** Stop the other process, or change host port in Compose / `--port` (and `DATABASE_URL` if you change 5432).

### `Provide a name or RXCUI. Full RxNorm import is not run by default.`

**Cause.** `sync-rxnorm` with no `--name` or `--rxcui`. Similar messages exist for LOINC, UCUM, and ICD-10-CM.  
**Fix.** Pass a selector. There is no full-import flag except `sync-ucum --all`.

### pytest wiped my generated cases

**Cause.** Session fixture downgrades to `base`.  
**Fix.** Re-run bootstrap and freeze, or use a separate test database URL.

---

## 24. Data provenance and safety constraints

- **Official-source provenance** on reference rows: `source_system`, `source_version` (nullable if the API omitted it), timezone-aware `retrieved_at`.
- **Canonical identifiers** come only from those sources or from `TEST_` fixtures in tests. No generated RXCUI/LOINC/ICD/UCUM/SNOMED/UDI.
- **Unknown scalars** on cases are `NULL`, not `""`.
- **Synthetic vs empirical:** vitals/labs are RNG draws labeled `synthetic_model_generated`. `ref_clinical_distributions` is unused by this pipeline; `MIMIC_IV_RAW` is rejected by check constraint.
- **MIMIC:** not ingested. Registry documents that raw rows are never stored as concepts and never sent to OpenAI. `MIMIC_LOCAL_PATH` is unused.
- **OpenAI:** optional wording of selected names only; `store=False`; freeze path disables it.
- **Clinician review is required** because official-source ranking can yield atypical formulations (oral solutions, topical gel), SI example units, and oximetry hemoglobin LOINC. In the committed freeze, NLM conditions token-match stored **Anasarca** for an `edema` query and **Chronic fatigue syndrome** for `fatigue`. Software does not certify clinical realism.

---

## 25. Database and schema notes

Models: `app/models/`. Migrations: `alembic/versions/`. Tests list expected table names in `tests/test_database_constraints.py` (`EXPECTED_TABLES`).

| Area | Tables |
| --- | --- |
| Registry | `data_source_registry` (8 metadata rows after `db-init`) |
| `ref_*` | `ref_medications`, `ref_drug_labels`, `ref_diagnoses`, `ref_symptoms`, `ref_lab_tests`, `ref_units`, `ref_vitals`, `ref_procedures`, `ref_devices`, `ref_microbiology`, `ref_clinical_distributions` |
| Rules | `clinical_rules` |
| Cases | `clinical_cases` plus children (`case_presentations`, `case_symptoms`, `case_diagnoses`, `case_labs`, `case_medications`, `case_answer_keys`, …) |
| Generation | `case_blueprints`, `case_generation_runs`, `case_medication_plans` |
| Freeze | `validation_batch_cases` (`VAL-###` unique, `immutable`, snapshots, `ON DELETE RESTRICT` to `clinical_cases`) |

Delete behavior:

- Case children: `ON DELETE CASCADE` from `clinical_cases.id`
- Optional FKs to `ref_*`: `ON DELETE RESTRICT`
- `case_generation_runs.case_id`: `ON DELETE SET NULL`
- `case_generation_runs.blueprint_id`: `ON DELETE RESTRICT`

Internal PK is UUID (`gen_random_uuid()`). Dashboard ids (`SYN-*`, `VAL-*`, `DX-…`) are separate unique strings.

---

## 26. Current limitations

**Implemented**

- PostgreSQL schema and Alembic through `c3f8a91b2e47`
- RxNorm, LOINC (credentialed), UCUM, ICD-10-CM, DailyMed, RxClass, NLM conditions, NLM HPO clients
- Bounded bootstrap, three curated rules, five inpatient scenarios
- Deterministic generation, four reconciliation-error families, four-layer validation
- Freeze/export of blinded `VAL-*` batch
- Local reference search API + `/health`
- Optional OpenAI narrative wording

**Partially implemented**

- SNOMED CT: columns and a disabled registry row exist; **no ingestion**
- AccessGUDID: enabled registry metadata; **no client**
- `ref_clinical_distributions`: table and MIMIC_IV_RAW guard; **no calculator**
- LOINC labs: bootstrap works only with credentials; otherwise skipped
- Error families: only omission, dose mismatch, frequency mismatch, incorrect continuation (the last needs a scenario stop medication)
- Narrative: template always available; OpenAI optional with silent fallback

**Not implemented**

- AccessGUDID or SNOMED CT ingestion
- MIMIC ingestion or aggregate calculation
- Resident review UI / dashboard application
- Full vocabulary import (`sync-all` does not exist)
- Duplicate therapy, missing co-prescription, contraindicated restart, failure-to-restart error families
- A complete clinical-realism guarantee; human review is required
- Using OpenAI as clinical truth, error chooser, or answer-key writer

---

## 27. Licensing

Terminology and dataset content is **not bundled**. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license and access rules. LOINC requires a Regenstrief account. SNOMED CT and MIMIC-IV stay disabled in `data_source_registry` until a future ingestion path exists; setting unused env vars does not load them.
