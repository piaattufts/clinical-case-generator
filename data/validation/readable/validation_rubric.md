# CliniProof Clinical Case Validation Rubric

## Purpose

Two clinical reviewers independently evaluate each synthetic inpatient case before it is accepted for use in the resident assessment. The study method is independent dual expert review with structured consensus resolution. It is not a Delphi process.

Review proceeds in two stages.

1. Blinded clinical plausibility review. Both reviewers first receive only the resident-visible version of each case. They do not see whether the case is a control, the intended error family, the intended error category, the medication targeted by the assessment, the correct action, or any other answer-key field. They independently complete Criterion 1 (C1). Those ratings are submitted and locked before Stage 2 begins.
2. Assessment-target validation. After C1 ratings are locked, both reviewers receive the investigator packet that names the intended assessment target. They then independently complete Criteria C2 through C5 and record an overall recommendation of Accept, Revise, or Exclude.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. The frozen set is `CLINIPROOF_TAXONOMY_V1`, containing cases VAL-201 through VAL-224.

The five criteria serve different purposes and should not be collapsed into a single pass or fail judgment. C1 can be completed from the resident-visible chart alone. C2 through C4 are hard requirements: if any of them fails, the case cannot be used against its intended answer key until it is revised or excluded. C5 is advisory and must not by itself cause a case to fail validation.

The taxonomy also defines required companion medication omitted (`f2_coprescription_omitted`), which represents a situation in which a clinically required companion medication is missing. This category is not included in the current validation set because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category.

## C1 — Clinical plausibility

### Clinical question

Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

### Reviewer should look for

Both reviewers independently rate the following eight domains from the resident-visible chart only:

1. Presentation and demographics
2. Fit between presentation and diagnosis
3. Vital signs
4. Laboratory findings
5. Medication regimen
6. Hospital course
7. Consistency across the chart
8. Discharge plan and follow-up

Clinical plausibility is not the same as optimal management or complete guideline concordance. Unusual but source-backed formulations or units should be recorded if they undermine credibility. They should not be silently corrected in the frozen case.

### Scale for each domain

A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible.

Any domain rated 1 or 2 must include a written explanation that identifies the specific clinical concern.

Reviewers also answer the overall question: could this reasonably represent a patient encountered in the stated inpatient clinical setting? The allowed answers are Yes or No.

### Result

C1 passes when all clinically relevant domains are rated 3 or 4 and the overall clinical plausibility answer is Yes.

If any domain is rated 1 or 2, or if the overall answer is No, record that revision is needed for clinical plausibility.

On the Stage 1 form, record only:

- Clinically plausible
- Revision needed for clinical plausibility

Do not record Accept, Revise, or Exclude until Stage 2 is complete.

### Technical interpretation

C1 is a clinical-realism judgment on the resident-visible export. It does not inspect the concealed family or category fields. Software already checked schema, terminology identifiers, and implemented rules. C1 asks whether a physician still finds the chart coherent.

## C2 — Intended assessment problem

### Clinical question

Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess?

### Reviewer should look for

Determine whether the intended problem is present, whether it matches the intended category, and whether the investigator description accurately reflects the clinical case.

### Result

Record Pass or Fail. C2 is a hard requirement. If C2 fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

### Technical interpretation

This criterion checks fidelity of the deterministic injection to the planned standardized category. The planned category, the injected kind, and the answer-key category must describe the same visible target.

## C3 — Detectability

### Clinical question

Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case?

### Reviewer should look for

Consider whether all necessary evidence is available, whether important information is missing, whether the case is ambiguous, and whether wording or formatting gives away the answer. For Family 2, the trigger or precondition must be visible and unambiguous.

### Result

Record Pass or Fail. C3 is a hard requirement. A written explanation is required for a failure.

### Technical interpretation

This corresponds to evidentiary sufficiency and cue integrity in the CliniProof assessment model. The resident export must be sufficient without investigator fields.

## C4 — Absence of unintended problems

### Clinical question

Apart from the intended assessment problem, does the case contain another clinically meaningful medication-reconciliation or transition-of-care problem?

### Reviewer should look for

Reviewers must actively search for additional problems. This is not simply a record of problems that happen to be noticed. After reviewing the complete case, ask whether another clinically meaningful discrepancy is present that a reasonable resident could interpret as an assessment target.

### Result

Record Pass or Fail. C4 is a hard requirement. If the result is Fail, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful.

### Technical interpretation

Error isolation means exactly one intended assessment target on error-bearing cases and zero on clean controls. An unintended second target makes the answer key unusable.

## C5 — Expected learner difficulty

### Clinical question

How difficult would this case likely be for an internal medicine resident?

### Reviewer should look for

Provide a provisional expert estimate using Easy, Moderate, Hard, or Inappropriate / outlier.

This is an expert estimate of difficulty. Actual difficulty should ultimately be determined from resident performance.

### Result

C5 is advisory. It should not by itself cause a case to fail validation.

### Technical interpretation

Any prior difficulty field in the answer key is optional metadata, not a software-computed score.

## Family-specific guidance for C2 through C4

Criteria C2 through C4 must account for different clinical structures. Family 1 problems generally involve comparing home, inpatient, and discharge medication lists. Family 2 problems may leave those lists unchanged and instead omit a required transition action.

### Family 1 — medication-list and transition discrepancies

#### Medication omitted at discharge (`f1_omission`)

A medication intended to continue after hospitalization is absent from the discharge medication list without a documented reason.

#### Medication inappropriately added or continued (`f1_commission`)

A medication that should not be on the discharge list, for example one that was held or stopped, appears there without a documented decision to continue it.

#### Unexplained dose discrepancy (`f1_dose_mismatch`)

The discharge dose differs from the intended continued dose without an explanation.

#### Unexplained route discrepancy (`f1_route_mismatch`)

The discharge route differs from the intended continued route without an explanation.

#### Unexplained frequency discrepancy (`f1_frequency_mismatch`)

The discharge frequency differs from the intended continued frequency without an explanation.

#### Unexplained therapeutic substitution (`f1_therapeutic_substitution`)

The discharge list replaces an intended continued medication with another agent of the same class without documenting an intentional switch.

### Family 2 — transition-of-care gaps

These problems may involve absence of monitoring, follow-up, supply, restart planning, or another transition action. Do not identify Family 2 solely by comparing medication lists. For Family 2, the trigger or precondition must be visible, and the missing companion action is the specified target.

#### Required outpatient monitoring not arranged (`f2_monitoring_not_arranged`)

Warfarin is continued at discharge, but outpatient INR monitoring has not been arranged. In CliniProof this is classified as a Family 2 transition-of-care gap because the medication order itself remains unchanged; the missing element is the required follow-up action.

#### Held medication without a restart plan (`f2_held_med_no_restart_plan`)

A home medication is intentionally held in the hospital for a legitimate temporary reason, but discharge documentation does not say when or under what conditions it should be resumed.

#### Insufficient medication supply (`f2_insufficient_supply`)

Days’ supply at discharge is too short to last until the planned follow-up. The medication identity on the list may be correct; the missing element is enough supply to bridge to the next visit.

#### Hospital-only medication continued after discharge (`f2_hospital_only_continued`)

A medication started for an inpatient-only indication is still on the discharge list. Reviewers should notice that a hospital-only product was not stopped at the transition home.

#### Temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`)

A temporary inpatient substitute was used, but discharge does not revert to home therapy or document an intentional decision to continue the substitute.

#### Follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`)

A treatment decision was left pending, but no follow-up is arranged to resolve it. The medication list may look intact, but the chart does not say when or by whom the unresolved decision will be revisited.

#### Required companion medication omitted (`f2_coprescription_omitted`)

The taxonomy also defines this category for a situation in which a clinically required companion medication is missing. This category is not included in the current validation set because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category.

## Reviewer recommendation

Each reviewer records one independent recommendation after completing C1 through C5. Consensus is not a recommendation option on this form.

☐ Accept

☐ Revise

☐ Exclude

Accept means the case is suitable for use without clinically meaningful revision. Revise means the case requires one or more changes before it should be used. Exclude means the case should not be used in the validation set because its problems cannot be reasonably corrected without substantially reconstructing it.

If revision is requested:

### Recommended revision

____________________________________

### Clinical reason for revision

____________________________________

Recommended revisions are required whenever Revise is selected. Examples may include changing an implausible formulation, clarifying the hospital course, correcting an unrealistic laboratory unit, adding information needed to detect the intended problem, or removing an unintended second discrepancy.

Do not automatically modify a case based on reviewer comments. Human review comments are recommendations that must be considered by the study team. Do not overwrite the frozen CLINIPROOF_TAXONOMY_V1 case files during human review. Reviewer comments and revision requests should be stored separately.

## Consensus review

Complete only when independent reviewers disagree.

Reviewer A initial recommendation:

Reviewer B initial recommendation:

Areas of disagreement:

Consensus discussion summary:

Consensus outcome:

☐ Accepted

☐ Revision required

☐ Excluded

☐ Unresolved

Preserve both original independent ratings. Show both reviewers the areas of disagreement. Discuss the clinical rationale. Record a consensus outcome separately. Do not overwrite original reviewer ratings with the consensus result.

If the two reviewers cannot reach consensus, mark Unresolved. Do not automatically accept the case. An unresolved case is not considered clinically validated. It may receive an additional clinical opinion if one becomes available, or it may remain excluded from the clinically validated set.

Structured consensus review is required when reviewers disagree on C1 pass versus revision needed, when either reviewer fails C2, when reviewers disagree on C2, C3, C4, or Accept / Revise / Exclude, or when clinically important reviewer comments conflict. Cases with agreement require no consensus discussion unless the investigators choose to review them.

If the consensus outcome is Revision required, record the specific requested revision, the reason, the criterion affected, and the date or version of the revision. After the case is revised, it should be reviewed again. Only the criteria affected by the revision need to be repeated unless the change materially alters the whole case. If a revision changes the clinical presentation, medication regimen, target discrepancy, evidence needed to detect the problem, or answer key, then repeat the relevant C1 through C4 assessments.
