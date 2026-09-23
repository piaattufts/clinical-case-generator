# Active CliniProof Validation Sets

The repository has **two active prospective validation datasets**, totaling **48** cases. Clinical validation uses a single review stage (C1–C5). Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

Do not combine the two sets into one answer key. Each set has its own manifest, investigator key, worksheet, and provenance.

See also the investigator comparison: [`validation_comparison/active_batch_comparison.md`](validation_comparison/active_batch_comparison.md).

## Balanced structured set

`CLINIPROOF_BALANCED_V3` — VAL-501 through VAL-524 — `generation_strategy = balanced_structured`

Twenty-four distinct clinical profiles. Clean-case uniqueness is evaluated before error injection.

- [All cases](validation_balanced_v3/readable/all_cases.md)
- [Clinician validation packet](validation_balanced_v3/readable/clinician_validation_packet.md)
- [Validation worksheet](validation_balanced_v3/readable/clinical_validation_worksheet.csv)
- [Validation rubric](validation_balanced_v3/readable/validation_rubric.md)
- [Diversity report](validation_balanced_v3/diversity_report.md)
- [Investigator answer key](validation_balanced_v3/investigator_answer_key.md)
- [Batch catalog](validation_balanced_v3/README.md)

## Resident-seed-guided set

`CLINIPROOF_SEEDCASES_V2` — VAL-601 through VAL-624 — `generation_strategy = resident_seed_guided`

Twenty-four synthetic cases derived from abstracted resident-authored archetypes. They are not copies of the source patients.

- [All cases](validation_seedcases_v2/readable/all_cases.md)
- [Clinician validation packet](validation_seedcases_v2/readable/clinician_validation_packet.md)
- [Validation worksheet](validation_seedcases_v2/readable/clinical_validation_worksheet.csv)
- [Validation rubric](validation_seedcases_v2/readable/validation_rubric.md)
- [Diversity report](validation_seedcases_v2/diversity_report.md)
- [Investigator answer key](validation_seedcases_v2/investigator_answer_key.md)
- [Batch catalog](validation_seedcases_v2/README.md)
- [Seed-case provenance](seed_cases/README.md)

## Historical / preclinical-QC archives

`CLINIPROOF_TAXONOMY_V1` — VAL-201 through VAL-224 — `generation_strategy = original_template_randomized`

Preserved for provenance. It is **not** an active prospective study set. New reviewers should not start here.

- [Archived catalog](validation/README.md)
- [Archived readable cases](validation/readable/all_cases.md)

`CLINIPROOF_BALANCED_V2` (VAL-301–VAL-324) and `CLINIPROOF_SEEDCASES_V1` (VAL-401–VAL-424) are preclinical-QC versions retained after the clinical-coherence correction pass. They are **not** active prospective study sets.

- [Balanced V2 catalog](validation_balanced/README.md)
- [Seed V1 catalog](validation_seedcases/README.md)
