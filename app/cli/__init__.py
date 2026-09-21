"""Command line interface. The only Phase 1 command is db-init."""

from __future__ import annotations

from pathlib import Path

import typer
from alembic import command
from alembic.config import Config

from app.database import session_scope
from app.repositories.reference import seed_data_source_registry

cli = typer.Typer(no_args_is_help=True, add_completion=False)


def _alembic_config() -> Config:
    root = Path(__file__).resolve().parents[2]
    config = Config(str(root / "alembic.ini"))
    return config


@cli.command("db-init")
def db_init() -> None:
    """Apply Alembic migrations and ensure DataSourceRegistry metadata rows exist."""
    command.upgrade(_alembic_config(), "head")
    with session_scope() as session:
        inserted = seed_data_source_registry(session)
    typer.echo(
        "Schema is at Alembic head. "
        f"DataSourceRegistry metadata rows inserted this call: {inserted}. "
        "No clinical reference rows were loaded."
    )


def main() -> None:
    cli()
