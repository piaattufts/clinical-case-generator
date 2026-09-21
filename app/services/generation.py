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
from app.repositories.cases import delete_case_graph, get_case_by_code
from app.repositories.reference import (
    get_data_source,
    list_enabled_rules,
    list_symptoms,
    search_symptoms,
)
from app.services.bootstrap import (
    DEFAULT_SCENARIO_PATH,
    load_json_object,
    match_diagnosis,
    match_lab,
    match_medication,
)
from app.services.error_injection import InjectionResult, inject_reconciliation_error
from app.services.rules import CaseSnapshot, evaluate_rules, hard_violations
from app.services.validation import require_valid, serialize_report, validate_case
from app.sources.exceptions import CaseValidationError, ReferenceResolutionError
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


@dataclass
class GeneratedCaseResult:
    case_id_code: str
    case_id: UUID
    seed: str
    clean_passed: bool
    injected: InjectionResult | None
    validation: dict[str, Any]
    narrative_source: str


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
                target_error_category=str(item.get("target_error_category") or "omission"),
                diagnosis_queries=_str_list(item.get("diagnosis_queries")),
                symptom_queries=_str_list(item.get("symptom_queries")),
                medication_queries=_str_list(item.get("medication_queries")),
                anticoagulant_mutex_queries=_str_list(item.get("anticoagulant_mutex_queries")),
                lab_queries=_str_list(item.get("lab_queries")),
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
) -> GeneratedCaseResult:
    case_id_code = format_case_id_code(sequence)
    case_seed = f"{seed}:{sequence}:{scenario.code}"
    rng = random.Random(case_seed)
    existing = get_case_by_code(session, case_id_code)
    if existing is not None:
        delete_case_graph(session, existing)
    diagnosis = _require_diagnosis(session, scenario)
    symptoms = _select_symptoms(session, scenario)
    medications = _select_medications(session, scenario, rng)
    labs = _select_labs(session, scenario)
    _assert_rules_allow(session, medications, diagnosis, labs)
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
        target_home_med_count=len(medications),
        target_problem_count=1,
        clean_case=True,
        target_error_category=scenario.target_error_category if inject_error else None,
        target_error_medication_class=None,
        settings={
            "scenario": scenario.code,
            "seed": case_seed,
            "rxcuis": [item.rxcui for item in medications],
            "icd10cm": diagnosis.icd10cm_code,
            "loinc_codes": [item.loinc_code for item in labs],
        },
    )
    session.add(blueprint)
    session.flush()
    display_diagnosis = diagnosis.preferred_name or diagnosis.icd10cm_code or "source diagnosis"
    symptom_names = [item.preferred_name or "symptom" for item in symptoms]
    med_names = [_med_label(item) for item in medications]
    template = _template_narrative(age, sex, display_diagnosis, symptom_names, med_names)
    narrative, narrative_source = _maybe_openai_narrative(
        template,
        age=age,
        sex=sex,
        diagnosis=display_diagnosis,
        symptoms=symptom_names,
        medications=med_names,
        use_openai=use_openai,
        allowed_names=set(symptom_names + med_names + [display_diagnosis]),
        allowed_codes=_allowed_codes(diagnosis, medications, labs),
    )
    case = ClinicalCase(
        case_id_code=case_id_code,
        title=f"{scenario.specialty} inpatient case {case_id_code}",
        case_status="validated_clean",
        clean_case=True,
        generation_source=GENERATOR_NAME,
        one_liner=f"{age}-year-old {sex} with {display_diagnosis}",
        admission_dx=display_diagnosis,
        disposition_status="home",
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
            symptom_duration="several days",
            symptom_course="worsening",
        )
    )
    for symptom in symptoms:
        session.add(
            CaseSymptom(
                case_id=case.id,
                symptom_id=ids.next_id("symptom"),
                ref_symptom_id=symptom.id,
                symptom=symptom.preferred_name,
                duration="several days",
                severity="moderate",
                course="worsening",
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
        CaseVital(
            case_id=case.id,
            vital_id=ids.next_id("vital"),
            ref_vital_id=None,
            timepoint="admission",
            temp_c=Decimal("36.8"),
            bp_systolic=rng.randint(118, 158),
            bp_diastolic=rng.randint(68, 96),
            heart_rate=rng.randint(72, 110),
            resp_rate=rng.randint(16, 24),
            spo2_percent=Decimal(str(rng.randint(91, 98))),
            oxygen_support=None,
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
                value=float(rng.randint(20, 80)) / 10.0,
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
            timepoint="hospital_day_1",
            intake_ml=intake,
            output_ml=output,
            net_ml=intake - output,
            notes=NUMERIC_ORIGIN,
        )
    )
    for medication in medications:
        label = _med_label(medication)
        dose = medication.strength
        for context, status in (
            ("home", "home"),
            ("inpatient", "active"),
            ("discharge", "discharge"),
        ):
            session.add(
                CaseMedication(
                    case_id=case.id,
                    medication_id=ids.next_id("medication"),
                    ref_medication_id=medication.id,
                    context=context,
                    drug=label,
                    reported_name=label,
                    dose=dose,
                    route=medication.route,
                    frequency=None,
                    indication=display_diagnosis,
                    status=status,
                    held_reason=None,
                    verification_status="source_backed",
                    verification_source="RXNORM",
                    target_or_goal=None,
                    monitoring=None,
                    quantity_or_days=None,
                    refills=None,
                    source_type="reference",
                    source_file=None,
                    source_reference=f"RXCUI:{medication.rxcui}",
                    notes=None,
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
            disposition="home",
            disposition_detail=None,
            discharge_readiness="ready",
            anticipated_discharge_date=None,
            transportation_needed=False,
            home_health_ordered=False,
            barriers_to_discharge=[],
            dme_needed=[],
        )
    )
    session.add(
        CaseFollowup(
            case_id=case.id,
            followup_id=ids.next_id("followup"),
            item="Primary care follow-up",
            timing="7 days",
            with_service="primary care",
            status="planned",
        )
    )
    session.add(
        CaseInstruction(
            case_id=case.id,
            instruction_id=ids.next_id("instruction"),
            category="medications",
            instruction_text=(
                "Take discharge medications exactly as listed on the clean medication plan."
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
    clean_report = validate_case(session, case, expect_injected_error=False)
    require_valid(clean_report)
    injected: InjectionResult | None = None
    if inject_error:
        injected = inject_reconciliation_error(
            session,
            case,
            rng=rng,
            seed=case_seed,
            preferred_category=scenario.target_error_category,
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
    final_report = validate_case(session, case, expect_injected_error=inject_error)
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
            "reference_versions": _reference_versions(session),
            "rules_applied": [rule.rule_code for rule in list_enabled_rules(session)],
            "numeric_value_origin": NUMERIC_ORIGIN,
            "narrative_source": narrative_source,
            "clean_validation": serialize_report(clean_report),
            "final_validation": serialize_report(final_report),
            "error_injection": None
            if injected is None
            else {
                "category": injected.category,
                "rxcui": injected.rxcui,
                "drug": injected.drug,
                "seed": injected.seed,
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
        report = validate_case(session, case, expect_injected_error=expect_error)
        payload = serialize_report(report)
        reports.append(payload)
        if not report.passed:
            raise CaseValidationError("case", payload["errors"][0], payload["errors"])
    return reports


def _require_diagnosis(session: Session, scenario: Scenario) -> RefDiagnosis:
    for query in scenario.diagnosis_queries:
        row = match_diagnosis(session, query)
        if row is not None:
            return row
    raise ReferenceResolutionError("diagnosis", ",".join(scenario.diagnosis_queries))


def _select_symptoms(session: Session, scenario: Scenario) -> list[RefSymptom]:
    found: list[RefSymptom] = []
    seen: set[UUID] = set()
    for query in scenario.symptom_queries:
        rows, _ = search_symptoms(session, query, limit=20, offset=0)
        ranked = sorted(rows, key=lambda item: (item.preferred_name or "", str(item.id)))
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
    session: Session, scenario: Scenario, rng: random.Random
) -> list[RefMedication]:
    selected: list[RefMedication] = []
    seen: set[str] = set()
    for query in scenario.medication_queries:
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
    if mutex:
        mutex.sort(key=lambda item: item.rxcui)
        chosen = rng.choice(mutex)
        selected.append(chosen)
        seen.add(chosen.rxcui)
    if not selected:
        raise ReferenceResolutionError("medication", ",".join(scenario.medication_queries))
    selected.sort(key=lambda item: item.rxcui)
    return selected


def _select_labs(session: Session, scenario: Scenario) -> list[RefLabTest]:
    found: list[RefLabTest] = []
    seen: set[str] = set()
    for query in scenario.lab_queries:
        row = match_lab(session, query)
        if row is None or row.loinc_code in seen:
            continue
        seen.add(row.loinc_code)
        found.append(row)
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
            responsible_service="inpatient medicine",
        )
    )


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
) -> CaseNarrative:
    symptom_text = ", ".join(symptoms) if symptoms else "reported symptoms"
    med_text = ", ".join(medications) if medications else "the selected home medications"
    chief = f"{symptom_text} in the setting of {diagnosis}"
    hpi = (
        f"A {age}-year-old {sex} is admitted with {diagnosis}. "
        f"Presenting symptoms include {symptom_text}. "
        f"Home medications include {med_text}."
    )
    note = (
        f"Admission note for a {age}-year-old {sex} with {diagnosis}. "
        f"Symptoms: {symptom_text}. Medications continued from home: {med_text}."
    )
    return CaseNarrative(chief_complaint=chief, hpi=hpi, note_text=note)


def _reference_versions(session: Session) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for code in ("RXNORM", "ICD10CM", "LOINC", "UCUM", "DAILYMED"):
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
