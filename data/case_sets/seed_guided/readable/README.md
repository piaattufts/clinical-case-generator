# Readable CliniProof review materials

This directory contains the human-readable review materials for `CLINIPROOF_SEEDCASES_V3`, cases VAL-801 through VAL-824.

Status: active prospective set pending clinician validation.
Generation strategy: `resident_seed_guided`.

Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. Passing automated checks does not mean the cases are clinically validated.

These synthetic cases were guided by resident-authored clinical examples. They are not copies of the source patients, and the six source examples are not an epidemiologic sample. Blinded resident materials do not name the source document.

These Markdown files are readable views. They do not replace the frozen JSON. Current prospective sets are listed in [`../../active_validation_sets.md`](../../active_validation_sets.md). `CLINIPROOF_TAXONOMY_V1` is archived historical provenance and is not the current study set.

## Where should I start?

| Who is using it | File |
| --- | --- |
| Resident or clinician reviewing and rating cases | [`clinician_validation_packet.md`](clinician_validation_packet.md) |
| Resident or clinician recording ratings | [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv) |
| Medical educator reviewing the validation criteria | [`validation_rubric.md`](validation_rubric.md) |
| Someone reading every chart in order | [`all_cases.md`](all_cases.md) |
| One case at a time | [`cases/`](cases/) |

[`clinician_validation_packet.md`](clinician_validation_packet.md) contains the readable chart, the intended assessment issue, and the C1–C5 forms. Individual pages under [`cases/`](cases/) do not include the answer key.

## Machine validation is not clinical validation

Automated checks cover structure, terminology provenance, curated regimen constraints, and the intended assessment manipulation. Human reviewers still complete C1–C5 in one pass.
