# ruff: noqa: E501
"""Canonical Set 1 version 3 stays inside the six reviewed cases."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.services.cycle2_v3_cases import (
    CASE_IDS,
    LEDGER,
    REVIEW_ITEMS,
    SPECIAL_QUESTIONS,
    leak_hits,
    old_design_hits,
    readme_mismatches,
    write_revision_package,
)
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "exports" / "ko_cycle2_revised_validation_v3"
UNTOUCHED = (
    ROOT / "data" / "case_sets" / "seed_guided" / "resident_validation_cases.json",
    ROOT / "data" / "case_sets" / "balanced" / "resident_validation_cases.json",
    ROOT / "exports" / "clean_balanced_seed_set" / "VAL-801_resident.json",
    ROOT / "exports" / "clean_balanced_seed_set" / "VAL-805_resident.json",
    ROOT / "exports" / "ko_revised_cases_v1" / "VAL-801_resident.json",
    ROOT / "exports" / "ko_revised_cases_v1" / "VAL-805_resident.json",
    ROOT / "exports" / "ko_cycle2_revised_validation_v2" / "VAL-801_resident.json",
    ROOT / "exports" / "ko_cycle2_revised_validation_v2" / "VAL-813_resident.json",
    ROOT / "exports" / "ko_clean_cases_for_review_v1" / "VAL-804_resident.json",
    ROOT / "exports" / "ko_clean_cases_for_review_v1" / "VAL-814_resident.json",
    ROOT / "exports" / "ko_clean_cases_for_review_v1" / "VAL-824_evaluator.json",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(directory: Path, case_id: str, kind: str) -> dict:
    return json.loads((directory / f"{case_id}_{kind}.json").read_text(encoding="utf-8"))


def test_v3_package_gates_and_leaves_other_cases_unchanged(tmp_path: Path) -> None:
    before = {path: _sha(path) for path in UNTOUCHED}
    document = write_revision_package(tmp_path)
    assert {path: _sha(path) for path in UNTOUCHED} == before
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    residents = {case_id: _load(tmp_path, case_id, "resident") for case_id in CASE_IDS}
    assert readme_mismatches(readme, residents) == []
    assert "exports/ko_cycle2_revised_validation_v3/CliniProof_Cycle2_Revised_Cases_Validation.docx" in readme
    assert "exports/ko_cycle2_revised_validation_v2/CliniProof_Cycle2_Revised_Cases_Validation.docx" not in readme
    log = (tmp_path / "CLINICAL_REVISION_LOG.md").read_text(encoding="utf-8")
    assert "Author response" not in log
    assert "author response" not in log.lower()
    for name in (
        "ROUND1_FEEDBACK_COMPLETE.md",
        "ROUND1_FEEDBACK_EXTRACTION_AUDIT.md",
        "CLINICAL_REVISION_LOG.md",
        "REVISION_DIFF.md",
        "REVISION_EVIDENCE_LEDGER.md",
        "SET1_VERSION_RECONCILIATION.md",
        "ANSWER_LEAK_AUDIT.md",
        "REFERENCE_EVIDENCE_AUDIT.md",
        "KATIE_REAUDIT.md",
        "MANIFEST.md",
        "README.md",
    ):
        assert (tmp_path / name).is_file()
    assert "DIRECT_ANSWER_LEAK count: 0" in (tmp_path / "ANSWER_LEAK_AUDIT.md").read_text(encoding="utf-8")
    assert "HIDDEN_REFERENCE_DEPENDENCY count: 0" in (
        tmp_path / "REFERENCE_EVIDENCE_AUDIT.md"
    ).read_text(encoding="utf-8")
    assert "CLINICALLY_INCONSISTENT count: 0" in (
        tmp_path / "REFERENCE_EVIDENCE_AUDIT.md"
    ).read_text(encoding="utf-8")
    feedback = (tmp_path / "ROUND1_FEEDBACK_COMPLETE.md").read_text(encoding="utf-8")
    assert "NOT_COMPLETED_IN_ROUND_1" in feedback
    assert "VAL-803" in feedback
    sodium = [row for row in LEDGER if row["case"] == "VAL-803" and "Sodium" in row["change"]]
    assert sodium
    assert sodium[0]["classification"] == "SYNTHETIC_ADDITION_SUPPORTED_BY_LITERATURE"
    for item in REVIEW_ITEMS:
        assert item["comment"] and item["revision"] and item["reasoning"]
        if item["status"] == "REVISED":
            assert "[E" in item["evidence"]
    for case_id in CASE_IDS:
        resident = residents[case_id]
        evaluator = _load(tmp_path, case_id, "evaluator")
        assert "reference_discharge_plan" not in resident
        assert leak_hits(resident) == []
        assert old_design_hits(resident) == []
        assert evaluator["clinician_review_status"] == "PREPARED_FOR_RE_REVIEW"
        assert "clinician_review_status" not in resident
    resident_801 = residents["VAL-801"]
    assert any(vital.get("timepoint") == "admission_standing" for vital in resident_801["CaseVital"])
    assert any(vital.get("bp_systolic") == 136 for vital in resident_801["CaseVital"])
    resident_803 = residents["VAL-803"]
    sodium_values = [
        lab.get("value")
        for lab in resident_803["CaseLab"]
        if "Sodium" in str(lab.get("test_name"))
    ]
    assert sodium_values == [128, 135]
    assert "are continued" not in json.dumps(resident_803)
    resident_805 = residents["VAL-805"]
    furosemide = [
        medication
        for medication in resident_805["CaseMedication"]
        if "furosemide" in medication["drug"]
    ]
    assert {medication["route"] for medication in furosemide} == {"oral"}
    assert "30 percent" not in json.dumps(resident_805)
    assert "78.000" in json.dumps(resident_805["CaseWeight"])
    resident_809 = residents["VAL-809"]
    recorded = [vital["temp_c"] for vital in resident_809["CaseVital"]]
    assert recorded == ["36.80", "36.80"]
    assert "38.4" not in json.dumps(resident_809)
    assert "fever" not in resident_809["ClinicalCase"]["presentation"]["hpi"].lower()
    assert "viridans" not in json.dumps(resident_809).lower()
    assert "dental extraction" not in json.dumps(resident_809).lower()
    assert "prosthetic valve is recorded" in json.dumps(resident_809).lower() or "No prosthetic valve" in json.dumps(resident_809)
    resident_813 = residents["VAL-813"]
    assert "mycophenolate" not in json.dumps(resident_813).lower()
    assert not any(
        medication.get("context") == "home" and "valganciclovir" in medication["drug"]
        for medication in resident_813["CaseMedication"]
    )
    text = "\n".join(paragraph.text for paragraph in Document(str(document)).paragraphs)
    for table in Document(str(document)).tables:
        for row in table.rows:
            text += "\n" + " ".join(cell.text for cell in row.cells)
    assert text.count("CASE VAL-") == 6
    for case_id in CASE_IDS:
        section = text.split(f"CASE {case_id}", 1)[1]
        if case_id != "VAL-813":
            section = section.split("CASE VAL-", 1)[0]
        assert section.index("RESIDENT-FACING CHART") < section.index("C1 — Clinical plausibility")
        assert section.index("C1 — Clinical plausibility") < section.index("C2 — Sufficiency")
        assert section.index("C2 — Sufficiency") < section.index("CLINICIAN VALIDATION REFERENCE")
        assert section.index("CLINICIAN VALIDATION REFERENCE") < section.index(
            "ROUND 1 CLINICIAN FEEDBACK"
        )
        assert section.index("ROUND 1 CLINICIAN FEEDBACK") < section.index("CLINICAL REVISION RECORD")
        question = SPECIAL_QUESTIONS[case_id]
        assert question in section
        adjudication = section.split("Case-specific adjudication", 1)[1].split("C3 —", 1)[0]
        assert "30 percent" not in adjudication
        assert "mycophenolate" not in adjudication.lower()
    assert "NOT COMPLETED IN ROUND 1" in text
    assert "Author response" not in text
    eight = [f"VAL-{number}" for number in range(801, 825) if f"VAL-{number}" not in CASE_IDS]
    for case_id in eight:
        assert f"CASE {case_id}" not in text


def test_committed_v3_package_matches_the_generator(tmp_path: Path) -> None:
    write_revision_package(tmp_path)
    for case_id in CASE_IDS:
        for kind in ("resident", "evaluator"):
            committed = (PACKAGE / f"{case_id}_{kind}.json").read_text(encoding="utf-8")
            generated = (tmp_path / f"{case_id}_{kind}.json").read_text(encoding="utf-8")
            assert committed == generated
    assert (PACKAGE / "SUPERSEDED.md").exists() is False
    assert (ROOT / "exports" / "ko_revised_cases_v1" / "SUPERSEDED.md").is_file()
    assert (ROOT / "exports" / "ko_cycle2_revised_validation_v2" / "SUPERSEDED.md").is_file()
    assert (PACKAGE / "CliniProof_Cycle2_Revised_Cases_Validation.docx").is_file()
