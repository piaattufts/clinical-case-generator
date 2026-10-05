"""Optional storage for machine suggestions.

This module does not call a model and does not read an API key.
Suggestions are stored apart from human screening decisions.
"""

from __future__ import annotations

import hashlib

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.normalize import utc_now_iso
from inthewild_review.schemas import AI_SUGGESTION_FIELDS


def record_suggestion(
    layout: ReviewLayout,
    *,
    suggestion_id: str,
    record_id: str,
    task: str,
    suggested_value: str,
    model_provider: str,
    model_name: str,
    model_version: str,
    prompt_id: str,
    prompt_text: str,
    notes: str = "",
) -> dict[str, str]:
    """Append one suggestion. Human screening files are not opened for writing."""
    if not model_provider or not model_name or not model_version or not prompt_id:
        raise ValueError(
            "AI suggestions require model_provider, model_name, model_version, and prompt_id."
        )
    row = {
        "suggestion_id": suggestion_id,
        "record_id": record_id,
        "task": task,
        "suggested_value": suggested_value,
        "model_provider": model_provider,
        "model_name": model_name,
        "model_version": model_version,
        "prompt_id": prompt_id,
        "prompt_sha256": hashlib.sha256(prompt_text.encode("utf-8")).hexdigest(),
        "created_at": utc_now_iso(),
        "human_verifier": "",
        "human_verified_at": "",
        "human_accepts": "",
        "notes": notes,
    }
    rows = read_csv(layout.ai_suggestions)
    if any(existing.get("suggestion_id") == suggestion_id for existing in rows):
        raise FileExistsError(f"Suggestion {suggestion_id} already exists and was not overwritten.")
    rows.append(row)
    write_csv(layout.ai_suggestions, rows, AI_SUGGESTION_FIELDS, layout.root)
    return row
