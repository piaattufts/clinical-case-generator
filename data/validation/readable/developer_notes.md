# CliniProof Implementation Notes for Clinical Informatics and AI Engineering

This note assumes you understand software engineering and may not have a clinical training background. It translates the medical objective into the modules that implement it.

It explains **mechanisms**. It does **not** map any frozen `VAL-201`–`VAL-224` identifier to a hidden assessment target. That mapping exists only in investigator-only files.

Status: machine-validated synthetic resident-review cases pending clinician validation.

## Clinical objective

Hospitals reconcile medications at admission and discharge so that intended home therapy is neither dropped nor continued unsafely, and so that required monitoring and follow-up actually occur.

CliniProof builds **synthetic** inpatient charts for that task. Each assessment item has a **known target** chosen before generation, not discovered afterwards by a model. Residents see a chart. Investigators see the target. Human clinicians still decide whether the chart is believable enough to use.

## Why canonical vocabularies are used

If the case said only “a heart-failure pill,” reviewers could not tell which product was meant, and software could not check rules. Official vocabularies give citable identifiers:

- **RxNorm (RXCUI)** for medications
- **ICD-10-CM** for diagnoses
- **LOINC** for laboratory *tests*
- **UCUM** for units

Those identifiers are stored only after an official service returns them, with provenance (`source_system`, `source_version`, `retrieved_at`). The generator never invents a code. SNOMED CT is not ingested here; SNOMED fields stay empty rather than being fabricated.

## Source-backed versus synthetic

| Layer | Meaning |
| --- | --- |
| Source-backed concept | The *type* of thing (warfarin as an RXCUI, creatinine as a LOINC) came from an official terminology |
| Synthetic value | The *patient-specific number or story* (age 72, creatinine 1.3, the HPI sentences) was generated |
| Deterministic assessment change | After the clean chart passed checks, software applied one planned edit |

A source-backed warfarin concept is **not** evidence that a real patient was taking warfarin.

## Scenario structure

`data/bootstrap/scenarios.json` holds teaching skeletons: specialty, age band, search phrases for diagnoses, symptoms, medications, labs, and which canonical assessment categories are allowed. Matching happens against **already bootstrapped** `ref_*` rows (`app/services/bootstrap.py`), not against live free text.

## Clean-case concept

Generation (`app/services/generation.py`) first builds a **clean** structured encounter: demographics, presentation, medications in three contexts (home, inpatient, discharge), labs, vitals, notes, monitoring, follow-up, instructions. “Clean” means the chart should not already contain the assessment target that the plan might later introduce.

A small rules engine (`app/services/rules.py`) applies only conditionals that have attached DailyMed or RxClass evidence. There are few such rules. They are not a complete specialty guideline.

## Family 1 versus Family 2

Identifiers live in `app/services/error_taxonomy.py`.

**Family 1 (`family_1`)** — the discharge *list* is wrong relative to intended continuation.

| Clinical meaning | Identifier |
| --- | --- |
| Medication omitted at discharge | `f1_omission` |
| Medication inappropriately added or continued | `f1_commission` |
| Unexplained dose discrepancy | `f1_dose_mismatch` |
| Unexplained route discrepancy | `f1_route_mismatch` |
| Unexplained frequency discrepancy | `f1_frequency_mismatch` |
| Unexplained therapeutic substitution | `f1_therapeutic_substitution` |

**Family 2 (`family_2`)** — a required *transition action* is missing; the continued-drug identity may be unchanged.

| Clinical meaning | Identifier |
| --- | --- |
| Required monitoring not arranged | `f2_monitoring_not_arranged` |
| Held medication without a restart plan | `f2_held_med_no_restart_plan` |
| Insufficient medication supply | `f2_insufficient_supply` |
| Hospital-only medication continued after discharge | `f2_hospital_only_continued` |
| Temporary inpatient substitution not addressed at discharge | `f2_inpatient_substitution_not_reverted` |
| Follow-up missing for an unresolved treatment decision | `f2_pending_decision_followup_missing` |
| Required companion medication omitted | `f2_coprescription_omitted` (specified, `not_yet_implementable`) |

**Held medication without restart plan** means the original medication is intentionally stopped during hospitalization for a legitimate temporary reason, but the discharge documentation does not tell the patient or outpatient clinician when or under what conditions it should be resumed. That maps to `f2_held_med_no_restart_plan`.

**Required monitoring not arranged** means, for example, warfarin continues at discharge but outpatient INR monitoring was not scheduled. That maps to `f2_monitoring_not_arranged`. The medication row stays; the monitoring record is what changes.

Do not implement Family 2 detection as “diff the three medication lists.”

## Eligibility, injection, and no fallback

The freeze plan names `error_family` and `error_category` **before** generation (`data/validation/batch_plan.json`).

`app/services/error_taxonomy.py` decides whether the clean case is **eligible** for that category (for example, there is a continued discharge drug to omit, or a monitoring-dependency rule matches).

`app/services/error_injection.py` then applies the exact edit, or skips injection for a clean control (`none`).

If the category is unknown, ineligible, or `not_yet_implementable`, freeze **aborts**. It does not pick a different error. An LLM never chooses the category.

## Clean state and injected state

The investigator answer key stores both:

- **Clean expected state** — what the field was after clean validation (for example, the omitted drug `present` on the discharge list)
- **Injected state** — what residents see after the edit (for example, `absent`)

Residents must not receive these fields. The readable investigator packet is the human view of the same concealed specification.

## Machine validation

`app/services/validation.py` and freeze-time checks in `app/services/validation_batch.py` cover structure, terminology integrity, implemented rules, category eligibility, the expected state transition, answer-key consistency, isolation of a second target, and leak checks on the resident export.

They do **not** establish clinical validity.

## Resident blinding

The resident JSON omits answer-key objects, internal `SYN-*` generation identifiers, family/category fields, trigger metadata, and clean/injected state. Readable files `all_cases.md`, `plausibility_only_packet.md`, and `cases/VAL-*.md` are derived only from that blinded export.

## Freeze immutability and provenance

Frozen `CLINIPROOF_TAXONOMY_V1` files under `data/validation/` are the study source of truth. Regenerating live terminology from APIs is **not** expected to reproduce bit-identical JSON. Readable Markdown is allowed to be regenerated from those frozen files; the frozen files themselves must not be rewritten to “improve” clinical content.

Each frozen assignment records scenario, seed, family, category, source-version snapshots, and validation statuses in the investigator key and manifest.

## Optional narrative LLM

`app/openai/narrative.py` may reword admission prose from already chosen names. It is not a case generator. The committed freeze used templates only.

## Reproducing the pipeline (operators)

```bash
clinical-case-generator db-init
clinical-case-generator bootstrap-reference-data
clinical-case-generator freeze-validation-batch
clinical-case-generator export-validation-batch
python scripts/build_readable_validation_packets.py
```

Do not re-freeze expecting to replace `VAL-201`–`VAL-224`. To refresh clinician-facing Markdown only, run the readable-packet script.
