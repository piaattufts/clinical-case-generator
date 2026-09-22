"""RxClass lookup for source-backed pharmacologic classes.

Official API: https://rxnav.nlm.nih.gov/REST/rxclass
Classes are copied from RxNav. They are not inferred from drug-name similarity.
"""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.sources.http import as_list, get_json, new_client

RXCLASS_BASE_URL = "https://rxnav.nlm.nih.gov/REST/rxclass"
SOURCE_CODE = "RXCLASS"


@dataclass(frozen=True)
class RxClassHit:
    rxcui: str
    class_id: str
    class_name: str
    class_type: str | None
    rela: str | None


class RxClassClient:
    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        base_url: str = RXCLASS_BASE_URL,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._owns_client = client is None
        self._client = client or new_client(transport=transport)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def classes_for_rxcui(self, rxcui: str) -> list[RxClassHit]:
        code = rxcui.strip()
        if code == "":
            raise ValueError("RXCUI is required")
        payload = get_json(
            self._client,
            f"{self.base_url}/class/byRxcui.json",
            source_code=SOURCE_CODE,
            params={"rxcui": code},
            allow_404=True,
        )
        if not isinstance(payload, dict):
            return []
        hits: list[RxClassHit] = []
        group = payload.get("rxclassDrugInfoList", {})
        for item in as_list(group.get("rxclassDrugInfo")):
            if not isinstance(item, dict):
                continue
            concept = item.get("rxclassMinConceptItem") or {}
            min_concept = item.get("minConcept") or {}
            class_id = str(concept.get("classId") or "").strip()
            class_name = str(concept.get("className") or "").strip()
            if class_id == "" or class_name == "":
                continue
            hits.append(
                RxClassHit(
                    rxcui=str(min_concept.get("rxcui") or code),
                    class_id=class_id,
                    class_name=class_name,
                    class_type=str(concept.get("classType") or "") or None,
                    rela=str(item.get("rela") or "") or None,
                )
            )
        return hits
