# CliniProof clinician-validation rubric

This rubric is for clinician and investigator review of the frozen validation set whose batch code is `CLINIPROOF_TAXONOMY_V1`, which contains cases VAL-201 through VAL-224. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

The five criteria serve different purposes, and they should not be collapsed into a single pass/fail judgment.

Clinical plausibility (C1) can be completed from the resident-visible chart alone. It is fixable: a case that is implausible should be revised rather than scored as an assessment item.

Criteria C2 through C4 are hard gates. They require the concealed assessment specification in the investigator packet. A failure means the case cannot be used against its intended answer key until it is fixed or retired.

Difficulty (C5) is advisory. It must not by itself reject a case.

The taxonomy also defines required companion medication omitted (`f2_coprescription_omitted`), which represents a situation in which a clinically required companion medication is missing. This category is not included in the current validation set because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category.

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

Days’ supply at discharge is too short to last until the planned follow-up.

#### Hospital-only medication continued after discharge (`f2_hospital_only_continued`)

A medication started for an inpatient-only indication is still on the discharge list.

#### Temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`)

A temporary inpatient substitute was used, but discharge does not revert to home therapy or document an intentional decision to continue the substitute.

#### Follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`)

A treatment decision was left pending, but no follow-up is arranged to resolve it.

#### Required companion medication omitted (`f2_coprescription_omitted`)

This category is specified conceptually. It is not currently implementable because no source-backed companion-prescription rule exists in this repository.

## Criterion 1 — Clinical plausibility — fixable

### Clinical question

Apart from any intentionally planted reconciliation discrepancy, could this case reasonably represent a patient encountered in the stated clinical setting?

### Reviewer should look for

Assess the following domains independently: presentation and demographics; diagnosis-presentation coherence; vital signs; laboratory findings; medication regimen; hospital course; cross-document consistency; and discharge context and follow-up.

Clinical plausibility is not synonymous with optimal management or complete guideline concordance. Unusual but source-backed formulations or units should be recorded if they undermine credibility. They should not be silently corrected in the frozen case.

### Scale for each domain

A rating of 4 means fully plausible, with no clinically meaningful concern. A rating of 3 means plausible with minor concern: an issue is present but would not materially alter interpretation. A rating of 2 means questionable: a clinically meaningful inconsistency or implausibility is present and the case requires revision. A rating of 1 means implausible: a major contradiction or unrealistic feature prevents the case from representing a credible inpatient encounter.

### Result

Record a global judgment of Yes or No.

C1 pass requires that all clinically relevant domains are rated 3 or 4 and that the global judgment is Yes.

C1 revise applies if any domain is rated 2 or 1, or if the global judgment is No.

Require comments identifying the exact field or issue for any rating below 3.

### Technical interpretation

C1 is a clinical-realism gate on the resident-visible export. It does not inspect the concealed family or category fields. Software already checked schema, terminology identifiers, and implemented rules. C1 asks whether a physician still finds the chart coherent.

## Criterion 2 — Intended error present and correctly classified — hard gate

### Clinical question

Is the intended medication-reconciliation problem actually present in this chart, and is it the problem the specification claims?

### Reviewer should look for

Ask whether the intended discrepancy or gap is actually present, whether it is correctly classified as a Family 1 list discrepancy or a Family 2 transition gap and as the specific category named in the specification, and whether the investigator specification describes what is actually visible in the case.

### Result

Record Pass or Fail. A failure means the case cannot be scored against its intended answer key.

### Technical interpretation

This criterion checks fidelity of the deterministic injection to the planned standardized category. The planned category, the injected kind, and the answer-key category must describe the same visible target.

## Criterion 3 — Detectability from documents alone — hard gate

### Clinical question

Could a resident identify and resolve the intended problem using only the information available in this case?

### Reviewer should look for

Confirm that the required clinical evidence is present, that information is not contradictory, that no critical information is withheld, and that wording does not accidentally reveal the answer. For Family 2, the trigger or precondition must be visible and unambiguous.

### Result

Record Pass or Fail. Comment on evidence location, ambiguity, missing information, and cueing.

### Technical interpretation

This corresponds to evidentiary sufficiency and cue integrity in the CliniProof assessment model. The resident export must be sufficient without investigator fields.

## Criterion 4 — Absence of unintended errors — hard gate

### Clinical question

Is there any additional clinically meaningful medication-reconciliation discrepancy or transition-of-care gap beyond the specified target?

### Reviewer should look for

This must be assessed by an active hunt. Do not merely record errors that happen to be noticed. List any additional possible error and its severity or importance.

### Result

Record Pass or Fail.

### Technical interpretation

Error isolation means exactly one intended assessment target on error-bearing cases and zero on clean controls. An unintended second target makes the answer key unusable.

## Criterion 5 — Difficulty for target learner — advisory

### Clinical question

How difficult would this item be for an internal medicine resident?

### Reviewer should look for

Provide a provisional expert estimate using Easy, Moderate, Hard, or Outlier / inappropriate.

### Result

This rating is advisory only. Difficulty is ultimately an empirical property to be calibrated after resident administration. C5 alone should not reject a case.

### Technical interpretation

Any prior difficulty field in the answer key is optional metadata, not a software-computed score.

## Final disposition

Choose one of the following: Accept; Revise and re-rate; Regenerate / retire; or Adjudication required.
