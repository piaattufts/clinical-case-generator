"""Generation 2 cohort invariants and Generation 1 isolation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from app.services.discharge_episode import SCENARIO_ORDER, build_episode, variants_for
from app.services.g2_audit import chronology_errors, round1_row
from app.services.g2_cohort import jaccard
from app.services.g2_terminology import ICD10, LOINC
from app.services.synthea_eligibility import evaluate_patient
from app.sources.synthea import parse_bundle
from scripts.build_synthea_g2 import load_config, meta_from_config

ROOT = Path(__file__).resolve().parents[1]
COHORT = ROOT / "data" / "case_sets" / "synthea_g2"
FIXTURE = ROOT / "tests" / "fixtures" / "synthea" / "heart_failure_bundle.json"


def _meta() -> dict[str, str]:
    return meta_from_config(load_config(ROOT / "config" / "synthea.yml"))


def test_fixture_parses_and_is_eligible_for_heart_failure() -> None:
    patient = parse_bundle(json.loads(FIXTURE.read_text(encoding="utf-8")))
    assert patient.synthea_patient_id == "fixture-hf-1"
    assert patient.age_years == 72
    assert patient.sex_display == "Female"
    assert patient.weight_kg == 82.0
    assert patient.latest_lab("2160-0", unit="mg/dL") is not None
    decision = evaluate_patient(patient)["HF_DECOMPENSATION"]
    assert decision.eligible
    assert decision.tier == "known_heart_failure"
    assert "314076" in patient.source_rxcuis()


def test_episode_is_reproducible_and_passes_audit() -> None:
    patient = parse_bundle(json.loads(FIXTURE.read_text(encoding="utf-8")))
    variant = variants_for("HF_DECOMPENSATION")[0]
    meta = _meta()
    first = build_episode(patient, "HF_DECOMPENSATION", variant, meta)
    second = build_episode(patient, "HF_DECOMPENSATION", variant, meta)
    assert first["resident"]["CaseLab"] == second["resident"]["CaseLab"]
    assert first["reference_discharge_plan"] == second["reference_discharge_plan"]
    assert round1_row(first, "X")["overall_pass"]
    broken = json.loads(json.dumps(first))
    broken["facts"] = [fact for fact in broken["facts"] if "baseline" not in fact["domains"]]
    assert not round1_row(broken, "X")["baseline_visible"]


def test_backwards_chronology_is_rejected() -> None:
    patient = parse_bundle(json.loads(FIXTURE.read_text(encoding="utf-8")))
    episode = build_episode(patient, "HF_DECOMPENSATION", variants_for("HF_DECOMPENSATION")[0], _meta())
    for event in episode["timeline"]:
        if event["event_type"] == "diagnosis":
            event["time_order"] = 1
    assert chronology_errors(episode)


def test_scenario_catalog_matches_the_spec() -> None:
    spec = json.loads((ROOT / "data" / "bootstrap" / "discharge_scenarios_g2.json").read_text())
    assert [row["scenario_code"] for row in spec["scenarios"]] == list(SCENARIO_ORDER)


def test_final_cohort_shape() -> None:
    residents = sorted((COHORT / "cases" / "resident").glob("G2-*.json"))
    evaluators = sorted((COHORT / "cases" / "evaluator").glob("G2-*.json"))
    assert len(residents) == 24
    assert [path.name for path in residents] == [path.name for path in evaluators]
    counts: dict[str, int] = {code: 0 for code in SCENARIO_ORDER}
    fingerprints = []
    for path in evaluators:
        episode = json.loads(path.read_text(encoding="utf-8"))
        resident = json.loads((COHORT / "cases" / "resident" / path.name).read_text())
        assert episode["case_id_code"] == resident["case_id_code"]
        assert "reference_discharge_plan" not in resident
        blob = json.dumps(resident).casefold()
        for token in ("reference_discharge_plan", "acceptable_alternatives", "baseline delirium"):
            assert token not in blob
        assert episode["control_error_status"] == "NO INTENTIONAL ERROR"
        assert "intentional_changes" not in episode
        assert episode["clinically_validated"] is False
        assert episode["ready_for_clinician_review"] is True
        row = round1_row(episode, path.stem)
        assert row["overall_pass"], row["notes"]
        counts[str(episode["scenario_code"])] += 1
        fingerprints.append(episode["fingerprint"])
        for action in episode["reference_discharge_plan"]["actions"]:
            assert action["resident_visible_evidence"]
            assert set(action["resident_visible_evidence"]) <= set(episode["visible_fact_ids"])
            for alternative in action["acceptable_alternatives"]:
                assert alternative["rationale"]
                assert alternative["conditions"]
        for fact in episode["facts"]:
            if fact["provenance"] == "cliniproof_episode_generated":
                assert "synthea recorded this inpatient" not in fact["text"].casefold()
        for lab in episode["CaseLab"]:
            assert lab["loinc_code"] in LOINC
            if lab["unit"]:
                assert lab["unit"]
        for diagnosis in episode["CaseDiagnosis"]:
            if diagnosis.get("icd10cm"):
                assert diagnosis["icd10cm"] in ICD10
    assert counts == {code: 4 for code in SCENARIO_ORDER}
    for left, right in zip(fingerprints, fingerprints[1:], strict=False):
        if left["scenario"] == right["scenario"]:
            assert left["variant_id"] != right["variant_id"]
            assert jaccard(left, right) < 0.85


def test_generation1_sources_are_unchanged() -> None:
    diff = subprocess.run(
        [
            "git",
            "diff",
            "--exit-code",
            "--",
            "data/case_sets/seed_guided",
            "docs/validation/CliniProof_Clinical_Validation_Template.docx",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert diff.returncode == 0, diff.stdout
    text = (ROOT / "docs" / "source_integrity.md").read_text(encoding="utf-8")
    checked = 0
    for line in text.splitlines():
        if "CLEAN_BASE" not in line or not line.startswith("|"):
            continue
        path_text, digest = [part.strip().strip("`") for part in line.strip("|").split("|")[:2]]
        payload = (ROOT / path_text).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == digest
        checked += 1
    assert checked == 48
    template = ROOT / "docs" / "validation" / "CliniProof_Clinical_Validation_Template.docx"
    template_line = next(
        line
        for line in text.splitlines()
        if "CliniProof_Clinical_Validation_Template.docx" in line and line.startswith("|")
    )
    expected = [part.strip().strip("`") for part in template_line.strip("|").split("|")][1]
    assert hashlib.sha256(template.read_bytes()).hexdigest() == expected
