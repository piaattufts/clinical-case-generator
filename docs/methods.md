# Methods

## Overview

All prospective cases are generated as clinically coherent clean cases before any experimental discrepancy is introduced. The two active strategies stay separate. Balanced structured generation does not use the resident seed documents. Resident-seed-guided generation does not rebalance itself into the scenario grid.

## Shared structured pipeline

1. Select the case-generation strategy.
2. Select the scenario or archetype and the named clinical profile.
3. Resolve canonical terminology.
4. Synthesize demographics, numeric values, and chart context.
5. Construct clean medication transitions from the curated regimen, including temporal role.
6. Validate structure and implemented constraints.
7. Perform the clean-case diversity audit.
8. Verify that the assigned error category is eligible. If it is not, freeze fails. Another category is not substituted.
9. Inject exactly one predetermined discrepancy, or retain the case as a control.
10. Revalidate and audit error isolation.
11. Freeze the assignment.
12. Create blinded resident and investigator exports.
13. Conduct human clinician C1–C5 validation. That step is not automated.

## Balanced structured generation

`CLINIPROOF_BALANCED_V4` uses predefined scenario families and named clinical profiles. The current families are inpatient heart failure, atrial fibrillation, hypertension, type 2 diabetes, and community-acquired pneumonia. Each assignment names a distinct profile. The design is intentionally balanced. It is not prevalence-weighted and is not a sample of hospital discharges. Profile diversity is measured on the clean case before error injection. Exact duplicate fingerprints are rejected. Similarity at or above 0.85 is rejected. Similarity from 0.70 to 0.85 is reported as a warning.

## Resident-seed-guided generation

`CLINIPROOF_SEEDCASES_V3` starts from six resident-authored source examples stored under `data/seed_cases/resident_authored/`. Those documents are clinical design references. Reviewers abstracted them into archetypes and profiles. The source cases are not copied. Synthetic age, sex, weight, vitals, and laboratory numbers are regenerated from the case seed. The six source examples are not a statistical sample and are not used to estimate prevalence. The six archetype families are medication-history uncertainty, heart-failure decompensation, OPAT/endocarditis, transplant/CMV, postoperative anticoagulation, and gastrointestinal bleeding with an acute medication change. This strategy uses the same terminology, regimen, provenance, and error-injection framework as the balanced set.

## Source-backed versus synthetic

RxNorm, LOINC, ICD-10-CM, and UCUM identities are resolved from the project's terminology sources. Patient-level ages, weights, vital signs, and laboratory numbers are synthetic draws. A valid RxNorm concept does not prove that the charted dose or frequency is appropriate. Terminology validity does not prove clinical validity.

## Clinical regimen curation

RxNorm product identity does not automatically determine an appropriate dose or frequency. The generator does not copy product strength into the administered dose and does not assume once daily. Scenario-level regimens live in [`data/bootstrap/medication_regimens.json`](../data/bootstrap/medication_regimens.json). Each entry records the concept query, clinical role, indication mapping, dose, route, frequency, temporal role, profile restrictions, and a citation. Route, form, dose, and frequency are validated against that entry. If a real medication has no curated regimen, generation fails rather than inventing a dose. Test fixtures whose identifiers start with `TEST_` may still use a strength fallback so pipeline tests can run. Clinician review remains required. Curated assumptions in the current active sets include:

- Apixaban for nonvalvular atrial fibrillation is charted as 5 MG orally twice daily. Age is kept under 80 and weight above 60 kg so the chart does not meet two of the three labeled dose-reduction criteria. Reduced-dose apixaban is not used.
- Warfarin is charted as 5 MG orally once daily with an explicit note that the dose is adjusted to the INR. INR laboratory monitoring is separate from the anticoagulation-clinic appointment.
- Enoxaparin in the postoperative profiles is hospital-only prophylaxis, 40 MG subcutaneously once daily from the 0.4 mL (100 MG/mL) syringe, not a weight-based treatment bridge.
- Heart-failure beta blockers use metoprolol succinate extended release 25 MG once daily when that concept is selected, or metoprolol tartrate 25 MG twice daily when the stored concept is tartrate. Carvedilol immediate release is 6.25 MG twice daily. Spironolactone for straightforward heart failure is 25 MG once daily. Lisinopril is 10 MG once daily. Enalapril is 5 MG twice daily. Furosemide is 40 MG once daily.
- Ceftriaxone for adult endocarditis/OPAT is 2000 MG intravenously once daily. The product concept is the 2000 MG injection. The route stays intravenous.
- Azithromycin started for the current pneumonia is 250 MG orally once daily for the remaining course and is not a home medication.
- Insulin lispro, when used for inpatient glucose stabilization, is hospital-only. The dose is recorded as individualized, not as a copied pen strength.
- Tacrolimus maintenance is 1 MG orally every 12 hours, with the note that the dose is individualized to the trough. Mycophenolate mofetil for the kidney-transplant profiles is 1000 MG orally twice daily, given as 500 MG tablets. Valganciclovir for CMV treatment with preserved renal function is 900 MG orally twice daily, given as 450 MG tablets.

Citations for each row are stored beside the regimen. They are labeling references used to avoid a distracting baseline, not a claim that every chart meets a full guideline.

## Temporal medication roles

A medication is not listed as a home medication only because it exists in the case. Roles used in generation include pre-existing home therapy, started during the admission, continued at discharge, stopped, temporarily held, and hospital-only. Acute antibiotics and ceftriaxone for these profiles start during the admission unless a profile explicitly says the patient was already receiving them. Hospital-only drugs are absent at discharge unless continuation is the injected discrepancy. New enalapril in the new-hypertension profile is marked as started during the admission.

## Repeated chart fields

Fields were not randomized for cosmetic variety.

| Field | Decision |
| --- | --- |
| Language preference English | Study-controlled constant, so language is not an extra discrepancy. |
| Pharmacist review completed | Study-controlled constant on the reconciliation record. |
| Patient participation | Study-controlled constant on the balanced set. On the seed-guided set it varies when the archetype is about an uncertain or collateral medication history. |
| Medication-history source | Study-controlled `patient_and_prior_records` on the balanced set. Profile-driven for seed-guided history-uncertainty profiles. |
| Baseline living situation | Study-controlled label: the patient normally lives at home. Discharge disposition is separate and profile-driven. |
| Reconciliation marked complete before injection | Study-controlled background. The injected discrepancy is the experimental change. |

## Error injection

Family 1 changes the medication list or a list field: omission, commission, dose, route, frequency, or an unexplained same-class substitute. Family 2 keeps the list fact that should have triggered an action and removes that action: monitoring, a restart plan after a hold, enough supply, stopping a hospital-only drug, reverting an inpatient formulary substitute, or scheduling follow-up for a pending decision. Controls receive no injection. The category is assigned in the batch plan. Definitions are in [`error_taxonomy.md`](error_taxonomy.md).

## Validation

Automated checks run before and after injection. They include terminology provenance, laboratory value and unit coherence, regimen dose/route/frequency, beta-blocker formulation and frequency, temporal-role consistency, imaging timepoint versus comparative wording, endocarditis microbiology chronology, echo findings that are imaging findings, disposition versus baseline living situation, and exactly one intended discrepancy on error-bearing cases. Human review is the one-stage C1–C5 procedure in [`clinical_validation.md`](clinical_validation.md). Passing automation means the case is ready for that review.
