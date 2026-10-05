"""Screening labels, exclusion codes, and the calibration sample."""

from __future__ import annotations

from pathlib import Path

from inthewild_review.calibration import draw_calibration_sample, stratified_sample
from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.schemas import NORMALIZED_FIELDS, SCREENING_FIELDS
from inthewild_review.screening import (
    ScreeningValidationError,
    queue_full_text_rows,
    validate_full_text_row,
    validate_title_abstract_row,
)


def test_exclude_requires_one_known_code_and_include_maybe_forbid_one() -> None:
    validate_title_abstract_row(
        {"record_id": "rec_a", "decision": "EXCLUDE", "exclusion_code": "N1_NOT_NATURALISTIC"}
    )
    for decision in ("INCLUDE", "MAYBE"):
        validate_title_abstract_row({"record_id": "rec_a", "decision": decision, "exclusion_code": ""})
        try:
            validate_title_abstract_row(
                {"record_id": "rec_a", "decision": decision, "exclusion_code": "N2_NOT_SOCIAL_ROBOT"}
            )
        except ScreeningValidationError:
            continue
        raise AssertionError(f"{decision} accepted an exclusion code")
    try:
        validate_title_abstract_row({"record_id": "rec_a", "decision": "EXCLUDE", "exclusion_code": ""})
    except ScreeningValidationError as exc:
        assert "exactly one" in str(exc)
    else:
        raise AssertionError("EXCLUDE without a code was accepted")
    try:
        validate_title_abstract_row(
            {"record_id": "rec_a", "decision": "EXCLUDE", "exclusion_code": "NOT_A_REAL_CODE"}
        )
    except ScreeningValidationError:
        return
    raise AssertionError("Unknown exclusion code was accepted")


def test_maybe_is_retained_as_its_own_decision() -> None:
    row = {"record_id": "rec_a", "decision": "MAYBE", "exclusion_code": ""}
    validate_title_abstract_row(row)
    assert row["decision"] == "MAYBE"
    queued = queue_full_text_rows([row], [])
    assert queued[0]["record_id"] == "rec_a"
    assert queued[0]["decision"] == ""
    excluded = {
        "record_id": "rec_b",
        "decision": "EXCLUDE",
        "exclusion_code": "N5_NOT_A_RECORD",
    }
    queued = queue_full_text_rows([row, excluded], queued)
    assert [item["record_id"] for item in queued] == ["rec_a"]


def test_full_text_include_requires_explicit_yes_and_does_not_infer() -> None:
    criteria = {
        "record_id": "rec_a",
        "full_text_available": "YES",
        "physically_embodied_robot": "YES",
        "substantive_social_interaction": "YES",
        "human_participants": "YES",
        "naturalistic_or_repeated_longterm": "YES",
        "identifiable_interaction_situation": "YES",
        "setting_extractable": "YES",
        "duration_extractable": "YES",
        "interaction_structure_extractable": "UNCLEAR",
        "decision": "INCLUDE",
        "exclusion_reason": "",
    }
    try:
        validate_full_text_row(criteria)
    except ScreeningValidationError as exc:
        assert "interaction_structure_extractable" in str(exc)
    else:
        raise AssertionError("INCLUDE was accepted with UNCLEAR evidence")
    criteria["interaction_structure_extractable"] = "YES"
    validate_full_text_row(criteria)
    criteria["decision"] = "EXCLUDE"
    criteria["exclusion_reason"] = "NOT_PHYSICALLY_EMBODIED_ROBOT"
    criteria["physically_embodied_robot"] = "UNCLEAR"
    try:
        validate_full_text_row(criteria)
    except ScreeningValidationError as exc:
        assert "must not be recoded as NO" in str(exc) or "not NO" in str(exc)
    else:
        raise AssertionError("UNCLEAR was treated as a confirmed NO exclusion")


def _population() -> list[dict[str, str]]:
    rows = []
    for index in range(8):
        rows.append(
            {
                "record_id": f"rec_a{index:02d}",
                "year": "2000",
                "source_database": "scopus",
                "title": "SYNTHETIC TEST FIXTURE",
            }
        )
    for index in range(4):
        rows.append(
            {
                "record_id": f"rec_b{index:02d}",
                "year": "2010",
                "source_database": "pubmed",
                "title": "SYNTHETIC TEST FIXTURE",
            }
        )
    return rows


def test_calibration_sample_is_stratified_and_repeatable() -> None:
    population = _population()
    first = stratified_sample(population, 4, 20261005)
    second = stratified_sample(population, 4, 20261005)
    assert [row["record_id"] for row in first] == [row["record_id"] for row in second]
    years = {row["year"] for row in first}
    sources = {row["source_database"] for row in first}
    assert years == {"2000", "2010"}
    assert sources == {"scopus", "pubmed"}
    first_four_ids = [row["record_id"] for row in population[:4]]
    assert [row["record_id"] for row in first] != first_four_ids


def test_calibration_does_not_overwrite_reviewer_decisions(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    rows = []
    for row in _population():
        full = {field: "" for field in NORMALIZED_FIELDS}
        full.update(row)
        full["origin"] = "database"
        rows.append(full)
    write_csv(layout.normalized, rows, NORMALIZED_FIELDS, tmp_path)
    draw_calibration_sample(layout, sample_size=4, seed=20261005)
    reviewer = read_csv(layout.reviewer_1)
    reviewer[0]["decision"] = "MAYBE"
    reviewer[0]["notes"] = "keep this note"
    write_csv(layout.reviewer_1, reviewer, SCREENING_FIELDS, tmp_path)
    draw_calibration_sample(layout, sample_size=4, seed=20261005)
    again = read_csv(layout.reviewer_1)
    assert again[0]["decision"] == "MAYBE"
    assert again[0]["notes"] == "keep this note"
    assert (layout.calibration_consensus).exists()
    assert read_csv(layout.calibration_consensus) == []
