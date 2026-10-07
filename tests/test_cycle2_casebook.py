"""The Cycle 2 validation casebook is blank and covers each seed case once."""

from __future__ import annotations

import hashlib
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from app.services.cycle2_casebook import CASE_IDS, SPECIAL_QUESTIONS, write_cycle2_final_validation
from app.services.word_controls import audit_form_controls
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
FROZEN = (
    ROOT / "data" / "case_sets" / "seed_guided" / "resident_validation_cases.json",
    ROOT / "data" / "case_sets" / "balanced" / "resident_validation_cases.json",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cycle2_casebook_is_blank_and_complete(tmp_path: Path) -> None:
    before = {path: _sha(path) for path in FROZEN}
    write_cycle2_final_validation(tmp_path)
    assert {path: _sha(path) for path in FROZEN} == before
    document_path = tmp_path / "CliniProof_Cycle2_Final_Validation.docx"
    text = "\n".join(paragraph.text for paragraph in Document(str(document_path)).paragraphs)
    headings = [
        line.removeprefix("CASE ").strip()
        for line in text.splitlines()
        if line.startswith("CASE VAL-")
    ]
    assert headings == list(CASE_IDS)
    lowered = text.casefold()
    assert "clinician validation reference" in lowered
    assert "not shown to residents" in lowered
    assert "c1 — clinical plausibility" in lowered
    assert "c2 — sufficiency for resident decision-making" in lowered
    assert "c3 — reference-plan validity" in lowered
    assert "c4 — acceptable alternatives" in lowered
    assert "c5 — missing, misleading, or competing issues" in lowered
    assert "c6 — expected learner difficulty" in lowered
    assert "does any wording reveal the intended answer?" in lowered
    for question in SPECIAL_QUESTIONS.values():
        assert question in text
    assert "☒" not in text
    assert "error-bearing" not in lowered
    audit = audit_form_controls(document_path)
    assert audit.malformed_checkboxes == 0
    assert audit.checkbox_controls > 0
    assert audit.unchecked_checkboxes == audit.checkbox_controls
    assert audit.compatibility_mode == "16"
    with ZipFile(document_path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    namespace = {"w14": "http://schemas.microsoft.com/office/word/2010/wordml"}
    checked_name = "{http://schemas.microsoft.com/office/word/2010/wordml}val"
    checked = [
        node.get(checked_name) for node in root.findall(".//w14:checked", namespace)
    ]
    assert checked
    assert set(checked) == {"0"}
