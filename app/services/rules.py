"""Deterministic clinical conditionals with source-backed provenance.

Rules stay disabled until DailyMed or RxClass evidence is attached. Terminology
lookup alone does not enable a hard clinical rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.models.reference import ClinicalRule, RefDiagnosis, RefLabTest, RefMedication
from app.repositories.reference import list_enabled_rules, upsert_rule
from app.services.bootstrap import (
    DEFAULT_RULE_TEMPLATE_PATH,
    load_json_object,
    match_diagnosis,
    match_lab,
    match_medication,
)
from app.sources.dailymed import DailyMedClient
from app.sources.http import SOURCE_BASE_URLS
from app.sources.rxclass import RxClassClient
from app.utils.provenance import build_provenance


@dataclass(frozen=True)
class RuleViolation:
    rule_code: str
    severity: str
    message: str
    source_identifier: str | None


@dataclass(frozen=True)
class CaseSnapshot:
    age: int | None
    sex: str | None
    care_context: str | None
    icd10cm_codes: frozenset[str]
    rxcuis: frozenset[str]
    loinc_codes: frozenset[str]


def load_rule_templates(path: Any | None = None) -> list[dict[str, Any]]:
    raw = load_json_object(path or DEFAULT_RULE_TEMPLATE_PATH)
    templates = raw.get("templates", [])
    if not isinstance(templates, list):
        raise ValueError("rule_templates.templates must be a list")
    return [item for item in templates if isinstance(item, dict)]


def enable_rules_from_templates(
    session: Session,
    *,
    dailymed: DailyMedClient,
    rxclass: RxClassClient,
    template_path: Path | None = None,
) -> list[str]:
    """Upsert curated templates and enable only those with source evidence."""
    enabled: list[str] = []
    for template in load_rule_templates(template_path):
        values = _rule_values_from_template(session, template, dailymed=dailymed, rxclass=rxclass)
        if values is None:
            continue
        row = upsert_rule(session, values)
        if row.enabled:
            enabled.append(row.rule_code)
    return enabled


def evaluate_rules(session: Session, snapshot: CaseSnapshot) -> list[RuleViolation]:
    violations: list[RuleViolation] = []
    for rule in list_enabled_rules(session):
        violation = _evaluate_one(rule, snapshot)
        if violation is not None:
            violations.append(violation)
    return violations


def hard_violations(hits: list[RuleViolation]) -> list[RuleViolation]:
    return [item for item in hits if item.severity == "hard"]


def _evaluate_one(rule: ClinicalRule, snapshot: CaseSnapshot) -> RuleViolation | None:
    if not _applies_to_demographics(rule, snapshot):
        return None
    constraint = rule.constraint_json if isinstance(rule.constraint_json, dict) else {}
    action = str(constraint.get("action") or "")
    if action == "prohibit_coadministration":
        left = rule.input_rxcui
        right = rule.related_rxcui
        if left and right and left in snapshot.rxcuis and right in snapshot.rxcuis:
            return RuleViolation(
                rule.rule_code,
                rule.severity,
                f"Medications {left} and {right} must not be co-administered",
                rule.source_identifier,
            )
        return None
    if action == "require_lab":
        needed = rule.input_loinc_code or str(constraint.get("loinc_code") or "")
        if rule.input_rxcui and rule.input_rxcui in snapshot.rxcuis and needed:
            if needed not in snapshot.loinc_codes:
                return RuleViolation(
                    rule.rule_code,
                    rule.severity,
                    f"Medication {rule.input_rxcui} requires lab {needed}",
                    rule.source_identifier,
                )
        return None
    if action == "allow_with_diagnosis":
        if rule.input_rxcui and rule.input_rxcui in snapshot.rxcuis:
            wanted = rule.input_icd10cm_code
            if wanted and wanted not in snapshot.icd10cm_codes:
                return RuleViolation(
                    rule.rule_code,
                    rule.severity,
                    f"Medication {rule.input_rxcui} is not paired with diagnosis {wanted}",
                    rule.source_identifier,
                )
        return None
    return None


def _applies_to_demographics(rule: ClinicalRule, snapshot: CaseSnapshot) -> bool:
    if rule.age_min is not None and snapshot.age is not None and snapshot.age < rule.age_min:
        return False
    if rule.age_max is not None and snapshot.age is not None and snapshot.age > rule.age_max:
        return False
    if rule.sex is not None and snapshot.sex is not None:
        if rule.sex.casefold() != snapshot.sex.casefold():
            return False
    if rule.care_context is not None and snapshot.care_context is not None:
        if rule.care_context.casefold() != snapshot.care_context.casefold():
            return False
    return True


def _rule_values_from_template(
    session: Session,
    template: dict[str, Any],
    *,
    dailymed: DailyMedClient,
    rxclass: RxClassClient,
) -> dict[str, Any] | None:
    rule_code = str(template.get("rule_code") or "").strip()
    if rule_code == "":
        return None
    meds = _resolve_named_medications(session, _as_str_list(template.get("medication_names")))
    diagnoses = _resolve_named_diagnoses(session, _as_str_list(template.get("diagnosis_names")))
    labs = _resolve_named_labs(session, _as_str_list(template.get("lab_names")))
    evidence_needles = [item.casefold() for item in _as_str_list(template.get("evidence_needles"))]
    excerpts: list[str] = []
    source_identifier: str | None = None
    source_url: str | None = None
    rxclass_names: list[str] = []
    for medication in meds:
        try:
            for label in dailymed.labels_for_rxcui(medication.rxcui, limit=1):
                blob = " ".join(
                    part
                    for part in (
                        label.indication_text,
                        label.contraindications_text,
                        label.warnings_text,
                        label.dosage_text,
                    )
                    if part
                )
                if blob:
                    excerpts.append(blob)
                    source_identifier = label.set_id
                    source_url = f"{SOURCE_BASE_URLS['DAILYMED']}/spls/{label.set_id}.xml"
        except Exception:
            pass
        try:
            for hit in sorted(
                rxclass.classes_for_rxcui(medication.rxcui),
                key=lambda item: (item.class_id, item.class_name),
            ):
                rxclass_names.append(hit.class_name)
        except Exception:
            pass
    combined = " ".join(excerpts).casefold()
    evidence_mode = str(template.get("evidence_mode") or "all").casefold()
    if evidence_needles and evidence_mode == "any":
        label_evidence = any(needle in combined for needle in evidence_needles)
    else:
        label_evidence = bool(evidence_needles) and all(
            needle in combined for needle in evidence_needles
        )
    class_evidence = False
    if not label_evidence and rxclass_names:
        joined_classes = " ".join(rxclass_names).casefold()
        class_evidence = any(needle in joined_classes for needle in evidence_needles)
        if class_evidence and source_identifier is None:
            matching = [
                name
                for name in rxclass_names
                if any(needle in name.casefold() for needle in evidence_needles)
            ]
            source_identifier = matching[0] if matching else rxclass_names[0]
            source_url = SOURCE_BASE_URLS["RXCLASS"]
    has_label_evidence = label_evidence or class_evidence
    severity = str(template.get("severity") or "soft")
    raw_constraint = template.get("constraint")
    constraint: dict[str, Any] = raw_constraint if isinstance(raw_constraint, dict) else {}
    input_rxcui = meds[0].rxcui if meds else None
    related_rxcui = meds[1].rxcui if len(meds) > 1 else None
    input_icd = diagnoses[0].icd10cm_code if diagnoses else None
    input_loinc = labs[0].loinc_code if labs else None
    action = str(constraint.get("action") or "")
    enable = False
    if action == "prohibit_coadministration":
        enable = has_label_evidence and input_rxcui is not None and related_rxcui is not None
    elif action == "require_lab":
        enable = has_label_evidence and input_rxcui is not None and input_loinc is not None
    elif action == "allow_with_diagnosis":
        enable = has_label_evidence and input_rxcui is not None and input_icd is not None
    if label_evidence:
        evidence_source = "DAILYMED"
    elif class_evidence:
        evidence_source = "RXCLASS"
    else:
        evidence_source = "CURATED_PENDING"
    provenance = build_provenance(evidence_source)
    excerpt = excerpts[0][:1000] if excerpts else None
    return {
        "rule_code": rule_code,
        "rule_type": str(template.get("rule_type") or "unspecified"),
        "severity": severity if severity in {"hard", "soft"} else "soft",
        "enabled": enable,
        "input_icd10cm_code": input_icd,
        "input_rxcui": input_rxcui,
        "input_loinc_code": input_loinc,
        "related_rxcui": related_rxcui,
        "age_min": None,
        "age_max": None,
        "sex": None,
        "care_context": None,
        "constraint_json": constraint,
        "logic_notes": str(template.get("logic_notes") or "") or None,
        "source_identifier": source_identifier,
        "source_url": source_url,
        "evidence_excerpt": excerpt,
        "source_system": provenance["source_system"] if enable else None,
        "source_version": provenance["source_version"] if enable else None,
        "retrieved_at": provenance["retrieved_at"] if enable else None,
    }


def _resolve_named_medications(session: Session, names: list[str]) -> list[RefMedication]:
    found: list[RefMedication] = []
    seen: set[str] = set()
    for name in names:
        row = match_medication(session, name)
        if row is None or row.rxcui in seen:
            continue
        seen.add(row.rxcui)
        found.append(row)
    return found


def _resolve_named_diagnoses(session: Session, names: list[str]) -> list[RefDiagnosis]:
    found: list[RefDiagnosis] = []
    for name in names:
        row = match_diagnosis(session, name)
        if row is not None:
            found.append(row)
    return found


def _resolve_named_labs(session: Session, names: list[str]) -> list[RefLabTest]:
    found: list[RefLabTest] = []
    for name in names:
        row = match_lab(session, name)
        if row is not None:
            found.append(row)
    return found


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            result.append(text)
    return result
