"""Validation casebooks pair each chart with its canonical answer-key reference."""

from __future__ import annotations

import hashlib
from pathlib import Path

from app.services.validation_casebook import (
    export_casebooks,
    load_active_batches,
    load_prepared_cases,
    stats_for,
)
from app.services.word_facts import medication_tuple, rows_for_context
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "docs" / "resident_review_package" / "files"


def _blocks(path: Path) -> list[tuple[str, str, object]]:
    document = Document(str(path))
    found: list[tuple[str, str, object]] = []
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            paragraph = Paragraph(child, document)
            style = paragraph.style.name if paragraph.style is not None else ""
            found.append(("p", style, paragraph.text.strip()))
        elif child.tag == qn("w:tbl"):
            table = Table(child, document)
            rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            found.append(("t", "", rows))
    return found


def _chunks(blocks: list[tuple[str, str, object]]) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    current = ""
    buffer: list[str] = []
    for kind, style, payload in blocks:
        text = str(payload)
        if kind == "p" and style == "Heading 1" and text.startswith("CASE VAL-"):
            if current:
                chunks.append((current, "\n".join(buffer)))
            current = text.removeprefix("CASE ")
            buffer = [text]
            continue
        if not current:
            continue
        if kind == "p":
            buffer.append(text)
        else:
            rows = payload if isinstance(payload, list) else []
            for row in rows:
                buffer.extend(str(cell) for cell in row)
    if current:
        chunks.append((current, "\n".join(buffer)))
    return chunks


def _source_hashes() -> dict[str, str]:
    names = (
        "resident_validation_cases.json",
        "investigator_answer_key.json",
        "batch_plan.json",
    )
    hashes: dict[str, str] = {}
    for folder in ("balanced", "seed_guided"):
        for name in names:
            path = ROOT / "data" / "case_sets" / folder / name
            hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def test_casebooks_match_plan_and_answer_key_without_changing_sources(tmp_path: Path) -> None:
    before = _source_hashes()
    written = export_casebooks(ROOT, tmp_path)
    assert _source_hashes() == before
    balanced, seed = load_active_batches(ROOT)
    expected = {
        balanced: "CliniProof_Balanced_Validation_Casebook.docx",
        seed: "CliniProof_SeedGuided_Validation_Casebook.docx",
    }
    for batch, filename in expected.items():
        cases = load_prepared_cases(batch)
        stats = stats_for(batch, cases)
        assert stats.total == 24
        assert stats.controls == 4
        assert stats.error_bearing == 20
        assert stats.family_1 + stats.family_2 == 20
        path = written[filename]
        document = Document(str(path))
        assert document.paragraphs
        chunks = _chunks(_blocks(path))
        assert [case_id for case_id, _text in chunks] == [item.case_id for item in cases]
        by_id = {item.case_id: item for item in cases}
        for case_id, text in chunks:
            item = by_id[case_id]
            chart, after_c1 = text.split("C1 — Clinical plausibility", 1)
            _c1, reference_onward = after_c1.split("Validation Reference", 1)
            reference, after_reference = reference_onward.split(
                "C2 — Intended assessment problem", 1
            )
            assert "C2 — Intended assessment problem" in reference_onward
            assert "C3 — Detectability" in after_reference
            assert "C4 — Absence of unintended competing problems" in after_reference
            assert "C5 — Expected learner difficulty" in after_reference
            assert "Overall recommendation" in after_reference
            assert "☐ Accept" in after_reference
            assert "☐ Revise" in after_reference
            assert "☐ Exclude" in after_reference
            for label in (
                "C1 reviewer comments",
                "C2 reviewer comments",
                "C3 reviewer comments",
                "C4 reviewer comments",
                "C5 reviewer comments",
                "Overall comments / suggested revisions",
            ):
                assert label in text
            assert "Validation Reference" not in chart
            for context in ("home", "inpatient", "discharge"):
                for row in rows_for_context(item.resident, context):
                    drug, dose, route, frequency = medication_tuple(row)
                    assert drug in chart
                    assert dose in chart
                    assert route in chart
                    assert frequency in chart
            if item.is_control:
                assert "Clean control" in reference
                assert "Error-bearing" not in reference
            else:
                assert item.error["error_description"] in reference
                assert item.error["correct_action"] in reference
                assert item.error["error_category"] in reference
                assert "Error-bearing" in reference
        whole = "\n".join(paragraph.text for paragraph in document.paragraphs)
        assert "Saving your completed review" in whole
        assert "agreed study communication channel" in whole
        assert "do not need to edit GitHub" in whole
        assert "will not be shown to residents during the later assessment study" in whole


def test_committed_casebooks_open() -> None:
    for name in (
        "CliniProof_Balanced_Validation_Casebook.docx",
        "CliniProof_SeedGuided_Validation_Casebook.docx",
    ):
        document = Document(str(PACKAGE / name))
        headings = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.style is not None
            and paragraph.style.name == "Heading 1"
            and paragraph.text.startswith("CASE VAL-")
        ]
        assert len(headings) == 24
        assert len(set(headings)) == 24
