# Technical source files

These files reproduce the teaching charts. They are not the clinician-facing case. Read [the heart-failure chart](../examples/clean_heart_failure_case.md) and the [walkthrough](../README.md) for the clinical content.

| File | Role |
| --- | --- |
| [teach-001-clean.json](teach-001-clean.json) | Structured source for TEACH-001, the clean chart |
| [teach-002-omission.json](teach-002-omission.json) | Structured source for TEACH-002, the resident-facing chart after one discharge medication was removed |
| [teach-002-investigator.json](teach-002-investigator.json) | Investigator record for TEACH-002. This file names the target. It is not part of the chart. |
| [historical/](historical/README.md) | Earlier generator snapshots, kept for reproducibility |

TEACH-001 and TEACH-002 were produced with the current case pipeline and the curated medication regimen. The generator case id is `SYN-009901`. The batch seed is `20260923`, the scenario is `HF_INPATIENT`, and the clinical profile is `HF_VOLUME_OVERLOAD`. Narrative text was generated from the structured facts without an external language model. TEACH-002 is that same case after the omission step. Neither identifier is a VAL study case.
