# CliniProof: A Framework for Generating and Validating Synthetic Cases for Discharge Medication Reasoning

Working title. Two alternatives are recorded in `docs/paper_revision_plan.md` and are not locked: “CliniProof: Clinician-Informed Generation and Validation of Synthetic Discharge Medication Reasoning Cases,” and the September title, “CliniProof: A Framework for Generating and Validating Synthetic Cases for Medication Reconciliation Assessment.”

Pia Tripathi, Katie Oakes, Alex Sugarman, Matthias Scheutz

Tufts Institute of AI, Tufts Medical

Drafting note. Parenthetical status labels mark what the repository currently implements, what is planned, what is only proposed, and what has been clinically validated. They are for this revision and can be removed in a submission copy. Reviewer names are not used in the method. The author line is the line from the September manuscript.

## Abstract

**Background.** Medication reconciliation at hospital discharge remains safety-critical and difficult to teach and assess at scale. A useful practice case has to give a trainee enough coherent evidence to decide a discharge medication plan. Fluent synthetic text does not by itself supply that evidence.

**Objective.** Develop a reproducible framework for generating clinically coherent synthetic discharge-medication reasoning cases, separating the resident-visible chart from a hidden reference plan, and validating the cases before learner use.

**Methods.** Generation 1 abstracted six resident-provided examples into six reasoning families and built 24 structured synthetic cases. Medication identity used RxNorm, laboratory identity used LOINC, units used UCUM, and stored diagnoses used ICD-10-CM where a code was recorded. The frozen set did not use a language model to choose facts. Two clinicians then reviewed subsets independently with one instrument. Four cases received substantive comments from both clinicians and were revised directly from the clean baseline. Recurring defects were frozen as ten revision domains and applied by investigators to the other twenty clean charts. Two of those twenty also used comments from the clinician who reviewed them; the other eighteen did not. Generation 2 built one independently generated counterpart for each revised Generation 1 case. Synthea supplied longitudinal synthetic context. CliniProof built the inpatient episode, applied sufficiency gates taken from the first review, and derived the hidden discharge reference only after the resident chart existed. No planted medication error was introduced in this clean phase. Both generations are prepared for the same C1–C5 clinician instrument.

**Results.** Generation 1 has 24 clean revised candidate charts. Substantive feedback was recorded for 6 of 24 cases from one clinician and 4 of 24 from the other. The overlap was four cases. Those four were revised from both clinicians’ comments and are pending re-review. The framework was applied to the remaining twenty. None of the revised charts has completed the next clinician review. Generation 2 used a Synthea export of 1,000 living synthetic patients (162 deceased exports excluded; 1,162 FHIR bundles parsed), seed 20261008. Eligibility varied by family, from 11 patients for transplant-associated cases to 787 for endocarditis-context cases. Ninety-six matched episode attempts produced 24 clean cases, G2-001 through G2-024. All 24 passed the automated sufficiency audit. No Generation 1 fact or reference plan was copied. Generation 2 has not been clinically validated.

**Conclusion.** CliniProof separates construction of a synthetic patient, construction of an evidence-sufficient discharge-reasoning case, and clinician validation of that case. Generation 1 shows where archetype-based charts failed and how those failures were repaired. Generation 2 turns the same failures into prospective gates on Synthea-grounded patients. The comparison of which method clinicians judge to be stronger has not been done.

## Introduction

Medication reconciliation is the formal process of assembling the most complete and accurate list possible of a patient's current medications and comparing it against the medications ordered at each transition of care in order to identify and resolve unintended discrepancies (Barnsteiner, 2008; Joint Commission on Accreditation of Healthcare Organizations, 2006; Kwan et al., 2013). The Joint Commission specifies five steps: developing a list of current medications, developing a list of medications to be prescribed, comparing the two, making clinical decisions based on that comparison, and communicating the reconciled list to the patient and subsequent caregivers (Joint Commission on Accreditation of Healthcare Organizations, 2006). Failed reconciliation sends patients home with lists that may duplicate existing drugs or specify wrong doses. These discrepancies at discharge affect a meaningful minority of patients. In a systematic review of 18 hospital-based reconciliation studies that required independent clinician adjudication of severity, Kwan et al. (2013) found that a median of 34% of unintended discrepancies were clinically significant and that 45% of patients had at least one such discrepancy. Coleman et al. (2005), who compared pre-hospital lists, discharge instructions, and the medications actually being taken among 375 older adults within 72 hours of discharge, identified discrepancies in 14.1% of patients and observed that patients with a discrepancy were rehospitalized within 30 days at more than twice the rate of those without one (14.3% vs. 6.1%). Since 2005, the process has been a Joint Commission National Patient Safety Goal and is required for hospital accreditation in the United States and Canada (Barnsteiner, 2008; Joint Commission on Accreditation of Healthcare Organizations, 2006).

Residents and advanced practice providers perform most discharge reconciliation yet receive little deliberate practice with feedback. In teaching hospitals, medication reconciliation on admission, transfer, and discharge is most often carried out by physicians-in-training, who report little or no formal training in eliciting and reconciling a medication history (Boockvar et al., 2011; Ramjaun et al., 2015). A systematic review of trainee-targeted education identified only seven eligible studies, none of which measured objective reconciliation accuracy, and the resident-focused interventions among them produced no measurable improvement in reconciliation skill despite gains in self-reported confidence (Ramjaun et al., 2015). Case-based simulation is a natural mechanism for deliberate practice because trainees can work through controlled, repeatable scenarios and receive structured feedback.

In the problem-based learning tradition, a clinical case presents a coherent patient encounter, structured to trigger clinical reasoning rather than to display isolated facts. Traditionally, such cases were written by hand. Faculty distilled real or hypothetical encounters into vignettes, a process that scales poorly to the volume and variety a competency-based curriculum demands (Thomas et al., 2015). A faculty author may produce only a handful of vetted cases in a month. Synthetic generation can increase supply. Supply is not the only problem. A discharge-reasoning case is useful only when the trainee can independently determine an appropriate discharge medication plan from the chart. That requires a clinically coherent trajectory: a baseline state, an acute illness, a diagnostic work-up, treatment, a physiologic response, medication transitions, and a visible account of discharge readiness. A fluent vignette can fail every one of those requirements and still look like a case.

This paper describes CliniProof, a provenance-aware framework for generating those cases and for validating them before any learner uses them. The work has two generations. They are not a claim that one generation is better.

Generation 1 starts from resident-informed clinical archetypes, builds clean synthetic hospitalizations, and then uses clinician review to repair failures of clinical sufficiency. Generation 2 builds a matched counterpart for each revised Generation 1 case. Synthea provides the longitudinal synthetic patient. CliniProof constructs the inpatient reasoning episode and applies the lessons of the first review as prospective constraints. Both generations are intended to be read with the same clinical validation instrument. The instrument has been used once, on incomplete coverage of the original Generation 1 charts. It has not yet been used to accept the revised charts or any Generation 2 chart.

The aims are:

1. Define a structured framework for clean synthetic discharge-medication reasoning cases with a hidden evidence-backed reference. Status: IMPLEMENTED.
2. Use clinician review to identify failures of clinical sufficiency and to remediate them in a traceable way. Status: IMPLEMENTED for case revision; the revised charts are not VALIDATED.
3. Develop a second-generation Synthea-grounded matched generator that incorporates those failure modes prospectively. Status: IMPLEMENTED as a candidate cohort.
4. Establish a design that permits a later blinded comparison of the two generation approaches with the same instrument. Status: PROPOSED. The comparison has not been conducted. A blinded casebook has been prepared.

The study does not demonstrate that the Synthea-grounded method is superior.

## Background and Related Work

### Post-discharge medication safety and reconciliation systems

Despite the mandate, the period following discharge remains one of the least protected points in the medication-use process. In a systematic review of post-discharge medication safety, Alqenae et al. (2020) pooled 54 studies covering 20,895 discharges and found that a median of 53% of adult patients experienced at least one medication error and 50% at least one unintentional discrepancy after returning home, with 19% experiencing an adverse drug event. The drug classes most often implicated, including cardiovascular agents, antidiabetics, antibiotics, and analgesics, overlap with those Coleman et al. (2005) identified earlier.

Reconciliation systems may help, and they are expensive. Bishop et al. (2015), studying a hospitalist service where residents and attendings performed discharge reconciliation, found that a single pharmacist's review identified discrepancies in 41% of patients, most often therapeutic duplication or omission, but required up to 45 minutes per patient. Killin et al. (2021), reviewing ten studies, found that electronic or enhanced reconciliation reduced discrepancies and adverse drug events. The reconciliation studied in published trials is performed predominantly by pharmacists, whereas in routine practice the task often falls to physicians, including residents, whose competence is rarely assessed directly (Kwan et al., 2013).

### Review and feedback on trainee reconciliation

Faculty review of trainee reconciliation reasoning is labor-intensive, unstandardized, and rarely timely. Residents and pharmacists describe reconciliation as a task displaced by competing priorities and completed without anyone checking its quality (Boockvar et al., 2011). Even a well-received case-based curriculum illustrates the gap: residents who received real-time group feedback reached 100% accuracy on a reconciliation task, whereas those completing it independently reached only 41%, and program evaluation depended on chief residents manually auditing a handful of charts (McShane & Stark, 2018). Interventions shown to reduce discrepancies rely on intensive pharmacist involvement rather than on developing prescribers' own competence, and the literature offers no scalable mechanism for reviewing trainee reasoning at the point of care (Mueller et al., 2012).

### Case-based simulation and case-based learning

Case-based simulation is an established method for teaching medication reconciliation and one of the few with evidence of improving performance rather than confidence alone. Trainees reconcile medications from conflicting sources and must resolve discrepancies (Lindquist et al., 2008; Ramjaun et al., 2015). The format descends from problem-based learning (Barrows & Tamblyn, 1980; Norman & Schmidt, 1992). In a randomized comparison, students who completed a lecture plus a case workshop outscored lecture-only and control groups on a blinded standardized-patient reconciliation (Komperda & Lempicki, 2019). The conditions that separate effective from ineffective implementations are also clear. Cases must be realistic, and trainees must receive feedback on their reasoning (Boockvar et al., 2011; Ramjaun et al., 2015). Both conditions are resource-bound. A single well-constructed case takes faculty time to build.

### Structured synthetic health records and longitudinal patient simulation

Synthetic data, generated by a model rather than collected from real patients, have been proposed as a way to expand access to realistic material while limiting privacy exposure. Education is one proposed use (Gonzales et al., 2023). Longitudinal synthetic health records are a different object from a stand-alone vignette. Synthea is an open-source simulator that generates synthetic patients and lifetime electronic health records from public statistics and models of care, encoded in standard formats including HL7 FHIR (Walonoski et al., 2018). A Synthea patient has an age, a sex, a problem list, outpatient medicines, and prior encounters because a longitudinal model produced them. A vignette has those elements because an author or a language model wrote them into one scene.

That difference matters for discharge reasoning, and it does not solve discharge reasoning. A longitudinal record can be thin at the moment of an acute hospitalization. It may lack the baseline laboratory value, the precipitant, the confirmatory test, or the inpatient medication timeline that a discharge decision needs. CliniProof therefore treats Synthea as a source of longitudinal context, not as an author of the inpatient episode. Additional synthetic-EHR systems beyond Synthea are relevant background and are not cited here. [CITATION NEEDED]

### Language-model vignettes as a comparison, not the foundation

Large language models can produce clinical vignettes that experts rate as usable for instruction (Rao et al., 2025; Emekli et al., 2026). Generation strategies differ in how tightly they are anchored to real data, from conditioning on trial questionnaires (Cayres Ribeiro et al., 2026) to training on registry codes (Chung et al., 2023) to sequential prompts that randomize patient attributes (Bakkum et al., 2024). Expert review remains necessary, and no standard method yet exists for validating synthetic clinical content (Gonzales et al., 2023). Published evaluations vary in sampling, prompts, and statistics (Ruggiano et al., 2026; Takahashi et al., 2024; Yanagita et al., 2024; Abidi et al., 2026). Language-model output is also prone to characteristic errors (Gorenshtein et al., 2025; Zhang et al., 2025).

Those studies motivate skepticism about untreated synthetic text. They are not the technical foundation of the current CliniProof pipeline. Three objects should stay distinct.

A language-model vignette is a piece of clinical prose. A structured synthetic patient is a longitudinal record with a stated generative model and a provenance trail. A controlled assessment case is a resident-visible hospitalization that supports a discharge medication decision, paired with a hidden reference that can be defended from that hospitalization. CliniProof builds the third object. Generation 1 does it from archetypes. Generation 2 does it from Synthea patients. Neither current cohort uses a language model to select a diagnosis, a drug, a dose, a route, a frequency, a laboratory value, or a reference action.

### Structured iterative clinician review

Expert review is the appropriate check on synthetic educational cases, because clinical sufficiency has no single external gold standard. Delphi procedures are one formal way to turn distributed expert judgment into a consensus, with a predefined statistical rule (Nasa et al., 2021). Modified Delphi procedures have been used to build simulation-scenario standards, including the Simulation Scenario Evaluation Tool (Hernandez et al., 2020; see also Arthur et al., 2012; Cumyn & Harris, 2012).

The review completed for CliniProof is not a classical Delphi study and is not a modified Delphi with a predefined item pool and a consensus threshold. It is a structured iterative clinician review. It can be called Delphi-informed only in the weak sense that independent clinicians used one instrument and their responses were compared before a later round. Two clinicians reviewed subsets of the same 24 cases. Coverage was incomplete. Agreement was described case by case. Silence was not treated as agreement. No kappa was calculated. The four cases with substantive comments from both clinicians were the development subset for direct revision and for the quality requirements that followed. That panel cannot establish that the cases are valid assessment items.

## Methods

### A synthetic case is a controlled reasoning environment

Status: IMPLEMENTED for the case representation; learner administration is PLANNED.

A CliniProof case is not a vignette that happens to mention medicines, and it is not a chart with a pre-specified planted error. It is a controlled clinical reasoning environment in two layers.

Layer 1 is the resident-visible clinical case. It contains demographics, presentation, relevant longitudinal history, the hospital course, diagnoses, laboratories and vital signs, home medications, the inpatient medication timeline, diagnostic studies and consultations, discharge status, and follow-up context. It does not contain a completed discharge medication list. The resident's task is to derive that plan from Layer 1.

Layer 2 is the hidden reference. It contains reference discharge medication actions, rationales, pointers to resident-visible evidence, monitoring, follow-up, acceptable alternatives where more than one action is defensible, and provenance. The reference is written after Layer 1 is complete. The chart is not written backward from a desired answer.

This is a different task from asking a resident to find a planted error in a discharge list that has already been supplied.

**Table 1. Resident-visible case layer.**

| Clinical construct | Structured representation | Resident visible? | Purpose |
| --- | --- | --- | --- |
| Patient demographics | Age, sex, weight | Yes | Set the clinical context |
| Presentation | Chief complaint, history of the present illness, symptoms | Yes | Show why the patient is in the hospital |
| Baseline clinical state | Premorbid function, prior cognition, prior weight or laboratory baseline when the decision needs it | Yes | Separate baseline from the acute change |
| Relevant prior diagnoses | Problem list and past history drawn from the archetype or the longitudinal record | Yes | Constrain which medicines are plausible |
| Home medication history | Outpatient products and the best possible medication history | Yes | State what the patient was taking |
| Inpatient medication timeline | Continued, held, hospital-only, new, substituted, restarted, and discontinued orders | Yes | Show what changed in the hospital and why |
| Diagnostic work-up | Laboratories, imaging, microbiology, consultations | Yes | Support diagnoses that bear on discharge medicines |
| Laboratory trajectory | Baseline, admission, intermediate, and discharge values as the scenario requires | Yes | Support holds, restarts, and dose decisions |
| Vital trajectory | Admission and discharge vital signs, and intermediate values when the course needs them | Yes | Support volume status, perfusion, and discharge readiness |
| Hospital treatment | Timed acute therapy, distinct from the home list when the acute problem requires it | Yes | Show the response the discharge plan inherits |
| Clinical response | Change in symptoms, weight, cultures, or laboratories after treatment | Yes | Justify stopping, continuing, or restarting |
| Discharge readiness | The chart's own stability criterion | Yes | Show why discharge is being considered |
| Monitoring context | What must be watched, without giving the signed discharge list | Yes | Make follow-up obligations visible |
| Follow-up context | Service and timing | Yes | Bound supply and restart decisions |
| Disposition | Home or another destination | Yes | Set the care setting |
| Completed discharge medication list | Not stored on the resident chart | No | The resident must construct it |

**Table 2. Hidden reference layer.**

| Field | Role |
| --- | --- |
| Medication | The product the action concerns |
| Reference action | Continue, stop, restart, hold, dose change, or new start |
| Dose, route, and frequency | Included when the action specifies them; taken from the curated regimen or the visible chart, not invented at scoring time |
| Indication | Why the medicine is in play |
| Rationale | Why this action follows from the chart |
| Resident-visible evidence | The facts in Layer 1 that defend the action |
| Monitoring | What the reference expects to be watched |
| Follow-up | The visit or check the reference expects |
| Acceptable alternatives | Another defensible action, the condition, and the reason, when more than one action follows from the same facts |
| Provenance | Whether the supporting fact came from the longitudinal record, the episode generator, terminology, or an investigator-derived reference |

### Future experimental perturbation layer

Status: PLANNED. Not part of the current clean cohorts.

The repository still contains a two-family taxonomy of medication-reconciliation discrepancies, adapted from the MATCH toolkit and from transitions-of-care work (Gleason et al., 2012; National Coordinating Council for Medication Error Reporting and Prevention, 2026; Bajorek & McElroy, 2020; Forster et al., 2003). Family 1 covers omission, unintended addition, dose or route or frequency discrepancy, and therapeutic substitution. Family 2 covers monitoring gaps, missing restart plans, insufficient supply, hospital-only medicines continued after discharge, and related transition gaps. The historical Generation 1 freeze assigned a planted discrepancy to 20 of 24 slots and left four as clean controls. That freeze is provenance. It is not the current resident-facing cohort.

The current method requires the opposite order. The base case is accepted as clinically coherent first. Only then may a controlled discrepancy be introduced for an experiment. Otherwise a reviewer cannot tell a bad case from a bad error. The taxonomy remains available for that later layer. It does not define the base case.

The intended sequence is:

```text
clean case
        ↓
clinical validation
        ↓
locked reference
        ↓
optional experimental perturbation
        ↓
resident reasoning study
```

The last three arrows are PLANNED. No resident study has been run.

### Clinical-sufficiency requirements

Status: IMPLEMENTED as revision domains and as automated gates. Not VALIDATED by a completed second clinician review.

Generation 1 formalized ten domains from the four doubly reviewed cases. The names are the names in the frozen framework.

**Table 5. Clinical-sufficiency domains used to revise Generation 1 and to gate Generation 2.**

| Domain | What must be true | Where it is implemented |
| --- | --- | --- |
| Presentation and diagnosis coherence | The arrival problem matches how that illness presents. A diagnosis established by testing is not the arrival label. | Frozen framework |
| Causal context | The chart states why this hospitalization happened. | Frozen framework; Generation 2 precipitant sufficiency |
| Diagnostic work-up | Studies that explain the presentation and that bear on discharge medicines are present, with results. | Frozen framework; Generation 2 diagnostic-work-up check |
| Treatment trajectory | Acute treatment is timed and is not a silent copy of the home list when the acute problem requires different treatment. | Frozen framework |
| Laboratory and vital trend | A value used to hold, restart, or dose a medicine is shown when that decision needs it, including a baseline when a change is claimed. | Frozen framework; Generation 2 physiologic coherence |
| Hospital-course completeness | The short series that shows why the patient can leave is visible. | Frozen framework; Generation 2 hospital-course check |
| Medication-decision support | A resident can see why each discharge action would be continue, start, stop, hold, restart, or change. | Frozen framework; Generation 2 medication-decision check |
| Discharge stability and chronology | Events are in a possible order, and the chart's own stability criterion is met. | Frozen framework; Generation 2 chronology check |
| Internal consistency | Narrative, medication rows, laboratories, and the reference describe the same events. | Frozen framework |
| Unsupported hidden-reference action | Every hidden discharge action can be defended from the resident-visible text alone. | Frozen framework; Generation 2 reference-support check |
| Answer leakage | The resident chart does not contain a finished discharge list or a scoring label. | Generation 2 answer-leak check |
| Baseline sufficiency | The baseline state required to interpret the acute change is visible. | Generation 2 baseline check |

Passing an automated check does not clinically validate the case.

Educational appropriateness, in the sense of whether the reasoning demand suits an internal-medicine resident, is an item on the clinician instrument (C5). It is not an automated gate.

Educational appropriateness, in the sense of whether the reasoning demand suits an internal-medicine resident, is an item on the clinician instrument (C5). It is not an automated gate.

### Generation 1: resident-seed-guided case construction

Status: IMPLEMENTED. The revised charts are candidate revisions, not VALIDATED cases.

Generation 1 did not copy patient records. Six resident-provided clinical documents were design inputs. They were abstracted into six reasoning families and stored as archetypes. Four synthetic profiles were written for each family, producing 24 study slots, VAL-801 through VAL-824. Profiles differ in symptoms, hospital course, which medicine is held or started, and what follow-up is arranged. Four profiles are a design choice, not a prevalence weight. The resident examples are not a sample of how often a problem occurs.

**Table 3. Generation 1 reasoning families.**

| Display name | Generation 1 code | Slots | What the resident must reason about |
| --- | --- | --- | --- |
| Medication history uncertainty | MEDREC_UNCERTAIN_HISTORY | VAL-801–VAL-804 | An acute change, an initially uncertain outpatient list, and which medicines continue, stop, or restart |
| Acute heart-failure decompensation | HF_DECOMPENSATION | VAL-805–VAL-808 | Diuresis, volume status, and heart-failure therapy at discharge |
| Outpatient parenteral antibiotic therapy after endocarditis | OPAT_ENDOCARDITIS | VAL-809–VAL-812 | How endocarditis was established and what antimicrobial plan can leave the hospital |
| Post-kidney-transplant infectious complication | TRANSPLANT_CMV | VAL-813–VAL-816 | Symptom-to-diagnosis order, cytomegalovirus therapy, and immunosuppression |
| Postoperative anticoagulation after hip fracture | POSTOP_ANTICOAGULATION | VAL-817–VAL-820 | Holding and restarting anticoagulation around hip-fracture repair |
| Gastrointestinal bleed with anticoagulation decisions | GI_BLEED_ACUTE_CHANGE | VAL-821–VAL-824 | Holding antithrombotic therapy for bleeding and deciding the restart |

Concepts were resolved through source-backed terminology. Medication identity comes from RxNorm. Laboratory identity comes from LOINC. Units come from UCUM. Diagnosis text uses ICD-10-CM where a code is stored. Symptom names come from NLM Clinical Tables, with the Human Phenotype Ontology as a fallback, and are not given invented SNOMED codes. Dose, route, and frequency come from a curated regimen table, not from copying an RxNorm product strength into a dose. Age, sex, weight, vital signs, and laboratory numbers are synthetic. Narrative sentences in the frozen set are template wording. The batch plan states that OpenAI was not used. A later development option may reword a sentence from the same facts. It may not add a diagnosis, a medicine, or a number. That option was not used for the frozen set.

The historical freeze, stored as CLINIPROOF_SEEDCASES_V3, is the same 24 slots that reviewed casebooks labeled CLINIPROOF_SEEDCASES_FirstRound. Twenty of those frozen charts carried one planted discrepancy. Four were clean controls. The current work does not use those planted-error files as the charts under revision. The clean pre-manipulation baseline was recovered and stored separately. Revised charts are derivatives of that baseline.

### Clinician review of Generation 1

Status: IMPLEMENTED as one incomplete round. Not a consensus panel.

Two clinicians completed the same validation casebook independently. The instrument was not revised between them, so later ratings can be compared with ratings already recorded. Completed forms are private study records. The public record is a de-identified comparison.

One clinician left substantive case-level feedback on 6 of 24 cases: VAL-801, VAL-802, VAL-803, VAL-805, VAL-809, and VAL-813. Eighteen cases have no substantive completed feedback. VAL-803 has a completed plausibility rating. The later ratings and the overall recommendation on that case are blank and were left blank.

The other clinician left substantive feedback on 4 of 24 cases: VAL-801, VAL-805, VAL-809, and VAL-813. On those four, the later items and the overall recommendation are blank and were not inferred. Twenty cases have no selected ratings and no comments.

The overlap is four cases: VAL-801, VAL-805, VAL-809, and VAL-813. On domain scores where both clinicians recorded a single response, exact agreement was 11 of 31 pairs (35%), and the mean absolute difference was 0.77. Overall plausibility agreed on 3 of 4 cases. The disagreement was VAL-805. These counts are descriptive. They are not a kappa and not a consensus threshold.

On VAL-805, one clinician failed plausibility and failed the detectability item. That clinician also marked both 2 and 3 on the medication-regimen domain, which is recorded as a double tick rather than resolved to one score. The other clinician marked plausibility as Pass. That Pass conflicts with that clinician's own score of 2 on fit between presentation and diagnosis, because the form rule is that any domain scored 1 or 2 makes plausibility Fail. The conflict is reported. It is not corrected.

### Direct revision of the four overlap cases

Status: IMPLEMENTED as candidate revisions. Pending clinician re-review. Not VALIDATED.

The four overlap cases were revised from the clean baseline using both clinicians' comments. Recurring concerns, stated at the level of the revision log rather than as a new consensus, were these.

VAL-801. The delirium story did not show a cognitive baseline or a precipitant, and the reason for stopping ibuprofen was not visible.

VAL-805. The heart-failure hospitalization did not show why the patient decompensated, used an inpatient diuretic course that repeated the home dose, did not show a volume trajectory to dry weight, and did not set up a heart-failure therapy decision. Renal and electrolyte context for that decision was thin. One clinician failed plausibility and the detectability item.

VAL-809. The endocarditis chart needed fever and a predisposition, a source evaluation, laboratory course, imaging, and a statement about surgery. One clinician wrote that acute kidney injury was unexplained and that lisinopril continued despite it.

VAL-813. The patient arrived already labeled with cytomegalovirus colitis, valganciclovir was already a home medicine, the transplant regimen was too thin, and the potassium change was described in the recorded comment as a “change in potassium with obvious cause or indication.” Treating that phrase as “unexplained” is an interpretation; the recorded wording likely intended “without.” Volume status, kidney function, and immunosuppression were part of the same gap.

The revised charts add the missing baseline, precipitant, work-up, and medication rationale, and they rewrite the hidden reference from the revised resident-visible text. New patient-specific values are synthetic and are labeled as such on the evaluator file. The resident file does not contain the reference plan. These four cases are revised from dual-clinician feedback and are pending re-review. They are not validated cases.

### The frozen revision framework

Status: IMPLEMENTED as an investigator procedure. Not additional clinician validation.

The sequence was:

```text
four cases with substantive comments from both clinicians
        ↓
direct case-level revision
        ↓
recurring sufficiency defects named as ten domains
        ↓
framework frozen
        ↓
framework applied unchanged to the other twenty clean charts
```

The framework was not relaxed to make a later case fit. A domain with no defect was recorded as pass and was not revised. A finished discharge medication list was kept off the resident chart.

VAL-802 and VAL-803 had substantive comments from only one clinician. They are not consensus cases. Their revision used those comments together with the frozen framework. The comparison record marks that track as reviewer-specific feedback plus the framework. The other eighteen cases had no case-specific clinician comment. Their revision is framework-guided investigator revision. It is not a clinician review of those eighteen charts, and it is not validation.

### Generation 2: Synthea-grounded matched case generation

Status: IMPLEMENTED as 24 clean candidate cases. Clinician validation is PLANNED and has not occurred. No clinician has approved Generation 2.

```text
Synthea population
        ↓
scenario-specific eligibility
        ↓
longitudinal synthetic patient
        ↓
Generation 1 matching profile
        ↓
CliniProof controlled inpatient episode
        ↓
clinical sufficiency gates
        ↓
hidden reference derivation
        ↓
candidate selection
        ↓
clinician validation
```

The last arrow is the intended next review. It is not a completed result.

Synthea was pinned to commit d9d07a6eef91ee5144293b42ab64224d84d124f8, seed 20261008, reference date 20261008, FHIR R4, ten years of history, Massachusetts. The run requested 1,000 living patients. Deceased exports are additional and were excluded: 1,162 bundles were parsed, 1,000 living and 162 deceased. Bulk FHIR is not in the public repository.

### What Synthea supplies and what CliniProof supplies

Synthea supplies longitudinal synthetic context when the export contains it: age, sex, chronic and prior diagnoses, outpatient medication products, recent encounters, selected observations, procedures, and care-plan titles. CliniProof supplies the acute hospitalization: precipitant, presentation, diagnostic work-up, diagnosis, treatment, hospital course, laboratory and vital trajectory, medication transitions, and discharge state.

Provenance is stored on episode facts. A fact is labeled as coming from the longitudinal record only when it was in the extract. Acute precipitants, hospital laboratories, imaging interpretations, medication holds, and responses are labeled episode-generated unless a value was actually present. The paper does not claim that Synthea generated the inpatient diagnostic findings.

Two families show the boundary. Endocarditis was not present in this Synthea population. Eligibility for that family is baseline context only, and the infection is episode-generated. Heart-failure eligibility prefers an active Synthea heart-failure condition. In this living cohort that pool was 4 patients. The scenario also accepted a compatible cardiovascular history plus a curated cardiovascular medicine (257 patients). The inpatient episode then establishes acute heart failure during the stay and does not relabel the patient as having had Synthea heart failure. Transplant eligibility required a Synthea renal-transplant history and a matching extended-release tacrolimus product (11 patients). Mycophenolate was not added because it is common. Valganciclovir was not placed on the home list unless a variant explicitly included prior prophylaxis, and that prophylaxis is labeled episode-generated.

### The matched design

Status: IMPLEMENTED as a design and as 24 selected pairs. The clinical comparison is PROPOSED.

Generation 1 identifiers VAL-801 through VAL-824 map one-to-one onto Generation 2 identifiers G2-001 through G2-024. VAL-801 is the counterpart of G2-001, and the numbering continues through VAL-824 and G2-024. Generation 2 identifiers are candidate identifiers. They are not VAL study identifiers.

Matching targets the reasoning problem: scenario family, primary reasoning task, approximate number and type of important medication decisions, monitoring burden, follow-up burden, and approximate complexity. It does not match exact age, exact laboratories, the exact medication list, the same precipitant, the same patient, the same hidden reference, or the same narrative. The purpose is to match the decision, not to reproduce the answer.

**Table 6. What a pair is, and is not, matched on.**

| Dimension | Matched? |
| --- | --- |
| Reasoning family | Yes |
| Primary discharge-reasoning task | Yes |
| Approximate decision types and monitoring burden | Yes, approximately |
| Exact age, laboratories, or medication list | No |
| Same precipitant, patient, narrative, or hidden reference | No |
| Copied Generation 1 facts or reference plan | No; the pair audit recorded none |

An automated pair audit recorded family, decision, monitoring, and difficulty agreement for all 24 pairs, with no copied facts and no copied reference. That audit is a generation check. It is not a clinician comparison.

### Round 1 concerns as prospective constraints

Status: IMPLEMENTED as generator gates. The gates themselves have not been clinically VALIDATED.

The first review is the source of the gates. It is not an endorsement of Generation 2. A failed gate rejects or blocks a candidate. It does not add a cosmetic sentence after selection.

**Table 4. Round 1 deficiency and the Generation 2 design response.**

| Round 1 observed deficiency | Generation 2 prospective design response |
| --- | --- |
| Baseline versus acute state unclear, including delirium without a baseline | Explicit baseline and an acute deviation are required when the syndrome needs them |
| Precipitant absent, including heart failure described only as exacerbation and improvement | A precipitant, or a documented evaluation that did not find one, is required |
| Diagnosis appears without work-up, including endocarditis or cytomegalovirus labeled on arrival | The confirmatory studies precede the specific diagnosis |
| Hospital course too thin to show treatment and response | A treatment trajectory and a response are required |
| Relevant physiology absent or contradictory | A scenario-specific laboratory and vital trajectory is required |
| Medication decision unsupported | Every important discharge action maps to resident-visible evidence |
| Chronology runs backward | An event-timeline check rejects impossible order |
| The chart does not contain enough information for a discharge decision | A pre-selection sufficiency gate blocks the candidate |

The concrete patterns these gates are meant to prevent are a delirium story without baseline cognition, a heart-failure story that is only “exacerbation, diuresis, improved,” an endocarditis label without cultures and echocardiography, and a cytomegalovirus label that appears before the work-up. New patients are not copies of VAL-801 through VAL-824.

### Laboratory, vital, and medication trajectories

Status: IMPLEMENTED in Generation 2.

Laboratory and vital values are trajectories, not independent draws. The states used, when the decision needs them, are baseline, admission, an intermediate peak or nadir, and discharge. An acute-kidney-injury course must show a peak and a later value no higher than that peak. A bleeding course must show a hemoglobin nadir and a later value at or above it. A diuresis course must lose weight. An infection is not required to have fever. The requirement is coherence with the stated physiology, not a textbook curve.

Medication state is temporal: home, continued inpatient, held, hospital-only, new inpatient, substituted, restarted, discontinued, and candidate discharge therapy. A change stores a trigger, the decision, the visible evidence, and the final state. Hospital-only medicines stop. A held medicine has a final disposition. Doses come from the curated regimen table. A Synthea product is charted only when the curated dose is the strength named on that product. Product strength is not otherwise copied into the dose. This representation is what makes the discharge reasoning task inspectable: each transition can be pointed at.

### Hidden reference derivation

Status: IMPLEMENTED.

The hidden reference is derived after the resident-visible chart exists. For each relevant medicine the question is what discharge action the visible case supports: continue, stop, restart, hold, dose change, or new start. Each action stores the regimen, the rationale, resident-visible fact identifiers, monitoring, and follow-up. Terminology codes do not establish that a decision is appropriate. Guidelines cited in the scenario file constrain the shape of the work-up and the monitoring. They are not the source of a patient's creatinine.

If the visible chart does not support an action, the candidate is not rescued by writing the chart backward. The case is revised, the reference is changed, an acceptable alternative is encoded, or the candidate is rejected.

### Acceptable alternatives

Status: IMPLEMENTED in the reference record.

Discharge medicine does not always have one exact action. When more than one action follows from the same visible facts, the reference records the other action, the condition, and the reason. A reasonable alternative is not marked wrong because the generator preferred another action. This is a validity choice. It refuses false precision. It is not a statement that every action is acceptable.

### Candidate generation and selection

Status: IMPLEMENTED counts below. They are automated counts, not clinician outcomes.

Generation 2 did not keep the first eligible patient. For the matched cohort, 96 episode attempts were run, four for each Generation 1 target, across distinct variants where the scenario allowed. Exact or high-similarity structural fingerprints were rejected. A different age or sex alone was not treated as diversity. The final set keeps four cases in each family, 24 cases. If a family could not fill four passing cases, the build was specified to stop rather than to loosen a constraint.

Eligibility among the 1,000 living patients was 32 for medication-history uncertainty, 261 for heart-failure decompensation (4 with known Synthea heart failure and 257 with compatible cardiovascular context), 787 for endocarditis context only, 11 for transplant with matching tacrolimus, 13 for older adults with warfarin eligible for the hip-fracture scenario, and 15 for warfarin with an indication eligible for the bleeding scenario. All 24 selected cases passed every column of the automated validation report, including causal completeness, the sufficiency gates, chronology, reference support, the answer-leak check, diversity, and provenance. `ready_for_clinician_review` is true. `clinically_validated` is false.

No language model selected the diagnosis, drug, dose, route, frequency, laboratory value, or reference action. Generation 2 does not call an external language-model API. It does not use MIMIC.

### Clinical validation instrument

Status: IMPLEMENTED as the review form. A second round of ratings has not been collected.

The instrument is the C1–C5 codebook used for the first review. It was not redesigned. Clean cases, which include all revised Generation 1 charts and all Generation 2 charts, use the clean-case questions. The historical template also contains different questions for error-bearing cases. Those questions are not used for the current clean books.

**Table 7. Clean-case validation instrument, in the wording of the current template.**

| Item | What the clinician records |
| --- | --- |
| C1, clinical plausibility | Could this reasonably represent a patient encountered in the stated inpatient clinical setting? Eight domains, each scored 1 to 4: presentation and demographics; fit between presentation and diagnosis; vital signs; laboratory findings; medication regimen; hospital course; consistency across the chart; discharge plan and follow-up. A rating of 1 is implausible. A rating of 2 is questionable and requires revision. A rating of 3 is plausible with minor concern. A rating of 4 is fully plausible. Any domain rated 1 or 2 needs a written explanation. C1 passes when every clinically relevant domain is rated 3 or 4. Overall Pass or Fail, plus a comment. |
| C2, intended assessment problem | Does this case appropriately contain no deliberately introduced medication-reconciliation or transition-of-care problem? Pass or Fail, plus a comment. |
| C3, detectability | Does the case avoid misleading cues suggesting that an error must exist? Pass or Fail, plus a comment. |
| C4, competing problems | Does the case contain any clinically meaningful medication-reconciliation or transition-of-care problem that should not be present? Pass or Fail. If C4 fails, the clinician names the medication or clinical issue, where it appears, and why it is clinically meaningful. |
| C5, expected difficulty | Easy, Moderate, Hard, or Inappropriate / outlier. This is an expert estimate. Actual difficulty requires resident performance, which has not been collected. |
| Overall recommendation | Accept: suitable without clinically meaningful revision. Revise: one or more changes are required before use. Exclude: the case should not be used, because its problems cannot be reasonably corrected without substantially reconstructing it. |
| Blanks | A blank field stays blank. Reviewer initials and the date are separate fields on the form. |

### Validation order

Status: IMPLEMENTED as the written review protocol. Not a software lock.

The casebook instructs the clinician to read the chart, complete C1 before using the case-specific validation reference, then read the reference, then complete C2 through C5 and the overall recommendation. The instruction exists so that the hidden plan does not decide the plausibility rating. A Word document does not prevent a reviewer from scrolling. The order is the protocol, not an enforced blind.

### Proposed comparison of Generation 1 and Generation 2

Status: PROPOSED. No results.

The paired question is whether a Synthea-grounded, trajectory-based method produces clinically stronger discharge-reconciliation cases than the revised archetype method when the cases are matched on reasoning task and read with the same instrument. Outcomes that could be compared, and that have not been compared, include clinical plausibility, information sufficiency, internal consistency, diagnostic sufficiency, medication-decision support, reference-plan defensibility, expected difficulty, the accept/revise/exclude decision, and the number and type of requested revisions. No statistic for that comparison is reported, because the comparison has not been done.

### Blinding for that comparison

Status: a blinded casebook is IMPLEMENTED. The blinded review is PROPOSED.

A paired casebook places all 48 charts in pair order and randomizes order within each pair with a fixed seed. The chart shows a neutral identifier. It does not show VAL or G2 identifiers, the family code, Synthea, or the generation method. An investigator-only key maps the neutral identifiers back to the source cases and is not part of the reviewer packet. Preparation of that document is not a completed blinded study.

### Intended workflow, dashboard, and scoring

Status: mixed. Case construction and automated checks are IMPLEMENTED. Clinician-validation materials are IMPLEMENTED. Resident administration and scoring are PLANNED.

Stage 1, case construction. Generate a structured clean candidate, either from an archetype or from a Synthea-grounded episode.

Stage 2, automated sufficiency and provenance checks. Check chronology, medication evidence, reference support, and answer leakage. A pass marks the case ready for clinician review. It does not validate it.

Stage 3, clinician validation. The clinician uses C1–C5 and recommends accept, revise, or exclude. One incomplete round has been completed on the original Generation 1 charts. The revised charts and the Generation 2 charts are waiting for the next round.

Stage 4, resident administration. PLANNED. A resident would receive Layer 1 only and would construct the discharge medication plan and the reasoning for it. A resident review dashboard is described in the software as planned and is not implemented. The intended screen shows the clinical chart, home medications, inpatient medications, course, laboratories, vital signs, and follow-up context. It does not show a correct discharge list before submission. The September design, in which the resident compared a supplied discharge list with the home and inpatient lists, does not match this task.

Stage 5, scoring and calibration. PLANNED. The intended comparison is between the resident's proposed plan and the locked hidden reference. Medication-level categories that could be used, and that are not an implemented scorer, are: the reference action, an acceptable alternative, an unsafe or unsupported action, and omission of a required action. Argumentation-graph scoring and a five-dimension competency profile are not part of the implemented system and are not claimed here. Empirical difficulty and discrimination require resident responses that have not been collected.

## Results

Results below are implementation and first-round review facts. They are not acceptance rates for the revised library, and they are not Generation 2 clinician outcomes.

### Generation 1

Twenty-four clean baseline charts, VAL-801 through VAL-824, are preserved. Twenty-four revised candidate charts exist, each with a resident file and an evaluator file. The resident files do not contain the hidden reference.

Substantive clinician feedback covered 6 of 24 cases for one reviewer and 4 of 24 for the other. Four cases were in both sets and were revised directly from those comments. A ten-domain framework taken from that revision was applied to the other twenty. VAL-802 and VAL-803 also incorporate the comments of the one clinician who reviewed them. The other eighteen were revised from the framework alone. No revised chart has completed clinician re-review. The historical planted-error freeze remains stored and was not the revision baseline.

### Generation 2

The Synthea run produced 1,162 FHIR bundles: 1,000 living patients and 162 deceased patients who were excluded. Family eligibility counts were 32, 261, 787, 11, 13, and 15, as detailed in the methods. Ninety-six matched episode attempts yielded 24 clean cases. The automated audit passed on all 24, including reference support and the answer-leak check. The pair audit found no copied Generation 1 facts and no copied reference plans. `clinically_validated` is false for the cohort. No clinician rating of Generation 2 is reported because none has been collected.

## Discussion

The principal difficulty in a synthetic discharge-reasoning case is not fluent clinical text. It is keeping cause, time, and the medication decision coherent, while making sure the expected discharge plan can be justified entirely from information the learner can see.

Generation 1 showed where archetype-based charts failed that test. Clinicians who reviewed the overlap cases asked for a baseline, a precipitant, a work-up that precedes the diagnosis, a treatment course that is not a copy of the home list, and a medication change that the chart itself explains. Those requests recurred across delirium, heart failure, endocarditis, and transplant infection. They are structural, not cosmetic.

The frozen framework is a way to apply that lesson without pretending that two clinicians reviewed all 24 cases. It is also a limitation. An investigator applying a written rule is not a clinician accepting a chart.

Generation 2 moves the same lesson from repair to design. The gates require the missing pieces before a case is kept. Synthea adds a longitudinal patient who already has medicines and diagnoses, which is a better starting point than an empty vignette. Synthea does not, in this implementation, write the acute hospitalization. Where the export had no endocarditis, or almost no living patients with heart failure, CliniProof generated the episode and labeled it as such. Longitudinal realism is not inpatient validity.

The matched design makes the generation strategy testable later. Because the pairs share a reasoning task and not a hidden answer, a future review can ask which method produced the more sufficient case. That review has not been done. Until it has, neither generation should be described as the better one, and neither revised nor Generation 2 chart should be described as validated.

## Limitations

The cases are synthetic. They are built for a reasoning task. They are not de-identified hospital encounters.

Only six reasoning families are represented. Four profiles per family do not estimate how often a problem occurs on a medicine service.

The expert panel had two clinicians. The first round covered 6 and 4 of 24 cases. Four doubly reviewed cases formed the development subset. Silence on the other cases is missing review, not agreement. No consensus threshold was defined.

Propagation of the framework to the other charts was investigator-led. VAL-802 and VAL-803 add one clinician's comments to that procedure. Framework-guided revision is not clinician validation. None of the revised charts has completed the next review.

Synthea-derived longitudinal context does not guarantee that the inpatient episode is clinically valid. Some scenarios required explicit episode generation because the export did not contain the disease. Heart-failure eligibility in this living cohort rested mostly on compatible cardiovascular context rather than on a Synthea heart-failure condition. Endocarditis was episode-generated.

Matched cases are matched on the reasoning target and on approximate decision complexity. They are not statistically equivalent patients.

Generation 2 has passed automated checks only. Clinical validation is pending.

No resident has taken these cases. Expected difficulty on the form is an expert estimate. Discrimination, calibration, and the relationship to reconciliation performance in practice are unmeasured.

The framework is specific to discharge medication reasoning. Transfer to other competencies has not been tested.

A resident dashboard and a scorer against the hidden reference are specified as future work. They are not results of this paper.

## Conclusion

CliniProof separates three problems that are often treated as one. The first is generating a plausible synthetic patient. The second is constructing an evidence-sufficient clinical reasoning case. The third is validating that case before it is used for assessment.

Generation 1 supplies clinician-informed evidence about how archetype-based charts fail, revises the four cases both clinicians reviewed, and applies the resulting framework to the rest without calling that application a new review. Generation 2 operationalizes those failure modes as prospective constraints, using Synthea for longitudinal context and CliniProof for a controlled inpatient trajectory. Clean cases do not contain planted errors. A planted discrepancy, if it is used at all, belongs in a later experiment on a case whose base form and reference have already been accepted.

The contribution is a pipeline in which provenance, clinical sufficiency, hidden-reference derivation, and expert validation are separated. The next empirical question is whether the matched Synthea-grounded cases receive more favorable clinician ratings, or require fewer revisions, than the revised archetype cases when both are read with the same instrument.

## Figures

These are specifications for figures. They are not data plots, and this draft does not present them as completed graphics.

**Figure 1. Case pipeline.**

```text
Synthea longitudinal record, or a resident-informed archetype
        ↓
CliniProof inpatient trajectory
        ↓
clean resident-visible case, with no completed discharge list
        ↓
hidden evidence-backed reference, written after the chart
        ↓
automated sufficiency and provenance checks
        ↓
clinician validation with the C1–C5 instrument
        ↓
resident assessment (planned; not conducted)
```

**Figure 2. Two-generation design.**

```text
Generation 1: archetype → clean chart → clinician review → revision
Generation 2: Synthea context → inpatient episode → prospective sufficiency gates

Pairs, matched on reasoning task, not on the answer:
VAL-801 ↔ G2-001
…
VAL-824 ↔ G2-024

Clinical comparison of the pairs: proposed, not performed.
```

**Figure 3. Two layers.**

```text
Layer 1, resident-visible: baseline, acute illness, work-up,
treatment, response, medication timeline, discharge readiness.
The discharge medication plan is absent.

Layer 2, hidden: action, rationale, evidence pointer,
monitoring, follow-up, acceptable alternatives, provenance.
```

**Figure 4. From review to design.**

```text
Round 1 concern on the overlap cases
        ↓
named sufficiency domain
        ↓
Generation 2 gate that rejects a candidate missing that domain
```

The figure should use the rows of Table 4. It should not imply that the gates have been clinically validated.

## References

References below are those retained from the September draft for claims that this revision still makes, plus the Synthea source verified for this revision. Citation-status notes are in `docs/paper_revision_plan.md`. LLM-vignette papers are cited only in the comparison subsection.

Abidi, S. H., Almazan, J., Fabiyi, O., Zehra, F., & Tariq, M. (2026). AI-supported case-based learning in medical education: A comprehensive scoping review. Frontiers in Medicine, 13, 1798097. https://doi.org/10.3389/fmed.2026.1798097

Alqenae, F. A., Steinke, D., & Keers, R. N. (2020). Prevalence and nature of medication errors and medication-related harm following discharge from hospital to community settings: A systematic review. Drug Safety, 43, 517–537. https://doi.org/10.1007/s40264-020-00918-3

Arthur, C., Levett-Jones, T., & Kable, A. (2012). Quality indicators for design and implementation of simulation experiences: A Delphi study. Nurse Education Today, 33, 1357–1361.

Bajorek, S. A., & McElroy, V. (2020). Discharge planning and transitions of care. Agency for Healthcare Research and Quality.

Bakkum, M. J., Hartjes, M. G., Piët, J. D., Donker, E. M., Likic, R., Sanz, E., de Ponti, F., Verdonk, P., Richir, M. C., van Agtmael, M. A., & Tichelaar, J. (2024). Using artificial intelligence to create diverse and inclusive medical case vignettes for education. British Journal of Clinical Pharmacology, 90(3), 640–648. https://doi.org/10.1111/bcp.15977

Barnsteiner, J. H. (2008). Medication reconciliation. In R. G. Hughes (Ed.), Patient safety and quality: An evidence-based handbook for nurses. Agency for Healthcare Research and Quality. https://www.ncbi.nlm.nih.gov/books/NBK2648/

Barrows, H. S., & Tamblyn, R. M. (1980). Problem-based learning: An approach to medical education. Springer Publishing Company.

Bishop, M. A., Cohen, B. A., Billings, L. K., & Thomas, E. V. (2015). Reducing errors through discharge medication reconciliation by pharmacy services. American Journal of Health-System Pharmacy, 72(17 Suppl 2), S120–S126. https://doi.org/10.2146/sp150021

Boockvar, K. S., Santos, S. L., Kushniruk, A., Johnson, C., & Nebeker, J. R. (2011). Medication reconciliation: Barriers and facilitators from the perspectives of resident physicians and pharmacists. Journal of Hospital Medicine, 6(6), 329–337. https://doi.org/10.1002/jhm.891

Cayres Ribeiro, L. M., Sidorenkov, G., El-Baz, N., Vliegenthart, R., Koopman, M. Y., Durning, S. J., & de Carvalho Filho, M. A. (2026). Generating synthetic patient vignettes from real medical texts for the teaching of clinical reasoning. Medical Teacher, 48(6), 945–948. https://doi.org/10.1080/0142159X.2025.2537334

Chung, P., Boodoo, M., & Doboli, S. (2023). Case scenario generators for trauma surgery simulation utilizing autoregressive language models. Artificial Intelligence in Medicine, 144, 102635. https://doi.org/10.1016/j.artmed.2023.102635

Coleman, E., Smith, J., Raha, D., & Min, S. (2005). Posthospital medication discrepancies: Prevalence and contributing factors. Archives of Internal Medicine, 165, 1842–1847. https://doi.org/10.1001/archinte.165.16.1842

Cumyn, A., & Harris, I. B. (2012). A comprehensive process of content validation of curriculum consensus guidelines for a medical specialty. Medical Teacher, 34(8), e566–e572. https://doi.org/10.3109/0142159X.2012.668623

Desai, S. V., Burk-Rafel, J., Lomis, K. D., & others. (2024). Precision education: The future of lifelong learning in medicine. Academic Medicine, 99(4S Suppl 1), S14–S20. https://doi.org/10.1097/ACM.0000000000005552

Emekli, E., Emekli, E., & Özel, B. (2026). Artificial intelligence-assisted generation of case scenarios and multiple-choice questions in psychiatry: A pilot study. Academic Psychiatry, 50(4), 391–397. https://doi.org/10.1007/s40596-025-02298-1

Forster, A. J., Murff, H. J., Peterson, J. F., Gandhi, T. K., & Bates, D. W. (2003). The incidence and severity of adverse events affecting patients after discharge from the hospital. Annals of Internal Medicine, 138(3), 161–167. https://doi.org/10.7326/0003-4819-138-3-200302040-00007

Gleason, K. M., Brake, H., Agramonte, V., & Perfetti, C. (2012). Medications at Transitions and Clinical Handoffs (MATCH) toolkit for medication reconciliation (AHRQ Publication No. 11(12)-0059). Agency for Healthcare Research and Quality.

Gonzales, A., Guruswamy, G., & Smith, S. R. (2023). Synthetic data in health care: A narrative review. PLOS Digital Health, 2(1), e0000082. https://doi.org/10.1371/journal.pdig.0000082

Gorenshtein, A., Omar, M., Glicksberg, B. S., Nadkarni, G. N., & Klang, E. (2025). AI agents in clinical medicine: A systematic review. medRxiv. https://doi.org/10.1101/2025.08.22.25334232

Hernandez, J., Frallicciardi, A., Nadir, N. A., Gothard, M. D., & Ahmed, R. A. (2020). Development of a Simulation Scenario Evaluation Tool (SSET): Modified Delphi study. BMJ Simulation & Technology Enhanced Learning, 6(6), 344–350. https://doi.org/10.1136/bmjstel-2019-000521

Joint Commission on Accreditation of Healthcare Organizations. (2006). Using medication reconciliation to prevent errors. Sentinel Event Alert, (35), 1–4.

Killin, L., Hezam, A., Anderson, K. K., & Welk, B. (2021). Advanced medication reconciliation: A systematic review of the impact on medication errors and adverse drug events associated with transitions of care. The Joint Commission Journal on Quality and Patient Safety, 47(7), 438–451. https://doi.org/10.1016/j.jcjq.2021.03.011

Komperda, K., & Lempicki, K. (2019). Cited in the September manuscript for a lecture-plus-workshop comparison. The source bibliography did not include a full entry, and this revision does not supply one.

Kwan, J. L., Lo, L., Sampson, M., & Shojania, K. G. (2013). Medication reconciliation during transitions of care as a patient safety strategy: A systematic review. Annals of Internal Medicine, 158(5), 397–403. https://doi.org/10.7326/0003-4819-158-5-201303051-00006

Lindquist, L. A., Gleason, K. M., McDaniel, M. R., Doeksen, A., & Liss, D. (2008). Teaching medication reconciliation through simulation: A patient safety initiative for second year medical students. Journal of General Internal Medicine, 23(7), 998–1001. https://doi.org/10.1007/s11606-008-0567-3

McShane, M., & Stark, R. (2018). Medication reconciliation in the hospital: An interactive case-based session for internal medicine residents. MedEdPORTAL, 14, 10770. https://doi.org/10.15766/mep_2374-8265.10770

Mueller, S. K., Sponsler, K. C., Kripalani, S., & Schnipper, J. L. (2012). Hospital-based medication reconciliation practices: A systematic review. Archives of Internal Medicine, 172(14), 1057–1069. https://doi.org/10.1001/archinternmed.2012.2246

Nasa, P., Jain, R., & Juneja, D. (2021). Delphi methodology in healthcare research: How to decide its appropriateness. World Journal of Methodology, 11(4), 116–129. https://doi.org/10.5662/wjm.v11.i4.116

National Coordinating Council for Medication Error Reporting and Prevention. (2026). About medication errors. https://www.nccmerp.org/about-medication-errors

Norman, G. R., & Schmidt, H. G. (1992). The psychological basis of problem-based learning: A review of the evidence. Academic Medicine, 67(9), 557–565.

Ramjaun, A., Sudarshan, M., Patakfalvi, L., Tamblyn, R., & Meguerditchian, A. N. (2015). Educating medical trainees on medication reconciliation: A systematic review. BMC Medical Education, 15, 33. https://doi.org/10.1186/s12909-015-0306-5

Rao, A. S., Kim, J., Mu, A., Young, C. C., Kalmowitz, E., Senter-Zapata, M., Whitehead, D. C., Garibyan, L., Landman, A. B., & Succi, M. D. (2025). Synthetic medical education in dermatology leveraging generative artificial intelligence. npj Digital Medicine, 8(1), 247. https://doi.org/10.1038/s41746-025-01650-x

Ruggiano, N., Sahoo, S., Brashear, A., Nwatu, U., Brunson, A., Noh, H., Cole, H., McKinney, R., Framil Suarez, C. V., Brown, E. L., & Prevost, S. (2026). Evaluating AI-generated geriatric case studies for interprofessional education: Systematic analysis across 5 platforms. JMIR Medical Education, 12, e83085. https://doi.org/10.2196/83085

Takahashi, H., Shikino, K., Kondo, T., Komori, A., Yamada, Y., Saita, M., & Naito, T. (2024). Educational utility of clinical vignettes generated in Japanese by ChatGPT-4: Mixed methods study. JMIR Medical Education, 10, e59133. https://doi.org/10.2196/59133

Thomas, P. A., Kern, D. E., Hughes, M. T., & Chen, B. Y. (Eds.). (2015). Curriculum development for medical education: A six-step approach (3rd ed.). Johns Hopkins University Press.

Triola, M. M., & Burk-Rafel, J. (2023). Precision medical education. Academic Medicine, 98(7), 775–781. https://doi.org/10.1097/ACM.0000000000005245

Walonoski, J., Kramer, M., Nichols, J., Quina, A., Moesel, C., Hall, D., Duffett, C., Dube, K., Gallagher, T., McLachlan, S., et al. (2018). Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. Journal of the American Medical Informatics Association, 25(3), 230–238. https://doi.org/10.1093/jamia/ocx079

Yanagita, Y., Yokokawa, D., Uchida, S., Li, Y., Uehara, T., & Ikusaka, M. (2024). Can AI-generated clinical vignettes in Japanese be used medically and linguistically? https://doi.org/10.1101/2024.02.28.24303173

Zhang, Q., Huang, Z., Huang, Y., Wang, G., Zhang, R., Yang, J., Cheng, Y., Chen, B., Wang, H., Qiu, K., & Chen, H. (2025). Generative AI in medical education: Feasibility and educational value of LLM-generated clinical cases with MCQs. BMC Medical Education, 25(1), 1502. https://doi.org/10.1186/s12909-025-08085-8
