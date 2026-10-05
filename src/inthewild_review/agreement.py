"""Agreement statistics for the calibration sample.

Cohen's kappa is undefined when expected agreement is 1. That case is reported
and does not raise. Empty samples do not produce a fabricated kappa.
"""

from __future__ import annotations

import math
from collections import defaultdict

from inthewild_review.schemas import SCREENING_DECISIONS

COLLAPSED_INCLUDE = "INCLUDE_OR_MAYBE"
COLLAPSED_CATEGORIES = (COLLAPSED_INCLUDE, "EXCLUDE")


def collapse_decision(decision: str) -> str:
    if decision in {"INCLUDE", "MAYBE"}:
        return COLLAPSED_INCLUDE
    if decision == "EXCLUDE":
        return "EXCLUDE"
    raise ValueError(f"Cannot collapse decision {decision!r}.")


def confusion_matrix(
    pairs: list[tuple[str, str]],
    categories: tuple[str, ...] | list[str],
) -> dict[str, dict[str, int]]:
    matrix = {left: {right: 0 for right in categories} for left in categories}
    for left, right in pairs:
        if left not in matrix or right not in matrix[left]:
            raise ValueError(f"Label pair {(left, right)!r} is outside {tuple(categories)!r}.")
        matrix[left][right] += 1
    return matrix


def percentage_agreement(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    matches = sum(1 for left, right in pairs if left == right)
    return matches / len(pairs)


def cohens_kappa(
    pairs: list[tuple[str, str]],
    categories: tuple[str, ...] | list[str],
) -> dict[str, float | int | str | None]:
    """Cohen's kappa for a fixed category list. Zero cells are allowed."""
    categories = tuple(categories)
    sample_size = len(pairs)
    if sample_size == 0:
        return {
            "n": 0,
            "po": None,
            "pe": None,
            "kappa": None,
            "note": "No paired decisions. Kappa is not estimated.",
        }
    matrix = confusion_matrix(pairs, categories)
    observed = sum(matrix[category][category] for category in categories) / sample_size
    row_totals = {category: sum(matrix[category].values()) for category in categories}
    column_totals = {
        category: sum(matrix[left][category] for left in categories) for category in categories
    }
    expected = sum(
        (row_totals[category] / sample_size) * (column_totals[category] / sample_size)
        for category in categories
    )
    if math.isclose(expected, 1.0):
        return {
            "n": sample_size,
            "po": observed,
            "pe": expected,
            "kappa": None,
            "note": "Expected agreement is 1, so Cohen's kappa is undefined.",
        }
    return {
        "n": sample_size,
        "po": observed,
        "pe": expected,
        "kappa": (observed - expected) / (1.0 - expected),
        "note": "",
    }


def paired_decisions(
    reviewer_1: list[dict[str, str]],
    reviewer_2: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[str], list[str]]:
    """Pair rows that both have a decision. Returns pairs plus ids missing a partner decision."""
    left = {
        row["record_id"]: row
        for row in reviewer_1
        if row.get("record_id") and (row.get("decision") or "").strip()
    }
    right = {
        row["record_id"]: row
        for row in reviewer_2
        if row.get("record_id") and (row.get("decision") or "").strip()
    }
    shared = sorted(set(left) & set(right))
    pairs = []
    for record_id in shared:
        pairs.append(
            {
                "record_id": record_id,
                "reviewer_1_decision": left[record_id]["decision"].strip(),
                "reviewer_2_decision": right[record_id]["decision"].strip(),
                "reviewer_1_exclusion_code": (left[record_id].get("exclusion_code") or "").strip(),
                "reviewer_2_exclusion_code": (right[record_id].get("exclusion_code") or "").strip(),
                "reviewer_1_notes": left[record_id].get("notes", ""),
                "reviewer_2_notes": right[record_id].get("notes", ""),
            }
        )
    missing_1 = sorted(set(right) - set(left))
    missing_2 = sorted(set(left) - set(right))
    return pairs, missing_1, missing_2


def disagreement_rows(pairs: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in pairs if row["reviewer_1_decision"] != row["reviewer_2_decision"]]


def agreement_summary(pairs: list[dict[str, str]]) -> dict[str, object]:
    three_way = [
        (row["reviewer_1_decision"], row["reviewer_2_decision"]) for row in pairs
    ]
    collapsed = [(collapse_decision(left), collapse_decision(right)) for left, right in three_way]
    return {
        "three_way": cohens_kappa(three_way, SCREENING_DECISIONS),
        "three_way_matrix": confusion_matrix(three_way, SCREENING_DECISIONS) if three_way else {},
        "collapsed": cohens_kappa(collapsed, COLLAPSED_CATEGORIES),
        "collapsed_matrix": confusion_matrix(collapsed, COLLAPSED_CATEGORIES) if collapsed else {},
        "disagreements": disagreement_rows(pairs),
    }


def _format_stat(value: float | int | str | None) -> str:
    if value is None:
        return "undefined"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _matrix_markdown(
    matrix: dict[str, dict[str, int]],
    categories: tuple[str, ...],
) -> list[str]:
    if not matrix:
        return ["No paired ratings.", ""]
    header = "| Reviewer 1 \\ Reviewer 2 | " + " | ".join(categories) + " |"
    separator = "| --- | " + " | ".join("---" for _ in categories) + " |"
    lines = [header, separator]
    for left in categories:
        cells = " | ".join(str(matrix[left][right]) for right in categories)
        lines.append(f"| {left} | {cells} |")
    lines.append("")
    return lines


def render_calibration_report(
    *,
    sample_size: int,
    seed: str,
    method: str,
    pairs: list[dict[str, str]],
    missing_reviewer_1: list[str],
    missing_reviewer_2: list[str],
) -> str:
    summary = agreement_summary(pairs)
    three = summary["three_way"]
    collapsed = summary["collapsed"]
    assert isinstance(three, dict)
    assert isinstance(collapsed, dict)
    lines = [
        "# Calibration agreement",
        "",
        "This report is calculated from the independent reviewer files.",
        "It does not change those files and it does not adjudicate disagreements.",
        "",
        f"- Calibration sample size: {sample_size}",
        f"- Random seed recorded with the sample: {seed or 'not recorded'}",
        f"- Sampling method: {method or 'not recorded'}",
        f"- Paired records with decisions from both reviewers: {len(pairs)}",
        f"- Decisions present for reviewer 2 only: {len(missing_reviewer_1)}",
        f"- Decisions present for reviewer 1 only: {len(missing_reviewer_2)}",
        "",
        "## Three-category agreement (INCLUDE / MAYBE / EXCLUDE)",
        "",
        "MAYBE is kept as its own category in this calculation.",
        "",
        f"- Percentage agreement: {_format_stat(None if three['po'] is None else float(three['po']) * 100)}%",
        f"- Cohen's kappa: {_format_stat(three['kappa'])}",
        f"- Observed agreement (proportion): {_format_stat(three['po'])}",
        f"- Expected agreement (proportion): {_format_stat(three['pe'])}",
    ]
    if three.get("note"):
        lines.append(f"- Note: {three['note']}")
    lines.extend(["", "### Confusion matrix", ""])
    matrix = summary["three_way_matrix"]
    assert isinstance(matrix, dict)
    lines.extend(_matrix_markdown(matrix, SCREENING_DECISIONS))
    lines.extend(
        [
            "## Collapsed agreement (INCLUDE_OR_MAYBE vs EXCLUDE)",
            "",
            "INCLUDE and MAYBE are combined only in this section.",
            "The stored screening decisions are not changed.",
            "",
            f"- Percentage agreement: {_format_stat(None if collapsed['po'] is None else float(collapsed['po']) * 100)}%",
            f"- Cohen's kappa: {_format_stat(collapsed['kappa'])}",
            f"- Observed agreement (proportion): {_format_stat(collapsed['po'])}",
            f"- Expected agreement (proportion): {_format_stat(collapsed['pe'])}",
        ]
    )
    if collapsed.get("note"):
        lines.append(f"- Note: {collapsed['note']}")
    lines.extend(["", "### Collapsed confusion matrix", ""])
    collapsed_matrix = summary["collapsed_matrix"]
    assert isinstance(collapsed_matrix, dict)
    lines.extend(_matrix_markdown(collapsed_matrix, COLLAPSED_CATEGORIES))
    lines.extend(["## Disagreements", ""])
    disagreements = summary["disagreements"]
    assert isinstance(disagreements, list)
    if not disagreements:
        lines.append("No disagreements among paired decisions.")
        lines.append("")
    else:
        lines.append("| record_id | reviewer 1 | reviewer 2 | exclusion code 1 | exclusion code 2 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for row in disagreements:
            lines.append(
                "| {record_id} | {reviewer_1_decision} | {reviewer_2_decision} | "
                "{reviewer_1_exclusion_code} | {reviewer_2_exclusion_code} |".format(**row)
            )
        lines.append("")
    if missing_reviewer_1 or missing_reviewer_2:
        lines.extend(["## Unpaired decisions", ""])
        if missing_reviewer_1:
            lines.append("Reviewer 2 has a decision and reviewer 1 does not:")
            lines.append("")
            for record_id in missing_reviewer_1:
                lines.append(f"- {record_id}")
            lines.append("")
        if missing_reviewer_2:
            lines.append("Reviewer 1 has a decision and reviewer 2 does not:")
            lines.append("")
            for record_id in missing_reviewer_2:
                lines.append(f"- {record_id}")
            lines.append("")
    lines.append(
        "Percentage agreement above is the observed proportion multiplied by 100. "
        "A blank kappa means the statistic is undefined for these ratings, not that agreement is zero."
    )
    lines.append("")
    return "\n".join(lines)


def count_by_decision(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        decision = (row.get("decision") or "").strip()
        if decision:
            counts[decision] += 1
    return dict(counts)
