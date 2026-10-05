"""Recover the frozen 48-case set as clean resident charts.

The resident exports in VAL-701–VAL-724 and VAL-801–VAL-824 are the charts
after error injection, and they include the discharge list. Each error-bearing
investigator record stores the pre-injection medication snapshot. Clean controls
have no injection; their chart is already the clean source.

This module restores that source, hides the discharge list, and classifies
clinical problems that were already in the clean chart. It does not generate
replacement cases.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from app.services.clinical_coherence import implausible_lab_errors, indication_matches_problems
from app.services.medication_decisions import _resolve_indication, public_action

REPO_ROOT = Path(__file__).resolve().parents[2]
BALANCED_RESIDENT = (
    REPO_ROOT / "data" / "case_sets" / "balanced" / "resident_validation_cases.json"
)
BALANCED_INVESTIGATOR = (
    REPO_ROOT / "data" / "case_sets" / "balanced" / "investigator_answer_key.json"
)
BALANCED_PLAN = REPO_ROOT / "data" / "case_sets" / "balanced" / "batch_plan.json"
SEED_RESIDENT = (
    REPO_ROOT / "data" / "case_sets" / "seed_guided" / "resident_validation_cases.json"
)
SEED_INVESTIGATOR = (
    REPO_ROOT / "data" / "case_sets" / "seed_guided" / "investigator_answer_key.json"
)
SEED_PLAN = REPO_ROOT / "data" / "case_sets" / "seed_guided" / "batch_plan.json"

CLEAN_READY = "CLEAN_READY"
CLEAN_BUT_NEEDS_MINOR_FIX = "CLEAN_BUT_NEEDS_MINOR_FIX"
CLINICALLY_INCONSISTENT = "CLINICALLY_INCONSISTENT"
CANNOT_RECONSTRUCT = "CANNOT_RECONSTRUCT"

_LEAK_INSTRUCTION = "exactly as listed"
_STOP_INSTRUCTION = "was stopped during this admission"
_GENERIC_STOP = "stopped during this admission"
# Same warfarin monitoring text the generator writes, and the same text still
# present on the untouched clean control VAL-710. The deleted row body was not
# archived; only this template and the case's own INR lab name are used.
_WARFARIN_MONITORING_FREQUENCY = "within 7 days, then by the INR result"
_WARFARIN_MONITORING_TRIGGER = (
    "Repeat INR sooner if bleeding or a new interacting medicine occurs"
)
_WARFARIN_MONITORING_SERVICE = "laboratory monitoring"
_RESTORED_FIELDS = (
    "drug",
    "dose",
    "route",
    "frequency",
    "status",
    "quantity_or_days",
    "monitoring",
    "held_reason",
)


def recover_clean_balanced_set(output_dir: Path) -> dict[str, Any]:
    """Write one resident file and one evaluator file for each original case."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [_recover_case(item) for item in _load_sources()]
    for row in rows:
        case_id = row["case_id"]
        (output_dir / f"{case_id}_resident.json").write_text(
            json.dumps(row["resident"], indent=2) + "\n",
            encoding="utf-8",
        )
        (output_dir / f"{case_id}_evaluator.json").write_text(
            json.dumps(row["evaluator"], indent=2) + "\n",
            encoding="utf-8",
        )
    summary = _summary(rows)
    (output_dir / "AUDIT.md").write_text(_audit_markdown(rows, summary), encoding="utf-8")
    return summary


def _load_sources() -> list[dict[str, Any]]:
    loaded: list[dict[str, Any]] = []
    for resident_path, investigator_path, plan_path in (
        (BALANCED_RESIDENT, BALANCED_INVESTIGATOR, BALANCED_PLAN),
        (SEED_RESIDENT, SEED_INVESTIGATOR, SEED_PLAN),
    ):
        resident = json.loads(resident_path.read_text(encoding="utf-8"))
        investigator = json.loads(investigator_path.read_text(encoding="utf-8"))
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        resident_by_id = {item["case_id_code"]: item for item in resident["cases"]}
        plan_by_id = {item["validation_case_id"]: item for item in plan["cases"]}
        for record in investigator["cases"]:
            case_id = record["validation_case_id"]
            loaded.append(
                {
                    "case_id": case_id,
                    "resident": resident_by_id[case_id],
                    "investigator": record,
                    "plan": plan_by_id[case_id],
                    "master_seed": plan["master_seed"],
                }
            )
    return loaded


def _recover_case(source: dict[str, Any]) -> dict[str, Any]:
    case_id = source["case_id"]
    investigator = source["investigator"]
    plan_row = source["plan"]
    error = investigator.get("error") or {}
    snapshot = error.get("clean_expected_state")
    is_control = error.get("control_error_status") == "clean_control"
    changes = error.get("intentional_changes") or []
    if not isinstance(changes, list):
        changes = []
    seed = _seed(source, changes)
    chart = deepcopy(source["resident"])
    recovery = "clean_control_chart" if is_control else ""
    notes: list[str] = []
    if is_control:
        recovery = "clean_control_chart"
    elif isinstance(snapshot, dict) and isinstance(snapshot.get("medications"), list):
        chart["CaseMedication"] = _align_medications(
            chart.get("CaseMedication") or [],
            snapshot["medications"],
        )
        _restore_side_effects(chart, changes, case_id, notes)
        recovery = "clean_snapshot"
    else:
        recovery = "cannot_reconstruct"
    reference = _reference_plan(chart, snapshot if isinstance(snapshot, dict) else None)
    issues = [] if recovery == "cannot_reconstruct" else _clinical_issues(chart, reference)
    minor = [item for item in issues if item.startswith("minor:")]
    blocking = [item for item in issues if not item.startswith("minor:")]
    if minor and not blocking:
        _apply_minor_fixes(chart, reference, minor)
        notes.extend(minor)
        issues = _clinical_issues(chart, reference)
        blocking = [item for item in issues if not item.startswith("minor:")]
        minor = [item for item in issues if item.startswith("minor:")]
    status = _status(recovery, blocking, minor or notes)
    resident = _resident_view(chart)
    evaluator = deepcopy(resident)
    evaluator["reference_discharge_plan"] = reference
    return {
        "case_id": case_id,
        "seed": seed,
        "scenario": investigator.get("scenario") or plan_row.get("scenario"),
        "profile": investigator.get("clinical_profile") or plan_row.get("clinical_profile"),
        "recovery": recovery,
        "error_removed": (not is_control) and recovery == "clean_snapshot",
        "leakage_removed": _leakage_removed(resident),
        "cleanup": notes,
        "issues": blocking,
        "status": status,
        "resident": resident,
        "evaluator": evaluator,
    }


def _seed(source: dict[str, Any], changes: list[Any]) -> str:
    for change in changes:
        if isinstance(change, dict) and change.get("seed"):
            return str(change["seed"])
    plan = source["plan"]
    profile = plan.get("clinical_profile") or ""
    base = f"{source['master_seed']}:{plan['sequence']}:{plan['scenario']}"
    return f"{base}:{profile}" if profile else base


def _align_medications(
    resident_rows: list[dict[str, Any]],
    snapshot_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Replace injected medication fields with the stored pre-injection rows."""
    unused = [deepcopy(row) for row in resident_rows]
    aligned: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    for snap in snapshot_rows:
        match = _pop_exact(unused, snap.get("drug"), snap.get("context"))
        if match is None:
            pending.append(snap)
            continue
        aligned.append(_copy_snapshot_fields(match, snap, resident_rows))
    snapshot_discharge = {
        row.get("drug") for row in snapshot_rows if row.get("context") == "discharge"
    }
    for snap in pending:
        match = None
        if snap.get("context") == "discharge":
            match = _pop_substituted_discharge(unused, snapshot_discharge)
        if match is None:
            aligned.append(_row_from_snapshot(snap, resident_rows))
            continue
        aligned.append(_copy_snapshot_fields(match, snap, resident_rows))
    return aligned


def _pop_exact(
    unused: list[dict[str, Any]], drug: str | None, context: str | None
) -> dict[str, Any] | None:
    for index, row in enumerate(unused):
        if row.get("drug") == drug and row.get("context") == context:
            return unused.pop(index)
    return None


def _pop_substituted_discharge(
    unused: list[dict[str, Any]], snapshot_discharge: set[str | None]
) -> dict[str, Any] | None:
    for index, row in enumerate(unused):
        if row.get("context") == "discharge" and row.get("drug") not in snapshot_discharge:
            return unused.pop(index)
    return None


def _copy_snapshot_fields(
    match: dict[str, Any], snap: dict[str, Any], resident_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    for field in _RESTORED_FIELDS:
        if field in snap:
            match[field] = snap[field]
    if snap.get("rxcui"):
        match["source_reference"] = f"RXCUI:{snap['rxcui']}"
    sibling = next(
        (
            row
            for row in resident_rows
            if row.get("drug") == snap.get("drug") and row.get("indication")
        ),
        None,
    )
    if sibling is not None and sibling.get("indication"):
        match["indication"] = sibling["indication"]
    return match


def _row_from_snapshot(
    snap: dict[str, Any], resident_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    sibling = next(
        (row for row in resident_rows if row.get("drug") == snap.get("drug")),
        None,
    )
    base = deepcopy(sibling) if sibling is not None else {}
    base.update(
        {
            "context": snap.get("context"),
            "drug": snap.get("drug"),
            "reported_name": snap.get("drug"),
            "dose": snap.get("dose"),
            "route": snap.get("route"),
            "frequency": snap.get("frequency"),
            "status": snap.get("status"),
            "quantity_or_days": snap.get("quantity_or_days"),
            "monitoring": snap.get("monitoring"),
            "held_reason": snap.get("held_reason"),
            "source_reference": (
                f"RXCUI:{snap['rxcui']}" if snap.get("rxcui") else base.get("source_reference")
            ),
            "source_type": base.get("source_type") or "reference",
        }
    )
    return base


def _restore_side_effects(
    chart: dict[str, Any],
    changes: list[Any],
    case_id: str,
    notes: list[str],
) -> None:
    for change in changes:
        if not isinstance(change, dict):
            continue
        field = change.get("changed_field")
        expected = change.get("clean_expected_state")
        if field == "restart_plan" and isinstance(expected, dict):
            _restore_restart(chart, change.get("drug"), expected)
        elif field == "followup" and isinstance(expected, list):
            _restore_followups(chart, expected, case_id)
        elif field == "monitoring" and isinstance(expected, dict):
            _restore_monitoring(chart, change.get("drug"), expected, case_id, notes)


def _restore_restart(chart: dict[str, Any], drug: str | None, expected: dict[str, Any]) -> None:
    goals = [item for item in expected.get("target_or_goal") or [] if item]
    goal = goals[0] if goals else None
    if goal and drug:
        for row in chart.get("CaseMedication") or []:
            if row.get("drug") == drug and not row.get("target_or_goal"):
                row["target_or_goal"] = goal
    texts = [item for item in expected.get("instructions") or [] if item]
    instructions = chart.setdefault("CaseInstruction", [])
    present = {item.get("instruction_text") for item in instructions}
    for text in texts:
        if text in present:
            continue
        instructions.append(
            {
                "instruction_id": None,
                "case_id": chart.get("case_id_code"),
                "category": "medications",
                "instruction_text": text,
                "source_type": "recovered_clean_chart",
                "source_reference": None,
            }
        )


def _restore_followups(chart: dict[str, Any], expected: list[Any], case_id: str) -> None:
    current = chart.setdefault("CaseFollowup", [])
    present = {(item.get("item"), item.get("timing"), item.get("with_service")) for item in current}
    for index, item in enumerate(expected, start=len(current) + 1):
        if not isinstance(item, dict):
            continue
        key = (item.get("item"), item.get("timing"), item.get("with_service"))
        if key in present:
            continue
        current.append(
            {
                "followup_id": f"FU-{case_id}-{index:03d}",
                "case_id": case_id,
                "item": item.get("item"),
                "timing": item.get("timing"),
                "with_service": item.get("with_service"),
                "source_reference": None,
            }
        )


def _restore_monitoring(
    chart: dict[str, Any],
    drug: str | None,
    expected: dict[str, Any],
    case_id: str,
    notes: list[str],
) -> None:
    monitoring_text = expected.get("medication_monitoring")
    if drug and monitoring_text:
        for row in chart.get("CaseMedication") or []:
            if row.get("drug") == drug and row.get("context") == "discharge":
                row["monitoring"] = monitoring_text
    if chart.get("CaseMonitoring"):
        return
    if monitoring_text != "INR check":
        notes.append("minor: monitoring row body was not archived and was not INR")
        return
    lab_name = _inr_lab_name(chart)
    if lab_name is None:
        notes.append("minor: INR monitoring id was archived without an INR lab on the chart")
        return
    chart["CaseMonitoring"] = [
        {
            "monitoring_id": f"MON-{case_id}-001",
            "case_id": case_id,
            "parameter": lab_name,
            "frequency": _WARFARIN_MONITORING_FREQUENCY,
            "target": None,
            "trigger_for_action": _WARFARIN_MONITORING_TRIGGER,
            "duration": None,
            "responsible_service": _WARFARIN_MONITORING_SERVICE,
            "source_reference": None,
        }
    ]
    notes.append(
        "minor: restored the deleted INR monitoring task from this case's INR lab "
        "and the generator's warfarin monitoring text"
    )


def _inr_lab_name(chart: dict[str, Any]) -> str | None:
    for lab in chart.get("CaseLab") or []:
        name = str(lab.get("test_name") or "")
        if "inr" in name.casefold():
            return name
    return None


def _reference_plan(
    chart: dict[str, Any], snapshot: dict[str, Any] | None
) -> dict[str, Any]:
    meds = chart.get("CaseMedication") or []
    by_drug_context = {(row.get("drug"), row.get("context")): row for row in meds}
    stored_plans = [] if snapshot is None else snapshot.get("plans") or []
    medications: list[dict[str, Any]] = []
    if stored_plans:
        for plan in stored_plans:
            drug = plan.get("drug")
            source = (
                by_drug_context.get((drug, "discharge"))
                or by_drug_context.get((drug, "inpatient"))
                or by_drug_context.get((drug, "home"))
                or {}
            )
            medications.append(
                _plan_entry(
                    drug,
                    plan.get("decision"),
                    plan.get("decision_reason"),
                    source,
                )
            )
    else:
        medications.extend(_plans_from_clean_chart(meds))
    return {
        "medications": medications,
        "monitoring_requirements": [
            {
                "parameter": item.get("parameter"),
                "frequency": item.get("frequency"),
                "target": item.get("target"),
                "duration": item.get("duration"),
            }
            for item in chart.get("CaseMonitoring") or []
        ],
        "follow_up_requirements": [
            {
                "item": item.get("item"),
                "timing": item.get("timing"),
                "with_service": item.get("with_service"),
            }
            for item in chart.get("CaseFollowup") or []
        ],
    }


def _plan_entry(
    drug: str | None,
    decision: str | None,
    reason: str | None,
    source: dict[str, Any],
) -> dict[str, Any]:
    return {
        "medication": drug,
        "action": public_action(decision) if decision else _action_from_row(source),
        "dose": source.get("dose"),
        "route": source.get("route"),
        "frequency": source.get("frequency"),
        "duration": source.get("quantity_or_days"),
        "indication": source.get("indication"),
        "rationale": reason,
        "monitoring": source.get("monitoring"),
    }


def _plans_from_clean_chart(meds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Clean controls did not archive plan rows. Read the action from the chart."""
    by_drug: dict[str, dict[str, dict[str, Any]]] = {}
    for row in meds:
        drug = row.get("drug")
        context = row.get("context")
        if not drug or not context:
            continue
        by_drug.setdefault(drug, {})[context] = row
    entries: list[dict[str, Any]] = []
    for drug, contexts in by_drug.items():
        home = contexts.get("home")
        inpatient = contexts.get("inpatient")
        discharge = contexts.get("discharge")
        source = discharge or inpatient or home or {}
        if discharge is not None and home is not None:
            same = all(
                (home.get(field) or None) == (discharge.get(field) or None)
                for field in ("dose", "route", "frequency")
            )
            decision = "continue" if same else "dose_change"
            reason = (
                "Home and discharge rows in the clean chart match."
                if same
                else "Home and discharge rows in the clean chart differ."
            )
        elif discharge is not None:
            decision = "new_start"
            reason = "The clean chart starts this medicine during the admission."
        elif home is not None or inpatient is not None:
            decision = "stop"
            reason = "The clean chart does not continue this medicine at discharge."
        else:
            continue
        entries.append(_plan_entry(drug, decision, reason, source))
    return entries


def _action_from_row(source: dict[str, Any]) -> str:
    if source.get("context") == "discharge":
        return "continue"
    return "stop"


def _resident_view(chart: dict[str, Any]) -> dict[str, Any]:
    view = deepcopy(chart)
    view["CaseMedication"] = [
        row
        for row in view.get("CaseMedication") or []
        if row.get("context") != "discharge"
    ]
    view["CaseInstruction"] = [
        row
        for row in view.get("CaseInstruction") or []
        if not _instruction_leaks(row.get("instruction_text"))
    ]
    view.pop("reference_discharge_plan", None)
    return view


def _instruction_leaks(text: str | None) -> bool:
    lowered = (text or "").casefold()
    return _LEAK_INSTRUCTION in lowered or _STOP_INSTRUCTION in lowered


def _leakage_removed(resident: dict[str, Any]) -> bool:
    if "reference_discharge_plan" in resident:
        return False
    for row in resident.get("CaseMedication") or []:
        if row.get("context") == "discharge":
            return False
    blob = json.dumps(resident).casefold()
    if _LEAK_INSTRUCTION in blob or "reference_discharge_plan" in blob:
        return False
    return True


def _diagnosis_names(chart: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for row in chart.get("CaseDiagnosis") or []:
        if row.get("diagnosis") and row["diagnosis"] not in names:
            names.append(row["diagnosis"])
    history = (chart.get("ClinicalCase") or {}).get("medical_history") or []
    for item in history:
        if item and item not in names:
            names.append(item)
    admission = (chart.get("ClinicalCase") or {}).get("admission_dx")
    if admission and admission not in names:
        names.append(admission)
    return names


def _clinical_issues(chart: dict[str, Any], reference: dict[str, Any]) -> list[str]:
    names = _diagnosis_names(chart)
    issues: list[str] = []
    meds = chart.get("CaseMedication") or []
    drug_rows: dict[str, list[dict[str, Any]]] = {}
    for row in meds:
        if row.get("drug"):
            drug_rows.setdefault(row["drug"], []).append(row)
    continued = {
        item.get("medication")
        for item in reference.get("medications") or []
        if item.get("action") in {"continue", "start", "change", "restart"}
    }
    anticoagulants = []
    for drug, rows in drug_rows.items():
        indication = next((row.get("indication") for row in rows if row.get("indication")), None)
        held = " ".join(row.get("held_reason") or "" for row in rows)
        active = any(row.get("status") in {"home", "active", "discharge"} for row in rows)
        problem = _indication_issue(
            drug,
            indication,
            names,
            drug in continued or active,
            held,
        )
        if problem:
            issues.append(problem)
        if any(token in drug.casefold() for token in ("warfarin", "apixaban", "enoxaparin")):
            if drug in continued or any(row.get("context") == "discharge" for row in rows):
                anticoagulants.append(drug)
    oral = [drug for drug in anticoagulants if "enoxaparin" not in drug.casefold()]
    if len({drug.casefold() for drug in oral}) > 1:
        issues.append("two oral anticoagulants are both continued")
    warfarin = any("warfarin" in drug.casefold() for drug in drug_rows)
    if not warfarin and _has_inr(chart):
        issues.append("minor: INR is present without warfarin")
    for lab in chart.get("CaseLab") or []:
        value = lab.get("value")
        try:
            number = None if value is None else float(value)
        except (TypeError, ValueError):
            number = None
        issues.extend(
            implausible_lab_errors(lab.get("test_name"), number, lab.get("unit"))
        )
    return issues


def _indication_issue(
    drug: str,
    indication: str | None,
    diagnoses: list[str],
    needs_indication: bool,
    held_reason: str,
) -> str | None:
    if not needs_indication:
        chart = " ".join(diagnoses).casefold() + " " + held_reason.casefold()
        stop_tokens = ("bleed", "hemorrhage", "creatinine", "hypotension", "potassium")
        if _GENERIC_STOP in held_reason.casefold() and not any(
            token in chart for token in stop_tokens
        ):
            return f"{drug} is stopped without a clinical reason on the chart"
        return None
    supported, _how = _resolve_indication(drug.casefold(), diagnoses)
    supported = supported or _special_case_indication(drug, diagnoses)
    if supported is None and _context_supports(drug, diagnoses):
        return None
    if indication and "not a treatment for the admission diagnosis" in indication.casefold():
        return None
    if supported and indication and indication_matches_problems(indication, [supported]):
        return None
    if supported and indication and not indication_matches_problems(indication, [supported]):
        return f"minor: retarget {drug} indication to {supported}"
    if supported is None:
        return f"{drug} has no supported indication on this case"
    return None


def _special_case_indication(drug: str, diagnoses: list[str]) -> str | None:
    """Acceptance rules already implemented by the original indication helper."""
    blob = drug.casefold()
    for name in diagnoses:
        lowered = name.casefold()
        if any(token in blob for token in ("metoprolol", "carvedilol")) and (
            "atrial fibrillation" in lowered or "heart failure" in lowered
        ):
            return name
        if "aspirin" in blob and any(
            token in lowered for token in ("ischemic", "atherosclerotic", "coronary", "infarct")
        ):
            return name
        if "enoxaparin" in blob and any(
            token in lowered for token in ("fibrillation", "fracture", "thromb")
        ):
            return name
    return None


def _context_supports(drug: str, diagnoses: list[str]) -> bool:
    blob = drug.casefold()
    text = " ".join(diagnoses).casefold()
    if "insulin" in blob and "diabetes" in text:
        return True
    if "pantoprazole" in blob and any(
        token in text for token in ("gastro", "bleed", "hemorrhage", "reflux")
    ):
        return True
    if "albuterol" in blob:
        return True
    return False


def _has_inr(chart: dict[str, Any]) -> bool:
    for lab in chart.get("CaseLab") or []:
        if "inr" in str(lab.get("test_name") or "").casefold():
            return True
    for row in chart.get("CaseMonitoring") or []:
        if "inr" in str(row.get("parameter") or "").casefold():
            return True
    for row in chart.get("CaseMedication") or []:
        if "inr" in str(row.get("monitoring") or "").casefold():
            return True
    return False


def _apply_minor_fixes(
    chart: dict[str, Any], reference: dict[str, Any], minor: list[str]
) -> None:
    if any(item.startswith("minor: INR") for item in minor):
        chart["CaseLab"] = [
            row
            for row in chart.get("CaseLab") or []
            if "inr" not in str(row.get("test_name") or "").casefold()
        ]
        chart["CaseMonitoring"] = [
            row
            for row in chart.get("CaseMonitoring") or []
            if "inr" not in str(row.get("parameter") or "").casefold()
        ]
        for row in chart.get("CaseMedication") or []:
            if "inr" in str(row.get("monitoring") or "").casefold():
                row["monitoring"] = None
        reference["monitoring_requirements"] = [
            item
            for item in reference.get("monitoring_requirements") or []
            if "inr" not in str(item.get("parameter") or "").casefold()
        ]
    for item in minor:
        if not item.startswith("minor: retarget "):
            continue
        _retarget_indication(chart, reference, item)


def _retarget_indication(chart: dict[str, Any], reference: dict[str, Any], issue: str) -> None:
    # "minor: retarget {drug} indication to {diagnosis}"
    marker = " indication to "
    if marker not in issue:
        return
    left, diagnosis = issue.split(marker, 1)
    drug = left.removeprefix("minor: retarget ").strip()
    for row in chart.get("CaseMedication") or []:
        if row.get("drug") == drug:
            row["indication"] = diagnosis
    for item in reference.get("medications") or []:
        if item.get("medication") == drug:
            item["indication"] = diagnosis


def _status(recovery: str, blocking: list[str], notes: list[str]) -> str:
    if recovery == "cannot_reconstruct":
        return CANNOT_RECONSTRUCT
    if blocking:
        return CLINICALLY_INCONSISTENT
    if notes:
        return CLEAN_BUT_NEEDS_MINOR_FIX
    return CLEAN_READY


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    def count(status: str) -> int:
        return sum(1 for row in rows if row["status"] == status)

    recovered = sum(
        1 for row in rows if row["recovery"] in {"clean_snapshot", "clean_control_chart"}
    )
    return {
        "cases": len(rows),
        "recovered_from_clean_source": recovered,
        "reconstructed_from_seed": sum(
            1 for row in rows if row["recovery"] == "seed_reconstruction"
        ),
        "minor_cleanup": sum(1 for row in rows if row["cleanup"]),
        "clinically_inconsistent": count(CLINICALLY_INCONSISTENT),
        "unrecoverable": count(CANNOT_RECONSTRUCT),
        "ready_for_review": count(CLEAN_READY) + count(CLEAN_BUT_NEEDS_MINOR_FIX),
        "clean_ready": count(CLEAN_READY),
        "minor_status": count(CLEAN_BUT_NEEDS_MINOR_FIX),
    }


def _audit_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# Clean recovery of the original 48-case set",
        "",
        "Original frozen files were not overwritten. Each case was recovered from",
        "its archived clean chart: the pre-injection snapshot for error-bearing",
        "cases, and the resident chart itself for clean controls. No case was",
        "regenerated from a new seed draw.",
        "",
        "| Case | Original seed | Scenario | Error injection removed | "
        "Answer leakage removed | Clinical cleanup | Final status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        cleanup = "; ".join(row["cleanup"] + row["issues"]) or "none"
        lines.append(
            "| {case} | {seed} | {scenario} | {removed} | {leak} | {cleanup} | {status} |".format(
                case=row["case_id"],
                seed=row["seed"],
                scenario=row["scenario"],
                removed="yes" if row["error_removed"] else "not injected",
                leak="yes" if row["leakage_removed"] else "no",
                cleanup=cleanup.replace("|", "/"),
                status=row["status"],
            )
        )
    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Recovered directly from the clean source: {summary['recovered_from_clean_source']}",
            f"- Reconstructed by rerunning the seed: {summary['reconstructed_from_seed']}",
            f"- Requiring minor cleanup: {summary['minor_cleanup']}",
            f"- Clinically inconsistent: {summary['clinically_inconsistent']}",
            f"- Unrecoverable: {summary['unrecoverable']}",
            f"- Ready for expert review: {summary['ready_for_review']}",
            "",
            "Ready means the injected error and the discharge-answer wording are gone,",
            "and the remaining chart does not have a blocking clinical inconsistency.",
            "Cases marked clinically inconsistent are still exported, without a",
            "rewritten diagnosis or a replacement case.",
            "",
        ]
    )
    return "\n".join(lines)
