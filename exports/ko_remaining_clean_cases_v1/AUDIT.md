# Remaining recovered clean cases

These charts were not rewritten. Each file starts from the recovered clean export.

| Case | Clean source recovered | Error mutation absent | Answer leakage absent | Precheck finding | Status |
| --- | --- | --- | --- | --- | --- |
| VAL-804 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-806 | yes | yes | no | answer leakage:an instruction directs the resident to resume a held medicine; unsupported:a restart instruction refers to a creatinine baseline that is not in the chart | NEEDS_PRE_REVIEW_FIX |
| VAL-807 | yes | yes | yes | unsupported:hospital course describes potassium repletion but no potassium medication is listed | NEEDS_PRE_REVIEW_FIX |
| VAL-808 | yes | yes | no | answer leakage:resident narrative states an intended discharge list; inconsistent:discharge weight 92 kg remains above dry weight 86 kg; contradictory timeline:narrative says the diuretic plan was adjusted but the home and inpatient loop-diuretic regimens match | CLINICALLY_INCONSISTENT |
| VAL-810 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-811 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-812 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-814 | yes | yes | no | answer leakage:an instruction directs the resident to resume a held medicine; contradictory timeline:valganciclovir is already a home medicine while the admission is for CMV disease, and the chart does not describe prophylaxis | CLINICALLY_INCONSISTENT |
| VAL-815 | yes | yes | yes | contradictory timeline:narrative describes a tacrolimus dose adjustment but the home and inpatient doses match; contradictory timeline:valganciclovir is already a home medicine while the admission is for CMV disease, and the chart does not describe prophylaxis | CLINICALLY_INCONSISTENT |
| VAL-816 | yes | yes | yes | contradictory timeline:valganciclovir is already a home medicine while the admission is for CMV disease, and the chart does not describe prophylaxis | CLINICALLY_INCONSISTENT |
| VAL-817 | yes | yes | no | answer leakage:resident narrative states an intended discharge list; contradictory timeline:narrative describes enoxaparin but it is not on the medication list | CLINICALLY_INCONSISTENT |
| VAL-818 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-819 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-820 | yes | yes | yes | indication mismatch:enoxaparin is labeled for atrial fibrillation while the narrative describes venous-thromboembolism prophylaxis | NEEDS_PRE_REVIEW_FIX |
| VAL-821 | yes | yes | no | answer leakage:an instruction directs the resident to resume a held medicine | NEEDS_PRE_REVIEW_FIX |
| VAL-822 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-823 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
| VAL-824 | yes | yes | yes | none | READY_FOR_FRESH_REVIEW |
