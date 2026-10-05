# Screening manual

Status: operational manual for the workflow in this repository. Exclusion-code sentences are provisional until `InTheWild_Review_Methods.docx` is added. If the protocol wording differs, change this file and add a prospective row to `protocol/decision_log.csv`. Do not edit completed screening sheets without that row.

## Title and abstract

Work in `data/screening/title_abstract_screening.csv` for the review, and in the calibration reviewer files for the calibration sample.

Columns: `record_id`, `reviewer`, `decision`, `exclusion_code`, `notes`, `screened_at`, `criteria_version`.

`criteria_version` for rows coded before the protocol file is checked: `brief-pending-protocol-file`.

### Decisions

| Decision | Meaning | Exclusion code |
| --- | --- | --- |
| INCLUDE | The record appears to meet eligibility | Blank |
| MAYBE | Eligibility is not clear from the title and abstract | Blank |
| EXCLUDE | The record does not meet eligibility | Exactly one code below |

MAYBE is a real decision. Do not rewrite it to INCLUDE or EXCLUDE in order to simplify a spreadsheet. The agreement report can collapse INCLUDE and MAYBE only in a separate calculation. The stored value stays MAYBE.

### Exclusion codes

| Code | When to use it | When not to use it |
| --- | --- | --- |
| `N1_NOT_NATURALISTIC` | The interaction is not in an intended use setting, not in a purpose-built high-fidelity stand-in for that setting, and not a repeated everyday-use laboratory evaluation as defined in the eligibility note | Do not use it only because the authors call the place a laboratory |
| `N2_NOT_SOCIAL_ROBOT` | There is no physically embodied social or companion robot | A robot that is embodied and used socially is not excluded because the platform is unfamiliar |
| `N3_NON_PRIMARY` | The record is not a primary evaluation report. Reviews, commentaries, editorials, and protocol-only papers are the examples used here | A primary paper that also reviews prior work can still be included |
| `N4_TECHNICAL_NO_SITUATED_HRI` | The paper is technical and does not present a situated human–robot evaluation that can be screened | A technical paper that also reports a situated evaluation is screened on that evaluation |
| `N5_NOT_A_RECORD` | The export row is not a publication record: empty, unusable, or not a scholarly item that can be screened | Do not use this for a real paper you have decided to exclude for a substantive reason |

One primary code only. Put extra comments in `notes`.

## Calibration

1. Draw the sample with the shared seed. The default is 100 records and seed `20261005`.
2. Reviewer 1 fills `calibration_reviewer_1.csv` without opening reviewer 2's file.
3. Reviewer 2 fills `calibration_reviewer_2.csv` the same way.
4. After both are done, write agreed labels in `calibration_consensus.csv`.
5. Run `agreement`.

Consensus without a decision in both independent files fails validation. The agreement command does not write consensus and does not change the reviewer files.

## Full text

`prepare-fulltext` adds a blank row for each title/abstract INCLUDE or MAYBE. It leaves existing full-text cells alone. EXCLUDE at title/abstract is not queued. That queue rule is provisional. See the decision log.

Columns include the criterion fields, `decision`, `exclusion_reason`, `reviewer`, `notes`, and `screened_at`.

Criterion fields use `YES`, `NO`, or `UNCLEAR`:

- `full_text_available`
- `physically_embodied_robot`
- `substantive_social_interaction`
- `human_participants`
- `naturalistic_or_repeated_longterm`
- `identifiable_interaction_situation`
- `setting_extractable`
- `duration_extractable`
- `interaction_structure_extractable`

INCLUDE is valid only when `full_text_available` and every criterion field are `YES`.

EXCLUDE needs one reason:

| Reason | The matching field must be |
| --- | --- |
| `NOT_PHYSICALLY_EMBODIED_ROBOT` | `physically_embodied_robot` = NO |
| `NO_SUBSTANTIVE_SOCIAL_INTERACTION` | `substantive_social_interaction` = NO |
| `NO_HUMAN_PARTICIPANTS` | `human_participants` = NO |
| `NOT_NATURALISTIC_OR_REPEATED_LONGTERM` | `naturalistic_or_repeated_longterm` = NO |
| `NO_IDENTIFIABLE_INTERACTION_SITUATION` | `identifiable_interaction_situation` = NO |
| `SETTING_NOT_EXTRACTABLE` | `setting_extractable` = NO |
| `DURATION_NOT_EXTRACTABLE` | `duration_extractable` = NO |
| `INTERACTION_STRUCTURE_NOT_EXTRACTABLE` | `interaction_structure_extractable` = NO |
| `FULL_TEXT_UNAVAILABLE` | `full_text_available` = NO |

`UNCLEAR` cannot support an exclusion reason. Missing text is not evidence of absence.

Poor reporting of relationship history, materials, autonomy, or similar extraction fields is not a full-text exclusion reason. Those fields are coded `NOT_REPORTED_OR_UNCLEAR` after inclusion. Setting, duration, and interaction structure are different: the protocol requires them to be extractable for inclusion.

MAYBE remains available at full text when a criterion is `UNCLEAR`. Confirm that practice against the protocol file.
