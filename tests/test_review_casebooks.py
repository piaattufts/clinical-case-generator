"""The revised and paired casebooks use the Round 1 instrument and the source JSON."""

from __future__ import annotations

import csv
import json
import random
import re
from pathlib import Path

from app.services.review_casebook import (
    BLIND_SEED,
    item_labels,
    template_instrument,
    zip_text,
)
from app.services.word_export import _dict_rows, _lab_rows, _vital_rows
from app.services.word_facts import medication_note, medication_tuple, rows_for_context
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

REPO = Path(__file__).resolve().parents[1]
VALIDATION = REPO / "docs" / "validation"
BOOKS = (
    "CliniProof_Revised_G1_Casebook.docx",
    "CliniProof_Revised_Overlap4_Codebook.docx",
    "CliniProof_Revised_Remaining20_Codebook.docx",
    "CliniProof_Synthea_G2_Clinical_Validation.docx",
    "CliniProof_Paired_Blinded_Casebook.docx",
)
BANNED = (
    "VAL-",
    "G2-",
    "MEDREC_UNCERTAIN_HISTORY",
    "MED_HISTORY_UNCERTAINTY",
    "HF_DECOMPENSATION",
    "OPAT_ENDOCARDITIS",
    "ENDOCARDITIS_OPAT",
    "TRANSPLANT_CMV",
    "POSTOP_ANTICOAGULATION",
    "HIP_FRACTURE_ANTICOAGULATION",
    "GI_BLEED_ACUTE_CHANGE",
    "GI_BLEED_ANTICOAGULATION",
    "Synthea",
    "Generation",
    "seed",
)


def _cycles(path: Path) -> list[list[str]]:
    from app.services.review_casebook import instrument_markers

    markers = instrument_markers(Document(str(path)))
    starts = [
        index
        for index, marker in enumerate(markers)
        if marker == "C1 — Clinical plausibility"
    ]
    cycles = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(markers)
        cycles.append(markers[start:end])
    return cycles


def test_every_casebook_matches_the_template_instrument() -> None:
    gold = template_instrument()
    assert gold
    for name in BOOKS:
        cycles = _cycles(VALIDATION / name)
        assert cycles, name
        for cycle in cycles:
            assert cycle == gold, name


def _sections(path: Path) -> dict[str, list[tuple[str, object]]]:
    document = Document(str(path))
    current = ""
    sections: dict[str, list[tuple[str, object]]] = {}
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            text = Paragraph(child, document).text.strip()
            if text.startswith("CASE "):
                current = text.removeprefix("CASE ").strip()
                sections[current] = []
            elif current:
                sections[current].append(("p", text))
        elif child.tag == qn("w:tbl") and current:
            table = Table(child, document)
            rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            sections[current].append(("t", rows))
    return sections


def _table_after(blocks: list[tuple[str, object]], heading: str) -> list[list[str]] | None:
    for index, (kind, value) in enumerate(blocks):
        if kind == "p" and value == heading:
            for later_kind, later in blocks[index + 1 :]:
                if later_kind == "p" and later in {
                    "Vital signs",
                    "Laboratory findings",
                    "Weight",
                    "Home medications",
                    "Medications during hospitalization",
                    "Discharge medications",
                    "Medication reconciliation",
                    "Clinical validation",
                    "C1 — Clinical plausibility",
                }:
                    return None
                if later_kind == "t":
                    rows = later
                    assert isinstance(rows, list)
                    return rows
            return None
    return None


def _check_case(
    case_id: str,
    resident: dict[str, object],
    blocks: list[tuple[str, object]],
) -> None:
    chart: list[tuple[str, object]] = []
    for kind, value in blocks:
        if kind == "p" and value == "Clinical validation":
            break
        chart.append((kind, value))
    contexts = {
        "Home medications": "home",
        "Medications during hospitalization": "inpatient",
        "Discharge medications": "discharge",
    }
    for heading, context in contexts.items():
        expected = []
        for row in rows_for_context(resident, context):
            if not isinstance(row, dict):
                continue
            drug, dose, route, frequency = medication_tuple(row)
            expected.append([drug, dose, route, frequency, medication_note(row)])
        rendered = _table_after(chart, heading)
        if not expected:
            assert rendered is None, case_id
            continue
        assert rendered is not None, f"{case_id} missing {heading}"
        assert rendered[0][0] == "Medication"
        assert rendered[1:] == expected, case_id
    vital_tables: list[list[list[str]]] = []
    lab_tables: list[list[list[str]]] = []
    for index, (kind, value) in enumerate(chart):
        if kind != "p":
            continue
        if value == "Vital signs":
            table = _table_after(chart[index:], "Vital signs")
            if table:
                vital_tables.append(table[1:])
        if value == "Laboratory findings":
            table = _table_after(chart[index:], "Laboratory findings")
            if table:
                lab_tables.append(table[1:])
    expected_vitals: list[tuple[str, str, str]] = []
    expected_labs: list[tuple[str, str, str]] = []
    for timepoint in ("admission", "discharge"):
        vital_rows = [
            row
            for row in _dict_rows(resident, "CaseVital")
            if str(row.get("timepoint")) == timepoint
        ]
        lab_rows = [
            row
            for row in _dict_rows(resident, "CaseLab")
            if str(row.get("timepoint")) == timepoint
        ]
        expected_vitals.extend(tuple(row) for row in _vital_rows(vital_rows))
        expected_labs.extend(tuple(row) for row in _lab_rows(lab_rows))
    rendered_vitals = [tuple(row) for table in vital_tables for row in table]
    rendered_labs = [tuple(row) for table in lab_tables for row in table]
    assert rendered_vitals == expected_vitals, case_id
    assert rendered_labs == expected_labs, case_id


def test_rendered_facts_match_the_json_for_three_cases_per_cohort() -> None:
    rng = random.Random(BLIND_SEED)
    g1_ids = rng.sample([f"VAL-{index}" for index in range(801, 825)], 3)
    g2_ids = rng.sample([f"G2-{index:03d}" for index in range(1, 25)], 3)
    g1_sections = _sections(VALIDATION / "CliniProof_Revised_G1_Casebook.docx")
    g2_sections = _sections(VALIDATION / "CliniProof_Synthea_G2_Clinical_Validation.docx")
    for case_id in g1_ids:
        overlap = {"VAL-801", "VAL-805", "VAL-809", "VAL-813"}
        folder = "overlap_4" if case_id in overlap else "remaining_20"
        path = (
            REPO
            / "data"
            / "case_sets"
            / "seed_guided"
            / "REVISED"
            / folder
            / f"{case_id}_resident.json"
        )
        resident = json.loads(path.read_text(encoding="utf-8"))
        _check_case(case_id, resident, g1_sections[case_id])
    for case_id in g2_ids:
        path = REPO / "data" / "case_sets" / "synthea_g2" / "cases" / "resident" / f"{case_id}.json"
        resident = json.loads(path.read_text(encoding="utf-8"))
        _check_case(case_id, resident, g2_sections[case_id])


def test_blinded_casebook_has_no_generation_identifiers() -> None:
    payload = zip_text(VALIDATION / "CliniProof_Paired_Blinded_Casebook.docx")
    for token in BANNED:
        assert token not in payload, token
    assert not re.search(r"VAL-\d", payload)
    assert "Matched counterpart" not in payload


def test_response_templates_use_the_item_rating_labels_and_stay_blank() -> None:
    labels = item_labels()
    expected_counts = {
        "CliniProof_Revised_G1_Casebook_response_template.csv": 24,
        "CliniProof_Revised_Overlap4_Codebook_response_template.csv": 4,
        "CliniProof_Revised_Remaining20_Codebook_response_template.csv": 20,
        "CliniProof_Synthea_G2_Clinical_Validation_response_template.csv": 24,
        "CliniProof_Paired_Blinded_Casebook_response_template.csv": 48,
    }
    for name, cases in expected_counts.items():
        with (VALIDATION / name).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == cases * 14
        assert [row["item"] for row in rows[:14]] == labels
        for row in rows:
            assert row["reviewer_1_rating"] == ""
            assert row["reviewer_2_rating"] == ""
            assert row["reviewer_1_comment"] == ""
            assert row["agree"] == ""
            assert row["abs_diff_c1"] == ""


def test_case_links_are_one_to_one_and_paged() -> None:
    with (VALIDATION / "case_links.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["val_id"] for row in rows] == [f"VAL-{index}" for index in range(801, 825)]
    assert [row["g2_id"] for row in rows] == [f"G2-{index:03d}" for index in range(1, 25)]
    assert len({row["pair_id"] for row in rows}) == 24
    assert len({row["blinded_id_g1"] for row in rows}) == 24
    assert len({row["blinded_id_g2"] for row in rows}) == 24
    for row in rows:
        assert int(row["g1_casebook_page"]) > 0
        assert int(row["g2_casebook_page"]) > 0
        assert row["family"]
        assert row["g1_revision_source"] in {
            "dual-review",
            "Reviewer 1 + framework",
            "framework only",
        }
    key_path = REPO / "data" / "blinding" / "unblinding_key.json"
    key = json.loads(key_path.read_text(encoding="utf-8"))
    assert key["investigator_only"] is True
    assert key["order_seed"] == BLIND_SEED
    assert len(key["pairs"]) == 24
