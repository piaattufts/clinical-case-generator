# Clinical Validation Protocol

This protocol describes independent dual expert review with structured consensus resolution for the frozen CliniProof validation set whose batch code is `CLINIPROOF_TAXONOMY_V1`. The set contains twenty-four synthetic inpatient cases labeled VAL-201 through VAL-224. The method is not a Delphi process and is not a modified Delphi process.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

### Reviewers

Two clinical experts independently review all 24 cases. There is no third reviewer in the primary protocol. Each reviewer records original ratings before any discussion occurs. Those original ratings must be preserved.

### Round 1: blinded plausibility assessment

Both reviewers review the resident-facing cases and complete C1 before seeing the answer key. They use [`plausibility_only_packet.md`](plausibility_only_packet.md). They do not see whether a case is a control, the intended error family, the intended error category, the medication targeted by the assessment, the correct action, or any other answer-key field.

They score eight domains on a 1-to-4 scale and answer whether the chart could reasonably represent a patient encountered in the stated inpatient clinical setting. C1 ratings are submitted and locked before Round 2 begins. The Stage 1 result is Clinically plausible or Revision needed for clinical plausibility. Accept, Revise, and Exclude are not recorded at this stage.

### Round 2: assessment validation

After C1 ratings are locked, both reviewers receive the investigator target in [`clinician_validation_packet.md`](clinician_validation_packet.md) and independently complete C2 through C5 and their overall recommendation. C2 asks whether the intended assessment problem is present and correctly described. C3 asks whether an internal medicine resident could detect and resolve that problem from the case documents alone. C4 requires an active search for another clinically meaningful medication-reconciliation or transition-of-care problem. C5 is an expert estimate of expected learner difficulty and is advisory.

The independent recommendation is Accept, Revise, or Exclude. If Revise is selected, recommended revisions are required. Reviewer comments are recommendations for the study team. They do not automatically change frozen case files.

### Consensus

Disagreements on clinically meaningful criteria or final recommendation are discussed after independent review. Original ratings remain unchanged. A separate consensus outcome is recorded on [`consensus_worksheet.csv`](consensus_worksheet.csv), not on the independent reviewer row.

Structured consensus review is used when reviewers disagree on C1 pass versus revision needed, when either reviewer fails C2, when reviewers disagree on C2, C3, C4, or Accept / Revise / Exclude, or when clinically important reviewer comments conflict. Cases with agreement require no consensus discussion unless the investigators choose to review them.

During consensus review, both original independent ratings are preserved, both reviewers are shown the areas of disagreement, the clinical rationale is discussed, and a consensus outcome is recorded separately as Accepted, Revision required, Excluded, or Unresolved. Consensus is not itself a case disposition on the independent form.

### Revisions

Reviewers may request specific changes. Cases requiring revision are corrected only after the initial ratings have been recorded. Revised cases are then reviewed again as appropriate. Only the criteria affected by the revision need to be repeated unless the change materially alters the whole case. If a revision changes the clinical presentation, the medication regimen, the target discrepancy, the evidence needed to detect the problem, or the answer key, then the relevant C1 through C4 assessments are repeated.

Do not silently modify the frozen CLINIPROOF_TAXONOMY_V1 case files. For the current validation study, the existing frozen cases remain the original validation candidates. Reviewer comments and revision requests should be stored separately from those frozen source files.

### Unresolved cases

If consensus cannot be achieved, the case is not considered clinically validated. It may receive another expert opinion if available or be excluded. An unresolved case must not be treated as accepted.

## Agreement reporting

Planned agreement reporting uses raw agreement for C2 through C4, raw agreement for the overall recommendation, and weighted Cohen's kappa for ordinal C1 ratings where appropriate. Weighted Cohen's kappa may optionally be reported for C5.

Because the validation set contains only 24 cases, agreement coefficients will be interpreted alongside the underlying counts and percentage agreement rather than as standalone evidence of reliability.

Do not overclaim statistical reliability. Kappa is not a criterion for whether a case passes validation. Case-level decisions remain the independent ratings, the separate consensus outcome when discussion occurs, and the study team's subsequent handling of requested revisions.

Independent ratings are recorded on [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv). Consensus outcomes are recorded on [`consensus_worksheet.csv`](consensus_worksheet.csv). Criterion definitions are in [`validation_rubric.md`](validation_rubric.md).
