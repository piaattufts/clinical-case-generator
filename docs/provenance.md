# Provenance

Terminology provenance establishes concept identity. It does not independently establish clinical plausibility.

## What is source-backed

| Source | What a stored identifier means |
| --- | --- |
| RxNorm | The medication concept, ingredient, strength, and dose form that were resolved for that row. |
| LOINC | The laboratory observation identity. Import uses the value set `http://loinc.org/vs` on `https://fhir.loinc.org`. The older `http://loinc.org?fhir_vs` URL returns 404 and is not active. Credentials are `LOINC_USERNAME` and `LOINC_PASSWORD` in the environment or a gitignored `.env` file. |
| ICD-10-CM | The diagnosis concept used for the problem. |
| UCUM | The unit identity attached to a numeric result. |
| Curated clinical rules and regimens | A project decision, with a citation, about dose, route, frequency, temporal role, or a hard constraint. The citation is stored with the regimen or rule. |
| Resident seed documents | The unchanged DOCX files under `data/seed_cases/resident_authored/`. They are design references. They are not study records. |
| Case blueprints | The archetype and profile definitions derived from those references, in `data/seed_cases/blueprints/`. |
| Deterministic seeds | The master seed and the per-assignment seed that reproduce the synthetic draws. |
| Batch manifests | The frozen list of VAL identifiers, scenarios, profiles, and error assignments. |
| Answer keys | Historical investigator records of an injected discrepancy, the clean expected state, and the injected state. The current resident task uses `reference_discharge_plan` on the evaluator file instead. |

## What is synthetic

Age, sex, weight, vital signs, laboratory numbers, narrative wording, and the invented patient label are synthetic. They are drawn or templated inside the constraints of the profile. They are not records from a hospital system.

## What provenance does not establish

A resolved RxNorm RXCUI does not mean the administered dose equals the product strength. A resolved ICD-10-CM code does not mean the hospitalization is clinically convincing. A curated regimen citation does not mean a clinician has accepted the chart. Passing the automated audit does not mean the case is clinically validated.

The current original freeze is `CLINIPROOF_SEEDCASES_V3` in `data/case_sets/seed_guided/`. The clean pre-injection charts for VAL-801 through VAL-824 are in `data/case_sets/seed_guided/CLEAN_BASE/`. Hashes are in `docs/source_integrity.md`. An additional seed-guided freeze, `CLINIPROOF_SEEDCASES_V4` (VAL-901–VAL-924), is in `data/case_sets/seed_guided_v4/`. It does not replace the original freeze. Older freezes and superseded revision exports were removed from this tree and remain in Git history.
