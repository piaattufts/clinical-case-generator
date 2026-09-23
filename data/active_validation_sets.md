# Active CliniProof Validation Sets

Two prospective sets are active. They are reviewed separately. Clinical validation is one C1–C5 pass, described in [`../docs/clinical_validation.md`](../docs/clinical_validation.md). Until that review is finished, every record is a machine-checked synthetic chart pending clinician validation.

The descriptive comparison is [`validation_comparison/active_batch_comparison.md`](validation_comparison/active_batch_comparison.md). It does not rank the strategies.

## Balanced structured set

- Batch code: `CLINIPROOF_BALANCED_V4`
- VAL range: VAL-701–VAL-724
- Generation strategy: `balanced_structured`
- Case count: 24
- Status: pending clinician validation
- [Resident cases](validation_balanced_v4/readable/all_cases.md)
- [Clinician packet](validation_balanced_v4/readable/clinician_validation_packet.md)
- [Worksheet](validation_balanced_v4/readable/clinical_validation_worksheet.csv)
- [Diversity report](validation_balanced_v4/diversity_report.md)
- [Manifest](validation_balanced_v4/validation_manifest.json)
- [Batch catalog](validation_balanced_v4/README.md)

## Resident-seed-guided set

- Batch code: `CLINIPROOF_SEEDCASES_V3`
- VAL range: VAL-801–VAL-824
- Generation strategy: `resident_seed_guided`
- Case count: 24
- Six archetype families, four profiles each
- Status: pending clinician validation
- [Resident cases](validation_seedcases_v3/readable/all_cases.md)
- [Clinician packet](validation_seedcases_v3/readable/clinician_validation_packet.md)
- [Worksheet](validation_seedcases_v3/readable/clinical_validation_worksheet.csv)
- [Diversity report](validation_seedcases_v3/diversity_report.md)
- [Manifest](validation_seedcases_v3/validation_manifest.json)
- [Batch catalog](validation_seedcases_v3/README.md)
- [Seed-case provenance](seed_cases/README.md)

## Comparison

[`validation_comparison/active_batch_comparison.md`](validation_comparison/active_batch_comparison.md) summarizes both active batches. It does not include historical freezes and does not choose a preferred strategy.

## Historical

These batches are preserved and are **not** an active prospective study set.

| Batch | Identifiers | Where |
| --- | --- | --- |
| `CLINIPROOF_TAXONOMY_V1` (historical, not the current study set) | VAL-201–VAL-224 | [`validation/README.md`](validation/README.md) |
| `CLINIPROOF_BALANCED_V2` | VAL-301–VAL-324 | [`validation_balanced/README.md`](validation_balanced/README.md) |
| `CLINIPROOF_SEEDCASES_V1` | VAL-401–VAL-424 | [`validation_seedcases/README.md`](validation_seedcases/README.md) |
| `CLINIPROOF_BALANCED_V3` | VAL-501–VAL-524 | [`validation_balanced_v3/README.md`](validation_balanced_v3/README.md) |
| `CLINIPROOF_SEEDCASES_V2` | VAL-601–VAL-624 | [`validation_seedcases_v2/README.md`](validation_seedcases_v2/README.md) |

`CLINIPROOF_TAXONOMY_V1` is archived historical provenance. It was superseded operationally by the two current prospective sets. It is not labeled invalid.
