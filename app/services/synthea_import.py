"""Load a directory of Synthea FHIR bundles into longitudinal patients."""

from __future__ import annotations

import json
from pathlib import Path

from app.sources.synthea import LongitudinalPatient, parse_bundle


def load_population(directory: Path) -> tuple[list[LongitudinalPatient], dict[str, int]]:
    """Parse every bundle in a directory.

    One file is read at a time so the raw export is not held in memory.
    """
    patients: list[LongitudinalPatient] = []
    skipped = 0
    files = sorted(path for path in directory.glob("*.json") if path.is_file())
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            skipped += 1
            continue
        try:
            patients.append(parse_bundle(payload))
        except ValueError:
            skipped += 1
    alive = sum(1 for patient in patients if not patient.deceased)
    return patients, {
        "fhir_files": len(files),
        "patients_parsed": len(patients),
        "bundles_skipped": skipped,
        "alive": alive,
        "deceased": len(patients) - alive,
    }
