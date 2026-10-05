"""Integrity checks. These functions report errors and do not change data."""

from __future__ import annotations

from dataclasses import dataclass

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv
from inthewild_review.schemas import (
    CONTINUOUS_VS_EPISODIC,
    DEPLOYMENT_TRI_STATE_FIELDS,
    DUPLICATE_DECISIONS,
    EMBODIMENT_COUNT,
    PROVENANCE_CODES,
    SCENARIO_EXPLICITNESS,
    SCENARIO_TRI_STATE_FIELDS,
    SETTING_TYPES,
    TRI_STATE,
)
from inthewild_review.screening import (
    validate_full_text_row,
    validate_title_abstract_row,
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str


class ValidationFailure(Exception):
    def __init__(self, issues: list[Issue]) -> None:
        self.issues = issues
        lines = [f"{issue.code}: {issue.message}" for issue in issues]
        super().__init__(f"{len(issues)} validation error(s):\n" + "\n".join(lines))


def _duplicate_ids(rows: list[dict[str, str]], field: str, label: str, issues: list[Issue]) -> None:
    seen: set[str] = set()
    for row in rows:
        value = (row.get(field) or "").strip()
        if not value:
            issues.append(Issue("MISSING_ID", f"{label} row is missing {field}."))
            continue
        if value in seen:
            issues.append(Issue("DUPLICATE_ID", f"Duplicate {field} {value} in {label}."))
        seen.add(value)


def _tri_state(row: dict[str, str], field: str, label: str, issues: list[Issue]) -> None:
    value = (row.get(field) or "").strip()
    if value not in TRI_STATE:
        issues.append(
            Issue(
                "INVALID_TRI_STATE",
                f"{label} field {field} is {value or 'blank'!r}. "
                "Use YES, NO, or NOT_REPORTED_OR_UNCLEAR. Blank is not allowed, "
                "and missing information must not be coded NO.",
            )
        )


def _ids(rows: list[dict[str, str]], field: str) -> set[str]:
    return {(row.get(field) or "").strip() for row in rows if (row.get(field) or "").strip()}


def validate_repository(layout: ReviewLayout) -> list[Issue]:
    issues: list[Issue] = []
    normalized = read_csv(layout.normalized)
    duplicates = read_csv(layout.duplicates)
    title_abstract = read_csv(layout.title_abstract)
    full_text = read_csv(layout.full_text)
    publications = read_csv(layout.publications)
    studies = read_csv(layout.studies)
    deployments = read_csv(layout.deployments)
    scenarios = read_csv(layout.scenarios)
    reviewer_1 = read_csv(layout.reviewer_1)
    reviewer_2 = read_csv(layout.reviewer_2)
    consensus = read_csv(layout.calibration_consensus)

    _duplicate_ids(normalized, "record_id", "normalized records", issues)
    _duplicate_ids(publications, "publication_id", "publications", issues)
    _duplicate_ids(studies, "study_id", "studies", issues)
    _duplicate_ids(deployments, "deployment_id", "deployments", issues)
    _duplicate_ids(scenarios, "scenario_id", "scenarios", issues)

    record_ids = _ids(normalized, "record_id")
    publication_ids = _ids(publications, "publication_id")
    study_ids = _ids(studies, "study_id")
    deployment_ids = _ids(deployments, "deployment_id")
    study_publication = {
        (row.get("study_id") or "").strip(): (row.get("publication_id") or "").strip()
        for row in studies
    }
    deployment_study = {
        (row.get("deployment_id") or "").strip(): (row.get("study_id") or "").strip()
        for row in deployments
    }

    for row in publications:
        record_id = (row.get("record_id") or "").strip()
        publication_id = (row.get("publication_id") or "").strip()
        if record_id and record_ids and record_id not in record_ids:
            issues.append(
                Issue(
                    "ORPHAN_RECORD",
                    f"Publication {publication_id} points at unknown record_id {record_id}.",
                )
            )
        if not record_id:
            issues.append(
                Issue("MISSING_RECORD_LINK", f"Publication {publication_id} has no record_id.")
            )

    for row in studies:
        publication_id = (row.get("publication_id") or "").strip()
        study_id = (row.get("study_id") or "").strip()
        if publication_id not in publication_ids:
            issues.append(
                Issue(
                    "ORPHAN_STUDY",
                    f"Study {study_id} points at unknown publication_id {publication_id or 'blank'}.",
                )
            )

    for row in deployments:
        deployment_id = (row.get("deployment_id") or "").strip()
        study_id = (row.get("study_id") or "").strip()
        if study_id not in study_ids:
            issues.append(
                Issue(
                    "ORPHAN_DEPLOYMENT",
                    f"Deployment {deployment_id} points at unknown study_id {study_id or 'blank'}.",
                )
            )
        setting = (row.get("setting_type") or "").strip()
        if setting not in SETTING_TYPES:
            issues.append(
                Issue(
                    "INVALID_SETTING",
                    f"Deployment {deployment_id} has setting_type {setting or 'blank'!r}. "
                    "Use NOT_REPORTED_OR_UNCLEAR when the setting is not reported.",
                )
            )
        additional = (row.get("additional_setting_types") or "").strip()
        if additional:
            for part in additional.split("|"):
                part = part.strip()
                if part and part not in SETTING_TYPES:
                    issues.append(
                        Issue(
                            "INVALID_SETTING",
                            f"Deployment {deployment_id} has additional setting {part!r}.",
                        )
                    )
        exposure = (row.get("continuous_vs_episodic") or "").strip()
        if exposure not in CONTINUOUS_VS_EPISODIC:
            issues.append(
                Issue(
                    "INVALID_EXPOSURE",
                    f"Deployment {deployment_id} has continuous_vs_episodic {exposure!r}.",
                )
            )
        embodiments = (row.get("single_or_multiple_embodiments") or "").strip()
        if embodiments not in EMBODIMENT_COUNT:
            issues.append(
                Issue(
                    "INVALID_EMBODIMENT_COUNT",
                    f"Deployment {deployment_id} has single_or_multiple_embodiments {embodiments!r}.",
                )
            )
        for field in DEPLOYMENT_TRI_STATE_FIELDS:
            _tri_state(row, field, f"Deployment {deployment_id}", issues)

    for row in scenarios:
        scenario_id = (row.get("scenario_id") or "").strip()
        deployment_id = (row.get("deployment_id") or "").strip()
        if deployment_id not in deployment_ids:
            issues.append(
                Issue(
                    "ORPHAN_SCENARIO",
                    f"Scenario {scenario_id} points at unknown deployment_id {deployment_id or 'blank'}.",
                )
            )
        study_id = (row.get("study_id") or "").strip()
        if study_id and study_id not in study_ids:
            issues.append(
                Issue(
                    "ORPHAN_SCENARIO_STUDY",
                    f"Scenario {scenario_id} points at unknown study_id {study_id}.",
                )
            )
        if deployment_id in deployment_study and study_id:
            expected = deployment_study[deployment_id]
            if expected and study_id != expected:
                issues.append(
                    Issue(
                        "SCENARIO_STUDY_MISMATCH",
                        f"Scenario {scenario_id} study_id {study_id} does not match "
                        f"deployment {deployment_id} study_id {expected}.",
                    )
                )
        publication_id = (row.get("publication_id") or "").strip()
        if publication_id and publication_id not in publication_ids:
            issues.append(
                Issue(
                    "ORPHAN_SCENARIO_PUBLICATION",
                    f"Scenario {scenario_id} points at unknown publication_id {publication_id}.",
                )
            )
        if study_id and publication_id and study_id in study_publication:
            expected_publication = study_publication[study_id]
            if expected_publication and publication_id != expected_publication:
                issues.append(
                    Issue(
                        "SCENARIO_PUBLICATION_MISMATCH",
                        f"Scenario {scenario_id} publication_id {publication_id} does not match "
                        f"study {study_id} publication_id {expected_publication}.",
                    )
                )
        explicitness = (row.get("scenario_explicitness") or "").strip()
        if explicitness not in SCENARIO_EXPLICITNESS:
            issues.append(
                Issue(
                    "INVALID_EXPLICITNESS",
                    f"Scenario {scenario_id} has scenario_explicitness {explicitness!r}.",
                )
            )
        provenance = (row.get("provenance_codes") or "").strip()
        if not provenance:
            issues.append(
                Issue(
                    "MISSING_PROVENANCE",
                    f"Scenario {scenario_id} has blank provenance_codes. "
                    "Use NOT_REPORTED_OR_UNCLEAR when the paper does not report provenance.",
                )
            )
        else:
            parts = [part.strip() for part in provenance.split("|") if part.strip()]
            if not parts:
                issues.append(Issue("MISSING_PROVENANCE", f"Scenario {scenario_id} has blank provenance."))
            for part in parts:
                if part not in PROVENANCE_CODES:
                    issues.append(
                        Issue(
                            "INVALID_PROVENANCE",
                            f"Scenario {scenario_id} has illegal provenance code {part!r}.",
                        )
                    )
            if "NOT_REPORTED_OR_UNCLEAR" in parts and len(parts) > 1:
                issues.append(
                    Issue(
                        "INVALID_PROVENANCE",
                        f"Scenario {scenario_id} combines NOT_REPORTED_OR_UNCLEAR with other provenance codes.",
                    )
                )
        for field in SCENARIO_TRI_STATE_FIELDS:
            _tri_state(row, field, f"Scenario {scenario_id}", issues)

    for label, rows in (
        ("title/abstract screening", title_abstract),
        ("calibration reviewer 1", reviewer_1),
        ("calibration reviewer 2", reviewer_2),
        ("calibration consensus", consensus),
    ):
        for row in rows:
            if not (row.get("decision") or "").strip() and not (row.get("exclusion_code") or "").strip():
                continue
            try:
                validate_title_abstract_row(row)
            except ValueError as exc:
                issues.append(Issue("INVALID_SCREENING", f"{label}: {exc}"))

    for row in full_text:
        if not any((row.get(key) or "").strip() for key in row):
            continue
        if not (row.get("decision") or "").strip() and not (row.get("exclusion_reason") or "").strip():
            continue
        try:
            validate_full_text_row(row)
        except ValueError as exc:
            issues.append(Issue("INVALID_FULL_TEXT", str(exc)))

    for row in duplicates:
        decision = (row.get("human_decision") or "").strip()
        if decision and decision not in DUPLICATE_DECISIONS:
            issues.append(
                Issue(
                    "INVALID_DUPLICATE_DECISION",
                    f"Duplicate pair {row.get('record_id_1')} / {row.get('record_id_2')} "
                    f"has human_decision {decision!r}.",
                )
            )
        for field in ("record_id_1", "record_id_2"):
            record_id = (row.get(field) or "").strip()
            if record_ids and record_id and record_id not in record_ids:
                issues.append(
                    Issue(
                        "ORPHAN_DUPLICATE",
                        f"Duplicate candidate {field} {record_id} is not in normalized records.",
                    )
                )
        retained = (row.get("retained_record_id") or "").strip()
        pair = {(row.get("record_id_1") or "").strip(), (row.get("record_id_2") or "").strip()}
        if retained and retained not in pair:
            issues.append(
                Issue(
                    "INVALID_RETAINED_RECORD",
                    f"retained_record_id {retained} is not one of the paired record ids.",
                )
            )

    reviewer_1_ids = {
        (row.get("record_id") or "").strip()
        for row in reviewer_1
        if (row.get("decision") or "").strip()
    }
    reviewer_2_ids = {
        (row.get("record_id") or "").strip()
        for row in reviewer_2
        if (row.get("decision") or "").strip()
    }
    for row in consensus:
        if not (row.get("decision") or "").strip():
            continue
        record_id = (row.get("record_id") or "").strip()
        if record_id not in reviewer_1_ids or record_id not in reviewer_2_ids:
            issues.append(
                Issue(
                    "CONSENSUS_WITHOUT_INDEPENDENT_RATINGS",
                    f"Consensus for {record_id} exists without a decision in both "
                    "calibration reviewer files.",
                )
            )

    included_ids = {
        (row.get("record_id") or "").strip()
        for row in full_text
        if (row.get("decision") or "").strip() == "INCLUDE"
    }
    if publications:
        for row in publications:
            record_id = (row.get("record_id") or "").strip()
            if record_id not in included_ids:
                issues.append(
                    Issue(
                        "PUBLICATION_NOT_INCLUDED",
                        f"Publication {row.get('publication_id')} record {record_id} "
                        "does not have a full-text INCLUDE decision.",
                    )
                )
    return issues


def require_valid(layout: ReviewLayout) -> None:
    issues = validate_repository(layout)
    if issues:
        raise ValidationFailure(issues)
