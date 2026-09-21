"""LOINC FHIR Terminology Service client.

Official base URL: https://fhir.loinc.org
HTTP Basic authentication uses LOINC_USERNAME and LOINC_PASSWORD.
If either is missing, SourceNotConfigured is raised. There is no generated fallback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from app.config import Settings, get_settings
from app.sources.exceptions import SourceNotConfigured, SourceParseError
from app.sources.http import as_list, get_json, new_client

LOINC_FHIR_BASE_URL = "https://fhir.loinc.org"
LOINC_SYSTEM = "http://loinc.org"
LOINC_VALUESET_URL = "http://loinc.org/vs"
SOURCE_CODE = "LOINC"

_LOOKUP_PROPERTY_MAP = {
    "COMPONENT": "component",
    "PROPERTY": "property_code",
    "TIME_ASPCT": "time_aspect",
    "SYSTEM": "system_specimen",
    "SCALE_TYP": "scale",
    "METHOD_TYP": "method",
    "CLASS": "class_name",
    "SHORTNAME": "short_name",
    "SHORT_NAME": "short_name",
    "LONG_COMMON_NAME": "long_common_name",
    "STATUS": "status",
    "EXAMPLE_UCUM_UNITS": "example_ucum_units",
}


@dataclass
class LoincConcept:
    loinc_code: str
    long_common_name: str | None = None
    short_name: str | None = None
    component: str | None = None
    property_code: str | None = None
    time_aspect: str | None = None
    system_specimen: str | None = None
    scale: str | None = None
    method: str | None = None
    class_name: str | None = None
    status: str | None = None
    example_ucum_units: list[str] | None = None
    version: str | None = None
    extra: dict[str, str] = field(default_factory=dict)


class LoincClient:
    """Lookup and search LOINC terms. Requires a Regenstrief LOINC account."""

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        client: httpx.Client | None = None,
        transport: httpx.BaseTransport | None = None,
        settings: Settings | None = None,
        base_url: str = LOINC_FHIR_BASE_URL,
    ) -> None:
        user, secret = _require_credentials(username, password, settings)
        self._owns_client = client is None
        self._client = client or new_client(
            base_url=base_url,
            headers={"Accept": "application/fhir+json"},
            auth=(user, secret),
            transport=transport,
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> LoincClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def lookup_by_code(self, code: str) -> LoincConcept | None:
        loinc_code = code.strip()
        if loinc_code == "":
            raise ValueError("LOINC code is required")
        payload = get_json(
            self._client,
            "CodeSystem/$lookup",
            source_code=SOURCE_CODE,
            params={"system": LOINC_SYSTEM, "code": loinc_code},
            allow_404=True,
        )
        if payload is None:
            return None
        return _concept_from_lookup(loinc_code, payload)

    def search_by_name(self, query: str, *, count: int = 20) -> list[LoincConcept]:
        """Search via ValueSet $expand with a required text filter. No unfiltered dump."""
        text = query.strip()
        if text == "":
            raise ValueError(
                "LOINC search requires a query; full LOINC import is not run by default"
            )
        if count < 1:
            raise ValueError("count must be a positive integer")
        payload = get_json(
            self._client,
            "ValueSet/$expand",
            source_code=SOURCE_CODE,
            params={
                "url": LOINC_VALUESET_URL,
                "filter": text,
                "count": str(count),
            },
        )
        expansion = payload.get("expansion", {})
        concepts: list[LoincConcept] = []
        for item in as_list(expansion.get("contains")):
            if not isinstance(item, dict):
                continue
            system = str(item.get("system") or LOINC_SYSTEM)
            if system.rstrip("/") != LOINC_SYSTEM:
                continue
            code = _optional_str(item.get("code"))
            if code is None:
                continue
            concepts.append(
                LoincConcept(
                    loinc_code=code,
                    long_common_name=_optional_str(item.get("display")),
                    version=_optional_str(item.get("version"))
                    or _optional_str(expansion.get("version")),
                )
            )
        return concepts


def _require_credentials(
    username: str | None,
    password: str | None,
    settings: Settings | None,
) -> tuple[str, str]:
    cfg = settings or get_settings()
    user = (username if username is not None else cfg.loinc_username).strip()
    secret = (password if password is not None else cfg.loinc_password).strip()
    missing: list[str] = []
    if user == "":
        missing.append("LOINC_USERNAME")
    if secret == "":
        missing.append("LOINC_PASSWORD")
    if missing:
        raise SourceNotConfigured(SOURCE_CODE, missing)
    return user, secret


def _concept_from_lookup(loinc_code: str, payload: Any) -> LoincConcept:
    if not isinstance(payload, dict):
        raise SourceParseError("LOINC lookup payload was not an object")
    concept = LoincConcept(loinc_code=loinc_code)
    for parameter in as_list(payload.get("parameter")):
        if not isinstance(parameter, dict):
            continue
        name = parameter.get("name")
        if name == "display":
            concept.long_common_name = _parameter_value(parameter) or concept.long_common_name
        elif name == "version":
            concept.version = _parameter_value(parameter)
        elif name == "property":
            code, value = _property_pair(parameter)
            if code is None or value is None:
                continue
            field_name = _LOOKUP_PROPERTY_MAP.get(code)
            if field_name == "example_ucum_units":
                concept.example_ucum_units = _split_official_units(value)
            elif field_name is not None:
                setattr(concept, field_name, value)
            else:
                concept.extra[code] = value
    return concept


def _property_pair(parameter: dict[str, Any]) -> tuple[str | None, str | None]:
    code: str | None = None
    value: str | None = None
    for part in as_list(parameter.get("part")):
        if not isinstance(part, dict):
            continue
        part_name = part.get("name")
        if part_name == "code":
            code = _parameter_value(part)
        elif part_name in {"value", "valueString", "valueCode"}:
            value = _parameter_value(part)
    if value is None:
        value = _parameter_value(parameter)
    return code, value


def _parameter_value(parameter: dict[str, Any]) -> str | None:
    for key in ("valueString", "valueCode", "valueId", "valueUri"):
        if key in parameter:
            return _optional_str(parameter.get(key))
    if "valueBoolean" in parameter:
        return str(parameter["valueBoolean"]).lower()
    coding = parameter.get("valueCoding")
    if isinstance(coding, dict):
        return _optional_str(coding.get("code")) or _optional_str(coding.get("display"))
    return None


def _split_official_units(value: str) -> list[str]:
    """Split an official EXAMPLE_UCUM_UNITS string on semicolons. Tokens are not invented."""
    units = [part.strip() for part in value.split(";")]
    return [part for part in units if part != ""]


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text != "" else None
