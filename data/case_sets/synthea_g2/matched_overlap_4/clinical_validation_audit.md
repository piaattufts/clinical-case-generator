# Clinical audit of the four matched Generation 2 cases

These four charts already existed in `data/case_sets/synthea_g2/cases/`. This audit did not create a second pipeline and did not copy the Generation 1 charts. Two derivative corrections were applied before the codebook was rendered.

Non-disease Synthea findings were removed from the resident-visible problem list: education level, housing, transport, and a criminal-record flag. The SNOMED codes remain on `source_snomed`. They are not new facts.

Unsupported reference wording was corrected from the charts that already existed. Ibuprofen and the second metoprolol salt on G2-001 now stop. Hydrochlorothiazide on G2-013 now stops. Lisinopril on G2-005 records that a mineralocorticoid receptor antagonist is not required on the day of discharge. The hospitalizations were not rewritten to force those answers.

Automated checks are not clinician approval. `clinically_validated` remains false. No reviewer is described as having accepted a correction.

## Requirement checklist

| Requirement | G2-001 | G2-005 | G2-009 | G2-013 |
| --- | --- | --- | --- | --- |
| Baseline status sufficiently described | Pass. No dementia in the longitudinal record. Usual function is conversing and recognizing family. | Pass for premorbid function and weight. Prior heart failure is absent from Synthea and is labeled as such. | Pass. No prior endocarditis. First creatinine is 1.2 mg/dL. | Pass. Transplant status and tacrolimus are from the longitudinal record. |
| Acute illness explained | Pass. New disorientation and dysuria. | Pass. New dyspnea, orthopnea, and edema. | Pass. New fever, sweats, and a murmur. | Pass. New watery stool, not a preassigned cytomegalovirus label. |
| Diagnostic work-up appropriate | Pass. Urinalysis, urine culture, blood cultures, chest radiograph, before the infection is treated as known. | Pass. Radiograph, natriuretic peptide, troponin, then echocardiogram. | Pass. Cultures before antibiotics, then echocardiography. | Pass. Clostridioides difficile testing, then cytomegalovirus DNA, then endoscopy and biopsy. |
| Treatment course clinically coherent | Pass. Five days of cephalexin after the culture. | Pass. Intravenous then oral furosemide, with a falling weight. | Pass. Ceftriaxone 2 g daily after cultures, day 6 at discharge planning. | Pass. Valganciclovir 900 mg twice daily only after the diagnostic result. |
| Laboratory and vital trends plausible | Pass. Creatinine 1.0, then 1.6, then 1.1. | Pass. Weight 82.2 to 87.7 to 83.0 kg. Creatinine peaks at 1.1. | Pass. Creatinine stays 1.2 mg/dL. Clearance culture has no growth. | Pass. Creatinine 1.1 to 1.8 to 1.2. Potassium 3.2 to 4.0. |
| Medication changes supported | Corrected. Duplicate metoprolol tartrate stops. Ibuprofen stops because of the creatinine rise. Lisinopril continues after recovery, with a hold as an alternative. | Pass. Furosemide is a new start. Existing metoprolol, lisinopril, and amlodipine continue. An mineralocorticoid receptor antagonist is recorded as not required today. | Pass. Ceftriaxone continues. No home regimen was available to change. | Corrected. Tacrolimus continues. Valganciclovir starts. Hydrochlorothiazide stops because of volume loss. |
| Relevant complications considered | Pass. Acute kidney injury is on the chart. | Pass. Ischemia was checked with a flat troponin. | Pass. Surgery found no abscess and no urgent indication to operate. | Pass. Other causes of diarrhea were tested before cytomegalovirus was treated as the cause. |
| Discharge stability supported | Pass. Attention returned to the caregiver's baseline. | Pass. Weight down, oxygen 96 percent, lying flat. | Pass. Afebrile, walking, clearance culture negative. | Pass. Drinking, walking, potassium recovered. Cytomegalovirus DNA is still detected and is not described as cleared. |
| Hidden reference supported by visible facts | Pass after the reference correction. | Pass. | Pass. | Pass after the hydrochlorothiazide correction. |
| Resident discharge answer not revealed | Pass. The course says the discharge list is unsigned. | Pass. The unsigned task remains. | Pass. The remaining antibiotic duration is not signed. | Pass. The induction course is not signed as a finished list. |
| Synthea provenance verified | Pass. Patient `035db839-25b9-cb92-8853-12152fc6b257`. | Pass. Patient `023d2efe-5482-ee13-418f-729c0823db68`. | Pass. Patient `0041e9d6-876a-25b9-d55d-96876882622a`. | Pass. Patient `1d9427d1-dd59-3e23-541f-4faebc086080`. |
| Synthetic augmentation explicitly labeled | Pass. Episode facts use `cliniproof_episode_generated`. | Pass. | Pass. | Pass. |

## Round 1 concern to Generation 2 evidence

The concern text is the de-identified comparison, not a claim that a reviewer has approved the new chart.

### VAL-801 and G2-001

| Round 1 concern | Generation 2 requirement | Evidence in G2-001 |
| --- | --- | --- |
| Delirium without a baseline | State usual cognition before the acute change | The record does not list dementia. The patient handled daily activities and recognized family. The caregiver said he had been conversant the day before. |
| No precipitant | A plausible acute illness, found by testing | Dysuria, pyuria, and Escherichia coli in the urine. The infection is named after those results. |
| Ibuprofen stopped without a reason | Do not stop an analgesic unless the chart supports it | Ibuprofen was on the Synthea list. Creatinine rose from 1.0 to 1.6 mg/dL. The reference stops it for that rise and records continue as an alternative. |
| Medication list not clear enough for a decision | Home products come from the longitudinal extract | Five outpatient products are named, including two metoprolol salts. The reference continues succinate and stops tartrate so both are not discharged. |

### VAL-805 and G2-005

| Round 1 concern | Generation 2 requirement | Evidence in G2-005 |
| --- | --- | --- |
| No reason for decompensation | A precipitant or an evaluation | Home cardiovascular medicines were stopped because the refill was unaffordable. Diet and rhythm were unchanged. |
| Inpatient diuretic copied the home dose | An acute diuretic course | No loop diuretic was in the extract. Intravenous furosemide was started, then oral 40 mg daily. |
| Discharge weight not at a stated dry weight | A weight trajectory | 82.2 kg before admission, 87.7 kg on arrival, 83.0 kg by hospital day 4. |
| Heart-failure therapy not a decision | Visible evidence for what continues or starts | Metoprolol and lisinopril were already outpatient medicines and continue. Furosemide is new. A mineralocorticoid receptor antagonist is not added today. |
| Reviewer 2 asked why heart failure decompensated | The same precipitant is visible before the diagnosis | The missed medicines precede the radiograph and the echocardiogram. |

### VAL-809 and G2-009

| Round 1 concern | Generation 2 requirement | Evidence in G2-009 |
| --- | --- | --- |
| Need fever and a predisposition | Symptoms, and a source evaluation | Fever to 38.4 C. A dental extraction two weeks earlier is episode-generated, not a copy of the Generation 1 caries history. Skin examination found no abscess. |
| Thin work-up | Cultures before antibiotics, then imaging | Two culture sets grew Streptococcus sanguinis. An 8 mm mitral vegetation followed. |
| Lisinopril continued through AKI | Do not invent that problem if the patient has no such medicine | This Synthea patient had no curated home regimen. Creatinine stays 1.2 mg/dL, which is why the 2 g ceftriaxone dose is used. |
| Surgery not addressed | A documented surgical opinion | Cardiac surgery found no abscess, no severe regurgitation, and no urgent indication to operate. |

### VAL-813 and G2-013

| Round 1 concern | Generation 2 requirement | Evidence in G2-013 |
| --- | --- | --- |
| Arrived already labeled with cytomegalovirus colitis | Symptoms first, diagnosis after testing | Eight days of diarrhea. Clostridioides difficile toxin was negative. Cytomegalovirus DNA, then endoscopy and biopsy, then the diagnosis. |
| Valganciclovir already a home medicine | Do not place it on the home list unless the longitudinal record has it | The chart states it was not a home medicine and was not inferred from transplant status. |
| Transplant regimen too thin | Use only immunosuppression Synthea recorded | Extended-release tacrolimus continues. Mycophenolate was not added. |
| Potassium change without a supported mechanism | Show volume loss and the values | Potassium 3.2 mmol/L on arrival with dry membranes and watery stool, then 4.0 mmol/L. Hydrochlorothiazide stops. |

## Outstanding uncertainty

G2-005 does not have prior heart failure in the Synthea record. The acute syndrome is episode-generated on a cardiovascular background. The living export contained only four patients with known Synthea heart failure.

G2-009 has no curated home medication list, so the discharge decision is the antibiotic plan rather than a multi-drug reconciliation. Four episode variants were attempted for this patient. None added a home regimen, because the longitudinal products did not match a curated regimen. A different patient was not substituted.

G2-009's dental extraction is an episode variant. It is the same kind of predisposition the first review requested for VAL-809, and it is not that case's history. The organism is Streptococcus sanguinis, not the Generation 1 organism.

G2-001 and G2-013 reference actions were corrected in this audit. A clinician may still prefer the recorded alternatives. That preference is what the review is for.

None of the four cases is clinically validated.
