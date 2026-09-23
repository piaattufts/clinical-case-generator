# Resident-authored seed cases

Resident-authored documents in [`resident_authored/`](resident_authored/) are **clinical design references**. They were collected so the generator would have expert examples of discharge workflows that a balanced scenario grid does not cover by itself: an incomplete medication history, a heart-failure admission, endocarditis treated with outpatient parenteral therapy, a transplant infection, a hip fracture with anticoagulation, and a gastrointestinal bleed with a pending anticoagulation decision.

They are not study cases. They are not copied, paraphrased patient-by-patient, or frozen as VAL records. The six source files are preserved unchanged. They are abstracted into blueprints. Synthetic study cases are new patients. The six examples do not establish prevalence of diseases, medications, or errors, and exact original patient details are not reused as study records. Source-backed terminology is resolved separately from resident expertise.

The active study cases that use these archetypes are `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824, in [`../validation_seedcases_v3/`](../validation_seedcases_v3/README.md). Until clinicians finish review, those generated records remain machine-validated synthetic resident-review cases pending clinician validation. Passing a diversity audit is not clinical validation.

## Why the source cases are not an epidemiological sample

Six documents cannot estimate how often a problem occurs on a medicine service. They were chosen because each one shows a different reconciliation structure a resident might actually have to read. The active batch then builds four synthetic profiles from each structure so the study can assign different error categories, including controls, without treating the original documents as a population. Medication prevalence in the synthetic batch follows the archetype and the curated regimen, not the frequency of those drugs in the source files. Error prevalence follows the batch plan, not the number of mistakes in the source documents.

## How a seed becomes a study case

1. A resident-authored DOCX is stored unchanged as an immutable source artifact.
2. A reviewer abstracts the **clinical structure** into a reusable archetype under [`blueprints/`](blueprints/).
3. Each archetype declares several named clinical profiles that differ before error injection.
4. Canonical medications, diagnoses, laboratories, and symptoms are resolved through the existing source-backed terminology pipeline (RxNorm, ICD-10-CM, LOINC, UCUM, and the curated rule layer). The DOCX does not supply official identifiers.
5. Ages, sexes, weights, vital numbers, and laboratory numbers remain synthetic draws from the case seed.
6. The clean case is validated and fingerprinted.
7. One CliniProof Family 1 or Family 2 error is injected, or the case is kept as a control.

Generation strategy for this path is `resident_seed_guided`. Frozen template batches keep `randomized_template`.

## Six archetype families

1. `MEDREC_UNCERTAIN_HISTORY` — medication history uncertainty
2. `HF_DECOMPENSATION` — acute heart-failure decompensation
3. `OPAT_ENDOCARDITIS` — outpatient parenteral therapy for endocarditis
4. `TRANSPLANT_CMV` — transplant immunosuppression and CMV treatment
5. `POSTOP_ANTICOAGULATION` — postoperative anticoagulation after hip fracture
6. `GI_BLEED_ACUTE_CHANGE` — gastrointestinal bleeding with an acute medication change

## Mapping

| Resident source | Archetype | Key preserved concepts | Details intentionally varied |
| --------------- | --------- | ---------------------- | ---------------------------- |
| `Bad_Med_Rec_Case.docx` | `MEDREC_UNCERTAIN_HISTORY` | Incomplete history, later collateral list, deprescribing versus an uncertain list, home services, PCP follow-up | Exact age/sex/language/neighborhood, specific family members, copied medication nicknames, source laboratory sequence |
| `Heart_Failure_Case.docx` | `HF_DECOMPENSATION` | Congestion, diuresis trajectory, weights/I&O, electrolyte and creatinine course, holds that need reassessment | Source weight series, copied GDMT brand combination, URI/dietary story, exact laboratory numbers |
| `OPAT_Case.docx` | `OPAT_ENDOCARDITIS` | Prolonged parenteral therapy, specified duration, recurring labs, infectious-disease follow-up, line precautions | Organism name, valve surgery year, colonoscopy finding, copied home-medication milligrams |
| `Post_transplant_case.docx` | `TRANSPLANT_CMV` | Transplant history, immunosuppression, infectious complication, temporary holds, antiviral conversion, specialty follow-up | Source tacrolimus goals as a hard rule, copied viral-load series, identifiable transplant chronology |
| `Post-Op_Case.docx` | `POSTOP_ANTICOAGULATION` | Perioperative anticoagulation interruption/resumption, INR trajectory, postoperative hemoglobin, rehabilitation follow-up | Mechanical-valve brand details, opioid taper milligrams, copied hemoglobin series, family availability |
| `Sepsis_AMA_Case.docx` | `GI_BLEED_ACUTE_CHANGE` | GI bleed, anticoagulation held, pending restart decision, PPI context | The seed’s later fever and hypotension are **not** copied into the study cases. An obviously unstable patient would make discharge medication reconciliation uninterpretable. Generated cases are discharge-ready after bleeding has settled. |

## GI-bleed seed handling

`GI_BLEED_ACUTE_CHANGE` is retained as an archetype because the seed is a useful example of changing clinical status. The active set `CLINIPROOF_SEEDCASES_V3` includes it only as **discharge-ready** variants (held anticoagulation, pending restart, hospital-only PPI, or an isolated list error). The febrile hypotensive overlay is documented here and omitted from generated charts. `CLINIPROOF_SEEDCASES_V1` and `CLINIPROOF_SEEDCASES_V2` remain archived.

## What blinded residents do not see

Resident-facing JSON and readable case pages do not include the DOCX filename, seed-author identity, archetype source document, original wording, or investigator answer-key fields. Investigator files may retain archetype ID, source filename, and blueprint version for provenance.

## Archetype and profile

An archetype is the reusable clinical structure abstracted from one source document: the kind of admission, the medication roles, the inpatient changes, and the discharge decision the chart has to support. A profile is one synthetic variant of that archetype. Profiles differ before any error is injected, in symptoms, hospital course, which medication is held or started, and what follow-up is arranged. Four profiles per archetype are used in `CLINIPROOF_SEEDCASES_V3` so each family can include a control and more than one error type. Four is not a claim about prevalence.

## What is synthesized, and what is not copied

Synthesized for every study patient: age, sex, weight, vital signs, laboratory numbers, narrative sentences, and the specific medication orders from the curated regimen. Not copied: names, neighborhoods, family members, source laboratory series, brand combinations, organism names and valve-surgery years from the endocarditis example, tacrolimus goal ranges as if they were a hard rule, opioid tapers, and the later fever and hypotension in the gastrointestinal-bleed source. The DOCX files stay in the repository so a later reader can see the design input. They are not attached to the resident packet.

Privacy handling is straightforward because these files are teaching examples rather than an extract of identified records, and because generation does not paste them into VAL charts. Provenance on the investigator key records the archetype id, the source filename, and the blueprint version. Resident JSON does not.

## How the archetypes connect to VAL-801–VAL-824

| VAL range | Archetype | Profiles |
| --- | --- | --- |
| VAL-801–VAL-804 | `MEDREC_UNCERTAIN_HISTORY` | collateral history verified; statin continued after verification; home-services supply; pending cognitive therapy |
| VAL-805–VAL-808 | `HF_DECOMPENSATION` | uncomplicated diuresis; holds during acute kidney injury; potassium replacement; diuretic adjustment |
| VAL-809–VAL-812 | `OPAT_ENDOCARDITIS` | stable completion plan; omitted parenteral therapy; short antibiotic supply; missing infectious-diseases follow-up |
| VAL-813–VAL-816 | `TRANSPLANT_CMV` | improving CMV; mycophenolate hold and restart; tacrolimus adjustment; pending antiviral duration |
| VAL-817–VAL-820 | `POSTOP_ANTICOAGULATION` | warfarin after hip-fracture repair, including INR monitoring, supply, and inpatient enoxaparin prophylaxis |
| VAL-821–VAL-824 | `GI_BLEED_ACUTE_CHANGE` | anticoagulation held for bleeding, a PPI started in the hospital, and VAL-823 holding apixaban while restart versus continued hold is still pending |

The assigned error for each VAL identifier is in the batch plan and the investigator key, not in this file’s resident-facing summary.

## Reproducibility

Blueprints are versioned (`blueprint_version` in [`blueprints/archetypes.json`](blueprints/archetypes.json)). Generation does not parse DOCX files at freeze time. Changing a DOCX without changing the blueprint does not change generated cases. `CLINIPROOF_SEEDCASES_V1` and `CLINIPROOF_SEEDCASES_V2` remain archived. The current prospective seed-guided batch is `CLINIPROOF_SEEDCASES_V3`.
