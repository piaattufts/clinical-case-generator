# Clinician walkthrough

This page explains how a CliniProof chart is built, using four teaching snapshots. The snapshots are not study cases. The cases under review are the [balanced structured set](../../data/case_sets/balanced/README.md) (VAL-701–VAL-724) and the [resident-seed-guided set](../../data/case_sets/seed_guided/README.md) (VAL-801–VAL-824).

The teaching files are in [examples/](examples/). They were generated before the current curated-regimen layer. Some doses in those JSON files copy a product strength or use a once-daily fallback. Current study charts do not. In particular, current prospective apixaban is 5 MG orally twice daily, not the 2.5 MG once-daily demonstration in the older snapshot. Read the snapshots to see the construction steps. Read the study overviews to see the charts you would validate.

## 1. One clean example

[examples/syn-000901.json](examples/syn-000901.json) is a clean heart-failure teaching chart (`SYN-000901`). No assessment problem was introduced. The file shows a synthetic inpatient encounter: diagnosis, symptoms, vital signs, laboratories, medication lists, and a hospital course. It is a teaching object, not VAL-701 and not a copy of any study case.

## 2. How structured facts are selected

A scenario family is chosen first, here an inpatient heart-failure theme. The generator then selects symptoms, a hospital-course pattern, a medication subset, and a follow-up structure from that family's allowed lists. Age, sex, weight, and numeric results are synthetic draws. They are not taken from a hospital record. The same steps apply to the atrial-fibrillation snapshot [syn-000902.json](examples/syn-000902.json) and the pneumonia snapshot [syn-000903.json](examples/syn-000903.json).

## 3. How terminology is attached

Medication concepts are resolved to RxNorm, diagnoses to ICD-10-CM, and laboratory tests to LOINC, using terminology already stored for the project. The code on a row identifies the concept. It does not by itself prove that the dose, the frequency, or the clinical story is appropriate. A source-backed terminology concept is not automatically a clinically appropriate choice for a particular synthetic patient.

## 4. How the medication transition is constructed

The clean chart distinguishes the home regimen, what was given in the hospital, and what is intended at discharge. A drug may be continued, held, started, stopped, substituted, or limited to the hospital stay. Monitoring and follow-up sit beside the list. On current study cases those orders come from a curated regimen: dose, route, frequency, indication, and temporal role. The teaching snapshots predate that layer, so their doses are not the doses to imitate.

## 5. How a clean chart differs from an error-bearing chart

[syn-000901.json](examples/syn-000901.json), [syn-000902.json](examples/syn-000902.json), and [syn-000903.json](examples/syn-000903.json) are clean. [syn-000904.json](examples/syn-000904.json) is an investigator-only demonstration in which one medication was omitted from the discharge list (`f1_omission`). The omission is recorded in an answer key inside that file. Do not give `syn-000904.json` to a resident who is supposed to find the problem unaided. Study cases separate the blinded chart from the investigator key in the same way. This walkthrough does not say which VAL case has which target.

## 6. What automated checks do

The software checks structure, terminology identity, implemented clinical constraints, and, after a problem is introduced, whether that change is the one that was requested. Those checks can catch a broken code, a unit error, or a second mechanical discrepancy. They cannot decide that the hospitalization is believable or that a resident could fairly be asked to solve it.

## 7. Why human review remains necessary

Passing automated validation does not establish clinical validity. A clinician still reads the complete chart and rates C1 through C5: plausibility, whether the intended problem is present, whether a resident could find it, whether a second problem competes with it, and how difficult it is likely to be. That review is described on each [case-set overview](../../data/case_sets/README.md) and in [clinical validation](../clinical_validation.md).

Until a clinician finishes review, treat both the teaching snapshots and the study charts as machine-checked synthetic cases pending clinician validation.
