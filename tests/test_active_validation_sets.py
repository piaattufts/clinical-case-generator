"""Two active prospective sets plus archived V1/V2 preclinical provenance."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

import pytest
from app.cli import cli
from app.services.batch_comparison import summarize_batch, write_active_batch_comparison
from app.services.case_diversity import require_unique_clean_cases
from app.services.readable_packets import main as readable_main
from app.services.validation_batch import load_batch_plan
from app.services.validation_registry import (
    ARCHIVED_BATCH_CODE,
    BALANCED_BATCH_CODE,
    PRECLINICAL_BALANCED_CODE,
    PRECLINICAL_SEED_CODE,
    SEEDCASES_BATCH_CODE,
    STRATEGY_BALANCED,
    STRATEGY_ORIGINAL,
    STRATEGY_SEED,
    active_batch_codes,
    archived_batch_codes,
    get_batch,
    missing_batch_code_message,
)
from typer.testing import CliRunner

from tests.test_case_diversity import EXPECTED_V1_HASHES
from tests.test_seed_batch import EXPECTED_SEED_HASHES, EXPECTED_V2_HASHES

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
INDEX = REPO / "data" / "active_validation_sets.md"
COMPARISON = REPO / "data" / "validation_comparison" / "active_batch_comparison.md"
REGISTRY = REPO / "data" / "validation_registry.json"
SEED_LEAK_NEEDLES = (
    "seed_archetype_id",
    "seed_archetype_name",
    "seed_source_filename",
    "blueprint_version",
    "resident_authored",
    "Bad_Med_Rec_Case.docx",
    "Heart_Failure_Case.docx",
    "OPAT_Case.docx",
    "Post_Transplant_Case.docx",
    "Post-op_Case.docx",
    "Sepsis_AMA_Case.docx",
)
ANSWER_KEY_NEEDLES = (
    "CaseAnswerKey",
    "is_clean_control",
    "error_family",
    "error_category",
    "clean_expected_state",
    "injected_state",
    "correct_action",
)
FORBIDDEN_CURRENT_STUDY_PHRASES = (
    "the current study set is CLINIPROOF_TAXONOMY_V1",
    "--batch-code` defaults to `CLINIPROOF_TAXONOMY_V1",
    "holds tracked study artifacts for `CLINIPROOF_TAXONOMY_V1`",
    "The study batch `CLINIPROOF_TAXONOMY_V1`",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_hashes(root: Path, expected: dict[str, str]) -> None:
    for name, digest in expected.items():
        actual = _hash(root / name)
        assert actual == digest, f"{root / name} hash changed"


def _case_ids(first: str, last: str) -> list[str]:
    start = int(first.removeprefix("VAL-"))
    end = int(last.removeprefix("VAL-"))
    return [f"VAL-{index:03d}" for index in range(start, end + 1)]


def _load(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_registry_separates_active_and_archived_batches() -> None:
    raw = _load(REGISTRY)
    assert raw["active_validation_batches"] == [
        BALANCED_BATCH_CODE,
        SEEDCASES_BATCH_CODE,
    ]
    assert raw["archived_validation_batches"] == [
        ARCHIVED_BATCH_CODE,
        PRECLINICAL_BALANCED_CODE,
        PRECLINICAL_SEED_CODE,
        "CLINIPROOF_BALANCED_V3",
        "CLINIPROOF_SEEDCASES_V2",
    ]
    assert active_batch_codes() == (BALANCED_BATCH_CODE, SEEDCASES_BATCH_CODE)
    assert archived_batch_codes() == (
        ARCHIVED_BATCH_CODE,
        PRECLINICAL_BALANCED_CODE,
        PRECLINICAL_SEED_CODE,
        "CLINIPROOF_BALANCED_V3",
        "CLINIPROOF_SEEDCASES_V2",
    )
    assert ARCHIVED_BATCH_CODE not in active_batch_codes()
    balanced = get_batch(BALANCED_BATCH_CODE)
    seed = get_batch(SEEDCASES_BATCH_CODE)
    archived = get_batch(ARCHIVED_BATCH_CODE)
    assert balanced.is_active
    assert seed.is_active
    assert archived.is_archived
    assert get_batch(PRECLINICAL_BALANCED_CODE).is_archived
    assert get_batch(PRECLINICAL_SEED_CODE).is_archived
    assert balanced.generation_strategy == STRATEGY_BALANCED
    assert seed.generation_strategy == STRATEGY_SEED
    assert archived.generation_strategy == STRATEGY_ORIGINAL
    assert balanced.case_ids() == tuple(_case_ids("VAL-701", "VAL-724"))
    assert seed.case_ids() == tuple(_case_ids("VAL-801", "VAL-824"))
    assert archived.case_ids() == tuple(_case_ids("VAL-201", "VAL-224"))


def test_v1_frozen_source_hashes_are_unchanged() -> None:
    _assert_hashes(REPO / "data" / "validation", EXPECTED_V1_HASHES)


def test_preclinical_qc_freezes_remain_hashed() -> None:
    _assert_hashes(REPO / "data" / "validation_balanced", EXPECTED_V2_HASHES)
    _assert_hashes(REPO / "data" / "validation_seedcases", EXPECTED_SEED_HASHES)


def _require_frozen() -> None:
    for spec in (get_batch(BALANCED_BATCH_CODE), get_batch(SEEDCASES_BATCH_CODE)):
        if not (spec.directory / "resident_validation_cases.json").is_file():
            pytest.skip(f"{spec.code} freeze artifacts are not written yet")


def test_active_batches_have_twenty_four_cases_and_non_overlapping_ids() -> None:
    _require_frozen()
    balanced_ids = set(get_batch(BALANCED_BATCH_CODE).case_ids())
    seed_ids = set(get_batch(SEEDCASES_BATCH_CODE).case_ids())
    archived_ids = set(get_batch(ARCHIVED_BATCH_CODE).case_ids())
    preclinical_balanced = set(get_batch(PRECLINICAL_BALANCED_CODE).case_ids())
    preclinical_seed = set(get_batch(PRECLINICAL_SEED_CODE).case_ids())
    assert len(balanced_ids) == 24
    assert len(seed_ids) == 24
    assert len(archived_ids) == 24
    assert not balanced_ids & seed_ids
    assert not balanced_ids & archived_ids
    assert not seed_ids & archived_ids
    assert not balanced_ids & preclinical_balanced
    assert not seed_ids & preclinical_seed
    for spec in (get_batch(BALANCED_BATCH_CODE), get_batch(SEEDCASES_BATCH_CODE)):
        resident = _load(spec.directory / "resident_validation_cases.json")
        investigator = _load(spec.directory / "investigator_answer_key.json")
        assert resident["batch_code"] == spec.code
        assert investigator["batch_code"] == spec.code
        resident_ids = [row["case_id_code"] for row in resident["cases"]]
        investigator_ids = [row["validation_case_id"] for row in investigator["cases"]]
        assert resident_ids == list(spec.case_ids())
        assert investigator_ids == list(spec.case_ids())


def test_each_active_batch_has_independent_study_materials() -> None:
    _require_frozen()
    for spec in (get_batch(BALANCED_BATCH_CODE), get_batch(SEEDCASES_BATCH_CODE)):
        readable = spec.readable_dir
        assert (spec.directory / "investigator_answer_key.md").is_file()
        assert (spec.directory / "investigator_answer_key.json").is_file()
        assert (spec.directory / "validation_manifest.json").is_file()
        assert (spec.directory / "batch_plan.json").is_file()
        assert (spec.directory / "coverage_report.md").is_file()
        assert (spec.directory / "diversity_report.md").is_file()
        assert (readable / "all_cases.md").is_file()
        assert (readable / "clinician_validation_packet.md").is_file()
        assert (readable / "validation_rubric.md").is_file()
        worksheet = list(csv.DictReader((readable / "clinical_validation_worksheet.csv").open()))
        assert [row["validation_case_id"] for row in worksheet] == list(spec.case_ids())
        assert len(worksheet) == 24
        for case_id in spec.case_ids():
            assert (readable / "cases" / f"{case_id}.md").is_file()
        packet = (readable / "clinician_validation_packet.md").read_text(encoding="utf-8")
        assert spec.code in packet
        assert ARCHIVED_BATCH_CODE not in packet
        assert "single review stage" in packet
        assert packet.count("### C1 Clinical plausibility") == 24
        assert "Stage 1" not in packet
        assert "Stage 2" not in packet


def test_active_corpus_is_forty_eight_cases() -> None:
    assert len(get_batch(BALANCED_BATCH_CODE).case_ids()) + len(
        get_batch(SEEDCASES_BATCH_CODE).case_ids()
    ) == 48


def test_resident_exports_are_blinded_and_seed_provenance_stays_investigator_only() -> None:
    _require_frozen()
    for spec in (get_batch(BALANCED_BATCH_CODE), get_batch(SEEDCASES_BATCH_CODE)):
        resident_blob = (spec.directory / "resident_validation_cases.json").read_text(
            encoding="utf-8"
        )
        all_cases = (spec.readable_dir / "all_cases.md").read_text(encoding="utf-8")
        for needle in ANSWER_KEY_NEEDLES:
            assert needle not in resident_blob, f"{spec.code} resident leaked {needle}"
            if needle != "error_category":
                assert needle not in all_cases, f"{spec.code} all_cases leaked {needle}"
        if spec.code == SEEDCASES_BATCH_CODE:
            investigator = (spec.directory / "investigator_answer_key.json").read_text(
                encoding="utf-8"
            )
            assert "seed_archetype_id" in investigator
            assert "blueprint_version" in investigator
            assert "resident_authored" in investigator
            for needle in SEED_LEAK_NEEDLES:
                assert needle not in resident_blob, needle
                assert needle not in all_cases, needle
            for case_id in spec.case_ids():
                page = (spec.readable_dir / "cases" / f"{case_id}.md").read_text(encoding="utf-8")
                for needle in SEED_LEAK_NEEDLES:
                    assert needle not in page, f"{case_id} leaked {needle}"


def test_clean_case_uniqueness_holds_for_both_active_batches() -> None:
    _require_frozen()
    for spec, strategy in (
        (get_batch(BALANCED_BATCH_CODE), STRATEGY_BALANCED),
        (get_batch(SEEDCASES_BATCH_CODE), STRATEGY_SEED),
    ):
        summary = summarize_batch(
            resident_path=spec.directory / "resident_validation_cases.json",
            investigator_path=spec.directory / "investigator_answer_key.json",
            default_strategy=strategy,
        )
        assert summary["exact_duplicates"] == 0
        labeled = []
        resident = _load(spec.directory / "resident_validation_cases.json")
        investigator = _load(spec.directory / "investigator_answer_key.json")
        keys = {row["validation_case_id"]: row for row in investigator["cases"]}
        from app.services.batch_comparison import fingerprint_from_resident_case

        for case in resident["cases"]:
            case_id = case["case_id_code"]
            inv = keys[case_id]
            labeled.append(
                (
                    case_id,
                    fingerprint_from_resident_case(
                        case,
                        scenario=str(inv.get("scenario") or ""),
                        profile=str(inv.get("clinical_profile") or "default"),
                    ),
                )
            )
        require_unique_clean_cases(labeled)


def test_error_isolation_counts_match_investigator_keys() -> None:
    _require_frozen()
    for spec in (get_batch(BALANCED_BATCH_CODE), get_batch(SEEDCASES_BATCH_CODE)):
        investigator = _load(spec.directory / "investigator_answer_key.json")
        family_1 = family_2 = controls = 0
        for row in investigator["cases"]:
            error = row.get("error") or {}
            category = str(error.get("error_category") or "none")
            if category.startswith("f1_"):
                family_1 += 1
            elif category.startswith("f2_"):
                family_2 += 1
            else:
                controls += 1
        assert family_1 + family_2 + controls == 24
        assert controls == 4


def test_cli_and_plan_loader_do_not_silently_select_archived_v1() -> None:
    runner = CliRunner()
    export = runner.invoke(cli, ["export-validation-batch"])
    assert export.exit_code == 2
    assert "no default study batch" in export.output
    assert BALANCED_BATCH_CODE in export.output
    assert SEEDCASES_BATCH_CODE in export.output
    assert "Archived historical sets" in export.output
    freeze = runner.invoke(cli, ["freeze-validation-batch"])
    assert freeze.exit_code == 2
    assert "explicit --plan" in freeze.output
    with pytest.raises(ValueError, match="explicit --plan"):
        load_batch_plan()
    with pytest.raises(SystemExit):
        readable_main([])
    message = missing_batch_code_message()
    assert ARCHIVED_BATCH_CODE not in message.split("Active prospective sets:", 1)[1].split(
        "Archived historical sets", 1
    )[0]


def test_readme_and_index_route_to_two_active_sets() -> None:
    readme = README.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    lowered = readme.casefold()
    for phrase in FORBIDDEN_CURRENT_STUDY_PHRASES:
        assert phrase.casefold() not in lowered, phrase
    assert "two active prospective validation datasets" in lowered
    assert "48" in readme
    assert BALANCED_BATCH_CODE in readme
    assert SEEDCASES_BATCH_CODE in readme
    assert "CLINIPROOF_BALANCED_V3" in readme
    assert "CLINIPROOF_SEEDCASES_V2" in readme
    assert "CLINIPROOF_BALANCED_V2" in readme
    assert "CLINIPROOF_SEEDCASES_V1" in readme
    assert "archived historical provenance" in lowered or "historical provenance" in lowered
    assert "not** the current study set" in lowered or "not the current study set" in lowered
    assert "data/active_validation_sets.md" in readme
    assert BALANCED_BATCH_CODE in index
    assert SEEDCASES_BATCH_CODE in index
    assert "not** an active prospective study set" in index.casefold() or (
        "not an active prospective study set" in index.casefold()
    )


def test_markdown_navigation_links_resolve() -> None:
    top = README.read_text(encoding="utf-8").split("\n## Contents\n", 1)[0]
    files = [
        (README, top),
        (INDEX, INDEX.read_text(encoding="utf-8")),
        (COMPARISON, COMPARISON.read_text(encoding="utf-8")),
        (
            get_batch(ARCHIVED_BATCH_CODE).directory / "README.md",
            (get_batch(ARCHIVED_BATCH_CODE).directory / "README.md").read_text(encoding="utf-8"),
        ),
        (
            get_batch(BALANCED_BATCH_CODE).directory / "README.md",
            (get_batch(BALANCED_BATCH_CODE).directory / "README.md").read_text(encoding="utf-8"),
        ),
        (
            get_batch(SEEDCASES_BATCH_CODE).directory / "README.md",
            (get_batch(SEEDCASES_BATCH_CODE).directory / "README.md").read_text(encoding="utf-8"),
        ),
    ]
    for path, text in files:
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            assert resolved.exists(), f"{path} -> {target}"


def test_archived_v1_catalog_is_labeled_historical() -> None:
    catalog = (REPO / "data" / "validation" / "README.md").read_text(encoding="utf-8")
    readable = (REPO / "data" / "validation" / "readable" / "README.md").read_text(
        encoding="utf-8"
    )
    lowered_catalog = catalog.casefold()
    assert "historical / archived" in lowered_catalog or "archived historical" in lowered_catalog
    assert "not** an active prospective study set" in lowered_catalog or (
        "not an active prospective study set" in lowered_catalog
    )
    assert "archived historical provenance" in readable.casefold()
    packet_path = REPO / "data" / "validation" / "readable" / "clinician_validation_packet.md"
    packet = packet_path.read_text(encoding="utf-8")
    assert "archived historical provenance" in packet.casefold()


def test_active_batch_comparison_is_descriptive() -> None:
    _require_frozen()
    write_active_batch_comparison(COMPARISON)
    blob = COMPARISON.read_text(encoding="utf-8")
    assert "does not rank" in blob
    assert STRATEGY_BALANCED in blob
    assert STRATEGY_SEED in blob
    assert ARCHIVED_BATCH_CODE in blob
    assert "Exact duplicate fingerprints" in blob
    assert "Specialty distribution" in blob
    left = summarize_batch(
        resident_path=get_batch(BALANCED_BATCH_CODE).directory / "resident_validation_cases.json",
        investigator_path=get_batch(BALANCED_BATCH_CODE).directory / "investigator_answer_key.json",
        default_strategy=STRATEGY_BALANCED,
    )
    right = summarize_batch(
        resident_path=get_batch(SEEDCASES_BATCH_CODE).directory / "resident_validation_cases.json",
        investigator_path=get_batch(SEEDCASES_BATCH_CODE).directory
        / "investigator_answer_key.json",
        default_strategy=STRATEGY_SEED,
    )
    assert left["exact_duplicates"] == 0
    assert right["exact_duplicates"] == 0
    assert left["case_count"] == 24
    assert right["case_count"] == 24
