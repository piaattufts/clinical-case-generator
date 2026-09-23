# Developer guide

## Setup

Python 3.12 or newer, Docker, and a LOINC account are required for a full bootstrap.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
```

Set `LOINC_USERNAME` and `LOINC_PASSWORD` in `.env` before importing laboratories. Then:

```bash
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
```

`pytest` rebuilds the database schema and will wipe local case rows. Re-run bootstrap and freeze after a full test session if you still need the database loaded. Exported JSON under `data/` is not stored only in the database.

## Study batches

Freeze and export require an explicit plan or batch code. Neither command defaults to archived historical `CLINIPROOF_TAXONOMY_V1` or to either active strategy.

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v4/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V4
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_BALANCED_V4 \
  --resident data/validation_balanced_v4/resident_validation_cases.json

clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V3
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_SEEDCASES_V3 \
  --resident data/validation_seedcases_v3/resident_validation_cases.json
```

Do not re-freeze a batch that has already been committed as immutable. The current active batches were new freezes because the previous prospective batches were already immutable. A further clinical correction needs a new batch code and a non-overlapping VAL range.

## Regimens

Dose, route, frequency, and temporal role for real medications come from `data/bootstrap/medication_regimens.json` through `app/services/medication_regimens.py`. Product strength is only a concept-ranking hint. Adding a medication to a profile requires a cited regimen entry or the medication must be removed from that profile.

## Checks

```bash
pytest
ruff check .
mypy app
python scripts/check_docs.py
```

## API

After bootstrap, `clinical-case-generator` can serve the reference API with the project's ASGI app (`app.main:app`) through uvicorn. Reference search endpoints read the bootstrapped terminology tables. They do not generate the validation batches.

## Generated cases outside a study batch

`clinical-case-generator generate-synthetic-cases --count 3 --seed 42` builds ordinary synthetic cases for development. Those cases are not part of either prospective validation set. Validate one with `clinical-case-generator validate-cases --case-id SYN-000001` only after generation has created that identifier.
