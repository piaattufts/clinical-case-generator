# Readable CliniProof review materials

This directory contains the human-readable review materials for `CLINIPROOF_BALANCED_V4`, cases VAL-701 through VAL-724.

Status: active prospective set pending clinician validation.
Generation strategy: `balanced_structured`.

Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass. Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation. Passing automated checks does not mean the cases are clinically validated.

These Markdown files are readable views. They do not replace the frozen JSON. The case-set overview is [`../README.md`](../README.md).

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
