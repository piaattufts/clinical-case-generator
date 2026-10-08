"""Causal inpatient episodes for the six Generation 2 scenario families.

Numbers are deterministic functions of the episode seed and the patient's own
baseline when Synthea recorded one. Doses come from curated regimens.
"""

from __future__ import annotations

import random
from typing import Any

from app.services.g2_chart import EPISODE, SYNTHEA, Chart, net_from_weight
from app.services.g2_terminology import ICD10, regimen_by_id
from app.services.synthea_eligibility import (
    RAAS_IDS,
    MappedMedication,
    has_known_heart_failure,
    mapped_medications,
)
from app.sources.synthea import LongitudinalPatient

HCTZ = "HCTZ_25_DAILY"
METFORMIN = "METFORMIN_500_BID"
IBUPROFEN = "IBUPROFEN_400_PRN"
WARFARIN = "WARFARIN_INR_INDIVIDUALIZED"
TACROLIMUS = "TACROLIMUS_ER_1MG_DAILY"
FUROSEMIDE = "FUROSEMIDE_40_DAILY"
CEFTRIAXONE = "CEFTRIAXONE_ENDOCARDITIS_OPAT"
AZITHROMYCIN = "AZITHROMYCIN_CAP_CONTINUATION"
CEPHALEXIN = "CEPHALEXIN_UTI_500_BID"
PANTOPRAZOLE = "PANTOPRAZOLE_40_DAILY"
ENOXAPARIN = "ENOXAPARIN_HOSPITAL_PROPHYLAXIS"
VALGAN_TREAT = "VALGANCICLOVIR_CMV_TREATMENT"
VALGAN_PROPH = "VALGANCICLOVIR_CMV_PROPHYLAXIS"


def _one(value: float) -> float:
    return float(f"{value:.1f}")


def _seed(meta: dict[str, str], patient: LongitudinalPatient, scenario: str, variant: str) -> str:
    return f"{meta['population_seed']}:{patient.synthea_patient_id}:{scenario}:{variant}"


def _creatinine(patient: LongitudinalPatient, rng: random.Random) -> tuple[float, str]:
    observed = patient.latest_lab("2160-0", unit="mg/dL")
    if observed is not None and 0.6 <= observed.value <= 1.5:
        return _one(observed.value), SYNTHEA
    return _one(0.8 + rng.randrange(0, 5) / 10), EPISODE


def _weight(patient: LongitudinalPatient, rng: random.Random) -> tuple[float, str]:
    if patient.weight_kg is not None and 50 <= patient.weight_kg <= 140:
        return _one(patient.weight_kg), SYNTHEA
    return _one(70 + rng.randrange(0, 25)), EPISODE


def _find(meds: list[MappedMedication], regimen_ids: set[str] | frozenset[str]) -> MappedMedication | None:
    for med in meds:
        if med.regimen_id in regimen_ids:
            return med
    return None


def _history(chart: Chart, patient: LongitudinalPatient, limit: int = 4) -> None:
    added = 0
    for condition in patient.conditions:
        if condition.status != "active" or not condition.text:
            continue
        chart.diagnosis(
            condition.text,
            None,
            "past_history",
            SYNTHEA,
            snomed_code=condition.snomed_code,
            context="history",
        )
        added += 1
        if added >= limit:
            break


def _products(meds: list[MappedMedication]) -> str:
    if not meds:
        return "no curated single-ingredient outpatient regimen"
    return "; ".join(item.display for item in meds[:6])


def _continue_rest(
    chart: Chart,
    meds: list[MappedMedication],
    skip: set[str],
    evidence: list[str],
    indication: str,
) -> None:
    for med in meds:
        if med.regimen_id in skip:
            continue
        if any(item["regimen_id"] == med.regimen_id for item in chart.medications):
            continue
        chart.continue_mapped(
            med,
            indication,
            evidence,
            (
                f"{med.display} remains indicated. The hospitalization did not create a "
                "contraindication, so the curated regimen that matches the recorded product continues."
            ),
            "Given through the hospitalization from the verified outpatient list.",
        )


def _task(chart: Chart) -> None:
    chart.instruction(
        "discharge medication task",
        "Determine the discharge medication plan from this hospitalization. "
        "A completed discharge medication list is not provided.",
    )


def _events(chart: Chart, rows: list[tuple[str, int, str]], *, empiric_at: int | None = None) -> None:
    for event_type, order, summary in rows:
        chart.event(
            f"ev-{event_type}-{order}",
            event_type,
            order,
            EPISODE,
            summary,
            [],
            empiric=empiric_at == order,
        )


def _cr_series(base: float, aki: bool) -> tuple[float, float, float]:
    if aki:
        admission = _one(min(base + 0.7, 2.4))
        peak = _one(min(admission + 0.2, 2.8))
        discharge = _one(min(base + 0.1, peak))
        return admission, peak, discharge
    admission = _one(base + 0.1)
    return admission, admission, base


def build_heart_failure(
    patient: LongitudinalPatient,
    variant: dict[str, Any],
    meta: dict[str, str],
) -> dict[str, Any]:
    meds = mapped_medications(patient)
    variant = dict(variant)
    if variant["variant_id"] == "new_atrial_fibrillation" and "atrial fibrillation" in patient.condition_blob():
        variant["precipitant_text"] = (
            "The longitudinal record already lists atrial fibrillation. On arrival the ventricular "
            "rate was 138, which was an acute acceleration rather than a new disease label."
        )
    rng = random.Random(_seed(meta, patient, "HF_DECOMPENSATION", variant["variant_id"]))
    known = has_known_heart_failure(patient)
    base_cr, cr_src = _creatinine(patient, rng)
    base_wt, wt_src = _weight(patient, rng)
    aki = bool(variant["aki"])
    adm_cr, peak_cr, dis_cr = _cr_series(base_cr, aki)
    adm_wt = _one(base_wt + 5.5)
    dis_wt = _one(base_wt + 0.8)
    raas = _find(meds, RAAS_IDS)
    loop = _find(meds, {FUROSEMIDE})
    beta = _find(
        meds,
        {
            "METOPROLOL_SUCCINATE_DAILY",
            "METOPROLOL_SUCCINATE_100_DAILY",
            "METOPROLOL_TARTRATE_BID",
            "CARVEDILOL_HF_BID",
        },
    )
    chart = Chart(
        patient=patient,
        scenario_code="HF_DECOMPENSATION",
        variant_id=variant["variant_id"],
        eligibility_tier="known_heart_failure" if known else "compatible_cardiovascular_history",
        episode_seed=_seed(meta, patient, "HF_DECOMPENSATION", variant["variant_id"]),
        fingerprint={
            "scenario": "HF_DECOMPENSATION",
            "variant_id": variant["variant_id"],
            "precipitant": variant["precipitant"],
            "diagnostic_pathway": variant["pathway"],
            "renal_pattern": "aki_recovered" if aki else "creatinine_stable",
            "procedure": "transthoracic_echocardiogram",
            "disposition": "home",
            "known_hf": "yes" if known else "no",
            "raas": "hold_open" if raas and aki else "no_raas_hold",
        },
        physiology_expectations=["diuresis_weight_down"] + (["aki_recovered"] if aki else []),
        synthea_meta=meta,
        chief_complaint="Progressive dyspnea, orthopnea, and leg swelling",
        syndrome=(
            "acute on chronic heart failure"
            if known
            else "new pulmonary edema with heart failure established during the stay"
        ),
        symptom_duration="five days",
        symptom_course="worse until diuresis, then returned toward the pre-admission baseline",
        symptoms=["dyspnea", "orthopnea", "leg edema"],
        disposition="home",
        specialty="cardiology",
    )
    _history(chart, patient)
    hf_name = ICD10["I50.23"] if known else ICD10["I50.21"]
    chart.diagnosis(hf_name, "I50.23" if known else "I50.21", "hospital", EPISODE)
    cr_words = (
        f"The most recent longitudinal creatinine was {base_cr:.1f} mg/dL."
        if cr_src == SYNTHEA
        else (
            f"No pre-admission creatinine was in the extracted record. The first creatinine "
            f"used as the pre-treatment baseline was {base_cr:.1f} mg/dL."
        )
    )
    wt_words = (
        f"The most recent longitudinal weight was {base_wt:.1f} kg."
        if wt_src == SYNTHEA
        else f"A pre-admission scale weight was not in the extract. The reported home weight was {base_wt:.1f} kg."
    )
    prior = (
        "The longitudinal record already lists heart failure."
        if known
        else "The longitudinal record does not list heart failure. Cardiovascular disease and cardiac medication are present."
    )
    chart.fact(
        "hf-baseline",
        ["baseline"],
        f"{prior} Outpatient products in the longitudinal extract: {_products(meds)}.",
        SYNTHEA,
        10,
        "hpi",
    )
    chart.fact(
        "hf-baseline-numbers",
        ["baseline", "physiology"],
        f"{cr_words} {wt_words}",
        SYNTHEA if cr_src == SYNTHEA and wt_src == SYNTHEA else EPISODE,
        12,
        "hpi",
    )
    chart.fact(
        "hf-acute",
        ["acute_change"],
        (
            "Over five days dyspnea progressed from exertion to conversation, orthopnea required "
            "three pillows, and both legs became swollen. Those symptoms were not the patient's "
            "usual state."
        ),
        EPISODE,
        20,
        "hpi",
    )
    chart.fact("hf-precip", ["precipitant"], variant["precipitant_text"], EPISODE, 30, "hpi")
    chart.fact(
        "hf-present",
        ["presentation"],
        (
            f"On arrival the weight was {adm_wt:.1f} kg, oxygen saturation was 91 percent on room air, "
            "the respiratory rate was 26, the jugular venous pressure was elevated, and crackles were "
            "present halfway up both lung fields. There was pitting edema to the knees."
        ),
        EPISODE,
        40,
        "hpi",
    )
    chart.fact(
        "hf-workup",
        ["workup"],
        variant["workup_text"]
        + " A transthoracic echocardiogram, obtained after the radiograph, showed reduced left-ventricular "
        "systolic function and a congested filling pattern. The numeric ejection fraction was estimated at "
        f"{variant['ef']} percent.",
        EPISODE,
        50,
        "course",
    )
    chart.fact(
        "hf-dx",
        ["diagnosis"],
        (
            f"Those findings established {hf_name}. The diagnosis was not used as the presenting label "
            "before the examination, radiograph, natriuretic peptide, and echocardiogram."
        ),
        EPISODE,
        60,
        "course",
    )
    loop_sentence = (
        f"Home {loop.display} was continued and supplemented with intravenous furosemide while weight was rising."
        if loop
        else (
            "No loop diuretic was in the longitudinal extract. Intravenous furosemide was begun for "
            "congestion and then converted to oral furosemide 40 MG daily."
        )
    )
    chart.fact(
        "hf-treat",
        ["treatment", "medication_decision"],
        (
            f"{loop_sentence} Daily weights and net fluid output were recorded. "
            + (
                f"Home {raas.display} was held on hospital day 1 because creatinine rose from "
                f"{base_cr:.1f} to {adm_cr:.1f} mg/dL. It had not been given again when discharge "
                "planning began."
                if raas and aki
                else "No angiotensin-converting enzyme inhibitor or angiotensin-receptor blocker from a curated regimen was held."
            )
        ),
        EPISODE,
        70,
        "course",
    )
    intake, output = net_from_weight(adm_wt, dis_wt)
    chart.intake_output(
        "diuresis",
        intake,
        output,
        "Net negative balance during the diuretic phase, in the same direction as the weight loss.",
    )
    chart.fact(
        "hf-response",
        ["response", "physiology"],
        (
            f"By hospital day 4 the weight was {dis_wt:.1f} kg, oxygen saturation was 96 percent on room air, "
            f"the respiratory rate was 16, and the patient could lie flat. Creatinine was {dis_cr:.1f} mg/dL "
            f"after a peak of {peak_cr:.1f}. Potassium was 4.3 mmol/L. Dyspnea had returned to the "
            "pre-admission baseline rather than merely being called improved."
        ),
        EPISODE,
        80,
        "course",
    )
    chart.fact(
        "hf-ready",
        ["discharge_readiness"],
        (
            "The patient was walking on the ward, eating, and without resting dyspnea or new chest pain. "
            "The unsigned task is the discharge medication plan, not another day of intravenous diuresis."
        ),
        EPISODE,
        90,
        "course",
    )
    chart.fact(
        "hf-follow",
        ["followup"],
        "Heart-failure clinic follow-up and a chemistry panel were arranged. Home weight monitoring was requested.",
        EPISODE,
        95,
        "course",
    )
    _events(
        chart,
        [
            ("baseline", 10, "Baseline heart-failure or cardiovascular context"),
            ("acute_change", 20, "Progressive congestion"),
            ("precipitant", 30, variant["precipitant"]),
            ("presentation", 40, "Hypoxemia and volume overload"),
            ("workup", 50, "Radiograph, natriuretic peptide, and echocardiogram"),
            ("diagnosis", 60, hf_name),
            ("treatment", 70, "Diuresis and medication review"),
            ("response", 80, "Weight and oxygenation improved"),
            ("discharge", 100, "Discharge planning with unsigned medication reconciliation"),
        ],
    )
    chart.lab(
        "2160-0",
        [("baseline", base_cr), ("admission", adm_cr), ("peak", peak_cr), ("discharge", dis_cr)],
        cr_src if cr_src == SYNTHEA else EPISODE,
    )
    # Inpatient points are episode-generated even when the baseline value was inherited.
    for row in chart.labs:
        if row["timepoint"] != "baseline":
            row["provenance"] = EPISODE
    chart.lab("2823-3", [("admission", 4.6), ("discharge", 4.3)], EPISODE)
    chart.lab("30934-4", [("admission", 1280), ("discharge", 410)], EPISODE)
    chart.lab("10839-9", [("admission", 0.01), ("intermediate", 0.01)], EPISODE)
    admission_temp = 37.2 if variant["variant_id"] == "pulmonary_infection" else 36.8
    admission_systolic = 186 if variant["variant_id"] == "hypertensive_surge" else 150
    admission_diastolic = 104 if variant["variant_id"] == "hypertensive_surge" else 90
    admission_rate = 138 if variant["variant_id"] == "new_atrial_fibrillation" else 104
    chart.vital(
        "admission",
        temp_c=admission_temp,
        bp_systolic=admission_systolic,
        bp_diastolic=admission_diastolic,
        heart_rate=admission_rate,
        resp_rate=26,
        spo2_percent=91,
        provenance=EPISODE,
    )
    chart.vital("discharge", temp_c=36.7, bp_systolic=124, bp_diastolic=72, heart_rate=74, resp_rate=16, spo2_percent=96, provenance=EPISODE)
    chart.weight("baseline", base_wt, wt_src)
    chart.weight("admission", adm_wt, EPISODE)
    chart.weight("discharge", dis_wt, EPISODE)
    chart.image(
        "admission",
        "Chest radiograph",
        "Bilateral pulmonary edema without a focal lobar consolidation.",
        EPISODE,
    )
    chart.image(
        "hospital_day_1",
        "Transthoracic echocardiogram",
        f"Reduced left-ventricular systolic function, estimated ejection fraction {variant['ef']} percent, congested filling.",
        EPISODE,
    )
    chart.consult(
        "cardiology",
        "inpatient",
        "Congestion responded to diuresis. Ischemic and arrhythmic evaluation was the one described in the course.",
        "Primary team to complete the unsigned discharge medication reconciliation.",
    )
    evidence = ["hf-baseline", "hf-response", "hf-ready"]
    if raas and aki:
        regimen = regimen_by_id(raas.regimen_id)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="chronic cardiovascular therapy recorded before this admission",
            regimen_id=regimen.id,
            identity_provenance=SYNTHEA,
            rxcui=raas.rxcui,
            synthea_product=raas.display,
            states=[
                {
                    "state": "home",
                    "time_order": 10,
                    "trigger": "outpatient product in the longitudinal record",
                    "evidence": ["hf-baseline"],
                    "provenance": SYNTHEA,
                },
                {
                    "state": "held",
                    "time_order": 70,
                    "trigger": f"creatinine rose from {base_cr:.1f} to {adm_cr:.1f} mg/dL",
                    "evidence": ["hf-treat"],
                    "provenance": EPISODE,
                },
            ],
            discharge_action="restart",
            evidence_ids=["hf-baseline", "hf-treat", "hf-response"],
            resident_note=(
                f"Held after the creatinine rise. Still held at discharge planning, when creatinine "
                f"was {dis_cr:.1f} mg/dL, potassium was 4.3 mmol/L, and blood pressure was 124/72."
            ),
            rationale=(
                "Restart is supported by the home indication, recovery of creatinine from its peak, "
                "an acceptable potassium, and a stable blood pressure. The chart does not show a "
                "signed restart."
            ),
            monitoring="Chemistry panel within 7 days.",
            follow_up="Heart-failure clinic within 7 days.",
            alternatives=[
                {
                    "alternative_action": "hold",
                    "conditions": "If the clinician wants one more outpatient chemistry before the first dose.",
                    "rationale": "A short additional hold is defensible because the drug is currently held and follow-up is already arranged.",
                }
            ],
        )
    if loop:
        chart.continue_mapped(
            loop,
            "congestion from heart failure",
            ["hf-treat", "hf-response"],
            "The loop diuretic was still required after intravenous therapy stopped, and the weight remained above the pre-admission value.",
            "Oral loop diuretic continued after intravenous doses stopped.",
        )
    else:
        regimen = regimen_by_id(FUROSEMIDE)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="new congestion from heart failure",
            regimen_id=FUROSEMIDE,
            identity_provenance=EPISODE,
            rxcui=None,
            synthea_product=None,
            states=[
                {
                    "state": "new_inpatient",
                    "time_order": 70,
                    "trigger": "no home loop diuretic and ongoing congestion",
                    "evidence": ["hf-treat"],
                    "provenance": EPISODE,
                }
            ],
            discharge_action="new_start",
            evidence_ids=["hf-treat", "hf-response"],
            resident_note="Oral furosemide 40 MG daily replaced intravenous furosemide once the weight was falling.",
            rationale="A maintenance loop diuretic is supported because congestion was the reason for admission and the patient was not previously taking one.",
            monitoring="Daily home weight and a chemistry panel within 7 days.",
            follow_up="Heart-failure clinic within 7 days.",
            alternatives=[
                {
                    "alternative_action": "dose_change",
                    "conditions": "If home weights rise above the discharge weight by more than 2 kg.",
                    "rationale": "The 40 MG dose is a starting regimen. A later increase would be a separate decision if congestion returns.",
                }
            ],
        )
    if variant["variant_id"] == "new_atrial_fibrillation" and beta is None:
        regimen = regimen_by_id("METOPROLOL_SUCCINATE_DAILY")
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="new atrial fibrillation with a rapid ventricular rate",
            regimen_id=regimen.id,
            identity_provenance=EPISODE,
            rxcui=None,
            synthea_product=None,
            states=[
                {
                    "state": "new_inpatient",
                    "time_order": 70,
                    "trigger": "ventricular rate 138 during new atrial fibrillation",
                    "evidence": ["hf-precip", "hf-response"],
                    "provenance": EPISODE,
                }
            ],
            discharge_action="new_start",
            evidence_ids=["hf-precip", "hf-response"],
            resident_note=(
                "Started for the rapid ventricular rate. The rate was 74 at discharge planning "
                "and blood pressure remained 124/72."
            ),
            rationale=(
                "Continuing a once-daily beta blocker is supported by new atrial fibrillation, "
                "a rate that came down on treatment, and a blood pressure that tolerated it."
            ),
            monitoring="Heart rate and blood pressure at follow-up.",
            follow_up="Cardiology within 7 days.",
        )
    if variant["variant_id"] == "recent_nsaid":
        nsaid = _find(meds, {IBUPROFEN})
        regimen = regimen_by_id(IBUPROFEN)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="musculoskeletal pain, not heart failure",
            regimen_id=IBUPROFEN,
            identity_provenance=SYNTHEA if nsaid else EPISODE,
            rxcui=nsaid.rxcui if nsaid else None,
            synthea_product=nsaid.display if nsaid else None,
            states=[
                {
                    "state": "home",
                    "time_order": 10,
                    "trigger": "used for pain before the weight gain",
                    "evidence": ["hf-precip"],
                    "provenance": SYNTHEA if nsaid else EPISODE,
                },
                {
                    "state": "discontinued",
                    "time_order": 70,
                    "trigger": "congestion and a rise in creatinine",
                    "evidence": ["hf-treat", "hf-response"],
                    "provenance": EPISODE,
                },
            ],
            discharge_action="stop",
            evidence_ids=["hf-precip", "hf-treat", "hf-response"],
            resident_note="Stopped during the stay because of fluid retention and the creatinine rise. Not given again.",
            rationale="Stopping is supported by the temporal relationship to decompensation and the creatinine rise. Pain control does not require this anti-inflammatory drug.",
            monitoring="No nonsteroidal monitoring is required after it is stopped.",
            follow_up="Use acetaminophen if pain returns; do not resume the anti-inflammatory drug without review.",
        )
    if variant["variant_id"] == "pulmonary_infection":
        regimen = regimen_by_id(AZITHROMYCIN)
        chart.medication(
            drug=regimen.query,
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            indication="community-acquired pulmonary infection precipitating decompensation",
            regimen_id=AZITHROMYCIN,
            identity_provenance=EPISODE,
            rxcui=None,
            synthea_product=None,
            states=[
                {
                    "state": "hospital_only",
                    "time_order": 70,
                    "trigger": "focal infiltrate and acute dyspnea",
                    "evidence": ["hf-workup"],
                    "provenance": EPISODE,
                },
                {
                    "state": "discontinued",
                    "time_order": 90,
                    "trigger": "five-day course completed and fever never developed",
                    "evidence": ["hf-response"],
                    "provenance": EPISODE,
                },
            ],
            discharge_action="stop",
            evidence_ids=["hf-workup", "hf-response"],
            resident_note="Inpatient course completed. Not a chronic medication.",
            rationale="The respiratory course is finished, so the antibiotic is not continued.",
            monitoring="No further antibiotic monitoring.",
            follow_up="Return for recurrent fever or productive cough.",
            hospital_only=True,
        )
    _continue_rest(
        chart,
        meds,
        {item["regimen_id"] for item in chart.medications},
        evidence,
        "outpatient condition still present",
    )
    chart.monitor("weight", "each morning", "call if more than 2 kg above the discharge weight", "patient")
    chart.monitor("chemistry panel", "within 7 days", "review creatinine and potassium", "primary care")
    chart.follow("Heart-failure clinic", "within 7 days", "cardiology")
    chart.follow("Primary care", "within 7 days", "primary care")
    _task(chart)
    return chart.to_episode()


HF_VARIANTS: list[dict[str, Any]] = [
    {
        "variant_id": "dietary_sodium_missed_diuretic",
        "precipitant": "dietary_sodium_and_missed_diuretic",
        "pathway": "radiograph_bnp_echo_troponin",
        "aki": True,
        "ef": 35,
        "precipitant_text": (
            "The patient described three days of restaurant meals and missed the oral diuretic "
            "on those days. There was no fever, chest pain, or new palpitation."
        ),
        "workup_text": (
            "The chest radiograph showed pulmonary edema. Natriuretic peptide B was elevated. "
            "Troponin I remained 0.01 ng/mL and the electrocardiogram was sinus rhythm without "
            "ST-segment elevation."
        ),
    },
    {
        "variant_id": "nonadherence_cost",
        "precipitant": "medication_nonadherence",
        "pathway": "radiograph_bnp_echo_adherence_history",
        "aki": False,
        "ef": 30,
        "precipitant_text": (
            "The patient stopped several home cardiovascular medicines ten days ago because the "
            "pharmacy refill was unaffordable. Diet and cardiac rhythm were unchanged."
        ),
        "workup_text": (
            "The chest radiograph showed pulmonary edema. Natriuretic peptide B was elevated. "
            "Troponin I remained 0.01 ng/mL. There was no focal infiltrate."
        ),
    },
    {
        "variant_id": "new_atrial_fibrillation",
        "precipitant": "new_atrial_fibrillation_with_rapid_rate",
        "pathway": "telemetry_radiograph_bnp_echo",
        "aki": False,
        "ef": 40,
        "precipitant_text": (
            "Telemetry after arrival showed atrial fibrillation with a ventricular rate of 138. "
            "The longitudinal extract did not list atrial fibrillation, so this rhythm was new."
        ),
        "workup_text": (
            "The chest radiograph showed pulmonary edema. Natriuretic peptide B was elevated. "
            "Troponin I remained 0.01 ng/mL, arguing against an acute coronary occlusion as the cause."
        ),
    },
    {
        "variant_id": "pulmonary_infection",
        "precipitant": "pulmonary_infection",
        "pathway": "radiograph_infiltrate_bnp_echo",
        "aki": True,
        "ef": 35,
        "precipitant_text": (
            "A three-day cough with purulent sputum preceded the dyspnea. Temperature on arrival "
            "was 37.2 degrees Celsius, so fever was not required to recognize the infection."
        ),
        "workup_text": (
            "The chest radiograph showed pulmonary edema plus a right-lower-lobe infiltrate. "
            "Natriuretic peptide B was elevated. Troponin I remained 0.01 ng/mL."
        ),
    },
    {
        "variant_id": "no_clear_precipitant",
        "precipitant": "no_clear_precipitant_after_evaluation",
        "pathway": "negative_adherence_ischemia_rhythm_infection_evaluation",
        "aki": False,
        "ef": 40,
        "precipitant_text": (
            "Pharmacy refill dates confirmed the home medicines were being obtained. There was no "
            "dietary sodium binge, no cough, and no chest pain. The evaluation did not find a discrete precipitant."
        ),
        "workup_text": (
            "The electrocardiogram was sinus. Troponin I remained 0.01 ng/mL. The radiograph showed "
            "edema without infiltrate. Natriuretic peptide B was elevated."
        ),
    },
    {
        "variant_id": "ischemia_evaluated_negative",
        "precipitant": "chest_discomfort_without_infarction",
        "pathway": "serial_troponin_ecg_radiograph_echo",
        "aki": False,
        "ef": 45,
        "precipitant_text": (
            "Pressure-like chest discomfort occurred the evening before admission and resolved before "
            "arrival. It was investigated rather than assumed to be the mechanism of congestion."
        ),
        "workup_text": (
            "Serial troponin I values were 0.01 ng/mL. The electrocardiogram had no ST-segment elevation "
            "or new Q waves. The radiograph showed pulmonary edema, and natriuretic peptide B was elevated."
        ),
    },
    {
        "variant_id": "recent_nsaid",
        "precipitant": "recent_nsaid_use",
        "pathway": "radiograph_bnp_echo_medication_review",
        "aki": True,
        "ef": 30,
        "precipitant_text": (
            "Ibuprofen had been taken for knee pain for six days before the weight rose. No chest pain "
            "or fever was reported."
        ),
        "workup_text": (
            "The chest radiograph showed pulmonary edema without infiltrate. Natriuretic peptide B was "
            "elevated. Troponin I remained 0.01 ng/mL."
        ),
    },
    {
        "variant_id": "hypertensive_surge",
        "precipitant": "missed_antihypertensive_and_pressure_surge",
        "pathway": "blood_pressure_radiograph_bnp_echo",
        "aki": False,
        "ef": 45,
        "precipitant_text": (
            "The patient missed two days of the home antihypertensive medicine. Arrival blood pressure "
            "was 186/104, with no focal neurologic deficit and no chest pain."
        ),
        "workup_text": (
            "The chest radiograph showed pulmonary edema. Natriuretic peptide B was elevated. Troponin I "
            "remained 0.01 ng/mL and the electrocardiogram did not show infarction."
        ),
    },
]
