"""Optional OpenAI narrative assembly from already selected structured facts.

The model does not choose diagnoses, medications, labs, units, or errors.
Missing credentials skip OpenAI and return None so a template can be used.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.config import get_settings


class CaseNarrative(BaseModel):
    chief_complaint: str = Field(min_length=1)
    hpi: str = Field(min_length=1)
    note_text: str = Field(min_length=1)


def assemble_narrative(facts: dict[str, Any]) -> CaseNarrative | None:
    """Ask OpenAI to word the presentation from structured facts only.

    Returns None when OPENAI_API_KEY is unset or the request fails. Raw MIMIC and
    other patient-source rows are never sent.
    """
    settings = get_settings()
    api_key = settings.openai_api_key.strip()
    if api_key == "":
        return None
    try:
        from openai import OpenAI
    except Exception:
        return None
    payload = {
        "age": facts.get("age"),
        "sex": facts.get("sex"),
        "diagnosis": facts.get("diagnosis"),
        "symptoms": facts.get("symptoms"),
        "medications": facts.get("medications"),
        "chief_complaint_seed": facts.get("chief_complaint"),
    }
    instructions = (
        "Write admission narrative text from the provided structured facts only. "
        "Do not add diagnoses, medications, laboratory tests, units, doses, "
        "frequencies, procedures, devices, or identifiers that are not listed. "
        "Do not invent clinical reference ranges or medication-label facts."
    )
    try:
        client: Any = OpenAI(api_key=api_key)
        parsed = client.responses.parse(
            model=settings.openai_model,
            store=False,
            input=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": str(payload)},
            ],
            text_format=CaseNarrative,
        )
        narrative = parsed.output_parsed
        if not isinstance(narrative, CaseNarrative):
            return None
        return narrative
    except Exception:
        return None
