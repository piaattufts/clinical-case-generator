# Five-case clean pilot

Seed `42`, start index `9001`, scenario `HF_INPATIENT`, profile `default`. `--inject-error` was not used. Existing VAL-701–VAL-824 files were not changed.

Automated validation passed on all five cases, with no answer key and no `reference_discharge_plan` in the resident document. None is ready for expert review as a discharge-decision case. The reference plan still continues a home medication because the scenario list contains it. The written rationale is “Home therapy is continued through discharge in the clean case.”

The default command uses the family-level profile, not one of the named heart-failure variants. On that profile, with error injection off, inpatient-only drugs such as pantoprazole are not added. Stopping ibuprofen is assigned by `stop_medication_queries`, not by a bleeding or kidney event. Warfarin or apixaban is chosen at random from the anticoagulant pair. The only diagnosis stored is acute systolic heart failure, but atorvastatin and the anticoagulant are labeled with that diagnosis.

| Case | Resident case clean | Reference plan valid | Evidence sufficient | Clinical inconsistencies | Ready for expert review |
| --- | --- | --- | --- | --- | --- |
| SYN-009001 | Yes | No | No | Warfarin and atorvastatin labeled as heart failure; no atrial fibrillation or lipid diagnosis | No |
| SYN-009002 | Yes | No | No | Apixaban and atorvastatin labeled as heart failure; INR present without warfarin | No |
| SYN-009003 | Yes | No | No | Same pattern as SYN-009001, with warfarin | No |
| SYN-009004 | Yes | No | No | Same pattern as SYN-009002, with apixaban | No |
| SYN-009005 | Yes | No | No | Same pattern as SYN-009002, with apixaban | No |

## Evidence trace (same pattern in every case)

| Reference decision | Support actually used by the generator | Where the resident can see it | Class |
| --- | --- | --- | --- |
| Continue lisinopril, furosemide, metoprolol succinate, spironolactone | Profile list of home drugs. Rationale does not cite the heart-failure diagnosis, BNP, creatinine, or potassium. | Heart-failure diagnosis, dyspnea/edema/orthopnea, elevated BNP, and the same drugs on the home and inpatient lists. Potassium and creatinine are in a range that does not force a hold. | WEAK_EVIDENCE |
| Continue atorvastatin | Same home-list default. Indication text is the heart-failure diagnosis because hyperlipidemia is not on the problem list. | Drug is on the home and inpatient lists. No lipid diagnosis, event, or lab. | CLINICALLY_INCONSISTENT |
| Continue warfarin or apixaban | Random draw from the scenario anticoagulant pair when the profile does not name one. | Drug is on the home and inpatient lists. No atrial fibrillation or other anticoagulant indication. Warfarin cases include an INR; apixaban cases also include an INR with no warfarin. | CLINICALLY_INCONSISTENT |
| Stop ibuprofen | `stop_medication_queries`. Rationale is that a home drug was discontinued. | Instruction and held reason say it was stopped during the admission. No gastrointestinal bleed, acute kidney injury, or other precipitant. | WEAK_EVIDENCE |

Heart-failure drugs are plausible chronic therapy, but the plan does not show that anyone weighed the labs. The answer for ibuprofen is stated in the resident instructions rather than left for the resident to infer.
