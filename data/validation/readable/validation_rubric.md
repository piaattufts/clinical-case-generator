# CliniProof clinician-validation rubric

Status: machine-validated synthetic resident-review cases pending clinician validation.

This rubric is for clinician review of frozen `CLINIPROOF_TAXONOMY_V1` cases (`VAL-201`–`VAL-224`). The five criteria serve different purposes. C1 can be completed from resident-visible documents alone. C2–C5 require the concealed assessment specification and belong on the investigator packet.

`CLINIPROOF_TAXONOMY_V1` covers all currently implemented CliniProof error categories. `f2_coprescription_omitted` is not represented in this frozen batch and remains `not_yet_implementable`.

## Family-specific guidance for C2–C4

**Family 1** categories are medication-list / transition discrepancies:

- `f1_omission`
- `f1_commission`
- `f1_dose_mismatch`
- `f1_route_mismatch`
- `f1_frequency_mismatch`
- `f1_therapeutic_substitution`

**Family 2** categories are transition-of-care gaps. They may occur without changing the medication list:

- `f2_monitoring_not_arranged`
- `f2_held_med_no_restart_plan`
- `f2_insufficient_supply`
- `f2_hospital_only_continued`
- `f2_inpatient_substitution_not_reverted`
- `f2_pending_decision_followup_missing`

Do **not** identify Family 2 solely by comparing home versus discharge medication lists. For Family 2, confirm that the trigger or precondition is visible and that the missing companion action (monitoring, restart plan, supply, hospital-only stop, substitution revert, or follow-up) is the specified target.

## C1. Clinical plausibility — fixable

Definition: the resident-visible case forms a coherent and clinically credible inpatient encounter.

Assess the following domains independently:

1. Presentation and demographics
2. Diagnosis-presentation coherence
3. Vital signs
4. Laboratory findings
5. Medication regimen
6. Hospital course
7. Cross-document consistency
8. Discharge context and follow-up

Scale for each domain:

- **4 — Fully plausible.** No clinically meaningful concern.
- **3 — Plausible with minor concern.** A minor issue is present but would not materially alter interpretation.
- **2 — Questionable.** A clinically meaningful inconsistency or implausibility is present and the case requires revision.
- **1 — Implausible.** A major contradiction or unrealistic feature prevents the case from representing a credible inpatient encounter.

Global question:

“Apart from the intentionally planted reconciliation discrepancy, could this case reasonably represent a patient encountered in the stated clinical setting?”

Yes / No

**C1 pass:** all clinically relevant domains ≥ 3 **and** global judgment = Yes.

**C1 revise:** any domain ≤ 2 **or** global judgment = No.

Require comments identifying the exact field or issue for any rating below 3.

Clinical plausibility is **not** synonymous with optimal management or complete guideline concordance.

## C2. Intended error present and correctly classified — hard gate

Standard: the planted error is actually present and matches the specified CliniProof family/category.

Response: Pass / Fail

Questions:

- Is the intended discrepancy/gap actually present?
- Is it correctly classified?
- Does the investigator specification describe what is actually visible in the case?

A failure means the case cannot be scored against its intended answer key.

## C3. Detectability from documents alone — hard gate

Standard: the target is recoverable from the resident-visible case alone. The resident should not require withheld clinical information. The error must also not be artificially disclosed by formatting or wording.

For Family 2: the trigger/precondition must be visible and unambiguous.

Response: Pass / Fail

Require comments on evidence location, ambiguity, missing information, and cueing.

## C4. Absence of unintended errors — hard gate

Standard: no additional clinically meaningful medication-reconciliation discrepancy or transition-of-care gap exists beyond the specified target.

This must be assessed by **active hunt**. Do not merely record errors that happen to be noticed.

Ask raters to list any additional possible error and its severity/importance.

Response: Pass / Fail

## C5. Difficulty for target learner — advisory

Target learner: internal medicine resident.

Rating: Easy / Moderate / Hard / Outlier / inappropriate

This is an expert provisional estimate only. Difficulty is ultimately an empirical property to be calibrated after resident administration.

C5 alone should not reject a case.

## Final disposition

- Accept
- Revise and re-rate
- Regenerate / retire
- Adjudication required
