"""Pydantic models matching Phase 1 tables. These are not a generation pipeline."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class DataSourceRegistry(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    source_code: str
    source_name: str
    provider: str | None = None
    source_category: str | None = None
    version: str | None = None
    release_date: date | None = None
    access_type: str | None = None
    requires_credentials: bool
    license_or_terms: str | None = None
    enabled: bool
    last_sync_at: datetime | None = None
    last_successful_sync_at: datetime | None = None
    sync_status: str
    records_imported: int
    error_message: str | None = None
    metadata: Any | None = Field(
        default=None,
        validation_alias=AliasChoices("metadata", "metadata_json"),
    )
    id: UUID


class RefProcedure(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    procedure_code: str | None = None
    code_system: str | None = None
    procedure_name: str | None = None
    procedure_category: str | None = None
    body_site: str | None = None
    laterality_applicable: bool | None = None
    active: bool | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefClinicalDistribution(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    source_dataset: str | None = None
    source_dataset_version: str | None = None
    clinical_context: str | None = None
    diagnosis_code: str | None = None
    diagnosis_system: str | None = None
    age_min: int | None = None
    age_max: int | None = None
    sex: str | None = None
    care_setting: str | None = None
    variable_type: str | None = None
    variable_code: str | None = None
    variable_name: str | None = None
    unit: str | None = None
    timepoint: str | None = None
    n: int | None = None
    mean: Decimal | None = None
    sd: Decimal | None = None
    median: Decimal | None = None
    p05: Decimal | None = None
    p10: Decimal | None = None
    p25: Decimal | None = None
    p75: Decimal | None = None
    p90: Decimal | None = None
    p95: Decimal | None = None
    min_observed: Decimal | None = None
    max_observed: Decimal | None = None
    calculation_method: str | None = None
    calculated_at: datetime | None = None
    id: UUID


class RefUnit(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    ucum_code: str
    display_name: str | None = None
    quantity_type: str | None = None
    canonical_unit: str | None = None
    conversion_factor: Decimal | None = None
    active: bool | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefMedication(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    rxcui: str
    concept_name: str | None = None
    generic_name: str | None = None
    brand_name: str | None = None
    ingredient: str | None = None
    strength: str | None = None
    strength_value: Decimal | None = None
    strength_unit: str | None = None
    dose_form: str | None = None
    route: str | None = None
    term_type: str | None = None
    is_brand: bool | None = None
    is_current: bool | None = None
    prescribable: bool | None = None
    source_concept_id: str | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefDiagnosis(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    snomed_code: str | None = None
    icd10cm_code: str | None = None
    preferred_name: str | None = None
    synonyms: Any | None = None
    semantic_category: str | None = None
    parent_concept_id: str | None = None
    active: bool | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefMicrobiology(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    test_loinc_code: str | None = None
    test_name: str | None = None
    specimen: str | None = None
    organism_code: str | None = None
    organism_name: str | None = None
    result_type: str | None = None
    unit_if_applicable: str | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefLabTest(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    loinc_code: str
    long_common_name: str | None = None
    short_name: str | None = None
    component: str | None = None
    property: str | None = None
    time_aspect: str | None = None
    system_specimen: str | None = None
    scale: str | None = None
    method: str | None = None
    class_name: str | None = None
    status: str | None = None
    example_ucum_units: Any | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefDrugLabel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    set_id: str | None = None
    rxcui: str | None = None
    drug_name: str | None = None
    active_ingredient: str | None = None
    indication_text: str | None = None
    dosage_text: str | None = None
    route: str | None = None
    contraindications_text: str | None = None
    warnings_text: str | None = None
    renal_impairment_text: str | None = None
    hepatic_impairment_text: str | None = None
    geriatric_use_text: str | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefVital(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    loinc_code: str | None = None
    vital_name: str | None = None
    component: str | None = None
    measurement_site: str | None = None
    preferred_ucum_unit: str | None = None
    alternative_ucum_units: Any | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefSymptom(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    snomed_code: str | None = None
    preferred_name: str | None = None
    synonyms: Any | None = None
    body_system: str | None = None
    semantic_category: str | None = None
    active: bool | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None


class RefDevice(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    device_identifier: str | None = None
    device_name: str | None = None
    brand_name: str | None = None
    company_name: str | None = None
    device_description: str | None = None
    device_category: str | None = None
    device_term: str | None = None
    implantable: bool | None = None
    single_use: bool | None = None
    sterile: bool | None = None
    active: bool | None = None
    id: UUID
    source_system: str | None = None
    source_version: str | None = None
    retrieved_at: datetime | None = None
