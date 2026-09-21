"""Unit text helpers.

Phase 1 does not ship UCUM concepts or conversion factors.
"""

from __future__ import annotations


def normalize_unit_text(value: str | None) -> str | None:
    """Strip surrounding whitespace. Blank text becomes None rather than an empty string."""
    if value is None:
        return None
    stripped = value.strip()
    if stripped == "":
        return None
    return stripped
