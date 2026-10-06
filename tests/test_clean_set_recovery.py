"""The frozen 48-case set can be recovered without regenerating it."""

from __future__ import annotations

import json
from pathlib import Path

from app.services.clean_set_recovery import recover_clean_balanced_set

ORIGINAL = Path("data/case_sets/balanced/resident_validation_cases.json")


def test_recovery_hides_answers_and_keeps_the_original_files(tmp_path: Path) -> None:
    before = ORIGINAL.read_text(encoding="utf-8")
    summary = recover_clean_balanced_set(tmp_path)
    assert ORIGINAL.read_text(encoding="utf-8") == before
    assert summary["cases"] == 48
    assert summary["recovered_from_clean_source"] == 48
    assert summary["reconstructed_from_seed"] == 0
    assert summary["unrecoverable"] == 0
    assert summary["clinically_inconsistent"] == 4

    resident = json.loads((tmp_path / "VAL-701_resident.json").read_text(encoding="utf-8"))
    evaluator = json.loads((tmp_path / "VAL-701_evaluator.json").read_text(encoding="utf-8"))
    blob = json.dumps(resident).casefold()
    assert "exactly as listed" not in blob
    assert "reference_discharge_plan" not in resident
    assert all(row["context"] != "discharge" for row in resident["CaseMedication"])
    assert any(row["drug"].startswith("lisinopril") for row in resident["CaseMedication"])
    actions = {
        item["medication"]: item
        for item in evaluator["reference_discharge_plan"]["medications"]
    }
    assert actions["lisinopril 10 MG Oral Tablet"]["action"] == "continue"
    assert actions["lisinopril 10 MG Oral Tablet"]["dose"] == "10 MG"

    dose_case = json.loads((tmp_path / "VAL-708_evaluator.json").read_text(encoding="utf-8"))
    atorvastatin = next(
        item
        for item in dose_case["reference_discharge_plan"]["medications"]
        if item["medication"].startswith("atorvastatin")
    )
    assert atorvastatin["dose"] == "40 MG"

    inconsistent = json.loads((tmp_path / "VAL-711_resident.json").read_text(encoding="utf-8"))
    assert all(row["context"] != "discharge" for row in inconsistent["CaseMedication"])
    audit = (tmp_path / "AUDIT.md").read_text(encoding="utf-8")
    assert "VAL-711" in audit
    assert "CLINICALLY_INCONSISTENT" in audit
    assert "VAL-801" in audit
    assert "VAL-724" in audit
