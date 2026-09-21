# Clinical Case Generator

Phase 1 is the PostgreSQL schema for three kinds of data. It does not sync terminology, generate cases, read MIMIC, or call OpenAI.

## Three data classes

**Authoritative reference data.** RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, and AccessGUDID concepts will live in `ref_*` tables after a later sync. Every real reference row keeps `source_system`, `source_version`, and a timezone-aware `retrieved_at`. Those tables are empty in Phase 1. The application does not invent RxNorm, LOINC, SNOMED, ICD-10-CM, UCUM, or device identifiers.

**Empirical aggregate data.** `ref_clinical_distributions` is for statistics calculated locally from a permitted dataset. Aggregates are not patient rows. Raw MIMIC patient rows, notes, identifiers, and events must never be sent to OpenAI and must never be stored in this table. A check constraint rejects `source_dataset = 'MIMIC_IV_RAW'`. Phase 1 inserts no distribution rows.

**Synthetic patient data.** `clinical_cases` and its child tables will hold generated cases in a later phase. Phase 1 only creates the tables. Unknown scalars are `NULL`, not empty strings. Dashboard business ids (`symptom_id`, `diagnosis_id`, and the other child ids) are unique strings and stay null until Python assigns them after generation. The internal primary key on every table is a UUID named `id`. Child rows point at `clinical_cases.id` through `case_id`.

## Licensing

Terminology and dataset content is not bundled. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license and access rules. SNOMED CT, LOINC, and MIMIC-IV stay disabled in `data_source_registry` until credentials are configured. This repository does not download MIMIC.

## Layout

- `app/models` — SQLAlchemy 2 models
- `app/schemas` — Pydantic v2 models that match the tables
- `app/repositories` — lookups, plus the source-registry metadata seed
- `app/cli` — `db-init` only
- `app/main.py` — `GET /health`
- `app/sources`, `app/services`, `app/openai`, `app/api` — packages reserved for later phases; they do not call external systems

`CaseGenerationRun.blueprint_id` is the UUID foreign key to `case_blueprints.id`. The human blueprint code is the separate string `case_blueprints.blueprint_id`. Optional links to reference rows use `ON DELETE RESTRICT`. Case children use `ON DELETE CASCADE` on `case_id`. A generation run's `case_id` uses `ON DELETE SET NULL`.

Business ids for a later phase use `SYN-000001` for cases and `DX-SYN000001-001`, `SYM-`, `LAB-`, `MED-`, `VIT-`, `PROC-`, and `AK-` for children. `app/utils/identifiers.py` documents that format. Phase 1 does not assign those ids.

## Install

Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Database

PostgreSQL 16. `docker-compose.yml` publishes database `clinical_cases` with the local development user and password from `.env.example`. Those values are not production secrets.

```bash
docker compose up -d
clinical-case-generator db-init
```

`db-init` runs `alembic upgrade head` and ensures eight `data_source_registry` rows exist: `RXNORM`, `DAILYMED`, `LOINC`, `UCUM`, `ICD10CM`, `SNOMED_CT`, `ACCESS_GUDID`, `MIMIC_IV`. Each row has `records_imported = 0`. Public sources are `never_synced` and enabled. `LOINC`, `SNOMED_CT`, and `MIMIC_IV` are `not_configured` and disabled. Running it again does not duplicate those rows and does not load clinical concepts.

Equivalent migration command:

```bash
alembic upgrade head
```

## Environment

See `.env.example`.

| Variable | Phase 1 use |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy URL. Default `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `OPENAI_API_KEY` | Unused. The OpenAI SDK is installed and not called |
| `OPENAI_MODEL` | Unused. Example default `gpt-5` |
| `LOINC_USERNAME`, `LOINC_PASSWORD` | Unused. LOINC stays not configured |
| `SNOMED_BASE_URL`, `SNOMED_API_TOKEN` | Unused. SNOMED CT stays disabled |
| `MIMIC_LOCAL_PATH` | Unused. No MIMIC files are read |

`.env` is for local development and is gitignored.

## API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

`GET /health` returns `{"status": "ok"}`. It does not check the database.

## Checks

```bash
pytest
ruff check .
mypy
```

Constraint tests need the `DATABASE_URL` database. They use `TEST_` identifiers only inside tests.

## Not implemented yet

Phase 1 does not provide these, and there is no command that pretends to:

- Reference sync or source API clients
- OpenAI requests, case generation, blueprints as a workflow, or medication-plan generation
- Error injection, answer-key generation, or blinded review
- Dashboard export
- MIMIC ingestion or aggregate calculation
- Search or case APIs besides `GET /health`

Later phases, in order: terminology access for RxNorm, LOINC, UCUM, and ICD-10-CM plus a reference search API; clean case generation and dashboard export; validation, medication-plan decisions, error injection, and blinded review; DailyMed, AccessGUDID, and optional SNOMED CT; local MIMIC-IV aggregation into `ref_clinical_distributions`.
