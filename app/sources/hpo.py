"""NLM Clinical Tables Human Phenotype Ontology search.

Official API: https://clinicaltables.nlm.nih.gov/api/hpo/v3/search
HPO identifiers are stored only when returned by the source. They are not SNOMED codes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.sources.exceptions import SourceParseError
from app.sources.http import as_list, get_json, new_client

HPO_SEARCH_URL = "https://clinicaltables.nlm.nih.gov/api/hpo/v3/search"
SOURCE_CODE = "NLM_HPO"


@dataclass(frozen=True)
class HpoConcept:
    hpo_id: str
    name: str
    synonyms: list[str]


class HpoClient:
    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        search_url: str = HPO_SEARCH_URL,
    ) -> None:
        self.search_url = search_url
        self._owns_client = client is None
        self._client = client or new_client(transport=transport)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def search(self, query: str, *, count: int = 20) -> list[HpoConcept]:
        text = query.strip()
        if text == "":
            raise ValueError("HPO search requires a query")
        payload = get_json(
            self._client,
            self.search_url,
            source_code=SOURCE_CODE,
            params={
                "terms": text,
                "ef": "id,name,synonyms",
                "maxList": str(count),
            },
        )
        return parse_hpo_payload(payload)


def parse_hpo_payload(payload: Any) -> list[HpoConcept]:
    if not isinstance(payload, list) or len(payload) < 3:
        raise SourceParseError("HPO search payload was not the NLM Clinical Tables array")
    extra = payload[2] if isinstance(payload[2], dict) else {}
    identifiers = [_optional_str(item) for item in as_list(extra.get("id"))]
    names = [_optional_str(item) for item in as_list(extra.get("name"))]
    synonyms_col = as_list(extra.get("synonyms"))
    concepts: list[HpoConcept] = []
    for index, hpo_id in enumerate(identifiers):
        if hpo_id is None or not hpo_id.startswith("HP:"):
            continue
        name = names[index] if index < len(names) else None
        if not name:
            continue
        raw_syn = synonyms_col[index] if index < len(synonyms_col) else []
        synonyms = [item for item in (_optional_str(value) for value in as_list(raw_syn)) if item]
        concepts.append(HpoConcept(hpo_id=hpo_id, name=name, synonyms=synonyms))
    return concepts


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text != "" else None
