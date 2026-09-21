"""Pydantic models matching Phase 1 tables. These are not a generation pipeline."""

from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CaseAnswerKey(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    answer_id: str | None = None
    error_family: str | None = None
    error_category: str | None = None
    error_description: str | None = None
    trigger_meds: Any | None = None
    detectability_location: str | None = None
    correct_action: str | None = None
    severity_ncc_merp: str | None = None
    difficulty_a_priori: str | None = None
    is_primary_error: bool | None = None
    intentional_changes: Any | None = None
    case_id: UUID
    id: UUID


class CaseLab(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    lab_id: str | None = None
    ref_lab_id: UUID | None = None
    timepoint: str | None = None
    test_name: str | None = None
    value: float | None = None
    value_text: str | None = None
    unit: str | None = None
    status: str | None = None
    case_id: UUID
    id: UUID


class CaseDischargePlanning(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    disposition: str | None = None
    disposition_detail: str | None = None
    discharge_readiness: str | None = None
    anticipated_discharge_date: date_type | None = None
    transportation_needed: bool | None = None
    home_health_ordered: bool | None = None
    barriers_to_discharge: Any | None = None
    dme_needed: Any | None = None
    case_id: UUID
    id: UUID


class CaseDevice(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    device_id: str | None = None
    ref_device_id: UUID | None = None
    device_type: str | None = None
    site: str | None = None
    placement_timepoint: str | None = None
    status: str | None = None
    tip_location_or_confirmation: str | None = None
    care_instructions: str | None = None
    removal_plan: str | None = None
    case_id: UUID
    id: UUID


class CaseMonitoring(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    monitoring_id: str | None = None
    parameter: str | None = None
    frequency: str | None = None
    target: str | None = None
    trigger_for_action: str | None = None
    duration: str | None = None
    responsible_service: str | None = None
    case_id: UUID
    id: UUID


class CaseVital(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    vital_id: str | None = None
    ref_vital_id: UUID | None = None
    timepoint: str | None = None
    temp_c: Decimal | None = None
    bp_systolic: int | None = None
    bp_diastolic: int | None = None
    heart_rate: int | None = None
    resp_rate: int | None = None
    spo2_percent: Decimal | None = None
    oxygen_support: str | None = None
    case_id: UUID
    id: UUID


class CaseProcedure(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    procedure_id: str | None = None
    ref_procedure_id: UUID | None = None
    procedure_name: str | None = None
    procedure_type: str | None = None
    date: date_type | None = None
    timepoint: str | None = None
    performed_by: str | None = None
    anesthesia_type: str | None = None
    findings: str | None = None
    complications: str | None = None
    duration_minutes: int | None = None
    laterality: str | None = None
    case_id: UUID
    id: UUID


class CaseDiagnosis(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    diagnosis_id: str | None = None
    ref_diagnosis_id: UUID | None = None
    diagnosis: str | None = None
    diagnosis_type: str | None = None
    status: str | None = None
    context: str | None = None
    source_type: str | None = None
    source_reference: str | None = None
    case_id: UUID
    id: UUID


class CaseWeight(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    weight_id: str | None = None
    timepoint: str | None = None
    weight_kg: Decimal | None = None
    dry_weight_kg: Decimal | None = None
    case_id: UUID
    id: UUID


class CaseMedicationReconciliation(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    medrec_id: str | None = None
    reconciliation_context: str | None = None
    medrec_status: str | None = None
    patient_able_to_participate: bool | None = None
    bpmh_source: str | None = None
    bpmh_interviewer: str | None = None
    bpmh_date: date_type | None = None
    discrepancies_found: bool | None = None
    resolved: bool | None = None
    discrepancy_types: Any | None = None
    pharmacist_review: bool | None = None
    high_alert_meds_identified: Any | None = None
    notes: str | None = None
    case_id: UUID
    id: UUID


class CaseFollowup(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    followup_id: str | None = None
    item: str | None = None
    timing: str | None = None
    with_service: str | None = None
    status: str | None = None
    case_id: UUID
    id: UUID


class CaseInstruction(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    instruction_id: str | None = None
    category: str | None = None
    instruction_text: str | None = None
    source_type: str | None = None
    case_id: UUID
    id: UUID


class ClinicalCase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    case_id_code: str
    title: str | None = None
    case_status: str | None = None
    clean_case: bool | None = None
    generation_source: str | None = None
    one_liner: str | None = None
    admission_dx: str | None = None
    disposition_status: str | None = None
    chief_complaint: str | None = None
    patient_name: str | None = None
    patient_age: int | None = None
    patient_gender: str | None = None
    ethnicity: str | None = None
    specialty: str | None = None
    difficulty: str | None = None
    is_active: bool | None = None
    source_type: str | None = None
    source_file: str | None = None
    id: UUID


class CaseIntakeOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    io_id: str | None = None
    timepoint: str | None = None
    intake_ml: int | None = None
    output_ml: int | None = None
    net_ml: int | None = None
    notes: str | None = None
    case_id: UUID
    id: UUID


class CasePresentation(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    chief_complaint: str | None = None
    hpi: str | None = None
    review_of_systems: str | None = None
    symptom_duration: str | None = None
    symptom_course: str | None = None
    case_id: UUID
    id: UUID


class CaseConsult(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    consult_id: str | None = None
    service: str | None = None
    timepoint: str | None = None
    assessment: str | None = None
    recommendation: str | None = None
    case_id: UUID
    id: UUID


class CaseTherapyRestriction(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    therapy_id: str | None = None
    category: str | None = None
    item: str | None = None
    order_detail: str | None = None
    start_date: date_type | None = None
    end_date: date_type | None = None
    status: str | None = None
    ordered_by: str | None = None
    case_id: UUID
    id: UUID


class CaseMedication(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    medication_id: str | None = None
    ref_medication_id: UUID | None = None
    context: str | None = None
    drug: str | None = None
    reported_name: str | None = None
    dose: str | None = None
    route: str | None = None
    frequency: str | None = None
    indication: str | None = None
    status: str | None = None
    held_reason: str | None = None
    verification_status: str | None = None
    verification_source: str | None = None
    target_or_goal: str | None = None
    monitoring: str | None = None
    quantity_or_days: str | None = None
    refills: str | None = None
    source_type: str | None = None
    source_file: str | None = None
    source_reference: str | None = None
    notes: str | None = None
    case_id: UUID
    id: UUID


class CaseImaging(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    study_id: str | None = None
    timepoint: str | None = None
    study_type: str | None = None
    body_site: str | None = None
    finding: str | None = None
    case_id: UUID
    id: UUID


class CaseReturnPrecaution(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    precaution_id: str | None = None
    symptom: str | None = None
    reason: str | None = None
    action: str | None = None
    severity: str | None = None
    patient_instruction: str | None = None
    case_id: UUID
    id: UUID


class CaseProblemList(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    problem_id: str | None = None
    problem: str | None = None
    problem_type: str | None = None
    priority: str | None = None
    status: str | None = None
    assessment: str | None = None
    plan: str | None = None
    case_id: UUID
    id: UUID


class CaseSocialSupport(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    living_situation: str | None = None
    caregiver_support: str | None = None
    health_care_proxy: str | None = None
    supervision_requirement: str | None = None
    transportation: str | None = None
    financial_barriers: str | None = None
    health_literacy: str | None = None
    language_preference: str | None = None
    substance_use: str | None = None
    advance_directive: str | None = None
    case_id: UUID
    id: UUID


class CaseSymptom(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    symptom_id: str | None = None
    ref_symptom_id: UUID | None = None
    symptom: str | None = None
    duration: str | None = None
    severity: str | None = None
    course: str | None = None
    status: str | None = None
    notes: str | None = None
    case_id: UUID
    id: UUID


class CaseMicrobiology(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    micro_id: str | None = None
    ref_micro_id: UUID | None = None
    timepoint: str | None = None
    specimen: str | None = None
    test: str | None = None
    organism: str | None = None
    result: str | None = None
    quantity: str | None = None
    status: str | None = None
    notes: str | None = None
    case_id: UUID
    id: UUID


class CaseNote(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    note_id: str | None = None
    note_type: str | None = None
    note_text: str | None = None
    source_type: str | None = None
    case_id: UUID
    id: UUID
