# Balanced structured set (`CLINIPROOF_BALANCED_V4`)

**Status: active prospective validation set, pending clinician validation.**

1. Batch code: `CLINIPROOF_BALANCED_V4`
2. Generation strategy: `balanced_structured`
3. VAL range: VAL-701–VAL-724
4. Cases: 24
5. Status: ready for human clinician validation. Not clinically validated.
6. Scenario distribution: heart failure 5, atrial fibrillation 5, hypertension 5, type 2 diabetes 5, community-acquired pneumonia 4. Each case uses a distinct clinical profile. The grid is balanced by design and is not prevalence-weighted.
7. Error distribution: Family 1 has 11 cases, Family 2 has 9, and 4 cases are controls. The assignment list is the batch plan and the manifest, not a second hand-maintained key.
8. Uniqueness: exact duplicate clean-case fingerprints 0. Closest pair similarity 0.74 (VAL-717 vs VAL-719), which is a warning and not a rejection. Details are in [`diversity_report.md`](diversity_report.md).
9. Artifacts in this directory:
   - [`batch_plan.json`](batch_plan.json) — assignment source
   - [`resident_validation_cases.json`](resident_validation_cases.json) — blinded export
   - [`investigator_answer_key.json`](investigator_answer_key.json) and [`investigator_answer_key.md`](investigator_answer_key.md) — concealed targets
   - [`validation_manifest.json`](validation_manifest.json) — exported identity card
   - [`coverage_report.md`](coverage_report.md) and [`scenario_coverage_matrix.md`](scenario_coverage_matrix.md)
   - [`diversity_report.md`](diversity_report.md)
   - [`resident_review_worksheet.csv`](resident_review_worksheet.csv) and [`resident_review_schema.json`](resident_review_schema.json)
   - [`readable/`](readable/README.md) — charts, clinician packet, and worksheet
10. Audience: residents start at [`readable/all_cases.md`](readable/all_cases.md). Clinicians rating C1–C5 start at [`readable/clinician_validation_packet.md`](readable/clinician_validation_packet.md) and [`../docs/clinical_validation.md`](../../docs/clinical_validation.md). Investigators use the answer key. Developers use [`../../docs/developer_guide.md`](../../docs/developer_guide.md).
11. Regenerate only before this batch is treated as published. From a bootstrapped database:

```bash
clinical-case-generator freeze-validation-batch --plan data/validation_balanced_v4/batch_plan.json
clinical-case-generator export-validation-batch --batch-code CLINIPROOF_BALANCED_V4
python -m app.services.readable_packets \
  --batch-code CLINIPROOF_BALANCED_V4 \
  --resident data/validation_balanced_v4/resident_validation_cases.json
```

12. Immutable after this freeze is committed: the case JSON, manifest, plan assignments, and readable case pages. Do not edit them in place. `CLINIPROOF_BALANCED_V3` and earlier balanced freezes stay untouched.
13. Still required: human C1–C5 review. Software isolation and the internal QC table in [`../clinical_qc_report.md`](../clinical_qc_report.md) do not replace that review.

Master seed: `20260925`. Sequences: 1401–1424. Case seed: `{master_seed}:{sequence}:{scenario}:{clinical_profile}`.
