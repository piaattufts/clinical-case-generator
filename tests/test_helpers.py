"""Unit tests for Phase 1 helpers and schema/table parity. No database required."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import app.models  # noqa: F401
import app.schemas as schemas
import pytest
from app.database import Base
from app.schemas.reference import DataSourceRegistry
from app.utils.identifiers import (
    format_case_id_code,
    format_child_business_id,
    format_validation_case_id,
    format_validation_child_id,
)
from app.utils.jsonio import dumps_json, loads_json
from app.utils.provenance import build_provenance
from app.utils.units import normalize_unit_text


def test_case_and_child_id_formats() -> None:
    assert format_case_id_code(1) == "SYN-000001"
    assert format_child_business_id("DX", "SYN-000001", 1) == "DX-SYN000001-001"
    assert format_child_business_id("SYM", "SYN-000001", 12) == "SYM-SYN000001-012"
    assert format_validation_case_id(1) == "VAL-001"
    assert format_validation_child_id("DX", "VAL-001", 1) == "DX-VAL001-001"
    with pytest.raises(ValueError):
        format_case_id_code(0)
    with pytest.raises(ValueError):
        format_child_business_id("DX", "CASE-1", 1)
    with pytest.raises(ValueError):
        format_validation_child_id("DX", "SYN-000001", 1)


def test_provenance_requires_timezone() -> None:
    payload = build_provenance("RxNorm", "2026-01")
    assert payload["source_system"] == "RxNorm"
    retrieved = payload["retrieved_at"]
    assert isinstance(retrieved, datetime)
    assert retrieved.tzinfo is not None
    with pytest.raises(ValueError):
        build_provenance("RxNorm", retrieved_at=datetime(2026, 1, 1))


def test_blank_unit_text_is_null() -> None:
    assert normalize_unit_text("  mg/dL ") == "mg/dL"
    assert normalize_unit_text("   ") is None
    assert normalize_unit_text(None) is None


def test_json_helpers_round_trip_phase1_types() -> None:
    when = datetime(2026, 1, 2, 3, 4, tzinfo=UTC)
    encoded = dumps_json({"id": uuid.UUID("11111111-1111-1111-1111-111111111111"), "at": when})
    assert loads_json(encoded)["at"].startswith("2026-01-02T03:04:00")
    with pytest.raises(ValueError):
        dumps_json({"at": datetime(2026, 1, 1)})


def test_pydantic_fields_match_table_columns() -> None:
    for mapper in Base.registry.mappers:
        schema = getattr(schemas, mapper.class_.__name__)
        column_names = {column.name for column in mapper.local_table.columns}
        assert set(schema.model_fields) == column_names


def test_registry_schema_reads_metadata_attribute() -> None:
    source = SimpleNamespace(
        id=uuid.uuid4(),
        source_code="RXNORM",
        source_name="RxNorm",
        provider=None,
        source_category=None,
        version=None,
        release_date=None,
        access_type=None,
        requires_credentials=False,
        license_or_terms=None,
        enabled=True,
        last_sync_at=None,
        last_successful_sync_at=None,
        sync_status="never_synced",
        records_imported=0,
        error_message=None,
        metadata_json={"required_env": []},
    )
    parsed = DataSourceRegistry.model_validate(source)
    assert parsed.metadata == {"required_env": []}
