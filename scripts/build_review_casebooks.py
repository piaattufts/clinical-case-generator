"""Render the revised and paired casebooks and record their page numbers."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.review_casebook import (  # noqa: E402
    blinded_order,
    build_all,
    load_generation1,
    load_generation2,
    pages_for_headings,
    write_case_links,
    write_unblinding_key,
)


def _pdf_text(docx: Path, work: Path) -> str:
    work.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "soffice",
            "--headless",
            "--norestore",
            "--convert-to",
            "pdf",
            "--outdir",
            str(work),
            str(docx),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    pdf = work / f"{docx.stem}.pdf"
    return subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)


def main() -> None:
    outputs = build_all()
    generation1 = load_generation1()
    generation2 = load_generation2()
    blinded = blinded_order(generation1, generation2)
    work = Path("/tmp/cliniproof-casebook-pages")
    g1_pages = pages_for_headings(
        _pdf_text(outputs["g1"], work / "g1"),
        [case.case_id for case in generation1],
    )
    g2_pages = pages_for_headings(
        _pdf_text(outputs["g2"], work / "g2"),
        [case.case_id for case in generation2],
    )
    blinded_pages = pages_for_headings(
        _pdf_text(outputs["blinded"], work / "blinded"),
        [shown for shown, _case in blinded],
    )
    missing = [
        case.case_id
        for case in generation1
        if case.case_id not in g1_pages or case.counterpart not in g2_pages
    ]
    if missing or len(blinded_pages) != 48:
        raise SystemExit(f"page lookup incomplete: {missing} blinded={len(blinded_pages)}")
    blinded_rows = [{"blinded_id": shown, "source_id": case.case_id} for shown, case in blinded]
    write_case_links(generation1, blinded_rows, g1_pages=g1_pages, g2_pages=g2_pages)
    write_unblinding_key(generation1, blinded_rows, blinded_pages=blinded_pages)
    print("g1 pages", g1_pages["VAL-801"], g1_pages["VAL-824"])
    print("g2 pages", g2_pages["G2-001"], g2_pages["G2-024"])
    print("blinded pages", min(blinded_pages.values()), max(blinded_pages.values()))


if __name__ == "__main__":
    main()
