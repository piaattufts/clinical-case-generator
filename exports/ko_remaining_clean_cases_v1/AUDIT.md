# Clean cases for fresh clinician review

Untouched rows are the recovered charts that already passed the precheck. Repaired rows are corrected copies that passed the evidence audit.

| Case | Clean source | Correction | Evidence | Status |
| --- | --- | --- | --- | --- |
| VAL-804 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-806 | yes | No prior creatinine exists in the source data. The lisinopril reference is hold, based on creatinine 2.8 then 1.6 mg/dL, potassium 4.5 mmol/L, and systolic pressure 116 mmHg. Direct restart instructions were removed. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-807 | yes | The source medication list has no potassium product, so the repletion claim was removed. Potassium remains the measured 3.5 then 3.8 mmol/L. Home heart-failure medicines stay on the reference plan. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-808 | yes | Answer-revealing discharge-list language was removed. Inpatient furosemide is intravenous 40 MG twice daily, distinct from home oral 40 MG once daily. Discharge weight is the 86 kg dry weight after four days of negative balance. The reference changes oral furosemide to twice daily. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-810 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-811 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-812 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-814 | yes | Valganciclovir is no longer a home medicine. It starts after the in-hospital viral load, at 450 MG twice daily once creatinine is 1.6 mg/dL. Direct mycophenolate restart instructions were removed. The hidden reference still restarts mycophenolate because the viral load is lower and diarrhea was improving. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-815 | yes | The tacrolimus dose-change claim was removed because home and inpatient doses are both 1 MG every 12 hours. CMV is framed as disease already under valganciclovir before this admission. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-816 | yes | CMV is framed as established disease already treated with valganciclovir before this admission. The direct pending-decision instruction was replaced with follow-up context. The reference continues the recorded doses. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-817 | yes | The phrase 'in this profile' and the enoxaparin sentence were removed. Enoxaparin is not part of this medication record, and the INR is already 2.6 on warfarin, so no prophylactic enoxaparin row was added. The reference continues warfarin, lisinopril, and metformin. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-818 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-819 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-820 | yes | Enoxaparin indication is inpatient venous-thromboembolism prophylaxis in the narrative, the medication record, and the hidden stop decision. It is not labeled as atrial-fibrillation therapy. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-821 | yes | Direct instructions to resume apixaban were removed. The chart shows the bleed, hemoglobin rise from 8.7 to 10.9 g/dL, the atrial-fibrillation indication, and gastroenterology follow-up in 7 days. The hidden reference restarts apixaban. | sufficient | READY_FOR_CLINICIAN_REVIEW |
| VAL-822 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-823 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
| VAL-824 | yes | none | recovered reference retained | READY_FOR_FRESH_REVIEW |
