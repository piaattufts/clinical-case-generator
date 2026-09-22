# How CliniProof Builds and Validates a Case

This overview is for residents who are curious about the technology, physicians, medical educators, pharmacists, informatics staff, and AI engineers. It explains the system in clinical language first, then names the software pieces.

It discusses how cases are made. It does not reveal which frozen case labeled VAL-201 through VAL-224 contains which assessment target.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

## A. Clinical overview

CliniProof creates synthetic inpatient medication-reconciliation cases with a known assessment target.

Medication reconciliation is the clinical work of making a best-possible medication history, comparing it with inpatient orders and the discharge list, and ensuring that holds, stops, continuations, substitutions, supplies, monitoring, and follow-up are explicit and safe.

Some cases are clean controls. In those charts the software leaves the encounter without an intentionally planted assessment problem, so reviewers and residents can also see an intact reconciliation. Other cases receive exactly one planned problem after the clean chart has already passed automated checks. Four of the twenty-four frozen cases are clean controls. They are included so that residents cannot assume that every case necessarily contains an error. This document does not say which identifiers are controls.

Family 1 problems, recorded in software as `family_1`, are discrepancies on the medication lists themselves: a drug missing at discharge, an extra drug, or an unexplained change in dose, route, frequency, or product.

Family 2 problems, recorded as `family_2`, are transition-of-care gaps. The discharge medication identity may be unchanged; what is missing is a required companion action such as INR monitoring, a restart plan for a held drug, enough days’ supply, stopping a hospital-only drug, reverting a temporary substitute, or arranging follow-up for an unresolved decision.

Do not identify Family 2 solely by comparing home versus discharge lists.

### Implemented categories

Each category has a clinical name and a standardized identifier used in software and investigator materials. The current dataset uses the canonical CliniProof taxonomy. The identifier is shown in parentheses after the clinical name.

#### Family 1

##### Medication omitted at discharge (`f1_omission`)

A medication intended to continue after hospitalization is absent from the discharge medication list without a documented reason. This is a Family 1 medication-transition discrepancy. The clean expected discharge medication is present before assessment modification and removed from the final discharge list.

##### Medication inappropriately added or continued (`f1_commission`)

A medication that should not continue, for example one held or stopped, appears on the discharge list. The injector adds or retains a discharge-list entry that the clean case had omitted for a documented reason.

##### Unexplained dose discrepancy (`f1_dose_mismatch`)

The discharge dose differs from the intended continued dose without a documented explanation. This is a Family 1 medication-list discrepancy. After the clean case passes validation, the injector changes only the dose field on the discharge entry. Home and inpatient lists remain unchanged so that a reviewer can see the intended dose.

##### Unexplained route discrepancy (`f1_route_mismatch`)

The discharge route differs from the intended continued route without a documented explanation. For example, an oral medication might appear as a different route at discharge with no rationale in the chart.

##### Unexplained frequency discrepancy (`f1_frequency_mismatch`)

The discharge frequency differs from the intended continued frequency without a documented explanation. For example, a once-daily medication might appear as twice daily at discharge, or the reverse.

##### Unexplained therapeutic substitution (`f1_therapeutic_substitution`)

The discharge list shows a same-class substitute instead of the intended continued product, without documenting an intentional switch. The original product remains visible on the home or inpatient list so that the substitution can be noticed.

#### Family 2

##### Required outpatient monitoring not arranged (`f2_monitoring_not_arranged`)

Warfarin is continued at discharge, but outpatient INR monitoring has not been arranged. In CliniProof this is classified as a Family 2 transition-of-care gap because the medication order itself remains unchanged; the missing element is the required follow-up action. After the clean case passes validation, the injector removes the expected monitoring record. The medication itself remains unchanged.

##### Held medication without a restart plan (`f2_held_med_no_restart_plan`)

The original medication is intentionally stopped during hospitalization for a legitimate temporary reason, but the discharge documentation does not tell the patient or outpatient clinician when or under what conditions it should be resumed. The hold itself remains visible; what is missing is the restart plan.

##### Insufficient medication supply (`f2_insufficient_supply`)

Days’ supply at discharge is shortened so that treatment cannot last until the planned follow-up. The medication identity on the discharge list may be correct; the missing element is enough supply to bridge to the next visit.

##### Hospital-only medication continued after discharge (`f2_hospital_only_continued`)

A drug started for an inpatient-only indication remains on the discharge list. Reviewers are expected to notice that a hospital-only product was not stopped at the transition home.

##### Temporary inpatient substitution not addressed at discharge (`f2_inpatient_substitution_not_reverted`)

A temporary inpatient substitute is left in place without reverting to home therapy or documenting an intentional decision to continue the substitute.

##### Follow-up missing for an unresolved treatment decision (`f2_pending_decision_followup_missing`)

A pending therapeutic decision has no arranged follow-up. The medication list may look intact, but the chart does not say when or by whom the unresolved decision will be revisited.

##### Required companion medication omitted (`f2_coprescription_omitted`)

The taxonomy also defines this category for a situation in which a clinically required companion medication is missing. This category is not included in the current validation set because the software does not yet have a sufficiently source-backed deterministic rule for deciding when such a companion medication is required (`not_yet_implementable`). Rather than guessing or encoding an unsupported rule, the system currently rejects this category.

## B. Source-backed versus synthetic information

A source-backed concept is not the same thing as real patient data. An RxNorm identifier for warfarin means the concept came from RxNorm, not that a real patient was taking warfarin.

The table below separates the kinds of information that appear on a case. Official vocabulary rows are retrieved from terminology services. Patient-specific numbers and stories are generated. Assessment discrepancies are introduced only after the clean chart has passed automated checks.

| Type of information | Example | How it is obtained |
| --- | --- | --- |
| Medication concept | Warfarin | Retrieved from RxNorm |
| Diagnosis concept | Heart failure | Retrieved from ICD-10-CM |
| Laboratory test | Creatinine | Retrieved from LOINC |
| Unit | mmol/L | Retrieved from UCUM or LOINC |
| Age | 72 | Synthetically generated |
| Blood pressure | 128/74 | Synthetically generated |
| Lab result | Creatinine 1.3 | Synthetic patient value |
| Clinical narrative | History of present illness | Template sentences, or optional LLM wording of already selected facts |
| Assessment discrepancy | Missing monitoring | Introduced deterministically after clean validation |

Official source ranking can yield technically valid but clinically atypical formulations or units, for example a solution or gel, or an SI laboratory unit. Those oddities are left visible for clinician review. They are not silently rewritten.

## C. Generation pipeline

Cases are built in a fixed order. Each stage completes before the next stage begins.

1. A clinical scenario is selected. A clinical scenario is an inpatient teaching skeleton chosen by an operator. It specifies specialty, age band, diagnosis and medication search phrases, and which assessment categories are allowed.
2. Terminology is resolved. Search phrases are matched to identifiers already stored from official services, including RxNorm, ICD-10-CM, LOINC, UCUM, and related sources. The generator does not invent codes.
3. A clean synthetic patient is assembled: demographics, vital signs, laboratory values, medication lists, notes, and follow-up, internally consistent with the scenario and the stored concepts.
4. Rule checks apply a small set of source-backed if-then constraints, and only those with attached DailyMed or RxClass evidence. This is not a complete clinical guideline.
5. Clean validation checks structure, confirms that every coded concept exists in local reference tables, confirms that hard rules hold, and confirms that the clean chart does not already contain the assessment target that would later be planted.
6. Assessment target eligibility asks whether the planned category can actually be applied to this case. If not, generation stops. Another category is not silently substituted.
7. Controlled error introduction applies exactly one planned change for assessment cases. Clean controls skip this step.
8. Post-error validation checks that the intended target is now present, that required evidence remains visible, and that a second assessment target was not introduced.
9. Blinded resident export gives residents the chart without family, category, trigger metadata, or answer keys.
10. Clinician validation is the human step. Two clinical reviewers independently complete blinded clinical plausibility (C1). After those ratings are submitted and locked, they independently complete C2 through C5 and an Accept, Revise, or Exclude recommendation. Important disagreements undergo structured consensus review. Original independent ratings are preserved. Automated checks cannot certify realism or educational appropriateness.

## D. What OpenAI does

OpenAI is optional in the CliniProof pipeline and is used only to help word narrative text from clinical facts that have already been selected by the structured generator. It does not choose diagnoses, medications, terminology codes, error categories, clinical rules, or answer-key content.

The current frozen validation set uses template narrative rather than OpenAI. The freeze command sets the OpenAI flag to false.

Raw patient-source rows are never sent to a language model.

## E. Why machine validation is not clinical validation

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. These checks are useful for detecting technical inconsistencies, but they do not establish that a case is clinically realistic, educationally appropriate, or representative of actual practice. Those judgments require review by clinicians.

Until clinicians finish review, every generated record remains a machine-validated synthetic resident-review case pending clinician validation.

## F. Technical implementation

Physicians can stop here. The table below is for engineers and informatics staff. It names the repository files that implement each function already described in clinical language.

| Function | Implementation |
| --- | --- |
| Scenario definitions | `data/bootstrap/scenarios.json` |
| Terminology bootstrap | `app/services/bootstrap.py` |
| Case generation | `app/services/generation.py` |
| Error taxonomy | `app/services/error_taxonomy.py` |
| Error injection | `app/services/error_injection.py` |
| Validation | `app/services/validation.py` |
| Freeze/export | `app/services/validation_batch.py` |
| Optional narrative LLM | `app/openai/narrative.py` |
| Readable Markdown views | `app/services/readable_packets.py` |

Standardized families are Family 1 (`family_1`), Family 2 (`family_2`), and no planted target (`none`) for a clean control. Standardized categories are the `f1_*` and `f2_*` identifiers listed above. Unknown names fail rather than being aliased.

Readable packets are regenerated with `python scripts/build_readable_validation_packets.py` and do not rewrite frozen JSON.
