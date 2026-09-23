# CliniProof

CliniProof is a synthetic clinical-case generation and validation framework for studying medication reconciliation and transition-of-care reasoning.

The cases are hospital charts written for clinicians, medical educators, residents, and research collaborators. Each chart is a new synthetic encounter. It is not an extract from a medical record. Medication, diagnosis, and laboratory concepts are tied to standard terminologies. Ages, vital signs, and laboratory numbers are synthetic. A clinician still has to decide whether the chart is fit to use.

## Current prospective case sets

Two case sets are open for review. Both have 24 cases. Both are pending human clinician validation. They ask different design questions. They are not two versions of the same batch.

| Case set | Cases | Generation approach | Main purpose |
| --- | --- | --- | --- |
| [Balanced structured case set](data/case_sets/balanced/README.md) | VAL-701–VAL-724 (24) | Balanced structured generation | Controlled coverage across common inpatient scenario families |
| [Resident-seed-guided case set](data/case_sets/seed_guided/README.md) | VAL-801–VAL-824 (24) | Resident-seed-guided generation | Workflow diversity grounded in resident-authored clinical archetypes |

Batch codes, kept in the study files: `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3`.

## How the two sets differ

| | [Balanced structured set](data/case_sets/balanced/README.md) | [Resident-seed-guided set](data/case_sets/seed_guided/README.md) |
| --- | --- | --- |
| Cases | 24 | 24 |
| Starting point | predefined structured profiles | resident-authored clinical archetypes |
| Primary design goal | controlled scenario coverage | clinically grounded workflow diversity |
| Patient data | synthetic | synthetic |
| Source case copied | N/A | No |
| Prevalence weighted | No | No |
| Clinician validation required | Yes | Yes |

The table compares design choices. It does not rank the strategies. A reader should choose a set because of the question being asked.

## For clinicians

Start with the overview page for either case set. That page shows the clinical composition, how every chart is organized, the 24-case map, and how to record a review. You do not need the generator, the database, or the answer key to begin.

- [Balanced structured overview](data/case_sets/balanced/README.md), then [all cases](data/case_sets/balanced/readable/all_cases.md), the [clinician validation packet](data/case_sets/balanced/readable/clinician_validation_packet.md), and the [worksheet](data/case_sets/balanced/readable/clinical_validation_worksheet.csv).
- [Resident-seed-guided overview](data/case_sets/seed_guided/README.md), then [all cases](data/case_sets/seed_guided/readable/all_cases.md), the [clinician validation packet](data/case_sets/seed_guided/readable/clinician_validation_packet.md), and the [worksheet](data/case_sets/seed_guided/readable/clinical_validation_worksheet.csv).
- A short teaching walkthrough, separate from the study cases, is in [docs/clinician_walkthrough/README.md](docs/clinician_walkthrough/README.md).

The packet includes the intended assessment issue so a validator can rate the chart and the target together. The case pages in `all_cases.md` do not. Do not send the packet or the answer key to a resident who is supposed to find the problem without being told what it is.

## What this repository studies

Discharge is a high-risk transition. A drug can be left off the list, continued when it should stop, written at the wrong dose, route, or frequency, or continued without the monitoring, supply, restart, or follow-up that makes it safe. Those problems are common in medication reconciliation, and they are easy to miss when the list itself looks tidy.

CliniProof builds charts in which that question can be studied under known conditions. Some charts contain one medication-reconciliation or transition-of-care problem. Some are clean controls, so a reviewer cannot assume every chart is wrong. The immediate use of the two case sets is clinician validation: is each chart plausible, is the intended problem actually there, could a resident find it, and is there a second problem that could be mistaken for the answer?

## Study design

The repository holds two active prospective validation datasets, 48 cases in all. Each dataset is frozen as its own batch. Both strategies build a clinically coherent clean case before any assessment problem is introduced. Canonical medication, diagnosis, and laboratory concepts are resolved from the project's terminology tables. Demographics, numeric results, and narrative wording are synthetic. The assigned problem is chosen in the batch plan. It is not chosen by a language model, and a failed assignment is not silently replaced with a different category.

OpenAI is optional. It may only reword narrative from facts the structured generator has already chosen. It does not choose diagnoses, medications, doses, error categories, or answer-key content. The committed study cases used template wording.

Neither set is a prevalence-weighted sample of hospital discharges. Passing software checks does not make a chart clinically valid. Human clinician validation remains required. The cases are ready for that review. They are not yet clinically validated.

## Balanced structured generation

The balanced set is built from predefined clinical scenario families and named clinical profiles. The current families are heart failure, atrial fibrillation, hypertension, type 2 diabetes, and pneumonia. Each of the 24 assignments uses a different profile. The counts are a study-design choice: five cases in each of the first four families and four pneumonia cases. They are not an estimate of how often those problems are admitted.

Each profile specifies the presentation, the medication roles, the hospital course, and the follow-up. Generation then:

1. selects the scenario family and the named profile;
2. constructs a synthetic clean encounter;
3. checks terminology, units, route and formulation, and the implemented clinical rules;
4. audits whether the clean case is distinct from the other clean cases;
5. confirms that the preassigned target is eligible for that chart;
6. introduces exactly one discrepancy, or keeps the chart as a clean control;
7. checks the chart again;
8. freezes separate resident-facing and investigator-facing files.

The overview, including the case map, is [data/case_sets/balanced/README.md](data/case_sets/balanced/README.md).

## Resident-seed-guided generation

The seed-guided set starts from six resident-authored clinical examples. Those documents are design references. They are not copied into the study charts, and they are not an epidemiologic sample. A reviewer abstracted each example into an archetype: the discharge workflow the chart has to support. Four synthetic profiles were then written for each archetype so the 24 charts differ before any assessment problem is introduced.

The six workflows are:

- medication-history uncertainty, including delirium and a later collateral list;
- acute heart-failure decompensation, diuresis, and medication adjustment;
- endocarditis treated with outpatient parenteral antibiotics;
- kidney transplant with cytomegalovirus treatment and immunosuppression changes;
- hip fracture with interruption and resumption of anticoagulation;
- gastrointestinal bleeding with anticoagulation holds and restart decisions.

Generation uses the same terminology, regimen, validation, and error-injection steps as the balanced set. The source documents stay in [data/seed_cases/](data/seed_cases/README.md). The study charts are [data/case_sets/seed_guided/README.md](data/case_sets/seed_guided/README.md).

## How each case is structured

Every study case is written as a hospital chart, in this order:

```text
Patient overview
        ↓
Reason for hospitalization
        ↓
Relevant medical history / problem list
        ↓
Hospital course
        ↓
Admission vitals and laboratories
        ↓
Discharge / most-recent clinical status
        ↓
Home medications
        ↓
Medications used during hospitalization
        ↓
Discharge medications
        ↓
Medication reconciliation
        ↓
Monitoring and follow-up
        ↓
Discharge instructions
        ↓
Imaging / consultations / procedures / other context
```

| Case section | What the clinician should learn from it |
| --- | --- |
| Patient overview | Demographic and admission context |
| Reason for hospitalization | Why hospital-level care occurred |
| Relevant medical history | Comorbidities needed to interpret the medications |
| Hospital course | Clinical trajectory and treatment decisions |
| Admission vs discharge status | Whether the transition is clinically coherent |
| Home medications | Pre-admission regimen |
| Inpatient medications | Continuation, starts, substitutions, holds, and hospital-only therapy |
| Discharge medications | Outpatient regimen as presented to the resident |
| Medication reconciliation | History source, participation, and pharmacist review |
| Monitoring and follow-up | Transition-of-care requirements |
| Other clinical information | Imaging, procedures, consultations, and return precautions |

Read the medication lists against the course and the follow-up. The assessment problem is not always inside the list.

## How medication transitions are represented

```text
Home regimen
    ↓
Hospitalization
    ├── continued
    ├── temporarily held
    ├── substituted
    ├── discontinued
    ├── newly started
    └── hospital-only therapy
    ↓
Discharge regimen
    +
monitoring
    +
follow-up
    +
restart / pending decisions
```

A problem can sit in the medication list itself, or in the plan around that list. Monitoring, supply, a restart, follow-up, or a drug that should stay in the hospital can each be the issue. A clinic appointment is not the same thing as a laboratory task. An anticoagulation clinic visit can be present while the INR check itself is missing.

An RxNorm product and a clinical regimen are different objects. The product identifies a concept, a strength, and a dose form. The regimen is the order a clinician would read: what was given, by which route, how often, why, and whether it continues after discharge. The generator does not treat product strength as the administered dose and does not assume once daily.

A synthetic medication entry is:

```text
RxNorm concept
+ profile or archetype medication role
+ dose
+ route
+ frequency
+ indication
+ temporal state
= synthetic clinical medication entry
```

Curated regimens live in [data/bootstrap/medication_regimens.json](data/bootstrap/medication_regimens.json). If a real medication has no curated regimen, generation fails rather than inventing a dose. Citations are investigator provenance. They are not printed into the resident chart as reassurance that a dose is standard or correct.

Temporal states used on the study cases include pre-existing home therapy, started during the hospitalization, continued at discharge, temporarily held, hospital-only, discontinued, formulary substitution with home therapy resumed on the clean discharge list, new at discharge, and a pending restart or start decision. Hospital-only drugs such as correctional insulin, prophylactic enoxaparin, and a proton-pump inhibitor started for an acute bleed are described in ordinary clinical language. The investigator record keeps the expected discharge state. That record is not copied into the resident indication.

## What varies across cases

Cases are meant to differ in the clinical situation:

- diagnosis or archetype
- presentation and symptoms
- clinical trajectory
- relevant past history
- medication regimen
- inpatient medication changes
- laboratory findings
- imaging, procedures, or consultations
- discharge clinical status
- monitoring and follow-up
- disposition, when the profile calls for a change from the patient's baseline living situation

## What does not count as meaningful case diversity

Two cases are not treated as clinically distinct merely because they differ in age, sex, random seed, an exact laboratory number, an exact vital sign, the case identifier, or which discrepancy was later introduced. The diversity audit ignores those fields and compares the clean clinical structure. Exact duplicate fingerprints are rejected. Similarity of 0.85 or higher is rejected. Similarity from 0.70 to 0.85 is reported as a warning, not as a rejection. A warning means two charts share clinical structure. It does not mean they failed clinician review, because that review has not happened yet.

On the current balanced set the closest clean-case pair is VAL-717 and VAL-719, similarity 0.74, with one warning and no exact duplicates. On the current seed-guided set the closest pair is VAL-805 and VAL-807, similarity 0.79, with seven warnings and no exact duplicates. Those figures describe structure. They are not a claim of pedagogical or clinical validity.

## Medication-reconciliation problems represented

Each error-bearing case is built around one medication-reconciliation or transition-of-care problem. Clean controls are included so a reviewer cannot assume every chart is wrong. This page does not say which case is which. The case-set overviews do not either. The answer key is an investigator file.

### Family 1 — the regimen itself

The discharge regimen does not match the intended plan. Examples:

- a medication that should continue is missing
- a medication that should have stopped is still listed
- the dose does not match the rest of the chart
- the route does not match the formulation
- the frequency does not match the regimen
- a same-class substitute appears without a documented reason

The software identifiers are `f1_omission`, `f1_commission`, `f1_dose_mismatch`, `f1_route_mismatch`, `f1_frequency_mismatch`, and `f1_therapeutic_substitution`.

### Family 2 — the transition around the list

The medication list can look plausible while a required transition step is missing. Examples:

- required laboratory monitoring is not arranged
- a held medication has no restart plan
- the supply will not last until follow-up
- a hospital-only medication is still on the discharge list
- a temporary inpatient substitute was not changed back
- a pending medication decision has no follow-up

The software identifiers are `f2_monitoring_not_arranged`, `f2_held_med_no_restart_plan`, `f2_insufficient_supply`, `f2_hospital_only_continued`, `f2_inpatient_substitution_not_reverted`, and `f2_pending_decision_followup_missing`. Do not identify Family 2 only by comparing medication lists. The evidence is often in the course, the monitoring section, or the follow-up.

A required companion medication omitted (`f2_coprescription_omitted`) is defined conceptually and is not implemented. Freeze rejects that category rather than inventing a companion-drug rule (`not_yet_implementable`).

Definitions in clinical language are also in [docs/error_taxonomy.md](docs/error_taxonomy.md).

### Controls

A control has no introduced discrepancy. Residents are not told which identifiers are controls. Investigators use the answer key. Clinician review of a control asks whether the chart is plausible and whether any unintended medication problem is present.

## How clinicians should review these cases

Review is one reading of the complete case. Record all five ratings in that same pass. There is no separate plausibility stage and no second consensus stage. This review decides whether a chart is fit to use. It is not the later task in which a resident, blinded to the answer, says what is wrong.

### C1 — Clinical plausibility

Could this reasonably be an inpatient encounter? Consider the presentation, the diagnosis, the vital signs, the laboratories, the regimen, the hospital course, internal consistency, and the discharge plan.

### C2 — Intended assessment problem

Is the intended medication-reconciliation or transition-of-care problem actually present, and does it match its category? A control should contain none.

### C3 — Detectability

Could an internal-medicine resident identify the problem from the visible chart and say what should change, without the chart announcing the answer?

### C4 — No unintended clinically meaningful problem

Is there another clinically meaningful medication problem that could reasonably be read as a different answer? A second dose, frequency, route, hold, or monitoring problem can make the case unusable.

### C5 — Difficulty

How difficult is the case likely to be for the intended learner? This rating is advisory. Actual difficulty will later be estimated from resident performance.

Recommendations:

- **Accept.** The chart can be used for its assigned purpose, or as a control.
- **Revise.** The chart needs a stated correction before use. Do not silently edit a case after review has started. A revision after that point is a new freeze.
- **Exclude.** The chart should not be used, even if software checks passed.

C1 through C4 need to be acceptable before a case is used against its answer key. The worksheet instructions are also in [docs/clinical_validation.md](docs/clinical_validation.md). The per-case forms are in each clinician validation packet.

## What residents see later

After a chart is accepted, a resident study is a different task. The resident receives the blinded chart and records what, if anything, is wrong. That response is not a substitute for C1–C5, and a clinician rating is not a resident answer.

Blinded files for that later task are [data/case_sets/balanced/resident_validation_cases.json](data/case_sets/balanced/resident_validation_cases.json) and [data/case_sets/seed_guided/resident_validation_cases.json](data/case_sets/seed_guided/resident_validation_cases.json), with the matching empty resident worksheet. They omit the answer key, the batch plan, the manifest, and the investigator notes. The readable pages under `readable/cases/` are the same blinded charts in Markdown.

## Terminology and provenance

Terminology provenance validates concept identity. It does not establish that the choice is clinically appropriate for the synthetic patient.

| Source | What a stored identifier means |
| --- | --- |
| RxNorm | Medication concept, ingredient, strength, and dose form |
| LOINC | Laboratory observation identity |
| ICD-10-CM | Diagnosis concept |
| UCUM | Unit identity on a numeric result |
| Curated regimens and rules | A project decision, with a citation, about dose, route, frequency, temporal role, or a hard constraint |
| Resident seed documents | Unchanged design references under `data/seed_cases/resident_authored/` |
| Case blueprints | Archetype and profile definitions derived from those references |

A source-backed terminology concept is not automatically a clinically appropriate choice for a particular synthetic patient. Passing automated validation does not establish clinical validity. Human clinician validation remains required.

More detail is in [docs/provenance.md](docs/provenance.md).

## Clinical regimen assumptions in the current sets

These are the regimen choices used so the charts do not contain a second, accidental prescribing problem. They are not a claim that every similar patient should receive the same order.

- Apixaban for nonvalvular atrial fibrillation is 5 MG orally twice daily. Age is kept under 80 and weight above 60 kg so the chart does not meet two of the three labeled dose-reduction criteria. Reduced-dose apixaban is not used.
- Warfarin is 5 MG orally once daily. The investigator citation records that the dose is individualized to the INR. The resident chart does not say the dose is correct. INR monitoring is a laboratory task and is separate from the anticoagulation-clinic appointment. When the intended problem is missing INR monitoring, the clinic visit can remain and the INR task is removed. When missing INR monitoring is not the target, the chart includes a coherent INR plan.
- Enoxaparin in the postoperative profiles is hospital-only prophylaxis, 40 MG subcutaneously once daily from the 0.4 mL syringe, not a weight-based treatment bridge.
- Heart-failure beta blockers use metoprolol succinate extended release 25 MG once daily when that concept is selected, or metoprolol tartrate 25 MG twice daily when the stored concept is tartrate. Carvedilol immediate release is 6.25 MG twice daily. Spironolactone for straightforward heart failure is 25 MG once daily. Lisinopril is 10 MG once daily. Enalapril is 5 MG twice daily. Furosemide is 40 MG once daily.
- Ceftriaxone for adult endocarditis treated with outpatient parenteral therapy is 2000 MG intravenously once daily and is started in the hospital, not listed as a home medication.
- Azithromycin started for the current pneumonia is 250 MG orally once daily for the remaining course and is not a home medication.
- Insulin lispro, when used for inpatient glucose stabilization, is hospital-only. The dose is recorded as individualized.
- Tacrolimus maintenance is 1 MG orally every 12 hours. Mycophenolate mofetil for the kidney-transplant profiles is 1000 MG orally twice daily. Valganciclovir for cytomegalovirus treatment with preserved renal function is 900 MG orally twice daily.

The [clinician walkthrough](docs/clinician_walkthrough/README.md) uses a heart-failure teaching chart built with this regimen. That chart is not a study case.

## Artifacts

Each current case set has the same kinds of files. Clinicians rating cases start with the overview and the readable packet. Investigators use the key.

| File | Who uses it | Contains the answer? |
| --- | --- | --- |
| `README.md` | Clinicians and collaborators | No |
| `readable/all_cases.md` and `readable/cases/` | Anyone reading the charts | No |
| `readable/clinician_validation_packet.md` | Clinician validators | Yes, the intended issue for each case |
| `readable/clinical_validation_worksheet.csv` | Validators recording C1–C5 | No, until a reviewer fills it in |
| `resident_validation_cases.json` | Later blinded resident review | No |
| `investigator_answer_key.md` | Investigators | Yes |
| `batch_plan.json`, manifest, coverage, diversity report | Investigators and developers | The plan names the assigned target |

The internal pre-review QC note is [data/case_sets/investigator/clinical_qc_report.md](data/case_sets/investigator/clinical_qc_report.md). A descriptive comparison of the two sets, which does not rank them, is [data/case_sets/investigator/comparison/active_batch_comparison.md](data/case_sets/investigator/comparison/active_batch_comparison.md).

## Reproducibility

Freeze and export do not choose a batch by default. Pass the plan or the batch code.

```bash
clinical-case-generator freeze-validation-batch --plan data/case_sets/balanced/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V4 --output-dir data/case_sets/balanced

clinical-case-generator freeze-validation-batch --plan data/case_sets/seed_guided/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V3 --output-dir data/case_sets/seed_guided
```

Readable Markdown is regenerated from the frozen JSON without rewriting it:

```bash
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_BALANCED_V4 \
  --resident data/case_sets/balanced/resident_validation_cases.json
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_SEEDCASES_V3 \
  --resident data/case_sets/seed_guided/resident_validation_cases.json
python -m app.services.case_set_overview
```

Do not re-freeze a batch that has already been treated as immutable in order to change clinical content. After clinician review of these sets starts, a clinical correction should be a new batch code and a non-overlapping case-identifier range. The human-facing directories `data/case_sets/balanced/` and `data/case_sets/seed_guided/` can stay stable while the batch code inside the files changes.

The case-set overview pages are rendered from the manifest, the profiles, and the diversity report. Regenerate them with `python -m app.services.case_set_overview` after a new freeze. That renderer does not copy answer-key fields into the public case map.

## Worked teaching examples

[docs/clinician_walkthrough/README.md](docs/clinician_walkthrough/README.md) walks through one readable heart-failure chart, how the chart is assembled, how a medication transition is represented, how a clean chart differs from a chart with one assessment problem, what the software checks, and what the clinician still reviews. The teaching charts are not study cases.

## Limitations

- The cases are synthetic charts, not extracts from an electronic health record.
- The supported scenarios and archetypes are a bounded teaching set, not the range of inpatient medicine.
- Neither batch is prevalence-weighted.
- A resolved terminology code does not prove the charted dose or the hospitalization is clinically convincing.
- Only implemented constraints are enforced. Companion-drug omission is not implemented.
- Medication regimens are curated for these profiles. They are not a universal prescribing engine.
- Template narrative can still show regularities across cases.
- Automated uniqueness metrics do not by themselves establish pedagogical diversity.
- Clinician C1–C5 review is still required. Internal QC means ready for that review, not clinically validated.
- C5 is advisory. Actual difficulty requires later resident performance.
- There is no resident-review application in this repository. Review uses the Markdown packet and the worksheet.
- SNOMED CT and MIMIC-IV are not ingested. LOINC laboratory import requires credentials.

## Developer setup

Python 3.12 or newer is required. A PostgreSQL database and a LOINC account are required for a full terminology bootstrap. The application entry point is `clinical-case-generator`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
```

Set `DATABASE_URL`, `LOINC_USERNAME`, and `LOINC_PASSWORD` in `.env` before importing laboratories. The example database URL is `postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases`. Empty LOINC credentials raise an error. There is no generated laboratory fallback.

```bash
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
```

`db-init` applies migrations. It does not rewrite the committed case files. `pytest` rebuilds the database schema and will wipe local case rows. Re-run bootstrap and freeze after a full test session if you still need the database loaded. Exported JSON under `data/` is not stored only in the database.

Ordinary development cases, which are not part of either study set:

```bash
clinical-case-generator generate-synthetic-cases --count 3 --seed 42
clinical-case-generator validate-cases --case-id SYN-000001
```

Checks used before a change is considered complete:

```bash
pytest
ruff check .
mypy app
python scripts/check_docs.py
```

Further command detail is in [docs/developer_guide.md](docs/developer_guide.md). The directory map is in [docs/repository_structure.md](docs/repository_structure.md). Methods are in [docs/methods.md](docs/methods.md).

### Troubleshooting

- `clinical-case-generator: command not found` means the virtual environment is not active or the package was not installed editable.
- A connection refused on port 5432 means PostgreSQL is not running. Start it with `docker compose up -d` and confirm `DATABASE_URL`.
- Missing LOINC credentials stop laboratory import. They do not stop a checkout of the already frozen cases.
- `Frozen validation case ... cannot be overwritten` means that identifier is already frozen. Use a new plan rather than replacing it.
- Export or freeze without `--plan` or `--batch-code` exits with an error. There is no silent default batch.

## Historical datasets and provenance

Earlier frozen batches are retained under [data/archive/validation_sets/](data/archive/validation_sets/README.md) for reproducibility and provenance. They are not the current study set. The archive README is the place to see what each historical directory contains. The clinical narrative above does not depend on them.

Earlier generator snapshots, from before the current teaching charts, are stored under [docs/clinician_walkthrough/source_json/historical/](docs/clinician_walkthrough/source_json/historical/README.md). They are reproducibility records. The clinician walkthrough uses the readable teaching charts instead.

| Historical batch | Archive directory | Historical identifiers |
| --- | --- | --- |
| `CLINIPROOF_TAXONOMY_V1` | `data/archive/validation_sets/CLINIPROOF_TAXONOMY_V1` | historical VAL-201–VAL-224 |
| `CLINIPROOF_BALANCED_V2` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V2` | historical VAL-301–VAL-324 |
| `CLINIPROOF_BALANCED_V3` | `data/archive/validation_sets/CLINIPROOF_BALANCED_V3` | historical VAL-501–VAL-524 |
| `CLINIPROOF_SEEDCASES_V1` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V1` | historical VAL-401–VAL-424 |
| `CLINIPROOF_SEEDCASES_V2` | `data/archive/validation_sets/CLINIPROOF_SEEDCASES_V2` | historical VAL-601–VAL-624 |

Those files were not regenerated when the repository was reorganized. Do not send an archived packet as the current review set.

## Licensing

Terminology and dataset content is not bundled. RxNorm, DailyMed, LOINC, UCUM, ICD-10-CM, SNOMED CT, AccessGUDID, and MIMIC-IV each have their own license and access rules. LOINC requires a Regenstrief account. SNOMED CT and MIMIC-IV stay disabled until a future ingestion path exists.
