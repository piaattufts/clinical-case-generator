"""Compare exported validation batches on clean-case structure, not demographics."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from app.services.case_diversity import (
    CleanCaseFingerprint,
    audit_fingerprints,
    fingerprint_from_mapping,
)
from app.services.seed_archetypes import GENERATION_STRATEGY_SEED, GENERATION_STRATEGY_TEMPLATE
from app.services.validation_registry import (
    STRATEGY_BALANCED,
    STRATEGY_SEED,
    active_batches,
)

DATASET_STATUS = "machine-validated synthetic resident-review cases pending clinician validation"


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def fingerprint_from_resident_case(
    case: dict[str, Any],
    *,
    scenario: str,
    profile: str,
) -> CleanCaseFingerprint:
    clinical = case.get("ClinicalCase") or {}
    presentation = clinical.get("presentation") or {}
    discharge = clinical.get("discharge_planning") or {}
    symptoms = [
        str(item).casefold()
        for item in (presentation.get("presenting_symptoms") or [])
        if item
    ]
    home = sorted(
        {
            str(item.get("drug") or "")
            for item in (case.get("CaseMedication") or [])
            if item.get("context") == "home" and item.get("drug")
        }
    )
    inpatient = sorted(
        {
            str(item.get("drug") or "")
            for item in (case.get("CaseMedication") or [])
            if item.get("context") == "inpatient" and item.get("drug")
        }
    )
    labs = sorted(
        {
            str(item.get("test_name") or "")
            for item in (case.get("CaseLab") or [])
            if item.get("test_name")
        }
    )
    followup = sorted(
        f"{item.get('with_service') or ''}|{item.get('item') or ''}|{item.get('timing') or ''}"
        for item in (case.get("CaseFollowup") or [])
    )
    course = next(
        (
            str(item.get("note_text") or "")
            for item in (case.get("CaseNote") or [])
            if item.get("note_type") == "hospital_course"
        ),
        "",
    )
    io = case.get("CaseIntakeOutput") or []
    io_time = str(io[0].get("timepoint") or "") if io else ""
    home_health = "home_health" if discharge.get("home_health_ordered") else "no_home_health"
    duration = str(presentation.get("symptom_duration") or "")
    symptom_course = str(presentation.get("symptom_course") or "")
    disposition = discharge.get("disposition") or clinical.get("disposition_status") or "home"
    return fingerprint_from_mapping(
        {
            "scenario": scenario,
            "clinical_profile": profile,
            "specialty": clinical.get("specialty") or "",
            "diagnosis_codes": [clinical.get("admission_dx") or ""],
            "symptoms": symptoms,
            "home_medications": home,
            "inpatient_medications": inpatient,
            "lab_concepts": labs,
            "monitoring": [
                str(item.get("parameter") or "")
                for item in (case.get("CaseMonitoring") or [])
                if item.get("parameter")
            ],
            "hospital_course_pattern": "|".join(
                [course[:80], duration, symptom_course, io_time]
            ),
            "followup": followup,
            "disposition": f"{disposition}|{home_health}",
        }
    )


def summarize_batch(
    *,
    resident_path: Path,
    investigator_path: Path,
    default_strategy: str,
) -> dict[str, Any]:
    resident = _load(resident_path)
    investigator = _load(investigator_path)
    inv_rows = {
        str(item.get("validation_case_id")): item
        for item in investigator.get("cases") or []
        if isinstance(item, dict)
    }
    labeled: list[tuple[str, CleanCaseFingerprint]] = []
    diagnoses: Counter[str] = Counter()
    specialties: Counter[str] = Counter()
    strategies: Counter[str] = Counter()
    families: Counter[str] = Counter()
    profiles: set[str] = set()
    error_categories: Counter[str] = Counter()
    error_families: Counter[str] = Counter()
    imaging_sets: set[tuple[str, ...]] = set()
    consult_sets: set[tuple[str, ...]] = set()
    for case in resident.get("cases") or []:
        if not isinstance(case, dict):
            continue
        case_id = str(case.get("case_id_code") or "")
        inv = inv_rows.get(case_id) or {}
        scenario = str(inv.get("scenario") or "")
        profile = str(inv.get("clinical_profile") or "default")
        strategy = str(inv.get("generation_strategy") or default_strategy)
        fingerprint = fingerprint_from_resident_case(case, scenario=scenario, profile=profile)
        labeled.append((case_id, fingerprint))
        clinical = case.get("ClinicalCase") or {}
        diagnoses[str(clinical.get("admission_dx") or "unknown")] += 1
        specialties[str(clinical.get("specialty") or fingerprint.specialty or "unknown")] += 1
        strategies[strategy] += 1
        families[scenario] += 1
        if profile:
            profiles.add(profile)
        error = inv.get("error") or {}
        error_categories[str(error.get("error_category") or "none")] += 1
        error_families[str(error.get("error_family") or "none")] += 1
        imaging_sets.add(
            tuple(
                sorted(
                    str(item.get("study_type") or "")
                    for item in (case.get("CaseImaging") or [])
                    if item.get("study_type")
                )
            )
        )
        consult_sets.add(
            tuple(
                sorted(
                    str(item.get("service") or "")
                    for item in (case.get("CaseConsult") or [])
                    if item.get("service")
                )
            )
        )
    audit = audit_fingerprints(labeled) if len(labeled) >= 2 else None
    symptom_sets = {item[1].symptoms for item in labeled}
    med_sets = {item[1].home_medications for item in labeled}
    courses = {item[1].hospital_course_pattern for item in labeled}
    followups = {item[1].followup for item in labeled}
    return {
        "batch_code": resident.get("batch_code"),
        "case_count": len(labeled),
        "generation_strategy": dict(strategies),
        "families": dict(sorted(families.items())),
        "diagnoses": dict(sorted(diagnoses.items())),
        "specialties": dict(sorted(specialties.items())),
        "unique_profiles": len(profiles),
        "unique_symptom_sets": len(symptom_sets),
        "unique_home_medication_sets": len(med_sets),
        "unique_hospital_course_profiles": len(courses),
        "unique_followup_profiles": len(followups),
        "unique_imaging_sets": len(imaging_sets),
        "unique_consult_sets": len(consult_sets),
        "error_families": dict(sorted(error_families.items())),
        "error_categories": dict(sorted(error_categories.items())),
        "exact_duplicates": 0 if audit is None else len(audit.duplicates),
        "near_duplicate_rejections": 0 if audit is None else len(audit.rejected_pairs),
        "near_duplicate_warnings": 0 if audit is None else len(audit.warnings),
        "closest_pair": (
            None
            if audit is None or audit.closest is None
            else f"{audit.closest.left_id} vs {audit.closest.right_id}"
        ),
        "closest_score": None if audit is None or audit.closest is None else audit.closest.score,
    }


def comparison_markdown(left: dict[str, Any], right: dict[str, Any]) -> str:
    def row(label: str, left_value: object, right_value: object) -> str:
        return f"| {label} | {left_value} | {right_value} |"

    left_code = left["batch_code"]
    right_code = right["batch_code"]
    lines = [
        "# Randomized template batch versus resident-seed-guided batch",
        "",
        DATASET_STATUS,
        "",
        "This comparison uses exported charts. It does not regenerate or modify",
        "either frozen batch. Uniqueness is judged on clean-case structure",
        "reconstructed from resident-facing fields plus investigator labels.",
        "Age, sex, exact vitals, and exact laboratory numbers are excluded.",
        "",
        f"Left: `{left_code}` (`{GENERATION_STRATEGY_TEMPLATE}` unless labeled).",
        f"Right: `{right_code}` (`{GENERATION_STRATEGY_SEED}` unless labeled).",
        "",
        f"| Measure | {left_code} | {right_code} |",
        "| --- | ---: | ---: |",
        row("Cases", left["case_count"], right["case_count"]),
        row("Scenario / archetype families", len(left["families"]), len(right["families"])),
        row("Unique clinical profiles", left["unique_profiles"], right["unique_profiles"]),
        row("Unique diagnoses", len(left["diagnoses"]), len(right["diagnoses"])),
        row("Unique symptom sets", left["unique_symptom_sets"], right["unique_symptom_sets"]),
        row(
            "Unique home-medication sets",
            left["unique_home_medication_sets"],
            right["unique_home_medication_sets"],
        ),
        row(
            "Unique hospital-course profiles",
            left["unique_hospital_course_profiles"],
            right["unique_hospital_course_profiles"],
        ),
        row(
            "Unique follow-up profiles",
            left["unique_followup_profiles"],
            right["unique_followup_profiles"],
        ),
        row("Exact duplicate fingerprints", left["exact_duplicates"], right["exact_duplicates"]),
        row(
            "Near-duplicate warnings",
            left["near_duplicate_warnings"],
            right["near_duplicate_warnings"],
        ),
        row("Closest-pair similarity", left["closest_score"], right["closest_score"]),
        "",
        "## Families",
        "",
        "### Left",
        "",
    ]
    for name, count in left["families"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "### Right", ""])
    for name, count in right["families"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(
        [
            "",
            "## Error-category coverage",
            "",
            "### Left",
            "",
        ]
    )
    for name, count in left["error_categories"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "### Right", ""])
    for name, count in right["error_categories"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(
        [
            "",
            "## Closest pairs",
            "",
            f"- Left closest pair: {left['closest_pair']} ({left['closest_score']})",
            f"- Right closest pair: {right['closest_pair']} ({right['closest_score']})",
            "",
            "## Method note",
            "",
            "`CLINIPROOF_TAXONOMY_V1` is generated from structured/randomized inpatient",
            "scenario families. `CLINIPROOF_SEEDCASES_V1` is generated from resident-authored",
            "seed archetypes plus named clinical profiles. Neither batch is declared the",
            "study dataset by this report. Human clinician review is still required.",
            "",
        ]
    )
    return "\n".join(lines)


def write_randomized_vs_seedcase_comparison(
    *,
    left_resident: Path,
    left_investigator: Path,
    right_resident: Path,
    right_investigator: Path,
    output: Path,
) -> Path:
    left = summarize_batch(
        resident_path=left_resident,
        investigator_path=left_investigator,
        default_strategy=GENERATION_STRATEGY_TEMPLATE,
    )
    right = summarize_batch(
        resident_path=right_resident,
        investigator_path=right_investigator,
        default_strategy=GENERATION_STRATEGY_SEED,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(comparison_markdown(left, right), encoding="utf-8")
    return output


def write_active_batch_comparison(output: Path | None = None) -> Path:
    specs = active_batches()
    if len(specs) != 2:
        raise ValueError("active comparison requires exactly two active batches")
    left_spec, right_spec = specs[0], specs[1]
    left = summarize_batch(
        resident_path=left_spec.directory / "resident_validation_cases.json",
        investigator_path=left_spec.directory / "investigator_answer_key.json",
        default_strategy=STRATEGY_BALANCED,
    )
    right = summarize_batch(
        resident_path=right_spec.directory / "resident_validation_cases.json",
        investigator_path=right_spec.directory / "investigator_answer_key.json",
        default_strategy=STRATEGY_SEED,
    )
    target = output or (
        Path(__file__).resolve().parents[2]
        / "data"
        / "case_sets"
        / "investigator"
        / "comparison"
        / "active_batch_comparison.md"
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    def row(label: str, left_value: object, right_value: object) -> str:
        return f"| {label} | {left_value} | {right_value} |"

    lines = [
        "# Active prospective validation batches",
        "",
        DATASET_STATUS,
        "",
        "This investigator-facing comparison is descriptive. It does not rank one",
        "generation strategy as better than the other. It does not regenerate or",
        "modify either frozen batch. Uniqueness is judged on clean-case structure",
        "reconstructed from resident-facing fields plus investigator labels.",
        "Age, sex, exact vitals, and exact laboratory numbers are excluded.",
        "",
        f"Left: `{left_spec.code}` (`{STRATEGY_BALANCED}`).",
        f"Right: `{right_spec.code}` (`{STRATEGY_SEED}`).",
        "",
        "The archived original freeze `CLINIPROOF_TAXONOMY_V1` is excluded.",
        "",
        f"| Measure | {left_spec.code} | {right_spec.code} |",
        "| --- | ---: | ---: |",
        row("Cases", left["case_count"], right["case_count"]),
        row("Generation strategy", STRATEGY_BALANCED, STRATEGY_SEED),
        row("Scenario / archetype families", len(left["families"]), len(right["families"])),
        row("Unique clinical profiles", left["unique_profiles"], right["unique_profiles"]),
        row("Unique diagnoses", len(left["diagnoses"]), len(right["diagnoses"])),
        row("Unique specialties", len(left["specialties"]), len(right["specialties"])),
        row("Unique symptom sets", left["unique_symptom_sets"], right["unique_symptom_sets"]),
        row(
            "Unique home-medication sets",
            left["unique_home_medication_sets"],
            right["unique_home_medication_sets"],
        ),
        row(
            "Unique hospital-course profiles",
            left["unique_hospital_course_profiles"],
            right["unique_hospital_course_profiles"],
        ),
        row(
            "Unique follow-up profiles",
            left["unique_followup_profiles"],
            right["unique_followup_profiles"],
        ),
        row("Unique imaging sets", left["unique_imaging_sets"], right["unique_imaging_sets"]),
        row("Unique consult sets", left["unique_consult_sets"], right["unique_consult_sets"]),
        row("Exact duplicate fingerprints", left["exact_duplicates"], right["exact_duplicates"]),
        row(
            "Near-duplicate warnings",
            left["near_duplicate_warnings"],
            right["near_duplicate_warnings"],
        ),
        row("Closest-pair similarity", left["closest_score"], right["closest_score"]),
        row(
            "Family 1 count",
            left["error_families"].get("family_1", 0),
            right["error_families"].get("family_1", 0),
        ),
        row(
            "Family 2 count",
            left["error_families"].get("family_2", 0),
            right["error_families"].get("family_2", 0),
        ),
        row(
            "Clean-control count",
            left["error_families"].get("none", 0),
            right["error_families"].get("none", 0),
        ),
        "",
        "## Scenario / archetype distribution",
        "",
        "### Left",
        "",
    ]
    for name, count in left["families"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "### Right", ""])
    for name, count in right["families"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "## Diagnosis distribution", "", "### Left", ""])
    for name, count in left["diagnoses"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "### Right", ""])
    for name, count in right["diagnoses"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Specialty distribution", "", "### Left", ""])
    for name, count in left["specialties"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "### Right", ""])
    for name, count in right["specialties"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(
        [
            "",
            "## Closest pairs",
            "",
            f"- Left closest pair: {left['closest_pair']} ({left['closest_score']})",
            f"- Right closest pair: {right['closest_pair']} ({right['closest_score']})",
            "",
            "## Method note",
            "",
            "`CLINIPROOF_BALANCED_V3` uses named clinical profiles inside the five",
            "template inpatient families. `CLINIPROOF_SEEDCASES_V2` uses resident-authored",
            "seed archetypes plus named profiles. Both are active prospective sets after",
            "clinical-coherence QC. `CLINIPROOF_BALANCED_V2` and `CLINIPROOF_SEEDCASES_V1`",
            "remain preclinical-QC archives. `CLINIPROOF_TAXONOMY_V1` remains archived",
            "historical provenance. Human clinician review is still required.",
            "",
        ]
    )
    target.write_text("\n".join(lines), encoding="utf-8")
    return target
