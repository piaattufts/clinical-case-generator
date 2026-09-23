"""Clean-case uniqueness fingerprints and near-duplicate auditing.

Diversity is evaluated on the structured clinical case before error injection.
Demographics, seeds, numeric vitals/labs, and planted error categories are
excluded so they cannot make two otherwise identical charts look unique.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cases import (
    CaseDischargePlanning,
    CaseIntakeOutput,
    CasePresentation,
    ClinicalCase,
)
from app.repositories.cases import (
    list_diagnoses_for_case,
    list_followups_for_case,
    list_labs_for_case,
    list_medications_for_case,
    list_monitoring_for_case,
    list_symptoms_for_case,
)
from app.sources.exceptions import CaseValidationError, DuplicateClinicalCaseError

NEAR_DUPLICATE_REJECT = 0.85
NEAR_DUPLICATE_WARN = 0.70

_SIMILARITY_WEIGHTS = {
    "diagnosis": 0.22,
    "scenario": 0.10,
    "medications": 0.25,
    "symptoms": 0.15,
    "hospital_course": 0.12,
    "labs": 0.05,
    "followup": 0.04,
    "disposition": 0.04,
    "specialty": 0.03,
}


@dataclass(frozen=True)
class CleanCaseFingerprint:
    scenario: str
    clinical_profile: str
    specialty: str
    diagnosis_codes: tuple[str, ...]
    symptoms: tuple[str, ...]
    home_medications: tuple[str, ...]
    inpatient_medications: tuple[str, ...]
    lab_concepts: tuple[str, ...]
    monitoring: tuple[str, ...]
    hospital_course_pattern: str
    followup: tuple[str, ...]
    disposition: str

    def key(self) -> tuple[str, ...]:
        return (
            self.scenario,
            self.clinical_profile,
            self.specialty,
            "|".join(self.diagnosis_codes),
            "|".join(self.symptoms),
            "|".join(self.home_medications),
            "|".join(self.inpatient_medications),
            "|".join(self.lab_concepts),
            "|".join(self.monitoring),
            self.hospital_course_pattern,
            "|".join(self.followup),
            self.disposition,
        )

    def digest(self) -> str:
        blob = "\n".join(self.key()).encode("utf-8")
        return sha256(blob).hexdigest()

    def shared_with(self, other: CleanCaseFingerprint) -> list[str]:
        shared: list[str] = []
        pairs = (
            ("scenario", self.scenario, other.scenario),
            ("clinical_profile", self.clinical_profile, other.clinical_profile),
            ("specialty", self.specialty, other.specialty),
            ("diagnosis", self.diagnosis_codes, other.diagnosis_codes),
            ("symptoms", self.symptoms, other.symptoms),
            ("home_medications", self.home_medications, other.home_medications),
            ("inpatient_medications", self.inpatient_medications, other.inpatient_medications),
            ("lab_concepts", self.lab_concepts, other.lab_concepts),
            (
                "hospital_course_pattern",
                self.hospital_course_pattern,
                other.hospital_course_pattern,
            ),
            ("followup", self.followup, other.followup),
            ("disposition", self.disposition, other.disposition),
        )
        for name, left, right in pairs:
            if left == right:
                shared.append(name)
        return shared


@dataclass
class PairAudit:
    left_id: str
    right_id: str
    score: float
    shared: list[str]
    different: list[str]


@dataclass
class DiversityAudit:
    fingerprints: dict[str, CleanCaseFingerprint] = field(default_factory=dict)
    duplicates: list[tuple[str, str, list[str]]] = field(default_factory=list)
    rejected_pairs: list[PairAudit] = field(default_factory=list)
    warnings: list[PairAudit] = field(default_factory=list)
    closest: PairAudit | None = None


def fingerprint_from_case(
    session: Session,
    case: ClinicalCase,
    *,
    scenario_code: str,
    profile_code: str,
    hospital_course_pattern: str,
) -> CleanCaseFingerprint:
    diagnoses = tuple(
        sorted(
            {
                str(item.diagnosis or "")
                for item in list_diagnoses_for_case(session, case.id)
                if item.diagnosis
            }
        )
    )
    symptoms = tuple(
        sorted(
            {
                str(item.symptom or "").casefold()
                for item in list_symptoms_for_case(session, case.id)
                if item.symptom
            }
        )
    )
    home: set[str] = set()
    inpatient: set[str] = set()
    for medication in list_medications_for_case(session, case.id):
        concept = (medication.source_reference or medication.drug or "").strip()
        if not concept:
            continue
        context = (medication.context or "").casefold()
        if context == "home":
            home.add(concept)
        elif context == "inpatient":
            inpatient.add(concept)
    labs = tuple(
        sorted(
            {
                (
                    getattr(item, "source_reference", None) or item.test_name or ""
                ).strip()
                for item in list_labs_for_case(session, case.id)
                if item.test_name or getattr(item, "source_reference", None)
            }
        )
    )
    monitoring = tuple(
        sorted(
            {
                f"{item.parameter or ''}:{item.frequency or ''}"
                for item in list_monitoring_for_case(session, case.id)
            }
        )
    )
    followup = tuple(
        sorted(
            {
                f"{item.with_service or ''}|{item.item or ''}|{item.timing or ''}"
                for item in list_followups_for_case(session, case.id)
            }
        )
    )
    discharge = session.scalar(
        select(CaseDischargePlanning).where(CaseDischargePlanning.case_id == case.id)
    )
    disposition = "home"
    if discharge is not None:
        home_health = "home_health" if discharge.home_health_ordered else "no_home_health"
        disposition = f"{discharge.disposition or case.disposition_status or 'home'}|{home_health}"
    presentation = session.scalar(
        select(CasePresentation).where(CasePresentation.case_id == case.id)
    )
    io_row = session.scalar(
        select(CaseIntakeOutput).where(CaseIntakeOutput.case_id == case.id)
    )
    course_bits = [hospital_course_pattern]
    if presentation is not None:
        course_bits.append(presentation.symptom_duration or "")
        course_bits.append(presentation.symptom_course or "")
    if io_row is not None:
        course_bits.append(io_row.timepoint or "")
    return CleanCaseFingerprint(
        scenario=scenario_code,
        clinical_profile=profile_code,
        specialty=str(case.specialty or ""),
        diagnosis_codes=diagnoses,
        symptoms=symptoms,
        home_medications=tuple(sorted(home)),
        inpatient_medications=tuple(sorted(inpatient)),
        lab_concepts=labs,
        monitoring=monitoring,
        hospital_course_pattern="|".join(course_bits),
        followup=followup,
        disposition=disposition,
    )


def fingerprint_from_mapping(
    payload: Mapping[str, Any],
    *,
    scenario_code: str = "unknown",
    profile_code: str = "unknown",
    hospital_course_pattern: str = "unspecified",
) -> CleanCaseFingerprint:
    """Build a fingerprint from a dict so tests do not need a database case."""
    def _tuple(name: str) -> tuple[str, ...]:
        value = payload.get(name) or ()
        return tuple(sorted(str(item) for item in value))

    return CleanCaseFingerprint(
        scenario=str(payload.get("scenario") or scenario_code),
        clinical_profile=str(payload.get("clinical_profile") or profile_code),
        specialty=str(payload.get("specialty") or ""),
        diagnosis_codes=_tuple("diagnosis_codes"),
        symptoms=_tuple("symptoms"),
        home_medications=_tuple("home_medications"),
        inpatient_medications=_tuple("inpatient_medications"),
        lab_concepts=_tuple("lab_concepts"),
        monitoring=_tuple("monitoring"),
        hospital_course_pattern=str(
            payload.get("hospital_course_pattern") or hospital_course_pattern
        ),
        followup=_tuple("followup"),
        disposition=str(payload.get("disposition") or "home"),
    )


def fingerprint_as_dict(fingerprint: CleanCaseFingerprint) -> dict[str, Any]:
    return {
        "scenario": fingerprint.scenario,
        "clinical_profile": fingerprint.clinical_profile,
        "specialty": fingerprint.specialty,
        "diagnosis_codes": list(fingerprint.diagnosis_codes),
        "symptoms": list(fingerprint.symptoms),
        "home_medications": list(fingerprint.home_medications),
        "inpatient_medications": list(fingerprint.inpatient_medications),
        "lab_concepts": list(fingerprint.lab_concepts),
        "monitoring": list(fingerprint.monitoring),
        "hospital_course_pattern": fingerprint.hospital_course_pattern,
        "followup": list(fingerprint.followup),
        "disposition": fingerprint.disposition,
        "digest": fingerprint.digest(),
    }


def fingerprint_from_clean_state(clean_state: Mapping[str, Any]) -> CleanCaseFingerprint | None:
    diversity = clean_state.get("diversity")
    if not isinstance(diversity, Mapping):
        return None
    raw = diversity.get("fingerprint")
    if isinstance(raw, Mapping):
        return fingerprint_from_mapping(raw)
    return None


def similarity(left: CleanCaseFingerprint, right: CleanCaseFingerprint) -> float:
    score = 0.0
    score += _SIMILARITY_WEIGHTS["diagnosis"] * _exact(left.diagnosis_codes, right.diagnosis_codes)
    score += _SIMILARITY_WEIGHTS["scenario"] * _exact(left.scenario, right.scenario)
    meds_left = set(left.home_medications) | set(left.inpatient_medications)
    meds_right = set(right.home_medications) | set(right.inpatient_medications)
    score += _SIMILARITY_WEIGHTS["medications"] * _jaccard(meds_left, meds_right)
    score += _SIMILARITY_WEIGHTS["symptoms"] * _jaccard(set(left.symptoms), set(right.symptoms))
    score += _SIMILARITY_WEIGHTS["hospital_course"] * _exact(
        left.hospital_course_pattern, right.hospital_course_pattern
    )
    score += _SIMILARITY_WEIGHTS["labs"] * _jaccard(set(left.lab_concepts), set(right.lab_concepts))
    score += _SIMILARITY_WEIGHTS["followup"] * _exact(left.followup, right.followup)
    score += _SIMILARITY_WEIGHTS["disposition"] * _exact(left.disposition, right.disposition)
    score += _SIMILARITY_WEIGHTS["specialty"] * _exact(left.specialty, right.specialty)
    return round(score, 4)


def audit_fingerprints(labeled: Sequence[tuple[str, CleanCaseFingerprint]]) -> DiversityAudit:
    audit = DiversityAudit(fingerprints={case_id: fp for case_id, fp in labeled})
    closest: PairAudit | None = None
    for index, (left_id, left_fp) in enumerate(labeled):
        for right_id, right_fp in labeled[index + 1 :]:
            if left_fp.digest() == right_fp.digest():
                shared = left_fp.shared_with(right_fp)
                audit.duplicates.append((left_id, right_id, shared))
                continue
            score = similarity(left_fp, right_fp)
            shared = left_fp.shared_with(right_fp)
            different = [
                name
                for name in (
                    "diagnosis",
                    "clinical_profile",
                    "symptoms",
                    "home_medications",
                    "hospital_course_pattern",
                    "followup",
                    "disposition",
                )
                if name not in shared
            ]
            pair = PairAudit(left_id, right_id, score, shared, different)
            if closest is None or score > closest.score:
                closest = pair
            if score >= NEAR_DUPLICATE_REJECT:
                audit.rejected_pairs.append(pair)
            elif score >= NEAR_DUPLICATE_WARN:
                audit.warnings.append(pair)
    audit.closest = closest
    return audit


def require_unique_clean_cases(
    labeled: Sequence[tuple[str, CleanCaseFingerprint]],
) -> DiversityAudit:
    audit = audit_fingerprints(labeled)
    if audit.duplicates:
        left_id, right_id, shared = audit.duplicates[0]
        raise DuplicateClinicalCaseError(left_id, right_id, shared)
    if audit.rejected_pairs:
        pair = audit.rejected_pairs[0]
        raise CaseValidationError(
            "clean_case_uniqueness",
            f"{pair.left_id} and {pair.right_id} are near-duplicate clean cases "
            f"(similarity {pair.score:.2f} >= {NEAR_DUPLICATE_REJECT})",
            pair.shared,
        )
    return audit


def diversity_report_markdown(
    *,
    batch_code: str,
    labeled: Sequence[tuple[str, CleanCaseFingerprint, Mapping[str, Any]]],
    audit: DiversityAudit,
) -> str:
    scenario_counts: dict[str, int] = {}
    profile_counts: dict[str, int] = {}
    specialty_counts: dict[str, int] = {}
    diagnosis_counts: dict[str, int] = {}
    family_counts: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    symptom_sets: set[tuple[str, ...]] = set()
    med_sets: set[tuple[str, ...]] = set()
    course_sets: set[str] = set()
    followup_sets: set[tuple[str, ...]] = set()
    dispositions: set[str] = set()
    lines = [
        f"# Clean-case diversity report (`{batch_code}`)",
        "",
        "Case diversity is evaluated on the clean clinical case before error injection. "
        "Different seeds, demographics, numeric results, or planted error categories do "
        "not by themselves make two cases clinically unique.",
        "",
        "Until clinicians finish review, treat every record as a machine-validated "
        "synthetic resident-review case pending clinician validation.",
        "",
        "## Scenario distribution",
        "",
        "| Family | Clinical profile | Count |",
        "| --- | --- | ---: |",
    ]
    rows = []
    for _case_id, fingerprint, meta in labeled:
        scenario_counts[fingerprint.scenario] = scenario_counts.get(fingerprint.scenario, 0) + 1
        profile_counts[fingerprint.clinical_profile] = (
            profile_counts.get(fingerprint.clinical_profile, 0) + 1
        )
        specialty_counts[fingerprint.specialty] = specialty_counts.get(fingerprint.specialty, 0) + 1
        diagnosis_key = "|".join(fingerprint.diagnosis_codes) or "(none)"
        diagnosis_counts[diagnosis_key] = diagnosis_counts.get(diagnosis_key, 0) + 1
        family = str(meta.get("error_family") or "none")
        category = str(meta.get("error_category") or "control")
        family_counts[family] = family_counts.get(family, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1
        symptom_sets.add(fingerprint.symptoms)
        med_sets.add(fingerprint.home_medications)
        course_sets.add(fingerprint.hospital_course_pattern)
        followup_sets.add(fingerprint.followup)
        dispositions.add(fingerprint.disposition)
        rows.append((fingerprint.scenario, fingerprint.clinical_profile))
    for scenario, profile in sorted(set(rows)):
        count = sum(1 for item in rows if item == (scenario, profile))
        lines.append(f"| `{scenario}` | `{profile}` | {count} |")
    total = len(labeled) or 1
    lines.extend(
        [
            "",
            "### Specialty and diagnosis",
            "",
        ]
    )
    for name, counts in (
        ("Specialty", specialty_counts),
        ("Diagnosis", diagnosis_counts),
        ("Broad scenario family", scenario_counts),
    ):
        lines.append(f"**{name}**")
        lines.append("")
        for key, count in sorted(counts.items()):
            pct = 100.0 * count / total
            lines.append(f"- {key}: {count} ({pct:.1f}%)")
        lines.append("")
    lines.extend(
        [
            "## Clinical-feature diversity",
            "",
            f"- unique symptom sets: {len(symptom_sets)}",
            f"- unique home-medication sets: {len(med_sets)}",
            f"- unique hospital-course profiles: {len(course_sets)}",
            f"- unique follow-up profiles: {len(followup_sets)}",
            f"- unique discharge dispositions: {len(dispositions)}",
            f"- unique clinical profiles: {len(profile_counts)}",
            "",
            "## Error distribution",
            "",
        ]
    )
    for family, count in sorted(family_counts.items()):
        lines.append(f"- {family}: {count}")
    lines.append("")
    for category, count in sorted(category_counts.items()):
        lines.append(f"- `{category}`: {count}")
    lines.extend(["", "## Similarity audit", ""])
    if audit.closest is None:
        lines.append("Only one case was audited.")
    else:
        closest = audit.closest
        lines.extend(
            [
                f"- closest pair: {closest.left_id} vs {closest.right_id}",
                f"- similarity score: {closest.score:.2f}",
                f"- features shared: {', '.join(closest.shared) or '(none)'}",
                f"- features different: {', '.join(closest.different) or '(none)'}",
                "",
            ]
        )
    if audit.warnings:
        lines.append("Pairs at or above the warning threshold:")
        lines.append("")
        for pair in audit.warnings:
            lines.append(
                f"- {pair.left_id} vs {pair.right_id}: {pair.score:.2f} "
                f"(shared {', '.join(pair.shared)})"
            )
        lines.append("")
    else:
        lines.append("No pairs reached the warning threshold.")
        lines.append("")
    passed = not audit.duplicates and not audit.rejected_pairs
    lines.extend(
        [
            "## Uniqueness conclusion",
            "",
            (
                "All clean cases passed the uniqueness requirement. Exact fingerprints "
                "are distinct and no pair met the near-duplicate rejection threshold."
                if passed
                else "The batch failed clean-case uniqueness and must not be frozen."
            ),
            "",
            f"- exact duplicate fingerprints: {len(audit.duplicates)}",
            f"- near-duplicate rejections: {len(audit.rejected_pairs)}",
            f"- near-duplicate warnings: {len(audit.warnings)}",
            "",
        ]
    )
    return "\n".join(lines)


def _exact(left: Any, right: Any) -> float:
    return 1.0 if left == right else 0.0


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
