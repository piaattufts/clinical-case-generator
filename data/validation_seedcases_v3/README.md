# Resident-seed-guided set (`CLINIPROOF_SEEDCASES_V3`)

**Status: active prospective validation set, pending clinician validation.**

1. Batch code: `CLINIPROOF_SEEDCASES_V3`
2. Generation strategy: `resident_seed_guided`
3. VAL range: VAL-801–VAL-824
4. Cases: 24
5. Status: ready for human clinician validation. Not clinically validated.
6. Archetype distribution: four profiles in each of six families — medication-history uncertainty, heart-failure decompensation, OPAT/endocarditis, transplant/CMV, postoperative anticoagulation, and gastrointestinal bleeding with an acute medication change. The six resident source documents are design references, not an epidemiologic sample. See [`../seed_cases/README.md`](../seed_cases/README.md).
7. Error distribution: Family 1 has 7 cases, Family 2 has 13, and 4 cases are controls. Assignments are in the batch plan and the manifest.
8. Uniqueness: exact duplicate clean-case fingerprints 0. Closest pair similarity 0.79 (VAL-805 vs VAL-807), below the 0.85 rejection threshold. Details are in [`diversity_report.md`](diversity_report.md).
9. Artifacts in this directory:
   - [`batch_plan.json`](batch_plan.json)
   - [`resident_validation_cases.json`](resident_validation_cases.json)
   - [`investigator_answer_key.json`](investigator_answer_key.json) and [`investigator_answer_key.md`](investigator_answer_key.md)
   - [`validation_manifest.json`](validation_manifest.json)
   - [`coverage_report.md`](coverage_report.md) and [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md)
   - [`diversity_report.md`](diversity_report.md)
   - [`resident_review_worksheet.csv`](resident_review_worksheet.csv) and [`resident_review_schema.json`](resident_review_schema.json)
   - [`readable/`](readable/README.md)
10. Audience: residents start at [`readable/all_cases.md`](readable/all_cases.md). Clinicians rating C1–C5 start at [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) and [`../../docs/clinical_validation.md`](../../docs/clinical_validation.md). The seed documents are not resident study materials.
11. Regenerate only before this batch is treated as published. From a bootstrapped database:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_seedcases_v3/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_SEEDCASES_V3
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_SEEDCASES_V3 \
  --resident data/validation_seedcases_v3/resident_validation_cases.json
```

12. Immutable after this freeze is committed: the case JSON, manifest, plan, and readable case pages. Do not edit the resident DOCX files to change these charts. Generation reads the blueprint, not the DOCX, at freeze time. `CLINIPROOF_SEEDCASES_V2` and `CLINIPROOF_SEEDCASES_V1` stay untouched.
13. Still required: human C1–C5 review. See [`../clinical_qc_report.md`](../clinical_qc_report.md) for the internal pre-review QC table.

Master seed: `20260926`. Sequences: 1501–1524. Case seed: `{master_seed}:{sequence}:{scenario}:{clinical_profile}`.
