"""Clinician-facing navigation, case maps, and archive confinement."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
BALANCED = ROOT / "data" / "case_sets" / "balanced"
SEED = ROOT / "data" / "case_sets" / "seed_guided"
OVERVIEWS = (BALANCED / "README.md", SEED / "README.md")
ARCHIVED_CODES = (
    "CLINIPROOF_TAXONOMY_V1",
    "CLINIPROOF_BALANCED_V2",
    "CLINIPROOF_BALANCED_V3",
    "CLINIPROOF_SEEDCASES_V1",
    "CLINIPROOF_SEEDCASES_V2",
)
CLINICIAN_DOCS = (
    ROOT / "data" / "README.md",
    ROOT / "data" / "case_sets" / "README.md",
    ROOT / "data" / "active_validation_sets.md",
    ROOT / "data" / "seed_cases" / "README.md",
    ROOT / "docs" / "clinician_walkthrough" / "README.md",
    ROOT / "docs" / "methods.md",
    ROOT / "docs" / "clinical_validation.md",
    *OVERVIEWS,
)
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ANSWER_NEEDLES = (
    "error_category",
    "error_family",
    "is_clean_control",
    "f1_",
    "f2_",
    "CaseAnswerKey",
    "clean_expected_state",
)


def _manifest(directory: Path) -> dict[str, object]:
    payload = json.loads((directory / "validation_manifest.json").read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _case_map_rows(text: str) -> list[str]:
    start = text.split("## Case map", 1)[1]
    end = start.split("## Dataset composition", 1)[0]
    return [
        line
        for line in end.splitlines()
        if line.startswith("| VAL-")
    ]


def test_root_navigation_names_exactly_two_current_sets() -> None:
    text = README.read_text(encoding="utf-8")
    opening = text.split("## What this repository studies", 1)[0]
    assert opening.count("data/case_sets/balanced/README.md") >= 1
    assert opening.count("data/case_sets/seed_guided/README.md") >= 1
    assert "CLINIPROOF_BALANCED_V4" in opening
    assert "CLINIPROOF_SEEDCASES_V3" in opening
    assert "VAL-701" in opening and "VAL-724" in opening
    assert "VAL-801" in opening and "VAL-824" in opening
    for code in ARCHIVED_CODES:
        assert code not in opening


def test_overviews_have_required_clinician_sections() -> None:
    for path in OVERVIEWS:
        text = path.read_text(encoding="utf-8")
        assert "## At a glance" in text
        assert "## How each case is structured" in text
        assert "## How clinicians should review these cases" in text
        assert "### C1 — Clinical plausibility" in text
        assert "### C5 — Difficulty" in text
        assert "](readable/all_cases.md)" in text
        assert "](readable/clinician_validation_packet.md)" in text
        assert "](readable/clinical_validation_worksheet.csv)" in text
        assert text.index("## Start reviewing") < text.index("## Investigator / technical material")
        rows = _case_map_rows(text)
        assert len(rows) == 24
        for needle in ANSWER_NEEDLES:
            assert needle not in text


def test_case_map_and_family_counts_match_manifests() -> None:
    for directory in (BALANCED, SEED):
        text = (directory / "README.md").read_text(encoding="utf-8")
        manifest = _manifest(directory)
        cases = manifest["cases"]
        assert isinstance(cases, list)
        ids = [str(row["validation_case_id"]) for row in cases]
        rows = _case_map_rows(text)
        assert [row.split("|")[1].strip() for row in rows] == ids
        families: dict[str, int] = {}
        for row in cases:
            scenario = str(row["scenario"])
            families[scenario] = families.get(scenario, 0) + 1
        for count in families.values():
            assert f"| {count} |" in text or f"| {count} " in text
        assert "24 distinct clinical profiles" in text
        assert "0 exact clean-case duplicates" in text


def test_archived_codes_stay_out_of_current_clinician_pages() -> None:
    for path in CLINICIAN_DOCS:
        text = path.read_text(encoding="utf-8")
        for code in ARCHIVED_CODES:
            assert code not in text, f"{path.relative_to(ROOT)} mentions {code}"


def test_clinician_markdown_links_resolve() -> None:
    files = [
        README,
        *CLINICIAN_DOCS,
        ROOT / "docs" / "README.md",
        ROOT / "docs" / "developer_guide.md",
        ROOT / "docs" / "repository_structure.md",
        ROOT / "docs" / "provenance.md",
        ROOT / "docs" / "clinician_walkthrough" / "examples" / "README.md",
        ROOT / "data" / "archive" / "validation_sets" / "README.md",
    ]
    missing: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    assert missing == []
