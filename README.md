# CliniProof

CliniProof is a research framework for creating and validating synthetic inpatient cases used to study discharge-medication decision-making. A resident is meant to read one clean hospitalization and independently decide the discharge medication plan. The resident is not shown a completed discharge list and is not asked to find a planted error. The research team keeps a separate reference plan. That reference is not for scoring until clinicians have accepted it. Passing automated checks does not mean a case is clinically validated.

## What is current

The current study is the seed-guided series VAL-801 through VAL-824.

The original frozen set, `CLINIPROOF_SEEDCASES_V3`, is preserved and was not altered by this cleanup. It still contains the earlier planted-error variants. The charts that the next revision must start from are the clean pre-injection cases in one directory, `data/case_sets/seed_guided/CLEAN_BASE/`.

Two clinicians have reviewed the clean cases with the same codebook. Reviewer 1 left substantive feedback on 6 of 24 cases. Reviewer 2 left substantive feedback on 4 of 24 cases. Four cases were reviewed by both and are the second-revision candidates: VAL-801, VAL-805, VAL-809, and VAL-813. That revision has not been done. No case in this tree should be called clinically validated.

| Artifact | Source of truth |
| --- | --- |
| Original cases | `data/case_sets/seed_guided/` excluding `CLEAN_BASE/`, batch `CLINIPROOF_SEEDCASES_V3` |
| Clean cases | `data/case_sets/seed_guided/CLEAN_BASE/` |
| Reviewer 1 feedback | `docs/clinical_feedback/reviewer_1/KO_Casebook_Validation.docx` |
| Reviewer 2 feedback | `docs/clinical_feedback/reviewer_2/CliniProof_SeedGuided_Validation_Casebook_final_alex.docx` |
| Normalized comparison | `docs/clinical_feedback/reviewer_comparison.csv` |
| Validation instrument | `docs/validation/` |
| Methodology | `docs/methodology.md` |
| Current revised cases | None yet. The second revision is pending. `exports/current/` is empty until then. |

## Where the reviews are

Reviewer 1 completed the KO casebook. Substantive case-level feedback is present for VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. The other eighteen cases have no substantive completed feedback. VAL-803 stops after C1; the later ratings and the overall recommendation are blank.

Reviewer 2 completed the seed-guided casebook. Substantive case-level feedback is present for VAL-801, VAL-805, VAL-809, and VAL-813. The other twenty cases have no selected ratings or comments. On the four reviewed cases, C2 through C5 and the overall recommendation are blank and were not inferred.

The case-level comparison is in [reviewer_comparison.md](docs/clinical_feedback/reviewer_comparison.md). The four overlapping cases are marked `SECOND_REVISION_CANDIDATE`. They have not been revised in this cleanup.

## Methodology and codebook

How the original cases were generated, why the clean charts are the review set, and what happens after a clinician accepts a case are in [docs/methodology.md](docs/methodology.md). The process is iterative clinician review. It is informed by a second clinician reading, and a later round is expected to use the same instrument. It is not a classical Delphi study.

The blank codebook is [docs/validation/CliniProof_Clinical_Validation_Template.docx](docs/validation/CliniProof_Clinical_Validation_Template.docx). The fields are described in [docs/validation/CODEBOOK.md](docs/validation/CODEBOOK.md). The coding scheme was not changed. The next round should use this file so ratings stay comparable.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word.

## Reproduce a checkout

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
pytest
ruff check .
mypy app
python scripts/check_docs.py
```

Medication names are taken from RxNorm, laboratory observations from LOINC, units from UCUM, and diagnosis text from ICD-10-CM. A source-backed terminology concept is not automatically a clinically appropriate choice. The generator does not treat product strength as the administered dose. Curated regimens are in [data/bootstrap/medication_regimens.json](data/bootstrap/medication_regimens.json). Scenarios are in [data/bootstrap/scenarios.json](data/bootstrap/scenarios.json). What those identifiers do not prove is in [docs/provenance.md](docs/provenance.md).

Hashes of the original set, the clean base, and both review files are in [docs/source_integrity.md](docs/source_integrity.md). The cleanup inventory is in [docs/repository_cleanup_inventory.md](docs/repository_cleanup_inventory.md).

## Historical datasets and provenance

Superseded revision packages and older frozen batches were removed from this working tree. They remain in Git history under the tag `repo-before-clinical-cleanup-2026-10`. They are not the current study set.
