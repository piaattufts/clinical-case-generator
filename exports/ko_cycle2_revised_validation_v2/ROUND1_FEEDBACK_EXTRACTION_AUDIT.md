# Round 1 feedback extraction audit

This audit checks the JSON extract against the completed review. A domain is extracted when all four checkbox states are stored. An item is incomplete when no box was selected. Ambiguity means more than one box in that item is selected. VAL-803 C2 through the overall recommendation were blank in the source and stay blank.

| Case | Pages/source | C1 extracted | C2 | C3 | C4 | C5 | Overall recommendation | Comments extracted | Ambiguity/incomplete? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-801 | KO Casebook Validation.docx | yes | Fail | Pass and Fail (SOURCE_SELECTION_AMBIGUITY) | Fail | inappropriate_or_outlier | revise | 5 | C3 |
| VAL-802 | KO Casebook Validation.docx | yes | Fail | Fail | Fail | inappropriate_or_outlier | exclude | 6 | no |
| VAL-803 | KO Casebook Validation.docx | yes | NOT_COMPLETED_IN_ROUND_1 | NOT_COMPLETED_IN_ROUND_1 | NOT_COMPLETED_IN_ROUND_1 | NOT_COMPLETED_IN_ROUND_1 | NOT_COMPLETED_IN_ROUND_1 | 1 | partial review |
| VAL-805 | KO Casebook Validation.docx | yes | Pass | Fail | Pass | moderate | revise | 3 | C1 Medication regimen: scores 2, 3 both selected |
| VAL-809 | KO Casebook Validation.docx | yes | Fail | Pass | Fail | inappropriate_or_outlier | revise | 4 | no |
| VAL-813 | KO Casebook Validation.docx | yes | Fail | Fail | Fail | inappropriate_or_outlier | exclude | 4 | no |

Programmatic checks required before revision: eight C1 domains for each case, raw score booleans present, VAL-801 C3 Pass and Fail both true, VAL-805 medication-regimen scores 2 and 3 both true, and VAL-803 C2, C3, C4, C5, and the overall recommendation all marked NOT_COMPLETED_IN_ROUND_1.
