"""Constrained synthetic case generation from local source-backed reference rows.

Canonical concepts are selected in Python. OpenAI may only assemble narrative
language after that selection. Numeric values are synthetic and labeled as such.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import __version__
from app.models.cases import (
    CaseConsult,
    CaseDevice,
    CaseDiagnosis,
    CaseDischargePlanning,
    CaseFollowup,
    CaseImaging,
    CaseInstruction,
    CaseIntakeOutput,
    CaseLab,
    CaseMedication,
    CaseMedicationReconciliation,
    CaseMicrobiology,
    CaseMonitoring,
    CaseNote,
    CasePresentation,
    CaseProblemList,
    CaseProcedure,
    CaseReturnPrecaution,
    CaseSocialSupport,
    CaseSymptom,
    CaseVital,
    CaseWeight,
    ClinicalCase,
)
from app.models.generation import CaseBlueprint, CaseGenerationRun, CaseMedicationPlan
from app.models.reference import RefDiagnosis, RefLabTest, RefMedication, RefSymptom
from app.openai.narrative import CaseNarrative, assemble_narrative
from app.repositories.cases import (
    delete_case_graph,
    delete_generation_artifacts_for_case_code,
    get_case_by_code,
    get_frozen_case_for_clinical_id,
    list_answer_keys_for_case,
    list_diagnoses_for_case,
    list_labs_for_case,
    list_medications_for_case,
    list_plans_for_case,
)
from app.repositories.reference import (
    get_data_source,
    list_enabled_rules,
    list_medication_classes_for_rxcui,
    list_medications_sharing_class,
    search_symptoms,
)
from app.services.bootstrap import (
    DEFAULT_SCENARIO_PATH,
    load_json_object,
    match_diagnosis,
    match_lab,
    match_medication,
)
from app.services.case_diversity import (
    CleanCaseFingerprint,
    fingerprint_as_dict,
    fingerprint_from_case,
)
from app.services.clinical_coherence import (
    INDICATION_BY_QUERY,
    convert_conventional,
    is_symptom_level_concept,
    preferred_lab_unit,
    spec_for_lab,
)
from app.services.error_injection import InjectionResult, inject_reconciliation_error
from app.services.error_taxonomy import (
    CLEAN_SUPPLY_DAYS,
    F1_COMMISSION,
    F1_SUBSTITUTION,
    F2_HELD_RESTART,
    F2_HOSPITAL_ONLY,
    F2_INPATIENT_SUB,
    F2_MONITORING,
    F2_PENDING_FOLLOWUP,
    F2_SUPPLY,
    FAMILY_FOR_CATEGORY,
    FOLLOWUP_DAYS_FOR_SUPPLY,
    NONE,
    canonicalize_category,
    class_usable_for_substitution,
    require_eligible,
    resolve_requested_category,
)
from app.services.medication_regimens import (
    administration_for,
    regimen_for_medication,
    temporal_role_for,
)
from app.services.rules import CaseSnapshot, evaluate_rules, hard_violations
from app.services.validation import require_valid, serialize_report, validate_case
from app.sources.exceptions import (
    CaseValidationError,
    FrozenValidationCaseError,
    ReferenceResolutionError,
)
from app.utils.identifiers import CHILD_ID_PREFIXES, format_case_id_code, format_child_business_id

GENERATOR_NAME = "clinical-case-generator"
NUMERIC_ORIGIN = "synthetic_model_generated"


@dataclass
class Scenario:
    code: str
    specialty: str
    care_context: str
    age_min: int
    age_max: int
    target_error_category: str
    diagnosis_queries: list[str]
    symptom_queries: list[str]
    medication_queries: list[str]
    anticoagulant_mutex_queries: list[str]
    lab_queries: list[str]
    stop_medication_queries: list[str] = field(default_factory=list)
    hospital_only_medication_queries: list[str] = field(default_factory=list)
    allowed_error_categories: list[str] = field(default_factory=list)
    default_frequency: str = "once daily"
    profiles: list[ClinicalProfile] = field(default_factory=list)
    generation_strategy: str = "randomized_template"
    seed_archetype_name: str | None = None
    seed_source_filename: str | None = None
    seed_source_type: str | None = None
    blueprint_version: str | None = None


@dataclass
class ClinicalProfile:
    code: str
    symptom_queries: list[str] = field(default_factory=list)
    symptom_duration: str = "several days"
    symptom_course: str = "worsening"
    symptom_severity: str = "moderate"
    medication_required_queries: list[str] = field(default_factory=list)
    medication_optional_queries: list[str] = field(default_factory=list)
    optional_include: list[str] = field(default_factory=list)
    anticoagulant: str | None = None
    stop_medication_queries: list[str] = field(default_factory=list)
    hospital_only_medication_queries: list[str] = field(default_factory=list)
    lab_queries: list[str] = field(default_factory=list)
    hospital_course_pattern: str = "day1_io_ready_home"
    disposition: str = "home"
    home_health_ordered: bool = False
    followup_item: str = "Primary care follow-up"
    followup_service: str = "primary care"
    followup_timing: str = "7 days"
    allowed_error_categories: list[str] = field(default_factory=list)
    vital_pattern: str = "standard"
    io_timepoint: str = "hospital_day_1"
    context_note: str = ""
    comorbidity_queries: list[str] = field(default_factory=list)
    imaging: list[dict[str, str]] = field(default_factory=list)
    consults: list[dict[str, str]] = field(default_factory=list)
    procedures: list[dict[str, str]] = field(default_factory=list)
    devices: list[dict[str, str]] = field(default_factory=list)
    microbiology: list[dict[str, str]] = field(default_factory=list)
    io_enabled: bool = False
    io_net_direction: str = "neutral"
    bpmh_source: str = "patient_and_prior_records"
    patient_able_to_participate: bool = True
    medrec_notes: str = ""
    target_medication_query: str | None = None
    hold_medication_query: str | None = None
    hold_reason: str | None = None
    restart_plan: str | None = None
    pending_decision_medication_query: str | None = None
    pending_decision_text: str | None = None
    monitoring_parameter: str | None = None
    monitoring_frequency: str | None = None
    monitoring_service: str | None = None
    include_discharge_status: bool = True
    admission_reason: str = ""
    medication_temporal_roles: dict[str, str] = field(default_factory=dict)


HOSPITAL_COURSE_TEXT = {
    "day1_io_ready_home": (
        "The inpatient stay was brief. Symptoms and vital signs were observed, "
        "and the patient was judged ready for discharge home."
    ),
    "multi_day_diuresis": (
        "The hospital course focused on diuresis over several inpatient days. "
        "Intake and output were recorded, and congestion improved enough for discharge."
    ),
    "improving_after_treatment": (
        "Symptoms improved after inpatient treatment. The patient was observed "
        "until discharge readiness was documented."
    ),
    "rate_control_observed": (
        "Heart rate was observed and treated during the stay. The patient was "
        "discharged once rate control was clinically acceptable."
    ),
    "antibiotic_course_inpatient": (
        "Inpatient antimicrobial therapy was administered and respiratory symptoms "
        "were monitored until the patient was ready for discharge."
    ),
    "glycemic_stabilization": (
        "Capillary glucose was monitored. Correctional subcutaneous insulin was "
        "given while inpatient and stopped at discharge. Home metformin was continued."
    ),
    "hypertensive_treatment": (
        "Blood pressure was treated and observed in hospital. The discharge plan "
        "continues the selected antihypertensive regimen."
    ),
    "medication_adjustment": (
        "Home therapy was reviewed and adjusted during the stay. The discharge "
        "list reflects the intended outpatient regimen."
    ),
    "observed_stabilization": (
        "The patient was observed until vital signs and symptoms stabilized "
        "enough for discharge."
    ),
    "collateral_medrec_complete": (
        "A collateral medication list was obtained after admission and verified. "
        "Unknown names were not converted into discharge orders. Intentionally "
        "discontinued therapy was documented separately from incomplete information."
    ),
    "home_services_transition": (
        "The patient returned to cognitive baseline. Home services were arranged "
        "and the verified medication list was prepared for discharge."
    ),
    "pending_outpatient_therapy_decision": (
        "A new disease-modifying start was deferred to outpatient confirmation."
    ),
    "opat_pending_duration": (
        "Cultures cleared on inpatient therapy. Remaining parenteral duration is "
        "to be confirmed as an outpatient decision."
    ),
    "multi_day_diuresis_weights": (
        "Congestion was treated with inpatient diuresis. Serial weights and "
        "intake/output were used to judge readiness for discharge."
    ),
    "aki_hold_reassessment": (
        "Creatinine rose with congestion. Selected therapy was held."
    ),
    "potassium_repletion_diuresis": (
        "Diuresis was accompanied by potassium repletion. Electrolytes were "
        "trending toward a range acceptable for discharge."
    ),
    "diuretic_dose_adjustment": (
        "The outpatient diuretic plan was adjusted during the stay after the "
        "inpatient response to therapy was observed."
    ),
    "opat_parenteral_course": (
        "Parenteral antimicrobial therapy was continued with a specified remaining "
        "duration, laboratory monitoring, and line precautions for discharge."
    ),
    "opat_culture_clearance": (
        "Cultures cleared on inpatient therapy. The remaining parenteral course "
        "and infectious-disease follow-up were arranged before discharge."
    ),
    "transplant_antiviral_conversion": (
        "Infectious symptoms improved. Inpatient antiviral therapy was converted "
        "to the intended outpatient agent."
    ),
    "transplant_aki_holds": (
        "Volume-related kidney injury led to temporary holds of selected immunosuppression."
    ),
    "postop_anticoag_resume": (
        "Anticoagulation was interrupted for surgery and then resumed."
    ),
    "postop_hemoglobin_observed": (
        "Postoperative hemoglobin was observed without transfusion. Rehabilitation "
        "and anticoagulation follow-up were planned."
    ),
    "gi_bleed_held_ac_stable": (
        "Gastrointestinal bleeding settled and hemoglobin was stable. "
        "Anticoagulation was held."
    ),
    "gi_bleed_aspirin_stopped": (
        "Gastrointestinal bleeding settled and hemoglobin was stable. "
        "Aspirin used for primary prevention was stopped."
    ),
    "pending_endoscopy_decision": (
        "Restart versus continued hold of anticoagulation remains a pending "
        "outpatient decision. The patient is otherwise ready for discharge."
    ),
    "gi_bleed_observed_stabilization": (
        "Gastrointestinal bleeding was observed with serial hemoglobin checks. "
        "Inpatient acid suppression was used while the patient stabilized for discharge."
    ),
}


def default_profile(scenario: Scenario) -> ClinicalProfile:
    """Family-level profile used when a batch assignment does not name a variant."""
    return ClinicalProfile(
        code="default",
        symptom_queries=list(scenario.symptom_queries),
        medication_required_queries=list(scenario.medication_queries),
        stop_medication_queries=list(scenario.stop_medication_queries),
        hospital_only_medication_queries=list(scenario.hospital_only_medication_queries),
        lab_queries=list(scenario.lab_queries),
        allowed_error_categories=list(scenario.allowed_error_categories),
    )


def resolve_profile(scenario: Scenario, profile_code: str | None) -> ClinicalProfile:
    if profile_code:
        for item in scenario.profiles:
            if item.code == profile_code:
                return item
        raise ValueError(
            f"unknown clinical profile {profile_code!r} for scenario {scenario.code}"
        )
    if len(scenario.profiles) == 1:
        return scenario.profiles[0]
    return default_profile(scenario)


def _load_profiles(item: dict[str, Any]) -> list[ClinicalProfile]:
    raw = item.get("clinical_profiles") or item.get("profiles") or []
    if not isinstance(raw, list):
        return []
    profiles: list[ClinicalProfile] = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        anticoagulant = row.get("anticoagulant")
        profiles.append(
            ClinicalProfile(
                code=str(row.get("code") or "default"),
                symptom_queries=_str_list(row.get("symptom_queries")),
                symptom_duration=str(row.get("symptom_duration") or "several days"),
                symptom_course=str(row.get("symptom_course") or "worsening"),
                symptom_severity=str(row.get("symptom_severity") or "moderate"),
                medication_required_queries=_str_list(row.get("medication_required_queries")),
                medication_optional_queries=_str_list(row.get("medication_optional_queries")),
                optional_include=_str_list(row.get("optional_include")),
                anticoagulant=None if anticoagulant in (None, "") else str(anticoagulant),
                stop_medication_queries=_str_list(row.get("stop_medication_queries")),
                hospital_only_medication_queries=_str_list(
                    row.get("hospital_only_medication_queries")
                ),
                lab_queries=_str_list(row.get("lab_queries")),
                hospital_course_pattern=str(
                    row.get("hospital_course_pattern") or "day1_io_ready_home"
                ),
                disposition=str(row.get("disposition") or "home"),
                home_health_ordered=bool(row.get("home_health_ordered")),
                followup_item=str(row.get("followup_item") or "Primary care follow-up"),
                followup_service=str(row.get("followup_service") or "primary care"),
                followup_timing=str(row.get("followup_timing") or "7 days"),
                allowed_error_categories=_str_list(row.get("allowed_error_categories")),
                vital_pattern=str(row.get("vital_pattern") or "standard"),
                io_timepoint=str(row.get("io_timepoint") or "hospital_day_1"),
                context_note=str(row.get("context_note") or ""),
                comorbidity_queries=_str_list(row.get("comorbidity_queries")),
                imaging=_dict_list(row.get("imaging")),
                consults=_dict_list(row.get("consults")),
                procedures=_dict_list(row.get("procedures")),
                devices=_dict_list(row.get("devices")),
                microbiology=_dict_list(row.get("microbiology")),
                io_enabled=bool(row.get("io_enabled")),
                io_net_direction=str(row.get("io_net_direction") or "neutral"),
                bpmh_source=str(row.get("bpmh_source") or "patient_and_prior_records"),
                patient_able_to_participate=(
                    True
                    if row.get("patient_able_to_participate") is None
                    else bool(row.get("patient_able_to_participate"))
                ),
                medrec_notes=str(row.get("medrec_notes") or ""),
                target_medication_query=_optional_str(row.get("target_medication_query")),
                hold_medication_query=_optional_str(row.get("hold_medication_query")),
                hold_reason=_optional_str(row.get("hold_reason")),
                restart_plan=_optional_str(row.get("restart_plan")),
                pending_decision_medication_query=_optional_str(
                    row.get("pending_decision_medication_query")
                ),
                pending_decision_text=_optional_str(row.get("pending_decision_text")),
                monitoring_parameter=_optional_str(row.get("monitoring_parameter")),
                monitoring_frequency=_optional_str(row.get("monitoring_frequency")),
                monitoring_service=_optional_str(row.get("monitoring_service")),
                include_discharge_status=(
                    True
                    if row.get("include_discharge_status") is None
                    else bool(row.get("include_discharge_status"))
                ),
                admission_reason=str(row.get("admission_reason") or ""),
                medication_temporal_roles=_role_map(row.get("medication_temporal_roles")),
            )
        )
    return profiles


def _scenario_from_mapping(item: dict[str, Any]) -> Scenario:
    return Scenario(
        code=str(item.get("code") or "DEFAULT"),
        specialty=str(item.get("specialty") or "unspecified"),
        care_context=str(item.get("care_context") or "inpatient"),
        age_min=int(item.get("age_min") or 55),
        age_max=int(item.get("age_max") or 85),
        target_error_category=str(item.get("target_error_category") or "f1_omission"),
        diagnosis_queries=_str_list(item.get("diagnosis_queries")),
        symptom_queries=_str_list(item.get("symptom_queries")),
        medication_queries=_str_list(item.get("medication_queries")),
        anticoagulant_mutex_queries=_str_list(item.get("anticoagulant_mutex_queries")),
        lab_queries=_str_list(item.get("lab_queries")),
        stop_medication_queries=_str_list(item.get("stop_medication_queries")),
        hospital_only_medication_queries=_str_list(
            item.get("hospital_only_medication_queries")
        ),
        allowed_error_categories=_str_list(item.get("allowed_error_categories")),
        default_frequency=str(item.get("default_frequency") or "once daily"),
        profiles=_load_profiles(item),
        generation_strategy=str(item.get("generation_strategy") or "randomized_template"),
        seed_archetype_name=(
            None
            if item.get("seed_archetype_name") in (None, "")
            else str(item.get("seed_archetype_name"))
        ),
        seed_source_filename=(
            None
            if item.get("seed_source_filename") in (None, "")
            else str(item.get("seed_source_filename"))
        ),
        seed_source_type=(
            None
            if item.get("seed_source_type") in (None, "")
            else str(item.get("seed_source_type"))
        ),
        blueprint_version=(
            None
            if item.get("blueprint_version") in (None, "")
            else str(item.get("blueprint_version"))
        ),
    )


@dataclass
class GeneratedCaseResult:
    case_id_code: str
    case_id: UUID
    seed: str
    clean_passed: bool
    injected: InjectionResult | None
    validation: dict[str, Any]
    narrative_source: str
    clean_state: dict[str, Any]
    clean_validation: dict[str, Any]
    clinical_profile: str = "default"
    hospital_course_pattern: str = "day1_io_ready_home"
    fingerprint: CleanCaseFingerprint | None = None


@dataclass
class _IdCounter:
    case_id_code: str
    counts: dict[str, int] = field(default_factory=dict)

    def next_id(self, kind: str) -> str:
        prefix = CHILD_ID_PREFIXES[kind]
        self.counts[kind] = self.counts.get(kind, 0) + 1
        return format_child_business_id(prefix, self.case_id_code, self.counts[kind])


def load_scenarios(path: Path | None = None) -> list[Scenario]:
    raw = load_json_object(path or DEFAULT_SCENARIO_PATH)
    items = raw.get("scenarios", [])
    if not isinstance(items, list) or not items:
        raise ValueError("scenarios.json must contain a non-empty scenarios list")
    scenarios: list[Scenario] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        scenarios.append(_scenario_from_mapping(item))
    if not scenarios:
        raise ValueError("no usable scenarios found")
    return scenarios


def generate_synthetic_cases(
    session: Session,
    *,
    count: int,
    seed: int,
    start_index: int = 1,
    scenario_code: str | None = None,
    inject_error: bool = True,
    use_openai: bool = True,
    error_category: str | None = None,
) -> list[GeneratedCaseResult]:
    if count < 1:
        raise ValueError("count must be a positive integer")
    if start_index < 1:
        raise ValueError("start_index must be a positive integer")
    scenarios = load_scenarios()
    selected = scenarios[0]
    if scenario_code is not None:
        matched = [item for item in scenarios if item.code == scenario_code]
        if not matched:
            raise ValueError(f"unknown scenario {scenario_code!r}")
        selected = matched[0]
    results: list[GeneratedCaseResult] = []
    for offset in range(count):
        sequence = start_index + offset
        results.append(
            generate_one_case(
                session,
                sequence=sequence,
                seed=seed,
                scenario=selected,
                inject_error=inject_error,
                use_openai=use_openai,
                error_category=error_category,
            )
        )
    return results


def generate_one_case(
    session: Session,
    *,
    sequence: int,
    seed: int,
    scenario: Scenario,
    inject_error: bool = True,
    use_openai: bool = True,
    error_category: str | None = None,
    profile_code: str | None = None,
) -> GeneratedCaseResult:
    profile = resolve_profile(scenario, profile_code)
    case_id_code = format_case_id_code(sequence)
    if profile.code and profile.code != "default":
        case_seed = f"{seed}:{sequence}:{scenario.code}:{profile.code}"
    else:
        case_seed = f"{seed}:{sequence}:{scenario.code}"
    rng = random.Random(case_seed)
    existing = get_case_by_code(session, case_id_code)
    if existing is not None:
        frozen = get_frozen_case_for_clinical_id(session, existing.id)
        if frozen is not None and frozen.immutable:
            raise FrozenValidationCaseError(
                frozen.validation_case_id,
                f"underlying case {case_id_code} is frozen",
            )
        delete_case_graph(session, existing)
    else:
        delete_generation_artifacts_for_case_code(session, case_id_code)
    preferred_error = resolve_requested_category(
        inject_error=inject_error,
        error_category=error_category,
        scenario_target=scenario.target_error_category,
    )
    diagnosis = _require_diagnosis(session, scenario)
    symptoms = _select_symptoms(session, profile.symptom_queries or scenario.symptom_queries)
    medications = _select_medications(
        session,
        scenario,
        rng,
        profile=profile,
        force_warfarin=inject_error and preferred_error == F2_MONITORING,
    )
    stop_queries = (
        list(profile.stop_medication_queries)
        if profile.code != "default"
        else (profile.stop_medication_queries or scenario.stop_medication_queries)
    )
    stop_medications = _select_named_medications(
        session, stop_queries, {item.rxcui for item in medications}
    )
    if inject_error and preferred_error == F1_COMMISSION and not stop_medications:
        raise ReferenceResolutionError(
            "stop_medication",
            ",".join(stop_queries or scenario.stop_medication_queries) or preferred_error,
            "f1_commission requires a source-backed discontinued home medication",
        )
    if profile.code != "default":
        hospital_only_queries = list(profile.hospital_only_medication_queries)
    elif inject_error and preferred_error == F2_HOSPITAL_ONLY:
        hospital_only_queries = list(scenario.hospital_only_medication_queries)
    else:
        hospital_only_queries = []
    hospital_only: list[RefMedication] = []
    if hospital_only_queries:
        hospital_only = _select_named_medications(
            session,
            hospital_only_queries,
            {item.rxcui for item in medications + stop_medications},
        )
    if inject_error and preferred_error == F2_HOSPITAL_ONLY and not hospital_only:
        raise ReferenceResolutionError(
            "hospital_only_medication",
            ",".join(hospital_only_queries) or preferred_error,
            "f2_hospital_only_continued requires a source-backed inpatient-only medication",
        )
    labs = _select_labs(session, profile.lab_queries or scenario.lab_queries)
    if inject_error and preferred_error == F2_MONITORING:
        _require_warfarin_and_inr(medications, labs)
    comorbidities = _select_comorbidities(
        session,
        profile=profile,
        medications=medications + stop_medications + hospital_only,
        medication_queries=(
            list(profile.medication_required_queries or scenario.medication_queries)
            + list(stop_queries)
            + list(hospital_only_queries)
        ),
        admission=diagnosis,
    )
    _assert_rules_allow(
        session,
        medications + stop_medications + hospital_only,
        diagnosis,
        labs,
        comorbidities,
    )
    hold_restart = None
    substitution_pair = None
    if inject_error and preferred_error == F2_HELD_RESTART:
        if not medications:
            raise CaseValidationError(
                "error_eligibility",
                "f2_held_med_no_restart_plan requires a home medication "
                "that can be held with a restart plan",
            )
        hold_query = profile.hold_medication_query or profile.target_medication_query
        if hold_query:
            hold_restart = _pick_medication(medications, hold_query)
            if hold_restart is None:
                raise CaseValidationError(
                    "error_eligibility",
                    "f2_held_med_no_restart_plan requires the profile-defined hold medication",
                )
        else:
            hold_restart = medications[0]
        medications = [item for item in medications if item.rxcui != hold_restart.rxcui]
        if not medications:
            raise CaseValidationError(
                "error_eligibility",
                "f2_held_med_no_restart_plan requires at least one additional continued medication",
            )
    if inject_error and preferred_error in {F1_SUBSTITUTION, F2_INPATIENT_SUB}:
        substitution_pair = _select_substitution_pair(session, medications, labs)
        if substitution_pair is None:
            raise CaseValidationError(
                "error_eligibility",
                f"{preferred_error} requires a source-backed same-class substitute "
                "that is not already on the case; no substitute category will be used",
            )
    ids = _IdCounter(case_id_code)
    age = rng.randint(scenario.age_min, scenario.age_max)
    if _case_uses_standard_apixaban(medications) and age >= 80:
        age = 79
    sex = rng.choice(["Female", "Male"])
    hospital_day = rng.randint(2, 6)
    patient_name = f"SYN Patient {sequence:03d}"
    now = datetime.now(UTC)
    target_query = (
        profile.pending_decision_medication_query
        or profile.target_medication_query
        or (
            profile.hold_medication_query
            if preferred_error in {F2_HELD_RESTART, F2_PENDING_FOLLOWUP}
            else None
        )
    )
    target_pool = [
        item
        for item in medications
        + stop_medications
        + hospital_only
        + ([hold_restart] if hold_restart is not None else [])
        if item
    ]
    target_medication = None
    if target_query:
        target_medication = _pick_medication(target_pool, target_query)
        if target_medication is None:
            raise CaseValidationError(
                "error_eligibility",
                f"profile target medication {target_query!r} was not present on the case",
            )
    blueprint = CaseBlueprint(
        blueprint_id=ids.next_id("blueprint"),
        specialty=scenario.specialty,
        primary_diagnosis_ref_id=diagnosis.id,
        age_min=scenario.age_min,
        age_max=scenario.age_max,
        sex=None,
        hospital_day=hospital_day,
        difficulty="standard",
        target_home_med_count=len(medications) + len(stop_medications),
        target_problem_count=1 + len(comorbidities),
        clean_case=True,
        target_error_category=None if preferred_error == NONE else preferred_error,
        target_error_medication_class=None,
        settings={
            "scenario": scenario.code,
            "clinical_profile": profile.code,
            "seed": case_seed,
            "error_family": FAMILY_FOR_CATEGORY[preferred_error],
            "error_category": preferred_error,
            "rxcuis": [item.rxcui for item in medications],
            "stop_rxcuis": [item.rxcui for item in stop_medications],
            "hospital_only_rxcuis": [item.rxcui for item in hospital_only],
            "icd10cm": diagnosis.icd10cm_code,
            "loinc_codes": [item.loinc_code for item in labs],
            "generation_strategy": scenario.generation_strategy,
            "seed_archetype_id": scenario.code,
            "seed_archetype_name": scenario.seed_archetype_name,
            "seed_source_type": scenario.seed_source_type,
            "seed_source_filename": scenario.seed_source_filename,
            "blueprint_version": scenario.blueprint_version,
            "target_medication_query": target_query,
            "target_medication_rxcui": (
                None if target_medication is None else target_medication.rxcui
            ),
            "hold_medication_query": profile.hold_medication_query,
            "hold_reason": profile.hold_reason,
        },
    )
    session.add(blueprint)
    session.flush()
    display_diagnosis = diagnosis.preferred_name or diagnosis.icd10cm_code or "source diagnosis"
    symptom_names = [item.preferred_name or "symptom" for item in symptoms]
    home_meds, started_meds = _partition_temporal(medications, profile)
    med_names = [_med_label(item) for item in home_meds]
    started_names = [_med_label(item) for item in started_meds]
    stopped_names = [_med_label(item) for item in stop_medications]
    hospital_names = [_med_label(item) for item in hospital_only]
    hold_name = _med_label(hold_restart) if hold_restart is not None else None
    context_note = " ".join(
        part for part in (profile.admission_reason, profile.context_note) if part and part.strip()
    )
    template = _template_narrative(
        age,
        sex,
        display_diagnosis,
        symptom_names,
        med_names,
        stopped_names,
        duration=profile.symptom_duration,
        course=profile.symptom_course,
        hospital_course=_hospital_course_text(profile.hospital_course_pattern),
        context_note=context_note,
        hold_name=hold_name,
        hold_reason=profile.hold_reason,
        started=started_names,
        hospital_only_names=hospital_names,
    )
    narrative, narrative_source = _maybe_openai_narrative(
        template,
        age=age,
        sex=sex,
        diagnosis=display_diagnosis,
        symptoms=symptom_names,
        medications=med_names
        + started_names
        + stopped_names
        + hospital_names
        + ([hold_name] if hold_name else []),
        use_openai=use_openai,
        allowed_names=set(
            symptom_names
            + med_names
            + started_names
            + hospital_names
            + stopped_names
            + ([hold_name] if hold_name else [])
            + [display_diagnosis]
            + [item.preferred_name or "" for item in comorbidities]
        ),
        allowed_codes=_allowed_codes(diagnosis, medications + stop_medications, labs),
    )
    case = ClinicalCase(
        case_id_code=case_id_code,
        title=f"{scenario.specialty} inpatient case {case_id_code}",
        case_status="validated_clean",
        clean_case=True,
        generation_source=GENERATOR_NAME,
        one_liner=f"{age}-year-old {sex} with {display_diagnosis}",
        admission_dx=display_diagnosis,
        disposition_status=profile.disposition,
        chief_complaint=narrative.chief_complaint,
        patient_name=patient_name,
        patient_age=age,
        patient_gender=sex,
        ethnicity=None,
        specialty=scenario.specialty,
        difficulty="standard",
        is_active=True,
        source_type="synthetic",
        source_file=None,
    )
    session.add(case)
    session.flush()
    session.add(
        CasePresentation(
            case_id=case.id,
            chief_complaint=narrative.chief_complaint,
            hpi=narrative.hpi,
            review_of_systems=None,
            symptom_duration=profile.symptom_duration,
            symptom_course=profile.symptom_course,
        )
    )
    for symptom in symptoms:
        session.add(
            CaseSymptom(
                case_id=case.id,
                symptom_id=ids.next_id("symptom"),
                ref_symptom_id=symptom.id,
                symptom=symptom.preferred_name,
                duration=profile.symptom_duration,
                severity=profile.symptom_severity,
                course=profile.symptom_course,
                status="present",
                notes=None,
            )
        )
    session.add(
        CaseSocialSupport(
            case_id=case.id,
            living_situation="Baseline living situation: lives at home",
            caregiver_support=None,
            health_care_proxy=None,
            supervision_requirement=None,
            transportation=None,
            financial_barriers=None,
            health_literacy=None,
            language_preference="English",
            substance_use=None,
            advance_directive=None,
        )
    )
    session.add(
        CaseDiagnosis(
            case_id=case.id,
            diagnosis_id=ids.next_id("diagnosis"),
            ref_diagnosis_id=diagnosis.id,
            diagnosis=display_diagnosis,
            diagnosis_type="admission",
            status="active",
            context="inpatient",
            source_type="reference",
            source_reference=diagnosis.icd10cm_code,
        )
    )
    for extra in comorbidities:
        extra_name = extra.preferred_name or extra.icd10cm_code or "comorbid diagnosis"
        session.add(
            CaseDiagnosis(
                case_id=case.id,
                diagnosis_id=ids.next_id("diagnosis"),
                ref_diagnosis_id=extra.id,
                diagnosis=extra_name,
                diagnosis_type="past_history",
                status="active",
                context="history",
                source_type="reference",
                source_reference=extra.icd10cm_code,
            )
        )
        session.add(
            CaseProblemList(
                case_id=case.id,
                problem_id=ids.next_id("problem"),
                problem=extra_name,
                problem_type="diagnosis",
                priority="medium",
                status="active",
                assessment=extra_name,
                plan="Accounted for in the medication plan.",
            )
        )
    session.add(
        CaseProblemList(
            case_id=case.id,
            problem_id=ids.next_id("problem"),
            problem=display_diagnosis,
            problem_type="diagnosis",
            priority="high",
            status="active",
            assessment=display_diagnosis,
            plan="Continue inpatient management of the listed problem.",
        )
    )
    session.add(
        CaseNote(
            case_id=case.id,
            note_id=ids.next_id("note"),
            note_type="admission",
            note_text=narrative.note_text,
            source_type=narrative_source,
        )
    )
    session.add(
        CaseNote(
            case_id=case.id,
            note_id=ids.next_id("note"),
            note_type="hospital_course",
            note_text=_hospital_course_text(profile.hospital_course_pattern),
            source_type="template",
        )
    )
    problems = [diagnosis, *comorbidities]
    vitals = _synthetic_vitals(rng, profile.vital_pattern)
    session.add(
        CaseVital(
            case_id=case.id,
            vital_id=ids.next_id("vital"),
            ref_vital_id=None,
            timepoint="admission",
            temp_c=vitals["temp_c"],
            bp_systolic=vitals["bp_systolic"],
            bp_diastolic=vitals["bp_diastolic"],
            heart_rate=vitals["heart_rate"],
            resp_rate=vitals["resp_rate"],
            spo2_percent=vitals["spo2_percent"],
            oxygen_support=vitals["oxygen_support"],
        )
    )
    if profile.include_discharge_status:
        discharge_vitals = _synthetic_vitals(rng, _discharge_vital_pattern(profile.vital_pattern))
        session.add(
            CaseVital(
                case_id=case.id,
                vital_id=ids.next_id("vital"),
                ref_vital_id=None,
                timepoint="discharge",
                temp_c=discharge_vitals["temp_c"],
                bp_systolic=discharge_vitals["bp_systolic"],
                bp_diastolic=discharge_vitals["bp_diastolic"],
                heart_rate=discharge_vitals["heart_rate"],
                resp_rate=discharge_vitals["resp_rate"],
                spo2_percent=discharge_vitals["spo2_percent"],
                oxygen_support=discharge_vitals["oxygen_support"],
            )
        )
    for lab in labs:
        unit = preferred_lab_unit(lab)
        session.add(
            CaseLab(
                case_id=case.id,
                lab_id=ids.next_id("lab"),
                ref_lab_id=lab.id,
                timepoint="admission",
                test_name=lab.long_common_name or lab.loinc_code,
                value=_synthetic_lab_value(
                    rng,
                    lab,
                    timepoint="admission",
                    lab_pattern=_lab_pattern_for(profile),
                ),
                value_text=None,
                unit=unit,
                status="final",
            )
        )
        if profile.include_discharge_status:
            session.add(
                CaseLab(
                    case_id=case.id,
                    lab_id=ids.next_id("lab"),
                    ref_lab_id=lab.id,
                    timepoint="discharge",
                    test_name=lab.long_common_name or lab.loinc_code,
                    value=_synthetic_lab_value(
                        rng,
                        lab,
                        timepoint="discharge",
                        lab_pattern=_lab_pattern_for(profile),
                    ),
                    value_text=None,
                    unit=unit,
                    status="final",
                )
            )
    admission_weight = rng.randint(65, 110)
    if _case_uses_standard_apixaban(medications) and admission_weight <= 60:
        admission_weight = 72
    session.add(
        CaseWeight(
            case_id=case.id,
            weight_id=ids.next_id("weight"),
            timepoint="admission",
            weight_kg=Decimal(str(admission_weight)),
            dry_weight_kg=None,
        )
    )
    if profile.io_enabled or profile.hospital_course_pattern.startswith("multi_day_diuresis"):
        session.add(
            CaseWeight(
                case_id=case.id,
                weight_id=ids.next_id("weight"),
                timepoint="discharge",
                weight_kg=Decimal(str(max(50, admission_weight - rng.randint(2, 6)))),
                dry_weight_kg=Decimal(str(max(48, admission_weight - rng.randint(4, 8)))),
            )
        )
        intake, output = _io_volumes(rng, profile.io_net_direction)
        session.add(
            CaseIntakeOutput(
                case_id=case.id,
                io_id=ids.next_id("io"),
                timepoint=profile.io_timepoint,
                intake_ml=intake,
                output_ml=output,
                net_ml=intake - output,
                notes=None,
            )
        )
    _add_investigations(session, case, ids, profile)
    supply_days = CLEAN_SUPPLY_DAYS if preferred_error == F2_SUPPLY else None
    followup_item, followup_service, followup_timing = _followup_fields(profile, preferred_error)
    continued_for_sub = medications
    if substitution_pair is not None and preferred_error == F2_INPATIENT_SUB:
        continued_for_sub = [
            item for item in medications if item.rxcui != substitution_pair[0].rxcui
        ]
    for medication in continued_for_sub:
        _add_continued_medication(
            session,
            case=case,
            ids=ids,
            medication=medication,
            indication=_indication_for(session, medication, problems),
            frequency=scenario.default_frequency,
            quantity_or_days=None if supply_days is None else f"{supply_days} days",
            verification_source=profile.bpmh_source,
            temporal_overrides=profile.medication_temporal_roles,
        )
    if hold_restart is not None:
        _add_held_restart_medication(
            session,
            case=case,
            ids=ids,
            medication=hold_restart,
            indication=_indication_for(session, hold_restart, problems),
            frequency=scenario.default_frequency,
            held_reason=profile.hold_reason,
            restart_plan=profile.restart_plan,
            verification_source=profile.bpmh_source,
        )
    if substitution_pair is not None and preferred_error == F2_INPATIENT_SUB:
        _add_inpatient_substitution(
            session,
            case=case,
            ids=ids,
            home_medication=substitution_pair[0],
            substitute=substitution_pair[1],
            class_id=substitution_pair[2],
            class_name=substitution_pair[3],
            indication=_indication_for(session, substitution_pair[0], problems),
            frequency=scenario.default_frequency,
        )
    for medication in stop_medications:
        _add_stopped_medication(
            session,
            case=case,
            ids=ids,
            medication=medication,
            indication=_indication_for(session, medication, problems),
            frequency=scenario.default_frequency,
            verification_source=profile.bpmh_source,
        )
    for medication in hospital_only:
        _add_hospital_only_medication(
            session,
            case=case,
            ids=ids,
            medication=medication,
            indication=_indication_for(session, medication, problems),
            frequency=scenario.default_frequency,
        )
    session.add(
        CaseMedicationReconciliation(
            case_id=case.id,
            medrec_id=ids.next_id("medrec"),
            reconciliation_context="discharge",
            medrec_status="complete",
            patient_able_to_participate=profile.patient_able_to_participate,
            bpmh_source=profile.bpmh_source,
            bpmh_interviewer=None,
            bpmh_date=None,
            discrepancies_found=False,
            resolved=True,
            discrepancy_types=[],
            pharmacist_review=True,
            high_alert_meds_identified=[],
            notes=profile.medrec_notes or None,
        )
    )
    _maybe_add_warfarin_monitoring(session, case, ids, medications, labs)
    if profile.monitoring_parameter:
        session.add(
            CaseMonitoring(
                case_id=case.id,
                monitoring_id=ids.next_id("monitoring"),
                parameter=profile.monitoring_parameter,
                frequency=profile.monitoring_frequency or "weekly",
                target=None,
                trigger_for_action=None,
                duration=None,
                responsible_service=profile.monitoring_service or followup_service,
            )
        )
    session.add(
        CaseDischargePlanning(
            case_id=case.id,
            disposition=profile.disposition,
            disposition_detail=None,
            discharge_readiness="ready",
            anticipated_discharge_date=None,
            transportation_needed=False,
            home_health_ordered=profile.home_health_ordered,
            barriers_to_discharge=[],
            dme_needed=[],
        )
    )
    session.add(
        CaseFollowup(
            case_id=case.id,
            followup_id=ids.next_id("followup"),
            item=followup_item,
            timing=followup_timing,
            with_service=followup_service,
            status="planned",
        )
    )
    session.add(
        CaseInstruction(
            case_id=case.id,
            instruction_id=ids.next_id("instruction"),
            category="medications",
            instruction_text="Take discharge medications exactly as listed.",
            source_type="synthetic",
        )
    )
    if preferred_error == F2_PENDING_FOLLOWUP:
        pending_query = (
            profile.pending_decision_medication_query or profile.target_medication_query
        )
        pending_med = _pick_medication(target_pool, pending_query) if pending_query else None
        pending_name = _med_label(pending_med) if pending_med is not None else display_diagnosis
        pending_text = profile.pending_decision_text or (
            f"A pending therapeutic decision remains: duration of {pending_name} "
            "will be confirmed at the scheduled follow-up."
        )
        if "pending therapeutic decision" not in pending_text.casefold():
            pending_text = "A pending therapeutic decision remains. " + pending_text
        session.add(
            CaseInstruction(
                case_id=case.id,
                instruction_id=ids.next_id("instruction"),
                category="followup",
                instruction_text=pending_text,
                source_type="synthetic",
            )
        )
    if symptoms:
        session.add(
            CaseReturnPrecaution(
                case_id=case.id,
                precaution_id=ids.next_id("precaution"),
                symptom=symptoms[0].preferred_name,
                reason="Worsening of the presenting symptom",
                action="Seek urgent evaluation",
                severity="urgent",
                patient_instruction=None,
            )
        )
    session.flush()
    fingerprint = fingerprint_from_case(
        session,
        case,
        scenario_code=scenario.code,
        profile_code=profile.code,
        hospital_course_pattern=profile.hospital_course_pattern,
    )
    clean_state = _case_state_snapshot(session, case)
    clean_state["diversity"] = {
        "scenario": scenario.code,
        "clinical_profile": profile.code,
        "hospital_course_pattern": profile.hospital_course_pattern,
        "generation_strategy": scenario.generation_strategy,
        "seed_archetype_id": (
            scenario.code if scenario.generation_strategy == "resident_seed_guided" else None
        ),
        "seed_archetype_name": scenario.seed_archetype_name,
        "seed_source_type": scenario.seed_source_type,
        "seed_source_filename": scenario.seed_source_filename,
        "blueprint_version": scenario.blueprint_version,
        "fingerprint": fingerprint_as_dict(fingerprint),
    }
    clean_report = validate_case(session, case, expect_injected_error=False, expected_category=NONE)
    require_valid(clean_report)
    injected: InjectionResult | None = None
    if inject_error:
        require_eligible(session, case, preferred_error)
        injected = inject_reconciliation_error(
            session,
            case,
            rng=rng,
            seed=case_seed,
            preferred_category=preferred_error,
            target_rxcui=None if target_medication is None else target_medication.rxcui,
        )
        if injected.category != preferred_error:
            raise CaseValidationError(
                "error_injection",
                f"injected category {injected.category!r} != requested {preferred_error!r}",
            )
        rec = session.scalar(
            select(CaseMedicationReconciliation).where(
                CaseMedicationReconciliation.case_id == case.id
            )
        )
        if rec is not None:
            rec.discrepancies_found = True
            rec.resolved = False
            rec.medrec_status = "error_injected"
            rec.discrepancy_types = [injected.category]
        session.flush()
    final_report = validate_case(
        session,
        case,
        expect_injected_error=inject_error,
        expected_category=preferred_error,
    )
    require_valid(final_report)
    run = CaseGenerationRun(
        run_id=ids.next_id("run"),
        blueprint_id=blueprint.id,
        case_id=case.id,
        model_name=None if narrative_source == "template" else "openai",
        prompt_version="narrative-v1" if narrative_source == "openai" else "template-v1",
        started_at=now,
        completed_at=datetime.now(UTC),
        status="completed",
        validation_status="passed",
        error_message=None,
        token_usage=None,
        metadata_json={
            "random_seed": case_seed,
            "batch_seed": seed,
            "generator_version": __version__,
            "generator_name": GENERATOR_NAME,
            "scenario": scenario.code,
            "clinical_profile": profile.code,
            "reference_versions": _reference_versions(session),
            "rules_applied": [rule.rule_code for rule in list_enabled_rules(session)],
            "numeric_value_origin": NUMERIC_ORIGIN,
            "narrative_source": narrative_source,
            "clean_validation": serialize_report(clean_report),
            "final_validation": serialize_report(final_report),
            "error_injection": None
            if injected is None
            else {
                "family": injected.family,
                "category": injected.category,
                "rxcui": injected.rxcui,
                "drug": injected.drug,
                "seed": injected.seed,
                "changed_field": injected.changed_field,
            },
        },
    )
    session.add(run)
    session.flush()
    return GeneratedCaseResult(
        case_id_code=case_id_code,
        case_id=case.id,
        seed=case_seed,
        clean_passed=clean_report.passed,
        injected=injected,
        validation=serialize_report(final_report),
        narrative_source=narrative_source,
        clean_state=clean_state,
        clean_validation=serialize_report(clean_report),
        clinical_profile=profile.code,
        hospital_course_pattern=profile.hospital_course_pattern,
        fingerprint=fingerprint,
    )


def validate_persisted_cases(
    session: Session,
    *,
    case_id_code: str | None = None,
) -> list[dict[str, Any]]:
    from app.repositories.cases import list_cases

    cases = list_cases(session)
    if case_id_code is not None:
        cases = [item for item in cases if item.case_id_code == case_id_code]
        if not cases:
            raise CaseValidationError("case", f"case {case_id_code} was not found")
    reports: list[dict[str, Any]] = []
    for case in cases:
        expect_error = case.clean_case is False
        expected_category = NONE
        if expect_error:
            keys = list_answer_keys_for_case(session, case.id)
            if keys:
                expected_category = canonicalize_category(keys[0].error_category)
        report = validate_case(
            session,
            case,
            expect_injected_error=expect_error,
            expected_category=expected_category,
        )
        payload = serialize_report(report)
        reports.append(payload)
        if not report.passed:
            raise CaseValidationError("case", payload["errors"][0], payload["errors"])
    return reports


def _select_stop_medications(
    session: Session, scenario: Scenario, seen: set[str]
) -> list[RefMedication]:
    selected: list[RefMedication] = []
    used = set(seen)
    for query in scenario.stop_medication_queries:
        row = match_medication(session, query)
        if row is None or row.rxcui in used:
            continue
        used.add(row.rxcui)
        selected.append(row)
    selected.sort(key=lambda item: item.rxcui)
    return selected


def _add_continued_medication(
    session: Session,
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    medication: RefMedication,
    indication: str,
    frequency: str,
    quantity_or_days: str | None = None,
    verification_source: str = "patient_and_prior_records",
    temporal_overrides: dict[str, str] | None = None,
) -> None:
    label = _med_label(medication)
    admin = administration_for(
        medication,
        fallback_frequency=frequency,
        overrides=temporal_overrides,
    )
    dose = admin.dose
    route = admin.route
    frequency = admin.frequency
    if admin.temporal_role == "started_inpatient":
        _add_started_inpatient_medication(
            session,
            case=case,
            ids=ids,
            medication=medication,
            label=label,
            indication=indication,
            dose=dose,
            route=route,
            frequency=frequency,
            notes=_started_inpatient_note(admin.chart_note),
            quantity_or_days=quantity_or_days,
        )
        return
    for context, status in (
        ("home", "home"),
        ("inpatient", "active"),
        ("discharge", "discharge"),
    ):
        session.add(
            _medication_row(
                case=case,
                ids=ids,
                medication=medication,
                label=label,
                context=context,
                status=status,
                dose=dose,
                route=route,
                frequency=frequency,
                indication=indication,
                held_reason=None,
                quantity_or_days=quantity_or_days if context == "discharge" else None,
                verification_source=verification_source,
                notes=admin.chart_note,
            )
        )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=medication.id,
            drug=label,
            home_state="continue",
            inpatient_state="continue",
            correct_discharge_state="continue",
            decision="continue",
            decision_reason="Home therapy is continued through discharge in the clean case.",
            is_error_target=False,
        )
    )


def _add_stopped_medication(
    session: Session,
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    medication: RefMedication,
    indication: str,
    frequency: str,
    verification_source: str = "patient_and_prior_records",
) -> None:
    label = _med_label(medication)
    admin = administration_for(medication, fallback_frequency=frequency)
    dose = admin.dose
    route = admin.route
    frequency = admin.frequency
    held_reason = "Held on admission; not continued at discharge."
    for context, status in (("home", "held"), ("inpatient", "held")):
        session.add(
            _medication_row(
                case=case,
                ids=ids,
                medication=medication,
                label=label,
                context=context,
                status=status,
                dose=dose,
                route=route,
                frequency=frequency,
                indication=indication,
                held_reason=held_reason,
                verification_source=verification_source,
            )
        )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=medication.id,
            drug=label,
            home_state="held",
            inpatient_state="held",
            correct_discharge_state="stop",
            decision="stop",
            decision_reason="Home medication is discontinued and is not continued at discharge.",
            is_error_target=False,
        )
    )
    session.add(
        CaseInstruction(
            case_id=case.id,
            instruction_id=ids.next_id("instruction"),
            category="medications",
            instruction_text=(
                f"Do not restart at discharge: {label} was discontinued and has no outpatient role."
            ),
            source_type="synthetic",
        )
    )


def _add_held_restart_medication(
    session: Session,
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    medication: RefMedication,
    indication: str,
    frequency: str,
    held_reason: str | None = None,
    restart_plan: str | None = None,
    verification_source: str = "patient_and_prior_records",
) -> None:
    label = _med_label(medication)
    admin = administration_for(medication, fallback_frequency=frequency)
    dose = admin.dose
    route = admin.route
    frequency = admin.frequency
    reason = held_reason or (
        "Held inpatient for documented in-hospital hypotension; intended to restart."
    )
    restart = restart_plan or (
        "Resume when systolic blood pressure remains above 100 mmHg for 24 hours."
    )
    session.add(
        _medication_row(
            case=case,
            ids=ids,
            medication=medication,
            label=label,
            context="home",
            status="home",
            dose=dose,
            route=route,
            frequency=frequency,
            indication=indication,
            held_reason=None,
            verification_source=verification_source,
        )
    )
    for context, status in (("inpatient", "held"), ("discharge", "held")):
        session.add(
            _medication_row(
                case=case,
                ids=ids,
                medication=medication,
                label=label,
                context=context,
                status=status,
                dose=dose,
                route=route,
                frequency=frequency,
                indication=indication,
                held_reason=reason,
                target_or_goal=restart,
                verification_source=verification_source,
            )
        )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=medication.id,
            drug=label,
            home_state="continue",
            inpatient_state="held",
            correct_discharge_state="restart",
            decision="restart",
            decision_reason="Home medication is held inpatient and has a documented restart plan.",
            is_error_target=False,
        )
    )
    session.add(
        CaseInstruction(
            case_id=case.id,
            instruction_id=ids.next_id("instruction"),
            category="medications",
            instruction_text=f"Resume when holding {label}: {restart}",
            source_type="synthetic",
        )
    )


def _add_hospital_only_medication(
    session: Session,
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    medication: RefMedication,
    indication: str,
    frequency: str,
) -> None:
    label = _med_label(medication)
    admin = administration_for(medication, fallback_frequency=frequency)
    dose = admin.dose
    route = admin.route
    frequency = admin.frequency
    reason = (
        f"Started in hospital for an inpatient-only indication; stop at discharge. "
        f"No outpatient continuation of {label}."
    )
    session.add(
        _medication_row(
            case=case,
            ids=ids,
            medication=medication,
            label=label,
            context="inpatient",
            status="active",
            dose=dose,
            route=route,
            frequency=frequency,
            indication=reason,
            held_reason=None,
            notes=admin.chart_note,
        )
    )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=medication.id,
            drug=label,
            home_state="absent",
            inpatient_state="new_start",
            correct_discharge_state="stop",
            decision="stop",
            decision_reason=reason,
            is_error_target=False,
        )
    )


def _add_inpatient_substitution(
    session: Session,
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    home_medication: RefMedication,
    substitute: RefMedication,
    class_id: str,
    class_name: str,
    indication: str,
    frequency: str,
) -> None:
    home_label = _med_label(home_medication)
    sub_label = _med_label(substitute)
    home_admin = administration_for(home_medication, fallback_frequency=frequency)
    sub_admin = administration_for(substitute, fallback_frequency=frequency)
    home_dose = home_admin.dose
    sub_dose = sub_admin.dose
    home_route = home_admin.route
    sub_route = sub_admin.route
    frequency = home_admin.frequency
    sub_frequency = sub_admin.frequency
    sub_indication = (
        f"Formulary substitution for {home_label} during admission "
        f"(RxClass {class_id} {class_name})."
    )
    session.add(
        _medication_row(
            case=case,
            ids=ids,
            medication=home_medication,
            label=home_label,
            context="home",
            status="home",
            dose=home_dose,
            route=home_route,
            frequency=frequency,
            indication=indication,
            held_reason=None,
            notes=home_admin.chart_note,
        )
    )
    session.add(
        _medication_row(
            case=case,
            ids=ids,
            medication=substitute,
            label=sub_label,
            context="inpatient",
            status="active",
            dose=sub_dose,
            route=sub_route,
            frequency=sub_frequency,
            indication=sub_indication,
            held_reason=None,
            notes=sub_admin.chart_note,
        )
    )
    session.add(
        _medication_row(
            case=case,
            ids=ids,
            medication=home_medication,
            label=home_label,
            context="discharge",
            status="discharge",
            dose=home_dose,
            route=home_route,
            frequency=frequency,
            indication=indication,
            held_reason=None,
            notes=home_admin.chart_note,
        )
    )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=home_medication.id,
            drug=home_label,
            home_state="continue",
            inpatient_state="held",
            correct_discharge_state="continue",
            decision="continue",
            decision_reason="Resume home therapy after the inpatient formulary substitute.",
            is_error_target=False,
        )
    )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=substitute.id,
            drug=sub_label,
            home_state="absent",
            inpatient_state="new_start",
            correct_discharge_state="stop",
            decision="stop",
            decision_reason=sub_indication,
            is_error_target=False,
        )
    )
    session.add(
        CaseInstruction(
            case_id=case.id,
            instruction_id=ids.next_id("instruction"),
            category="medications",
            instruction_text=(
                f"Resume home therapy {home_label}. Inpatient {sub_label} was a "
                f"formulary substitution for {home_label} only."
            ),
            source_type="synthetic",
        )
    )


def _medication_row(
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    medication: RefMedication,
    label: str,
    context: str,
    status: str,
    dose: str,
    route: str | None,
    frequency: str,
    indication: str,
    held_reason: str | None,
    quantity_or_days: str | None = None,
    target_or_goal: str | None = None,
    monitoring: str | None = None,
    verification_source: str = "patient_and_prior_records",
    notes: str | None = None,
) -> CaseMedication:
    return CaseMedication(
        case_id=case.id,
        medication_id=ids.next_id("medication"),
        ref_medication_id=medication.id,
        context=context,
        drug=label,
        reported_name=label,
        dose=dose,
        route=route,
        frequency=frequency,
        indication=indication,
        status=status,
        held_reason=held_reason,
        verification_status="verified",
        verification_source=verification_source,
        target_or_goal=target_or_goal,
        monitoring=monitoring,
        quantity_or_days=quantity_or_days,
        refills=None,
        source_type="reference",
        source_file=None,
        source_reference=f"RXCUI:{medication.rxcui}",
        notes=notes,
    )


def _lab_pattern_for(profile: ClinicalProfile) -> str:
    course = profile.hospital_course_pattern.casefold()
    vital = profile.vital_pattern.casefold()
    code = (profile.code or "").casefold()
    reason = (profile.admission_reason or "").casefold()
    if "aki" in course:
        return "aki"
    if (
        "gi_bleed" in course
        or "gi_bleed" in code
        or "postop_hemoglobin" in course
        or "postop_anticoag" in course
        or "endoscopy" in course
        or "hemorrhage" in reason
        or "bleeding" in reason
        or "bleed" in reason
    ):
        return "bleed"
    if "glycemic" in course or vital == "glycemic":
        return "glycemic"
    if "diuresis" in course:
        return "hf"
    return "standard"


def _synthetic_lab_value(
    rng: random.Random,
    lab: RefLabTest,
    *,
    timepoint: str = "admission",
    lab_pattern: str = "standard",
) -> float:
    spec = spec_for_lab(lab)
    unit = preferred_lab_unit(lab)
    if spec is None:
        return rng.randint(20, 80) / 10.0
    if spec.name == "inr":
        conventional = rng.randint(18, 32) / 10.0
        if timepoint == "discharge":
            conventional = rng.randint(20, 30) / 10.0
    elif spec.name == "potassium":
        conventional = rng.randint(32, 48) / 10.0
        if timepoint == "discharge":
            conventional = rng.randint(36, 46) / 10.0
    elif spec.name == "creatinine":
        if lab_pattern == "aki":
            conventional = rng.randint(18, 28) / 10.0
            if timepoint == "discharge":
                conventional = rng.randint(12, 18) / 10.0
        elif lab_pattern == "hf":
            conventional = rng.randint(11, 18) / 10.0
            if timepoint == "discharge":
                conventional = rng.randint(9, 14) / 10.0
        else:
            conventional = rng.randint(8, 13) / 10.0
            if timepoint == "discharge":
                conventional = rng.randint(8, 12) / 10.0
    elif spec.name == "sodium":
        conventional = float(rng.randint(132, 144))
    elif spec.name == "glucose":
        if lab_pattern == "glycemic":
            conventional = float(
                rng.randint(240, 380) if timepoint == "admission" else rng.randint(110, 160)
            )
        else:
            conventional = float(
                rng.randint(110, 180) if timepoint == "admission" else rng.randint(100, 140)
            )
    elif spec.name == "hemoglobin":
        if lab_pattern == "bleed":
            if timepoint == "admission":
                conventional = rng.randint(72, 95) / 10.0
            else:
                conventional = rng.randint(88, 112) / 10.0
        else:
            if timepoint == "admission":
                conventional = rng.randint(115, 140) / 10.0
            else:
                conventional = rng.randint(118, 145) / 10.0
    elif spec.name == "natriuretic peptide":
        if timepoint == "admission":
            conventional = float(rng.randint(400, 1400))
        else:
            conventional = float(rng.randint(180, 700))
    else:
        low = int(spec.conventional_low * 10)
        high = int(spec.conventional_high * 10)
        conventional = rng.randint(low, high) / 10.0
    return convert_conventional(spec, conventional, unit)


def _case_state_snapshot(session: Session, case: ClinicalCase) -> dict[str, Any]:
    medications = []
    for medication in list_medications_for_case(session, case.id):
        rxcui = None
        if medication.ref_medication_id is not None:
            med_row = session.get(RefMedication, medication.ref_medication_id)
            rxcui = med_row.rxcui if med_row is not None else None
        medications.append(
            {
                "medication_id": medication.medication_id,
                "context": medication.context,
                "drug": medication.drug,
                "dose": medication.dose,
                "route": medication.route,
                "frequency": medication.frequency,
                "status": medication.status,
                "quantity_or_days": medication.quantity_or_days,
                "monitoring": medication.monitoring,
                "held_reason": medication.held_reason,
                "rxcui": rxcui,
            }
        )
    plans = [
        {
            "plan_id": plan.plan_id,
            "drug": plan.drug,
            "decision": plan.decision,
            "correct_discharge_state": plan.correct_discharge_state,
            "is_error_target": plan.is_error_target,
        }
        for plan in list_plans_for_case(session, case.id)
    ]
    diagnoses = []
    for diagnosis in list_diagnoses_for_case(session, case.id):
        code = None
        if diagnosis.ref_diagnosis_id is not None:
            dx_row = session.get(RefDiagnosis, diagnosis.ref_diagnosis_id)
            code = dx_row.icd10cm_code if dx_row is not None else None
        diagnoses.append({"diagnosis": diagnosis.diagnosis, "icd10cm_code": code})
    labs = []
    for lab in list_labs_for_case(session, case.id):
        code = None
        if lab.ref_lab_id is not None:
            lab_row = session.get(RefLabTest, lab.ref_lab_id)
            code = lab_row.loinc_code if lab_row is not None else None
        labs.append(
            {
                "test_name": lab.test_name,
                "value": lab.value,
                "unit": lab.unit,
                "loinc_code": code,
            }
        )
    return {
        "case_id_code": case.case_id_code,
        "clean_case": case.clean_case,
        "medications": medications,
        "plans": plans,
        "diagnoses": diagnoses,
        "labs": labs,
    }


def _require_diagnosis(session: Session, scenario: Scenario) -> RefDiagnosis:
    for query in scenario.diagnosis_queries:
        row = match_diagnosis(session, query)
        if row is not None:
            return row
    raise ReferenceResolutionError("diagnosis", ",".join(scenario.diagnosis_queries))


def _select_symptoms(session: Session, queries: list[str]) -> list[RefSymptom]:
    found: list[RefSymptom] = []
    seen: set[UUID] = set()
    missing: list[str] = []
    for query in queries:
        rows, _ = search_symptoms(session, query, limit=20, offset=0)
        ranked = sorted(
            (
                item
                for item in rows
                if is_symptom_level_concept(item.preferred_name, query)
                or any(
                    is_symptom_level_concept(str(synonym), query)
                    for synonym in (item.synonyms or [])
                )
            ),
            key=lambda item: (
                0 if (item.preferred_name or "").casefold() == query.casefold() else 1,
                item.preferred_name or "",
                str(item.id),
            ),
        )
        if ranked:
            pick = ranked[0]
            if pick.id not in seen:
                seen.add(pick.id)
                found.append(pick)
        else:
            missing.append(query)
    if missing and not found:
        raise ReferenceResolutionError(
            "symptom",
            ",".join(missing),
            "no symptom-level concept matched the requested queries",
        )
    if found:
        return found
    raise ReferenceResolutionError(
        "symptom",
        ",".join(queries),
        "no symptom-level concept matched the requested queries",
    )


def _select_medications(
    session: Session,
    scenario: Scenario,
    rng: random.Random,
    *,
    profile: ClinicalProfile | None = None,
    force_warfarin: bool = False,
) -> list[RefMedication]:
    selected: list[RefMedication] = []
    seen: set[str] = set()
    required = (
        profile.medication_required_queries
        if profile and profile.medication_required_queries
        else scenario.medication_queries
    )
    optional = []
    if profile is not None:
        optional = list(profile.optional_include) + list(profile.medication_optional_queries)
    for query in list(required) + optional:
        row = match_medication(session, query)
        if row is None or row.rxcui in seen:
            continue
        seen.add(row.rxcui)
        selected.append(row)
    mutex: list[RefMedication] = []
    for query in scenario.anticoagulant_mutex_queries:
        row = match_medication(session, query)
        if row is not None and row.rxcui not in seen:
            mutex.append(row)
    wanted: str | None = None
    if force_warfarin:
        wanted = "warfarin"
    elif profile is not None and profile.anticoagulant:
        wanted = profile.anticoagulant
    if mutex:
        mutex.sort(key=lambda item: item.rxcui)
        chosen: RefMedication | None
        if wanted:
            chosen = next(
                (
                    item
                    for item in mutex
                    if _contains(item.concept_name, wanted)
                    or _contains(item.ingredient, wanted)
                    or _contains(item.generic_name, wanted)
                ),
                None,
            )
            if chosen is None and wanted == "warfarin":
                raise ReferenceResolutionError(
                    "medication",
                    "warfarin",
                    "f2_monitoring_not_arranged requires a source-backed warfarin row",
                )
        elif (
            profile is None
            or profile.code == "default"
            or not profile.medication_required_queries
        ):
            chosen = rng.choice(mutex)
        else:
            chosen = None
        if chosen is not None:
            selected.append(chosen)
            seen.add(chosen.rxcui)
    if not selected:
        raise ReferenceResolutionError(
            "medication",
            ",".join(required or scenario.medication_queries),
        )
    selected.sort(key=lambda item: item.rxcui)
    return selected


def _select_named_medications(
    session: Session, queries: list[str], seen: set[str]
) -> list[RefMedication]:
    selected: list[RefMedication] = []
    used = set(seen)
    missing: list[str] = []
    for query in queries:
        row = match_medication(session, query)
        if row is None:
            missing.append(query)
            continue
        if row.rxcui in used:
            continue
        used.add(row.rxcui)
        selected.append(row)
    if missing:
        raise ReferenceResolutionError(
            "medication",
            ",".join(missing),
            "named medication has no source-backed concept",
        )
    selected.sort(key=lambda item: item.rxcui)
    return selected


def _select_substitution_pair(
    session: Session,
    medications: list[RefMedication],
    labs: list[RefLabTest],
) -> tuple[RefMedication, RefMedication, str, str] | None:
    excluded = {item.rxcui for item in medications}
    loinc_codes = frozenset(item.loinc_code for item in labs)
    for source in sorted(medications, key=lambda item: item.rxcui):
        classes = list_medication_classes_for_rxcui(session, source.rxcui)
        for membership in classes:
            if not class_usable_for_substitution(
                class_type=membership.class_type,
                class_id=membership.class_id,
                class_name=membership.class_name,
            ):
                continue
            siblings = list_medications_sharing_class(
                session, membership.class_id, exclude_rxcui=source.rxcui
            )
            for sibling in sorted(siblings, key=lambda item: item.rxcui):
                if sibling.rxcui in excluded:
                    continue
                if regimen_for_medication(sibling) is None and not str(sibling.rxcui).startswith(
                    "TEST_"
                ):
                    continue
                snapshot = CaseSnapshot(
                    age=None,
                    sex=None,
                    care_context="inpatient",
                    icd10cm_codes=frozenset(),
                    rxcuis=frozenset(excluded | {sibling.rxcui}),
                    loinc_codes=loinc_codes,
                )
                if hard_violations(evaluate_rules(session, snapshot)):
                    continue
                return source, sibling, membership.class_id, membership.class_name
    return None


def _require_warfarin_and_inr(medications: list[RefMedication], labs: list[RefLabTest]) -> None:
    warfarin = next(
        (
            item
            for item in medications
            if _contains(item.concept_name, "warfarin")
            or _contains(item.ingredient, "warfarin")
            or _contains(item.generic_name, "warfarin")
        ),
        None,
    )
    inr = next(
        (
            item
            for item in labs
            if _contains(item.long_common_name, "inr")
            or _contains(item.component, "inr")
            or _contains(item.long_common_name, "international normalized")
        ),
        None,
    )
    if warfarin is None or inr is None:
        raise CaseValidationError(
            "error_eligibility",
            "f2_monitoring_not_arranged requires warfarin and a source-backed INR lab "
            "on the clean case; no substitute category will be used",
        )


def _select_labs(session: Session, queries: list[str]) -> list[RefLabTest]:
    found: list[RefLabTest] = []
    seen: set[str] = set()
    missing: list[str] = []
    for query in queries:
        row = match_lab(session, query)
        if row is None:
            missing.append(query)
            continue
        if row.loinc_code in seen:
            continue
        seen.add(row.loinc_code)
        found.append(row)
    if missing:
        raise ReferenceResolutionError("lab", ",".join(missing))
    found.sort(key=lambda item: item.loinc_code)
    return found


def _assert_rules_allow(
    session: Session,
    medications: list[RefMedication],
    diagnosis: RefDiagnosis,
    labs: list[RefLabTest],
    comorbidities: list[RefDiagnosis] | None = None,
) -> None:
    codes = {diagnosis.icd10cm_code} if diagnosis.icd10cm_code else set()
    for extra in comorbidities or []:
        if extra.icd10cm_code:
            codes.add(extra.icd10cm_code)
    snapshot = CaseSnapshot(
        age=None,
        sex=None,
        care_context="inpatient",
        icd10cm_codes=frozenset(code for code in codes if code),
        rxcuis=frozenset(item.rxcui for item in medications),
        loinc_codes=frozenset(item.loinc_code for item in labs),
    )
    hits = hard_violations(evaluate_rules(session, snapshot))
    if hits:
        raise CaseValidationError("clinical", hits[0].message, [item.message for item in hits])


def _maybe_add_warfarin_monitoring(
    session: Session,
    case: ClinicalCase,
    ids: _IdCounter,
    medications: list[RefMedication],
    labs: list[RefLabTest],
) -> None:
    _ = medications
    session.flush()
    warfarin_ref: RefMedication | None = None
    for row in list_medications_for_case(session, case.id):
        if row.ref_medication_id is None:
            continue
        med = session.get(RefMedication, row.ref_medication_id)
        if med is None:
            continue
        if (
            _contains(med.concept_name, "warfarin")
            or _contains(med.ingredient, "warfarin")
            or _contains(med.generic_name, "warfarin")
        ):
            warfarin_ref = med
            break
    inr = next(
        (
            item
            for item in labs
            if _contains(item.long_common_name, "inr")
            or _contains(item.component, "inr")
            or _contains(item.long_common_name, "international normalized")
        ),
        None,
    )
    if warfarin_ref is None or inr is None:
        return
    active_discharge = any(
        row.ref_medication_id == warfarin_ref.id
        and row.context == "discharge"
        and row.status != "held"
        for row in list_medications_for_case(session, case.id)
    )
    if not active_discharge:
        return
    session.add(
        CaseMonitoring(
            case_id=case.id,
            monitoring_id=ids.next_id("monitoring"),
            parameter=inr.long_common_name or inr.loinc_code,
            frequency="within 7 days, then by the INR result",
            target=None,
            trigger_for_action="Repeat INR sooner if bleeding or a new interacting medicine occurs",
            duration=None,
            responsible_service="laboratory monitoring",
        )
    )
    for row in list_medications_for_case(session, case.id):
        if row.ref_medication_id != warfarin_ref.id or row.context != "discharge":
            continue
        row.monitoring = "INR laboratory monitoring is separate from the clinic appointment."


def _maybe_openai_narrative(
    template: CaseNarrative,
    *,
    age: int,
    sex: str,
    diagnosis: str,
    symptoms: list[str],
    medications: list[str],
    use_openai: bool,
    allowed_names: set[str],
    allowed_codes: set[str],
) -> tuple[CaseNarrative, str]:
    if not use_openai:
        return template, "template"
    narrative = assemble_narrative(
        {
            "age": age,
            "sex": sex,
            "diagnosis": diagnosis,
            "symptoms": symptoms,
            "medications": medications,
            "chief_complaint": template.chief_complaint,
        }
    )
    if narrative is None:
        return template, "template"
    if _narrative_rejected(narrative, allowed_names, allowed_codes):
        return template, "template"
    return narrative, "openai"


def _narrative_rejected(
    narrative: CaseNarrative, allowed_names: set[str], allowed_codes: set[str]
) -> bool:
    blob = " ".join([narrative.chief_complaint, narrative.hpi, narrative.note_text])
    lowered = blob.casefold()
    if not any(name.casefold() in lowered for name in allowed_names if name):
        return True
    for code in allowed_codes:
        if code.startswith("TEST_"):
            continue
        if len(code) >= 6 and code.isdigit() and code not in blob:
            continue
    return False


def _template_narrative(
    age: int,
    sex: str,
    diagnosis: str,
    symptoms: list[str],
    medications: list[str],
    held: list[str] | None = None,
    *,
    duration: str = "several days",
    course: str = "worsening",
    hospital_course: str = "",
    context_note: str = "",
    hold_name: str | None = None,
    hold_reason: str | None = None,
    started: list[str] | None = None,
    hospital_only_names: list[str] | None = None,
) -> CaseNarrative:
    symptom_text = ", ".join(symptoms) if symptoms else "reported symptoms"
    if medications:
        med_text = ", ".join(medications)
    else:
        med_text = "no chronic home medications were recorded"
    held_text = ", ".join(held) if held else ""
    held_sentence = (
        f" {held_text} was discontinued and is not intended at discharge." if held_text else ""
    )
    hold_sentence = ""
    if hold_name:
        reason = hold_reason or "a documented inpatient safety concern"
        hold_sentence = f" {hold_name} was held during the admission ({reason})."
    started_text = ", ".join(started or [])
    started_sentence = (
        f" Started during this admission: {started_text}." if started_text else ""
    )
    hospital_text = ", ".join(hospital_only_names or [])
    hospital_sentence = (
        f" Used only in the hospital and stopped at discharge: {hospital_text}."
        if hospital_text
        else ""
    )
    course_sentence = f" {hospital_course}" if hospital_course else ""
    context_sentence = f" {context_note}" if context_note.strip() else ""
    chief = f"{symptom_text} in the setting of {diagnosis}"
    hpi = (
        f"A {age}-year-old {sex} is admitted with {diagnosis}. "
        f"Presenting symptoms include {symptom_text}, present for {duration} and {course}. "
        f"Home medications include {med_text}.{started_sentence}{hospital_sentence}"
        f"{hold_sentence}{held_sentence}{context_sentence}{course_sentence}"
    )
    note = (
        f"Admission note for a {age}-year-old {sex} with {diagnosis}. "
        f"Symptoms: {symptom_text} for {duration} ({course}). "
        f"Medications continued from home: {med_text}."
        f"{started_sentence}{hospital_sentence}{hold_sentence}{held_sentence}"
        f"{context_sentence}{course_sentence}"
    )
    return CaseNarrative(chief_complaint=chief, hpi=hpi, note_text=note)


def _partition_temporal(
    medications: list[RefMedication], profile: ClinicalProfile
) -> tuple[list[RefMedication], list[RefMedication]]:
    home: list[RefMedication] = []
    started: list[RefMedication] = []
    for medication in medications:
        role = temporal_role_for(medication, profile.medication_temporal_roles)
        if role == "started_inpatient":
            started.append(medication)
        else:
            home.append(medication)
    return home, started


def _case_uses_standard_apixaban(medications: list[RefMedication]) -> bool:
    for medication in medications:
        regimen = regimen_for_medication(medication)
        if regimen is not None and regimen.id == "APIXABAN_NVAF_STANDARD":
            return True
        if "apixaban" in " ".join(
            part
            for part in (medication.ingredient, medication.generic_name, medication.concept_name)
            if part
        ).casefold():
            return True
    return False


def _started_inpatient_note(chart_note: str | None) -> str:
    marker = "Started during this admission."
    if chart_note and "started during this admission" in chart_note.casefold():
        return chart_note
    if chart_note:
        return f"{chart_note} {marker}"
    return marker


def _add_started_inpatient_medication(
    session: Session,
    *,
    case: ClinicalCase,
    ids: _IdCounter,
    medication: RefMedication,
    label: str,
    indication: str,
    dose: str,
    route: str | None,
    frequency: str,
    notes: str,
    quantity_or_days: str | None,
) -> None:
    for context, status in (("inpatient", "active"), ("discharge", "discharge")):
        session.add(
            _medication_row(
                case=case,
                ids=ids,
                medication=medication,
                label=label,
                context=context,
                status=status,
                dose=dose,
                route=route,
                frequency=frequency,
                indication=indication,
                held_reason=None,
                quantity_or_days=quantity_or_days if context == "discharge" else None,
                notes=notes,
            )
        )
    session.add(
        CaseMedicationPlan(
            plan_id=ids.next_id("plan"),
            case_id=case.id,
            ref_medication_id=medication.id,
            drug=label,
            home_state="absent",
            inpatient_state="new_start",
            correct_discharge_state="continue",
            decision="continue",
            decision_reason="Started during this admission and continued at discharge.",
            is_error_target=False,
        )
    )


def _reference_versions(session: Session) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for code in ("RXNORM", "ICD10CM", "LOINC", "UCUM", "DAILYMED", "RXCLASS"):
        row = get_data_source(session, code)
        versions[code] = row.version if row is not None else None
    return versions


def _allowed_codes(
    diagnosis: RefDiagnosis, medications: list[RefMedication], labs: list[RefLabTest]
) -> set[str]:
    codes = {item.rxcui for item in medications}
    if diagnosis.icd10cm_code:
        codes.add(diagnosis.icd10cm_code)
    codes.update(item.loinc_code for item in labs)
    return codes


def _med_label(medication: RefMedication) -> str:
    return (
        medication.generic_name
        or medication.concept_name
        or medication.ingredient
        or medication.rxcui
    )


def _contains(value: str | None, query: str) -> bool:
    if value is None:
        return False
    return query.casefold() in value.casefold()


def _str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _optional_str(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value)


def _role_map(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): str(role)
        for key, role in value.items()
        if str(key).strip() and str(role).strip()
    }


def _dict_list(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    rows: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        rows.append({str(key): str(val) for key, val in item.items() if val not in (None, "")})
    return rows


def _pick_medication(
    medications: list[RefMedication], query: str | None
) -> RefMedication | None:
    if not medications or not query:
        return None
    needle = query.casefold()
    for item in medications:
        blob = " ".join(
            part
            for part in (item.ingredient, item.generic_name, item.concept_name, item.rxcui)
            if part
        ).casefold()
        if needle in blob:
            return item
    return None


def _select_comorbidities(
    session: Session,
    *,
    profile: ClinicalProfile,
    medications: list[RefMedication],
    medication_queries: list[str],
    admission: RefDiagnosis,
) -> list[RefDiagnosis]:
    queries = list(profile.comorbidity_queries)
    found: list[RefDiagnosis] = []
    seen = {admission.icd10cm_code or str(admission.id)}
    admission_name = (admission.preferred_name or "").casefold()
    for query in queries:
        if query.casefold() in admission_name:
            continue
        row = match_diagnosis(session, query)
        if row is None:
            continue
        key = row.icd10cm_code or str(row.id)
        if key in seen:
            continue
        seen.add(key)
        found.append(row)
    _ = medications
    return found


def _indication_for(
    session: Session, medication: RefMedication, problems: list[RefDiagnosis]
) -> str:
    _ = session
    names = [item.preferred_name or item.icd10cm_code or "" for item in problems]
    blob = " ".join(
        part
        for part in (medication.ingredient, medication.generic_name, medication.concept_name)
        if part
    ).casefold()
    if "ibuprofen" in blob:
        return "symptomatic analgesia; not a treatment for the admission diagnosis"
    if "aspirin" in blob:
        for name in names:
            lowered = name.casefold()
            if any(
                token in lowered
                for token in ("ischemic", "atherosclerotic", "coronary", "infarct")
            ):
                return name
        return "antiplatelet therapy; not a treatment for the admission diagnosis"
    mapped_needles: list[str] = []
    for query, mapped in INDICATION_BY_QUERY.items():
        if query in blob:
            mapped_needles.append(mapped)
    for mapped in mapped_needles:
        for name in names:
            if mapped.casefold() in name.casefold() or name.casefold() in mapped.casefold():
                return name
    if "metoprolol" in blob or "carvedilol" in blob:
        for name in names:
            lowered = name.casefold()
            if "atrial fibrillation" in lowered or "heart failure" in lowered:
                return name
    if "enoxaparin" in blob:
        for name in names:
            lowered = name.casefold()
            if "fibrillation" in lowered or "fracture" in lowered or "thromb" in lowered:
                return name
    if "albuterol" in blob:
        return "symptomatic bronchospasm; not a treatment for the admission diagnosis"
    for name in names:
        if name:
            return name
    return "documented indication"


def _io_volumes(rng: random.Random, direction: str) -> tuple[int, int]:
    if direction == "negative":
        intake = rng.randint(1200, 1600)
        output = rng.randint(1800, 2800)
        return intake, output
    if direction == "positive":
        intake = rng.randint(2000, 2800)
        output = rng.randint(900, 1400)
        return intake, output
    intake = rng.randint(1400, 2000)
    output = rng.randint(1300, 2000)
    return intake, output


def _discharge_vital_pattern(pattern: str) -> str:
    _ = pattern
    return "discharge_ready"


def _add_investigations(
    session: Session, case: ClinicalCase, ids: _IdCounter, profile: ClinicalProfile
) -> None:
    for row in profile.imaging:
        session.add(
            CaseImaging(
                case_id=case.id,
                study_id=ids.next_id("imaging"),
                timepoint=row.get("timepoint") or "admission",
                study_type=row.get("study_type") or row.get("type"),
                body_site=row.get("body_site"),
                finding=row.get("finding"),
            )
        )
    for row in profile.consults:
        session.add(
            CaseConsult(
                case_id=case.id,
                consult_id=ids.next_id("consult"),
                service=row.get("service"),
                timepoint=row.get("timepoint") or "inpatient",
                assessment=row.get("assessment"),
                recommendation=row.get("recommendation"),
            )
        )
    for row in profile.procedures:
        session.add(
            CaseProcedure(
                case_id=case.id,
                procedure_id=ids.next_id("procedure"),
                procedure_name=row.get("procedure_name") or row.get("name"),
                procedure_type=row.get("procedure_type"),
                timepoint=row.get("timepoint") or "inpatient",
                findings=row.get("findings"),
            )
        )
    for row in profile.devices:
        session.add(
            CaseDevice(
                case_id=case.id,
                device_id=ids.next_id("device"),
                device_type=row.get("device_type") or row.get("type"),
                site=row.get("site"),
                placement_timepoint=row.get("placement_timepoint") or "inpatient",
                status=row.get("status") or "in_place",
                tip_location_or_confirmation=row.get("tip_location_or_confirmation"),
                care_instructions=row.get("care_instructions"),
                removal_plan=row.get("removal_plan"),
            )
        )
    for row in profile.microbiology:
        session.add(
            CaseMicrobiology(
                case_id=case.id,
                micro_id=ids.next_id("micro"),
                timepoint=row.get("timepoint") or "admission",
                specimen=row.get("specimen"),
                test=row.get("test"),
                organism=row.get("organism"),
                result=row.get("result"),
                status=row.get("status") or "final",
                notes=row.get("notes"),
            )
        )


def _hospital_course_text(pattern: str) -> str:
    return HOSPITAL_COURSE_TEXT.get(pattern) or HOSPITAL_COURSE_TEXT["day1_io_ready_home"]


def _followup_fields(profile: ClinicalProfile, preferred_error: str) -> tuple[str, str, str]:
    item = profile.followup_item
    service = profile.followup_service
    timing = profile.followup_timing
    if preferred_error == F2_PENDING_FOLLOWUP:
        item = "Reassess pending therapeutic decision"
    if preferred_error == F2_SUPPLY:
        timing = f"{FOLLOWUP_DAYS_FOR_SUPPLY} days"
    return item, service, timing


def _synthetic_vitals(rng: random.Random, pattern: str) -> dict[str, Any]:
    if pattern == "decompensated_hf":
        return {
            "temp_c": Decimal("36.8"),
            "bp_systolic": rng.randint(108, 138),
            "bp_diastolic": rng.randint(64, 88),
            "heart_rate": rng.randint(88, 118),
            "resp_rate": rng.randint(20, 26),
            "spo2_percent": Decimal(str(rng.randint(88, 94))),
            "oxygen_support": None,
        }
    if pattern == "hypertensive":
        return {
            "temp_c": Decimal("36.7"),
            "bp_systolic": rng.randint(180, 210),
            "bp_diastolic": rng.randint(100, 120),
            "heart_rate": rng.randint(72, 96),
            "resp_rate": rng.randint(14, 20),
            "spo2_percent": Decimal(str(rng.randint(95, 99))),
            "oxygen_support": None,
        }
    if pattern == "tachycardic_af":
        return {
            "temp_c": Decimal("36.8"),
            "bp_systolic": rng.randint(118, 148),
            "bp_diastolic": rng.randint(70, 92),
            "heart_rate": rng.randint(110, 138),
            "resp_rate": rng.randint(16, 22),
            "spo2_percent": Decimal(str(rng.randint(93, 98))),
            "oxygen_support": None,
        }
    if pattern == "febrile_pneumonia":
        return {
            "temp_c": Decimal("38.2"),
            "bp_systolic": rng.randint(110, 138),
            "bp_diastolic": rng.randint(64, 86),
            "heart_rate": rng.randint(92, 118),
            "resp_rate": rng.randint(22, 28),
            "spo2_percent": Decimal(str(rng.randint(90, 95))),
            "oxygen_support": None,
        }
    if pattern == "glycemic":
        return {
            "temp_c": Decimal("36.6"),
            "bp_systolic": rng.randint(118, 142),
            "bp_diastolic": rng.randint(70, 88),
            "heart_rate": rng.randint(70, 92),
            "resp_rate": rng.randint(14, 20),
            "spo2_percent": Decimal(str(rng.randint(95, 99))),
            "oxygen_support": None,
        }
    if pattern == "discharge_ready":
        return {
            "temp_c": Decimal("36.8"),
            "bp_systolic": rng.randint(110, 142),
            "bp_diastolic": rng.randint(64, 86),
            "heart_rate": rng.randint(62, 88),
            "resp_rate": rng.randint(14, 20),
            "spo2_percent": Decimal(str(rng.randint(95, 99))),
            "oxygen_support": None,
        }
    return {
        "temp_c": Decimal("36.8"),
        "bp_systolic": rng.randint(118, 148),
        "bp_diastolic": rng.randint(68, 88),
        "heart_rate": rng.randint(68, 92),
        "resp_rate": rng.randint(14, 20),
        "spo2_percent": Decimal(str(rng.randint(94, 98))),
        "oxygen_support": None,
    }
