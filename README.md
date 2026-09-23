# Clinical Case Generator / CliniProof

CliniProof creates synthetic inpatient medication-reconciliation cases for resident and clinician review. Each case is meant to be read like a hospital chart: who the patient is, why they were admitted, what they take at home, what they received in the hospital, what they leave with, and what follow-up is arranged.

The software loads official terminology, applies a small set of source-backed clinical rules, builds a structured clean case, and may then introduce exactly one pre-specified reconciliation problem. Each active prospective set includes four clean controls so reviewers cannot assume that every case contains an error. This README does not list which public identifiers are controls in the resident-facing sections below.

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians.

The generator does not invent RxNorm, LOINC, SNOMED CT, ICD-10-CM, UCUM, or device identifiers. It does not send raw MIMIC patient rows, notes, identifiers, or events to OpenAI. Until clinicians finish review, treat every generated record as a machine-validated synthetic resident-review case pending clinician validation.

There are **two active prospective validation datasets**, totaling **48** cases. The original freeze `CLINIPROOF_TAXONOMY_V1` (VAL-201–VAL-224) is preserved as historical provenance and is **not** the current study set. The study design now evaluates two newer generation strategies. Each assessment category has a standardized identifier, such as `f1_omission` for a medication that is unintentionally absent at discharge or `f2_monitoring_not_arranged` for a medication that is continued without the required follow-up monitoring. The taxonomy also defines required companion medication omitted (`f2_coprescription_omitted`). That category is not included in the current validation sets because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category.

This repository has no resident review user interface. Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass.

Navigation for reviewers: [`data/active_validation_sets.md`](data/active_validation_sets.md). Registry: [`data/validation_registry.json`](data/validation_registry.json).

# Current prospective validation datasets

## 1. CLINIPROOF_BALANCED_V3

- 24 cases, VAL-501–VAL-524
- `generation_strategy = balanced_structured`
- balanced structured scenario generation with 24 distinct clinical profiles
- clinical-coherence correction of the preclinical freeze `CLINIPROOF_BALANCED_V2`
- controlled error injection after clean-case generation
- pending clinician validation

Links: [all cases](data/validation_balanced_v3/readable/all_cases.md) · [clinician packet](data/validation_balanced_v3/readable/clinician_validation_packet.md) · [worksheet](data/validation_balanced_v3/readable/clinical_validation_worksheet.csv) · [diversity report](data/validation_balanced_v3/diversity_report.md) · [investigator key](data/validation_balanced_v3/investigator_answer_key.md)

## 2. CLINIPROOF_SEEDCASES_V2

- 24 cases, VAL-601–VAL-624
- `generation_strategy = resident_seed_guided`
- derived from expert-authored clinical archetypes
- synthetic, not copies of resident cases
- clinical-coherence correction of the preclinical freeze `CLINIPROOF_SEEDCASES_V1`
- controlled error injection after clean-case generation
- pending clinician validation

Links: [all cases](data/validation_seedcases_v2/readable/all_cases.md) · [clinician packet](data/validation_seedcases_v2/readable/clinician_validation_packet.md) · [worksheet](data/validation_seedcases_v2/readable/clinical_validation_worksheet.csv) · [diversity report](data/validation_seedcases_v2/diversity_report.md) · [investigator key](data/validation_seedcases_v2/investigator_answer_key.md)

# Historical / preclinical-QC datasets

## CLINIPROOF_TAXONOMY_V1

- VAL-201–VAL-224
- original template/randomized set (`generation_strategy = original_template_randomized`)
- preserved for provenance under [`data/validation/`](data/validation/)
- superseded for prospective validation by the two active datasets
- **not** the current study set

This archive is not labeled clinically invalid. It was superseded as the active prospective set because the study design now evaluates two newer generation strategies.

## CLINIPROOF_BALANCED_V2 and CLINIPROOF_SEEDCASES_V1

These merged freezes (VAL-301–VAL-324 and VAL-401–VAL-424) are **preclinical-QC versions**. They were not mutated in place. The corrected active revisions are `CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2`. They are **not** active prospective study sets.

## Where should I start?

The table below routes new reviewers to the two **active** datasets. Do not start with archived VAL-201–VAL-224, VAL-301–VAL-324, or VAL-401–VAL-424.

| Audience | Balanced set `CLINIPROOF_BALANCED_V3` | Seed-derived set `CLINIPROOF_SEEDCASES_V2` |
| --- | --- | --- |
| Resident / blinded reviewer | [balanced readable cases](data/validation_balanced_v3/readable/all_cases.md) | [seed readable cases](data/validation_seedcases_v2/readable/all_cases.md) |
| Clinician validator | [balanced clinician packet](data/validation_balanced_v3/readable/clinician_validation_packet.md) | [seed clinician packet](data/validation_seedcases_v2/readable/clinician_validation_packet.md) |
| Clinician entering ratings | [balanced worksheet](data/validation_balanced_v3/readable/clinical_validation_worksheet.csv) | [seed worksheet](data/validation_seedcases_v2/readable/clinical_validation_worksheet.csv) |
| Investigator | [balanced answer key](data/validation_balanced_v3/investigator_answer_key.md) | [seed answer key](data/validation_seedcases_v2/investigator_answer_key.md) |
| Diversity audit | [balanced diversity report](data/validation_balanced_v3/diversity_report.md) | [seed diversity report](data/validation_seedcases_v2/diversity_report.md) |
| Rubric | [balanced rubric](data/validation_balanced_v3/readable/validation_rubric.md) | [seed rubric](data/validation_seedcases_v2/readable/validation_rubric.md) |

## What CliniProof is

CliniProof is a generator of synthetic inpatient charts used to assess medication reconciliation. Medication reconciliation means comparing home, hospital, and discharge therapy, then ensuring that holds, stops, continuations, monitoring, supply, and follow-up are explicit.

Worked educational examples, which are not members of the blinded study set, appear in [For Clinicians: How a Synthetic Case Is Built](#for-clinicians-how-a-synthetic-case-is-built). Standardized identifiers are defined in [CliniProof error taxonomy](#cliniproof-error-taxonomy).

## Why medication reconciliation is being assessed

Discharge is a high-risk transition. A drug can be omitted, continued when it should stop, given at the wrong dose or frequency, or continued without the monitoring or restart plan that makes it safe. CliniProof cases let reviewers practice finding one known problem, or confirming that a control chart has none, from documents alone.

## What a case contains

A readable case is organized as a chart review: patient overview, reason for hospitalization, history, hospital course, vitals and labs, home medications, medications during hospitalization, discharge medications, follow-up, and instructions. Medication, diagnosis, and laboratory concepts are retrieved from official terminologies. Ages, vital signs, and laboratory values are synthetic.

## How cases are built

See [Case-generation methods](#case-generation-methods). Narrative wording is template text, or optionally a language model restating already chosen facts. OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. It does not choose diagnoses, medications, terminology codes, error categories, clinical rules, or answer-key content. The committed active prospective sets, and the archived freezes, used template narrative rather than OpenAI.

## Case-generation methods

CliniProof uses two complementary synthetic case-generation strategies for prospective validation. Both strategies construct a clinically coherent clean case before applying any experimental medication-reconciliation error. Canonical medication, diagnosis, and laboratory concepts are resolved from the project's source-backed terminology tables; patient-specific demographics, numeric results, and narrative context are synthetic. Error category assignment is deterministic and separate from clinical-case construction.

### Balanced structured generation

The balanced structured set is generated from predefined clinical scenario families and named clinical profiles. The batch is deliberately balanced across supported scenario families rather than sampled according to disease prevalence. Each profile specifies clinically meaningful features such as presentation, medications, relevant laboratory testing, hospital-course structure, and discharge/follow-up requirements.

Generation follows:

1. select scenario family;
2. select a distinct clinical profile;
3. construct a synthetic clean case;
4. validate terminology, units, route/form compatibility, clinical structure, and implemented hard rules;
5. audit clean-case uniqueness;
6. confirm eligibility for the preassigned CliniProof target;
7. inject exactly one controlled medication-reconciliation discrepancy or transition-of-care gap, or retain the case as a clean control;
8. revalidate the modified case;
9. freeze and export separate resident-facing and investigator-facing artifacts.

Case diversity is measured on the clean case before error injection. Differences in identifiers, random seed, demographics, exact numeric values, or planted error category do not by themselves establish clinical uniqueness.

The current active balanced batch is `CLINIPROOF_BALANCED_V3` (VAL-501–VAL-524). It supersedes the preclinical-QC freeze `CLINIPROOF_BALANCED_V2` (VAL-301–VAL-324), which remains archived and was not mutated.

### Resident-seed-guided generation

The resident-seed-guided set begins with resident-authored clinical examples representing realistic medication-reconciliation and transition-of-care workflows. The source cases are used as clinical design references and are not copied directly into the study dataset.

Each resident case is abstracted into a reusable clinical archetype describing relevant elements such as presentation, medication roles, inpatient medication changes, monitoring, follow-up, and discharge decisions. Multiple synthetic clinical profiles are then generated from each archetype. Patient-specific demographics, values, and chart details are newly synthesized, while canonical clinical concepts continue to be resolved through the same source-backed terminology pipeline used by the balanced generator.

The current archetype families include:

* medication-history uncertainty / delirium;
* acute heart-failure management;
* outpatient parenteral antimicrobial therapy / endocarditis;
* kidney-transplant infection and immunosuppression transitions;
* postoperative anticoagulation after hip fracture;
* gastrointestinal bleeding with anticoagulation or discharge-transition decisions.

The six resident-authored examples are not treated as an empirical dataset and are not used to estimate diagnosis prevalence, medication prevalence, error frequency, or outcome probabilities.

Generation follows:

1. select resident-derived archetype;
2. select a distinct profile within that archetype;
3. synthesize a new clean patient encounter;
4. resolve coded clinical concepts from source-backed terminology;
5. validate clinical structure and implemented constraints;
6. audit within- and across-archetype diversity;
7. confirm error-category eligibility;
8. inject exactly one predetermined CliniProof error or retain a clean control;
9. revalidate, freeze, and export blinded resident and investigator materials separately.

The current active seed-guided batch is `CLINIPROOF_SEEDCASES_V2` (VAL-601–VAL-624). It supersedes the preclinical-QC freeze `CLINIPROOF_SEEDCASES_V1` (VAL-401–VAL-424), which remains archived and was not mutated.

### Relationship between the two sets

The two case sets represent different synthetic-generation strategies and are maintained as separate prospective validation datasets.

The balanced set emphasizes controlled coverage and structural diversity across predefined scenario families.

The resident-seed-guided set emphasizes workflow realism derived from expert-authored clinical examples.

Neither strategy is assumed to be clinically valid solely because it passes software checks. All generated cases remain subject to the same one-stage clinician review using C1–C5 before resident-study use.

### Source versus synthetic content

| Component                            | Balanced set                   | Seed-guided set                         |
| ------------------------------------ | ------------------------------ | --------------------------------------- |
| Clinical architecture                | predefined structured profiles | abstracted resident-authored archetypes |
| Diagnosis/medication/lab terminology | source-backed reference tables | same source-backed reference tables     |
| Patient demographics                 | synthetic                      | synthetic                               |
| Numeric vitals/labs                  | synthetic                      | synthetic                               |
| Exact narrative                      | synthetic                      | synthetic                               |
| Error assignment                     | predetermined, deterministic   | predetermined, deterministic            |
| Resident source case copied verbatim | N/A                            | No                                      |
| Prevalence-weighted                  | No                             | No                                      |
| Requires clinician validation        | Yes                            | Yes                                     |

### Source-backed terminology is not clinical truth

Terminology provenance validates concept identity: an RXCUI, LOINC code, or ICD-10-CM code on a case was retrieved from an official source rather than invented. Structured clinical rules validate only the constraints that are implemented in software, such as unit/value coupling, route/form compatibility, and the single intended experimental discrepancy. Those checks do not independently prove clinical plausibility, educational appropriateness, or representativeness of practice. Clinician validation remains necessary.

## Clean-case uniqueness

Case diversity is evaluated on the **clean clinical case before error injection**. Different seeds, demographics, numeric vital or laboratory values, or planted CliniProof error categories do not by themselves make two cases clinically unique.

A validation case must represent a distinct underlying clinical scenario before experimental error injection. Two cases must not differ only by patient age or sex, a random seed, anticoagulant selection, or the injected Family 1 / Family 2 category.

The generator now names a clinical profile inside each scenario family (for example several heart-failure or atrial-fibrillation variants). Each profile specifies a permitted symptom set, duration and course, medication subset, laboratory subset, hospital-course pattern, and follow-up structure using only source-backed concepts. After the clean case is validated, the software computes a fingerprint that excludes VAL/SYN identifiers, seed, exact age, sex, weight, vital numbers, laboratory numbers, and the intended error. Exact fingerprint matches raise `DuplicateClinicalCaseError` and the batch is not frozen. Weighted similarity of 0.85 or higher is also rejected. Scores between 0.70 and 0.85 are reported as investigator warnings.

The archived freeze `CLINIPROOF_TAXONOMY_V1` (VAL-201–VAL-224) remains unchanged as historical provenance. The two **active** prospective sets are `CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2`. Preclinical-QC archives `CLINIPROOF_BALANCED_V2` and `CLINIPROOF_SEEDCASES_V1` remain unchanged. Passing the diversity audit does not mean the cases are clinically validated. Human clinician review is still required.

## Family 1 and Family 2

Family 1 (`family_1`) means the medication list is wrong at the transition to discharge. The implemented categories are a medication omitted at discharge (`f1_omission`), a medication inappropriately added or continued (`f1_commission`), an unexplained dose discrepancy (`f1_dose_mismatch`), an unexplained route discrepancy (`f1_route_mismatch`), an unexplained frequency discrepancy (`f1_frequency_mismatch`), and an unexplained therapeutic substitution (`f1_therapeutic_substitution`).

Family 2 (`family_2`) means a transition action is missing even if the drug list looks intact. The implemented categories are required outpatient monitoring not arranged (`f2_monitoring_not_arranged`), held medication without a restart plan (`f2_held_med_no_restart_plan`), insufficient medication supply (`f2_insufficient_supply`), hospital-only medication continued after discharge (`f2_hospital_only_continued`), temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`), and follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`). Do not identify Family 2 solely by comparing lists.

## Machine validation versus clinician validation

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians.

Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass. Use the packets for the two active sets in [Where should I start?](#where-should-i-start).

## Active prospective sets

See [Current prospective validation datasets](#current-prospective-validation-datasets). Frozen JSON for each active batch is that batch’s source of truth and must not be regenerated to improve clinical content. Archived `CLINIPROOF_TAXONOMY_V1` files must not be rewritten either.

## Human-readable review materials

See [Human-readable clinician validation packets](#human-readable-clinician-validation-packets) and the starting-point table above. Active case pages are VAL-501–VAL-524 and VAL-601–VAL-624. Archived VAL-201–VAL-224, VAL-301–VAL-324, and VAL-401–VAL-424 remain available for provenance.

---

## Contents

**Start here by audience:** [Where should I start?](#where-should-i-start)

**Methods:** [Case-generation methods](#case-generation-methods)

**Clinician walkthrough:** [For Clinicians: How a Synthetic Case Is Built](#for-clinicians-how-a-synthetic-case-is-built)

1. [Project overview](#1-project-overview)
2. [Quick start](#2-quick-start)
3. [Architecture and repository layout](#3-architecture-and-repository-layout)
4. [Prerequisites](#4-prerequisites)
5. [Clone and initial setup](#5-clone-and-initial-setup)
6. [Environment configuration](#6-environment-configuration)
7. [Start PostgreSQL](#7-start-postgresql)
8. [Initialize the database](#8-initialize-the-database)
9. [Reference terminology](#9-reference-terminology)
10. [Bootstrap reference data](#10-bootstrap-reference-data)
11. [Individual terminology sync commands](#11-individual-terminology-sync-commands)
12. [Clinical rules](#12-clinical-rules)
13. [Generate synthetic cases](#13-generate-synthetic-cases)
14. [OpenAI usage](#14-openai-usage)
15. [Validate generated cases](#15-validate-generated-cases)
16. [Resident-validation workflow](#16-resident-validation-workflow)
17. [Resident-validation output files](#17-resident-validation-output-files)
18. [How to give cases to residents](#18-how-to-give-cases-to-residents)
19. [Reproducing the frozen validation batch](#19-reproducing-the-frozen-validation-batch)
20. [API](#20-api)
21. [Testing and code quality](#21-testing-and-code-quality)
22. [Common workflows](#22-common-workflows)
23. [Troubleshooting](#23-troubleshooting)
24. [Data provenance and safety constraints](#24-data-provenance-and-safety-constraints)
25. [Database, tables, and UML](#25-database-tables-and-uml)
26. [Current limitations](#26-current-limitations)
27. [Licensing](#27-licensing)

**Error taxonomy (CliniProof):** [CliniProof error taxonomy](#cliniproof-error-taxonomy)

**Readable clinician packets:** [Human-readable clinician validation packets](#human-readable-clinician-validation-packets)

---

## 1. Project overview

### What this repository does

The application:

1. Talks to official terminology services (RxNav, LOINC FHIR, UCUM essence XML, NLM ICD-10-CM, NLM conditions, NLM HPO, DailyMed, RxClass).
2. Stores only identifiers and text those sources return, with provenance (`source_system`, `source_version`, `retrieved_at`).
3. Enables curated clinical conditionals only when DailyMed or RxClass evidence is attached.
4. Builds synthetic inpatient cases from **already stored** `ref_*` rows.
5. Validates each case (structural, terminology, hard clinical rules, assessment consistency for Family 1 and Family 2).
6. Optionally plants **exactly one** pre-specified CliniProof error after the target category is selected. An LLM never chooses the error.
7. Freezes a resident-review batch as immutable `VAL-*` IDs and exports a **blinded** resident JSON plus an **investigator** answer key.

The command-line entry point declared in `pyproject.toml` is `clinical-case-generator = "app.cli:main"`. After installation, operators invoke the tool as `clinical-case-generator`.

### Problem it solves

Medication-reconciliation review studies need realistic-looking cases with known (hidden) **assessment** errors — Family 1 discharge-list mismatches and Family 2 transition-of-care gaps — using **canonical codes that can be cited**. This tool generates those cases from official vocabularies instead of free-text invention, then blinds the answer key for residents.

### Three data classes

**Authoritative reference data.** RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, and AccessGUDID *concepts* live in `ref_*` tables. Every real reference row keeps `source_system`, `source_version`, and a timezone-aware `retrieved_at`. Targeted sync and `bootstrap-reference-data` upsert **only** identifiers returned by official sources. DailyMed labels are stored when an RXCUI is already validated through RxNorm. SNOMED CT fields remain null rather than invented; there is **no SNOMED ingestion client** in this repository even if SNOMED environment variables are set. AccessGUDID and MIMIC ingestion are not implemented.

**Empirical aggregate data.** `ref_clinical_distributions` is for statistics calculated locally from a permitted dataset. Aggregates are not patient rows. A check constraint rejects `source_dataset = 'MIMIC_IV_RAW'`. This pipeline inserts no distribution rows and does not invent empirical distributions.

**Synthetic patient data.** `clinical_cases` and child tables hold generated cases. Unknown scalars are `NULL`, not empty strings. Dashboard business ids are assigned in Python after structured generation (`SYN-000001`, `DX-SYN000001-001`, and the other prefixes in `app/utils/identifiers.py`). Canonical concepts on a case must already exist in local reference tables. Numeric vital and laboratory values are synthetic and labeled `synthetic_model_generated`; they are not MIMIC empirical draws.

### What OpenAI is and is not used for

OpenAI is optional in the CliniProof pipeline and is used only to help word admission narrative text (chief complaint, history of present illness, and note) from structured facts that have already been selected by the generator, including age, sex, diagnosis name, symptom names, medication names, and a template chief-complaint seed. See [OpenAI usage](#14-openai-usage).

OpenAI is **not** used to choose or invent diagnoses, RXCUIs, LOINC codes, ICD-10-CM codes, UCUM codes, clinical rules, error categories, error families, or answer-key contents. Raw MIMIC and other patient-source rows are never sent. Structured cases are **not** wholly LLM-generated.

`freeze-validation-batch` hardcodes `use_openai=False`, so the committed `CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2` freezes, and the archived `CLINIPROOF_TAXONOMY_V1`, `CLINIPROOF_BALANCED_V2`, and `CLINIPROOF_SEEDCASES_V1` freezes, used template narrative only.

### Clinical validation

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians. Until that review is complete, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

---

## For Clinicians: How a Synthetic Case Is Built

This section is for physicians and clinical reviewers. It explains how a synthetic inpatient case is assembled, using language from ordinary clinical work (presentation, admission diagnosis, home / inpatient / discharge medications, medication reconciliation) rather than software architecture.

**Worked examples below are educational demonstrations**, not members of the blinded resident-validation study. They were generated with the same code path as the study freeze (`app/services/generation.py`), with template admission wording (no OpenAI call), sequences **901–904**, and seed **20260926**. Snapshots: [`data/docs/clinician_examples/`](data/docs/clinician_examples/). Active study cases for residents are VAL-501–VAL-524 and VAL-601–VAL-624. This walkthrough does **not** say which `VAL-*` cases are controls or which discrepancy was planted.

Until a clinician finishes review, treat every generated record as a machine-validated synthetic resident-review case pending clinician validation. The software has checked structure and implemented rules; it has not certified clinical realism.

The implemented pipeline is not “ask a language model to make a clinical case and then find an error.” The order of operations is: an assessment or batch specification is written; a scenario is selected; canonical terminology is resolved from local authoritative reference tables; a deterministic structured clean case is generated; source-backed clinical rules are applied; the clean case is machine-validated; eligibility for the requested standardized error category is checked; the exact requested error is injected deterministically, or skipped for a clean control; hidden assessment and answer-key state is recorded; post-injection category-aware validation runs; the case is frozen under an immutable VAL identifier; and blinded resident and investigator exports are written.

The requested error category is selected **prospectively**. Ineligible categories **abort**. They do **not** silently substitute another category. Planned category, injected category, and answer-key category must agree. Every error-bearing case in an active freeze has exactly one intended injected assessment target. Clean controls have zero. The clean expected state and injected state are retained in the concealed assessment data.

A language model is optional and, when used, only rewords admission narrative from already-chosen facts. OpenAI does not choose diagnoses, medications, terminology codes, error categories, clinical rules, or answer-key content. The committed prospective freezes do not call a language model (`freeze-validation-batch` sets `use_openai=False` in `app/cli/__init__.py`). These demonstration cases also used template wording because `OPENAI_API_KEY` was empty, so `narrative_source` is `template` in `app/openai/narrative.py`.

The following table distinguishes six kinds of content that can appear on a case. Official terminology rows are not the same thing as real patient measurements. Synthetic numbers are not MIMIC rows. Assessment discrepancies are hidden from residents.

| Kind | What it is | Clinical implication |
| --- | --- | --- |
| **Source-backed clinical concept** | A diagnosis, medication, laboratory *test*, unit, or symptom name stored locally after an official terminology service returned it | You can cite the identifier (ICD-10-CM, RXCUI, LOINC). The software did not invent the code. |
| **Synthetic patient-specific value** | Age, sex, blood pressure, heart rate, the *numeric* lab result, weight, display name | These numbers were drawn by a seeded random generator. They are **not** measurements from a real patient and are **not** MIMIC rows. |
| **Deterministic clinical rule** | A stored IF/THEN constraint, enabled only when DailyMed or RxClass evidence was attached | Only three rules exist. They are not a complete heart-failure or pneumonia guideline. |
| **Narrative wording** | Chief complaint, HPI, admission note | Template sentences (or optional OpenAI rewording) built from names already selected. Not a source of new diagnoses or drugs. |
| **Assessment discrepancy (CliniProof)** | At most one controlled change after the clean case passed machine validation. **Family 1** changes the discharge list. **Family 2** typically leaves the continued-drug identity intact and removes a required companion action (monitoring, restart plan, supply, follow-up, or similar). | Present only when error injection is turned on. Hidden from residents. |
| **Human clinical validation** | Resident or investigator judgment | Software cannot certify that the picture is realistic, complete, or appropriate for teaching. |

Those six kinds of content are stored in PostgreSQL as described in [Database, tables, and UML](#25-database-tables-and-uml). Residents do not query the database; they receive a blinded JSON export.

---

## The Case Generation Process — Clinical View

The thirteen steps below follow `generate_one_case` in [`app/services/generation.py`](app/services/generation.py). Study freeze adds the freeze and export steps (`app/services/validation_batch.py`). The last step is clinician review, which is not performed by software. Each step is written as ordinary clinical and technical explanation rather than as a labeled checklist.

### 1. Select a clinical scenario

What happens at this step is that an operator, or the freeze plan, chooses one inpatient teaching family from [`data/bootstrap/scenarios.json`](data/bootstrap/scenarios.json). The family is a teaching skeleton. It names the specialty, age band, diagnosis search text, symptom search text, medication search text, an optional stop medication, an optional hospital-only medication, an optional anticoagulant either-or list, laboratory search text, and which standardized CliniProof error categories (`f1_*` / `f2_*`) are allowed.

For example, the heart-failure family `HF_INPATIENT` is a cardiology inpatient skeleton for ages 55 through 85. Its diagnosis query is `heart failure`. Its symptom queries are `dyspnea`, `edema`, and `orthopnea`. Its continue-medication queries are lisinopril, furosemide, metoprolol, spironolactone, and atorvastatin. Its stop query is `ibuprofen`. Its hospital-only query is `pantoprazole`, which is constructed only when the target category is hospital-only medication continued after discharge (`f2_hospital_only_continued`). Its anticoagulant mutex chooses warfarin or apixaban, but not both. Its laboratory queries are potassium, creatinine, INR, and natriuretic peptide.

This matters clinically because the scenario decides the problem-list theme and which drug classes will appear. It does not yet pick a specific RxNorm identifier (RXCUI) or ICD-10-CM code.

There is no authoritative terminology source at this step. The scenario file is a curated search list, not a codebook. No patient-specific synthetic values have been generated yet. The software automatically rejects unknown scenario codes at freeze time.

Whether five inpatient families are enough for a given study remains a protocol question for physicians, not a software check.

### 2. Resolve clinical concepts

What happens next is that, for each search phrase, Python looks up already stored local reference rows. Diagnosis, medication, and laboratory matching live in `match_diagnosis`, `match_medication`, and `match_lab` in [`app/services/bootstrap.py`](app/services/bootstrap.py); symptoms are matched through `search_symptoms`. Those rows were filled earlier by `bootstrap-reference-data` from official APIs listed in [`data/bootstrap/manifest.json`](data/bootstrap/manifest.json). Combination RxNorm products are filtered at bootstrap. Official LOINC term codes are stored; LOINC Parts are not. SNOMED CT is not ingested, so `snomed_code` stays null rather than being invented.

For example, the query `heart failure` resolves to local ICD-10-CM **I50.20**, “Unspecified systolic (congestive) heart failure.” The query `lisinopril` resolves to RxNorm **1806884**, “lisinopril 1 MG/ML Oral Solution.” The query `creatinine` resolves to LOINC **14682-9**. The query `edema` resolves to the NLM conditions name **Anasarca** by token match, not because the stored preferred name is the word “edema.” The query `orthopnea` resolves to the NLM HPO name **Orthopnea**; `snomed_code` remains null, and the synonym list contains `HP:0012764`, which is an HPO identifier and is not written into `snomed_code`.

This matters clinically because every named drug, diagnosis, and laboratory concept on the case is traceable to an official code that the source actually returned. Ranking can prefer an oral solution or an oximetry hemoglobin term over the tablet or methodless term a clinician might expect.

The authoritative sources at this step are RxNav, NLM ICD-10-CM, LOINC FHIR terminology services, NLM conditions, NLM HPO, UCUM essence XML for units, DailyMed for later label text, and RxClass for rule evidence and medication-class membership. The search phrases in the scenario file are synthetic teaching queries. The identifiers those queries retrieve are not.

If a required diagnosis, medication, or laboratory query does not resolve, generation raises `ReferenceResolutionError` and does not invent a code. Whether I50.20, an oral-solution lisinopril, or hemoglobin LOINC 55782-7 (oximetry) is a fair teaching proxy is a reviewer judgment.

### 3. Apply clinical constraints (before the patient is built)

What happens here is that `_assert_rules_allow` builds a snapshot of the chosen ICD-10-CM codes, RxNorm identifiers, and LOINC codes and runs hard rules in `app/services/rules.py`. If a hard rule fails, generation stops. Soft rules become warnings later; they do not block construction.

For example, warfarin and apixaban are never both selected. That restriction is both the anticoagulant mutex in the scenario and the hard rule `NO_DUAL_ORAL_ANTICOAGULANT`. If warfarin is selected, INR LOINC `38875-1` must be among the laboratories because of `WARFARIN_INR_MONITORING`.

This matters clinically because the machine prevents two implemented unsafe patterns. It does not encode guideline-directed medical therapy completeness, antibiotic duration, or renal dosing. A rule is enabled only when DailyMed or RxClass evidence is attached in `data/bootstrap/rule_templates.json`. Terminology lookup alone does not turn a rule on. No patient-specific synthetic values are created at this step. Hard violations abort generation. Absence of a guideline in this engine is not evidence that the guideline is unimportant.

### 4. Generate patient-specific synthetic values

A Python `random.Random` object is then seeded with `{seed}:{sequence}:{scenario}`, for example `20260926:901:HF_INPATIENT`. Age is drawn in the scenario band. Sex is `Female` or `Male`. Weight is drawn between 60 and 110 kg. Blood pressure, heart rate, respiratory rate, and SpO2 come from integer ranges. Temperature is fixed at `36.8`. Laboratory numbers use analyte-specific draws in `_synthetic_lab_value`. The display name is `SYN Patient {sequence}`. Numeric origin is labeled `synthetic_model_generated` on generation metadata and on some dose notes in `app/services/generation.py`.

The demonstration heart-failure case `SYN-000901` is an 83-year-old man weighing 69 kg, with blood pressure 124/70, heart rate 108, respiratory rate 23, SpO2 98%, and creatinine **1.6** with unit `umol/L`.

This matters clinically because the laboratory concept, creatinine LOINC 14682-9, is source-backed, while the result 1.6 umol/L is synthetic and uses the first example UCUM unit stored on that LOINC row, which is often an SI moles-per-volume unit. Do not read it as a real patient’s mg/dL creatinine. There is no authoritative source for the numbers themselves. Units come from stored LOINC example UCUM text. Age, sex, name, weight, vital signs, laboratory numbers, and intake and output are synthetic. The ranges are code constants, not physiologic plausibility checks. Whether heart rate 108 with blood pressure 124/70 and SpO2 98% forms a coherent decompensated-heart-failure picture is a clinical question. The machine does not score that.

### 5. Word the narrative

`_template_narrative` writes the chief complaint, history of present illness, and an admission note from the already chosen age, sex, diagnosis name, symptom names, and medication names. If OpenAI is enabled and a key is set, `assemble_narrative` may reword those facts. Unknown drugs or diagnoses in the model text cause fallback to the template. Freeze never calls OpenAI.

On `SYN-000901`, the chief complaint is “Dyspnea, Anasarca, Orthopnea in the setting of Unspecified systolic (congestive) heart failure,” and the note `source_type` is `template`.

This matters clinically because the prose is a label on structured facts, not an independent history. There is no authoritative source for the sentences. The sentences themselves are synthetic. OpenAI output is rejected if none of the allowed names appear (`_narrative_rejected`). Freeze skips OpenAI entirely. Template history of present illness is short and generic, and reviewers may judge it too thin for a real admission note.

### 6. Construct medication timelines

Each continue medication is written three times: at home (`status: home`), in the hospital (`status: active`), and at discharge (`status: discharge`), at the same dose and `once daily`. Each stop medication is written on the home and inpatient lists as `held`, and it is absent from the clean discharge list. A `CaseMedicationPlan` row records the intended reconciliation decision, continue versus stop. Dose is the RxNorm `strength` string when present; otherwise the synthetic fallback is **`1 tablet`**.

The heart-failure medication table in Worked Example 1 shows this pattern on a complete chart.

This matters clinically because review is about transitions from home through hospital to discharge, not about whether a drug name is a valid RxNorm concept. The drug concept and RXCUI are source-backed. The dose string often copies RxNorm strength, and `1 tablet` is a synthetic fallback. The three-context copies, the default frequency `once daily`, and the fallback dose are synthetic. Later, the assessment layer counts mechanically detectable findings, including Family 1 discharge or plan mismatches and Family 2 missing companion actions. Oral-solution ACE inhibitor, topical ibuprofen as the NSAID, and `1 tablet` of furosemide solution are ranking and fallback artifacts. They are not a claim that this is usual inpatient prescribing.

### 7. Create the clean structured case

Remaining dashboard arrays are filled with constants or simple templates: living situation “Lives at home,” symptom duration “several days,” severity “moderate,” course “worsening,” primary-care follow-up in 7 days, the medication instruction “Take discharge medications exactly as listed,” and disposition home. If warfarin and INR are both present, a monitoring row is added (`_maybe_add_warfarin_monitoring`). A clean-state snapshot is stored for the investigator key.

`SYN-000901` has INR monitoring labeled as arranged because warfarin was selected. `SYN-000904` selected apixaban, so that monitoring row is absent, even though INR is still on the laboratory list because the heart-failure laboratory list always includes the INR query.

This matters clinically because much of the chart is scaffolding. Empty allergies and null ethnicity are empty fields, not a claim that “none documented” after a real interview. Only fields linked to `ref_*` rows are source-backed. Social support, follow-up, instructions, the problem-list plan sentence, and return precautions are synthetic. The structural layer requires at least one diagnosis and legal medication contexts. Whether missing allergies, language “English,” and a single problem are acceptable for teaching is a physician judgment.

### 8. Perform machine validation (clean case)

`validate_case` in [`app/services/validation.py`](app/services/validation.py) then runs four layers: structural, terminology, clinical hard rules, and assessment. On a clean case the assessment layer requires zero mechanically detectable findings and no answer key. `require_valid` aborts on failure.

On `SYN-000901`, all four layers report `passed: true`, and `rules` is empty. There are no hard or soft violations; furosemide is paired with I50.20, so the soft allow-rule does not fire.

This is integrity checking, not a finding that therapy is appropriate. The terminology layer checks that identifiers still resolve to provenance-bearing `ref_*` rows. External APIs are not called on this read. Everything else remains a clinician question; see [Why machine validation is not clinical validation](#why-machine-validation-is-not-clinical-validation).

### 9. Optionally inject one controlled CliniProof error

The assessment blueprint selects the target error family and category first. A clinically suitable clean case is then constructed for that target, preconditions are checked, the clean case is machine-validated, and only then does `inject_reconciliation_error` in [`app/services/error_injection.py`](app/services/error_injection.py) plant exactly one discrepancy using the same random-number generator. OpenAI does not choose the error. If the requested category is unknown, marked `not_yet_implementable`, or ineligible for that case, generation fails. It does not silently switch to another category.

The current dataset uses the canonical CliniProof taxonomy. Family 1 names medication-reconciliation discrepancies on the lists themselves. Family 2 names transition-of-care gaps. Clean controls have no planted target. The identifiers and clinical meanings are in [CliniProof error taxonomy](#cliniproof-error-taxonomy).

The educational case `SYN-000904`, in the investigator-only section below, omits one continued medication, apixaban, from discharge. That is a Family 1 medication omitted at discharge (`f1_omission`). Demonstration cases 901 through 903 used `--no-inject-error` and have no planted discrepancy.

The study signal is a specified assessment error, not whatever discrepancy happened to appear after generation. There is no authoritative source for the mutation itself. Trigger medications, class membership from RxClass, and monitoring rules remain source-backed. The mutation is synthetic. Software then checks deterministic preconditions (`eligible_errors`), that the requested category equals the injected category and the answer-key category, mechanical error-isolation, and a leak audit on the resident export. Clinical coherence, error fidelity, evidentiary sufficiency, error isolation beyond mechanical checks, cue integrity, and educational appropriateness remain physician judgments.

### 10. Revalidate and save

Validation runs again with `expect_injected_error` matching whether injection occurred. Family 1 is checked as a medication-plan mutation. Family 2 is checked as a present trigger plus a required companion action that is now absent, with evidence remaining in the resident-visible case. A `CaseGenerationRun` stores seed, generator version, narrative source, rule list, and validation reports.

On `SYN-000904`, post-injection validation still passes because the assessment layer expects the requested category.

A planted assessment error is allowed to remain; it is not “fixed” by the validator. Machine validation does not mean the case is clinically valid. Software checks that the requested category, injected kind, and answer-key category agree, that structural, terminology, and hard-rule layers still pass, and that a second mechanically detectable discrepancy was not introduced. Everything the machine cannot see remains a clinician question; see [CliniProof error taxonomy](#cliniproof-error-taxonomy).

### 11. Freeze the validation case (study path only)

`freeze-validation-batch` generates as above with `use_openai=False`, audits that there are no `TEST_` identifiers and that the plan matches control versus error, and writes an immutable `VAL-###` row in `validation_batch_cases`. A second freeze reuses matching VAL identifiers and will not overwrite them.

The archived freeze `CLINIPROOF_TAXONOMY_V1` assigned VAL-201 through VAL-224 to sequences 801 through 824. The active freeze `CLINIPROOF_BALANCED_V3` assigns VAL-501 through VAL-524 to sequences 1201 through 1224. The active freeze `CLINIPROOF_SEEDCASES_V2` assigns VAL-601 through VAL-624 to sequences 1301 through 1324. Preclinical-QC archives remain VAL-301–VAL-324 (sequences 1001–1024) and VAL-401–VAL-424 (sequences 1101–1124). Demonstration `SYN-000901` was not frozen into a VAL identifier. Freeze is an operational lock, not clinical sign-off.

### 12. Export resident-facing and investigator-facing versions

`export-validation-batch` writes a blinded resident JSON, with VAL identifiers, no answer key, RXCUI `source_reference` cleared, and titles rewritten, plus investigator files including the answer key, manifest, and coverage. `--batch-code` is required. There is no default study batch. A leak audit fails export if resident JSON contains markers such as `syn-000`, `answer_key`, or `is_clean_control`.

### 13. Obtain clinician validation

Clinical validation uses a single review stage. A clinician or resident reviews the complete frozen case once and completes C1–C5 in the same review. Ratings are recorded on the batch-specific worksheet (see [Where should I start?](#where-should-i-start)). Software does not fill those ratings. The review files are the clinician validation packets for `CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2`.

Separately, when the frozen cases are later administered as an assessment, residents who must find the planted problem themselves use the blinded JSON for the chosen active set — [`data/validation_balanced_v3/resident_validation_cases.json`](data/validation_balanced_v3/resident_validation_cases.json) or [`data/validation_seedcases_v2/resident_validation_cases.json`](data/validation_seedcases_v2/resident_validation_cases.json) — and the matching worksheet schema. That resident performance worksheet is not the clinician-validation form.

---

## CliniProof error taxonomy

The assessment target is selected before the final case is produced. An assessment blueprint names the target family and category. A clinically suitable clean case is then constructed, preconditions are verified, and the clean case is machine-validated. Exactly one target discrepancy is injected. Post-injection validation, an error-isolation audit, a hidden answer key, and a blinded resident export follow.

An LLM is never used to decide which error is planted. The injector is deterministic. If the category requested in `batch_plan.json` is not eligible for that scenario, freeze **rejects** the assignment instead of substituting another category.

### What the resident must notice

The table below lists each implemented or specified assessment category. The first column names the family in clinical language. The second column names the clinical problem. The third column is the software identifier used in investigator files. The last column says what a resident should be able to notice from the chart. Read the clinical name first; the identifier is a token for software and answer keys, not a substitute for the clinical meaning.

| Family | Clinical problem | Identifier | What the resident must notice |
| --- | --- | --- | --- |
| Family 1 — list-transition discrepancy | Medication omitted at discharge | `f1_omission` | A medication that should continue is absent from the discharge list |
| Family 1 — list-transition discrepancy | Medication inappropriately added or continued | `f1_commission` | An unindicated medication appears on the discharge list |
| Family 1 — list-transition discrepancy | Unexplained dose, route, or frequency discrepancy | `f1_dose_mismatch`, `f1_route_mismatch`, `f1_frequency_mismatch` | The discharge order differs from the intended plan without a documented rationale |
| Family 1 — list-transition discrepancy | Unexplained therapeutic substitution | `f1_therapeutic_substitution` | A different same-class drug appears without an explanation |
| Family 2 — transition-of-care gap | Required companion medication omitted | `f2_coprescription_omitted` | The trigger drug is present, but a required companion medication is absent |
| Family 2 — transition-of-care gap | Required outpatient monitoring not arranged | `f2_monitoring_not_arranged` | The trigger drug is present, but required monitoring is missing |
| Family 2 — transition-of-care gap | Held medication without a restart plan | `f2_held_med_no_restart_plan` | A legitimate hold has no documented resumption plan |
| Family 2 — transition-of-care gap | Insufficient medication supply | `f2_insufficient_supply` | Days’ supply does not last until the planned follow-up |
| Family 2 — transition-of-care gap | Hospital-only medication continued after discharge | `f2_hospital_only_continued` | An inpatient-only drug remains on the discharge list |
| Family 2 — transition-of-care gap | Temporary inpatient substitution not addressed at discharge | `f2_inpatient_substitution_not_reverted` | A temporary inpatient substitute persists without explanation |
| Family 2 — transition-of-care gap | Follow-up missing for an unresolved treatment decision | `f2_pending_decision_followup_missing` | An unresolved treatment decision has no planned reassessment |
| Clean control | No planted assessment problem | `none` | No planted discrepancy; the chart is an intact reconciliation |

The taxonomy also defines required companion medication omitted (`f2_coprescription_omitted`), which represents a situation in which a clinically required companion medication is missing. This category is not included in the current validation set because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category. Manuscript examples such as a steroid without a proton-pump inhibitor, or an opioid without a bowel regimen, are not hard-coded.

Do **not** treat every error-bearing case as “exactly one medication-list discrepancy.” That statement is true of Family 1 list-transition errors. It is **not** true of Family 2.

**Family 1** errors are medication-reconciliation and list-transition discrepancies: a medication omitted at discharge, a medication inappropriately added or continued, or an unexplained change in dose, route, frequency, or product.

**Family 2** errors are transition-of-care gaps that may leave the medication list itself unchanged. Implemented categories include required outpatient monitoring not arranged, held medication without a restart plan, insufficient supply, hospital-only medication continued, inpatient substitution not reverted, and missing follow-up for a pending therapeutic decision.

Validation is **category-aware**. For Family 2 the freeze checks that the trigger/precondition is present, the expected companion action exists in the clean state, the specified action is absent or incorrect after injection, resident-visible evidence needed for detection remains present, and no unintended second assessment target was introduced.

The freeze plan specifies the standardized family and category in each batch’s `batch_plan.json` before generation. Freeze and export require an explicit plan or batch code. The two active datasets use the canonical CliniProof taxonomy and cover implemented categories. Required companion medication omitted (`f2_coprescription_omitted`) is intentionally absent because it is `not_yet_implementable`. Unknown or obsolete category names fail rather than being translated.

### Example A — Family 1 dose mismatch (demonstration)

This is a teaching sketch. It is not a blinded `VAL-*` answer.

The clinical knowledge in this sketch is source-backed: lisinopril is a stored RxNorm concept, and the clean intended discharge plan continues it. The synthetic patient-specific information is that the patient has heart failure, and that home, inpatient, and intended discharge lists all show lisinopril **10 mg oral once daily**.

The deliberately injected assessment error is an unexplained dose discrepancy (`f1_dose_mismatch`). That category is selected first. After the clean case passes validation, only the discharge dose is changed to **20 mg**. Home and inpatient lists, diagnosis, and laboratories are left intact.

After injection, the resident-visible case shows lisinopril 20 mg oral once daily at discharge while home and inpatient lists still show 10 mg, with no documented rationale for a dose change.

The hidden investigator answer key records Family 1 (`family_1`), unexplained dose discrepancy (`f1_dose_mismatch`), the changed field `dose`, clean expected state `10 mg`, injected state `20 mg`, the trigger medication, evidence locations on the home and discharge medication lists, and the expected action, which is to restore the intended dose.

The same pattern applies to unexplained route discrepancy (`f1_route_mismatch`) and unexplained frequency discrepancy (`f1_frequency_mismatch`): the answer key preserves the field that changed, plus expected versus planted values. Medication omitted at discharge (`f1_omission`) removes the discharge row only. Medication inappropriately added or continued (`f1_commission`) copies an unindicated stop medication onto discharge.

### Example B — Family 2 monitoring not arranged (demonstration)

The clinical knowledge here is a source-backed rule. The enabled rule `WARFARIN_INR_MONITORING` (`require_lab`) is attached only when DailyMed or RxClass evidence exists. It is not inferred from the drug name.

The synthetic patient-specific information on the clean case is that warfarin is continued at discharge and that outpatient INR monitoring is arranged, stored as a `CaseMonitoring` row plus a medication monitoring note. Admission INR remains on the case as a laboratory result.

The deliberately injected assessment error is required outpatient monitoring not arranged (`f2_monitoring_not_arranged`). That target is selected first. Injection does not change the warfarin order. It removes the monitoring arrangement only.

After injection, the resident-visible case still lists warfarin at discharge. The required outpatient monitoring row is absent. The fact that warfarin is being continued remains visible.

The hidden investigator answer key records the trigger medication, the required monitoring (INR), the field removed (`CaseMonitoring` / `CaseMedication.monitoring`), and the expected action, which is to arrange outpatient INR monitoring. This is not a home-versus-discharge medication mismatch.

### Example C — Clean control (demonstration)

The clinical knowledge in this sketch is that ibuprofen is a stored RxNorm concept and that the scenario lists it as a stop medication. The synthetic patient-specific information is that the home list includes ibuprofen, that it is held on admission with an explicit instruction not to restart at discharge, and that continued heart-failure therapy remains on the discharge list. That home-versus-discharge difference is documented and intended.

No assessment error is injected. The family is `none`, the category is `none`, and `clean_case` is true.

A difference between home and discharge does not automatically mean an error. Residents still review the case; investigators score it as a control. The hidden key states `NO INTENTIONAL ERROR`.

### Machine validation versus clinician review

The software performs automated checks of schema and structure, terminology and reference integrity, deterministic rule constraints, category eligibility, the expected state transition, answer-key consistency, implemented error-isolation checks, and resident-export leak checks. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians.

It does **not** establish overall clinical realism, guideline completeness, optimal therapy, educational appropriateness, clinical validity, or calibrated learner difficulty. Those remain part of clinician/resident validation. Code alone does not prove clinical validity.

---

## Worked Example 1 — Heart Failure

Educational demonstration **`SYN-000901`**. The snapshot is [`data/docs/clinician_examples/syn-000901.json`](data/docs/clinician_examples/syn-000901.json). The case seed is `20260926:901:HF_INPATIENT`. This is not a `VAL-*` study case.

### Patient presentation

The patient is an 83-year-old man weighing 69 kg. The display name is `SYN Patient 901`, which is synthetic. Ethnicity is not recorded (`null`).

The reason for admission is unspecified systolic (congestive) heart failure, ICD-10-CM **I50.20**, on a cardiology service, with planned disposition home.

The presenting symptoms are dyspnea, anasarca, and orthopnea. Duration “several days,” severity “moderate,” and course “worsening” are template constants.

Admission vital signs are temperature 36.8 °C (fixed in code), blood pressure 124/70, heart rate 108, respiratory rate 23, and SpO2 98%. No vital-sign terminology row is linked (`ref_vital_id` is null).

The following table lists the laboratory concepts retrieved from LOINC and the synthetic numeric results written onto this demonstration case. The concept identity is source-backed. The number is not a real-patient measurement.

| Test (LOINC long name) | Result | Unit on case | LOINC | Concept source | Result source |
| --- | ---: | --- | --- | --- | --- |
| Creatinine [Moles/volume] in Serum or Plasma | 1.6 | umol/L | 14682-9 | LOINC 2.83 | Synthetic |
| Potassium [Moles/volume] in Serum or Plasma | 3.6 | mmol/L | 2823-3 | LOINC 2.83 | Synthetic |
| Natriuretic peptide B [Mass/volume] in Serum or Plasma | 648 | pg/mL | 30934-4 | LOINC 2.83 | Synthetic |
| INR in Platelet poor plasma or blood by Coagulation assay | 2.6 | {INR} | 38875-1 | LOINC 2.83 | Synthetic |

Home medications are furosemide solution, spironolactone suspension, metoprolol 37.5 mg, lisinopril solution, atorvastatin 80 mg, and warfarin 1 mg, all once daily, with ibuprofen topical gel held.

Inpatient medications are the same continue set as active, with ibuprofen still held.

Discharge medications on this clean case are the same six continue medications, once daily. Ibuprofen is not listed.

### Step 1 — Clinical scenario

Family `HF_INPATIENT` in [`data/bootstrap/scenarios.json`](data/bootstrap/scenarios.json) is a cardiology inpatient skeleton for ages 55 through 85. The diagnosis query is heart failure. The symptom queries are dyspnea, edema, and orthopnea. The continue-medication queries are lisinopril, furosemide, metoprolol, spironolactone, and atorvastatin. The stop-medication query is ibuprofen. The hospital-only query is pantoprazole, which is constructed only when the target is hospital-only medication continued after discharge (`f2_hospital_only_continued`). The anticoagulant mutex chooses exactly one of warfarin or apixaban. The laboratory queries are potassium, creatinine, INR, and natriuretic peptide. If injection is turned on, the allowed error categories are the standardized `f1_*` and `f2_*` identifiers in `scenarios.json`. Required companion medication omitted (`f2_coprescription_omitted`) is not listed because the software does not yet have a sufficiently source-backed deterministic rule for that situation (`not_yet_implementable`).

This demonstration used `--no-inject-error`, so the discharge list matches the clean plan.

### Step 2 — Diagnosis terminology

The human-readable query **heart failure** is sent to NLM ICD-10-CM search at bootstrap (`app/sources/icd10cm.py`). The matching local `ref_diagnoses` row is ICD-10-CM **I50.20**, preferred name “Unspecified systolic (congestive) heart failure,” with `source_system` ICD10CM. That row is copied onto the case as the admission diagnosis.

A SNOMED CT identifier is not stored (`snomed_code` is null). This repository has no SNOMED ingestion client.

### Step 3 — Medication terminology

RxNorm resolution happens at bootstrap, before this patient is built. Generation only matches local rows.

The following table lists the medications stored on `SYN-000901`, the official source of each concept, the RxNorm identifier, and the intended reconciliation role.
| --- | --- | --- | --- |
| lisinopril 1 MG/ML Oral Solution | RxNorm | RXCUI `1806884` | Continue (home, inpatient, discharge) |
| furosemide 4 MG/ML Oral Solution | RxNorm | RXCUI `104220` | Continue |
| metoprolol tartrate 37.5 MG Oral Tablet | RxNorm | RXCUI `1606347` | Continue |
| spironolactone 1 MG/ML Oral Suspension | RxNorm | RXCUI `104230` | Continue |
| atorvastatin 80 MG Oral Tablet | RxNorm | RXCUI `259255` | Continue |
| warfarin sodium 1 MG Oral Tablet | RxNorm | RXCUI `855288` | Continue (mutex pick on this seed) |
| ibuprofen 0.05 MG/MG Topical Gel | RxNorm | RXCUI `141997` | Held stop medication; absent from clean discharge |

Apixaban RXCUI `1364435` exists in the local reference table and is the other mutex option; it was **not** selected for 901.

Dose strings `37.5 MG`, `80 MG`, `1 MG`, and `1 MG/ML` are RxNorm `strength` values. Furosemide, spironolactone, and ibuprofen have empty strength in the stored row, so the generator wrote the synthetic fallback **`1 tablet`**.

### Step 4 — Symptoms and clinical context

The following table shows how each scenario symptom query resolved, and which parts of the symptom line are synthetic constants rather than retrieved names.

| Scenario query | Stored name | Terminology source | What is synthetic |
| --- | --- | --- | --- |
| dyspnea | Dyspnea | NLM conditions | duration / severity / course constants |
| edema | **Anasarca** | NLM conditions (token match; synonym includes “massive edema”) | same constants |
| orthopnea | Orthopnea | NLM HPO (`source_system` NLM_HPO). Synonym list includes `HP:0012764`. **`snomed_code` is null** — the HPO id is not treated as SNOMED | same constants |

Chief complaint and HPI are template sentences that concatenate those names with the diagnosis name (`_template_narrative`).

### Step 5 — Vitals and labs

The following table lists the vital signs and laboratory numbers on this demonstration case and whether each value is synthetic.

| Field | Example value | Source/type |
| --- | ---: | --- |
| Temperature | 36.8 °C | Synthetic (fixed in code) |
| Blood pressure | 124/70 | Synthetic (`randint` ranges) |
| Heart rate | 108 | Synthetic |
| Respiratory rate | 23 | Synthetic |
| SpO2 | 98% | Synthetic |
| Weight | 69 kg | Synthetic |
| Creatinine | 1.6 umol/L | **Synthetic value**; LOINC concept `14682-9` is source-backed |
| Potassium | 3.6 mmol/L | Synthetic value; LOINC `2823-3` source-backed |
| BNP | 648 pg/mL | Synthetic value; LOINC `30934-4` source-backed |
| INR | 2.6 | Synthetic value; LOINC `38875-1` source-backed |

The **test identity** (what was ordered) comes from LOINC. The **patient’s number** does not. These are not real-patient or MIMIC values.

### Step 6 — Clinical rules

Only three templates exist ([`data/bootstrap/rule_templates.json`](data/bootstrap/rule_templates.json)). All three were enabled in the local rule table when this case was built (DailyMed / RxClass evidence attached in `app/services/rules.py`).

**`NO_DUAL_ORAL_ANTICOAGULANT`** (hard, DailyMed set id `a454cd24-0c6d-46e8-b1e4-197388606175`)

> IF warfarin RXCUI `855288` **and** apixaban RXCUI `1364435` are both on the case snapshot THEN prohibit co-administration.

The clinical meaning is that the engine will not emit a chart that lists both oral anticoagulants. It is not a complete anticoagulation guideline. It does not compute CHA₂DS₂-VASc, a bleeding score, or a procedure hold.

**`WARFARIN_INR_MONITORING`** (hard, DailyMed set id `724b0061-f42a-4008-a078-09c800ee9785`, LOINC `38875-1`)

> IF warfarin RXCUI `855288` is on the case AND INR LOINC `38875-1` is missing THEN fail.

The clinical meaning is that a warfarin case must include that INR term. The engine does not check whether 2.6 is a suitable INR target or whether the patient has a valid indication for warfarin.

**`FUROSEMIDE_HF_INDICATION`** (soft, RxClass class name `Edema`)

> IF furosemide RXCUI `104220` is on the case AND ICD-10-CM `I50.20` is missing THEN warn (soft; does not fail the case).

The clinical meaning is a weak pairing check between furosemide and the stored heart-failure code, enabled from an RxClass “Edema” hit, not from a full labeling review. It does not require an ACE inhibitor, beta blocker, mineralocorticoid-receptor antagonist, or guideline-directed doses. Soft hits are warnings in the clinical validation layer; this example had no warning because I50.20 is present.

No other clinical guidelines are encoded (no NSAID–HF hard stop, no antibiotic duration, no renal dosing). Ibuprofen is held because the **scenario lists it as a stop medication**, not because an NSAID rule fired.

### Step 7 — Clean medication timeline

The following table is the investigator view of the intended reconciliation on the clean case, before any experimental discrepancy.

| Medication | Home | Inpatient | Discharge |
| --- | --- | --- | --- |
| furosemide 4 MG/ML Oral Solution | continue, `1 tablet` daily | active, same | listed, same |
| spironolactone 1 MG/ML Oral Suspension | continue, `1 tablet` daily | active, same | listed, same |
| metoprolol tartrate 37.5 MG Oral Tablet | continue, 37.5 MG daily | active, same | listed, same |
| lisinopril 1 MG/ML Oral Solution | continue, 1 MG/ML daily | active, same | listed, same |
| atorvastatin 80 MG Oral Tablet | continue, 80 MG daily | active, same | listed, same |
| warfarin sodium 1 MG Oral Tablet | continue, 1 MG daily | active, same | listed, same |
| ibuprofen 0.05 MG/MG Topical Gel | held | held | **not listed** |

The clinically relevant question on review is whether those transitions are intentional and supported — not whether “warfarin” is a real RxNorm concept.

### Step 8 — Machine validation

**Machine-checkable on this example (all passed):**

- Case id format `SYN-000901`; medication contexts `home` / `inpatient` / `discharge`; at least one diagnosis (**structural**)
- Every med/diagnosis/lab links to a `ref_*` row with provenance; units are stored UCUM or LOINC example units (**terminology**)
- No hard rule violations (**clinical**)
- Discharge list matches the continue/stop plan; required companion actions (for example warfarin INR monitoring) are present; no answer key (**assessment**, clean mode)

**Requires clinician review (not checked):**

- Overall plausibility of an 83-year-old with HR 108, BP 124/70, SpO2 98%, creatinine 1.6 **umol/L**
- Whether oral-solution ACE inhibitor / loop diuretic and topical ibuprofen are acceptable teaching formulations
- Whether warfarin 1 mg daily plus INR 2.6 is a defensible regimen
- Missing allergies, missing additional diagnoses (AF, CKD, etc.), missing imaging
- Whether the one-paragraph template HPI is sufficient context
- Whether difficulty is appropriate for residents

---

## Worked Example 2 — Atrial Fibrillation

Educational demonstration **`SYN-000902`**. The snapshot is [`data/docs/clinician_examples/syn-000902.json`](data/docs/clinician_examples/syn-000902.json). The case seed is `20260926:902:AF_ANTICOAGULATION`. This is not a `VAL-*` study case. It is a clean case (`--no-inject-error`).

### Patient presentation

The patient is a 75-year-old woman weighing 109 kg.

The reason for admission is paroxysmal atrial fibrillation, ICD-10-CM **I48.0**, on a cardiology service.

The presenting symptoms are dyspnea and **Chronic fatigue syndrome**. The second name is the NLM conditions token match for the scenario query `fatigue`. It is not a claim that the patient meets diagnostic criteria for chronic fatigue syndrome.

Admission vital signs are 36.8 °C, blood pressure 125/77, heart rate 79, respiratory rate 16, and SpO2 96%.

The laboratory results are creatinine 0.9 umol/L (LOINC 14682-9) and INR 3.2 (LOINC 38875-1). There is no potassium or BNP because those queries are not in the atrial-fibrillation scenario.

Home, inpatient, and discharge continue medications are metoprolol tartrate 37.5 mg daily (RXCUI `1606347`), atorvastatin 80 mg daily (`259255`), and warfarin 1 mg daily (`855288`). Ibuprofen topical gel (`141997`) is held and is not on the discharge list.

This family is thinner than HF: rate-control + statin + **exactly one** oral anticoagulant, plus a held NSAID. The mutex again chose warfarin on this seed (apixaban is the other official option). Hard rules still forbid listing warfarin and apixaban together and still require INR when warfarin is present.

What is different from Example 1, clinically:

- Admission diagnosis is AF, not HF; furosemide/MRA/ACE inhibitor are **not** in this scenario’s medication list
- Symptom set is dyspnea + fatigue-query result, not orthopnea/anasarca
- Reconciliation still uses three contexts. The teaching point is: metoprolol and warfarin continue across home, hospital, and discharge at the **same** dose and frequency on the clean case. A later dose or frequency injection would change **only discharge**, which is the difference residents are meant to notice
- Template HPI still states that ibuprofen was held and is not intended for discharge continuation

SNOMED remains unset on I48.0.

---

## Worked Example 3 — Pulmonology (community pneumonia family)

Educational demonstration **`SYN-000903`**. The snapshot is [`data/docs/clinician_examples/syn-000903.json`](data/docs/clinician_examples/syn-000903.json). The case seed is `20260926:903:CAP_INPATIENT`. Specialty is **pulmonology**. This is a clean case and is not a `VAL-*` study case.

### Patient presentation

The patient is a 58-year-old woman weighing 103 kg.

The reason for admission is lobar pneumonia, unspecified organism, ICD-10-CM **J18.1**.

The presenting symptoms are cough, dyspnea, and wheezing, all from NLM conditions, with `snomed_code` null.

Admission vital signs are 36.8 °C, blood pressure 130/80, heart rate 73, respiratory rate 21, and SpO2 92%.

The laboratory results are creatinine 1.3 umol/L (14682-9), sodium 139 mmol/L (2951-2), and hemoglobin 13.9 g/dL on LOINC **55782-7**, “Hemoglobin [Mass/volume] in Blood **by Oximetry**.” That method is what LOINC ranking stored; it is not a methodless CBC hemoglobin.

The following table lists the continue medications on home, inpatient, and discharge lists for this pneumonia demonstration.

| Drug as stored | RXCUI | Dose on case | Note |
| --- | --- | --- | --- |
| albuterol 0.4 MG Inhalation Powder | 104514 | `1 tablet` once daily | RxNorm strength empty → synthetic `1 tablet`; `route` stored as `oral` (default when the reference row has no route) |
| azithromycin 250 MG Oral Capsule | 141962 | `1 tablet` once daily | strength empty → `1 tablet` |
| pantoprazole 20 MG Delayed Release Oral Tablet | 251872 | 20 MG once daily | strength copied from RxNorm |

This pneumonia family has no stop medication and no anticoagulant mutex ([`data/bootstrap/scenarios.json`](data/bootstrap/scenarios.json)). Allowed error categories therefore omit medication inappropriately added or continued (`f1_commission`), because there is no held drug to copy onto discharge, and required outpatient monitoring not arranged (`f2_monitoring_not_arranged`), because there is no warfarin and INR monitoring trigger. Canonical identifiers still include medication omitted at discharge (`f1_omission`), unexplained dose discrepancy (`f1_dose_mismatch`), unexplained frequency discrepancy (`f1_frequency_mismatch`), unexplained therapeutic substitution (`f1_therapeutic_substitution`), and several Family 2 gaps.

None of the three implemented rules is about pneumonia or macrolides. Dual-anticoagulant and warfarin/INR rules are idle here (those RXCUIs are absent). Furosemide/HF is idle (no furosemide).

This family shows that disease-specific scenarios differ by diagnosis query, specialty label, symptom set, lab panel, and whether a held NSAID exists — not by a second copy of the HF template with the title changed.

---

## Medication Reconciliation Explained Clinically

Each continue medication is stored in three **contexts** (`CaseMedication.context` in `app/models/cases.py`):

- **HOME** — what the patient was taking before admission (`status: home`)
- **INPATIENT** — what is marked active in hospital (`status: active`)
- **DISCHARGE** — what is written on the discharge list (`status: discharge`)

Held drugs use home and inpatient with `status: held` and a held reason, and they are omitted from the **clean** discharge list.

The validator compares those lists to `CaseMedicationPlan` (`continue` vs `stop`, and dose/frequency equality between home and discharge for continue drugs). It is not scoring “is Drug A a valid RxNorm concept?” — that already passed terminology checks.

A schematic of the *kind* of discrepancy residents are asked to notice (not a study answer):

```text
Home:      Drug A  5 mg  once daily
Hospital:  Drug A  5 mg  once daily
Discharge: Drug A 10 mg  once daily   ← dose transition
```

The clinically relevant question is: **was the change from 5 mg to 10 mg intentional and supported by the rest of the case?** The engine’s dose-mismatch injector performs a mechanical first-digit change (`_altered_dose`); it does not consult renal function, INR, or blood pressure to justify a new dose.

Frequency mismatch flips `once daily` ↔ `twice daily` on discharge only. Omission deletes a continue drug from discharge only (it remains on home and inpatient). Incorrect continuation copies a held stop drug onto discharge (CliniProof **commission**, `f1_commission` — not Family 2 “held medication, no restart plan”).

Family 2 injectors generally do **not** change the intended discharge identity of a continued drug. They remove a required companion action while leaving the trigger medication visible (for example, warfarin continued without outpatient INR monitoring). See [CliniProof error taxonomy](#cliniproof-error-taxonomy).

---

## Clean Cases Versus Error-Injected Cases

The following terms are used in this codebase (`clinical_cases.clean_case`, `validation_batch_cases.is_clean_control`, and freeze plan `inject_error`).

### Clean case

A clean case is the structured patient after concept selection, synthetic values, and narrative, and before any experimental mutation. Machine validation in this state requires zero mechanically detectable findings and no answer key.

Demonstration `SYN-000901`, `SYN-000902`, and `SYN-000903` were left in this state (`--no-inject-error`).

### Error-injected case

After a clean pass, `inject_reconciliation_error` plants one controlled assessment error. For Family 1 that error is a discharge-list change. For Family 2 it is a missing companion action such as monitoring, a restart plan, supply, or follow-up. The injector writes `CaseAnswerKey`, sets `clean_case = false` and `case_status = error_injected`. Revalidation expects that single specified category. Family 2 may pass without a discharge-list mutation.

### Control case (study freeze)

A freeze-plan assignment with `inject_error: false` remains a clean case and is stored as `is_clean_control = true`. Residents are not told which `VAL-*` identifiers are controls. This README therefore does not list the study control identifiers in a resident-facing way; investigators should use [`data/validation/README.md`](data/validation/README.md), which is investigator-only.

Ad-hoc `generate-synthetic-cases` defaults to injecting an error unless `--no-inject-error` is passed. Freeze follows the JSON plan.

---

## Investigator-only generation example

> **WARNING — INVESTIGATOR ONLY**
>
> This subsection shows how a planted medication-reconciliation error is created. **Do not distribute it to resident study participants.** It uses educational case `SYN-000904`, which is **not** in the `VAL-*` blinded set. The method is the same one used on error-bearing study cases; naming the method here must not be attached to a specific `VAL` identifier in resident packets.

The snapshot is [`data/docs/clinician_examples/syn-000904.json`](data/docs/clinician_examples/syn-000904.json). The case seed is `20260926:904:HF_INPATIENT`. The scenario is heart-failure inpatient (`HF_INPATIENT`). The anticoagulant mutex on this seed chose **apixaban** 2.5 mg (RXCUI `1364435`), not warfarin. Heart-failure laboratories still include INR because that query is on the scenario laboratory list, but no warfarin monitoring row was added.

### Before error injection

The continue set is the same as other heart-failure cases, with apixaban instead of warfarin. Ibuprofen is held. Clean discharge would list furosemide, spironolactone, apixaban, metoprolol, lisinopril, and atorvastatin.

### Error injection operation

The preferred category is medication omitted at discharge (`f1_omission`), which is a Family 1 list-transition discrepancy (`family_1`). `inject_reconciliation_error` in `app/services/error_injection.py` does not ask a language model which error to plant. It collects continue-plan medications that have a discharge row, sorts them by RXCUI, chooses one with the case random-number generator, deletes the discharge row for that medication, marks the plan `is_error_target = true` (here: `PLAN-SYN000904-003`, apixaban), and writes `CaseAnswerKey` with Family 1, `f1_omission`, and detectability on the discharge medication list.

Home and inpatient apixaban rows are left unchanged.

### After error injection

The following table shows home, inpatient, and discharge status after the omission was injected. Apixaban remains on the home and inpatient lists and is missing at discharge.

| Medication | Home | Inpatient | Discharge after injection |
| --- | --- | --- | --- |
| furosemide 4 MG/ML Oral Solution | continue | active | listed |
| spironolactone 1 MG/ML Oral Suspension | continue | active | listed |
| **apixaban 2.5 MG Oral Tablet** | **continue 2.5 mg daily** | **active 2.5 mg daily** | **omitted** |
| metoprolol tartrate 37.5 MG Oral Tablet | continue | active | listed |
| lisinopril 1 MG/ML Oral Solution | continue | active | listed |
| atorvastatin 80 MG Oral Tablet | continue | active | listed |
| ibuprofen topical gel | held | held | not listed |

### Hidden answer key (what the software stores)

The following fields are stored for `SYN-000904` by `_write_answer_key` using definitions in `app/models/cases.py`. The clinical category is medication omitted at discharge (`f1_omission`). The family is Family 1 (`family_1`). The trigger medication is apixaban 2.5 MG Oral Tablet, RXCUI `1364435`. The rationale is that the correct discharge medication list includes this continued home medication and that it was intentionally omitted from the discharge list. The expected action is to restore the omitted continued discharge medication from the medication plan. The intentional change records clean state present, injected state absent, context discharge, and seed `20260926:904:HF_INPATIENT`. Severity (`severity_ncc_merp`) and a priori difficulty (`difficulty_a_priori`) are null because software does not score them.

Study investigator exports add control/error status, SYN id, seed, rule snapshots, and source versions (`app/services/validation_batch.py` `_investigator_payload`). Those files for `VAL-*` cases live next to the study JSON and **must stay off the resident packet**.

The implemented CliniProof injector set is in [CliniProof error taxonomy](#cliniproof-error-taxonomy). This educational snapshot uses the standardized family and category identifiers. Required companion medication omitted (`f2_coprescription_omitted`) remains `not_yet_implementable` until a source-backed companion-prescription rule exists.

---

## What the Resident Actually Sees

Study residents receive the blinded JSON and review worksheet for the **chosen active set**: [`data/validation_balanced_v3/resident_validation_cases.json`](data/validation_balanced_v3/resident_validation_cases.json) (`CLINIPROOF_BALANCED_V3`) or [`data/validation_seedcases_v2/resident_validation_cases.json`](data/validation_seedcases_v2/resident_validation_cases.json) (`CLINIPROOF_SEEDCASES_V2`). They do **not** receive the investigator key, freeze plan, manifest, coverage files, or batch README catalogs. Do not send archived [`data/validation/resident_validation_cases.json`](data/validation/resident_validation_cases.json) (`CLINIPROOF_TAXONOMY_V1`) as the current study packet.

The audited resident export contains no `CaseAnswerKey`, no `SYN-*` identifiers, no `TEST_*` identifiers, no `LEAK_MARKERS`, no planted-error category, no error-family field, no target-medication metadata, no `clean_expected_state`, no `injected_state`, and no correct-action answer. The resident worksheet retains empty rating and response fields. Do not pre-populate resident judgments.

Export (`_resident_payload`) rewrites ids to `VAL-*`, sets `case_status` to `review`, clears `source_reference` (so RXCUI is not on the resident med rows), omits `CaseAnswerKey`, and strips leak markers. Patient display names become `VAL Patient 501` or `VAL Patient 601` on the active sets. Archived V1 used `VAL Patient 201`.

Educational analogue using **clean** demonstration `SYN-000901` (if this were exported as a resident case, RXCUIs would be omitted). Layout:

### Educational case SYN-000901 (shape of a resident case)

The presentation is an 83-year-old man with unspecified systolic (congestive) heart failure. The chief complaint is dyspnea, anasarca, and orthopnea in the setting of that diagnosis. The history of present illness is the short template paragraph listing those symptoms and the home medication names, including that ibuprofen was held.

Admission vital signs are 36.8 °C, 124/70, heart rate 108, respiratory rate 23, and SpO2 98%. Weight is 69 kg.

The laboratory results are creatinine 1.6 umol/L, potassium 3.6 mmol/L, BNP 648 pg/mL, and INR 2.6. LOINC codes are not required on the resident laboratory rows; `source_reference` is null in the study export.

Home medications are furosemide solution, spironolactone suspension, metoprolol 37.5 mg, lisinopril solution, atorvastatin 80 mg, and warfarin 1 mg, all once daily, with ibuprofen gel held.

Hospital medications are the same continue set, marked active, with ibuprofen held.

Discharge medications are the same six continue medications. This educational case was not error-injected. Study cases may differ on discharge; residents are not told which.

Follow-up is primary care in 7 days. The instruction is to take discharge medications exactly as listed. When warfarin is continued, a clean case also includes outpatient INR monitoring. Family 2 study cases may omit a companion action such as that monitoring row or a follow-up; residents are not told which.

The worksheet asks residents to record the following fields, defined in [`data/validation_balanced_v3/resident_review_schema.json`](data/validation_balanced_v3/resident_review_schema.json) (the seed-guided set has the same schema under [`data/validation_seedcases_v2/resident_review_schema.json`](data/validation_seedcases_v2/resident_review_schema.json)):

- Clinical realism rating (`clinical_realism_rating`), on a 1 through 5 scale
- Medication-reconciliation correctness rating (`medication_reconciliation_correctness_rating`), on a 1 through 5 scale
- Case clarity rating (`case_clarity_rating`), on a 1 through 5 scale
- Identified error type (`identified_error_type`)
- Identified affected medication (`identified_affected_medication`)
- Confidence rating (`confidence_rating`), on a 1 through 5 scale
- Free-text comments (`free_text_comments`)
- Overall acceptability (`overall_acceptability`)
- Revision recommendation (`revision_recommendation`)

The software does not pre-fill those answers and does not tell the resident whether a discrepancy was planted.

---

## What the Investigator Sees

In addition to the resident JSON, freeze export writes the following investigator files **in that batch’s directory**. Active sets live in [`data/validation_balanced_v3/`](data/validation_balanced_v3/) and [`data/validation_seedcases_v2/`](data/validation_seedcases_v2/). Archived V1 files remain in [`data/validation/`](data/validation/) for provenance only. The table says what extra information each file contains. Residents should not receive these files.

| Artifact | Extra information |
| --- | --- |
| `investigator_answer_key.json` / `.md` | Internal `SYN-*` id, seed, control vs error-bearing, error category, affected RXCUI, clean expected state, rule/reference snapshots |
| `validation_manifest.json` | Batch code, generator version, per-VAL freeze metadata, official source versions and sync times |
| `batch_plan.json` | Planned VAL id, scenario, inject flag, `error_family`, `error_category`, sequence |
| `coverage_report.md` / `scenario_coverage_matrix.md` | Mix counts and resolved concepts per family |
| `data/validation/README.md` | Investigator catalog of planted errors for the **archived** V1 freeze |

This split exists so residents cannot score from the key. Do not “fix” blinding by pasting RXCUIs or control flags into the resident JSON.

---

## Source Versus Synthetic — One-Page Table

The following table answers which parts of a case are official terminology or rules, and which parts were generated. Examples are from `SYN-000901` unless noted.

| Case element | Source-backed or synthetic? | Example from `SYN-000901` unless noted |
| --- | --- | --- |
| Medication *concept* | Source-backed (RxNorm, after bootstrap) | warfarin sodium 1 MG Oral Tablet |
| Drug identifier | Source-backed | RXCUI `855288` |
| Lab *concept* | Source-backed (LOINC) | Creatinine LOINC `14682-9` |
| Lab *result* | Synthetic | creatinine **1.6** umol/L |
| Vital sign values | Synthetic; no vital LOINC linked | HR 108, BP 124/70 |
| Diagnosis concept | Source-backed where resolved (ICD-10-CM) | I50.20 |
| SNOMED CT | **Not stored** | `snomed_code` null; not invented |
| Symptom name | Source-backed (NLM conditions or HPO) | Anasarca; Orthopnea |
| Clinical rule | Curated template; enabled only with DailyMed or RxClass evidence | `NO_DUAL_ORAL_ANTICOAGULANT` |
| Patient age / sex / name | Synthetic | 83-year-old Male, `SYN Patient 901` |
| Weight | Synthetic | 69 kg |
| Narrative wording | Template here; optional OpenAI rewording on the ad-hoc path; freeze forces template | HPI paragraph |
| Dose when RxNorm strength exists | Copied from stored strength | metoprolol `37.5 MG` |
| Dose when strength is empty | Synthetic fallback | furosemide `1 tablet` |
| Frequency on the clean case | Synthetic constant | `once daily` |
| Medication-reconciliation error | Deterministically injected **after** clean validation, only if enabled | Educational `SYN-000904`: apixaban omitted on discharge |
| MIMIC patient-level data | **Not used** | No raw MIMIC rows, notes, or identifiers appear on these cases |

---

## Why Machine Validation Is Not Clinical Validation

Software can confirm, for a given case, only what the code actually checks:

- schema/structure (allowed medication contexts, plan decisions, identifier shapes)
- terminology/reference integrity (stored RxNorm / ICD-10-CM / LOINC / UCUM rows with provenance)
- deterministic rule constraints (the three **implemented** hard rules)
- category eligibility (requested canonical category is implementable and eligible)
- expected deterministic state transition (planned category = injected kind)
- answer-key consistency (investigator category matches the injection)
- implemented error-isolation checks (no unintended second assessment target)
- resident-export leak checks (`LEAK_MARKERS`, no `CaseAnswerKey` on the resident packet)

Software **cannot** establish:

- overall clinical realism (formulations, units, vital-sign clustering, template HPI)
- guideline completeness
- optimal therapy
- educational appropriateness
- clinical validity
- calibrated learner difficulty
- necessary clinical context (allergies, CKD, cultures, imaging, social needs)
- that a medication change would be clinically justified in a real patient
- that practice patterns match a given hospital

Passing `validate-cases` or a freeze audit means the record is a **machine-validated synthetic resident-review case pending clinician validation**. It is not a clinically validated teaching case until reviewers say so.

---

## Generation Lineage for One Case

The following sequence is the exact path for educational `SYN-000901`. Study freeze uses the same function and then assigns a VAL identifier.

1. A scenario definition is read from `data/bootstrap/scenarios.json`; for this example the family is `HF_INPATIENT`.
2. Human-readable search requests come from `manifest.json` and the scenario queries.
3. Official terminology is resolved at bootstrap from RxNav, ICD-10-CM, LOINC, and related sources.
4. Matching local reference rows are stored in `ref_medications`, `ref_diagnoses`, `ref_lab_tests`, and `ref_symptoms`.
5. Per-case concept selection matches those rows and, when needed, applies the anticoagulant mutex using the seeded random-number generator.
6. Hard clinical-rule checks run on the selected codes (`_assert_rules_allow`).
7. Synthetic demographics, vital signs, laboratory numbers, and weight are drawn with the seeded generator.
8. Template narrative, or optional OpenAI rewording, is written from already chosen names.
9. Three-context medication lists and a continue-or-stop plan are assembled.
10. The remaining dashboard arrays complete a clean structured case.
11. Machine validation runs on structure, terminology, hard rules, and assessment consistency.
12. An optional controlled CliniProof category may then be applied. It is skipped on 901. Family 1 omission is used on 904. Family 2 may leave the medication list unchanged.
13. Revalidation runs and a `CaseGenerationRun` is stored.
14. On the study path only, a freeze audit writes an immutable VAL identifier and a blinded resident export.
15. Clinician and resident review use the worksheet. That review is not performed by software.

---

The following table maps each clinical or operational claim in this walkthrough to the repository file that implements or stores it.

| Claim | Where to look |
| --- | --- |
| Scenario families and queries | `data/bootstrap/scenarios.json` |
| Bootstrap search requests | `data/bootstrap/manifest.json` |
| Rule templates and evidence needles | `data/bootstrap/rule_templates.json`, `app/services/rules.py` |
| Concept matching and LOINC ranking | `app/services/bootstrap.py` |
| Case assembly, RNG, doses, labs, mutex | `app/services/generation.py` |
| Four-layer validation (`structural`, `terminology`, `clinical`, `assessment`) | `app/services/validation.py` |
| CliniProof taxonomy, eligibility, isolation | `app/services/error_taxonomy.py` |
| Error injectors and answer key | `app/services/error_injection.py` |
| Freeze, export, leak audit | `app/services/validation_batch.py` |
| Optional narrative LLM | `app/openai/narrative.py` |
| Active resident JSON (balanced) | `data/validation_balanced_v3/resident_validation_cases.json` (`CLINIPROOF_BALANCED_V3`) |
| Active resident JSON (seed) | `data/validation_seedcases_v2/resident_validation_cases.json` (`CLINIPROOF_SEEDCASES_V2`) |
| Archived resident JSON | `data/validation/resident_validation_cases.json` (`CLINIPROOF_TAXONOMY_V1`, historical) |
| Active investigator keys | `data/validation_balanced_v3/investigator_answer_key.json` and `data/validation_seedcases_v2/investigator_answer_key.json` (investigator-only) |
| Active readable clinician packets | `data/validation_balanced_v3/readable/` and `data/validation_seedcases_v2/readable/` |
| Archived investigator key | `data/validation/investigator_answer_key.json` (historical; not the current study key) |
| Archived readable packets | `data/validation/readable/` |
| These worked examples | `data/docs/clinician_examples/` |

---

## 2. Quick start

Shortest path if Git, Python 3.12+, Docker, and (for labs) a Regenstrief LOINC account are already available.

**macOS/Linux**

```bash
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
# Edit .env: set LOINC_USERNAME and LOINC_PASSWORD for lab import.
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator validate-cases --case-id SYN-000001
```

**Windows PowerShell**

```powershell
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
# Edit .env: set LOINC_USERNAME and LOINC_PASSWORD for lab import.
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator validate-cases --case-id SYN-000001
```

To **use the committed resident-review files** without regenerating: give reviewers the active JSON under `data/validation_balanced_v3/` or `data/validation_seedcases_v2/` and the matching empty worksheet. Do not send investigator keys. Details: [How to give cases to residents](#18-how-to-give-cases-to-residents).

To **rebuild an active frozen batch in a local database** (after bootstrap), pass an explicit plan and batch code:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
```

`freeze-validation-batch` generates, validates, and freezes internally. A prior `validate-cases` run is not a prerequisite. See [Resident-validation workflow](#16-resident-validation-workflow).

---

## 3. Architecture and repository layout

```text
Official terminology sources
        ↓
Local reference tables (ref_*)
        ↓
Scenario specification
        ↓
Deterministic structured clean case
        ↓
Source-backed clinical rules
        ↓
Clean machine validation
        ↓
Category eligibility
        ↓
Deterministic error injection (exactly one pre-specified canonical category; skipped for controls)
        ↓
Category-aware post-injection validation
        ↓
Immutable VAL assignment
        ↓
Blinded resident export
        ↓
Investigator answer key
        ↓
Clinician review
```

This matches `app/cli/__init__.py` and `app/services/validation_batch.py`. There is no AccessGUDID, SNOMED, or MIMIC stage in the running pipeline.

| Path | Role |
| --- | --- |
| `app/models` | SQLAlchemy 2 tables (`reference.py`, `cases.py`, `generation.py`). Schema map: [§25](#25-database-tables-and-uml) |
| `app/schemas` | Pydantic v2 models matching those tables |
| `app/repositories` | Lookups, upserts by official identifiers, `data_source_registry` seed |
| `app/sources` | HTTP clients: RxNav, LOINC FHIR, UCUM essence XML, NLM ICD-10-CM, NLM conditions, NLM HPO, DailyMed, RxClass |
| `app/services` | Sync, bootstrap, local search, rules, generation, validation, CliniProof taxonomy/injection, freeze/export |
| `app/cli` | Typer CLI (`clinical-case-generator`) |
| `app/api` | `GET /reference/medications`, `/labs`, `/diagnoses`, `/symptoms` |
| `app/main.py` | FastAPI app plus `GET /health` |
| `app/openai` | Optional narrative wording after canonical concepts are selected |
| `app/config.py` | Settings from `.env` |
| `app/database.py` | Engine, sessions, `ProvenanceMixin`, `CaseChildMixin` |
| `data/bootstrap` | `manifest.json`, `rule_templates.json`, `scenarios.json` |
| `data/validation` | Archived `CLINIPROOF_TAXONOMY_V1` freeze ([catalog](data/validation/README.md)) |
| `data/validation/readable` | Archived Markdown packets for VAL-201–VAL-224 |
| `data/validation_balanced` | Preclinical-QC archive `CLINIPROOF_BALANCED_V2` (VAL-301–VAL-324) |
| `data/validation_balanced_v3` | Active `CLINIPROOF_BALANCED_V3` (VAL-501–VAL-524) |
| `data/validation_balanced/readable` | Preclinical-QC balanced clinician packets |
| `data/validation_balanced_v3/readable` | Active balanced clinician packets |
| `data/seed_cases` | Resident-authored DOCX design references and derived archetypes |
| `data/seed_cases/resident_authored` | Immutable source DOCX files (not study cases) |
| `data/seed_cases/blueprints` | Machine-readable seed archetypes (`archetypes.json`) |
| `data/validation_seedcases` | Preclinical-QC archive `CLINIPROOF_SEEDCASES_V1` (VAL-401–VAL-424) |
| `data/validation_seedcases_v2` | Active `CLINIPROOF_SEEDCASES_V2` (VAL-601–VAL-624) |
| `data/validation_seedcases/readable` | Preclinical-QC seed-guided clinician packets |
| `data/validation_seedcases_v2/readable` | Active seed-guided clinician packets |
| `data/validation_registry.json` | Active versus archived batch registry |
| `data/active_validation_sets.md` | Reviewer navigation for the two active sets |
| `data/validation_comparison` | Investigator comparison of the two active sets |
| `data/exports` | Gitignored local export directory (placeholder `.gitkeep` only) |
| `data/imports`, `data/aggregates`, `data/mimic` | Gitignored placeholders; this pipeline does not read them |
| `alembic/versions` | Migrations |
| `tests` | pytest; HTTP mocked with `httpx.MockTransport` |
| `docker-compose.yml` | Local PostgreSQL 16 |

`CaseGenerationRun.blueprint_id` is the UUID foreign key to `case_blueprints.id`. Optional links to reference rows use `ON DELETE RESTRICT`. Case children use `ON DELETE CASCADE` on `case_id`. Frozen `validation_batch_cases.case_id` uses `ON DELETE RESTRICT`.

Alembic:

- `1c236aeaadc7` — Phase 1 clinical schema (do not rewrite)
- `7b9e4c21d6a0` — `clinical_rules` (revises `1c236aeaadc7`)
- `c3f8a91b2e47` — `validation_batch_cases` (revises `7b9e4c21d6a0`)
- `d4e8b17c6a91` — CliniProof `error_family` column and `ref_medication_classes` (current head)

---

## 4. Prerequisites

| Requirement | Detail |
| --- | --- |
| Git | To clone the repository |
| Python | **3.12 or newer** (`requires-python = ">=3.12"` in `pyproject.toml`; Ruff/mypy target 3.12) |
| PostgreSQL | **16**, via the provided Compose file (`image: postgres:16`) or an equivalent local server |
| Docker Engine + Compose v2 | For the documented `docker compose` database |
| Regenstrief LOINC account | **Required** to import labs (`sync-loinc` and bootstrap lab rows) |
| OpenAI API key | **Optional**; narrative wording only |
| Network access | Official source hosts listed in [Reference terminology](#9-reference-terminology) |

**Required vs optional credentials**

| Credential | Required? |
| --- | --- |
| PostgreSQL (Compose defaults or `DATABASE_URL`) | Required to run CLI commands that use the database |
| `LOINC_USERNAME` / `LOINC_PASSWORD` | Required for LOINC. Empty values raise `SourceNotConfigured`. Bootstrap **skips** lab requests and continues; `sync-loinc` **exits 2**. Generation that needs labs then fails resolution. |
| `OPENAI_API_KEY` | Optional. Empty → template narrative. |
| `SNOMED_BASE_URL` / `SNOMED_API_TOKEN` | Unused. No SNOMED client. |
| `MIMIC_LOCAL_PATH` | Unused. No MIMIC reader. |

There is no resident-review web UI in this repository.

---

## 5. Clone and initial setup

Repository URL from `git remote`: `https://github.com/piaattufts/clinical-case-generator`.

### 1. Clone

**macOS/Linux** and **Windows PowerShell** (same):

```bash
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
```

### 2. Create and activate a virtual environment

The package is installed **editable** with development extras (`pytest`, `ruff`, `mypy`).

**macOS/Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation (`running scripts is disabled`), for this process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Confirm the CLI is on `PATH` (venv must be active):

```bash
clinical-case-generator --help
```

You should see commands including `db-init`, `sync-rxnorm`, `sync-loinc`, `sync-ucum`, `sync-icd10`, `reference-search`, `bootstrap-reference-data`, `generate-synthetic-cases`, `validate-cases`, `freeze-validation-batch`, and `export-validation-batch`. There is **no** `sync-all` command.

### 3. Create `.env`

**macOS/Linux**

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

`.env` is gitignored. Fill LOINC fields before lab import. Do not commit credentials.

### 4. Update an existing clone

GitHub’s default branch is `main`. `git pull` on `main` only brings in **merged** commits. Open pull requests (README, validation batches, CliniProof taxonomy, and so on) are **not** on `main` until they are merged.

From the repository root, with a clean working tree:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
```

`--ff-only` refuses to create a merge commit if local `main` has diverged. If that happens, inspect `git status` and `git log --oneline main..origin/main` before deciding.

To look at a feature branch without merging it into `main`:

```bash
git fetch origin
git checkout <branch-name>
git pull --ff-only origin <branch-name>
```

After a pull that changed Python packaging or migrations:

```bash
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
clinical-case-generator db-init
```

`db-init` applies Alembic to the current head. It does **not** rewrite committed files under `data/validation/`. Do not regenerate frozen `VAL-*` JSON “to match” a pull.

To confirm what you have:

```bash
git status
git log -1 --oneline
git rev-parse --abbrev-ref HEAD
```

The GitHub homepage README is the README on `main`. A newer README on another branch is visible in that branch or its pull request until merge.

---

## 6. Environment configuration

Settings are defined in `app/config.py` (`pydantic-settings`, `env_file=".env"`, `extra="ignore"`). Missing values fall back to empty strings or the local database URL.

| Variable | Required? | Purpose | Example / default |
| --- | --- | --- | --- |
| `DATABASE_URL` | Yes, for DB-backed commands | SQLAlchemy URL used by the app and Alembic (`alembic/env.py` copies it; `alembic.ini` has an empty `sqlalchemy.url`) | `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `OPENAI_API_KEY` | No | If non-empty, `assemble_narrative` may call OpenAI. If empty, it returns `None` and generation uses a template. | empty in `.env.example` |
| `OPENAI_MODEL` | No | Model name passed to `client.responses.parse(...)` | `gpt-5` |
| `LOINC_USERNAME` | For LOINC | HTTP Basic user for `https://fhir.loinc.org` | empty |
| `LOINC_PASSWORD` | For LOINC | HTTP Basic password | empty |
| `SNOMED_BASE_URL` | Unused | Loaded into settings only. No client reads it. | empty |
| `SNOMED_API_TOKEN` | Unused | Loaded into settings only. No client reads it. | empty |
| `MIMIC_LOCAL_PATH` | Unused | Loaded into settings only. No MIMIC files are read. | empty |

`.env.example` comment on LOINC: empty values raise `SourceNotConfigured`; there is no generated fallback.

Compose database user/password/name (`postgres` / `postgres` / `clinical_cases` on port `5432`) match that default URL. They are local development values, not production secrets.

---

## 7. Start PostgreSQL

`docker-compose.yml` defines one service:

| Item | Value |
| --- | --- |
| Service name | `postgres` |
| Image | `postgres:16` |
| Database | `clinical_cases` |
| User / password | `postgres` / `postgres` |
| Host port | `5432` |
| Volume | named volume `clinical_cases_pg` |
| Healthcheck | `pg_isready -U postgres -d clinical_cases` |

**macOS/Linux** and **Windows PowerShell**:

```bash
docker compose up -d
```

### Confirm it is running

```bash
docker compose ps
docker compose exec postgres pg_isready -U postgres -d clinical_cases
```

`pg_isready` should exit 0 and report that the server is accepting connections.

### Stop (data kept)

```bash
docker compose stop
```

### Start again

```bash
docker compose start
```

or `docker compose up -d`.

### Restart

```bash
docker compose restart postgres
```

### Reset the development database (destructive)

This **deletes** the named volume `clinical_cases_pg` (all tables, reference rows, generated cases, and freeze rows in that Docker database).

```bash
docker compose down -v
```

Then `docker compose up -d` and `clinical-case-generator db-init` again. Committed files under `data/validation/` are not deleted by this command.

`docker compose down` **without** `-v` stops containers and keeps the volume.

---

## 8. Initialize the database

```bash
clinical-case-generator db-init
```

What it does (`app/cli/__init__.py`):

1. `alembic upgrade head` using `alembic.ini` (URL from application settings).
2. `seed_data_source_registry(session)` — inserts the nine `data_source_registry` metadata rows if missing (`on_conflict_do_nothing` on `source_code`). Existing rows are unchanged.

It does **not** load RxNorm, LOINC, diagnoses, or other clinical concepts.

Printed message (exact template):

```text
Schema is at Alembic head. DataSourceRegistry metadata rows inserted this call: <n>. No clinical reference rows were loaded.
```

First run typically inserts `9`. Later runs insert `0`.

### Verify

1. The command exits 0 and prints the message above.
2. Optional SQL (Compose credentials):

```bash
docker compose exec postgres psql -U postgres -d clinical_cases -c "SELECT source_code, enabled, sync_status, records_imported FROM data_source_registry ORDER BY source_code;"
```

Expected source codes: `ACCESS_GUDID`, `DAILYMED`, `ICD10CM`, `LOINC`, `MIMIC_IV`, `RXCLASS`, `RXNORM`, `SNOMED_CT`, `UCUM`.

3. Optional Alembic:

```bash
alembic current
```

Head revision is `d4e8b17c6a91`.

---

## 9. Reference terminology

Official base URLs are in `app/sources/http.py` (`SOURCE_BASE_URLS`) and the matching client modules.

| Source | Status | Used for | Official URL / notes |
| --- | --- | --- | --- |
| RxNorm | **Implemented** (public) | Medications (`ref_medications`) | `https://rxnav.nlm.nih.gov/REST` |
| DailyMed | **Implemented** (public) | SPL labels (`ref_drug_labels`); rule evidence | `https://dailymed.nlm.nih.gov/dailymed/services/v2` |
| LOINC | **Implemented, credential-dependent** | Labs (`ref_lab_tests`) | `https://fhir.loinc.org`. Search valueset `http://loinc.org?fhir_vs`. Only official term codes matching `^\d{1,5}-\d$` are stored as labs. Parts (`LP`), answers (`LA`), and groups (`LG`) are excluded. |
| UCUM | **Implemented** (public file) | Units (`ref_units`) | `https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml`. Conversion factors are copied from the file, never invented. Composed units such as `kg` keep a null factor when the essence file does not supply one. |
| ICD-10-CM | **Implemented** (public) | Diagnoses (`ref_diagnoses`) | `https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search` |
| NLM conditions | **Implemented** (public) | Symptom names during bootstrap | `https://clinicaltables.nlm.nih.gov/api/conditions/v3/search` |
| NLM HPO | **Implemented** (public) | Symptom fallback if conditions token-match fails | `https://clinicaltables.nlm.nih.gov/api/hpo/v3/search`. HPO `HP:` ids are source metadata/synonyms, **not** written to `snomed_code`. |
| RxClass | **Implemented** (public) | Rule evidence; source-backed medication-class membership (`ref_medication_classes`) for therapeutic substitution | `https://rxnav.nlm.nih.gov/REST/rxclass`. Classes are copied from RxNav, not inferred from drug names. |
| SNOMED CT | **Registered, not implemented** | Registry row only (`enabled=False`, `sync_status=not_configured`) | No client. `SNOMED_*` env vars are unused. |
| AccessGUDID | **Registered, not implemented** | Registry row only (`enabled=True` in metadata, `never_synced`) | No client, no CLI sync. |
| MIMIC-IV | **Registered, disabled, not implemented** | Registry row only | No reader. `MIMIC_LOCAL_PATH` unused. Raw rows must never be stored as reference concepts and are never sent to OpenAI. |

HTTP helpers use User-Agent `clinical-case-generator/0.1.0 (terminology-sync; no-patient-data)` and retry on 429/502/503/504 (two retries). This is not an OpenAI call and does not transmit patient rows.

---

## 10. Bootstrap reference data

```bash
clinical-case-generator bootstrap-reference-data
```

Optional: `--manifest PATH` (default `data/bootstrap/manifest.json`).

This is a **bounded** import of names listed in the manifest, not a full vocabulary download.

### What `data/bootstrap/manifest.json` contains

Version 2. Keys are lists of **human-readable search strings**, not fabricated codes:

- `medications`, `diagnoses`, `symptoms`, `labs`, `units`

Empty strings are skipped.

Related files (not passed as CLI flags except rules via bootstrap internals):

- `data/bootstrap/scenarios.json` — generation families (used at generate/freeze time)
- `data/bootstrap/rule_templates.json` — curated rules (enabled during bootstrap)

### How names are resolved

`app/services/bootstrap.py`:

1. **Medications** — RxNav name search; combination products (`name / name`, TTY `MIN`, or more than one related ingredient) are not selected unless the request itself is a combination.
2. **Diagnoses** — NLM ICD-10-CM search; stored description is the official text; `snomed_code` stays null.
3. **Symptoms** — NLM conditions token match; if that fails, NLM HPO. `snomed_code` is not filled with `HP:` ids.
4. **Units** — official UCUM essence XML search / compose.
5. **Labs** — LOINC FHIR search with ranking (prefer serum/plasma/blood term codes). Missing LOINC credentials: each lab request is **skipped** with `SourceNotConfigured`, registry marked `not_configured`, and bootstrap **continues**.
6. **Labels** — DailyMed SPL XML for resolved RXCUIs.
7. **Rules** — `enable_rules_from_templates` (see [Clinical rules](#12-clinical-rules)).
8. **Medication classes** — RxClass membership copied into `ref_medication_classes` for therapeutic-substitution eligibility (source-backed; not inferred from drug names).
9. Registry `records_imported` counts are refreshed.

### Provenance

Upserted rows get `source_system`, `source_version` when the source supplied one, and timezone-aware `retrieved_at` (`app/utils/provenance.py`). ICD-10-CM and DailyMed APIs often do not supply a version string; version may be null.

### Unresolved vs skipped

JSON printed by the CLI (`upserted`, `unresolved`, `skipped`, `rules_enabled`):

- `unresolved` — source was queried; no acceptable concept (or similar).
- `skipped` — not attempted; currently used for labs when LOINC is not configured.
- A second run **upserts** and does not duplicate canonical identifiers (unique RXCUI, LOINC, UCUM, ICD-10-CM, rule_code, label set_id).

### Verify

```bash
clinical-case-generator reference-search medications --query lisinopril
clinical-case-generator reference-search labs --query potassium
clinical-case-generator reference-search diagnoses --query "heart failure"
clinical-case-generator reference-search symptoms --query dyspnea
```

Each prints JSON with `kind`, `query`, `total`, `limit`, `offset`, `items` (row UUIDs), and `codes` (RXCUI / LOINC / ICD-10-CM / `snomed_code`, which may be `null` for symptoms).

If labs were skipped, `labs` search `total` stays `0` until LOINC credentials are set and bootstrap (or `sync-loinc`) is run.

---

## 11. Individual terminology sync commands

These call official APIs or the UCUM file and upsert what they return. They are **not** a full import. Limit is 1–100 (default 20). Exit code **2** on `ValueError` or `SourceNotConfigured`.

There is no `sync-dailymed`, `sync-snomed`, `sync-gudid`, or `sync-all` command. DailyMed/RxClass/HPO/conditions run as part of bootstrap.

### `sync-rxnorm`

**Purpose.** Upsert RxNorm concepts by RXCUI from NLM RxNav.

**Syntax.** `--name` and/or `--rxcui` required (at least one non-empty). `--limit` default 20.

**Examples**

```bash
clinical-case-generator sync-rxnorm --name lisinopril
clinical-case-generator sync-rxnorm --rxcui 1806884
```

(`1806884` is the RXCUI stored for lisinopril in the committed `CLINIPROOF_TAXONOMY_V1` freeze, not a code invented by this repo.)

Running with neither selector prints: `Provide a name or RXCUI. Full RxNorm import is not run by default.` and exits 2.

**Expected result.** `RXNORM upserted N row(s): <rxcui>, ...` (or `(none)`).

### `sync-loinc`

**Purpose.** Upsert official LOINC **term** codes from the FHIR Terminology Service. Requires credentials.

**Syntax.** `--query` / `-q` or `--code` required. `--limit` default 20.

**Examples**

```bash
clinical-case-generator sync-loinc --query potassium
clinical-case-generator sync-loinc --code 2823-3
```

**Expected result.** `LOINC upserted N row(s): ...`. Missing credentials: `LOINC is not configured. Missing LOINC_USERNAME, LOINC_PASSWORD. No generated fallback is used.`

### `sync-ucum`

**Purpose.** Import units from official UCUM essence XML. Conversion factors are never invented.

**Syntax.** `--query` / `-q`, `--code`, or `--all` required.

**Examples**

```bash
clinical-case-generator sync-ucum --query gram
clinical-case-generator sync-ucum --all
```

**Expected result.** `UCUM upserted N row(s): ...`. `--all` imports every unit parsed from the essence file (not limited to `--limit`). Search without `--all` applies `--limit`.

### `sync-icd10`

**Purpose.** Store ICD-10-CM codes and the **exact official description**. No model-generated codes.

**Syntax.** `--query` / `-q` or `--code` required.

**Examples**

```bash
clinical-case-generator sync-icd10 --query "heart failure"
clinical-case-generator sync-icd10 --code I50.20
```

**Expected result.** `ICD10CM upserted N row(s): ...`.

### `reference-search`

**Purpose.** Search **locally stored** rows. Does not call terminology APIs or OpenAI.

**Syntax.** Argument `kind` is required: `medications`, `labs`, `diagnoses`, or `symptoms`. `--query` / `-q` default `""`. `--limit` default 20 (1–100). `--offset` default 0.

**Example**

```bash
clinical-case-generator reference-search medications --query lisinopril --limit 20 --offset 0
```

Unknown kind: `kind must be medications, labs, diagnoses, or symptoms.` (exit 2).

**Expected result.** Compact JSON (`separators=(",", ":")`) with `items` (UUIDs) and `codes`.

---

## 12. Clinical rules

**Where they live**

- Templates: `data/bootstrap/rule_templates.json`
- Database: `clinical_rules` (`app/models/reference.py` `ClinicalRule`)
- Enablement: `app/services/rules.py` `enable_rules_from_templates` (called from bootstrap)
- Evaluation: `evaluate_rules` / `hard_violations`

**IF/THEN structure**

Each template has `rule_code`, `rule_type`, `severity` (`hard` or `soft`; other values stored as `soft`), medication/diagnosis/lab **names** (resolved against local `ref_*`), `evidence_needles`, optional `evidence_mode` (`all` default, or `any`), and `constraint.action`:

| Action | Meaning when enabled |
| --- | --- |
| `prohibit_coadministration` | Snapshot must not contain both `input_rxcui` and `related_rxcui` |
| `require_lab` | If the medication RXCUI is present, `input_loinc_code` must be present |
| `allow_with_diagnosis` | If the medication RXCUI is present, `input_icd10cm_code` must be present |

**Provenance vs lookup**

Terminology lookup **alone does not enable** a rule. Enablement requires DailyMed label text and/or RxClass class names matching the needles, plus the resolved identifiers the action needs. Until then the row can be stored with `enabled=false` and `source_system` null.

Current templates (all enabled in the committed freeze after evidence attached):

| Rule | Type | Severity | Evidence in freeze |
| --- | --- | --- | --- |
| `NO_DUAL_ORAL_ANTICOAGULANT` | medication_incompatibility | hard | DailyMed |
| `WARFARIN_INR_MONITORING` | monitoring_dependency | hard | DailyMed INR language **or** “prothrombin” (`evidence_mode: any`) plus LOINC INR |
| `FUROSEMIDE_HF_INDICATION` | medication_diagnosis_allow | soft | RxClass class matching edema/heart-failure needles |

**How generation uses them**

Before persist, generation evaluates **hard** violations on the planned ICD + RXCUI + LOINC snapshot and aborts on a hit. Validation’s `clinical` layer fails the case on hard violations; soft hits are **warnings** and do not fail the layer.

No LLM writes or enables rules.

---

## 13. Generate synthetic cases

```bash
clinical-case-generator generate-synthetic-cases [OPTIONS]
```

Implemented flags (`generate-synthetic-cases --help`):

| Flag | Default | Notes |
| --- | --- | --- |
| `--count` | `3` | Integer 1–100 |
| `--seed` | `42` | Integer; combined with sequence and scenario into the case seed |
| `--start-index` | `1` | Integer ≥ 1; becomes `SYN-{index:06d}` |
| `--scenario` | omitted | Must match a `code` in `data/bootstrap/scenarios.json`. If omitted, the **first** scenario in that file is used (`HF_INPATIENT`). |
| `--inject-error` / `--no-inject-error` | `--inject-error` | Exactly one pre-specified CliniProof error after a clean, validated case |
| `--error-category` | omitted | Canonical ID (`f1_omission`, …). Unknown names fail; never silently replaced. Omitted error-bearing generation uses the scenario default. |

There is **no** `--use-openai` flag. The service default is `use_openai=True`; OpenAI is still skipped when the key is empty. Freeze is the path that forces `use_openai=False`.

Unknown `--scenario` raises `unknown scenario '...'` (exit 2).

### Examples

Three cases, default scenario, with injection:

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

Creates/replaces `SYN-000001`, `SYN-000002`, `SYN-000003` unless those underlying rows are frozen.

Without injection:

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --no-inject-error
```

One atrial-fibrillation family case at sequence 10:

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 42 --start-index 10 --scenario AF_ANTICOAGULATION --no-inject-error
```

Request a specific CliniProof category (fails instead of substituting another category if the case is ineligible):

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 42 --scenario HF_INPATIENT --error-category f2_monitoring_not_arranged
```

Scenario codes in `data/bootstrap/scenarios.json`: `HF_INPATIENT`, `AF_ANTICOAGULATION`, `HTN_INPATIENT`, `T2DM_INPATIENT`, `CAP_INPATIENT`.

### Lifecycle

```text
Load scenario
  → resolve diagnosis, symptoms, meds, stop meds, labs from local ref_*
  → hard-rule check
  → persist clean case (IDs, vitals, labs, plans)
  → optional OpenAI wording of already-selected names (or template)
  → validate clean case (must pass)
  → optional inject exactly one pre-specified CliniProof error; write answer key in Python
  → validate again (expects that category; Family 1 is a plan/discharge mutation, Family 2 may be a missing companion action)
```

Case seed: `f"{seed}:{sequence}:{scenario.code}"` (Python `random.Random`). Example: `42:1:HF_INPATIENT`.

If `SYN-000001` already exists and is **not** frozen, it is deleted and regenerated. If it is frozen as a `VAL-*` assignment, `generate_one_case` raises `FrozenValidationCaseError` (`Frozen validation case VAL-… cannot be overwritten: underlying case SYN-… is frozen`). The `generate-synthetic-cases` CLI does not catch that exception class (the freeze CLI does), so the process exits with a traceback instead of the usual exit code 2.

### Fields that are synthetic / model-generated

- Demographics in the scenario age band; sex `Female`/`Male`; weight; BP/HR/RR/SpO2 ranges; hospital day 2–6
- Laboratory numeric values (`NUMERIC_ORIGIN = "synthetic_model_generated"`)
- Dose = RxNorm `strength` when present, else `"1 tablet"`; clean frequency default `"once daily"`
- Narrative: template, or OpenAI wording of the same facts
- `generation_source` = `clinical-case-generator`; `source_type` on the case = `synthetic`

Not synthetic: RXCUI, LOINC, ICD-10-CM, UCUM codes (must already exist in `ref_*`).

### Expected CLI JSON

A list of objects with `case_id_code`, `seed`, `clean_passed`, `narrative_source` (`template` or `openai`), `error_family`, `error_category`, `error_rxcui`, `validation_passed`. Compact JSON (no extra spaces).

If local labs/meds/diagnoses are missing: `Could not resolve ... from an authoritative source` (exit 2).

---

## 14. OpenAI usage

The only OpenAI module is `app/openai/narrative.py` (`assemble_narrative`). Generation calls it after concept selection. `tests/test_cli_phase2.py` asserts that `app/sources`, `app/services`, `app/api`, and `app/cli` do not import the `openai` package. `from openai import OpenAI` lives inside `assemble_narrative`.

OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. It does not choose diagnoses, medications, terminology codes, error categories, clinical rules, or answer-key content.

When the key is absent, `openai_api_key.strip() == ""` causes an immediate `None` return. Generation uses `_template_narrative` and `narrative_source="template"`.

When the key is present, the client is imported lazily as `OpenAI`. The request uses `client.responses.parse`, `model=settings.openai_model` (default `gpt-5`), and `store=False`. System instructions tell the model to write admission narrative from structured facts only, and not to add diagnoses, medications, labs, units, doses, frequencies, procedures, devices, or identifiers that are not listed, and not to invent reference ranges or unlabeled facts. User content is `str({age, sex, diagnosis, symptoms, medications, chief_complaint_seed})`. The text format is `CaseNarrative` with `chief_complaint`, `hpi`, and `note_text`.

On any exception, including a missing SDK or HTTP failure, the function returns `None` and generation falls back to the template. There is no retry user interface and no raised OpenAI error on the generate CLI path.

After a successful parse, generation rejects the narrative and falls back to the template if none of the allowed names appear in the text (`_narrative_rejected`).

Freeze calls `freeze_validation_batch(..., use_openai=False)`, so OpenAI is not called for the committed freezes even if a key is set.

OpenAI cannot invent or choose diagnoses, RxNorm identifiers, LOINC codes, ICD-10-CM codes, UCUM codes, clinical rules, error categories, error families, or answer-key contents. Raw MIMIC rows are not in the payload. CliniProof structured cases are not wholly generated by a language model.

This documents what the code sends. It is not a broader privacy certification.

---

## 15. Validate generated cases

```bash
clinical-case-generator validate-cases
clinical-case-generator validate-cases --case-id SYN-000001
```

`--case-id` is a `SYN-######` business id (help text: “Validate one SYN-000001 case id.”).

Without `--case-id`, every row in `clinical_cases` is validated, ordered by `case_id_code`. If the table is empty, the command prints `[]` and exits 0.

If `--case-id` is missing in the database: `case validation failed: case SYN-... was not found` (exit 2).

The first failing case raises `CaseValidationError` and stops the rest (exit 2). On success, prints a JSON list of reports:

- `case_id_code`, `passed`, `errors`
- `layers`: `structural`, `terminology`, `clinical`, `assessment` (each with `passed`, `errors`, `warnings`)
- `rules`: enabled-rule hits (`rule_code`, `severity`, `message`)

**What it checks** (`app/services/validation.py`)

| Layer | Passes when |
| --- | --- |
| structural | Case id matches `SYN-######`; medication context/status and plan decisions are in allowed sets; at least one diagnosis |
| terminology | Meds/diagnoses/labs link to `ref_*` with provenance; units are stored UCUM or LOINC example units; invented `fake_` / `invented_` ids rejected (`TEST_` fixtures allowed in tests) |
| clinical | No **hard** rule violations (soft → warnings) |
| assessment | Clean case: no mechanically detectable findings and no answer key. Error-bearing (`clinical_cases.clean_case` is false): exactly one answer key whose category matches the requested CliniProof ID; isolation checks pass (no second mechanically detectable discrepancy). Family 1 is a discharge/plan mutation. Family 2 may pass with an intact discharge list when the missing companion action is the intended finding. A missing `is_error_target` plan is a warning, not a silent category change. |

**What it does not establish:** clinical realism, guideline completeness, or resident-review quality. It does not call external terminology APIs on ordinary reads.

---

## 16. Resident-validation workflow

This is how the **fixed resident-review set** is created. Ad-hoc `generate-synthetic-cases` (sequences 1+) is a separate development path.

### Prerequisites

1. Database initialized ([§8](#8-initialize-the-database)).
2. `bootstrap-reference-data` completed with LOINC credentials so every scenario lab query resolves.
3. Leave `OPENAI_API_KEY` empty if you want template narrative matching the committed freeze. Freeze does not call OpenAI regardless.

`validate-cases` is **not** required before freeze. Freeze generates each assignment, validates the clean case, injects if planned, validates again, then writes `validation_batch_cases`.

Recommended operator order:

```bash
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v2/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2
```

Freeze and export require an explicit plan or batch code. They do **not** default to archived `CLINIPROOF_TAXONOMY_V1`.

Optional inspection of persisted `SYN-*` rows (including freeze sequences 801–824):

```bash
clinical-case-generator validate-cases
clinical-case-generator validate-cases --case-id SYN-000801
```

### `batch_plan.json`

There is no default plan. Pass `--plan` for an active batch:

- [`data/validation_balanced_v3/batch_plan.json`](data/validation_balanced_v3/batch_plan.json) (`CLINIPROOF_BALANCED_V3`, VAL-501–VAL-524, sequences 1201–1224, `balanced_structured`)
- [`data/validation_seedcases_v2/batch_plan.json`](data/validation_seedcases_v2/batch_plan.json) (`CLINIPROOF_SEEDCASES_V2`, VAL-601–VAL-624, sequences 1301–1324, `resident_seed_guided`)

The archived plan [`data/validation/batch_plan.json`](data/validation/batch_plan.json) remains for provenance (`CLINIPROOF_TAXONOMY_V1`, VAL-201–VAL-224, sequences 801–824) and is not used as a CLI default.

Controls:

- `batch_code`
- `master_seed`
- `generation_strategy` (seed-guided plans set `resident_seed_guided`)
- `cases[]`: `validation_case_id` (`VAL-###`), `scenario`, `clinical_profile`, `inject_error`, `error_family`, `error_category`, `sequence`

Case seed for named-profile batches: `{master_seed}:{sequence}:{scenario}:{clinical_profile}`.

### Immutable `VAL-*` IDs

After a successful freeze, `validation_batch_cases.immutable` is true (default). A second freeze **reuses** matching VAL IDs (same seed and scenario) and will not overwrite them. If an existing frozen row disagrees with the plan, the CLI raises:

```text
Frozen validation case VAL-00N cannot be overwritten: existing frozen assignment does not match this plan
```

If any assignment fails generation, eligibility, or audit, freeze **raises** and the transaction is not committed. The injector never substitutes a different error category.

### Archived historical set `CLINIPROOF_TAXONOMY_V1`

Files remain in [`data/validation/`](data/validation/). Do not regenerate them. Freeze and export do not write here unless you pass this plan or batch code explicitly.

### Prospective balanced set `CLINIPROOF_BALANCED_V3`

`CLINIPROOF_TAXONOMY_V1` remains immutable and archived. An **active** balanced structured set is `CLINIPROOF_BALANCED_V3` (VAL-501–VAL-524, sequences 1201–1224) in [`data/validation_balanced_v3/`](data/validation_balanced_v3/). Preclinical-QC `CLINIPROOF_BALANCED_V2` remains in [`data/validation_balanced/`](data/validation_balanced/). Each assignment names a distinct clinical profile so clean-case diversity is specified before error injection. Freeze with:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3 --output-dir data/validation_balanced_v3
```

Do not point those commands at `data/validation/`. The V1 hashes must remain unchanged.

### Active seed-guided set `CLINIPROOF_SEEDCASES_V2`

`CLINIPROOF_TAXONOMY_V1` is archived. `CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2` are the two active prospective sets. `CLINIPROOF_SEEDCASES_V2` (VAL-601–VAL-624, sequences 1301–1324) is generated with `generation_strategy=resident_seed_guided` from abstracted archetypes in [`data/seed_cases/`](data/seed_cases/). Resident-authored DOCX files are immutable design references; they are not copied into study charts. Freeze with:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v2/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2 --output-dir data/validation_seedcases_v2
```

Do not point those commands at `data/validation/` or `data/validation_balanced/`.

### Archived mix summary (`CLINIPROOF_TAXONOMY_V1`)

The archived freeze contains twenty-four cases labeled VAL-201 through VAL-224 (internal sequences 801 through 824). It covered every CliniProof error category that the software could implement at the time. That is not complete coverage of the full conceptual taxonomy. Files remain in [`data/validation/`](data/validation/). Do not run freeze or export without `--plan` / `--batch-code`; those commands no longer default here.

The table below is a compact historical summary.

| Item | `CLINIPROOF_TAXONOMY_V1` |
| --- | --- |
| Public IDs | `VAL-201`–`VAL-224` |
| Internal IDs | `SYN-000801`–`SYN-000824` |
| Mix | 4 clean controls, 20 error-bearing (exactly one pre-specified canonical category each; Family 1 is a list-transition discrepancy, Family 2 may leave the medication list unchanged) |
| Identifiers | Canonical `f1_*` / `f2_*` / `none` in that batch plan (not listed per VAL in this README) |
| Audited coverage | Family 1 **11** (`f1_omission` 3, `f1_commission` 2, `f1_dose_mismatch` 2, `f1_frequency_mismatch` 2, `f1_route_mismatch` 1, `f1_therapeutic_substitution` 1); Family 2 implemented **9** (`f2_monitoring_not_arranged` 2, `f2_held_med_no_restart_plan` 2, `f2_insufficient_supply` 2, `f2_hospital_only_continued` 1, `f2_inpatient_substitution_not_reverted` 1, `f2_pending_decision_followup_missing` 1); `f2_coprescription_omitted` **0** (`not_yet_implementable`) |
| Scenario mix | `HF_INPATIENT` 13/24, `HTN_INPATIENT` 4/24, `AF_ANTICOAGULATION` 3/24, `T2DM_INPATIENT` 3/24, `CAP_INPATIENT` 1/24 — not prevalence-weighted |
| Dataset status | `machine-validated synthetic resident-review cases pending clinician validation` |

Four of the twenty-four cases are clean controls. These cases do not contain an intentionally introduced medication-reconciliation problem and are included so that residents cannot assume that every case necessarily contains an error. Of the twenty cases containing an intended assessment problem, eleven represent Family 1 medication-reconciliation discrepancies, in which the medication regimen itself differs across the transition to discharge. The remaining nine represent Family 2 transition-of-care gaps, in which the medication order may be correct but an important action such as monitoring, medication supply, restart instructions, or follow-up is missing. Required companion medication omitted (`f2_coprescription_omitted`) has count zero because it is `not_yet_implementable`. The scenario mix is not prevalence-weighted; heart-failure cases predominate, and community-acquired pneumonia appears once.

**How controls versus planted errors work (do not tell residents which is which):**

- **Clean control** (`inject_error: false`, `error_family` / `error_category` `none`): the clean intended plan remains. A held “stop” medication (when the scenario has one) stays off the discharge list. Companion actions that belong on a clean case (for example warfarin INR monitoring) remain present.
- **Error-bearing `CLINIPROOF_TAXONOMY_V1`:** one canonical `f1_*` or `f2_*` category specified in that batch plan **before** generation. Family 2 cases may look like a complete discharge list while a required monitoring row, restart instruction, supply duration, hospital-only stop, substitution revert, or follow-up is missing. This README does not list which `VAL-201`–`VAL-224` ids received which category.

Residents should review every case as if the assessment might be wrong (discharge list **and** monitoring / follow-up / instructions). Investigators score against [`data/validation/investigator_answer_key.md`](data/validation/investigator_answer_key.md) and [`data/validation/README.md`](data/validation/README.md) — not in resident packets.

### Freeze CLI output

```text
{"batch_code":"CLINIPROOF_TAXONOMY_V1","master_seed":20260922,"frozen":["VAL-201",...],"reused":[...],"rejected":[...]}
```

### Export CLI

```bash
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2
```

`--batch-code` is **required**. There is no default study batch. Export does not silently write archived `CLINIPROOF_TAXONOMY_V1`. `--output-dir` defaults to the registry directory for that batch code. Requires frozen rows **in the local database**. If none: `no frozen cases for batch <code>` (exit 2). If `--batch-code` is omitted, the CLI prints the active-batch list and exits 2.

Export regenerates blinded payloads, writes files listed in [§17](#17-resident-validation-output-files), and runs a leak audit (fails `audit_passed` if resident JSON contains markers such as `syn-000`, `answer_key`, `is_clean_control`, `rxcui:`, or `TEST_` identifier values).

Printed paths: `resident_path`, `investigator_path`, `manifest_path`, `coverage_path`, `worksheet_path`, `schema_path`, plus `audit_passed` / `audit_errors`.

---

## 17. Resident-validation output files

Each **active** batch writes the same family of files into its own directory:

- Balanced structured: [`data/validation_balanced_v3/`](data/validation_balanced_v3/) (`CLINIPROOF_BALANCED_V3`, VAL-501–VAL-524)
- Resident-seed-guided: [`data/validation_seedcases_v2/`](data/validation_seedcases_v2/) (`CLINIPROOF_SEEDCASES_V2`, VAL-601–VAL-624)

Archived historical files remain in [`data/validation/`](data/validation/) (`CLINIPROOF_TAXONOMY_V1`, VAL-201–VAL-224) and are **not** the current study packet. Generated files under `data/exports/` are gitignored. The table below uses the balanced directory as the path example. The seed-guided batch has the same filenames under `data/validation_seedcases_v2/`. The table tells you which file a resident may receive and which files are investigator-only.

| File | Purpose | Who should see it | Blinded? | Contains answer key? | Give to residents? |
| --- | --- | --- | --- | --- | --- |
| [`resident_validation_cases.json`](data/validation_balanced_v3/resident_validation_cases.json) | Dashboard-shaped cases (`VAL-*` ids, nested `ClinicalCase`, child arrays). Omits `CaseAnswerKey`. Titles use `VAL-*`. | Residents | Yes | No | **Yes — this is the case file** |
| [`resident_review_worksheet.csv`](data/validation_balanced_v3/resident_review_worksheet.csv) | Empty capture rows, one per VAL ID | Residents / study staff | Yes (no answers) | No | **Yes** |
| [`resident_review_schema.json`](data/validation_balanced_v3/resident_review_schema.json) | Worksheet field definitions (ratings 1–5, identified error type, comments, …) | Study staff; optional for residents | Yes | No | Optional |
| [`investigator_answer_key.json`](data/validation_balanced_v3/investigator_answer_key.json) | Seeds, `SYN-*`, error category, affected RXCUI, clean expected state, snapshots | Investigators | No | **Yes** | **No** |
| [`investigator_answer_key.md`](data/validation_balanced_v3/investigator_answer_key.md) | Human-readable key | Investigators | No | **Yes** | **No** |
| [`validation_manifest.json`](data/validation_balanced_v3/validation_manifest.json) | Freeze metadata, source versions, control status | Investigators | No | Control/error status | **No** |
| [`batch_plan.json`](data/validation_balanced_v3/batch_plan.json) | Planned VAL IDs, scenarios, inject flags, `error_family`, `error_category` | Operators / investigators | No | Planned errors | **No** |
| [`coverage_report.md`](data/validation_balanced_v3/coverage_report.md) | Counts by scenario/error/terminology | Investigators | No | Mix summary | **No** |
| [`scenario_coverage_matrix.md`](data/validation_balanced_v3/scenario_coverage_matrix.md) | Resolved meds/labs/diagnoses per family | Investigators | No | Not per-case answers | **No** |
| [`README.md`](data/validation_balanced_v3/README.md) | Batch catalog | Investigators | No | Mix / provenance | **No** |
| [`readable/all_cases.md`](data/validation_balanced_v3/readable/all_cases.md) | Human-readable charts without intended-assessment issues | Optional supporting view | Yes | No | Not a required review stage |
| [`readable/clinician_validation_packet.md`](data/validation_balanced_v3/readable/clinician_validation_packet.md) | Readable cases + intended issues + C1–C5 | Clinician/resident validators | Packet | **Yes** | Primary one-stage review file |
| [`readable/validation_rubric.md`](data/validation_balanced_v3/readable/validation_rubric.md) | C1–C5 rubric | Medical educators / validators | Rubric only | No | Rubric may be shared; it has no per-case answers |
| [`readable/clinical_validation_worksheet.csv`](data/validation_balanced_v3/readable/clinical_validation_worksheet.csv) | One empty rating row per case | Clinical reviewers / study staff | Identifiers only | No | Record C1–C5 here |

Resident vs investigator split is enforced in export code (`LEAK_MARKERS` in `app/services/validation_batch.py`). Do not “fix” blinding by editing resident JSON to add codes or keys.

---

## Human-readable clinician validation packets

Derived Markdown views live next to each batch:

- Active balanced: [`data/validation_balanced_v3/readable/`](data/validation_balanced_v3/readable/)
- Active seed-guided: [`data/validation_seedcases/readable/`](data/validation_seedcases/readable/)
- Archived V1: [`data/validation/readable/`](data/validation/readable/)

Frozen JSON in each batch directory is that batch’s source of truth. Generating Markdown does not regenerate VAL identifiers.

Clinical validation uses a single review stage. Use the clinician packet and worksheet for the batch under review. Start at [`data/active_validation_sets.md`](data/active_validation_sets.md).

To regenerate readable views after pulling, without modifying frozen JSON:

```bash
python -m app.services.readable_packets --batch-code CLINIPROOF_BALANCED_V3 --resident data/validation_balanced_v3/resident_validation_cases.json
python -m app.services.readable_packets --batch-code CLINIPROOF_SEEDCASES_V2 --resident data/validation_seedcases_v2/resident_validation_cases.json
```

The script requires `--batch-code` and `--resident`. It does not default to archived V1.

---

## 18. How to give cases to residents

This repository **does not contain a resident review UI**, dashboard importer, or scoring app. The HTTP API only searches local reference rows and serves `/health`. Delivery is a file handoff into whatever review process the study already uses.

1. **Send / import for review:** the active blinded JSON for the chosen set — [`data/validation_balanced_v3/resident_validation_cases.json`](data/validation_balanced_v3/resident_validation_cases.json) (`VAL-501`–`VAL-524`) or [`data/validation_seedcases_v2/resident_validation_cases.json`](data/validation_seedcases_v2/resident_validation_cases.json) (`VAL-601`–`VAL-624`). Clinicians validating whether the cases themselves are suitable should use the matching clinician validation packet and complete C1–C5 in one pass. Residents who must find the planted problem themselves should receive the blinded JSON, not the clinician validation packet.
2. **Keep investigator-only:** answer keys, `batch_plan.json`, `validation_manifest.json`, coverage files, batch README catalogs, [`data/docs/clinician_examples/syn-000904.json`](data/docs/clinician_examples/syn-000904.json), and the README subsection [Investigator-only generation example](#investigator-only-generation-example).
3. **Capture responses** in the matching `resident_review_worksheet.csv` or the clinician `clinical_validation_worksheet.csv`. Do not pre-fill ratings.
4. **Worksheet ↔ cases:** `validation_case_id` on each CSV row matches `case_id_code` in the resident JSON.
5. **“Clinically validated” in this project** means a clinician or resident completed C1–C5 in one pass and judged the case acceptable for the study protocol. Until that happens, use the dataset-status sentence: machine-validated synthetic resident-review cases pending clinician validation.
6. **The software’s checks are not clinical validity.** Passing `validate-cases` or the freeze audit does not certify realism of formulations, units, or narratives. Those judgments require review by clinicians.

Do not tell residents which cases are clean controls. Do not send archived VAL-201–VAL-224 as the current study packet.

---

## 19. Reproducing the frozen validation batch

The committed JSON and Markdown under `data/validation_balanced_v3/` and `data/validation_seedcases_v2/` are the active sources of truth. Archived files under `data/validation/` remain historical provenance.

Live bootstrap can differ because RxNav and LOINC ranking can change. The same string (`lisinopril`, `hemoglobin`, `edema`) may resolve to a different official concept. Seeds do not freeze upstream search order.

To reprint without mutating VAL identifiers, when the database already has an active freeze, run the matching explicit plan and batch code:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
# reused should list VAL-501 … VAL-524; rejected should be []
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v2/batch_plan.json
# reused should list VAL-601 … VAL-624; rejected should be []
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2
```

Compare export files to git. If they match, that study dataset is unchanged. Do not omit `--plan` or `--batch-code`; those commands no longer default to archived V1.

**Empty database rebuild** (may **not** bit-match if APIs drifted):

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v2/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2
```

If ranking differs, keep the committed files as the dataset. Start a new `batch_code` and new VAL IDs for any replacement study set. Do not hand-edit frozen JSON to substitute a “more typical” tablet RXCUI or conventional US lab unit the source did not return.

Freeze-time identity, seeds, RXCUIs, LOINC, and per-case planted errors: [`data/validation/README.md`](data/validation/README.md).

Generator version: `0.1.0` (`app/__init__.py` / `pyproject.toml`).

---

## 20. API

Start the process (venv active). `uvicorn` is a project dependency. Host and port below match the command used in this repository’s documentation; they are not FastAPI defaults.

**macOS/Linux** and **Windows PowerShell**:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

App: `app.main:app` (`title="Clinical Case Generator"`, `version="0.1.0"`). FastAPI also serves interactive docs at `http://127.0.0.1:8765/docs` (framework default, not a custom route).

No route calls OpenAI or external terminology services. Reference routes read PostgreSQL via `app.api.deps.get_session`.

### `GET /health`

Process liveness. **Does not** check the database.

**macOS/Linux**

```bash
curl -s http://127.0.0.1:8765/health
```

**Windows PowerShell**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8765/health
```

Response: `{"status":"ok"}` (HTTP 200).

### `GET /reference/medications` | `/labs` | `/diagnoses` | `/symptoms`

The table below lists query parameters for the local reference search routes in `app/api/reference.py`. These endpoints search already stored terminology rows; they do not call external APIs.

| Name | Type | Default | Constraints |
| --- | --- | --- | --- |
| `query` | string | `""` | Local substring search |
| `limit` | int | `20` | 1–100 |
| `offset` | int | `0` | ≥ 0 |

**macOS/Linux**

```bash
curl -s "http://127.0.0.1:8765/reference/medications?query=lisinopril&limit=20&offset=0"
```

**Windows PowerShell**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8765/reference/medications?query=lisinopril&limit=20&offset=0"
```

Response shape (`MedicationSearchPage` and siblings): `items` (full reference objects), `total`, `limit`, `offset`, `query`. Medication items include `rxcui`, names, provenance fields, and `id`. Lab items include `loinc_code`. Diagnosis items include `icd10cm_code` / `snomed_code`. Symptom items include `preferred_name` and possibly null `snomed_code`.

These endpoints require a reachable `DATABASE_URL`. `/health` does not.

---

## 21. Testing and code quality

From the repo root, venv active, PostgreSQL reachable at `DATABASE_URL` for the full suite:

```bash
pytest
ruff check .
mypy
```

Configuration:

- pytest: `testpaths = ["tests"]`, `asyncio_mode = auto`
- ruff: `target-version = py312`, `line-length = 100`, lint `E,F,I,UP,B,W`
- mypy: `python_version = 3.12`, `strict = true`, `files = ["app", "tests"]`, `exclude = ["alembic/"]`

### PostgreSQL and destructive migrations

`tests/conftest.py` session fixture runs `alembic upgrade head`, then **`downgrade base`**, then `upgrade head` on `DATABASE_URL`. That **drops and recreates** application tables.

Do **not** point `pytest` at a database whose frozen `VAL-*` rows you need to keep, unless you can re-run freeze afterward. `/health` tests do not need the database, but `pytest` with no arguments runs the whole suite, including constraint, sync, bootstrap, generation, API, and freeze tests.

### HTTP

Client tests use `httpx.MockTransport`. They do not use live LOINC credentials. Fixture identifiers use the `TEST_` prefix only. `TEST_` ids must not appear in the resident-validation dataset.

### Before opening a PR

1. Venv active; `ruff check .` and `mypy` clean.
2. PostgreSQL up; understand that `pytest` will migrate `DATABASE_URL` through `base`.
3. `pytest` green.
4. Do not rewrite `alembic/versions/1c236aeaadc7_phase_1_clinical_schema.py`.
5. Do not commit `.env` or credentials.
6. Do not add `TEST_` identifiers to resident exports.
7. Do not claim cases are clinically validated.

---

## 22. Common workflows

Commands below assume the venv is active and `.env` exists. Where the shell differs, both variants are shown.

### A. First-time setup

**macOS/Linux**

```bash
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
# Set LOINC_USERNAME and LOINC_PASSWORD in .env for labs.
docker compose up -d
clinical-case-generator db-init
```

**Windows PowerShell**

```powershell
git clone https://github.com/piaattufts/clinical-case-generator.git
cd clinical-case-generator
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
# Set LOINC_USERNAME and LOINC_PASSWORD in .env for labs.
docker compose up -d
clinical-case-generator db-init
```

### A2. Update an existing git clone

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
```

That updates **merged** `main` only. Feature-branch work (including a README or `data/validation/` that is still in an open PR) needs `git checkout <branch-name>` after `git fetch`. Full notes: [§5.4](#4-update-an-existing-clone).

### B. Refresh terminology

```bash
clinical-case-generator bootstrap-reference-data
```

Optional targeted sync (examples):

```bash
clinical-case-generator sync-rxnorm --name metoprolol
clinical-case-generator sync-loinc --query creatinine
clinical-case-generator sync-ucum --query milligram
clinical-case-generator sync-icd10 --query "atrial fibrillation"
```

### C. Generate three test cases

Requires bootstrap (including labs if the scenario lists labs).

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

Default scenario: `HF_INPATIENT`. IDs: `SYN-000001`–`SYN-000003`.

### D. Generate without injected errors

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --no-inject-error
```

### E. Validate a specific case

```bash
clinical-case-generator validate-cases --case-id SYN-000001
```

### F. Rebuild / export an active resident validation batch

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V3
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v2/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V2
```

**Warnings:** VAL IDs are immutable; freeze reuses existing matching rows. Export overwrites files in the registry directory for that batch code. Live APIs may change ranking. `pytest` can wipe the same database. Do not freeze onto archived VAL-201–VAL-224.

### G. Run the API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8765
```

### H. Run all checks

```bash
pytest
ruff check .
mypy
```

---

## 23. Troubleshooting

### `clinical-case-generator: command not found` (or PowerShell “not recognized”)

This usually means the virtual environment is not active, or the package is not installed. Activate `.venv` ([§5](#5-clone-and-initial-setup)), then run `python -m pip install -e ".[dev]"`. Confirm with `clinical-case-generator --help`.

### Connection refused / database errors talking to port 5432

This usually means PostgreSQL is not running, the port is wrong, or `DATABASE_URL` does not match the host, user, or password. Run `docker compose up -d`, then `docker compose exec postgres pg_isready -U postgres -d clinical_cases`. Confirm `DATABASE_URL` matches Compose (`postgres:postgres@localhost:5432/clinical_cases`) unless you intend a different server.

### Missing `.env`

Settings then fall back to defaults in `app/config.py`, so LOINC and OpenAI stay empty. Copy `.env.example` to `.env`. Alembic still uses `get_settings().database_url`.

### `LOINC is not configured. Missing LOINC_USERNAME, LOINC_PASSWORD. No generated fallback is used.`

`LoincClient` raises `SourceNotConfigured` when those variables are missing. Set both in `.env`. `sync-loinc` exits 2. Bootstrap skips labs (`skipped` in JSON) and continues. Generation that requires laboratories then fails resolution.

### `Could not resolve lab request '...' from an authoritative source`

This is a `ReferenceResolutionError`: the scenario laboratory query is not in `ref_lab_tests`, often because LOINC was skipped. Configure LOINC, re-run `bootstrap-reference-data`, and confirm `reference-search labs`.

### Unresolved medication / diagnosis / symptom during bootstrap

Official search returned nothing acceptable after combination filtering, token matching, or ranking. Inspect `unresolved` in the bootstrap JSON. Do not invent a code. Adjust the search string in the manifest only if you still query the official API.

### Duplicate / idempotent bootstrap or `db-init`

This is expected when unique identifiers already exist; the registry uses `on_conflict_do_nothing`. No additional fix is required. `db-init` reports `inserted this call: 0`. Bootstrap upserts the same RXCUI or LOINC again.

### Alembic / migration problems

The database is not empty of conflicting objects, or the URL is missing. Confirm `alembic current` and `DATABASE_URL`. Do not edit `1c236aeaadc7`. The destructive last resort on a development Docker database only is `docker compose down -v`, then bring the stack up and run `db-init`.

### OpenAI key missing

`OPENAI_API_KEY` is empty. No additional configuration is required if template narrative is acceptable. Generation still runs, and `narrative_source` is `template`.

### OpenAI request failure

`assemble_narrative` catches all exceptions and returns `None`. Generation continues with the template. Check the key, model, and network if you expected `"openai"` in CLI output.

### `case validation failed: ...`

A validation layer failed. The CLI prints the first error and exits 2. Read the `layer:` prefix. Clean cases must have zero mechanically detectable findings. Error-bearing cases must match the requested CliniProof category: Family 1 requires one discharge or plan mutation, and Family 2 requires the specified missing companion action. A hard dual-anticoagulant conflict, or missing INR when warfarin is selected, fails the clinical layer.

### `Frozen validation case VAL-00N cannot be overwritten`

The freeze row is immutable, the seed or scenario does not match, or `generate-synthetic-cases` targeted a frozen `SYN-000101`–`SYN-000124` or `SYN-000801`–`SYN-000824` identifier. Do not overwrite. Use a new batch and VAL identifiers, or reuse via freeze when the plan matches.

### `no frozen cases for batch <code>`

Export ran before freeze, pytest or a downgrade wiped rows, the command used the wrong database, or `--batch-code` named a batch that is not frozen locally. Run `freeze-validation-batch --plan ...` on this `DATABASE_URL`, or use the committed JSON without exporting. `--batch-code` is required; omitting it lists the two active prospective sets and the archived V1 code.

### Port 5432 or 8765 already in use

Another PostgreSQL instance or an old uvicorn process is bound to the port. Stop the other process, or change the host port in Compose or `--port`, and update `DATABASE_URL` if you change 5432.

### `Provide a name or RXCUI. Full RxNorm import is not run by default.`

`sync-rxnorm` was invoked with no `--name` or `--rxcui`. Similar messages exist for LOINC, UCUM, and ICD-10-CM. Pass a selector. There is no full-import flag except `sync-ucum --all`.

### pytest wiped my generated cases

The pytest session fixture downgrades the schema to `base`. Re-run bootstrap and freeze, or use a separate test database URL.

---

## 24. Data provenance and safety constraints

Every real reference row keeps official-source provenance: `source_system`, `source_version` (nullable if the API omitted it), and a timezone-aware `retrieved_at`. Canonical identifiers come only from those sources or from `TEST_` fixtures in tests. The generator does not invent RxNorm, LOINC, ICD-10-CM, UCUM, SNOMED CT, or UDI codes.

Unknown scalars on cases are stored as `NULL`, not empty strings. Vital signs and laboratory numbers are random-number-generator draws labeled `synthetic_model_generated`. `ref_clinical_distributions` is unused by this pipeline, and `MIMIC_IV_RAW` is rejected by a check constraint.

MIMIC is not ingested. The registry documents that raw rows are never stored as concepts and never sent to OpenAI. `MIMIC_LOCAL_PATH` is unused.

OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. Calls use `store=False`. The freeze path disables OpenAI.

Clinician review is required because official-source ranking can yield atypical formulations such as oral solutions or topical gel, SI example units, and oximetry hemoglobin LOINC. In the committed freeze, NLM conditions token-match stored **Anasarca** for an `edema` query and **Chronic fatigue syndrome** for `fatigue`. Software does not certify clinical realism.

---

## 25. Database, tables, and UML

This section is the schema map. Models: `app/models/`. Mixins: `app/database.py`. Migrations: `alembic/versions/`. The test list of table names is `EXPECTED_TABLES` in `tests/test_database_constraints.py`: **43** application tables (1 registry + 12 `ref_*` + 1 rules + 25 case hub/children + 4 generation/freeze), plus Alembic’s `alembic_version`.

Residents never connect to this database. They receive blinded JSON. Investigators who need planted-error catalogs use [`data/validation/README.md`](data/validation/README.md) — not a live SQL dump of `case_answer_keys`.

### What the database is

The table below records the local PostgreSQL identity used by this repository’s default Compose file. It is an implementation snapshot, not a claim about a hospital production database.

| Item | Value |
| --- | --- |
| Engine | **PostgreSQL 16** (`image: postgres:16` in `docker-compose.yml`) |
| Database name | `clinical_cases` |
| Default URL | `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` (Compose; not a production secret) |
| Volume | named Docker volume `clinical_cases_pg` |
| ORM | SQLAlchemy 2 declarative models |
| Migrations | Alembic. Head is `d4e8b17c6a91` |
| Create / migrate | `clinical-case-generator db-init` → `alembic upgrade head`, then seed nine `data_source_registry` rows |

`db-init` creates **empty** clinical tables. Official concepts arrive later via `bootstrap-reference-data`. Synthetic charts arrive via `generate-synthetic-cases` or `freeze-validation-batch`.

The same three data classes from [Project overview](#1-project-overview) are three groups of tables:

1. **Authoritative reference** — `ref_*` plus `clinical_rules`. Codes come from official APIs. Provenance columns are required on those rows (`source_system`, `source_version`, `retrieved_at`).
2. **Empirical aggregates** — `ref_clinical_distributions` only. This pipeline inserts **no** rows. `source_dataset = 'MIMIC_IV_RAW'` is rejected.
3. **Synthetic patient data** — `clinical_cases` and children, plus generation/freeze tables. Unknown scalars are `NULL`, not `""`.

### Identity rules (read this before the diagrams)

Every application table has an internal UUID primary key `id` (`gen_random_uuid()`). That UUID is not an RxNorm, LOINC, ICD-10-CM, or dashboard identifier. The table below distinguishes internal primary keys, official terminology codes, dashboard case identifiers, and frozen study identifiers. Read the kind of identifier first; the examples are tokens stored in the schema.

| Kind of identifier | Where it lives | Example |
| --- | --- | --- |
| Internal PK | `*.id` | UUID |
| Official terminology code | Unique/indexed column on `ref_*` | `ref_medications.rxcui`, `ref_lab_tests.loinc_code`, `ref_diagnoses.icd10cm_code`, `ref_units.ucum_code` |
| Dashboard case id | `clinical_cases.case_id_code` | `SYN-000001` |
| Frozen study id | `validation_batch_cases.validation_case_id` | `VAL-201` |
| Dashboard child id | unique nullable string on the child (`diagnosis_id`, `medication_id`, …) | `DX-SYN000001-001`, `MED-SYN000001-001` |

Optional foreign keys from a case child to a `ref_*` row use `ON DELETE RESTRICT`, so deleting a vocabulary concept cannot silently blank a case field. DailyMed labels (`ref_drug_labels.rxcui`) and RxClass membership (`ref_medication_classes.rxcui`) store the RXCUI **string**; they are not foreign keys to `ref_medications.id`. Clinical rules also store ICD/RXCUI/LOINC as strings, not FKs.

### UML — overall layout

The diagram below shows how data moves into tables. It is not a claim that every `ref_*` table is populated by the current pipeline.

```mermaid
flowchart TB
    subgraph sources [Official APIs]
        RxNav[RxNav RxNorm / RxClass]
        DailyMed[DailyMed]
        LOINC[LOINC FHIR TS]
        UCUM[UCUM essence XML]
        ICD[NLM ICD-10-CM]
        NLM[NLM conditions / HPO]
    end

    subgraph db ["PostgreSQL clinical_cases"]
        REG[data_source_registry]
        REF["ref_* vocabulary"]
        RULES[clinical_rules]
        CASE[clinical_cases + children]
        PLAN[case_medication_plans]
        KEY[case_answer_keys]
        GEN[case_blueprints / case_generation_runs]
        VAL[validation_batch_cases]
    end

    RxNav --> REF
    DailyMed --> REF
    LOINC --> REF
    UCUM --> REF
    ICD --> REF
    NLM --> REF
    REF --> RULES
    REF --> CASE
    RULES --> CASE
    CASE --> PLAN
    CASE --> KEY
    CASE --> GEN
    CASE --> VAL
    REG -.-> sources
```

`data_source_registry` is metadata about those APIs (enabled flag, last sync, `records_imported`). It does not store clinical concepts.

### UML — shared mixins

```mermaid
classDiagram
    class UUIDPrimaryKeyMixin {
        +UUID id PK
    }
    class ProvenanceMixin {
        +source_system
        +source_version
        +retrieved_at timestamptz
    }
    class CaseChildMixin {
        +UUID case_id FK CASCADE
    }

    UUIDPrimaryKeyMixin <|-- DataSourceRegistry
    UUIDPrimaryKeyMixin <|-- RefMedication
    ProvenanceMixin <|-- RefMedication
    UUIDPrimaryKeyMixin <|-- ClinicalRule
    ProvenanceMixin <|-- ClinicalRule
    UUIDPrimaryKeyMixin <|-- ClinicalCase
    UUIDPrimaryKeyMixin <|-- CaseMedication
    CaseChildMixin <|-- CaseMedication
    UUIDPrimaryKeyMixin <|-- ValidationBatchCase
```

`RefClinicalDistribution` is the exception among `ref_*` tables: it has a UUID PK but **no** provenance mixin (aggregates are local calculations, not official-source concepts). This pipeline does not insert distribution rows.

### UML — reference vocabulary and rules

Solid lines are real foreign keys. RXCUI/LOINC/ICD strings that are **not** FKs are omitted as edges (labels and class membership copy the official code as text).

```mermaid
erDiagram
    DATA_SOURCE_REGISTRY {
        uuid id PK
        string source_code UK
        bool enabled
        string sync_status
        int records_imported
    }

    REF_MEDICATIONS {
        uuid id PK
        string rxcui UK
        string concept_name
        string strength
        string source_system
    }

    REF_MEDICATION_CLASSES {
        uuid id PK
        string rxcui
        string class_id
        string class_name
        string class_type
    }

    REF_DRUG_LABELS {
        uuid id PK
        string set_id
        string rxcui
        text indication_text
    }

    REF_DIAGNOSES {
        uuid id PK
        string icd10cm_code
        string snomed_code
        string preferred_name
    }

    REF_SYMPTOMS {
        uuid id PK
        string snomed_code
        string preferred_name
    }

    REF_LAB_TESTS {
        uuid id PK
        string loinc_code UK
        string long_common_name
        jsonb example_ucum_units
    }

    REF_UNITS {
        uuid id PK
        string ucum_code UK
        string display_name
        numeric conversion_factor
    }

    REF_VITALS {
        uuid id PK
        string loinc_code
        string vital_name
    }

    REF_PROCEDURES {
        uuid id PK
        string procedure_code
        string procedure_name
    }

    REF_DEVICES {
        uuid id PK
        string device_identifier
        string device_name
    }

    REF_MICROBIOLOGY {
        uuid id PK
        string test_loinc_code
        string organism_code
    }

    REF_CLINICAL_DISTRIBUTIONS {
        uuid id PK
        string source_dataset
        string variable_code
        int n
    }

    CLINICAL_RULES {
        uuid id PK
        string rule_code UK
        string rule_type
        string severity
        bool enabled
        string input_rxcui
        string input_loinc_code
        string input_icd10cm_code
        text evidence_excerpt
    }
```

`ref_diagnoses` requires at least one of `snomed_code` or `icd10cm_code` (check constraint). This repository has **no SNOMED ingestion client**, so stored diagnoses use ICD-10-CM and leave `snomed_code` null rather than inventing a code.

Tables with a schema but **no implemented loader** in this pipeline: `ref_vitals`, `ref_procedures`, `ref_devices`, `ref_microbiology`, `ref_clinical_distributions`. AccessGUDID and MIMIC-IV have registry rows only.

### UML — one synthetic case

`clinical_cases` is the hub. Every `case_*` child except `case_medication_plans` / `case_generation_runs` / `validation_batch_cases` uses `CaseChildMixin` (`case_id` `ON DELETE CASCADE`). Optional `ref_*` links use `ON DELETE RESTRICT`.

```mermaid
erDiagram
    CLINICAL_CASES {
        uuid id PK
        string case_id_code UK
        bool clean_case
        string case_status
        int patient_age
        string specialty
    }

    CASE_BLUEPRINTS {
        uuid id PK
        string blueprint_id UK
        string target_error_category
        uuid primary_diagnosis_ref_id FK
    }

    CASE_GENERATION_RUNS {
        uuid id PK
        string run_id UK
        uuid blueprint_id FK
        uuid case_id FK
        string status
        jsonb metadata
    }

    CASE_MEDICATION_PLANS {
        uuid id PK
        string plan_id UK
        uuid case_id FK
        uuid ref_medication_id FK
        string decision
        bool is_error_target
    }

    CASE_MEDICATIONS {
        uuid id PK
        string medication_id UK
        uuid case_id FK
        uuid ref_medication_id FK
        string context
        string status
        string dose
        string frequency
        string quantity_or_days
        string monitoring
    }

    CASE_DIAGNOSES {
        uuid id PK
        string diagnosis_id UK
        uuid case_id FK
        uuid ref_diagnosis_id FK
        string diagnosis
    }

    CASE_LABS {
        uuid id PK
        string lab_id UK
        uuid case_id FK
        uuid ref_lab_id FK
        float value
        string unit
    }

    CASE_MONITORING {
        uuid id PK
        string monitoring_id UK
        uuid case_id FK
        string parameter
        string frequency
    }

    CASE_FOLLOWUPS {
        uuid id PK
        string followup_id UK
        uuid case_id FK
        string item
        string timing
    }

    CASE_INSTRUCTIONS {
        uuid id PK
        string instruction_id UK
        uuid case_id FK
        string instruction_text
    }

    CASE_ANSWER_KEYS {
        uuid id PK
        string answer_id UK
        uuid case_id FK
        string error_family
        string error_category
        jsonb trigger_meds
        bool is_primary_error
    }

    VALIDATION_BATCH_CASES {
        uuid id PK
        string validation_case_id UK
        string batch_code
        uuid case_id FK
        string error_family
        string error_category
        bool is_clean_control
        bool immutable
    }

    REF_MEDICATIONS ||--o{ CASE_MEDICATIONS : "ref_medication_id RESTRICT"
    REF_MEDICATIONS ||--o{ CASE_MEDICATION_PLANS : "ref_medication_id RESTRICT"
    REF_DIAGNOSES ||--o{ CASE_DIAGNOSES : "ref_diagnosis_id RESTRICT"
    REF_LAB_TESTS ||--o{ CASE_LABS : "ref_lab_id RESTRICT"
    REF_DIAGNOSES ||--o{ CASE_BLUEPRINTS : "primary_diagnosis_ref_id RESTRICT"

    CLINICAL_CASES ||--o{ CASE_MEDICATIONS : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_MEDICATION_PLANS : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_DIAGNOSES : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_LABS : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_MONITORING : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_FOLLOWUPS : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_INSTRUCTIONS : "CASCADE"
    CLINICAL_CASES ||--o{ CASE_ANSWER_KEYS : "CASCADE"
    CLINICAL_CASES ||--o| VALIDATION_BATCH_CASES : "RESTRICT"
    CASE_BLUEPRINTS ||--o{ CASE_GENERATION_RUNS : "RESTRICT"
    CLINICAL_CASES ||--o| CASE_GENERATION_RUNS : "SET NULL"
```

`case_medications.context` is constrained to `home` / `inpatient` / `inpatient_history` / `discharge`. `status` is constrained to `home` / `active` / `held` / `discontinued` / `discharge`. `case_medication_plans.decision` is constrained to `continue` / `stop` / `restart` / `hold` / `dose_change` / `new_start`. `validation_batch_cases.validation_case_id` must match `^VAL-[0-9]{3}$`.

Family 1 planted errors mutate discharge `case_medications` (and mark a plan `is_error_target`). Family 2 typically leaves the continued-drug identity intact and removes a companion row in `case_monitoring`, `case_followups`, `case_instructions`, or related fields such as `quantity_or_days`. The hidden key is `case_answer_keys` (omitted from resident JSON).

### Clinical content → table (physician map)

The table below maps what a clinician sees on the chart to the PostgreSQL table that stores it. The notes column says whether the content is source-backed, synthetic, or hidden from residents.

| What you see on the chart | Table | Notes |
| --- | --- | --- |
| Patient age, sex, specialty, SYN id | `clinical_cases` | Synthetic demographics |
| Chief complaint / HPI | `case_presentations` | Template or optional OpenAI wording of already-chosen names |
| Admission note | `case_notes` | Same narrative source |
| Symptoms | `case_symptoms` | Linked to `ref_symptoms` when resolved |
| Admission diagnosis | `case_diagnoses` | Linked to `ref_diagnoses` (ICD-10-CM) |
| Problem list | `case_problem_list` | Scaffolding text |
| Vitals | `case_vitals` | Synthetic numbers; `ref_vital_id` is typically null (no vital-concept loader) |
| Laboratory results | `case_labs` | Concept from `ref_lab_tests`; **numeric value is synthetic** |
| Weight | `case_weights` | Synthetic |
| Home / inpatient / discharge medications | `case_medications` | One row per drug per context; RXCUI via `ref_medications` |
| Intended continue/stop plan | `case_medication_plans` | Correct plan **before** injection; residents do not see this table |
| Held-med / restart language | `case_instructions` | Held medication without a restart plan (`f2_held_med_no_restart_plan`) reads this |
| Outpatient monitoring (e.g. INR) | `case_monitoring` | Required outpatient monitoring not arranged (`f2_monitoring_not_arranged`) removes this on error-bearing cases |
| Follow-up appointments | `case_followups` | Follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`) may remove a pending-decision follow-up |
| Discharge disposition | `case_discharge_planning` | Template “home” |
| Planted-error answer | `case_answer_keys` | Investigator only |
| Frozen VAL assignment | `validation_batch_cases` | Immutable lock + snapshots |

### Table catalog

The tables below list every application relation in this schema. Counts in the headings are how many tables sit in that group. They are an engineering inventory, not a clinical completeness claim.

**Registry (1)**

The registry stores metadata about official sources. `db-init` inserts nine rows and does not load vocabulary concepts.

| Table | Purpose | Loaded by |
| --- | --- | --- |
| `data_source_registry` | Nine source-metadata rows (`RXNORM`, `DAILYMED`, `RXCLASS`, `LOINC`, `UCUM`, `ICD10CM`, `SNOMED_CT`, `ACCESS_GUDID`, `MIMIC_IV`) | `db-init` only |

**Authoritative reference (12)**

These tables hold official terminology rows. Identifiers are stored only after an official service returns them.

| Table | Official identifier | Loaded by this pipeline? |
| --- | --- | --- |
| `ref_medications` | `rxcui` unique | Yes — RxNav |
| `ref_medication_classes` | `(rxcui, class_id, class_type, rela)` unique | Yes — RxClass (therapeutic substitution) |
| `ref_drug_labels` | DailyMed `set_id` / RXCUI string | Yes — DailyMed, after RxNorm |
| `ref_diagnoses` | `icd10cm_code` and/or `snomed_code` | Yes — ICD-10-CM search. SNOMED column stays null |
| `ref_symptoms` | `snomed_code` nullable | Yes — NLM conditions / HPO names; no invented SNOMED |
| `ref_lab_tests` | `loinc_code` unique | Yes — LOINC FHIR, if credentials are set |
| `ref_units` | `ucum_code` unique | Yes — UCUM essence XML |
| `ref_vitals` | optional LOINC | **No client** |
| `ref_procedures` | optional procedure code | **No client** |
| `ref_devices` | optional `device_identifier` (nullable so no fake UDI) | **No client** (AccessGUDID not implemented) |
| `ref_microbiology` | optional LOINC / organism code | **No client** |
| `ref_clinical_distributions` | aggregate key; `MIMIC_IV_RAW` forbidden | **No calculator** |

**Rules (1)**

The rules table stores curated if-then constraints. A rule is enabled only when DailyMed or RxClass evidence is attached.

| Table | Purpose |
| --- | --- |
| `clinical_rules` | Curated IF/THEN rows. `enabled` becomes true only when DailyMed/RxClass evidence is attached. Severity `hard` or `soft`. Current codes: `NO_DUAL_ORAL_ANTICOAGULANT`, `WARFARIN_INR_MONITORING`, `FUROSEMIDE_HF_INDICATION` |

**Synthetic case hub and children (25)**

These tables store one synthetic chart and its child documents. Empty schema tables exist for dashboard completeness even when generation does not populate them.

| Table | Role in generation |
| --- | --- |
| `clinical_cases` | One synthetic patient (`SYN-######`) |
| `case_presentations` | CC / HPI / ROS |
| `case_symptoms` | Symptom rows |
| `case_social_supports` | Living situation, language, … (template) |
| `case_diagnoses` | Diagnoses |
| `case_problem_list` | Problem + plan sentence |
| `case_notes` | Admission note |
| `case_vitals` | Synthetic vital numbers |
| `case_labs` | Synthetic lab numbers on official LOINC concepts |
| `case_weights` | Synthetic weight |
| `case_intake_outputs` | I/O scaffolding (often empty/net-zero template) |
| `case_medication_reconciliations` | Med-rec process flags (scaffolding) |
| `case_medications` | Home / inpatient / discharge drug lists |
| `case_monitoring` | Outpatient monitoring plan |
| `case_discharge_planning` | Disposition |
| `case_followups` | Follow-up items |
| `case_instructions` | Patient instructions (including hold/restart language) |
| `case_return_precautions` | Return-if language |
| `case_answer_keys` | Hidden CliniProof key after injection |
| `case_microbiology` | Schema for dashboard completeness; generation does not populate organisms |
| `case_imaging` | Schema; generation does not invent studies |
| `case_procedures` | Schema; no procedure loader |
| `case_devices` | Schema; no device loader |
| `case_consults` | Schema; generation does not invent consults |
| `case_therapy_restrictions` | Schema; unused by current scenarios |

**Generation and freeze (4)**

These tables record generation intent, run metadata, the correct medication plan before injection, and the immutable VAL freeze.

| Table | Purpose | Delete rule |
| --- | --- | --- |
| `case_blueprints` | Per-case generation intent (scenario, age band, `target_error_category`) | Referenced by runs `RESTRICT` |
| `case_generation_runs` | Seed, generator version, narrative source, validation JSON in `metadata` | `case_id` `SET NULL`; `blueprint_id` `RESTRICT` |
| `case_medication_plans` | Correct continue/stop plan before injection | `CASCADE` with the case |
| `validation_batch_cases` | Immutable `VAL-###` freeze, `error_family` / `error_category`, clean vs resident snapshots | `case_id` `RESTRICT` so a frozen case cannot be deleted out from under a VAL id |

**Alembic**

Alembic stores the current migration revision. It is not an application model.

| Table | Purpose |
| --- | --- |
| `alembic_version` | Current revision string. Not an application model |

Migration chain: `1c236aeaadc7` (Phase 1 clinical schema) → `7b9e4c21d6a0` (`clinical_rules`) → `c3f8a91b2e47` (`validation_batch_cases`) → `d4e8b17c6a91` (`error_family` column and `ref_medication_classes`). Do not rewrite `1c236aeaadc7`.

### Delete behavior (summary)

Case children, including `CaseChildMixin` rows and `case_medication_plans`, use `ON DELETE CASCADE` from `clinical_cases.id`. Optional foreign keys to `ref_*` tables use `ON DELETE RESTRICT`. `case_generation_runs.case_id` uses `ON DELETE SET NULL`. `case_generation_runs.blueprint_id` uses `ON DELETE RESTRICT`. `validation_batch_cases.case_id` uses `ON DELETE RESTRICT`, so a frozen case cannot be deleted out from under a VAL identifier.

### Inspecting the live schema

```bash
docker compose exec postgres psql -U postgres -d clinical_cases -c "\dt"
docker compose exec postgres psql -U postgres -d clinical_cases -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY 1;"
alembic current
```

After `db-init` and before bootstrap, every clinical table except `data_source_registry` has **zero** rows. That is intentional: the schema exists, the vocabulary does not, until official APIs are queried.

---

## 26. Current limitations

The paragraphs below inventory what the software does and does not do. They are not a clinical evaluation of the frozen cases.

The repository currently includes a PostgreSQL schema and Alembic migrations through `d4e8b17c6a91`; clients for RxNorm, credentialed LOINC, UCUM, ICD-10-CM, DailyMed, RxClass, NLM conditions, and NLM HPO; bounded bootstrap; three curated rules; five inpatient scenarios plus seed archetypes; deterministic generation with Family 1 and Family 2 injectors (see the taxonomy section); freeze and export of two active blinded VAL batches (`CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2`) with archived `CLINIPROOF_TAXONOMY_V1` retained for provenance; a local reference search API and `/health`; and optional OpenAI narrative wording that was not used on the committed freezes.

Several pieces are only partially implemented. SNOMED CT columns and a disabled registry row exist, but there is no ingestion client. AccessGUDID has enabled registry metadata but no client. `ref_clinical_distributions` has a table and a MIMIC_IV_RAW guard, but no calculator. LOINC laboratory bootstrap works only with credentials; otherwise those laboratories are skipped. The taxonomy specifies required companion medication omitted (`f2_coprescription_omitted`), but the software does not yet have a sufficiently source-backed deterministic companion-prescription rule (`not_yet_implementable`), so freeze rejects that category rather than guessing. Narrative wording always has a template path. OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. If the call fails, wording falls back silently to the template.

The following capabilities are not implemented: AccessGUDID or SNOMED CT ingestion; MIMIC ingestion or aggregate calculation; a resident review user interface or dashboard application; a full vocabulary import (`sync-all` does not exist); companion co-prescription errors such as a steroid without a proton-pump inhibitor or an opioid without a bowel regimen, unless a stored rule exists; a complete clinical-realism guarantee, because human review is required; and using OpenAI as clinical truth, error chooser, or answer-key writer.

The archived freeze `CLINIPROOF_TAXONOMY_V1` has additional study-design limits that motivated the two active sets. That historical batch is not evenly distributed by scenario: thirteen of twenty-four cases use the heart-failure inpatient skeleton, four use hypertension, three use atrial fibrillation with anticoagulation, three use type 2 diabetes, and one uses community-acquired pneumonia. It is not a prevalence-weighted or representative sample of inpatient medicine. Several error categories occur only once, so that batch alone does not support stable category-specific psychometric estimates. The active batch `CLINIPROOF_BALANCED_V3` rebalances those families and requires distinct clean-case fingerprints, but it is still not a prevalence-weighted sample and still requires clinician review. The active batch `CLINIPROOF_SEEDCASES_V2` uses resident-authored seed archetypes rather than the five template families and also requires clinician review. Required companion medication omitted (`f2_coprescription_omitted`) is intentionally absent because the software does not yet have a sufficiently source-backed deterministic rule for that situation (`not_yet_implementable`). Official source ranking can produce technically source-valid but clinically atypical formulations or units, such as RxNorm solutions or gels, or SI laboratory units. Clinical plausibility therefore requires physician review.

---

## 27. Licensing

Terminology and dataset content is **not bundled**. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license and access rules. LOINC requires a Regenstrief account. SNOMED CT and MIMIC-IV stay disabled in `data_source_registry` until a future ingestion path exists; setting unused env vars does not load them.
