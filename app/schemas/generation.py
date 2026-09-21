"""Pydantic models matching Phase 1 tables. These are not a generation pipeline."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CaseBlueprint(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    blueprint_id: str | None = None
    specialty: str | None = None
    primary_diagnosis_ref_id: UUID | None = None
    age_min: int | None = None
    age_max: int | None = None
    sex: str | None = None
    hospital_day: int | None = None
    difficulty: str | None = None
    target_home_med_count: int | None = None
    target_problem_count: int | None = None
    clean_case: bool | None = None
    target_error_category: str | None = None
    target_error_medication_class: str | None = None
    settings: Any | None = None
    created_at: datetime
    id: UUID


class CaseGenerationRun(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    run_id: str | None = None
    blueprint_id: UUID
    case_id: UUID | None = None
    model_name: str | None = None
    prompt_version: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    status: str | None = None
    validation_status: str | None = None
    error_message: str | None = None
    token_usage: Any | None = None
    metadata: Any | None = Field(
        default=None,
        validation_alias=AliasChoices("metadata", "metadata_json"),
    )
    id: UUID


class CaseMedicationPlan(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    plan_id: str | None = None
    case_id: UUID
    ref_medication_id: UUID | None = None
    drug: str | None = None
    home_state: str | None = None
    inpatient_state: str | None = None
    correct_discharge_state: str | None = None
    decision: str | None = None
    decision_reason: str | None = None
    is_error_target: bool
    id: UUID
