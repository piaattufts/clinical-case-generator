"""NLM RxNav client. Identifiers come from RxNorm; none are generated here.

Official REST service: https://rxnav.nlm.nih.gov/REST
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.sources.http import as_list, get_json, new_client

RXNORM_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
SOURCE_CODE = "RXNORM"

# Official RxNorm term types used only to classify values returned by RxNav.
BRAND_TTY = frozenset({"BN", "SBD", "SBDC", "SBDF", "SBDG", "BPCK"})
PRESCRIBABLE_TTY = frozenset({"SCD", "SBD", "GPCK", "BPCK"})
RELATED_TTY = "IN PIN BN DF SCD SBD SCDC SBDC SCDG SBDG GPCK BPCK"


@dataclass(frozen=True)
class RxNormConcept:
    rxcui: str
    name: str | None
    synonym: str | None = None
    tty: str | None = None
    suppress: str | None = None


class RxNormClient:
    """Search by name, look up by RXCUI, read properties, and read related concepts."""

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        base_url: str = RXNORM_BASE_URL,
    ) -> None:
        self._owns_client = client is None
        self._client = client or new_client(base_url=base_url, transport=transport)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> RxNormClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def search_by_name(self, name: str) -> list[RxNormConcept]:
        """Return drug concepts for a name from RxNav getDrugs, then findRxcuiByString."""
        query = name.strip()
        if query == "":
            raise ValueError("RxNorm name search requires a non-empty name")
        concepts = self._parse_concept_groups(
            self._get("drugs.json", params={"name": query}).get("drugGroup", {}).get("conceptGroup")
        )
        if concepts:
            return _dedupe_concepts(concepts)
        payload = self._get("rxcui.json", params={"name": query, "search": "2"})
        identifiers = as_list(payload.get("idGroup", {}).get("rxnormId"))
        found: list[RxNormConcept] = []
        for raw_id in identifiers:
            rxcui = str(raw_id).strip()
            if rxcui == "":
                continue
            concept = self.lookup_by_rxcui(rxcui)
            if concept is not None:
                found.append(concept)
        return _dedupe_concepts(found)

    def lookup_by_rxcui(self, rxcui: str) -> RxNormConcept | None:
        """Return the active RxNorm concept for an RXCUI, or None if RxNav has no properties."""
        code = rxcui.strip()
        if code == "":
            raise ValueError("RXCUI is required")
        payload = self._get(f"rxcui/{code}/properties.json")
        properties = payload.get("properties")
        if not isinstance(properties, dict):
            return None
        parsed = _concept_from_properties(properties)
        if parsed is None or parsed.rxcui == "":
            return None
        return parsed

    def properties(self, rxcui: str) -> dict[str, str]:
        """Return official property name/value pairs from RxNav getAllProperties."""
        code = rxcui.strip()
        if code == "":
            raise ValueError("RXCUI is required")
        payload = self._get(f"rxcui/{code}/allProperties.json", params={"prop": "ALL"})
        pairs: dict[str, str] = {}
        group = payload.get("propConceptGroup", {})
        for item in as_list(group.get("propConcept")):
            if not isinstance(item, dict):
                continue
            name = _optional_str(item.get("propName"))
            value = _optional_str(item.get("propValue"))
            if name is None or value is None or name in pairs:
                continue
            pairs[name] = value
        return pairs

    def related_concepts(self, rxcui: str, tty: str | None = None) -> list[RxNormConcept]:
        """Return related RxNorm concepts from getRelatedByType or getAllRelatedInfo."""
        code = rxcui.strip()
        if code == "":
            raise ValueError("RXCUI is required")
        if tty is not None and tty.strip() != "":
            payload = self._get(f"rxcui/{code}/related.json", params={"tty": tty.strip()})
            groups = payload.get("relatedGroup", {}).get("conceptGroup")
        else:
            payload = self._get(f"rxcui/{code}/allrelated.json")
            groups = payload.get("allRelatedGroup", {}).get("conceptGroup")
            if groups is None:
                groups = payload.get("relatedGroup", {}).get("conceptGroup")
        return _dedupe_concepts(self._parse_concept_groups(groups))

    def version(self) -> str | None:
        """Return the RxNorm dataset version string published by RxNav, if present."""
        payload = self._get("version.json")
        return _optional_str(payload.get("version"))

    def _get(self, path: str, params: dict[str, str] | None = None) -> Any:
        payload = get_json(
            self._client, path, source_code=SOURCE_CODE, params=params, allow_404=True
        )
        return payload if isinstance(payload, dict) else {}

    def _parse_concept_groups(self, groups: Any) -> list[RxNormConcept]:
        concepts: list[RxNormConcept] = []
        for group in as_list(groups):
            if not isinstance(group, dict):
                continue
            for item in as_list(group.get("conceptProperties")):
                parsed = _concept_from_properties(item)
                if parsed is not None:
                    concepts.append(parsed)
        return concepts


def _concept_from_properties(item: Any) -> RxNormConcept | None:
    if not isinstance(item, dict):
        return None
    rxcui = _optional_str(item.get("rxcui"))
    if rxcui is None:
        return None
    return RxNormConcept(
        rxcui=rxcui,
        name=_optional_str(item.get("name")),
        synonym=_optional_str(item.get("synonym")),
        tty=_optional_str(item.get("tty")),
        suppress=_optional_str(item.get("suppress")),
    )


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text != "" else None


def _dedupe_concepts(concepts: list[RxNormConcept]) -> list[RxNormConcept]:
    seen: set[str] = set()
    unique: list[RxNormConcept] = []
    for concept in concepts:
        if concept.rxcui in seen:
            continue
        seen.add(concept.rxcui)
        unique.append(concept)
    return unique
