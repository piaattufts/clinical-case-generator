# Error taxonomy

This is the human-readable taxonomy for the discrepancies the generator can inject. Other documents should link here instead of keeping a second table. The software identifiers are the source of truth in `app/services/error_taxonomy.py`. A category that is not implemented is rejected. Freeze does not substitute a different category.

Each error-bearing case is assigned one category in the batch plan. Controls use `none`.

## Family 1 — list and field discrepancies

The discharge list itself is wrong relative to the intended plan.

| Category | What the reviewer should find |
| --- | --- |
| `f1_omission` | A medication that should continue is missing from the discharge list. |
| `f1_commission` | A medication that should have stopped is on the discharge list. |
| `f1_dose_mismatch` | The discharge dose differs from the intended dose. |
| `f1_route_mismatch` | The discharge route differs from the intended route. |
| `f1_frequency_mismatch` | The discharge frequency differs from the intended frequency. |
| `f1_therapeutic_substitution` | The discharge list substitutes a same-class drug without a documented reason. |

## Family 2 — trigger present, action missing

The chart still shows why an action was required, and that action is missing.

| Category | What the reviewer should find |
| --- | --- |
| `f2_monitoring_not_arranged` | A drug that needs laboratory monitoring is continued, and the monitoring task is gone. The clinic appointment is not a substitute for that task. |
| `f2_held_med_no_restart_plan` | A drug was held for a documented reason and no restart plan remains. |
| `f2_insufficient_supply` | The days' supply does not cover the planned follow-up. |
| `f2_hospital_only_continued` | A hospital-only drug is still on the discharge list. |
| `f2_inpatient_substitution_not_reverted` | A temporary inpatient formulary substitute was not reverted to home therapy. |
| `f2_pending_decision_followup_missing` | A pending therapeutic decision remains and the follow-up that would resolve it was removed. |

## Not in the active sets

`f2_coprescription_omitted` is defined conceptually and is not implemented. The generator does not invent a companion-drug rule in order to include it.

## Controls

A control has no injected discrepancy. Automated isolation must find zero mechanically detectable reconciliation discrepancies. Clinician C4 still asks whether any unintended clinical problem remains.
