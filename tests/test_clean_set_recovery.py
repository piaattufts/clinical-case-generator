"""The committed clean base is the pre-injection VAL-801–VAL-824 source."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "case_sets" / "seed_guided" / "CLEAN_BASE"
ORIGINAL = ROOT / "data" / "case_sets" / "seed_guided" / "resident_validation_cases.json"
INTEGRITY = ROOT / "docs" / "source_integrity.md"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_clean_base_matches_the_integrity_record_and_hides_the_reference() -> None:
    text = INTEGRITY.read_text(encoding="utf-8")
    assert _sha(ORIGINAL) in text
    ids = [f"VAL-{index:03d}" for index in range(801, 825)]
    assert len(list(CLEAN.glob("VAL-*_resident.json"))) == 24
    for case_id in ids:
        resident_path = CLEAN / f"{case_id}_resident.json"
        evaluator_path = CLEAN / f"{case_id}_evaluator.json"
        assert _sha(resident_path) in text
        assert _sha(evaluator_path) in text
        resident = json.loads(resident_path.read_text(encoding="utf-8"))
        evaluator = json.loads(evaluator_path.read_text(encoding="utf-8"))
        assert "reference_discharge_plan" not in resident
        assert "reference_discharge_plan" in evaluator
        medications = resident["CaseMedication"]
        assert all(row["context"] != "discharge" for row in medications)
