# CliniProof

CliniProof is a research framework for creating and validating synthetic inpatient cases used to study discharge-medication decision-making and clinical reasoning. Each case is a synthetic hospitalization. It includes the information a clinician would ordinarily use when planning discharge: the presenting problem, relevant history, hospital course, laboratory and vital-sign trends, medicines taken at home, medicines used in the hospital, and follow-up context. The cases are not extracts from a medical record. Medication, diagnosis, and laboratory names are tied to standard terminologies. Ages, vital signs, and laboratory numbers are synthetic.

The intended resident task is to read one clean chart and independently determine a discharge medication plan. The resident may later be asked for a written rationale or a confidence rating. That response would then be compared with a hidden reference plan maintained by the research team. The reference is the investigator-facing proposal for what should happen to each medicine at discharge, together with the rationale for those actions. It is not shown to the resident. It has to be reviewed by clinicians before it can be used for comparison or scoring. A finished scoring program is not part of this repository.

```text
clean clinical case
        ↓
resident independently determines a discharge medication plan
        ↓
resident may provide reasoning and confidence
        ↓
response is later compared with a clinician-reviewed hidden reference
```

The resident is not shown a completed discharge medication list, and the resident is not asked to find a planted error. Passing the repository's automated checks does not mean a case is clinically validated. Passing automated validation does not establish clinical validity. A case that is prepared for clinician review has passed the internal task and sufficiency gates and is ready to be read. That internal status is sometimes stored as `READY_FOR_CLINICIAN_REVIEW` or `READY_WITH_DECLARED_UNCERTAINTY`. Neither code means a clinician has accepted the case.

## Current Round 2 v4 status

Round 2 is the current study. It contains 24 study slots, VAL-801 through VAL-824. The current revision is version 4, in `exports/ko_round2_combined_validation_v4/`. It was built from two complementary kinds of clinician feedback.

Task validity comes primarily from Katie's review. The question is whether the case matches the resident task and avoids revealing the discharge answer. Clinical sufficiency comes primarily from Alex's review. The question is whether the hospitalization contains enough clinically relevant detail to support meaningful reasoning. A case can satisfy one of those questions and still fail the other, so version 4 required both.

All 24 cases are prepared for clinician review under the version 4 protocol. Clinician adjudication is still pending. None of the cases has been clinically validated.

Three cases passed with no declared gap in the reference plan: VAL-808, VAL-816, and VAL-817. Their internal status is `READY_FOR_CLINICIAN_REVIEW`.

Twenty-one cases also passed every blocking internal check and are suitable for clinician adjudication, but one or more medication decisions remain clinically ambiguous or have more than one defensible answer. Their internal status is `READY_WITH_DECLARED_UNCERTAINTY`. That status does not mean the case failed. It means the uncertainty is written down, usually as an acceptable alternative or as a fact that was deliberately left uninvented, so a reviewer can judge it. Those cases are VAL-801, VAL-802, VAL-803, VAL-804, VAL-805, VAL-806, VAL-807, VAL-809, VAL-810, VAL-811, VAL-812, VAL-813, VAL-814, VAL-815, VAL-818, VAL-819, VAL-820, VAL-821, VAL-822, VAL-823, and VAL-824.

No case is held for revision, and no case was excluded from the current set.

## Current Round 2 v4 clinician review

Clinicians should use the two version 4 codebooks below. Each file is a fillable Word document. The resident-facing chart comes first. Historical comments and the revision record come after the blank form, so they do not anchor the new reading.

### Set 1 — cases revised from direct clinician feedback

[Download Set 1 clinician codebook](exports/ko_round2_combined_validation_v4/codebooks/CliniProof_Round2_v4_Set1_Clinician_Validation.docx)

Set 1 contains VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. These six cases received substantive earlier clinician feedback. Version 4 reassessed each of them against both task validity and clinical sufficiency. Where Alex completed a case, his C1 comments are reproduced after the blank form and are labeled as his. Katie's Round 1 comments, from the KO review, are reproduced in the same position and are labeled separately.

### Set 2 — remaining Round 2 cases

[Download Set 2 clinician codebook](exports/ko_round2_combined_validation_v4/codebooks/CliniProof_Round2_v4_Set2_Clinician_Validation.docx)

Set 2 contains VAL-804, VAL-806, VAL-807, VAL-808, VAL-810, VAL-811, VAL-812, VAL-814, VAL-815, VAL-816, VAL-817, VAL-818, VAL-819, VAL-820, VAL-821, VAL-822, VAL-823, and VAL-824. These eighteen cases were evaluated with the same task-validity rules and the same clinical-sufficiency rubric. Alex did not write case-specific comments for them, and the codebook does not attribute any comment to him. The rubric was an investigator application of the sufficiency questions raised by his review of the four clean controls.

### Investigator convenience copy

[Download combined investigator copy](exports/ko_round2_combined_validation_v4/codebooks/CliniProof_Round2_v4_Combined_Investigator_Copy.docx)

This file places the same twenty-four cases in one document for investigators who want a single copy. It is not the preferred clinician workflow.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word.

## How clinician feedback shaped v4

Katie and Alex did not perform the same review. Their comments answer different questions about whether a case is fit to use.

Katie's review, preserved from the KO Round 1 casebook, focused on construct and task alignment. The core finding was that the earlier workflow treated the resident task as error detection. In that design, a resident received a medication transition that might contain one deliberately inserted problem and was asked whether the problem was present and detectable. The intended task is different. The resident has to construct the discharge medication plan from the chart. That finding produced the version 4 task rules: the base case does not supply a discharge medication answer; it does not contain a planted error; it does not use wording that reveals the intended regimen; the reference plan stays hidden; every reference action has to be supportable from resident-visible evidence; and when more than one action is defensible, the others are encoded as acceptable alternatives rather than scored as wrong.

Alex's review focused on clinical plausibility and information sufficiency. His completed casebook records C1, the plausibility rating, for four clean-control cases: VAL-801, VAL-805, VAL-809, and VAL-813. He did not complete the later ratings or an overall accept, revise, or exclude decision, and those blanks were left blank. He did not review the other twenty cases. His comments showed that a chart can be free of a planted error and still be too sparse for meaningful reasoning. On VAL-801, delirium was not represented as a change from baseline with an interpretable precipitant. On VAL-805, the heart-failure story was recognizable but did not investigate why the patient had decompensated. On VAL-809, endocarditis was recognizable but lacked the work-up and management context a resident would use. On VAL-813, the chronology was backwards if the patient was said to present already labeled with cytomegalovirus colitis; symptoms should lead to the work-up, and the volume and electrolyte consequences of diarrhea need to be visible. The clinical-sufficiency rubric derived from that review was then applied systematically to every case, including the twenty he did not personally review. Those applications are labeled as investigator use of the rubric, not as Alex comments.

## Combined validation dimensions

Task validity asks whether the materials implement the resident task. Clinical sufficiency asks whether the hospitalization is detailed enough for that task. The combination is the rule used to decide whether a case could enter the version 4 codebooks.

| Task validity | Clinical sufficiency | Interpretation |
| --- | --- | --- |
| Adequate | Adequate | Prepared for clinician review |
| Adequate | Insufficient | Revise the clinical content |
| Insufficient | Adequate | Revise the assessment representation |
| Insufficient | Insufficient | Substantial reconstruction, or exclusion from the current set |

The full account of extraction, comparison, evidence classes, and readiness rules is in the [combined clinician-revision methodology](docs/combined_clinician_revision_method.md).

## How v4 cases were revised

Version 4 did not start from the old error-bearing charts. Set 1 started from the version 3 revised charts. Set 2 started from the recovered clean charts. For each case the sequence was the same. The preserved clean representation was read against the reviewer comment, or against the sufficiency rubric when there was no case-specific comment. The clinical gap was identified. Only the missing piece was added or the revealing sentence removed. The old and new wording were recorded. The clinical reason was recorded. The provenance of any new fact was recorded. The hidden reference was then re-read from the resident-visible chart. If two actions were reasonable, the second was encoded as an acceptable alternative. Task-validity and clinical-sufficiency audits were run before the clinician package was generated.

The direction of that work is fixed:

```text
clinical facts
        ↓
clinical reasoning
        ↓
discharge medication decision
        ↓
hidden reference plan
```

The opposite direction was not used. A desired reference action was not allowed to justify invented facts. If the chart could not support an action, the reference was changed or the action was marked ambiguous before any new fact was considered.

## Synthetic fact provenance

Synthetic details are allowed when a case cannot support reasoning without them. They have to be explicit. Version 4 added 23 new synthetic facts. Each one is listed in the evidence ledger with the reason it was needed, the reviewer concern or rubric item it addresses, and the literature that supports the plausibility of that kind of finding. The literature does not turn the patient-specific value into a recovered measurement. No unsupported synthetic fact remains in the clinician-ready set.

Some synthetic facts were already present in version 3 and were kept, still labeled as synthetic. They were not recovered from an original record. Examples are the standing systolic pressure on VAL-801, the sodium pair of 128 mmol/L then 135 mmol/L on VAL-803, and poor dentition on VAL-809. Version 4 did not add a fever, a dental extraction, a prosthetic valve, or a named organism to the endocarditis case, and it did not add an intravenous furosemide dose or an ejection fraction to the heart-failure case, because those values were not in the source and were not required once an alternative action could be encoded.

## Why the hidden reference is not always a single answer

Twenty of the twenty-four cases contain at least one clinically reasonable alternative to the primary reference action. The hidden reference is a proposed structure for later comparison. It is not an unquestionable answer, and it is not a gold-standard label. Where more than one discharge decision is defensible, one action is stored as the primary reference and the others are stored as acceptable alternatives. Clinician review is what determines whether those alternatives should be accepted. Ambiguity of that kind is part of real discharge decision-making, so the materials keep it visible instead of forcing a single action.

## Internal audit results

After revision, the resident charts and hidden references were audited again. Direct answer leaks are sentences that tell the resident the discharge action; the count is 0. Hidden reference dependencies are reference actions whose reason exists only in the hidden plan; the count is 0. Clinical inconsistencies are reference actions that contradict the visible chart; the count among included cases is 0. Unsupported synthetic facts, meaning new patient-specific values without a provenance label, are 0. Twenty cases carry at least one acceptable alternative, as described above.

The row-level results are in the [final readiness matrix](exports/ko_round2_combined_validation_v4/audit/FINAL_READINESS_MATRIX.csv), the [revision evidence ledger](exports/ko_round2_combined_validation_v4/revision/REVISION_EVIDENCE_LEDGER.md), and the [reviewer comparison matrix](exports/ko_round2_combined_validation_v4/method/REVIEWER_COMPARISON_MATRIX.md).

## What the clinician completes

Each version 4 case uses the same order. The reviewer sees the resident-facing chart and answers C1 and C2 before the reference appears. C1 asks whether the case is plausible and detailed enough for meaningful reasoning. C2 asks whether the chart contains enough clinically relevant information for an internal-medicine resident to determine a defensible discharge regimen independently. The hidden reference is then shown in a section marked as not for residents. C3 asks whether that reference is defensible. C4 asks whether another decision should also be accepted. C5 asks whether something is missing, misleading, or competing. C6 records expected difficulty. The overall recommendation is Accept, Revise, or Exclude.

```text
resident-facing chart
        ↓
C1 clinical plausibility and information sufficiency
        ↓
C2 sufficiency for an independent discharge decision
        ↓
hidden clinician validation reference
        ↓
C3 reference validity
        ↓
C4 acceptable alternatives
        ↓
C5 missing, misleading, or competing issues
        ↓
C6 expected difficulty
        ↓
Accept, Revise, or Exclude
```

Historical feedback and the clinical revision record are printed after that blank section. A reviewer can finish the new reading before seeing what an earlier reviewer said or how the chart was changed.

## Round 1, retained for provenance

Round 1 was the first formal clinician review of VAL-801 through VAL-824. Twenty of those cases were given one deliberately planted medication-reconciliation problem. Four were left as clean controls. Reviewers were asked whether the case was plausible, whether the intended problem was present and detectable, whether another problem competed with it, and how difficult the case seemed. That was a reasonable test of an error-injection design. It is not the resident task in the current study, which is why Round 2 returned to the preserved clean charts and changed the questions.

The Round 1 casebooks remain available so the earlier method can be reproduced. They should not be used for the current review.

[Round 1 seed-guided casebook, VAL-801–VAL-824](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx)

[Round 1 balanced casebook, VAL-701–VAL-724](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx)

[Round 1 review-package notes](docs/resident_review_package/README.md)

The frozen sources of those rounds are still in the repository and were not overwritten. The balanced structured set is [`CLINIPROOF_BALANCED_V4`](data/case_sets/balanced/README.md), VAL-701–VAL-724. The resident-seed-guided set is [`CLINIPROOF_SEEDCASES_V3`](data/case_sets/seed_guided/README.md), VAL-801–VAL-824. They are the Round 1 record from which the clean charts were recovered. They are not the files to give a resident now.

## Previous revision packages and provenance

Earlier review packages are kept so the path from Round 1 to version 4 can be audited. They are not the current clinician assignment.

[Set 1 version 3](exports/ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx), in `exports/ko_cycle2_revised_validation_v3/`, is the previous canonical six-case revision. It is superseded by Round 2 version 4. `exports/ko_cycle2_revised_validation_v2/` and `exports/ko_revised_cases_v1/` are earlier superseded revision attempts. `exports/ko_clean_cases_for_review_v1/` is the previous Set 2 preparation package and the starting point for the version 4 Set 2 charts. `exports/ko_cycle2_clean_validation/` is the Set 2 codebook from before the sufficiency revision. `exports/ko_cycle2_final_validation/` is the previous combined convenience copy. None of these directories was deleted.

## What this repository studies

The sections above are enough to open the current review. This section states the scientific question those files are built to answer, and the sections after it explain how cases are represented and generated.

CliniProof creates structured synthetic inpatient cases in which a resident must use the clinical presentation, hospital course, medication history, laboratory data, treatment response, monitoring needs, and follow-up context to determine an appropriate discharge medication plan. The central validation question is not whether a planted error can be detected. It is whether the chart contains sufficient and coherent clinical evidence for a resident to make a defensible discharge decision, and whether the hidden reference plan itself is clinically defensible.

The resident reviews the clean inpatient case and independently determines the appropriate discharge medication plan. The frozen source registry still lists two active prospective validation datasets, 48 case slots in all. Those frozen files are the Round 1 record that recovery read. They are not the files to give a resident, and they are not a claim that the Round 2 charts have already been accepted. The recovered resident-facing export of those same 48 slots is described with the validation materials below. Its audit labels 44 files ready for expert review and 4 clinically inconsistent. That count describes the recovered export only. It is not clinician approval, and it is not the Round 2 status of VAL-801 through VAL-824.

OpenAI is optional. It may only reword narrative from facts the structured generator has already chosen. It does not choose diagnoses, medications, doses, or the reference plan. The committed study cases used template wording. Neither original batch is a prevalence-weighted sample of hospital discharges. Human clinician review remains required before a case is used for scoring.

## Recorded case facts

The accounts below preserve the chart facts that distinguish each study slot. They are here so an investigator can see what the resident chart contains without opening every JSON file. They are not a second status report. Current readiness is the version 4 matrix linked above. None of these reference plans has been accepted by a clinician.

### Cases revised from Round 1 clinician feedback

Six study slots were rewritten because the first clinician review found a weakness in the clinical story itself, not only in the planted discrepancy. Each account below is the chart and the hidden reference that accompanies it.

#### VAL-801 — Delirium and poor oral intake

The resident chart describes several days of confusion, fatigue, and poor oral intake, and dry mucous membranes. Supine blood pressure on admission is 136/78 mmHg. A standing systolic pressure of 116 mmHg is recorded on its own vital row. That standing pressure is synthetic. The supine row is the source vital. Glucose is 163 mg/dL then 103 mg/dL. Creatinine is 1.1 mg/dL then 1.0 mg/dL. Ibuprofen 400 mg every 8 hours as needed is on the home list and the inpatient list. No melena or hematemesis is recorded. The chart does not say whether to stop ibuprofen. The hidden reference continues atorvastatin, lisinopril, metformin, and ibuprofen. Stopping ibuprofen is an acceptable alternative.

#### VAL-802 — Delirium and poor oral intake

Poor oral intake is the only precipitant named. Creatinine is 1.3 mg/dL on admission and 1.2 mg/dL at discharge. No creatinine from before this admission is recorded, and none was added. Blood pressure is 138/69 mmHg then 124/68 mmHg. Atorvastatin 40 mg daily is on the home list. The chart does not say to continue it. The hidden reference continues lisinopril and atorvastatin. Holding lisinopril is an acceptable alternative because no baseline creatinine is stored.

#### VAL-803 — Confusion with a synthetic sodium pair

Hydrochlorothiazide 25 mg daily is a source medicine. Sodium 128 mmol/L on admission and 135 mmol/L at discharge are synthetic values. They were not in the clean laboratories. Hydrochlorothiazide is on the home list and was not given after the admission sodium. The inpatient row is held. Confusion cleared. Creatinine is 1.0 mg/dL then 1.2 mg/dL. Potassium is 4.4 mmol/L then 4.2 mmol/L. Glucose is 149 mg/dL then 129 mg/dL. The resident chart does not state the discharge action. The hidden reference stops hydrochlorothiazide and continues lisinopril for 30 days, atorvastatin, and metformin. Restarting hydrochlorothiazide with planned sodium checks is an acceptable alternative. Holding lisinopril is an acceptable alternative. Round 1 stopped after C1, and the later form fields stay incomplete.

#### VAL-805 — Acute systolic heart failure

Admission weight is 81 kg. Discharge weight is 78 kg. Dry weight is 73 kg. One intake-and-output day is stored, hospital day 3, with intake 1418 mL, output 2463 mL, and net -1045 mL. Home and inpatient furosemide are both recorded as 40 mg oral once daily. No intravenous dose is recorded. Creatinine is 1.7 mg/dL then 0.9 mg/dL. Potassium is 4.7 mmol/L then 4.3 mmol/L. B-type natriuretic peptide is 1120 pg/mL then 369 pg/mL. Blood pressure is 109/82 mmHg then 110/84 mmHg. Oxygen saturation is 92 percent then 98 percent. No ejection fraction is recorded. The hidden reference continues oral furosemide 40 mg once daily. That continuation is ambiguous because discharge weight remains above dry weight. Increasing the loop diuretic, without a fabricated dose, is an acceptable alternative. Metoprolol succinate 25 mg daily and atorvastatin continue. An additional heart-failure drug class is acceptable and is not required.

#### VAL-809 — Infective endocarditis

The recorded symptom is fatigue for one week. Recorded temperatures are 36.80°C on admission and at discharge. No home fever was added. Poor dentition is a synthetic addition. No prosthetic valve was added. Blood culture grew gram-positive cocci, and a later culture showed no growth. The echocardiogram shows a vegetation with preserved ventricular function. Ceftriaxone 2000 mg intravenously once daily was started during the admission. No remaining duration is recorded. Creatinine is 1.3 mg/dL then 0.8 mg/dL. No creatinine from before this admission is recorded. The chart does not say to complete the antibiotic course and does not say what to do with lisinopril. The hidden reference starts ceftriaxone and continues lisinopril and atorvastatin. Holding lisinopril is an acceptable alternative.

#### VAL-813 — Cytomegalovirus after kidney transplantation

Valganciclovir is not a home medicine. The admission viral-load review detected CMV viral burden, and valganciclovir 900 mg twice daily, given as 450 mg tablets, was started after that result. A later review showed a lower viral burden. Home medicines are tacrolimus 1 mg every 12 hours, amlodipine 5 mg daily, and atorvastatin 40 mg daily. Creatinine is 1.2 mg/dL then 1.0 mg/dL. Potassium is 4.7 mmol/L then 3.9 mmol/L. No cause for the potassium change is recorded. No tacrolimus trough is recorded. The hidden reference starts valganciclovir and continues tacrolimus, amlodipine, and atorvastatin. A temporary tacrolimus reduction is an acceptable alternative. The chart does not contain another immunosuppressant, and the review question does not ask about one.

### Cases that needed narrower consistency corrections

Nine of the eighteen recovered clean cases were coherent enough to keep, but they contained a contradiction, a sentence that revealed the discharge answer, or a mismatch between the narrative and the medication data. They were not regenerated, and they were not treated as accepted cases. Each correction is a traceable copy of the recovered clean source. The copies that passed that earlier evidence check are in the recovered clean-case package. None of the nine remains held. Version 4 reassessed these cases with the same gates used for the full set, and they are included in the current Set 2 codebook. The nine are VAL-806, VAL-807, VAL-808, VAL-814, VAL-815, VAL-816, VAL-817, VAL-820, and VAL-821.

#### VAL-806 — Lisinopril after acute kidney injury

No prior creatinine existed in the source data, so none was invented. The sentence that told the resident to restart lisinopril was removed. The visible data are creatinine 2.8 then 1.6 mg/dL, potassium 4.5 mmol/L, systolic pressure 116 mmHg, and cardiology follow-up in three days. The hidden reference still restarts lisinopril from that visible course. The decision is flagged `WEAK_EVIDENCE` because creatinine is still elevated and no baseline is known. Continued hold is an acceptable alternative. Weak evidence did not keep the case out of review. A hidden dependency or a clinical contradiction would have.

#### VAL-807 — Diuretic continuation without an invented potassium product

The potassium-repletion claim was removed because no potassium product existed in the medication data. The measured potassium, 3.5 then 3.8 mmol/L, remains, as does creatinine 1.2 mg/dL. The phrase that named an intended outpatient diuretic dose was removed because it revealed the answer. The reference continues oral furosemide 40 mg daily, atorvastatin, and metoprolol. A potassium chloride product was not added.

#### VAL-808 — Heart failure without an invented diuretic change

The phrase that named an intended regimen was removed. The source home and inpatient loop-diuretic doses are the same, oral furosemide 40 mg once daily, so no dose change and no intravenous course were added. Observed weight falls from 94 kg to 92 kg, with one modest negative fluid-balance day, which does not support an 8 kg loss. Discharge weight stays 92 kg. The unsupported dry weight of 86 kg was the incorrect field, and it is corrected to 92 kg so that it matches the discharge weight. The reference continues oral furosemide 40 mg once daily together with spironolactone, lisinopril, and metoprolol. Creatinine is 0.9 mg/dL, potassium moves from 3.4 to 3.7 mmol/L, and discharge systolic pressure is 142 mmHg.

#### VAL-814 — New cytomegalovirus infection with a renal-adjusted dose

Valganciclovir was removed from the home list. Treatment begins after the in-hospital viral-load result. The inpatient dose is adjusted for kidney function: 450 mg once daily while creatinine is 2.5 mg/dL, then 450 mg twice daily at creatinine 1.6 mg/dL. A dose of 900 mg twice daily would not fit that creatinine. The sentence that told the resident to restart mycophenolate was removed. The hidden reference starts valganciclovir and restarts mycophenolate, because the later viral load is lower and the diarrhea is improving. A continued mycophenolate hold is an acceptable alternative. Tacrolimus and amlodipine continue.

#### VAL-815 — New cytomegalovirus infection without a tacrolimus dose change

The unsupported claim that the tacrolimus dose had been adjusted was removed. Home and inpatient tacrolimus both remain 1 mg every 12 hours. Creatinine is 0.8 then 0.9 mg/dL, and potassium is 4.6 then 4.5 mmol/L. Cytomegalovirus uses the same chronology as VAL-813. Valganciclovir is not a home medicine. It starts after the in-hospital viral load, at 900 mg twice daily, which the creatinine supports. The reference continues tacrolimus, amlodipine, lisinopril, and atorvastatin, and starts valganciclovir.

#### VAL-816 — Established cytomegalovirus treatment

This chart is the other chronology. The patient is already taking valganciclovir before admission, and the admission is a reassessment of improving diarrhea and fatigue rather than a new diagnosis. The source already described treatment that was underway and a duration that was still pending, which is why this case was not rewritten as a new infection. The sentence that left the decision sounding unfinished was replaced with infectious-disease follow-up. The reference continues valganciclovir 900 mg twice daily, tacrolimus, and atorvastatin.

#### VAL-817 — Warfarin without an extra anticoagulant

Implementation wording such as “in this profile” was removed. The enoxaparin sentence was removed because enoxaparin was not in the source medication record and the INR is already 2.6 on warfarin. The reference continues warfarin, lisinopril, and metformin. Hemoglobin moves from 9.0 to 10.1 g/dL, and glucose moves from 127 to 113 mg/dL.

#### VAL-820 — Enoxaparin as inpatient prophylaxis

The enoxaparin indication is inpatient venous-thromboembolism prophylaxis, not atrial fibrillation. The dose remains 40 mg subcutaneously once daily, and it is not a home medicine. Warfarin remains the medicine associated with atrial fibrillation. INR is 3.2 then 2.0, and hemoglobin is 8.3 then 11.1 g/dL. The reference stops the prophylactic enoxaparin. The reviewer is asked whether prophylaxis together with warfarin is appropriate at the documented INR. The atrial-fibrillation history was not changed.

#### VAL-821 — Apixaban after gastrointestinal bleeding

The sentences that told the resident to resume apixaban were removed, including goal text that named a restart. The chart shows the gastrointestinal bleed, hemoglobin 8.7 then 10.9 g/dL, atrial fibrillation, creatinine 1.2 mg/dL, weight 83 kg, gastroenterology follow-up in seven days, and systolic pressure near 140 mmHg. The hidden reference restarts apixaban 5 mg twice daily. A continued hold until the gastroenterology visit is an acceptable alternative.

These nine corrections did not by themselves accept the cases. They removed obstacles that would have made a review unfair, and they left the clinical judgments below for the reviewer. The table is the list of decisions that the form still has to settle.

| Case | Judgment still required |
| --- | --- |
| VAL-801 | Continue versus stop ibuprofen. No melena or hematemesis is recorded, and creatinine is 1.1 mg/dL then 1.0 mg/dL. |
| VAL-802 | Continue versus hold lisinopril. No creatinine from before this admission is recorded. |
| VAL-803 | Stop versus restart hydrochlorothiazide after sodium 128 mmol/L then 135 mmol/L. Continue versus hold lisinopril after creatinine 1.0 mg/dL then 1.2 mg/dL. |
| VAL-805 | Continue versus increase oral furosemide 40 mg once daily. Discharge weight is 78 kg and dry weight is 73 kg. No ejection fraction is recorded. Additional heart-failure medicines are acceptable and are not required. |
| VAL-806 | Lisinopril restart is `WEAK_EVIDENCE`. Continued hold is an acceptable alternative because no renal baseline is known. |
| VAL-813 | Whether the recorded valganciclovir dose is appropriate and whether tacrolimus should be temporarily reduced. No other immunosuppressant is on the chart. |
| VAL-814 | Restart versus continued hold of mycophenolate |
| VAL-820 | Whether separate enoxaparin prophylaxis is appropriate while the patient is receiving warfarin at the documented INR values |
| VAL-821 | Restart versus continued hold of apixaban after gastrointestinal bleeding |

### How those corrections were decided

Round 2 did not preserve an existing reference answer at all costs. When a medication decision could not be supported by information the resident can see, either the clinical representation or the hidden reference was corrected. Clinical facts determine the reference plan. Facts were not invented merely to justify a pre-existing answer. The sequence below is that rule. The implication is that a reference action which the chart cannot support was changed or explicitly marked as weak, rather than propped up with a new diagnosis or a new drug.

```text
clinical facts
    ↓
hospital course, laboratories, and treatment response
    ↓
medication decision
    ↓
hidden reference plan
```

### Evidence check before review

Every reference medication decision is checked against information visible in the resident chart. The internal labels are `SUFFICIENT_EVIDENCE`, `WEAK_EVIDENCE`, `HIDDEN_ANSWER_DEPENDENCY`, and `CLINICALLY_INCONSISTENT`. A decision is sufficient when every supporting phrase appears in the resident file and does not depend on the hidden plan. It is hidden when the reason exists only in the reference. It is clinically inconsistent when the chart contradicts the action. Weak evidence means the visible facts are thin but present. Weak evidence is recorded and does not by itself block review. A hidden dependency or a clinical contradiction does.

The version 3 re-audit of the six Set 1 cases is kept at [exports/ko_cycle2_revised_validation_v3/KATIE_REAUDIT.md](exports/ko_cycle2_revised_validation_v3/KATIE_REAUDIT.md). That earlier audit found no direct answer leak, no hidden-reference dependency, and no clinical contradiction in those six resident charts. Version 4 is the current package and repeated the audits for all 24 cases. Clinician reviewers still determine whether a reference plan is acceptable.

The preparation path for one study slot is drawn below. Historical frozen files remain available, and Round 2 does not overwrite them. VAL-701 through VAL-724 were not part of this cycle. Their recovered charts, including three inconsistent balanced cases, are unchanged.

```text
original frozen VAL case
        ↓
archived pre-injection clean source
        ↓
clean-source recovery
        ↓
Round 1 clinician feedback
        ↓
Round 2 revision or consistency correction
        ↓
resident chart and hidden reference
        ↓
Round 2 clinician review
```


## Resident-facing and investigator-facing representations

Every current case can be represented in two ways. The resident-facing representation contains only the clinical information needed to reason about discharge. It includes the presentation, diagnoses, hospital course, home and inpatient medications, laboratory and vital-sign trends, disposition, and relevant follow-up information. It does not include the proposed discharge medication answer. Home and inpatient medication lists are evidence about what has already been prescribed. They are not the regimen the resident is being asked to produce.

The evaluator representation contains the same underlying clinical case plus the hidden reference discharge plan. Clinicians use it when they validate the proposed answer, and investigators would use it later to compare a resident’s response with that answer. It must not be shown to a study participant. Where the recovered cases store the information, each reference medication includes the medicine, the action, dose, route, frequency, duration, indication, rationale, and any monitoring note on that row. The action is one of continue, start, stop, change, hold, or restart. The plan also lists monitoring requirements and follow-up requirements when those rows exist.

The table is the exposure difference. The implication is that a developer or a study coordinator can hand over the resident file and keep the evaluator file with the research team.

| Representation | Who may see it | What it adds |
| --- | --- | --- |
| Resident-facing chart | The resident, after a case is accepted | Clinical evidence only. No reference plan, expected actions, scoring labels, or planted-error metadata |
| Evaluator file | Clinicians and investigators | The same chart plus `reference_discharge_plan` |
| Round 2 casebook | The clinician reviewer | The resident chart first, then the reference, with blank C1 through C6 ratings |

A newly generated case, built by `app/services/resident_case.py`, can also store evaluator-only fields: `required`, `evidence_class`, `supporting_evidence`, `evidence_trace`, and `consistency_errors`. Those fields are not in the recovered 48-case files. `acceptable_alternatives` and `contraindications` exist on newly generated plans and are currently empty lists. `medications_to_stop` is filled only when a reference action is stop. The example below is the recovered plan for VAL-701, a synthetic heart-failure chart. It is not a real patient, and it is not a Round 2 case.

```json
{
  "medications": [
    {
      "medication": "lisinopril 10 MG Oral Tablet",
      "action": "continue",
      "dose": "10 MG",
      "route": "oral",
      "frequency": "once daily",
      "duration": null,
      "indication": "Essential (primary) hypertension",
      "rationale": "Home therapy is continued through discharge in the clean case.",
      "monitoring": null
    }
  ],
  "monitoring_requirements": [],
  "follow_up_requirements": [
    {
      "item": "Heart-failure clinic follow-up",
      "timing": "7 days",
      "with_service": "cardiology"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `medication` | Drug name as charted |
| `action` | Intended discharge action |
| `dose`, `route`, `frequency` | Intended administration |
| `duration` | Days’ supply or course length when the clean chart stored one. Often null |
| `indication` | Diagnosis or purpose stored on the medication row |
| `rationale` | Why the reference records that action. On the recovered set this is often the original generator sentence |
| `monitoring` | Monitoring text stored on that medication row, or null |
| `monitoring_requirements` | Case-level monitoring tasks. Empty when the clean chart had none |
| `follow_up_requirements` | Follow-up item, timing, and service |

`required`, `medications_to_stop`, `acceptable_alternatives`, and `contraindications` are part of the generator’s evaluator document. They are not fields in the recovered VAL-701 file above. The full evaluator file is [exports/clean_balanced_seed_set/VAL-701_evaluator.json](exports/clean_balanced_seed_set/VAL-701_evaluator.json). The matching resident file omits `reference_discharge_plan`.

After a clinician accepts a case, the later study would show the resident only the clean chart. The resident would construct a discharge medication plan from that chart. The reference, once clinicians have accepted it, would stay with the research team. The study may also collect a written rationale, a confidence rating, or a later response to computer-generated advice. Those collection tools are not implemented in this repository, and neither is a scoring engine. Any manipulated recommendation from a model would be a separate experiment, inserted after the resident’s first decision. It would not be written into the chart the resident reads first.

## Case generation and terminology

A clean case is assembled from a clinical scenario, not from a pasted discharge list. The generator assigns a structured profile, builds a synthetic encounter, and writes a hospital course, laboratories, treatments, and a medication history that are meant to agree with one another. It then keeps a hidden reference plan for the evaluator and runs consistency checks before a clinician ever sees the file. Default generation writes one clean case. It does not insert a medication error, and it does not write a second, corrupted case. The diagram is that construction order. The implication is that the reference plan is a consequence of the chart, not a list that the chart was written backward to justify.

```text
clinical scenario or resident-derived archetype
        ↓
structured clinical profile
        ↓
synthetic patient encounter
        ↓
clinical course, laboratories, treatment, and medication history
        ↓
clean resident-facing chart
        ↓
internal consistency and evidence checks
        ↓
hidden reference discharge plan
        ↓
clinician validation
        ↓
accepted case
        ↓
later resident assessment
```

Medication names are taken from RxNorm, and laboratory observations are tied to LOINC. Diagnosis text uses ICD-10-CM where the case stores a coded diagnosis. A source-backed terminology concept is not automatically a clinically appropriate choice for a particular synthetic patient. The code establishes identity. It does not establish that the dose, the indication, or the discharge action is the right one for the story. Curated regimens live in [data/bootstrap/medication_regimens.json](data/bootstrap/medication_regimens.json). The generator does not treat product strength as the administered dose and does not assume once daily. If a real medication has no curated regimen, generation fails rather than inventing a dose.

Laboratory import uses the LOINC FHIR value set at `http://loinc.org/vs`. The older URL `http://loinc.org?fhir_vs` returns 404 and is not the active endpoint. The FHIR base is `https://fhir.loinc.org`. `LOINC_USERNAME` and `LOINC_PASSWORD` are read from the environment or from a local `.env` file. `.env` is gitignored. Do not commit credentials. Empty LOINC credentials stop laboratory import. They do not stop a checkout of the frozen or recovered cases.

The two frozen batches that the registry still treats as active prospective datasets were chosen in different ways, and then built with the same terminology, regimens, and validation. Balanced structured generation and resident-seed-guided generation are those two labels. They are not two versions of the same batch.

| Case set | Cases | How the profiles were chosen | Frozen files |
| --- | ---: | --- | --- |
| [Balanced structured set](data/case_sets/balanced/README.md) | 24 | Balanced structured generation from predefined profiles | `CLINIPROOF_BALANCED_V4`, VAL-701–VAL-724 |
| [Resident-seed-guided set](data/case_sets/seed_guided/README.md) | 24 | Resident-seed-guided generation from six resident-authored archetypes | `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824 |

`CLINIPROOF_BALANCED_V4`, VAL-701 through VAL-724, uses predefined structured clinical profiles: heart failure, atrial fibrillation, hypertension, type 2 diabetes, and pneumonia. Each of the 24 assignments uses a different profile. The counts are a study-design choice. The set is not prevalence-weighted. `CLINIPROOF_SEEDCASES_V3`, VAL-801 through VAL-824, starts from six resident-provided cases that were abstracted into archetypes. The VAL charts are not copies of those source documents. The six workflows are medication-history uncertainty, acute heart-failure decompensation, endocarditis treated with outpatient parenteral antibiotics, kidney transplant with cytomegalovirus treatment, hip fracture with interruption and resumption of anticoagulation, and gastrointestinal bleeding with anticoagulation holds and restart decisions.

Readable Markdown for the frozen charts remains at [data/case_sets/balanced/readable/all_cases.md](data/case_sets/balanced/readable/all_cases.md) and [data/case_sets/seed_guided/readable/all_cases.md](data/case_sets/seed_guided/readable/all_cases.md). Those pages still show the historical charts, including discharge lists and, where one was introduced, the planted discrepancy. Do not use them as the current resident-facing study set. The historical validation artifacts are retained for provenance and reproducibility. They should not be used as the current resident-facing study set.

The default command generates clean cases. Pass `--scenario` when you want a family other than the first scenario in `data/bootstrap/scenarios.json`, which is currently `HF_INPATIENT`.

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --scenario HF_INPATIENT
```

Validate one persisted case with `clinical-case-generator validate-cases --case-id SYN-000001`. The historical frozen batches were built differently from this default. After the clean chart passed, the batch plan introduced one discrepancy for most cases and left four controls in each set of 24 unchanged. That step is experimental and optional. It is not part of the default resident-case pipeline.

## Historical error-injection framework

Earlier validation work used clean controls and deliberately injected medication-reconciliation discrepancies to test whether the software could represent one intended problem. That design is retained for provenance and for experimental tooling. It is not the current resident-facing study workflow, and it is not the task in the Round 2 casebook. A clean control, in that earlier design, was a chart that was left unchanged so that a reviewer could not assume every case contained a problem.

The command flag `--inject-error` is experimental, legacy, and optional. It is not part of the default resident-case pipeline, and it should not be used to generate the resident study set. The flag does not add an error label beside an otherwise clean chart. It changes the chart: a dose, a route, a frequency, a supply, a monitoring task, a follow-up, a restart instruction, or which drug is present. Restoring a clean case requires the pre-injection source. Deleting the metadata is not enough. The example below asks for one historical omission category. It is documentation of the old tool, not a recipe for the current cases.

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 42 --inject-error --error-category f1_omission
```

The historical categories are documented in [docs/error_taxonomy.md](docs/error_taxonomy.md). Family 1 changes the regimen itself. Its labels are `f1_omission`, `f1_commission`, `f1_dose_mismatch`, `f1_route_mismatch`, `f1_frequency_mismatch`, and `f1_therapeutic_substitution`. Family 2 changes the transition around the list. Its labels are `f2_monitoring_not_arranged`, `f2_held_med_no_restart_plan`, `f2_insufficient_supply`, `f2_hospital_only_continued`, `f2_inpatient_substitution_not_reverted`, and `f2_pending_decision_followup_missing`. A required companion medication omitted (`f2_coprescription_omitted`) is defined conceptually and is not implemented.

The five headings below are the ratings printed in the historical Word casebooks. They belong to Round 1. They are not the C1 through C6 questions in the current Round 2 form.

### C1 — Clinical plausibility

C1 asks whether the encounter is believable as charted, including the presentation, the course, and the medicines.

### C2 — Intended assessment problem

C2 asks whether a predetermined discrepancy, when one was injected, is actually present. A clean control should contain none.

### C3 — Detectability

C3 asks whether a resident could see that historical problem from the chart without the chart announcing the answer.

### C4 — No unintended clinically meaningful problem

C4 asks whether a second problem could be mistaken for the intended answer.

### C5 — Difficulty

C5 is advisory. It records how hard the historical case was expected to be for the intended learner. Accept. Revise. Exclude. are the recommendations in that historical casebook. They are not a claim that the recovered clean cases, or the Round 2 cases, have already passed that review.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word. The historical casebooks are [the balanced casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx) and [the seed-guided casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx). Do not give those casebooks to a resident. Each one prints a validation reference after the first rating.

## Validation and testing

Automated checks and clinician review answer different questions, and both appear in the repository because the project needs both. Structural validation can confirm schema completeness, terminology consistency, medication timeline consistency, answer leakage, whether the clinical evidence for a reference decision is visible in the resident chart, evidence sufficiency, and separation of the resident file from the evaluator file. `tests/test_clean_set_recovery.py` checks that recovery does not modify the frozen resident export. Those checks do not establish clinical correctness, whether a medicine should actually be restarted, whether an alternative should be accepted, educational appropriateness, or actual learner difficulty.

Clinical validation is the human reading described in the Round 2 casebook. A clinician still has to judge whether each medicine has an appropriate indication, whether the discharge action is justified by the chart, whether laboratories and monitoring fit the medicines, and whether the hidden reference is defensible. More than one regimen can be reasonable. Missing information, contradictions, inappropriate monitoring, and unsafe recommendations are reasons to exclude a case. Passing automated tests does not mean a case has passed clinician review.

The recovery audit of the original 48 slots is a separate statement from Round 2. [exports/clean_balanced_seed_set/](exports/clean_balanced_seed_set/AUDIT.md) is the resident-facing export of those slots. Forty-eight original case slots were recovered, and none were regenerated. Original seeds, scenarios, and profiles were preserved. The original frozen VAL files were not overwritten. Error-bearing cases were recovered from their archived pre-injection clean source, and clean controls used their original clean chart. The table is that recovery audit. It is not the Round 2 count, and it is not clinician approval.

| Status | Count |
| --- | ---: |
| Recovered from clean source | 48 |
| Reconstructed from seed | 0 |
| Minor cleanup | 3 |
| Clinically inconsistent | 4 |
| Unrecoverable | 0 |
| Ready for expert review | 44 |

Ready for expert review, in this recovery table, means the injected chart change and the discharge-answer wording are gone, and the automated clinical pass did not find a blocking inconsistency. It does not mean an expert has approved the case. The row-by-row record is [exports/clean_balanced_seed_set/AUDIT.md](exports/clean_balanced_seed_set/AUDIT.md).

Four files inside that export remain labeled `CLINICALLY_INCONSISTENT`. They were not rewritten there, and no replacement was generated. VAL-709, VAL-711, and VAL-714 stop or associate a medicine without a supported reason on that chart, and they were not part of Round 2. VAL-801 in the same export still stops ibuprofen without a visible reason. The current Round 2 chart for VAL-801 is in `exports/ko_round2_combined_validation_v4/`. The previous chart remains in `exports/ko_cycle2_revised_validation_v3/`.

| Case | Problem in the recovered export |
| --- | --- |
| VAL-709 | Ibuprofen is stopped without a visible clinical reason |
| VAL-711 | Ibuprofen is stopped without a visible clinical reason |
| VAL-714 | Pantoprazole is associated with hypertension, which is not a supported indication on that chart |
| VAL-801 | Ibuprofen is stopped without a visible clinical reason |

Three monitoring rows were put back rather than invented. VAL-703, VAL-707, and VAL-817 lost the INR monitoring row when historical error injection removed it, and the body of that row was not archived. Recovery restored it from two stored facts: the case’s own INR laboratory name, and the warfarin-monitoring frequency, trigger, and service text that the generator writes and that remains on the untouched clean control VAL-710. This did not add a new clinical fact. It restored the monitoring task the clean chart had before injection.

The same directory holds one resident file and one evaluator file for every identifier from VAL-701 through VAL-724 and from VAL-801 through VAL-824. `AUDIT.md` records the seed, the scenario, the recovery source, any cleanup, and the final status. Re-running generation with today’s code would not reproduce these files, because the default decision path has changed and because recovery refuses to draw a new case. Provenance of the terminologies and the seeds is described in [docs/provenance.md](docs/provenance.md).

The test commands below are how a developer checks that this separation still holds.

```bash
pytest
pytest tests/test_clean_resident_case.py
pytest tests/test_clean_set_recovery.py
```

`pytest` runs the full suite. It rebuilds the database schema and will wipe local case rows. `tests/test_clean_resident_case.py` checks that a default generated case has no injected error, that the resident document omits discharge-context medications and `reference_discharge_plan`, and that the evaluator document still has the reference. `tests/test_clean_set_recovery.py` checks that the original resident export is unchanged, that pre-injection content is restored, including VAL-701 lisinopril remaining a continue at 10 MG, that a known injected dose change is reversed, including VAL-708 atorvastatin at 40 MG rather than the planted 20 MG, and that recovered files are written to a separate directory.

Also used before a code change is considered complete:

```bash
ruff check .
mypy app
python scripts/check_docs.py
```

## Repository structure

The directories below are the ones a new collaborator is most likely to open. Application code builds and checks cases. `data/case_sets/` holds the frozen Round 1 sources and is not rewritten by Round 2. `exports/` holds the recovered 48-slot set and the current review packages. Methods and a longer directory map are in [docs/methods.md](docs/methods.md) and [docs/repository_structure.md](docs/repository_structure.md).

```text
app/services/generation.py            default clean-case generator
app/services/resident_case.py        resident chart versus hidden reference plan
app/services/validation.py            structural and coherence checks
app/services/error_injection.py       experimental chart discrepancies; not the default path
app/services/clean_set_recovery.py    rebuilds the 48 resident and evaluator files from frozen sources
app/services/ko_review_sets.py        Round 2 review copies for VAL-801–VAL-824
app/services/validation_batch.py      freeze and export of historical VAL batches
tests/test_clean_resident_case.py     clean generation hides the reference and does not inject an error
tests/test_clean_set_recovery.py      recovery leaves frozen files unchanged and restores known clean facts
tests/test_ko_review_sets.py          Round 2 packages hide the reference and leave frozen files unchanged
exports/clean_balanced_seed_set/      recovered 48-slot export; not overwritten by Round 2
exports/ko_revised_cases_v1/          superseded Set 1 revision attempt
    KO_REVISED_CASES_REVIEW.docx
    AUDIT.md
exports/ko_clean_cases_for_review_v1/ eighteen recovered clean cases; version 4 starting point, not the current codebook
    KO_CLEAN_CASES_REVIEW.docx
    AUDIT.md
exports/ko_held_cases_v1/             held audit; currently records zero held cases
    KO_HELD_CASES_AUDIT.md
exports/ko_cycle2_revised_validation/   earlier Round 1 extract and response matrix
exports/ko_cycle2_revised_validation_v2/ superseded Set 1 revision attempt
exports/ko_cycle2_revised_validation_v3/ previous canonical Set 1 revision, superseded by Round 2 version 4
    CliniProof_Cycle2_Revised_Cases_Validation.docx
    CLINICAL_REVISION_LOG.md
    REVISION_DIFF.md
    REVISION_EVIDENCE_LEDGER.md
exports/ko_cycle2_clean_validation/     earlier Set 2 package, superseded by the version 4 Set 2 codebook
exports/ko_round2_combined_validation_v4/ current Round 2 version 4 package
    codebooks/   Set 1 clinician codebook, Set 2 clinician codebook, combined investigator copy
    method/      reviewer comparison, combined review method, clinical sufficiency rubric
    revision/    case revision log, revision diff, evidence ledger
    audit/       task validity, clinical sufficiency, answer leakage, reference support,
                 synthetic facts, multiple answers, final readiness matrix
    cases/       resident and evaluator JSON for VAL-801–VAL-824
docs/combined_clinician_revision_method.md   manuscript-ready version 4 methodology
exports/ko_cycle2_final_validation/     previous combined convenience copy, not the current workflow
    CliniProof_Cycle2_Final_Validation.docx
```

Copy `.env.example` to `.env` before running the application. The settings it reads are the database URL, optional OpenAI credentials, and the LOINC account used only for laboratory import. The default database URL in code is `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases`. `SNOMED_BASE_URL`, `SNOMED_API_TOKEN`, and `MIMIC_LOCAL_PATH` are unused. SNOMED CT and MIMIC-IV are not ingested. `db-init` applies migrations. It does not rewrite committed case files.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
```

## Historical datasets and provenance

Earlier frozen batches are retained under [data/archive/validation_sets/](data/archive/validation_sets/README.md) so that an older experiment can be reproduced. They are not the current study set. The table names those archived batches and the historical identifiers they used. None of them is VAL-801 through VAL-824, and none of them is the Round 2 casebook.

| Historical batch | Archive directory | Historical identifiers |
| --- | --- | --- |
| `CLINIPROOF_TAXONOMY_V1` | `data/archive/validation_sets/CLINIPROOF_TAXONOMY_V1` | historical VAL-201–VAL-224 |
| `CLINIPROOF_BALANCED_V2` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V2` | historical VAL-301–VAL-324 |
| `CLINIPROOF_BALANCED_V3` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V3` | historical VAL-501–VAL-524 |
| `CLINIPROOF_SEEDCASES_V1` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V1` | historical VAL-401–VAL-424 |
| `CLINIPROOF_SEEDCASES_V2` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V2` | historical VAL-601–VAL-624 |

The frozen `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3` directories under `data/case_sets/` are also retained. They are the source of the recovery, not the current resident-facing export. Teaching charts that are not study cases are in [docs/clinician_walkthrough/README.md](docs/clinician_walkthrough/README.md). TEACH-002 shows one historical injected omission. It is not a recovered study case.

## Limitations

The cases are synthetic, and the scenario list is a bounded teaching set rather than a prevalence-weighted sample of hospital discharges. A terminology code does not prove that a dose is appropriate, companion-drug omission is not implemented, and the curated regimens are not a universal prescribing engine. There is no resident-review application and no finished scoring engine in this repository. SNOMED CT and MIMIC-IV are not ingested. The four inconsistent files inside the recovered 48-slot export are not ready for use as study cases. Round 2 does not change those files. The current VAL-801 chart is in the version 4 package and is prepared for clinician review. Clinician adjudication is still pending.

## Licensing

Terminology content is not bundled. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license. LOINC requires a Regenstrief account.
