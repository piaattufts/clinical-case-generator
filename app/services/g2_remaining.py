"""Transplant, anticoagulation, and the variant catalogs for every family."""

from __future__ import annotations

import random
from typing import Any

from app.services.g2_chart import EPISODE, SYNTHEA, Chart
from app.services.g2_episodes import (
    ENOXAPARIN,
    IBUPROFEN,
    PANTOPRAZOLE,
    TACROLIMUS,
    VALGAN_PROPH,
    VALGAN_TREAT,
    WARFARIN,
    _continue_rest,
    _creatinine,
    _events,
    _find,
    _history,
    _one,
    _products,
    _seed,
    _task,
)
from app.services.g2_terminology import ICD10, regimen_by_id
from app.services.synthea_eligibility import mapped_medications
from app.sources.synthea import LongitudinalPatient

MED_VARIANTS: list[dict[str, Any]] = [
    {
        "variant_id": "delirium_dehydration",
        "precipitant": "poor_intake_and_dehydration",
        "pathway": "exam_chemistry_cognitive_baseline",
        "procedure": "none",
        "chief": "Acute confusion after poor intake",
        "syndrome": "acute confusion that reversed after volume was restored",
        "duration": "two days",
        "symptoms": ["confusion", "poor intake"],
        "acute_text": "Family said the patient was inattentive and newly unable to recognize them. That was a change from the baseline described above.",
        "precipitant_text": "Intake had been only sips for two days after a viral illness. There was no head trauma and no witnessed seizure.",
        "present_text": "On arrival the patient was inattentive, the mucous membranes were dry, and the heart rate was 108.",
        "workup_text": "Chemistry, a complete blood count, and a chest radiograph were obtained before a cause was assigned. The radiograph did not show pneumonia. The examination did not show a focal neurologic deficit.",
        "diagnosis_text": "Delirium due to dehydration was diagnosed after that evaluation. The chart does not describe delirium as the patient's baseline.",
        "treatment_text": "Intravenous fluid was given. Medicines that reduce blood pressure or renal perfusion were reviewed against the creatinine.",
        "response_text": "Creatinine went from {adm:.1f} mg/dL on arrival to {dis:.1f} mg/dL, against a prior value of {base:.1f}. Attention returned, and the caregiver said this matched the patient's usual function.",
        "med_text": "The reconciliation table separates a medicine that was intentionally stopped from medicines that were only unknown on arrival and were later confirmed by the pharmacy.",
    },
    {
        "variant_id": "delirium_uti",
        "precipitant": "urinary_tract_infection",
        "pathway": "urinalysis_culture_then_diagnosis",
        "procedure": "none",
        "chief": "Acute confusion and dysuria",
        "syndrome": "acute confusion with a urine infection found during the work-up",
        "duration": "one day",
        "symptoms": ["confusion", "dysuria"],
        "acute_text": "The patient was newly disoriented to place. The caregiver said the patient had been conversant the day before.",
        "precipitant_text": "Dysuria and frequency began the same day as the confusion. No antibiotic had been started at home.",
        "present_text": "Temperature was 37.8 degrees Celsius. The patient was inattentive and suprapubic tenderness was present.",
        "workup_text": "Urinalysis showed pyuria. A urine culture later grew Escherichia coli. Blood cultures were drawn and showed no growth. The chest radiograph was clear.",
        "diagnosis_text": "Delirium was attributed to the urine infection only after the urinalysis and culture. The infection was not a label on arrival.",
        "treatment_text": "A five-day cephalexin course was completed in the hospital after the culture result. Intravenous fluid was given while intake was poor.",
        "response_text": "Creatinine went from {adm:.1f} mg/dL to {dis:.1f} mg/dL, with a prior value of {base:.1f}. Dysuria resolved and the caregiver confirmed the usual mental status.",
        "med_text": "Cephalexin was a completed course. Outpatient medicines that the pharmacy confirmed were separated from any medicine stopped for a clinical reason.",
    },
    {
        "variant_id": "delirium_pneumonia",
        "precipitant": "lobar_pneumonia",
        "pathway": "radiograph_then_antibiotic",
        "procedure": "chest_radiograph",
        "chief": "Acute confusion and cough",
        "syndrome": "acute confusion with pneumonia found on the chest radiograph",
        "duration": "three days",
        "symptoms": ["confusion", "cough"],
        "acute_text": "Confusion appeared over one day after three days of cough. The patient had been oriented at a visit the prior week.",
        "precipitant_text": "Purulent cough preceded the confusion. Temperature was 36.9 degrees Celsius, so the diagnosis did not depend on fever.",
        "present_text": "Oxygen saturation was 94 percent. There were focal crackles at the right base and new inattention.",
        "workup_text": "The chest radiograph showed a right-lower-lobe infiltrate. Blood cultures showed no growth. Chemistry did not show a primary metabolic cause.",
        "diagnosis_text": "Pneumonia, and delirium due to that infection, were diagnosed after the radiograph. Neither label was the presenting diagnosis.",
        "treatment_text": "Azithromycin was given for the infiltrate and the course was completed before discharge planning. Oxygen was weaned to room air.",
        "response_text": "Cough and inattention resolved. Creatinine was {dis:.1f} mg/dL at discharge planning, admission {adm:.1f}, prior {base:.1f}. The caregiver agreed this was the usual mental status.",
        "med_text": "The antibiotic course is finished. The outpatient list was confirmed with the pharmacy and is not the same thing as a medicine that was deliberately stopped.",
    },
    {
        "variant_id": "hyponatremia_hctz",
        "precipitant": "thiazide_associated_hyponatremia",
        "pathway": "serial_sodium_medication_review",
        "procedure": "none",
        "chief": "Confusion and a low sodium",
        "syndrome": "hyponatremia with thiazide use, distinguished from an unknown medicine",
        "duration": "four days",
        "symptoms": ["confusion", "unsteady gait"],
        "acute_text": "The patient became unsteady and mildly confused over four days. Baseline function, per the caregiver, was independent walking and full orientation.",
        "precipitant_text": "Hydrochlorothiazide was still being taken. No diarrhea or diuretic overdose was described.",
        "present_text": "Sodium on arrival was 128 mmol/L. The patient was euvolemic on examination and inattentive.",
        "workup_text": "Repeat sodium, creatinine, and a chest radiograph were obtained before the thiazide was blamed. The radiograph was clear and the patient was not volume overloaded.",
        "diagnosis_text": "Hypo-osmolality and hyponatremia were established from the sodium result. The thiazide was the implicated medicine after other causes were not found.",
        "treatment_text": "Hydrochlorothiazide was stopped on purpose. Isotonic fluid was given. This stop was intentional and was not an incomplete history.",
        "response_text": "Sodium rose from 128 mmol/L to 134 mmol/L. Creatinine was {dis:.1f} mg/dL compared with {adm:.1f} on arrival and {base:.1f} beforehand. Gait and attention returned to the caregiver's baseline.",
        "med_text": "Hydrochlorothiazide was intentionally discontinued. A separate outpatient medicine was unknown at arrival and was confirmed by the pharmacy rather than stopped.",
    },
    {
        "variant_id": "pharmacy_confirmation",
        "precipitant": "unaccompanied_arrival_without_bottles",
        "pathway": "pharmacy_dispense_history",
        "procedure": "none",
        "chief": "Admission without medication bottles",
        "syndrome": "an resolved outpatient-list discrepancy after pharmacy confirmation",
        "duration": "one day",
        "symptoms": ["weakness"],
        "acute_text": "The patient came unaccompanied after a near-fall at home. Cognition on arrival was at the usual baseline; this was not delirium.",
        "precipitant_text": "No bottles were brought. The patient could not reconstruct the list from memory. That uncertainty was the reason the history was incomplete, and it was resolved before discharge planning.",
        "present_text": "Strength was normal and the patient was oriented. There was no focal deficit and no head injury.",
        "workup_text": "The pharmacy dispense history and a call to the caregiver were obtained before any medicine was called unknown or stopped.",
        "diagnosis_text": "No new inpatient diagnosis replaced the outpatient list. The list itself was reconciled by the pharmacy record.",
        "treatment_text": "Medicines the pharmacy showed as currently filled were continued. One medicine the patient had already stopped for a side effect was left stopped.",
        "response_text": "The patient remained at baseline cognition. Creatinine was {dis:.1f} mg/dL, arrival {adm:.1f}, prior {base:.1f}. The list was no longer uncertain.",
        "med_text": "The intentionally stopped medicine and the medicine that was only forgotten are recorded separately in the reconciliation table.",
    },
    {
        "variant_id": "lisinopril_hold_aki",
        "precipitant": "poor_intake_with_creatinine_rise",
        "pathway": "serial_creatinine_then_volume",
        "procedure": "none",
        "chief": "Poor intake and a rise in creatinine",
        "syndrome": "volume depletion with a held angiotensin-converting enzyme inhibitor or angiotensin-receptor blocker",
        "duration": "three days",
        "symptoms": ["poor intake", "fatigue"],
        "acute_text": "Fatigue and poor intake developed over three days. The patient remained oriented, which separates this admission from delirium.",
        "precipitant_text": "Meals had been skipped and urine output fell. No chest pain was reported.",
        "present_text": "The patient was oriented, the mucous membranes were dry, and the heart rate was elevated for that person.",
        "workup_text": "Chemistry was repeated after fluid. There was no focal infection on examination or chest radiograph.",
        "diagnosis_text": "The creatinine rise was measured before any medicine change was called a reconciliation error. Dehydration was the working cause.",
        "treatment_text": "Intravenous fluid was given. The angiotensin-pathway medicine was held because of the creatinine rise. It is not an unknown medicine.",
        "response_text": "Intake resumed. Creatinine was {dis:.1f} mg/dL versus {adm:.1f} on arrival and {base:.1f} beforehand. Potassium was 4.1 mmol/L and blood pressure was 128/74. No restart order is signed.",
        "med_text": "The angiotensin-pathway medicine remains held. A different outpatient medicine was unknown on arrival and was confirmed by the pharmacy. Those are different problems.",
    },
    {
        "variant_id": "orthostasis_hctz",
        "precipitant": "orthostatic_symptoms_on_thiazide",
        "pathway": "orthostatic_vitals_and_medication_review",
        "procedure": "none",
        "chief": "A fall with lightheadedness on standing",
        "syndrome": "orthostasis related to a thiazide, with the rest of the list confirmed",
        "duration": "one week",
        "symptoms": ["lightheadedness", "fall"],
        "acute_text": "Lightheadedness on standing began over a week and ended in a fall. There was no loss of consciousness and no confusion.",
        "precipitant_text": "Hydrochlorothiazide was still being taken each morning. The fall happened when the patient stood from a chair.",
        "present_text": "Supine blood pressure was 148/82. Standing blood pressure was 102/64, with reproduced lightheadedness. Cognition was at baseline.",
        "workup_text": "Orthostatic vital signs, creatinine, sodium, and a hip radiograph were obtained. The radiograph showed no fracture. Sodium was not low.",
        "diagnosis_text": "Orthostatic hypotension was documented by the standing vital signs. The thiazide was the implicated medicine.",
        "treatment_text": "Hydrochlorothiazide was stopped intentionally. Fluid was encouraged. This was not an unknown medicine.",
        "response_text": "Standing blood pressure was 126/74 without lightheadedness before discharge planning. Creatinine was {dis:.1f} mg/dL, arrival {adm:.1f}, prior {base:.1f}.",
        "med_text": "The thiazide stop is intentional. Another outpatient medicine was missing from the patient's recall and was confirmed by the pharmacy.",
    },
    {
        "variant_id": "nsaid_dyspepsia",
        "precipitant": "nsaid_dyspepsia",
        "pathway": "medication_history_and_creatinine",
        "procedure": "none",
        "chief": "Epigastric pain and an uncertain medication list",
        "syndrome": "dyspepsia after ibuprofen, with the rest of the list confirmed",
        "duration": "one week",
        "symptoms": ["epigastric pain"],
        "acute_text": "Epigastric burning began after a week of ibuprofen for knee pain. There was no melena and no confusion.",
        "precipitant_text": "Ibuprofen was a real outpatient exposure, not a missing history item. The patient had chosen it for pain and then developed burning pain.",
        "present_text": "The abdomen was soft with epigastric tenderness and no peritoneal signs. Stool testing for occult blood was negative.",
        "workup_text": "A complete blood count, creatinine, and the medication history were reviewed before the anti-inflammatory drug was classified as stopped rather than unknown.",
        "diagnosis_text": "Dyspepsia related to the anti-inflammatory drug was the working diagnosis after the examination and the negative bleeding evaluation.",
        "treatment_text": "Ibuprofen was stopped because of the pain and a creatinine rise. Pantoprazole was not started because there was no bleeding.",
        "response_text": "Epigastric pain resolved. Creatinine returned from {adm:.1f} mg/dL to {dis:.1f} mg/dL, prior {base:.1f}.",
        "med_text": "Ibuprofen was intentionally stopped. It is not an unknown medicine. The pharmacy confirmed the other outpatient medicines the patient could not list on arrival.",
    },
]

ENDO_VARIANTS: list[dict[str, Any]] = [
    {
        "variant_id": "dental_mitral",
        "precipitant": "recent_dental_extraction",
        "pathway": "cultures_then_mitral_echo",
        "disposition": "home",
        "organism": "Streptococcus sanguinis",
        "echo": "an 8 mm mitral vegetation without abscess or severe regurgitation",
        "source_text": "A dental extraction occurred two weeks earlier. Skin examination showed no abscess. The dental procedure is the predisposition recorded for this episode.",
    },
    {
        "variant_id": "no_source_aortic",
        "precipitant": "no_source_after_directed_evaluation",
        "pathway": "cultures_then_aortic_echo_negative_source_search",
        "disposition": "home",
        "organism": "Streptococcus mitis",
        "echo": "a 6 mm aortic vegetation without abscess",
        "source_text": "Dental and skin examinations and a review for intravenous drug use did not find a source. The absence of a source was a result of that evaluation, not an omitted history.",
    },
    {
        "variant_id": "gi_source_evaluated",
        "precipitant": "gastrointestinal_source_evaluation",
        "pathway": "cultures_echo_and_gi_consultation",
        "disposition": "skilled nursing facility",
        "organism": "Streptococcus gallolyticus",
        "echo": "a 7 mm mitral vegetation without abscess",
        "source_text": "Because this organism is associated with colonic lesions, gastroenterology was consulted. A colonoscopy was scheduled after the acute infection, rather than claimed as already done.",
    },
    {
        "variant_id": "bicuspid_predisposition",
        "precipitant": "bicuspid_aortic_valve",
        "pathway": "cultures_and_echo_showing_bicuspid_valve",
        "disposition": "home",
        "organism": "Streptococcus sanguinis",
        "echo": "a bicuspid aortic valve with a 5 mm vegetation and no abscess",
        "source_text": "The echocardiogram identified a bicuspid aortic valve, which is the predisposition. No recent dental procedure was reported.",
    },
    {
        "variant_id": "skin_source",
        "precipitant": "resolved_skin_abscess",
        "pathway": "cultures_echo_and_skin_exam",
        "disposition": "home",
        "organism": "Streptococcus anginosus",
        "echo": "a 6 mm mitral vegetation without abscess",
        "source_text": "A drained skin abscess had closed two weeks before the fever. The wound was examined and was not still draining. The organism was a streptococcus treated with the ceftriaxone regimen, not a staphylococcal regimen.",
    },
    {
        "variant_id": "surgery_consult_no_indication",
        "precipitant": "unknown_portal_after_exam",
        "pathway": "cultures_echo_and_surgical_review",
        "disposition": "home",
        "organism": "Streptococcus mitis",
        "echo": "a 9 mm aortic vegetation, no abscess, and normal forward flow",
        "source_text": "No dental, skin, or urinary source was found. Surgery reviewed the study because the vegetation was the largest in this family and found no indication for an operation.",
    },
    {
        "variant_id": "opat_home_infusion",
        "precipitant": "dental_cleaning",
        "pathway": "cultures_echo_home_infusion_assessment",
        "disposition": "home",
        "organism": "Streptococcus sanguinis",
        "echo": "a 5 mm mitral vegetation without abscess",
        "source_text": "A dental cleaning occurred ten days before the fever. Home infusion nursing assessed the residence and found it suitable.",
    },
    {
        "variant_id": "opat_skilled_nursing",
        "precipitant": "no_home_infusion_support",
        "pathway": "cultures_echo_skilled_nursing_assessment",
        "disposition": "skilled nursing facility",
        "organism": "Streptococcus gallolyticus",
        "echo": "a 7 mm aortic vegetation without abscess",
        "source_text": "No infusion caregiver was available at home. A skilled nursing facility accepted the patient for intravenous therapy. A colonic evaluation remains scheduled, and it was not pretended to have occurred already.",
    },
]

TRANSPLANT_VARIANTS: list[dict[str, Any]] = [
    {"variant_id": "colitis_biopsy", "precipitant": "diarrhea_without_prior_antiviral", "pathway": "stool_studies_pcr_then_biopsy", "procedure": "flex_sig_biopsy", "prophylaxis": False, "aki": True, "form": "colitis"},
    {"variant_id": "prophylaxis_breakthrough", "precipitant": "breakthrough_during_scenario_prophylaxis", "pathway": "pcr_on_prophylaxis_then_induction", "procedure": "none", "prophylaxis": True, "aki": False, "form": "syndrome"},
    {"variant_id": "pcr_syndrome", "precipitant": "fever_and_leukopenia", "pathway": "pcr_without_colitis", "procedure": "none", "prophylaxis": False, "aki": False, "form": "syndrome"},
    {"variant_id": "cdiff_excluded", "precipitant": "diarrhea_after_negative_c_difficile", "pathway": "c_difficile_negative_then_pcr_and_biopsy", "procedure": "flex_sig_biopsy", "prophylaxis": False, "aki": True, "form": "colitis"},
    {"variant_id": "leukopenia_recovered", "precipitant": "viremia_with_leukopenia", "pathway": "pcr_and_serial_leukocyte_count", "procedure": "none", "prophylaxis": False, "aki": False, "form": "syndrome"},
    {"variant_id": "volume_loss", "precipitant": "high_volume_diarrhea", "pathway": "volume_exam_chemistry_pcr_biopsy", "procedure": "flex_sig_biopsy", "prophylaxis": False, "aki": True, "form": "colitis"},
    {"variant_id": "transplant_clinic_followup", "precipitant": "subacute_diarrhea", "pathway": "pcr_biopsy_transplant_clinic_plan", "procedure": "flex_sig_biopsy", "prophylaxis": False, "aki": False, "form": "colitis"},
    {"variant_id": "id_clinic_followup", "precipitant": "fever_without_diarrhea", "pathway": "pcr_only_id_clinic_plan", "procedure": "none", "prophylaxis": False, "aki": False, "form": "syndrome"},
]

HIP_VARIANTS: list[dict[str, Any]] = [
    {"variant_id": "inr_delay_home", "precipitant": "ground_level_fall", "pathway": "xray_inr_then_orif", "disposition": "home", "bleeding": False, "restart": "restart"},
    {"variant_id": "snf_after_orif", "precipitant": "fall_from_standing", "pathway": "xray_inr_orif_therapy_recommendation", "disposition": "skilled nursing facility", "bleeding": False, "restart": "restart"},
    {"variant_id": "wound_hematoma_hold", "precipitant": "fall_with_postoperative_oozing", "pathway": "xray_orif_then_hematoma", "disposition": "home", "bleeding": True, "restart": "hold"},
    {"variant_id": "mechanical_valve_context", "precipitant": "fall_in_a_patient_with_a_prosthetic_valve", "pathway": "xray_inr_orif_valve_history", "disposition": "home", "bleeding": False, "restart": "restart"},
    {"variant_id": "af_early_hemostasis", "precipitant": "fall_with_prompt_hemostasis", "pathway": "xray_orif_day2_hemostasis", "disposition": "home", "bleeding": False, "restart": "restart"},
    {"variant_id": "delayed_mobilization_snf", "precipitant": "fall_with_slow_mobilization", "pathway": "xray_orif_physical_therapy", "disposition": "skilled nursing facility", "bleeding": False, "restart": "restart"},
    {"variant_id": "supratherapeutic_inr", "precipitant": "fall_while_inr_was_above_range", "pathway": "inr_reversal_without_a_new_drug_then_orif", "disposition": "home", "bleeding": False, "restart": "restart"},
    {"variant_id": "hematoma_snf", "precipitant": "fall_with_a_stable_wound_hematoma", "pathway": "orif_hematoma_observation", "disposition": "skilled nursing facility", "bleeding": True, "restart": "hold"},
]

GI_VARIANTS: list[dict[str, Any]] = [
    {"variant_id": "duodenal_ulcer_restart", "precipitant": "melena", "pathway": "egd_duodenal_ulcer", "source": "duodenal ulcer with a clean base", "code": "K26.4", "upper": True, "restart": "restart", "transfused": False, "nsaid": False},
    {"variant_id": "gastric_ulcer_inr", "precipitant": "hematemesis", "pathway": "egd_gastric_ulcer_supratherapeutic_inr", "source": "gastric ulcer with a clean base", "code": "K25.4", "upper": True, "restart": "restart", "transfused": True, "nsaid": False},
    {"variant_id": "diverticular_hold", "precipitant": "hematochezia", "pathway": "colonoscopy_diverticular_bleed", "source": "diverticulosis with stigmata of recent bleeding", "code": "K57.31", "upper": False, "restart": "hold", "transfused": False, "nsaid": False},
    {"variant_id": "esophagitis", "precipitant": "melena_and_reflux", "pathway": "egd_esophagitis", "source": "erosive esophagitis without a spurting vessel", "code": "K20.90", "upper": True, "restart": "restart", "transfused": False, "nsaid": False},
    {"variant_id": "nsaid_and_warfarin", "precipitant": "melena_after_ibuprofen", "pathway": "egd_ulcer_and_nsaid_review", "source": "duodenal ulcer with a clean base", "code": "K26.4", "upper": True, "restart": "restart", "transfused": False, "nsaid": True},
    {"variant_id": "transfused_stable", "precipitant": "melena_with_tachycardia", "pathway": "resuscitation_egd_ulcer", "source": "gastric ulcer with a flat pigmented spot", "code": "K25.4", "upper": True, "restart": "restart", "transfused": True, "nsaid": False},
    {"variant_id": "defer_restart", "precipitant": "hematochezia", "pathway": "colonoscopy_then_unresolved_restart_timing", "source": "diverticulosis with stigmata of recent bleeding", "code": "K57.31", "upper": False, "restart": "hold", "transfused": True, "nsaid": False},
    {"variant_id": "stable_no_transfusion", "precipitant": "melena_hemodynamically_stable", "pathway": "egd_ulcer_no_transfusion", "source": "duodenal ulcer with a clean base", "code": "K26.4", "upper": True, "restart": "restart", "transfused": False, "nsaid": False},
]


def build_transplant(
    patient: LongitudinalPatient,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    meds = mapped_medications(patient)
    tacrolimus = _find(meds, {TACROLIMUS})
    if tacrolimus is None:
        raise ValueError("transplant episode requires extended-release tacrolimus")
    rng = random.Random(_seed(meta, patient, "TRANSPLANT_CMV", variant["variant_id"]))
    base_cr, cr_src = _creatinine(patient, rng)
    aki = bool(variant["aki"])
    adm_cr = _one(min(base_cr + 0.7, 2.2)) if aki else _one(base_cr + 0.1)
    dis_cr = _one(base_cr + 0.1) if aki else base_cr
    chart = Chart(
        patient=patient,
        scenario_code="TRANSPLANT_CMV",
        variant_id=variant["variant_id"],
        eligibility_tier="synthea_renal_transplant",
        episode_seed=_seed(meta, patient, "TRANSPLANT_CMV", variant["variant_id"]),
        fingerprint={
            "scenario": "TRANSPLANT_CMV",
            "variant_id": variant["variant_id"],
            "precipitant": variant["precipitant"],
            "diagnostic_pathway": variant["pathway"],
            "renal_pattern": "aki_recovered" if aki else "creatinine_stable",
            "procedure": variant["procedure"],
            "disposition": "home",
            "prophylaxis": "scenario_prophylaxis" if variant["prophylaxis"] else "no_home_antiviral",
            "disease_form": variant["form"],
        },
        physiology_expectations=["aki_recovered"] if aki else [],
        synthea_meta=meta,
        chief_complaint="Diarrhea" if variant["form"] == "colitis" else "Fever and fatigue",
        syndrome="cytomegalovirus disease established during the hospitalization, not as the presenting label",
        symptom_duration="eight days",
        symptom_course="stool frequency or fever improved after diagnosis and antiviral therapy",
        symptoms=["diarrhea"] if variant["form"] == "colitis" else ["fever", "fatigue"],
        disposition="home",
        specialty="transplant medicine",
    )
    _history(chart, patient)
    chart.diagnosis(ICD10["Z94.0"], "Z94.0", "past_history", SYNTHEA, context="history")
    dx_code = "B25.8" if variant["form"] == "colitis" else "B25.9"
    chart.diagnosis(ICD10[dx_code], dx_code, "hospital", EPISODE)
    if aki:
        chart.diagnosis(ICD10["N17.9"], "N17.9", "hospital", EPISODE)
        chart.diagnosis(ICD10["E87.6"], "E87.6", "hospital", EPISODE)
    chart.fact(
        "tx-base",
        ["baseline"],
        (
            "The longitudinal record includes renal transplant status and extended-release tacrolimus. "
            f"Other outpatient products in the extract: {_products(meds)}."
        ),
        SYNTHEA,
        10,
        "hpi",
    )
    if variant["prophylaxis"]:
        chart.fact(
            "tx-prophylaxis",
            ["baseline", "medication_decision"],
            (
                "A prior valganciclovir prophylaxis course, 900 MG once daily, is part of this "
                "scenario. It was not on the pre-admission medication list."
            ),
            EPISODE,
            14,
            "hpi",
        )
    else:
        chart.fact(
            "tx-no-antiviral",
            ["baseline", "medication_decision"],
            "Valganciclovir was not a home medicine. None was inferred from transplant status alone.",
            EPISODE,
            14,
            "hpi",
        )
    chart.fact(
        "tx-acute",
        ["acute_change"],
        (
            "Eight days of watery stool, up to ten movements a day, were new."
            if variant["form"] == "colitis"
            else "Fever and fatigue for six days were new. There was no chronic febrile illness at baseline."
        ),
        EPISODE,
        20,
        "hpi",
    )
    chart.fact(
        "tx-precip",
        ["precipitant"],
        (
            "The transplant and the immunosuppression are the predisposition. "
            + (
                "Stool testing for Clostridioides difficile toxin was negative before cytomegalovirus testing was treated as the cause."
                if variant["variant_id"] == "cdiff_excluded"
                else "Rejection, drug toxicity, and ordinary gastroenteritis were still on the differential at arrival."
            )
        ),
        EPISODE,
        30,
        "hpi",
    )
    chart.fact(
        "tx-present",
        ["presentation"],
        (
            f"Arrival creatinine was {adm_cr:.1f} mg/dL"
            + (" and potassium was 3.2 mmol/L. The mucous membranes were dry." if aki else ".")
            + " The presentation was the symptom above, not a preassigned cytomegalovirus diagnosis."
        ),
        EPISODE,
        40,
        "hpi",
    )
    work = "Plasma cytomegalovirus DNA was detected after the symptom evaluation."
    if variant["procedure"] == "flex_sig_biopsy":
        work += " Flexible sigmoidoscopy then showed colitis, and the biopsy was consistent with cytomegalovirus colitis."
    else:
        work += " There was no colitis syndrome, so endoscopy was not required to name cytomegalovirus syndrome."
    chart.fact("tx-work", ["workup"], work, EPISODE, 50, "course")
    chart.fact(
        "tx-dx",
        ["diagnosis"],
        "The cytomegalovirus diagnosis followed that testing. It was not the admitting label.",
        EPISODE,
        60,
        "course",
    )
    chart.fact(
        "tx-treat",
        ["treatment", "medication_decision"],
        (
            "Valganciclovir induction, 900 MG twice daily, was started only after the diagnostic result. "
            "Tacrolimus was continued at the recorded once-daily extended-release dose. "
            "Mycophenolate was not added, because it was not in the longitudinal record. "
            f"Creatinine at that point was {adm_cr:.1f} mg/dL and later {dis_cr:.1f} mg/dL, within the range for the full induction dose."
        ),
        EPISODE,
        70,
        "course",
    )
    chart.fact(
        "tx-response",
        ["response", "physiology"],
        (
            "Stool frequency fell to three movements a day and the patient was drinking."
            if variant["form"] == "colitis"
            else "Fever resolved and the patient was eating."
        )
        + (
            f" Potassium was 4.0 mmol/L after having been 3.2. Creatinine was {dis_cr:.1f} mg/dL."
            if aki
            else f" Creatinine remained {dis_cr:.1f} mg/dL."
        )
        + " Plasma cytomegalovirus DNA was still detected, which is expected this early.",
        EPISODE,
        80,
        "course",
    )
    follow_service = (
        "transplant clinic"
        if "transplant_clinic" in variant["variant_id"]
        else "infectious diseases"
    )
    chart.fact(
        "tx-ready",
        ["discharge_readiness"],
        f"The patient was keeping fluids down and walking. Follow-up with {follow_service} was arranged. The induction course was not signed as a finished discharge list.",
        EPISODE,
        90,
        "course",
    )
    chart.fact("tx-follow", ["followup"], f"Weekly laboratory monitoring and {follow_service} follow-up were specified.", EPISODE, 95, "course")
    _events(
        chart,
        [
            ("baseline", 10, "Transplant and tacrolimus"),
            ("acute_change", 20, "New symptoms"),
            ("precipitant", 30, variant["precipitant"]),
            ("presentation", 40, "Symptom presentation"),
            ("workup", 50, "Testing before antiviral induction"),
            ("diagnosis", 60, "Cytomegalovirus disease after testing"),
            ("treatment", 70, "Induction after the result"),
            ("response", 80, "Symptom and volume response"),
            ("discharge", 100, "Ready for an unsigned discharge plan"),
        ],
    )
    chart.lab("2160-0", [("baseline", base_cr), ("admission", adm_cr), ("peak", adm_cr), ("discharge", dis_cr)], EPISODE)
    if cr_src == SYNTHEA:
        for row in chart.labs:
            if row["loinc_code"] == "2160-0" and row["timepoint"] == "baseline":
                row["provenance"] = SYNTHEA
    chart.lab("2823-3", [("admission", 3.2 if aki else 4.1), ("discharge", 4.0 if aki else 4.2)], EPISODE)
    chart.lab("30246-3", [("intermediate", "detected"), ("discharge", "detected")], EPISODE)
    chart.lab("6690-2", [("admission", 3.4), ("nadir", 2.6), ("discharge", 3.5)] if variant["variant_id"] == "leukopenia_recovered" else [("admission", 6.2), ("discharge", 5.8)], EPISODE)
    chart.vital("admission", temp_c=38.2 if variant["form"] == "syndrome" else 37.1, bp_systolic=108 if aki else 132, bp_diastolic=64 if aki else 78, heart_rate=112 if aki else 84, resp_rate=16, spo2_percent=98, provenance=EPISODE)
    chart.vital("discharge", temp_c=36.7, bp_systolic=124, bp_diastolic=74, heart_rate=78, resp_rate=16, spo2_percent=98, provenance=EPISODE)
    if variant["procedure"] == "flex_sig_biopsy":
        chart.procedure(
            "Flexible sigmoidoscopy with biopsy",
            "hospital day 2",
            "Colitis. Biopsy consistent with cytomegalovirus.",
            EPISODE,
        )
    if variant["variant_id"] == "cdiff_excluded":
        chart.microbiology(
            "admission",
            "stool",
            "Clostridioides difficile toxin",
            "negative",
            EPISODE,
            notes="Result available before antiviral therapy.",
        )
    tacro = regimen_by_id(TACROLIMUS)
    chart.medication(
        drug=tacro.query,
        dose=tacro.dose,
        route=tacro.route,
        frequency=tacro.frequency,
        indication="maintenance immunosuppression after kidney transplant",
        regimen_id=TACROLIMUS,
        identity_provenance=SYNTHEA,
        rxcui=tacrolimus.rxcui,
        synthea_product=tacrolimus.display,
        states=[
            {"state": "home", "time_order": 10, "trigger": "longitudinal outpatient product", "evidence": ["tx-base"], "provenance": SYNTHEA},
            {"state": "continued_inpatient", "time_order": 70, "trigger": "transplant indication unchanged and no new contraindication", "evidence": ["tx-treat"], "provenance": EPISODE},
        ],
        discharge_action="continue",
        evidence_ids=["tx-base", "tx-treat", "tx-response"],
        resident_note="Extended-release tacrolimus was continued once daily. It was not converted to an every-12-hour product.",
        rationale="Continuing the recorded extended-release dose is supported by ongoing transplant indication and the absence of a toxicity event that required a change.",
        monitoring="Tacrolimus trough at the transplant visit.",
        follow_up=follow_service,
    )
    antiviral = regimen_by_id(VALGAN_TREAT)
    chart.medication(
        drug=antiviral.query,
        dose=antiviral.dose,
        route=antiviral.route,
        frequency=antiviral.frequency,
        indication="cytomegalovirus induction after laboratory or histologic confirmation",
        regimen_id=VALGAN_TREAT,
        identity_provenance=EPISODE,
        rxcui=None,
        synthea_product=None,
        states=[
            {
                "state": "home" if variant["prophylaxis"] else "new_inpatient",
                "time_order": 10 if variant["prophylaxis"] else 70,
                "trigger": "scenario prophylaxis" if variant["prophylaxis"] else "started after the diagnostic result",
                "evidence": ["tx-prophylaxis"] if variant["prophylaxis"] else ["tx-dx", "tx-treat"],
                "provenance": EPISODE,
            }
        ],
        discharge_action="dose_change" if variant["prophylaxis"] else "new_start",
        evidence_ids=["tx-work", "tx-dx", "tx-treat", "tx-response"],
        resident_note=(
            "Home scenario prophylaxis was 900 MG once daily. The inpatient dose after confirmation is 900 MG twice daily. Creatinine supports that induction dose."
            if variant["prophylaxis"]
            else "Started after confirmation. Not a home medicine. Induction dose 900 MG twice daily."
        ),
        rationale=(
            "A change from prophylaxis to induction is supported by confirmed disease, preserved renal function, and an incomplete treatment course."
            if variant["prophylaxis"]
            else "Starting induction is supported because the drug was absent at home, the diagnosis followed testing, and renal function allows the labeled induction dose."
        ),
        monitoring="Weekly complete blood count, creatinine, and cytomegalovirus DNA.",
        follow_up=f"{follow_service} within 7 days.",
        alternatives=[
            {
                "alternative_action": "hold",
                "conditions": "If the leukocyte count falls below 2.0 x10^3/uL.",
                "rationale": "Holding would then be a response to marrow toxicity. It is not the current situation: the latest leukocyte count is above that threshold.",
            }
        ]
        if variant["variant_id"] == "leukopenia_recovered"
        else [],
    )
    if variant["prophylaxis"]:
        chart.medications[-1]["home_dose"] = regimen_by_id(VALGAN_PROPH).dose
        chart.medications[-1]["home_frequency"] = regimen_by_id(VALGAN_PROPH).frequency
    _continue_rest(chart, meds, {TACROLIMUS, VALGAN_TREAT, VALGAN_PROPH}, ["tx-base", "tx-ready"], "unchanged outpatient indication")
    chart.monitor("complete blood count, creatinine, and cytomegalovirus DNA", "weekly", "during induction", follow_service)
    chart.follow(follow_service, "within 7 days", follow_service)
    _task(chart)
    return chart.to_episode()


def build_hip(
    patient: LongitudinalPatient,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    meds = mapped_medications(patient)
    warfarin = _find(meds, {WARFARIN})
    if warfarin is None:
        raise ValueError("hip-fracture episode requires warfarin")
    rng = random.Random(_seed(meta, patient, "HIP_FRACTURE_ANTICOAGULATION", variant["variant_id"]))
    base_cr, _cr_src = _creatinine(patient, rng)
    high_inr = variant["variant_id"] == "supratherapeutic_inr"
    adm_inr = 4.2 if high_inr else 2.6
    chart = Chart(
        patient=patient,
        scenario_code="HIP_FRACTURE_ANTICOAGULATION",
        variant_id=variant["variant_id"],
        eligibility_tier="older_adult_warfarin",
        episode_seed=_seed(meta, patient, "HIP_FRACTURE_ANTICOAGULATION", variant["variant_id"]),
        fingerprint={
            "scenario": "HIP_FRACTURE_ANTICOAGULATION",
            "variant_id": variant["variant_id"],
            "precipitant": variant["precipitant"],
            "diagnostic_pathway": variant["pathway"],
            "renal_pattern": "creatinine_stable",
            "procedure": "orif_right_femoral_neck",
            "disposition": variant["disposition"],
            "restart_decision": variant["restart"],
            "bleeding": "wound_hematoma" if variant["bleeding"] else "hemostasis",
        },
        physiology_expectations=["inr_down"],
        synthea_meta=meta,
        chief_complaint="Right hip pain after a fall",
        syndrome="a right femoral-neck fracture treated after the INR fell",
        symptom_duration="hours",
        symptom_course="pain controlled and the wound reviewed before discharge planning",
        symptoms=["hip pain", "inability to bear weight"],
        disposition=variant["disposition"],
        specialty="internal medicine",
    )
    _history(chart, patient)
    chart.diagnosis(ICD10["S72.001A"], "S72.001A", "hospital", EPISODE)
    chart.fact(
        "hip-base",
        ["baseline"],
        (
            f"The longitudinal extract includes warfarin ({warfarin.display}) and an anticoagulation indication "
            f"among the active conditions. Other products: {_products(meds)}."
        ),
        SYNTHEA,
        10,
        "hpi",
    )
    chart.fact(
        "hip-acute",
        ["acute_change"],
        "A ground-level fall was followed immediately by right hip pain and inability to bear weight. That was not the prior mobility.",
        EPISODE,
        20,
        "hpi",
    )
    chart.fact("hip-precip", ["precipitant"], variant["precipitant"].replace("_", " ") + ". No chest pain or syncope was described.", EPISODE, 30, "hpi")
    chart.fact(
        "hip-present",
        ["presentation"],
        f"The right leg was shortened and externally rotated. Arrival INR was {adm_inr:.1f}. Warfarin was held on arrival.",
        EPISODE,
        40,
        "hpi",
    )
    chart.fact(
        "hip-work",
        ["workup"],
        "A radiograph, not the history alone, showed a right femoral-neck fracture. The INR was repeated before the operating room.",
        EPISODE,
        50,
        "course",
    )
    chart.fact(
        "hip-dx",
        ["diagnosis"],
        "The fracture diagnosis followed the radiograph. Anticoagulation management was then planned around that injury.",
        EPISODE,
        60,
        "course",
    )
    bleed = (
        "A wound hematoma was present on postoperative day 1 and was not expanding. Hemoglobin was stable."
        if variant["bleeding"]
        else "The wound was dry and hemoglobin was stable after surgery."
    )
    chart.fact(
        "hip-treat",
        ["treatment", "medication_decision"],
        (
            f"Surgery waited until the INR was 1.3. No separate reversal drug was charted. "
            f"Open reduction and internal fixation was then performed. {bleed} "
            "Enoxaparin 40 MG subcutaneously once daily was used for postoperative prophylaxis while warfarin remained held."
        ),
        EPISODE,
        70,
        "course",
    )
    chart.fact(
        "hip-response",
        ["response", "physiology"],
        (
            f"INR fell from {adm_inr:.1f} to 1.3. Creatinine stayed near {base_cr:.1f} mg/dL. "
            "Pain was controlled with non-opioid measures and the patient could sit and transfer with therapy."
        ),
        EPISODE,
        80,
        "course",
    )
    chart.fact(
        "hip-ready",
        ["discharge_readiness"],
        (
            f"Therapy recommended {variant['disposition']}. The wound assessment is the one above. "
            "Warfarin and the prophylactic anticoagulant do not yet have a signed discharge order."
        ),
        EPISODE,
        90,
        "course",
    )
    chart.fact("hip-follow", ["followup"], "Orthopedics, the anticoagulation indication's clinician, and a wound check were arranged.", EPISODE, 95, "course")
    _events(
        chart,
        [
            ("baseline", 10, "Warfarin and prior mobility"),
            ("acute_change", 20, "Fall and inability to bear weight"),
            ("precipitant", 30, "Fall"),
            ("presentation", 40, "Deformity and INR"),
            ("workup", 50, "Radiograph and repeat INR"),
            ("diagnosis", 60, "Femoral-neck fracture"),
            ("treatment", 70, "Delayed fixation, then prophylaxis"),
            ("response", 80, "INR down and wound assessed"),
            ("discharge", 100, "Disposition recommended, anticoagulation unsigned"),
        ],
    )
    chart.lab("6301-6", [("admission", adm_inr), ("intermediate", 1.3), ("discharge", 1.3)], EPISODE)
    chart.lab("718-7", [("admission", 12.4), ("discharge", 11.2 if variant["bleeding"] else 11.8)], EPISODE)
    chart.lab("2160-0", [("admission", base_cr), ("discharge", base_cr)], EPISODE)
    chart.vital("admission", temp_c=36.7, bp_systolic=146, bp_diastolic=78, heart_rate=92, resp_rate=16, spo2_percent=97, provenance=EPISODE)
    chart.vital("discharge", temp_c=36.8, bp_systolic=132, bp_diastolic=74, heart_rate=78, resp_rate=16, spo2_percent=97, provenance=EPISODE)
    chart.procedure("Open reduction and internal fixation of the right femoral neck", "after INR 1.3", "Fixation completed.", EPISODE, complications="wound hematoma" if variant["bleeding"] else "none")
    chart.image("admission", "Right hip radiograph", "Femoral-neck fracture.", EPISODE)
    war = regimen_by_id(WARFARIN)
    chart.medication(
        drug=war.query,
        dose=war.dose,
        route=war.route,
        frequency=war.frequency,
        indication="longitudinal anticoagulation indication",
        regimen_id=WARFARIN,
        identity_provenance=SYNTHEA,
        rxcui=warfarin.rxcui,
        synthea_product=warfarin.display,
        states=[
            {"state": "home", "time_order": 10, "trigger": "outpatient warfarin", "evidence": ["hip-base"], "provenance": SYNTHEA},
            {"state": "held", "time_order": 40, "trigger": "fall, fracture, and need for surgery", "evidence": ["hip-present", "hip-treat"], "provenance": EPISODE},
        ],
        discharge_action=variant["restart"],
        evidence_ids=["hip-base", "hip-treat", "hip-response", "hip-ready"],
        resident_note=(
            "Still held. INR is 1.3 and the wound is dry."
            if variant["restart"] == "restart"
            else "Still held. A wound hematoma is present and not expanding, and hemoglobin is stable."
        ),
        rationale=(
            "Restart is supported by a persistent anticoagulation indication, an INR that has fallen, hemostasis, and completed fixation."
            if variant["restart"] == "restart"
            else "Continued hold is supported by the wound hematoma. The indication is still present, so the hold is temporary."
        ),
        monitoring="INR within 3 days if warfarin is resumed, and sooner for wound bleeding.",
        follow_up="Orthopedics and the clinician who manages anticoagulation within 7 days.",
        alternatives=[
            {
                "alternative_action": "hold" if variant["restart"] == "restart" else "restart",
                "conditions": "If the wound assessment is weighed differently at the moment of the order.",
                "rationale": "Hemostasis is recent. Either a restart now or a short further hold can be defended from the same wound and INR facts.",
            }
        ],
    )
    enox = regimen_by_id(ENOXAPARIN)
    chart.medication(
        drug=enox.query,
        dose=enox.dose,
        route=enox.route,
        frequency=enox.frequency,
        indication="postoperative venous-thromboembolism prophylaxis",
        regimen_id=ENOXAPARIN,
        identity_provenance=EPISODE,
        rxcui=None,
        synthea_product=None,
        states=[
            {"state": "hospital_only", "time_order": 72, "trigger": "postoperative prophylaxis while warfarin was held", "evidence": ["hip-treat"], "provenance": EPISODE},
            {"state": "discontinued", "time_order": 95, "trigger": "prophylaxis has no chronic indication once therapeutic anticoagulation is being decided", "evidence": ["hip-ready"], "provenance": EPISODE},
        ],
        discharge_action="stop",
        evidence_ids=["hip-treat", "hip-ready"],
        resident_note="Hospital prophylaxis only. Not a home medicine. Creatinine did not require a different prophylactic dose.",
        rationale="Stopping enoxaparin avoids stacking it onto a warfarin decision. It was never a chronic outpatient drug.",
        monitoring="Observe the wound.",
        follow_up="No enoxaparin follow-up.",
        hospital_only=True,
    )
    _continue_rest(chart, meds, {WARFARIN, ENOXAPARIN}, ["hip-base", "hip-ready"], "unchanged outpatient indication")
    chart.monitor("INR", "within 3 days", "therapeutic range for the pre-existing indication", "anticoagulation clinician")
    chart.follow("Orthopedics", "within 14 days", "orthopedics")
    chart.follow("Anticoagulation follow-up", "within 7 days", "anticoagulation clinician")
    _task(chart)
    return chart.to_episode()


def build_gi(
    patient: LongitudinalPatient,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    meds = mapped_medications(patient)
    warfarin = _find(meds, {WARFARIN})
    if warfarin is None:
        raise ValueError("gastrointestinal-bleed episode requires warfarin")
    rng = random.Random(_seed(meta, patient, "GI_BLEED_ANTICOAGULATION", variant["variant_id"]))
    _base_cr, _cr_src = _creatinine(patient, rng)
    adm_inr = 4.1 if "inr" in variant["variant_id"] else 2.7
    nadir = 7.4 if variant["transfused"] else 8.6
    discharge_hgb = 9.0 if variant["transfused"] else 8.8
    chart = Chart(
        patient=patient,
        scenario_code="GI_BLEED_ANTICOAGULATION",
        variant_id=variant["variant_id"],
        eligibility_tier="warfarin_with_indication",
        episode_seed=_seed(meta, patient, "GI_BLEED_ANTICOAGULATION", variant["variant_id"]),
        fingerprint={
            "scenario": "GI_BLEED_ANTICOAGULATION",
            "variant_id": variant["variant_id"],
            "precipitant": variant["precipitant"],
            "diagnostic_pathway": variant["pathway"],
            "renal_pattern": "creatinine_stable",
            "procedure": "endoscopy",
            "disposition": "home",
            "restart_decision": variant["restart"],
            "source": variant["source"],
        },
        physiology_expectations=["bleed_hemoglobin", "inr_down"],
        synthea_meta=meta,
        chief_complaint=variant["precipitant"].replace("_", " "),
        syndrome="gastrointestinal bleeding with warfarin held and the source established by endoscopy",
        symptom_duration="one day",
        symptom_course="bleeding stopped and the heart rate and hemoglobin stabilized",
        symptoms=[variant["precipitant"].replace("_", " ")],
        disposition="home",
        specialty="gastroenterology",
    )
    _history(chart, patient)
    chart.diagnosis(ICD10["K92.2"], "K92.2", "admission", EPISODE)
    chart.diagnosis(ICD10[variant["code"]], variant["code"], "hospital", EPISODE)
    chart.diagnosis(ICD10["D62"], "D62", "hospital", EPISODE)
    chart.fact(
        "gi-base",
        ["baseline"],
        (
            f"The longitudinal extract includes warfarin ({warfarin.display}) for a recorded indication. "
            f"Other products: {_products(meds)}. There was no chronic daily bleeding at baseline."
        ),
        SYNTHEA,
        10,
        "hpi",
    )
    chart.fact(
        "gi-acute",
        ["acute_change"],
        "Overt bleeding began within the day before arrival and was not the patient's usual pattern.",
        EPISODE,
        20,
        "hpi",
    )
    nsaid = _find(meds, {IBUPROFEN}) if variant["nsaid"] else None
    chart.fact(
        "gi-precip",
        ["precipitant"],
        (
            "Ibuprofen had been taken for pain during the prior week, on top of warfarin."
            if variant["nsaid"]
            else "No new nonsteroidal drug was identified. The bleeding itself was the acute event on chronic anticoagulation."
        ),
        EPISODE,
        30,
        "hpi",
    )
    chart.fact(
        "gi-present",
        ["presentation", "physiology"],
        f"Heart rate was 114 and blood pressure was 96/58. Hemoglobin was 9.2 g/dL. INR was {adm_inr:.1f}. Warfarin was held.",
        EPISODE,
        40,
        "hpi",
    )
    study = "Esophagogastroduodenoscopy" if variant["upper"] else "Colonoscopy"
    chart.fact(
        "gi-work",
        ["workup"],
        f"{study} was performed after resuscitation and showed {variant['source']}. Hemostasis was achieved or the lesion was already flat.",
        EPISODE,
        50,
        "course",
    )
    chart.fact(
        "gi-dx",
        ["diagnosis"],
        "The source above was assigned only after endoscopy. The admitting problem was bleeding, not that finished source.",
        EPISODE,
        60,
        "course",
    )
    transfusion = " One unit of red cells was given. " if variant["transfused"] else " No transfusion was required. "
    chart.fact(
        "gi-treat",
        ["treatment", "medication_decision"],
        "Warfarin remained held." + transfusion + (
            "Pantoprazole was started for the upper source. " if variant["upper"] else "Acid suppression was not started for a colonic source. "
        ),
        EPISODE,
        70,
        "course",
    )
    chart.fact(
        "gi-response",
        ["response", "physiology"],
        (
            f"Hemoglobin nadir was {nadir:.1f} g/dL and the pre-discharge value was {discharge_hgb:.1f} g/dL. "
            f"Heart rate fell to 78 and blood pressure was 122/70. INR fell to 1.6. No further melena or hematochezia occurred."
        ),
        EPISODE,
        80,
        "course",
    )
    chart.fact(
        "gi-ready",
        ["discharge_readiness"],
        "The patient was eating and hemodynamically stable. The anticoagulation restart decision was still unsigned.",
        EPISODE,
        90,
        "course",
    )
    chart.fact("gi-follow", ["followup"], "Gastroenterology and anticoagulation follow-up were arranged, with a hemoglobin check.", EPISODE, 95, "course")
    _events(
        chart,
        [
            ("baseline", 10, "Warfarin indication"),
            ("acute_change", 20, "Overt bleeding"),
            ("precipitant", 30, variant["precipitant"]),
            ("presentation", 40, "Tachycardia and anemia"),
            ("workup", 50, study),
            ("diagnosis", 60, variant["source"]),
            ("treatment", 70, "Hold, endoscopy, and supportive care"),
            ("response", 80, "Hemoglobin and vital signs stabilized"),
            ("discharge", 100, "Stable, restart unsigned"),
        ],
    )
    chart.lab("718-7", [("baseline", 13.1), ("admission", 9.2), ("nadir", nadir), ("discharge", discharge_hgb)], EPISODE)
    chart.lab("6301-6", [("admission", adm_inr), ("discharge", 1.6)], EPISODE)
    chart.vital("admission", temp_c=36.8, bp_systolic=96, bp_diastolic=58, heart_rate=114, resp_rate=18, spo2_percent=98, provenance=EPISODE)
    chart.vital("discharge", temp_c=36.7, bp_systolic=122, bp_diastolic=70, heart_rate=78, resp_rate=16, spo2_percent=98, provenance=EPISODE)
    chart.procedure(study, "after resuscitation", variant["source"], EPISODE)
    war = regimen_by_id(WARFARIN)
    chart.medication(
        drug=war.query,
        dose=war.dose,
        route=war.route,
        frequency=war.frequency,
        indication="longitudinal anticoagulation indication",
        regimen_id=WARFARIN,
        identity_provenance=SYNTHEA,
        rxcui=warfarin.rxcui,
        synthea_product=warfarin.display,
        states=[
            {"state": "home", "time_order": 10, "trigger": "outpatient warfarin", "evidence": ["gi-base"], "provenance": SYNTHEA},
            {"state": "held", "time_order": 40, "trigger": "overt bleeding", "evidence": ["gi-present"], "provenance": EPISODE},
        ],
        discharge_action=variant["restart"],
        evidence_ids=["gi-base", "gi-work", "gi-response", "gi-ready"],
        resident_note=(
            "Still held after hemostasis, a stable hemoglobin, and an INR of 1.6."
            if variant["restart"] == "restart"
            else "Still held. Hemostasis is recent and the source was diverticular, so restart timing is explicitly unresolved."
        ),
        rationale=(
            "Restart is supported by a persistent indication, endoscopic hemostasis or a flat lesion, stable hemoglobin, and a fallen INR."
            if variant["restart"] == "restart"
            else "A further hold is supported because diverticular hemostasis is recent. The indication remains, so this is not a permanent stop."
        ),
        monitoring="Hemoglobin within 48 hours and INR if warfarin resumes.",
        follow_up="Gastroenterology and anticoagulation follow-up within 7 days.",
        alternatives=[
            {
                "alternative_action": "hold" if variant["restart"] == "restart" else "restart",
                "conditions": "If the clinician weighs rebleeding risk more heavily, or less heavily, than the thrombotic indication.",
                "rationale": "Both a restart now and a short additional hold are defensible once bleeding has stopped and follow-up exists.",
            }
        ],
    )
    if variant["upper"]:
        ppi = regimen_by_id(PANTOPRAZOLE)
        chart.medication(
            drug=ppi.query,
            dose=ppi.dose,
            route=ppi.route,
            frequency=ppi.frequency,
            indication=variant["source"],
            regimen_id=PANTOPRAZOLE,
            identity_provenance=EPISODE,
            rxcui=None,
            synthea_product=None,
            states=[
                {"state": "new_inpatient", "time_order": 70, "trigger": "upper endoscopic source", "evidence": ["gi-work"], "provenance": EPISODE},
            ],
            discharge_action="new_start",
            evidence_ids=["gi-work", "gi-response"],
            resident_note="Started for the upper source. A duration order is not signed.",
            rationale="Acid suppression is supported by the upper endoscopic source and should continue at least through mucosal healing.",
            monitoring="No specific laboratory monitoring for this dose.",
            follow_up="Gastroenterology to review the duration.",
        )
    if variant["nsaid"]:
        regimen = regimen_by_id(IBUPROFEN)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="pain, implicated in the bleed",
            regimen_id=IBUPROFEN,
            identity_provenance=SYNTHEA if nsaid else EPISODE,
            rxcui=nsaid.rxcui if nsaid else None,
            synthea_product=nsaid.display if nsaid else None,
            states=[
                {"state": "home", "time_order": 10, "trigger": "used for pain before melena", "evidence": ["gi-precip"], "provenance": SYNTHEA if nsaid else EPISODE},
                {"state": "discontinued", "time_order": 40, "trigger": "bleeding", "evidence": ["gi-present", "gi-work"], "provenance": EPISODE},
            ],
            discharge_action="stop",
            evidence_ids=["gi-precip", "gi-work"],
            resident_note="Stopped because of bleeding. Not an unknown medicine.",
            rationale="The anti-inflammatory drug contributed to an ulcer while the patient was anticoagulated, so it stays stopped.",
            monitoring="None specific.",
            follow_up="Use a non-anti-inflammatory analgesic if pain returns.",
        )
    _continue_rest(chart, meds, {item["regimen_id"] for item in chart.medications}, ["gi-base", "gi-ready"], "unchanged outpatient indication")
    chart.monitor("hemoglobin", "within 48 hours", "no further drop", "primary care")
    chart.follow("Gastroenterology", "within 7 days", "gastroenterology")
    chart.follow("Anticoagulation follow-up", "within 7 days", "anticoagulation clinician")
    _task(chart)
    return chart.to_episode()
