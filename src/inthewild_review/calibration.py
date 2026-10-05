"""Draw the two-reviewer calibration sample.

The sample is stratified by year and source database. Reviewer files are created
if they are missing and are never overwritten once a reviewer has saved a decision.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.schemas import (
    CALIBRATION_SAMPLE_FIELDS,
    DEFAULT_CALIBRATION_N,
    DEFAULT_CALIBRATION_SEED,
    SAMPLING_METHOD,
    SCREENING_FIELDS,
)


def _stratum(row: dict[str, str]) -> tuple[str, str]:
    year = (row.get("year") or "").strip() or "UNKNOWN_YEAR"
    source = (row.get("source_database") or "").strip() or "UNKNOWN_SOURCE"
    return year, source


def _allocate_quotas(
    grouped: dict[tuple[str, str], list[dict[str, str]]],
    sample_size: int,
) -> dict[tuple[str, str], int]:
    """Cover year/source strata, then allocate remaining seats by largest remainder."""
    keys = sorted(grouped)
    quotas = {key: 0 for key in keys}
    if sample_size >= len(keys):
        for key in keys:
            quotas[key] = 1
        remaining = sample_size - len(keys)
        capacities = {key: len(grouped[key]) - quotas[key] for key in keys}
        total_capacity = sum(capacities.values())
        if remaining <= 0 or total_capacity <= 0:
            return quotas
        remainders: list[tuple[float, tuple[str, str]]] = []
        allocated = 0
        for key in keys:
            if capacities[key] <= 0:
                continue
            exact = remaining * capacities[key] / total_capacity
            base = min(int(exact), capacities[key])
            quotas[key] += base
            allocated += base
            remainders.append((exact - int(exact), key))
        remainders.sort(key=lambda item: (-item[0], item[1][0], item[1][1]))
        for _fraction, key in remainders:
            if allocated >= remaining:
                break
            if quotas[key] < len(grouped[key]):
                quotas[key] += 1
                allocated += 1
        return quotas

    by_source: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for key in keys:
        by_source[key[1]].append(key)
    assigned = 0
    cursors = {source: 0 for source in by_source}
    while assigned < sample_size:
        progress = False
        for source in sorted(by_source):
            bucket = by_source[source]
            cursor = cursors[source]
            if cursor >= len(bucket) or assigned >= sample_size:
                continue
            key = bucket[cursor]
            cursors[source] = cursor + 1
            if quotas[key] < len(grouped[key]):
                quotas[key] += 1
                assigned += 1
                progress = True
        if not progress:
            break
    return quotas


def stratified_sample(
    records: list[dict[str, str]],
    sample_size: int,
    seed: int,
) -> list[dict[str, str]]:
    """Deterministic sample across year and source strata."""
    if sample_size < 1:
        raise ValueError("Calibration sample size must be at least 1.")
    population = [row for row in records if row.get("record_id")]
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in population:
        grouped[_stratum(row)].append(row)
    generator = random.Random(seed)
    for key in sorted(grouped):
        grouped[key].sort(key=lambda row: row["record_id"])
        generator.shuffle(grouped[key])
    keys = sorted(grouped)
    if len(population) <= sample_size:
        selected = list(population)
    else:
        quotas = _allocate_quotas(grouped, sample_size)
        selected = []
        for key in keys:
            selected.extend(grouped[key][: quotas[key]])
        if len(selected) < min(sample_size, len(population)):
            chosen = {row["record_id"] for row in selected}
            leftover = [row for row in population if row["record_id"] not in chosen]
            leftover.sort(key=lambda row: row["record_id"])
            generator.shuffle(leftover)
            selected.extend(leftover[: sample_size - len(selected)])
    selected.sort(key=lambda row: (row.get("year", ""), row.get("source_database", ""), row["record_id"]))
    return selected


def _has_decisions(rows: list[dict[str, str]]) -> bool:
    return any((row.get("decision") or "").strip() for row in rows)


def _merge_reviewer_file(
    existing: list[dict[str, str]],
    sample_rows: list[dict[str, str]],
    reviewer: str,
) -> list[dict[str, str]]:
    """Append new sample ids. Never replace a row that is already present."""
    ordered: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in existing:
        record_id = row.get("record_id", "")
        if record_id and record_id not in seen:
            ordered.append(row)
            seen.add(record_id)
    for sample in sample_rows:
        record_id = sample["record_id"]
        if record_id in seen:
            continue
        ordered.append(
            {
                "record_id": record_id,
                "reviewer": reviewer,
                "decision": "",
                "exclusion_code": "",
                "notes": "",
                "screened_at": "",
                "criteria_version": "",
            }
        )
        seen.add(record_id)
    return ordered


def draw_calibration_sample(
    layout: ReviewLayout,
    *,
    sample_size: int = DEFAULT_CALIBRATION_N,
    seed: int = DEFAULT_CALIBRATION_SEED,
) -> dict[str, object]:
    records = read_csv(layout.normalized)
    selected = stratified_sample(records, sample_size, seed)
    sample_rows: list[dict[str, str]] = []
    strata: dict[str, int] = defaultdict(int)
    for order, row in enumerate(selected, start=1):
        year, source = _stratum(row)
        label = f"{year}|{source}"
        strata[label] += 1
        sample_rows.append(
            {
                "record_id": row["record_id"],
                "year": row.get("year", ""),
                "source_database": row.get("source_database", ""),
                "stratum": label,
                "sample_order": str(order),
                "random_seed": str(seed),
                "sample_size": str(len(selected)),
                "sampling_method": SAMPLING_METHOD,
            }
        )
    write_csv(layout.calibration_sample, sample_rows, CALIBRATION_SAMPLE_FIELDS, layout.root)
    meta = {
        "random_seed": seed,
        "requested_n": sample_size,
        "drawn_n": len(selected),
        "population_n": len([row for row in records if row.get("record_id")]),
        "sampling_method": SAMPLING_METHOD,
        "strata": dict(sorted(strata.items())),
        "note": (
            "The sample is not the first N rows of the bibliographic table. "
            "Reviewer files are left untouched when they already contain decisions."
        ),
    }
    layout.calibration_meta.parent.mkdir(parents=True, exist_ok=True)
    layout.calibration_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    for path, reviewer in (
        (layout.reviewer_1, "REVIEWER_1"),
        (layout.reviewer_2, "REVIEWER_2"),
    ):
        existing = read_csv(path)
        if _has_decisions(existing):
            merged = _merge_reviewer_file(existing, sample_rows, reviewer)
            if len(merged) != len(existing):
                write_csv(path, merged, SCREENING_FIELDS, layout.root)
            continue
        if existing and not sample_rows:
            continue
        existing_ids = {row.get("record_id", "") for row in existing}
        sample_ids = {row["record_id"] for row in sample_rows}
        if existing and existing_ids == sample_ids:
            continue
        notes_by_id = {row.get("record_id", ""): row for row in existing}
        rebuilt: list[dict[str, str]] = []
        for sample in sample_rows:
            prior = notes_by_id.get(sample["record_id"])
            if prior is not None:
                rebuilt.append(prior)
            else:
                rebuilt.append(
                    {
                        "record_id": sample["record_id"],
                        "reviewer": reviewer,
                        "decision": "",
                        "exclusion_code": "",
                        "notes": "",
                        "screened_at": "",
                        "criteria_version": "",
                    }
                )
        write_csv(path, rebuilt, SCREENING_FIELDS, layout.root)
    consensus = layout.calibration_consensus
    if not consensus.exists():
        write_csv(consensus, [], SCREENING_FIELDS, layout.root)
    return meta
