# Combined clinician revision method

## 1. Rationale

Round 2 asks an internal-medicine resident to read a clean hospital chart and construct a discharge medication plan. Two clinician reviews showed that a chart can fail that purpose in more than one way. It can reveal the answer, or it can withhold the clinical material the resident would need in order to reason. Version 4 treats those as separate validity questions and requires a case to satisfy both before it is sent for clinician review.

## 2. Reviewer roles

Katie's review, preserved from the KO Round 1 casebook and its audited extract, addressed the assessment construct. The resident task is not to receive a finished discharge list and search it for a planted error. The resident receives the clinical chart, determines the discharge medication plan, and can later be compared with a hidden reference that clinicians have reviewed.

Alex's review is the completed seed-guided casebook identified by the file name and by the document property lastModifiedBy Sugerman, Alexander. The form's reviewer-code and date fields are blank. Alex completed C1, clinical plausibility, for four clean-control cases: VAL-801, VAL-805, VAL-809, and VAL-813. He did not complete C2 through C5 or an Accept, Revise, or Exclude decision for those cases. Those blanks stay blank. His comments are not copied onto cases he did not review.

The other twenty cases are examined with a general clinical-sufficiency rubric motivated by the finding that several charts were too thin for meaningful reasoning. That application is an investigator step. It is not an Alex case-specific judgment.

## 3. Two complementary validation dimensions

Task alignment asks whether the case implements the resident task. The chart is clean. The reference plan is hidden. Visible evidence supports each reference action. Prose does not announce the discharge regimen. When more than one action is defensible, the other action is encoded as an acceptable alternative. Facts are not invented to rescue a preferred reference.

Clinical sufficiency asks whether the hospitalization contains enough realistic detail for that reasoning. A case can meet the task rules and still be too sparse. A case can be clinically rich and still give the answer away.

| Task alignment | Clinical sufficiency | Interpretation |
| --- | --- | --- |
| Adequate | Adequate | Eligible for clinician review |
| Adequate | Inadequate | The case is clinically too sparse and is revised |
| Inadequate | Adequate | The assessment representation is revised |
| Inadequate | Inadequate | The case needs substantial reconstruction or is held |

## 4. Feedback extraction

Alex's checkbox states and comments were read from the Word content controls. An unchecked box stayed unchecked. An empty comment stayed empty. A second parse of the same file was compared with the stored JSON. Katie's comments were taken from the audited version 3 extract of the KO casebook, not rewritten from memory.

## 5. Case-level comparison

Each concern is kept with its reviewer. Overlapping comments are classified as concordant, complementary, or independent. Concordant means both reviewers identified the same defect. Complementary means the comments address different validity questions on the same case. Independent means the comment comes from only one source, including every Set 2 rubric row, which has no Alex case review.

VAL-805 is the clearest complementary pair. Katie's review required the discharge plan to be derivable from visible evidence and not handed to the resident, and also questioned an inpatient diuretic course that matched the home dose. Alex's review found that the heart-failure hospitalization did not investigate why the patient decompensated. Removing answer leakage would not have supplied that work-up, and adding a precipitant would not by itself have fixed a chart that announced the regimen.

## 6. Revision decision rules

Version 4 starts from canonical Set 1 version 3 for VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813, and from the recovered Set 2 charts for the other eighteen identifiers. It does not return to the error-bearing Round 1 files.

A requested fact is added only when the decision needs it, a narrower fact will not do, and the addition can be labeled. Katie's request for an intravenous furosemide dose and an ejection fraction on VAL-805 was not adopted, because those values are not in the source and the discharge decision can be represented as an alternative without them. Katie's request for fever, a prosthetic valve, or a named organism on VAL-809 was not adopted. Alex's example of a urinary infection on VAL-801 was not adopted; volume depletion with a negative infection screen was the precipitant already supported by the chart. Mycophenolate was not added to VAL-813, because it is not on that medication list.

## 7. Clinical evidence hierarchy

Changed clinical facts are classified as case source, repository source, database, clinical literature, or synthetic addition supported by literature. Terminology databases identify a drug or a test. They do not establish that a dose is appropriate.

## 8. Treatment of synthetic additions

A synthetic addition records the new fact, why it was necessary, the reviewer concern or rubric item it addresses, the literature that supports plausibility of that kind of finding, and a statement that the patient-specific value is synthetic. Literature is not described as the source of the number.

## 9. Reference-plan revision

The direction of revision is from the clinical case to the decision to the hidden reference. For each medicine the question is whether a resident could support the action from the resident-visible chart. Actions are classified as sufficient visible evidence, weak visible evidence, clinically ambiguous, hidden-reference dependency, or clinically inconsistent. An unsupported reference is changed before facts are invented to defend it. Version 4 included cases use only the first three of those classes.

## 10. Multiple defensible answers

When two actions are reasonable, the reference keeps one and the other is an acceptable alternative. The resident chart does not announce which one was chosen. Ambiguity is a property of the case, not a defect to be edited out.

## 11. Post-revision audit

After revision, each resident chart is searched for direct answer leaks and for leftover planted-error metadata. Each reference medicine is checked against the resident chart. Each synthetic fact is listed. Clinical sufficiency is answered as eight questions: the admission problem, the decision the resident must make, the evidence, the work-up, the treatment, the response, the decisions that remain, and whether that context is present without revealing the answer.

## 12. Criteria for clinician-review readiness

A case enters a clinician codebook when task validity and clinical sufficiency are each Pass or Pass with minor concern, and when direct answer leaks, hidden-reference dependencies, clinical inconsistencies, and unsupported synthetic facts are zero. Other cases are listed in the held file with the unresolved reason. Readiness for clinician review is not clinical validation. Some included cases are marked ready with declared uncertainty when a relevant fact, such as an ejection fraction, an organism species, a baseline creatinine, or an endoscopy, is deliberately absent and the alternative actions are encoded.

## 13. Versioning and provenance

Version 4 is a new package. Version 3 and the recovered Set 2 files remain in place. Round 1 planted-error casebooks remain historical. Source hashes are stored in the version 4 source manifest and are checked after the package is written.

## Manuscript summary

Cases were revised using two complementary forms of clinician feedback. One review focused on construct validity of the assessment task, specifically whether a resident could independently derive a discharge medication plan without being shown or cued toward the expected answer. A second review focused on clinical plausibility and information sufficiency, including whether the presentation, diagnostic work-up, treatment course, laboratory trends, and discharge context were detailed enough to support meaningful clinical reasoning. Reviewer comments were coded by case and revision domain and classified as concordant, complementary, or independent. Cases were revised from the preserved clean representation. Newly introduced synthetic findings were explicitly distinguished from recovered case data. The hidden reference plan was then re-evaluated from the resident-visible case, and clinically defensible alternatives were encoded where appropriate. Cases were returned for clinician review only when they satisfied both task-validity and clinical-sufficiency criteria.

No inter-rater reliability was calculated. The two reviews were not a consensus procedure. Alex's comments are reported only for the four cases in which his casebook contains ratings.
