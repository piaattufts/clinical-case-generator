# Consistency audit

This audit compares the public reviewer record, family labels, revised and Generation 2 files, and the validation instrument. Status is PASS, FAIL, or FIXED. A FIXED row was a mismatch that this change corrected. An open item is a mismatch that was not rewritten.

Verbatim reviewer comments in `reviewer_1_comments` and `reviewer_2_comments` were not edited. Blank ratings were not filled in. `data/case_sets/seed_guided/` outside this audit's read-only checks, and `CLEAN_BASE/`, were not modified.

## A1. Reviewer record

| Item | Expected | Found | Status | File:line |
| --- | --- | --- | --- | --- |
| Reviewer 1 coverage | 6 of 24: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, VAL-813 | Same six rows have substantive ratings; the other 18 are blank | PASS | docs/clinical_feedback/reviewer_comparison.csv |
| Reviewer 2 coverage | 4 of 24, C1 only: VAL-801, VAL-805, VAL-809, VAL-813 | C2–C5 and overall are blank on those four and on the other 20 | PASS | docs/clinical_feedback/reviewer_comparison.csv |
| VAL-805 C1 and C3 | Reviewer 1 C1 Fail and C3 Fail; reviewers disagree on C1; Reviewer 2 Pass conflicts with Fit = 2 | CSV: Fail / Pass, C3 Fail, domains `3/3/3/3/2;3/2/3/3` and `3/2/3/4/4/3/4/3` | FIXED | README.md:103; docs/methodology.md:51; docs/revision/overlap_4_revision_log.md:54 |
| VAL-805 double tick | Medication regimen recorded as 2 and 3 | `2;3`, agree and absolute difference blank | PASS | docs/clinical_feedback/reviewer_item_ratings.csv |
| VAL-809 wording | Reviewer 1 wrote "AKI" | Derived summary and method text quote "AKI was unexplained and lisinopril was continued despite AKI" | FIXED | README.md:105; docs/methodology.md:53; docs/revision/overlap_4_revision_log.md:88 |
| VAL-813 potassium | Quote "change in potassium with obvious cause or indication"; "unexplained" is an interpretation | Comment column still has that sentence; the derived summary now quotes it | FIXED | README.md:107; docs/clinical_feedback/reviewer_comparison.md; docs/revision/overlap_4_revision_log.md:122 |
| VAL-802 ratings | C2 Fail, C3 Fail, C4 lisinopril despite elevated creatinine, overall Exclude | CSV columns match; the planted omission was not recognized | FIXED | docs/methodology.md:57; docs/clinical_feedback/reviewer_comparison.csv |
| VAL-803 supply note | 7-day lisinopril comment coincides with `f2_insufficient_supply` | Stated in the derived concern and the method note; later ratings stay blank | FIXED | docs/methodology.md:59 |
| Form flags | VAL-801 C3 Pass and Fail; VAL-805 Medication regimen 2 and 3, plus Reviewer 2 C1 Pass against Fit = 2 | Both flags are in `form_flags` | PASS | docs/clinical_feedback/reviewer_comparison.md |
| `revision_candidate` | VAL-802 and VAL-803 were revised from Reviewer 1 plus the framework | Filled as `REVIEWER_1_PLUS_FRAMEWORK`; `SECOND_REVISION_CANDIDATE` remains the four overlap cases; blank means no case-specific comment | FIXED | README.md:97; docs/methodology.md:47 |
| C1 agreement | 11 of 31 single-response domain pairs (35%), mean absolute difference 0.77, overall C1 3 of 4; descriptive only; no kappa | Same figures in the README, method note, and comparison note | PASS | README.md:95; docs/methodology.md:63; docs/clinical_feedback/reviewer_comparison.md |

## A2. Identifiers and labels

| Item | Expected | Found | Status | File:line |
| --- | --- | --- | --- | --- |
| Batch label | `CLINIPROOF_SEEDCASES_FirstRound` and `CLINIPROOF_SEEDCASES_V3` are the same VAL-801–VAL-824 freeze | `batch_plan.json` and `validation_registry.json` both store `CLINIPROOF_SEEDCASES_V3` for that range. The README states that the reviewed casebooks' cover label is the same freeze | PASS | data/case_sets/seed_guided/batch_plan.json:2; data/validation_registry.json:3; README.md:68 |
| Family display name | One display name per family; codes kept | Display name is the archetype `seed_archetype_name`. Generation 1 and Generation 2 codes are unchanged | FIXED | README.md:291; docs/methodology.md:15; app/services/g2_match.py; data/bootstrap/discharge_scenarios_g2.json |
| Pair map | VAL-801↔G2-001 through VAL-824↔G2-024, one to one, same family | `matched_pairs.csv`, `matching_profiles/`, `blinding_map.json`, and `case_links.csv` agree. Each blinding pair id is shared by the two members | PASS | data/case_sets/synthea_g2/matched_pairs.csv; data/case_sets/synthea_g2/blinding_map.json |

The display names are:

| Display name | Generation 1 code | Generation 2 code |
| --- | --- | --- |
| Medication history uncertainty | `MEDREC_UNCERTAIN_HISTORY` | `MED_HISTORY_UNCERTAINTY` |
| Acute heart-failure decompensation | `HF_DECOMPENSATION` | `HF_DECOMPENSATION` |
| Outpatient parenteral antibiotic therapy after endocarditis | `OPAT_ENDOCARDITIS` | `ENDOCARDITIS_OPAT` |
| Post-kidney-transplant infectious complication | `TRANSPLANT_CMV` | `TRANSPLANT_CMV` |
| Postoperative anticoagulation after hip fracture | `POSTOP_ANTICOAGULATION` | `HIP_FRACTURE_ANTICOAGULATION` |
| Gastrointestinal bleed with anticoagulation decisions | `GI_BLEED_ACUTE_CHANGE` | `GI_BLEED_ANTICOAGULATION` |

## A3. Data integrity

| Item | Expected | Found | Status | File:line |
| --- | --- | --- | --- | --- |
| Revised pair of files | 24 cases, no gaps or duplicates, resident and evaluator | overlap_4 has VAL-801, VAL-805, VAL-809, VAL-813; remaining_20 has the other 20 | PASS | data/case_sets/seed_guided/REVISED/ |
| Resident separation, Generation 1 | No reference plan, answer key, archetype code, source DOCX name, or generation-method name | Those strings are absent. `generation_source` is `synthetic` and `source_file` is null | PASS | data/case_sets/seed_guided/REVISED/ |
| Resident separation, Generation 2 | Same separation | No reference plan in the resident file. See open items for `source_type` and one regimen id | OPEN | data/case_sets/synthea_g2/cases/resident/ |
| Specialty and diagnosis | Match the slot archetype | general medicine, cardiology, infectious disease, nephrology, orthopedics, and general medicine, with an in-family admission diagnosis | PASS | revised resident JSON |
| Revision logs | Every revised case has an entry, and every entry names an existing case | overlap log: 4 cases. Remaining log and `revision_framework_application.csv`: the other 20 | PASS | docs/revision/overlap_4_revision_log.md; docs/revision/remaining_20_revision_log.md |
| Overlap concerns | Each comparison concern is cited by the revision log | The four logs cite both reviewers' concerns, including VAL-805 C3 Fail, the AKI sentence, and the potassium quotation | FIXED | docs/revision/overlap_4_revision_log.md |
| SHA-256 | Recompute the preserved-source hashes and do not overwrite them | 93 of 93 recorded digests in `docs/source_integrity.md` match the files on disk | PASS | docs/source_integrity.md |

## A4. Instrument fidelity

| Item | Expected | Found | Status | File:line |
| --- | --- | --- | --- | --- |
| Clean-case C1–C5, overall recommendation, comment boxes, and C4 fields | Identical to `CliniProof_Clinical_Validation_Template.docx` | CODEBOOK and the README codebook section now use the template's clean-case questions, anchors, pass rule, and field labels | FIXED | docs/validation/CODEBOOK.md:7; README.md:764 |
| Error-bearing questions inside the historical template | Reported, not rewritten | The template's error-bearing cases ask whether the intended problem is present, whether a resident could detect it, and whether another problem competes with it. The clean books do not use those questions | PASS | docs/validation/CliniProof_Clinical_Validation_Template.docx |
| Generated casebooks | Same clean-case instrument text as the template | Programmatic marker diff is empty for every case in the five casebooks | PASS | tests/test_review_casebooks.py |

## A5. Docs and tests

| Check | Result |
| --- | --- |
| `python scripts/check_docs.py` | documentation checks passed |
| `pytest` | 196 passed |
| `ruff check .` | all checks passed |
| `mypy app` | no issues in 80 source files |

## Open items

| Item | Why it is open |
| --- | --- |
| Generation 2 resident `source_type` | The value is `synthea_cliniproof_g2`. That is a generation-method label stored on the resident JSON. The casebook renderer does not print it. Removing it would rewrite the Generation 2 case files, so it was left in place. |
| `CEFTRIAXONE_ENDOCARDITIS_OPAT` | That regimen id appears in the Generation 2 resident JSON for G2-009–G2-012. It is not a family field, and the renderer does not print regimen ids. Renaming it would change the stored medication identity. |
| Historical template error-case wording | C2, C3, and C4 questions differ for error-bearing cases in the original template. Those questions stay in the template. The current review books are clean cases and use the clean questions. |

## Casebook verification

The shared renderer is `app/services/review_casebook.py`. It uses the existing chart renderer and the existing C1–C5 controls. Every revised and Generation 2 case uses the clean-case C2 question. The hidden reference discharge plan is copied from the evaluator file into the Validation Reference and labeled "For clinician validation only — not shown to residents." The template's own banner sentence is unchanged.

| Check | Result |
| --- | --- |
| Instrument marker diff against the template | Zero differences for all five casebooks |
| Rendered medications, doses, routes, frequencies, admission/discharge labs, and vital signs | Zero mismatches on VAL-822, VAL-807, VAL-815, G2-005, G2-011, and G2-003, drawn with seed `20261009` |
| Blinded casebook XML (`word/`, `docProps/`, `customXml/`) | Zero hits for `VAL-`, `G2-`, the family codes, `Synthea`, `Generation`, and `seed` |
| Blinded order | Pairs follow `blinding_map.json`. Within each pair, `random.Random(20261009)` shuffles the two charts. Neutral ids are `N-` plus four hex digits and do not embed 801–824 |
| Pages | Recorded in `docs/validation/case_links.csv` from a LibreOffice PDF conversion. VAL-801 starts on page 4 of the Generation 1 book. G2-001 starts on page 3 of the Generation 2 book |

`data/blinding/unblinding_key.json` is investigator-only. It is not part of the blinded reviewer packet.
