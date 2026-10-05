"""Extraction integrity. Missing reporting stays distinct from NO."""

from __future__ import annotations

from pathlib import Path

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import write_csv
from inthewild_review.schemas import (
    DEPLOYMENT_FIELDS,
    DEPLOYMENT_TRI_STATE_FIELDS,
    FULL_TEXT_FIELDS,
    NORMALIZED_FIELDS,
    PUBLICATION_FIELDS,
    SCENARIO_FIELDS,
    SCENARIO_TRI_STATE_FIELDS,
    SCREENING_FIELDS,
    STUDY_FIELDS,
)
from inthewild_review.synthesis import _tri_counts
from inthewild_review.validation import validate_repository


def _blank(fields: list[str], **overrides: str) -> dict[str, str]:
    row = {field: "" for field in fields}
    row.update(overrides)
    return row


def _deployment(deployment_id: str, study_id: str, **overrides: str) -> dict[str, str]:
    row = _blank(
        DEPLOYMENT_FIELDS,
        deployment_id=deployment_id,
        study_id=study_id,
        setting_type="PRIVATE_HOME",
        continuous_vs_episodic="EPISODIC",
        single_or_multiple_embodiments="SINGLE",
    )
    for field in DEPLOYMENT_TRI_STATE_FIELDS:
        row[field] = "NOT_REPORTED_OR_UNCLEAR"
    row.update(overrides)
    return row


def _scenario(scenario_id: str, deployment_id: str, study_id: str, publication_id: str) -> dict[str, str]:
    row = _blank(
        SCENARIO_FIELDS,
        scenario_id=scenario_id,
        deployment_id=deployment_id,
        study_id=study_id,
        publication_id=publication_id,
        scenario_explicitness="IMPLICIT",
        provenance_codes="IMPLICIT_EVERYDAY_ACTIVITY|FIELD_OBSERVATION",
    )
    for field in SCENARIO_TRI_STATE_FIELDS:
        row[field] = "NOT_REPORTED_OR_UNCLEAR"
    return row


def _full_text_include(record_id: str) -> dict[str, str]:
    row = _blank(FULL_TEXT_FIELDS, record_id=record_id, decision="INCLUDE", full_text_available="YES")
    for field in (
        "physically_embodied_robot",
        "substantive_social_interaction",
        "human_participants",
        "naturalistic_or_repeated_longterm",
        "identifiable_interaction_situation",
        "setting_extractable",
        "duration_extractable",
        "interaction_structure_extractable",
    ):
        row[field] = "YES"
    return row


def _write_chain(layout: ReviewLayout, relationship_history: str) -> None:
    root = layout.root
    write_csv(
        layout.normalized,
        [_blank(NORMALIZED_FIELDS, record_id="rec_a", title="SYNTHETIC TEST FIXTURE", origin="database")],
        NORMALIZED_FIELDS,
        root,
    )
    write_csv(layout.full_text, [_full_text_include("rec_a")], FULL_TEXT_FIELDS, root)
    write_csv(
        layout.publications,
        [
            _blank(
                PUBLICATION_FIELDS,
                publication_id="pub_a",
                record_id="rec_a",
                title="SYNTHETIC TEST FIXTURE",
            )
        ],
        PUBLICATION_FIELDS,
        root,
    )
    write_csv(
        layout.studies,
        [_blank(STUDY_FIELDS, study_id="study_a", publication_id="pub_a")],
        STUDY_FIELDS,
        root,
    )
    write_csv(
        layout.deployments,
        [_deployment("dep_a", "study_a")],
        DEPLOYMENT_FIELDS,
        root,
    )
    scenario = _scenario("scen_a", "dep_a", "study_a", "pub_a")
    scenario["relationships_and_history"] = relationship_history
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, root)


def test_foreign_keys_and_not_reported_are_distinct_from_no(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    _write_chain(layout, "NOT_REPORTED_OR_UNCLEAR")
    assert validate_repository(layout) == []
    stored = layout.scenarios.read_text(encoding="utf-8")
    assert "NOT_REPORTED_OR_UNCLEAR" in stored
    assert validate_repository(layout) == []
    from inthewild_review.io_utils import read_csv

    scenario = read_csv(layout.scenarios)[0]
    assert scenario["relationships_and_history"] == "NOT_REPORTED_OR_UNCLEAR"
    scenario["relationships_and_history"] = "NO"
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, tmp_path)
    assert validate_repository(layout) == []
    assert read_csv(layout.scenarios)[0]["relationships_and_history"] == "NO"
    counts = _tri_counts(read_csv(layout.scenarios), "relationships_and_history")
    assert counts["NO"] == 1
    assert counts["NOT_REPORTED_OR_UNCLEAR"] == 0


def test_blank_tri_state_and_orphan_scenario_fail(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    _write_chain(layout, "NOT_REPORTED_OR_UNCLEAR")
    from inthewild_review.io_utils import read_csv

    scenario = read_csv(layout.scenarios)[0]
    scenario["relationships_and_history"] = ""
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, tmp_path)
    blank_issues = validate_repository(layout)
    assert any(issue.code == "INVALID_TRI_STATE" for issue in blank_issues)
    scenario["relationships_and_history"] = "NOT_REPORTED_OR_UNCLEAR"
    scenario["deployment_id"] = "dep_missing"
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, tmp_path)
    orphan_issues = validate_repository(layout)
    assert any(issue.code == "ORPHAN_SCENARIO" for issue in orphan_issues)


def test_illegal_provenance_and_consensus_without_reviewers_fail(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    _write_chain(layout, "NOT_REPORTED_OR_UNCLEAR")
    from inthewild_review.io_utils import read_csv

    scenario = read_csv(layout.scenarios)[0]
    scenario["provenance_codes"] = "NOT_REPORTED_OR_UNCLEAR|FICTION_DERIVED"
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, tmp_path)
    mixed = validate_repository(layout)
    assert any(issue.code == "INVALID_PROVENANCE" for issue in mixed)
    scenario["provenance_codes"] = "MADE_UP_CODE"
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, tmp_path)
    illegal = validate_repository(layout)
    assert any(issue.code == "INVALID_PROVENANCE" for issue in illegal)
    write_csv(
        layout.calibration_consensus,
        [
            _blank(
                SCREENING_FIELDS,
                record_id="rec_a",
                reviewer="CONSENSUS",
                decision="MAYBE",
            )
        ],
        SCREENING_FIELDS,
        tmp_path,
    )
    issues = validate_repository(layout)
    assert any(issue.code == "CONSENSUS_WITHOUT_INDEPENDENT_RATINGS" for issue in issues)


def test_hybrid_provenance_can_carry_more_than_one_code(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    _write_chain(layout, "YES")
    from inthewild_review.io_utils import read_csv

    scenario = read_csv(layout.scenarios)[0]
    scenario["provenance_codes"] = "HYBRID|RESEARCHER_AUTHORED|CO_DESIGNED_PARTICIPATORY"
    write_csv(layout.scenarios, [scenario], SCENARIO_FIELDS, tmp_path)
    assert validate_repository(layout) == []
