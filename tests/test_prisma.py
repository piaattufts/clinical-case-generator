"""PRISMA totals are derived and have to add up."""

from __future__ import annotations

from pathlib import Path

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import write_csv
from inthewild_review.prisma import assert_prisma_consistent, build_prisma_counts
from inthewild_review.schemas import (
    DEPLOYMENT_FIELDS,
    DUPLICATE_FIELDS,
    FULL_TEXT_FIELDS,
    NORMALIZED_FIELDS,
    PUBLICATION_FIELDS,
    SCENARIO_FIELDS,
    SCREENING_FIELDS,
    STUDY_FIELDS,
)
from tests.test_extraction import _deployment, _full_text_include, _scenario


def _record(record_id: str, database: str, origin: str = "database") -> dict[str, str]:
    row = {field: "" for field in NORMALIZED_FIELDS}
    row.update(
        {
            "record_id": record_id,
            "source_database": database,
            "title": "SYNTHETIC TEST FIXTURE",
            "origin": origin,
            "year": "2014",
        }
    )
    return row


def _screen(record_id: str, decision: str, code: str = "") -> dict[str, str]:
    return {
        "record_id": record_id,
        "reviewer": "REVIEWER_1",
        "decision": decision,
        "exclusion_code": code,
        "notes": "",
        "screened_at": "",
        "criteria_version": "test",
    }


def test_empty_repository_counts_are_zero_and_consistent(tmp_path: Path) -> None:
    counts = build_prisma_counts(ReviewLayout(tmp_path))
    identification = counts["identification"]
    assert isinstance(identification, dict)
    assert identification["total_records"] == 0
    included = counts["included"]
    assert isinstance(included, dict)
    assert included["publications"] == 0
    assert included["studies"] == 0
    assert included["deployments"] == 0
    assert included["scenarios"] == 0
    assert_prisma_consistent(counts)


def test_prisma_arithmetic_keeps_units_separate(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    records = [
        _record("rec_s1", "scopus"),
        _record("rec_s2", "scopus"),
        _record("rec_p1", "pubmed"),
        _record("rec_c1", "citation_chasing", origin="citation_chasing"),
    ]
    write_csv(layout.normalized, records, NORMALIZED_FIELDS, tmp_path)
    write_csv(
        layout.duplicates,
        [
            {
                "duplicate_group_id": "dup_test",
                "record_id_1": "rec_s1",
                "record_id_2": "rec_s2",
                "match_type": "EXACT_TITLE",
                "doi_match": "NO",
                "exact_title_match": "YES",
                "fuzzy_title_score": "1.0000",
                "recommended_review": "YES",
                "human_decision": "SAME_RECORD",
                "human_reason": "synthetic fixture",
                "decision_by": "reviewer",
                "decision_date": "2026-10-05",
                "retained_record_id": "rec_s1",
            }
        ],
        DUPLICATE_FIELDS,
        tmp_path,
    )
    write_csv(
        layout.title_abstract,
        [
            _screen("rec_s1", "INCLUDE"),
            _screen("rec_p1", "MAYBE"),
            _screen("rec_c1", "EXCLUDE", "N3_NON_PRIMARY"),
        ],
        SCREENING_FIELDS,
        tmp_path,
    )
    include = _full_text_include("rec_s1")
    maybe = {field: "" for field in FULL_TEXT_FIELDS}
    maybe.update({"record_id": "rec_p1", "decision": "MAYBE", "full_text_available": "YES"})
    write_csv(layout.full_text, [include, maybe], FULL_TEXT_FIELDS, tmp_path)
    write_csv(
        layout.publications,
        [
            {
                "publication_id": "pub_a",
                "record_id": "rec_s1",
                "doi": "",
                "title": "SYNTHETIC TEST FIXTURE",
                "authors": "",
                "year": "2014",
                "venue": "",
                "publication_type": "",
                "source_database": "scopus",
                "notes": "",
            }
        ],
        PUBLICATION_FIELDS,
        tmp_path,
    )
    write_csv(
        layout.studies,
        [
            {field: "" for field in STUDY_FIELDS}
            | {"study_id": "study_a", "publication_id": "pub_a"},
            {field: "" for field in STUDY_FIELDS}
            | {"study_id": "study_b", "publication_id": "pub_a"},
        ],
        STUDY_FIELDS,
        tmp_path,
    )
    write_csv(
        layout.deployments,
        [_deployment("dep_a", "study_a")],
        DEPLOYMENT_FIELDS,
        tmp_path,
    )
    write_csv(
        layout.scenarios,
        [
            _scenario("scen_a", "dep_a", "study_a", "pub_a"),
            _scenario("scen_b", "dep_a", "study_a", "pub_a"),
        ],
        SCENARIO_FIELDS,
        tmp_path,
    )
    counts = build_prisma_counts(layout)
    identification = counts["identification"]
    title_abstract = counts["title_abstract"]
    full_text = counts["full_text"]
    included = counts["included"]
    assert isinstance(identification, dict)
    assert isinstance(title_abstract, dict)
    assert isinstance(full_text, dict)
    assert isinstance(included, dict)
    assert identification["database_total"] == 3
    assert identification["by_database"] == {"pubmed": 1, "scopus": 2}
    assert identification["citation_chasing"] == 1
    assert identification["total_records"] == 4
    assert counts["records_after_confirmed_duplicate_removal"] == 3
    assert title_abstract["screened"] == 3
    assert title_abstract["include"] == 1
    assert title_abstract["maybe"] == 1
    assert title_abstract["exclude"] == 1
    assert title_abstract["exclude_by_code"] == {"N3_NON_PRIMARY": 1}
    assert full_text["sought"] == 2
    assert full_text["assessed"] == 2
    assert full_text["include"] == 1
    assert full_text["maybe"] == 1
    assert included["publications"] == 1
    assert included["studies"] == 2
    assert included["deployments"] == 1
    assert included["scenarios"] == 2
    assert included["publications"] != included["studies"]
    assert included["deployments"] != included["scenarios"]
    assert_prisma_consistent(counts)


def test_same_record_without_a_retained_id_is_not_removed(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    write_csv(
        layout.normalized,
        [_record("rec_a", "scopus"), _record("rec_b", "pubmed")],
        NORMALIZED_FIELDS,
        tmp_path,
    )
    write_csv(
        layout.duplicates,
        [
            {
                "duplicate_group_id": "dup_test",
                "record_id_1": "rec_a",
                "record_id_2": "rec_b",
                "match_type": "EXACT_DOI",
                "doi_match": "YES",
                "exact_title_match": "NO",
                "fuzzy_title_score": "",
                "recommended_review": "YES",
                "human_decision": "SAME_RECORD",
                "human_reason": "",
                "decision_by": "reviewer",
                "decision_date": "",
                "retained_record_id": "",
            }
        ],
        DUPLICATE_FIELDS,
        tmp_path,
    )
    counts = build_prisma_counts(layout)
    duplicates = counts["duplicates"]
    assert isinstance(duplicates, dict)
    assert duplicates["confirmed_same_record_pairs"] == 1
    assert duplicates["records_removed"] == 0
    assert counts["records_after_confirmed_duplicate_removal"] == 2
