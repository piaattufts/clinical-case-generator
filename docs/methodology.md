# Methodology

CliniProof builds synthetic inpatient charts for studying how an internal-medicine resident chooses discharge medicines. The current study uses one seed-guided case series, VAL-801 through VAL-824.

## How the cases were generated

The original set is `CLINIPROOF_SEEDCASES_V3`. It was generated from six resident-authored scenarios that were abstracted into archetypes, then filled with synthetic ages, vital signs, laboratories, and medication lists drawn from the project's reference tables. Medication names come from RxNorm. Laboratory names come from LOINC. Units come from UCUM. Diagnosis text uses ICD-10-CM where a code is stored. Doses come from the curated regimen table, not from the product strength. The frozen original files, including the readable charts and the manifest, are in `data/case_sets/seed_guided/`, excluding `CLEAN_BASE/`.

Most of those frozen charts were then altered so that each contained one medication-reconciliation discrepancy. Four were left unchanged as clean controls. That altered set is the original source. It is not the chart a reviewer should use when the task is to construct a discharge plan.

## Why clean cases are reviewed

The resident task is to read a hospitalization and decide the discharge medication plan. The resident is not shown a finished discharge list and is not asked to find a planted error. The research team keeps a separate reference plan for later comparison. That reference has to be reviewed by clinicians before it is used for scoring.

The charts for that review are the recovered pre-injection versions of VAL-801 through VAL-824. They are stored once, in `data/case_sets/seed_guided/CLEAN_BASE/`. Each file is a byte-identical copy of the recovered clean resident or evaluator JSON. The next revision starts from these files.

## Reviewer coverage

Two clinicians completed the same validation casebook.

Reviewer 1 left substantive case-level feedback on 6 of 24 cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. Eighteen cases have no substantive completed feedback.

Reviewer 2 left substantive case-level feedback on 4 of 24 cases: VAL-801, VAL-805, VAL-809, and VAL-813. Twenty cases have no selected ratings or comments. On the four reviewed cases, C2 through C5 and the overall recommendation were left blank. Those blanks were not filled in by inference.

## Comparison

Comments were compared case by case and stored in `docs/clinical_feedback/reviewer_comparison.csv`. A case is a second-revision candidate only when both reviewers left substantive feedback. That is four cases: VAL-801, VAL-805, VAL-809, and VAL-813. This cleanup does not revise them.

The review process is iterative clinician review. It can be described as Delphi-informed, because a later round returns the same cases to clinicians after revision and uses the same instrument. It is not a classical Delphi study. No formal consensus procedure has been run.

## Provenance

Original charts, clean charts, and the two completed review files are hashed in `docs/source_integrity.md`. Synthetic values that were added in later revision packages are not part of the clean base. Git history retains the superseded revision exports that were removed from this tree.

## After clinical acceptance

A case is not clinically validated until a clinician accepts it on the unchanged codebook. Only after that acceptance would the project use a case in a later experiment that introduces an error or model-generated advice. Those experiments are not part of the current review.

## What the next round will do

Revise the clean cases, starting with the four second-revision candidates. Review the revised charts with the same codebook in `docs/validation/`. Put the resulting package in `exports/current/` when it exists. That directory is empty until then.
