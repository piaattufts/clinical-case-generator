"""Regression tests for clinical-coherence QC of synthetic generation."""

from __future__ import annotations

import json

from app.models.cases import CaseMedication, ClinicalCase
from app.models.reference import RefLabTest, RefMedication
from app.repositories.cases import (
    list_diagnoses_for_case,
    list_labs_for_case,
    list_medications_for_case,
)
from app.services.clinical_coherence import (
    convert_conventional,
    dose_compatible_with_form,
    formulation_preference_rank_blob,
    implausible_lab_errors,
    indication_matches_problems,
    inferred_route,
    is_symptom_level_concept,
    resident_leak_hits,
    route_compatible_with_form,
    spec_for_lab,
    synthetic_dose_for,
)
from app.services.generation import Scenario, generate_one_case, resolve_profile
from app.services.seed_archetypes import load_seed_archetypes
from app.services.validation_registry import (
    ARCHIVED_BATCH_CODE,
    BALANCED_BATCH_CODE,
    PRECLINICAL_BALANCED_CODE,
    PRECLINICAL_SEED_CODE,
    SEEDCASES_BATCH_CODE,
    active_batch_codes,
    archived_batch_codes,
)
from app.utils.provenance import build_provenance
from sqlalchemy.orm import Session

from tests.test_generation_pipeline import _seed_generation_refs, _test_scenario


def _lab(name: str, unit: str, loinc: str = "TEST_2160-0") -> RefLabTest:
    return RefLabTest(
        loinc_code=loinc,
        long_common_name=name,
        component=name,
        example_ucum_units=[unit],
        **build_provenance("LOINC", "TEST_LOINC_VERSION"),
    )


def test_creatinine_value_unit_coherence_rejects_mgdl_on_umol() -> None:
    errors = implausible_lab_errors("Creatinine [Moles/volume] in Serum or Plasma", 1.2, "umol/L")
    assert errors


def test_glucose_value_unit_coherence_rejects_mgdl_on_mmol() -> None:
    errors = implausible_lab_errors("Glucose [Moles/volume] in Serum or Plasma", 175, "mmol/L")
    assert errors


def test_creatinine_conversion_to_umol_is_physiologic() -> None:
    spec = spec_for_lab(_lab("Creatinine [Moles/volume]", "umol/L"))
    assert spec is not None
    converted = convert_conventional(spec, 1.2, "umol/L")
    assert 90 <= converted <= 130


def test_fatigue_does_not_resolve_to_chronic_fatigue_syndrome() -> None:
    assert is_symptom_level_concept("Fatigue", "fatigue")
    assert not is_symptom_level_concept("Chronic fatigue syndrome", "fatigue")


def test_adult_gi_bleed_outranks_neonatal_hemorrhage() -> None:
    from types import SimpleNamespace

    from app.services.bootstrap import _prefer_icd_concept

    neonatal = SimpleNamespace(
        description="Other neonatal gastrointestinal hemorrhage", icd10cm_code="P54.3"
    )
    adult = SimpleNamespace(
        description="Gastrointestinal hemorrhage, unspecified", icd10cm_code="K92.2"
    )
    chosen = _prefer_icd_concept([neonatal, adult], "gastrointestinal hemorrhage")
    assert chosen is not None
    assert chosen.icd10cm_code == "K92.2"


def test_chest_pain_symptom_does_not_become_angina_pectoris() -> None:
    assert is_symptom_level_concept("Chest pain", "chest pain")
    assert not is_symptom_level_concept("Angina pectoris", "chest pain")


def test_confusion_dyspnea_nausea_remain_symptom_level() -> None:
    for name in ("Confusion", "Dyspnea", "Nausea", "Diarrhea"):
        assert is_symptom_level_concept(name, name.casefold())


def test_injectable_ceftriaxone_cannot_have_oral_route() -> None:
    med = RefMedication(
        rxcui="TEST_CEF",
        concept_name="ceftriaxone 1000 MG Injection",
        generic_name="ceftriaxone",
        dose_form="Injection",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    assert inferred_route(med, "ceftriaxone") == "intravenous"
    assert not route_compatible_with_form("oral", med)
    assert route_compatible_with_form("intravenous", med)


def test_oral_albuterol_capsule_is_not_forced_inhaled() -> None:
    med = RefMedication(
        rxcui="TEST_ALB_CAP",
        concept_name="albuterol 4 MG Extended Release Oral Capsule",
        generic_name="albuterol",
        ingredient="albuterol",
        dose_form="Extended Release Oral Capsule",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    assert inferred_route(med, "albuterol") == "oral"
    assert route_compatible_with_form("oral", med)
    assert not route_compatible_with_form("inhaled", med)


def test_albuterol_inhalation_product_uses_inhaled_route() -> None:
    med = RefMedication(
        rxcui="TEST_ALB_INH",
        concept_name="albuterol 90 MCG/ACTUAT Metered Dose Inhaler",
        generic_name="albuterol",
        ingredient="albuterol",
        dose_form="Metered Dose Inhaler",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    assert inferred_route(med, "albuterol") == "inhaled"
    assert route_compatible_with_form("inhaled", med)
    assert not route_compatible_with_form("oral", med)


def test_formulation_preference_ranks_inhalation_for_albuterol() -> None:
    assert (
        formulation_preference_rank_blob(
            "albuterol 90 MCG/ACTUAT Metered Dose Inhaler", "albuterol"
        )
        == 0
    )
    assert (
        formulation_preference_rank_blob(
            "albuterol 4 MG Extended Release Oral Capsule", "albuterol"
        )
        == 2
    )
    assert formulation_preference_rank_blob("ceftriaxone 1000 MG Injection", "ceftriaxone") == 0
    assert formulation_preference_rank_blob("ceftriaxone Oral Capsule", "ceftriaxone") == 2


def test_dosage_form_and_dose_representation_agree() -> None:
    injection = RefMedication(
        rxcui="TEST_INJ",
        concept_name="ceftriaxone 1000 MG Injection",
        dose_form="Injection",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    inhaler = RefMedication(
        rxcui="TEST_INH",
        concept_name="albuterol inhalation powder",
        dose_form="Inhalation Powder",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    assert synthetic_dose_for(injection) != "1 tablet"
    assert not dose_compatible_with_form("1 tablet", injection)
    assert not dose_compatible_with_form("1 tablet", inhaler)


def test_oral_capsule_does_not_use_tablet_dose() -> None:
    capsule = RefMedication(
        rxcui="TEST_AZITH",
        concept_name="azithromycin 250 MG Oral Capsule",
        generic_name="azithromycin",
        dose_form="Oral Capsule",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    dose = synthetic_dose_for(capsule)
    assert "tablet" not in dose.casefold()
    assert dose == "250 MG"
    assert not dose_compatible_with_form("1 tablet", capsule)


def test_enoxaparin_prefilled_syringe_is_subcutaneous() -> None:
    med = RefMedication(
        rxcui="TEST_ENOX",
        concept_name="0.3 ML enoxaparin sodium 100 MG/ML Prefilled Syringe",
        generic_name="enoxaparin",
        ingredient="enoxaparin",
        dose_form="Prefilled Syringe",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    assert inferred_route(med, "enoxaparin") == "subcutaneous"
    assert route_compatible_with_form("subcutaneous", med)
    assert not route_compatible_with_form("oral", med)


def test_transplant_cmv_profiles_include_valganciclovir() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    for profile in archetypes["TRANSPLANT_CMV"].profiles:
        queries = " ".join(profile.medication_required_queries).casefold()
        assert "valganciclovir" in queries, profile.code
        blob = json.dumps(profile.consults).casefold()
        if "antiviral" in blob:
            assert "valganciclovir" in queries


def test_gi_bleed_lab_pattern_covers_all_bleed_profiles() -> None:
    from app.services.generation import ClinicalProfile, _lab_pattern_for

    for code, course in (
        ("GI_BLEED_PPI_HOSPITAL_ONLY", "gi_bleed_observed_stabilization"),
        ("GI_BLEED_PENDING_AC_DECISION", "pending_endoscopy_decision"),
        ("GI_BLEED_AC_HELD_RESTART", "gi_bleed_held_ac_stable"),
        ("POSTOP_WARFARIN_MONITORING", "postop_anticoag_resume"),
    ):
        profile = ClinicalProfile(
            code=code,
            hospital_course_pattern=course,
            admission_reason="Admitted for gastrointestinal bleeding.",
        )
        assert _lab_pattern_for(profile) == "bleed", code


def test_resident_leak_phrases_are_detected() -> None:
    blob = "The clean case documents a planted error from the seed document."
    hits = resident_leak_hits(blob)
    assert "clean case" in " ".join(hits).casefold()
    assert "planted error" in " ".join(hits).casefold()
    assert "seed document" in " ".join(hits).casefold()
    assert not resident_leak_hits("No medication discrepancies were identified on review.")


def test_generated_labs_use_coherent_creatinine_units(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    db_session.add(
        _lab("Creatinine [Moles/volume] in Serum or Plasma", "umol/L", loinc="TEST_14682-9")
    )
    db_session.flush()
    scenario = _test_scenario()
    scenario.lab_queries = ["Creatinine"]
    result = generate_one_case(
        db_session, sequence=40, seed=1, scenario=scenario, inject_error=False, use_openai=False
    )
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    labs = list_labs_for_case(db_session, case.id)
    creat = [row for row in labs if row.unit == "umol/L"]
    assert creat
    for row in creat:
        assert row.value is not None
        assert row.value >= 50


def test_generated_glucose_is_not_mgdl_labeled_as_mmol(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    db_session.add(
        _lab("Glucose [Moles/volume] in Serum or Plasma", "mmol/L", loinc="TEST_14749-6")
    )
    db_session.flush()
    scenario = _test_scenario()
    scenario.lab_queries = ["Glucose"]
    result = generate_one_case(
        db_session, sequence=41, seed=1, scenario=scenario, inject_error=False, use_openai=False
    )
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    labs = list_labs_for_case(db_session, case.id)
    glucose = [row for row in labs if "Glucose" in (row.test_name or "")]
    assert glucose
    for row in glucose:
        assert row.value is not None
        assert row.value < 40


def test_medication_indication_maps_to_case_diagnosis(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    result = generate_one_case(
        db_session,
        sequence=42,
        seed=1,
        scenario=_test_scenario(),
        inject_error=False,
        use_openai=False,
    )
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    problems = [
        item.diagnosis
        for item in list_diagnoses_for_case(db_session, case.id)
        if item.diagnosis
    ]
    meds = list_medications_for_case(db_session, case.id)
    assert meds
    assert problems
    for row in meds:
        assert indication_matches_problems(row.indication, problems) or (
            "not a treatment for the admission diagnosis" in (row.indication or "").casefold()
        )


def test_admission_and_discharge_labs_are_labeled(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    result = generate_one_case(
        db_session,
        sequence=43,
        seed=1,
        scenario=_test_scenario(),
        inject_error=False,
        use_openai=False,
    )
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    timepoints = {row.timepoint for row in list_labs_for_case(db_session, case.id)}
    assert "admission" in timepoints
    assert "discharge" in timepoints


def test_monitoring_tuple_target_rxcui_binds_medication() -> None:
    from types import SimpleNamespace

    from app.services.error_injection import _tuple_rxcui

    medication = SimpleNamespace(source_reference="RXCUI:855288", rxcui=None)
    target = (medication, "WARFARIN_INR_MONITORING", "INR")
    assert _tuple_rxcui(target) == "855288"


def test_substitution_uses_substitute_dose_not_source_dose() -> None:
    sibling = RefMedication(
        rxcui="TEST_SIB",
        concept_name="TEST_sib 5 MG Oral Tablet",
        generic_name="TEST_sib",
        ingredient="TEST_sib",
        strength="5 mg",
        dose_form="Oral Tablet",
        **build_provenance("RXNORM", "TEST_RXNORM_VERSION"),
    )
    from app.services.error_injection import _replace_medication_identity

    row = CaseMedication(drug="TEST_med", dose="40 mg", route="oral")
    _replace_medication_identity(row, sibling)
    assert row.dose == "5 mg"
    assert row.drug == "TEST_sib"


def test_seed_archetypes_bind_target_medication_queries() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    expected = {
        "OPAT_ENDOCARDITIS": "ceftriaxone",
        "TRANSPLANT_CMV": "valganciclovir",
        "POSTOP_ANTICOAGULATION": "warfarin",
        "GI_BLEED_ACUTE_CHANGE": "apixaban",
        "HF_DECOMPENSATION": "lisinopril",
    }
    for code, needle in expected.items():
        profiles = archetypes[code].profiles
        assert any(
            needle
            in " ".join(
                [
                    item.target_medication_query or "",
                    item.hold_medication_query or "",
                    item.pending_decision_medication_query or "",
                    *item.medication_required_queries,
                ]
            ).casefold()
            for item in profiles
        )


def test_opat_monitoring_is_specified_on_clean_profiles() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    opat = next(
        item
        for item in archetypes["OPAT_ENDOCARDITIS"].profiles
        if item.code == "OPAT_STABLE_COMPLETION_PLAN"
    )
    assert opat.monitoring_parameter
    assert "weekly" in (opat.monitoring_frequency or "weekly")
    assert opat.devices


def test_held_restart_narratives_do_not_claim_a_completed_plan() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    for code in ("HF_DECOMPENSATION", "TRANSPLANT_CMV", "GI_BLEED_ACUTE_CHANGE"):
        for profile in archetypes[code].profiles:
            if "f2_held_med_no_restart_plan" not in profile.allowed_error_categories:
                continue
            blob = " ".join(
                [
                    profile.context_note,
                    profile.admission_reason,
                    profile.hold_reason or "",
                ]
            ).casefold()
            assert "documented restart plan" not in blob, profile.code
            assert "documented plan to reassess restart" not in blob, profile.code
            assert "explicit plan to reassess restart" not in blob, profile.code


def test_hold_reason_is_profile_specific() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    hf = next(
        item
        for item in archetypes["HF_DECOMPENSATION"].profiles
        if item.code == "HF_DECOMP_AKI_HOLDS"
    )
    assert hf.hold_medication_query == "lisinopril"
    assert hf.hold_reason is not None
    assert "creatinine" in hf.hold_reason.casefold()


def test_active_batch_codes_are_corrected_revisions() -> None:
    assert BALANCED_BATCH_CODE == "CLINIPROOF_BALANCED_V3"
    assert SEEDCASES_BATCH_CODE == "CLINIPROOF_SEEDCASES_V2"
    assert active_batch_codes() == (BALANCED_BATCH_CODE, SEEDCASES_BATCH_CODE)
    assert ARCHIVED_BATCH_CODE in archived_batch_codes()
    assert PRECLINICAL_BALANCED_CODE in archived_batch_codes()
    assert PRECLINICAL_SEED_CODE in archived_batch_codes()


def test_io_omitted_by_default_profile() -> None:
    profile = resolve_profile(
        Scenario(
            code="X",
            specialty="x",
            care_context="inpatient",
            age_min=50,
            age_max=60,
            target_error_category="none",
            diagnosis_queries=["x"],
            symptom_queries=["x"],
            medication_queries=["x"],
            anticoagulant_mutex_queries=[],
            lab_queries=["x"],
        ),
        None,
    )
    assert profile.io_enabled is False


def test_pending_decision_targets_match_profile_definitions() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    opat = next(
        item
        for item in archetypes["OPAT_ENDOCARDITIS"].profiles
        if item.code == "OPAT_MISSING_ID_FOLLOWUP"
    )
    assert opat.pending_decision_medication_query == "ceftriaxone"
    transplant = next(
        item
        for item in archetypes["TRANSPLANT_CMV"].profiles
        if item.code == "TRANSPLANT_PENDING_ANTIVIRAL_DURATION"
    )
    assert transplant.pending_decision_medication_query == "valganciclovir"
    gi = next(
        item
        for item in archetypes["GI_BLEED_ACUTE_CHANGE"].profiles
        if item.code == "GI_BLEED_PENDING_AC_DECISION"
    )
    assert gi.pending_decision_medication_query == "apixaban"
    medrec = next(
        item
        for item in archetypes["MEDREC_UNCERTAIN_HISTORY"].profiles
        if item.code == "MEDREC_PENDING_COGNITIVE_THERAPY"
    )
    assert medrec.pending_decision_medication_query is None
    assert "cognitive-enhancer" in (medrec.pending_decision_text or "").casefold()


def test_source_seed_documents_remain_unchanged() -> None:
    import hashlib
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "data" / "seed_cases" / "resident_authored"
    expected = {
        "Bad_Med_Rec_Case.docx": "exists",
        "Heart_Failure_Case.docx": "exists",
        "OPAT_Case.docx": "exists",
        "Post_transplant_case.docx": "exists",
        "Post-Op_Case.docx": "exists",
        "Sepsis_AMA_Case.docx": "exists",
    }
    files = sorted(path.name for path in root.iterdir() if path.suffix.lower() == ".docx")
    assert set(expected) <= set(files)
    for name in expected:
        digest = hashlib.sha256((root / name).read_bytes()).hexdigest()
        assert len(digest) == 64


def test_hospital_course_text_has_no_resident_leakage() -> None:
    from app.services.generation import HOSPITAL_COURSE_TEXT

    blob = " ".join(HOSPITAL_COURSE_TEXT.values())
    assert not resident_leak_hits(blob)
    postop = HOSPITAL_COURSE_TEXT["postop_anticoag_resume"].casefold()
    opat = HOSPITAL_COURSE_TEXT["opat_pending_duration"].casefold()
    assert "monitoring was arranged" not in postop
    assert "follow-up were arranged" not in opat
    assert "clean case" not in blob.casefold()


def test_historical_taxonomy_v1_and_source_seeds_remain_on_disk() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "validation" / "resident_validation_cases.json").is_file()
    v1 = json.loads((root / "data" / "validation" / "resident_validation_cases.json").read_text())
    assert v1["batch_code"] == "CLINIPROOF_TAXONOMY_V1"
    assert len(v1["cases"]) == 24
    seeds = root / "data" / "seed_cases" / "resident_authored"
    assert (seeds / "OPAT_Case.docx").is_file()


def test_one_stage_c1_c5_form_is_used() -> None:
    from app.services.readable_packets import C1_TO_C5_FORM

    assert "### C1 Clinical plausibility" in C1_TO_C5_FORM
    assert "Stage 1" not in C1_TO_C5_FORM
    assert "Stage 2" not in C1_TO_C5_FORM


def test_discharge_vitals_use_discharge_ready_pattern() -> None:
    from random import Random

    from app.services.generation import _discharge_vital_pattern, _synthetic_vitals

    assert _discharge_vital_pattern("febrile_pneumonia") == "discharge_ready"
    assert _discharge_vital_pattern("hypertensive") == "discharge_ready"
    vitals = _synthetic_vitals(Random(7), "discharge_ready")
    assert vitals["heart_rate"] <= 88
    assert float(vitals["spo2_percent"]) >= 95
    assert vitals["resp_rate"] <= 20


def test_lab_pattern_is_profile_specific() -> None:
    from app.services.generation import ClinicalProfile, _lab_pattern_for

    opat = ClinicalProfile(code="opat", hospital_course_pattern="opat_parenteral_course")
    assert _lab_pattern_for(opat) == "standard"
    aki = ClinicalProfile(code="aki", hospital_course_pattern="aki_hold_reassessment")
    assert _lab_pattern_for(aki) == "aki"
    bleed = ClinicalProfile(code="bleed", hospital_course_pattern="gi_bleed_held_ac_stable")
    assert _lab_pattern_for(bleed) == "bleed"
    ppi = ClinicalProfile(
        code="GI_BLEED_PPI_HOSPITAL_ONLY",
        hospital_course_pattern="gi_bleed_observed_stabilization",
    )
    assert _lab_pattern_for(ppi) == "bleed"
    glycemic = ClinicalProfile(
        code="dm", hospital_course_pattern="glycemic_stabilization", vital_pattern="glycemic"
    )
    assert _lab_pattern_for(glycemic) == "glycemic"


def test_opat_consults_are_not_copied_from_antiviral_text() -> None:
    archetypes = {item.code: item for item in load_seed_archetypes()}
    for profile in archetypes["OPAT_ENDOCARDITIS"].profiles:
        blob = json.dumps(profile.consults).casefold()
        assert "antiviral" not in blob, profile.code


def test_balanced_v3_plan_declares_balanced_structured() -> None:
    from pathlib import Path

    plan = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "data"
            / "validation_balanced_v3"
            / "batch_plan.json"
        ).read_text(encoding="utf-8")
    )
    assert plan["generation_strategy"] == "balanced_structured"
    assert plan["batch_code"] == "CLINIPROOF_BALANCED_V3"
    assert len(plan["cases"]) == 24


def test_low_dose_aspirin_maps_to_ischemic_problem() -> None:
    from types import SimpleNamespace

    from app.services.generation import _indication_for

    med = SimpleNamespace(
        ingredient="aspirin",
        generic_name="aspirin",
        concept_name="aspirin 75 MG Delayed Release Oral Tablet",
    )
    cad = SimpleNamespace(
        preferred_name="Atherosclerotic heart disease of native coronary artery",
        icd10cm_code="I25.10",
    )
    assert "atherosclerotic" in _indication_for(None, med, [cad]).casefold()
    gi = SimpleNamespace(
        preferred_name="Gastrointestinal hemorrhage, unspecified",
        icd10cm_code="K92.2",
    )
    skipped = _indication_for(None, med, [gi]).casefold()
    assert "not a treatment for the admission diagnosis" in skipped


def test_readable_investigations_are_not_python_dicts() -> None:
    from app.services.readable_packets import _other_visible

    text = _other_visible(
        {
            "CaseImaging": [
                {
                    "study_type": "Chest radiograph",
                    "timepoint": "admission",
                    "body_site": "chest",
                    "finding": "Right lower-lobe infiltrate",
                }
            ],
            "CaseConsult": [
                {
                    "service": "infectious disease",
                    "timepoint": "inpatient",
                    "assessment": "Endocarditis under treatment.",
                    "recommendation": "Complete the planned parenteral course.",
                }
            ],
        },
        {},
    )
    assert "{'study_type'" not in text
    assert "Chest radiograph" in text
    assert "infectious disease" in text.casefold()


def test_resident_leak_detects_generator_origin_phrase() -> None:
    assert resident_leak_hits("value origin synthetic_model_generated")
    assert not resident_leak_hits("The QRS generator interval was not recorded.")
