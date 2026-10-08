# Provenance for CLINIPROOF_SEEDCASES_V4

This batch is additive. `CLINIPROOF_SEEDCASES_V3` (VAL-801–VAL-824), its clean base, and the completed clinician reviews were not rewritten to produce it.

## What the resident documents contributed

Six resident-authored files in `data/seed_cases/resident_authored/` were read as design inputs. The reusable structure, not the source patient, is what entered the blueprint `seed-archetypes-v1`.

| Source document | Archetype | Reusable structure that was kept | Source-patient detail that was not copied |
| --- | --- | --- | --- |
| `Bad_Med_Rec_Case.docx` | `MEDREC_UNCERTAIN_HISTORY` | Inpatient medicine admission for an acute confusional state, an incomplete medication history, later collateral verification, and a discharge plan that has to separate verified medicines from stopped ones | Age, sex, language, neighborhood, family availability, and the source laboratory series |
| `Heart_Failure_Case.docx` | `HF_DECOMPENSATION` | Congestion, a diuretic course, weight and laboratory trajectory, and medicines that may be held and then reconsidered at discharge | The source weight series, the copied brand combination, and the exact laboratory numbers |
| `OPAT_Case.docx` | `OPAT_ENDOCARDITIS` | Infective endocarditis treated with a defined outpatient parenteral course, recurring laboratory monitoring, and infectious-diseases follow-up | Organism name, valve surgery year, and the copied imaging report |
| `Post_transplant_case.docx` | `TRANSPLANT_CMV` | Kidney transplant, immunosuppression, cytomegalovirus treatment, a temporary hold, antiviral conversion, and specialty follow-up | The source viral-load series and the identifiable transplant chronology |
| `Post-Op_Case.docx` | `POSTOP_ANTICOAGULATION` | Hip-fracture repair with anticoagulation interrupted and resumed, an INR trajectory, and rehabilitation follow-up | Valve brand, opioid taper, and the copied hemoglobin series |
| `Sepsis_AMA_Case.docx` | `GI_BLEED_ACUTE_CHANGE` | Gastrointestinal bleeding, anticoagulation held, and a discharge decision about restart. The later febrile hypotensive course is documented in the source and omitted here, because an unstable patient would make a discharge medication decision uninterpretable | Source age, sex, and the later sepsis overlay |

Four profiles already defined for each archetype differ in comorbidity, home regimen, hospital course, holds or starts, monitoring, and follow-up. Age, sex, the VAL identifier, and the random seed are not treated as that diversity. The diversity audit on the clean cases found 0 exact duplicate fingerprints and 0 near-duplicate rejections.

## Generation path

```text
resident source case
        ↓
reusable archetype in data/seed_cases/blueprints/archetypes.json
        ↓
four structured profiles
        ↓
terminology-backed concepts and curated regimens
        ↓
synthetic encounter
        ↓
clean-case machine validation
        ↓
pre-specified assessment category from batch_plan.json
        ↓
freeze as VAL-901–VAL-924
```

`generation_strategy` is `resident_seed_guided`. The master seed is `20261008`. Case seeds are derived from that master seed, the sequence, the archetype, and the profile. Sequences are 2501–2524, which produce internal `SYN-002501`–`SYN-002524` identifiers. Those identifiers are not the study ids.

Medication identity is an RxNorm RXCUI. Laboratory identity is a LOINC code. Units are UCUM. Diagnosis text is the ICD-10-CM description stored for the code the official source returned. Dose, route, and frequency come from `data/bootstrap/medication_regimens.json`. A missing curated regimen fails generation rather than inventing a dose. The freeze call disabled OpenAI, so narrative sentences are the template built from the selected facts.

The batch plan, written before generation, assigns four clean controls (VAL-901, VAL-905, VAL-909, VAL-913) and twenty error-bearing cases. Each error-bearing case has one pre-specified Family 1 or Family 2 category. The generator did not substitute a different category. Clean validation passed for every case before injection, and post-injection validation passed for every frozen case.

## What each export is allowed to show

The resident JSON and the readable case pages omit the answer key, the error category, the clean expected state, the source filename, and the reference discharge plan. The investigator answer key and the clinician validation packet retain the assigned category for scoring. The blank worksheet has no ratings.

A stored RXCUI, LOINC code, or ICD-10-CM code identifies a concept. It does not establish that the chart is clinically appropriate. Machine validation is not clinician acceptance. No case in this batch has been clinically validated.
