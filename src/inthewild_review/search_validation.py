"""Known-item search validation report.

A study is missed only when a human or a recorded search has set retrieved to NO.
A blank retrieved cell means the search has not been checked.
"""

from __future__ import annotations

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.schemas import KNOWN_ITEM_LABELS, SEARCH_VALIDATION_FIELDS


def seed_known_items(layout: ReviewLayout) -> list[dict[str, str]]:
    """Create the known-item rows once. Never marks a study retrieved."""
    existing = read_csv(layout.search_validation)
    if existing:
        return existing
    rows = []
    for index, label in enumerate(KNOWN_ITEM_LABELS, start=1):
        rows.append(
            {
                "validation_id": f"KV{index:03d}",
                "citation_label": label,
                "database": "",
                "expected_retrieval": "YES",
                "retrieved": "",
                "retrieval_date": "",
                "failure_reason": "",
                "search_version": "",
                "notes": (
                    "Known-item named in the implementation brief. "
                    "expected_retrieval YES means the search is supposed to find it. "
                    "retrieved is blank until a database export is checked. "
                    "No DOI is stored here."
                ),
            }
        )
    write_csv(layout.search_validation, rows, SEARCH_VALIDATION_FIELDS, layout.root)
    return rows


def render_search_validation_report(layout: ReviewLayout) -> str:
    rows = read_csv(layout.search_validation)
    lines = [
        "# Search validation",
        "",
        "This report reads `data/search_validation.csv`.",
        "It does not query a database and it does not fill retrieval outcomes.",
        "",
        "Status rules:",
        "",
        "- blank `retrieved`: not yet assessed",
        "- `retrieved` YES: retrieved by the recorded search",
        "- `retrieved` NO: missed by the recorded search",
        "",
    ]
    if not rows:
        lines.append("No known-item rows are recorded.")
        lines.append("")
        return "\n".join(lines)
    missed: list[dict[str, str]] = []
    retrieved: list[dict[str, str]] = []
    pending: list[dict[str, str]] = []
    for row in rows:
        status = (row.get("retrieved") or "").strip().upper()
        if status == "YES":
            retrieved.append(row)
        elif status == "NO":
            missed.append(row)
        elif status == "":
            pending.append(row)
        else:
            lines.append(
                f"- {row.get('validation_id')}: retrieved value {status!r} is not YES, NO, or blank."
            )
    lines.extend(
        [
            f"- Known-item rows: {len(rows)}",
            f"- Retrieved: {len(retrieved)}",
            f"- Missed: {len(missed)}",
            f"- Not yet assessed: {len(pending)}",
            "",
            "## Not yet assessed",
            "",
        ]
    )
    if not pending:
        lines.append("None.")
        lines.append("")
    for row in pending:
        database = row.get("database") or "database not specified"
        lines.append(
            f"- {row.get('citation_label')} ({database}); search version: "
            f"{row.get('search_version') or 'not recorded'}"
        )
    lines.extend(["", "## Missed by a recorded search", ""])
    if not missed:
        lines.append("No known item is marked missed.")
        lines.append("")
    else:
        lines.append("| citation | database | search version | failure reason |")
        lines.append("| --- | --- | --- | --- |")
        for row in missed:
            lines.append(
                f"| {row.get('citation_label', '')} | {row.get('database', '')} | "
                f"{row.get('search_version', '')} | {row.get('failure_reason', '')} |"
            )
        lines.append("")
    lines.extend(["## Retrieved", ""])
    if not retrieved:
        lines.append("No known item is marked retrieved.")
        lines.append("")
    else:
        for row in retrieved:
            lines.append(
                f"- {row.get('citation_label')} via {row.get('database') or 'unspecified database'} "
                f"on {row.get('retrieval_date') or 'date not recorded'}"
            )
        lines.append("")
    return "\n".join(lines)


def write_search_validation_report(layout: ReviewLayout) -> str:
    text = render_search_validation_report(layout)
    output = layout.path("outputs", "reports")
    output.mkdir(parents=True, exist_ok=True)
    (output / "search_validation_report.md").write_text(text, encoding="utf-8")
    return text
