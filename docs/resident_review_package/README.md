# CliniProof Resident and Clinician Review Package

Historical validation design. Not the current resident-facing study workflow. The current clinician package is [Set 1, version 3, the six revised cases](../../exports/ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx). Set 2, [the eighteen recovered clean cases](../../exports/ko_cycle2_clean_validation/CliniProof_Cycle2_Clean_Cases_Validation.docx), is still under internal correction and is not yet ready for clinician review. The link is retained for investigators. The combined 24-case file is an investigator convenience copy. This page is the Word-format review package for the two frozen prospective batches, `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3`. Those casebooks include a validation reference after C1 because they were built when many charts contained one injected discrepancy. They are historical review artifacts. They are not the current resident-facing study set. The recovered clean charts are in [exports/clean_balanced_seed_set/](../../exports/clean_balanced_seed_set/AUDIT.md). The current Set 1 codebook is linked above. [An earlier six-case revision](../../exports/ko_revised_cases_v1/KO_REVISED_CASES_REVIEW.docx) is superseded. The Set 2 source package remains [the clean-case form](../../exports/ko_clean_cases_for_review_v1/KO_CLEAN_CASES_REVIEW.docx), which is under internal revision and is not yet ready for clinician review. Ready for clinician review does not mean clinically validated. The [project README](../../README.md) describes that workflow.

The Word files are a reading format. They are not a second source of truth.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word. A preview can show the boxes as ordinary characters; in Word they are form controls.

```text
canonical structured case data
        ↓
clinical chart
+
canonical investigator metadata
        ↓
validation reference, placed after C1
+
fixed validation rubric
        ↓
validation casebook
```

The canonical clinical content remains the active structured case data for `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3`. If a Word chart and the structured case ever disagree, the structured case is the source of truth.

## At a glance

| Resource | Contents | Intended use |
| --- | --- | --- |
| Balanced validation casebook | 24 charts from `CLINIPROOF_BALANCED_V4`, VAL-701–VAL-724, each followed by its rubric and comments | Clinician validation |
| Seed-guided validation casebook | 24 charts from `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824, each followed by its rubric and comments | Clinician validation |
| Generation prompt | Exact instructions used to produce the earlier chart-only Word export | Reproducibility and transparency |
| Export QA reports | Fidelity checks for the chart export and for the validation casebooks | Technical and provenance review |

## Review files

Complete validation documents containing each clinical case followed immediately by its validation rubric and reviewer comment fields. The instructions are inside the casebook. A separate codebook is not required.

### Balanced structured case set

[Download the Balanced Validation Casebook (Word)](files/CliniProof_Balanced_Validation_Casebook.docx)

### Resident-seed-guided case set

[Download the Seed-Guided Validation Casebook (Word)](files/CliniProof_SeedGuided_Validation_Casebook.docx)

Case-set overviews, with composition and review links, are the [balanced structured overview](../../data/case_sets/balanced/README.md) and the [resident-seed-guided overview](../../data/case_sets/seed_guided/README.md). The full rating method is in [clinical validation](../clinical_validation.md).

## The two case sets

The sets ask different design questions. This page does not rank them.

### Balanced structured set

`CLINIPROOF_BALANCED_V4` contains VAL-701 through VAL-724 (24 cases).

Each chart was generated from a predefined structured clinical profile: a specified presentation, medication role, hospital course, and follow-up. The profiles were chosen so the set covers selected inpatient scenarios in a controlled way. Ages, vital signs, weights, and laboratory numbers are synthetic. The balance of scenarios is a study design. It is not an estimate of how often these problems occur in practice.

### Resident-seed-guided set

`CLINIPROOF_SEEDCASES_V3` contains VAL-801 through VAL-824 (24 cases).

Six cases supplied by residents were used as design inputs. Those examples were abstracted into clinical archetypes, and new synthetic encounters were generated from the archetypes. The current VAL cases are not copies of the original resident cases. The six source cases are not treated as prevalence data: they do not estimate how often a disease, a drug, or a reconciliation problem occurs.

## What each case contains

```text
Patient overview
        ↓
Reason for hospitalization
        ↓
Relevant medical history
        ↓
Hospital course
        ↓
Admission findings
        ↓
Discharge / most recent findings
        ↓
Home medications
        ↓
Medications during hospitalization
        ↓
Discharge medications
        ↓
Medication reconciliation
        ↓
Monitoring and follow-up
        ↓
Discharge instructions
        ↓
Other relevant clinical information
```

The Word documents render the current structured case data in that clinical-chart order. A section appears when the case has that information. Monitoring and follow-up stay separate from the medication lists.

## How the cases were generated

```text
Clinical scenario or resident-derived archetype
        ↓
Structured synthetic patient
        ↓
Medication and transition plan
        ↓
Clean case
        ↓
Automated structural and clinical-consistency checks
        ↓
Pre-specified assessment modification where applicable
        ↓
Post-modification checks
        ↓
Blinded resident-facing case
        +
separate investigator reference
```

The clean clinical state is built first. Where a case is designed to assess a medication-reconciliation or transition-of-care problem, that change is introduced afterward, from a pre-specified plan. The target is not selected retrospectively by looking at an arbitrary generated chart and deciding what seems wrong. The resident-facing Word charts do not contain the concealed answer key. This page does not say which case has which target.

## How the Word files were produced

The Word documents were created as deterministic renderings of the existing active case data. They were not generated by asking a language model to rewrite or medically complete the cases.

The DOCX generation step was not allowed to:

- invent clinical information
- infer missing values
- change medication doses
- change medication frequency
- add diagnoses
- add monitoring
- add follow-up
- repair an assessment target
- expose concealed answer keys

The exact instructions used for the export are in the [DOCX generation prompt](DOCX_GENERATION_PROMPT.md).

## How this connects to the CliniProof dashboard

These Word documents provide a convenient format for reviewing the clinical content before study administration. The same underlying case structure is intended to provide the clinical content for the CliniProof dashboard. In the dashboard, residents will review components of the synthetic chart and perform medication-reconciliation or transition-of-care reasoning. The Word review step allows the clinical content to be validated before it is administered through the interactive study interface.

```text
case generator
      ↓
validated clinical case
      ↓
dashboard / study presentation
      ↓
resident review and reasoning
```

A resident review dashboard is **planned**. It is not implemented in the current software. What exists now is the case generator and a reference-terminology search service. These Word files are the review format for the clinical content.

## How to use this review package

1. Download the validation casebook for the set you are reviewing.
2. Read each clinical chart, and complete C1 before you read that case's validation reference.
3. Click the checkboxes to select ratings. Type comments directly into the provided fields. Please select one response per rating item.
4. Save a separate copy. Do not overwrite the original file.
5. Return that copy to the study investigator. Do not upload it to this public repository.

The clinician validation packet for a set, linked from that set's overview, is where a validator sees the intended target. The Word case sets on this page do not include it.

## What is being validated

The full instructions, scales, and recommendation definitions are printed in each validation casebook.

### C1 — Clinical plausibility

Does the complete case represent a believable inpatient encounter?

### C2 — Intended assessment problem

Where an intended problem is specified for formal validation, is it actually present and correctly represented?

### C3 — Detectability

Could an internal-medicine resident identify and resolve the intended issue using the information provided?

### C4 — No unintended competing problem

Is there another clinically meaningful medication-reconciliation or transition-of-care issue that could reasonably be interpreted as an alternative target?

### C5 — Expected difficulty

How difficult is the case likely to be for the intended learner? Actual difficulty is determined later from resident performance, not from this estimate alone.

## Why human review is still required

Automated checks assess structure, terminology consistency, implemented medication rules, temporal consistency, and export fidelity.

They do not establish clinical realism, educational appropriateness, fair detectability, absence of a clinically meaningful alternative interpretation, or actual learner difficulty. Those judgments require human review. Automated checking is not clinical validation.

## Export verification

[View the DOCX export QA report](DOCX_EXPORT_QA.md)

The report for this package records:

- Balanced set `CLINIPROOF_BALANCED_V4`: 24 cases expected and 24 exported, VAL-701–VAL-724, no missing or duplicate case identifiers
- Seed-guided set `CLINIPROOF_SEEDCASES_V3`: 24 cases expected and 24 exported, VAL-801–VAL-824, no missing or duplicate case identifiers
- Medication mismatches: 0 in each set
- Numeric mismatches: 0 in each set
- Unsupported or generated patient-specific facts: 0 in each set
- Answer-key leakage in those chart-only files: none
- Result: PASS for both chart-only sets and for that codebook check

The validation casebooks intentionally include each case's investigator reference after C1. [Casebook QA](VALIDATION_CASEBOOK_QA.md) checks that this reference matches the batch plan and the answer key, and that the chart still matches the resident-facing source.

Historical case-set versions are retained elsewhere in the repository for provenance.
