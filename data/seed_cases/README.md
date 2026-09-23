# Resident-authored seed cases

Resident-authored documents in [`resident_authored/`](resident_authored/) are **clinical design references**. They are not study cases. They are not copied, paraphrased patient-by-patient, or frozen as VAL records.

Until clinicians finish review, generated records remain machine-validated synthetic resident-review cases pending clinician validation. Passing a diversity audit is not clinical validation.

## How a seed becomes a study case

1. A resident-authored DOCX is stored unchanged as an immutable source artifact.
2. A reviewer abstracts the **clinical structure** into a reusable archetype under [`blueprints/`](blueprints/).
3. Each archetype declares several named clinical profiles that differ before error injection.
4. Canonical medications, diagnoses, laboratories, and symptoms are resolved through the existing source-backed terminology pipeline (RxNorm, ICD-10-CM, LOINC, UCUM, and the curated rule layer). The DOCX does not supply official identifiers.
5. Ages, sexes, weights, vital numbers, and laboratory numbers remain synthetic draws from the case seed.
6. The clean case is validated and fingerprinted.
7. One CliniProof Family 1 or Family 2 error is injected, or the case is kept as a control.

Generation strategy for this path is `resident_seed_guided`. Frozen template batches keep `randomized_template`.

## Mapping

| Resident source | Archetype | Key preserved concepts | Details intentionally varied |
| --------------- | --------- | ---------------------- | ---------------------------- |
| `Bad_Med_Rec_Case.docx` | `MEDREC_UNCERTAIN_HISTORY` | Incomplete history, later collateral list, deprescribing vs unknown vs planted error, home services, PCP follow-up | Exact age/sex/language/neighborhood, specific family members, copied medication nicknames, source laboratory sequence |
| `Heart_Failure_Case.docx` | `HF_DECOMPENSATION` | Congestion, diuresis trajectory, weights/I&O, electrolyte and creatinine course, holds that need reassessment | Source weight series, copied GDMT brand combination, URI/dietary story, exact laboratory numbers |
| `OPAT_Case.docx` | `OPAT_ENDOCARDITIS` | Prolonged parenteral therapy, specified duration, recurring labs, infectious-disease follow-up, line precautions | Organism name, valve surgery year, colonoscopy finding, copied home-medication milligrams |
| `Post_transplant_case.docx` | `TRANSPLANT_CMV` | Transplant history, immunosuppression, infectious complication, temporary holds, antiviral conversion, specialty follow-up | Source tacrolimus goals as a hard rule, copied viral-load series, identifiable transplant chronology |
| `Post-Op_Case.docx` | `POSTOP_ANTICOAGULATION` | Perioperative anticoagulation interruption/resumption, INR trajectory, postoperative hemoglobin, rehabilitation follow-up | Mechanical-valve brand details, opioid taper milligrams, copied hemoglobin series, family availability |
| `Sepsis_AMA_Case.docx` | `GI_BLEED_ACUTE_CHANGE` | GI bleed, anticoagulation held, pending restart decision, PPI context | The seed’s later fever and hypotension are **not** copied into the study cases. An obviously unstable patient would make discharge medication reconciliation uninterpretable. Generated cases are discharge-ready after bleeding has settled. |

## GI-bleed seed handling

`GI_BLEED_ACUTE_CHANGE` is retained as an archetype because the seed is a useful example of changing clinical status. It is included in `CLINIPROOF_SEEDCASES_V1` only as **discharge-ready** variants (held anticoagulation, pending restart, hospital-only PPI, or an isolated list error). The febrile hypotensive overlay is documented here and omitted from generated charts.

## What blinded residents do not see

Resident-facing JSON and readable case pages do not include the DOCX filename, seed-author identity, archetype source document, original wording, or investigator answer-key fields. Investigator files may retain archetype ID, source filename, and blueprint version for provenance.

## Reproducibility

Blueprints are versioned (`blueprint_version` in [`blueprints/archetypes.json`](blueprints/archetypes.json)). Generation does not parse DOCX files at freeze time. Changing a DOCX without changing the blueprint does not change generated cases.
