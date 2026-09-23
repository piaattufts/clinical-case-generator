# Resident-seed-guided set (`CLINIPROOF_SEEDCASES_V3`)

**Status: active prospective validation set, pending human clinician validation.**

This directory is one of the two current prospective datasets. The other is [`../validation_balanced_v4/`](../validation_balanced_v4/README.md). The resident DOCX files are design references, not study charts. Historical seed freezes are not the current study set.

## Batch identity

| Item | Value |
| --- | --- |
| Batch code | `CLINIPROOF_SEEDCASES_V3` |
| Generation strategy | `resident_seed_guided` |
| VAL range | VAL-801–VAL-824 |
| Case count | 24 |
| Master seed | `20260926` |
| Sequences | 1501–1524 |
| Case seed | `{master_seed}:{sequence}:{scenario}:{clinical_profile}` |
| Status | Ready for human clinician validation. Not clinically validated. |

`CLINIPROOF_SEEDCASES_V3` supersedes the immutable predecessors `CLINIPROOF_SEEDCASES_V2` (VAL-601–VAL-624, [`../validation_seedcases_v2/`](../validation_seedcases_v2/README.md)) and `CLINIPROOF_SEEDCASES_V1` (VAL-401–VAL-424, [`../validation_seedcases/`](../validation_seedcases/README.md)). Those directories were not edited, and the resident DOCX files were not edited to change these charts. This batch had not been sent for clinician ratings, so the final pre-validation QC was applied here in place. That QC includes the structured apixaban hold on VAL-823. The batch code did not change. After clinician review starts, further clinical corrections should be a new batch code.

## Purpose

The seed-guided set asks whether charts built from expert clinical examples, rather than from a balanced scenario grid, can still be synthetic, terminology-backed, and limited to one assigned discrepancy. The goal is workflow realism: incomplete histories, diuresis, OPAT, transplant infection, postoperative anticoagulation, and a gastrointestinal bleed with an unresolved anticoagulation decision. The six source documents do not set disease prevalence, medication prevalence, or error prevalence.

## Generation method

The path is:

```text
resident-authored clinical example
→ structured clinical archetype
→ four clinically distinct profiles
→ new synthetic encounter
→ terminology resolution
→ clean-case validation
→ diversity audit
→ error eligibility
→ one controlled discrepancy, or a clean control
→ final validation
```

Generation reads [`../seed_cases/blueprints/archetypes.json`](../seed_cases/blueprints/archetypes.json). It does not parse the DOCX files at freeze time. Exact original patient details are not reused as study patients. Age, sex, weight, vital signs, and laboratory numbers are new draws. Medication concepts are resolved through RxNorm. Dose, route, frequency, indication, and temporal state come from the same curated regimen layer used by the balanced set.

The clean case is validated before injection. Exact duplicate fingerprints are rejected. Similarity of 0.85 or higher is rejected. Similarity from 0.70 to 0.85 is a warning. The audit looks at within-archetype and across-archetype structure, not at the planted error.

Resident text does not say “clean case,” “planted error,” or “seed document,” and it does not announce the expected disposition. Investigator `decision_reason` keeps hospital-only and hold rationale.

## Six archetypes

Each archetype has four profiles. Four was chosen so each family could carry more than one error type and still include a control, without turning six examples into a prevalence sample. Full abstraction notes are in [`../seed_cases/README.md`](../seed_cases/README.md).

1. `MEDREC_UNCERTAIN_HISTORY` — medication-history uncertainty, including collateral history and a patient who cannot give a complete list. VAL-801–VAL-804.
2. `HF_DECOMPENSATION` — acute heart-failure management, diuresis, and medication holds that need a discharge plan. VAL-805–VAL-808.
3. `OPAT_ENDOCARDITIS` — endocarditis treated with outpatient parenteral therapy, including ceftriaxone 2 g IV once daily started during the hospitalization, a PICC, weekly laboratory monitoring, culture clearance, and an echocardiographic vegetation finding. VAL-809–VAL-812.
4. `TRANSPLANT_CMV` — kidney transplant, immunosuppression, and CMV treatment. VAL-813–VAL-816.
5. `POSTOP_ANTICOAGULATION` — postoperative hip fracture, warfarin, and prophylactic enoxaparin as a hospital-only medication. VAL-817–VAL-820.
6. `GI_BLEED_ACUTE_CHANGE` — gastrointestinal bleeding that is discharge-ready, with endoscopy context and an anticoagulation decision. The febrile hypotensive overlay in the source document is not copied. VAL-821–VAL-824.

VAL-823 (`GI_BLEED_PENDING_AC_DECISION`) is the unresolved restart case. The clean plan holds apixaban at discharge and arranges follow-up to resolve restart versus continued hold. The injected error is `f2_pending_decision_followup_missing`, so the resident chart keeps the held apixaban and the pending-decision language and omits that follow-up. Apixaban is not active on the discharge list.

## Batch composition

| Archetype | Cases |
| --- | ---: |
| Medication-history uncertainty | 4 |
| Heart-failure decompensation | 4 |
| OPAT / endocarditis | 4 |
| Transplant / CMV | 4 |
| Postoperative anticoagulation | 4 |
| Gastrointestinal bleeding | 4 |

## Error and control composition

| Group | Cases |
| --- | ---: |
| Family 1 list discrepancies | 7 |
| Family 2 transition-of-care gaps | 13 |
| Clean controls | 4 |
| Total | 24 |

Family 1 in this batch: omission 3, commission 1, dose mismatch 2, therapeutic substitution 1. There is no route or frequency mismatch in this batch.

Family 2 in this batch: monitoring not arranged 1, held medication without a restart plan 3, insufficient supply 3, hospital-only medication continued 2, pending-decision follow-up missing 4. There is no inpatient-substitution case in this batch.

`f2_coprescription_omitted` is not implemented and is not assigned. Counts come from [`coverage_report.md`](coverage_report.md) and the manifest.

## Diversity results

Source: [`diversity_report.md`](diversity_report.md). Measured on the clean case.

| Result | Value |
| --- | --- |
| Unique profiles | 24 |
| Exact duplicate fingerprints | 0 |
| Near-duplicate rejections (≥ 0.85) | 0 |
| Similarity warnings (0.70–0.85) | 7 |
| Closest pair | VAL-805 vs VAL-807, similarity 0.79 |

The warnings are pairs inside the same archetype that share a diagnosis and parts of the medication list while differing in profile, symptoms, hospital course, or follow-up. They were not rejected. They are listed in the diversity report so a reviewer can see the residual similarity.

## Clinical QC

These checks are internal. They are not clinician validation.

Automated review covers curated regimens, ceftriaxone as intravenous 2 g and not a home medication, temporal roles, endocarditis culture chronology, echo findings that describe an imaging finding rather than a treatment-course sentence, living situation labeled as baseline when disposition leaves home, and single-error isolation. The case-level table is [`../clinical_qc_report.md`](../clinical_qc_report.md). A pass means ready for human C1–C5 review.

Warfarin was checked against the answer key rather than by adding monitoring to every case:

| VAL | Warfarin at discharge | Structured INR monitoring | Anticoagulation-clinic follow-up | Intended category | Coherent |
| --- | --- | --- | --- | --- | --- |
| VAL-817 | yes | no | yes | `f2_monitoring_not_arranged` | yes |
| VAL-818 | no (omitted) | yes | orthopedic follow-up that also names anticoagulation | `f1_omission` | yes |
| VAL-819 | yes | yes | yes | `f2_insufficient_supply` | yes |
| VAL-820 | yes | yes | no; follow-up is orthopedics | `f2_hospital_only_continued` | yes |

VAL-817 keeps the clinic visit and removes the INR task, which is the assigned gap. VAL-818 keeps monitoring as evidence that warfarin was supposed to continue. VAL-820’s target is hospital-only enoxaparin left on the discharge list, so the INR task stays.

## File index

| File | What it is | Who should open it |
| --- | --- | --- |
| [`batch_plan.json`](batch_plan.json) | Assignment source | Developers |
| [`resident_validation_cases.json`](resident_validation_cases.json) | Blinded resident export | Residents |
| [`investigator_answer_key.json`](investigator_answer_key.json) | Concealed targets and clean state, including `decision_reason` | Investigators only |
| [`investigator_answer_key.md`](investigator_answer_key.md) | Readable answer key | Investigators only |
| [`validation_manifest.json`](validation_manifest.json) | Identity, seeds, and terminology snapshot | Reproducibility |
| [`coverage_report.md`](coverage_report.md) | Archetype and category counts | Investigators |
| [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md) | Profile grid | Investigators |
| [`diversity_report.md`](diversity_report.md) | Clean-case uniqueness | Investigators |
| [`resident_review_worksheet.csv`](resident_review_worksheet.csv) | Later resident-study worksheet | Study staff, after acceptance |
| [`resident_review_schema.json`](resident_review_schema.json) | Worksheet schema | Developers |
| [`readable/all_cases.md`](readable/all_cases.md) | Resident-safe charts | Residents |
| [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) | Charts plus intended targets | Clinician reviewers |
| [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv) | Empty C1–C5 rows | Clinician reviewers |
| [`readable/validation_rubric.md`](readable/validation_rubric.md) | Rubric without per-case answers | Reviewers |
| [`readable/README.md`](readable/README.md) | Readable-packet index | Anyone opening `readable/` |

## Reviewer workflow

Residents use [`readable/all_cases.md`](readable/all_cases.md) or the blinded JSON. They do not receive the DOCX filename, the archetype essay, or the answer key.

Clinicians use [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) and [`readable/clinical_validation_worksheet.csv`](readable/clinical_validation_worksheet.csv). The procedure is one C1–C5 pass, described in [`../../docs/clinical_validation.md`](../../docs/clinical_validation.md).

Investigators use the answer key. The seed documents under [`../seed_cases/resident_authored/`](../seed_cases/resident_authored/) explain provenance. They are not resident study materials.

## Regeneration

From a bootstrapped database, while this batch is still pre-validation:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V3
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_SEEDCASES_V3 \
  --resident data/validation_seedcases_v3/resident_validation_cases.json
```

Freeze reuses a VAL row when the identifier, seed, and scenario match. Changing clinical content means deleting this batch’s frozen rows first. Do not point `--plan` at an archived seed batch, and do not edit the DOCX files expecting the charts to change.

## Reproducibility

Blueprint version, archetype id, and source filename are stored on the investigator record. The manifest stores the master seed and terminology snapshot. Patient-level numbers are functions of the case seed. The answer key is deterministic. Narrative is template text.

## Limitations and status

Ready for human clinician validation. Not clinically validated. Six expert examples are not an epidemiologic sample. Four profiles per archetype are a design choice so that each workflow can carry different assigned errors. They do not estimate how often those workflows occur. Synthetic narrative can still look templated. A diversity warning means two clean charts are similar, not that the generator failed the freeze.
