"""Deterministic bibliographic normalization.

Original title and DOI strings are preserved on their own fields.
"""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime

_DOI_PREFIXES = (
    "https://doi.org/",
    "http://doi.org/",
    "https://dx.doi.org/",
    "http://dx.doi.org/",
)

_PUNCTUATION_TRANSLATION = {
    ord("\u2018"): "'",
    ord("\u2019"): "'",
    ord("\u201c"): '"',
    ord("\u201d"): '"',
    ord("\u2013"): "-",
    ord("\u2014"): "-",
    ord("\u00a0"): " ",
    ord("\u2212"): "-",
}

_YEAR_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")


def normalize_doi(raw: str | None) -> str:
    """Lowercase a DOI and remove a leading resolver or doi: label."""
    if raw is None:
        return ""
    value = raw.strip().lower()
    changed = True
    while changed and value:
        changed = False
        for prefix in _DOI_PREFIXES:
            if value.startswith(prefix):
                value = value[len(prefix) :].strip()
                changed = True
        if value.startswith("doi:"):
            value = value[4:].strip()
            changed = True
    return value


def normalize_title(title: str | None) -> str:
    """Build a comparison title. This does not replace the stored title."""
    if title is None:
        return ""
    value = title.strip().lower().translate(_PUNCTUATION_TRANSLATION)
    characters: list[str] = []
    for character in value:
        if character.isalnum() or character.isspace():
            characters.append(character)
        else:
            characters.append(" ")
    return " ".join("".join(characters).split())


def extract_year(value: str | None) -> str:
    if not value:
        return ""
    match = _YEAR_RE.search(value)
    if match:
        return match.group(1)
    return value.strip()


def make_record_id(
    source_database: str,
    source_record_id: str,
    doi_normalized: str,
    normalized_title: str,
    year: str,
    source_file: str,
) -> str:
    """Stable id for one source row. The same export row keeps the same id."""
    key = "\n".join(
        [
            source_database.strip().lower(),
            source_record_id.strip().lower(),
            doi_normalized.strip().lower(),
            normalized_title,
            year.strip(),
            source_file.strip(),
        ]
    )
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    return f"rec_{digest}"


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def batch_id_for(source_database: str, source_file: str, payload: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(source_database.strip().lower().encode("utf-8"))
    digest.update(b"\n")
    digest.update(source_file.encode("utf-8"))
    digest.update(b"\n")
    digest.update(payload)
    return f"batch_{digest.hexdigest()[:16]}"
