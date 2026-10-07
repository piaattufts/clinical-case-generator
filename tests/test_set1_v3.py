# ruff: noqa: E501
"""Version 3 Set 1 matches the chart, hides the answer, and is the README target."""

from __future__ import annotations

import json
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "exports" / "ko_cycle2_revised_validation_v3"
CASE_IDS = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")
DIRECT = (
    "no reason to stop",
    "no discharge medicine is stopped",
    "verified list at discharge",
    "verified collateral medication list at discharge",
    "intended at discharge",
    "intended to continue",
    "intended after discharge",
    "should continue",
    "should stop",
    "complete the planned",
    "take exactly as listed",
    "are continued",
)


def test_v3_resident_files_hide_the_reference_and_the_answer() -> None:
    for case_id in CASE_IDS:
        resident = json.loads((V3 / f"{case_id}_resident.json").read_text(encoding="utf-8"))
        evaluator = json.loads((V3 / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
        assert "reference_discharge_plan" not in resident
        assert "reference_discharge_plan" in evaluator
        blob = json.dumps(resident).lower()
        for phrase in DIRECT:
            assert phrase not in blob, f"{case_id} contains {phrase}"
        for item in evaluator["reference_discharge_plan"]["medications"]:
            assert item.get("evidence_class") != "HIDDEN_REFERENCE_DEPENDENCY"
            assert item.get("evidence_class") != "CLINICALLY_INCONSISTENT"


def test_v3_facts_match_the_canonical_choices() -> None:
    chart_803 = json.dumps(json.loads((V3 / "VAL-803_resident.json").read_text(encoding="utf-8")))
    assert "128" in chart_803 and "135" in chart_803
    assert "synthetic_v3" in chart_803
    meds_805 = json.loads((V3 / "VAL-805_resident.json").read_text(encoding="utf-8"))[
        "CaseMedication"
    ]
    furosemide = [row for row in meds_805 if "furosemide" in row["drug"]]
    assert {row["route"] for row in furosemide} == {"oral"}
    reference_805 = json.loads((V3 / "VAL-805_evaluator.json").read_text(encoding="utf-8"))
    changed = [
        row
        for row in reference_805["reference_discharge_plan"]["medications"]
        if "furosemide" in row["medication"]
    ][0]
    assert changed["action"] == "change"
    assert changed["frequency"] == "twice daily"
    chart_809 = json.dumps(json.loads((V3 / "VAL-809_resident.json").read_text(encoding="utf-8")))
    assert "36.80" in chart_809
    assert "viridans" not in chart_809.lower()
    assert "dental" not in chart_809.lower()
    chart_813 = json.dumps(
        json.loads((V3 / "VAL-813_resident.json").read_text(encoding="utf-8"))
    ).lower()
    assert "mycophenolate" not in chart_813
    home = [
        row["drug"]
        for row in json.loads((V3 / "VAL-813_resident.json").read_text(encoding="utf-8"))[
            "CaseMedication"
        ]
        if row["context"] == "home"
    ]
    assert not any("valganciclovir" in drug for drug in home)


def test_codebook_does_not_ask_about_absent_facts() -> None:
    document = Document(str(V3 / "CliniProof_Cycle2_Revised_Cases_Validation.docx"))
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    lowered = text.lower()
    assert "ejection fraction 30" not in lowered
    assert "hold mycophenolate" not in lowered
    assert "continue mycophenolate" not in lowered
    assert "no mycophenolate row" in lowered
    assert text.count("same information the resident would see") == 6
    assert "NOT COMPLETED IN ROUND 1" in text
    assert "CLINICAL REVISION RECORD" in text
    assert "Author response" not in text


def test_readme_points_at_v3_and_matches_the_charts() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert (
        "exports/ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx"
        in readme
    )
    section = readme.split("#### VAL-801", 1)[1].split("### Cases that needed narrower", 1)[0]
    assert "81 kg" in section
    assert "78 kg" in section
    assert "73 kg" in section
    assert "128 mmol/L" in section
    assert "synthetic" in section.lower()
    assert "36.80" in section
    assert "900 mg twice daily" in section
    for absent in (
        "86 kg",
        "ejection fraction is 30",
        "30 percent",
        "intravenous 40",
        "dental extraction",
        "viridans",
        "38.6",
        "six weeks earlier",
        "mycophenolate",
    ):
        assert absent not in section.lower(), absent
