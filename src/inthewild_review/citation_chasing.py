"""Citation-chasing provenance.

Citation-chain records enter the same normalization, duplicate, and screening
pipeline as database records. They are not treated as eligible.
No stopping rule is applied. The protocol's stopping rule is unresolved.
"""

from __future__ import annotations

import hashlib

from inthewild_review.config import ReviewLayout
from inthewild_review.importers import rebuild_normalized
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.normalize import (
    batch_id_for,
    extract_year,
    make_record_id,
    normalize_doi,
    normalize_title,
    utc_now_iso,
)
from inthewild_review.schemas import (
    CITATION_DIRECTIONS,
    CITATION_EDGE_FIELDS,
    CITATION_NODE_FIELDS,
    IMPORT_MANIFEST_FIELDS,
    NORMALIZED_FIELDS,
)


def _edge_id(row: dict[str, str]) -> str:
    key = "|".join(
        [
            row.get("seed_record_id", ""),
            row.get("citing_or_cited_record", ""),
            row.get("direction", ""),
            row.get("iteration", ""),
            row.get("parent_record", ""),
        ]
    )
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    return f"edge_{digest}"


def validate_edge(row: dict[str, str]) -> None:
    direction = (row.get("direction") or "").strip()
    if direction not in CITATION_DIRECTIONS:
        raise ValueError(
            f"Citation direction {direction!r} is invalid. Use BACKWARD or FORWARD."
        )
    if not (row.get("citing_or_cited_record") or "").strip() and not (
        row.get("title") or ""
    ).strip():
        raise ValueError("A citation-chasing row needs citing_or_cited_record or a title.")
    iteration = (row.get("iteration") or "").strip()
    if iteration and not iteration.isdigit():
        raise ValueError(f"Citation iteration {iteration!r} must be a positive integer string.")


def import_citation_edges(
    layout: ReviewLayout,
    incoming: list[dict[str, str]],
) -> dict[str, int]:
    """Store edges and add any unseen cited/citing works to the normalized table.

    Existing normalized rows and existing edges are kept. Eligibility is not set.
    """
    for row in incoming:
        validate_edge(row)
    existing_edges = read_csv(layout.citation_edges)
    known_edge_ids = {row.get("edge_id", "") for row in existing_edges}
    new_edges: list[dict[str, str]] = []
    for row in incoming:
        edge = {field: row.get(field, "") for field in CITATION_EDGE_FIELDS if field != "edge_id"}
        edge["edge_id"] = row.get("edge_id") or _edge_id(row)
        edge["direction"] = row.get("direction", "").strip()
        if edge["edge_id"] in known_edge_ids:
            continue
        new_edges.append(edge)
        known_edge_ids.add(edge["edge_id"])
    all_edges = existing_edges + new_edges
    write_csv(layout.citation_edges, all_edges, CITATION_EDGE_FIELDS, layout.root)

    records = read_csv(layout.normalized)
    if layout.batches_dir.exists():
        for batch_path in layout.batches_dir.glob("*.csv"):
            records.extend(read_csv(batch_path))
    known_ids = {row.get("record_id", "") for row in records}
    known_dois = {row.get("doi_normalized", "") for row in records if row.get("doi_normalized")}
    added_rows: list[dict[str, str]] = []
    timestamp = utc_now_iso()
    for row in incoming:
        external_id = (row.get("citing_or_cited_record") or "").strip()
        doi = normalize_doi(row.get("doi_raw") or row.get("doi") or "")
        title = row.get("title", "")
        year = extract_year(row.get("year", ""))
        normalized = normalize_title(title)
        if external_id and external_id in known_ids:
            continue
        if doi and doi in known_dois:
            continue
        record_id = external_id if external_id.startswith("rec_") else make_record_id(
            "citation_chasing",
            external_id,
            doi,
            normalized,
            year,
            row.get("discovery_source", "citation_chasing"),
        )
        if record_id in known_ids:
            continue
        added_rows.append(
            {
                "record_id": record_id,
                "source_database": "citation_chasing",
                "source_record_id": external_id,
                "title": title,
                "normalized_title": normalized,
                "abstract": row.get("abstract", ""),
                "authors": row.get("authors", ""),
                "year": year,
                "journal_or_venue": row.get("journal_or_venue", ""),
                "volume": "",
                "issue": "",
                "pages": "",
                "doi_raw": row.get("doi_raw") or row.get("doi") or "",
                "doi_normalized": doi,
                "url": "",
                "document_type": "",
                "keywords": "",
                "indexed_keywords": "",
                "language": "",
                "source_file": row.get("discovery_source", ""),
                "import_timestamp": timestamp,
                "origin": "citation_chasing",
                "discovery_source": row.get("discovery_source", ""),
            }
        )
        known_ids.add(record_id)
        if doi:
            known_dois.add(doi)
    by_external = {
        row["source_record_id"]: row["record_id"]
        for row in added_rows
        if row["source_record_id"] and row["source_record_id"] != row["record_id"]
    }
    if by_external:
        for edge in all_edges:
            current = edge.get("citing_or_cited_record", "")
            if current in by_external:
                edge["citing_or_cited_record"] = by_external[current]
            parent = edge.get("parent_record", "")
            if parent in by_external:
                edge["parent_record"] = by_external[parent]
        write_csv(layout.citation_edges, all_edges, CITATION_EDGE_FIELDS, layout.root)
    if added_rows:
        payload = "\n".join(row["record_id"] for row in added_rows).encode("utf-8")
        batch_id = batch_id_for("citation_chasing", timestamp, payload)
        batch_path = layout.batches_dir / f"{batch_id}.csv"
        write_csv(batch_path, added_rows, NORMALIZED_FIELDS, layout.root)
        manifest_rows = read_csv(layout.manifest)
        manifest_rows.append(
            {
                "batch_id": batch_id,
                "source_database": "citation_chasing",
                "source_format": "citation_edges",
                "source_file": "citation_chasing",
                "import_timestamp": timestamp,
                "record_count": str(len(added_rows)),
                "notes": "Citation-chasing records. Not eligible until screened.",
            }
        )
        write_csv(layout.manifest, manifest_rows, IMPORT_MANIFEST_FIELDS, layout.root)
    rebuilt = rebuild_normalized(layout)
    _write_nodes(layout, rebuilt, all_edges)
    return {
        "edges_added": len(new_edges),
        "records_added": len(added_rows),
        "edges_total": len(all_edges),
    }


def _write_nodes(
    layout: ReviewLayout,
    records: list[dict[str, str]],
    edges: list[dict[str, str]],
) -> None:
    by_id = {row["record_id"]: row for row in records if row.get("record_id")}
    seeds = sorted({row.get("seed_record_id", "") for row in edges if row.get("seed_record_id")})
    nodes: list[dict[str, str]] = []
    seen: set[str] = set()
    for seed in seeds:
        if seed in seen:
            continue
        source = by_id.get(seed, {})
        nodes.append(
            {
                "record_id": seed,
                "seed_record_id": seed,
                "title": source.get("title", ""),
                "doi_normalized": source.get("doi_normalized", ""),
                "year": source.get("year", ""),
                "entry_route": "SEED",
                "discovery_source": "seed",
                "date_retrieved": "",
                "in_bibliographic_set": "YES" if source else "NO",
            }
        )
        seen.add(seed)
    for edge in edges:
        record_id = edge.get("citing_or_cited_record", "")
        if not record_id or record_id in seen:
            continue
        source = by_id.get(record_id, {})
        nodes.append(
            {
                "record_id": record_id,
                "seed_record_id": edge.get("seed_record_id", ""),
                "title": source.get("title", ""),
                "doi_normalized": source.get("doi_normalized", ""),
                "year": source.get("year", ""),
                "entry_route": edge.get("direction", ""),
                "discovery_source": edge.get("discovery_source", ""),
                "date_retrieved": edge.get("date_retrieved", ""),
                "in_bibliographic_set": "YES" if source else "NO",
            }
        )
        seen.add(record_id)
    write_csv(layout.citation_nodes, nodes, CITATION_NODE_FIELDS, layout.root)
