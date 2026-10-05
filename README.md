# CliniProof

CliniProof builds structured synthetic inpatient charts for studying discharge medication decisions. A resident receives a clean clinical chart and decides which medicines should continue, stop, start, or change after discharge. The intended regimen is stored separately as a hidden reference discharge plan. It is used only for evaluation.

The charts are not extracts from a medical record. Medication, diagnosis, and laboratory concepts are tied to standard terminologies. Ages, vital signs, and laboratory numbers are synthetic. A clinician still has to decide whether a chart is fit to use.

```text
Current status

- Clean resident/evaluator separation implemented.
- Default generator produces clean cases only.
- Original 48-case balanced set recovered from archived clean sources.
- 44 cases currently ready for clinician review.
- 4 cases remain clinically inconsistent and are excluded pending resolution.
- Original frozen VAL files remain unchanged.
```

The study set is not finalized. Passing automated tests does not mean a case has passed clinician review.

## Project purpose

The project creates structured inpatient clinical cases for studying discharge medication decision-making and related clinical reasoning.

The resident receives a clean clinical chart and independently determines the discharge medication regimen. The resident is not asked to find a deliberately planted medication error. The base case does not contain one.

The intended discharge regimen is retained separately as a hidden reference standard for validation and later scoring. A complete scoring engine is not implemented in this repository. Comparison of a resident response with the reference is a study procedure, not a finished product.

## Core principle

> The clinical case and the scoring reference are deliberately separated. Residents see the clinical evidence needed to make a discharge decision, but they do not see the intended discharge medication plan. The hidden reference plan is used only for evaluation.

## Study workflow

```text
source-backed clinical data
        ↓
clinically coherent case
        ↓
resident-facing clean chart
        ↓
resident determines discharge medication plan
        ↓
hidden reference discharge plan
        ↓
resident response compared with reference
        ↓
errors / agreement / reasoning can be evaluated
```

The same sequence, drawn as the study steps:

```text
Clinical case
    ↓
Resident-facing chart
    ↓
Resident proposes discharge medications
    ↓
Hidden reference discharge plan
    ↓
Comparison / scoring
```

A later experiment may insert an AI recommendation between the resident's first decision and a revised decision. That recommendation is not part of the base case.

```text
Resident initial decision
    ↓
AI recommendation
    ↓
Resident accepts / rejects / revises
    ↓
Final decision
```

Any manipulated AI recommendation is a separate experimental intervention. It is not written into the clinical chart the resident reads first.

## Resident and evaluator views

Two files can describe the same underlying case. They do not expose the same information.

### Resident-facing case

The resident-facing case may contain:

- presentation
- diagnoses and history
- hospital course
- home medications
- inpatient medications
- labs and vitals
- relevant treatments
- discharge disposition
- instructions that do not reveal the regimen
- follow-up context

It must not contain:

- the reference discharge medication plan
- expected discharge decisions
- an answer key
- scoring labels
- planted-error labels
- evaluator rationale

Home and inpatient medication lists are clinical evidence. They are not the answer. The resident still has to decide what should happen at discharge.

### Evaluator representation

The evaluator file is the resident chart plus `reference_discharge_plan`. It is not for study participants.

Where the recovered cases have the information, each reference medication includes the medicine, the action (`continue`, `start`, `stop`, `change`, `hold`, or `restart`), dose, route, frequency, duration, indication, rationale, and any monitoring note stored on that row. The plan also lists monitoring requirements and follow-up requirements when those rows exist.

Newly generated cases, built by `app/services/resident_case.py`, add evaluator-only fields: `required`, `evidence_class`, `supporting_evidence`, `evidence_trace`, and `consistency_errors`. Those fields are not in the recovered 48-case files. `acceptable_alternatives` and `contraindications` exist on newly generated plans and are currently empty lists. `medications_to_stop` is filled only when a reference action is `stop`.

## `reference_discharge_plan`

This object is the hidden reference standard. The example below is the recovered plan for VAL-701, a synthetic heart-failure chart. It is not a real patient.

```json
{
  "medications": [
    {
      "medication": "lisinopril 10 MG Oral Tablet",
      "action": "continue",
      "dose": "10 MG",
      "route": "oral",
      "frequency": "once daily",
      "duration": null,
      "indication": "Essential (primary) hypertension",
      "rationale": "Home therapy is continued through discharge in the clean case.",
      "monitoring": null
    }
  ],
  "monitoring_requirements": [],
  "follow_up_requirements": [
    {
      "item": "Heart-failure clinic follow-up",
      "timing": "7 days",
      "with_service": "cardiology"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `medication` | Drug name as charted |
| `action` | Intended discharge action |
| `dose`, `route`, `frequency` | Intended administration |
| `duration` | Days' supply or course length when the clean chart stored one. Often null |
| `indication` | Diagnosis or purpose stored on the medication row |
| `rationale` | Why the reference records that action. On the recovered set this is often the original generator sentence, not a new narrative |
| `monitoring` | Monitoring text stored on that medication row, or null |
| `monitoring_requirements` | Case-level monitoring tasks. Empty when the clean chart had none |
| `follow_up_requirements` | Follow-up item, timing, and service |

`required`, `medications_to_stop`, `acceptable_alternatives`, and `contraindications` are part of the generator's evaluator document. They are not fields in the recovered VAL-701 file above. Do not assume every export fills them.

The full VAL-701 evaluator file is [exports/clean_balanced_seed_set/VAL-701_evaluator.json](exports/clean_balanced_seed_set/VAL-701_evaluator.json). The matching resident file omits `reference_discharge_plan`.

## Frozen source batches

The registry still lists two active prospective validation datasets. They are the frozen originals that the recovery read. They are not the files to give a resident.

| Case set | Cases | Generation approach | Frozen files |
| --- | ---: | --- | --- |
| [Balanced structured set](data/case_sets/balanced/README.md) | 24 | Balanced structured generation from predefined profiles | `CLINIPROOF_BALANCED_V4`, VAL-701–VAL-724 |
| [Resident-seed-guided set](data/case_sets/seed_guided/README.md) | 24 | Resident-seed-guided generation from six resident-authored archetypes | `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824 |

`CLINIPROOF_BALANCED_V4`, VAL-701 through VAL-724, uses predefined structured clinical profiles: heart failure, atrial fibrillation, hypertension, type 2 diabetes, and pneumonia. Each of the 24 assignments uses a different profile. The counts are a study-design choice. The set is not prevalence-weighted.

`CLINIPROOF_SEEDCASES_V3`, VAL-801 through VAL-824, starts from six resident-provided cases abstracted into archetypes. The VAL charts are not copies of those documents. The six workflows are medication-history uncertainty, acute heart-failure decompensation, endocarditis treated with outpatient parenteral antibiotics, kidney transplant with cytomegalovirus treatment, hip fracture with interruption and resumption of anticoagulation, and gastrointestinal bleeding with anticoagulation holds and restart decisions.

Readable Markdown for the frozen charts remains at [data/case_sets/balanced/readable/all_cases.md](data/case_sets/balanced/readable/all_cases.md) and [data/case_sets/seed_guided/readable/all_cases.md](data/case_sets/seed_guided/readable/all_cases.md). Those pages still show the historical charts, including discharge lists and, where injected, the planted discrepancy. Do not use them as the current resident-facing study set.

Historical validation artifacts are retained for provenance and reproducibility. They should not be used as the current resident-facing study set.

## What this repository studies

Discharge is a high-risk transition. The study question is which medicines a resident would continue, stop, start, or change, given the chart. Differences from the hidden reference can later be classified. That classifier is not built here.

The repository holds two active prospective validation datasets, 48 cases in all, as frozen source batches. The recovered resident-facing export of those same 48 slots is [exports/clean_balanced_seed_set/](exports/clean_balanced_seed_set/AUDIT.md). Forty-four of those recovered cases are ready for expert review. Four are not. None of the 48 is clinically approved.

OpenAI is optional. It may only reword narrative from facts the structured generator has already chosen. It does not choose diagnoses, medications, doses, or the reference plan. The committed study cases used template wording.

Neither set is a prevalence-weighted sample of hospital discharges. Passing automated validation does not establish clinical validity. Human clinician validation remains required.

## How a clean case is constructed

```text
Clinical scenario or resident-derived archetype
        ↓
Structured clinical profile
        ↓
Diagnoses, labs, vitals, hospital course, medication history
        ↓
Hidden reference discharge plan
        ↓
Resident-facing chart (no reference plan)
        ↓
Automated structural checks
```

Default generation writes one clean case. It does not inject a medication error and does not write a second case.

The historical frozen batches were built differently. After the clean chart passed, the batch plan introduced one discrepancy for most cases and left four controls in each set of 24 unchanged. That step is experimental / legacy / optional and not part of the default resident case pipeline. See [Experimental error injection](#experimental-error-injection).

Balanced structured generation and resident-seed-guided generation are the two labels for how the frozen profiles were chosen. They share terminology, regimens, and validation. They are not two versions of the same batch.

## Generation

The default command generates clean cases. No medication error is injected. No second corrupted case is written. The hidden reference plan is retained on the case for an evaluator export. Pass `--scenario` when you want a family other than the first scenario in `data/bootstrap/scenarios.json` (currently `HF_INPATIENT`).

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
```

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42 --scenario HF_INPATIENT
```

Validate one persisted case:

```bash
clinical-case-generator validate-cases --case-id SYN-000001
```

The generator does not treat product strength as the administered dose and does not assume once daily. Curated regimens live in [data/bootstrap/medication_regimens.json](data/bootstrap/medication_regimens.json). If a real medication has no curated regimen, generation fails rather than inventing a dose.

## Experimental error injection

`--inject-error` is experimental / legacy / optional and not part of the default resident case pipeline. Do not use it to generate the resident study set.

```bash
clinical-case-generator generate-synthetic-cases --count 1 --seed 42 --inject-error --error-category f1_omission
```

It is retained for future experimental work and for the historical validation batches. The flag does not add an error label beside an otherwise clean chart. It changes the chart: a dose, a route, a frequency, a supply, a monitoring task, a follow-up, a restart instruction, or which drug is present at discharge. Restoring a clean case requires the pre-injection source. Deleting metadata is not enough.

The historical categories are documented in [docs/error_taxonomy.md](docs/error_taxonomy.md). Family 1 changes the regimen itself (`f1_omission`, `f1_commission`, `f1_dose_mismatch`, `f1_route_mismatch`, `f1_frequency_mismatch`, `f1_therapeutic_substitution`). Family 2 changes the transition around the list (`f2_monitoring_not_arranged`, `f2_held_med_no_restart_plan`, `f2_insufficient_supply`, `f2_hospital_only_continued`, `f2_inpatient_substitution_not_reverted`, `f2_pending_decision_followup_missing`). A required companion medication omitted (`f2_coprescription_omitted`) is defined conceptually and is not implemented.

### C1 — Clinical plausibility

### C2 — Intended assessment problem

### C3 — Detectability

### C4 — No unintended clinically meaningful problem

### C5 — Difficulty

Those five headings are the ratings printed in the historical Word casebooks for the frozen charts. C1 asks whether the encounter is believable. C2 asks whether a predetermined discrepancy, when one was injected, is actually present. A control should contain none. C3 asks whether a resident could see that historical problem. C4 asks whether a second problem could be mistaken for the answer. C5 is advisory. Accept. Revise. Exclude. are the recommendations in that casebook. They are not a claim that the recovered clean cases have been through that review.

The validation casebooks are fillable Microsoft Word documents. Click the checkboxes to select ratings and type comments directly into the provided fields. Please select one response per rating item. Open the file in desktop Microsoft Word. The historical casebooks are [the balanced casebook](docs/resident_review_package/files/CliniProof_Balanced_Validation_Casebook.docx) and [the seed-guided casebook](docs/resident_review_package/files/CliniProof_SeedGuided_Validation_Casebook.docx). Do not give those casebooks to a resident. Each one prints a validation reference after C1.

## Recovered balanced study set

[exports/clean_balanced_seed_set/](exports/clean_balanced_seed_set/AUDIT.md) is the current resident-facing export of the original 48 case slots.

- 48 original case slots were recovered.
- No cases were regenerated.
- Original seeds were preserved.
- Original scenarios were preserved.
- Original profiles were preserved.
- The original frozen VAL files were not overwritten.
- Error-bearing cases were recovered from their archived pre-injection clean source.
- Clean controls used their original clean chart.

| Status | Count |
| --- | ---: |
| Recovered from clean source | 48 |
| Reconstructed from seed | 0 |
| Minor cleanup | 3 |
| Clinically inconsistent | 4 |
| Unrecoverable | 0 |
| Ready for expert review | 44 |

Ready for expert review means the injected chart change and the discharge-answer wording are gone, and the automated clinical pass did not find a blocking inconsistency. It does not mean an expert has approved the case.

The full row-by-row record is [exports/clean_balanced_seed_set/AUDIT.md](exports/clean_balanced_seed_set/AUDIT.md).

### Four cases that are not validated study cases

These four are not currently considered validated study cases. They are exported and labeled `CLINICALLY_INCONSISTENT`. They were not rewritten, and no replacement was generated.

| Case | Problem |
| --- | --- |
| VAL-709 | Ibuprofen is stopped without a visible clinical reason |
| VAL-711 | Ibuprofen is stopped without a visible clinical reason |
| VAL-714 | Pantoprazole is associated with hypertension, which is not a supported indication on that chart |
| VAL-801 | Ibuprofen is stopped without a visible clinical reason |

### Three traceable monitoring restorations

VAL-703, VAL-707, and VAL-817 lost the INR monitoring row when historical error injection removed it. The body of that row was not archived. Recovery restored it from two stored facts: the case's own INR laboratory name, and the warfarin-monitoring frequency, trigger, and service text that the generator writes and that remains on the untouched clean control VAL-710. This did not add a new clinical fact. It put back the monitoring task the clean chart had before injection.

## Output directory

```text
exports/clean_balanced_seed_set/
```

| File | Role |
| --- | --- |
| `AUDIT.md` | Seed, scenario, recovery source, cleanup, and final status for each of the 48 cases |
| `VAL-701_resident.json` | Resident-facing chart. No reference plan |
| `VAL-701_evaluator.json` | Same chart plus `reference_discharge_plan` |

The same pair exists for every identifier from VAL-701 through VAL-724 and from VAL-801 through VAL-824. Resident and evaluator files are the same underlying case with different exposure. Do not show the evaluator file to a participant.

## Provenance of a recovered case

```text
original generated clean case
        ↓
archived pre-injection snapshot
        ↓
historical injected variant
        ↓
recovery uses archived clean source
        ↓
resident/evaluator split
```

The recovered set does not come from rerunning the generator. Seeds in `AUDIT.md` are the original assignment seeds. Re-running generation with today's code would not reproduce these files, because the default decision path has changed and because recovery refuses to draw a new case.

A source-backed terminology concept is not automatically a clinically appropriate choice for a particular synthetic patient. Provenance detail is in [docs/provenance.md](docs/provenance.md).

## Case lifecycle

```text
generated
validated
frozen
optionally error-injected for historical experiments
recovered from clean source
resident/evaluator export
expert review
```

Error injection is not required. The default lifecycle stops at a clean case, a hidden reference, and expert review. The optional injection step describes only the historical batches and future experiments.

## Structural validation and clinical validation

### Structural validation

Automated checks can confirm that required fields exist, that the resident file does not contain the reference plan, that serialization is valid, that identifiers resolve to source-backed rows, and that the same seed rebuilds the same development case. `tests/test_clean_set_recovery.py` checks that recovery does not modify the frozen resident export.

### Clinical validation

A clinician still has to judge whether each medicine has an appropriate indication, whether the discharge action is justified by the chart, whether labs and monitoring fit the medicines, and whether the hidden reference is defensible. More than one regimen can be reasonable. Missing information, contradictions, inappropriate monitoring, and unsafe recommendations are reasons to exclude a case.

> Passing automated tests does not mean a case has passed clinician review.

The recovered set contains 44 cases ready for expert review. Those 44 are not cases that experts have already validated.

## Using the cases in a study

1. Show the resident the clean chart (`*_resident.json`), not the evaluator file.
2. Collect the resident's discharge medication decisions.
3. Optionally collect confidence and reasoning.
4. Compare the response with `reference_discharge_plan` in the evaluator file.
5. Classify differences. A scoring engine for that comparison is not implemented here.
6. Optionally, in a later experiment, introduce an AI recommendation that is not part of the base chart.
7. Collect a revised decision.
8. Analyze changes in accuracy, reliance, confidence, or reasoning.

## Clinician review

Review the recovered resident chart and, separately, the hidden reference. Do not stop at whether the file parses.

Assess:

- clinical coherence and realism
- whether the chart contains enough information to decide
- medication indications
- whether the hidden reference action is defensible
- whether more than one answer could reasonably be accepted
- missing information and contradictions
- inappropriate monitoring
- unsafe recommendations

The four inconsistent cases above should be reviewed as problems, not as cases that already passed.

## Repository structure

```text
app/services/generation.py           default clean-case generator
app/services/resident_case.py       resident chart versus hidden reference plan
app/services/validation.py           structural and coherence checks
app/services/error_injection.py      experimental chart discrepancies; not the default path
app/services/clean_set_recovery.py   rebuilds the 48 resident/evaluator files from frozen sources
app/services/validation_batch.py     freeze and export of historical VAL batches
tests/test_clean_resident_case.py    clean generation hides the reference and does not inject an error
tests/test_clean_set_recovery.py     recovery leaves frozen files unchanged and restores known clean facts
exports/clean_balanced_seed_set/     current resident-facing and evaluator export of the 48 slots
```

Methods and the directory map are also in [docs/methods.md](docs/methods.md) and [docs/repository_structure.md](docs/repository_structure.md).

## Testing

```bash
pytest
pytest tests/test_clean_resident_case.py
pytest tests/test_clean_set_recovery.py
```

`pytest` runs the full suite. It rebuilds the database schema and will wipe local case rows.

`tests/test_clean_resident_case.py` checks that a default generated case has no injected error, that the resident document omits discharge-context medications and `reference_discharge_plan`, and that the evaluator document still has the reference.

`tests/test_clean_set_recovery.py` checks that the original resident export is unchanged, that pre-injection content is restored (VAL-701 lisinopril remains a continue at 10 MG), that a known injected dose change is reversed (VAL-708 atorvastatin is 40 MG, not the planted 20 MG), and that recovered files are written to a separate directory.

Also used before a code change is considered complete:

```bash
ruff check .
mypy app
python scripts/check_docs.py
```

## LOINC

Laboratory import uses the LOINC FHIR value set at `http://loinc.org/vs`. The older URL `http://loinc.org?fhir_vs` returns 404 and is not the active endpoint. The FHIR base is `https://fhir.loinc.org`.

`LOINC_USERNAME` and `LOINC_PASSWORD` are read from the environment or from a local `.env` file. `.env` is gitignored. Do not commit credentials. Empty LOINC credentials stop laboratory import. They do not stop a checkout of the frozen or recovered cases.

## Environment

Copy `.env.example` to `.env`. The settings the application reads are:

| Variable | Role |
| --- | --- |
| `DATABASE_URL` | PostgreSQL URL. Default in code: `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases` |
| `LOINC_USERNAME` | LOINC account name. Required for laboratory import |
| `LOINC_PASSWORD` | LOINC account password. Required for laboratory import. Never commit it |
| `OPENAI_API_KEY` | Optional. Empty means template narrative |
| `OPENAI_MODEL` | Optional model name. Default `gpt-5` |
| `SNOMED_BASE_URL` | Unused until a SNOMED ingestion path exists. Leave empty |
| `SNOMED_API_TOKEN` | Unused until a SNOMED ingestion path exists. Leave empty |
| `MIMIC_LOCAL_PATH` | Unused. MIMIC-IV is not ingested. Leave empty |

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
```

`db-init` applies migrations. It does not rewrite committed case files.

## Historical datasets and provenance

Earlier frozen batches are retained under [data/archive/validation_sets/](data/archive/validation_sets/README.md) for reproducibility and provenance. They are not the current study set.

| Historical batch | Archive directory | Historical identifiers |
| --- | --- | --- |
| `CLINIPROOF_TAXONOMY_V1` | `data/archive/validation_sets/CLINIPROOF_TAXONOMY_V1` | historical VAL-201–VAL-224 |
| `CLINIPROOF_BALANCED_V2` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V2` | historical VAL-301–VAL-324 |
| `CLINIPROOF_BALANCED_V3` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V3` | historical VAL-501–VAL-524 |
| `CLINIPROOF_SEEDCASES_V1` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V1` | historical VAL-401–VAL-424 |
| `CLINIPROOF_SEEDCASES_V2` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V2` | historical VAL-601–VAL-624 |

The frozen `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3` directories under `data/case_sets/` are also retained. They are the source of the recovery, not the current resident-facing export.

Teaching charts that are not study cases are in [docs/clinician_walkthrough/README.md](docs/clinician_walkthrough/README.md). TEACH-002 shows one historical injected omission. It is not a recovered study case.

## Limitations

- The cases are synthetic.
- The scenario list is a bounded teaching set.
- Neither original batch is prevalence-weighted.
- A terminology code does not prove a dose is appropriate.
- Companion-drug omission is not implemented.
- Regimens are curated for these profiles. They are not a universal prescribing engine.
- There is no resident-review application and no finished scoring engine in this repository.
- SNOMED CT and MIMIC-IV are not ingested.
- The four inconsistent recovered cases are not ready for use as study cases.

## Licensing

Terminology content is not bundled. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license. LOINC requires a Regenstrief account.
