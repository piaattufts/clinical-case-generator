# Clinical Case Generator / CliniProof

CliniProof builds synthetic inpatient charts for studying medication reconciliation. A reviewer reads one chart and decides whether the home, hospital, and discharge medications, monitoring, and follow-up fit the clinical story.

The research problem is that discharge reconciliation errors are common and hard to study with real charts. Real records are private, incomplete, and cannot be assigned a single known discrepancy. CliniProof produces charts with source-backed terminology, synthetic patient values, and either no intended reconciliation discrepancy or exactly one.

There are **two active prospective validation datasets**, totaling **48** cases. They use different generation strategies and are not merged. `CLINIPROOF_TAXONOMY_V1` is preserved as archived historical provenance and is **not** the current study set.

Automated checks cover structure, terminology identity, curated regimen constraints, and isolation of the intended discrepancy. They do not establish clinical plausibility. These cases are ready for human clinician validation. They are not clinically validated until C1–C5 review is complete.

## Current prospective validation datasets

### CLINIPROOF_BALANCED_V4

- 24 cases, VAL-701–VAL-724
- Generation strategy: balanced structured generation
- Status: pending clinician validation
- [Readable cases](data/validation_balanced_v4/readable/all_cases.md)
- [Clinician packet](data/validation_balanced_v4/readable/clinician_validation_packet.md)
- [Worksheet](data/validation_balanced_v4/readable/clinical_validation_worksheet.csv)
- [Diversity report](data/validation_balanced_v4/diversity_report.md)

`CLINIPROOF_BALANCED_V3` (VAL-501–VAL-524) remains frozen. This revision was created because that batch had already been declared immutable.

### CLINIPROOF_SEEDCASES_V3

- 24 cases, VAL-801–VAL-824
- Generation strategy: resident-seed-guided generation
- Six resident-derived archetype families: medication-history uncertainty, heart-failure decompensation, OPAT/endocarditis, transplant/CMV, postoperative anticoagulation, and gastrointestinal bleeding with an acute medication change
- Status: pending clinician validation
- [Readable cases](data/validation_seedcases_v3/readable/all_cases.md)
- [Clinician packet](data/validation_seedcases_v3/readable/clinician_validation_packet.md)
- [Worksheet](data/validation_seedcases_v3/readable/clinical_validation_worksheet.csv)
- [Diversity report](data/validation_seedcases_v3/diversity_report.md)

`CLINIPROOF_SEEDCASES_V2` (VAL-601–VAL-624) remains frozen. This revision was created because that batch had already been declared immutable.

## Historical datasets

`CLINIPROOF_TAXONOMY_V1` (VAL-201–VAL-224, [`data/validation/`](data/validation/)) is preserved for provenance. It is not an active prospective review set. It was superseded operationally by the two current prospective sets. It is not labeled invalid.

Also preserved, and not active: `CLINIPROOF_BALANCED_V2` (VAL-301–VAL-324), `CLINIPROOF_SEEDCASES_V1` (VAL-401–VAL-424), `CLINIPROOF_BALANCED_V3`, and `CLINIPROOF_SEEDCASES_V2`.

## How cases are generated

Both strategies build a clinically coherent clean case first. The generator resolves RxNorm, LOINC, ICD-10-CM, and UCUM identities, applies a separately curated medication regimen (dose, route, frequency, and temporal role are not copied from the product strength), validates the chart, and then either keeps a control or injects one predetermined discrepancy. Details are in [`docs/methods.md`](docs/methods.md).

## What is automated, and what still needs clinicians

Automated checks can reject broken structure, missing terminology provenance, impossible value/unit pairs, regimen conflicts, temporal-role contradictions, and a second mechanically detectable discrepancy. Clinicians still rate C1 clinical plausibility, C2 the intended assessment problem, C3 detectability, C4 absence of another meaningful problem, and C5 expected difficulty. That review is one pass. See [`docs/clinical_validation.md`](docs/clinical_validation.md).

## Where should I start?

| I want to… | Go to |
| --- | --- |
| Understand the project | [`README.md`](README.md) |
| Understand case-generation methodology | [`docs/methods.md`](docs/methods.md) |
| Review active case sets | [`data/active_validation_sets.md`](data/active_validation_sets.md) |
| Review balanced cases | [`data/validation_balanced_v4/readable/all_cases.md`](data/validation_balanced_v4/readable/all_cases.md) |
| Review seed-derived cases | [`data/validation_seedcases_v3/readable/all_cases.md`](data/validation_seedcases_v3/readable/all_cases.md) |
| Perform clinician C1–C5 review | [`docs/clinical_validation.md`](docs/clinical_validation.md) and the packet linked from [`data/active_validation_sets.md`](data/active_validation_sets.md) |
| Understand the error taxonomy | [`docs/error_taxonomy.md`](docs/error_taxonomy.md) |
| Understand terminology/provenance | [`docs/provenance.md`](docs/provenance.md) |
| Understand repository layout | [`docs/repository_structure.md`](docs/repository_structure.md) |
| Develop or modify the generator | [`docs/developer_guide.md`](docs/developer_guide.md) |

## Install and run

Requires Python 3.12+, Docker, and a LOINC account for laboratory import.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
docker compose up -d
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
```

Study commands take an explicit batch. There is no default study batch.

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v4/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V4
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V3
```

Setup, tests, and regeneration steps are in [`docs/developer_guide.md`](docs/developer_guide.md). The documentation index is [`docs/README.md`](docs/README.md).
