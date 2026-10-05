# Reproducibility

## Raw data stay immutable

Files under `data/raw/` are bibliographic exports and citation-chasing source files. Importers open them for reading. `write_csv` refuses a path inside `data/raw/`. Importing the same bytes again raises `FileExistsError` instead of overwriting the batch.

## Derived data are regenerated

| Path | Produced by | Safe to delete and rebuild |
| --- | --- | --- |
| `data/interim/batches/` | `import-records` | No. These are the immutable parsed copies. |
| `data/interim/normalized_records.csv` | `normalize` and citation import | Yes. `normalize` rebuilds it from batches, including citation-chasing batches. |
| `data/interim/duplicate_candidates.csv` | `duplicates` | Yes. Human decisions are copied back onto pairs that are found again. |
| `data/processed/` | `prisma` | Yes. |
| `outputs/` | `agreement`, `prisma`, `synthesize`, `search-validation-report` | Yes. |

Human screening files and extraction files are source data. Do not regenerate them from a script.

## Deterministic steps

- DOI and title normalization are pure functions.
- Record identifiers are SHA-256 prefixes of the source database, source id, normalized DOI, normalized title, year, and source path.
- Calibration uses `random.Random(seed)` after sorting identifiers. The default seed is `20261005`. The method string is stored with the sample.
- Duplicate pairs are ordered by record id. Fuzzy scores are rounded to four decimal places.
- Cohen's kappa uses the standard observed-versus-expected formula on a fixed category list. Zero cells stay in the matrix. If expected agreement is 1, kappa is reported as undefined.

## Provenance

Each normalized row keeps `source_database`, `source_record_id`, `source_file`, `import_timestamp`, `origin`, and `discovery_source`. `doi_raw` and `title` keep the source strings. `doi_normalized` and `normalized_title` are the comparison copies.

Citation edges keep the seed, direction, iteration, parent, discovery source, and retrieval date.

## What is not silent

- Duplicate candidates are not merged.
- Conference and journal versions are not collapsed.
- Blank yes/no cells fail validation.
- `NOT_REPORTED_OR_UNCLEAR` is not converted to `NO`.
- AI suggestions, if any, are stored in `data/screening/ai_suggestions.csv` with provider, model, version, and prompt hash. They are not written into the decision column of a screening file.
- Protocol changes go in `protocol/decision_log.csv`.

## Tests

Tests live in `tests/test_normalization.py`, `tests/test_deduplication.py`, `tests/test_screening.py`, `tests/test_agreement.py`, `tests/test_extraction.py`, and `tests/test_prisma.py`. Fixtures are synthetic and labeled `SYNTHETIC TEST FIXTURE`. They are not written into `data/`.
