"""Derived readable validation packets stay faithful, blinded, and deterministic."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from app.services.readable_packets import (
    CASE_IDS,
    DEFAULT_INVESTIGATOR_PATH,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_RESIDENT_PATH,
    build_readable_packets,
)

REPO = Path(__file__).resolve().parents[1]
FROZEN_FILES = (
    "batch_plan.json",
    "resident_validation_cases.json",
    "resident_review_worksheet.csv",
    "resident_review_schema.json",
    "investigator_answer_key.json",
    "investigator_answer_key.md",
    "validation_manifest.json",
    "coverage_report.md",
    "scenario_coverage_matrix.md",
)
BLINDED_RELATIVE_PATHS = (
    "all_cases.md",
    "plausibility_only_packet.md",
    *[f"cases/{case_id}.md" for case_id in CASE_IDS],
)
GENERIC_SAFE_RELATIVE_PATHS = (
    "how_cliniproof_works.md",
    "developer_notes.md",
    "validation_rubric.md",
    "reviewer_protocol.md",
    "README.md",
)
EXPECTED_FROZEN_HASHES = {
    "batch_plan.json": (
        "2a34f26326655c9c786263d32bcf87cbb99b9a90a9171fbd34758a62281f955d"
    ),
    "resident_validation_cases.json": (
        "90227220afcc2398c969f36a1cc27bc11a4a04de39c6a93b495cca649b2cfdec"
    ),
    "investigator_answer_key.json": (
        "6d82319ba48d1dfea6b0fe6fd6fd1d07f5fe970f907e44968193cc5aaa2ea07d"
    ),
    "investigator_answer_key.md": (
        "425cb79d7ace8c4c379ed5f1cdfeaf957c25c0f4d9e3a4960347885d11e81e0b"
    ),
    "validation_manifest.json": (
        "1b6a87d3c48bc31896ac5ac2629fa1ac68118504384bef36994940623f02feba"
    ),
    "coverage_report.md": (
        "d399eb61010ba7c1643ae3dd0ec911c1aaecf360061fad40be2f3aa9f4bf15d2"
    ),
    "scenario_coverage_matrix.md": (
        "9a24b908d7d953e0d50770f75c6890db0b5015405a0c7c5a1ea6132cab7c7582"
    ),
    "resident_review_worksheet.csv": (
        "8178c07c5e85fd66d845472f498297c6a3f97c1dfda426efa706b3680ba694c1"
    ),
    "resident_review_schema.json": (
        "118edb2a716988aa2891c30c512af931d54957a49e6f77989542299bd40fc6c7"
    ),
}
ANSWER_KEY_NEEDLES = (
    "error_family",
    "error_category",
    "is_clean_control",
    "error_bearing",
    "NO INTENTIONAL ERROR",
    "correct_action",
    "clean_expected_state",
    "injected_state",
    "detectability_location",
    "family_1",
    "family_2",
    "f1_",
    "f2_",
    "SYN-",
)
CANONICAL_IDS = (
    "f1_omission",
    "f1_commission",
    "f1_dose_mismatch",
    "f1_route_mismatch",
    "f1_frequency_mismatch",
    "f1_therapeutic_substitution",
    "f2_monitoring_not_arranged",
    "f2_held_med_no_restart_plan",
    "f2_insufficient_supply",
    "f2_hospital_only_continued",
    "f2_inpatient_substitution_not_reverted",
    "f2_pending_decision_followup_missing",
    "f2_coprescription_omitted",
)
RANGE_PHRASES = (
    "VAL-201 through VAL-224",
    "VAL-201–VAL-224",
    "`VAL-201`–`VAL-224`",
    "VAL-201`–`VAL-224",
)


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _frozen_hashes() -> dict[str, str]:
    root = REPO / "data" / "validation"
    return {name: _hash(root / name) for name in FROZEN_FILES}


def _strip_case_range(text: str) -> str:
    stripped = text
    for phrase in RANGE_PHRASES:
        stripped = stripped.replace(phrase, "CASE_RANGE")
    return stripped


def test_committed_readable_packets_cover_all_current_cases() -> None:
    cases_dir = DEFAULT_OUTPUT_DIR / "cases"
    names = sorted(path.name for path in cases_dir.glob("VAL-*.md"))
    assert names == [f"{case_id}.md" for case_id in CASE_IDS]
    all_cases = (DEFAULT_OUTPUT_DIR / "all_cases.md").read_text(encoding="utf-8")
    plausibility = (DEFAULT_OUTPUT_DIR / "plausibility_only_packet.md").read_text(encoding="utf-8")
    investigator = (DEFAULT_OUTPUT_DIR / "clinician_validation_packet.md").read_text(
        encoding="utf-8"
    )
    rubric = (DEFAULT_OUTPUT_DIR / "validation_rubric.md").read_text(encoding="utf-8")
    how = (DEFAULT_OUTPUT_DIR / "how_cliniproof_works.md").read_text(encoding="utf-8")
    developer = (DEFAULT_OUTPUT_DIR / "developer_notes.md").read_text(encoding="utf-8")
    for case_id in CASE_IDS:
        heading = f"# {case_id}"
        assert all_cases.count(heading) == 1
        assert plausibility.count(heading) == 1
        assert investigator.count(heading) == 1
        assert (cases_dir / f"{case_id}.md").read_text(encoding="utf-8").startswith(heading)
    protocol = (DEFAULT_OUTPUT_DIR / "reviewer_protocol.md").read_text(encoding="utf-8")
    assert plausibility.count("### C1 Clinical plausibility") == 24
    assert investigator.count("### C1 Clinical plausibility") == 0
    assert investigator.count("### C2 Intended assessment problem") == 24
    assert investigator.count("### C3 Detectability") == 24
    assert investigator.count("### C4 Absence of unintended problems") == 24
    assert investigator.count("### C5 Expected learner difficulty") == 24
    assert "Investigator / Clinical Validator Copy" in investigator
    assert "INVESTIGATOR / VALIDATOR ONLY" in investigator
    assert "f2_coprescription_omitted" in rubric
    assert "not_yet_implementable" in rubric
    assert "How CliniProof Builds and Validates a Case" in how
    assert "CliniProof Implementation Notes" in developer
    assert all_cases.startswith("# CliniProof Clinical Case Set")
    assert protocol.startswith("# Clinical Validation Protocol")
    assert "Two clinical experts independently review all 24 cases." in protocol


def test_plausibility_files_do_not_contain_answer_key_fields() -> None:
    for relative in BLINDED_RELATIVE_PATHS:
        blob = (DEFAULT_OUTPUT_DIR / relative).read_text(encoding="utf-8")
        leaked = [needle for needle in ANSWER_KEY_NEEDLES if needle in blob]
        assert leaked == [], f"{relative} leaked {leaked}"
        assert re.search(r"SYN\d", blob) is None, f"{relative} leaked a SYN identifier"


def test_generic_overviews_do_not_reveal_per_val_answers() -> None:
    investigator = json.loads(DEFAULT_INVESTIGATOR_PATH.read_text(encoding="utf-8"))
    keys = {row["validation_case_id"]: row for row in investigator["cases"]}
    for relative in GENERIC_SAFE_RELATIVE_PATHS:
        blob = _strip_case_range((DEFAULT_OUTPUT_DIR / relative).read_text(encoding="utf-8"))
        for case_id in CASE_IDS:
            assert case_id not in blob, (
                f"{relative} mentions {case_id} outside the study-range phrase"
            )
            error = keys[case_id].get("error") or {}
            action = error.get("correct_action")
            if isinstance(action, str) and action.strip():
                assert action not in blob, f"{relative} leaked correct_action for {case_id}"
            for med in error.get("trigger_meds") or []:
                drug = med.get("drug")
                if drug:
                    assert not re.search(
                        rf"{re.escape(case_id)}.{{0,80}}{re.escape(str(drug))}",
                        blob,
                        flags=re.S,
                    )


def test_canonical_ids_appear_in_framework_docs_not_blinded_cases() -> None:
    how = (DEFAULT_OUTPUT_DIR / "how_cliniproof_works.md").read_text(encoding="utf-8")
    developer = (DEFAULT_OUTPUT_DIR / "developer_notes.md").read_text(encoding="utf-8")
    rubric = (DEFAULT_OUTPUT_DIR / "validation_rubric.md").read_text(encoding="utf-8")
    investigator = (DEFAULT_OUTPUT_DIR / "clinician_validation_packet.md").read_text(
        encoding="utf-8"
    )
    for identifier in CANONICAL_IDS:
        assert identifier in how, identifier
        assert identifier in developer, identifier
        assert identifier in rubric, identifier
    assert "f1_omission" in investigator
    assert "f2_monitoring_not_arranged" in investigator
    blinded = "\n".join(
        (DEFAULT_OUTPUT_DIR / relative).read_text(encoding="utf-8")
        for relative in BLINDED_RELATIVE_PATHS
    )
    for identifier in CANONICAL_IDS:
        assert identifier not in blinded


def test_investigator_packet_contains_concealed_targets() -> None:
    blob = (DEFAULT_OUTPUT_DIR / "clinician_validation_packet.md").read_text(encoding="utf-8")
    assert "Clinical category:" in blob
    assert "CliniProof identifier:" in blob
    assert "family_1" in blob
    assert "family_2" in blob
    assert "f1_omission" in blob
    assert "f2_monitoring_not_arranged" in blob
    assert "Expected clinical action:" in blob
    assert "Medication(s) involved:" in blob
    assert "NO INTENTIONAL ERROR" in blob
    assert "What should have occurred clinically:" in blob
    assert "What appears in the case:" in blob
    assert "Where the relevant evidence appears:" in blob


def test_readable_case_text_is_taken_from_frozen_resident_json() -> None:
    resident = json.loads(DEFAULT_RESIDENT_PATH.read_text(encoding="utf-8"))
    investigator = json.loads(DEFAULT_INVESTIGATOR_PATH.read_text(encoding="utf-8"))
    cases = {row["case_id_code"]: row for row in resident["cases"]}
    keys = {row["validation_case_id"]: row for row in investigator["cases"]}
    page = (DEFAULT_OUTPUT_DIR / "cases" / "VAL-201.md").read_text(encoding="utf-8")
    clinical = cases["VAL-201"]["ClinicalCase"]
    assert str(clinical["patient_age"]) in page
    assert clinical["admission_dx"] in page
    assert cases["VAL-201"]["CaseLab"][0]["test_name"] in page
    assert cases["VAL-201"]["CaseMedication"][0]["drug"] in page
    assert cases["VAL-201"]["CaseNote"][0]["note_text"] in page
    assert "## Patient overview" in page
    assert "## Home medications" in page
    assert "## Medications during hospitalization" in page
    assert "## About the case data" in page
    assert "error_family" not in page
    packet = (DEFAULT_OUTPUT_DIR / "clinician_validation_packet.md").read_text(encoding="utf-8")
    error = keys["VAL-201"]["error"]
    assert error["error_category"] in packet
    assert error["correct_action"] in packet
    assert error["trigger_meds"][0]["drug"] in packet


def test_generator_is_deterministic_and_does_not_mutate_frozen_sources(
    tmp_path: Path,
) -> None:
    before = _frozen_hashes()
    first = tmp_path / "first"
    second = tmp_path / "second"
    build_readable_packets(output_dir=first)
    build_readable_packets(output_dir=second)
    first_files = sorted(
        path.relative_to(first).as_posix() for path in first.rglob("*") if path.is_file()
    )
    second_files = sorted(
        path.relative_to(second).as_posix() for path in second.rglob("*") if path.is_file()
    )
    assert first_files == second_files
    assert "how_cliniproof_works.md" in first_files
    assert "developer_notes.md" in first_files
    assert "reviewer_protocol.md" in first_files
    assert "clinical_validation_worksheet.csv" in first_files
    assert "consensus_worksheet.csv" in first_files
    for relative in first_files:
        assert (first / relative).read_bytes() == (second / relative).read_bytes()
        committed = DEFAULT_OUTPUT_DIR / relative
        assert committed.is_file()
        assert (first / relative).read_bytes() == committed.read_bytes()
    assert _frozen_hashes() == before
    assert hashlib.sha256(DEFAULT_RESIDENT_PATH.read_bytes()).hexdigest() == before[
        "resident_validation_cases.json"
    ]
    assert hashlib.sha256(DEFAULT_INVESTIGATOR_PATH.read_bytes()).hexdigest() == before[
        "investigator_answer_key.json"
    ]


def test_each_case_id_appears_exactly_once_in_case_directory() -> None:
    names = [path.stem for path in (DEFAULT_OUTPUT_DIR / "cases").glob("VAL-*.md")]
    assert sorted(names) == list(CASE_IDS)
    assert len(set(names)) == 24


def test_frozen_source_hashes_remain_unchanged() -> None:
    assert _frozen_hashes() == EXPECTED_FROZEN_HASHES


def _nonempty_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def test_reviewer_worksheets_are_empty_templates() -> None:
    independent = (DEFAULT_OUTPUT_DIR / "clinical_validation_worksheet.csv").read_text(
        encoding="utf-8"
    )
    consensus = (DEFAULT_OUTPUT_DIR / "consensus_worksheet.csv").read_text(encoding="utf-8")
    independent_lines = _nonempty_lines(independent)
    consensus_lines = _nonempty_lines(consensus)
    assert len(independent_lines) == 1
    assert len(consensus_lines) == 1
    assert independent_lines[0].startswith("validation_case_id,reviewer_id,review_round,")
    assert "initial_recommendation" in independent_lines[0]
    assert "consensus_outcome" not in independent_lines[0]
    assert consensus_lines[0].startswith("validation_case_id,reviewer_a_recommendation,")
    assert "consensus_outcome" in consensus_lines[0]
    for case_id in CASE_IDS:
        assert case_id not in independent
        assert case_id not in consensus


def test_reviewer_protocol_describes_two_independent_reviewers() -> None:
    protocol = (DEFAULT_OUTPUT_DIR / "reviewer_protocol.md").read_text(encoding="utf-8")
    rubric = (DEFAULT_OUTPUT_DIR / "validation_rubric.md").read_text(encoding="utf-8")
    investigator = (DEFAULT_OUTPUT_DIR / "clinician_validation_packet.md").read_text(
        encoding="utf-8"
    )
    plausibility = (DEFAULT_OUTPUT_DIR / "plausibility_only_packet.md").read_text(
        encoding="utf-8"
    )
    assert "Two clinical experts independently review all 24 cases." in protocol
    assert "independent dual expert review with structured consensus resolution" in protocol
    assert "is not a Delphi process" in protocol
    assert "is not a modified Delphi process" in protocol
    for match in re.finditer(r".{0,48}Delphi.{0,48}", protocol):
        snippet = match.group(0).lower()
        assert "not" in snippet, snippet
    assert "complete C1 before seeing the answer key" in protocol
    assert "independently complete C2 through C5" in protocol
    assert "Original ratings remain unchanged" in protocol
    assert "A separate consensus outcome is recorded" in protocol
    assert (
        "If consensus cannot be achieved, the case is not considered clinically validated."
        in protocol
    )
    assert "☐ Accept" in investigator
    assert "☐ Revise" in investigator
    assert "☐ Exclude" in investigator
    assert "☐ Adjudicate" not in investigator
    assert "Adjudication required" not in investigator
    assert "Revise and re-rate" not in investigator
    assert "Regenerate / retire" not in investigator
    assert "☐ Accept" not in plausibility
    assert "☐ Exclude" not in plausibility
    assert (
        "Both clinical reviewers complete this section independently before seeing "
        "the intended assessment target."
    ) in plausibility
    assert (
        "Reviewers should complete and submit the blinded C1 plausibility review "
        "before using this packet."
    ) in investigator
    assert "☐ Accepted" in rubric
    assert "☐ Unresolved" in rubric
    assert "Do not overwrite original reviewer ratings with the consensus result." in rubric
    assert "Recommended revision" in rubric


def test_consensus_is_stored_separately_from_independent_ratings() -> None:
    protocol = (DEFAULT_OUTPUT_DIR / "reviewer_protocol.md").read_text(encoding="utf-8")
    independent = (DEFAULT_OUTPUT_DIR / "clinical_validation_worksheet.csv").read_text(
        encoding="utf-8"
    )
    consensus = (DEFAULT_OUTPUT_DIR / "consensus_worksheet.csv").read_text(encoding="utf-8")
    investigator = (DEFAULT_OUTPUT_DIR / "clinician_validation_packet.md").read_text(
        encoding="utf-8"
    )
    assert "not on the independent reviewer row" in protocol
    assert "consensus_outcome" in consensus
    assert "consensus_outcome" not in independent
    assert "Do not record consensus on this independent form." in investigator
    assert "Original independent ratings are preserved" in investigator or (
        "Original independent C1 ratings remain unchanged." in investigator
    )
