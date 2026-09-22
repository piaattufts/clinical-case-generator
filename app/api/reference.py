"""Reference search API. Reads locally stored terminology rows only."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.schemas.reference import (
    DiagnosisSearchPage,
    LabSearchPage,
    MedicationSearchPage,
    SymptomSearchPage,
)
from app.services.reference_search import (
    search_reference_diagnoses,
    search_reference_labs,
    search_reference_medications,
    search_reference_symptoms,
)

router = APIRouter(prefix="/reference", tags=["reference"])


@router.get("/medications", response_model=MedicationSearchPage)
def get_medications(
    session: Annotated[Session, Depends(get_session)],
    query: str = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> MedicationSearchPage:
    page = search_reference_medications(session, query, limit=limit, offset=offset)
    return MedicationSearchPage(
        items=page.items,
        total=page.total,
        limit=page.limit,
        offset=page.offset,
        query=page.query,
    )


@router.get("/labs", response_model=LabSearchPage)
def get_labs(
    session: Annotated[Session, Depends(get_session)],
    query: str = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> LabSearchPage:
    page = search_reference_labs(session, query, limit=limit, offset=offset)
    return LabSearchPage(
        items=page.items,
        total=page.total,
        limit=page.limit,
        offset=page.offset,
        query=page.query,
    )


@router.get("/diagnoses", response_model=DiagnosisSearchPage)
def get_diagnoses(
    session: Annotated[Session, Depends(get_session)],
    query: str = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> DiagnosisSearchPage:
    page = search_reference_diagnoses(session, query, limit=limit, offset=offset)
    return DiagnosisSearchPage(
        items=page.items,
        total=page.total,
        limit=page.limit,
        offset=page.offset,
        query=page.query,
    )


@router.get("/symptoms", response_model=SymptomSearchPage)
def get_symptoms(
    session: Annotated[Session, Depends(get_session)],
    query: str = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> SymptomSearchPage:
    page = search_reference_symptoms(session, query, limit=limit, offset=offset)
    return SymptomSearchPage(
        items=page.items,
        total=page.total,
        limit=page.limit,
        offset=page.offset,
        query=page.query,
    )
