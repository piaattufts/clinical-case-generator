"""Generation tracking tables. Phase 1 does not generate cases or call a model.

CaseGenerationRun.blueprint_id is the UUID foreign key to case_blueprints.id.
The human blueprint code is the separate nullable string case_blueprints.blueprint_id.
A later phase may store random_seed inside CaseGenerationRun.metadata. It is not a column.

CaseMedicationPlan is the correct plan before any planted error. No rows are seeded.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, UUIDPrimaryKeyMixin
from app.models.cases import ClinicalCase

_PLAN_DECISION = (
    "decision IS NULL OR decision IN "
    "('continue', 'stop', 'restart', 'hold', 'dose_change', 'new_start')"
)


class CaseBlueprint(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "case_blueprints"

    blueprint_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    specialty: Mapped[str | None] = mapped_column(String(128))
    primary_diagnosis_ref_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ref_diagnoses.id", ondelete="RESTRICT"),
        index=True,
    )
    age_min: Mapped[int | None] = mapped_column(Integer)
    age_max: Mapped[int | None] = mapped_column(Integer)
    sex: Mapped[str | None] = mapped_column(String(32))
    hospital_day: Mapped[int | None] = mapped_column(Integer)
    difficulty: Mapped[str | None] = mapped_column(String(64))
    target_home_med_count: Mapped[int | None] = mapped_column(Integer)
    target_problem_count: Mapped[int | None] = mapped_column(Integer)
    clean_case: Mapped[bool | None] = mapped_column(Boolean)
    target_error_category: Mapped[str | None] = mapped_column(String(64))
    target_error_medication_class: Mapped[str | None] = mapped_column(String(128))
    settings: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
    )


class CaseGenerationRun(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "case_generation_runs"

    run_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    blueprint_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("case_blueprints.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    case_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("clinical_cases.id", ondelete="SET NULL"),
        index=True,
    )
    model_name: Mapped[str | None] = mapped_column(String(128))
    prompt_version: Mapped[str | None] = mapped_column(String(64))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str | None] = mapped_column(String(64))
    validation_status: Mapped[str | None] = mapped_column(String(64))
    error_message: Mapped[str | None] = mapped_column(Text)
    token_usage: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB)

    blueprint: Mapped[CaseBlueprint] = relationship()
    case: Mapped[ClinicalCase | None] = relationship()


class CaseMedicationPlan(Base, UUIDPrimaryKeyMixin):
    """Correct medication transition before planted errors. decision is constrained."""

    __tablename__ = "case_medication_plans"
    __table_args__ = (CheckConstraint(_PLAN_DECISION, name="decision_values"),)

    plan_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    case_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clinical_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ref_medication_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ref_medications.id", ondelete="RESTRICT"),
        index=True,
    )
    drug: Mapped[str | None] = mapped_column(String(512))
    home_state: Mapped[str | None] = mapped_column(String(64))
    inpatient_state: Mapped[str | None] = mapped_column(String(64))
    correct_discharge_state: Mapped[str | None] = mapped_column(String(64))
    decision: Mapped[str | None] = mapped_column(String(32))
    decision_reason: Mapped[str | None] = mapped_column(Text)
    is_error_target: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
    )

    case: Mapped[ClinicalCase] = relationship()
