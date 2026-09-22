"""FastAPI database session dependency."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.database import get_session_factory


def get_session() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
