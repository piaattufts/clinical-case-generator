# CliniProof clinician-validation rubric

Status: machine-validated synthetic resident-review cases pending clinician validation.

This rubric is for clinician and investigator review of frozen `CLINIPROOF_TAXONOMY_V1` cases (`VAL-201`–`VAL-224`). The five criteria serve different purposes.

- **C1 (clinical plausibility)** can be completed from the resident-visible chart alone. It is *fixable*: a case that is implausible should be revised rather than scored as an assessment item.
- **C2–C4** are *hard gates*. They require the concealed assessment specification (investigator packet). A failure means the case cannot be used against its intended answer key until it is fixed or retired.
- **C5 (difficulty)** is *advisory*. It must not by itself reject a case.

`f2_coprescription_omitted` is not represented in this frozen batch and remains `not_yet_implementable`.

## Family-specific guidance for C2–C4

C2–C4 must account for different structures.

### Family 1 — medication-list / transition discrepancies

These generally involve comparing home, inpatient, and discharge medication lists.

#### Medication omitted at discharge

`f1_omission`

A medication intended to continue after hospitalization is absent from the discharge medication list without a documented reason.

#### Medication inappropriately added or continued

`f1_commission`

A medication that should not be on the discharge list (for example, one that was held or stopped) appears there without a documented decision to continue it.

#### Unexplained dose discrepancy

`f1_dose_mismatch`

The discharge dose differs from the intended continued dose without an explanation.

#### Unexplained route discrepancy

`f1_route_mismatch`

The discharge route differs from the intended continued route without an explanation.

#### Unexplained frequency discrepancy

`f1_frequency_mismatch`

The discharge frequency differs from the intended continued frequency without an explanation.

#### Unexplained therapeutic substitution

`f1_therapeutic_substitution`

The discharge list replaces an intended continued medication with another agent of the same class without documenting an intentional switch.

### Family 2 — transition-of-care gaps

These may involve absence of monitoring, follow-up, supply, restart planning, or another transition action. Do **not** identify Family 2 solely by comparing medication lists. For Family 2, the trigger or precondition must be visible, and the missing companion action is the specified target.

#### Required monitoring not arranged

`f2_monitoring_not_arranged`

**Clinical explanation.** Warfarin is continued at discharge, but outpatient INR monitoring has not been arranged.

**Technical concept.** In CliniProof this is classified as a Family 2 transition-of-care gap because the medication order itself remains unchanged; the missing element is the required follow-up action.

#### Held medication without a restart plan

`f2_held_med_no_restart_plan`

A home medication is intentionally held in the hospital for a legitimate temporary reason, but discharge documentation does not say when or under what conditions it should be resumed.

#### Insufficient medication supply

`f2_insufficient_supply`

Days’ supply at discharge is too short to last until the planned follow-up.

#### Hospital-only medication continued after discharge

`f2_hospital_only_continued`

A medication started for an inpatient-only indication is still on the discharge list.

#### Temporary inpatient substitution not addressed at discharge

`f2_inpatient_substitution_not_reverted`

A temporary inpatient substitute was used, but discharge does not revert to home therapy or document an intentional decision to continue the substitute.

#### Follow-up missing for an unresolved treatment decision

`f2_pending_decision_followup_missing`

A treatment decision was left pending, but no follow-up is arranged to resolve it.

#### Required companion medication omitted (not in this freeze)

`f2_coprescription_omitted`

Specified conceptually. Not currently implementable because no source-backed companion-prescription rule exists in this repository.

## Criterion 1 — Clinical plausibility — fixable

### Clinical question

“Apart from any intentionally planted reconciliation discrepancy, could this case reasonably represent a patient encountered in the stated clinical setting?”

### Reviewer should look for

Assess these domains independently:

1. Presentation and demographics
2. Diagnosis-presentation coherence
3. Vital signs
4. Laboratory findings
5. Medication regimen
6. Hospital course
7. Cross-document consistency
8. Discharge context and follow-up

Clinical plausibility is **not** synonymous with optimal management or complete guideline concordance. Unusual but source-backed formulations or units should be recorded if they undermine credibility; they should not be silently “corrected” in the frozen case.

### Scale (each domain)

- **4 — Fully plausible.** No clinically meaningful concern.
- **3 — Plausible with minor concern.** A minor issue is present but would not materially alter interpretation.
- **2 — Questionable.** A clinically meaningful inconsistency or implausibility is present and the case requires revision.
- **1 — Implausible.** A major contradiction or unrealistic feature prevents the case from representing a credible inpatient encounter.

### Result

Global judgment: Yes / No.

**C1 pass:** all clinically relevant domains ≥ 3 **and** global judgment = Yes.

**C1 revise:** any domain ≤ 2 **or** global judgment = No.

Require comments identifying the exact field or issue for any rating below 3.

### Technical interpretation

C1 is a clinical-realism gate on the resident-visible export. It does not inspect `error_family` / `error_category`. Software already checked schema, terminology identifiers, and implemented rules; C1 asks whether a physician still finds the chart coherent.

## Criterion 2 — Intended error present and correctly classified — hard gate

### Clinical question

“Is the intended medication-reconciliation problem actually present in this chart, and is it the problem the specification claims?”

### Reviewer should look for

- Is the intended discrepancy or gap actually present?
- Is it correctly classified (Family 1 list discrepancy versus Family 2 transition gap, and the specific category)?
- Does the investigator specification describe what is actually visible in the case?

### Result

Pass / Fail.

A failure means the case cannot be scored against its intended answer key.

### Technical interpretation

This is fidelity of the deterministic injection to the planned canonical category. Planned category, injected `kind`, and answer-key `error_category` must describe the same visible target.

## Criterion 3 — Detectability from documents alone — hard gate

### Clinical question

“Could a resident identify and resolve the intended problem using only the information available in this case?”

### Reviewer should look for

- required clinical evidence is present
- information is not contradictory
- no critical information is withheld
- wording does not accidentally reveal the answer (cueing)
- for Family 2: the trigger or precondition is visible and unambiguous

### Result

Pass / Fail.

Comment on evidence location, ambiguity, missing information, and cueing.

### Technical interpretation

This corresponds to evidentiary sufficiency and cue integrity in the CliniProof assessment model. The resident export must be sufficient without investigator fields.

## Criterion 4 — Absence of unintended errors — hard gate

### Clinical question

“Is there any additional clinically meaningful medication-reconciliation discrepancy or transition-of-care gap beyond the specified target?”

### Reviewer should look for

This must be assessed by **active hunt**. Do not merely record errors that happen to be noticed. List any additional possible error and its severity or importance.

### Result

Pass / Fail.

### Technical interpretation

Error isolation: exactly one intended assessment target on error-bearing cases, zero on clean controls. Unintended second targets make the answer key unusable.

## Criterion 5 — Difficulty for target learner — advisory

### Clinical question

“How difficult would this item be for an internal medicine resident?”

### Reviewer should look for

A provisional expert estimate: Easy / Moderate / Hard / Outlier / inappropriate.

### Result

Advisory only. Difficulty is ultimately an empirical property to be calibrated after resident administration. C5 alone should not reject a case.

### Technical interpretation

`difficulty_a_priori` in the answer key is optional metadata, not a software-computed score.

## Final disposition

- Accept
- Revise and re-rate
- Regenerate / retire
- Adjudication required
