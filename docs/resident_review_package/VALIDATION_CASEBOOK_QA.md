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

## Fillable form controls

Response boxes are Microsoft Word checkbox content controls (`w:sdt` / `w14:checkbox`), not static ballot-box characters. Each case has 47 controls: C1 domain ratings 32, C1 Pass/Fail 2, C2 Pass/Fail 2, C3 Pass/Fail 2, C4 Pass/Fail 2, C5 difficulty 4, and Accept / Revise / Exclude 3. Across 24 cases that is 1128 checkbox controls in each file. Reviewer code, review date, initials, and date are plain-text content controls. Comment areas remain ordinary editable table cells. The files contain no macros, no ActiveX, and no document protection.

- Checkbox content controls in each file: 1128
- Static ballot-box glyphs outside a content control: 0
- Unchecked display character inside each checkbox control: present, because that is the control's unchecked appearance
- Please select one response per item unless otherwise indicated: printed on the cover
- Reviewer code, review date, initials, and date: plain-text content controls, still editable
- Comment areas: ordinary table cells, still editable
- Macros, ActiveX, and document protection: none

A save/reopen cycle kept the checkbox controls, a toggled checkbox state, a typed comment, and a reviewer code.

## Visual render

Both files were rendered to page images. C1 domain names stay on one line, with one checkbox centered under each of 1, 2, 3, and 4. C2–C4 Pass/Fail, C5, and Accept / Revise / Exclude stay on one line, with space between each box and its label. Comment boxes and reviewer lines remain open. Validation reference tables are unchanged. No clipped text and no missing checkbox glyphs were seen on the inspected pages.

The page images show the unchecked appearance. They do not by themselves prove a click. The clickable control is the Word checkbox content control counted above.

## What this report does not claim

The chart-only export QA in `DOCX_EXPORT_QA.md` is a different check. Those earlier Word files do not contain validation references. The casebooks do, after C1, copied from the investigator record.
