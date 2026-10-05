"""PRISMA counts derived from repository files.

No count in this module is a literal. Empty inputs produce zeros.
"""

from __future__ import annotations

import json
from collections import Counter

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.normalize import utc_now_iso
from inthewild_review.schemas import (
    DEPLOYMENT_FIELDS,
    PUBLICATION_FIELDS,
    SCENARIO_FIELDS,
    STUDY_FIELDS,
)
from inthewild_review.screening import adjudicated_title_abstract


class PrismaConsistencyError(RuntimeError):
    """Raised when derived PRISMA totals do not add up."""


def _unique_by_id(rows: list[dict[str, str]], field: str, label: str) -> list[dict[str, str]]:
    chosen: dict[str, dict[str, str]] = {}
    for row in rows:
        identifier = (row.get(field) or "").strip()
        if not identifier:
            continue
        if identifier in chosen and chosen[identifier] != row:
            raise PrismaConsistencyError(
                f"Conflicting {label} rows for {identifier}. Counts are not resolved automatically."
            )
        chosen[identifier] = row
    return [chosen[key] for key in sorted(chosen)]


def build_prisma_counts(layout: ReviewLayout) -> dict[str, object]:
    records = _unique_by_id(read_csv(layout.normalized), "record_id", "normalized record")
    database_counts: Counter[str] = Counter()
    citation_count = 0
    other_count = 0
    for row in records:
        origin = (row.get("origin") or "database").strip() or "database"
        source = (row.get("source_database") or "unspecified").strip() or "unspecified"
        if origin == "citation_chasing" or source == "citation_chasing":
            citation_count += 1
        elif origin == "database":
            database_counts[source] += 1
        else:
            other_count += 1

    duplicate_rows = read_csv(layout.duplicates)
    removed_ids: set[str] = set()
    confirmed_pairs = 0
    for row in duplicate_rows:
        if (row.get("human_decision") or "").strip() != "SAME_RECORD":
            continue
        confirmed_pairs += 1
        retained = (row.get("retained_record_id") or "").strip()
        left = (row.get("record_id_1") or "").strip()
        right = (row.get("record_id_2") or "").strip()
        if retained and retained in {left, right}:
            removed_ids.add(left if retained == right else right)

    screened = adjudicated_title_abstract(read_csv(layout.title_abstract))
    decision_counts: Counter[str] = Counter()
    exclusion_counts: Counter[str] = Counter()
    for row in screened:
        decision = row["decision"].strip()
        decision_counts[decision] += 1
        if decision == "EXCLUDE":
            exclusion_counts[row.get("exclusion_code", "").strip()] += 1

    full_rows = _unique_by_id(read_csv(layout.full_text), "record_id", "full-text screening")
    availability_counts: Counter[str] = Counter()
    full_decisions: Counter[str] = Counter()
    full_reasons: Counter[str] = Counter()
    without_decision = 0
    for row in full_rows:
        availability = (row.get("full_text_available") or "").strip() or "BLANK"
        if availability not in {"YES", "NO", "UNCLEAR"}:
            availability = "BLANK"
        availability_counts[availability] += 1
        decision = (row.get("decision") or "").strip()
        if not decision:
            without_decision += 1
            continue
        full_decisions[decision] += 1
        if decision == "EXCLUDE":
            full_reasons[(row.get("exclusion_reason") or "").strip()] += 1

    included_record_ids = {
        (row.get("record_id") or "").strip()
        for row in full_rows
        if (row.get("decision") or "").strip() == "INCLUDE"
    }
    publications = [
        row
        for row in read_csv(layout.publications)
        if (row.get("record_id") or "").strip() in included_record_ids
    ]
    publication_ids = {(row.get("publication_id") or "").strip() for row in publications}
    studies = [
        row
        for row in read_csv(layout.studies)
        if (row.get("publication_id") or "").strip() in publication_ids
    ]
    study_ids = {(row.get("study_id") or "").strip() for row in studies}
    deployments = [
        row
        for row in read_csv(layout.deployments)
        if (row.get("study_id") or "").strip() in study_ids
    ]
    deployment_ids = {(row.get("deployment_id") or "").strip() for row in deployments}
    scenarios = [
        row
        for row in read_csv(layout.scenarios)
        if (row.get("deployment_id") or "").strip() in deployment_ids
    ]

    counts: dict[str, object] = {
        "generated_at": utc_now_iso(),
        "data_state": "derived_from_repository_files",
        "note": (
            "Counts are computed from the files in this repository. "
            "Zero means the corresponding file has no coded rows. "
            "It is not a search result and it is not a completed review."
        ),
        "identification": {
            "by_database": dict(sorted(database_counts.items())),
            "database_total": int(sum(database_counts.values())),
            "citation_chasing": citation_count,
            "other": other_count,
            "total_records": len(records),
        },
        "duplicates": {
            "candidate_pairs": len(duplicate_rows),
            "confirmed_same_record_pairs": confirmed_pairs,
            "records_removed": len(removed_ids),
            "note": (
                "A record is removed only when a human has marked SAME_RECORD and "
                "named retained_record_id. Unconfirmed candidates stay in the set."
            ),
        },
        "records_after_confirmed_duplicate_removal": len(records) - len(removed_ids),
        "title_abstract": {
            "screened": len(screened),
            "include": int(decision_counts.get("INCLUDE", 0)),
            "maybe": int(decision_counts.get("MAYBE", 0)),
            "exclude": int(decision_counts.get("EXCLUDE", 0)),
            "exclude_by_code": dict(sorted(exclusion_counts.items())),
            "source": "data/screening/title_abstract_screening.csv",
            "note": "Calibration files are not included in these counts.",
        },
        "full_text": {
            "sought": len(full_rows),
            "unavailable": int(availability_counts.get("NO", 0)),
            "assessed": int(availability_counts.get("YES", 0)),
            "unclear": int(availability_counts.get("UNCLEAR", 0)),
            "pending": int(availability_counts.get("BLANK", 0)),
            "include": int(full_decisions.get("INCLUDE", 0)),
            "maybe": int(full_decisions.get("MAYBE", 0)),
            "exclude": int(full_decisions.get("EXCLUDE", 0)),
            "with_decision": int(sum(full_decisions.values())),
            "without_decision": without_decision,
            "exclude_by_reason": dict(sorted(full_reasons.items())),
        },
        "included": {
            "full_text_include_records": len(included_record_ids),
            "publications": len(publications),
            "studies": len(studies),
            "deployments": len(deployments),
            "scenarios": len(scenarios),
            "note": (
                "Publication, study, deployment, and scenario counts are different units. "
                "They are not interchangeable."
            ),
        },
    }
    assert_prisma_consistent(counts)
    _write_included_views(layout, publications, studies, deployments, scenarios)
    return counts


def assert_prisma_consistent(counts: dict[str, object]) -> None:
    identification = counts["identification"]
    duplicates = counts["duplicates"]
    title_abstract = counts["title_abstract"]
    full_text = counts["full_text"]
    assert isinstance(identification, dict)
    assert isinstance(duplicates, dict)
    assert isinstance(title_abstract, dict)
    assert isinstance(full_text, dict)
    by_database = identification["by_database"]
    assert isinstance(by_database, dict)
    if identification["database_total"] != sum(by_database.values()):
        raise PrismaConsistencyError("Database total does not equal the sum of database counts.")
    expected_total = (
        identification["database_total"] + identification["citation_chasing"] + identification["other"]
    )
    if identification["total_records"] != expected_total:
        raise PrismaConsistencyError("Identification totals do not sum to total records.")
    screened_sum = title_abstract["include"] + title_abstract["maybe"] + title_abstract["exclude"]
    if title_abstract["screened"] != screened_sum:
        raise PrismaConsistencyError("Title/abstract decisions do not sum to records screened.")
    exclusion_codes = title_abstract["exclude_by_code"]
    assert isinstance(exclusion_codes, dict)
    if sum(exclusion_codes.values()) != title_abstract["exclude"]:
        raise PrismaConsistencyError("Exclusion-code counts do not sum to title/abstract exclusions.")
    sought_sum = (
        full_text["unavailable"]
        + full_text["assessed"]
        + full_text["unclear"]
        + full_text["pending"]
    )
    if full_text["sought"] != sought_sum:
        raise PrismaConsistencyError("Full-text availability counts do not sum to full texts sought.")
    decision_sum = full_text["include"] + full_text["maybe"] + full_text["exclude"]
    if full_text["with_decision"] != decision_sum:
        raise PrismaConsistencyError("Full-text decisions do not sum to rows with a decision.")
    if full_text["with_decision"] + full_text["without_decision"] != full_text["sought"]:
        raise PrismaConsistencyError("Full-text decision status does not cover every sought record.")
    reasons = full_text["exclude_by_reason"]
    assert isinstance(reasons, dict)
    if sum(reasons.values()) != full_text["exclude"]:
        raise PrismaConsistencyError("Full-text exclusion reasons do not sum to full-text exclusions.")
    if duplicates["records_removed"] > identification["total_records"]:
        raise PrismaConsistencyError("Removed duplicates exceed identified records.")
    after = identification["total_records"] - duplicates["records_removed"]
    if counts["records_after_confirmed_duplicate_removal"] != after:
        raise PrismaConsistencyError("Records remaining after duplicate removal are inconsistent.")


def _write_included_views(
    layout: ReviewLayout,
    publications: list[dict[str, str]],
    studies: list[dict[str, str]],
    deployments: list[dict[str, str]],
    scenarios: list[dict[str, str]],
) -> None:
    write_csv(
        layout.path("data", "processed", "included_publications.csv"),
        publications,
        PUBLICATION_FIELDS,
        layout.root,
    )
    write_csv(
        layout.path("data", "processed", "included_studies.csv"),
        studies,
        STUDY_FIELDS,
        layout.root,
    )
    write_csv(
        layout.path("data", "processed", "included_deployments.csv"),
        deployments,
        DEPLOYMENT_FIELDS,
        layout.root,
    )
    write_csv(
        layout.path("data", "processed", "included_scenarios.csv"),
        scenarios,
        SCENARIO_FIELDS,
        layout.root,
    )


def counts_to_rows(counts: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(section: str, item: str, value: object) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                add(section, f"{item}.{key}" if item else str(key), nested)
            return
        rows.append({"section": section, "item": item, "value": "" if value is None else str(value)})

    for section in (
        "identification",
        "duplicates",
        "title_abstract",
        "full_text",
        "included",
    ):
        block = counts[section]
        assert isinstance(block, dict)
        for key, value in block.items():
            add(section, key, value)
    rows.append(
        {
            "section": "deduplicated",
            "item": "records_after_confirmed_duplicate_removal",
            "value": str(counts["records_after_confirmed_duplicate_removal"]),
        }
    )
    return rows


def render_prisma_markdown(counts: dict[str, object]) -> str:
    identification = counts["identification"]
    duplicates = counts["duplicates"]
    title_abstract = counts["title_abstract"]
    full_text = counts["full_text"]
    included = counts["included"]
    assert isinstance(identification, dict)
    assert isinstance(duplicates, dict)
    assert isinstance(title_abstract, dict)
    assert isinstance(full_text, dict)
    assert isinstance(included, dict)
    lines = [
        "# PRISMA counts",
        "",
        counts["note"],
        "",
        "These counts were generated from repository data. They are not a completed review.",
        "",
        "## Identification",
        "",
        f"- Records identified from databases: {identification['database_total']}",
    ]
    by_database = identification["by_database"]
    assert isinstance(by_database, dict)
    if not by_database:
        lines.append("- No database records are in the normalized table.")
    for database, count in by_database.items():
        lines.append(f"  - {database}: {count}")
    lines.extend(
        [
            f"- Records identified from citation chasing: {identification['citation_chasing']}",
            f"- Records from other origins: {identification['other']}",
            f"- Total records in the normalized table: {identification['total_records']}",
            f"- Confirmed duplicate records removed: {duplicates['records_removed']}",
            f"- Candidate duplicate pairs still flagged: {duplicates['candidate_pairs']}",
            (
                "- Records after confirmed duplicate removal: "
                f"{counts['records_after_confirmed_duplicate_removal']}"
            ),
            "",
            "## Title and abstract screening",
            "",
            f"- Records screened: {title_abstract['screened']}",
            f"- INCLUDE: {title_abstract['include']}",
            f"- MAYBE: {title_abstract['maybe']}",
            f"- EXCLUDE: {title_abstract['exclude']}",
            "",
        ]
    )
    codes = title_abstract["exclude_by_code"]
    assert isinstance(codes, dict)
    if codes:
        lines.append("Excluded at title and abstract, by code:")
        lines.append("")
        for code, count in codes.items():
            lines.append(f"- {code}: {count}")
        lines.append("")
    lines.extend(
        [
            "## Full text",
            "",
            f"- Full texts sought: {full_text['sought']}",
            f"- Full texts unavailable: {full_text['unavailable']}",
            f"- Full texts assessed: {full_text['assessed']}",
            f"- Full-text availability unclear: {full_text['unclear']}",
            f"- Full-text availability still blank: {full_text['pending']}",
            f"- INCLUDE: {full_text['include']}",
            f"- MAYBE: {full_text['maybe']}",
            f"- EXCLUDE: {full_text['exclude']}",
            "",
        ]
    )
    reasons = full_text["exclude_by_reason"]
    assert isinstance(reasons, dict)
    if reasons:
        lines.append("Full-text exclusions by reason:")
        lines.append("")
        for reason, count in reasons.items():
            lines.append(f"- {reason}: {count}")
        lines.append("")
    lines.extend(
        [
            "## Included units",
            "",
            "These four counts answer different questions. Do not substitute one for another.",
            "",
            f"- Included records (full-text INCLUDE): {included['full_text_include_records']}",
            f"- Publication rows linked to those records: {included['publications']}",
            f"- Studies: {included['studies']}",
            f"- Deployments: {included['deployments']}",
            f"- Scenarios: {included['scenarios']}",
            "",
            "## Flow",
            "",
            "```mermaid",
            "flowchart TD",
            f'  A["Database records: {identification["database_total"]}"] --> C["Normalized records: {identification["total_records"]}"]',
            f'  B["Citation chasing: {identification["citation_chasing"]}"] --> C',
            f'  C --> D["After confirmed duplicate removal: {counts["records_after_confirmed_duplicate_removal"]}"]',
            f'  D --> E["Title/abstract screened: {title_abstract["screened"]}"]',
            f'  E --> F["Excluded: {title_abstract["exclude"]}"]',
            f'  E --> G["INCLUDE {title_abstract["include"]} / MAYBE {title_abstract["maybe"]}"]',
            f'  G --> H["Full texts sought: {full_text["sought"]}"]',
            f'  H --> I["Unavailable: {full_text["unavailable"]}"]',
            f'  H --> J["Assessed: {full_text["assessed"]}"]',
            f'  J --> K["Full-text excluded: {full_text["exclude"]}"]',
            f'  J --> L["Included records: {included["full_text_include_records"]}"]',
            f'  L --> M["Studies {included["studies"]} / deployments {included["deployments"]} / scenarios {included["scenarios"]}"]',
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_prisma_svg(counts: dict[str, object]) -> str:
    identification = counts["identification"]
    title_abstract = counts["title_abstract"]
    full_text = counts["full_text"]
    included = counts["included"]
    assert isinstance(identification, dict)
    assert isinstance(title_abstract, dict)
    assert isinstance(full_text, dict)
    assert isinstance(included, dict)
    labels = [
        f"Database records ({identification['database_total']})",
        f"Citation chasing ({identification['citation_chasing']})",
        f"Normalized records ({identification['total_records']})",
        f"After confirmed duplicate removal ({counts['records_after_confirmed_duplicate_removal']})",
        f"Screened ({title_abstract['screened']}); excluded ({title_abstract['exclude']})",
        f"Full texts sought ({full_text['sought']}); unavailable ({full_text['unavailable']})",
        f"Included records ({included['full_text_include_records']})",
        (
            f"Studies {included['studies']}; deployments {included['deployments']}; "
            f"scenarios {included['scenarios']}"
        ),
    ]
    width = 760
    box_height = 42
    gap = 18
    height = 40 + len(labels) * (box_height + gap)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        'role="img" aria-label="PRISMA flow derived from repository counts">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="28" font-family="sans-serif" font-size="16">'
        "PRISMA-style flow (counts from data, not typed by hand)</text>",
    ]
    for index, label in enumerate(labels):
        top = 48 + index * (box_height + gap)
        parts.append(
            f'<rect x="24" y="{top}" width="712" height="{box_height}" rx="6" '
            'fill="#f4f7fb" stroke="#243044"/>'
        )
        parts.append(
            f'<text x="40" y="{top + 26}" font-family="sans-serif" font-size="14">{label}</text>'
        )
        if index < len(labels) - 1:
            next_top = top + box_height
            parts.append(
                f'<line x1="380" y1="{next_top}" x2="380" y2="{next_top + gap}" stroke="#243044"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_prisma_outputs(layout: ReviewLayout) -> dict[str, object]:
    counts = build_prisma_counts(layout)
    output = layout.path("outputs", "prisma")
    output.mkdir(parents=True, exist_ok=True)
    (output / "prisma_counts.json").write_text(
        json.dumps(counts, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(output / "prisma_counts.csv", counts_to_rows(counts), ["section", "item", "value"], layout.root)
    (output / "prisma_summary.md").write_text(render_prisma_markdown(counts), encoding="utf-8")
    (output / "prisma_flow.svg").write_text(render_prisma_svg(counts), encoding="utf-8")
    return counts
