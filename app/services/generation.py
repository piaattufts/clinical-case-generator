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
    CaseDiagnosis,
    CaseDischargePlanning,
    CaseFollowup,
    CaseInstruction,
    CaseIntakeOutput,
    CaseLab,
    CaseMedication,
    CaseMedicationReconciliation,
    CaseMonitoring,
    CaseNote,
    CasePresentation,
    CaseProblemList,
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
    list_symptoms,
    search_symptoms,
)
from app.services.bootstrap import (
    DEFAULT_SCENARIO_PATH,
    load_json_object,
    match_diagnosis,
    match_lab,
    match_medication,
    token_match,
)
from app.services.case_diversity import (
    CleanCaseFingerprint,
    fingerprint_as_dict,
    fingerprint_from_case,
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


HOSPITAL_COURSE_TEXT = {
    "day1_io_ready_home": (
        "The inpatient stay was brief. Intake and output were recorded, and the "
        "patient was judged ready for discharge home."
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
        "Glucose was monitored and diabetes therapy was continued while the "
        "inpatient team prepared a discharge plan."
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
            )
        )
    return profiles


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
        scenarios.append(
            Scenario(
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
            )
        )
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
    _assert_rules_allow(session, medications + stop_medications + hospital_only, diagnosis, labs)
    hold_restart = None
    substitution_pair = None
    if inject_error and preferred_error == F2_HELD_RESTART:
        if not medications:
            raise CaseValidationError(
                "error_eligibility",
                "f2_held_med_no_restart_plan requires a home medication "
                "that can be held with a restart plan",
            )
        hold_restart = medications[0]
        medications = medications[1:]
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
    sex = rng.choice(["Female", "Male"])
    hospital_day = rng.randint(2, 6)
    patient_name = f"SYN Patient {sequence:03d}"
    now = datetime.now(UTC)
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
        target_problem_count=1,
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
        },
    )
    session.add(blueprint)
    session.flush()
    display_diagnosis = diagnosis.preferred_name or diagnosis.icd10cm_code or "source diagnosis"
    symptom_names = [item.preferred_name or "symptom" for item in symptoms]
    med_names = [_med_label(item) for item in medications]
    held_names = [_med_label(item) for item in stop_medications]
    if hold_restart is not None:
        held_names = [_med_label(hold_restart), *held_names]
    template = _template_narrative(
        age,
        sex,
        display_diagnosis,
        symptom_names,
        med_names,
        held_names,
        duration=profile.symptom_duration,
        course=profile.symptom_course,
        hospital_course=_hospital_course_text(profile.hospital_course_pattern),
    )
    narrative, narrative_source = _maybe_openai_narrative(
        template,
        age=age,
        sex=sex,
        diagnosis=display_diagnosis,
        symptoms=symptom_names,
        medications=med_names + held_names,
        use_openai=use_openai,
        allowed_names=set(symptom_names + med_names + held_names + [display_diagnosis]),
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
            living_situation="Lives at home",
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
    session.add(
        CaseProblemList(
            case_id=case.id,
            problem_id=ids.next_id("problem"),
            problem=display_diagnosis,
            problem_type="diagnosis",
            priority="high",
            status="active",
            assessment=display_diagnosis,
            plan="Continue source-backed inpatient therapy selected from local reference data.",
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
    for lab in labs:
        unit = None
        examples = lab.example_ucum_units or []
        if examples:
            unit = str(examples[0])
        session.add(
            CaseLab(
                case_id=case.id,
                lab_id=ids.next_id("lab"),
                ref_lab_id=lab.id,
                timepoint="admission",
                test_name=lab.long_common_name or lab.loinc_code,
                value=_synthetic_lab_value(rng, lab),
                value_text=None,
                unit=unit,
                status="final",
            )
        )
    session.add(
        CaseWeight(
            case_id=case.id,
            weight_id=ids.next_id("weight"),
            timepoint="admission",
            weight_kg=Decimal(str(rng.randint(60, 110))),
            dry_weight_kg=None,
        )
    )
    intake = rng.randint(1200, 2200)
    output = rng.randint(800, 1800)
    session.add(
        CaseIntakeOutput(
            case_id=case.id,
            io_id=ids.next_id("io"),
            timepoint=profile.io_timepoint,
            intake_ml=intake,
            output_ml=output,
            net_ml=intake - output,
            notes=NUMERIC_ORIGIN,
        )
    )
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
            indication=display_diagnosis,
            frequency=scenario.default_frequency,
            quantity_or_days=None if supply_days is None else f"{supply_days} days",
        )
    if hold_restart is not None:
        _add_held_restart_medication(
            session,
            case=case,
            ids=ids,
            medication=hold_restart,
            indication=display_diagnosis,
            frequency=scenario.default_frequency,
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
            indication=display_diagnosis,
            frequency=scenario.default_frequency,
        )
    for medication in stop_medications:
        _add_stopped_medication(
            session,
            case=case,
            ids=ids,
            medication=medication,
            indication=display_diagnosis,
            frequency=scenario.default_frequency,
        )
    for medication in hospital_only:
        _add_hospital_only_medication(
            session,
            case=case,
            ids=ids,
            medication=medication,
            indication=display_diagnosis,
            frequency=scenario.default_frequency,
        )
    session.add(
        CaseMedicationReconciliation(
            case_id=case.id,
            medrec_id=ids.next_id("medrec"),
            reconciliation_context="discharge",
            medrec_status="complete_clean",
            patient_able_to_participate=True,
            bpmh_source="synthetic_history",
            bpmh_interviewer=None,
            bpmh_date=None,
            discrepancies_found=False,
            resolved=True,
            discrepancy_types=[],
            pharmacist_review=True,
            high_alert_meds_identified=[],
            notes="Clean case before intentional error injection.",
        )
    )
    _maybe_add_warfarin_monitoring(session, case, ids, medications, labs)
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
        pending_name = _med_label(medications[0]) if medications else display_diagnosis
        session.add(
            CaseInstruction(
                case_id=case.id,
                instruction_id=ids.next_id("instruction"),
                category="followup",
                instruction_text=(
                    f"Pending therapeutic decision: duration of {pending_name} remains "
                    "uncertain and will be determined at the scheduled follow-up."
                ),
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
            rec.notes = injected.explanation
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
) -> None:
    label = _med_label(medication)
    dose = _synthetic_dose(medication)
    route = medication.route or "oral"
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
) -> None:
    label = _med_label(medication)
    dose = _synthetic_dose(medication)
    route = medication.route or "oral"
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
) -> None:
    label = _med_label(medication)
    dose = _synthetic_dose(medication)
    route = medication.route or "oral"
    held_reason = "Held inpatient for documented in-hospital hypotension; intended to restart."
    restart = "Resume when systolic blood pressure remains above 100 mmHg for 24 hours."
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
                held_reason=held_reason,
                target_or_goal=restart,
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
    dose = _synthetic_dose(medication)
    route = medication.route or "oral"
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
    home_dose = _synthetic_dose(home_medication)
    sub_dose = _synthetic_dose(substitute)
    home_route = home_medication.route or "oral"
    sub_route = substitute.route or "oral"
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
            frequency=frequency,
            indication=sub_indication,
            held_reason=None,
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
        verification_source="prior_records",
        target_or_goal=target_or_goal,
        monitoring=monitoring,
        quantity_or_days=quantity_or_days,
        refills=None,
        source_type="reference",
        source_file=None,
        source_reference=f"RXCUI:{medication.rxcui}",
        notes=NUMERIC_ORIGIN if medication.strength is None else None,
    )


def _synthetic_dose(medication: RefMedication) -> str:
    if medication.strength and medication.strength.strip():
        return medication.strength.strip()
    return "1 tablet"


def _synthetic_lab_value(rng: random.Random, lab: RefLabTest) -> float:
    blob = " ".join(
        part
        for part in (lab.long_common_name, lab.short_name, lab.component, lab.loinc_code)
        if part
    ).casefold()
    if "inr" in blob or "international normalized" in blob:
        return rng.randint(18, 32) / 10.0
    if "potassium" in blob:
        return rng.randint(35, 48) / 10.0
    if "creatinine" in blob:
        return rng.randint(8, 16) / 10.0
    if "sodium" in blob:
        return float(rng.randint(134, 144))
    if "glucose" in blob:
        return float(rng.randint(110, 180))
    if "hemoglobin" in blob or "haemoglobin" in blob:
        return rng.randint(105, 145) / 10.0
    if "natriuretic" in blob or "bnp" in blob:
        return float(rng.randint(180, 900))
    return rng.randint(20, 80) / 10.0


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
    for query in queries:
        rows, _ = search_symptoms(session, query, limit=20, offset=0)
        ranked = sorted(
            (
                item
                for item in rows
                if token_match(item.preferred_name, query)
                or any(token_match(str(synonym), query) for synonym in (item.synonyms or []))
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
    if found:
        return found
    fallback = list_symptoms(session)
    return fallback[:3]


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
    for query in queries:
        row = match_medication(session, query)
        if row is None or row.rxcui in used:
            continue
        used.add(row.rxcui)
        selected.append(row)
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
) -> None:
    snapshot = CaseSnapshot(
        age=None,
        sex=None,
        care_context="inpatient",
        icd10cm_codes=frozenset({diagnosis.icd10cm_code} if diagnosis.icd10cm_code else set()),
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
            frequency="as labeled",
            target=None,
            trigger_for_action=None,
            duration=None,
            responsible_service="outpatient anticoagulation",
        )
    )
    for row in list_medications_for_case(session, case.id):
        if row.ref_medication_id != warfarin_ref.id:
            continue
        row.monitoring = "Outpatient monitoring arranged."


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
) -> CaseNarrative:
    symptom_text = ", ".join(symptoms) if symptoms else "reported symptoms"
    med_text = ", ".join(medications) if medications else "the selected home medications"
    held_text = ", ".join(held) if held else ""
    held_sentence = (
        f" {held_text} was held on admission and is not intended for discharge continuation."
        if held_text
        else ""
    )
    course_sentence = f" {hospital_course}" if hospital_course else ""
    chief = f"{symptom_text} in the setting of {diagnosis}"
    hpi = (
        f"A {age}-year-old {sex} is admitted with {diagnosis}. "
        f"Presenting symptoms include {symptom_text}, present for {duration} and {course}. "
        f"Home medications include {med_text}.{held_sentence}{course_sentence}"
    )
    note = (
        f"Admission note for a {age}-year-old {sex} with {diagnosis}. "
        f"Symptoms: {symptom_text} for {duration} ({course}). "
        f"Medications continued from home: {med_text}.{held_sentence}{course_sentence}"
    )
    return CaseNarrative(chief_complaint=chief, hpi=hpi, note_text=note)


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
            "bp_systolic": rng.randint(150, 178),
            "bp_diastolic": rng.randint(88, 108),
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
    return {
        "temp_c": Decimal("36.8"),
        "bp_systolic": rng.randint(118, 158),
        "bp_diastolic": rng.randint(68, 96),
        "heart_rate": rng.randint(72, 110),
        "resp_rate": rng.randint(16, 24),
        "spo2_percent": Decimal(str(rng.randint(91, 98))),
        "oxygen_support": None,
    }
