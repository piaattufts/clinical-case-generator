# Workflow

Human steps are marked HUMAN. Commands are marked AUTO. AUTO steps do not decide eligibility.

## 0. Protocol file

HUMAN. Copy `InTheWild_Review_Methods.docx` to `protocol/InTheWild_Review_Methods.docx`.

HUMAN. Paste the final Scopus query into `search/scopus.txt` without editing it.

HUMAN. Translate it per database. Leave `# TODO: HUMAN VERIFICATION REQUIRED` until you have checked the translation.

## 1. Search

HUMAN. Run each database search. Save the export in the matching `data/raw/` directory. Do not open the export and delete rows.

HUMAN. Add one row to `search/search_log.csv` with the date, the query file, the filters, the hit count shown by the database, and the export filename.

AUTO.

```bash
PYTHONPATH=src python -m inthewild_review import-records --database scopus --input data/raw/scopus/export.csv
PYTHONPATH=src python -m inthewild_review normalize
```

Repeat import for each export. `normalize` rebuilds `data/interim/normalized_records.csv` from the batches. Re-importing the same bytes is refused so a raw file is not silently loaded twice.

## 2. Duplicates

AUTO. `PYTHONPATH=src python -m inthewild_review duplicates`

HUMAN. In `data/interim/duplicate_candidates.csv`, set `human_decision` to one of `SAME_RECORD`, `DISTINCT_PUBLICATIONS`, `CONFERENCE_JOURNAL_PAIR`, or `UNCERTAIN`. For `SAME_RECORD`, also set `retained_record_id` to the record you are keeping. Leave the other record in the file. The script does not delete it.

## 3. Calibration

AUTO. `PYTHONPATH=src python -m inthewild_review calibration --n 100 --seed 20261005`

HUMAN. Two reviewers complete their own files.

AUTO. `PYTHONPATH=src python -m inthewild_review agreement`

HUMAN. Write consensus only after both reviews exist.

## 4. Title and abstract screening

HUMAN. Fill `data/screening/title_abstract_screening.csv`.

AUTO. `PYTHONPATH=src python -m inthewild_review prepare-fulltext`

## 5. Full text

HUMAN. Fill `data/screening/full_text_screening.csv` using YES, NO, and UNCLEAR. Do not infer missing evidence.

## 6. Extraction

HUMAN. Enter publications, studies, deployments, and scenarios. Use `NOT_REPORTED_OR_UNCLEAR` when the paper does not say.

AUTO. `PYTHONPATH=src python -m inthewild_review validate`

Validation prints every problem and exits with an error. It does not repair rows.

## 7. Citation chasing

HUMAN. Record edges. There is no coded stopping rule.

AUTO. `PYTHONPATH=src python -m inthewild_review citation-import --input data/raw/citation_chasing/edges.csv`

Citation records are stored as an import batch and rebuilt into the normalized table. A later `normalize` keeps them. Run `duplicates` again. Screen the new records. They are not eligible by default.

## 8. Outputs

AUTO.

```bash
PYTHONPATH=src python -m inthewild_review prisma
PYTHONPATH=src python -m inthewild_review synthesize
PYTHONPATH=src python -m inthewild_review search-validation-report
```

HUMAN. Read the outputs. Do not type replacement counts into the JSON. If a number looks wrong, fix the source row and regenerate.

## 9. A change to the methods

HUMAN. Before changing a search string, an eligibility rule, a code, an extraction field, or an analysis, add a prospective row to `protocol/decision_log.csv`.
