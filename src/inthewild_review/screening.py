"""Title/abstract and full-text screening rules.

MAYBE is a real decision. It is not rewritten to INCLUDE or EXCLUDE.
"""

from __future__ import annotations

from inthewild_review.schemas import (
    EXCLUSION_CODES,
    FULL_TEXT_CRITERION_FIELDS,
    FULL_TEXT_EXCLUSION_REASONS,
    FULL_TEXT_REASON_TO_FIELD,
    FULL_TEXT_RESPONSES,
    SCREENING_DECISIONS,
)


class ScreeningValidationError(ValueError):
    """A screening row breaks a protocol rule."""


def validate_title_abstract_row(row: dict[str, str]) -> None:
    decision = (row.get("decision") or "").strip()
    code = (row.get("exclusion_code") or "").strip()
    if decision == "":
        if code:
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} has an exclusion code without a decision."
            )
        return
    if decision not in SCREENING_DECISIONS:
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} has invalid decision {decision!r}. "
            f"Allowed decisions are {', '.join(SCREENING_DECISIONS)}."
        )
    if decision in {"INCLUDE", "MAYBE"}:
        if code:
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} is {decision} and must not have an "
                "exclusion code."
            )
        return
    if not code:
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} is EXCLUDE and needs exactly one exclusion code."
        )
    if code not in EXCLUSION_CODES:
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} has invalid exclusion code {code!r}."
        )
    if any(separator in code for separator in ("|", ";", ",")):
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} has more than one exclusion code."
        )


def validate_title_abstract_rows(rows: list[dict[str, str]]) -> None:
    for row in rows:
        validate_title_abstract_row(row)


def validate_full_text_row(row: dict[str, str]) -> None:
    decision = (row.get("decision") or "").strip()
    reason = (row.get("exclusion_reason") or "").strip()
    availability = (row.get("full_text_available") or "").strip()
    if availability and availability not in FULL_TEXT_RESPONSES:
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} has invalid full_text_available {availability!r}."
        )
    for field in FULL_TEXT_CRITERION_FIELDS:
        value = (row.get(field) or "").strip()
        if value and value not in FULL_TEXT_RESPONSES:
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} field {field} has invalid value {value!r}. "
                "Use YES, NO, or UNCLEAR."
            )
    if decision == "":
        if reason:
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} has an exclusion reason without a decision."
            )
        return
    if decision not in SCREENING_DECISIONS:
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} has invalid full-text decision {decision!r}."
        )
    if decision in {"INCLUDE", "MAYBE"} and reason:
        raise ScreeningValidationError(
            f"Record {row.get('record_id', '')} is {decision} and must not have an exclusion reason."
        )
    if decision == "EXCLUDE":
        if reason not in FULL_TEXT_EXCLUSION_REASONS:
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} has invalid full-text exclusion reason {reason!r}."
            )
        field = FULL_TEXT_REASON_TO_FIELD[reason]
        if (row.get(field) or "").strip() != "NO":
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} is excluded as {reason}, but {field} is not NO. "
                "Missing evidence must stay UNCLEAR and must not be recoded as NO."
            )
        return
    if decision == "INCLUDE":
        if availability != "YES":
            raise ScreeningValidationError(
                f"Record {row.get('record_id', '')} cannot be INCLUDE unless full_text_available is YES."
            )
        for field in FULL_TEXT_CRITERION_FIELDS:
            if (row.get(field) or "").strip() != "YES":
                raise ScreeningValidationError(
                    f"Record {row.get('record_id', '')} cannot be INCLUDE while {field} is "
                    f"{(row.get(field) or '').strip() or 'blank'!r}. "
                    "Do not infer a YES from missing text."
                )


def queue_full_text_rows(
    screened: list[dict[str, str]],
    existing: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Add INCLUDE and MAYBE records to full-text screening without touching existing rows.

    EXCLUDE records are not queued. This routing is recorded as a provisional
    operational rule because the protocol file was not available to confirm it.
    """
    validate_title_abstract_rows([row for row in screened if row.get("decision")])
    by_id = {row.get("record_id", ""): row for row in existing if row.get("record_id")}
    ordered_ids: list[str] = []
    for row in screened:
        decision = (row.get("decision") or "").strip()
        record_id = row.get("record_id", "")
        if decision in {"INCLUDE", "MAYBE"} and record_id and record_id not in ordered_ids:
            ordered_ids.append(record_id)
    for record_id in ordered_ids:
        if record_id not in by_id:
            by_id[record_id] = {
                "record_id": record_id,
                "full_text_available": "",
                "physically_embodied_robot": "",
                "substantive_social_interaction": "",
                "human_participants": "",
                "naturalistic_or_repeated_longterm": "",
                "identifiable_interaction_situation": "",
                "setting_extractable": "",
                "duration_extractable": "",
                "interaction_structure_extractable": "",
                "decision": "",
                "exclusion_reason": "",
                "reviewer": "",
                "notes": "",
                "screened_at": "",
            }
    queued_ids = set(ordered_ids)
    retained = [row for row in existing if row.get("record_id") in queued_ids or row.get("decision")]
    known = {row.get("record_id", "") for row in retained}
    for record_id in ordered_ids:
        if record_id not in known:
            retained.append(by_id[record_id])
    return retained


def adjudicated_title_abstract(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """One row per record from the main screening sheet.

    Rows marked CONSENSUS or ADJUDICATED win. Otherwise all completed decisions
    for a record must agree. Disagreement is an error, not a silent choice.
    """
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        record_id = row.get("record_id", "")
        if not record_id or not (row.get("decision") or "").strip():
            continue
        validate_title_abstract_row(row)
        grouped.setdefault(record_id, []).append(row)
    chosen: list[dict[str, str]] = []
    for record_id in sorted(grouped):
        group = grouped[record_id]
        preferred = [
            row
            for row in group
            if (row.get("reviewer") or "").strip().upper() in {"CONSENSUS", "ADJUDICATED"}
        ]
        pool = preferred or group
        decisions = {(row.get("decision") or "").strip() for row in pool}
        codes = {(row.get("exclusion_code") or "").strip() for row in pool}
        if len(decisions) != 1 or len(codes) != 1:
            raise ScreeningValidationError(
                f"Title/abstract rows for {record_id} disagree. "
                "PRISMA counts will not choose a decision automatically."
            )
        chosen.append(pool[-1])
    return chosen
