"""Resident-seed-guided batch isolation, provenance, and uniqueness tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from app.models.cases import ClinicalCase
from app.services.case_diversity import (
    fingerprint_from_mapping,
    require_unique_clean_cases,
    similarity,
)
from app.services.generation import generate_one_case, load_scenarios
from app.services.seed_archetypes import (
    GENERATION_STRATEGY_SEED,
    GENERATION_STRATEGY_TEMPLATE,
    SEED_SOURCE_DIR,
    load_seed_archetypes,
)
from app.services.validation_batch import (
    freeze_validation_batch,
    load_batch_plan,
    parse_assignments,
)
from app.utils.jsonio import dumps_json
from sqlalchemy.orm import Session

from tests.test_case_diversity import EXPECTED_V1_HASHES, _fp
from tests.test_generation_pipeline import _seed_generation_refs, _test_scenario

REPO = Path(__file__).resolve().parents[1]
SEED_PLAN = REPO / "data" / "validation_seedcases" / "batch_plan.json"
SEED_DIR = REPO / "data" / "validation_seedcases"
V1_DIR = REPO / "data" / "validation"
V2_DIR = REPO / "data" / "validation_balanced"
EXPECTED_V2_HASHES = {
    "batch_plan.json": "7be72c20186284321e86e5a6246544d16094b51ccb688ab7c7fa9f754c8b19a7",
    "resident_validation_cases.json": (
        "f60e24cf942ac8a91bb178eda5a452ac536ee19837399ee661a7b6fbe7238dbf"
    ),
    "investigator_answer_key.json": (
        "c9e1684edd102c4e2964d052f17cad74984d6af7e35903e47eefafcebda93505"
    ),
    "investigator_answer_key.md": (
        "e0540c7afbe9885f8c365beb1e784ed09358dceb004452457066497462b1bc7b"
    ),
    "validation_manifest.json": (
        "1e43a4d2c0925d550775678d9d3f0c282db5dbd67385493b03d1cf93f862ea8e"
    ),
    "coverage_report.md": "7985d999cd571f05d96ac9a00fada978e1497a1262f8a19fc88c5fd24ea07d33",
    "scenario_coverage_matrix.md": (
        "3ad1ab7435b56e0659202d57f05e2d029044247ac4384b805a40d67998923d13"
    ),
    "resident_review_worksheet.csv": (
        "c5428f174ead12833e9e036abe243d51873d0a6541a89fed441a317abf9a9eaa"
    ),
    "resident_review_schema.json": (
        "118edb2a716988aa2891c30c512af931d54957a49e6f77989542299bd40fc6c7"
    ),
    "diversity_report.md": "529cbe9e8f46f2e7615b332fb9accf7a46b89617cd2be9fad41231a4ee3db120",
}
EXPECTED_SEED_HASHES = {
    "batch_plan.json": "dfbbafa6389b80ac6384cab8042fe4c22819f90076ba9fc5be5a7073f439af6b",
    "resident_validation_cases.json": (
        "36a51ae538842dcb1884968349ce1117fa411e6ef70c181c44c98d1b71ac894d"
    ),
    "investigator_answer_key.json": (
        "606e290f9f300b9feb573f1ce16eb051896334a2d42612819cb0db9a16783406"
    ),
    "investigator_answer_key.md": (
        "e740e02106288332f078091e2c30760990cf065bb4cc4d774a011f3f5789a751"
    ),
    "validation_manifest.json": (
        "e5aad6afd923f99349118e4ef7359989edfbbe5d026f440dd2066335b5edc668"
    ),
    "coverage_report.md": "40b98d8dab164d5ffb851aab2899f7c8e90b0a31da7fd8636c723fd9d1e11927",
    "scenario_coverage_matrix.md": (
        "a4db5d86b1c605e5f02af86221b6dd5afbd4ed21823308206462136a9b7f0c23"
    ),
    "resident_review_worksheet.csv": (
        "a15ae7bdad9419186421a7be24ea575df19d3d3771830d89c665b13d8895dbfb"
    ),
    "resident_review_schema.json": (
        "118edb2a716988aa2891c30c512af931d54957a49e6f77989542299bd40fc6c7"
    ),
    "diversity_report.md": "5519d1824476488e5dae1f5d8f84951e90e2da0f991629a2f7dbf7a50309c6b8",
    "randomized_vs_seedcase_comparison.md": (
        "c7313a4a267f81b664668eb8586ef4a42db25e32a07a07b8f07ad944ee37c166"
    ),
}
SEED_DOCUMENTS = (
    "Bad_Med_Rec_Case.docx",
    "Heart_Failure_Case.docx",
    "OPAT_Case.docx",
    "Post_transplant_case.docx",
    "Post-Op_Case.docx",
    "Sepsis_AMA_Case.docx",
)


def _assert_hashes(root: Path, expected: dict[str, str]) -> None:
    for name, digest in expected.items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        assert actual == digest, name


def test_taxonomy_v1_frozen_files_remain_unchanged() -> None:
    _assert_hashes(V1_DIR, EXPECTED_V1_HASHES)


def test_balanced_v2_frozen_files_remain_unchanged() -> None:
    _assert_hashes(V2_DIR, EXPECTED_V2_HASHES)


def test_seed_batch_frozen_files_match_expected_hashes() -> None:
    _assert_hashes(SEED_DIR, EXPECTED_SEED_HASHES)


def test_seed_source_documents_are_present_and_docx() -> None:
    for name in SEED_DOCUMENTS:
        path = SEED_SOURCE_DIR / name
        assert path.is_file(), name
        assert path.read_bytes()[:2] == b"PK"


def test_seed_plan_uses_resident_seed_guided_strategy() -> None:
    plan = load_batch_plan(SEED_PLAN)
    assignments = parse_assignments(plan)
    assert plan["batch_code"] == "CLINIPROOF_SEEDCASES_V1"
    assert plan["generation_strategy"] == GENERATION_STRATEGY_SEED
    assert len(assignments) == 24
    assert {item.generation_strategy for item in assignments} == {GENERATION_STRATEGY_SEED}
    assert all(item.clinical_profile for item in assignments)
    assert all(item.scenario for item in assignments)
    assert len({item.clinical_profile for item in assignments}) == 24
    assert all(item.validation_case_id.startswith("VAL-4") for item in assignments)
    families = {item.scenario: 0 for item in assignments}
    for item in assignments:
        families[item.scenario] += 1
    assert families == {
        "MEDREC_UNCERTAIN_HISTORY": 4,
        "HF_DECOMPENSATION": 4,
        "OPAT_ENDOCARDITIS": 4,
        "TRANSPLANT_CMV": 4,
        "POSTOP_ANTICOAGULATION": 4,
        "GI_BLEED_ACUTE_CHANGE": 4,
    }
    assert sum(1 for item in assignments if not item.inject_error) == 4


def test_randomized_plans_are_not_relabeled_seed_guided() -> None:
    v1 = parse_assignments(load_batch_plan(V1_DIR / "batch_plan.json"))
    v2 = parse_assignments(load_batch_plan(V2_DIR / "batch_plan.json"))
    assert {item.generation_strategy for item in v1} == {GENERATION_STRATEGY_TEMPLATE}
    assert {item.generation_strategy for item in v2} == {GENERATION_STRATEGY_TEMPLATE}
    template_codes = {item.code for item in load_scenarios()}
    assert "MEDREC_UNCERTAIN_HISTORY" not in template_codes
    assert "HF_INPATIENT" in template_codes


def test_seed_archetypes_have_four_distinct_profiles_each() -> None:
    archetypes = load_seed_archetypes()
    assert {item.generation_strategy for item in archetypes} == {GENERATION_STRATEGY_SEED}
    assert len(archetypes) == 6
    for archetype in archetypes:
        assert archetype.seed_source_filename
        assert (SEED_SOURCE_DIR / archetype.seed_source_filename).is_file()
        codes = [profile.code for profile in archetype.profiles]
        assert len(codes) == 4, archetype.code
        assert len(set(codes)) == 4
        fingerprints = []
        for profile in archetype.profiles:
            fingerprints.append(
                fingerprint_from_mapping(
                    {
                        "scenario": archetype.code,
                        "clinical_profile": profile.code,
                        "specialty": archetype.specialty,
                        "diagnosis_codes": archetype.diagnosis_queries,
                        "symptoms": profile.symptom_queries,
                        "home_medications": profile.medication_required_queries,
                        "inpatient_medications": profile.medication_required_queries,
                        "lab_concepts": profile.lab_queries,
                        "hospital_course_pattern": (
                            f"{profile.hospital_course_pattern}|"
                            f"{profile.symptom_duration}|{profile.symptom_course}"
                        ),
                        "followup": [
                            f"{profile.followup_service}|{profile.followup_item}|"
                            f"{profile.followup_timing}"
                        ],
                        "disposition": (
                            f"{profile.disposition}|"
                            f"{'home_health' if profile.home_health_ordered else 'no_home_health'}"
                        ),
                    }
                )
            )
        labeled = [
            (profile.code, fingerprint)
            for profile, fingerprint in zip(archetype.profiles, fingerprints, strict=True)
        ]
        require_unique_clean_cases(labeled)


def test_seed_archetype_id_alone_does_not_make_identical_cases_unique() -> None:
    left = _fp(scenario="MEDREC_UNCERTAIN_HISTORY", clinical_profile="SHARED")
    right = _fp(scenario="HF_DECOMPENSATION", clinical_profile="SHARED")
    score = similarity(left, right)
    assert score >= 0.85


def test_seed_case_seed_is_reproducible() -> None:
    plan = load_batch_plan(SEED_PLAN)
    first = parse_assignments(plan)
    second = parse_assignments(json.loads(SEED_PLAN.read_text(encoding="utf-8")))
    assert [item.clinical_profile for item in first] == [item.clinical_profile for item in second]
    from app.services.validation_batch import assignment_case_seed

    master = int(plan["master_seed"])
    seeds = [assignment_case_seed(master, item) for item in first]
    assert seeds == [assignment_case_seed(master, item) for item in second]
    assert len(set(seeds)) == 24
    paired = zip(first, seeds, strict=True)
    assert all(item.clinical_profile and item.clinical_profile in seed for item, seed in paired)


def test_fingerprint_computed_before_error_injection(
    db_session: Session,
) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.generation_strategy = GENERATION_STRATEGY_SEED
    scenario.anticoagulant_mutex_queries = []
    scenario.seed_source_filename = "Bad_Med_Rec_Case.docx"
    scenario.seed_source_type = "resident_authored"
    clean = generate_one_case(
        db_session,
        sequence=71,
        seed=9,
        scenario=scenario,
        inject_error=False,
        use_openai=False,
    )
    injected = generate_one_case(
        db_session,
        sequence=72,
        seed=9,
        scenario=scenario,
        inject_error=True,
        use_openai=False,
        error_category="f1_omission",
    )
    assert clean.fingerprint is not None
    assert injected.fingerprint is not None
    assert clean.fingerprint.digest() == injected.fingerprint.digest()
    diversity = injected.clean_state["diversity"]
    assert diversity["generation_strategy"] == GENERATION_STRATEGY_SEED
    assert diversity["seed_source_filename"] == "Bad_Med_Rec_Case.docx"


def test_resident_payload_does_not_leak_seed_metadata(
    db_session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.generation_strategy = GENERATION_STRATEGY_SEED
    scenario.seed_source_filename = "Heart_Failure_Case.docx"
    scenario.seed_archetype_name = "Acute heart-failure decompensation"
    scenario.seed_source_type = "resident_authored"
    scenario.blueprint_version = "seed-archetypes-v1"
    monkeypatch.setattr("app.services.validation_batch.load_seed_archetypes", lambda: [scenario])
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps(
            {
                "batch_code": "TEST_SEED",
                "generation_strategy": GENERATION_STRATEGY_SEED,
                "master_seed": 13,
                "cases": [
                    {
                        "validation_case_id": "VAL-501",
                        "scenario": scenario.code,
                        "clinical_profile": None,
                        "inject_error": False,
                        "error_family": "none",
                        "error_category": None,
                        "sequence": 1301,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    freeze_validation_batch(db_session, plan_path=plan, allow_test_identifiers=True)
    from app.repositories.cases import get_frozen_case_by_validation_id
    from app.services.validation_batch import _resident_payload

    frozen = get_frozen_case_by_validation_id(db_session, "VAL-501")
    assert frozen is not None
    case = db_session.get(ClinicalCase, frozen.case_id)
    assert case is not None
    resident = _resident_payload(db_session, case, frozen)
    blob = dumps_json(resident).casefold()
    for marker in (
        "generation_strategy",
        "resident_seed_guided",
        "seed_archetype",
        "resident_authored",
        ".docx",
        "heart_failure_case",
        "blueprint_version",
        "answer_key",
    ):
        assert marker not in blob
    diversity = (frozen.clean_state or {}).get("diversity") or {}
    assert diversity.get("generation_strategy") == GENERATION_STRATEGY_SEED
    assert diversity.get("seed_source_filename") == "Heart_Failure_Case.docx"


def test_exported_seed_resident_json_does_not_leak_source_metadata() -> None:
    path = REPO / "data" / "validation_seedcases" / "resident_validation_cases.json"
    investigator = REPO / "data" / "validation_seedcases" / "investigator_answer_key.json"
    resident = json.loads(path.read_text(encoding="utf-8"))
    blob = json.dumps(resident).casefold()
    for marker in (
        "generation_strategy",
        "resident_seed_guided",
        "seed_archetype",
        "resident_authored",
        ".docx",
        "bad_med_rec_case",
        "blueprint_version",
        "answer_key",
    ):
        assert marker not in blob, marker
    key = json.loads(investigator.read_text(encoding="utf-8"))
    assert key["batch_code"] == "CLINIPROOF_SEEDCASES_V1"
    assert {item["generation_strategy"] for item in key["cases"]} == {GENERATION_STRATEGY_SEED}
    assert all(item.get("seed_archetype_id") for item in key["cases"])
    assert all(item.get("clinical_profile") for item in key["cases"])


def test_seed_val_ids_do_not_overlap_prior_batches() -> None:
    v1 = {
        item.validation_case_id
        for item in parse_assignments(load_batch_plan(V1_DIR / "batch_plan.json"))
    }
    v2 = {
        item.validation_case_id
        for item in parse_assignments(load_batch_plan(V2_DIR / "batch_plan.json"))
    }
    seed = {item.validation_case_id for item in parse_assignments(load_batch_plan(SEED_PLAN))}
    assert v1 == {f"VAL-{n}" for n in range(201, 225)}
    assert v2 == {f"VAL-{n}" for n in range(301, 325)}
    assert seed == {f"VAL-{n}" for n in range(401, 425)}
    assert seed.isdisjoint(v1)
    assert seed.isdisjoint(v2)
    assert v1.isdisjoint(v2)


def test_age_sex_numbers_and_error_do_not_uniquify_seed_profiles() -> None:
    clinical = {
        "scenario": "MEDREC_UNCERTAIN_HISTORY",
        "clinical_profile": "MEDREC_COLLATERAL_VERIFIED",
        "specialty": "general medicine",
        "diagnosis_codes": ["Delirium"],
        "symptoms": ["confusion", "fatigue"],
        "home_medications": ["RXCUI:lisinopril", "RXCUI:metformin"],
        "inpatient_medications": ["RXCUI:lisinopril", "RXCUI:metformin"],
        "lab_concepts": ["LOINC:CR"],
        "monitoring": [],
        "hospital_course_pattern": "collateral_medrec_complete|several days|improving",
        "followup": ["primary care|Primary care follow-up|7 days"],
        "disposition": "home|home_health",
    }
    left = fingerprint_from_mapping(
        {
            **clinical,
            "age": 72,
            "sex": "Male",
            "seed": "20260924:1101:MEDREC_UNCERTAIN_HISTORY:MEDREC_COLLATERAL_VERIFIED",
            "error_category": "none",
            "lab_values": [1.2],
            "vitals": {"hr": 88},
            "seed_source_filename": "Bad_Med_Rec_Case.docx",
        }
    )
    right = fingerprint_from_mapping(
        {
            **clinical,
            "age": 84,
            "sex": "Female",
            "seed": "999:9999:MEDREC_UNCERTAIN_HISTORY:MEDREC_COLLATERAL_VERIFIED",
            "error_category": "f1_omission",
            "lab_values": [0.8],
            "vitals": {"hr": 61},
            "seed_source_filename": "Heart_Failure_Case.docx",
        }
    )
    assert left.digest() == right.digest()
    assert similarity(left, right) == 1.0


def test_seed_guided_generation_is_reproducible(
    db_session: Session,
) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.generation_strategy = GENERATION_STRATEGY_SEED
    scenario.seed_source_filename = "Bad_Med_Rec_Case.docx"
    first = generate_one_case(
        db_session, sequence=81, seed=17, scenario=scenario, inject_error=False, use_openai=False
    )
    second = generate_one_case(
        db_session, sequence=81, seed=17, scenario=scenario, inject_error=False, use_openai=False
    )
    assert first.fingerprint is not None
    assert second.fingerprint is not None
    assert first.fingerprint.digest() == second.fingerprint.digest()
    assert first.seed == second.seed


def test_seed_coverage_matrix_uses_archetypes_not_templates() -> None:
    matrix = (SEED_DIR / "scenario_coverage_matrix.md").read_text(encoding="utf-8")
    v1 = (V1_DIR / "scenario_coverage_matrix.md").read_text(encoding="utf-8")
    for heading in (
        "## MEDREC_UNCERTAIN_HISTORY",
        "## HF_DECOMPENSATION",
        "## OPAT_ENDOCARDITIS",
        "## TRANSPLANT_CMV",
        "## POSTOP_ANTICOAGULATION",
        "## GI_BLEED_ACUTE_CHANGE",
    ):
        assert heading in matrix
    assert "## HF_INPATIENT" not in matrix
    assert "resident_seed_guided" in matrix
    assert "(unresolved)" not in matrix
    assert "## HF_INPATIENT" in v1
    assert "resident_seed_guided" not in v1


def test_seed_one_stage_clinician_materials_are_separate() -> None:
    readable = SEED_DIR / "readable"
    packet = (readable / "clinician_validation_packet.md").read_text(encoding="utf-8")
    all_cases = (readable / "all_cases.md").read_text(encoding="utf-8")
    worksheet = (readable / "clinical_validation_worksheet.csv").read_text(encoding="utf-8")
    assert "CLINIPROOF_SEEDCASES_V1" in packet
    assert "VAL-401 through VAL-424" in packet
    assert "single review stage" in packet
    assert packet.count("### C1 Clinical plausibility") == 24
    assert packet.count("### C2 Intended assessment problem") == 24
    assert packet.count("### C3 Detectability") == 24
    assert packet.count("### C4 Absence of unintended problems") == 24
    assert packet.count("### C5 Expected learner difficulty") == 24
    assert "CLINIPROOF_TAXONOMY_V1" not in packet
    assert "VAL-201" not in packet
    assert "VAL-301" not in packet
    blinded = all_cases.casefold()
    for marker in (".docx", "seed_archetype", "answer_key", "bad_med_rec_case"):
        assert marker not in blinded
    for case_id in (f"VAL-{n}" for n in range(401, 425)):
        assert f"# {case_id}" in all_cases
        page = (readable / "cases" / f"{case_id}.md").read_text(encoding="utf-8")
        assert page.startswith(f"# {case_id}")
        assert ".docx" not in page.casefold()
        assert case_id in worksheet


def test_exported_seed_cases_have_distinct_clean_profiles() -> None:
    investigator = json.loads(
        (SEED_DIR / "investigator_answer_key.json").read_text(encoding="utf-8")
    )
    profiles = [item["clinical_profile"] for item in investigator["cases"]]
    archetypes = [item["seed_archetype_id"] for item in investigator["cases"]]
    assert len(profiles) == 24
    assert len(set(profiles)) == 24
    counts: dict[str, int] = {}
    for archetype in archetypes:
        counts[archetype] = counts.get(archetype, 0) + 1
    assert counts == {
        "MEDREC_UNCERTAIN_HISTORY": 4,
        "HF_DECOMPENSATION": 4,
        "OPAT_ENDOCARDITIS": 4,
        "TRANSPLANT_CMV": 4,
        "POSTOP_ANTICOAGULATION": 4,
        "GI_BLEED_ACUTE_CHANGE": 4,
    }
    diversity = (SEED_DIR / "diversity_report.md").read_text(encoding="utf-8")
    assert "exact duplicate fingerprints: 0" in diversity
    assert "near-duplicate rejections: 0" in diversity
    assert "near-duplicate warnings: 7" in diversity
    assert "similarity score: 0.79" in diversity

