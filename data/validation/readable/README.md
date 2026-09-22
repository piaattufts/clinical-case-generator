# Readable CliniProof review materials

This directory contains the human-readable review materials for the frozen CliniProof validation set whose batch code is `CLINIPROOF_TAXONOMY_V1`. These files are the first documents a clinical reviewer should use. They explain what CliniProof is, what the twenty-four cases contain, and how two clinical reviewers independently decide whether each case is suitable for an assessment of medication-reconciliation reasoning.

The set contains twenty-four synthetic inpatient cases labeled VAL-201 through VAL-224. They were developed so that internal medicine residents and other clinicians can practice comparing home therapy, inpatient orders, and the discharge plan, then deciding what should continue, stop, change, be monitored, or be followed up. Twenty of the cases contain one pre-specified medication-reconciliation or transition-of-care assessment problem. Four of the cases are clean controls in which no problem was intentionally introduced. Reviewers are not told which cases are controls during the blinded plausibility stage, and this page does not identify them.

These Markdown files are readable views of the frozen cases. They do not replace the frozen JSON, and they do not regenerate the underlying cases. Clinician-visible patient information comes from [`../resident_validation_cases.json`](../resident_validation_cases.json). The investigator-only packet also reads [`../investigator_answer_key.json`](../investigator_answer_key.json).

The twenty-four-case validation set will undergo independent dual expert review with structured consensus resolution. Two clinical reviewers first assess clinical plausibility while blinded to the intended assessment target. After submitting those ratings, they review the concealed target and independently evaluate whether the intended problem is present, whether a resident could detect it from the chart, whether another unintended problem is also present, and how difficult the case is likely to be. Cases with important disagreements undergo structured consensus review. Original independent ratings are preserved.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. That sentence means the software has already checked structure, terminology, and a limited set of implemented rules, but a clinician has not yet accepted the case for educational use.

To regenerate the Markdown from the repository root without modifying frozen JSON, run:

```bash
python scripts/build_readable_validation_packets.py
```

This command regenerates the readable Markdown views only. It does not alter the frozen study cases.

## What is CliniProof?

CliniProof is a synthetic inpatient case-generation framework designed to support assessment of medication-reconciliation reasoning. Medication reconciliation, in ordinary clinical terms, is the work of comparing what the patient was taking before admission, what was given in the hospital, and what is prescribed at discharge, then making holds, stops, continuations, supplies, monitoring, and follow-up explicit.

Each readable case is meant to be read like a hospital chart. It typically includes the reason for admission, diagnoses and relevant clinical history, vital signs, laboratory findings, home medications, medications during hospitalization, discharge medications, monitoring and follow-up, and discharge instructions.

A source-backed concept is not the same thing as a real patient record. Medication concepts are linked to established terminology such as RxNorm. Diagnoses are linked to established terminology such as ICD-10-CM. Laboratory tests are linked to LOINC where that mapping is implemented. Patient-specific values such as age, vital signs, and laboratory results are synthetic. An RxNorm identifier for a warfarin product means the software used an official medication concept. It does not mean that a real patient was taking warfarin.

The basic construction sequence is as follows. A clinical scenario is selected, for example an inpatient heart-failure or pneumonia theme. The system constructs a structured clean case. Automated structural, terminology, and implemented clinical-rule checks are run. When the planned case is error-bearing, one pre-specified assessment problem is introduced. The case is checked again. Separate resident-facing and investigator-facing versions are then produced.

Automated checking does not establish clinical realism or educational appropriateness. Those judgments are why this review exists.

A fuller clinical-to-technical explanation, still without per-case answers, is in [`how_cliniproof_works.md`](how_cliniproof_works.md). Informatics and engineering notes are in [`developer_notes.md`](developer_notes.md).

## What does “frozen validation set” mean?

VAL-201 through VAL-224 are the fixed versions initially presented to reviewers. “Frozen” means the study team locked these cases as the original validation candidates. It does not mean that a clinician has already accepted them.

During initial clinical review, reviewers evaluate the same version of each case. The original case files are not silently edited. Each reviewer’s original ratings are preserved. Requested revisions are recorded separately from the frozen source files.

This matters if a case is later revised. The study team should be able to distinguish the version originally reviewed, the requested revision, and the revised version that may subsequently be reviewed again. Do not edit the frozen case files directly. Record recommended changes in the review worksheets and comments.

## What are reviewers being asked to determine?

The purpose of this review is not simply to confirm that software checks passed. Two clinical reviewers independently determine whether each case is suitable for use in an assessment involving internal medicine residents.

The rating criteria are defined in full in [`validation_rubric.md`](validation_rubric.md). The two-reviewer workflow is in [`reviewer_protocol.md`](reviewer_protocol.md). The five criteria are summarized here so that this page can stand on its own.

### C1 — Clinical plausibility

Clinical question: Could this reasonably represent a patient encountered in the stated inpatient clinical setting?

Reviewers consider presentation and demographics; fit between presentation and diagnosis; vital signs; laboratory findings; medication regimen; hospital course; consistency across the chart; and discharge plan and follow-up.

Clinical plausibility does not mean that every treatment decision must be the only possible or ideal clinical choice. The issue is whether the case is coherent and credible enough to function as an assessment case.

Each domain is rated on a 1-to-4 scale. A rating of 1 means implausible. A rating of 2 means questionable and requires revision. A rating of 3 means plausible with minor concern. A rating of 4 means fully plausible. Any domain rated 1 or 2 should include a written explanation of the specific clinical concern.

C1 is completed before the reviewer sees the concealed assessment target.

### C2 — Intended assessment problem

Clinical question: Does the case actually contain the medication-reconciliation or transition-of-care problem that it was designed to assess?

After C1 is submitted, the reviewer is shown the concealed target and checks whether the intended problem is present, whether it is correctly characterized, and whether the investigator description matches what appears in the case.

C2 is a required criterion. If it fails, the case cannot be used against its intended answer key until the problem is corrected or the case is excluded. A written explanation is required for a failure.

### C3 — Detectability

Clinical question: Could an internal medicine resident identify and resolve the intended problem using only the clinical information provided in the case?

Reviewers should consider whether all necessary evidence is available, whether clinically important information is missing, whether the case is unnecessarily ambiguous, and whether wording or formatting accidentally gives away the answer. The target should be discoverable from the chart, but it should not be explicitly signposted.

C3 is a required criterion. A written explanation is required for a failure.

### C4 — Absence of unintended problems

Clinical question: Apart from the intended assessment problem, is there another clinically meaningful medication-reconciliation or transition-of-care problem in the case?

Reviewers should actively search for additional problems. This is not merely a note of issues that happen to catch the eye. After reviewing the complete case, ask whether another discrepancy is present that a reasonable resident could interpret as the assessment target.

This matters because an unintended second problem could make a case ambiguous. A resident might reasonably identify a different problem from the one the assessment was designed to score.

C4 is a required criterion. If it fails, identify the additional problem, the medication or clinical issue involved, and why it is clinically meaningful.

### C5 — Expected learner difficulty

Clinical question: How difficult would this case likely be for an internal medicine resident?

The options are Easy, Moderate, Hard, and Inappropriate / outlier.

This is an expert estimate of difficulty. Actual difficulty should eventually be assessed from resident performance. C5 alone does not determine whether a case is accepted.

## Two-stage review process

The validation methodology is independent dual expert review with structured consensus resolution. It is not a Delphi process. Two clinical reviewers independently evaluate all twenty-four cases. Their original ratings are recorded before any discussion occurs.

### Stage 1 — Blinded clinical plausibility review

Both reviewers first receive only resident-visible case information. They do not see whether the case is a clean control, the intended Family 1 or Family 2 classification, the specific assessment category, the medication involved in the concealed assessment target, the expected correction, or the investigator answer key.

They independently complete C1. This allows the reviewer to judge whether the case itself is clinically credible without being influenced by already knowing what error or transition-of-care problem the case was designed to contain.

Use [`plausibility_only_packet.md`](plausibility_only_packet.md) for Stage 1. On that form, record whether the case is clinically plausible or whether revision is needed for clinical plausibility. Do not record Accept, Revise, or Exclude until Stage 2 is complete. C1 ratings must be submitted and locked before Stage 2 begins.

### Stage 2 — Assessment-target validation

Only after C1 has been submitted should reviewers open the investigator and clinical-validator packet. At that stage they independently evaluate C2 (intended problem), C3 (detectability), C4 (absence of unintended problems), C5 (expected difficulty), and their overall recommendation.

Use [`clinician_validation_packet.md`](clinician_validation_packet.md) for Stage 2. This file contains concealed per-case study information and must not be provided to resident participants.

## Reviewer recommendations

After completing their independent review, each reviewer gives one of three recommendations.

**Accept.** The case is suitable for use without clinically meaningful revision.

**Revise.** The case could be suitable, but one or more changes are required before use. Reviewers who choose Revise should describe what they want changed, why the change is clinically necessary, and which criterion is affected. Examples include correcting an implausible formulation, clarifying a hospital course, correcting an inappropriate or confusing laboratory unit, adding information needed to detect the intended problem, and removing an unintended second discrepancy.

**Exclude.** The case should not be used because the problems cannot reasonably be corrected without substantially reconstructing it.

Reviewer recommendations do not directly modify the frozen cases. Comments are recommendations for the study team. Record independent ratings on the empty [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv) template.

## What happens when the two reviewers disagree?

Original ratings remain preserved. Cases with agreement require no consensus discussion unless the investigators choose to review them. If reviewers disagree on an important criterion or on the final recommendation, the case undergoes structured consensus review.

The process is to preserve both original independent ratings, identify the areas of disagreement, discuss the clinical reasoning behind each rating, and record a separate consensus outcome. Possible consensus outcomes are Accepted, Revision required, Excluded, and Unresolved.

Consensus does not overwrite the original ratings. Record it on [`consensus_worksheet.csv`](consensus_worksheet.csv), not on the independent reviewer row.

If consensus cannot be reached, the case remains unresolved and is not considered clinically validated. It may later receive another expert opinion, or it may remain outside the validated set.

## Family 1 and Family 2 assessment problems

The concealed target, when one exists, belongs to one of two clinical families. Reviewers do not need this classification during Stage 1. It becomes relevant in Stage 2, when the investigator packet names the intended problem. Canonical software identifiers are shown in parentheses after the clinical names; they are labels for investigator files, not a substitute for the clinical meaning.

### Family 1 — Medication-reconciliation discrepancies

These involve an unexplained discrepancy in the medication regimen across the transition to discharge. In a Family 1 case, the medication regimen or list itself contains the relevant discrepancy.

Examples include a medication omitted at discharge (`f1_omission`); a medication inappropriately continued or added (`f1_commission`); an unexplained dose discrepancy (`f1_dose_mismatch`); an unexplained route discrepancy (`f1_route_mismatch`); an unexplained frequency discrepancy (`f1_frequency_mismatch`); and an unexplained therapeutic substitution (`f1_therapeutic_substitution`).

### Family 2 — Transition-of-care gaps

These involve an important action needed for safe medication management after discharge that is absent or incomplete. The discharge medication list itself may appear correct in a Family 2 case. Therefore a reviewer should not evaluate these cases solely by comparing home and discharge medication lists. Monitoring, instructions, medication supply, restart planning, and follow-up may contain the relevant assessment problem.

Examples include required outpatient monitoring not arranged (`f2_monitoring_not_arranged`); a temporarily held medication without a restart plan (`f2_held_med_no_restart_plan`); insufficient medication supply until follow-up (`f2_insufficient_supply`); a hospital-only medication continued at discharge (`f2_hospital_only_continued`); a temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`); and missing follow-up for an unresolved treatment decision (`f2_pending_decision_followup_missing`).

The taxonomy also names required companion medication omitted (`f2_coprescription_omitted`). That category is not included in the current validation set because the software does not yet have a sufficiently source-backed rule for deciding when such a companion medication is required.

## Machine validation is not clinical validation

The software can establish expected case structure; terminology and reference integrity; implemented clinical rules; eligibility of the requested assessment category; the expected deterministic state change; answer-key consistency; implemented checks for an unintended second assessment target; and removal of concealed answer-key information from resident-facing files.

The software cannot establish whether the overall case is clinically realistic; whether medications are appropriate in real practice; whether clinically important context is missing; whether formulations or units would distract or confuse a resident; whether the intended problem is fair; whether the case is educationally appropriate; or whether difficulty is appropriate for residents.

Until clinicians finish review, every record remains a machine-validated synthetic resident-review case pending clinician validation. Automated checks are useful for detecting technical inconsistencies. They are not a substitute for this clinical review.

## Important points for reviewers

### Do not assume every case contains an error

Four of the twenty-four cases are clean controls. They do not contain an intentionally introduced medication-reconciliation problem. This page does not identify them. Clean controls are included so that a reviewer cannot assume that every chart necessarily contains an error.

### Do not assume unusual features are intentional

Unusual formulation, route, unit, medication regimen, laboratory result, vital sign, or narrative detail should be reported if it is clinically concerning. A terminology source can return something technically valid that is still unusual in normal clinical documentation. Those oddities are left visible for clinician review. They are not silently rewritten.

### Evaluate what is actually documented

Do not fill missing information by assumption. If a case requires undocumented information to solve its intended assessment problem, that is important feedback for C3.

### Actively look for additional problems

C4 requires a deliberate search for unintended, clinically meaningful medication-reconciliation or transition-of-care problems, not only a record of issues that happen to be noticed.

### Do not directly edit the frozen case

Record requested revisions in the review materials. The study team will preserve the original reviewed version and handle any revision separately.

## Where should I start?

The table below routes different readers to the file that matches their task. A clinical reviewer completing this validation should begin with Stage 1 and stay on the resident-safe files until C1 ratings have been submitted. Residents and plausibility reviewers should stay on the resident-safe files. Only investigators and expert validators should open the concealed-target packet, and only after Stage 1 is complete.

| If you are... | Start here |
| --- | --- |
| Resident or clinician reviewing cases | [`all_cases.md`](all_cases.md) |
| Clinical reviewer completing Stage 1 (blinded C1) | [`plausibility_only_packet.md`](plausibility_only_packet.md) |
| Clinical reviewer completing Stage 2 (C2–C5) | [`clinician_validation_packet.md`](clinician_validation_packet.md) |
| Clinical reviewer reading the two-reviewer protocol | [`reviewer_protocol.md`](reviewer_protocol.md) |
| Medical educator reviewing the framework | [`validation_rubric.md`](validation_rubric.md) |
| Recording independent ratings (empty template) | [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv) |
| Recording consensus (empty template) | [`consensus_worksheet.csv`](consensus_worksheet.csv) |
| Clinician or resident curious how CliniProof works | [`how_cliniproof_works.md`](how_cliniproof_works.md) |
| Clinical informatics / AI engineer | [`developer_notes.md`](developer_notes.md) |

## Safe for residents and plausibility-only review

The files listed here contain resident-visible case content and generic explanations of how cases are made. They do not associate an individual VAL case with its concealed assessment target. They do not include planted-error family, category, trigger labels, control status, or per-case answer keys.

| File | Contents |
| --- | --- |
| [`all_cases.md`](all_cases.md) | All twenty-four readable cases, presented sequentially |
| [`plausibility_only_packet.md`](plausibility_only_packet.md) | Each readable case followed by the Stage 1 C1 form |
| [`cases/`](cases/) | One page per case, VAL-201 through VAL-224 |
| [`how_cliniproof_works.md`](how_cliniproof_works.md) | Clinical-to-technical overview with no per-case answers |
| [`developer_notes.md`](developer_notes.md) | Informatics and engineering notes that describe mechanisms only |
| [`validation_rubric.md`](validation_rubric.md) | The C1 through C5 rubric with no per-case answers |
| [`reviewer_protocol.md`](reviewer_protocol.md) | Two-reviewer independent dual expert review protocol |
| [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv) | Empty independent-rating template; no ratings are pre-filled |
| [`consensus_worksheet.csv`](consensus_worksheet.csv) | Empty consensus-outcome template, stored separately from independent ratings |

## Investigator / clinical-validator only

Do not provide this file to resident study participants. Clinical reviewers should complete and submit Stage 1 C1 before opening it.

The following file associates each VAL identifier with its intended assessment target. It contains the readable case, the concealed target, the C2 through C5 review forms, and the independent recommendation.

| File | Contents |
| --- | --- |
| [`clinician_validation_packet.md`](clinician_validation_packet.md) | Readable case, concealed target, C2 through C5 forms, and independent recommendation |

## Questions or concerns during review

If a reviewer is unsure whether something is important, it is preferable to document the concern rather than resolve it through assumption. Comments remain valuable even if the reviewer ultimately accepts the case.

Please comment on clinically unusual formulations; questionable doses, routes, or frequencies; laboratory values or units that appear inconsistent; missing clinical context; contradictions between sections; inadequate information to identify the intended problem; unintended additional medication-related problems; and anything that could make the case confusing, misleading, or unfair for an internal medicine resident.
