# ruff: noqa: E501
"""Round 1 feedback for the six cases the reviewer actually marked.

The selections and comments are the completed KO review of
CLINIPROOF_SEEDCASES_FirstRound (reviewer KO, document date 10/5/2026).
Blank items stay blank. Double selections stay double selections.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

NOT_COMPLETED = "NOT_COMPLETED_IN_ROUND_1"
AMBIGUITY = "SOURCE_SELECTION_AMBIGUITY"
CASES = ("VAL-801", "VAL-802", "VAL-803", "VAL-805", "VAL-809", "VAL-813")
C1_DOMAINS = (
    "Presentation and demographics",
    "Fit between presentation and diagnosis",
    "Vital signs",
    "Laboratory findings",
    "Medication regimen",
    "Hospital course",
    "Consistency across the chart",
    "Discharge plan and follow-up",
)

CONTROL_C2 = (
    "Does this case appropriately contain no deliberately introduced "
    "medication-reconciliation or transition-of-care problem?"
)
ERROR_C2 = (
    "Does the clinical case actually contain the intended "
    "medication-reconciliation or transition-of-care problem described above, "
    "and does it match the intended category?"
)
CONTROL_C3 = "Does the case avoid misleading cues suggesting that an error must exist?"
ERROR_C3 = (
    "Could an internal-medicine resident identify and resolve the intended "
    "problem using only the clinical information provided in the patient-facing case?"
)
CONTROL_C4 = (
    "Does the case contain any clinically meaningful medication-reconciliation "
    "or transition-of-care problem that should not be present?"
)
ERROR_C4 = (
    "Apart from the intended assessment problem, does the case contain another "
    "clinically meaningful medication-reconciliation or transition-of-care "
    "problem that a reasonable resident could interpret as an alternative target?"
)


def _score(*selected: int) -> dict[str, Any]:
    marks = {str(score): score in selected for score in (1, 2, 3, 4)}
    flags: list[str] = []
    if sum(marks.values()) > 1:
        flags.append(AMBIGUITY)
    if not any(marks.values()):
        flags.append(NOT_COMPLETED)
    return {"scores": marks, "flags": flags}


def _binary(pass_selected: bool | None, fail_selected: bool | None) -> dict[str, Any]:
    if pass_selected is None and fail_selected is None:
        return {
            "pass": None,
            "fail": None,
            "status": NOT_COMPLETED,
            "flags": [NOT_COMPLETED],
        }
    flags: list[str] = []
    if pass_selected and fail_selected:
        flags.append(AMBIGUITY)
    if not pass_selected and not fail_selected:
        flags.append(NOT_COMPLETED)
    payload: dict[str, Any] = {
        "pass": bool(pass_selected),
        "fail": bool(fail_selected),
        "flags": flags,
    }
    if AMBIGUITY in flags:
        payload["extraction_note"] = "Both options are selected in the source document."
    if NOT_COMPLETED in flags:
        payload["status"] = NOT_COMPLETED
    return payload


def _difficulty(
    easy: bool | None,
    moderate: bool | None,
    hard: bool | None,
    outlier: bool | None,
) -> dict[str, Any]:
    if easy is None:
        return {
            "easy": None,
            "moderate": None,
            "hard": None,
            "inappropriate_or_outlier": None,
            "status": NOT_COMPLETED,
            "flags": [NOT_COMPLETED],
        }
    marks = {
        "easy": bool(easy),
        "moderate": bool(moderate),
        "hard": bool(hard),
        "inappropriate_or_outlier": bool(outlier),
    }
    flags: list[str] = []
    if sum(bool(value) for value in marks.values()) > 1:
        flags.append(AMBIGUITY)
    if not any(marks.values()):
        flags.append(NOT_COMPLETED)
    payload: dict[str, Any] = {**marks, "flags": flags}
    if NOT_COMPLETED in flags:
        payload["status"] = NOT_COMPLETED
    return payload


def _overall(accept: bool | None, revise: bool | None, exclude: bool | None) -> dict[str, Any]:
    if accept is None:
        return {
            "accept": None,
            "revise": None,
            "exclude": None,
            "status": NOT_COMPLETED,
            "flags": [NOT_COMPLETED],
        }
    marks = {"accept": bool(accept), "revise": bool(revise), "exclude": bool(exclude)}
    flags: list[str] = []
    if sum(marks.values()) > 1:
        flags.append(AMBIGUITY)
    if not any(marks.values()):
        flags.append(NOT_COMPLETED)
    payload: dict[str, Any] = {**marks, "flags": flags}
    if AMBIGUITY in flags:
        payload["extraction_note"] = "Both options are selected in the source document."
    if NOT_COMPLETED in flags:
        payload["status"] = NOT_COMPLETED
    return payload


def _case(
    case_id: str,
    *,
    complete: bool,
    domains: tuple[tuple[int, ...], ...],
    c1_pass: bool,
    c1_fail: bool,
    c1_comment: str,
    reference: dict[str, str],
    c2_question: str,
    c2: dict[str, Any],
    c2_comment: str | None,
    c3_question: str,
    c3: dict[str, Any],
    c3_comment: str | None,
    c4_question: str,
    c4: dict[str, Any],
    c4_issue: str | None,
    c4_location: str | None,
    c4_meaning: str | None,
    c4_comment: str | None,
    c5: dict[str, Any],
    c5_comment: str | None,
    overall: dict[str, Any],
    overall_comment: str | None,
    reviewer: str | None,
    review_date: str | None,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "source_document": "KO Casebook Validation.docx",
        "source_case_set": "CLINIPROOF_SEEDCASES_FirstRound",
        "document_reviewer_code": "KO",
        "document_review_date": "10/5/2026",
        "round1_review_status": "complete" if complete else "partial",
        "c1": {
            "domains": [
                {"domain": name, **_score(*selected)}
                for name, selected in zip(C1_DOMAINS, domains, strict=True)
            ],
            "overall": _binary(c1_pass, c1_fail),
            "comment": c1_comment,
        },
        "validation_reference": reference,
        "c2": {"question": c2_question, "selection": c2, "comment": c2_comment},
        "c3": {"question": c3_question, "selection": c3, "comment": c3_comment},
        "c4": {
            "question": c4_question,
            "selection": c4,
            "medication_or_clinical_issue": c4_issue,
            "where_it_appears": c4_location,
            "why_clinically_meaningful": c4_meaning,
            "comment": c4_comment,
        },
        "c5": {"selection": c5, "comment": c5_comment},
        "overall_recommendation": {
            "selection": overall,
            "comment": overall_comment,
            "reviewer_code": reviewer,
            "date": review_date,
        },
    }


def completed_reviews() -> dict[str, dict[str, Any]]:
    """Return the six extracted reviews keyed by case id."""
    blank_pf = _binary(False, False)
    blank_diff = _difficulty(False, False, False, False)
    blank_overall = _overall(False, False, False)
    reviews = {
        "VAL-801": _case(
            "VAL-801",
            complete=True,
            domains=((2,), (2,), (3,), (3,), (3,), (2,), (3,), (4,)),
            c1_pass=False,
            c1_fail=True,
            c1_comment=(
                "This case is lacking clinical complexity. The patient presents with "
                "delirium, but the cause is not revealed during the hospital course, "
                "we just learn that the delirium improves with treatment. There are no "
                "further details on why the patient was delirious or why he improved. "
                "It is also not clear why the ibuprofen was stopped. I would add that "
                "he is discovered to have an infection or GI bleed or something that "
                "would explain this better."
            ),
            reference={
                "case_type": "Clean control",
                "error_family": "None",
                "error_category": "None",
                "planted_assessment_discrepancy": "None",
                "expected_condition": (
                    "No deliberately introduced medication-reconciliation or "
                    "transition-of-care discrepancy"
                ),
            },
            c2_question=CONTROL_C2,
            c2=_binary(False, True),
            c2_comment="It wasn’t clear why ibuprofen should be stopped.",
            c3_question=CONTROL_C3,
            c3=_binary(True, True),
            c3_comment=None,
            c4_question=CONTROL_C4,
            c4=_binary(False, True),
            c4_issue="Ibuprofen stopped on admission",
            c4_location="In home medication list",
            c4_meaning="No obvious indication for why this should be stopped",
            c4_comment="Not clear why ibuprofen was stopped",
            c5=_difficulty(False, False, False, True),
            c5_comment="Case is unclear",
            overall=_overall(False, True, False),
            overall_comment=(
                "This case could be usable if there was more complexity to the "
                "clinical case, i.e infection discovered and treated. Delirium due "
                "to known physiologic condition and then not elaborating on the "
                "physiologic condition doesn’t make sense. Medication list should "
                "be clearer."
            ),
            reviewer="KO",
            review_date="10/5/26",
        ),
        "VAL-802": _case(
            "VAL-802",
            complete=True,
            domains=((2,), (1,), (3,), (2,), (2,), (1,), (2,), (2,)),
            c1_pass=False,
            c1_fail=True,
            c1_comment=(
                "Several issues with this – delirium cause is not revealed "
                "(delirium due to known physiologic condition doesn’t make sense), "
                "it doesn’t appear that anything happened in the hospital course, "
                "creatinine was the only lab value and changed slightly, but it was "
                "not clear what the baseline creatinine was, lots of mention of the "
                "statin and it said that she was taking the statin, but this was not "
                "continued at discharge for no obvious reason"
            ),
            reference={
                "case_type": "Error-bearing",
                "error_family": "Family 1",
                "error_category": "Medication omitted at discharge (f1_omission)",
                "intended_assessment_target": (
                    "A medication indicated at discharge was omitted from the "
                    "discharge medication list."
                ),
                "medication_involved": "atorvastatin 40 MG Oral Tablet",
                "clean_expected_state": "present; original clean discharge row is atorvastatin 40 MG once daily",
                "what_appears_in_the_historical_case": "absent",
                "evidence_available": "Home/inpatient continuation of this medication with no stop rationale.",
                "evidence_location": "Home medications, Medications during hospitalization, Discharge medications",
                "detectability_location": "Discharge medications",
                "expected_clinical_action": "Restore the omitted continued discharge medication.",
            },
            c2_question=ERROR_C2,
            c2=_binary(False, True),
            c2_comment=(
                "Was the trainee supposed to continue the statin? Or recognize that "
                "it was not continued? It is unclear"
            ),
            c3_question=ERROR_C3,
            c3=_binary(False, True),
            c3_comment="Case lacks clinical complexity and reasoning for stopping the statin",
            c4_question=ERROR_C4,
            c4=_binary(False, True),
            c4_issue="Creatinine elevated but patient continued on lisinopril",
            c4_location="Lab data",
            c4_meaning="If creatinine was elevated to point of AKI the lisinopril should be stopped",
            c4_comment="As above",
            c5=_difficulty(False, False, False, True),
            c5_comment="This case is unclear and intended discharge medications are not stated",
            overall=_overall(False, False, True),
            overall_comment=(
                "Would exclude, this case would need major revisions to be "
                "compatible with the goals of this project"
            ),
            reviewer="KO",
            review_date="10/5/26",
        ),
        "VAL-803": _case(
            "VAL-803",
            complete=False,
            domains=((2,), (1,), (3,), (3,), (3,), (1,), (2,), (3,)),
            c1_pass=False,
            c1_fail=True,
            c1_comment=(
                "Several issues – delirium diagnosis is unclear (delirium due to "
                "known physiologic condition), cause is not revealed during the "
                "hospital course. Medication list is fine but no changes that need "
                "to be made at discharge. Her creatinine changes so this might be "
                "considered clinically relevant or why the patient receives only 7 "
                "days of lisinopril."
            ),
            reference={
                "case_type": "Error-bearing",
                "error_family": "Family 2",
                "error_category": "Insufficient medication supply (f2_insufficient_supply)",
                "intended_assessment_target": (
                    "The prescribed quantity or days' supply is insufficient to cover "
                    "the patient until the planned follow-up."
                ),
                "medication_involved": "lisinopril 10 MG Oral Tablet",
                "clean_expected_state": "30 days",
                "what_appears_in_the_historical_case": "7 days",
                "evidence_available": "Days' supply must cover the scheduled follow-up or treatment endpoint.",
                "evidence_location": "Follow-up appointments, discharge medications.quantity or days",
                "detectability_location": "discharge medications.quantity or days",
                "expected_clinical_action": (
                    "Increase days' supply so treatment continues through the planned follow-up."
                ),
            },
            c2_question=ERROR_C2,
            c2=blank_pf,
            c2_comment=None,
            c3_question=ERROR_C3,
            c3=blank_pf,
            c3_comment=None,
            c4_question=ERROR_C4,
            c4=blank_pf,
            c4_issue=None,
            c4_location=None,
            c4_meaning=None,
            c4_comment=None,
            c5=blank_diff,
            c5_comment=None,
            overall=blank_overall,
            overall_comment=None,
            reviewer=None,
            review_date=None,
        ),
        "VAL-805": _case(
            "VAL-805",
            complete=True,
            domains=((3,), (3,), (3,), (3,), (2, 3), (2,), (3,), (3,)),
            c1_pass=False,
            c1_fail=True,
            c1_comment=(
                "Clinical presentation was mostly clear and understandable. The vitals "
                "and lab trends make sense. The weight should be closer to dry weight "
                "at the time of discharge. The medications during hospitalization would "
                "not be the same as the home regimen - the lasix would be given IV and "
                "increased. Additionally, it would be more realistic to have several "
                "days of input and output data, as well as data on what medications the "
                "patient received during the hospitalization. It would be helpful to "
                "have either notes from cardiology or echocardiogram data and require "
                "the trainee to add additional medications to the patient’s regimen or "
                "adjust their dose of lasix."
            ),
            reference={
                "case_type": "Clean control",
                "error_family": "None",
                "error_category": "None",
                "planted_assessment_discrepancy": "None",
                "expected_condition": (
                    "No deliberately introduced medication-reconciliation or "
                    "transition-of-care discrepancy"
                ),
            },
            c2_question=CONTROL_C2,
            c2=_binary(True, False),
            c2_comment=None,
            c3_question=CONTROL_C3,
            c3=_binary(False, True),
            c3_comment=(
                "The discharge weight not being close to the patient’s dry weight is "
                "confusing and suggests that the patient is not in fact ready for discharge"
            ),
            c4_question=CONTROL_C4,
            c4=_binary(True, False),
            c4_issue=None,
            c4_location=None,
            c4_meaning=None,
            c4_comment=None,
            c5=_difficulty(False, True, False, False),
            c5_comment=None,
            overall=_overall(False, True, False),
            overall_comment=(
                "We need to add further details to the hospital course so there is a "
                "greater understanding of what diuresis the patient was receiving during "
                "the hospitalization (should not be the same as the patient’s home "
                "regimen). The trainee should have to make decisions on additional "
                "medications that should be added to the patient’s regimen – i.e. other "
                "GDMT such as ACE/ARB, SGLT2i, MRA"
            ),
            reviewer="KO",
            review_date="10/5/2026",
        ),
        "VAL-809": _case(
            "VAL-809",
            complete=True,
            domains=((2,), (2,), (3,), (2,), (2,), (2,), (2,), (3,)),
            c1_pass=False,
            c1_fail=True,
            c1_comment=(
                "Presentation – requires more details, should present with fevers, "
                "have a history of mechanical valve or poor dentition that would "
                "predispose to endocarditis\n"
                "Labs/meds – AKI was unexplained and lisinopril was continued despite AKI"
            ),
            reference={
                "case_type": "Clean control",
                "error_family": "None",
                "error_category": "None",
                "planted_assessment_discrepancy": "None",
                "expected_condition": (
                    "No deliberately introduced medication-reconciliation or "
                    "transition-of-care discrepancy"
                ),
            },
            c2_question=CONTROL_C2,
            c2=_binary(False, True),
            c2_comment="Lisinopril was continued despite the patient having an AKI",
            c3_question=CONTROL_C3,
            c3=_binary(True, False),
            c3_comment=None,
            c4_question=CONTROL_C4,
            c4=_binary(False, True),
            c4_issue="Lisinopril - AKI",
            c4_location="Medications",
            c4_meaning="Should not be continued",
            c4_comment=None,
            c5=_difficulty(False, False, False, True),
            c5_comment="Error in the case as described above",
            overall=_overall(False, True, False),
            overall_comment=(
                "Revise clinical scenario to add more details. Would have "
                "fevers/chills/predisposition to endocarditis. Lisinopril should be "
                "held if the patient has an AKI. Patient of this age would be very "
                "likely to have more than 2 home medications, would like to have more "
                "detail and complexity overall to this case."
            ),
            reviewer="KO",
            review_date="10/5/26",
        ),
        "VAL-813": _case(
            "VAL-813",
            complete=True,
            domains=((2,), (2,), (2,), (2,), (1,), (2,), (2,), (2,)),
            c1_pass=False,
            c1_fail=True,
            c1_comment=(
                "Patient is admitted for new diagnosis of CMV colitis, but was already "
                "on treatment for this (valganciclovir) prior to admission, which does "
                "not make sense. This medication would be started after diagnosis during "
                "the hospitalization. The medications are much too simplified for a post "
                "transplant patient. The labs are incomplete and the patient has a change "
                "in potassium without obvious cause or indication."
            ),
            reference={
                "case_type": "Clean control",
                "error_family": "None",
                "error_category": "None",
                "planted_assessment_discrepancy": "None",
                "expected_condition": (
                    "No deliberately introduced medication-reconciliation or "
                    "transition-of-care discrepancy"
                ),
            },
            c2_question=CONTROL_C2,
            c2=_binary(False, True),
            c2_comment=(
                "Since the patient was on valganciclovir on admission, it would make "
                "you think that you need to change to an alternative regimen to "
                "appropriately treat the CMV"
            ),
            c3_question=CONTROL_C3,
            c3=_binary(False, True),
            c3_comment="As above, it isn’t clear why the patient was already on valganciclovir",
            c4_question=CONTROL_C4,
            c4=_binary(False, True),
            c4_issue="Valganciclovir",
            c4_location="Admission medications",
            c4_meaning="Should not be an admission medication",
            c4_comment="This is an error in the case that would be confusing",
            c5=_difficulty(False, False, False, True),
            c5_comment=None,
            overall=_overall(False, False, True),
            overall_comment=None,
            reviewer="KO",
            review_date="10/5/2026",
        ),
    }
    return reviews


def ambiguities(review: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for domain in review["c1"]["domains"]:
        if AMBIGUITY in domain["flags"]:
            selected = [score for score, on in domain["scores"].items() if on]
            found.append(f"C1 {domain['domain']}: scores {', '.join(selected)} both selected")
    for label, block in (
        ("C1 overall", review["c1"]["overall"]),
        ("C2", review["c2"]["selection"]),
        ("C3", review["c3"]["selection"]),
        ("C4", review["c4"]["selection"]),
        ("C5", review["c5"]["selection"]),
        ("Overall", review["overall_recommendation"]["selection"]),
    ):
        if AMBIGUITY in block.get("flags", []):
            found.append(label)
    return found


def write_feedback_files(directory: Path) -> None:
    feedback_dir = directory / "round1_feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)
    reviews = completed_reviews()
    for case_id in CASES:
        path = feedback_dir / f"{case_id}_round1_feedback.json"
        path.write_text(json.dumps(reviews[case_id], indent=2) + "\n", encoding="utf-8")
    (directory / "ROUND1_FEEDBACK_COMPLETE.md").write_text(_complete_markdown(reviews), encoding="utf-8")
    (directory / "ROUND1_FEEDBACK_EXTRACTION_AUDIT.md").write_text(
        _audit_markdown(reviews),
        encoding="utf-8",
    )


def _marks(scores: dict[str, bool]) -> str:
    selected = [score for score, on in scores.items() if on]
    return ", ".join(selected) if selected else NOT_COMPLETED


def _binary_text(selection: dict[str, Any]) -> str:
    if selection.get("status") == NOT_COMPLETED and selection.get("pass") is None:
        return NOT_COMPLETED
    if NOT_COMPLETED in selection.get("flags", []) and not selection.get("pass") and not selection.get("fail"):
        return NOT_COMPLETED
    parts = []
    if selection.get("pass"):
        parts.append("Pass")
    if selection.get("fail"):
        parts.append("Fail")
    text = " and ".join(parts) if parts else NOT_COMPLETED
    if AMBIGUITY in selection.get("flags", []):
        text += f" ({AMBIGUITY})"
    return text


def _complete_markdown(reviews: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Round 1 feedback, complete extract",
        "",
        "Source: KO Casebook Validation.docx, reviewer code KO, document date 10/5/2026, "
        "case set CLINIPROOF_SEEDCASES_FirstRound. Only VAL-801, VAL-802, VAL-803, "
        "VAL-805, VAL-809, and VAL-813 contain reviewer entries. Checkbox states are "
        "stored in the JSON files before any single-number summary.",
        "",
    ]
    for case_id in CASES:
        review = reviews[case_id]
        lines.append(f"## {case_id}")
        lines.append("")
        lines.append(f"Review status: {review['round1_review_status']}.")
        lines.append("")
        lines.append("| Domain | 1 | 2 | 3 | 4 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for domain in review["c1"]["domains"]:
            cells = ["☒" if domain["scores"][str(score)] else "☐" for score in (1, 2, 3, 4)]
            note = " AMBIGUOUS" if AMBIGUITY in domain["flags"] else ""
            lines.append(f"| {domain['domain']}{note} | {' | '.join(cells)} |")
        lines.append("")
        lines.append(f"C1 overall: {_binary_text(review['c1']['overall'])}.")
        lines.append("")
        lines.append("C1 comment:")
        lines.append("")
        lines.append(f"> {review['c1']['comment']}")
        lines.append("")
        lines.append(f"C2: {_binary_text(review['c2']['selection'])}.")
        lines.append(f"C2 comment: {review['c2']['comment'] or NOT_COMPLETED}.")
        lines.append("")
        lines.append(f"C3: {_binary_text(review['c3']['selection'])}.")
        lines.append(f"C3 comment: {review['c3']['comment'] or NOT_COMPLETED}.")
        lines.append("")
        lines.append(f"C4: {_binary_text(review['c4']['selection'])}.")
        lines.append(f"C4 issue: {review['c4']['medication_or_clinical_issue'] or NOT_COMPLETED}.")
        lines.append(f"C4 comment: {review['c4']['comment'] or NOT_COMPLETED}.")
        lines.append("")
        c5 = review["c5"]["selection"]
        if c5.get("status") == NOT_COMPLETED and c5.get("easy") is None:
            lines.append(f"C5: {NOT_COMPLETED}.")
        else:
            chosen = [name for name, on in c5.items() if on is True]
            lines.append(f"C5: {', '.join(chosen) if chosen else NOT_COMPLETED}.")
        lines.append(f"C5 comment: {review['c5']['comment'] or NOT_COMPLETED}.")
        lines.append("")
        lines.append(
            "Overall recommendation: "
            f"{_binary_text(review['overall_recommendation']['selection']).replace('Pass', 'Accept').replace('Fail', 'Revise')}."
        )
        # overall uses accept/revise/exclude not pass/fail. Print explicitly.
        lines[-1] = "Overall recommendation: " + _overall_text(review) + "."
        lines.append(
            f"Overall comment: {review['overall_recommendation']['comment'] or NOT_COMPLETED}."
        )
        lines.append(
            "Case reviewer code: "
            f"{review['overall_recommendation']['reviewer_code'] or NOT_COMPLETED}. "
            f"Case date: {review['overall_recommendation']['date'] or NOT_COMPLETED}."
        )
        lines.append("")
    return "\n".join(lines)


def _overall_text(review: dict[str, Any]) -> str:
    selection = review["overall_recommendation"]["selection"]
    if NOT_COMPLETED in selection.get("flags", []) and not any(
        selection.get(name) for name in ("accept", "revise", "exclude")
    ):
        return NOT_COMPLETED
    chosen = [name for name in ("accept", "revise", "exclude") if selection.get(name)]
    text = ", ".join(chosen) if chosen else NOT_COMPLETED
    if AMBIGUITY in selection.get("flags", []):
        text += f" ({AMBIGUITY})"
    return text


def _audit_markdown(reviews: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Round 1 feedback extraction audit",
        "",
        "This audit checks the JSON extract against the completed review. A domain is "
        "extracted when all four checkbox states are stored. An item is incomplete when "
        "no box was selected. Ambiguity means more than one box in that item is selected. "
        "VAL-803 C2 through the overall recommendation were blank in the source and stay blank.",
        "",
        "| Case | Pages/source | C1 extracted | C2 | C3 | C4 | C5 | Overall recommendation | Comments extracted | Ambiguity/incomplete? |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for case_id in CASES:
        review = reviews[case_id]
        c1_ok = len(review["c1"]["domains"]) == 8 and all(
            set(domain["scores"]) == {"1", "2", "3", "4"} for domain in review["c1"]["domains"]
        )
        comments = [
            review["c1"]["comment"],
            review["c2"]["comment"],
            review["c3"]["comment"],
            review["c4"]["comment"],
            review["c5"]["comment"],
            review["overall_recommendation"]["comment"],
        ]
        comment_count = sum(1 for comment in comments if comment)
        flags = ambiguities(review)
        if review["round1_review_status"] != "complete":
            flags.append("partial review")
        lines.append(
            f"| {case_id} | KO Casebook Validation.docx | "
            f"{'yes' if c1_ok else 'no'} | {_binary_text(review['c2']['selection'])} | "
            f"{_binary_text(review['c3']['selection'])} | {_binary_text(review['c4']['selection'])} | "
            f"{_c5_text(review)} | {_overall_text(review)} | {comment_count} | "
            f"{'; '.join(flags) if flags else 'no'} |"
        )
    lines.extend(
        [
            "",
            "Programmatic checks required before revision: eight C1 domains for each case, "
            "raw score booleans present, VAL-801 C3 Pass and Fail both true, VAL-805 "
            "medication-regimen scores 2 and 3 both true, and VAL-803 C2, C3, C4, C5, and "
            "the overall recommendation all marked NOT_COMPLETED_IN_ROUND_1.",
            "",
        ]
    )
    return "\n".join(lines)


def _c5_text(review: dict[str, Any]) -> str:
    selection = review["c5"]["selection"]
    if selection.get("easy") is None:
        return NOT_COMPLETED
    chosen = [
        name
        for name in ("easy", "moderate", "hard", "inappropriate_or_outlier")
        if selection.get(name)
    ]
    return ", ".join(chosen) if chosen else NOT_COMPLETED
