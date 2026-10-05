# Methods traceability

The protocol document was not in the workspace. The "Protocol requirement" column quotes the implementation brief. The Notes column says where the protocol file still has to be checked. Validation or test points at an automated check when one exists.

| Protocol section | Protocol requirement | Implemented file / module | Validation / test | Notes |
| --- | --- | --- | --- | --- |
| Review questions | Five RQs on setting, scenario source, scenario content, performance measures, and trade-offs | `README.md`, `protocol/protocol_summary.md`, `protocol/extraction_codebook.md` | Manual reading | Wording is from the brief, not a transcription of the docx |
| Naturalistic definition | Intended setting, test house, or repeated everyday-use laboratory interaction | `protocol/eligibility_criteria.md`, `protocol/screening_manual.md` | `tests/test_screening.py` guards the laboratory exclusion note in the manual text used by reviewers | Code `N1` description says not to exclude on the word laboratory alone |
| Fidelity | Physical and contextual fidelity are extraction variables, not cutoffs | `protocol/extraction_codebook.md`, deployment columns `physical_fidelity*` and `contextual_fidelity*` | `tests/test_extraction.py` | No combined score is stored |
| Scenario definition | Explicit and implicit scenarios; the word scenario is not required | `scenario_explicitness` on `scenarios.csv` | Extraction validation | `UNCLEAR` is allowed |
| Databases | Scopus, Web of Science, IEEE, ACM, PubMed, PsycINFO, Google Scholar | `search/`, `src/inthewild_review/importers.py` | `tests/test_normalization.py` | Translations are unverified |
| Scopus query | Copy the final query exactly | `search/scopus.txt` | None, by design | Query text is absent until pasted |
| Sensitivity search | Scenario block stays out of the primary search | `search/scenario_sensitivity_searches/` | Manual | No sensitivity Boolean was invented |
| Platform terms | Keep Paro, robotic seal, Pleo, AIBO; do not add NAO or Pepper; avoid bare `home*` | `search/README.md` | Manual | Constraint text only |
| Known items | Named seed studies, not marked retrieved without evidence | `data/search_validation.csv`, `search_validation.py` | Report command | No DOIs added |
| Deduplication | Flag, do not delete; review conference/journal pairs | `deduplicate.py` | `tests/test_deduplication.py` | Removal needs `retained_record_id` |
| Title/abstract decisions | INCLUDE, MAYBE, EXCLUDE | `screening.py` | `tests/test_screening.py` | MAYBE is not collapsed in storage |
| Exclusion codes | N1 through N5 | `schemas.py`, screening manual | `tests/test_screening.py` | Prose is provisional |
| Calibration | Two reviewers, default 100, fixed seed, across years and sources | `calibration.py` | `tests/test_screening.py` | Seed stored in the sample file |
| Agreement | Percent agreement and kappa, three-way and collapsed; confusion matrix; disagreements | `agreement.py` | `tests/test_agreement.py` | Undefined kappa is reported, not invented |
| Full text | Embodied robot, human interaction, naturalistic or repeated, identifiable situation, extractable setting, duration, and structure | `screening.py` full-text validator | `tests/test_screening.py` | UNCLEAR cannot be treated as NO |
| Missing data | YES, NO, and NOT_REPORTED_OR_UNCLEAR | `validation.py` | `tests/test_extraction.py` | Blank tri-state cells fail |
| Levels | Publication, study, deployment, scenario | Extraction CSVs and foreign keys | `tests/test_extraction.py`, `tests/test_prisma.py` | Counts are separate |
| Scenario provenance | Multiple codes, including hybrid | `provenance_codes` | `tests/test_extraction.py` | Pipe-separated |
| Arnold and Scheutz | Touch, one-to-one competing interests, group decision-making | Scenario columns and `table_arnold_scheutz` | Synthesis writer | Absence of reporting is not coded as absence of the phenomenon |
| Measures | Constructs, instruments, observation, logs, interviews, qualitative methods, interaction and relationship outcomes | Deployment columns | Validation of tri-state measure flags | No quality score |
| Citation chasing | Backward and forward, same pipeline, no assumed eligibility | `citation_chasing.py` | Importer refuses bad directions | Stopping rule not coded |
| AI assistance | Optional, separate from human decisions, no key required | `ai_assist.py` | Suggestion writer does not open screening files for output | Standard commands do not call a model |
| Decision log | Changes after the protocol date are recorded | `protocol/decision_log.csv` | Manual | Setup rows are labeled provisional |
| PRISMA | Counts from data, not typed | `prisma.py` | `tests/test_prisma.py` | Zeros mean empty files |
| Descriptive synthesis | Tables 1–9 and the named cross-tabulations | `synthesis.py` | Completeness table has no total score | No meta-analysis |
| Reporting completeness | Proportions for reported fields, not a score | `table_reporting_completeness` | Built by `synthesize` | YES and NO both count as a definite report |

## Not yet traceable to the protocol file

Anything that was inside brackets in the docx. The inventory could not be made. See `docs/unresolved_protocol_decisions.md`.
