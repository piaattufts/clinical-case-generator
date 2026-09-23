"""Check active documentation links and manifest agreement.

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
TWO_STAGE = re.compile(
    r"two-stage|two stage|Stage 1|Stage 2|reviewer_protocol|plausibility_only|consensus_worksheet",
    re.IGNORECASE,
)
V1_TOKEN = re.compile(r"CLINIPROOF_TAXONOMY_V1|VAL-201")
V1_CONTEXT = (
    "not the current",
    "not an active",
    "historical",
    "archived",
    "provenance",
    "superseded",
    "preserved",
)

ACTIVE_DOCS = (
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "methods.md",
    ROOT / "docs" / "clinical_validation.md",
    ROOT / "docs" / "error_taxonomy.md",
    ROOT / "docs" / "provenance.md",
    ROOT / "docs" / "repository_structure.md",
    ROOT / "docs" / "developer_guide.md",
    ROOT / "docs" / "clinician_walkthrough" / "README.md",
    ROOT / "data" / "README.md",
    ROOT / "data" / "active_validation_sets.md",
    ROOT / "data" / "case_sets" / "README.md",
    ROOT / "data" / "seed_cases" / "README.md",
    ROOT / "data" / "case_sets" / "balanced" / "README.md",
    ROOT / "data" / "case_sets" / "seed_guided" / "README.md",
    ROOT / "data" / "case_sets" / "investigator" / "clinical_qc_report.md",
)

LINK_ROOTS = (
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "clinical_validation.md",
    ROOT / "docs" / "clinician_walkthrough" / "README.md",
    ROOT / "docs" / "clinician_walkthrough" / "examples" / "README.md",
    ROOT / "docs" / "clinician_walkthrough" / "source_json" / "README.md",
    ROOT / "docs" / "clinician_walkthrough" / "source_json" / "historical" / "README.md",
    ROOT / "docs" / "repository_structure.md",
    ROOT / "docs" / "developer_guide.md",
    ROOT / "data" / "active_validation_sets.md",
    ROOT / "data" / "case_sets" / "README.md",
    ROOT / "data" / "case_sets" / "balanced" / "README.md",
    ROOT / "data" / "case_sets" / "seed_guided" / "README.md",
    ROOT / "data" / "README.md",
    ROOT / "data" / "seed_cases" / "README.md",
    ROOT / "data" / "archive" / "validation_sets" / "README.md",
)

BATCHES = (
    ("CLINIPROOF_BALANCED_V4", "VAL-701", "VAL-724", ROOT / "data" / "case_sets" / "balanced"),
    ("CLINIPROOF_SEEDCASES_V3", "VAL-801", "VAL-824", ROOT / "data" / "case_sets" / "seed_guided"),
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


def _active_language() -> list[str]:
    errors: list[str] = []
    for path in ACTIVE_DOCS:
        text = path.read_text(encoding="utf-8")
        if TWO_STAGE.search(text):
            errors.append(f"{path.relative_to(ROOT)} describes a two-stage review")
        for line in text.splitlines():
            if V1_TOKEN.search(line) and not any(token in line.casefold() for token in V1_CONTEXT):
                detail = line.strip()
                errors.append(
                    f"{path.relative_to(ROOT)} mentions V1 without historical context: {detail}"
                )
    return errors


def _manifests() -> list[str]:
    errors: list[str] = []
    for code, first, last, directory in BATCHES:
        manifest = json.loads((directory / "validation_manifest.json").read_text(encoding="utf-8"))
        plan = json.loads((directory / "batch_plan.json").read_text(encoding="utf-8"))
        ids = [str(row["validation_case_id"]) for row in manifest["cases"]]
        plan_ids = [str(row["validation_case_id"]) for row in plan["cases"]]
        readme = (directory / "README.md").read_text(encoding="utf-8")
        if manifest.get("batch_code") != code or plan.get("batch_code") != code:
            errors.append(f"{code} manifest or plan batch code mismatch")
        if ids != plan_ids or ids[0] != first or ids[-1] != last or len(ids) != 24:
            errors.append(f"{code} VAL range or count does not match the manifest")
        if code not in readme or first not in readme or last not in readme or "24" not in readme:
            errors.append(f"{code} README does not repeat the manifest identity")
        missing = [
            case_id
            for case_id in ids
            if not (directory / "readable" / "cases" / f"{case_id}.md").is_file()
        ]
        if missing:
            errors.append(f"{code} missing readable pages: {', '.join(missing)}")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in LINK_ROOTS:
        errors.extend(_links(path))
    errors.extend(_active_language())
    errors.extend(_manifests())
    if errors:
        print("\n".join(errors))
        return 1
    print("documentation checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
