"""The additional seed-guided batch is separate from the frozen VAL-801 set."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from app.services.seed_archetypes import GENERATION_STRATEGY_SEED
from app.services.validation_batch import load_batch_plan, parse_assignments

REPO = Path(__file__).resolve().parents[1]
V3 = REPO / "data" / "case_sets" / "seed_guided"
V4 = REPO / "data" / "case_sets" / "seed_guided_v4"
SOURCE_FACTS = (
    "chinatown",
    "cantonese",
    "gallolyticus",
    "5360",
    "eliquis",
    "alzheimer",
    "bioprosthetic avr",
    "bileaflet",
)
LEAK_MARKERS = (
    "answer_key",
    "error_category",
    "error_family",
    "clean_expected_state",
    "reference_discharge_plan",
    "generation_strategy",
    "resident_seed_guided",
    "seed_archetype",
    ".docx",
    "blueprint_version",
)


def _load(name: str) -> dict[str, Any]:
    payload: Any = json.loads((V4 / name).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError(name)
    return payload


def test_original_seed_guided_freeze_is_unchanged() -> None:
    text = (REPO / "docs" / "source_integrity.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"`(data/case_sets/seed_guided/[^`]+\.(?:json|md|csv))` \| `([0-9a-f]{64})`",
        text,
    )
    assert len(rows) >= 40
    for relative, digest in rows:
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        assert actual == digest, relative
    assert not (V3 / "VAL-901_resident.json").exists()
    v3_plan = load_batch_plan(V3 / "batch_plan.json")
    assert v3_plan["batch_code"] == "CLINIPROOF_SEEDCASES_V3"
    assert [item.validation_case_id for item in parse_assignments(v3_plan)][0] == "VAL-801"


def test_v4_plan_is_a_separate_resident_seed_guided_batch() -> None:
    plan = load_batch_plan(V4 / "batch_plan.json")
    assignments = parse_assignments(plan)
    assert plan["batch_code"] == "CLINIPROOF_SEEDCASES_V4"
    assert plan["generation_strategy"] == GENERATION_STRATEGY_SEED
    assert plan["master_seed"] != 20260926
    assert len(assignments) == 24
    assert [item.validation_case_id for item in assignments] == [
        f"VAL-{number}" for number in range(901, 925)
    ]
    assert len({item.validation_case_id for item in assignments}) == 24
    assert {item.generation_strategy for item in assignments} == {GENERATION_STRATEGY_SEED}
    families: dict[str, int] = {}
    for item in assignments:
        families[item.scenario] = families.get(item.scenario, 0) + 1
    assert families == {
        "MEDREC_UNCERTAIN_HISTORY": 4,
        "HF_DECOMPENSATION": 4,
        "OPAT_ENDOCARDITIS": 4,
        "TRANSPLANT_CMV": 4,
        "POSTOP_ANTICOAGULATION": 4,
        "GI_BLEED_ACUTE_CHANGE": 4,
    }
    assert len({item.clinical_profile for item in assignments}) == 24
    assert sum(1 for item in assignments if not item.inject_error) == 4
    assert all(item.error_category for item in assignments if item.inject_error)


def test_v4_freeze_matches_the_plan_and_validates_clean_cases_first() -> None:
    assignments = parse_assignments(load_batch_plan(V4 / "batch_plan.json"))
    plan = {item.validation_case_id: item for item in assignments}
    investigator = _load("investigator_answer_key.json")
    manifest = _load("validation_manifest.json")
    assert investigator["batch_code"] == "CLINIPROOF_SEEDCASES_V4"
    assert manifest["batch_code"] == "CLINIPROOF_SEEDCASES_V4"
    assert len(investigator["cases"]) == 24
    manifest_by_id = {item["validation_case_id"]: item for item in manifest["cases"]}
    rxcuis: set[str] = set()
    loinc_codes: set[str] = set()
    icd_codes: set[str] = set()
    for case in investigator["cases"]:
        assignment = plan[case["validation_case_id"]]
        assert case["generation_strategy"] == GENERATION_STRATEGY_SEED
        assert case["clinical_profile"] == assignment.clinical_profile
        assert case["seed_archetype_id"] == assignment.scenario
        assert case["clean_validation"]["passed"] is True
        assert case["post_injection_validation"]["passed"] is True
        error = case["error"]
        identifiers = case["canonical_identifiers"]
        rxcuis.update(identifiers["rxcuis"])
        loinc_codes.update(identifiers["loinc_codes"])
        icd_codes.update(identifiers["icd10cm_codes"])
        manifest_row = manifest_by_id[case["validation_case_id"]]
        assert manifest_row["clean_validation_status"] == "passed"
        assert manifest_row["post_injection_validation_status"] == "passed"
        if assignment.inject_error:
            assert error["control_error_status"] == "error_bearing"
            assert error["error_category"] == assignment.error_category
            assert error["error_family"] == assignment.error_family
            assert "clean_expected_state" in error
            assert len(error["trigger_meds"]) >= 1
            assert manifest_row["control_error_status"] == "error_bearing"
        else:
            assert error["control_error_status"] == "clean_control"
            assert error["error_category"] == "none"
            assert error["statement"] == "NO INTENTIONAL ERROR"
            assert error.get("trigger_meds") in (None, [])
            assert manifest_row["control_error_status"] == "clean_control"
            assert manifest_row["error_category"] is None
    assert rxcuis and all(code.isdigit() for code in rxcuis)
    assert loinc_codes and all(re.fullmatch(r"\d{1,5}-\d", code) for code in loinc_codes)
    assert icd_codes and all(not code.startswith("TEST_") for code in icd_codes)
    assert all(not code.startswith("TEST_") for code in rxcuis)


def test_v4_resident_export_hides_the_answer_key_and_source_patient() -> None:
    resident = _load("resident_validation_cases.json")
    blob = json.dumps(resident).casefold()
    assert len(resident["cases"]) == 24
    for marker in (*LEAK_MARKERS, *SOURCE_FACTS):
        assert marker not in blob, marker
    readable = (V4 / "readable" / "all_cases.md").read_text(encoding="utf-8").casefold()
    for marker in ("answer_key", ".docx", "seed_archetype", *SOURCE_FACTS):
        assert marker not in readable, marker
    packet = (V4 / "readable" / "clinician_validation_packet.md").read_text(encoding="utf-8")
    worksheet = (V4 / "readable" / "clinical_validation_worksheet.csv").read_text(encoding="utf-8")
    assert "CLINIPROOF_SEEDCASES_V4" in packet
    assert "VAL-901 through VAL-924" in packet
    for case_id in (f"VAL-{number}" for number in range(901, 925)):
        assert case_id in worksheet
        page = (V4 / "readable" / "cases" / f"{case_id}.md").read_text(encoding="utf-8")
        assert page.startswith(f"# {case_id}")
        assert ".docx" not in page.casefold()


def test_v4_diversity_rejects_duplicate_clean_structures() -> None:
    report = (V4 / "diversity_report.md").read_text(encoding="utf-8")
    assert "exact duplicate fingerprints: 0" in report
    assert "near-duplicate rejections: 0" in report
    matrix = (V4 / "scenario_coverage_matrix.md").read_text(encoding="utf-8")
    for heading in (
        "## MEDREC_UNCERTAIN_HISTORY",
        "## HF_DECOMPENSATION",
        "## OPAT_ENDOCARDITIS",
        "## TRANSPLANT_CMV",
        "## POSTOP_ANTICOAGULATION",
        "## GI_BLEED_ACUTE_CHANGE",
    ):
        assert heading in matrix
    assert "(unresolved)" not in matrix
