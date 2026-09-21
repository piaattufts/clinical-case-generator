"""Authoritative reference tables and locally calculated aggregate statistics.

Phase 1 creates these tables and does not load clinical concepts. Do not insert
invented RxNorm, LOINC, SNOMED, ICD-10-CM, UCUM, or device identifiers.

RefClinicalDistribution stores aggregate statistics only. Raw MIMIC patient rows,
notes, identifiers, and events must never be sent to OpenAI. Only locally calculated
aggregates may be stored here. Never label aggregates as real patient data.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, ProvenanceMixin, UUIDPrimaryKeyMixin

# SQLAlchemy reserves the Declarative attribute name "metadata".
JsonObject = dict[str, Any]


class DataSourceRegistry(Base, UUIDPrimaryKeyMixin):
    """Registry of external sources. Rows are metadata, not clinical concepts."""

    __tablename__ = "data_source_registry"
    __table_args__ = (CheckConstraint("btrim(source_code) <> ''", name="source_code_not_blank"),)

    source_code: Mapped[str] = mapped_column(String(32), unique=True)
    source_name: Mapped[str] = mapped_column(String(256))
    provider: Mapped[str | None] = mapped_column(String(256))
    source_category: Mapped[str | None] = mapped_column(String(64))
    version: Mapped[str | None] = mapped_column(String(64))
    release_date: Mapped[date | None] = mapped_column(Date)
    access_type: Mapped[str | None] = mapped_column(String(64))
    requires_credentials: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    license_or_terms: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_successful_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sync_status: Mapped[str] = mapped_column(
        String(32), default="never_synced", server_default=text("'never_synced'")
    )
    records_imported: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[JsonObject | None] = mapped_column("metadata", JSONB)


class RefMedication(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """RxNorm concept. rxcui is the authoritative identifier, separate from id."""

    __tablename__ = "ref_medications"
    __table_args__ = (
        CheckConstraint("btrim(rxcui) <> ''", name="rxcui_not_blank"),
        Index("ix_ref_medications_generic_name", "generic_name"),
        Index("ix_ref_medications_ingredient", "ingredient"),
        Index("ix_ref_medications_concept_name", "concept_name"),
    )

    rxcui: Mapped[str] = mapped_column(String(64), unique=True)
    concept_name: Mapped[str | None] = mapped_column(String(512))
    generic_name: Mapped[str | None] = mapped_column(String(512))
    brand_name: Mapped[str | None] = mapped_column(String(512))
    ingredient: Mapped[str | None] = mapped_column(String(512))
    strength: Mapped[str | None] = mapped_column(String(128))
    strength_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    strength_unit: Mapped[str | None] = mapped_column(String(64))
    dose_form: Mapped[str | None] = mapped_column(String(128))
    route: Mapped[str | None] = mapped_column(String(128))
    term_type: Mapped[str | None] = mapped_column(String(32))
    is_brand: Mapped[bool | None] = mapped_column(Boolean)
    is_current: Mapped[bool | None] = mapped_column(Boolean)
    prescribable: Mapped[bool | None] = mapped_column(Boolean)
    source_concept_id: Mapped[str | None] = mapped_column(String(64))


class RefDrugLabel(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """DailyMed label text. rxcui is a string, not a foreign key to ref_medications."""

    __tablename__ = "ref_drug_labels"
    __table_args__ = (
        Index("ix_ref_drug_labels_rxcui", "rxcui"),
        Index("ix_ref_drug_labels_drug_name", "drug_name"),
        Index("ix_ref_drug_labels_set_id", "set_id"),
    )

    set_id: Mapped[str | None] = mapped_column(String(64))
    rxcui: Mapped[str | None] = mapped_column(String(64))
    drug_name: Mapped[str | None] = mapped_column(String(512))
    active_ingredient: Mapped[str | None] = mapped_column(Text)
    indication_text: Mapped[str | None] = mapped_column(Text)
    dosage_text: Mapped[str | None] = mapped_column(Text)
    route: Mapped[str | None] = mapped_column(String(128))
    contraindications_text: Mapped[str | None] = mapped_column(Text)
    warnings_text: Mapped[str | None] = mapped_column(Text)
    renal_impairment_text: Mapped[str | None] = mapped_column(Text)
    hepatic_impairment_text: Mapped[str | None] = mapped_column(Text)
    geriatric_use_text: Mapped[str | None] = mapped_column(Text)


class RefDiagnosis(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """Diagnosis concept. SNOMED CT and ICD-10-CM are not one-to-one.

    parent_concept_id is the external terminology id, not a foreign key to this table.
    """

    __tablename__ = "ref_diagnoses"
    __table_args__ = (
        CheckConstraint(
            "(snomed_code IS NOT NULL AND btrim(snomed_code) <> '') "
            "OR (icd10cm_code IS NOT NULL AND btrim(icd10cm_code) <> '')",
            name="has_snomed_or_icd10",
        ),
        Index("ix_ref_diagnoses_snomed_code", "snomed_code"),
        Index("ix_ref_diagnoses_icd10cm_code", "icd10cm_code"),
    )

    snomed_code: Mapped[str | None] = mapped_column(String(32))
    icd10cm_code: Mapped[str | None] = mapped_column(String(16))
    preferred_name: Mapped[str | None] = mapped_column(String(512))
    synonyms: Mapped[list[Any] | None] = mapped_column(JSONB)
    semantic_category: Mapped[str | None] = mapped_column(String(128))
    parent_concept_id: Mapped[str | None] = mapped_column(String(64))
    active: Mapped[bool | None] = mapped_column(Boolean)


class RefSymptom(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """Symptom concept. snomed_code may be null until a real code is linked. Do not invent one."""

    __tablename__ = "ref_symptoms"

    snomed_code: Mapped[str | None] = mapped_column(String(32), index=True)
    preferred_name: Mapped[str | None] = mapped_column(String(512))
    synonyms: Mapped[list[Any] | None] = mapped_column(JSONB)
    body_system: Mapped[str | None] = mapped_column(String(128))
    semantic_category: Mapped[str | None] = mapped_column(String(128))
    active: Mapped[bool | None] = mapped_column(Boolean)


class RefLabTest(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """LOINC lab test. loinc_code is the authoritative identifier."""

    __tablename__ = "ref_lab_tests"
    __table_args__ = (CheckConstraint("btrim(loinc_code) <> ''", name="loinc_code_not_blank"),)

    loinc_code: Mapped[str] = mapped_column(String(64), unique=True)
    long_common_name: Mapped[str | None] = mapped_column(String(512))
    short_name: Mapped[str | None] = mapped_column(String(256))
    component: Mapped[str | None] = mapped_column(String(256))
    property: Mapped[str | None] = mapped_column(String(64))
    time_aspect: Mapped[str | None] = mapped_column(String(64))
    system_specimen: Mapped[str | None] = mapped_column(String(128))
    scale: Mapped[str | None] = mapped_column(String(64))
    method: Mapped[str | None] = mapped_column(String(128))
    class_name: Mapped[str | None] = mapped_column(String(128))
    status: Mapped[str | None] = mapped_column(String(64))
    example_ucum_units: Mapped[list[Any] | None] = mapped_column(JSONB)


class RefUnit(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """UCUM unit. ucum_code is the authoritative identifier. No conversion table is seeded."""

    __tablename__ = "ref_units"
    __table_args__ = (CheckConstraint("btrim(ucum_code) <> ''", name="ucum_code_not_blank"),)

    ucum_code: Mapped[str] = mapped_column(String(64), unique=True)
    display_name: Mapped[str | None] = mapped_column(String(256))
    quantity_type: Mapped[str | None] = mapped_column(String(128))
    canonical_unit: Mapped[str | None] = mapped_column(String(64))
    conversion_factor: Mapped[Decimal | None] = mapped_column(Numeric(24, 12))
    active: Mapped[bool | None] = mapped_column(Boolean)


class RefVital(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """Vital sign concept. No normal ranges are stored or seeded."""

    __tablename__ = "ref_vitals"

    loinc_code: Mapped[str | None] = mapped_column(String(64), index=True)
    vital_name: Mapped[str | None] = mapped_column(String(256))
    component: Mapped[str | None] = mapped_column(String(256))
    measurement_site: Mapped[str | None] = mapped_column(String(128))
    preferred_ucum_unit: Mapped[str | None] = mapped_column(String(64))
    alternative_ucum_units: Mapped[list[Any] | None] = mapped_column(JSONB)


class RefProcedure(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    __tablename__ = "ref_procedures"

    procedure_code: Mapped[str | None] = mapped_column(String(64), index=True)
    code_system: Mapped[str | None] = mapped_column(String(64), index=True)
    procedure_name: Mapped[str | None] = mapped_column(String(512))
    procedure_category: Mapped[str | None] = mapped_column(String(128))
    body_site: Mapped[str | None] = mapped_column(String(128))
    laterality_applicable: Mapped[bool | None] = mapped_column(Boolean)
    active: Mapped[bool | None] = mapped_column(Boolean)


class RefDevice(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    """Device concept.

    device_identifier is nullable so a generic concept need not carry a fake UDI.
    """

    __tablename__ = "ref_devices"

    device_identifier: Mapped[str | None] = mapped_column(String(128), index=True)
    device_name: Mapped[str | None] = mapped_column(String(512))
    brand_name: Mapped[str | None] = mapped_column(String(256))
    company_name: Mapped[str | None] = mapped_column(String(256))
    device_description: Mapped[str | None] = mapped_column(Text)
    device_category: Mapped[str | None] = mapped_column(String(128))
    device_term: Mapped[str | None] = mapped_column(String(256))
    implantable: Mapped[bool | None] = mapped_column(Boolean)
    single_use: Mapped[bool | None] = mapped_column(Boolean)
    sterile: Mapped[bool | None] = mapped_column(Boolean)
    active: Mapped[bool | None] = mapped_column(Boolean)


class RefMicrobiology(Base, UUIDPrimaryKeyMixin, ProvenanceMixin):
    __tablename__ = "ref_microbiology"

    test_loinc_code: Mapped[str | None] = mapped_column(String(64), index=True)
    test_name: Mapped[str | None] = mapped_column(String(512))
    specimen: Mapped[str | None] = mapped_column(String(128))
    organism_code: Mapped[str | None] = mapped_column(String(64), index=True)
    organism_name: Mapped[str | None] = mapped_column(String(512))
    result_type: Mapped[str | None] = mapped_column(String(64))
    unit_if_applicable: Mapped[str | None] = mapped_column(String(64))


class RefClinicalDistribution(Base, UUIDPrimaryKeyMixin):
    """Aggregate statistics calculated locally. This is not a patient table.

    Raw MIMIC patient rows, notes, identifiers, and events must never be sent to
    OpenAI. Only locally calculated aggregates may be stored here. Never label
    aggregates as real patient data. Rows with source_dataset MIMIC_IV_RAW are rejected.
    """

    __tablename__ = "ref_clinical_distributions"
    __table_args__ = (
        CheckConstraint(
            "source_dataset IS NULL OR source_dataset <> 'MIMIC_IV_RAW'",
            name="no_raw_mimic_dataset",
        ),
        Index(
            "uq_ref_clinical_distributions_aggregate",
            "source_dataset",
            "clinical_context",
            "variable_code",
            "age_min",
            "age_max",
            "sex",
            "care_setting",
            "timepoint",
            unique=True,
            postgresql_nulls_not_distinct=True,
        ),
    )

    source_dataset: Mapped[str | None] = mapped_column(String(64))
    source_dataset_version: Mapped[str | None] = mapped_column(String(64))
    clinical_context: Mapped[str | None] = mapped_column(String(128))
    diagnosis_code: Mapped[str | None] = mapped_column(String(32))
    diagnosis_system: Mapped[str | None] = mapped_column(String(32))
    age_min: Mapped[int | None] = mapped_column(Integer)
    age_max: Mapped[int | None] = mapped_column(Integer)
    sex: Mapped[str | None] = mapped_column(String(32))
    care_setting: Mapped[str | None] = mapped_column(String(64))
    variable_type: Mapped[str | None] = mapped_column(String(64))
    variable_code: Mapped[str | None] = mapped_column(String(64))
    variable_name: Mapped[str | None] = mapped_column(String(256))
    unit: Mapped[str | None] = mapped_column(String(64))
    timepoint: Mapped[str | None] = mapped_column(String(64))
    n: Mapped[int | None] = mapped_column(Integer)
    mean: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    sd: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    median: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    p05: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    p10: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    p25: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    p75: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    p90: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    p95: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    min_observed: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    max_observed: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    calculation_method: Mapped[str | None] = mapped_column(String(128))
    calculated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
