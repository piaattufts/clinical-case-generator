"""Terminology client tests. HTTP is mocked. Fixture ids use the TEST_ prefix only."""

from __future__ import annotations

from decimal import Decimal

import httpx
import pytest
from app.sources.exceptions import SourceHttpError, SourceNotConfigured
from app.sources.icd10cm import Icd10CmClient
from app.sources.loinc import LoincClient
from app.sources.rxnorm import RxNormClient
from app.sources.ucum import UcumClient, parse_essence_xml
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
    tracking_transport,
    ucum_transport,
)


def test_rxnorm_search_lookup_properties_and_related() -> None:
    client = RxNormClient(
        client=httpx.Client(base_url="https://rxnav.nlm.nih.gov/REST", transport=rxnorm_transport())
    )
    matches = client.search_by_name("TEST_med")
    assert [item.rxcui for item in matches] == [TEST_RXCUI]
    looked_up = client.lookup_by_rxcui(TEST_RXCUI)
    assert looked_up is not None
    assert looked_up.rxcui == TEST_RXCUI
    assert looked_up.name == "TEST_med branded product"
    props = client.properties(TEST_RXCUI)
    assert props["AVAILABLE_STRENGTH"] == "TEST_strength"
    related = client.related_concepts(TEST_RXCUI)
    assert {item.rxcui for item in related} >= {"TEST_RXCUI_IN", "TEST_RXCUI_BN", "TEST_RXCUI_DF"}
    assert client.version() == "TEST_RXNORM_VERSION"


def test_rxnorm_name_search_requires_text() -> None:
    client = RxNormClient(
        client=httpx.Client(base_url="https://rxnav.nlm.nih.gov/REST", transport=rxnorm_transport())
    )
    with pytest.raises(ValueError):
        client.search_by_name("  ")


def test_loinc_missing_credentials_raises_without_http() -> None:
    calls: list[str] = []
    with pytest.raises(SourceNotConfigured) as exc_info:
        LoincClient(
            username="",
            password="",
            transport=tracking_transport(calls),
        )
    assert "LOINC_USERNAME" in str(exc_info.value)
    assert "LOINC_PASSWORD" in str(exc_info.value)
    assert "generated fallback" in str(exc_info.value)
    assert calls == []


def test_loinc_lookup_and_filtered_search() -> None:
    client = LoincClient(
        username="TEST_USER",
        password="TEST_PASS",
        client=httpx.Client(
            base_url="https://fhir.loinc.org",
            transport=loinc_transport(),
            headers={"Accept": "application/fhir+json"},
        ),
    )
    concept = client.lookup_by_code(TEST_LOINC)
    assert concept is not None
    assert concept.loinc_code == TEST_LOINC
    assert concept.long_common_name == "TEST_lab long name"
    assert concept.component == "TEST_component"
    assert concept.example_ucum_units == ["TEST_mg/dL", "TEST_mmol/L"]
    hits = client.search_by_name("TEST_lab", count=5)
    assert [item.loinc_code for item in hits] == [TEST_LOINC]


def test_loinc_search_refuses_unfiltered_dump() -> None:
    client = LoincClient(
        username="TEST_USER",
        password="TEST_PASS",
        client=httpx.Client(base_url="https://fhir.loinc.org", transport=loinc_transport()),
    )
    with pytest.raises(ValueError, match="full LOINC import"):
        client.search_by_name(" ")


def test_ucum_copies_official_factor_and_does_not_invent_missing() -> None:
    xml_text = official_shaped_ucum_xml()
    units = parse_essence_xml(xml_text)
    by_code = {unit.ucum_code: unit for unit in units}
    assert TEST_UCUM in by_code
    assert TEST_UCUM_NO_FACTOR in by_code
    assert "TEST_k" not in by_code
    assert by_code[TEST_UCUM].conversion_factor == Decimal("9.25")
    assert by_code[TEST_UCUM].canonical_unit == "TEST_CANON"
    assert by_code[TEST_UCUM_NO_FACTOR].conversion_factor is None
    client = UcumClient(
        client=httpx.Client(transport=ucum_transport(xml_text)),
        essence_url="https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml",
    )
    fetched = client.search_units("TEST_U1")
    assert [unit.ucum_code for unit in fetched] == [TEST_UCUM]


def test_ucum_search_requires_query() -> None:
    client = UcumClient(client=httpx.Client(transport=ucum_transport(official_shaped_ucum_xml())))
    with pytest.raises(ValueError, match="full UCUM import"):
        client.search_units(" ")


def test_icd10cm_stores_exact_description() -> None:
    client = Icd10CmClient(client=httpx.Client(transport=icd10cm_transport()))
    matches = client.search("TEST")
    assert len(matches) == 1
    assert matches[0].icd10cm_code == TEST_ICD
    assert matches[0].description == "TEST_exact description from source"
    looked_up = client.lookup_by_code(TEST_ICD)
    assert looked_up is not None
    assert looked_up.description == "TEST_exact description from source"


def test_icd10cm_http_error_is_not_a_generated_code() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="TEST_upstream")

    client = Icd10CmClient(client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(SourceHttpError):
        client.search("TEST")


def test_conditions_and_dailymed_parse_source_payloads() -> None:
    from app.sources.conditions import ConditionsClient
    from app.sources.dailymed import DailyMedClient
    from tests.source_fixtures import (
        TEST_SET_ID,
        TEST_SYMPTOM_NAME,
        conditions_transport,
        dailymed_transport,
    )

    conditions = ConditionsClient(client=httpx.Client(transport=conditions_transport()))
    hits = conditions.search("TEST_symptom")
    assert hits[0].name == TEST_SYMPTOM_NAME
    assert TEST_ICD in hits[0].icd10cm_codes
    labels = DailyMedClient(client=httpx.Client(transport=dailymed_transport())).labels_for_rxcui(
        TEST_RXCUI
    )
    assert labels[0].set_id == TEST_SET_ID
    assert labels[0].warnings_text is not None
    assert "anticoagulant" in labels[0].warnings_text.casefold()
