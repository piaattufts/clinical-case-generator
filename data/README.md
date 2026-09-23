# Data index

This directory holds inputs, frozen study artifacts, and historical freezes.

| Path | Role |
| --- | --- |
| [`active_validation_sets.md`](active_validation_sets.md) | Where to open the two current prospective sets. |
| [`validation_balanced_v4/`](validation_balanced_v4/README.md) | Active balanced structured batch. |
| [`validation_seedcases_v3/`](validation_seedcases_v3/README.md) | Active resident-seed-guided batch. |
| [`validation_comparison/active_batch_comparison.md`](validation_comparison/active_batch_comparison.md) | Descriptive comparison of those two batches. |
| [`seed_cases/`](seed_cases/README.md) | Resident-authored design references and the archetypes derived from them. |
| [`bootstrap/`](bootstrap/) | Terminology manifest, scenario profiles, and curated medication regimens. These are generator inputs. |
| [`validation/`](validation/README.md) | Historical `CLINIPROOF_TAXONOMY_V1`. Not an active review set. |
| [`validation_balanced/`](validation_balanced/README.md), [`validation_seedcases/`](validation_seedcases/README.md), [`validation_balanced_v3/`](validation_balanced_v3/README.md), [`validation_seedcases_v2/`](validation_seedcases_v2/README.md) | Earlier prospective freezes kept for provenance. |
| [`clinical_qc_report.md`](clinical_qc_report.md) | Investigator-only internal QC of the active cases before clinician review. |

Generated artifacts include resident JSON, investigator keys, manifests, coverage reports, diversity reports, and `readable/` packets. They are produced by freeze and export. Curated inputs include the bootstrap files, seed documents, blueprints, and batch plans. Do not hand-edit a generated answer key to change a frozen case.
