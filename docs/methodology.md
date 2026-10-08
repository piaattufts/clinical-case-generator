# Methodology

CliniProof builds synthetic inpatient charts so that an internal-medicine resident can read one hospitalization and independently determine the discharge medication plan. The current study uses one seed-guided series, VAL-801 through VAL-824. This note is the method. The technical orientation, schema, and reproduction commands are in the project [README](../README.md). The two accounts describe the same sequence.

## What the current stage validates

The current work validates the base clinical case. The intended study sequence is a clean case that clinicians have accepted, then an independent resident discharge plan, with reasoning and confidence collected if the protocol asks for them, then comparison with a clinician-reviewed reference. Only after that acceptance would an error-bearing chart or an AI-generated recommendation be introduced, and only then would the resident’s response to that intervention be evaluated.

The base case is validated first. A discrepancy planted on an under-specified or internally inconsistent hospitalization cannot be interpreted, because failure may belong to the chart rather than to the discrepancy. This review stage does not evaluate planted errors or model-generated advice.

## Seed-guided generation

The original set is `CLINIPROOF_SEEDCASES_V3`, stored in [data/case_sets/seed_guided/](../data/case_sets/seed_guided/) excluding [CLEAN_BASE](../data/case_sets/seed_guided/CLEAN_BASE/). Generation started from six resident-authored documents in [data/seed_cases/resident_authored/](../data/seed_cases/resident_authored/). Those documents were design inputs. They were not copied into the study dataset, they were not frozen as VAL records, and they are not a prevalence sample.

Each document was abstracted into one archetype in [data/seed_cases/blueprints/archetypes.json](../data/seed_cases/blueprints/archetypes.json). The six families are medication-history uncertainty (`MEDREC_UNCERTAIN_HISTORY`), acute heart-failure decompensation (`HF_DECOMPENSATION`), infective endocarditis with outpatient parenteral antimicrobial therapy (`OPAT_ENDOCARDITIS`), kidney transplant with cytomegalovirus treatment (`TRANSPLANT_CMV`), hip fracture with interruption and resumption of anticoagulation (`POSTOP_ANTICOAGULATION`), and gastrointestinal bleeding with anticoagulation hold and restart (`GI_BLEED_ACUTE_CHANGE`). Four synthetic profiles were written for each archetype, producing 24 study slots, VAL-801 through VAL-824. Profiles differ before any historical error injection. The mapping from archetype to VAL range is in [data/seed_cases/README.md](../data/seed_cases/README.md).

Concepts were then resolved through source-backed terminology. Medication identity comes from RxNorm. Laboratory identity comes from LOINC. Units come from UCUM. Diagnosis text uses ICD-10-CM where a code is stored. Symptom names come from NLM Clinical Tables, with HPO as a fallback, and are not given invented SNOMED codes. Dose, route, and frequency come from the curated regimen table in [data/bootstrap/medication_regimens.json](../data/bootstrap/medication_regimens.json), not from the RxNorm product strength. Deterministic clinical conditionals in [data/bootstrap/rule_templates.json](../data/bootstrap/rule_templates.json) stay disabled until DailyMed or RxClass evidence is attached. Age, sex, weight, vital signs, and laboratory numbers are synthetic draws from the case seed. Narrative sentences in this frozen set are template wording. The batch plan states that OpenAI was not used, and the freeze command disables it. OpenAI, when enabled on a later development run, may only reword narrative from facts already selected. It does not choose diagnoses, codes, doses, the reference plan, or reviewer judgments.

A resolved identifier establishes concept identity. It does not establish that the medication is appropriate or that the hospitalization is clinically convincing. That distinction is set out in [provenance.md](provenance.md).

## First-round construction, and the clean case that is reviewed

The first round had two stages. The generator built a clean structured hospitalization, ran source-backed checks, and fingerprinted the clean case. The batch plan then assigned a historical assessment manipulation to 20 of the 24 slots and left 4 as clean controls. The four controls in [batch_plan.json](../data/case_sets/seed_guided/batch_plan.json) are VAL-801, VAL-805, VAL-809, and VAL-813. The other twenty frozen charts contain one planted medication-reconciliation discrepancy. That 20-and-4 split is provenance of the original freeze.

The resident task is to read the hospitalization and decide the discharge medication plan. The resident is not shown a finished discharge list and is not asked to find a planted error. The research team keeps a separate reference plan. That reference has to be reviewed by clinicians before it is used for scoring.

The charts for the current review are therefore the recovered pre-injection versions of all 24 slots, not the error-bearing freeze. They are stored once, in [data/case_sets/seed_guided/CLEAN_BASE/](../data/case_sets/seed_guided/CLEAN_BASE/): 24 resident JSON files and 24 evaluator JSON files. Each file is a byte-identical copy of the recovered clean chart. The evaluator file adds `reference_discharge_plan`. The resident file does not. The next revision starts from these files. They are not regenerated in order to improve them.

## Clinician review

Two clinicians completed the same validation casebook independently. The instrument is unchanged and is stored as [CliniProof_Clinical_Validation_Template.docx](validation/CliniProof_Clinical_Validation_Template.docx), with field definitions in [CODEBOOK.md](validation/CODEBOOK.md). The cases may be revised between rounds. The coding instrument is not revised, so later ratings remain comparable with ratings already recorded.

For each case the form asks for eight C1 domain scores from 1 to 4, a C1 Pass or Fail, C2 through C4 as Pass or Fail, C5 as Easy, Moderate, Hard, or Inappropriate / outlier, and an overall recommendation of Accept, Revise, or Exclude, each with a comment. Reviewer initials and the date are separate fields. A blank field stays blank. The completed forms are preserved byte for byte:

- Reviewer 1: [KO_Casebook_Validation.docx](clinical_feedback/reviewer_1/KO_Casebook_Validation.docx)
- Reviewer 2: [CliniProof_SeedGuided_Validation_Casebook_final_alex.docx](clinical_feedback/reviewer_2/CliniProof_SeedGuided_Validation_Casebook_final_alex.docx)

Both reviewers provided clinical feedback. The method does not assign them separate scientific roles.

Reviewer 1 left substantive case-level feedback on 6 of 24 cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. Eighteen cases have no substantive completed feedback. VAL-803 has a completed C1. The later ratings and the overall recommendation on that case are blank.

Reviewer 2 left substantive case-level feedback on 4 of 24 cases: VAL-801, VAL-805, VAL-809, and VAL-813. Twenty cases have no selected ratings or comments. On the four reviewed cases, C2 through C5 and the overall recommendation were left blank. Those blanks were not filled in by inference.

## Case-level comparison

Comments were compared case by case, using the same coding structure, and stored in [reviewer_comparison.csv](clinical_feedback/reviewer_comparison.csv). The narrative form is [reviewer_comparison.md](clinical_feedback/reviewer_comparison.md). For each reviewed case the comparison preserves the original rating and the free-text comment, records agreement, records complementary comments, and records reviewer-specific concerns. It does not force a consensus where the forms disagree or where one form is silent. The normalized table does not replace the Word files.

A case is a second-revision candidate only when both reviewers left substantive feedback. That overlap is four cases: VAL-801, VAL-805, VAL-809, and VAL-813. Shared concerns on those four, at the level recorded in the comparison, are an insufficient delirium story, an incomplete heart-failure hospitalization, an endocarditis chart too thin for the reasoning it asks, and a cytomegalovirus presentation that both reviewers found clinically incoherent. Reviewer-specific comments are retained beside those shared concerns.

VAL-802 and VAL-803 have substantive feedback from Reviewer 1 only. They remain documented. They are not treated as consensus cases, and they are not the cases selected for this revision round.

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

The repository cleanup is complete. The second revision has not been performed. The revision will edit the four overlapping cases, starting from the clean base, and will submit the revised charts to the same codebook. Resulting review materials will go in `exports/current/` when they exist. That directory is empty. The four candidates are not clinically validated. No case in this series should be described as clinically validated until a clinician has accepted it on this instrument.

## After clinical acceptance

Only after that acceptance would the project use a case in a later experiment that introduces an error or model-generated advice. Historical error-bearing variants remain in the original freeze and in Git history. They are not the starting point for the revision, and they are not evidence that this review stage has validated an error-evaluation experiment.

## Additional batch

The same method was run again to produce `CLINIPROOF_SEEDCASES_V4`, VAL-901 through VAL-924, in [data/case_sets/seed_guided_v4/](../data/case_sets/seed_guided_v4/README.md). The resident documents remain design inputs. The six archetypes and their four profiles each are the blueprint already verified against those documents. A new master seed draws new synthetic values. The batch plan pre-specifies four clean controls and twenty single discrepancies. Clean validation precedes injection. The resident export omits the answer key. This batch does not replace VAL-801–VAL-824, and machine validation does not accept either batch clinically. Provenance for the new freeze is in [provenance.md](../data/case_sets/seed_guided_v4/provenance.md).

## Provenance

Original charts, clean charts, and the two completed review files are hashed in [source_integrity.md](source_integrity.md). Future revisions are new derivative artifacts. They are not written back into the freeze or into the clean base. Superseded packages that were removed from this working tree remain at Git tag `repo-before-clinical-cleanup-2026-10`.
