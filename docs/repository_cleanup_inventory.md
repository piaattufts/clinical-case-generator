# Repository cleanup inventory

Classification was made from directory purpose and from what the current VAL-801–VAL-824 study still needs. Git history keeps everything removed from this tree. The pre-cleanup tag is `repo-before-clinical-cleanup-2026-10`.

| Path | Purpose | Status before cleanup | Decision | Reason | Replacement |
| --- | --- | --- | --- | --- | --- |
| `data/case_sets/seed_guided/` excluding `CLEAN_BASE/` | Frozen `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824, including readable charts, manifest, and plan | Original source | KEEP_SOURCE | Immutable original seed-guided set, including planted-error variants | Unchanged path |
| `data/case_sets/seed_guided/CLEAN_BASE/` | Recovered pre-injection resident and evaluator JSON for VAL-801–VAL-824 | Copied byte-for-byte from `exports/clean_balanced_seed_set/` | KEEP_SOURCE | The next revision starts from clean cases, not from the planted-error freeze | This directory |
| `data/seed_cases/` | Resident-authored scenarios and archetypes used to build the seed-guided set | Source | KEEP_SOURCE | Required to understand and reproduce generation | Same path |
| `data/bootstrap/` | Scenarios, curated regimens, rule templates, terminology manifest | Source | KEEP_SOURCE | Required by the generator | Same path |
| `alembic/` | Database schema migrations | Source | KEEP_ACTIVE | Required to reproduce the database | Same path |
| `app/` core services | Generation, resident/evaluator representation, validation, terminology, Word export | Active code | KEEP_ACTIVE | Required to generate and check clean cases | Same path |
| `docs/clinical_feedback/reviewer_1/KO_Casebook_Validation.docx` | Reviewer 1 completed casebook | Copied byte-for-byte from the submitted KO file | KEEP_PROVENANCE | Original review; not edited | This path |
| `docs/clinical_feedback/reviewer_2/` | Reviewer 2 completed casebook | Copied byte-for-byte from the Alex file already in the tree | KEEP_PROVENANCE | Original review; not edited | This path |
| `docs/clinical_feedback/reviewer_comparison.csv` | Case-level comparison | Normalized from the two DOCX files | KEEP_PROVENANCE | One comparison table | This path |
| `docs/validation/CliniProof_Clinical_Validation_Template.docx` | Blank codebook | Byte-identical copy of the blank seed-guided casebook | KEEP_ACTIVE | Stable instrument for the next round | This path |
| `docs/methodology.md` | Current methods | New | KEEP_ACTIVE | Replaces competing round and version narratives | This path |
| `docs/provenance.md` | What terminologies do and do not establish | Existing, updated | KEEP_ACTIVE | Still the terminology provenance note | Same path |
| `docs/source_integrity.md` | SHA-256 of preserved sources | New | KEEP_PROVENANCE | Proves the cleanup did not rewrite sources | This path |
| `exports/current/` | Placeholder for the next reviewed package | Empty | KEEP_ACTIVE | No second revision yet | This path |
| `exports/clean_balanced_seed_set/` | Recovered clean charts for VAL-701–VAL-824 | Generated recovery export | REMOVE_GENERATED | VAL-801–VAL-824 copies now live in `CLEAN_BASE`. VAL-701–VAL-724 are not the current study | `CLEAN_BASE` for VAL-801–VAL-824 |
| `exports/ko_revised_cases_v1/` | First six-case revision package | Superseded | REMOVE_SUPERSEDED | Not the clean base and not the current review | Git history |
| `exports/ko_remaining_clean_cases_v1/` | Earlier clean-case packaging | Superseded | REMOVE_SUPERSEDED | Duplicate of later clean packaging | `CLEAN_BASE` |
| `exports/ko_clean_cases_for_review_v1/` | Set 2 preparation package | Superseded | REMOVE_SUPERSEDED | Working revision, not the clean source | `CLEAN_BASE` |
| `exports/ko_held_cases_v1/` | Held-case audit | Superseded | REMOVE_SUPERSEDED | Empty held list from an intermediate pass | Git history |
| `exports/ko_cycle2_revised_validation/` | Early cycle-2 extract | Superseded | REMOVE_SUPERSEDED | Intermediate working output | Reviewer DOCX and comparison CSV |
| `exports/ko_cycle2_revised_validation_v2/` | Second revision attempt | Superseded | REMOVE_SUPERSEDED | Intermediate working output | Git history |
| `exports/ko_cycle2_revised_validation_v3/` | Previous six-case canonical package | Superseded | REMOVE_SUPERSEDED | Revision output, not the clean base | `CLEAN_BASE` plus reviewer files |
| `exports/ko_cycle2_clean_validation/` | Earlier Set 2 codebook | Superseded | REMOVE_SUPERSEDED | Duplicate codebook | Template in `docs/validation/` |
| `exports/ko_cycle2_final_validation/` | Combined convenience copy | Superseded | REMOVE_SUPERSEDED | Not a source of truth | Git history |
| `exports/ko_round2_combined_validation_v4/` | Combined v4 package | Superseded working revision | REMOVE_SUPERSEDED | The user directed that this package not remain beside the clean base | `CLEAN_BASE`; second revision not yet done |
| `exports/clean_case_pilot/` and `exports/clean_case_pilot_v2/` | Pilot exports | Generated | REMOVE_GENERATED | Not the canonical clean base | `CLEAN_BASE` |
| `exports/word/` | Rendered case-set Word files | Generated | REMOVE_GENERATED | Convenience renders of frozen sets | Frozen JSON and readable Markdown |
| `data/case_sets/balanced/` | `CLINIPROOF_BALANCED_V4`, VAL-701–VAL-724 | Separate prospective set | REMOVE_SUPERSEDED | Not part of the current VAL-801–VAL-824 study | Git history |
| `data/case_sets/investigator/` | Dual-batch QC notes | Working QC | REMOVE_GENERATED | Describes sets that are no longer the current tree | Git history |
| `data/archive/validation_sets/` | Older freezes, VAL-201 through VAL-624 ranges | Archived | REMOVE_SUPERSEDED | No current study dependency; Git history retains them | Git history |
| `data/active_validation_sets.md` | Pointer that named two current sets | Out of date | REMOVE_SUPERSEDED | Replaced by the README source-of-truth table | `README.md` |
| `docs/methods.md`, `docs/clinical_validation.md`, `docs/repository_structure.md`, `docs/developer_guide.md`, `docs/error_taxonomy.md`, `docs/clinician_walkthrough/`, `docs/resident_review_package/` | Competing or historical narratives and the old blank package | Superseded as the public description | REMOVE_SUPERSEDED | One methodology and one codebook remain. The blank casebook was copied into `docs/validation/` first | `docs/methodology.md`, `docs/validation/` |
| `app/services/error_injection.py` | Experimental discrepancy injector | Imported by the generator for an optional flag | KEEP_ACTIVE | Removing it would break the generator import. It is not the current review workflow | Unchanged module |
| Revision-only services (`cycle2_*`, `round2_v4*`, `ko_review_sets.py`, and the revision-item modules) | Built the removed packages | Superseded | REMOVE_SUPERSEDED | No remaining package to generate | Git history |
