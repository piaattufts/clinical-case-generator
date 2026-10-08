# Provenance

Patient-specific facts use one of four classes: synthea_longitudinal, cliniproof_episode_generated, reference_terminology, or investigator_derived_reference.

Synthea did not supply endocarditis in this population. Those infection facts are cliniproof_episode_generated. Renal transplant facts are synthea_longitudinal when the extract contains them. Valganciclovir prophylaxis, when present, is scenario-generated and is not relabeled as Synthea.

Eligibility tiers:

```json
{
  "MED_HISTORY_UNCERTAINTY": {
    "medication_complexity": 32
  },
  "HF_DECOMPENSATION": {
    "compatible_cardiovascular_history": 257,
    "known_heart_failure": 4
  },
  "ENDOCARDITIS_OPAT": {
    "baseline_context_only": 787
  },
  "TRANSPLANT_CMV": {
    "synthea_renal_transplant": 11
  },
  "HIP_FRACTURE_ANTICOAGULATION": {
    "older_adult_warfarin": 13
  },
  "GI_BLEED_ANTICOAGULATION": {
    "warfarin_with_indication": 15
  }
}
```

Final cases: 24.
