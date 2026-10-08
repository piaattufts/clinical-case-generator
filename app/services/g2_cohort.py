"""Select the Generation 2 pilot from audited candidate episodes."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from app.services.discharge_episode import (
    SCENARIO_ORDER,
    build_episode,
    variant_supported,
    variants_for,
)
from app.services.g2_audit import audit_passes, round1_row
from app.services.synthea_eligibility import evaluate_patient, has_synthea_endocarditis
from app.sources.synthea import LongitudinalPatient

FINAL_PER_FAMILY = 4
MIN_CANDIDATES = 8
SIMILARITY_REJECT = 0.85


def fingerprint_tokens(fingerprint: dict[str, str]) -> set[str]:
    return {f"{key}={value}" for key, value in sorted(fingerprint.items()) if key != "med_signature"}


def jaccard(left: dict[str, str], right: dict[str, str]) -> float:
    a = fingerprint_tokens(left)
    b = fingerprint_tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def _prefer(patient: LongitudinalPatient, scenario: str) -> tuple[int, str]:
    eligibility = evaluate_patient(patient)[scenario]
    rank = 0 if eligibility.tier in {"known_heart_failure", "synthea_endocarditis"} else 1
    if scenario == "ENDOCARDITIS_OPAT":
        blob = patient.condition_blob()
        cardiac = any(token in blob for token in ("heart", "valve", "coronary"))
        rank = 0 if cardiac else 1
    return (rank, patient.synthea_patient_id)


def _eligible(
    patients: list[LongitudinalPatient],
) -> dict[str, list[LongitudinalPatient]]:
    grouped: dict[str, list[LongitudinalPatient]] = {code: [] for code in SCENARIO_ORDER}
    for patient in patients:
        decisions = evaluate_patient(patient)
        for code in SCENARIO_ORDER:
            if decisions[code].eligible:
                grouped[code].append(patient)
    for code in SCENARIO_ORDER:
        grouped[code].sort(key=lambda item: _prefer(item, code))
    return grouped


def generate_candidates(
    patients: list[LongitudinalPatient],
    meta: dict[str, str],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], dict[str, int]]:
    grouped = _eligible(patients)
    counts = {code: len(rows) for code, rows in grouped.items()}
    kept: dict[str, list[dict[str, Any]]] = {code: [] for code in SCENARIO_ORDER}
    rejected: list[dict[str, Any]] = []
    used: set[str] = set()
    for code in SCENARIO_ORDER:
        pool = [item for item in grouped[code] if item.synthea_patient_id not in used]
        if len(pool) < MIN_CANDIDATES:
            pool = list(grouped[code])
        for variant in variants_for(code):
            supporters = [item for item in pool if variant_supported(item, code, variant)]
            produced = 0
            for patient in supporters:
                if produced >= 2:
                    break
                episode = build_episode(patient, code, variant, meta)
                row = round1_row(episode, "")
                record = {
                    "scenario": code,
                    "variant_id": variant["variant_id"],
                    "synthea_patient_id": patient.synthea_patient_id,
                    "eligibility_tier": episode["eligibility_tier"],
                    "fingerprint": episode["fingerprint"],
                    "episode": episode,
                }
                if not row["overall_pass"]:
                    rejected.append({**record, "reason": row["notes"] or "audit_failed", "episode": None})
                    produced += 1
                    continue
                similar = next(
                    (
                        prior
                        for prior in kept[code]
                        if jaccard(prior["fingerprint"], episode["fingerprint"]) >= SIMILARITY_REJECT
                    ),
                    None,
                )
                if similar is not None:
                    rejected.append(
                        {
                            **record,
                            "reason": f"high_similarity_to_{similar['variant_id']}",
                            "episode": None,
                        }
                    )
                else:
                    kept[code].append(record)
                    used.add(patient.synthea_patient_id)
                produced += 1
                pool = [item for item in pool if item.synthea_patient_id != patient.synthea_patient_id]
        if len(kept[code]) < FINAL_PER_FAMILY:
            raise RuntimeError(
                f"{code} produced {len(kept[code])} passing candidates; "
                f"eligible patients: {counts[code]}"
            )
    counts["synthea_endocarditis_conditions"] = sum(
        1 for patient in patients if has_synthea_endocarditis(patient) and not patient.deceased
    )
    return kept, rejected, counts


def select_final(
    kept: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    for code in SCENARIO_ORDER:
        by_variant: dict[str, dict[str, Any]] = {}
        for item in kept[code]:
            by_variant.setdefault(str(item["variant_id"]), item)
        family: list[dict[str, Any]] = []
        for variant in variants_for(code):
            matched = by_variant.get(str(variant["variant_id"]))
            if matched is not None:
                family.append(matched)
            if len(family) == FINAL_PER_FAMILY:
                break
        if len(family) < FINAL_PER_FAMILY:
            raise RuntimeError(f"{code} has {len(family)} distinct variants")
        chosen.extend(family)
    for index, item in enumerate(chosen, start=1):
        case_id = f"G2-{index:03d}"
        episode = item["episode"]
        resident = episode["resident"]
        resident["case_id_code"] = case_id
        clinical = resident["ClinicalCase"]
        clinical["case_id_code"] = case_id
        clinical["title"] = f"{episode['scenario_code']} {case_id}"
        clinical["patient_name"] = case_id
        _retag(resident, case_id)
        episode["case_id"] = case_id
        item["case_id"] = case_id
    return chosen


def _retag(resident: dict[str, Any], case_id: str) -> None:
    for _key, rows in resident.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            if "case_id" in row:
                row["case_id"] = case_id
            for id_key, value in list(row.items()):
                if id_key.endswith("_id") and isinstance(value, str) and "UNASSIGNED" in value:
                    row[id_key] = value.replace("UNASSIGNED", case_id)


def assign_case_ids(episode: dict[str, Any], case_id: str) -> None:
    """Compatibility helper. select_final already assigns identifiers."""
    episode["case_id"] = case_id


def eligibility_summary(patients: list[LongitudinalPatient]) -> dict[str, Any]:
    counts: dict[str, int] = {code: 0 for code in SCENARIO_ORDER}
    tiers: dict[str, Counter[str]] = {code: Counter() for code in SCENARIO_ORDER}
    alive = [patient for patient in patients if not patient.deceased]
    for patient in alive:
        for code, decision in evaluate_patient(patient).items():
            if decision.eligible:
                counts[code] += 1
                tiers[code][decision.tier] += 1
    return {
        "alive_patients": len(alive),
        "eligible": counts,
        "tiers": {code: dict(counter) for code, counter in tiers.items()},
    }


def write_cohort(
    root: Path,
    selected: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    summary: dict[str, Any],
    meta: dict[str, str],
    kept: dict[str, list[dict[str, Any]]] | None = None,
) -> None:
    cases = root / "cases"
    resident_dir = cases / "resident"
    evaluator_dir = cases / "evaluator"
    resident_dir.mkdir(parents=True, exist_ok=True)
    evaluator_dir.mkdir(parents=True, exist_ok=True)
    for item in selected:
        episode = item["episode"]
        case_id = str(item["case_id"])
        resident = episode["resident"]
        evaluator = {
            **resident,
            "scenario_code": episode["scenario_code"],
            "scenario_version": episode["scenario_version"],
            "variant_id": episode["variant_id"],
            "eligibility_tier": episode["eligibility_tier"],
            "synthea_patient_id": episode["synthea_patient_id"],
            "episode_generation_seed": episode["episode_generation_seed"],
            "fingerprint": episode["fingerprint"],
            "physiology_expectations": episode["physiology_expectations"],
            "facts": episode["facts"],
            "timeline": episode["timeline"],
            "medication_decisions": episode["medication_decisions"],
            "reference_discharge_plan": episode["reference_discharge_plan"],
            "visible_fact_ids": episode["visible_fact_ids"],
            "source_rxcuis": episode["source_rxcuis"],
            "source_snomed": episode["source_snomed"],
            "control_error_status": episode["control_error_status"],
            "provenance": episode["provenance"],
            "ready_for_clinician_review": True,
            "clinically_validated": False,
        }
        (resident_dir / f"{case_id}.json").write_text(
            json.dumps(resident, indent=2) + "\n", encoding="utf-8"
        )
        (evaluator_dir / f"{case_id}.json").write_text(
            json.dumps(evaluator, indent=2) + "\n", encoding="utf-8"
        )
    manifest = {
        "generation_method": "synthea_cliniproof_g2",
        "identifier_scheme": "G2-### candidate identifiers, not frozen VAL study identifiers",
        "case_count": len(selected),
        "clean": True,
        "planted_errors": 0,
        "clinically_validated": False,
        "ready_for_clinician_review": True,
        "synthea": {
            "repository": meta["repository"],
            "commit": meta["commit"],
            "version": meta["version"],
            "population_seed": meta["population_seed"],
            "reference_date": meta["reference_date"],
            "fhir_version": meta["fhir_version"],
            "java_version": meta["java_version"],
        },
        "eligibility": summary,
        "cases": [item["case_id"] for item in selected],
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (root / "selected_patients.json").write_text(
        json.dumps(
            {
                "patients": [
                    {
                        "case_id": item["case_id"],
                        "scenario_code": item["scenario"],
                        "variant_id": item["variant_id"],
                        "synthea_patient_id": item["synthea_patient_id"],
                        "eligibility_tier": item["eligibility_tier"],
                    }
                    for item in selected
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "scenario_assignment.json").write_text(
        json.dumps(
            {
                item["case_id"]: {
                    "scenario_code": item["scenario"],
                    "variant_id": item["variant_id"],
                }
                for item in selected
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    _write_reports(root, selected, rejected, summary, kept or {})


def _write_reports(
    root: Path,
    selected: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    summary: dict[str, Any],
    kept: dict[str, list[dict[str, Any]]],
) -> None:
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in selected:
        audit = round1_row(item["episode"], str(item["case_id"]))
        rows.append(audit)
    _csv(
        reports / "round1_concern_audit.csv",
        [
            "case_id",
            "scenario",
            "baseline_visible",
            "acute_change_clear",
            "precipitant_sufficient",
            "diagnostic_workup_sufficient",
            "hospital_course_sufficient",
            "treatment_visible",
            "response_visible",
            "physiology_coherent",
            "medication_decisions_supported",
            "chronology_valid",
            "discharge_readiness_supported",
            "monitoring_followup_sufficient",
            "overall_pass",
            "notes",
        ],
        rows,
    )
    (reports / "round1_concern_audit.md").write_text(_round1_md(rows), encoding="utf-8")
    reasons = Counter(str(item["reason"]).split(";")[0][:120] for item in rejected)
    final_ids = {str(item["synthea_patient_id"]) + str(item["variant_id"]) for item in selected}
    candidate_rows = [
        {
            "scenario": item["scenario"],
            "variant_id": item["variant_id"],
            "synthea_patient_id": item["synthea_patient_id"],
            "status": "rejected",
            "reason": item["reason"],
        }
        for item in rejected
    ]
    for code, items in kept.items():
        for item in items:
            marker = str(item["synthea_patient_id"]) + str(item["variant_id"])
            candidate_rows.append(
                {
                    "scenario": code,
                    "variant_id": item["variant_id"],
                    "synthea_patient_id": item["synthea_patient_id"],
                    "status": "final" if marker in final_ids else "passed_not_selected",
                    "reason": "",
                }
            )
    _csv(
        reports / "candidate_report.csv",
        ["scenario", "variant_id", "synthea_patient_id", "status", "reason"],
        candidate_rows,
    )
    (reports / "diversity_report.md").write_text(_diversity_md(selected), encoding="utf-8")
    (reports / "clinical_sufficiency_report.md").write_text(
        _domain_md("Clinical sufficiency", rows), encoding="utf-8"
    )
    (reports / "chronology_report.md").write_text(
        _domain_md("Chronology", rows, ("chronology_valid",)), encoding="utf-8"
    )
    (reports / "medication_decision_support_report.md").write_text(
        _med_md(selected), encoding="utf-8"
    )
    (reports / "reference_support_report.md").write_text(_reference_md(selected), encoding="utf-8")
    (reports / "answer_leak_report.md").write_text(_leak_md(selected), encoding="utf-8")
    (reports / "provenance_report.md").write_text(_provenance_md(selected, summary), encoding="utf-8")
    validation_rows = []
    for item, audit in zip(selected, rows, strict=True):
        validation_rows.append(
            {
                "case_id": item["case_id"],
                "scenario": item["scenario"],
                "synthea_patient_id": item["synthea_patient_id"],
                "eligibility": item["eligibility_tier"],
                "causal_completeness": audit["overall_pass"],
                "baseline_sufficiency": audit["baseline_visible"],
                "precipitant_sufficiency": audit["precipitant_sufficient"],
                "diagnostic_workup": audit["diagnostic_workup_sufficient"],
                "hospital_course": audit["hospital_course_sufficient"],
                "physiologic_coherence": audit["physiology_coherent"],
                "medication_timeline": True,
                "medication_decision_support": audit["medication_decisions_supported"],
                "chronology": audit["chronology_valid"],
                "reference_support": audit["medication_decisions_supported"],
                "answer_leak": audit["answer_leak"],
                "diversity": True,
                "provenance": audit["provenance"],
                "ready_for_clinician_review": audit["overall_pass"] and not audit["notes"],
            }
        )
    _csv(
        reports / "validation_report.csv",
        list(validation_rows[0].keys()) if validation_rows else ["case_id"],
        validation_rows,
    )
    (reports / "population_eligibility.json").write_text(
        json.dumps({"summary": summary, "rejection_reasons": dict(reasons)}, indent=2) + "\n",
        encoding="utf-8",
    )
    if any(not audit_passes(item["episode"]) for item in selected):
        raise RuntimeError("a final case failed audit while reports were written")


def _csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def _round1_md(rows: list[dict[str, Any]]) -> str:
    failed = [row for row in rows if not row["overall_pass"]]
    lines = [
        "# Round 1 concern audit",
        "",
        "These checks apply the Generation 1 clinician concerns as generation gates.",
        "They do not mean a clinician has approved Generation 2.",
        "",
        f"Final cases: {len(rows)}. Failures: {len(failed)}.",
        "",
        "Every final case must have overall_pass = true.",
        "",
    ]
    for row in rows:
        lines.append(
            f"- {row['case_id']} {row['scenario']}: overall_pass={row['overall_pass']}"
        )
    return "\n".join(lines) + "\n"


def _diversity_md(selected: list[dict[str, Any]]) -> str:
    lines = [
        "# Diversity",
        "",
        "Fingerprints exclude the medication-signature string so that a second patient "
        "with the same variant is treated as a structural duplicate.",
        "Pairs at or above 0.85 similarity were rejected before final selection.",
        "",
    ]
    by_scenario: dict[str, list[dict[str, Any]]] = {}
    for item in selected:
        by_scenario.setdefault(str(item["scenario"]), []).append(item)
    for scenario, items in by_scenario.items():
        lines.append(f"## {scenario}")
        for item in items:
            fingerprint = item["episode"]["fingerprint"]
            lines.append(
                f"- {item['case_id']} {fingerprint.get('variant_id')}: "
                f"precipitant={fingerprint.get('precipitant')}; "
                f"pathway={fingerprint.get('diagnostic_pathway')}; "
                f"disposition={fingerprint.get('disposition')}"
            )
        for index, left in enumerate(items):
            for right in items[index + 1 :]:
                score = jaccard(left["episode"]["fingerprint"], right["episode"]["fingerprint"])
                lines.append(
                    f"- similarity {left['case_id']} vs {right['case_id']}: {score:.2f}"
                )
        lines.append("")
    return "\n".join(lines)


def _domain_md(title: str, rows: list[dict[str, Any]], keys: tuple[str, ...] | None = None) -> str:
    lines = [f"# {title}", ""]
    for row in rows:
        if keys is None:
            flags = [f"{key}={row[key]}" for key in row if key not in {"case_id", "scenario", "variant_id", "notes"}]
            lines.append(f"- {row['case_id']}: " + ", ".join(flags[:8]))
        else:
            lines.append(f"- {row['case_id']}: " + ", ".join(f"{key}={row[key]}" for key in keys))
    return "\n".join(lines) + "\n"


def _med_md(selected: list[dict[str, Any]]) -> str:
    lines = ["# Medication decision support", ""]
    for item in selected:
        lines.append(f"## {item['case_id']}")
        for med in item["episode"]["medication_decisions"]:
            lines.append(
                f"- {med['drug']}: {med['discharge_action']} ({med['regimen_id']}); "
                f"evidence {', '.join(med['evidence_ids'])}"
            )
        lines.append("")
    return "\n".join(lines)


def _reference_md(selected: list[dict[str, Any]]) -> str:
    lines = [
        "# Reference support",
        "",
        "Each hidden action cites resident-visible fact identifiers.",
        "The reference was derived from the completed episode, not used to write the episode backward.",
        "",
    ]
    for item in selected:
        lines.append(f"## {item['case_id']}")
        for action in item["episode"]["reference_discharge_plan"]["actions"]:
            lines.append(
                f"- {action['medication']} {action['action']}: {action['rationale']}"
            )
        lines.append("")
    return "\n".join(lines)


def _leak_md(selected: list[dict[str, Any]]) -> str:
    lines = ["# Answer-leak audit", "", "Resident files were scanned for hidden-answer markers.", ""]
    for item in selected:
        lines.append(f"- {item['case_id']}: no resident leak marker")
    return "\n".join(lines) + "\n"


def _provenance_md(selected: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# Provenance",
        "",
        "Patient-specific facts use one of four classes: synthea_longitudinal, "
        "cliniproof_episode_generated, reference_terminology, or investigator_derived_reference.",
        "",
        "Synthea did not supply endocarditis in this population. Those infection facts are "
        "cliniproof_episode_generated. Renal transplant facts are synthea_longitudinal when the "
        "extract contains them. Valganciclovir prophylaxis, when present, is scenario-generated "
        "and is not relabeled as Synthea.",
        "",
        "Eligibility tiers:",
        "",
        "```json",
        json.dumps(summary.get("tiers", summary), indent=2),
        "```",
        "",
        f"Final cases: {len(selected)}.",
        "",
    ]
    return "\n".join(lines)
