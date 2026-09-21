"""JSON helpers for JSONB values and files. Phase 1 has no export pipeline."""

from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID


def dumps_json(payload: object) -> str:
    """Serialize payload. Timezone-aware datetimes, dates, UUIDs, and Decimals are encoded."""
    return json.dumps(payload, default=_encode, ensure_ascii=False, separators=(",", ":"))


def loads_json(payload: str) -> Any:
    """Parse a JSON document."""
    return json.loads(payload)


def _encode(value: object) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("datetime values must be timezone-aware")
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return format(value, "f")
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")
