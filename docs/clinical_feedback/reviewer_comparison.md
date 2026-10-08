# Reviewer comparison

This table compares the two completed clinician reviews case by case. It does not assign the reviewers different scientific roles. Both reviewed clinical cases. The normalized case rows are in [reviewer_comparison.csv](reviewer_comparison.csv). Item-level ratings, one row per case and item, are in [reviewer_item_ratings.csv](reviewer_item_ratings.csv).

Checkbox states were read from the completed forms. Blank ratings stay blank. A double-ticked response stays as recorded text, such as `2;3` or `Pass;Fail`. Those rows leave `agree` and `abs_diff_c1` empty. Comments are copied verbatim, including original typos.

Reviewer 1 recorded substantive case-level feedback for six cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. The other eighteen cases have no selected ratings and no comments. VAL-803 has a completed C1 and blank later items, including a blank overall recommendation.

Reviewer 2 recorded substantive case-level feedback for four cases: VAL-801, VAL-805, VAL-809, and VAL-813. The other twenty cases have no selected ratings and no comments. On the four reviewed cases, C2 through C5 and the overall recommendation are blank.

The cases reviewed by both clinicians are VAL-801, VAL-805, VAL-809, and VAL-813. Those four were later revised directly from both reviewers’ comments. VAL-802 and VAL-803 were reviewed by Reviewer 1 only and were later revised from that feedback together with the frozen framework. The other eighteen cases had no case-specific clinician comment.

`reviewer_1_C1_domains` and `reviewer_2_C1_domains` list the eight C1 domain scores in this order: Presentation, Fit between presentation and diagnosis, Vital signs, Laboratory findings, Medication regimen, Hospital course, Consistency across the chart, and Discharge. An example is `2/2/3/3/3/2/3/4`. A case with no domain scores leaves that field blank.

`revision_candidate` records the revision track applied after this comparison:

| Value | Meaning |
| --- | --- |
| `SECOND_REVISION_CANDIDATE` | Both reviewers recorded substantive feedback. The case was revised directly from those comments. |
| `REVIEWER_1_PLUS_FRAMEWORK` | Only Reviewer 1 recorded substantive feedback. The revision used that feedback plus the frozen framework. |
| blank | No case-specific clinician comment. If the case was revised, the revision was framework-guided only. |

| Case | Reviewer 1 | Reviewer 2 | Overlap |
| --- | --- | --- | --- |
| VAL-801 | Reviewed. C1 Fail. Overall: revise. | Reviewed. C1 Fail. Overall blank. | Both |
| VAL-802 | Reviewed. C1 Fail. Overall: exclude. | Not reviewed. | Reviewer 1 only |
| VAL-803 | Reviewed. C1 Fail. Later items and overall blank. | Not reviewed. | Reviewer 1 only |
| VAL-805 | Reviewed. C1 Fail. C3 Fail. Overall: revise. | Reviewed. C1 Pass. Overall blank. | Both |
| VAL-809 | Reviewed. C1 Fail. Overall: revise. | Reviewed. C1 Fail. Overall blank. | Both |
| VAL-813 | Reviewed. C1 Fail. Overall: exclude. | Reviewed. C1 Fail. Overall blank. | Both |
| All other VAL-801–VAL-824 cases | Not reviewed. | Not reviewed. | Neither |

## C1 domain agreement

Agreement below uses only domain pairs where both reviewers recorded a single response. Exact agreement is 11 of 31 domain pairs (35%). The mean absolute difference on those pairs is 0.77. Medication regimen and Consistency across the chart have the lowest agreement, with 0 exact matches each. The double-ticked Medication regimen response on VAL-805 is outside the 31 pairs.

Overall C1 agrees on 3 of 4 overlapping cases. The disagreement is VAL-805: Reviewer 1 Fail, Reviewer 2 Pass. C2 through C5 and the overall recommendation have no pair rated by both reviewers.

These counts are descriptive only. They cover two raters, four overlapping cases, and C1 only. The comparison does not report kappa, and it does not apply a consensus threshold.

## Form-level data issues

`form_flags` in [reviewer_comparison.csv](reviewer_comparison.csv) records these form problems. Other cases leave the field blank.

- VAL-801: Reviewer 1 C3: both Pass and Fail ticked.
- VAL-805: Reviewer 1 C1 Medication regimen: both 2 and 3 ticked. Reviewer 2 marked C1 Pass although Fit between presentation and diagnosis = 2. The form rule is that any domain scored 1 or 2 makes C1 Fail.
