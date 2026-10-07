# Katie design audit

Audit date: 2026-10-07. No case, codebook, README, or frozen file was edited.

The question is whether the current Round 2 cases are the study Katie described: a clean chart, an independent discharge-medication decision, and a hidden reference used only for validation and later scoring. The question is not whether the JSON parses or whether tests pass.

## What was treated as current

The README tells a clinician to open two codebooks, in this order:

1. Set 1, `exports/ko_cycle2_revised_validation_v2/CliniProof_Cycle2_Revised_Cases_Validation.docx`, for VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. The chart in that file is the version 2 JSON in the same directory.
2. Set 2, `exports/ko_cycle2_clean_validation/CliniProof_Cycle2_Clean_Cases_Validation.docx`, for the other 18 cases. Its manifest points at `exports/ko_clean_cases_for_review_v1/`.

Those 24 resident/evaluator pairs are the cases audited below.

A second Set 1 still exists at `exports/ko_revised_cases_v1/`. The long case narratives in `README.md` describe that package: baseline creatinine 1.2 mg/dL for VAL-802, sodium 128 then 135 mmol/L and a hydrochlorothiazide stop for VAL-803, intravenous furosemide and an ejection fraction of 30 percent for VAL-805, fever and a dental extraction for VAL-809, and mycophenolate for VAL-813. The linked Set 1 codebook does not contain those facts. The codebook generator in `app/services/cycle2_split_casebooks.py` still loads `ko_revised_cases_v1`, while the published Set 1 link loads version 2. The study therefore does not have one current Set 1.

Frozen Round 1 files under `data/case_sets/` were not treated as the resident task. They were used only as historical evidence.

## Answer

The current cases do not, as a set, represent the study Katie described.

The file split is right: every resident JSON lacks `reference_discharge_plan`, and both codebooks place C1 and C2 before the hidden reference. The task type is no longer "find the planted error" in the form questions.

The charts are not yet that study. Five cases state the discharge action in the resident text. Eleven more need revision because a consult, a follow-up title, or a missing alternative still makes the decision for the resident, or because the chart cannot support the decision the reference scores. Six are close. Two match the design.

| Status | Count | Cases |
| --- | ---: | --- |
| PASS | 2 | VAL-814, VAL-821 |
| PASS_WITH_MINOR_CONCERN | 6 | VAL-802, VAL-806, VAL-807, VAL-813, VAL-815, VAL-817 |
| NEEDS_REVISION | 11 | VAL-801, VAL-804, VAL-805, VAL-808, VAL-809, VAL-812, VAL-816, VAL-819, VAL-820, VAL-822, VAL-823 |
| FAILS_KATIE_DESIGN | 5 | VAL-803, VAL-810, VAL-811, VAL-818, VAL-824 |

Counts: 24 audited. Detail is in `KATIE_DESIGN_CASE_MATRIX.csv`, `KATIE_DESIGN_ANSWER_LEAK_AUDIT.md`, and `KATIE_DESIGN_REFERENCE_EVIDENCE_AUDIT.md`.

## Part 1 — Resident task

A. Every current resident file is a clinical chart. None is only a completed discharge-medication answer sheet. Home and inpatient medication tables are present, and they are the right kind of evidence when the prose does not convert them into the answer.

B. No resident chart has a section titled Discharge medications, Intended discharge medications, Correct regimen, Expected medications, Reference plan, or Medication answer. The evaluator files have `reference_discharge_plan`. The codebooks show that table only after C2, under CLINICIAN VALIDATION REFERENCE.

C. Several charts still tell the resident the action. The direct examples are VAL-803 ("are continued. No discharge medicine is stopped."), VAL-810 and VAL-811 ("intended to continue after discharge"), VAL-818 ("Warfarin is intended to continue at discharge"), and VAL-824 ("intentional aspirin discontinuation"). The full list is in the leak audit.

D. Appropriate evidence is present in every chart: diagnosis, some course, home and inpatient medicines, and at least a few laboratories or vitals. That is not the same as enough evidence for the scored decision. VAL-803 still has no precipitant. VAL-805 is not back to dry weight and has no ejection fraction. VAL-804 discusses a cognitive enhancer that the reference does not score.

## Part 2 — Residual error-injection design

Searched the 24 resident JSON files for error-bearing, clean control, planted error, injected error, assessment discrepancy, intended problem, expected error, detectability, find the error, what is wrong, error family, Family 1, Family 2, f1_, f2_, and assessment target.

None of those labels appear in the active resident charts. They remain in historical places:

| Location | Classification |
| --- | --- |
| `data/case_sets/seed_guided/` and the Round 1 casebook | HISTORICAL_ONLY_OK |
| Round 1 feedback reproduced after the blank form in the Set 1 codebook, including C2 questions about an "intended problem" | HISTORICAL_ONLY_OK |
| README and `docs/methods.md` sections that are headed as Round 1 or historical | HISTORICAL_ONLY_OK |
| `docs/clinical_validation.md` C2–C4, which the page says are the Round 1 instrument | HISTORICAL_ONLY_OK |
| `docs/resident_review_package/README.md` C2 "Intended assessment problem" | HISTORICAL_ONLY_OK on a page that opens with "Historical validation design," but the heading itself can be read as current |

What does remain in active resident charts is the old design's answer language, without the old metadata labels. "Intended after discharge" in VAL-810, VAL-811, and VAL-818 is an `ACTIVE_STUDY_VIOLATION`. It is the predetermined plan written into the chart.

## Part 3 — Resident versus evaluator separation

For all 24 pairs, the resident object does not contain `reference_discharge_plan`. The only top-level key the evaluator adds in Set 1 is that plan.

Set 2 evaluators also carry `clinician_review_status` and `precheck_finding`. The nine corrected cases also carry `evidence_trace` and `revision_summary`. Those fields are absent from the resident files. They include labels such as `WEAK_EVIDENCE` and `READY_FOR_CLINICIAN_REVIEW`. They must stay out of any resident export.

No resident file contains `expected_action`, `evidence_class`, `supporting_evidence`, `medications_to_stop`, or planted-error metadata.

The separation fails in prose rather than in keys. A resident who never sees the evaluator file can still be told the action by the note, the consult, or the follow-up title. Those leaks are listed in the leak audit. Field-level medication comparisons are in the evidence audit.

## Part 4 — Can the resident reach the reference?

Summary. The evidence audit has one row per medication.

- Sufficient for the whole scored plan, with the real ambiguity encoded: VAL-814 and VAL-821.
- Sufficient for chronic medicines, with one explicitly weak or ambiguous decision that is encoded: VAL-802 and VAL-806.
- The reference action is visible only because the chart states it: VAL-803, VAL-810, VAL-811, VAL-818, and VAL-824.
- The reference conflicts with the chart: VAL-805 furosemide continued although discharge weight is 5 kg above dry weight; VAL-822 pantoprazole stopped although gastroenterology says to continue acid suppression.
- A decision the chart raises is missing from the reference: VAL-804 cognitive enhancer.

## Part 5 — Is the reference actually hidden?

File separation is intact. Wording is not. Direct leaks: VAL-803, VAL-810, VAL-811, VAL-818, VAL-824. Strong hints: VAL-801, VAL-804, VAL-808, VAL-809, VAL-812, VAL-815, VAL-816, VAL-817, VAL-819, VAL-822, VAL-823. Exact strings, fields, and the action each one reveals are in `KATIE_DESIGN_ANSWER_LEAK_AUDIT.md`.

## Part 6 — Facts that exist only because an error was needed

| Case | Fact | Would it belong if there had never been an error-injection study? |
| --- | --- | --- |
| VAL-803 | The evaluator rationale still explains a 7-day lisinopril supply. The resident chart no longer shows 7 days. | The 7-day supply was the injected discrepancy. It is gone from the resident chart. The rationale is evaluator-only. |
| VAL-810, VAL-811, VAL-818 | "Intended after discharge" / "intended to continue." | These sentences exist to announce a predetermined transition. They are not a clinical observation. |
| VAL-822 | Hidden stop of pantoprazole as an inpatient-only drug, against the consult. | A PPI after gastrointestinal bleeding is ordinary treatment. Stopping it solely because it started in the hospital is the old hospital-only pattern. |
| VAL-824 | "Intentional aspirin discontinuation," plus a consult about holding anticoagulation when the list has no anticoagulant. | Stopping aspirin for primary prevention after a bleed can be a real decision. The wording and the mismatched consult are leftover template text. |
| VAL-801 | Dry mucous membranes and a 20 mmHg orthostatic fall. | These were added in revision. They are not in the vital-sign table. They are synthetic teaching findings, not an injected medication error. |

The other injected discrepancies that Round 1 used, such as a shortened supply or a stopped statin that the clean list did not stop, are not in these resident charts.

## Part 7 — The six revised cases against both Round 1 and Katie's design

Round 1 source: the completed KO review of 10/5/2026, preserved in `exports/ko_cycle2_revised_validation_v2/round1_feedback/`. The current case is the version 2 chart in the linked codebook, not the different account in the README.

### VAL-801

- Round 1 concern: the cause of delirium is not shown, improvement is unexplained, and ibuprofen was stopped without an indication. Infection or gastrointestinal bleeding were examples.
- Round 2 change: poor intake, dry mucous membranes, and a 20 mmHg orthostatic fall were added. Ibuprofen is continued. Infection and bleeding were not added.
- Clinical problem resolved: PARTIAL. A precipitant is now named. The diagnosis line is still "Delirium due to known physiological condition." The new examination findings are not in the vital-sign table.
- Katie design preserved: NO.
- Answer leak introduced: YES. The course says there is no reason to stop ibuprofen. Geriatrics says to use the verified list at discharge.
- Remaining issue: the resident is told the ibuprofen decision.

### VAL-802

- Round 1 concern: no cause, an empty course, no baseline creatinine, confusing statin prose, and lisinopril should be stopped if the creatinine is acute kidney injury. Overall recommendation was Exclude.
- Round 2 change: poor oral intake is named. Creatinine 1.3 then 1.2 mg/dL is stated. No baseline was invented. The statin sentence that announced continuation was removed. Hold is an acceptable alternative.
- Clinical problem resolved: PARTIAL. The course is readable. The baseline the reviewer asked about is still absent, on purpose.
- Katie design preserved: YES.
- Answer leak introduced: NO.
- Remaining issue: lisinopril continuation is still a weak call, and the original review said the case might need to be excluded. The alternative is at least encoded.

### VAL-803

- Round 1 concern: the cause is not revealed. The medication list was called acceptable and no discharge change was requested. The reviewer asked about a 7-day lisinopril supply and the creatinine change. C2 through the overall rating were not completed.
- Round 2 change: creatinine 1.0 then 1.2 mg/dL is stated. The hidden duration is 30 days. The course says all four medicines are continued and none is stopped. No sodium series was added.
- Clinical problem resolved: NO. The missing cause remains.
- Katie design preserved: NO.
- Answer leak introduced: YES. The hospital course is the reference plan.
- Remaining issue: a resident does not have to decide anything.

### VAL-805

- Round 1 concern: discharge weight is not near dry weight, inpatient furosemide would be intravenous and increased, more intake/output days are needed, and the resident should decide about additional heart-failure therapy. An echocardiogram or a real cardiology recommendation was requested.
- Round 2 change: the weights were kept at 81 kg, 78 kg, and dry weight 73 kg. Furosemide stays 40 mg oral once daily. One intake/output day is stated. No ejection fraction was added. Extra therapy is only an acceptable alternative. The old "continue the intended plan" consult line was removed.
- Clinical problem resolved: NO. The chart now admits that it does not show decongestion or an intravenous regimen. It does not supply the course the reviewer said was required.
- Katie design preserved: NO.
- Answer leak introduced: NO as a direct order. The codebook then asks about an ejection fraction of 30 percent, which is not in the chart.
- Remaining issue: there is not enough information for the heart-failure medication decision, and the reference continues the same oral dose despite the weight gap.

### VAL-809

- Round 1 concern: the case should show fever and a predisposition such as a mechanical valve or poor dentition. Lisinopril should be held if there is acute kidney injury. The home list is too short.
- Round 2 change: fatigue, temperature 36.80°C, gram-positive cocci, a cleared culture, a vegetation, and creatinine 1.3 then 0.8 mg/dL are written into the course. Fever, a valve, and dental disease were not added. Lisinopril stays continued, with hold acceptable.
- Clinical problem resolved: PARTIAL. The recorded evidence is visible. The presentation the reviewer asked for was not added.
- Katie design preserved: NO.
- Answer leak introduced: YES. Infectious disease says to complete the planned parenteral course.
- Remaining issue: the antibiotic decision is announced, and the endocarditis picture is still afebrile fatigue plus a vegetation.

### VAL-813

- Round 1 concern: valganciclovir should not already be an admission medicine if this is a new CMV diagnosis. The transplant regimen is too simple. Potassium changes without a cause.
- Round 2 change: valganciclovir was removed from the home list and starts at 900 mg twice daily after the admission viral-load result. Mycophenolate was not added. Potassium 4.7 then 3.9 mmol/L is stated without a cause.
- Clinical problem resolved: PARTIAL. The chronology matches a new diagnosis. The regimen is still only tacrolimus plus two non-immunosuppressants.
- Katie design preserved: YES.
- Answer leak introduced: NO. The course describes inpatient treatment that already happened. It does not say "discharge on this list."
- Remaining issue: the codebook asks whether to continue mycophenolate, and mycophenolate is not on the chart. Potassium remains unexplained.

## Part 8 — Codebooks

Both current codebooks use the same form order:

resident-facing chart, then C1 clinical plausibility, then C2 sufficiency for an independent discharge decision, then CLINICIAN VALIDATION REFERENCE, then C3 reference validity, C4 acceptable alternatives, C5 competing issues and answer reveal, C6 difficulty, and an overall recommendation.

Checked in the published files: "Not shown to residents in the assessment study" appears once per case, and "Complete C1 and C2 before using this reference" appears once per case. Set 1 has 6 of each. Set 2 has 18 of each. Neither codebook says, in those words, that the opening chart is the same information the resident would see. C2 implies it. That sentence should be explicit.

The reference is allowed in the clinician codebook. The sequence does not make the reviewer score the chart only by comparing it with the answer, provided the reviewer follows the instruction to finish C1 and C2 first. Set 1 then prints the historical Round 1 form, including its planted-problem questions. That material is after the blank Round 2 form. It is historical. It will bias a reviewer who reads ahead.

Two Set 1 adjudication questions do not match the version 2 chart:

- VAL-805 asks about an ejection fraction of 30 percent. The version 2 chart has no ejection fraction.
- VAL-813 asks about continuing or holding mycophenolate. The version 2 chart has no mycophenolate.

Those questions are in the shared form, which was written for `ko_revised_cases_v1`. They are attached to a different chart.

Set 2 special questions for VAL-806, VAL-814, VAL-820, and VAL-821 match the Set 2 charts. VAL-820 and VAL-823 raise a second defensible action that the evaluator `acceptable_alternatives` list does not store. The form asks the reviewer. The scoring file would still mark the alternative wrong until it is encoded.

## Part 9 — README and study documents

The opening of `README.md`, `docs/methods.md`, and `docs/clinical_validation.md` does describe the intended design: clean chart, resident decides, hidden reference, later comparison. Round 1 error detection is mostly labeled historical.

These passages conflict with the cases a reviewer is told to open, or they can be read as the current task.

| File | Section | Text | Why it conflicts | Suggested correction |
| --- | --- | --- | --- | --- |
| README.md | Round 2 detailed revision record, VAL-802 | "A creatinine of 1.2 mg/dL six weeks earlier is the renal baseline." | The linked version 2 chart says no earlier creatinine is recorded. | Describe the chart in the linked codebook, or point the codebook at the package this paragraph describes. |
| README.md | same section, VAL-803 | "Sodium is 128 mmol/L ... Hydrochlorothiazide is held ... The reference plan stops hydrochlorothiazide." | Version 2 has no sodium values, continues hydrochlorothiazide, and the resident course says no medicine is stopped. | Same correction. |
| README.md | same section, VAL-805 | Weights 86 to 80 kg, intravenous furosemide 40 mg twice daily, ejection fraction 30 percent. | Version 2 keeps 81 kg, 78 kg, dry weight 73 kg, oral furosemide 40 mg daily, and no ejection fraction. | Same correction. |
| README.md | same section, VAL-809 | Fever 38.6°C, dental extraction, viridans streptococcus, lisinopril held and then restarted. | Version 2 temperature is 36.80°C, the organism is gram-positive cocci, and lisinopril is continued. | Same correction. |
| README.md | same section, VAL-813 | The patient is taking mycophenolate, and the reference continues it. | Version 2 has no mycophenolate. The codebook still asks about it. | Same correction. |
| README.md | Where to find the cases | The resident and evaluator examples link to `exports/ko_revised_cases_v1/VAL-801_*.json`. | Those files are not the charts in the linked Set 1 codebook. | Link the JSON pair that the current codebook renders. |
| README.md | Evidence check before review | "VAL-806 is the only decision currently marked WEAK_EVIDENCE. ... No current case is held for a hidden dependency." | Version 2 VAL-803 states the answer. VAL-805 continues a diuretic the weights do not support. Several Set 2 charts leak the action. The sentence treats the design check as already passed. | Say that the check did not include the wording audit in this folder, and do not claim that no hidden dependency remains. |
| docs/clinical_validation.md | Materials | "The packet shows the chart and the intended target." | A reader can take this as the current resident task. The page does say the C1–C5 table is Round 1. | Put "Round 1 only" in that sentence. |
| docs/resident_review_package/README.md | What is being validated, C2 | "Where an intended problem is specified for formal validation, is it actually present" | This is the old detection task. The page header says the page is historical, and it also links the current Round 2 codebooks. | Title the C2–C5 block "Round 1 questions, not the current resident task." |
| docs/methods.md | Current resident workflow and the numbered pipeline | The first section matches Katie. Steps 8–10 still say "Inject exactly one predetermined discrepancy." | The pipeline is labeled historical. It is easy to miss that label because it follows the current-workflow section. | Keep the label, and add one sentence that VAL-801–VAL-824 Round 2 charts are not produced by step 9. |
| data/active_validation_sets.md | Current case sets | Points at the README for the Cycle 2 casebook and calls the frozen sets historical. | This page matches Katie. No correction. | None. |
| docs/README.md | Documentation index | Sends the reader to the root README for Round 2 and labels the resident-review page as Round 1. | This page matches Katie. The root README it trusts does not match the linked charts. | Fix the root README case narratives. |

## Part 10 — Which direction the case was built in

`CASE_DRIVES_REFERENCE`: VAL-802, VAL-806, VAL-807, VAL-814, VAL-815, VAL-817, VAL-820, VAL-821. The visible illness supports the reference, and the reference was not used to invent a contradictory fact.

`REFERENCE_APPEARS_TO_DRIVE_CASE`: VAL-803, VAL-810, VAL-811, VAL-818, VAL-822, VAL-824. Either the note lists the reference actions, or a template sentence announces the predetermined transition, or the reference stop contradicts the consult.

`UNCLEAR`: VAL-801, VAL-804, VAL-805, VAL-808, VAL-809, VAL-812, VAL-813, VAL-816, VAL-819, VAL-823. These mix source facts with a sentence or a synthetic finding that was added to make one plan easier to see.

## Part 11 — More than one reasonable plan

| Case | Medication | Reference action | Reasonable alternative | Why both can be defended | Encoded? |
| --- | --- | --- | --- | --- | --- |
| VAL-802 | Lisinopril | continue | hold | Creatinine 1.3 then 1.2 mg/dL and no baseline. | YES |
| VAL-805 | Furosemide | continue 40 mg oral daily | increase the dose or do not discharge at this weight | Discharge weight is 78 kg and dry weight is 73 kg. | NO |
| VAL-805 | Additional heart-failure class | not required | start an ACE inhibitor, ARNI, SGLT2 inhibitor, or MRA | Discharge creatinine is 0.9 mg/dL and potassium is 4.3 mmol/L, but there is no ejection fraction. | YES, as one grouped alternative |
| VAL-806 | Lisinopril | restart | continued hold | Creatinine is still 1.6 mg/dL and no baseline is known. | YES |
| VAL-807 | Furosemide | continue | reduce the dose | Discharge weight is 93 kg and dry weight is 95 kg. | NO |
| VAL-809 | Lisinopril | continue | hold | Creatinine fell from 1.3 to 0.8 mg/dL without a baseline. | YES |
| VAL-813 | Tacrolimus | continue | temporary reduction | No trough is recorded during CMV disease. | YES |
| VAL-813 | Mycophenolate | absent | continue, reduce, or hold | The drug is not on the chart, so the question cannot be answered. | NO |
| VAL-814 | Mycophenolate | restart | continued hold | Viral burden is lower, not described as cleared. | YES |
| VAL-816 | Tacrolimus | continue | temporary reduction during CMV | Infection is improving but still the reason for admission. | NO |
| VAL-818 | Warfarin | continue | hold or reduce | Admission hemoglobin was 7.9 g/dL. | NO |
| VAL-819 | Warfarin | continue | longer postoperative hold | Hip surgery with a recent interruption. | NO |
| VAL-820 | Enoxaparin | stop | brief overlap with warfarin | INR has been 3.2 and is 2.0 at discharge after a bleed-range hemoglobin. | NO |
| VAL-821 | Apixaban | restart | continued hold until gastroenterology | Hemoglobin was 8.7 g/dL and follow-up is in 7 days. | YES |
| VAL-822 | Pantoprazole | stop | continue after the bleed | The consult says to continue acid suppression. | NO |
| VAL-823 | Apixaban | hold | restart | Bleeding has stopped and hemoglobin is 10.2 g/dL. | NO |

VAL-806, VAL-814, and VAL-821 are the cases in which the design already allows more than one answer. VAL-805, VAL-813, VAL-820, and the apixaban/PPI cases around them do not yet do that consistently. VAL-813 cannot, until the chart either includes mycophenolate or the question is withdrawn.

## Part 12 — Bottom line

1. Cases audited: 24.
2. PASS: 2.
3. PASS_WITH_MINOR_CONCERN: 6.
4. NEEDS_REVISION: 11.
5. FAILS_KATIE_DESIGN: 5.

Cases that fully match Katie's design: VAL-814, VAL-821.

Cases with answer leakage: VAL-801, VAL-803, VAL-804, VAL-808, VAL-809, VAL-810, VAL-811, VAL-812, VAL-815, VAL-816, VAL-817, VAL-818, VAL-819, VAL-822, VAL-823, VAL-824.

Cases with hidden-reference dependency or a reference the chart does not support: VAL-803, VAL-804, VAL-805, VAL-822.

Cases that still contain old error-injection answer text: VAL-810, VAL-811, VAL-818, VAL-822, VAL-824. The metadata words planted, f1_, and f2_ are not in the resident charts.

Cases where the reference appears to drive the clinical wording: VAL-803, VAL-810, VAL-811, VAL-818, VAL-822, VAL-824.

Cases with more than one reasonable answer that is not encoded: VAL-805 furosemide, VAL-807 furosemide, VAL-813 mycophenolate, VAL-816 tacrolimus, VAL-818 warfarin, VAL-819 warfarin, VAL-820 enoxaparin, VAL-822 pantoprazole, VAL-823 apixaban.

### The six revised cases

VAL-801. Round 1 concern addressed: partial. Katie design satisfied: no. Remaining problem: the chart tells the resident not to stop ibuprofen.

VAL-802. Round 1 concern addressed: partial. Katie design satisfied: yes. Remaining problem: lisinopril is still ambiguous, and that ambiguity is at least encoded.

VAL-803. Round 1 concern addressed: no. Katie design satisfied: no. Remaining problem: the hospital course states the entire discharge plan, and the delirium still has no cause.

VAL-805. Round 1 concern addressed: no. Katie design satisfied: no. Remaining problem: the diuretic course does not support a discharge decision, and the codebook cites an ejection fraction the chart does not have.

VAL-809. Round 1 concern addressed: partial. Katie design satisfied: no. Remaining problem: the consult says to complete the antibiotic course, and the presentation is still not a febrile endocarditis case.

VAL-813. Round 1 concern addressed: partial. Katie design satisfied: yes. Remaining problem: mycophenolate is absent while the codebook asks about it.

NO CASES WERE MODIFIED DURING THIS AUDIT.
