"""Committed resident-validation plans: unique IDs, V1 mix, no TEST_ identifiers."""

from __future__ import annotations

import json
from pathlib import Path

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

EXPECTED = {
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


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
