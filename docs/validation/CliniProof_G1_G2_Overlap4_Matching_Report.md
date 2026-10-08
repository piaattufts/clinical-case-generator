# Matching report: four revised Generation 1 cases and their Synthea counterparts

This report is for investigators. It is not part of the clinician packet. The clinician codebook is [CliniProof_Synthea_Matched_Overlap4_Codebook.docx](CliniProof_Synthea_Matched_Overlap4_Codebook.docx). The Generation 1 codebook is [CliniProof_Revised_Overlap4_Codebook.docx](CliniProof_Revised_Overlap4_Codebook.docx).

The pairs are VAL-801 with G2-001, VAL-805 with G2-005, VAL-809 with G2-009, and VAL-813 with G2-013. Matching is the reasoning problem. It is not a copy of age, doses, laboratories, narrative, or the hidden reference. No generation method has been judged superior. Neither set is clinically validated.

Synthea commit `d9d07a6eef91ee5144293b42ab64224d84d124f8`, seed `20261008`, 1,000 living patients requested, 162 deceased exports excluded. Provenance for the four patients is [provenance.json](../../data/case_sets/synthea_g2/matched_overlap_4/provenance.json). The case-level audit is [clinical_validation_audit.md](../../data/case_sets/synthea_g2/matched_overlap_4/clinical_validation_audit.md).

## VAL-801 and G2-001

1. Shared problem. An older adult has an acute cognitive change. The resident has to tell delirium from baseline and decide which outpatient medicines continue, stop, or restart.
2. Generation 1. VAL-801 was revised from both clinicians' comments on the clean baseline: a caregiver baseline, a urinary infection found during the stay, and a visible reason for each medicine change.
3. Synthea contribution. Patient `035db839-25b9-cb92-8853-12152fc6b257`, a 71-year-old man. Hypertension, osteoarthritis, and five outpatient products, including two metoprolol salts, are from the longitudinal record.
4. CliniProof augmentation. The delirium, the urinary infection, the cephalexin course, and the creatinine series are episode-generated.
5. Matching. Same family and the same kind of decision: stop a completed antibiotic, continue chronic medicines that the chart still supports, and stop medicines the acute illness makes unsafe.
6. History. Generation 1 uses a constructed mild cognitive disorder. Generation 2 uses a Synthea record that does not list dementia.
7. Trajectory. Generation 2 is a one-day change with dysuria, pyuria, and Escherichia coli, then recovery. The numbers are not the Generation 1 numbers.
8. Medication complexity. Generation 2 has two metoprolol products. The reference continues succinate 100 mg daily and stops tartrate 25 mg twice daily. Ibuprofen stops because creatinine rose from 1.0 to 1.6 mg/dL. Lisinopril continues after recovery to 1.1 mg/dL.
9. Quality control. Automated sufficiency checks pass. Non-disease Synthea findings were removed from the visible problem list.
10. Outstanding uncertainty. A clinician may prefer to continue ibuprofen or to stop the other metoprolol salt. Those alternatives are on the reference. They are not a completed review.

## VAL-805 and G2-005

1. Shared problem. Acute heart-failure decompensation, a diuretic course, and a discharge decision about heart-failure medicines.
2. Generation 1. VAL-805 was revised so the precipitant, the intravenous diuretic course, the weight trajectory, and one therapy decision are visible.
3. Synthea contribution. Patient `023d2efe-5482-ee13-418f-729c0823db68`, a 67-year-old man. Metoprolol succinate, lisinopril, and amlodipine, plus a longitudinal weight, come from the extract. The record does not list heart failure.
4. CliniProof augmentation. The missed refills, pulmonary edema, natriuretic peptide, echocardiogram with an ejection fraction of 30 percent, and the furosemide course are episode-generated.
5. Matching. Same family. The decision types are a new loop diuretic and continuation of medicines already in use. Monitoring is a chemistry panel and weights.
6. History. Generation 1 is a known heart-failure admission. Generation 2 establishes the syndrome during this stay, on a cardiovascular background.
7. Trajectory. Weight goes from 82.2 kg to 87.7 kg to 83.0 kg. That series is not the Generation 1 series. The precipitant is cost-related nonadherence, not a copied Generation 1 story.
8. Medication complexity. Furosemide 40 mg daily is new. Lisinopril and metoprolol continue. A mineralocorticoid receptor antagonist is explicitly not required on the day of discharge.
9. Quality control. Automated checks pass, including the falling weight. The known-heart-failure pool in this living export was four patients. This case did not use that pool.
10. Outstanding uncertainty. A reviewer may want a patient whose Synthea record already contained heart failure, or may want an mineralocorticoid receptor antagonist started now. Neither change was forced.

## VAL-809 and G2-009

1. Shared problem. Endocarditis established in the hospital, and a decision about outpatient intravenous antibiotics.
2. Generation 1. VAL-809 was revised to show fever, a predisposition, cultures before antibiotics, imaging, a statement about surgery, and the renal context of the antibiotic.
3. Synthea contribution. Patient `0041e9d6-876a-25b9-d55d-96876882622a`, a 41-year-old man. Asthma and other longitudinal conditions are Synthea's. Endocarditis is not. No curated home regimen matched the extract, so no outpatient list was copied.
4. CliniProof augmentation. Fever, a dental extraction, Streptococcus sanguinis bacteremia, an 8 mm mitral vegetation, ceftriaxone 2 g daily, and the surgery consult are episode-generated.
5. Matching. Same family and the same primary task: continue or stop the intravenous antibiotic. Monitoring is weekly laboratories and infectious-diseases follow-up.
6. History. Generation 1 includes chronic medicines and a renal course. Generation 2 has no home list and a stable creatinine of 1.2 mg/dL.
7. Trajectory. Cultures precede the antibiotic. Clearance cultures show no growth. The dental extraction is not the Generation 1 caries history, and the organism is not the Generation 1 organism.
8. Medication complexity. One drug. The reference continues ceftriaxone. The remaining duration is not signed on the resident chart. An alternative site of infusion does not change the drug.
9. Quality control. Automated checks pass. Four variants were attempted. All used this patient, because that is who the matcher selected. None created a home regimen.
10. Outstanding uncertainty. The reconciliation task is thinner than VAL-809 because there is no outpatient list. A different Synthea patient with curated home medicines was not substituted.

## VAL-813 and G2-013

1. Shared problem. A transplant recipient with a new illness in which cytomegalovirus disease has to be established by testing, and antiviral therapy plus immunosuppression have to be decided.
2. Generation 1. VAL-813 was revised so the diagnosis follows the work-up, valganciclovir is not already a home medicine for a new diagnosis, and volume and potassium changes have a visible mechanism.
3. Synthea contribution. Patient `1d9427d1-dd59-3e23-541f-4faebc086080`, a 61-year-old man. Kidney transplant status and extended-release tacrolimus are in the longitudinal record, as are hydrochlorothiazide and amlodipine. Eleven living patients met the transplant rule.
4. CliniProof augmentation. Diarrhea, a negative Clostridioides difficile test, cytomegalovirus DNA, colitis on biopsy, valganciclovir induction, and the creatinine and potassium course are episode-generated. Mycophenolate was not invented.
5. Matching. Same family. Decisions are a new antiviral, continuation of recorded tacrolimus, and a stop of the thiazide that accompanied the volume loss.
6. History. The transplant and tacrolimus are Synthea's. Valganciclovir was not on the home list.
7. Trajectory. The patient does not arrive labeled with cytomegalovirus colitis. Potassium falls to 3.2 mmol/L with dry membranes and then recovers to 4.0. Creatinine rises from 1.1 to 1.8 and returns to 1.2 mg/dL.
8. Medication complexity. Valganciclovir 900 mg twice daily starts only after the test. Tacrolimus continues at the recorded dose. Hydrochlorothiazide stops. Restart later is an alternative, not the reference.
9. Quality control. Automated checks pass. The reference correction for hydrochlorothiazide uses facts already on the chart.
10. Outstanding uncertainty. The immunosuppressive regimen is only what Synthea recorded. A reviewer may want a second immunosuppressant. It was not added.

## What this report does not say

It does not say that a clinician has approved any Generation 2 chart. It does not say that Generation 2 is more coherent than Generation 1. The next step is review with the same C1–C5 instrument.
