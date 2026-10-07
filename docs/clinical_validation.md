# Clinical validation

The current resident task is to read a clean chart and decide the discharge medication regimen. The intended regimen is a hidden reference. It is not printed in the resident chart, and the base case does not contain a deliberately planted medication error.

The active Cycle 2 form is [CliniProof_Cycle2_Final_Validation.docx](../exports/ko_cycle2_final_validation/CliniProof_Cycle2_Final_Validation.docx). Clinical Revision Cycle 2 for VAL-801–VAL-824 uses that form. The clinician rates plausibility, decision sufficiency, reference-plan validity, acceptable alternatives, missing or misleading information, resident-level appropriateness, and an overall Accept, Revise, or Exclude. The resident chart comes first. The hidden reference follows in a separate validation section. Those Word documents are linked from the root README. They are not the C1–C5 casebooks below.

The C1–C5 instrument below is the historical validation design. It was written for the frozen charts (`CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3`), many of which contain one injected discrepancy. Those Word casebooks are retained for provenance. They are not the current resident-facing study set. The recovered export remains [exports/clean_balanced_seed_set/](../exports/clean_balanced_seed_set/AUDIT.md). Passing automated tests does not mean a case has passed clinician review. `READY_FOR_CLINICIAN_REVIEW` is a workflow status, not clinical approval.

Clinician validation is one review of the complete case. There is no second stage and no separate plausibility-only pass. The same reading produces five ratings.

This document describes clinician validation of the synthetic charts. A clinician rating is not a resident answer, and a resident answer is not a substitute for C1–C5.

Until C1–C5 review is finished, active cases are machine-checked synthetic charts that are ready for human clinician validation. They are not clinically validated.

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
