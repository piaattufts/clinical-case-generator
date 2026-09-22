"""Sync upsert tests against PostgreSQL. HTTP is mocked. Fixture ids use TEST_ prefix."""

from __future__ import annotations

from decimal import Decimal

import httpx
import pytest
from app.repositories.reference import (
    get_diagnosis_by_icd10cm,
    get_lab_test_by_loinc,
    get_medication_by_rxcui,
    get_unit_by_ucum,
)
from app.services.reference_sync import sync_icd10cm, sync_loinc, sync_rxnorm, sync_ucum
from app.sources.exceptions import SourceNotConfigured
from app.sources.icd10cm import Icd10CmClient
from app.sources.loinc import LoincClient
from app.sources.rxnorm import RxNormClient
from app.sources.ucum import UcumClient
from sqlalchemy.orm import Session

from tests.source_fixtures import (
    TEST_ICD,
    TEST_LOINC,
    TEST_RXCUI,
    TEST_UCUM,
    TEST_UCUM_NO_FACTOR,
    icd10cm_transport,
    loinc_transport,
    official_shaped_ucum_xml,
    rxnorm_transport,
    ucum_transport,
)


def test_sync_rxnorm_upserts_by_rxcui(db_session: Session) -> None:
    client = RxNormClient(
        client=httpx.Client(base_url="https://rxnav.nlm.nih.gov/REST", transport=rxnorm_transport())
    )
    first = sync_rxnorm(db_session, name="TEST_med", client=client)
    assert first.identifiers == [TEST_RXCUI]
    row = get_medication_by_rxcui(db_session, TEST_RXCUI)
    assert row is not None
    assert row.concept_name == "TEST_med branded product"
    assert row.ingredient == "TEST_ingredient"
    assert row.brand_name == "TEST_brand_name"
    assert row.dose_form == "TEST_dose_form"
    assert row.strength == "TEST_strength"
    assert row.strength_value is None
    assert row.source_system == "RXNORM"
    row_id = row.id
    second = sync_rxnorm(db_session, rxcui=TEST_RXCUI, client=client)
    assert second.upserted == 1
    again = get_medication_by_rxcui(db_session, TEST_RXCUI)
    assert again is not None
    assert again.id == row_id


def test_sync_rxnorm_requires_selector(db_session: Session) -> None:
    with pytest.raises(ValueError, match="Full RxNorm import"):
        sync_rxnorm(db_session)


def test_sync_loinc_upserts_official_code(db_session: Session) -> None:
    client = LoincClient(
        username="TEST_USER",
        password="TEST_PASS",
        client=httpx.Client(base_url="https://fhir.loinc.org", transport=loinc_transport()),
    )
    result = sync_loinc(db_session, query="TEST_lab", client=client)
    assert result.identifiers == [TEST_LOINC]
    row = get_lab_test_by_loinc(db_session, TEST_LOINC)
    assert row is not None
    assert row.long_common_name == "TEST_lab long name"
    assert row.component == "TEST_component"
    assert row.example_ucum_units == ["TEST_mg/dL", "TEST_mmol/L"]
    assert row.source_system == "LOINC"


def test_sync_loinc_missing_credentials_does_not_insert(
    db_session: Session, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.config import Settings

    monkeypatch.setattr(
        "app.sources.loinc.get_settings",
        lambda: Settings(loinc_username="", loinc_password=""),
    )
    with pytest.raises(SourceNotConfigured):
        sync_loinc(db_session, query="TEST_lab")
    assert get_lab_test_by_loinc(db_session, TEST_LOINC) is None


def test_sync_ucum_does_not_invent_conversion_factors(db_session: Session) -> None:
    xml_text = official_shaped_ucum_xml()
    client = UcumClient(
        client=httpx.Client(transport=ucum_transport(xml_text)),
        essence_url="https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml",
    )
    result = sync_ucum(db_session, import_all=True, client=client)
    assert set(result.identifiers) == {TEST_UCUM, TEST_UCUM_NO_FACTOR}
    with_factor = get_unit_by_ucum(db_session, TEST_UCUM)
    without_factor = get_unit_by_ucum(db_session, TEST_UCUM_NO_FACTOR)
    assert with_factor is not None
    assert without_factor is not None
    assert with_factor.conversion_factor == Decimal("9.25")
    assert without_factor.conversion_factor is None


def test_sync_ucum_requires_selector(db_session: Session) -> None:
    with pytest.raises(ValueError, match="Full UCUM import"):
        sync_ucum(db_session)


def test_sync_icd10cm_stores_exact_description(db_session: Session) -> None:
    client = Icd10CmClient(client=httpx.Client(transport=icd10cm_transport()))
    result = sync_icd10cm(db_session, query="TEST", client=client)
    assert result.identifiers == [TEST_ICD]
    row = get_diagnosis_by_icd10cm(db_session, TEST_ICD)
    assert row is not None
    assert row.icd10cm_code == TEST_ICD
    assert row.preferred_name == "TEST_exact description from source"
    assert row.snomed_code is None
    assert row.source_system == "ICD10CM"
