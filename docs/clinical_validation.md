# Clinical validation

Clinician validation is one review of the complete case. There is no second stage and no separate plausibility-only pass. The same reading produces five ratings.

This document describes clinician validation of the synthetic charts. It is not the protocol for resident study responses. Resident study responses are the later task in which a resident reviews a blinded chart and records what, if anything, is wrong with reconciliation. Clinician validation decides whether a chart is fit to be used for that task. A clinician rating is not a resident answer, and a resident answer is not a substitute for C1–C5.

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

Use the clinician packet and worksheet for the batch under review. Packets for the two active sets are linked from [`data/active_validation_sets.md`](../data/active_validation_sets.md). The packet shows the chart and the intended target. Individual blinded case pages do not include the answer key. The category definitions are in [`error_taxonomy.md`](error_taxonomy.md).

## What software already checked

Software checked structure, terminology identity, curated regimen constraints, and whether the injected change is the only mechanically detectable discrepancy. Those checks do not replace C1–C5. A regimen citation shows where the dose and frequency came from. It does not certify that a clinician would choose that regimen for every similar patient.
