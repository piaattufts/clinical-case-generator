# Validation casebook QA

These checks were run on the two clinician validation casebooks. They compare each chart with the resident-facing case file and each validation reference with the batch plan and the investigator answer key. No case file was modified.

## Balanced set

- Batch: `CLINIPROOF_BALANCED_V4`
- Case range: VAL-701–VAL-724
- Expected case count: 24
- Exported case count: 24
- Clean controls: 4
- Error-bearing cases: 20
- Family 1: 11
- Family 2: 9
- Missing cases: none
- Duplicate cases: none
- Planned category, answer-key category, and casebook category mismatches: 0
- Medication dose, route, and frequency mismatches in the chart section: 0
- Missing canonical validation fields: 0
- Result: PASS

## Seed-guided set

- Batch: `CLINIPROOF_SEEDCASES_V3`
- Case range: VAL-801–VAL-824
- Expected case count: 24
- Exported case count: 24
- Clean controls: 4
- Error-bearing cases: 20
- Family 1: 7
- Family 2: 13
- Missing cases: none
- Duplicate cases: none
- Planned category, answer-key category, and casebook category mismatches: 0
- Medication dose, route, and frequency mismatches in the chart section: 0
- Missing canonical validation fields: 0
- Result: PASS

## Structure

- C1 is printed before the validation reference in every case.
- C2, C3, C4, C5, comment areas, and Accept / Revise / Exclude follow that reference.
- The validation reference states that it would not be shown to a resident in the later assessment.

## What this report does not claim

The chart-only export QA in `DOCX_EXPORT_QA.md` is a different check. Those earlier Word files do not contain validation references. The casebooks do, after C1, copied from the investigator record.
