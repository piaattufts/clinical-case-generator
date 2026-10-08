# Methodology

CliniProof builds synthetic inpatient charts so that an internal-medicine resident can read one hospitalization and independently determine the discharge medication plan. The current study uses one seed-guided series, VAL-801 through VAL-824. This note is the method. The technical orientation, schema, and reproduction commands are in the project [README](../README.md). The two accounts describe the same sequence.

## What the current stage validates

The current work validates the base clinical case. The intended study sequence is a clean case that clinicians have accepted, then an independent resident discharge plan, with reasoning and confidence collected if the protocol asks for them, then comparison with a clinician-reviewed reference. Only after that acceptance would an error-bearing chart or an AI-generated recommendation be introduced, and only then would the resident’s response to that intervention be evaluated.

The base case is validated first. A discrepancy planted on an under-specified or internally inconsistent hospitalization cannot be interpreted, because failure may belong to the chart rather than to the discrepancy. This review stage does not evaluate planted errors or model-generated advice.

## Seed-guided generation

The original set is `CLINIPROOF_SEEDCASES_V3`, stored in [data/case_sets/seed_guided/](../data/case_sets/seed_guided/) excluding [CLEAN_BASE](../data/case_sets/seed_guided/CLEAN_BASE/). Generation started from six resident-authored documents in [data/seed_cases/resident_authored/](../data/seed_cases/resident_authored/). Those documents were design inputs. They were not copied into the study dataset, they were not frozen as VAL records, and they are not a prevalence sample.

Each document was abstracted into one archetype in [data/seed_cases/blueprints/archetypes.json](../data/seed_cases/blueprints/archetypes.json). The display name is the archetype name. Generation 1 keeps its code, and Generation 2 keeps its own code: Medication history uncertainty (`MEDREC_UNCERTAIN_HISTORY` / `MED_HISTORY_UNCERTAINTY`), Acute heart-failure decompensation (`HF_DECOMPENSATION` / `HF_DECOMPENSATION`), Outpatient parenteral antibiotic therapy after endocarditis (`OPAT_ENDOCARDITIS` / `ENDOCARDITIS_OPAT`), Post-kidney-transplant infectious complication (`TRANSPLANT_CMV` / `TRANSPLANT_CMV`), Postoperative anticoagulation after hip fracture (`POSTOP_ANTICOAGULATION` / `HIP_FRACTURE_ANTICOAGULATION`), and Gastrointestinal bleed with anticoagulation decisions (`GI_BLEED_ACUTE_CHANGE` / `GI_BLEED_ANTICOAGULATION`). Four synthetic profiles were written for each archetype, producing 24 study slots, VAL-801 through VAL-824. Profiles differ before any historical error injection. The mapping from archetype to VAL range is in [data/seed_cases/README.md](../data/seed_cases/README.md).

Concepts were then resolved through source-backed terminology. Medication identity comes from RxNorm. Laboratory identity comes from LOINC. Units come from UCUM. Diagnosis text uses ICD-10-CM where a code is stored. Symptom names come from NLM Clinical Tables, with HPO as a fallback, and are not given invented SNOMED codes. Dose, route, and frequency come from the curated regimen table in [data/bootstrap/medication_regimens.json](../data/bootstrap/medication_regimens.json), not from the RxNorm product strength. Deterministic clinical conditionals in [data/bootstrap/rule_templates.json](../data/bootstrap/rule_templates.json) stay disabled until DailyMed or RxClass evidence is attached. Age, sex, weight, vital signs, and laboratory numbers are synthetic draws from the case seed. Narrative sentences in this frozen set are template wording. The batch plan states that OpenAI was not used, and the freeze command disables it. OpenAI, when enabled on a later development run, may only reword narrative from facts already selected. It does not choose diagnoses, codes, doses, the reference plan, or reviewer judgments.

A resolved identifier establishes concept identity. It does not establish that the medication is appropriate or that the hospitalization is clinically convincing. That distinction is set out in [provenance.md](provenance.md).

## First-round construction, and the clean case that is reviewed

The first round had two stages. The generator built a clean structured hospitalization, ran source-backed checks, and fingerprinted the clean case. The batch plan then assigned a historical assessment manipulation to 20 of the 24 slots and left 4 as clean controls. The four controls in [batch_plan.json](../data/case_sets/seed_guided/batch_plan.json) are VAL-801, VAL-805, VAL-809, and VAL-813. The other twenty frozen charts contain one planted medication-reconciliation discrepancy. That 20-and-4 split is provenance of the original freeze.

The resident task is to read the hospitalization and decide the discharge medication plan. The resident is not shown a finished discharge list and is not asked to find a planted error. The research team keeps a separate reference plan. That reference has to be reviewed by clinicians before it is used for scoring.

The charts for the current review are therefore the recovered pre-injection versions of all 24 slots, not the error-bearing freeze. They are stored once, in [data/case_sets/seed_guided/CLEAN_BASE/](../data/case_sets/seed_guided/CLEAN_BASE/): 24 resident JSON files and 24 evaluator JSON files. Each file is a byte-identical copy of the recovered clean chart. The evaluator file adds `reference_discharge_plan`. The resident file does not. The next revision starts from these files. They are not regenerated in order to improve them.

## Clinician review

Two clinicians completed the same validation casebook independently. The instrument is unchanged and is stored as [CliniProof_Clinical_Validation_Template.docx](validation/CliniProof_Clinical_Validation_Template.docx), with field definitions in [CODEBOOK.md](validation/CODEBOOK.md). The cases may be revised between rounds. The coding instrument is not revised, so later ratings remain comparable with ratings already recorded.

For each case the form asks for eight C1 domain scores from 1 to 4, a C1 Pass or Fail, C2 through C4 as Pass or Fail, C5 as Easy, Moderate, Hard, or Inappropriate / outlier, and an overall recommendation of Accept, Revise, or Exclude, each with a comment. Reviewer initials and the date are separate fields. A blank field stays blank. Completed review forms are private study records. The public comparison is [reviewer_comparison.md](clinical_feedback/reviewer_comparison.md) and [reviewer_comparison.csv](clinical_feedback/reviewer_comparison.csv).

Both reviewers provided clinical feedback. The method does not assign them separate scientific roles.

Reviewer 1 left substantive case-level feedback on 6 of 24 cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. Eighteen cases have no substantive completed feedback. VAL-803 has a completed C1. The later ratings and the overall recommendation on that case are blank.

Reviewer 2 left substantive case-level feedback on 4 of 24 cases: VAL-801, VAL-805, VAL-809, and VAL-813. Twenty cases have no selected ratings or comments. On the four reviewed cases, C2 through C5 and the overall recommendation were left blank. Those blanks were not filled in by inference.

## Case-level comparison

Comments were compared case by case, using the same coding structure, and stored in [reviewer_comparison.csv](clinical_feedback/reviewer_comparison.csv). The narrative form is [reviewer_comparison.md](clinical_feedback/reviewer_comparison.md). For each reviewed case the comparison preserves the original rating and the free-text comment, records agreement, records complementary comments, and records reviewer-specific concerns. It does not force a consensus where the forms disagree or where one form is silent. The public comparison is the de-identified table. Completed review forms remain private study records.

A case is a second-revision candidate only when both reviewers left substantive feedback. That overlap is four cases: VAL-801, VAL-805, VAL-809, and VAL-813. The comparison CSV records them as `SECOND_REVISION_CANDIDATE`. Shared concerns on those four, at the level recorded in the comparison, are an insufficient delirium story, an incomplete heart-failure hospitalization, an endocarditis chart too thin for the reasoning it asks, and a cytomegalovirus presentation that both reviewers found clinically incoherent. Reviewer-specific comments are retained beside those shared concerns.

VAL-802 and VAL-803 have substantive feedback from Reviewer 1 only. They are not consensus cases. Their later revision used that feedback together with the frozen framework. The comparison CSV records that track as `REVIEWER_1_PLUS_FRAMEWORK`. A blank `revision_candidate` means no case-specific clinician comment.

The recorded ratings, copied from the comparison, are these. Blank fields stay blank.

VAL-805. Reviewer 1 C1 is Fail and C3 is Fail. Reviewer 1 ticked both 2 and 3 on Medication regimen. Reviewer 2 C1 is Pass, so the reviewers disagree on C1. That Pass conflicts with Reviewer 2's own Fit between presentation and diagnosis score of 2, because any domain scored 1 or 2 makes C1 Fail. Reviewer 2 left C2 through C5 and the overall recommendation blank.

VAL-809. Reviewer 1 wrote "AKI", in the sentence "AKI was unexplained and lisinopril was continued despite AKI". Both reviewers failed C1. Reviewer 1 recommended revise.

VAL-813. Reviewer 1 wrote "change in potassium with obvious cause or indication". The word "unexplained" is an interpretation of that sentence; the recorded wording likely intended "without". Both reviewers failed C1. Reviewer 1 recommended exclude.

VAL-802. Reviewer 1 C2 is Fail, because the planted atorvastatin omission was not recognized as the intended problem. C3 is Fail. C4 names lisinopril continued despite elevated creatinine. The overall recommendation is Exclude.

VAL-803. Reviewer 1 completed C1 and left C2, C3, C4, C5, and the overall recommendation blank. The comment that the patient receives only 7 days of lisinopril coincides with the planted category Insufficient medication supply (`f2_insufficient_supply`).

VAL-801. Reviewer 1 ticked both Pass and Fail on C3. That double tick stays `Pass;Fail`.

On the four overlap cases, C1 domain agreement is descriptive only. Exact agreement is 11 of 31 single-response domain pairs (35%). The mean absolute difference is 0.77. Overall C1 agrees on 3 of 4 cases. No kappa is reported, and no consensus threshold is applied.

The four overlapping identifiers are also the four historical clean controls in the batch plan. The selection rule for the revision is the dual review, not the control flag.

## Iterative review, and what it is not

The review process is structured iterative clinician review. It is Delphi-informed: independent clinicians used a common codebook, their responses were compared, overlapping cases were selected for revision, and the next round will use the same instrument. It is not a classical Delphi study. The current process does not include a larger panel or a formal predefined statistical consensus threshold. Silence on a case is recorded as no substantive completed feedback. It is not converted into agreement.

```text
clean case
        ↓
Reviewer 1 assessment
        +
Reviewer 2 assessment
        ↓
structured case-level comparison
        ↓
shared concerns and reviewer-specific concerns retained
        ↓
cases reviewed by both selected for iterative revision
        ↓
clinical revision
        ↓
same validation codebook
        ↓
next clinician review
```

## What the next round will do

The four overlapping cases have been revised from the clean base. The revised charts are in [data/case_sets/seed_guided/REVISED/overlap_4/](../data/case_sets/seed_guided/REVISED/overlap_4/), with the change log in [overlap_4_revision_log.md](revision/overlap_4_revision_log.md). The defects found in that revision were frozen in [revision_framework.md](revision/revision_framework.md) and applied to the other twenty clean charts in [data/case_sets/seed_guided/REVISED/remaining_20/](../data/case_sets/seed_guided/REVISED/remaining_20/). VAL-802 and VAL-803 in that set of twenty also use Reviewer 1's case-specific comments. The other eighteen are framework-guided investigator revisions. That application is not additional clinician review. The next review uses the same codebook. None of these cases is clinically validated.

## After clinical acceptance

Only after that acceptance would the project use a case in a later experiment that introduces an error or model-generated advice. Historical error-bearing variants remain in the original freeze and in Git history. They are not the starting point for the revision, and they are not evidence that this review stage has validated an error-evaluation experiment.

## Provenance

Original charts, clean charts, and the two completed review files are hashed in [source_integrity.md](source_integrity.md). Future revisions are new derivative artifacts. They are not written back into the freeze or into the clean base. Superseded packages that were removed from this working tree remain at Git tag `repo-before-clinical-cleanup-2026-10`.

## Generation 2

The method above is the Generation 1 method. It is unchanged. A separate experimental pipeline, described in [methodology_synthea_g2.md](methodology_synthea_g2.md), starts from a Synthea longitudinal patient and builds a new inpatient episode. That pipeline does not revise VAL-801–VAL-824 and does not claim to have improved on them.
