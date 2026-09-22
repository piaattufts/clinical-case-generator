"""ICD-10-CM search against the NLM Clinical Table Search Service.

Official API: https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search
Codes and descriptions are stored exactly as returned. None are model-generated.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.sources.exceptions import SourceParseError
from app.sources.http import as_list, get_json, new_client

ICD10CM_SEARCH_URL = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
SOURCE_CODE = "ICD10CM"


@dataclass(frozen=True)
class Icd10CmConcept:
    icd10cm_code: str
    description: str


class Icd10CmClient:
    """Search ICD-10-CM codes and return the official code plus exact description."""

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        search_url: str = ICD10CM_SEARCH_URL,
    ) -> None:
        self.search_url = search_url
        self._owns_client = client is None
        self._client = client or new_client(transport=transport)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Icd10CmClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def search(self, query: str, *, count: int = 20, offset: int = 0) -> list[Icd10CmConcept]:
        text = query.strip()
        if text == "":
            raise ValueError(
                "ICD-10-CM search requires a query; full ICD-10-CM import is not run by default"
            )
        if count < 1:
            raise ValueError("count must be a positive integer")
        if offset < 0:
            raise ValueError("offset must be >= 0")
        payload = get_json(
            self._client,
            self.search_url,
            source_code=SOURCE_CODE,
            params={
                "terms": text,
                "sf": "code,name",
                "df": "code,name",
                "count": str(count),
                "offset": str(offset),
            },
        )
        return parse_icd10cm_search_payload(payload)

    def lookup_by_code(self, code: str) -> Icd10CmConcept | None:
        """Search for an exact official code string. Does not invent a description."""
        wanted = code.strip()
        if wanted == "":
            raise ValueError("ICD-10-CM code is required")
        matches = self.search(wanted, count=20, offset=0)
        for concept in matches:
            if concept.icd10cm_code.casefold() == wanted.casefold():
                return concept
        return None


def parse_icd10cm_search_payload(payload: Any) -> list[Icd10CmConcept]:
    if not isinstance(payload, list) or len(payload) < 4:
        raise SourceParseError("ICD-10-CM search payload was not the NLM Clinical Tables array")
    rows = as_list(payload[3])
    concepts: list[Icd10CmConcept] = []
    seen: set[str] = set()
    for row in rows:
        items = as_list(row)
        if len(items) < 2:
            continue
        code = _optional_str(items[0])
        description = items[1]
        if code is None or description is None:
            continue
        # Keep the description exactly as returned, including surrounding spaces.
        exact_description = str(description)
        if code in seen:
            continue
        seen.add(code)
        concepts.append(Icd10CmConcept(icd10cm_code=code, description=exact_description))
    return concepts


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text != "" else None
