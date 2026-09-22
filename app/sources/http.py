"""Shared HTTP helpers for official terminology endpoints.

This module does not call OpenAI and does not transmit MIMIC or other patient rows.
"""

from __future__ import annotations

import time
from typing import Any

import httpx

from app import __version__
from app.sources.exceptions import SourceHttpError, SourceParseError, SourceUnavailable

USER_AGENT = f"clinical-case-generator/{__version__} (terminology-sync; no-patient-data)"
DEFAULT_TIMEOUT = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=10.0)
RETRY_STATUS = frozenset({429, 502, 503, 504})
TRANSIENT_MAX_RETRIES = 2


def new_client(
    *,
    base_url: str = "",
    headers: dict[str, str] | None = None,
    auth: httpx.Auth | tuple[str, str] | None = None,
    transport: httpx.BaseTransport | None = None,
    timeout: httpx.Timeout | float | None = None,
) -> httpx.Client:
    merged = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        merged.update(headers)
    return httpx.Client(
        base_url=base_url,
        headers=merged,
        auth=auth,
        transport=transport,
        timeout=DEFAULT_TIMEOUT if timeout is None else timeout,
        follow_redirects=True,
    )


def as_list(value: Any) -> list[Any]:
    """Normalize payloads that emit one object instead of a one-element array."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def request(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    source_code: str,
    params: dict[str, str] | None = None,
    retries: int = TRANSIENT_MAX_RETRIES,
) -> httpx.Response:
    last_error: Exception | None = None
    attempts = retries + 1
    for attempt in range(attempts):
        try:
            response = client.request(method, url, params=params)
        except httpx.TransportError as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(0.4 * (2**attempt))
                continue
            raise SourceUnavailable(source_code, url, str(exc)) from exc
        if response.status_code in RETRY_STATUS and attempt < retries:
            time.sleep(0.4 * (2**attempt))
            continue
        return response
    raise SourceUnavailable(source_code, url, str(last_error) if last_error else "retry exhausted")


def raise_for_status(source_code: str, response: httpx.Response) -> None:
    if response.status_code >= 400:
        detail = response.text[:500]
        raise SourceHttpError(source_code, response.status_code, str(response.request.url), detail)


def read_json(source_code: str, response: httpx.Response) -> Any:
    raise_for_status(source_code, response)
    try:
        return response.json()
    except ValueError as exc:
        raise SourceParseError(f"{source_code} response was not JSON") from exc


def read_text(source_code: str, response: httpx.Response) -> str:
    raise_for_status(source_code, response)
    return response.text


def get_json(
    client: httpx.Client,
    url: str,
    *,
    source_code: str,
    params: dict[str, str] | None = None,
    allow_404: bool = False,
) -> Any:
    response = request(client, "GET", url, source_code=source_code, params=params)
    if allow_404 and response.status_code == 404:
        return None
    return read_json(source_code, response)


def get_text(
    client: httpx.Client,
    url: str,
    *,
    source_code: str,
    params: dict[str, str] | None = None,
) -> str:
    response = request(client, "GET", url, source_code=source_code, params=params)
    return read_text(source_code, response)


SOURCE_BASE_URLS: dict[str, str] = {
    "RXNORM": "https://rxnav.nlm.nih.gov/REST",
    "LOINC": "https://fhir.loinc.org",
    "UCUM": "https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml",
    "ICD10CM": "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search",
    "DAILYMED": "https://dailymed.nlm.nih.gov/dailymed/services/v2",
    "NLM_CONDITIONS": "https://clinicaltables.nlm.nih.gov/api/conditions/v3/search",
    "NLM_HPO": "https://clinicaltables.nlm.nih.gov/api/hpo/v3/search",
    "RXCLASS": "https://rxnav.nlm.nih.gov/REST/rxclass",
}
