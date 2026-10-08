"""Render Generation 2 charts without adding clinical facts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.services.validation_casebook import (
    PreparedCase,
    _start_case_section,
    _write_validation,
)
from app.services.word_controls import finalize_word_form, prepare_form_document
from app.services.word_export import _add_body, _add_heading, _new_document, _render_case


def render_case_markdown(resident: dict[str, Any]) -> str:
    clinical = resident.get("ClinicalCase") or {}
    presentation = clinical.get("presentation") or {}
    lines = [
        f"# {resident.get('case_id_code')}",
        "",
        clinical.get("one_liner") or "",
        "",
        "## Presentation",
        "",
        str(presentation.get("hpi") or ""),
        "",
        "## Hospital course",
        "",
    ]
    for note in resident.get("CaseNote") or []:
        if isinstance(note, dict) and note.get("note_type") == "hospital_course":
            lines.append(str(note.get("note_text") or ""))
    lines.extend(["", "## Diagnoses", ""])
    for row in resident.get("CaseDiagnosis") or []:
        if isinstance(row, dict):
            lines.append(
                f"- {row.get('diagnosis')} ({row.get('diagnosis_type')})"
            )
    lines.extend(["", "## Laboratory trajectory", ""])
    for row in resident.get("CaseLab") or []:
        if isinstance(row, dict):
            value = row.get("value")
            if value is None:
                value = row.get("value_text")
            lines.append(
                f"- {row.get('timepoint')}: {row.get('test_name')} {value} {row.get('unit') or ''}".rstrip()
            )
    lines.extend(["", "## Vital signs", ""])
    for row in resident.get("CaseVital") or []:
        if isinstance(row, dict):
            lines.append(
                f"- {row.get('timepoint')}: BP {row.get('bp_systolic')}/{row.get('bp_diastolic')}, "
                f"HR {row.get('heart_rate')}, temp {row.get('temp_c')}"
            )
    lines.extend(["", "## Medications", ""])
    for row in resident.get("CaseMedication") or []:
        if isinstance(row, dict):
            lines.append(
                f"- {row.get('context')}: {row.get('drug')} {row.get('dose')} {row.get('route')} "
                f"{row.get('frequency')}. {row.get('notes') or ''}"
            )
    lines.extend(["", "## Monitoring and follow-up", ""])
    for row in resident.get("CaseMonitoring") or []:
        if isinstance(row, dict):
            lines.append(f"- Monitor {row.get('parameter')} {row.get('frequency')}")
    for row in resident.get("CaseFollowup") or []:
        if isinstance(row, dict):
            lines.append(f"- {row.get('item')} {row.get('timing')} ({row.get('with_service')})")
    return "\n".join(lines).rstrip() + "\n"


def write_readable(root: Path) -> None:
    resident_dir = root / "cases" / "resident"
    readable = root / "readable"
    case_dir = readable / "cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    parts = [
        "# Generation 2 resident charts",
        "",
        "These pages are renderings of the structured resident JSON.",
        "They do not add facts. They omit the hidden reference plan.",
        "",
    ]
    for path in sorted(resident_dir.glob("G2-*.json")):
        resident = json.loads(path.read_text(encoding="utf-8"))
        text = render_case_markdown(resident)
        (case_dir / f"{path.stem}.md").write_text(text, encoding="utf-8")
        parts.append(text)
    (readable / "all_cases.md").write_text("\n".join(parts), encoding="utf-8")


def write_casebook(root: Path, destination: Path) -> None:
    resident_dir = root / "cases" / "resident"
    evaluator_dir = root / "cases" / "evaluator"
    document = _new_document("CliniProof Generation 2 clinical validation")
    prepare_form_document(document)
    _add_heading(document, "CliniProof Generation 2 clinical validation", 0)
    _add_body(document, "Case set: synthea_cliniproof_g2")
    _add_body(document, "Cases: G2-001–G2-024")
    _add_body(
        document,
        "These cases are synthetic. They have passed automated structural and "
        "clinical-sufficiency checks. They are NOT clinically validated. "
        "Clinician review is required.",
    )
    _add_body(
        document,
        "The coding instrument is the same C1–C5 clean-case instrument used for "
        "Generation 1. Every case in this book is a clean case. There is no planted "
        "medication error. G2 identifiers are candidate identifiers, not frozen VAL "
        "study identifiers.",
    )
    _add_body(document, "Read the chart before using the validation reference.")
    title = "CliniProof Generation 2 clinical validation"
    for path in sorted(resident_dir.glob("G2-*.json")):
        resident = json.loads(path.read_text(encoding="utf-8"))
        evaluator = json.loads((evaluator_dir / path.name).read_text(encoding="utf-8"))
        prepared = PreparedCase(
            case_id=str(resident.get("case_id_code")),
            resident=resident,
            investigator={
                "control_error_status": evaluator.get("control_error_status"),
                "error": {},
            },
            plan={},
        )
        _start_case_section(document, title, prepared.case_id)
        _render_case(
            document,
            resident,
            page_break=False,
            heading_text=f"CASE {prepared.case_id}",
        )
        _write_validation(document, prepared)
    destination.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(destination))
    finalize_word_form(destination)
