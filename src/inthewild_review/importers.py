"""Bibliographic importers.

Raw exports are read and left unchanged. Parsed rows are written only under
data/interim.
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, read_text_export, write_csv
from inthewild_review.normalize import (
    batch_id_for,
    extract_year,
    make_record_id,
    normalize_doi,
    normalize_title,
    utc_now_iso,
)
from inthewild_review.schemas import IMPORT_MANIFEST_FIELDS, NORMALIZED_FIELDS

_TITLE = ("title", "document title", "article title", "ti", "t1")
_ABSTRACT = ("abstract", "ab", "n2", "abstract note")
_AUTHORS = (
    "authors",
    "author",
    "author full names",
    "author(s)",
    "au",
    "a1",
)
_YEAR = ("year", "publication year", "py", "y1", "da", "dp")
_VENUE = (
    "journal_or_venue",
    "source title",
    "publication title",
    "so",
    "journal",
    "jo",
    "jf",
    "t2",
    "booktitle",
    "proceedings title",
)
_VOLUME = ("volume", "vl", "vi")
_ISSUE = ("issue", "is", "ip")
_PAGES = ("pages", "page", "pg")
_PAGE_START = ("page start", "bp", "sp")
_PAGE_END = ("page end", "ep")
_DOI = ("doi", "di", "do", "doi link")
_URL = ("url", "link", "ur", "pdf link")
_TYPE = ("document type", "document_type", "dt", "ty", "pubtype")
_KEYWORDS = ("keywords", "author keywords", "de", "kw")
_INDEX = ("indexed keywords", "index keywords", "id", "mesh terms", "mh")
_LANGUAGE = ("language", "la")
_SOURCE_ID = ("eid", "ut", "pmid", "an", "unique-id", "accession number", "id")


def _lookup(row: dict[str, str]) -> dict[str, str]:
    return {str(key).strip().lower(): (value or "") for key, value in row.items() if key}


def _first(lookup: dict[str, str], names: tuple[str, ...]) -> str:
    for name in names:
        value = lookup.get(name, "")
        if value:
            return value
    return ""


def _pages(lookup: dict[str, str]) -> str:
    pages = _first(lookup, _PAGES)
    if pages:
        return pages
    start = _first(lookup, _PAGE_START)
    end = _first(lookup, _PAGE_END)
    if start and end:
        return f"{start}-{end}"
    return start or end


def canonical_from_mapping(
    lookup: dict[str, str],
    *,
    source_database: str,
    source_file: str,
    import_timestamp: str,
    origin: str,
    discovery_source: str,
    source_record_id: str = "",
) -> dict[str, str]:
    title = _first(lookup, _TITLE)
    doi_raw = _first(lookup, _DOI)
    doi_normalized = normalize_doi(doi_raw)
    year = extract_year(_first(lookup, _YEAR))
    record_source_id = source_record_id or _first(lookup, _SOURCE_ID)
    normalized = normalize_title(title)
    return {
        "record_id": make_record_id(
            source_database,
            record_source_id,
            doi_normalized,
            normalized,
            year,
            source_file,
        ),
        "source_database": source_database,
        "source_record_id": record_source_id,
        "title": title,
        "normalized_title": normalized,
        "abstract": _first(lookup, _ABSTRACT),
        "authors": _first(lookup, _AUTHORS),
        "year": year,
        "journal_or_venue": _first(lookup, _VENUE),
        "volume": _first(lookup, _VOLUME),
        "issue": _first(lookup, _ISSUE),
        "pages": _pages(lookup),
        "doi_raw": doi_raw,
        "doi_normalized": doi_normalized,
        "url": _first(lookup, _URL),
        "document_type": _first(lookup, _TYPE),
        "keywords": _first(lookup, _KEYWORDS),
        "indexed_keywords": _first(lookup, _INDEX),
        "language": _first(lookup, _LANGUAGE),
        "source_file": source_file,
        "import_timestamp": import_timestamp,
        "origin": origin,
        "discovery_source": discovery_source,
    }


def detect_format(path: Path, text: str) -> str:
    stripped = text.lstrip("\ufeff").lstrip()
    head = stripped[:400].lower()
    name = path.name.lower()
    if name.endswith(".bib") or head.startswith("@"):
        return "bibtex"
    if head.startswith("ty  -") or "\nty  -" in head:
        return "ris"
    if head.startswith("pmid-") or re.search(r"(?m)^TI\s{2}-", stripped):
        return "nbib"
    first = stripped.splitlines()[0] if stripped else ""
    if "\t" in first:
        return "tsv"
    return "csv"


def parse_delimited(text: str, delimiter: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    rows: list[dict[str, str]] = []
    for row in reader:
        rows.append({key: value or "" for key, value in row.items() if key is not None})
    return rows


def parse_ris(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Z0-9]{2})\s*-\s?(.*)$", line)
        if not match:
            continue
        tag, value = match.group(1), match.group(2).strip()
        if tag == "TY":
            if current:
                records.append(current)
            current = {"TY": value}
        elif tag == "ER":
            if current:
                records.append(current)
            current = {}
        elif tag in current and current[tag]:
            current[tag] = current[tag] + "; " + value
        else:
            current[tag] = value
    if current:
        records.append(current)
    return records


def parse_nbib(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    last_tag = ""
    for line in text.splitlines():
        if not line.strip():
            if current:
                records.append(current)
                current = {}
                last_tag = ""
            continue
        match = re.match(r"^([A-Z0-9]{2,4})\s*-\s?(.*)$", line)
        if match and not line.startswith(" "):
            tag, value = match.group(1), match.group(2).strip()
            if tag in current and current[tag]:
                current[tag] = current[tag] + "; " + value
            else:
                current[tag] = value
            last_tag = tag
        elif last_tag:
            extra = line.strip()
            current[last_tag] = (current.get(last_tag, "") + " " + extra).strip()
    if current:
        records.append(current)
    normalized: list[dict[str, str]] = []
    for record in records:
        doi = ""
        for tag in ("LID", "AID", "DOI"):
            candidate = record.get(tag, "")
            if "10." in candidate:
                doi = candidate.split(" ")[0].strip(" .")
                break
        normalized.append(
            {
                "title": record.get("TI", ""),
                "abstract": record.get("AB", ""),
                "authors": record.get("AU", record.get("FAU", "")),
                "year": record.get("DP", record.get("PY", "")),
                "source title": record.get("JT", record.get("TA", record.get("JT", ""))),
                "volume": record.get("VI", ""),
                "issue": record.get("IP", ""),
                "pages": record.get("PG", ""),
                "doi": doi,
                "pmid": record.get("PMID", ""),
                "keywords": record.get("OT", ""),
                "indexed keywords": record.get("MH", ""),
                "language": record.get("LA", ""),
                "document type": record.get("PT", ""),
            }
        )
    return normalized


def _matching_brace(text: str, open_index: int) -> int | None:
    depth = 0
    for index in range(open_index, len(text)):
        character = text[index]
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


def parse_bibtex(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    cursor = 0
    while True:
        at = text.find("@", cursor)
        if at < 0:
            break
        brace = text.find("{", at)
        if brace < 0:
            break
        kind = text[at + 1 : brace].strip().lower()
        end = _matching_brace(text, brace)
        if end is None:
            break
        body = text[brace + 1 : end]
        cursor = end + 1
        if kind in {"comment", "string", "preamble"}:
            continue
        fields = _bibtex_fields(body)
        fields["document type"] = kind
        records.append(fields)
    return records


def _bibtex_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    depth = 0
    split_at = None
    for index, character in enumerate(body):
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
        elif character == "," and depth == 0:
            split_at = index
            break
    remainder = body if split_at is None else body[split_at + 1 :]
    if split_at is not None:
        fields["source_record_id"] = body[:split_at].strip()
    token = ""
    index = 0
    while index < len(remainder):
        character = remainder[index]
        if character == "=":
            name = token.strip().lower().replace("\n", " ")
            token = ""
            index += 1
            while index < len(remainder) and remainder[index].isspace():
                index += 1
            if index >= len(remainder):
                break
            if remainder[index] == "{":
                end = _matching_brace(remainder, index)
                if end is None:
                    break
                value = remainder[index + 1 : end]
                index = end + 1
            elif remainder[index] == '"':
                end = index + 1
                while end < len(remainder) and remainder[end] != '"':
                    end += 1
                value = remainder[index + 1 : end]
                index = end + 1
            else:
                end = index
                while end < len(remainder) and remainder[end] != ",":
                    end += 1
                value = remainder[index:end]
                index = end
            if name:
                cleaned = " ".join(value.replace("\n", " ").split())
                if name in fields and fields[name]:
                    fields[name] = fields[name] + "; " + cleaned
                else:
                    fields[name] = cleaned
            while index < len(remainder) and remainder[index] in {",", " ", "\n", "\t"}:
                index += 1
            continue
        token += character
        index += 1
    return fields


def parse_export(path: Path, text: str, explicit_format: str | None = None) -> tuple[str, list[dict[str, str]]]:
    chosen = (explicit_format or "auto").lower()
    if chosen == "auto":
        chosen = detect_format(path, text)
    if chosen in {"csv", "scopus", "ieee", "acm", "pubmed", "generic"}:
        return chosen, parse_delimited(text, ",")
    if chosen in {"tsv", "wos", "web_of_science"}:
        return chosen, parse_delimited(text, "\t")
    if chosen == "ris":
        return chosen, parse_ris(text)
    if chosen in {"nbib", "medline"}:
        return chosen, parse_nbib(text)
    if chosen == "bibtex":
        return chosen, parse_bibtex(text)
    raise ValueError(f"Unsupported export format: {chosen}")


def rows_from_mappings(
    mappings: list[dict[str, str]],
    *,
    source_database: str,
    source_file: str,
    import_timestamp: str,
    origin: str = "database",
    discovery_source: str = "",
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for mapping in mappings:
        lookup = _lookup(mapping)
        source_record_id = lookup.get("source_record_id", "")
        rows.append(
            canonical_from_mapping(
                lookup,
                source_database=source_database,
                source_file=source_file,
                import_timestamp=import_timestamp,
                origin=origin,
                discovery_source=discovery_source or source_database,
                source_record_id=source_record_id,
            )
        )
    return rows


def import_export(
    layout: ReviewLayout,
    source: Path,
    source_database: str,
    explicit_format: str | None = None,
    notes: str = "",
) -> dict[str, str]:
    """Read one export and store a batch. Refuses to overwrite raw files or an existing batch."""
    source_resolved = source.resolve()
    raw_root = layout.raw_dir.resolve()
    if source_resolved != raw_root and raw_root not in source_resolved.parents:
        # Exports may also be read from a fixture path during tests.
        pass
    payload = source_resolved.read_bytes()
    text = read_text_export(source_resolved)
    chosen, mappings = parse_export(source_resolved, text, explicit_format)
    try:
        relative = str(source_resolved.relative_to(layout.root))
    except ValueError:
        relative = str(source_resolved)
    timestamp = utc_now_iso()
    batch_id = batch_id_for(source_database, relative, payload)
    batch_path = layout.batches_dir / f"{batch_id}.csv"
    if batch_path.exists():
        raise FileExistsError(
            f"Batch {batch_id} already exists at {batch_path}. "
            "Raw imports are not overwritten. Use the existing batch."
        )
    rows = rows_from_mappings(
        mappings,
        source_database=source_database,
        source_file=relative,
        import_timestamp=timestamp,
    )
    write_csv(batch_path, rows, NORMALIZED_FIELDS, layout.root)
    manifest_rows = read_csv(layout.manifest)
    manifest_rows.append(
        {
            "batch_id": batch_id,
            "source_database": source_database,
            "source_format": chosen,
            "source_file": relative,
            "import_timestamp": timestamp,
            "record_count": str(len(rows)),
            "notes": notes,
        }
    )
    write_csv(layout.manifest, manifest_rows, IMPORT_MANIFEST_FIELDS, layout.root)
    return {
        "batch_id": batch_id,
        "record_count": str(len(rows)),
        "source_format": chosen,
        "batch_path": str(batch_path),
    }


def rebuild_normalized(layout: ReviewLayout) -> list[dict[str, str]]:
    """Rebuild the canonical table from immutable batches. Does not edit batches."""
    rows: list[dict[str, str]] = []
    if layout.batches_dir.exists():
        for batch_path in sorted(layout.batches_dir.glob("*.csv")):
            rows.extend(read_csv(batch_path))
    rows.sort(key=lambda row: (row.get("source_database", ""), row.get("record_id", "")))
    write_csv(layout.normalized, rows, NORMALIZED_FIELDS, layout.root)
    return rows
