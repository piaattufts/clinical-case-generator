# Provenance

Terminology provenance establishes concept identity. It does not independently establish clinical plausibility.

## What is source-backed

| Source | What a stored identifier means |
| --- | --- |
| RxNorm | The medication concept, ingredient, strength, and dose form that were resolved for that row. |
| LOINC | The laboratory observation identity. |
| ICD-10-CM | The diagnosis concept used for the problem. |
| UCUM | The unit identity attached to a numeric result. |
| Curated clinical rules and regimens | A project decision, with a citation, about dose, route, frequency, temporal role, or a hard constraint. The citation is stored with the regimen or rule. |
| Resident seed documents | The unchanged DOCX files under `data/seed_cases/resident_authored/`. They are design references. They are not study records. |
| Case blueprints | The archetype and profile definitions derived from those references, in `data/seed_cases/blueprints/`. |
| Deterministic seeds | The master seed and the per-assignment seed that reproduce the synthetic draws. |
| Batch manifests | The frozen list of VAL identifiers, scenarios, profiles, and error assignments. |
| Answer keys | The investigator record of the intended discrepancy, the clean expected state, and the injected state. |

## What is synthetic

Age, sex, weight, vital signs, laboratory numbers, narrative wording, and the invented patient label are synthetic. They are drawn or templated inside the constraints of the profile. They are not records from a hospital system.

## What provenance does not establish

A resolved RxNorm RXCUI does not mean the administered dose equals the product strength. A resolved ICD-10-CM code does not mean the hospitalization is clinically convincing. A curated regimen citation does not mean a clinician has accepted the chart. Passing the automated audit does not mean the case is clinically validated.

The active batches `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3` were frozen as new VAL ranges because `CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2` were already immutable. Those earlier batches, `CLINIPROOF_BALANCED_V2`, `CLINIPROOF_SEEDCASES_V1`, and `CLINIPROOF_TAXONOMY_V1`, remain in the repository as historical provenance. `CLINIPROOF_TAXONOMY_V1` is not an active review set. A later pre-validation QC pass edited `CLINIPROOF_BALANCED_V4` and `CLINIPROOF_SEEDCASES_V3` in place because clinician ratings had not started. That pass did not create another batch code. After clinician review starts, further clinical corrections should be a new freeze.
