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
    "README.md",
)
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
    assert plausibility.count("### C1 Clinical plausibility") == 24
    assert investigator.count("### C1 Clinical plausibility") == 24
    assert investigator.count("### C2 Intended error present and correctly classified") == 24
    assert investigator.count("### C5 Difficulty for internal medicine resident") == 24
    assert "Investigator / Clinical Validator Copy" in investigator
    assert "INVESTIGATOR / VALIDATOR ONLY" in investigator
    assert "f2_coprescription_omitted" in rubric
    assert "not_yet_implementable" in rubric
    assert "How CliniProof Builds and Validates a Case" in how
    assert "CliniProof Implementation Notes" in developer
    assert all_cases.startswith("# CliniProof Clinical Case Set")


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
    assert "What should have occurred:" in blob
    assert "What appears in the case:" in blob


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
