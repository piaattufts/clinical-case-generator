"""Duplicate candidates are flagged. They are not merged."""

from __future__ import annotations

from pathlib import Path

from inthewild_review.config import ReviewLayout
from inthewild_review.deduplicate import detect_duplicate_candidates, write_duplicate_candidates
from inthewild_review.io_utils import write_csv
from inthewild_review.schemas import DUPLICATE_FIELDS, NORMALIZED_FIELDS


def _record(**overrides: str) -> dict[str, str]:
    row = {field: "" for field in NORMALIZED_FIELDS}
    row.update(
        {
            "record_id": "rec_a",
            "source_database": "scopus",
            "title": "SYNTHETIC TEST FIXTURE",
            "normalized_title": "synthetic test fixture",
            "year": "2014",
            "origin": "database",
        }
    )
    row.update(overrides)
    return row


def test_exact_doi_match_and_empty_doi_is_not_a_match() -> None:
    rows = [
        _record(record_id="rec_a", doi_normalized="10.1000/abc", normalized_title="one title"),
        _record(
            record_id="rec_b",
            doi_normalized="10.1000/abc",
            normalized_title="another title",
            source_database="pubmed",
        ),
        _record(record_id="rec_c", doi_normalized="", normalized_title="third title"),
        _record(record_id="rec_d", doi_normalized="", normalized_title="fourth title"),
    ]
    pairs = detect_duplicate_candidates(rows, compare_all_fuzzy=False)
    doi_pairs = [pair for pair in pairs if pair["doi_match"] == "YES"]
    assert len(doi_pairs) == 1
    assert {doi_pairs[0]["record_id_1"], doi_pairs[0]["record_id_2"]} == {"rec_a", "rec_b"}
    assert doi_pairs[0]["human_decision"] == ""
    assert all(pair["doi_match"] == "NO" or "rec_c" not in (pair["record_id_1"], pair["record_id_2"]) for pair in pairs)


def test_exact_title_match_does_not_collapse_conference_and_journal_versions() -> None:
    rows = [
        _record(
            record_id="rec_conf",
            document_type="Conference Paper",
            doi_normalized="10.1000/conf",
        ),
        _record(
            record_id="rec_journal",
            document_type="Journal Article",
            doi_normalized="10.1000/journal",
            source_database="wos",
        ),
    ]
    pairs = detect_duplicate_candidates(rows, compare_all_fuzzy=False)
    assert len(pairs) == 1
    assert pairs[0]["exact_title_match"] == "YES"
    assert pairs[0]["match_type"] == "EXACT_TITLE"
    assert pairs[0]["human_decision"] == ""
    assert pairs[0]["human_decision"] != "SAME_RECORD"
    assert {rows[0]["record_id"], rows[1]["record_id"]} == {"rec_conf", "rec_journal"}


def test_fuzzy_title_is_only_a_flag(tmp_path: Path) -> None:
    rows = [
        _record(record_id="rec_a", normalized_title="synthetic test fixture robot home"),
        _record(
            record_id="rec_b",
            normalized_title="synthetic test fixture robot house",
            doi_normalized="10.1000/other",
        ),
    ]
    pairs = detect_duplicate_candidates(rows, fuzzy_threshold=0.8, compare_all_fuzzy=True)
    assert len(pairs) == 1
    assert pairs[0]["match_type"] == "FUZZY_TITLE"
    assert pairs[0]["exact_title_match"] == "NO"
    assert float(pairs[0]["fuzzy_title_score"]) >= 0.8
    assert pairs[0]["recommended_review"] == "YES"
    assert pairs[0]["human_decision"] == ""
    layout = ReviewLayout(tmp_path)
    write_csv(layout.normalized, rows, NORMALIZED_FIELDS, tmp_path)
    write_duplicate_candidates(layout, fuzzy_threshold=0.8)
    saved = layout.duplicates.read_text(encoding="utf-8")
    assert "SAME_RECORD" not in saved.splitlines()[1:]
    # A later run keeps a human decision instead of clearing it.
    from inthewild_review.io_utils import read_csv

    existing = read_csv(layout.duplicates)
    existing[0]["human_decision"] = "CONFERENCE_JOURNAL_PAIR"
    existing[0]["decision_by"] = "reviewer"
    write_csv(layout.duplicates, existing, DUPLICATE_FIELDS, tmp_path)
    write_duplicate_candidates(layout, fuzzy_threshold=0.8)
    again = read_csv(layout.duplicates)
    assert again[0]["human_decision"] == "CONFERENCE_JOURNAL_PAIR"
    assert again[0]["decision_by"] == "reviewer"
    assert len(read_csv(layout.normalized)) == 2
