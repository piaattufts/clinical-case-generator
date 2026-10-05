"""Command line for the scoping-review workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from inthewild_review.agreement import paired_decisions, render_calibration_report
from inthewild_review.ai_assist import record_suggestion
from inthewild_review.calibration import draw_calibration_sample
from inthewild_review.citation_chasing import import_citation_edges
from inthewild_review.config import ReviewLayout
from inthewild_review.deduplicate import write_duplicate_candidates
from inthewild_review.importers import import_export, rebuild_normalized
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.prisma import write_prisma_outputs
from inthewild_review.schemas import (
    DEFAULT_CALIBRATION_N,
    DEFAULT_CALIBRATION_SEED,
    DEFAULT_FUZZY_THRESHOLD,
    FULL_TEXT_FIELDS,
)
from inthewild_review.screening import queue_full_text_rows, validate_title_abstract_rows
from inthewild_review.search_validation import (
    seed_known_items,
    write_search_validation_report,
)
from inthewild_review.synthesis import write_synthesis
from inthewild_review.validation import ValidationFailure, require_valid


def _layout(args: argparse.Namespace) -> ReviewLayout:
    root = Path(args.root).resolve() if args.root else None
    return ReviewLayout(root)


def _cmd_import(args: argparse.Namespace) -> None:
    layout = _layout(args)
    summary = import_export(
        layout,
        Path(args.input),
        args.database,
        explicit_format=args.format,
        notes=args.notes or "",
    )
    print(
        f"Imported {summary['record_count']} records into {summary['batch_id']} "
        f"({summary['source_format']})."
    )
    print("The raw export was not modified. Run normalize to rebuild the canonical table.")


def _cmd_normalize(args: argparse.Namespace) -> None:
    layout = _layout(args)
    rows = rebuild_normalized(layout)
    print(f"Wrote {len(rows)} normalized records to {layout.normalized}.")


def _cmd_duplicates(args: argparse.Namespace) -> None:
    layout = _layout(args)
    rows = write_duplicate_candidates(layout, fuzzy_threshold=args.fuzzy_threshold)
    print(f"Wrote {len(rows)} duplicate candidate pairs to {layout.duplicates}.")
    print("No records were merged or deleted.")


def _cmd_calibration(args: argparse.Namespace) -> None:
    layout = _layout(args)
    meta = draw_calibration_sample(layout, sample_size=args.n, seed=args.seed)
    print(
        f"Drew {meta['drawn_n']} of {meta['population_n']} records "
        f"with seed {meta['random_seed']}."
    )
    print(f"Sample: {layout.calibration_sample}")
    print("Reviewer files were not overwritten where a decision was already saved.")


def _cmd_agreement(args: argparse.Namespace) -> None:
    layout = _layout(args)
    reviewer_1 = read_csv(Path(args.reviewer_1) if args.reviewer_1 else layout.reviewer_1)
    reviewer_2 = read_csv(Path(args.reviewer_2) if args.reviewer_2 else layout.reviewer_2)
    validate_title_abstract_rows(reviewer_1)
    validate_title_abstract_rows(reviewer_2)
    pairs, missing_1, missing_2 = paired_decisions(reviewer_1, reviewer_2)
    sample = read_csv(layout.calibration_sample)
    seed = sample[0].get("random_seed", "") if sample else ""
    method = sample[0].get("sampling_method", "") if sample else ""
    report = render_calibration_report(
        sample_size=len(sample),
        seed=seed,
        method=method,
        pairs=pairs,
        missing_reviewer_1=missing_1,
        missing_reviewer_2=missing_2,
    )
    output = layout.path("outputs", "reports")
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "calibration_report.md"
    destination.write_text(report, encoding="utf-8")
    print(f"Wrote {destination}.")
    print("Reviewer files were not modified.")


def _cmd_prepare_fulltext(args: argparse.Namespace) -> None:
    layout = _layout(args)
    screened = read_csv(layout.title_abstract)
    existing = read_csv(layout.full_text)
    queued = queue_full_text_rows(screened, existing)
    write_csv(layout.full_text, queued, FULL_TEXT_FIELDS, layout.root)
    print(f"Full-text queue has {len(queued)} rows at {layout.full_text}.")
    print("Existing full-text decisions were kept.")


def _cmd_validate(args: argparse.Namespace) -> None:
    layout = _layout(args)
    require_valid(layout)
    print("Validation passed.")


def _cmd_prisma(args: argparse.Namespace) -> None:
    layout = _layout(args)
    counts = write_prisma_outputs(layout)
    included = counts["included"]
    assert isinstance(included, dict)
    print("Wrote outputs/prisma/prisma_counts.json, prisma_counts.csv, prisma_summary.md, and prisma_flow.svg.")
    print(
        "Included units — "
        f"records {included['full_text_include_records']}, "
        f"publications {included['publications']}, "
        f"studies {included['studies']}, "
        f"deployments {included['deployments']}, "
        f"scenarios {included['scenarios']}."
    )


def _cmd_synthesize(args: argparse.Namespace) -> None:
    layout = _layout(args)
    write_synthesis(layout)
    print("Wrote descriptive tables under outputs/tables and figures under outputs/figures.")


def _cmd_citation_import(args: argparse.Namespace) -> None:
    layout = _layout(args)
    rows = read_csv(Path(args.input))
    summary = import_citation_edges(layout, rows)
    print(
        f"Added {summary['edges_added']} edges and {summary['records_added']} citation-chasing records."
    )
    print("New records are not eligible until they pass human screening.")


def _cmd_search_report(args: argparse.Namespace) -> None:
    layout = _layout(args)
    seed_known_items(layout)
    path = write_search_validation_report(layout)
    print("Wrote outputs/reports/search_validation_report.md.")
    print(path.splitlines()[0])


def _cmd_suggest(args: argparse.Namespace) -> None:
    layout = _layout(args)
    record_suggestion(
        layout,
        suggestion_id=args.suggestion_id,
        record_id=args.record_id,
        task=args.task,
        suggested_value=args.suggested_value,
        model_provider=args.model_provider,
        model_name=args.model_name,
        model_version=args.model_version,
        prompt_id=args.prompt_id,
        prompt_text=args.prompt_text,
        notes=args.notes or "",
    )
    print(f"Stored suggestion {args.suggestion_id} in {layout.ai_suggestions}.")
    print("Human screening files were not modified.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inthewild_review",
        description=(
            "Reproducible bookkeeping for the scoping review "
            "Evaluating Social Robots in the Wild. "
            "The commands do not decide inclusion."
        ),
    )
    parser.add_argument(
        "--root",
        default="",
        help="Repository root. Defaults to the directory that contains this package.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser("import-records", help="Import one bibliographic export.")
    import_parser.add_argument("--database", required=True)
    import_parser.add_argument("--input", required=True)
    import_parser.add_argument("--format", default="auto")
    import_parser.add_argument("--notes", default="")
    import_parser.set_defaults(func=_cmd_import)

    normalize_parser = subparsers.add_parser("normalize", help="Rebuild the canonical record table.")
    normalize_parser.set_defaults(func=_cmd_normalize)

    duplicate_parser = subparsers.add_parser("duplicates", help="Flag duplicate candidates.")
    duplicate_parser.add_argument("--fuzzy-threshold", type=float, default=DEFAULT_FUZZY_THRESHOLD)
    duplicate_parser.set_defaults(func=_cmd_duplicates)

    calibration_parser = subparsers.add_parser("calibration", help="Draw the calibration sample.")
    calibration_parser.add_argument("--n", type=int, default=DEFAULT_CALIBRATION_N)
    calibration_parser.add_argument("--seed", type=int, default=DEFAULT_CALIBRATION_SEED)
    calibration_parser.set_defaults(func=_cmd_calibration)

    agreement_parser = subparsers.add_parser("agreement", help="Calculate calibration agreement.")
    agreement_parser.add_argument("--reviewer-1", default="")
    agreement_parser.add_argument("--reviewer-2", default="")
    agreement_parser.set_defaults(func=_cmd_agreement)

    fulltext_parser = subparsers.add_parser(
        "prepare-fulltext",
        help="Queue INCLUDE and MAYBE records for full-text screening.",
    )
    fulltext_parser.set_defaults(func=_cmd_prepare_fulltext)

    validate_parser = subparsers.add_parser("validate", help="Run integrity checks.")
    validate_parser.set_defaults(func=_cmd_validate)

    prisma_parser = subparsers.add_parser("prisma", help="Derive PRISMA counts from the data files.")
    prisma_parser.set_defaults(func=_cmd_prisma)

    synthesize_parser = subparsers.add_parser("synthesize", help="Write descriptive synthesis tables.")
    synthesize_parser.set_defaults(func=_cmd_synthesize)

    citation_parser = subparsers.add_parser(
        "citation-import",
        help="Import citation-chasing edges. Does not mark records eligible.",
    )
    citation_parser.add_argument("--input", required=True)
    citation_parser.set_defaults(func=_cmd_citation_import)

    search_parser = subparsers.add_parser(
        "search-validation-report",
        help="Report which known items have been checked.",
    )
    search_parser.set_defaults(func=_cmd_search_report)

    suggest_parser = subparsers.add_parser(
        "record-suggestion",
        help="Store an optional AI suggestion outside the human screening files.",
    )
    suggest_parser.add_argument("--suggestion-id", required=True)
    suggest_parser.add_argument("--record-id", required=True)
    suggest_parser.add_argument("--task", required=True)
    suggest_parser.add_argument("--suggested-value", required=True)
    suggest_parser.add_argument("--model-provider", required=True)
    suggest_parser.add_argument("--model-name", required=True)
    suggest_parser.add_argument("--model-version", required=True)
    suggest_parser.add_argument("--prompt-id", required=True)
    suggest_parser.add_argument("--prompt-text", required=True)
    suggest_parser.add_argument("--notes", default="")
    suggest_parser.set_defaults(func=_cmd_suggest)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except ValidationFailure as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
