# Repository structure

```text
README.md                         project overview for clinicians and developers
app/services/generation.py        default clean-case generator
app/services/resident_case.py    resident chart versus hidden reference plan
app/services/validation.py        structural and coherence checks
app/services/error_injection.py   experimental chart discrepancies; not the default path
app/services/clean_set_recovery.py  resident/evaluator split from frozen clean sources
app/services/ko_review_sets.py    Cycle 2 review copies for VAL-801–VAL-824
app/services/validation_batch.py  freeze and export of historical VAL batches
exports/clean_balanced_seed_set/  recovered 48-slot export; not the Cycle 2 review handout
exports/ko_revised_cases_v1/      six revised VAL-801–VAL-824 cases and their review document
exports/ko_remaining_clean_cases_v1/  eighteen fresh-review cases and their review document
exports/ko_held_cases_v1/         held audit; currently zero held cases
tests/test_ko_review_sets.py      Cycle 2 package checks
data/case_sets/balanced/          frozen CLINIPROOF_BALANCED_V4 source, not the resident handout
data/case_sets/seed_guided/       frozen CLINIPROOF_SEEDCASES_V3 source, not the resident handout
data/case_sets/investigator/      internal QC of those frozen batches
data/seed_cases/                  resident source documents and derived archetypes
data/bootstrap/                   terminology manifest, scenarios, and curated regimens
data/archive/validation_sets/     earlier frozen batches, kept for provenance
docs/                             methods, validation, provenance, and this map
docs/clinician_walkthrough/       teaching charts, separate from the study cases
tests/test_clean_resident_case.py clean generation hides the reference
tests/test_clean_set_recovery.py  recovery does not modify frozen resident exports
scripts/                          documentation checks
```

## Source of truth versus generated files

| Kind | Examples | How to treat them |
| --- | --- | --- |
| Source of truth | `app/`, `data/bootstrap/`, `data/seed_cases/blueprints/`, `data/seed_cases/resident_authored/`, each batch `batch_plan.json`, `data/validation_registry.json` | Edit these to change future generation. Do not edit a frozen plan in order to change cases that were already frozen. |
| Generated study artifacts | resident JSON, investigator JSON, manifests, coverage reports, diversity reports, readable packets | Produced by freeze, export, and `python -m app.services.readable_packets`. |
| Case-set overviews | `data/case_sets/balanced/README.md`, `data/case_sets/seed_guided/README.md` | Rendered by `python -m app.services.case_set_overview` from the manifest, profiles, and diversity report. |
| Authoritative docs | `docs/*.md`, root `README.md`, `data/README.md` | Describe the study. Manifest counts are checked by `scripts/check_docs.py`. |

`data/case_sets/balanced/` and `data/case_sets/seed_guided/` are the frozen source batches. Historical validation artifacts are retained for provenance and reproducibility. They should not be used as the current resident-facing study set. The recovered 48-slot export is `exports/clean_balanced_seed_set/`. Clinical Revision Cycle 2 review copies for VAL-801–VAL-824 are `exports/ko_revised_cases_v1/` and `exports/ko_remaining_clean_cases_v1/`. The held audit at `exports/ko_held_cases_v1/AUDIT.md` currently records zero held cases. Earlier freezes live under `data/archive/validation_sets/`.
