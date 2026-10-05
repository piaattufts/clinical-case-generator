"""Flag duplicate candidates. Nothing in this module merges or deletes records."""

from __future__ import annotations

from collections import defaultdict
from difflib import SequenceMatcher

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.normalize import normalize_title
from inthewild_review.schemas import DEFAULT_FUZZY_THRESHOLD, DUPLICATE_DECISIONS, DUPLICATE_FIELDS


def _group_id(prefix: str, key: str) -> str:
    import hashlib

    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _pair_key(left: str, right: str) -> tuple[str, str]:
    return (left, right) if left <= right else (right, left)


def _title_score(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def _fuzzy_blocked(left: str, right: str) -> bool:
    if not left or not right:
        return False
    if left[:12] and left[:12] == right[:12]:
        return True
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    if not left_tokens or not right_tokens:
        return False
    overlap = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)
    return union > 0 and (overlap / union) >= 0.5


def detect_duplicate_candidates(
    records: list[dict[str, str]],
    *,
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
    compare_all_fuzzy: bool | None = None,
) -> list[dict[str, str]]:
    """Return candidate pairs. Human decision fields are left blank."""
    usable = [row for row in records if row.get("record_id")]
    pairs: dict[tuple[str, str], dict[str, str]] = {}

    def ensure(left: dict[str, str], right: dict[str, str]) -> dict[str, str]:
        key = _pair_key(left["record_id"], right["record_id"])
        if key not in pairs:
            score = ""
            left_title = left.get("normalized_title") or normalize_title(left.get("title", ""))
            right_title = right.get("normalized_title") or normalize_title(right.get("title", ""))
            if left_title and right_title:
                score = f"{_title_score(left_title, right_title):.4f}"
            pairs[key] = {
                "duplicate_group_id": "",
                "record_id_1": key[0],
                "record_id_2": key[1],
                "match_type": "",
                "doi_match": "NO",
                "exact_title_match": "NO",
                "fuzzy_title_score": score,
                "recommended_review": "YES",
                "human_decision": "",
                "human_reason": "",
                "decision_by": "",
                "decision_date": "",
                "retained_record_id": "",
            }
        return pairs[key]

    doi_buckets: dict[str, list[dict[str, str]]] = defaultdict(list)
    title_buckets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in usable:
        doi = (row.get("doi_normalized") or "").strip()
        title = (row.get("normalized_title") or "").strip()
        if doi:
            doi_buckets[doi].append(row)
        if title:
            title_buckets[title].append(row)

    for doi, bucket in doi_buckets.items():
        ordered = sorted(bucket, key=lambda row: row["record_id"])
        group = _group_id("dupdoi", doi)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                pair = ensure(left, right)
                pair["doi_match"] = "YES"
                pair["duplicate_group_id"] = group

    for title, bucket in title_buckets.items():
        ordered = sorted(bucket, key=lambda row: row["record_id"])
        group = _group_id("duptitle", title)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                pair = ensure(left, right)
                pair["exact_title_match"] = "YES"
                if not pair["duplicate_group_id"] or pair["doi_match"] != "YES":
                    if pair["doi_match"] != "YES":
                        pair["duplicate_group_id"] = group

    for pair in pairs.values():
        if pair["doi_match"] == "YES" and pair["exact_title_match"] == "YES":
            pair["match_type"] = "EXACT_DOI_AND_TITLE"
        elif pair["doi_match"] == "YES":
            pair["match_type"] = "EXACT_DOI"
        else:
            pair["match_type"] = "EXACT_TITLE"

    ordered_records = sorted(usable, key=lambda row: row["record_id"])
    use_all = compare_all_fuzzy if compare_all_fuzzy is not None else len(ordered_records) <= 400
    for index, left in enumerate(ordered_records):
        left_title = (left.get("normalized_title") or "").strip()
        if not left_title:
            continue
        for right in ordered_records[index + 1 :]:
            key = _pair_key(left["record_id"], right["record_id"])
            if key in pairs and pairs[key]["exact_title_match"] == "YES":
                continue
            right_title = (right.get("normalized_title") or "").strip()
            if not right_title:
                continue
            if not use_all and not _fuzzy_blocked(left_title, right_title):
                continue
            score = _title_score(left_title, right_title)
            if score < fuzzy_threshold or left_title == right_title:
                continue
            pair = ensure(left, right)
            pair["fuzzy_title_score"] = f"{score:.4f}"
            if pair["doi_match"] != "YES":
                pair["match_type"] = "FUZZY_TITLE"
                pair["duplicate_group_id"] = _group_id("dupfuzzy", key[0] + "|" + key[1])
            elif not pair["match_type"]:
                pair["match_type"] = "EXACT_DOI"

    emitted = [pairs[key] for key in sorted(pairs)]
    for row in emitted:
        if row["human_decision"] and row["human_decision"] not in DUPLICATE_DECISIONS:
            raise ValueError(f"Unexpected human decision {row['human_decision']!r}")
    return emitted


def _preserve_human_fields(
    detected: list[dict[str, str]],
    previous: list[dict[str, str]],
) -> list[dict[str, str]]:
    saved: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in previous:
        key = (row.get("record_id_1", ""), row.get("record_id_2", ""), row.get("match_type", ""))
        saved[key] = row
    for row in detected:
        key = (row["record_id_1"], row["record_id_2"], row["match_type"])
        prior = saved.get(key)
        if prior is None:
            continue
        for field in (
            "human_decision",
            "human_reason",
            "decision_by",
            "decision_date",
            "retained_record_id",
        ):
            if prior.get(field):
                row[field] = prior[field]
    return detected


def write_duplicate_candidates(
    layout: ReviewLayout,
    *,
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
) -> list[dict[str, str]]:
    records = read_csv(layout.normalized)
    detected = detect_duplicate_candidates(records, fuzzy_threshold=fuzzy_threshold)
    previous = read_csv(layout.duplicates)
    merged = _preserve_human_fields(detected, previous)
    write_csv(layout.duplicates, merged, DUPLICATE_FIELDS, layout.root)
    return merged
