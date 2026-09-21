"""CLI tests for Phase 2 commands. HTTP is not called; full import is not the default."""

from __future__ import annotations

import ast
from pathlib import Path

from app.cli import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_lists_phase2_commands() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    output = result.output
    assert "sync-rxnorm" in output
    assert "sync-loinc" in output
    assert "sync-ucum" in output
    assert "sync-icd10" in output
    assert "reference-search" in output
    assert "bootstrap-reference-data" in output
    assert "generate-synthetic-cases" in output
    assert "validate-cases" in output
    assert "sync-all" not in output


def test_sync_commands_require_a_selector() -> None:
    rxnorm = runner.invoke(cli, ["sync-rxnorm"])
    assert rxnorm.exit_code == 2
    assert "Full RxNorm import" in rxnorm.output

    loinc = runner.invoke(cli, ["sync-loinc"])
    assert loinc.exit_code == 2
    assert "Full LOINC import" in loinc.output or "not configured" in loinc.output

    ucum = runner.invoke(cli, ["sync-ucum"])
    assert ucum.exit_code == 2
    assert "Full UCUM import" in ucum.output

    icd10 = runner.invoke(cli, ["sync-icd10"])
    assert icd10.exit_code == 2
    assert "Full ICD-10-CM import" in icd10.output


def test_reference_search_rejects_unknown_kind() -> None:
    result = runner.invoke(cli, ["reference-search", "devices", "--query", "TEST_"])
    assert result.exit_code == 2
    assert "medications" in result.output


def test_phase2_modules_do_not_import_openai() -> None:
    roots = [
        Path("app/sources"),
        Path("app/services"),
        Path("app/api"),
        Path("app/cli"),
    ]
    for root in roots:
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    assert all(not alias.name.startswith("openai") for alias in node.names), path
                if isinstance(node, ast.ImportFrom) and node.module:
                    assert not node.module.startswith("openai"), path


def test_phase1_alembic_revision_is_unchanged() -> None:
    phase1 = Path("alembic/versions/1c236aeaadc7_phase_1_clinical_schema.py")
    text = phase1.read_text(encoding="utf-8")
    assert "revision: str = '1c236aeaadc7'" in text
    assert "down_revision: str | None = None" in text
    new_revision = Path("alembic/versions/7b9e4c21d6a0_clinical_rules.py")
    added = new_revision.read_text(encoding="utf-8")
    assert 'revision: str = "7b9e4c21d6a0"' in added
    assert 'down_revision: str | None = "1c236aeaadc7"' in added
    names = sorted(path.name for path in Path("alembic/versions").glob("*.py"))
    assert names == [
        "1c236aeaadc7_phase_1_clinical_schema.py",
        "7b9e4c21d6a0_clinical_rules.py",
    ]
