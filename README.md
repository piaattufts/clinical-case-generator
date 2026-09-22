# Clinical Case Generator

PostgreSQL schema, official terminology clients, source-backed reference bootstrap, deterministic clinical conditionals, and constrained synthetic case generation. The application does not invent RxNorm, LOINC, SNOMED, ICD-10-CM, UCUM, or device identifiers. Raw MIMIC patient rows, notes, identifiers, and events are never sent to OpenAI.

## Three data classes

**Authoritative reference data.** RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, and AccessGUDID concepts live in `ref_*` tables. Every real reference row keeps `source_system`, `source_version`, and a timezone-aware `retrieved_at`.

Targeted sync and `bootstrap-reference-data` upsert only identifiers returned by official sources. DailyMed labels are stored when an RXCUI is already validated through RxNorm. SNOMED CT stays unpopulated unless credentials are configured; SNOMED fields remain null rather than invented. AccessGUDID and MIMIC ingestion are not part of this pipeline.

**Empirical aggregate data.** `ref_clinical_distributions` is for statistics calculated locally from a permitted dataset. Aggregates are not patient rows. A check constraint rejects `source_dataset = 'MIMIC_IV_RAW'`. This pipeline inserts no distribution rows and does not invent empirical distributions.

**Synthetic patient data.** `clinical_cases` and child tables hold generated cases. Unknown scalars are `NULL`, not empty strings. Dashboard business ids are assigned in Python after structured generation (`SYN-000001`, `DX-SYN000001-001`, and the other prefixes in `app/utils/identifiers.py`). Canonical concepts on a case must already exist in local reference tables.

## Licensing

Terminology and dataset content is not bundled. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license and access rules. LOINC requires `LOINC_USERNAME` and `LOINC_PASSWORD`; missing credentials raise `SourceNotConfigured` and do not generate lab identifiers. SNOMED CT and MIMIC-IV stay disabled in `data_source_registry` until credentials are configured.

## Layout

- `app/models` — SQLAlchemy 2 models
- `app/schemas` — Pydantic v2 models that match the tables
- `app/repositories` — lookups, upserts by official identifiers, and the source-registry metadata seed
- `app/sources` — RxNav, LOINC FHIR, official UCUM essence XML, NLM ICD-10-CM, NLM conditions, DailyMed, and RxClass clients
- `app/services` — sync, bootstrap, local search, clinical rules, generation, validation, error injection
- `app/cli` — `db-init`, `sync-*`, `reference-search`, `bootstrap-reference-data`, `generate-synthetic-cases`, `validate-cases`, `freeze-validation-batch`, `export-validation-batch`
- `app/api` — `GET /reference/medications`, `/labs`, `/diagnoses`, `/symptoms`
- `app/openai` — optional narrative wording after canonical concepts are selected
- `data/bootstrap` — human-readable concept requests, curated rule templates, and generation scenarios
- `data/validation` — frozen VAL-* batch plan and blinded / investigator exports

`CaseGenerationRun.blueprint_id` is the UUID foreign key to `case_blueprints.id`. Optional links to reference rows use `ON DELETE RESTRICT`. Case children use `ON DELETE CASCADE` on `case_id`.

Alembic revision `1c236aeaadc7` is the Phase 1 schema and is not rewritten. `7b9e4c21d6a0` adds `clinical_rules`. `c3f8a91b2e47` adds `validation_batch_cases` for immutable VAL-* assignments.

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

`db-init` runs `alembic upgrade head` and ensures eight `data_source_registry` rows exist. It does not load clinical concepts.

## Terminology sync and bootstrap

Sync commands call official APIs or files and upsert what they return. They do not run a full terminology import by default.

```bash
clinical-case-generator sync-rxnorm --name <medication-name>
clinical-case-generator sync-rxnorm --rxcui <rxcui>
clinical-case-generator sync-loinc --query <lab-name>
clinical-case-generator sync-loinc --code <loinc-code>
clinical-case-generator sync-ucum --query <unit-text>
clinical-case-generator sync-ucum --all
clinical-case-generator sync-icd10 --query <diagnosis-text>
clinical-case-generator sync-icd10 --code <icd10cm-code>
clinical-case-generator reference-search medications --query <text>
clinical-case-generator bootstrap-reference-data
```

`bootstrap-reference-data` reads `data/bootstrap/manifest.json` (human-readable search requests, not fabricated codes), resolves them through official APIs, upserts source-returned identifiers, stores DailyMed labels for resolved RXCUIs, and enables curated clinical rules only when label or RxClass evidence is present. Unresolved requests are reported. A second run does not duplicate canonical identifiers. LOINC rows are skipped with `SourceNotConfigured` when credentials are absent. RxNorm combination products (`name / name` or multiple related ingredients) are not selected unless the request is itself a combination. Symptoms that fail NLM conditions token matching may resolve through NLM HPO; HPO identifiers are stored as source metadata and are not written to `snomed_code`. Composed UCUM units such as `kg` keep a null conversion factor when the official essence file does not supply a numeric factor for the base unit.

## Clinical conditionals and synthetic cases

Rules in `clinical_rules` are machine-readable IF/THEN constraints with provenance. Hard rules are not enabled from terminology lookup alone.

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --no-inject-error
clinical-case-generator validate-cases
clinical-case-generator validate-cases --case-id SYN-000001
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch --batch-code RESIDENT_VALIDATION_V1
```

Generation selects canonical concepts from the local reference database, applies conditionals, persists a clean case, validates it, optionally words narrative text (OpenAI if `OPENAI_API_KEY` is set, otherwise a template), then injects exactly one medication-reconciliation error when requested. The answer key records the planted error. Numeric vital/lab values are synthetic and labeled `synthetic_model_generated`; they are not empirical MIMIC distributions.

OpenAI is not used to invent diagnoses, medications, laboratory codes, units, clinical rules, or the hidden error.

`freeze-validation-batch` builds a fixed resident-review set from `data/validation/batch_plan.json`. VAL-* identifiers are immutable after freeze. Exports are:

- `data/validation/resident_validation_cases.json` — blinded dashboard-shaped cases
- `data/validation/investigator_answer_key.json` and `.md` — control/error status and seeds
- `data/validation/validation_manifest.json` — machine-readable freeze metadata
- `data/validation/resident_review_worksheet.csv` and `resident_review_schema.json` — empty review capture (no fabricated ratings)

These records are machine-validated synthetic resident-review cases pending clinician validation. Software checks terminology, structure, and implemented source-backed rules. They are not clinically validated until residents complete review.

## Environment

See `.env.example`.

| Variable | Use |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy URL. Default `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `OPENAI_API_KEY` | Optional. Used only to word narrative text from already selected structured facts |
| `OPENAI_MODEL` | Optional narrative model. Example default `gpt-5` |
| `LOINC_USERNAME`, `LOINC_PASSWORD` | Required for `sync-loinc` and bootstrap lab import. Empty values raise `SourceNotConfigured` |
| `SNOMED_BASE_URL`, `SNOMED_API_TOKEN` | Unused. SNOMED CT stays disabled |
| `MIMIC_LOCAL_PATH` | Unused. No MIMIC files are read |

`.env` is for local development and is gitignored.

## API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

- `GET /health` returns `{"status": "ok"}`. It does not check the database.
- `GET /reference/medications`, `/labs`, `/diagnoses`, `/symptoms` search locally stored rows. Query parameters: `query`, `limit` (1–100, default 20), `offset` (default 0). These routes do not call external terminology APIs or OpenAI.

## Checks

```bash
pytest
ruff check .
mypy
```

Constraint, sync, bootstrap, and generation tests need the `DATABASE_URL` database. Tests mock HTTP. Fixture identifiers use the `TEST_` prefix only.

## Not implemented

This repository does not currently provide:

- AccessGUDID or SNOMED CT ingestion
- MIMIC ingestion or aggregate calculation
- A complete clinical-realism guarantee; human review is required
- Additional reconciliation-error families beyond those with deterministic preconditions
