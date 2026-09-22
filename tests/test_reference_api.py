"""GET /reference search API. Fixture ids use the TEST_ prefix only."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from app.api.deps import get_session
from app.main import app
from app.models.reference import RefDiagnosis, RefLabTest, RefMedication, RefSymptom
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.source_fixtures import TEST_ICD, TEST_LOINC, TEST_RXCUI, TEST_SYMPTOM_NAME


@pytest.fixture
def api_client(db_session: Session) -> Iterator[TestClient]:
    def override_session() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_session] = override_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_session, None)


def test_health_still_ok(api_client: TestClient) -> None:
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_reference_search_medications_labs_diagnoses_symptoms(
    db_session: Session, api_client: TestClient
) -> None:
    db_session.add(
        RefMedication(
            rxcui=TEST_RXCUI,
            concept_name="TEST_med branded product",
            generic_name="TEST_ingredient",
        )
    )
    db_session.add(RefLabTest(loinc_code=TEST_LOINC, long_common_name="TEST_lab long name"))
    db_session.add(
        RefDiagnosis(icd10cm_code=TEST_ICD, preferred_name="TEST_exact description from source")
    )
    db_session.add(RefSymptom(preferred_name=TEST_SYMPTOM_NAME, snomed_code=None))
    db_session.flush()

    medications = api_client.get(
        "/reference/medications", params={"query": "TEST_med", "limit": 10, "offset": 0}
    )
    assert medications.status_code == 200
    body = medications.json()
    assert body["total"] == 1
    assert body["query"] == "TEST_med"
    assert body["items"][0]["rxcui"] == TEST_RXCUI

    labs = api_client.get("/reference/labs", params={"query": "TEST_lab", "limit": 10, "offset": 0})
    assert labs.status_code == 200
    assert labs.json()["items"][0]["loinc_code"] == TEST_LOINC

    diagnoses = api_client.get(
        "/reference/diagnoses", params={"query": TEST_ICD, "limit": 10, "offset": 0}
    )
    assert diagnoses.status_code == 200
    assert diagnoses.json()["items"][0]["preferred_name"] == "TEST_exact description from source"
    assert diagnoses.json()["items"][0]["icd10cm_code"] == TEST_ICD

    symptoms = api_client.get(
        "/reference/symptoms", params={"query": "TEST_symptom", "limit": 10, "offset": 0}
    )
    assert symptoms.status_code == 200
    assert symptoms.json()["items"][0]["preferred_name"] == TEST_SYMPTOM_NAME
    assert symptoms.json()["items"][0]["snomed_code"] is None


def test_reference_search_pagination(db_session: Session, api_client: TestClient) -> None:
    db_session.add(RefMedication(rxcui="TEST_RXCUI_A", concept_name="TEST_alpha"))
    db_session.add(RefMedication(rxcui="TEST_RXCUI_B", concept_name="TEST_beta"))
    db_session.flush()
    page = api_client.get(
        "/reference/medications", params={"query": "TEST_", "limit": 1, "offset": 0}
    )
    assert page.status_code == 200
    payload = page.json()
    assert payload["total"] == 2
    assert payload["limit"] == 1
    assert len(payload["items"]) == 1
    second = api_client.get(
        "/reference/medications", params={"query": "TEST_", "limit": 1, "offset": 1}
    )
    assert second.json()["items"][0]["rxcui"] != payload["items"][0]["rxcui"]
