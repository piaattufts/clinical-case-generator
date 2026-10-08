"""Controlled inpatient episode API for Generation 2.

Synthea supplies the longitudinal patient. This module builds the causal
hospitalization and does not call a language model.
"""

from __future__ import annotations

from typing import Any

from app.services.g2_episode_families import (
    build_endocarditis,
    build_medication_history,
    supports_family,
)
from app.services.g2_episodes import HF_VARIANTS, build_heart_failure
from app.services.g2_remaining import (
    ENDO_VARIANTS,
    GI_VARIANTS,
    HIP_VARIANTS,
    MED_VARIANTS,
    TRANSPLANT_VARIANTS,
    build_gi,
    build_hip,
    build_transplant,
)
from app.sources.synthea import LongitudinalPatient

VARIANTS: dict[str, list[dict[str, Any]]] = {
    "MED_HISTORY_UNCERTAINTY": MED_VARIANTS,
    "HF_DECOMPENSATION": HF_VARIANTS,
    "ENDOCARDITIS_OPAT": ENDO_VARIANTS,
    "TRANSPLANT_CMV": TRANSPLANT_VARIANTS,
    "HIP_FRACTURE_ANTICOAGULATION": HIP_VARIANTS,
    "GI_BLEED_ANTICOAGULATION": GI_VARIANTS,
}

SCENARIO_ORDER = (
    "MED_HISTORY_UNCERTAINTY",
    "HF_DECOMPENSATION",
    "ENDOCARDITIS_OPAT",
    "TRANSPLANT_CMV",
    "HIP_FRACTURE_ANTICOAGULATION",
    "GI_BLEED_ANTICOAGULATION",
)


def variants_for(scenario_code: str) -> list[dict[str, Any]]:
    try:
        return VARIANTS[scenario_code]
    except KeyError as exc:
        raise KeyError(f"unknown Generation 2 scenario {scenario_code}") from exc


def variant_supported(
    patient: LongitudinalPatient, scenario_code: str, variant: dict[str, Any]
) -> bool:
    if scenario_code == "HF_DECOMPENSATION":
        return True
    if scenario_code == "ENDOCARDITIS_OPAT":
        return True
    return supports_family(patient, scenario_code, variant)


def build_episode(
    patient: LongitudinalPatient,
    scenario_code: str,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    if scenario_code == "HF_DECOMPENSATION":
        return build_heart_failure(patient, variant, meta)
    if scenario_code == "MED_HISTORY_UNCERTAINTY":
        return build_medication_history(patient, variant, meta)
    if scenario_code == "ENDOCARDITIS_OPAT":
        return build_endocarditis(patient, variant, meta)
    if scenario_code == "TRANSPLANT_CMV":
        return build_transplant(patient, variant, meta)
    if scenario_code == "HIP_FRACTURE_ANTICOAGULATION":
        return build_hip(patient, variant, meta)
    if scenario_code == "GI_BLEED_ANTICOAGULATION":
        return build_gi(patient, variant, meta)
    raise KeyError(scenario_code)
