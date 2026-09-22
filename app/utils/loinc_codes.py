"""Official LOINC identifier shapes.

LOINC term codes are 1-5 digits, a hyphen, and a check digit. Part (LP), answer
(LA), and group (LG) codes are also issued by Regenstrief; they are not laboratory
observation identifiers and are not stored as ref_lab_tests.
"""

from __future__ import annotations

import re

LOINC_TERM_CODE_RE = re.compile(r"^\d{1,5}-\d$")


def is_loinc_term_code(code: str | None) -> bool:
    if code is None:
        return False
    return LOINC_TERM_CODE_RE.fullmatch(code.strip()) is not None


def is_storeable_lab_code(code: str | None) -> bool:
    """Official LOINC terms, or TEST_ fixtures. Parts/answers/groups are excluded."""
    if code is None:
        return False
    text = code.strip()
    if is_loinc_term_code(text):
        return True
    return text.startswith("TEST_")

