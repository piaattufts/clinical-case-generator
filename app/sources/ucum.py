"""UCUM import from the official essence XML. Conversion factors are never invented.

Official source: https://github.com/ucum-org/ucum (ucum-essence.xml, release v2.2)
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from xml.etree import ElementTree

import httpx

from app.sources.exceptions import SourceParseError
from app.sources.http import get_text, new_client

UCUM_ESSENCE_URL = "https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml"
UCUM_NAMESPACE = "http://unitsofmeasure.org/ucum-essence"
SOURCE_CODE = "UCUM"


@dataclass(frozen=True)
class UcumPrefix:
    code: str
    name: str | None
    factor: Decimal | None
    source_version: str | None


@dataclass(frozen=True)
class UcumUnit:
    ucum_code: str
    display_name: str | None
    quantity_type: str | None
    canonical_unit: str | None
    conversion_factor: Decimal | None
    active: bool
    source_version: str | None


class UcumClient:
    """Fetch and parse the official UCUM essence file. No local conversion table is invented."""

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        essence_url: str = UCUM_ESSENCE_URL,
    ) -> None:
        self.essence_url = essence_url
        self._owns_client = client is None
        self._client = client or new_client(
            headers={"Accept": "application/xml, text/xml, */*"},
            transport=transport,
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> UcumClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def fetch_essence_xml(self) -> str:
        return get_text(self._client, self.essence_url, source_code=SOURCE_CODE)

    def list_units(self, xml_text: str | None = None) -> list[UcumUnit]:
        payload = xml_text if xml_text is not None else self.fetch_essence_xml()
        return parse_essence_xml(payload)

    def search_units(self, query: str, xml_text: str | None = None) -> list[UcumUnit]:
        text = query.strip()
        if text == "":
            raise ValueError("UCUM search requires a query; full UCUM import is not run by default")
        payload = xml_text if xml_text is not None else self.fetch_essence_xml()
        needle = text.casefold()
        units = parse_essence_xml(payload)
        matched: list[UcumUnit] = []
        for unit in units:
            haystacks = [unit.ucum_code.casefold()]
            if unit.display_name is not None:
                haystacks.append(unit.display_name.casefold())
            if unit.quantity_type is not None:
                haystacks.append(unit.quantity_type.casefold())
            if any(needle in item for item in haystacks):
                matched.append(unit)
        if matched:
            return matched
        return compose_prefixed_units(text, units, parse_essence_prefixes(payload))


def parse_essence_xml(xml_text: str) -> list[UcumUnit]:
    """Parse official UCUM essence XML. conversion_factor is copied from value/@value only."""
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as exc:
        raise SourceParseError("UCUM essence XML could not be parsed") from exc
    source_version = _optional_str(root.attrib.get("version"))
    units: list[UcumUnit] = []
    for element in list(root):
        tag = _local_name(element.tag)
        if tag not in {"base-unit", "unit"}:
            continue
        parsed = _unit_from_element(element, source_version)
        if parsed is not None:
            units.append(parsed)
    return units


def _unit_from_element(element: ElementTree.Element, source_version: str | None) -> UcumUnit | None:
    code = _optional_str(element.attrib.get("Code"))
    if code is None:
        return None
    display_name = _child_text(element, "name")
    quantity_type = _child_text(element, "property")
    value_el = _child(element, "value")
    canonical_unit: str | None = None
    conversion_factor: Decimal | None = None
    if value_el is not None:
        canonical_unit = _optional_str(value_el.attrib.get("Unit"))
        raw_factor = _optional_str(value_el.attrib.get("value"))
        conversion_factor = _decimal_from_official_attribute(raw_factor)
    return UcumUnit(
        ucum_code=code,
        display_name=display_name,
        quantity_type=quantity_type,
        canonical_unit=canonical_unit,
        conversion_factor=conversion_factor,
        active=True,
        source_version=source_version,
    )


def parse_essence_prefixes(xml_text: str) -> list[UcumPrefix]:
    """Parse official UCUM prefix elements. Factors are copied from value/@value only."""
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as exc:
        raise SourceParseError("UCUM essence XML could not be parsed") from exc
    source_version = _optional_str(root.attrib.get("version"))
    prefixes: list[UcumPrefix] = []
    for element in list(root):
        if _local_name(element.tag) != "prefix":
            continue
        code = _optional_str(element.attrib.get("Code"))
        if code is None:
            continue
        value_el = _child(element, "value")
        raw_factor = _optional_str(value_el.attrib.get("value")) if value_el is not None else None
        prefixes.append(
            UcumPrefix(
                code=code,
                name=_child_text(element, "name"),
                factor=_decimal_from_official_attribute(raw_factor),
                source_version=source_version,
            )
        )
    return prefixes


def compose_prefixed_units(
    query: str, units: list[UcumUnit], prefixes: list[UcumPrefix]
) -> list[UcumUnit]:
    """Build a unit such as kg from official prefix kilo and official unit gram.

    Conversion factors are the product of official prefix and unit values. Missing
    official factors stay null; they are not invented.
    """
    needle = query.strip().casefold()
    if needle == "":
        return []
    composed: list[UcumUnit] = []
    seen: set[str] = set()
    for prefix in prefixes:
        prefix_name = (prefix.name or "").casefold()
        if prefix_name == "":
            continue
        for unit in units:
            unit_name = (unit.display_name or "").casefold()
            if unit_name == "":
                continue
            candidates = {prefix_name + unit_name, f"{prefix_name} {unit_name}"}
            if needle not in candidates:
                continue
            code = f"{prefix.code}{unit.ucum_code}"
            if code in seen:
                continue
            seen.add(code)
            factor: Decimal | None = None
            if prefix.factor is not None and unit.conversion_factor is not None:
                factor = prefix.factor * unit.conversion_factor
            composed.append(
                UcumUnit(
                    ucum_code=code,
                    display_name=f"{prefix.name}{unit.display_name}",
                    quantity_type=unit.quantity_type,
                    canonical_unit=unit.canonical_unit,
                    conversion_factor=factor,
                    active=unit.active,
                    source_version=unit.source_version or prefix.source_version,
                )
            )
    return composed


def _decimal_from_official_attribute(raw: str | None) -> Decimal | None:
    """Copy an official machine-readable factor. Unparsable attributes are stored as null."""
    if raw is None:
        return None
    try:
        return Decimal(raw)
    except InvalidOperation:
        return None


def _child(element: ElementTree.Element, local_name: str) -> ElementTree.Element | None:
    for child in list(element):
        if _local_name(child.tag) == local_name:
            return child
    return None


def _child_text(element: ElementTree.Element, local_name: str) -> str | None:
    child = _child(element, local_name)
    if child is None or child.text is None:
        return None
    return _optional_str(child.text)


def _local_name(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text != "" else None
