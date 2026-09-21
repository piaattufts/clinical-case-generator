"""Command line interface.

Commands sync official terminology, bootstrap a bounded development subset, search
local reference rows, generate constrained synthetic cases, and validate them.
A full terminology import is not run by default.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from alembic import command
from alembic.config import Config

from app.database import session_scope
from app.models.reference import RefDiagnosis, RefLabTest, RefMedication, RefSymptom
from app.repositories.reference import seed_data_source_registry
from app.services.bootstrap import bootstrap_reference_data
from app.services.generation import generate_synthetic_cases, validate_persisted_cases
from app.services.reference_search import (
    search_reference_diagnoses,
    search_reference_labs,
    search_reference_medications,
    search_reference_symptoms,
)
from app.services.reference_sync import sync_icd10cm, sync_loinc, sync_rxnorm, sync_ucum
from app.sources.exceptions import (
    CaseValidationError,
    ReferenceResolutionError,
    SourceNotConfigured,
)
from app.utils.jsonio import dumps_json

cli = typer.Typer(no_args_is_help=True, add_completion=False)

LimitOption = Annotated[
    int, typer.Option(min=1, max=100, help="Maximum rows to fetch from the source.")
]
QueryOption = Annotated[
    str | None, typer.Option("--query", "-q", help="Text to search in the official source.")
]
CodeOption = Annotated[str | None, typer.Option("--code", help="Official code to look up.")]


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


@cli.command("sync-rxnorm")
def sync_rxnorm_cmd(
    name: Annotated[
        str | None, typer.Option("--name", help="Medication name to search on RxNav.")
    ] = None,
    rxcui: Annotated[str | None, typer.Option("--rxcui", help="RxNorm RXCUI to look up.")] = None,
    limit: LimitOption = 20,
) -> None:
    """Upsert RxNorm concepts by RXCUI from NLM RxNav. Does not import all of RxNorm."""
    try:
        with session_scope() as session:
            result = sync_rxnorm(session, name=name, rxcui=rxcui, limit=limit)
    except (ValueError, SourceNotConfigured) as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(
        f"RXNORM upserted {result.upserted} row(s): {', '.join(result.identifiers) or '(none)'}"
    )


@cli.command("sync-loinc")
def sync_loinc_cmd(
    query: QueryOption = None,
    code: CodeOption = None,
    limit: LimitOption = 20,
) -> None:
    """Upsert LOINC terms from the official FHIR service. Requires LOINC credentials."""
    try:
        with session_scope() as session:
            result = sync_loinc(session, query=query, code=code, limit=limit)
    except (ValueError, SourceNotConfigured) as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(
        f"LOINC upserted {result.upserted} row(s): {', '.join(result.identifiers) or '(none)'}"
    )


@cli.command("sync-ucum")
def sync_ucum_cmd(
    query: QueryOption = None,
    code: CodeOption = None,
    import_all: Annotated[
        bool,
        typer.Option("--all", help="Import every unit from the official UCUM essence file."),
    ] = False,
    limit: LimitOption = 20,
) -> None:
    """Import UCUM units from the official essence XML. Conversion factors are never invented."""
    try:
        with session_scope() as session:
            result = sync_ucum(session, query=query, code=code, import_all=import_all, limit=limit)
    except (ValueError, SourceNotConfigured) as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(
        f"UCUM upserted {result.upserted} row(s): {', '.join(result.identifiers) or '(none)'}"
    )


@cli.command("sync-icd10")
def sync_icd10_cmd(
    query: QueryOption = None,
    code: CodeOption = None,
    limit: LimitOption = 20,
) -> None:
    """Store ICD-10-CM codes and exact official descriptions. No model-generated codes."""
    try:
        with session_scope() as session:
            result = sync_icd10cm(session, query=query, code=code, limit=limit)
    except (ValueError, SourceNotConfigured) as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(
        f"ICD10CM upserted {result.upserted} row(s): {', '.join(result.identifiers) or '(none)'}"
    )


@cli.command("reference-search")
def reference_search_cmd(
    kind: Annotated[
        str,
        typer.Argument(help="One of: medications, labs, diagnoses, symptoms."),
    ],
    query: Annotated[
        str, typer.Option("--query", "-q", help="Text to match in stored reference rows.")
    ] = "",
    limit: LimitOption = 20,
    offset: Annotated[int, typer.Option(min=0)] = 0,
) -> None:
    """Search locally stored reference rows. Does not call terminology APIs or OpenAI."""
    key = kind.strip().lower()
    searchers = {
        "medications": search_reference_medications,
        "labs": search_reference_labs,
        "diagnoses": search_reference_diagnoses,
        "symptoms": search_reference_symptoms,
    }
    searcher = searchers.get(key)
    if searcher is None:
        typer.secho("kind must be medications, labs, diagnoses, or symptoms.", err=True)
        raise typer.Exit(code=2)
    with session_scope() as session:
        page = searcher(session, query, limit=limit, offset=offset)
        codes: list[str | None] = []
        for item in page.items:
            if key == "medications":
                assert isinstance(item, RefMedication)
                codes.append(item.rxcui)
            elif key == "labs":
                assert isinstance(item, RefLabTest)
                codes.append(item.loinc_code)
            elif key == "diagnoses":
                assert isinstance(item, RefDiagnosis)
                codes.append(item.icd10cm_code)
            else:
                assert isinstance(item, RefSymptom)
                codes.append(item.snomed_code)
        payload = {
            "kind": key,
            "query": page.query,
            "total": page.total,
            "limit": page.limit,
            "offset": page.offset,
            "items": [item.id for item in page.items],
            "codes": codes,
        }
    typer.echo(dumps_json(payload))


@cli.command("bootstrap-reference-data")
def bootstrap_reference_data_cmd(
    manifest: Annotated[
        Path | None,
        typer.Option("--manifest", help="JSON manifest of human-readable concept requests."),
    ] = None,
) -> None:
    """Populate a bounded development subset from official sources. Not a full import."""
    try:
        with session_scope() as session:
            result = bootstrap_reference_data(session, manifest_path=manifest)
    except (ValueError, SourceNotConfigured) as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    payload = {
        "upserted": result.upserted,
        "unresolved": [item.__dict__ for item in result.unresolved],
        "skipped": [item.__dict__ for item in result.skipped],
        "rules_enabled": result.rules_enabled,
    }
    typer.echo(dumps_json(payload))


@cli.command("generate-synthetic-cases")
def generate_synthetic_cases_cmd(
    count: Annotated[int, typer.Option("--count", min=1, max=100)] = 3,
    seed: Annotated[int, typer.Option("--seed")] = 42,
    start_index: Annotated[int, typer.Option("--start-index", min=1)] = 1,
    scenario: Annotated[
        str | None,
        typer.Option("--scenario", help="Scenario code from data/bootstrap/scenarios.json."),
    ] = None,
    inject_error: Annotated[
        bool,
        typer.Option("--inject-error/--no-inject-error"),
    ] = True,
) -> None:
    """Generate constrained synthetic cases from local reference data."""
    try:
        with session_scope() as session:
            results = generate_synthetic_cases(
                session,
                count=count,
                seed=seed,
                start_index=start_index,
                scenario_code=scenario,
                inject_error=inject_error,
            )
            payload = [
                {
                    "case_id_code": item.case_id_code,
                    "seed": item.seed,
                    "clean_passed": item.clean_passed,
                    "narrative_source": item.narrative_source,
                    "error_category": None if item.injected is None else item.injected.category,
                    "error_rxcui": None if item.injected is None else item.injected.rxcui,
                    "validation_passed": item.validation.get("passed"),
                }
                for item in results
            ]
    except (ValueError, SourceNotConfigured, CaseValidationError, ReferenceResolutionError) as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(dumps_json(payload))


@cli.command("validate-cases")
def validate_cases_cmd(
    case_id: Annotated[
        str | None,
        typer.Option("--case-id", help="Validate one SYN-000001 case id."),
    ] = None,
) -> None:
    """Run deterministic validation on persisted synthetic cases."""
    try:
        with session_scope() as session:
            reports = validate_persisted_cases(session, case_id_code=case_id)
    except CaseValidationError as exc:
        typer.secho(str(exc), err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(dumps_json(reports))


def main() -> None:
    cli()
