"""Errors from terminology sources and generation. No generated clinical fallbacks."""

from __future__ import annotations

from collections.abc import Sequence


class SourceError(Exception):
    """Base error for terminology source access."""


class SourceNotConfigured(SourceError):
    """Raised when required credentials are missing. No generated fallback is used."""

    def __init__(self, source_code: str, missing_env: Sequence[str]) -> None:
        self.source_code = source_code
        self.missing_env = list(missing_env)
        missing = ", ".join(self.missing_env) if self.missing_env else "required credentials"
        super().__init__(
            f"{source_code} is not configured. Missing {missing}. No generated fallback is used."
        )


class SourceUnavailable(SourceError):
    """Raised for transport failures or transient upstream outages."""

    def __init__(self, source_code: str, url: str, detail: str = "") -> None:
        self.source_code = source_code
        self.url = url
        self.detail = detail
        message = f"{source_code} is unavailable for {url}"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


class SourceHttpError(SourceError):
    """Raised when an official source returns a non-success HTTP status."""

    def __init__(self, source_code: str, status_code: int, url: str, detail: str = "") -> None:
        self.source_code = source_code
        self.status_code = status_code
        self.url = url
        self.detail = detail
        message = f"{source_code} request failed with HTTP {status_code} for {url}"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


class SourceParseError(SourceError):
    """Raised when an official source payload cannot be parsed. Values are not invented."""


class SourceResponseInvalid(SourceParseError):
    """Raised when JSON/XML is well-formed but missing required official fields."""


class ReferenceResolutionError(Exception):
    """Raised when a requested concept cannot be resolved to a source identifier."""

    def __init__(self, kind: str, request: str, detail: str = "") -> None:
        self.kind = kind
        self.request = request
        self.detail = detail
        message = f"Could not resolve {kind} request {request!r} from an authoritative source"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


class CaseValidationError(Exception):
    """Raised when a synthetic case fails a deterministic validation layer."""

    def __init__(self, layer: str, message: str, details: list[str] | None = None) -> None:
        self.layer = layer
        self.details = details or []
        super().__init__(f"{layer} validation failed: {message}")


class FrozenValidationCaseError(Exception):
    """Raised when a frozen VAL-* assignment would be silently overwritten."""

    def __init__(self, validation_case_id: str, detail: str = "") -> None:
        self.validation_case_id = validation_case_id
        message = f"Frozen validation case {validation_case_id} cannot be overwritten"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)
