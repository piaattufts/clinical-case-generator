# Repository structure

```text
README.md                    clinician-facing project overview
app/                         application and generation code
data/case_sets/balanced/     current balanced structured case set
data/case_sets/seed_guided/  current resident-seed-guided case set
data/case_sets/investigator/ internal QC and the comparison of the two sets
data/seed_cases/             resident source documents and derived archetypes
data/bootstrap/              terminology manifest, scenarios, and curated regimens
data/archive/validation_sets/ earlier frozen batches, kept for provenance
docs/                        methods, validation, provenance, and this map
docs/clinician_walkthrough/  teaching snapshots, separate from the study cases
tests/                       automated tests
scripts/                     documentation checks
```

## Source of truth versus generated files

| Kind | Examples | How to treat them |
| --- | --- | --- |
| Source of truth | `app/`, `data/bootstrap/`, `data/seed_cases/blueprints/`, `data/seed_cases/resident_authored/`, each batch `batch_plan.json`, `data/validation_registry.json` | Edit these to change future generation. Do not edit a frozen plan in order to change cases that were already frozen. |
| Generated study artifacts | resident JSON, investigator JSON, manifests, coverage reports, diversity reports, readable packets | Produced by freeze, export, and `python -m app.services.readable_packets`. |
| Case-set overviews | `data/case_sets/balanced/README.md`, `data/case_sets/seed_guided/README.md` | Rendered by `python -m app.services.case_set_overview` from the manifest, profiles, and diversity report. |
| Authoritative docs | `docs/*.md`, root `README.md`, `data/README.md` | Describe the study. Manifest counts are checked by `scripts/check_docs.py`. |

The two directories under `data/case_sets/` are the prospective review sets. Earlier freezes live under `data/archive/validation_sets/`. Their own README explains the directories. The human-facing case-set paths stay stable when a batch code inside the files changes.
