# Generation 2 — Synthea-grounded discharge reconciliation

This directory is a new case-generation method. It does not replace Generation 1.

Generation 1 remains in [seed_guided](../seed_guided/), including [CLEAN_BASE](../seed_guided/CLEAN_BASE/) and [REVISED](../seed_guided/REVISED/). Those files are not inputs to this cohort and are not rewritten by it.

Identifiers `G2-001` through `G2-024` are candidate identifiers. They are not frozen VAL study identifiers.

Each case is clean. There is no planted medication error and no completed discharge-medication list on the resident chart. The hidden reference is only in `cases/evaluator/`.

The cases have passed automated structural and clinical-sufficiency checks. They are not clinically validated.

| Path | Contents |
| --- | --- |
| [manifest.json](manifest.json) | Cohort provenance and eligibility counts |
| [selected_patients.json](selected_patients.json) | Synthea patient identifiers used in the final 24 |
| [scenario_assignment.json](scenario_assignment.json) | Family and variant for each case |
| [cases/resident](cases/resident) | Resident-facing charts |
| [cases/evaluator](cases/evaluator) | Charts plus the hidden reference |
| [readable/all_cases.md](readable/all_cases.md) | Rendered resident charts |
| [reports](reports) | Audits, including the Round 1 concern audit |

Rebuild with `python scripts/build_synthea_g2.py`. Raw Synthea FHIR is local and gitignored.
