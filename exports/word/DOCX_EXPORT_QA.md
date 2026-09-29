# DOCX export QA

## Balanced set

- Batch: `CLINIPROOF_BALANCED_V4`
- Expected case count: 24
- Exported case count: 24
- Missing cases: none
- Duplicate cases: none
- Medication mismatches: 0
- Numeric mismatches: 0
- Unsupported/generated facts: 0
- Answer-key leakage: none
- Archived-batch leakage: none
- Result: PASS

## Seed-guided set

- Batch: `CLINIPROOF_SEEDCASES_V3`
- Expected case count: 24
- Exported case count: 24
- Missing cases: none
- Duplicate cases: none
- Medication mismatches: 0
- Numeric mismatches: 0
- Unsupported/generated facts: 0
- Answer-key leakage: none
- Archived-batch leakage: none
- Result: PASS

## Codebook

- Source documentation: `docs/clinical_validation.md` and the validation rubric
  distributed with each current case set (`readable/validation_rubric.md`).
- Scoring/rubric fidelity: pass
- Phrase present: A rating of 1 means implausible.
- Phrase present: Easy, Moderate, Hard, or Inappropriate / outlier
- Phrase present: Could this hospitalization occur as charted?
- Phrase present: Accept. The case is suitable for use without clinically meaningful revision.
- Phrase present: There is no resident-review application in this repository.
- Phrase present: A resident review dashboard is planned.
- Answer-key leakage check: none
- Dashboard wording: the resident review dashboard is described as planned; the implemented software is the generator and reference search.
- Result: PASS
