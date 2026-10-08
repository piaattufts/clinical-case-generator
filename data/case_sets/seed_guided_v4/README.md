# CLINIPROOF_SEEDCASES_V4

This directory is a new resident-seed-guided validation batch. It does not replace [the frozen CLINIPROOF_SEEDCASES_V3 set](../seed_guided/README.md) or the clean charts in [CLEAN_BASE](../seed_guided/CLEAN_BASE/README.md).

Batch: `CLINIPROOF_SEEDCASES_V4`
Cases: VAL-901–VAL-924
Number of cases: 24
Generation approach: Resident-seed-guided generation
Master seed: `20261008`
Blueprint: `seed-archetypes-v1` in [data/seed_cases/blueprints/archetypes.json](../../seed_cases/blueprints/archetypes.json)

The six resident-authored documents in [data/seed_cases/resident_authored/](../../seed_cases/resident_authored/) are design inputs. They were not copied into these charts. Each document supports one archetype, and each archetype has four clinically distinct profiles. The batch plan assigns four clean controls and twenty single, pre-specified discrepancies. A clean case was validated before any discrepancy was introduced. OpenAI was not used.

These files are machine-validated synthetic cases. They are not clinically validated.

Resident-facing charts are [resident_validation_cases.json](resident_validation_cases.json) and [readable/all_cases.md](readable/all_cases.md). The clinician packet, investigator key, and provenance notes are separate files and are not the resident chart.

| File | Role |
| --- | --- |
| [batch_plan.json](batch_plan.json) | Pre-specified VAL identifiers, profiles, and assessment categories |
| [resident_validation_cases.json](resident_validation_cases.json) | Resident-facing structured cases |
| [readable/all_cases.md](readable/all_cases.md) | Readable resident packet |
| [readable/clinician_validation_packet.md](readable/clinician_validation_packet.md) | Clinician validation packet |
| [readable/clinical_validation_worksheet.csv](readable/clinical_validation_worksheet.csv) | Blank clinical validation worksheet |
| [investigator_answer_key.json](investigator_answer_key.json) | Investigator answer key |
| [validation_manifest.json](validation_manifest.json) | Freeze manifest |
| [coverage_report.md](coverage_report.md) | Terminology coverage |
| [scenario_coverage_matrix.md](scenario_coverage_matrix.md) | Archetype coverage |
| [diversity_report.md](diversity_report.md) | Clean-case diversity, scored before error injection |
| [provenance.md](provenance.md) | How this batch was built and what it does not contain |
