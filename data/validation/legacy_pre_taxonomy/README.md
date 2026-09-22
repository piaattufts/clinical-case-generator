# Legacy pre-taxonomy V2–V4 artifacts

These folders are **not** taxonomy-compliant resident-validation batches. They are an archive of the pre-taxonomy V2–V4 generation. Do not list them as current CliniProof Family 1 / Family 2 study sets. Do not silently regenerate them in place with the current injector.

The historical record of that generation is **PR #4**, closed without merge. The PR branch was kept:

| Field | Value |
| --- | --- |
| Pull request | [#4](https://github.com/piaattufts/clinical-case-generator/pull/4) (closed, not merged) |
| Branch | `cursor/three-more-validation-batches-9f03` |
| Generating commit | `ba346834b7685b2e6ae13bee374995c9c118ccf3` (`Freeze and export resident-validation batches V2–V4.`) |
| Plan commit | `4711f17` (`Add three additional resident-validation batch plans (V2–V4).`) |
| Injector at that commit | `SUPPORTED_ERROR_FAMILIES = {omission, dose_mismatch, frequency_mismatch, incorrect_continuation}`; unknown preferred category **silently fell back to `omission`** |
| Artifact vocabulary | Historical names only; no `error_family` on plans or answer keys |

Byte-for-byte freeze exports (JSON, CSV, coverage Markdown) match that generating commit. Only the per-folder READMEs were labeled after the move.

## Batches

| Batch code | Public IDs | Internal IDs | Sequences | Master seed | Folder | Exported at |
| --- | --- | --- | --- | --- | --- | --- |
| `RESIDENT_VALIDATION_V2` | `VAL-025`–`VAL-048` | `SYN-000201`–`SYN-000224` | 201–224 | `20260923` | [`v2/`](v2/) | `2026-09-22T14:19:41.836935+00:00` |
| `RESIDENT_VALIDATION_V3` | `VAL-049`–`VAL-072` | `SYN-000301`–`SYN-000324` | 301–324 | `20260924` | [`v3/`](v3/) | `2026-09-22T14:19:44.051450+00:00` |
| `RESIDENT_VALIDATION_V4` | `VAL-073`–`VAL-096` | `SYN-000401`–`SYN-000424` | 401–424 | `20260925` | [`v4/`](v4/) | `2026-09-22T14:19:46.240896+00:00` |

Status language on these artifacts remains: **machine-validated synthetic resident-review cases pending clinician validation**.

## Why they are not taxonomy-compliant

The CliniProof injector on this branch uses canonical IDs (`f1_*`, `f2_*`, `none`), requires `error_family` on new plans, and **rejects** ineligible / `not_yet_implementable` categories instead of substituting. These V2–V4 files were produced before that injector existed. A later mapping table (`omission` → `f1_omission`, …) is documentation only; it does not make the committed cases a Family 1 / Family 2 freeze.

Current study copies:

- `RESIDENT_VALIDATION_V1` (`VAL-001`–`VAL-024`) — also historical injector names; immutable; lives in [`../`](../)
- `CLINIPROOF_TAXONOMY_V1` (`VAL-201`–`VAL-224`) — canonical IDs; lives in [`../cliniproof_v1/`](../cliniproof_v1/)

A new taxonomy-compliant validation set must use a **new** `batch_code` and **new** VAL IDs. Do not reuse `RESIDENT_VALIDATION_V2`–`V4` or `VAL-025`–`VAL-096`.
