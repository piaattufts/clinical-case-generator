"""Round 1 extraction and version-2 revisions stay inside the six reviewed cases."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.services.cycle2_v2_cases import LEDGER, REVIEW_ITEMS, write_revision_package
from app.services.round1_six_case_review import (
    AMBIGUITY,
    NOT_COMPLETED,
    completed_reviews,
)
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
CASE_IDS = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")
UNTOUCHED = (
    ROOT / "data" / "case_sets" / "seed_guided" / "resident_validation_cases.json",
    ROOT / "data" / "case_sets" / "balanced" / "resident_validation_cases.json",
    ROOT / "exports" / "clean_balanced_seed_set" / "VAL-801_resident.json",
    ROOT / "exports" / "clean_balanced_seed_set" / "VAL-805_resident.json",
    ROOT / "exports" / "ko_revised_cases_v1" / "VAL-801_resident.json",
    ROOT / "exports" / "ko_clean_cases_for_review_v1" / "VAL-804_resident.json",
    ROOT / "exports" / "ko_clean_cases_for_review_v1" / "VAL-824_evaluator.json",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_extraction_preserves_blanks_and_double_selections() -> None:
    reviews = completed_reviews()
    assert tuple(reviews) == CASE_IDS
    first = reviews["VAL-801"]
    assert first["c3"]["selection"]["pass"] is True
    assert first["c3"]["selection"]["fail"] is True
    assert AMBIGUITY in first["c3"]["selection"]["flags"]
    assert "ibuprofen was stopped" in first["c1"]["comment"]
    medication = reviews["VAL-805"]["c1"]["domains"][4]
    assert medication["scores"]["2"] is True
    assert medication["scores"]["3"] is True
    assert AMBIGUITY in medication["flags"]
    partial = reviews["VAL-803"]
    assert partial["round1_review_status"] == "partial"
    for block in (
        partial["c2"]["selection"],
        partial["c3"]["selection"],
        partial["c4"]["selection"],
        partial["c5"]["selection"],
        partial["overall_recommendation"]["selection"],
    ):
        assert NOT_COMPLETED in block["flags"]
    assert partial["overall_recommendation"]["comment"] is None
    assert partial["overall_recommendation"]["reviewer_code"] is None


def test_v2_package_changes_only_the_six_cases(tmp_path: Path) -> None:
    before = {path: _sha(path) for path in UNTOUCHED}
    feedback = tmp_path / "feedback"
    cases = tmp_path / "cases"
    document = write_revision_package(feedback, cases)
    assert {path: _sha(path) for path in UNTOUCHED} == before
    for case_id in CASE_IDS:
        assert (feedback / "round1_feedback" / f"{case_id}_round1_feedback.json").is_file()
        resident = json.loads((cases / f"{case_id}_resident.json").read_text(encoding="utf-8"))
        assert "reference_discharge_plan" not in resident
        assert "ibuprofen was stopped" not in json.dumps(resident) or case_id != "VAL-801"
    assert (feedback / "ROUND1_FEEDBACK_COMPLETE.md").is_file()
    assert (feedback / "ROUND1_FEEDBACK_EXTRACTION_AUDIT.md").is_file()
    assert (feedback / "ROUND1_REVIEWER_RESPONSE_MATRIX.md").is_file()
    assert (feedback / "REVISION_EVIDENCE_LEDGER.md").is_file()
    ledger_items = {row["item"] for row in LEDGER}
    for item in REVIEW_ITEMS:
        if item["decision"] in {"ACCEPTED", "PARTIALLY_ACCEPTED"} and item["change"] != "None.":
            assert item["id"] in ledger_items
    for row in LEDGER:
        assert row["locator"]
        assert row["source"]
    text = "\n".join(paragraph.text for paragraph in Document(str(document)).paragraphs)
    assert text.count("CASE VAL-") == 6
    for case_id in CASE_IDS:
        section = text.split(f"CASE {case_id}", 1)[1]
        if case_id != "VAL-813":
            section = section.split("CASE VAL-", 1)[0]
        assert section.index("CURRENT ROUND 2 CASE") < section.index(
            "ROUND 1 CLINICIAN FEEDBACK — HISTORICAL RECORD"
        )
        assert section.index("ROUND 1 CLINICIAN FEEDBACK — HISTORICAL RECORD") < section.index(
            "ROUND 2 RESPONSE TO ROUND 1 REVIEW"
        )
    assert "Not completed in Round 1" in text
    assert "Source document contains multiple selected responses" in text
    eight = [f"VAL-{number}" for number in range(801, 825) if f"VAL-{number}" not in CASE_IDS]
    for case_id in eight:
        assert f"CASE {case_id}" not in text
