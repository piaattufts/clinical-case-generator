"""KO review packages stay separated and do not alter frozen VAL files."""

from __future__ import annotations

import json
from pathlib import Path

from app.services.ko_review_sets import (
    FROZEN_RESIDENT,
    REMAINING_IDS,
    REVISED_IDS,
    SOURCE_DIR,
    write_ko_review_sets,
)
from docx import Document

FORBIDDEN_PACKET_PHRASES = ("error-bearing", "clean control", "clean controls")


def _tree_bytes(path: Path) -> dict[str, bytes]:
    files = [item for item in sorted(path.rglob("*")) if item.is_file()]
    return {item.relative_to(path).as_posix(): item.read_bytes() for item in files}


def test_ko_sets_cover_each_seed_case_once_and_hide_the_reference(tmp_path: Path) -> None:
    frozen_before = FROZEN_RESIDENT.read_bytes()
    frozen_trees = {
        name: _tree_bytes(Path("data/case_sets") / name) for name in ("seed_guided", "balanced")
    }
    source_before = _tree_bytes(SOURCE_DIR)
    revised = tmp_path / "revised"
    remaining = tmp_path / "remaining"
    summary = write_ko_review_sets(revised, remaining)
    assert FROZEN_RESIDENT.read_bytes() == frozen_before
    for name, before in frozen_trees.items():
        assert _tree_bytes(Path("data/case_sets") / name) == before
    assert _tree_bytes(SOURCE_DIR) == source_before
    assert summary["revised"] == list(REVISED_IDS)
    assert summary["remaining"] == list(REMAINING_IDS)
    assert len(REVISED_IDS) == 6
    assert len(REMAINING_IDS) == 18
    assert set(REVISED_IDS).isdisjoint(REMAINING_IDS)
    assert set(REVISED_IDS) | set(REMAINING_IDS) == {
        f"VAL-{number}" for number in range(801, 825)
    }

    for case_id in REVISED_IDS:
        resident = json.loads((revised / f"{case_id}_resident.json").read_text(encoding="utf-8"))
        evaluator = json.loads((revised / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
        _assert_split(resident, evaluator)
        original = json.loads(
            (SOURCE_DIR / f"{case_id}_resident.json").read_text(encoding="utf-8")
        )
        assert resident["ClinicalCase"]["presentation"]["hpi"] != original["ClinicalCase"][
            "presentation"
        ]["hpi"]

    for case_id in REMAINING_IDS:
        resident = json.loads((remaining / f"{case_id}_resident.json").read_text(encoding="utf-8"))
        evaluator = json.loads(
            (remaining / f"{case_id}_evaluator.json").read_text(encoding="utf-8")
        )
        original = json.loads(
            (SOURCE_DIR / f"{case_id}_resident.json").read_text(encoding="utf-8")
        )
        assert resident == original
        _assert_split(resident, evaluator)

    statin = json.loads((revised / "VAL-802_resident.json").read_text(encoding="utf-8"))
    assert any("atorvastatin" in row["drug"] for row in statin["CaseMedication"])
    supply = json.loads((revised / "VAL-803_evaluator.json").read_text(encoding="utf-8"))
    lisinopril = next(
        item
        for item in supply["reference_discharge_plan"]["medications"]
        if item["medication"].startswith("lisinopril")
    )
    assert lisinopril["duration"] == "30 days"
    ibuprofen = next(
        item
        for item in json.loads((revised / "VAL-801_evaluator.json").read_text(encoding="utf-8"))[
            "reference_discharge_plan"
        ]["medications"]
        if item["medication"].startswith("ibuprofen")
    )
    assert ibuprofen["action"] == "continue"
    assert summary["revised_status"] == {
        case_id: "READY_FOR_CLINICIAN_REVIEW" for case_id in REVISED_IDS
    }
    assert summary["remaining_status"]["VAL-824"] == "READY_FOR_FRESH_REVIEW"
    assert summary["remaining_status"]["VAL-808"] == "CLINICALLY_INCONSISTENT"
    assert summary["remaining_status"]["VAL-820"] == "NEEDS_PRE_REVIEW_FIX"
    for case_id in REVISED_IDS:
        evaluator = json.loads((revised / f"{case_id}_evaluator.json").read_text(encoding="utf-8"))
        classes = [item["evidence_class"] for item in evaluator["evidence_trace"]]
        assert classes
        assert set(classes) <= {"SUFFICIENT_EVIDENCE"}

    carvedilol = json.loads((remaining / "VAL-808_resident.json").read_text(encoding="utf-8"))
    assert all("carvedilol" not in row["drug"].casefold() for row in carvedilol["CaseMedication"])
    furosemide = next(
        item
        for item in json.loads((remaining / "VAL-807_evaluator.json").read_text(encoding="utf-8"))[
            "reference_discharge_plan"
        ]["medications"]
        if item["medication"].startswith("furosemide")
    )
    assert furosemide["dose"] == "40 MG"
    ceftriaxone = json.loads((remaining / "VAL-810_resident.json").read_text(encoding="utf-8"))
    assert any("ceftriaxone" in row["drug"] for row in ceftriaxone["CaseMedication"])

    for path in (
        revised / "KO_REVISED_CASES_REVIEW.docx",
        remaining / "KO_REMAINING_CLEAN_CASES_REVIEW.docx",
    ):
        text = "\n".join(paragraph.text for paragraph in Document(str(path)).paragraphs).casefold()
        for phrase in FORBIDDEN_PACKET_PHRASES:
            assert phrase not in text
        assert "clinician validation reference" in text
        assert "not shown to residents" in text
        assert "c1 — clinical plausibility" in text
        assert "c4 — alternative acceptable answers" in text


def _assert_split(resident: dict[str, object], evaluator: dict[str, object]) -> None:
    assert "reference_discharge_plan" not in resident
    assert "reference_discharge_plan" in evaluator
    blob = json.dumps(resident).casefold()
    assert "exactly as listed" not in blob
    assert "error_category" not in blob
    assert "clean_expected_state" not in blob
    medications = resident["CaseMedication"]
    assert isinstance(medications, list)
    assert all(row["context"] != "discharge" for row in medications)
