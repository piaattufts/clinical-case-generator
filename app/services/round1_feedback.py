"""Read a completed Round 1 validation casebook without rewriting comments.

The source is the clinician's filled Word file. Selections come from the
checkbox content controls. Comment text is the control's stored text.
An empty control stays empty. This module does not infer a rating.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
W14 = "{http://schemas.microsoft.com/office/word/2010/wordml}"

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
C1_SCORES = ("1", "2", "3", "4")
PASS_FAIL = ("Pass", "Fail")
C5_CHOICES = ("Easy", "Moderate", "Hard", "Inappropriate / outlier")
RECOMMENDATIONS = ("Accept", "Revise", "Exclude")
NOT_COMPLETED = "Not completed in Round 1"


@dataclass(frozen=True)
class ChoiceGroup:
    """One single-choice Round 1 item, in the order the form printed it."""

    labels: tuple[str, ...]
    selected: tuple[str, ...]

    @property
    def completed(self) -> bool:
        return bool(self.selected)


@dataclass(frozen=True)
class Round1CaseFeedback:
    """Ratings and comments copied from one case in the completed casebook."""

    case_id: str
    reviewer: str | None
    review_date: str | None
    c1_scores: tuple[ChoiceGroup, ...]
    c1_result: ChoiceGroup
    c1_comment: str | None
    c2_result: ChoiceGroup
    c2_comment: str | None
    c3_result: ChoiceGroup
    c3_comment: str | None
    c4_result: ChoiceGroup
    c4_comment: str | None
    c5_difficulty: ChoiceGroup
    c5_comment: str | None
    recommendation: ChoiceGroup
    overall_comment: str | None


def parse_round1_casebook(path: Path) -> dict[str, Round1CaseFeedback]:
    """Return feedback keyed by case id. Missing cases are simply absent."""
    with ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    body = root.find(f"{W}body")
    if body is None:
        raise ValueError(f"{path} has no document body")
    cover_reviewer: str | None = None
    cover_date: str | None = None
    current: _Accumulator | None = None
    found: dict[str, Round1CaseFeedback] = {}
    for kind, payload in _events(body):
        if kind == "case":
            if current is not None:
                found[current.case_id] = current.finish(cover_reviewer, cover_date)
            current = _Accumulator(str(payload))
            continue
        if not isinstance(payload, ET.Element):
            continue
        tag = _tag(payload)
        if current is None:
            if tag == "reviewer-code":
                cover_reviewer = _blank_to_none(_control_text(payload))
            elif tag == "review-date":
                cover_date = _blank_to_none(_control_text(payload))
            continue
        current.add(tag, payload)
    if current is not None:
        found[current.case_id] = current.finish(cover_reviewer, cover_date)
    if not found:
        raise ValueError(f"{path} does not contain CASE headings from a Round 1 casebook")
    return found


class _Accumulator:
    def __init__(self, case_id: str) -> None:
        self.case_id = case_id
        self.c1_checked: list[bool] = []
        self.results: dict[str, list[bool]] = {}
        self.comments: dict[str, str | None] = {}
        self.initials: str | None = None
        self.case_date: str | None = None

    def add(self, tag: str, control: ET.Element) -> None:
        if tag == "c1-score":
            self.c1_checked.append(_is_checked(control))
            return
        if tag in {
            "c1-result",
            "c2-result",
            "c3-result",
            "c4-result",
            "c5-difficulty",
            "recommendation",
        }:
            self.results.setdefault(tag, []).append(_is_checked(control))
            return
        if tag in {
            "c1-comments",
            "c2-comments",
            "c3-comments",
            "c4-comments",
            "c5-comments",
            "overall-comments",
        }:
            self.comments[tag] = _blank_to_none(_control_text(control))
            return
        if tag == "reviewer-initials":
            self.initials = _blank_to_none(_control_text(control))
        elif tag == "case-date":
            self.case_date = _blank_to_none(_control_text(control))

    def finish(self, cover_reviewer: str | None, cover_date: str | None) -> Round1CaseFeedback:
        scores = tuple(
            _choice(C1_SCORES, self.c1_checked[index * 4 : (index + 1) * 4])
            for index in range(len(C1_DOMAINS))
        )
        return Round1CaseFeedback(
            case_id=self.case_id,
            reviewer=self.initials or cover_reviewer,
            review_date=self.case_date or cover_date,
            c1_scores=scores,
            c1_result=_choice(PASS_FAIL, self.results.get("c1-result", [])),
            c1_comment=self.comments.get("c1-comments"),
            c2_result=_choice(PASS_FAIL, self.results.get("c2-result", [])),
            c2_comment=self.comments.get("c2-comments"),
            c3_result=_choice(PASS_FAIL, self.results.get("c3-result", [])),
            c3_comment=self.comments.get("c3-comments"),
            c4_result=_choice(PASS_FAIL, self.results.get("c4-result", [])),
            c4_comment=self.comments.get("c4-comments"),
            c5_difficulty=_choice(C5_CHOICES, self.results.get("c5-difficulty", [])),
            c5_comment=self.comments.get("c5-comments"),
            recommendation=_choice(RECOMMENDATIONS, self.results.get("recommendation", [])),
            overall_comment=self.comments.get("overall-comments"),
        )


def _choice(labels: tuple[str, ...], checked: list[bool]) -> ChoiceGroup:
    selected = tuple(label for label, flag in zip(labels, checked, strict=False) if flag)
    return ChoiceGroup(labels=labels, selected=selected)


def _events(body: ET.Element) -> list[tuple[str, str | ET.Element]]:
    events: list[tuple[str, str | ET.Element]] = []
    for child in list(body):
        if child.tag == f"{W}p":
            text = _paragraph_text(child).strip()
            if text.startswith("CASE VAL-"):
                events.append(("case", text.split()[1]))
            events.extend(("sdt", control) for control in child.findall(f".//{W}sdt"))
        elif child.tag == f"{W}tbl":
            events.extend(("sdt", control) for control in child.findall(f".//{W}sdt"))
    return events


def _paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(f".//{W}t"))


def _tag(control: ET.Element) -> str:
    properties = control.find(f"{W}sdtPr")
    if properties is None:
        return ""
    tag = properties.find(f"{W}tag")
    if tag is None:
        return ""
    return tag.get(f"{W}val") or ""


def _is_checked(control: ET.Element) -> bool:
    properties = control.find(f"{W}sdtPr")
    if properties is None:
        return False
    checked = properties.find(f"{W14}checkbox/{W14}checked")
    if checked is None:
        checked = properties.find(f".//{W14}checked")
    if checked is None:
        return False
    value = (checked.get(f"{W14}val") or checked.get(f"{W}val") or "0").casefold()
    return value in {"1", "true", "on"}


def _control_text(control: ET.Element) -> str:
    content = control.find(f"{W}sdtContent")
    if content is None:
        return ""
    paragraphs = content.findall(f"{W}p")
    if paragraphs:
        lines = [
            "".join(node.text or "" for node in paragraph.findall(f".//{W}t"))
            for paragraph in paragraphs
        ]
        return "\n".join(lines).strip()
    return "".join(node.text or "" for node in content.findall(f".//{W}t")).strip()


def _blank_to_none(text: str) -> str | None:
    stripped = text.strip()
    return stripped or None
