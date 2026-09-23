"""Readable clinician teaching charts are separate from blinded VAL study cases."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WALKTHROUGH = ROOT / "docs" / "clinician_walkthrough"
EXAMPLES = WALKTHROUGH / "examples"
SOURCE = WALKTHROUGH / "source_json"
README = WALKTHROUGH / "README.md"
CLEAN = EXAMPLES / "clean_heart_failure_case.md"
OMISSION = EXAMPLES / "heart_failure_omission_case.md"
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ACTIVE_VAL = {f"VAL-{index:03d}" for index in range(701, 725)} | {
    f"VAL-{index:03d}" for index in range(801, 825)
}
CURATED = {
    "furosemide": "FUROSEMIDE_40_DAILY",
    "lisinopril": "LISINOPRIL_10_DAILY",
    "spironolactone": "SPIRONOLACTONE_HF_25",
}
CHART_ANSWER_CUES = (
    "deliberately omitted",
    "this medication should be stopped",
    "this is the correct dose",
    "no outpatient continuation",
    "this is the intended problem",
    "f1_omission",
    "error_category",
)


def _load(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(path.name)
    return payload


def _regimens() -> dict[str, dict[str, object]]:
    payload = json.loads(
        (ROOT / "data" / "bootstrap" / "medication_regimens.json").read_text(encoding="utf-8")
    )
    rows = payload["regimens"]
    assert isinstance(rows, list)
    return {str(row["id"]): row for row in rows if isinstance(row, dict)}


def _med_rows(chart: str, context_heading: str) -> list[str]:
    section = chart.split(context_heading, 1)[1]
    section = section.split("\n## ", 1)[0]
    return [line for line in section.splitlines() if line.startswith("| ") and "---" not in line]


def test_walkthrough_links_current_case_sets() -> None:
    text = README.read_text(encoding="utf-8")
    assert "](../../data/case_sets/balanced/README.md)" in text
    assert "](../../data/case_sets/seed_guided/README.md)" in text
    assert "CLINIPROOF_BALANCED_V4" in text
    assert "CLINIPROOF_SEEDCASES_V3" in text
    assert "educational demonstrations only" in text


def test_walkthrough_contains_readable_teaching_case() -> None:
    text = README.read_text(encoding="utf-8")
    assert "](examples/clean_heart_failure_case.md)" in text
    chart = CLEAN.read_text(encoding="utf-8")
    assert chart.startswith("# Teaching case: Heart failure")
    for heading in (
        "## Patient overview",
        "## Reason for hospitalization",
        "## Relevant medical history",
        "## Hospital course",
        "## Home medications",
        "## Medications during hospitalization",
        "## Discharge medications",
        "## Medication reconciliation",
        "## Follow-up and monitoring",
    ):
        assert heading in chart
    assert "TEACH-001" in chart
    assert "How a CliniProof case is structured" in text


def test_walkthrough_explains_transition_error_and_review() -> None:
    text = README.read_text(encoding="utf-8")
    assert "Home regimen" in text
    assert "temporarily held" in text
    assert "hospital-only" in text
    assert "absent from the discharge list" in text
    assert "error-bearing" in text
    assert "](examples/heart_failure_omission_case.md)" in text
    for heading in (
        "### C1 — Clinical plausibility",
        "### C2 — Intended assessment problem",
        "### C3 — Detectability",
        "### C4 — Competing problems",
        "### C5 — Difficulty",
    ):
        assert heading in text
    assert "**Accept.**" in text and "**Revise.**" in text and "**Exclude.**" in text


def test_json_is_not_the_primary_teaching_interface() -> None:
    text = README.read_text(encoding="utf-8")
    primary, marker, technical = text.partition("## Technical source files")
    assert marker
    assert ".json)" not in primary
    assert "syn-000901" not in primary.casefold()
    assert ".json)" in technical
    assert "The structured source used to generate the teaching example" in technical
    examples = (EXAMPLES / "README.md").read_text(encoding="utf-8")
    assert ".json)" not in examples
    assert "clean_heart_failure_case.md" in examples


def test_teaching_ids_are_not_active_study_cases() -> None:
    current = [
        CLEAN,
        OMISSION,
        SOURCE / "teach-001-clean.json",
        SOURCE / "teach-002-omission.json",
        SOURCE / "teach-002-investigator.json",
    ]
    for path in current:
        text = path.read_text(encoding="utf-8")
        assert "TEACH-00" in text
        for case_id in ACTIVE_VAL:
            assert case_id not in text, path.name
        assert re.search(r"VAL-\d{3}", text) is None
    clean = _load(SOURCE / "teach-001-clean.json")
    teaching = clean["teaching"]
    assert isinstance(teaching, dict)
    assert teaching["generator_case_id"] == "SYN-009901"
    assert teaching["teaching_id"] == "TEACH-001"
    assert not str(teaching["generator_case_id"]).startswith("VAL-")


def test_teaching_chart_uses_current_curated_regimen() -> None:
    chart = CLEAN.read_text(encoding="utf-8")
    home = "\n".join(_med_rows(chart, "## Home medications"))
    discharge = "\n".join(_med_rows(chart, "## Discharge medications"))
    regimens = _regimens()
    for drug, regimen_id in CURATED.items():
        regimen = regimens[regimen_id]
        dose = str(regimen["dose"])
        route = str(regimen["route"])
        frequency = str(regimen["frequency"])
        for section in (home, discharge):
            row = next(line for line in section.splitlines() if drug in line.casefold())
            assert dose in row
            assert route in row
            assert frequency in row
            assert "Oral Tablet" in row
    assert "4 MG/ML" not in chart
    assert "1 MG/ML" not in chart
    assert "2.5 MG" not in chart
    omission = OMISSION.read_text(encoding="utf-8")
    omission_discharge = "\n".join(_med_rows(omission, "## Discharge medications")).casefold()
    omission_home = "\n".join(_med_rows(omission, "## Home medications")).casefold()
    assert "furosemide" in omission_home
    assert "furosemide" not in omission_discharge
    investigator = _load(SOURCE / "teach-002-investigator.json")
    assert investigator["injected_category"] == "f1_omission"
    assert investigator["injected_family"] == "family_1"
    assert investigator["injected_rxcui"] == "313988"
    keys = investigator["answer_keys"]
    assert isinstance(keys, list)
    assert keys[0]["error_category"] == "f1_omission"  # type: ignore[index]
    for chart_text in (chart, omission):
        folded = chart_text.casefold()
        for phrase in CHART_ANSWER_CUES:
            assert phrase not in folded


def test_walkthrough_markdown_links_resolve() -> None:
    missing: list[str] = []
    files = [
        README,
        EXAMPLES / "README.md",
        SOURCE / "README.md",
        SOURCE / "historical" / "README.md",
    ]
    for path in files:
        for match in LINK.finditer(path.read_text(encoding="utf-8")):
            target = match.group(1).split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    assert missing == []
