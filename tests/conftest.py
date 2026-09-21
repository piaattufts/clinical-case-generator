"""Session-scoped PostgreSQL migration for constraint tests."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from app.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    settings = get_settings()
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))
    return config


@pytest.fixture(scope="session")
def engine(alembic_config: Config) -> Iterator[Engine]:
    settings = get_settings()
    database = create_engine(settings.database_url, pool_pre_ping=True)
    command.upgrade(alembic_config, "head")
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")
    yield database
    database.dispose()


@pytest.fixture
def db_session(engine: Engine) -> Iterator[Session]:
    session = Session(bind=engine, expire_on_commit=False)
    try:
        yield session
    finally:
        session.rollback()
        session.close()
