"""Scenario eligibility for the Generation 2 Synthea population.

Rules are explicit. A patient who fails a rule is excluded. Transplant and
endocarditis facts that Synthea did not record are not created here; the
episode engine may add them later under cliniproof_episode_generated.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.services.g2_terminology import regimen_for_product
from app.sources.synthea import LongitudinalPatient, MedicationFact

CARDIAC_MED_IDS = frozenset(
    {
        "METOPROLOL_SUCCINATE_DAILY",
        "METOPROLOL_SUCCINATE_100_DAILY",
        "METOPROLOL_TARTRATE_BID",
        "CARVEDILOL_HF_BID",
        "LISINOPRIL_10_DAILY",
        "LISINOPRIL_20_DAILY",
        "ENALAPRIL_5_BID",
        "FUROSEMIDE_40_DAILY",
        "SPIRONOLACTONE_HF_25",
        "AMLODIPINE_5_DAILY",
        "AMLODIPINE_2_5_DAILY",
    }
)
RAAS_IDS = frozenset({"LISINOPRIL_10_DAILY", "LISINOPRIL_20_DAILY", "ENALAPRIL_5_BID"})
LOOP_IDS = frozenset({"FUROSEMIDE_40_DAILY"})
WARFARIN_IDS = frozenset({"WARFARIN_INR_INDIVIDUALIZED"})
TACROLIMUS_ER_IDS = frozenset({"TACROLIMUS_ER_1MG_DAILY"})


@dataclass(frozen=True)
class MappedMedication:
    display: str
    rxcui: str | None
    regimen_id: str
    dose: str
    route: str
    frequency: str
    synthea_frequency: str | None
    provenance: str = "synthea_longitudinal"


@dataclass(frozen=True)
class Eligibility:
    scenario_code: str
    eligible: bool
    tier: str
    reasons: tuple[str, ...]


def mapped_medications(patient: LongitudinalPatient) -> list[MappedMedication]:
    mapped: list[MappedMedication] = []
    seen: set[str] = set()
    for med in patient.active_medications():
        regimen = regimen_for_product(med.display)
        if regimen is None or regimen.id in seen:
            continue
        seen.add(regimen.id)
        mapped.append(
            MappedMedication(
                display=med.display,
                rxcui=med.rxcui,
                regimen_id=regimen.id,
                dose=regimen.dose,
                route=regimen.route,
                frequency=regimen.frequency,
                synthea_frequency=med.synthea_frequency,
            )
        )
    return mapped


def _adult_alive(patient: LongitudinalPatient) -> tuple[bool, str]:
    if patient.deceased:
        return False, "deceased patients are excluded"
    if patient.age_years < 18:
        return False, "age under 18"
    return True, "adult and alive"


def _has(patient: LongitudinalPatient, token: str) -> bool:
    return token.casefold() in patient.condition_blob()


def _indication(patient: LongitudinalPatient) -> bool:
    blob = patient.condition_blob()
    tokens = (
        "atrial fibrillation",
        "pulmonary embolism",
        "venous thrombosis",
        "deep vein",
        "valve replacement",
        "prosthetic",
        "mechanical valve",
    )
    return any(token in blob for token in tokens)


def has_known_heart_failure(patient: LongitudinalPatient) -> bool:
    return _has(patient, "heart failure")


def has_renal_transplant(patient: LongitudinalPatient) -> bool:
    for text in patient.active_condition_text():
        low = text.casefold()
        if "awaiting transplantation" in low:
            continue
        if "renal transplant" in low or "kidney transplant" in low:
            return True
    return False


def has_synthea_endocarditis(patient: LongitudinalPatient) -> bool:
    return _has(patient, "endocarditis")


def cardiovascular_context(patient: LongitudinalPatient, meds: list[MappedMedication]) -> bool:
    blob = patient.condition_blob()
    condition = any(
        token in blob
        for token in (
            "hypertension",
            "coronary",
            "cardiomyopathy",
            "myocardial",
            "ischemic heart",
            "heart failure",
        )
    )
    med = any(item.regimen_id in CARDIAC_MED_IDS for item in meds)
    return condition and med


def evaluate_patient(patient: LongitudinalPatient) -> dict[str, Eligibility]:
    meds = mapped_medications(patient)
    adult, adult_reason = _adult_alive(patient)
    results: dict[str, Eligibility] = {}

    med_reasons = [adult_reason]
    med_ok = adult and len(meds) >= 4
    if len(meds) < 4:
        med_reasons.append(
            f"{len(meds)} curated single-ingredient outpatient regimens; 4 are required"
        )
    else:
        med_reasons.append(f"{len(meds)} curated outpatient regimens")
    results["MED_HISTORY_UNCERTAINTY"] = Eligibility(
        "MED_HISTORY_UNCERTAINTY", med_ok, "medication_complexity", tuple(med_reasons)
    )

    hf_reasons = [adult_reason]
    known = has_known_heart_failure(patient)
    compatible = cardiovascular_context(patient, meds)
    if known:
        tier = "known_heart_failure"
        hf_reasons.append("active Synthea heart-failure condition")
    elif compatible:
        tier = "compatible_cardiovascular_history"
        hf_reasons.append(
            "no Synthea heart-failure condition; cardiovascular history and medication context"
        )
    else:
        tier = "ineligible"
        hf_reasons.append("no heart-failure condition and no compatible cardiovascular context")
    results["HF_DECOMPENSATION"] = Eligibility(
        "HF_DECOMPENSATION", adult and (known or compatible), tier, tuple(hf_reasons)
    )

    endo_reasons = [adult_reason]
    chronic = len(patient.active_condition_text())
    endo_ok = adult and chronic >= 2
    if has_synthea_endocarditis(patient):
        endo_tier = "synthea_endocarditis"
        endo_reasons.append("Synthea recorded endocarditis")
    else:
        endo_tier = "baseline_context_only"
        endo_reasons.append(
            "Synthea did not record endocarditis; eligibility is baseline context only"
        )
    if chronic < 2:
        endo_reasons.append("fewer than 2 active conditions")
    results["ENDOCARDITIS_OPAT"] = Eligibility(
        "ENDOCARDITIS_OPAT", endo_ok, endo_tier, tuple(endo_reasons)
    )

    transplant_reasons = [adult_reason]
    renal = has_renal_transplant(patient)
    tacro = any(item.regimen_id in TACROLIMUS_ER_IDS for item in meds)
    if renal and tacro:
        transplant_tier = "synthea_renal_transplant"
        transplant_reasons.append("renal transplant history and extended-release tacrolimus")
    elif renal:
        transplant_tier = "transplant_without_curated_tacrolimus"
        transplant_reasons.append(
            "renal transplant is present but no curated extended-release tacrolimus regimen matches"
        )
    else:
        transplant_tier = "ineligible"
        transplant_reasons.append("no Synthea renal-transplant history")
    results["TRANSPLANT_CMV"] = Eligibility(
        "TRANSPLANT_CMV", adult and renal and tacro, transplant_tier, tuple(transplant_reasons)
    )

    warfarin = any(item.regimen_id in WARFARIN_IDS for item in meds)
    indicated = _indication(patient)
    gi_reasons = [adult_reason]
    if not warfarin:
        gi_reasons.append("no active warfarin regimen with a curated dose")
    elif not indicated:
        gi_reasons.append("warfarin is present without an AF, valve, or VTE condition")
    else:
        gi_reasons.append("active warfarin plus a longitudinal anticoagulation indication")
    results["GI_BLEED_ANTICOAGULATION"] = Eligibility(
        "GI_BLEED_ANTICOAGULATION",
        adult and warfarin and indicated,
        "warfarin_with_indication",
        tuple(gi_reasons),
    )

    hip_reasons = list(gi_reasons)
    older = patient.age_years >= 65
    if not older:
        hip_reasons.append("age under 65; hip-fracture eligibility keeps the older-adult rule")
    else:
        hip_reasons.append("age 65 or older")
    results["HIP_FRACTURE_ANTICOAGULATION"] = Eligibility(
        "HIP_FRACTURE_ANTICOAGULATION",
        adult and older and warfarin and indicated,
        "older_adult_warfarin",
        tuple(hip_reasons),
    )
    return results


def medication_fact(patient: LongitudinalPatient, display: str) -> MedicationFact | None:
    for med in patient.active_medications():
        if med.display == display:
            return med
    return None
