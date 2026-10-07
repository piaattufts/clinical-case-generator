# Clinical validation

The current resident task is to read a clean chart and decide the discharge medication regimen. The reference plan is kept separate. It is not printed in the resident chart, and the base case does not contain a deliberately planted medication error.

Round 2 is the current clinician review of VAL-801–VAL-824. Clinicians start with [Set 1, the six revised cases](../exports/ko_cycle2_revised_validation/CliniProof_Cycle2_Revised_Cases_Validation.docx), and then review [Set 2, the eighteen clean cases](../exports/ko_cycle2_clean_validation/CliniProof_Cycle2_Clean_Cases_Validation.docx). The combined 24-case file is an investigator convenience copy, not the preferred workflow. The [project README](../README.md) explains how Round 2 was derived from Round 1. Ready for clinician review does not mean clinically validated.

The C1–C5 instrument below is the Round 1 validation design. It was written for the frozen charts (`CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3`), many of which contain one injected discrepancy. Those Word casebooks are retained so Round 1 can be reproduced. They are not the current resident-facing study set. The recovered clean charts remain in [exports/clean_balanced_seed_set/](../exports/clean_balanced_seed_set/AUDIT.md). Passing automated tests does not mean a case has passed clinician review.

Clinician validation is one review of the complete case. There is no second stage and no separate plausibility-only pass. The same reading produces five ratings.

This document describes the Round 1 instrument. A clinician rating is not a resident answer, and a resident answer is not a substitute for these ratings. The current Round 2 form, C1 through C6, is specified in the [project README](../README.md).

Round 2 cases are machine-checked and ready for that clinician reading. They are not clinically validated until a reviewer accepts them. The same is true of any chart that has only completed the Round 1 C1–C5 form described below.

## What the reviewer rates

| Criterion | Question |
| --- | --- |
| C1 Clinical plausibility | Could this hospitalization occur as charted? Consider presentation and demographics, diagnosis fit, vital signs, laboratory values and units, the medication regimen, the hospital course, chart consistency, and discharge and follow-up. |
| C2 Intended assessment problem | Is the predetermined discrepancy actually present, and does it match the answer key? Controls should contain none. |
| C3 Detectability and resolvability | Can an internal-medicine resident see the problem from resident-visible information and say what should change, without the chart announcing the answer? |
| C4 No other unintended clinically meaningful problem | Is there a second medication, monitoring, temporal, or diagnostic problem that could be an alternative answer? |
| C5 Expected resident difficulty | How hard should this chart be for the intended learner? C5 is advisory. Actual difficulty comes later from resident performance. |

C2, C3, and C4 must be acceptable before a case is used against its answer key. C1 must also be acceptable. C5 does not by itself exclude a case.

## Decisions

- **Accept.** The chart can be used for the assigned target or as a control.
- **Revise.** The chart needs a specific correction before use. Do not silently edit a frozen batch. A revision is a new freeze.
- **Exclude.** The chart should not be used, even if software checks passed.

## Materials

Use the clinician packet and worksheet for the set under review.

- [Balanced structured packet](../data/case_sets/balanced/readable/clinician_validation_packet.md) and [worksheet](../data/case_sets/balanced/readable/clinical_validation_worksheet.csv)
- [Resident-seed-guided packet](../data/case_sets/seed_guided/readable/clinician_validation_packet.md) and [worksheet](../data/case_sets/seed_guided/readable/clinical_validation_worksheet.csv)

The packet shows the chart and the intended target. Individual blinded case pages do not include the answer key. The category definitions are in [`error_taxonomy.md`](error_taxonomy.md). The criterion summary on each case-set overview is enough to start; this page is the same review in slightly more detail.

## What software already checked

Software checked structure, terminology identity, curated regimen constraints, and whether the injected change is the only mechanically detectable discrepancy. Those checks do not replace C1–C5. A regimen citation shows where the dose and frequency came from. It does not certify that a clinician would choose that regimen for every similar patient.
