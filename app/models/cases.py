"""Synthetic case tables.

case_id is the UUID foreign key. Dashboard business ids (symptom_id, diagnosis_id, and
the rest) are separate unique strings and stay null until a later phase assigns them.
No SYN-* identifiers are generated here.

Optional reference foreign keys use ON DELETE RESTRICT so removing a reference row
cannot silently orphan the meaning of a case field.
"""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Double,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, CaseChildMixin, UUIDPrimaryKeyMixin

_MEDICATION_CONTEXT = (
    "context IS NULL OR context IN ('home', 'inpatient', 'inpatient_history', 'discharge')"
)
_MEDICATION_STATUS = (
    "status IS NULL OR status IN ('home', 'active', 'held', 'discontinued', 'discharge')"
)
_MEDREC_CONTEXT = (
    "reconciliation_context IS NULL OR reconciliation_context IN ('admission', 'discharge')"
)


def _external_id(column_name: str) -> Mapped[str | None]:
    """Nullable unique dashboard business id. Multiple nulls are allowed."""
    return mapped_column(column_name, String(64), unique=True)


def _ref_fk(column_name: str, table_name: str) -> Mapped[uuid.UUID | None]:
    """Optional reference link. RESTRICT blocks deleting a referenced concept."""
    return mapped_column(
        column_name,
        ForeignKey(f"{table_name}.id", ondelete="RESTRICT"),
        index=True,
    )


class ClinicalCase(Base, UUIDPrimaryKeyMixin):
    """One synthetic case. case_id_code is required because every row is a case."""

    __tablename__ = "clinical_cases"
    __table_args__ = (
        CheckConstraint("btrim(case_id_code) <> ''", name="case_id_code_not_blank"),
    )

    case_id_code: Mapped[str] = mapped_column(String(32), unique=True)
    title: Mapped[str | None] = mapped_column(String(512))
    case_status: Mapped[str | None] = mapped_column(String(64))
    clean_case: Mapped[bool | None] = mapped_column(Boolean)
    generation_source: Mapped[str | None] = mapped_column(String(64))
    one_liner: Mapped[str | None] = mapped_column(Text)
    admission_dx: Mapped[str | None] = mapped_column(Text)
    disposition_status: Mapped[str | None] = mapped_column(String(64))
    chief_complaint: Mapped[str | None] = mapped_column(Text)
    patient_name: Mapped[str | None] = mapped_column(String(256))
    patient_age: Mapped[int | None] = mapped_column(Integer)
    patient_gender: Mapped[str | None] = mapped_column(String(64))
    ethnicity: Mapped[str | None] = mapped_column(String(128))
    specialty: Mapped[str | None] = mapped_column(String(128))
    difficulty: Mapped[str | None] = mapped_column(String(64))
    is_active: Mapped[bool | None] = mapped_column(Boolean)
    source_type: Mapped[str | None] = mapped_column(String(64))
    source_file: Mapped[str | None] = mapped_column(String(512))


class CasePresentation(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_presentations"

    chief_complaint: Mapped[str | None] = mapped_column(Text)
    hpi: Mapped[str | None] = mapped_column(Text)
    review_of_systems: Mapped[str | None] = mapped_column(Text)
    symptom_duration: Mapped[str | None] = mapped_column(String(128))
    symptom_course: Mapped[str | None] = mapped_column(String(128))

    case: Mapped[ClinicalCase] = relationship()


class CaseSymptom(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_symptoms"

    symptom_id: Mapped[str | None] = _external_id("symptom_id")
    ref_symptom_id: Mapped[uuid.UUID | None] = _ref_fk("ref_symptom_id", "ref_symptoms")
    symptom: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[str | None] = mapped_column(String(128))
    severity: Mapped[str | None] = mapped_column(String(64))
    course: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseSocialSupport(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_social_supports"

    living_situation: Mapped[str | None] = mapped_column(Text)
    caregiver_support: Mapped[str | None] = mapped_column(Text)
    health_care_proxy: Mapped[str | None] = mapped_column(Text)
    supervision_requirement: Mapped[str | None] = mapped_column(Text)
    transportation: Mapped[str | None] = mapped_column(Text)
    financial_barriers: Mapped[str | None] = mapped_column(Text)
    health_literacy: Mapped[str | None] = mapped_column(Text)
    language_preference: Mapped[str | None] = mapped_column(String(64))
    substance_use: Mapped[str | None] = mapped_column(Text)
    advance_directive: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseDiagnosis(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_diagnoses"

    diagnosis_id: Mapped[str | None] = _external_id("diagnosis_id")
    ref_diagnosis_id: Mapped[uuid.UUID | None] = _ref_fk("ref_diagnosis_id", "ref_diagnoses")
    diagnosis: Mapped[str | None] = mapped_column(Text)
    diagnosis_type: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))
    context: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str | None] = mapped_column(String(64))
    source_reference: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseProblemList(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_problem_list"

    problem_id: Mapped[str | None] = _external_id("problem_id")
    problem: Mapped[str | None] = mapped_column(Text)
    problem_type: Mapped[str | None] = mapped_column(String(64))
    priority: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))
    assessment: Mapped[str | None] = mapped_column(Text)
    plan: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseNote(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_notes"

    note_id: Mapped[str | None] = _external_id("note_id")
    note_type: Mapped[str | None] = mapped_column(String(64))
    note_text: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str | None] = mapped_column(String(64))

    case: Mapped[ClinicalCase] = relationship()


class CaseVital(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_vitals"

    vital_id: Mapped[str | None] = _external_id("vital_id")
    ref_vital_id: Mapped[uuid.UUID | None] = _ref_fk("ref_vital_id", "ref_vitals")
    timepoint: Mapped[str | None] = mapped_column(String(64))
    temp_c: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    bp_systolic: Mapped[int | None] = mapped_column(Integer)
    bp_diastolic: Mapped[int | None] = mapped_column(Integer)
    heart_rate: Mapped[int | None] = mapped_column(Integer)
    resp_rate: Mapped[int | None] = mapped_column(Integer)
    spo2_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    oxygen_support: Mapped[str | None] = mapped_column(String(128))

    case: Mapped[ClinicalCase] = relationship()


class CaseLab(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    """Numeric value and value_text are independent. Text is not coerced into value."""

    __tablename__ = "case_labs"

    lab_id: Mapped[str | None] = _external_id("lab_id")
    ref_lab_id: Mapped[uuid.UUID | None] = _ref_fk("ref_lab_id", "ref_lab_tests")
    timepoint: Mapped[str | None] = mapped_column(String(64))
    test_name: Mapped[str | None] = mapped_column(String(256))
    value: Mapped[float | None] = mapped_column(Double)
    value_text: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))

    case: Mapped[ClinicalCase] = relationship()


class CaseMicrobiology(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_microbiology"

    micro_id: Mapped[str | None] = _external_id("micro_id")
    ref_micro_id: Mapped[uuid.UUID | None] = _ref_fk("ref_micro_id", "ref_microbiology")
    timepoint: Mapped[str | None] = mapped_column(String(64))
    specimen: Mapped[str | None] = mapped_column(String(128))
    test: Mapped[str | None] = mapped_column(String(256))
    organism: Mapped[str | None] = mapped_column(String(256))
    result: Mapped[str | None] = mapped_column(Text)
    quantity: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseWeight(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_weights"

    weight_id: Mapped[str | None] = _external_id("weight_id")
    timepoint: Mapped[str | None] = mapped_column(String(64))
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))
    dry_weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(8, 3))

    case: Mapped[ClinicalCase] = relationship()


class CaseIntakeOutput(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_intake_outputs"

    io_id: Mapped[str | None] = _external_id("io_id")
    timepoint: Mapped[str | None] = mapped_column(String(64))
    intake_ml: Mapped[int | None] = mapped_column(Integer)
    output_ml: Mapped[int | None] = mapped_column(Integer)
    net_ml: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseImaging(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_imaging"

    study_id: Mapped[str | None] = _external_id("study_id")
    timepoint: Mapped[str | None] = mapped_column(String(64))
    study_type: Mapped[str | None] = mapped_column(String(128))
    body_site: Mapped[str | None] = mapped_column(String(128))
    finding: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseProcedure(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_procedures"

    procedure_id: Mapped[str | None] = _external_id("procedure_id")
    ref_procedure_id: Mapped[uuid.UUID | None] = _ref_fk("ref_procedure_id", "ref_procedures")
    procedure_name: Mapped[str | None] = mapped_column(String(512))
    procedure_type: Mapped[str | None] = mapped_column(String(64))
    date: Mapped[date | None] = mapped_column(Date)
    timepoint: Mapped[str | None] = mapped_column(String(64))
    performed_by: Mapped[str | None] = mapped_column(String(128))
    anesthesia_type: Mapped[str | None] = mapped_column(String(64))
    findings: Mapped[str | None] = mapped_column(Text)
    complications: Mapped[str | None] = mapped_column(Text)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    laterality: Mapped[str | None] = mapped_column(String(32))

    case: Mapped[ClinicalCase] = relationship()


class CaseDevice(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_devices"

    device_id: Mapped[str | None] = _external_id("device_id")
    ref_device_id: Mapped[uuid.UUID | None] = _ref_fk("ref_device_id", "ref_devices")
    device_type: Mapped[str | None] = mapped_column(String(128))
    site: Mapped[str | None] = mapped_column(String(128))
    placement_timepoint: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))
    tip_location_or_confirmation: Mapped[str | None] = mapped_column(Text)
    care_instructions: Mapped[str | None] = mapped_column(Text)
    removal_plan: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseConsult(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_consults"

    consult_id: Mapped[str | None] = _external_id("consult_id")
    service: Mapped[str | None] = mapped_column(String(128))
    timepoint: Mapped[str | None] = mapped_column(String(64))
    assessment: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseMedication(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    """Reported medications may keep drug null until a reference concept is verified."""

    __tablename__ = "case_medications"
    __table_args__ = (
        CheckConstraint(_MEDICATION_CONTEXT, name="context_values"),
        CheckConstraint(_MEDICATION_STATUS, name="status_values"),
    )

    medication_id: Mapped[str | None] = _external_id("medication_id")
    ref_medication_id: Mapped[uuid.UUID | None] = _ref_fk("ref_medication_id", "ref_medications")
    context: Mapped[str | None] = mapped_column(String(32))
    drug: Mapped[str | None] = mapped_column(String(512))
    reported_name: Mapped[str | None] = mapped_column(String(512))
    dose: Mapped[str | None] = mapped_column(String(128))
    route: Mapped[str | None] = mapped_column(String(64))
    frequency: Mapped[str | None] = mapped_column(String(64))
    indication: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(String(32))
    held_reason: Mapped[str | None] = mapped_column(Text)
    verification_status: Mapped[str | None] = mapped_column(String(64))
    verification_source: Mapped[str | None] = mapped_column(String(128))
    target_or_goal: Mapped[str | None] = mapped_column(Text)
    monitoring: Mapped[str | None] = mapped_column(Text)
    quantity_or_days: Mapped[str | None] = mapped_column(String(64))
    refills: Mapped[str | None] = mapped_column(String(32))
    source_type: Mapped[str | None] = mapped_column(String(64))
    source_file: Mapped[str | None] = mapped_column(String(512))
    source_reference: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseMedicationReconciliation(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_medication_reconciliations"
    __table_args__ = (CheckConstraint(_MEDREC_CONTEXT, name="reconciliation_context_values"),)

    medrec_id: Mapped[str | None] = _external_id("medrec_id")
    reconciliation_context: Mapped[str | None] = mapped_column(String(32))
    medrec_status: Mapped[str | None] = mapped_column(String(64))
    patient_able_to_participate: Mapped[bool | None] = mapped_column(Boolean)
    bpmh_source: Mapped[str | None] = mapped_column(String(128))
    bpmh_interviewer: Mapped[str | None] = mapped_column(String(128))
    bpmh_date: Mapped[date | None] = mapped_column(Date)
    discrepancies_found: Mapped[bool | None] = mapped_column(Boolean)
    resolved: Mapped[bool | None] = mapped_column(Boolean)
    discrepancy_types: Mapped[list[Any] | None] = mapped_column(JSONB)
    pharmacist_review: Mapped[bool | None] = mapped_column(Boolean)
    high_alert_meds_identified: Mapped[list[Any] | None] = mapped_column(JSONB)
    notes: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseMonitoring(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_monitoring"

    monitoring_id: Mapped[str | None] = _external_id("monitoring_id")
    parameter: Mapped[str | None] = mapped_column(String(128))
    frequency: Mapped[str | None] = mapped_column(String(64))
    target: Mapped[str | None] = mapped_column(String(128))
    trigger_for_action: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[str | None] = mapped_column(String(64))
    responsible_service: Mapped[str | None] = mapped_column(String(128))

    case: Mapped[ClinicalCase] = relationship()


class CaseTherapyRestriction(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_therapy_restrictions"

    therapy_id: Mapped[str | None] = _external_id("therapy_id")
    category: Mapped[str | None] = mapped_column(String(64))
    item: Mapped[str | None] = mapped_column(String(256))
    order_detail: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(String(64))
    ordered_by: Mapped[str | None] = mapped_column(String(128))

    case: Mapped[ClinicalCase] = relationship()


class CaseDischargePlanning(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_discharge_planning"

    disposition: Mapped[str | None] = mapped_column(String(128))
    disposition_detail: Mapped[str | None] = mapped_column(Text)
    discharge_readiness: Mapped[str | None] = mapped_column(String(64))
    anticipated_discharge_date: Mapped[date | None] = mapped_column(Date)
    transportation_needed: Mapped[bool | None] = mapped_column(Boolean)
    home_health_ordered: Mapped[bool | None] = mapped_column(Boolean)
    barriers_to_discharge: Mapped[list[Any] | None] = mapped_column(JSONB)
    dme_needed: Mapped[list[Any] | None] = mapped_column(JSONB)

    case: Mapped[ClinicalCase] = relationship()


class CaseFollowup(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_followups"

    followup_id: Mapped[str | None] = _external_id("followup_id")
    item: Mapped[str | None] = mapped_column(Text)
    timing: Mapped[str | None] = mapped_column(String(128))
    with_service: Mapped[str | None] = mapped_column(String(128))
    status: Mapped[str | None] = mapped_column(String(64))

    case: Mapped[ClinicalCase] = relationship()


class CaseInstruction(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_instructions"

    instruction_id: Mapped[str | None] = _external_id("instruction_id")
    category: Mapped[str | None] = mapped_column(String(64))
    instruction_text: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str | None] = mapped_column(String(64))

    case: Mapped[ClinicalCase] = relationship()


class CaseReturnPrecaution(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_return_precautions"

    precaution_id: Mapped[str | None] = _external_id("precaution_id")
    symptom: Mapped[str | None] = mapped_column(Text)
    reason: Mapped[str | None] = mapped_column(Text)
    action: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str | None] = mapped_column(String(64))
    patient_instruction: Mapped[str | None] = mapped_column(Text)

    case: Mapped[ClinicalCase] = relationship()


class CaseAnswerKey(Base, CaseChildMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "case_answer_keys"

    answer_id: Mapped[str | None] = _external_id("answer_id")
    error_family: Mapped[str | None] = mapped_column(String(64))
    error_category: Mapped[str | None] = mapped_column(String(64))
    error_description: Mapped[str | None] = mapped_column(Text)
    trigger_meds: Mapped[list[Any] | None] = mapped_column(JSONB)
    detectability_location: Mapped[str | None] = mapped_column(String(128))
    correct_action: Mapped[str | None] = mapped_column(Text)
    severity_ncc_merp: Mapped[str | None] = mapped_column(String(32))
    difficulty_a_priori: Mapped[str | None] = mapped_column(String(32))
    is_primary_error: Mapped[bool | None] = mapped_column(Boolean)
    intentional_changes: Mapped[list[Any] | None] = mapped_column(JSONB)

    case: Mapped[ClinicalCase] = relationship()
