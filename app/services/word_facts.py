"""Deterministic display values for resident-facing case JSON.

This module does not invent clinical content. It only normalizes whitespace,
renders booleans as Yes/No, and spells numbers the way JSON does.
"""

from __future__ import annotations

import json
import re
from typing import Any

NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
INTERNAL_MED_STATUS = frozenset({"home", "active", "discharge"})
INTERNAL_NOTE = "synthetic_model_generated"

LABELIZE_KEYS = frozenset(
    {
        "timepoint",
        "placement_timepoint",
        "diagnosis_type",
        "problem_type",
        "procedure_type",
        "context",
        "category",
        "priority",
        "bpmh_source",
        "medrec_status",
        "status",
    }
)


def is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if isinstance(value, list | tuple | dict) and len(value) == 0:
        return True
    return False


def exact_text(value: object) -> str | None:
    """Return the source value as text, without rounding or rewriting."""
    if is_missing(value):
        return None
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, str):
        text = value.replace("\r\n", "\n").replace("\r", "\n").strip()
        return text or None
    if isinstance(value, int | float):
        return json.dumps(value)
    if isinstance(value, list):
        parts = [exact_text(item) for item in value]
        kept = [part for part in parts if part]
        return ", ".join(kept) if kept else None
    text = str(value).strip()
    return text or None


def labelize(value: str) -> str:
    return value.replace("_", " ")


def field_text(row: dict[str, Any], key: str) -> str | None:
    raw = exact_text(row.get(key))
    if raw is None:
        return None
    if key in LABELIZE_KEYS:
        return labelize(raw)
    return raw


def source_numbers(case: dict[str, Any]) -> set[str]:
    return set(NUMBER_RE.findall(json.dumps(case)))


def strings_in(value: object, found: set[str]) -> None:
    if isinstance(value, str):
        text = value.strip()
        if text:
            found.add(text)
            if "_" in text:
                found.add(labelize(text))
    elif isinstance(value, dict):
        for item in value.values():
            strings_in(item, found)
    elif isinstance(value, list):
        for item in value:
            strings_in(item, found)


def source_strings(case: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    strings_in(case, found)
    return found


def medication_note(row: dict[str, Any]) -> str:
    parts: list[str] = []
    status = exact_text(row.get("status"))
    if status is not None and status not in INTERNAL_MED_STATUS:
        parts.append(f"Status: {status}")
    for key, label in (
        ("indication", "Indication"),
        ("held_reason", "Held reason"),
        ("quantity_or_days", "Supply"),
        ("monitoring", "Monitoring"),
        ("target_or_goal", "Target"),
        ("notes", "Note"),
    ):
        value = exact_text(row.get(key))
        if value is None or value == INTERNAL_NOTE:
            continue
        parts.append(f"{label}: {value}")
    return "; ".join(parts)


def medication_tuple(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        exact_text(row.get("drug")) or exact_text(row.get("reported_name")) or "",
        exact_text(row.get("dose")) or "",
        exact_text(row.get("route")) or "",
        exact_text(row.get("frequency")) or "",
    )


def rows_for_context(case: dict[str, Any], context: str) -> list[dict[str, Any]]:
    rows = [
        row
        for row in case.get("CaseMedication", [])
        if isinstance(row, dict) and str(row.get("context") or "") == context
    ]
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("drug") or ""),
            str(row.get("dose") or ""),
            str(row.get("route") or ""),
            str(row.get("frequency") or ""),
            str(row.get("medication_id") or ""),
        ),
    )


def clinical(case: dict[str, Any]) -> dict[str, Any]:
    raw = case.get("ClinicalCase")
    return raw if isinstance(raw, dict) else {}


def presentation(case: dict[str, Any]) -> dict[str, Any]:
    raw = clinical(case).get("presentation")
    return raw if isinstance(raw, dict) else {}


def note_text(case: dict[str, Any], note_type: str) -> str | None:
    texts: list[str] = []
    for row in case.get("CaseNote", []):
        if isinstance(row, dict) and str(row.get("note_type") or "") == note_type:
            text = exact_text(row.get("note_text"))
            if text and text != INTERNAL_NOTE:
                texts.append(text)
    if not texts:
        return None
    return "\n\n".join(texts)
