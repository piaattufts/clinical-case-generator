"""Remaining Generation 2 families. Heart failure lives in g2_episodes.py."""

from __future__ import annotations

import random
from typing import Any

from app.services.g2_chart import EPISODE, SYNTHEA, Chart
from app.services.g2_episodes import (
    AZITHROMYCIN,
    CEFTRIAXONE,
    CEPHALEXIN,
    HCTZ,
    IBUPROFEN,
    TACROLIMUS,
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
from app.services.synthea_eligibility import RAAS_IDS, MappedMedication, mapped_medications
from app.sources.synthea import LongitudinalPatient


def _cognition(patient: LongitudinalPatient) -> str:
    blob = patient.condition_blob()
    if "dementia" in blob or "alzheimer" in blob:
        return (
            "The longitudinal record includes a dementia diagnosis. The caregiver's account of "
            "baseline was recognition of family and the ability to hold a conversation."
        )
    return (
        "The longitudinal record does not list dementia. Before this illness the patient handled "
        "daily activities and recognized family."
    )


def _stop_nsaid_or_ace(
    meds: list[MappedMedication], patient: LongitudinalPatient
) -> tuple[MappedMedication | None, str]:
    nsaid = _find(meds, {IBUPROFEN})
    if nsaid is not None:
        return nsaid, "dyspepsia"
    from app.services.synthea_eligibility import has_known_heart_failure

    raas = _find(meds, RAAS_IDS)
    if raas is not None and not has_known_heart_failure(patient):
        return raas, "cough"
    return None, ""


def supports_family(patient: LongitudinalPatient, scenario: str, variant: dict[str, Any]) -> bool:
    meds = mapped_medications(patient)
    code = variant["variant_id"]
    if scenario == "MED_HISTORY_UNCERTAINTY":
        if len(meds) < 4:
            return False
        if code in {"hyponatremia_hctz", "orthostasis_hctz"}:
            return _find(meds, {HCTZ}) is not None
        if code == "lisinopril_hold_aki":
            return _find(meds, RAAS_IDS) is not None
        if code == "nsaid_dyspepsia":
            return _find(meds, {IBUPROFEN}) is not None
        if code == "pharmacy_confirmation":
            return _stop_nsaid_or_ace(meds, patient)[0] is not None
        if code == "delirium_dehydration":
            return _choose_stop(code, meds, patient)[0] is not None
        return True
    if scenario in {"GI_BLEED_ANTICOAGULATION", "HIP_FRACTURE_ANTICOAGULATION"}:
        if _find(meds, {WARFARIN}) is None:
            return False
        if code == "mechanical_valve_context":
            blob = patient.condition_blob()
            return "valve" in blob or "prosthetic" in blob
        return True
    if scenario == "TRANSPLANT_CMV":
        return _find(meds, {TACROLIMUS}) is not None
    return True


def build_medication_history(
    patient: LongitudinalPatient,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    meds = mapped_medications(patient)
    rng = random.Random(_seed(meta, patient, "MED_HISTORY_UNCERTAINTY", variant["variant_id"]))
    base_cr, cr_src = _creatinine(patient, rng)
    code = variant["variant_id"]
    aki = code in {"delirium_dehydration", "delirium_uti", "lisinopril_hold_aki"}
    adm_cr = _one(min(base_cr + 0.6, 2.2)) if aki else _one(base_cr + 0.1)
    dis_cr = _one(base_cr + 0.1) if aki else base_cr
    chart = Chart(
        patient=patient,
        scenario_code="MED_HISTORY_UNCERTAINTY",
        variant_id=code,
        eligibility_tier="medication_complexity",
        episode_seed=_seed(meta, patient, "MED_HISTORY_UNCERTAINTY", code),
        fingerprint={
            "scenario": "MED_HISTORY_UNCERTAINTY",
            "variant_id": code,
            "precipitant": variant["precipitant"],
            "diagnostic_pathway": variant["pathway"],
            "renal_pattern": "aki_recovered" if aki else "creatinine_stable",
            "procedure": variant["procedure"],
            "disposition": "home",
            "history_resolution": "collateral_confirmed",
        },
        physiology_expectations=["aki_recovered"] if aki else [],
        synthea_meta=meta,
        chief_complaint=variant["chief"],
        syndrome=variant["syndrome"],
        symptom_duration=variant["duration"],
        symptom_course="the acute change reversed after the precipitant was treated",
        symptoms=variant["symptoms"],
        disposition="home",
        specialty="internal medicine",
    )
    _history(chart, patient)
    if code.startswith("delirium"):
        chart.diagnosis(ICD10["F05"], "F05", "hospital", EPISODE)
    if code == "hyponatremia_hctz":
        chart.diagnosis(ICD10["E87.1"], "E87.1", "hospital", EPISODE)
    if code == "delirium_dehydration":
        chart.diagnosis(ICD10["E86.0"], "E86.0", "hospital", EPISODE)
    if code == "delirium_uti":
        chart.diagnosis(ICD10["N39.0"], "N39.0", "hospital", EPISODE)
    if code == "delirium_pneumonia":
        chart.diagnosis(ICD10["J18.9"], "J18.9", "hospital", EPISODE)
    if aki:
        chart.diagnosis(ICD10["N17.9"], "N17.9", "hospital", EPISODE)
    chart.fact(
        "mh-cognition",
        ["baseline"],
        _cognition(patient),
        EPISODE,
        10,
        "hpi",
    )
    chart.fact(
        "mh-base",
        ["baseline"],
        f"Outpatient products in the longitudinal extract: {_products(meds)}.",
        SYNTHEA,
        12,
        "hpi",
    )
    chart.fact("mh-acute", ["acute_change"], variant["acute_text"], EPISODE, 20, "hpi")
    chart.fact("mh-precip", ["precipitant"], variant["precipitant_text"], EPISODE, 30, "hpi")
    chart.fact("mh-present", ["presentation"], variant["present_text"], EPISODE, 40, "hpi")
    chart.fact("mh-work", ["workup"], variant["workup_text"], EPISODE, 50, "course")
    chart.fact("mh-dx", ["diagnosis"], variant["diagnosis_text"], EPISODE, 60, "course")
    chart.fact("mh-treat", ["treatment"], variant["treatment_text"], EPISODE, 70, "course")
    chart.fact(
        "mh-response",
        ["response", "physiology"],
        variant["response_text"].format(base=base_cr, adm=adm_cr, dis=dis_cr),
        EPISODE,
        80,
        "course",
    )
    chart.fact(
        "mh-meds",
        ["medication_decision"],
        variant["med_text"],
        EPISODE,
        85,
        "course",
    )
    chart.fact(
        "mh-ready",
        ["discharge_readiness"],
        (
            "Attention and intake had returned to the caregiver's account of baseline, and the "
            "outpatient medication history was no longer incomplete. The discharge medication list "
            "itself was still unsigned."
        ),
        EPISODE,
        90,
        "course",
    )
    chart.fact(
        "mh-follow",
        ["followup"],
        "Primary care follow-up and a chemistry panel were arranged.",
        EPISODE,
        95,
        "course",
    )
    _events(
        chart,
        [
            ("baseline", 10, "Baseline cognition and outpatient medicines"),
            ("acute_change", 20, "Acute change from baseline"),
            ("precipitant", 30, variant["precipitant"]),
            ("presentation", 40, "Presentation"),
            ("workup", 50, "Work-up"),
            ("diagnosis", 60, "Diagnosis after the work-up"),
            ("treatment", 70, "Treatment of the precipitant"),
            ("response", 80, "Return toward baseline"),
            ("discharge", 100, "History resolved and discharge planning open"),
        ],
    )
    chart.lab(
        "2160-0",
        [("baseline", base_cr), ("admission", adm_cr), ("peak", adm_cr), ("discharge", dis_cr)],
        EPISODE,
    )
    if cr_src == SYNTHEA:
        for row in chart.labs:
            if row["loinc_code"] == "2160-0" and row["timepoint"] == "baseline":
                row["provenance"] = SYNTHEA
    chart.lab("2823-3", [("admission", 4.2), ("discharge", 4.1)], EPISODE)
    if code == "hyponatremia_hctz":
        chart.lab("2951-2", [("baseline", 136), ("admission", 128), ("discharge", 134)], EPISODE)
    else:
        chart.lab("2951-2", [("admission", 141), ("discharge", 139)], EPISODE)
    if code in {"delirium_uti", "delirium_pneumonia"}:
        chart.lab("6690-2", [("admission", 13.4), ("discharge", 8.1)], EPISODE)
    chart.vital(
        "admission",
        temp_c=37.8 if code == "delirium_uti" else 36.9,
        bp_systolic=148 if code == "orthostasis_hctz" else 138,
        bp_diastolic=82 if code == "orthostasis_hctz" else 78,
        heart_rate=108 if code == "delirium_dehydration" else 88,
        resp_rate=18,
        spo2_percent=96,
        provenance=EPISODE,
    )
    chart.vital(
        "discharge",
        temp_c=36.7,
        bp_systolic=128,
        bp_diastolic=74,
        heart_rate=76,
        resp_rate=16,
        spo2_percent=97,
        provenance=EPISODE,
    )
    stopped, stop_reason = _choose_stop(code, meds, patient)
    reserved = {stopped.regimen_id} if stopped is not None else set()
    if code == "lisinopril_hold_aki":
        raas_for_hold = _find(meds, RAAS_IDS)
        if raas_for_hold is not None:
            reserved.add(raas_for_hold.regimen_id)
    confirmed = next(item for item in meds if item.regimen_id not in reserved)
    chart.medrec_row(
        confirmed.display,
        "pharmacy",
        "confirmed_after_initial_uncertainty",
        "Not recalled on arrival. The pharmacy dispense record confirmed ongoing fills.",
    )
    if stopped is not None:
        chart.medrec_row(
            stopped.display,
            "patient_and_collateral",
            "intentionally_stopped",
            f"Stopped on purpose because of {stop_reason}. This was not an unknown medicine.",
        )
        regimen = regimen_by_id(stopped.regimen_id)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication=stop_reason,
            regimen_id=regimen.id,
            identity_provenance=SYNTHEA,
            rxcui=stopped.rxcui,
            synthea_product=stopped.display,
            states=[
                {
                    "state": "home",
                    "time_order": 10,
                    "trigger": "previously filled outpatient product",
                    "evidence": ["mh-base"],
                    "provenance": SYNTHEA,
                },
                {
                    "state": "discontinued",
                    "time_order": 70,
                    "trigger": stop_reason,
                    "evidence": ["mh-meds", "mh-response"],
                    "provenance": EPISODE,
                },
            ],
            discharge_action="stop",
            evidence_ids=["mh-meds", "mh-response"],
            resident_note=f"Intentionally stopped for {stop_reason}. Distinguished from medicines that were only unknown at arrival.",
            rationale=f"Stopping remains supported by {stop_reason} and by the response after it was held.",
            monitoring="No further monitoring of the stopped medicine.",
            follow_up="Do not resume it unless the original reason has been reconsidered.",
        )
    if code == "lisinopril_hold_aki":
        raas = _find(meds, RAAS_IDS)
        assert raas is not None
        regimen = regimen_by_id(raas.regimen_id)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="outpatient cardiovascular therapy",
            regimen_id=raas.regimen_id,
            identity_provenance=SYNTHEA,
            rxcui=raas.rxcui,
            synthea_product=raas.display,
            states=[
                {
                    "state": "home",
                    "time_order": 10,
                    "trigger": "outpatient product in the longitudinal record",
                    "evidence": ["mh-base"],
                    "provenance": SYNTHEA,
                },
                {
                    "state": "held",
                    "time_order": 40,
                    "trigger": "creatinine rise during poor intake",
                    "evidence": ["mh-treat"],
                    "provenance": EPISODE,
                },
            ],
            discharge_action="restart",
            evidence_ids=["mh-base", "mh-response", "mh-meds"],
            resident_note=(
                "Held for the creatinine rise. At discharge planning creatinine is back toward "
                "the prior value, potassium is 4.1 mmol/L, and blood pressure is 128/74. "
                "A restart order has not been signed."
            ),
            rationale=(
                "Restart is supported by the home indication, creatinine recovery, acceptable "
                "potassium, and stable blood pressure. The order is unsigned."
            ),
            monitoring="Chemistry panel within 7 days.",
            follow_up="Primary care within 7 days.",
            alternatives=[
                {
                    "alternative_action": "hold",
                    "conditions": "If the clinician wants one more chemistry result before the first dose.",
                    "rationale": "A short further hold is defensible because the medicine is currently held and follow-up exists.",
                }
            ],
        )
    if code == "delirium_uti":
        _hospital_antibiotic(chart, CEPHALEXIN, "cystitis after the urine culture grew Escherichia coli")
    if code == "delirium_pneumonia":
        _hospital_antibiotic(chart, AZITHROMYCIN, "a lobar infiltrate with cough")
    _continue_rest(
        chart,
        meds,
        {item["regimen_id"] for item in chart.medications},
        ["mh-base", "mh-meds"],
        "confirmed outpatient indication",
    )
    chart.monitor("chemistry panel", "within 7 days", "creatinine and electrolytes", "primary care")
    chart.follow("Primary care", "within 7 days", "primary care")
    _task(chart)
    return chart.to_episode()


def _choose_stop(
    code: str, meds: list[MappedMedication], patient: LongitudinalPatient
) -> tuple[MappedMedication | None, str]:
    if code in {"hyponatremia_hctz", "orthostasis_hctz"}:
        med = _find(meds, {HCTZ})
        reason = "hyponatremia" if code == "hyponatremia_hctz" else "orthostatic lightheadedness and a fall"
        return med, reason
    if code == "nsaid_dyspepsia":
        return _find(meds, {IBUPROFEN}), "epigastric pain and a rise in creatinine"
    if code == "delirium_dehydration":
        raas = _find(meds, RAAS_IDS)
        if raas is not None:
            return raas, "a rise in creatinine during dehydration"
        return _find(meds, {HCTZ}), "a rise in creatinine during dehydration"
    if code == "pharmacy_confirmation":
        med, reason = _stop_nsaid_or_ace(meds, patient)
        if reason == "cough":
            return med, "a dry cough that began after the medicine was started and resolved when it was stopped"
        if reason == "dyspepsia":
            return med, "epigastric burning that the patient linked to the anti-inflammatory drug"
        return med, reason
    return None, ""


def _hospital_antibiotic(chart: Chart, regimen_id: str, reason: str) -> None:
    regimen = regimen_by_id(regimen_id)
    chart.medication(
        drug=regimen.query,
        dose=regimen.dose,
        route=regimen.route,
        frequency=regimen.frequency,
        indication=reason,
        regimen_id=regimen_id,
        identity_provenance=EPISODE,
        rxcui=None,
        synthea_product=None,
        states=[
            {
                "state": "hospital_only",
                "time_order": 70,
                "trigger": reason,
                "evidence": ["mh-treat"],
                "provenance": EPISODE,
            },
            {
                "state": "discontinued",
                "time_order": 90,
                "trigger": "the finite course was completed before discharge planning",
                "evidence": ["mh-response"],
                "provenance": EPISODE,
            },
        ],
        discharge_action="stop",
        evidence_ids=["mh-treat", "mh-response"],
        resident_note="The finite course was completed. It is not an outpatient maintenance medicine.",
        rationale="The course is complete and the precipitant has responded, so the antibiotic stops.",
        monitoring="No extended antibiotic monitoring.",
        follow_up="Return for recurrent fever or urinary symptoms.",
        hospital_only=True,
    )


def build_endocarditis(
    patient: LongitudinalPatient,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    meds = mapped_medications(patient)
    rng = random.Random(_seed(meta, patient, "ENDOCARDITIS_OPAT", variant["variant_id"]))
    base_cr, cr_src = _creatinine(patient, rng)
    chart = Chart(
        patient=patient,
        scenario_code="ENDOCARDITIS_OPAT",
        variant_id=variant["variant_id"],
        eligibility_tier="baseline_context_only",
        episode_seed=_seed(meta, patient, "ENDOCARDITIS_OPAT", variant["variant_id"]),
        fingerprint={
            "scenario": "ENDOCARDITIS_OPAT",
            "variant_id": variant["variant_id"],
            "precipitant": variant["precipitant"],
            "diagnostic_pathway": variant["pathway"],
            "renal_pattern": "creatinine_stable",
            "procedure": "echocardiogram",
            "disposition": variant["disposition"],
            "organism": variant["organism"],
        },
        physiology_expectations=[],
        synthea_meta=meta,
        chief_complaint="Fever, fatigue, and a new murmur",
        syndrome="fever with endocarditis established only after cultures and echocardiography",
        symptom_duration="ten days",
        symptom_course="fever resolved after antibiotics and clearance cultures were negative",
        symptoms=["fever", "fatigue", "night sweats"],
        disposition=variant["disposition"],
        specialty="infectious disease",
    )
    _history(chart, patient)
    chart.diagnosis("Fever and a new murmur", None, "admission", EPISODE)
    chart.diagnosis(ICD10["I33.0"], "I33.0", "hospital", EPISODE)
    chart.fact(
        "en-base",
        ["baseline"],
        (
            "The longitudinal extract does not list endocarditis. "
            f"Outpatient products in the extract: {_products(meds)}. "
            f"Pre-admission creatinine was {base_cr:.1f} mg/dL."
            if cr_src == SYNTHEA
            else (
                "The longitudinal extract does not list endocarditis. "
                f"Outpatient products in the extract: {_products(meds)}. "
                f"No pre-admission creatinine was present; the first value was {base_cr:.1f} mg/dL."
            )
        ),
        SYNTHEA if cr_src == SYNTHEA else EPISODE,
        10,
        "hpi",
    )
    chart.fact(
        "en-acute",
        ["acute_change"],
        "For ten days the patient had fever, sweats, and fatigue that were new. There was no chronic febrile illness in the history obtained on arrival.",
        EPISODE,
        20,
        "hpi",
    )
    chart.fact("en-precip", ["precipitant"], variant["source_text"], EPISODE, 30, "hpi")
    chart.fact(
        "en-present",
        ["presentation"],
        (
            "Arrival temperature was 38.4 degrees Celsius. A murmur that the patient did not recognize "
            "was present. The working concern was bloodstream infection, not a finished diagnosis of endocarditis."
        ),
        EPISODE,
        40,
        "hpi",
    )
    chart.fact(
        "en-work",
        ["workup"],
        (
            f"Two sets of blood cultures were drawn before any antibiotic. They grew {variant['organism']}. "
            f"A transthoracic echocardiogram then showed {variant['echo']}. Dental and skin examinations "
            "were recorded as part of the source evaluation."
        ),
        EPISODE,
        50,
        "course",
    )
    chart.fact(
        "en-dx",
        ["diagnosis"],
        (
            "Endocarditis was diagnosed only after the organism and the echocardiogram were both available. "
            "The patient did not present with that label already assigned."
        ),
        EPISODE,
        60,
        "course",
    )
    chart.fact(
        "en-treat",
        ["treatment", "medication_decision"],
        (
            "Ceftriaxone 2 g intravenously once daily was started after the cultures were drawn and was "
            "continued once the organism was known to be treated by that regimen. Cardiac surgery saw the "
            "patient: there was no abscess, no severe valve failure, and no indication for urgent surgery. "
            f"Creatinine stayed {base_cr:.1f} mg/dL, which is the range in which the curated 2 g dose is used."
        ),
        EPISODE,
        70,
        "course",
    )
    chart.fact(
        "en-response",
        ["response", "physiology"],
        (
            "Fever resolved by hospital day 3. A repeat blood culture showed no growth. Appetite and "
            "walking had returned. This was day 6 of intravenous ceftriaxone."
        ),
        EPISODE,
        80,
        "course",
    )
    chart.fact(
        "en-ready",
        ["discharge_readiness"],
        (
            f"Outpatient parenteral therapy is logistically feasible at {variant['disposition']}. "
            "The remaining duration has not been signed. Weekly laboratory monitoring and infectious-diseases "
            "follow-up are arranged."
        ),
        EPISODE,
        90,
        "course",
    )
    chart.fact(
        "en-follow",
        ["followup"],
        "Infectious diseases follow-up within one week and a weekly chemistry panel were specified.",
        EPISODE,
        95,
        "course",
    )
    _events(
        chart,
        [
            ("baseline", 10, "No prior endocarditis"),
            ("acute_change", 20, "New fever"),
            ("precipitant", 30, variant["precipitant"]),
            ("presentation", 40, "Fever and murmur"),
            ("workup", 48, "Cultures drawn before antibiotics"),
            ("treatment", 55, "Empiric ceftriaxone after cultures"),
            ("diagnosis", 60, "Organism and echocardiogram establish endocarditis"),
            ("treatment", 70, "Targeted ceftriaxone confirmed"),
            ("response", 80, "Defervescence and culture clearance"),
            ("discharge", 100, "OPAT feasible, order unsigned"),
        ],
        empiric_at=55,
    )
    chart.lab("2160-0", [("baseline", base_cr), ("admission", base_cr), ("discharge", base_cr)], EPISODE)
    if cr_src == SYNTHEA:
        for row in chart.labs:
            if row["timepoint"] == "baseline":
                row["provenance"] = SYNTHEA
    chart.lab("600-7", [("admission", variant["organism"]), ("pre_discharge", "no growth")], EPISODE)
    chart.vital("admission", temp_c=38.4, bp_systolic=118, bp_diastolic=68, heart_rate=104, resp_rate=18, spo2_percent=97, provenance=EPISODE)
    chart.vital("discharge", temp_c=36.7, bp_systolic=122, bp_diastolic=70, heart_rate=76, resp_rate=16, spo2_percent=98, provenance=EPISODE)
    chart.microbiology(
        "admission",
        "blood",
        "Blood culture",
        "growth",
        EPISODE,
        organism=variant["organism"],
        notes="Drawn before the first antibiotic dose.",
    )
    chart.microbiology(
        "pre_discharge",
        "blood",
        "Blood culture",
        "no growth",
        EPISODE,
        notes="Clearance culture after treatment had begun.",
    )
    chart.image("hospital_day_1", "Transthoracic echocardiogram", variant["echo"], EPISODE)
    chart.consult(
        "cardiac surgery",
        "inpatient",
        variant["echo"] + " No abscess and no refractory heart failure.",
        "Urgent surgery is not indicated. Reassess if heart failure or persistent bacteremia develops.",
    )
    chart.consult(
        "infectious diseases",
        "inpatient",
        f"{variant['organism']} endocarditis on the echocardiogram described above.",
        "Ceftriaxone 2 g intravenously once daily is the inpatient regimen. The unsigned question is completing it after discharge.",
    )
    regimen = regimen_by_id(CEFTRIAXONE)
    chart.medication(
        drug=regimen.query,
        dose=regimen.dose,
        route=regimen.route,
        frequency=regimen.frequency,
        indication="streptococcal endocarditis after cultures and echocardiography",
        regimen_id=CEFTRIAXONE,
        identity_provenance=EPISODE,
        rxcui=None,
        synthea_product=None,
        states=[
            {
                "state": "new_inpatient",
                "time_order": 55,
                "trigger": "blood cultures drawn, then empiric intravenous therapy",
                "evidence": ["en-treat"],
                "provenance": EPISODE,
            },
            {
                "state": "continued_inpatient",
                "time_order": 70,
                "trigger": "organism is treated with this curated regimen",
                "evidence": ["en-work", "en-dx"],
                "provenance": EPISODE,
            },
        ],
        discharge_action="continue",
        evidence_ids=["en-work", "en-treat", "en-response", "en-ready"],
        resident_note=(
            "Active inpatient therapy on day 6. Clearance cultures show no growth. "
            "A discharge duration order has not been signed."
        ),
        rationale=(
            "Continuing ceftriaxone 2 g once daily to finish a four-week course is supported by the "
            "organism, the echocardiogram, preserved creatinine, clearance of bacteremia, and feasible "
            "outpatient parenteral therapy."
        ),
        monitoring="Weekly chemistry panel and complete blood count.",
        follow_up="Infectious diseases within 7 days.",
        alternatives=[
            {
                "alternative_action": "continue",
                "conditions": f"If {variant['disposition']} infusion is declined, give the same regimen in the other supervised setting.",
                "rationale": "The drug and dose do not change when only the infusion site changes.",
            }
        ],
    )
    _continue_rest(chart, meds, {CEFTRIAXONE}, ["en-base", "en-ready"], "unchanged outpatient indication")
    chart.monitor("chemistry panel and blood count", "weekly", "while intravenous therapy continues", "infectious diseases")
    chart.follow("Infectious diseases", "within 7 days", "infectious diseases")
    chart.follow("Primary care", "within 14 days", "primary care")
    _task(chart)
    return chart.to_episode()
