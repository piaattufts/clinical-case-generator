"""Clinician-facing case-set overview pages derived from current study files.

The rendered pages describe clinical composition. They do not copy answer-key
fields (error category, control flag, or intended action) into the case map.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
BALANCED_DIR = REPO_ROOT / "data" / "case_sets" / "balanced"
SEED_DIR = REPO_ROOT / "data" / "case_sets" / "seed_guided"
SCENARIOS_PATH = REPO_ROOT / "data" / "bootstrap" / "scenarios.json"
ARCHETYPES_PATH = REPO_ROOT / "data" / "seed_cases" / "blueprints" / "archetypes.json"

BALANCED_FAMILIES: tuple[tuple[str, str, str], ...] = (
    ("HF_INPATIENT", "Heart failure", "Decompensation, diuresis, and medication adjustment"),
    ("AF_ANTICOAGULATION", "Atrial fibrillation", "Rate control and anticoagulation"),
    (
        "HTN_INPATIENT",
        "Hypertension",
        "Symptomatic or severe hypertension and medication transitions",
    ),
    ("T2DM_INPATIENT", "Type 2 diabetes", "Inpatient hyperglycemia and discharge therapy"),
    ("CAP_INPATIENT", "Pneumonia", "Acute infection and short-course medication transitions"),
)

SEED_WORKFLOWS: tuple[tuple[str, str], ...] = (
    (
        "MEDREC_UNCERTAIN_HISTORY",
        "Incomplete history, collateral reconciliation, and discharge-list verification",
    ),
    (
        "HF_DECOMPENSATION",
        "Diuresis, renal or electrolyte changes, and medication holds or adjustment",
    ),
    (
        "OPAT_ENDOCARDITIS",
        "Intravenous antibiotics, line care, monitoring, and infectious-diseases follow-up",
    ),
    (
        "TRANSPLANT_CMV",
        "Antiviral treatment, immunosuppression management, and monitoring",
    ),
    (
        "POSTOP_ANTICOAGULATION",
        "Surgery, interruption or resumption of anticoagulation, and rehabilitation",
    ),
    (
        "GI_BLEED_ACUTE_CHANGE",
        "Bleeding stabilization, medication holds, and restart decisions",
    ),
)

_LEAKY = ("intended", "intentional", "omitted", "should stop", "must be stopped")
_PROFILE_PREFIXES = (
    "HF_DECOMP_",
    "MEDREC_",
    "OPAT_",
    "TRANSPLANT_",
    "POSTOP_",
    "GI_BLEED_",
    "HF_",
    "AF_",
    "HTN_",
    "T2DM_",
    "CAP_",
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(path)
    return payload


def _profiles_by_code(kind: str) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    if kind == "balanced":
        raw = _load(SCENARIOS_PATH)
        families = raw.get("scenarios") or []
    else:
        raw = _load(ARCHETYPES_PATH)
        families = raw.get("archetypes") or []
    if not isinstance(families, list):
        raise TypeError(kind)
    for family in families:
        if not isinstance(family, dict):
            continue
        profiles = family.get("clinical_profiles") or []
        if not isinstance(profiles, list):
            continue
        for profile in profiles:
            if isinstance(profile, dict) and profile.get("code"):
                found[str(profile["code"])] = profile
    return found


def _family_label(kind: str, code: str) -> str:
    if kind == "balanced":
        for family_code, label, _detail in BALANCED_FAMILIES:
            if family_code == code:
                return label
    else:
        raw = _load(ARCHETYPES_PATH)
        for archetype in raw.get("archetypes") or []:
            if isinstance(archetype, dict) and archetype.get("code") == code:
                return str(archetype.get("seed_archetype_name") or code)
    return code.replace("_", " ").title()


_ACRONYMS = {
    "ace": "ACE",
    "aki": "AKI",
    "ccb": "CCB",
    "cmv": "CMV",
    "id": "ID",
    "inr": "INR",
    "mmf": "MMF",
    "ppi": "PPI",
}
_DROP_PROFILE_WORDS = frozenset({"omitted", "missing"})
_PROFILE_PHRASES = {
    "id followup": "infectious-diseases follow-up",
    "parenteral therapy": "parenteral antibiotic course",
}


def _human_profile(code: str) -> str:
    rest = code
    for prefix in _PROFILE_PREFIXES:
        if rest.startswith(prefix):
            rest = rest[len(prefix) :]
            break
    tokens = [
        token
        for token in rest.replace("_", " ").split()
        if token.casefold() not in _DROP_PROFILE_WORDS
    ]
    words = " ".join(tokens).strip().lower()
    words = _PROFILE_PHRASES.get(words, words)
    if words == "control" or not words:
        words = "uncomplicated course"
    parts: list[str] = []
    for index, word in enumerate(words.split()):
        if word in _ACRONYMS:
            parts.append(_ACRONYMS[word])
        elif index == 0:
            parts.append(word[:1].upper() + word[1:])
        else:
            parts.append(word)
    return " ".join(parts)


def _feature(profile: dict[str, Any]) -> str:
    note = str(profile.get("context_note") or "").strip()
    reason = str(profile.get("admission_reason") or "").strip()
    sentence = (note or reason).split(".")[0].strip()
    if any(token in sentence.casefold() for token in _LEAKY):
        sentence = reason.split(";")[0].strip().rstrip(".")
    if any(token in sentence.casefold() for token in _LEAKY) or len(sentence) < 24:
        follow = str(profile.get("followup_item") or "").strip()
        course = str(profile.get("hospital_course_pattern") or "").replace("_", " ")
        sentence = follow or course or sentence
    return sentence.rstrip(".")


def _diversity(directory: Path) -> dict[str, str]:
    text = (directory / "diversity_report.md").read_text(encoding="utf-8")
    def grab(pattern: str) -> str:
        match = re.search(pattern, text)
        if match is None:
            raise ValueError(f"diversity report missing {pattern}")
        return match.group(1).strip()

    return {
        "closest_pair": grab(r"closest pair: (.+)"),
        "closest_score": grab(r"similarity score: ([0-9.]+)"),
        "exact_duplicates": grab(r"exact duplicate fingerprints: (\d+)"),
        "warnings": grab(r"near-duplicate warnings: (\d+)"),
    }


def _rows(directory: Path, kind: str) -> list[dict[str, str]]:
    plan = _load(directory / "batch_plan.json")
    resident = _load(directory / "resident_validation_cases.json")
    profiles = _profiles_by_code(kind)
    by_id = {
        str(case["case_id_code"]): case
        for case in resident["cases"]
        if isinstance(case, dict)
    }
    rows: list[dict[str, str]] = []
    assignments = plan.get("cases") or []
    if not isinstance(assignments, list):
        raise TypeError(directory)
    for assignment in assignments:
        if not isinstance(assignment, dict):
            continue
        case_id = str(assignment["validation_case_id"])
        family_code = str(assignment["scenario"])
        profile_code = str(assignment["clinical_profile"])
        chart = by_id[case_id]["ClinicalCase"]
        if not isinstance(chart, dict):
            raise TypeError(case_id)
        profile = profiles[profile_code]
        rows.append(
            {
                "case_id": case_id,
                "family_code": family_code,
                "family": _family_label(kind, family_code),
                "diagnosis": str(chart.get("admission_dx") or ""),
                "specialty": str(chart.get("specialty") or ""),
                "disposition": str(chart.get("disposition_status") or ""),
                "profile_code": profile_code,
                "profile": _human_profile(profile_code),
                "feature": _feature(profile),
            }
        )
    return rows


def _count_table(title: str, counts: Counter[str]) -> str:
    lines = [f"### {title}", "", "| Item | Cases |", "| --- | ---: |"]
    for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {name} | {count} |")
    lines.append("")
    return "\n".join(lines)


def _transition_counts(rows: list[dict[str, str]], profiles: dict[str, dict[str, Any]]) -> str:
    hold = hospital = pending = 0
    for row in rows:
        profile = profiles[row["profile_code"]]
        if profile.get("hold_medication_query") or profile.get("stop_medication_queries"):
            hold += 1
        hospital_only = profile.get("hospital_only_medication_queries") or []
        if hospital_only:
            hospital += 1
        pending_query = profile.get("pending_decision_medication_query")
        pending_state = profile.get("pending_discharge_state")
        if pending_query or pending_state:
            pending += 1
    return "\n".join(
        [
            "### Medication-transition patterns in the clean profiles",
            "",
            "These counts describe the clinical situation designed into each profile.",
            "They are not the injected assessment targets.",
            "",
            "| Pattern designed into the profile | Cases |",
            "| --- | ---: |",
            f"| Home regimen continued into the hospitalization | {len(rows)} |",
            f"| A hold or a stop is part of the profile | {hold} |",
            f"| Hospital-only therapy is part of the profile | {hospital} |",
            f"| A pending outpatient medication decision is part of the profile | {pending} |",
            "",
        ]
    )


def _case_map(rows: list[dict[str, str]]) -> str:
    lines = [
        "## Case map",
        "",
        "Each row is one synthetic encounter. This table does not say which cases",
        "contain a discrepancy or what that discrepancy is.",
        "",
        (
            "| Case | Clinical family | Admission diagnosis | "
            "Profile / clinical context | Main distinguishing feature |"
        ),
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {case_id} | {family} | {diagnosis} | {profile} | {feature} |".format(**row)
        )
    lines.append("")
    return "\n".join(lines)


def _composition(directory: Path, rows: list[dict[str, str]], kind: str) -> str:
    diversity = _diversity(directory)
    profiles = _profiles_by_code(kind)
    families = Counter(row["family"] for row in rows)
    diagnoses = Counter(row["diagnosis"] for row in rows)
    specialties = Counter(row["specialty"] for row in rows)
    dispositions = Counter(row["disposition"] for row in rows)
    unique_profiles = len({row["profile_code"] for row in rows})
    parts = [
        "## Dataset composition",
        "",
        f"- {len(rows)} cases",
        f"- {unique_profiles} distinct clinical profiles",
        f"- {diversity['exact_duplicates']} exact clean-case duplicates",
        (
            f"- Highest clean-case similarity: {diversity['closest_score']} "
            f"({diversity['closest_pair']})"
        ),
        f"- Near-duplicate warnings: {diversity['warnings']}",
        "",
        "Similarity is measured on the clean clinical case before any discrepancy is introduced.",
        "A warning means two charts share clinical structure. It is not a rejection.",
        "",
        _count_table("Clinical families", families),
        _count_table("Admission diagnoses", diagnoses),
        _count_table("Clinical services", specialties),
        _count_table("Discharge disposition", dispositions),
        _transition_counts(rows, profiles),
    ]
    return "\n".join(parts)


def _shared_anatomy() -> str:
    return """## How each case is structured

Every case is written as a hospital chart, in this order:

```text
Patient overview
        ↓
Reason for hospitalization
        ↓
Relevant medical history / problem list
        ↓
Hospital course
        ↓
Admission vitals and laboratories
        ↓
Discharge / most-recent clinical status
        ↓
Home medications
        ↓
Medications used during hospitalization
        ↓
Discharge medications
        ↓
Medication reconciliation
        ↓
Monitoring and follow-up
        ↓
Discharge instructions
        ↓
Imaging / consultations / procedures / other context
```

| Case section | What the clinician should learn from it |
| --- | --- |
| Patient overview | Demographic and admission context |
| Reason for hospitalization | Why hospital-level care occurred |
| Relevant medical history | Comorbidities needed to interpret the medications |
| Hospital course | Clinical trajectory and treatment decisions |
| Admission vs discharge status | Whether the transition is clinically coherent |
| Home medications | Pre-admission regimen |
| Inpatient medications | Continuation, starts, substitutions, holds, and hospital-only therapy |
| Discharge medications | Outpatient regimen as presented to the resident |
| Medication reconciliation | History source, participation, and pharmacist review |
| Monitoring and follow-up | Transition-of-care requirements |
| Other clinical information | Imaging, procedures, consultations, and return precautions |

## How medication transitions are represented

```text
Home regimen
    ↓
Hospitalization
    ├── continued
    ├── temporarily held
    ├── substituted
    ├── discontinued
    ├── newly started
    └── hospital-only therapy
    ↓
Discharge regimen
    +
monitoring
    +
follow-up
    +
restart / pending decisions
```

A problem can sit in the medication list itself, or in the plan around that list.
Monitoring, supply, a restart, follow-up, or a drug that should stay in the
hospital can each be the issue. A list that looks complete can still hide a
missing transition step.

## What varies across cases

Cases differ in the clinical situation, not only in the identifier:

- diagnosis or archetype
- presentation and symptoms
- clinical trajectory
- relevant past history
- medication regimen
- inpatient medication changes
- laboratory findings
- imaging, procedures, or consultations
- discharge clinical status
- monitoring and follow-up
- disposition, when the profile calls for a change from the patient's baseline living situation

## What does not count as meaningful case diversity

Two cases are not treated as clinically distinct merely because they differ in:

- age
- sex
- random seed
- an exact laboratory number
- an exact vital sign
- the case identifier
- which discrepancy was later introduced

The diversity audit ignores those fields and compares the clean clinical structure.

## Medication-reconciliation problems represented

Each error-bearing case is built around one medication-reconciliation or
transition-of-care problem. Clean controls, with no introduced problem, are
included so a reviewer cannot assume every chart is wrong. This page does not
say which case is which.

### Family 1 — the regimen itself

The discharge regimen does not match the intended plan. Examples:

- a medication that should continue is missing
- a medication that should have stopped is still listed
- the dose does not match the rest of the chart
- the route does not match the formulation
- the frequency does not match the regimen
- a same-class substitute appears without a documented reason

### Family 2 — the transition around the list

The medication list can look plausible while a required transition step is missing. Examples:

- required laboratory monitoring is not arranged
- a held medication has no restart plan
- the supply will not last until follow-up
- a hospital-only medication is still on the discharge list
- a temporary inpatient substitute was not changed back
- a pending medication decision has no follow-up

A clinic appointment is not the same thing as the laboratory task.
An anticoagulation clinic visit can be present while the INR check itself
is the missing step.

## How clinicians should review these cases

Review is one reading of the complete case. Record all five ratings in that
same pass. There is no separate plausibility stage and no second consensus
stage. This review decides whether a chart is fit to use. It is not the later
task in which a resident, blinded to the answer, says what is wrong.

### C1 — Clinical plausibility

Could this reasonably be an inpatient encounter? Consider the presentation,
the diagnosis, the vital signs, the laboratories, the regimen, the hospital
course, internal consistency, and the discharge plan.

### C2 — Intended assessment problem

Is the intended medication-reconciliation or transition-of-care problem
actually present, and does it match its category? A control should contain none.

### C3 — Detectability

Could an internal-medicine resident identify the problem from the visible
chart and say what should change, without the chart announcing the answer?

### C4 — No unintended competing problem

Is there another clinically meaningful medication problem that could
reasonably be read as a different answer? A second dose, frequency, route,
hold, or monitoring problem can make the case unusable.

### C5 — Difficulty

How difficult is the case likely to be for the intended learner?
This rating is advisory. Actual difficulty will later be estimated from
resident performance.

Recommendations:

- **Accept.** The chart can be used for its assigned purpose, or as a control.
- **Revise.** The chart needs a stated correction before use.
  Do not silently edit a case after review has started.
- **Exclude.** The chart should not be used, even if software checks passed.

C1 through C4 need to be acceptable before a case is used against its answer key.
"""


def _identity_block(
    *,
    batch: str,
    val_range: str,
    approach: str,
) -> str:
    return "\n".join(
        [
            f"Batch: `{batch}`",
            f"Cases: {val_range}",
            "Number of cases: 24",
            "Status: Pending human clinician validation",
            f"Generation approach: {approach}",
            "",
        ]
    )


def render_balanced_overview() -> str:
    rows = _rows(BALANCED_DIR, "balanced")
    if len(rows) != 24:
        raise ValueError(f"expected 24 balanced cases, found {len(rows)}")
    counts = Counter(row["family_code"] for row in rows)
    glance = [
        "## At a glance",
        "",
        "| Clinical family | Number of cases | Typical clinical context |",
        "| --- | ---: | --- |",
    ]
    for code, label, detail in BALANCED_FAMILIES:
        glance.append(f"| {label} | {counts[code]} | {detail} |")
    glance.append("")
    body = "\n".join(
        [
            "# CliniProof Balanced Structured Case Set",
            "",
            _identity_block(
                batch="CLINIPROOF_BALANCED_V4",
                val_range="VAL-701–VAL-724",
                approach="Balanced structured generation",
            ),
            "## Start reviewing",
            "",
            "- [Read all cases](readable/all_cases.md)",
            "- [Open the clinician validation packet](readable/clinician_validation_packet.md)",
            "- [Open the validation worksheet](readable/clinical_validation_worksheet.csv)",
            "",
            "## What this case set is",
            "",
            "This set was designed to cover a range of common inpatient problems",
            "under a controlled study plan. Each case is a new synthetic encounter",
            "built from a named clinical profile: a specified presentation, medication",
            "role, hospital course, and follow-up. The profiles were chosen so that",
            "the 24 charts differ in clinical structure before any assessment problem",
            "is introduced.",
            "",
            "The other current set, the [resident-seed-guided cases]"
            "(../seed_guided/README.md), starts from resident-authored clinical examples",
            "instead of this scenario grid. The two sets ask different design questions.",
            "They are not two versions of the same batch.",
            "",
            "\n".join(glance),
            "The distribution is intentionally balanced for study design and is not",
            "intended to reproduce disease prevalence in clinical practice.",
            "",
            _shared_anatomy(),
            _case_map(rows),
            _composition(BALANCED_DIR, rows, "balanced"),
            "## Investigator / technical material",
            "",
            "Clinicians rating cases do not need these files to start. Investigators",
            "and developers use them to see how the set was frozen.",
            "",
            "- [Manifest](validation_manifest.json)",
            "- [Diversity report](diversity_report.md)",
            "- [Answer key](investigator_answer_key.md) — investigators only",
            "- [Batch plan](batch_plan.json)",
            "- [Coverage report](coverage_report.md)",
            "- [Internal QC report](../investigator/clinical_qc_report.md)",
            "",
            "Regenerate this overview from the manifest and profiles with",
            "`python -m app.services.case_set_overview`.",
            "",
        ]
    )
    return body


def render_seed_overview() -> str:
    rows = _rows(SEED_DIR, "seed")
    if len(rows) != 24:
        raise ValueError(f"expected 24 seed-guided cases, found {len(rows)}")
    counts = Counter(row["family_code"] for row in rows)
    names = {
        str(item["code"]): str(item.get("seed_archetype_name") or item["code"])
        for item in _load(ARCHETYPES_PATH).get("archetypes") or []
        if isinstance(item, dict)
    }
    glance = [
        "## At a glance",
        "",
        "| Resident-derived archetype | Cases | Core clinical workflow represented |",
        "| --- | ---: | --- |",
    ]
    for code, workflow in SEED_WORKFLOWS:
        glance.append(f"| {names[code]} | {counts[code]} | {workflow} |")
    glance.append("")
    body = "\n".join(
        [
            "# CliniProof Resident-Seed-Guided Case Set",
            "",
            _identity_block(
                batch="CLINIPROOF_SEEDCASES_V3",
                val_range="VAL-801–VAL-824",
                approach="Resident-seed-guided generation",
            ),
            "## Start reviewing",
            "",
            "- [Read all cases](readable/all_cases.md)",
            "- [Open the clinician validation packet](readable/clinician_validation_packet.md)",
            "- [Open the validation worksheet](readable/clinical_validation_worksheet.csv)",
            "",
            "## What this case set is",
            "",
            "This set starts from six resident-authored clinical examples. Each example",
            "was abstracted into an archetype: the workflow a discharging clinician has",
            "to get right. Four synthetic profiles were then written for each archetype",
            "so the charts differ before any assessment problem is introduced.",
            "",
            "The resident-authored source cases are used as clinical design references.",
            "The study cases are newly synthesized encounters, not copies of the source cases.",
            "Six examples do not estimate how often these problems occur, which drugs",
            "are most common, or which errors are most common. The [source documents]"
            "(../../seed_cases/README.md) are preserved separately and are not the charts",
            "under review.",
            "",
            "The other current set, the [balanced structured cases](../balanced/README.md),",
            "starts from a predefined scenario grid rather than from these examples.",
            "",
            "\n".join(glance),
            _shared_anatomy(),
            _case_map(rows),
            _composition(SEED_DIR, rows, "seed"),
            "## Investigator / technical material",
            "",
            "Clinicians rating cases do not need these files to start.",
            "",
            "- [Manifest](validation_manifest.json)",
            "- [Diversity report](diversity_report.md)",
            "- [Answer key](investigator_answer_key.md) — investigators only",
            "- [Batch plan](batch_plan.json)",
            "- [Coverage report](coverage_report.md)",
            "- [Internal QC report](../investigator/clinical_qc_report.md)",
            "- [Resident-authored source notes](../../seed_cases/README.md)",
            "",
            "Regenerate this overview from the manifest and archetypes with",
            "`python -m app.services.case_set_overview`.",
            "",
        ]
    )
    return body


def write_overviews() -> None:
    (BALANCED_DIR / "README.md").write_text(render_balanced_overview(), encoding="utf-8")
    (SEED_DIR / "README.md").write_text(render_seed_overview(), encoding="utf-8")


def main() -> None:
    write_overviews()


if __name__ == "__main__":
    main()
