# Revision log for the four overlapping cases

Status: ready for the next clinician review. These charts are not clinically validated.

The baseline for every case is the clean chart in `data/case_sets/seed_guided/CLEAN_BASE/`. The historical planted-error files were not used. Reviewer comments were taken from the de-identified comparison. Where the reviewers described the same gap in different words, both wordings were kept. A concern raised by only one reviewer was kept when it identified a real gap in the chart.

The hidden discharge reference was written again after the chart was revised. A discharge action is included only when the revised resident-visible chart states the facts that defend it. New patient-specific values are synthetic. Literature is cited for plausibility. A citation does not turn a synthetic value into a recovered fact.

Revised files:

- `data/case_sets/seed_guided/REVISED/overlap_4/`
- `docs/validation/CliniProof_Revised_Overlap4_Codebook.docx`

The coding instrument in that codebook is the existing C1–C5 form. It was not redesigned.

## VAL-801

### Reviewer 1 concern

The delirium improves without a cause, and the chart does not say why ibuprofen was stopped. The overall recommendation was revise.

### Reviewer 2 concern

Delirium is a change from baseline, and the chart does not supply that baseline or a precipitant. C2 through C5 and the overall recommendation were blank and were not inferred.

### Combined interpretation

The case needs a cognitive baseline, an acute precipitant that can explain the new confusion and the recovery, and a visible reason for stopping ibuprofen. Those gaps are one clinical problem: the hospitalization does not yet support a discharge medication decision.

### Old chart element

A 75-year-old man is admitted with “delirium due to known physiological condition.” Confusion improves with treatment. Ibuprofen is stopped with no clinical reason. Creatinine moves from 1.1 mg/dL to 1.0 mg/dL. Lisinopril, metformin, and atorvastatin simply continue.

### New chart element

He has mild major neurocognitive disorder. A caregiver describes his baseline. The admission is two days of confusion worse than that baseline. Fever, pyuria, and Escherichia coli in the urine explain the change. Ceftriaxone 1 g intravenously once daily is completed for seven days before discharge. Outpatient creatinine is 1.0 mg/dL, admission creatinine is 1.5 mg/dL, and discharge creatinine is 1.0 mg/dL. Ibuprofen is stopped and not restarted. Lisinopril and metformin are held during the creatinine rise and poor intake, then restarted. Atorvastatin continues. No discharge antibiotic is planned.

### Clinical rationale

The discharge list can now be read off the chart: restart lisinopril and metformin because kidney function and intake have recovered, continue atorvastatin, do not restart ibuprofen, and do not continue the finished antibiotic. The prior reference continued every chronic medicine and stopped ibuprofen without a reason the resident could see.

### Evidence

Delirium is defined as a change from baseline attention (DSM-5-TR). IDSA guidance for pyelonephritis includes ceftriaxone 1 g intravenously, and the ceftriaxone label lists 1 to 2 g once daily. The 2019 AGS Beers Criteria list NSAIDs among drugs that can worsen kidney function in older adults. The seven-day course and the creatinine values are synthetic. They are not measurements from a resident source document.

### Provenance

Recorded on the evaluator file under `revision_provenance.synthetic_facts`. The resident file does not contain the reference plan.

## VAL-805

### Reviewer 1 concern

The inpatient diuretic repeats the home oral dose, discharge weight is not at dry weight, and the chart does not give several days of intake and output or a cardiology or echocardiography finding that would let a trainee change the diuretic or add heart-failure therapy. The overall recommendation was revise.

### Reviewer 2 concern

The chart does not investigate why heart failure decompensated. C1 was Pass. Later fields were blank and were not inferred.

### Combined interpretation

The admission needs a precipitant, an intravenous diuretic course that is not a copy of the home prescription, weights that reach dry weight, and enough cardiac information for one discharge decision about the loop diuretic and one about disease-modifying therapy.

### Old chart element

Furosemide 40 mg orally once daily is both the home medicine and the inpatient medicine. Discharge weight is 78 kg and dry weight is 73 kg. One day of intake and output is shown. Cardiology says only to continue the intended plan. There is no explanation of the decompensation and no ACE inhibitor.

### New chart element

She missed four days of furosemide because the supply ran out. There is no chest pain. The electrocardiogram shows sinus rhythm without ischemic ST-segment change, and troponin I is 18 ng/L then 16 ng/L. Ejection fraction is 30 percent, without a new severe valve lesion. Furosemide 40 mg intravenously twice daily is given for three days and then stopped. Weight goes from 84 kg to 81 kg to 78 kg, which is the recorded dry weight. Intake and output are net negative on each of those days. Oxygen is weaned from 2 L/min to room air. Cardiology says to resume furosemide 40 mg orally once daily and to start enalapril 5 mg orally twice daily. The enalapril dose has not been given yet. Metoprolol succinate and atorvastatin continue. Creatinine is 0.9 mg/dL, potassium is 4.3 mmol/L, and systolic blood pressure is 110 mm Hg.

### Clinical rationale

Doubling the oral maintenance diuretic would not follow the stated precipitant. The missed doses explain the fluid gain, and the intravenous course has already ended at dry weight, so the defended diuretic action is to resume 40 mg orally once daily and to secure the supply. The defended new action is to start enalapril, because the ejection fraction is 30 percent and no ACE inhibitor, ARB, or ARNI is on the home list. The prior reference, which continued the unchanged oral furosemide and added nothing, is not preserved.

### Evidence

The 2022 AHA/ACC/HFSA heart failure guideline recommends intravenous loop diuretic treatment for admitted patients with fluid overload and an ACE inhibitor when an ARNI is not used. SOLVD studied enalapril in systolic heart failure. The enalapril dose is the project’s curated 5 mg twice-daily regimen. The missed days, troponin pair, ejection fraction, weights, and intake-output rows are synthetic.

### Provenance

Recorded on the evaluator file. A higher oral furosemide dose was considered and not used, because the chart attributes the decompensation to missed doses rather than to failure of 40 mg daily.

## VAL-809

### Reviewer 1 concern

The case should include fever and a predisposition such as a mechanical valve or poor dentition. The creatinine rise is unexplained, and lisinopril appears to continue through it. The overall recommendation was revise.

### Reviewer 2 concern

The chart needs a source evaluation, laboratory course, imaging, and a statement about surgery. C1 was Fail. Later fields were blank and were not inferred.

### Combined interpretation

Endocarditis treatment and the lisinopril decision both need visible evidence: how the infection was diagnosed, whether surgery is indicated, and what the creatinine did while the ACE inhibitor was held or given.

### Old chart element

An afebrile man is admitted with fatigue and a nonspecific gram-positive blood culture. A transthoracic study says there is a vegetation and ventricular function is preserved. Creatinine goes from 1.3 mg/dL to 0.8 mg/dL with no baseline and no hold of lisinopril. Ceftriaxone 2 g daily is started, but the duration is only “specified.”

### New chart element

Admission temperature is 38.8 C. He has caries and periodontal disease and no prosthetic valve. Two blood-culture sets drawn before antibiotics grow penicillin-susceptible Streptococcus mitis group and are negative on hospital day 3. Transesophageal echocardiography shows an 8 mm mitral vegetation, mild regurgitation, no abscess, and an ejection fraction of 55 percent. Cardiac surgery records no current indication for an operation. Outpatient creatinine is 0.9 mg/dL, hospital-day-1 creatinine is 1.6 mg/dL, and discharge creatinine is 0.8 mg/dL. Lisinopril is held during the rise and restarted the day before discharge. Ceftriaxone 2 g intravenously once daily continues for four weeks counted from the first negative culture, through a peripherally inserted central catheter, with weekly blood counts and creatinine. Infectious-diseases follow-up is in 7 days, and dental follow-up is in 2 weeks. The leukocyte count falls from 14.2 to 7.4 ×10³/µL.

### Clinical rationale

The discharge antibiotic is the regimen already started, for the duration infectious diseases states, in a patient whose bacteremia has cleared and who does not have an indication for surgery on this chart. Lisinopril is restarted only after the chart shows creatinine back at baseline. Continuing lisinopril straight through the rise was not kept.

### Evidence

The 2015 AHA scientific statement on infective endocarditis describes ceftriaxone 2 g every 24 hours for four weeks for native-valve infection with highly penicillin-susceptible viridans-group streptococci, and it reserves early surgery for heart failure from valve destruction, uncontrolled infection, or findings such as abscess. The KDIGO acute-kidney-injury guideline calls for review of hemodynamically active drugs when filtration falls. The organism, vegetation size, temperatures, and creatinine series are synthetic. The organism is not the organism in the resident source document.

### Provenance

Recorded on the evaluator file. Poor dentition was used instead of a prosthetic-valve history so the predisposition would not copy the source case.

## VAL-813

### Reviewer 1 concern

Valganciclovir is already a home medicine even though the illness is presented as a new diagnosis. The transplant regimen is too thin. The potassium change has no cause. The overall recommendation was exclude.

### Reviewer 2 concern

The patient should not arrive already labeled with cytomegalovirus colitis. Symptoms should lead to a work-up. Diarrhea would be expected to lower kidney function and potassium at presentation. C1 was Fail. Later fields were blank and were not inferred.

### Combined interpretation

The admission has to start from diarrhea, the diagnosis has to be earned by testing, the antiviral has to begin after that diagnosis, the transplant medicines have to be a real maintenance regimen, and the laboratory course has to match volume loss.

### Old chart element

The admission diagnosis is cytomegalovirus disease. Valganciclovir 900 mg twice daily is a home medicine. Immunosuppression is tacrolimus alone, plus amlodipine and atorvastatin. Admission potassium is 4.7 mmol/L and falls to 3.9 mmol/L. Creatinine is 1.2 mg/dL and falls to 1.0 mg/dL. Weight falls from 68 kg to 66 kg against a dry weight of 63 kg.

### New chart element

She is admitted for watery diarrhea and poor intake. Valganciclovir is not a home medicine. Home immunosuppression is tacrolimus 1 mg every 12 hours, mycophenolate mofetil 1000 mg twice daily, and prednisone 5 mg daily. Admission blood pressure is 100/62 mm Hg, heart rate is 110 beats per minute, weight is 64 kg, creatinine is 1.8 mg/dL against a baseline of 1.0 mg/dL, and potassium is 3.2 mmol/L. Stool culture shows no bacterial pathogen and Clostridioides difficile toxin is negative. Hospital-day-2 colonoscopy shows colitis, and the biopsy is positive for cytomegalovirus. Plasma cytomegalovirus DNA is 8500 IU/mL. Mycophenolate is held. Ganciclovir 5 mg/kg intravenously every 12 hours (330 mg at 66 kg) is given, then stopped. After repletion, discharge weight is 66 kg, creatinine is 0.9 mg/dL, and potassium is 4.0 mmol/L. The pharmacist records creatinine clearance above 60 mL/min, and valganciclovir 900 mg orally twice daily is started. A single 40 mEq potassium chloride dose is not continued. Tacrolimus continues at 1 mg every 12 hours with a trough of 6.5 ng/mL inside a stated target of 5 to 8 ng/mL. Prednisone continues. Transplant says not to restart mycophenolate at discharge.

### Clinical rationale

The antiviral discharge action is to start induction valganciclovir, not to continue a home prescription. Mycophenolate is held because the transplant note says so, not because the old reference continued every home drug. Tacrolimus, prednisone, amlodipine, and atorvastatin continue because the chart says to continue them and the trough and blood pressure support the tacrolimus and amlodipine doses. Standing potassium and intravenous ganciclovir are stopped because the chart shows they have finished. The prior reference, which continued home valganciclovir, is not preserved.

### Evidence

The 2018 international consensus guidelines on cytomegalovirus in solid-organ transplantation describe tissue-based diagnosis of gastrointestinal disease, antiviral induction, and reduction of immunosuppression when possible. Valganciclovir labeling uses 900 mg twice daily when creatinine clearance is at least 60 mL/min. Ganciclovir labeling uses 5 mg/kg every 12 hours for induction. CellCept labeling recommends 1 g orally twice daily after kidney transplantation. The KDIGO transplant guideline describes combination maintenance immunosuppression, commonly including a glucocorticoid. Hypokalemia from gastrointestinal loss is described by Gennari, N Engl J Med. 1998;339:451-458. The viral load, biopsy result, drug doses, and laboratory series are synthetic. The viral load is not the value in the resident source document.

### Provenance

Recorded on the evaluator file. The duration of induction is intentionally unfinished: infectious diseases ties the remaining length to symptoms and the next viral load, and the reference does not invent an end date.

## What was not done

VAL-802 and VAL-803 remain Reviewer-1-only cases. They were not revised. The original freeze, the clean base, and the completed review documents were not edited. No planted discrepancy was added to these four charts.
