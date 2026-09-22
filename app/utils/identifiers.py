"""Dashboard business-id formats.

Phase 1 defines the format only. Nothing here talks to a model or writes a row.
Case codes look like SYN-000001. Child ids look like DX-SYN000001-001.
Frozen resident-validation ids look like VAL-001.
"""

from __future__ import annotations

import re

CASE_CODE_RE = re.compile(r"^SYN-\d{6}$")
VALIDATION_CASE_RE = re.compile(r"^VAL-\d{3}$")

# Prefixes assigned in Python after structured generation.
CHILD_ID_PREFIXES: dict[str, str] = {
    "diagnosis": "DX",
    "symptom": "SYM",
    "lab": "LAB",
    "medication": "MED",
    "vital": "VIT",
    "procedure": "PROC",
    "answer_key": "AK",
    "problem": "PROB",
    "note": "NOTE",
    "weight": "WT",
    "io": "IO",
    "medrec": "MR",
    "plan": "PLAN",
    "monitoring": "MON",
    "followup": "FU",
    "instruction": "INS",
    "precaution": "RP",
    "blueprint": "BP",
    "run": "RUN",
}


def format_case_id_code(sequence: int) -> str:
    """Return a case code such as SYN-000001."""
    if sequence < 1:
        raise ValueError("sequence must be a positive integer")
    return f"SYN-{sequence:06d}"


def format_validation_case_id(sequence: int) -> str:
    """Return a frozen validation id such as VAL-001."""
    if sequence < 1:
        raise ValueError("sequence must be a positive integer")
    return f"VAL-{sequence:03d}"


def format_validation_child_id(prefix: str, validation_case_id: str, sequence: int) -> str:
    """Return a resident-facing child id such as DX-VAL001-001."""
    if sequence < 1:
        raise ValueError("sequence must be a positive integer")
    if prefix == "" or not prefix.replace("_", "").isalnum():
        raise ValueError("prefix must be a non-empty token")
    if VALIDATION_CASE_RE.fullmatch(validation_case_id) is None:
        raise ValueError("validation_case_id must match VAL-001")
    compact = validation_case_id.replace("-", "")
    return f"{prefix}-{compact}-{sequence:03d}"


def format_child_business_id(prefix: str, case_id_code: str, sequence: int) -> str:
    """Return a child id such as DX-SYN000001-001 for case code SYN-000001."""
    if sequence < 1:
        raise ValueError("sequence must be a positive integer")
    if prefix == "" or not prefix.replace("_", "").isalnum():
        raise ValueError("prefix must be a non-empty token")
    if CASE_CODE_RE.fullmatch(case_id_code) is None:
        raise ValueError("case_id_code must match SYN-000001")
    compact_case = "SYN" + case_id_code.removeprefix("SYN-")
    return f"{prefix}-{compact_case}-{sequence:03d}"
