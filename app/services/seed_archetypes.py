"""Load resident-seed-guided archetypes without mixing them into template scenarios.

Template families stay in data/bootstrap/scenarios.json and keep
generation_strategy=randomized_template. Seed archetypes are a separate file so
CLINIPROOF_TAXONOMY_V1 and CLINIPROOF_BALANCED_V2 are not relabeled.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.services.bootstrap import load_json_object
from app.services.generation import Scenario, _scenario_from_mapping

SEED_BLUEPRINT_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "seed_cases" / "blueprints" / "archetypes.json"
)
SEED_SOURCE_DIR = (
    Path(__file__).resolve().parents[2] / "data" / "seed_cases" / "resident_authored"
)

GENERATION_STRATEGY_TEMPLATE = "randomized_template"
GENERATION_STRATEGY_SEED = "resident_seed_guided"
SEED_SOURCE_TYPE = "resident_authored"
SEEDCASES_BATCH_CODE = "CLINIPROOF_SEEDCASES_V1"

SEED_LEAK_MARKERS = (
    "generation_strategy",
    "resident_seed_guided",
    "seed_archetype",
    "seed_source",
    "resident_authored",
    ".docx",
    "bad_med_rec_case",
    "heart_failure_case",
    "opat_case",
    "post_transplant_case",
    "post-op_case",
    "sepsis_ama",
    "blueprint_version",
)


def load_seed_blueprint_document(path: Path | None = None) -> dict[str, Any]:
    return load_json_object(path or SEED_BLUEPRINT_PATH)


def load_seed_archetypes(path: Path | None = None) -> list[Scenario]:
    raw = load_seed_blueprint_document(path)
    items = raw.get("archetypes")
    if not isinstance(items, list) or not items:
        raise ValueError("seed archetypes file must contain a non-empty archetypes list")
    blueprint_version = str(raw.get("blueprint_version") or "seed-archetypes-v1")
    strategy = str(raw.get("generation_strategy") or GENERATION_STRATEGY_SEED)
    source_type = str(raw.get("seed_source_type") or SEED_SOURCE_TYPE)
    archetypes: list[Scenario] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        payload = dict(item)
        payload.setdefault("generation_strategy", strategy)
        payload.setdefault("seed_source_type", source_type)
        payload.setdefault("blueprint_version", blueprint_version)
        archetypes.append(_scenario_from_mapping(payload))
    if not archetypes:
        raise ValueError("no usable seed archetypes found")
    return archetypes


def seed_provenance(scenario: Scenario) -> dict[str, str]:
    return {
        "generation_strategy": scenario.generation_strategy,
        "seed_archetype_id": scenario.code,
        "seed_archetype_name": scenario.seed_archetype_name or scenario.code,
        "seed_source_type": scenario.seed_source_type or SEED_SOURCE_TYPE,
        "seed_source_filename": scenario.seed_source_filename or "",
        "blueprint_version": scenario.blueprint_version or "",
    }
