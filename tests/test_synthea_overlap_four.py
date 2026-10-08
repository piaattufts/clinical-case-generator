"""The four overlap counterparts stay clean, matched, and on the current instrument."""

from __future__ import annotations

import json
from pathlib import Path

from app.services.g2_audit import round1_row
from app.services.review_casebook import instrument_markers, template_instrument
from docx import Document

REPO = Path(__file__).resolve().parents[1]
PAIRS = (
    ("VAL-801", "G2-001", "stop", "ibuprofen"),
    ("VAL-805", "G2-005", "new_start", "furosemide"),
    ("VAL-809", "G2-009", "continue", "ceftriaxone"),
    ("VAL-813", "G2-013", "stop", "hydrochlorothiazide"),
)
HIDDEN = (
    "Received higher education (finding)",
    "Has a criminal record (finding)",
    "Housing unsatisfactory (finding)",
    "Lack of access to transportation (finding)",
)


def _evaluator(case_id: str) -> dict:
    path = REPO / "data" / "case_sets" / "synthea_g2" / "cases" / "evaluator" / f"{case_id}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _resident(case_id: str) -> dict:
    path = REPO / "data" / "case_sets" / "synthea_g2" / "cases" / "resident" / f"{case_id}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_four_counterparts_pass_the_automated_audit_and_hide_the_reference() -> None:
    for _val_id, case_id, action, drug in PAIRS:
        episode = _evaluator(case_id)
        resident = _resident(case_id)
        row = round1_row(episode, case_id)
        assert row["overall_pass"], row["notes"]
        assert episode["clinically_validated"] is False
        assert episode["control_error_status"] == "NO INTENTIONAL ERROR"
        assert episode["synthea_patient_id"]
        blob = json.dumps(resident)
        assert "reference_discharge_plan" not in blob
        assert "acceptable_alternatives" not in blob
        actions = {
            (item["action"], item["medication"])
            for item in episode["reference_discharge_plan"]["actions"]
        }
        assert any(item_action == action and drug in name for item_action, name in actions)
        history = " ".join(resident["ClinicalCase"]["medical_history"])
        for label in HIDDEN:
            assert label not in history


def test_matched_overlap_codebook_uses_the_template_instrument() -> None:
    path = REPO / "docs" / "validation" / "CliniProof_Synthea_Matched_Overlap4_Codebook.docx"
    document = Document(str(path))
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    for case_id in ("G2-001", "G2-005", "G2-009", "G2-013"):
        assert f"CASE {case_id}" in text
    for other in ("G2-002", "G2-006", "VAL-801"):
        assert f"CASE {other}" not in text
    assert "not clinically validated" in text.casefold()
    gold = template_instrument()
    markers = instrument_markers(document)
    starts = [
        index
        for index, marker in enumerate(markers)
        if marker == "C1 — Clinical plausibility"
    ]
    assert len(starts) == 4
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(markers)
        assert markers[start:end] == gold
