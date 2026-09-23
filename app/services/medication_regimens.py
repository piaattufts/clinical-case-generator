"""Curated clinical regimens, separate from RxNorm product identity.

Product strength is not copied into the administered dose. Frequency is taken
from the regimen entry, not from a once-daily default. Missing regimen data
raises for real medications. Test fixtures may still fall back so pipeline
tests can run without a fabricated clinical dose.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.models.reference import RefMedication
from app.sources.exceptions import ReferenceResolutionError

REGIMEN_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "bootstrap" / "medication_regimens.json"
)

COMPARATIVE_IMAGING = re.compile(
    r"\b(?:improv(?:ing|ed|ement)|compared with admission)\b",
    re.IGNORECASE,
)
ADMISSION_TIMEPOINTS = frozenset({"admission", "on admission", "initial", "presenting"})
ECHO_COURSE_STATEMENTS = re.compile(
    r"treatment course|treated endocarditis|under treatment|improving clinical stability|"
    r"clinically stable|awaiting confirmation|clinical course",
    re.IGNORECASE,
)
POSITIVE_MICRO = re.compile(
    r"\b(?:growth|positive|cocci|isolated|detected)\b",
    re.IGNORECASE,
)
NEGATIVE_MICRO = re.compile(
    r"\b(?:no growth|negative|cleared|culture-negative)\b",
    re.IGNORECASE,
)
@dataclass(frozen=True)
class ClinicalRegimen:
    id: str
    query: str
    dose: str
    route: str
    frequency: str
    temporal_role: str
    preferred_tokens: tuple[str, ...]
    avoid_tokens: tuple[str, ...]
    selection_priority: int
    chart_note: str | None
    citation: str
    citation_url: str
    match_all: tuple[str, ...] = ()
    match_none: tuple[str, ...] = ()
    profile_restrictions: str | None = None
    additional_citation: str | None = None
    additional_citation_url: str | None = None

    def matches_text(self, blob: str) -> bool:
        if self.query.casefold() not in blob:
            return False
        if self.match_all and not all(token.casefold() in blob for token in self.match_all):
            return False
        if self.match_none and any(token.casefold() in blob for token in self.match_none):
            return False
        return True


@dataclass(frozen=True)
class Administration:
    dose: str
    route: str
    frequency: str
    temporal_role: str
    chart_note: str | None
    regimen_id: str | None


def medication_blob(medication: RefMedication | Any) -> str:
    parts = [
        getattr(medication, "ingredient", None),
        getattr(medication, "generic_name", None),
        getattr(medication, "concept_name", None),
        getattr(medication, "dose_form", None),
    ]
    return " ".join(part for part in parts if part).casefold()


def is_test_medication(medication: RefMedication | Any) -> bool:
    rxcui = str(getattr(medication, "rxcui", "") or "")
    name = str(getattr(medication, "concept_name", "") or "")
    return rxcui.startswith("TEST_") or name.startswith("TEST_")


@lru_cache(maxsize=1)
def load_regimens(path: str | None = None) -> tuple[ClinicalRegimen, ...]:
    source = Path(path) if path else REGIMEN_PATH
    raw = source.read_text(encoding="utf-8")
    payload = json.loads(raw)
    rows = payload.get("regimens")
    if not isinstance(rows, list):
        raise ValueError("medication_regimens.json must contain a regimens list")
    loaded: list[ClinicalRegimen] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        loaded.append(
            ClinicalRegimen(
                id=str(row["id"]),
                query=str(row["query"]).casefold(),
                dose=str(row["dose"]),
                route=str(row["route"]),
                frequency=str(row["frequency"]),
                temporal_role=str(row.get("temporal_role") or "pre_existing_home"),
                preferred_tokens=tuple(str(item) for item in row.get("preferred_tokens") or []),
                avoid_tokens=tuple(str(item) for item in row.get("avoid_tokens") or []),
                selection_priority=int(row.get("selection_priority") or 0),
                chart_note=(
                    None if row.get("chart_note") in (None, "") else str(row.get("chart_note"))
                ),
                citation=str(row.get("citation") or ""),
                citation_url=str(row.get("citation_url") or ""),
                match_all=tuple(str(item).casefold() for item in row.get("match_all") or []),
                match_none=tuple(str(item).casefold() for item in row.get("match_none") or []),
                profile_restrictions=(
                    None
                    if row.get("profile_restrictions") in (None, "")
                    else str(row.get("profile_restrictions"))
                ),
                additional_citation=(
                    None
                    if row.get("additional_citation") in (None, "")
                    else str(row.get("additional_citation"))
                ),
                additional_citation_url=(
                    None
                    if row.get("additional_citation_url") in (None, "")
                    else str(row.get("additional_citation_url"))
                ),
            )
        )
    return tuple(loaded)


def matching_regimens(blob: str) -> list[ClinicalRegimen]:
    text = blob.casefold()
    hits = [item for item in load_regimens() if item.matches_text(text)]
    hits.sort(key=lambda item: (-len(item.query), item.selection_priority, item.id))
    return hits


def regimen_for_text(blob: str) -> ClinicalRegimen | None:
    hits = matching_regimens(blob)
    return hits[0] if hits else None


def regimen_for_medication(medication: RefMedication | Any) -> ClinicalRegimen | None:
    return regimen_for_text(medication_blob(medication))


def token_in(token: str, blob: str) -> bool:
    """Match a strength token without treating 5 MG as present inside 0.5 MG or 25 MG."""
    needle = re.escape(token.casefold())
    return re.search(rf"(?<![\d.]){needle}(?!\d)", blob.casefold()) is not None


def concept_preference_key(name: str | None) -> tuple[int, int, int, str]:
    """Rank an RxNorm display name so the stored concept agrees with the regimen."""
    blob = (name or "").casefold()
    regimen = regimen_for_text(blob)
    if regimen is None:
        return (3, 1, 9, blob)
    avoided = 1 if any(token_in(token, blob) for token in regimen.avoid_tokens) else 0
    preferred_hit = bool(regimen.preferred_tokens) and all(
        token_in(token, blob) for token in regimen.preferred_tokens
    )
    preferred = 0 if preferred_hit else 1
    return (avoided, preferred, regimen.selection_priority, blob)


def temporal_role_for(
    medication: RefMedication | Any,
    overrides: dict[str, str] | None = None,
) -> str:
    blob = medication_blob(medication)
    for key, role in (overrides or {}).items():
        if key.casefold() in blob:
            return role
    regimen = regimen_for_medication(medication)
    if regimen is not None:
        return regimen.temporal_role
    return "pre_existing_home"


def administration_for(
    medication: RefMedication | Any,
    *,
    fallback_frequency: str,
    overrides: dict[str, str] | None = None,
) -> Administration:
    from app.services.clinical_coherence import inferred_route, synthetic_dose_for

    regimen = regimen_for_medication(medication)
    role = temporal_role_for(medication, overrides)
    if regimen is not None:
        return Administration(
            dose=regimen.dose,
            route=regimen.route,
            frequency=regimen.frequency,
            temporal_role=role,
            chart_note=regimen.chart_note,
            regimen_id=regimen.id,
        )
    if is_test_medication(medication):
        return Administration(
            dose=synthetic_dose_for(medication),
            route=inferred_route(medication),
            frequency=fallback_frequency,
            temporal_role=role,
            chart_note=None,
            regimen_id=None,
        )
    label = getattr(medication, "concept_name", None) or getattr(medication, "rxcui", "")
    raise ReferenceResolutionError(
        "medication_regimen",
        str(label),
        "no curated clinical regimen; product strength is not used as the administered dose",
    )


def normalize_admin_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").casefold()).strip()


def regimen_field_conflicts(
    medication: RefMedication | Any,
    *,
    dose: str | None,
    route: str | None,
    frequency: str | None,
) -> list[str]:
    regimen = regimen_for_medication(medication)
    if regimen is None:
        return []
    errors: list[str] = []
    label = getattr(medication, "concept_name", None) or regimen.query
    if dose is not None and normalize_admin_text(dose) != normalize_admin_text(regimen.dose):
        errors.append(
            f"dose {dose!r} for {label} does not match curated regimen {regimen.dose!r} "
            f"({regimen.id})"
        )
    if route is not None and normalize_admin_text(route) != normalize_admin_text(regimen.route):
        errors.append(
            f"route {route!r} for {label} does not match curated regimen {regimen.route!r}"
        )
    if frequency is not None and normalize_admin_text(frequency) != normalize_admin_text(
        regimen.frequency
    ):
        errors.append(
            f"frequency {frequency!r} for {label} does not match curated regimen "
            f"{regimen.frequency!r}"
        )
    return errors


def beta_blocker_frequency_conflicts(concept_name: str | None, frequency: str | None) -> list[str]:
    blob = (concept_name or "").casefold()
    freq = normalize_admin_text(frequency)
    if "metoprolol" not in blob and "carvedilol" not in blob:
        return []
    errors: list[str] = []
    if "metoprolol" in blob and "tartrate" in blob and "succinate" not in blob:
        if "twice" not in freq and "every 12" not in freq:
            errors.append("metoprolol tartrate is charted without a twice-daily frequency")
    if "metoprolol" in blob and (
        "succinate" in blob or "extended release" in blob or "24 hr" in blob or "24hr" in blob
    ):
        if "twice" in freq or "every 12" in freq:
            errors.append(
                "metoprolol succinate extended release is charted more often than once daily"
            )
        if "once" not in freq and "daily" not in freq:
            errors.append("metoprolol succinate is missing a once-daily frequency")
    if "carvedilol" in blob and "phosphate" not in blob and "extended" not in blob:
        if "twice" not in freq and "every 12" not in freq:
            errors.append("immediate-release carvedilol is charted without a twice-daily frequency")
    return errors


def imaging_timepoint_conflict(timepoint: str | None, finding: str | None) -> str | None:
    text = finding or ""
    if not COMPARATIVE_IMAGING.search(text):
        return None
    marker = (timepoint or "").casefold().strip()
    if marker in ADMISSION_TIMEPOINTS or marker.startswith("admission"):
        return (
            f"imaging timepoint {timepoint!r} uses comparative wording that requires "
            f"a later study: {text}"
        )
    return None


def echo_course_statement(finding: str | None) -> bool:
    return bool(finding and ECHO_COURSE_STATEMENTS.search(finding))


def endocarditis_microbiology_conflicts(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["endocarditis case has no microbiology chronology"]
    positives: list[str] = []
    later_negatives: list[str] = []
    for row in rows:
        blob = " ".join(
            part
            for part in (
                row.get("result"),
                row.get("organism"),
                row.get("status"),
                row.get("notes"),
            )
            if part
        )
        timepoint = (row.get("timepoint") or "").casefold()
        is_negative = bool(NEGATIVE_MICRO.search(blob))
        if POSITIVE_MICRO.search(blob) and not is_negative:
            positives.append(timepoint or "unspecified")
        if is_negative and timepoint not in ADMISSION_TIMEPOINTS:
            later_negatives.append(timepoint or "unspecified")
    errors: list[str] = []
    if not positives:
        errors.append("endocarditis microbiology has no initial positive culture evidence")
    if not later_negatives:
        errors.append(
            "endocarditis microbiology has no culture clearance after the initial culture"
        )
    return errors


def living_disposition_conflict(living: str | None, disposition: str | None) -> str | None:
    destination = (disposition or "").casefold()
    text = (living or "").casefold()
    leaves_home = any(
        token in destination
        for token in ("rehab", "rehabilitation", "skilled nursing", "nursing facility")
    )
    if not leaves_home:
        return None
    if "baseline" in text:
        return None
    if "lives at home" in text or text.strip() in {"home", "lives at home"}:
        return (
            "discharge disposition leaves home but living situation is not labeled as baseline"
        )
    return None
