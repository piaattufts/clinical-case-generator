# Answer-leak audit

Scope: the resident-facing text in the files opened by the current Round 2 codebooks.

- Set 1, VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, VAL-813: `exports/ko_cycle2_revised_validation_v2/*_resident.json`, rendered in `CliniProof_Cycle2_Revised_Cases_Validation.docx`.
- Set 2, the other 18 cases: `exports/ko_clean_cases_for_review_v1/*_resident.json`, rendered in `exports/ko_cycle2_clean_validation/CliniProof_Cycle2_Clean_Cases_Validation.docx`.

A home or inpatient medication row is evidence of what has already been prescribed. It is flagged here only when surrounding prose tells the resident which discharge action to take. Historical Round 1 text inside the Set 1 codebook, after the blank form, is not a resident-chart leak.

Severity: `DIRECT_ANSWER_LEAK`, `STRONG_HINT`, or `CLINICALLY_NEUTRAL`.

## Direct leaks

| Case | Field | Exact text | Reference action revealed | Severity |
| --- | --- | --- | --- | --- |
| VAL-803 | hospital_course | "Hydrochlorothiazide, lisinopril, atorvastatin, and metformin are continued. No discharge medicine is stopped." | Continue all four. Stop none. | DIRECT_ANSWER_LEAK |
| VAL-810 | presentation and admission note | "remaining parenteral ceftriaxone is intended after discharge. Parenteral ceftriaxone is intended to continue after discharge until the planned end date." | Continue ceftriaxone after discharge. | DIRECT_ANSWER_LEAK |
| VAL-810 | CaseConsult infectious disease | "Complete the planned parenteral course with laboratory follow-up." | Continue the ceftriaxone course. | DIRECT_ANSWER_LEAK |
| VAL-811 | presentation and admission note | "Parenteral ceftriaxone is intended to continue after discharge until the planned end date." | Continue ceftriaxone after discharge. | DIRECT_ANSWER_LEAK |
| VAL-811 | CaseConsult infectious disease | "Complete the planned parenteral course with laboratory follow-up." | Continue the ceftriaxone course. | DIRECT_ANSWER_LEAK |
| VAL-818 | presentation and admission note | "anticoagulation is intended at discharge. ... Warfarin is intended to continue at discharge." | Continue warfarin. | DIRECT_ANSWER_LEAK |
| VAL-824 | presentation, admission note, and hospital_course | "aspirin 81 MG Chewable Tablet was stopped during this admission. ... intentional aspirin discontinuation. Aspirin used for primary prevention was stopped after the bleed." | Stop aspirin. | DIRECT_ANSWER_LEAK |

## Strong hints

| Case | Field | Exact text | Reference action revealed | Severity |
| --- | --- | --- | --- | --- |
| VAL-801 | hospital_course | "Ibuprofen remains available for symptomatic analgesia. No bleeding and no kidney injury are recorded as a reason to stop it." | Continue ibuprofen. | STRONG_HINT |
| VAL-801 | CaseConsult geriatrics | "Use the verified collateral medication list at discharge." | Discharge the verified home list. | STRONG_HINT |
| VAL-804 | presentation and hospital_course | "A cognitive-enhancer start is deferred to outpatient confirmation. ... A new disease-modifying start was deferred to outpatient confirmation." | Do not start a cognitive enhancer now. That drug is not even on the reference plan. | STRONG_HINT |
| VAL-808 | CaseFollowup | "Primary care volume follow-up after diuretic adjustment" | Implies a diuretic change. The reference continues furosemide 40 mg oral once daily with no change. | STRONG_HINT |
| VAL-809 | CaseConsult infectious disease | "Complete the planned parenteral course with laboratory follow-up." | Continue ceftriaxone. | STRONG_HINT |
| VAL-812 | CaseConsult infectious disease | "Complete the planned parenteral course with laboratory follow-up." | Continue a completed course. The same chart says the remaining duration is still pending. | STRONG_HINT |
| VAL-815 | hospital_course and both consults | "There was no tacrolimus dose change." Repeated by transplant and infectious disease. | Continue tacrolimus 1 mg every 12 hours unchanged. | STRONG_HINT |
| VAL-816 | CaseConsult transplant | "Continue immunosuppression with infection-related adjustments as documented." | Continue tacrolimus. | STRONG_HINT |
| VAL-817 | CaseFollowup | "Anticoagulation clinic INR follow-up after warfarin resumption" | Warfarin has already been resumed. | STRONG_HINT |
| VAL-819 | presentation and hospital_course | "Warfarin was resumed. ... Anticoagulation was interrupted for surgery and then resumed." | Continue warfarin. The decision is narrated as already made. | STRONG_HINT |
| VAL-822 | CaseConsult gastroenterology | "Continue inpatient acid suppression and observe serial hemoglobin until stability." | Continue pantoprazole. The hidden reference stops it. | STRONG_HINT |
| VAL-823 | presentation, hospital_course, and CaseConsult | "Restart versus continued hold of anticoagulation remains a pending outpatient decision." Consult: "Hold anticoagulation while hemoglobin remains stable, then reassess." | Hold apixaban. Restart is not listed as an acceptable alternative. | STRONG_HINT |
| VAL-824 | CaseConsult gastroenterology | "Hold anticoagulation while hemoglobin remains stable, then reassess." | Hold an anticoagulant. This chart's relevant drug is aspirin, which the narrative already stops. The consult does not match the medication list. | STRONG_HINT |

## Clinically neutral or factual

| Case | Field | Exact text | Why it is not treated as the answer | Severity |
| --- | --- | --- | --- | --- |
| VAL-802 | hospital_course | "Atorvastatin 40 mg daily is on the verified home list." | States what the list contains. It does not say to continue it at discharge. | CLINICALLY_NEUTRAL |
| VAL-805 | hospital_course | "The only recorded furosemide order, at home and in the hospital, is 40 mg oral once daily." | States the recorded orders. It does not say that this is the discharge prescription. The same paragraph says discharge weight has not returned to dry weight. | CLINICALLY_NEUTRAL |
| VAL-806 | admission note | "Lisinopril was held because the creatinine rose during decongestion." | Gives the observable reason for a hold. It does not say whether to restart. | CLINICALLY_NEUTRAL |
| VAL-813 | hospital_course | "Valganciclovir 900 mg orally twice daily ... was started after that result. ... Tacrolimus 1 mg every 12 hours was continued." | Describes inpatient treatment that already happened. It does not say "discharge on this regimen." | CLINICALLY_NEUTRAL |
| VAL-814 | hospital_course | "Mycophenolate was held during the active CMV infection." | Gives the reason for the hold. Restart versus continued hold is left open, and both are on the evaluator plan. | CLINICALLY_NEUTRAL |
| VAL-820 | hospital_course | "Enoxaparin was used for venous-thromboembolism prophylaxis. It was not a home medicine." | Distinguishes indication and setting. It does not say to stop it at discharge. | CLINICALLY_NEUTRAL |
| VAL-821 | admission note and hospital_course | "Apixaban was held for the bleeding. ... Apixaban remained held for gastrointestinal bleeding." | The hold and its reason are visible. Restart is not instructed. | CLINICALLY_NEUTRAL |

## Cases with no flagged discharge instruction

VAL-802, VAL-806, VAL-807, VAL-814, VAL-820, and VAL-821 do not contain a sentence that states the hidden discharge action. VAL-805 and VAL-813 are close: they describe the inpatient regimen in enough detail that the discharge plan is easy to copy, but they do not use "intended," "should continue," or an equivalent discharge order.
