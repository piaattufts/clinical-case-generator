"""Repository paths and review constants that are not vocabularies."""

from __future__ import annotations

from pathlib import Path

from inthewild_review.schemas import DEFAULT_CALIBRATION_N, DEFAULT_CALIBRATION_SEED


def repository_root(start: Path | None = None) -> Path:
    """Find the review repository root from the working directory or this file."""
    current = (start or Path.cwd()).resolve()
    candidates = [current, *current.parents]
    here = Path(__file__).resolve()
    candidates.extend(here.parents)
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        package = candidate / "src" / "inthewild_review" / "__init__.py"
        if package.exists() and (candidate / "pyproject.toml").exists():
            return candidate
    return current


class ReviewLayout:
    """Paths used by the review workflow. All write helpers honor data/raw immutability."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or repository_root()).resolve()

    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    @property
    def raw_dir(self) -> Path:
        return self.path("data", "raw")

    @property
    def batches_dir(self) -> Path:
        return self.path("data", "interim", "batches")

    @property
    def manifest(self) -> Path:
        return self.path("data", "interim", "import_manifest.csv")

    @property
    def normalized(self) -> Path:
        return self.path("data", "interim", "normalized_records.csv")

    @property
    def duplicates(self) -> Path:
        return self.path("data", "interim", "duplicate_candidates.csv")

    @property
    def citation_nodes(self) -> Path:
        return self.path("data", "interim", "citation_graph", "nodes.csv")

    @property
    def citation_edges(self) -> Path:
        return self.path("data", "interim", "citation_graph", "edges.csv")

    @property
    def title_abstract(self) -> Path:
        return self.path("data", "screening", "title_abstract_screening.csv")

    @property
    def calibration_sample(self) -> Path:
        return self.path("data", "screening", "calibration_sample.csv")

    @property
    def calibration_meta(self) -> Path:
        return self.path("data", "screening", "calibration_sampling.json")

    @property
    def reviewer_1(self) -> Path:
        return self.path("data", "screening", "calibration_reviewer_1.csv")

    @property
    def reviewer_2(self) -> Path:
        return self.path("data", "screening", "calibration_reviewer_2.csv")

    @property
    def calibration_consensus(self) -> Path:
        return self.path("data", "screening", "calibration_consensus.csv")

    @property
    def full_text(self) -> Path:
        return self.path("data", "screening", "full_text_screening.csv")

    @property
    def publications(self) -> Path:
        return self.path("data", "extraction", "publications.csv")

    @property
    def studies(self) -> Path:
        return self.path("data", "extraction", "studies.csv")

    @property
    def deployments(self) -> Path:
        return self.path("data", "extraction", "deployments.csv")

    @property
    def scenarios(self) -> Path:
        return self.path("data", "extraction", "scenarios.csv")

    @property
    def extraction_notes(self) -> Path:
        return self.path("data", "extraction", "extraction_notes.csv")

    @property
    def search_validation(self) -> Path:
        return self.path("data", "search_validation.csv")

    @property
    def ai_suggestions(self) -> Path:
        return self.path("data", "screening", "ai_suggestions.csv")

    @property
    def decision_log(self) -> Path:
        return self.path("protocol", "decision_log.csv")


def default_calibration_n() -> int:
    return DEFAULT_CALIBRATION_N


def default_calibration_seed() -> int:
    return DEFAULT_CALIBRATION_SEED
