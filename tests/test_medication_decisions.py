"""Discharge actions come from indication and charted facts, not list membership."""

from __future__ import annotations

from app.services.medication_decisions import (
    CLINICALLY_INCONSISTENT,
    HIDDEN_ANSWER_DEPENDENCY,
    SUFFICIENT_EVIDENCE,
    WEAK_EVIDENCE,
    consider_source_backed_change,
    consistency_errors,
    justify_dose_change,
    justify_home_medication,
    justify_hospital_start,
    justify_visible_stop,
    public_action,
)

HF = "Acute systolic (congestive) heart failure"


def test_heart_failure_drug_continues_only_with_visible_safety_facts() -> None:
    decision = justify_home_medication(
        "furosemide 40 MG Oral Tablet",
        [HF],
        creatinine=1.1,
        potassium=4.0,
        systolic_bp=118,
        dose="40 MG",
        route="oral",
        frequency="once daily",
    )
    assert decision.include is True
    assert decision.action == "continue"
    assert decision.evidence_class == SUFFICIENT_EVIDENCE
    assert decision.indication == HF
    assert any(
        item.type == "lab" and item.name == "creatinine" for item in decision.supporting_evidence
    )


def test_statin_without_lipid_diagnosis_is_not_continued() -> None:
    decision = justify_home_medication(
        "atorvastatin 40 MG Oral Tablet",
        [HF],
        creatinine=1.0,
        potassium=4.0,
        systolic_bp=120,
    )
    assert decision.include is False
    assert decision.evidence_class == CLINICALLY_INCONSISTENT


def test_anticoagulant_without_indication_is_not_added() -> None:
    decision = justify_home_medication(
        "apixaban 5 MG Oral Tablet",
        [HF],
        systolic_bp=120,
    )
    assert decision.include is False
    assert decision.evidence_class == CLINICALLY_INCONSISTENT


def test_ace_inhibitor_can_use_the_regimen_citation_for_heart_failure() -> None:
    decision = justify_home_medication(
        "lisinopril 10 MG Oral Tablet",
        [HF],
        creatinine=1.0,
        potassium=4.0,
        systolic_bp=120,
    )
    assert decision.include is True
    assert decision.action == "continue"
    assert decision.indication == HF
    assert any(
        item.interpretation and "citation" in item.interpretation
        for item in decision.supporting_evidence
    )


def test_ace_inhibitor_still_matches_hypertension_from_the_indication_map() -> None:
    decision = justify_home_medication(
        "lisinopril 10 MG Oral Tablet",
        ["Essential (primary) hypertension"],
        creatinine=1.0,
        potassium=4.0,
        systolic_bp=120,
    )
    assert decision.include is True
    assert decision.indication == "Essential (primary) hypertension"


def test_hospital_start_without_indication_is_omitted() -> None:
    decision = justify_hospital_start(
        "pantoprazole 40 MG Delayed Release Oral Tablet",
        [HF],
    )
    assert decision.include is False


def test_stop_without_a_visible_clinical_fact_is_omitted() -> None:
    decision = justify_visible_stop(
        "ibuprofen 400 MG Oral Tablet",
        [HF],
        visible_reason="Stopped during this admission.",
    )
    assert decision.include is False
    assert decision.evidence_class == HIDDEN_ANSWER_DEPENDENCY


def test_stop_with_a_charted_bleed_is_sufficient() -> None:
    decision = justify_visible_stop(
        "ibuprofen 400 MG Oral Tablet",
        [HF],
        visible_reason="Gastrointestinal bleeding was documented during the admission.",
    )
    assert decision.include is True
    assert decision.action == "stop"
    assert decision.evidence_class == SUFFICIENT_EVIDENCE
    assert decision.held_reason is not None
    assert "stopped" not in decision.held_reason.casefold()


def test_dose_change_requires_a_different_regimen_and_a_visible_fact() -> None:
    refused = justify_dose_change(
        "furosemide 40 MG Oral Tablet",
        indication="heart failure",
        from_dose="40 MG",
        to_dose="40 MG",
        from_frequency="once daily",
        to_frequency="once daily",
        evidence_text="congestion persisted",
    )
    changed = justify_dose_change(
        "furosemide 40 MG Oral Tablet",
        indication="heart failure",
        from_dose="40 MG",
        to_dose="80 MG",
        from_frequency="once daily",
        to_frequency="once daily",
        evidence_text="persistent volume overload after the initial diuretic dose",
    )
    assert refused.include is False
    assert changed.include is True
    assert changed.action == "dose_change"
    assert public_action(changed.action) == "change"
    assert changed.evidence_class == SUFFICIENT_EVIDENCE


def test_source_backed_change_is_refused_when_only_one_regimen_exists() -> None:
    decision = consider_source_backed_change(
        "furosemide 40 MG Oral Tablet",
        indication=HF,
        evidence_text="The outpatient diuretic plan was adjusted during the stay.",
    )
    assert decision.include is False


def test_missing_creatinine_does_not_default_to_continue() -> None:
    decision = justify_home_medication(
        "spironolactone 25 MG Oral Tablet",
        [HF],
        creatinine=None,
        potassium=4.0,
        systolic_bp=120,
    )
    assert decision.include is False
    assert decision.action == "omit"
    assert decision.evidence_class == WEAK_EVIDENCE


def test_creatinine_at_the_existing_aki_floor_holds_the_medicine() -> None:
    decision = justify_home_medication(
        "lisinopril 10 MG Oral Tablet",
        [HF],
        creatinine=1.8,
        creatinine_unit="mg/dL",
        potassium=4.0,
        systolic_bp=118,
    )
    assert decision.include is True
    assert decision.action == "hold"
    assert decision.evidence_class == SUFFICIENT_EVIDENCE


def test_consistency_flags_an_admission_diagnosis_copied_onto_a_statin() -> None:
    errors = consistency_errors(
        medication="atorvastatin 40 MG Oral Tablet",
        action="continue",
        indication=HF,
        diagnosis_names=[HF],
        admission_diagnosis=HF,
        monitoring_parameters=[],
        medication_names=["atorvastatin 40 MG Oral Tablet"],
        allergies=[],
        visible_text=HF,
        temporal_role="pre_existing_home",
    )
    assert any("admission diagnosis" in item for item in errors)


def test_consistency_flags_inr_monitoring_without_warfarin() -> None:
    errors = consistency_errors(
        medication="apixaban 5 MG Oral Tablet",
        action="continue",
        indication="Atrial fibrillation",
        diagnosis_names=["Atrial fibrillation"],
        admission_diagnosis="Atrial fibrillation",
        monitoring_parameters=["INR check"],
        medication_names=["apixaban 5 MG Oral Tablet"],
        allergies=[],
        visible_text="Atrial fibrillation",
        temporal_role="pre_existing_home",
    )
    assert any("without warfarin" in item for item in errors)
