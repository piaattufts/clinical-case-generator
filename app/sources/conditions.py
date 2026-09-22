"""NLM Clinical Tables medical conditions.

Official API: https://clinicaltables.nlm.nih.gov/api/conditions/v3/search
ICD-10-CM codes are stored only when the source returns them on the icd10cm field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.sources.exceptions import SourceParseError
from app.sources.http import as_list, get_json, new_client

CONDITIONS_SEARCH_URL = "https://clinicaltables.nlm.nih.gov/api/conditions/v3/search"
SOURCE_CODE = "NLM_CONDITIONS"


@dataclass(frozen=True)
class ConditionConcept:
    name: str
    synonyms: list[str]
    icd10cm_codes: list[str]
    icd10cm_descriptions: dict[str, str]


class ConditionsClient:
    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        search_url: str = CONDITIONS_SEARCH_URL,
    ) -> None:
        self.search_url = search_url
        self._owns_client = client is None
        self._client = client or new_client(transport=transport)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def search(self, query: str, *, count: int = 20) -> list[ConditionConcept]:
        text = query.strip()
        if text == "":
            raise ValueError("Condition search requires a query")
        payload = get_json(
            self._client,
            self.search_url,
            source_code=SOURCE_CODE,
            params={
                "terms": text,
                "df": "primary_name,consumer_name",
                "ef": "primary_name,consumer_name,synonyms,icd10cm",
                "count": str(count),
            },
        )
        return parse_conditions_payload(payload)


def parse_conditions_payload(payload: Any) -> list[ConditionConcept]:
    if not isinstance(payload, list) or len(payload) < 4:
        raise SourceParseError("Conditions search payload was not the NLM Clinical Tables array")
    extra = payload[2] if isinstance(payload[2], dict) else {}
    names = [_optional_str(item) for item in as_list(extra.get("primary_name"))]
    if not any(names):
        names = []
        for row in as_list(payload[3]):
            items = as_list(row)
            names.append(_optional_str(items[0]) if items else None)
    synonyms_col = as_list(extra.get("synonyms"))
    icd_col = as_list(extra.get("icd10cm"))
    concepts: list[ConditionConcept] = []
    for index, name in enumerate(names):
        if not name:
            continue
        raw_syn = synonyms_col[index] if index < len(synonyms_col) else []
        synonyms = [s for s in (_optional_str(item) for item in as_list(raw_syn)) if s]
        codes: list[str] = []
        descriptions: dict[str, str] = {}
        raw_icd = icd_col[index] if index < len(icd_col) else []
        for entry in as_list(raw_icd):
            code: str | None = None
            description: str | None = None
            if isinstance(entry, dict):
                code = _optional_str(entry.get("code"))
                description = _optional_str(entry.get("name"))
            else:
                code = _optional_str(entry)
            if code is None or "?" in code:
                continue
            codes.append(code)
            if description is not None:
                descriptions[code] = description
        concepts.append(
            ConditionConcept(
                name=name,
                synonyms=synonyms,
                icd10cm_codes=codes,
                icd10cm_descriptions=descriptions,
            )
        )
    return concepts


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text != "" else None
