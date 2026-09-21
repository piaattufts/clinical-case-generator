"""Build provenance values for authoritative reference rows."""

from __future__ import annotations

from datetime import UTC, datetime


def build_provenance(
    source_system: str,
    source_version: str | None = None,
    retrieved_at: datetime | None = None,
) -> dict[str, str | datetime | None]:
    """Return source_system, source_version, and a timezone-aware retrieved_at.

    Does not insert a row and does not invent a terminology version.
    """
    if source_system.strip() == "":
        raise ValueError("source_system is required")
    when = retrieved_at if retrieved_at is not None else datetime.now(UTC)
    if when.tzinfo is None or when.tzinfo.utcoffset(when) is None:
        raise ValueError("retrieved_at must be timezone-aware")
    return {
        "source_system": source_system.strip(),
        "source_version": source_version,
        "retrieved_at": when,
    }
