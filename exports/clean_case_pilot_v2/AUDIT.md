# Second five-case pilot: evidence-based discharge decisions

Seed `42`, start index `9101`, scenario `HF_INPATIENT`, profile `default`. Clean generation only. Error injection was off. Narrative source is the local template.

This directory is new. `exports/clean_case_pilot/` (SYN-009001–SYN-009005) was not edited. VAL-701–VAL-724 and VAL-801–VAL-824 were not edited. The 48-case study set was not regenerated.

Case IDs: SYN-009101, SYN-009102, SYN-009103, SYN-009104, SYN-009105.

## What used to assign the discharge action

The clean writer previously copied a medicine onto the discharge list because the scenario profile named it. The indication helper then copied the admission diagnosis when its map did not match.

| Stored state | Code path | What actually decided it |
| --- | --- | --- |
| continue | `_add_continued_medication` | Membership in `medication_queries` / `medication_required_queries`. Rationale text was "Home therapy is continued through discharge in the clean case." |
| stop | `_add_stopped_medication` | Membership in `stop_medication_queries`. No bleed, kidney injury, or other charted fact was required. |
| start | hospital-only and `started_inpatient` writers | Membership in `hospital_only_medication_queries` or a regimen temporal role. |
| hold | pending-hold writer | Profile field `pending_discharge_state`, used by the error-injection path. |
| restart | held-restart writer | Profile hold fields, used when injecting `f2_held_med_no_restart_plan`. |
| change | none on the clean path | `dose_change` existed as a database value and was never written. |
| anticoagulant choice | `_select_medications` | `rng.choice` over `anticoagulant_mutex_queries` on the default profile. |
| indication text | `_indication_for` | `INDICATION_BY_QUERY` when it hit; otherwise the first problem name, which labeled atorvastatin and anticoagulants as heart failure. |
| INR | lab query list | Requested because the scenario listed INR, including apixaban cases. |

Enabled rules (`NO_DUAL_ORAL_ANTICOAGULANT`, `WARFARIN_INR_MONITORING`, `FUROSEMIDE_HF_INDICATION`) did not choose continue versus stop.

## What decides it now

The clean pipeline treats profile medication lists as candidates. `app/services/medication_decisions.py` assigns the action.

1. A home medicine is continued only when a supported indication is on the problem list and the safety facts that medicine requires are charted.
2. The indication comes from `INDICATION_BY_QUERY`, or, if that map misses, from a phrase in the stored regimen citation that also appears in a diagnosis. The admission diagnosis is not used as a fallback.
3. Lisinopril's stored citation names heart failure, so lisinopril can be continued for systolic heart failure when creatinine, potassium, and systolic pressure are charted and inside existing generator bounds. Atorvastatin's citation does not name heart failure, so atorvastatin is omitted when hyperlipidemia is absent.
4. Warfarin or apixaban is added on the clean path only when the profile asks for one and a diagnosis or comorbidity query contains fibrillation. The default heart-failure profile does neither. INR labs and INR monitoring are not created unless warfarin is actually discharged.
5. Ibuprofen is not stopped merely because it is listed in `stop_medication_queries`. A stop is written only when a resident-visible clinical fact is present (bleeding, a charted laboratory reason, prophylaxis noted as hospital-only, or an `adverse_events` entry). The default profile has no such fact, so ibuprofen is left out of the chart.
6. `dose_change` can be persisted when a second curated regimen differs in dose or frequency and the hospital-course pattern is `diuretic_dose_adjustment` or `medication_adjustment`. Furosemide has one curated regimen (40 MG daily), so the pilot does not invent an 80 MG change.
7. Creatinine at or above 1.8 mg/dL, the floor of the existing acute-kidney laboratory pattern, produces `hold`. Systolic pressure below 100 mmHg, the threshold already written into the restart-plan sentence, also produces `hold`. Missing creatinine, potassium, or systolic pressure omits the medicine instead of continuing it.
8. The evaluator document stores `evidence_trace` and `evidence_class`. The resident document does not.

`stop_medication_queries` and `hospital_only_medication_queries` remain on the scenario file for the experimental error-injection path. They are marked deprecated as discharge answers. The clean path does not treat them as the action.

No schema migration was added. The trace is computed from the chart when the evaluator document is built.

No rule template was added or edited. `FUROSEMIDE_HF_INDICATION` is attached as supporting evidence when that enabled rule matches the furosemide row. It does not by itself choose continue versus hold.

## Omitted candidates (all five cases)

| Candidate | Why it is not on the chart |
| --- | --- |
| atorvastatin | No hyperlipidemia diagnosis. The admission diagnosis was not copied onto it. |
| ibuprofen | `stop_medication_queries` is not a discharge answer. No bleeding or other adverse event is charted. |
| warfarin / apixaban | The default profile does not name an anticoagulant, and atrial fibrillation is not a diagnosis. |
| pantoprazole | Not added on the default clean path, and gastro-esophageal reflux is not a diagnosis. |
| INR | Not generated, because warfarin is not on the case. |

## Cases

Every case has one diagnosis: Acute systolic (congestive) heart failure. Home and inpatient lists contain the same four medicines. There is no inpatient dose change. Discharge blood pressure, creatinine, and potassium are the facts cited below. Natriuretic peptide B is also on the chart.

| Case | Age / sex | Discharge SBP / HR | Discharge Cr | Discharge K | Discharge BNP |
| --- | --- | --- | --- | --- | --- |
| SYN-009101 | 79 Female | 114 / 81 | 1.0 mg/dL | 4.4 mmol/L | 454 pg/mL |
| SYN-009102 | 55 Female | 123 / 68 | 1.1 mg/dL | 3.7 mmol/L | 653 pg/mL |
| SYN-009103 | 67 Male | 137 / 62 | 1.0 mg/dL | 4.4 mmol/L | 326 pg/mL |
| SYN-009104 | 81 Male | 126 / 80 | 1.0 mg/dL | 4.6 mmol/L | 670 pg/mL |
| SYN-009105 | 84 Male | 141 / 68 | 1.0 mg/dL | 4.4 mmol/L | 631 pg/mL |

Hidden reference plan, identical in action across the five cases:

| Medicine | Action | Indication source | Class |
| --- | --- | --- | --- |
| furosemide 40 MG daily | continue | `INDICATION_BY_QUERY` heart failure, plus creatinine, BNP, and systolic pressure. Enabled rule `FUROSEMIDE_HF_INDICATION`. | SUFFICIENT_EVIDENCE |
| spironolactone 25 MG daily | continue | `INDICATION_BY_QUERY` heart failure, plus creatinine, potassium, and BNP. | SUFFICIENT_EVIDENCE |
| lisinopril 10 MG daily | continue | Regimen citation names heart failure. Creatinine, potassium, and systolic pressure are charted inside existing bounds. | SUFFICIENT_EVIDENCE |
| metoprolol succinate 25 MG daily | continue | `INDICATION_BY_QUERY` heart failure, plus systolic pressure and heart rate. | SUFFICIENT_EVIDENCE |

Full per-medicine traces are in each `*_evaluator.json` under `reference_discharge_plan.medications[].evidence_trace`. They are absent from `*_resident.json`.

Validation passed on all five. Answer-key count is 0. Resident leak check is empty. No plan is an error target. No monitoring parameter is INR.

## Summary

| Case | Medication indications valid | Decisions evidence-based | Monitoring consistent | Evidence sufficient | Ready for expert review |
| --- | --- | --- | --- | --- | --- |
| SYN-009101 | Yes | Yes | Yes | Yes | Yes |
| SYN-009102 | Yes | Yes | Yes | Yes | Yes |
| SYN-009103 | Yes | Yes | Yes | Yes | Yes |
| SYN-009104 | Yes | Yes | Yes | Yes | Yes |
| SYN-009105 | Yes | Yes | Yes | Yes | Yes |

## Limitations

- These five cases are the default heart-failure profile. They differ in age, sex, and the generated numbers. They do not differ in medication list or discharge action.
- The pilot contains continue only. Start, stop, hold, and change are implemented and covered by unit tests. This profile does not contain a fact that justifies those actions, and furosemide does not have a second curated dose.
- Hold and the potassium bounds reuse numbers the generator already used for laboratory patterns and the restart sentence. They are not a new guideline implementation.
- Structured allergies are not stored on the case. The consistency check reads an "allergic to ..." phrase from notes. These charts have no such phrase.
- Lisinopril is tied to heart failure by the stored regimen citation, not by a separate hypertension diagnosis. Named profiles that include hypertension still map lisinopril to hypertension first.
