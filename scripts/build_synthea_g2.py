"""Build the Generation 2 Synthea cohort.

    python scripts/build_synthea_g2.py
    python scripts/build_synthea_g2.py audit
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.g2_audit import round1_row  # noqa: E402
from app.services.g2_cohort import (  # noqa: E402
    eligibility_summary,
    write_cohort,
)
from app.services.g2_match import build_matched_cohort, write_matching_artifacts  # noqa: E402
from app.services.g2_render import write_casebook, write_readable  # noqa: E402
from app.services.synthea_import import load_population  # noqa: E402

CONFIG = ROOT / "config" / "synthea.yml"
RAW = ROOT / "data" / "synthea" / "raw" / "fhir"
OUT = ROOT / "data" / "case_sets" / "synthea_g2"
CASEBOOK = ROOT / "docs" / "validation" / "CliniProof_Synthea_G2_Clinical_Validation.docx"


def load_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def meta_from_config(config: dict[str, str]) -> dict[str, str]:
    return {
        "repository": config["repository"],
        "commit": config["commit"],
        "version": config["version"],
        "population_seed": config["seed"],
        "reference_date": config["reference_date"],
        "fhir_version": config["fhir_version"],
        "java_version": config["java_version"],
        "generated_at": "2026-10-08T00:00:00Z",
    }


def build() -> None:
    config = load_config(CONFIG)
    patients, file_counts = load_population(RAW)
    summary = eligibility_summary(patients)
    summary["files"] = file_counts
    meta = meta_from_config(config)
    selected, rejected, attempts = build_matched_cohort(patients, meta)
    summary["matched_pairs"] = len(selected)
    summary["candidate_attempts"] = len(attempts)
    write_cohort(OUT, selected, rejected, summary, meta, {"matched": selected})
    write_matching_artifacts(OUT, selected, attempts)
    write_readable(OUT)
    write_casebook(OUT, CASEBOOK)
    print(json.dumps({"eligible": summary["eligible"], "files": file_counts, "rejected": len(rejected), "final": len(selected)}, indent=2))


def audit() -> None:
    failures = 0
    for path in sorted((OUT / "cases" / "evaluator").glob("G2-*.json")):
        episode = json.loads(path.read_text(encoding="utf-8"))
        row = round1_row(episode, path.stem)
        if not row["overall_pass"]:
            failures += 1
            print(path.stem, row["notes"])
    if failures:
        raise SystemExit(f"{failures} final cases failed audit")
    print("generation 2 audit passed")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "audit":
        audit()
        return
    build()


if __name__ == "__main__":
    main()
