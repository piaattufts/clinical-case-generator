"""Committed resident-validation plans: unique IDs, V1 mix, no TEST_ identifiers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict

from app.services.validation_batch import parse_assignments
from app.utils.identifiers import VALIDATION_CASE_RE

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "data" / "validation"

PLAN_PATHS = (
    VALIDATION / "batch_plan.json",
    VALIDATION / "v2" / "batch_plan.json",
    VALIDATION / "v3" / "batch_plan.json",
    VALIDATION / "v4" / "batch_plan.json",
)

class BatchMeta(TypedDict):
    master_seed: int
    first_val: str
    last_val: str
    first_seq: int
    last_seq: int


EXPECTED: dict[str, BatchMeta] = {
    "RESIDENT_VALIDATION_V1": {
        "master_seed": 20260922,
        "first_val": "VAL-001",
        "last_val": "VAL-024",
        "first_seq": 101,
        "last_seq": 124,
    },
    "RESIDENT_VALIDATION_V2": {
        "master_seed": 20260923,
        "first_val": "VAL-025",
        "last_val": "VAL-048",
        "first_seq": 201,
        "last_seq": 224,
    },
    "RESIDENT_VALIDATION_V3": {
        "master_seed": 20260924,
        "first_val": "VAL-049",
        "last_val": "VAL-072",
        "first_seq": 301,
        "last_seq": 324,
    },
    "RESIDENT_VALIDATION_V4": {
        "master_seed": 20260925,
        "first_val": "VAL-073",
        "last_val": "VAL-096",
        "first_seq": 401,
        "last_seq": 424,
    },
}

SCENARIO_COUNTS = {
    "HF_INPATIENT": 5,
    "AF_ANTICOAGULATION": 5,
    "HTN_INPATIENT": 5,
    "T2DM_INPATIENT": 5,
    "CAP_INPATIENT": 4,
}

NO_STOP_MED_SCENARIOS = {"T2DM_INPATIENT", "CAP_INPATIENT"}


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return payload


def test_committed_batch_plans_are_independent_and_follow_v1_mix() -> None:
    plans = [_load(path) for path in PLAN_PATHS]
    assert [plan["batch_code"] for plan in plans] == list(EXPECTED)
    assert len({plan["master_seed"] for plan in plans}) == 4

    all_val_ids: list[str] = []
    all_sequences: list[int] = []
    v1_pattern: list[tuple[str, bool, str | None]] | None = None

    for plan in plans:
        meta = EXPECTED[plan["batch_code"]]
        assignments = parse_assignments(plan)
        assert len(assignments) == 24
        assert plan["master_seed"] == meta["master_seed"]
        assert assignments[0].validation_case_id == meta["first_val"]
        assert assignments[-1].validation_case_id == meta["last_val"]
        assert assignments[0].sequence == meta["first_seq"]
        assert assignments[-1].sequence == meta["last_seq"]
        assert "TEST_" not in json.dumps(plan)

        scenario_counts: dict[str, int] = {}
        pattern: list[tuple[str, bool, str | None]] = []
        for item in assignments:
            assert VALIDATION_CASE_RE.fullmatch(item.validation_case_id)
            assert item.sequence >= 101
            all_val_ids.append(item.validation_case_id)
            all_sequences.append(item.sequence)
            scenario_counts[item.scenario] = scenario_counts.get(item.scenario, 0) + 1
            pattern.append((item.scenario, item.inject_error, item.error_category))
            if item.inject_error:
                assert item.error_category in {
                    "omission",
                    "dose_mismatch",
                    "frequency_mismatch",
                    "incorrect_continuation",
                }
            else:
                assert item.error_category is None
            if item.scenario in NO_STOP_MED_SCENARIOS:
                assert item.error_category != "incorrect_continuation"

        assert scenario_counts == SCENARIO_COUNTS
        assert sum(1 for item in assignments if not item.inject_error) == 5
        if v1_pattern is None:
            v1_pattern = pattern
        else:
            assert pattern == v1_pattern

    assert len(all_val_ids) == len(set(all_val_ids)) == 96
    assert len(all_sequences) == len(set(all_sequences)) == 96
    assert set(range(1, 4)).isdisjoint(all_sequences)


EXPORT_DIRS = {
    "RESIDENT_VALIDATION_V2": VALIDATION / "v2",
    "RESIDENT_VALIDATION_V3": VALIDATION / "v3",
    "RESIDENT_VALIDATION_V4": VALIDATION / "v4",
}

RESIDENT_LEAK_MARKERS = (
    "syn-000",
    "answer_key",
    "is_clean_control",
    "intentional error",
    "rxcui:",
    "caseanswerkey",
)


def test_committed_v2_v4_exports_are_blinded_and_complete() -> None:
    for batch_code, folder in EXPORT_DIRS.items():
        meta = EXPECTED[batch_code]
        resident = _load(folder / "resident_validation_cases.json")
        key = _load(folder / "investigator_answer_key.json")
        manifest = _load(folder / "validation_manifest.json")
        assert resident["batch_code"] == batch_code == key["batch_code"] == manifest["batch_code"]
        status = "machine-validated synthetic resident-review cases pending clinician validation"
        assert resident["dataset_status"] == status
        cases = resident["cases"]
        assert len(cases) == 24
        assert cases[0]["case_id_code"] == meta["first_val"]
        assert cases[-1]["case_id_code"] == meta["last_val"]
        blob = json.dumps(resident).casefold()
        for marker in RESIDENT_LEAK_MARKERS:
            assert marker not in blob
        assert "TEST_" not in json.dumps(resident)
        assert all(item["case_id_code"].startswith("VAL-") for item in cases)
        assert "CaseAnswerKey" not in json.dumps(resident)
        key_cases = key["cases"]
        assert len(key_cases) == 24
        clean = [
            item
            for item in key_cases
            if item["control_error_status"] == "NO INTENTIONAL ERROR"
        ]
        assert len(clean) == 5
        assert len(key_cases) - len(clean) == 19
        assert key_cases[0]["internal_case_id_code"].startswith("SYN-")
        worksheet = (folder / "resident_review_worksheet.csv").read_text(encoding="utf-8")
        assert meta["first_val"] in worksheet
        assert meta["last_val"] in worksheet
        assert (folder / "coverage_report.md").exists()
        assert (folder / "scenario_coverage_matrix.md").exists()
        assert (folder / "validation_manifest.json").exists()
