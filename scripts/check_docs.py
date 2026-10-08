"""Check documentation links and the seed-guided manifest.

Run from the repository root:

    python scripts/check_docs.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

LINK_ROOTS = (
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "methodology.md",
    ROOT / "docs" / "provenance.md",
    ROOT / "docs" / "clinical_feedback" / "reviewer_comparison.md",
    ROOT / "docs" / "validation" / "CODEBOOK.md",
    ROOT / "docs" / "repository_cleanup_inventory.md",
    ROOT / "data" / "case_sets" / "seed_guided" / "CLEAN_BASE" / "README.md",
)


def _links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = match.group(1).split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)} -> {target}")
    return errors


def _seed_manifest() -> list[str]:
    directory = ROOT / "data" / "case_sets" / "seed_guided"
    manifest = json.loads((directory / "validation_manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((directory / "batch_plan.json").read_text(encoding="utf-8"))
    ids = [str(row["validation_case_id"]) for row in manifest["cases"]]
    plan_ids = [str(row["validation_case_id"]) for row in plan["cases"]]
    errors: list[str] = []
    if manifest.get("batch_code") != "CLINIPROOF_SEEDCASES_V3":
        errors.append("seed-guided manifest batch code mismatch")
    if plan.get("batch_code") != "CLINIPROOF_SEEDCASES_V3":
        errors.append("seed-guided plan batch code mismatch")
    if ids != plan_ids or ids[0] != "VAL-801" or ids[-1] != "VAL-824" or len(ids) != 24:
        errors.append("seed-guided VAL range or count does not match the manifest")
    missing = [
        case_id
        for case_id in ids
        if not (directory / "readable" / "cases" / f"{case_id}.md").is_file()
    ]
    if missing:
        errors.append("seed-guided missing readable pages: " + ", ".join(missing))
    clean = directory / "CLEAN_BASE"
    for case_id in ids:
        for kind in ("resident", "evaluator"):
            if not (clean / f"{case_id}_{kind}.json").is_file():
                errors.append(f"clean base missing {case_id}_{kind}.json")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in LINK_ROOTS:
        if not path.is_file():
            errors.append(f"missing documentation file {path.relative_to(ROOT)}")
            continue
        errors.extend(_links(path))
    errors.extend(_seed_manifest())
    if errors:
        print("\n".join(errors))
        return 1
    print("documentation checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
