# CliniProof data

## Current resident-facing export

The recovered clean charts for the original 48 slots are in [../exports/clean_balanced_seed_set/](../exports/clean_balanced_seed_set/AUDIT.md). Forty-four are ready for expert review. VAL-709, VAL-711, VAL-714, and VAL-801 are clinically inconsistent and are not validated study cases. Those files were recovered from the frozen sources below. They were not regenerated.

## Frozen source batches

Historical validation artifacts are retained for provenance and reproducibility. They should not be used as the current resident-facing study set.

### Balanced structured

[Overview](case_sets/balanced/README.md) for `CLINIPROOF_BALANCED_V4`, VAL-701–VAL-724.

### Resident-seed-guided

[Overview](case_sets/seed_guided/README.md) for `CLINIPROOF_SEEDCASES_V3`, VAL-801–VAL-824.

Both overviews link to the readable charts, the clinician validation packet, and the worksheet. Those charts still reflect the historical freeze, including injected discrepancies where the batch plan added one.

## Resident-authored seed sources

[Seed-case documentation](seed_cases/README.md). These files are clinical design references for the seed-guided set. They are not the study charts.

## Reference and bootstrap data

[data/bootstrap/](bootstrap/) holds the terminology manifest, scenario profiles, and curated medication regimens used to build cases. Those files are generator inputs. They are not a case set.

A one-page pointer to the two current sets is also at [active_validation_sets.md](active_validation_sets.md).
