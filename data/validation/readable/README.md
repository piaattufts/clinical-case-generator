# Readable CliniProof review materials

This directory contains the human-readable review materials for the frozen CliniProof validation set whose batch code is `CLINIPROOF_TAXONOMY_V1`. Clinical validation uses a single review stage. Each clinician or resident reviews the complete case and assesses C1–C5 in one pass.

The set contains twenty-four synthetic inpatient cases labeled VAL-201 through VAL-224. They were developed for assessment of medication-reconciliation reasoning. Twenty of the cases contain one pre-specified medication-reconciliation or transition-of-care assessment problem. Four of the cases are clean controls in which no problem was intentionally introduced. This page does not identify the controls.

These Markdown files are readable views of the frozen cases. They do not replace the frozen JSON, and they do not regenerate the underlying cases. Clinician-visible patient information comes from [`../resident_validation_cases.json`](../resident_validation_cases.json). The clinician validation packet also reads [`../investigator_answer_key.json`](../investigator_answer_key.json) so that C1–C5 can be completed together.

Until clinicians finish review, treat every record as a machine-validated synthetic resident-review case pending clinician validation.

To regenerate the Markdown from the repository root without modifying frozen JSON, run:

```bash
python scripts/build_readable_validation_packets.py
```

This command regenerates the readable Markdown views only. It does not alter the frozen study cases.

## Where should I start?

A clinician or resident validating cases needs the packet and the worksheet. The other files are optional supporting material.

| Who is using it | File |
| --- | --- |
| Resident or clinician reviewing and rating cases | [`clinician_validation_packet.md`](clinician_validation_packet.md) |
| Resident or clinician recording ratings | [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv) |
| Medical educator reviewing the validation criteria | [`validation_rubric.md`](validation_rubric.md) |
| Clinician or resident wanting to understand how CliniProof generates cases | [`how_cliniproof_works.md`](how_cliniproof_works.md) |
| Developer maintaining the pipeline | [`developer_notes.md`](developer_notes.md) |

## Clinician review files

[`clinician_validation_packet.md`](clinician_validation_packet.md) is the primary clinician-facing validation artifact. For each case it contains the readable chart, the intended assessment issue, and the C1–C5 forms. Record ratings on [`clinical_validation_worksheet.csv`](clinical_validation_worksheet.csv), which has one empty row per case.

Individual case pages under [`cases/`](cases/) and the sequential chart dump [`all_cases.md`](all_cases.md) are supporting readable views of the same frozen cases. They do not include the intended assessment issue or rating forms, and they are not a separate review stage.

## Machine validation is not clinical validation

The software performs automated checks of structure, terminology provenance, implemented clinical constraints, and the intended assessment manipulation. Those checks do not establish that a case is clinically realistic or educationally appropriate. Human reviewers make that determination by completing C1–C5 in one pass.
