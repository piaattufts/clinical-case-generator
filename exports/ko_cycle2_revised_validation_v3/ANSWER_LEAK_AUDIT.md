# Answer-leak audit, version 3

Scope: resident JSON for VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. Historical Round 1 text in the codebook is not resident-chart text. The clinician adjudication questions sit after the hidden reference and are not resident text.

Searched phrases: intended, intended at discharge, continue after discharge, should continue, should stop, restart, resume, planned outpatient regimen, planned antibiotic course, correct medication, expected regimen, take exactly as listed, no reason to stop, no discharge medicine is stopped, verified list at discharge, are continued, complete the planned parenteral course, use the verified list.

| Case | Pattern | Severity |
| --- | --- | --- |
| VAL-801 | none | DIRECT_ANSWER_LEAK = 0 |
| VAL-802 | none | DIRECT_ANSWER_LEAK = 0 |
| VAL-803 | none | DIRECT_ANSWER_LEAK = 0 |
| VAL-805 | none | DIRECT_ANSWER_LEAK = 0 |
| VAL-809 | none | DIRECT_ANSWER_LEAK = 0 |
| VAL-813 | none | DIRECT_ANSWER_LEAK = 0 |

DIRECT_ANSWER_LEAK count: 0.

Removed resident sentences from version 2: “No bleeding and no kidney injury are recorded as a reason to stop it.” “Use the verified collateral medication list at discharge.” “Hydrochlorothiazide, lisinopril, atorvastatin, and metformin are continued. No discharge medicine is stopped.” “Complete the planned parenteral course with laboratory follow-up.”
