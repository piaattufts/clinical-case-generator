"""Render revised Generation 1 and Generation 2 cases on the Round 1 instrument.

Charts come from resident JSON. The hidden reference comes from the evaluator
file. The renderer copies those structured fields and does not invent facts.
"""

from __future__ import annotations

import csv
import json
import random
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from docx import Document
from docx.document import Document as WordDocument
from docx.oxml.ns import qn

from app.services.validation_casebook import (
    PreparedCase,
    _add_text_field,
    _start_case_section,
    _write_validation,
)
from app.services.word_controls import finalize_word_form, prepare_form_document
from app.services.word_export import _add_body, _add_heading, _new_document, _render_case

ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "docs" / "validation"
REVISED = ROOT / "data" / "case_sets" / "seed_guided" / "REVISED"
G2_RESIDENT = ROOT / "data" / "case_sets" / "synthea_g2" / "cases" / "resident"
G2_EVALUATOR = ROOT / "data" / "case_sets" / "synthea_g2" / "cases" / "evaluator"
COMPARISON = ROOT / "docs" / "clinical_feedback" / "reviewer_comparison.csv"
ITEM_RATINGS = ROOT / "docs" / "clinical_feedback" / "reviewer_item_ratings.csv"
BLINDING_MAP = ROOT / "data" / "case_sets" / "synthea_g2" / "blinding_map.json"
LINKS = VALIDATION / "case_links.csv"
UNBLINDING_KEY = ROOT / "data" / "blinding" / "unblinding_key.json"
BLIND_SEED = 20261009

DISPLAY_NAME = {
    "MEDREC_UNCERTAIN_HISTORY": "Medication history uncertainty",
    "MED_HISTORY_UNCERTAINTY": "Medication history uncertainty",
    "HF_DECOMPENSATION": "Acute heart-failure decompensation",
    "OPAT_ENDOCARDITIS": "Outpatient parenteral antibiotic therapy after endocarditis",
    "ENDOCARDITIS_OPAT": "Outpatient parenteral antibiotic therapy after endocarditis",
    "TRANSPLANT_CMV": "Post-kidney-transplant infectious complication",
    "POSTOP_ANTICOAGULATION": "Postoperative anticoagulation after hip fracture",
    "HIP_FRACTURE_ANTICOAGULATION": "Postoperative anticoagulation after hip fracture",
    "GI_BLEED_ACUTE_CHANGE": "Gastrointestinal bleed with anticoagulation decisions",
    "GI_BLEED_ANTICOAGULATION": "Gastrointestinal bleed with anticoagulation decisions",
}

G1_CODE = {
    **{index: "MEDREC_UNCERTAIN_HISTORY" for index in range(801, 805)},
    **{index: "HF_DECOMPENSATION" for index in range(805, 809)},
    **{index: "OPAT_ENDOCARDITIS" for index in range(809, 813)},
    **{index: "TRANSPLANT_CMV" for index in range(813, 817)},
    **{index: "POSTOP_ANTICOAGULATION" for index in range(817, 821)},
    **{index: "GI_BLEED_ACUTE_CHANGE" for index in range(821, 825)},
}

SOURCE_LABEL = {
    "SECOND_REVISION_CANDIDATE": "dual-review",
    "REVIEWER_1_PLUS_FRAMEWORK": "Reviewer 1 + framework",
    "": "framework only",
}

NEUTRAL_FOOTER = "CliniProof clinical validation"


@dataclass(frozen=True)
class ReviewCase:
    case_id: str
    resident: dict[str, Any]
    reference_plan: dict[str, Any]
    revision_source: str
    family_display: str
    counterpart: str


def item_labels() -> list[str]:
    labels: list[str] = []
    with ITEM_RATINGS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["case_id"] != "VAL-801":
                continue
            labels.append(row["item"])
    if len(labels) != 14:
        raise ValueError(f"expected 14 item labels, found {len(labels)}")
    return labels


def revision_sources() -> dict[str, str]:
    sources: dict[str, str] = {}
    with COMPARISON.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            token = row["revision_candidate"]
            if token not in SOURCE_LABEL:
                raise ValueError(f"unknown revision_candidate {token!r} for {row['case_id']}")
            sources[row["case_id"]] = SOURCE_LABEL[token]
    return sources


def _load_json(path: Path) -> dict[str, Any]:
    payload: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(path)
    return payload


def load_generation1() -> list[ReviewCase]:
    sources = revision_sources()
    cases: list[ReviewCase] = []
    for index in range(801, 825):
        case_id = f"VAL-{index}"
        overlap = {"VAL-801", "VAL-805", "VAL-809", "VAL-813"}
        folder = "overlap_4" if case_id in overlap else "remaining_20"
        resident = _load_json(REVISED / folder / f"{case_id}_resident.json")
        evaluator = _load_json(REVISED / folder / f"{case_id}_evaluator.json")
        plan = evaluator.get("reference_discharge_plan")
        if not isinstance(plan, dict):
            raise ValueError(f"{case_id} evaluator has no reference discharge plan")
        cases.append(
            ReviewCase(
                case_id=case_id,
                resident=resident,
                reference_plan=plan,
                revision_source=sources[case_id],
                family_display=DISPLAY_NAME[G1_CODE[index]],
                counterpart=f"G2-{index - 800:03d}",
            )
        )
    return cases


def load_generation2() -> list[ReviewCase]:
    sources = revision_sources()
    cases: list[ReviewCase] = []
    for index in range(1, 25):
        case_id = f"G2-{index:03d}"
        val_id = f"VAL-{800 + index}"
        resident = _load_json(G2_RESIDENT / f"{case_id}.json")
        evaluator = _load_json(G2_EVALUATOR / f"{case_id}.json")
        plan = evaluator.get("reference_discharge_plan")
        if not isinstance(plan, dict):
            raise ValueError(f"{case_id} evaluator has no reference discharge plan")
        cases.append(
            ReviewCase(
                case_id=case_id,
                resident=resident,
                reference_plan=plan,
                revision_source=sources[val_id],
                family_display=DISPLAY_NAME[G1_CODE[800 + index]],
                counterpart=val_id,
            )
        )
    return cases


def _prepared(case: ReviewCase, shown_id: str) -> PreparedCase:
    resident = dict(case.resident)
    resident["case_id_code"] = shown_id
    clinical = resident.get("ClinicalCase")
    if isinstance(clinical, dict):
        clinical = dict(clinical)
        clinical["case_id_code"] = shown_id
        clinical["title"] = shown_id
        resident["ClinicalCase"] = clinical
    return PreparedCase(
        case_id=shown_id,
        resident=resident,
        investigator={
            "control_error_status": "NO INTENTIONAL ERROR",
            "error": {"error_category": "none"},
        },
        plan={},
    )


def _clear_properties(document: WordDocument, title: str) -> None:
    props = document.core_properties
    props.author = ""
    props.last_modified_by = ""
    props.title = title
    props.subject = ""
    props.category = ""
    props.keywords = ""
    props.comments = ""
    props.identifier = ""


def _write_round1_instructions(
    document: WordDocument,
    *,
    filename_pattern: str,
    case_ids: list[str],
) -> None:
    _add_body(
        document,
        "Purpose: Clinical validation of synthetic medication-reconciliation "
        "and transition-of-care assessment cases.",
    )
    _add_text_field(document, "Reviewer code", tag="reviewer-code", alias="Reviewer code")
    _add_text_field(document, "Review date", tag="review-date", alias="Review date")
    _add_body(document, "Please select one response per item unless otherwise indicated.")
    _add_body(
        document,
        "These are clinician-validation documents. They contain case-specific "
        "validation references that will not be shown to residents during the "
        "later assessment study.",
    )
    _add_heading(document, "How to review each case", 1)
    _add_body(document, "Step 1. Read the clinical case first.")
    _add_body(
        document,
        "Step 2. Complete C1 — Clinical plausibility before using the case-specific "
        "validation reference.",
    )
    _add_body(document, "Step 3. Read the Validation Reference immediately following C1.")
    _add_body(document, "Step 4. Complete C2 through C5.")
    _add_body(document, "Step 5. Select Accept, Revise, or Exclude.")
    _add_body(document, "Step 6. Add comments where required or useful.")
    _add_body(
        document,
        "C1 should reflect your impression of the patient-facing case. "
        "Do not use the validation reference to decide C1.",
    )
    _add_heading(document, "Clean control", 2)
    _add_body(
        document,
        "A clean-control case contains no deliberately introduced "
        "medication-reconciliation or transition-of-care discrepancy. "
        "Still look actively for unintended clinical problems.",
    )
    _add_body(
        document,
        "Every case in this book is a clean case. C2 uses the clean-case question. "
        "There is no planted medication-reconciliation discrepancy.",
    )
    _add_heading(document, "Saving your completed review", 1)
    _add_body(
        document,
        "Please save a separate copy of this document before entering your ratings. "
        "Do not overwrite the original review file.",
    )
    _add_body(document, f"Filename: {filename_pattern}")
    _add_body(
        document,
        "Use the reviewer code assigned by the study team. Do not put a full name "
        "in the filename.",
    )
    _add_heading(document, "Returning your completed validation", 1)
    _add_body(
        document,
        "Return the completed Word document to the study investigator using the "
        "agreed study communication channel.",
    )
    _add_body(
        document,
        "Reviewers do not need to edit GitHub, open a pull request, or upload their "
        "completed validation to the public repository.",
    )
    _add_body(document, "Cases in this document:")
    _add_body(document, ", ".join(case_ids))


def _append_case(
    document: WordDocument,
    case: ReviewCase,
    *,
    shown_id: str,
    header_title: str,
    counterpart: str | None,
    blinded: bool,
) -> None:
    header = shown_id if blinded else None
    _start_case_section(document, header_title, shown_id, header_text=header)
    prepared = _prepared(case, shown_id)
    _render_case(
        document,
        prepared.resident,
        page_break=False,
        heading_text=f"CASE {shown_id}",
    )
    _write_validation(
        document,
        prepared,
        reference_plan=case.reference_plan,
        counterpart=None if blinded else counterpart,
    )


def _save(document: WordDocument, path: Path, *, title: str) -> None:
    _clear_properties(document, title)
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(path))
    finalize_word_form(path)


def render_identified_casebook(
    cases: list[ReviewCase],
    destination: Path,
    *,
    title: str,
    footer: str,
    filename_pattern: str,
    intro: list[str],
    show_revision_source: bool,
) -> None:
    document = _new_document(footer)
    prepare_form_document(document)
    _add_heading(document, title, 0)
    for paragraph in intro:
        _add_body(document, paragraph)
    _add_body(
        document,
        "Status: pending clinician review. These cases are not clinically validated.",
    )
    if show_revision_source:
        _add_heading(document, "Revision source", 1)
        for case in cases:
            _add_body(document, f"{case.case_id}: {case.revision_source}")
    _write_round1_instructions(
        document,
        filename_pattern=filename_pattern,
        case_ids=[case.case_id for case in cases],
    )
    for case in cases:
        _append_case(
            document,
            case,
            shown_id=case.case_id,
            header_title=title,
            counterpart=case.counterpart,
            blinded=False,
        )
    _save(document, destination, title=title)


def _neutral_ids(rng: random.Random, count: int) -> list[str]:
    chosen: list[str] = []
    while len(chosen) < count:
        token = f"N-{rng.randrange(16**4):04X}"
        if token in chosen:
            continue
        if any(str(number) in token for number in range(801, 825)):
            continue
        chosen.append(token)
    return chosen


def blinded_order(
    generation1: list[ReviewCase],
    generation2: list[ReviewCase],
) -> list[tuple[str, ReviewCase]]:
    by_g1 = {case.case_id: case for case in generation1}
    by_g2 = {case.case_id: case for case in generation2}
    mapping = _load_json(BLINDING_MAP)["neutral_study_id_by_case"]
    rng = random.Random(BLIND_SEED)
    tokens = _neutral_ids(rng, 48)
    ordered: list[tuple[str, ReviewCase]] = []
    cursor = 0
    for index in range(801, 825):
        val_id = f"VAL-{index}"
        g2_id = f"G2-{index - 800:03d}"
        pair_id = mapping[val_id]
        if mapping[g2_id] != pair_id:
            raise ValueError(f"{val_id} and {g2_id} do not share a blinding pair id")
        members = [(tokens[cursor], by_g1[val_id]), (tokens[cursor + 1], by_g2[g2_id])]
        cursor += 2
        rng.shuffle(members)
        ordered.extend(members)
    return ordered


def render_blinded_casebook(
    generation1: list[ReviewCase],
    generation2: list[ReviewCase],
    destination: Path,
) -> list[dict[str, str]]:
    ordered = blinded_order(generation1, generation2)
    document = _new_document(NEUTRAL_FOOTER)
    prepare_form_document(document)
    title = "CliniProof clinical validation"
    _add_heading(document, title, 0)
    _add_body(
        document,
        "Status: pending clinician review. These cases are not clinically validated.",
    )
    _add_body(
        document,
        "Each chart is identified only by the neutral case ID printed on that chart.",
    )
    _write_round1_instructions(
        document,
        filename_pattern="CliniProof_Paired_Blinded_[ReviewerCode]_[YYYY-MM-DD].docx",
        case_ids=[shown for shown, _case in ordered],
    )
    rows: list[dict[str, str]] = []
    for shown_id, case in ordered:
        _append_case(
            document,
            case,
            shown_id=shown_id,
            header_title=title,
            counterpart=None,
            blinded=True,
        )
        rows.append({"blinded_id": shown_id, "source_id": case.case_id})
    _save(document, destination, title=title)
    return rows


def write_response_template(path: Path, case_ids: list[str]) -> None:
    labels = item_labels()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_id",
                "case_type",
                "error_category",
                "item",
                "reviewer_1_rating",
                "reviewer_2_rating",
                "agree",
                "abs_diff_c1",
                "reviewer_1_comment",
                "reviewer_2_comment",
                "flag",
            ],
        )
        writer.writeheader()
        for case_id in case_ids:
            for item in labels:
                writer.writerow(
                    {
                        "case_id": case_id,
                        "case_type": "Clean control",
                        "error_category": "",
                        "item": item,
                        "reviewer_1_rating": "",
                        "reviewer_2_rating": "",
                        "agree": "",
                        "abs_diff_c1": "",
                        "reviewer_1_comment": "",
                        "reviewer_2_comment": "",
                        "flag": "",
                    }
                )


def write_case_links(
    generation1: list[ReviewCase],
    blinded_rows: list[dict[str, str]],
    *,
    g1_pages: dict[str, int],
    g2_pages: dict[str, int],
) -> None:
    blinded_by_source = {row["source_id"]: row["blinded_id"] for row in blinded_rows}
    LINKS.parent.mkdir(parents=True, exist_ok=True)
    with LINKS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "pair_id",
                "val_id",
                "g2_id",
                "family",
                "g1_revision_source",
                "g1_casebook_page",
                "g2_casebook_page",
                "blinded_id_g1",
                "blinded_id_g2",
            ],
        )
        writer.writeheader()
        mapping = _load_json(BLINDING_MAP)["neutral_study_id_by_case"]
        for case in generation1:
            val_id = case.case_id
            g2_id = case.counterpart
            writer.writerow(
                {
                    "pair_id": mapping[val_id],
                    "val_id": val_id,
                    "g2_id": g2_id,
                    "family": case.family_display,
                    "g1_revision_source": case.revision_source,
                    "g1_casebook_page": g1_pages.get(val_id, ""),
                    "g2_casebook_page": g2_pages.get(g2_id, ""),
                    "blinded_id_g1": blinded_by_source[val_id],
                    "blinded_id_g2": blinded_by_source[g2_id],
                }
            )


def write_unblinding_key(
    generation1: list[ReviewCase],
    blinded_rows: list[dict[str, str]],
    *,
    blinded_pages: dict[str, int],
) -> None:
    by_source = {case.case_id: case for case in generation1}
    mapping = _load_json(BLINDING_MAP)["neutral_study_id_by_case"]
    order = [row["source_id"] for row in blinded_rows]
    pairs: list[dict[str, Any]] = []
    for index in range(801, 825):
        val_id = f"VAL-{index}"
        g2_id = f"G2-{index - 800:03d}"
        members = []
        for source_id in (val_id, g2_id):
            blinded_id = next(
                row["blinded_id"] for row in blinded_rows if row["source_id"] == source_id
            )
            members.append(
                {
                    "blinded_id": blinded_id,
                    "source_id": source_id,
                    "cohort": "generation_1" if source_id.startswith("VAL-") else "generation_2",
                    "blinded_casebook_page": blinded_pages.get(blinded_id, ""),
                }
            )
        members.sort(key=lambda item: order.index(str(item["source_id"])))
        pairs.append(
            {
                "pair_id": mapping[val_id],
                "family": by_source[val_id].family_display,
                "g1_revision_source": by_source[val_id].revision_source,
                "document_order": [item["blinded_id"] for item in members],
                "members": members,
            }
        )
    payload = {
        "investigator_only": True,
        "do_not_send_to_reviewers": True,
        "order_seed": BLIND_SEED,
        "pair_order": (
            "Neutral pair id from data/case_sets/synthea_g2/blinding_map.json, ascending."
        ),
        "within_pair": (
            "random.Random(order_seed) shuffles the two members after the pair ids are sorted. "
            "The same generator draws the neutral chart ids."
        ),
        "pairs": pairs,
    }
    UNBLINDING_KEY.parent.mkdir(parents=True, exist_ok=True)
    UNBLINDING_KEY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_all(validation_dir: Path | None = None) -> dict[str, Path]:
    destination = validation_dir or VALIDATION
    generation1 = load_generation1()
    generation2 = load_generation2()
    outputs = {
        "g1": destination / "CliniProof_Revised_G1_Casebook.docx",
        "overlap": destination / "CliniProof_Revised_Overlap4_Codebook.docx",
        "remaining": destination / "CliniProof_Revised_Remaining20_Codebook.docx",
        "g2": destination / "CliniProof_Synthea_G2_Clinical_Validation.docx",
        "blinded": destination / "CliniProof_Paired_Blinded_Casebook.docx",
    }
    render_identified_casebook(
        generation1,
        outputs["g1"],
        title="CliniProof revised Generation 1 cases",
        footer="CliniProof revised Generation 1",
        filename_pattern="CliniProof_Revised_G1_[ReviewerCode]_[YYYY-MM-DD].docx",
        intro=[
            "Cohort: revised Generation 1, VAL-801–VAL-824.",
            (
                "These 24 charts were revised from the clean base. "
                "They are the current Generation 1 review set."
            ),
        ],
        show_revision_source=True,
    )
    overlap_ids = {"VAL-801", "VAL-805", "VAL-809", "VAL-813"}
    render_identified_casebook(
        [case for case in generation1 if case.case_id in overlap_ids],
        outputs["overlap"],
        title="CliniProof revised overlap cases",
        footer="CliniProof revised overlap cases",
        filename_pattern="CliniProof_Revised_Overlap4_[ReviewerCode]_[YYYY-MM-DD].docx",
        intro=[
            "Cohort: the four cases revised directly from dual-clinician feedback.",
            "Cases: VAL-801, VAL-805, VAL-809, and VAL-813.",
        ],
        show_revision_source=True,
    )
    render_identified_casebook(
        [case for case in generation1 if case.case_id not in overlap_ids],
        outputs["remaining"],
        title="CliniProof framework-revised cases",
        footer="CliniProof framework-revised cases",
        filename_pattern="CliniProof_Revised_Remaining20_[ReviewerCode]_[YYYY-MM-DD].docx",
        intro=[
            "Cohort: the twenty cases revised with the frozen framework.",
            (
                "VAL-802 and VAL-803 also use Reviewer 1 feedback. "
                "The other eighteen had no case-specific clinician comment."
            ),
        ],
        show_revision_source=True,
    )
    render_identified_casebook(
        generation2,
        outputs["g2"],
        title="CliniProof Generation 2 clinical validation",
        footer="CliniProof Generation 2 clinical validation",
        filename_pattern="CliniProof_Synthea_G2_[ReviewerCode]_[YYYY-MM-DD].docx",
        intro=[
            "Cohort: Generation 2, G2-001–G2-024.",
            (
                "These cases are synthetic. They have passed automated checks. "
                "They are not clinically validated."
            ),
            "G2 identifiers are candidate identifiers, not frozen VAL study identifiers.",
        ],
        show_revision_source=False,
    )
    blinded_rows = render_blinded_casebook(generation1, generation2, outputs["blinded"])
    write_response_template(
        destination / "CliniProof_Revised_G1_Casebook_response_template.csv",
        [case.case_id for case in generation1],
    )
    write_response_template(
        destination / "CliniProof_Revised_Overlap4_Codebook_response_template.csv",
        [c.case_id for c in generation1 if c.case_id in overlap_ids],
    )
    write_response_template(
        destination / "CliniProof_Revised_Remaining20_Codebook_response_template.csv",
        [c.case_id for c in generation1 if c.case_id not in overlap_ids],
    )
    write_response_template(
        destination / "CliniProof_Synthea_G2_Clinical_Validation_response_template.csv",
        [c.case_id for c in generation2],
    )
    write_response_template(
        destination / "CliniProof_Paired_Blinded_Casebook_response_template.csv",
        [row["blinded_id"] for row in blinded_rows],
    )
    write_case_links(generation1, blinded_rows, g1_pages={}, g2_pages={})
    write_unblinding_key(generation1, blinded_rows, blinded_pages={})
    return outputs


def pages_for_headings(pdf_text: str, headings: list[str]) -> dict[str, int]:
    pages = pdf_text.split("\f")
    found: dict[str, int] = {}
    for heading in headings:
        needle = f"CASE {heading}"
        for number, page in enumerate(pages, start=1):
            if needle in page:
                found[heading] = number
                break
    return found


def zip_text(path: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.startswith(("word/", "docProps/", "customXml/")) and name.endswith(".xml"):
                chunks.append(archive.read(name).decode("utf-8", errors="replace"))
    return "\n".join(chunks)


_INSTRUMENT_PARAGRAPHS = {
    "C1 — Clinical plausibility",
    (
        "Could this reasonably represent a patient encountered in the stated "
        "inpatient clinical setting?"
    ),
    (
        "A rating of 1 means implausible. A rating of 2 means questionable and "
        "requires revision. A rating of 3 means plausible with minor concern. "
        "A rating of 4 means fully plausible. Any domain rated 1 or 2 needs a "
        "written explanation. C1 passes when every clinically relevant domain "
        "is rated 3 or 4."
    ),
    "Validation Reference",
    (
        "The reviewer should actively inspect this case for any unintended "
        "clinically meaningful discrepancy."
    ),
    "C2 — Intended assessment problem",
    (
        "Does this case appropriately contain no deliberately introduced "
        "medication-reconciliation or transition-of-care problem?"
    ),
    "C3 — Detectability",
    "Does the case avoid misleading cues suggesting that an error must exist?",
    "C4 — Absence of unintended competing problems",
    (
        "Does the case contain any clinically meaningful "
        "medication-reconciliation or transition-of-care problem that should "
        "not be present?"
    ),
    "If C4 fails",
    "C5 — Expected learner difficulty",
    (
        "This is an expert estimate only. Actual difficulty will ultimately "
        "be determined from resident performance."
    ),
    "Overall recommendation",
    "Accept: the case is suitable for use without clinically meaningful revision.",
    "Revise: the case requires one or more changes before it should be used.",
    (
        "Exclude: the case should not be used, because its problems cannot be "
        "reasonably corrected without substantially reconstructing it."
    ),
}


def _table_marker(table: Any) -> str | None:
    cells = [cell.text.strip() for row in table.rows for cell in row.cells]
    joined = " | ".join(cells)
    if cells[:5] == ["Domain", "1", "2", "3", "4"]:
        return "C1 domains: " + " / ".join(cells[5::5])
    if "Medication / clinical issue" in cells and "Where it appears in the case" in cells:
        return "C4 fields: " + " / ".join(cell for cell in cells if cell)
    if cells[:2] == ["Field", "Validation reference"] and "Clean control" in cells:
        return "Clean reference: " + " / ".join(cells)
    banner = "For clinician validation only. This section would not"
    if any(cell.startswith(banner) for cell in cells):
        match = next(cell for cell in cells if cell.startswith(banner))
        return str(match)
    for label in (
        "C1 reviewer comments",
        "C2 reviewer comments",
        "C3 reviewer comments",
        "C4 reviewer comments",
        "C5 reviewer comments",
        "Overall comments / suggested revisions",
    ):
        if label in joined:
            return label
    return None


def instrument_markers(document: WordDocument) -> list[str]:
    """Fixed instrument strings in document order, skipping case-specific reference rows."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    markers: list[str] = []
    for kind, element in iter_blocks(document):
        if kind == "p":
            text = Paragraph(element, document).text.strip()
            if text in _INSTRUMENT_PARAGRAPHS:
                markers.append(text)
            continue
        marker = _table_marker(Table(element, document))
        if marker:
            markers.append(marker)
    return markers


def template_instrument() -> list[str]:
    document = Document(str(VALIDATION / "CliniProof_Clinical_Validation_Template.docx"))
    markers = instrument_markers(document)
    # The template repeats the instrument once per case. Keep the first cycle.
    first = markers.index("C1 — Clinical plausibility")
    second = markers.index("C1 — Clinical plausibility", first + 1)
    return markers[first:second]


def iter_blocks(document: WordDocument) -> list[Any]:
    blocks: list[Any] = []
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            blocks.append(("p", child))
        elif child.tag == qn("w:tbl"):
            blocks.append(("t", child))
    return blocks
