"""Search locally stored reference rows. This does not call OpenAI or source APIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.reference import (
    search_diagnoses,
    search_lab_tests,
    search_medications,
    search_symptoms,
)

DEFAULT_SEARCH_LIMIT = 20
MAX_SEARCH_LIMIT = 100


@dataclass
class SearchPage:
    items: list[Any]
    total: int
    limit: int
    offset: int
    query: str


def _clamp(limit: int, offset: int) -> tuple[int, int]:
    if limit < 1:
        raise ValueError("limit must be a positive integer")
    if offset < 0:
        raise ValueError("offset must be >= 0")
    return min(limit, MAX_SEARCH_LIMIT), offset


def search_reference_medications(
    session: Session, query: str, *, limit: int = DEFAULT_SEARCH_LIMIT, offset: int = 0
) -> SearchPage:
    capped, start = _clamp(limit, offset)
    items, total = search_medications(session, query, limit=capped, offset=start)
    return SearchPage(items=list(items), total=total, limit=capped, offset=start, query=query)


def search_reference_labs(
    session: Session, query: str, *, limit: int = DEFAULT_SEARCH_LIMIT, offset: int = 0
) -> SearchPage:
    capped, start = _clamp(limit, offset)
    items, total = search_lab_tests(session, query, limit=capped, offset=start)
    return SearchPage(items=list(items), total=total, limit=capped, offset=start, query=query)


def search_reference_diagnoses(
    session: Session, query: str, *, limit: int = DEFAULT_SEARCH_LIMIT, offset: int = 0
) -> SearchPage:
    capped, start = _clamp(limit, offset)
    items, total = search_diagnoses(session, query, limit=capped, offset=start)
    return SearchPage(items=list(items), total=total, limit=capped, offset=start, query=query)


def search_reference_symptoms(
    session: Session, query: str, *, limit: int = DEFAULT_SEARCH_LIMIT, offset: int = 0
) -> SearchPage:
    capped, start = _clamp(limit, offset)
    items, total = search_symptoms(session, query, limit=capped, offset=start)
    return SearchPage(items=list(items), total=total, limit=capped, offset=start, query=query)
