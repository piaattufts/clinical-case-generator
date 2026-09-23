# Internal clinical QC report

Investigator-only review of the two active prospective batches before human clinician validation.
Every row is an internal software-and-chart review result. **PASS** means ready for human clinician validation.
It does not mean the case is clinically validated.

## Version decision

`CLINIPROOF_BALANCED_V3` and `CLINIPROOF_SEEDCASES_V2` were already immutable, so those case files were not edited. The prospective sets are `CLINIPROOF_BALANCED_V4` (VAL-701–VAL-724) and `CLINIPROOF_SEEDCASES_V3` (VAL-801–VAL-824). Those two batches had not been sent for human clinician ratings. This final QC patch was therefore applied to the same batch codes. Version codes did not change. No V5 or seed V4 directory was created. Archived `CLINIPROOF_TAXONOMY_V1` remains historical provenance and is not an active study set.

The patch removed answer-revealing resident notes, kept hospital-only and hold rationale on investigator `decision_reason`, held apixaban on VAL-823 so the pending restart decision matches the discharge list, and checked every warfarin case against the answer key. Structured sources were regenerated. Markdown was not hand-edited as the clinical source.

## Answer-revealing chart language

Resident-facing medication notes, indications, held reasons, history, and instructions were scanned for phrases that state the expected disposition or reassure the reader that a dose is correct. Examples include “stop at discharge,” “no outpatient continuation,” “standard labeled dose,” “not a universal dose,” “correct dose,” “hospital-only medication that must be stopped,” and “inpatient-only indication.” The scan of both active resident exports found no remaining hits. Investigator plans still say “Started in hospital for an inpatient-only indication” where that is the clean stop reason. Residents do not receive that field.

## VAL-823

Profile `GI_BLEED_PENDING_AC_DECISION`. Intended category `f2_pending_decision_followup_missing`.

The clean state holds apixaban at discharge (`decision` hold, `correct_discharge_state` hold) because restart versus continued hold is unresolved. The clean fingerprint includes cardiology follow-up in 7 days to reassess that decision. The injected error removes the follow-up. The resident chart still says the decision is pending, and the discharge apixaban row is `held`, not active. Those statements agree.

## Warfarin monitoring audit

Laboratory INR monitoring is not the same task as an anticoagulation-clinic appointment. `f2_monitoring_not_arranged` keeps the clinic follow-up and omits the structured INR monitoring task. Other warfarin-at-discharge cases keep a coherent INR plan. VAL-818 omits warfarin itself, so the remaining INR task is evidence for the omission rather than a second missing-monitoring defect.

| VAL | Warfarin at discharge | Structured INR monitoring | Anticoagulation-clinic follow-up | Intended category | Coherent |
| --- | --- | --- | --- | --- | --- |
| VAL-703 | yes | no | yes | `f2_monitoring_not_arranged` | yes |
| VAL-707 | yes | no | yes | `f2_monitoring_not_arranged` | yes |
| VAL-710 | yes | yes | yes | `none` | yes |
| VAL-817 | yes | no | yes | `f2_monitoring_not_arranged` | yes |
| VAL-818 | no | yes | orthopedic follow-up that also names anticoagulation | `f1_omission` | yes |
| VAL-819 | yes | yes | yes | `f2_insufficient_supply` | yes |
| VAL-820 | yes | yes | no; follow-up is orthopedics | `f2_hospital_only_continued` | yes |

## Case review

Unintended extra discrepancies on this internal isolation check: 0. Cases reviewed: 48. Cases passing: 48.

| VAL | batch | profile/archetype | regimen QC | temporal-role QC | diagnostics QC | intended target isolated | result | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-701 | CLINIPROOF_BALANCED_V4 | HF_VOLUME_OVERLOAD | PASS | PASS | PASS | PASS | PASS | Intended target `f1_omission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-702 | CLINIPROOF_BALANCED_V4 | HF_POST_DIURESIS | PASS | PASS | PASS | PASS | PASS | Intended target `f1_therapeutic_substitution`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-703 | CLINIPROOF_BALANCED_V4 | HF_WITH_WARFARIN | PASS | PASS | PASS | PASS | PASS | Intended target `f2_monitoring_not_arranged`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-704 | CLINIPROOF_BALANCED_V4 | HF_MEDICATION_ADJUSTMENT | PASS | PASS | PASS | PASS | PASS | Intended target `f2_inpatient_substitution_not_reverted`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-705 | CLINIPROOF_BALANCED_V4 | HF_DISCHARGE_MONITORING | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-706 | CLINIPROOF_BALANCED_V4 | AF_RATE_CONTROL_APIXABAN | PASS | PASS | PASS | PASS | PASS | Intended target `f1_omission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-707 | CLINIPROOF_BALANCED_V4 | AF_WARFARIN_INR | PASS | PASS | PASS | PASS | PASS | Intended target `f2_monitoring_not_arranged`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-708 | CLINIPROOF_BALANCED_V4 | AF_WITH_STATIN | PASS | PASS | PASS | PASS | PASS | Intended target `f1_dose_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-709 | CLINIPROOF_BALANCED_V4 | AF_HELD_NSAID | PASS | PASS | PASS | PASS | PASS | Intended target `f2_held_med_no_restart_plan`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-710 | CLINIPROOF_BALANCED_V4 | AF_POST_RATE_CONTROL | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-711 | CLINIPROOF_BALANCED_V4 | HTN_ACE_CCB | PASS | PASS | PASS | PASS | PASS | Intended target `f1_commission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-712 | CLINIPROOF_BALANCED_V4 | HTN_ACE_THIAZIDE | PASS | PASS | PASS | PASS | PASS | Intended target `f1_dose_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-713 | CLINIPROOF_BALANCED_V4 | HTN_CCB_STATIN | PASS | PASS | PASS | PASS | PASS | Intended target `f1_route_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-714 | CLINIPROOF_BALANCED_V4 | HTN_TRIPLE_THERAPY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_hospital_only_continued`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-715 | CLINIPROOF_BALANCED_V4 | HTN_NEW_DIAGNOSIS | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-716 | CLINIPROOF_BALANCED_V4 | T2DM_METFORMIN_ACE | PASS | PASS | PASS | PASS | PASS | Intended target `f1_omission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-717 | CLINIPROOF_BALANCED_V4 | T2DM_METFORMIN_STATIN | PASS | PASS | PASS | PASS | PASS | Intended target `f1_frequency_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-718 | CLINIPROOF_BALANCED_V4 | T2DM_GLYCEMIC_STABILIZATION | PASS | PASS | PASS | PASS | PASS | Intended target `f2_insufficient_supply`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-719 | CLINIPROOF_BALANCED_V4 | T2DM_PENDING_DURATION | PASS | PASS | PASS | PASS | PASS | Intended target `f2_pending_decision_followup_missing`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-720 | CLINIPROOF_BALANCED_V4 | T2DM_CONTROL | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-721 | CLINIPROOF_BALANCED_V4 | CAP_TYPICAL_COUGH | PASS | PASS | PASS | PASS | PASS | Intended target `f1_frequency_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-722 | CLINIPROOF_BALANCED_V4 | CAP_DYSPNEA_WHEEZE | PASS | PASS | PASS | PASS | PASS | Intended target `f1_dose_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-723 | CLINIPROOF_BALANCED_V4 | CAP_INPATIENT_ANTIBIOTIC | PASS | PASS | PASS | PASS | PASS | Intended target `f2_held_med_no_restart_plan`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-724 | CLINIPROOF_BALANCED_V4 | CAP_HOME_TRANSITION | PASS | PASS | PASS | PASS | PASS | Intended target `f2_insufficient_supply`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-801 | CLINIPROOF_SEEDCASES_V3 | MEDREC_COLLATERAL_VERIFIED | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-802 | CLINIPROOF_SEEDCASES_V3 | MEDREC_VERIFIED_STATIN_CONTINUED | PASS | PASS | PASS | PASS | PASS | Intended target `f1_omission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-803 | CLINIPROOF_SEEDCASES_V3 | MEDREC_HOME_SERVICES_SUPPLY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_insufficient_supply`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-804 | CLINIPROOF_SEEDCASES_V3 | MEDREC_PENDING_COGNITIVE_THERAPY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_pending_decision_followup_missing`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-805 | CLINIPROOF_SEEDCASES_V3 | HF_DECOMP_UNCOMPLICATED_DIURESIS | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-806 | CLINIPROOF_SEEDCASES_V3 | HF_DECOMP_AKI_HOLDS | PASS | PASS | PASS | PASS | PASS | Intended target `f2_held_med_no_restart_plan`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-807 | CLINIPROOF_SEEDCASES_V3 | HF_DECOMP_POTASSIUM_REPLACEMENT | PASS | PASS | PASS | PASS | PASS | Intended target `f1_dose_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-808 | CLINIPROOF_SEEDCASES_V3 | HF_DECOMP_DIURETIC_ADJUSTMENT | PASS | PASS | PASS | PASS | PASS | Intended target `f1_therapeutic_substitution`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-809 | CLINIPROOF_SEEDCASES_V3 | OPAT_STABLE_COMPLETION_PLAN | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-810 | CLINIPROOF_SEEDCASES_V3 | OPAT_OMITTED_PARENTERAL_THERAPY | PASS | PASS | PASS | PASS | PASS | Intended target `f1_omission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-811 | CLINIPROOF_SEEDCASES_V3 | OPAT_SHORT_ANTIBIOTIC_SUPPLY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_insufficient_supply`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-812 | CLINIPROOF_SEEDCASES_V3 | OPAT_MISSING_ID_FOLLOWUP | PASS | PASS | PASS | PASS | PASS | Intended target `f2_pending_decision_followup_missing`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-813 | CLINIPROOF_SEEDCASES_V3 | TRANSPLANT_CMV_IMPROVING | PASS | PASS | PASS | PASS | PASS | Intended target `none`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-814 | CLINIPROOF_SEEDCASES_V3 | TRANSPLANT_MMF_HOLD_RESTART | PASS | PASS | PASS | PASS | PASS | Intended target `f2_held_med_no_restart_plan`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-815 | CLINIPROOF_SEEDCASES_V3 | TRANSPLANT_TACROLIMUS_ADJUSTMENT | PASS | PASS | PASS | PASS | PASS | Intended target `f1_dose_mismatch`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-816 | CLINIPROOF_SEEDCASES_V3 | TRANSPLANT_PENDING_ANTIVIRAL_DURATION | PASS | PASS | PASS | PASS | PASS | Intended target `f2_pending_decision_followup_missing`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-817 | CLINIPROOF_SEEDCASES_V3 | POSTOP_WARFARIN_MONITORING | PASS | PASS | PASS | PASS | PASS | Intended target `f2_monitoring_not_arranged`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-818 | CLINIPROOF_SEEDCASES_V3 | POSTOP_OMITTED_ANTICOAGULATION | PASS | PASS | PASS | PASS | PASS | Intended target `f1_omission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-819 | CLINIPROOF_SEEDCASES_V3 | POSTOP_ANTICOAG_SUPPLY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_insufficient_supply`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-820 | CLINIPROOF_SEEDCASES_V3 | POSTOP_BRIDGE_HOSPITAL_ONLY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_hospital_only_continued`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-821 | CLINIPROOF_SEEDCASES_V3 | GI_BLEED_AC_HELD_RESTART | PASS | PASS | PASS | PASS | PASS | Intended target `f2_held_med_no_restart_plan`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-822 | CLINIPROOF_SEEDCASES_V3 | GI_BLEED_PPI_HOSPITAL_ONLY | PASS | PASS | PASS | PASS | PASS | Intended target `f2_hospital_only_continued`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |
| VAL-823 | CLINIPROOF_SEEDCASES_V3 | GI_BLEED_PENDING_AC_DECISION | PASS | PASS | PASS | PASS | PASS | Intended target `f2_pending_decision_followup_missing`. Apixaban is held at discharge, matching the pending restart-versus-hold narrative. Clean follow-up is removed by the injection. No second unintended discrepancy. |
| VAL-824 | CLINIPROOF_SEEDCASES_V3 | GI_BLEED_ASPIRIN_NOT_RESTARTED | PASS | PASS | PASS | PASS | PASS | Intended target `f1_commission`. Regimen dose, route, frequency, temporal role, diagnostics, and isolation were reviewed; no second unintended medication-regimen discrepancy was found. |

Cases reviewed: 48. Cases passing: 48.
