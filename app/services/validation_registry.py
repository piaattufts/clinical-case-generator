"""Single registry of active versus archived CliniProof validation batches."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.services.bootstrap import load_json_object

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "data" / "validation_registry.json"

STRATEGY_BALANCED = "balanced_structured"
STRATEGY_SEED = "resident_seed_guided"
STRATEGY_ORIGINAL = "original_template_randomized"
STRATEGY_TEMPLATE_INTERNAL = "randomized_template"

SEED_STRATEGIES = frozenset({STRATEGY_SEED})
TEMPLATE_STRATEGIES = frozenset(
    {STRATEGY_TEMPLATE_INTERNAL, STRATEGY_BALANCED, STRATEGY_ORIGINAL}
)

BALANCED_BATCH_CODE = "CLINIPROOF_BALANCED_V3"
SEEDCASES_BATCH_CODE = "CLINIPROOF_SEEDCASES_V2"
ARCHIVED_BATCH_CODE = "CLINIPROOF_TAXONOMY_V1"
PRECLINICAL_BALANCED_CODE = "CLINIPROOF_BALANCED_V2"
PRECLINICAL_SEED_CODE = "CLINIPROOF_SEEDCASES_V1"


@dataclass(frozen=True)
class BatchSpec:
    code: str
    status: str
    generation_strategy: str
    directory: Path
    plan_path: Path
    readable_dir: Path
    public_id_first: str
    public_id_last: str
    case_count: int
    description: str

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def is_archived(self) -> bool:
        return self.status == "archived"

    def case_ids(self) -> tuple[str, ...]:
        start = int(self.public_id_first.removeprefix("VAL-"))
        end = int(self.public_id_last.removeprefix("VAL-"))
        return tuple(f"VAL-{index:03d}" for index in range(start, end + 1))


def load_registry(path: Path | None = None) -> dict[str, Any]:
    return load_json_object(path or REGISTRY_PATH)


def _spec_from_mapping(code: str, item: dict[str, Any]) -> BatchSpec:
    return BatchSpec(
        code=code,
        status=str(item.get("status") or ""),
        generation_strategy=str(item.get("generation_strategy") or ""),
        directory=REPO_ROOT / str(item["directory"]),
        plan_path=REPO_ROOT / str(item["plan"]),
        readable_dir=REPO_ROOT / str(item["readable"]),
        public_id_first=str(item["public_id_first"]),
        public_id_last=str(item["public_id_last"]),
        case_count=int(item["case_count"]),
        description=str(item.get("description") or ""),
    )


def all_batch_specs() -> dict[str, BatchSpec]:
    raw = load_registry()
    items = raw.get("batches")
    if not isinstance(items, dict):
        raise ValueError("validation registry must contain a batches object")
    specs = {
        str(code): _spec_from_mapping(str(code), payload)
        for code, payload in items.items()
        if isinstance(payload, dict)
    }
    if not specs:
        raise ValueError("validation registry has no batches")
    return specs


def get_batch(code: str) -> BatchSpec:
    specs = all_batch_specs()
    try:
        return specs[code]
    except KeyError as exc:
        known = ", ".join(sorted(specs))
        raise KeyError(f"unknown validation batch {code!r}; known: {known}") from exc


def active_batch_codes() -> tuple[str, ...]:
    raw = load_registry()
    codes = raw.get("active_validation_batches")
    if not isinstance(codes, list) or not codes:
        raise ValueError("registry must list active_validation_batches")
    return tuple(str(item) for item in codes)


def archived_batch_codes() -> tuple[str, ...]:
    raw = load_registry()
    codes = raw.get("archived_validation_batches") or []
    return tuple(str(item) for item in codes)


def active_batches() -> list[BatchSpec]:
    specs = all_batch_specs()
    return [specs[code] for code in active_batch_codes()]


def archived_batches() -> list[BatchSpec]:
    specs = all_batch_specs()
    return [specs[code] for code in archived_batch_codes() if code in specs]


def is_active_batch(code: str) -> bool:
    return code in active_batch_codes()


def uses_seed_archetypes(strategy: str | None) -> bool:
    return str(strategy or "") in SEED_STRATEGIES


def missing_batch_code_message() -> str:
    lines = [
        "Choose an explicit --batch-code. There is no default study batch.",
        "Active prospective sets:",
    ]
    for spec in active_batches():
        lines.append(
            f"  {spec.code} ({spec.public_id_first}–{spec.public_id_last}) "
            f"strategy={spec.generation_strategy}"
        )
    archived = ", ".join(archived_batch_codes()) or "(none)"
    lines.append(f"Archived historical sets (not active): {archived}")
    return "\n".join(lines)


def missing_plan_message() -> str:
    lines = [
        "Choose an explicit --plan. Freeze does not default to the archived V1 plan.",
        "Active plans:",
    ]
    for spec in active_batches():
        rel = spec.plan_path.relative_to(REPO_ROOT)
        lines.append(f"  {spec.code}: {rel}")
    return "\n".join(lines)


def resolve_export_dir(batch_code: str, output_dir: Path | None) -> Path:
    if output_dir is not None:
        return output_dir
    try:
        return get_batch(batch_code).directory
    except KeyError as exc:
        raise ValueError(
            f"unknown batch {batch_code!r}; pass --output-dir or use an active batch code"
        ) from exc


def public_generation_strategy(batch_code: str, stored: str | None = None) -> str:
    try:
        return get_batch(batch_code).generation_strategy
    except KeyError:
        return stored or STRATEGY_TEMPLATE_INTERNAL
