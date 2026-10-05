"""Descriptive tables for included studies.

There is no meta-analysis and no aggregate quality or fidelity score.
NOT_REPORTED_OR_UNCLEAR stays separate from NO.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from inthewild_review.config import ReviewLayout
from inthewild_review.io_utils import read_csv, write_csv
from inthewild_review.schemas import (
    COMPLETENESS_DEPLOYMENT_FIELDS,
    COMPLETENESS_SCENARIO_FIELDS,
    DEPLOYMENT_TRI_STATE_FIELDS,
    PROVENANCE_CODES,
    SCENARIO_TRI_STATE_FIELDS,
    SETTING_TYPES,
)

_TRI_STATE_ORDER = ("YES", "NO", "NOT_REPORTED_OR_UNCLEAR")
_ARNOLD_FIELDS = (
    ("touch_and_physical_contact", "Embodiment and touch"),
    ("competing_interests_in_one_to_one", "Competing interests within one-to-one interaction"),
    ("group_decision_making", "Multi-party or group decision-making"),
)


def included_extraction(layout: ReviewLayout) -> dict[str, list[dict[str, str]]]:
    full_text = read_csv(layout.full_text)
    included_records = {
        (row.get("record_id") or "").strip()
        for row in full_text
        if (row.get("decision") or "").strip() == "INCLUDE"
    }
    publications = [
        row
        for row in read_csv(layout.publications)
        if (row.get("record_id") or "").strip() in included_records
    ]
    publication_ids = {(row.get("publication_id") or "").strip() for row in publications}
    studies = [
        row
        for row in read_csv(layout.studies)
        if (row.get("publication_id") or "").strip() in publication_ids
    ]
    study_ids = {(row.get("study_id") or "").strip() for row in studies}
    deployments = [
        row
        for row in read_csv(layout.deployments)
        if (row.get("study_id") or "").strip() in study_ids
    ]
    deployment_ids = {(row.get("deployment_id") or "").strip() for row in deployments}
    scenarios = [
        row
        for row in read_csv(layout.scenarios)
        if (row.get("deployment_id") or "").strip() in deployment_ids
    ]
    return {
        "publications": publications,
        "studies": studies,
        "deployments": deployments,
        "scenarios": scenarios,
    }


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    rule = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([head, rule, *body]) + "\n"


def _csv_rows(headers: list[str], rows: list[list[str]]) -> list[dict[str, str]]:
    return [dict(zip(headers, row, strict=True)) for row in rows]


def _write_pair(
    layout: ReviewLayout,
    stem: str,
    title: str,
    prose: str,
    headers: list[str],
    rows: list[list[str]],
) -> None:
    table_dir = layout.path("outputs", "tables")
    table_dir.mkdir(parents=True, exist_ok=True)
    write_csv(table_dir / f"{stem}.csv", _csv_rows(headers, rows), headers, layout.root)
    text = f"# {title}\n\n{prose}\n\n" + _markdown_table(headers, rows)
    (table_dir / f"{stem}.md").write_text(text, encoding="utf-8")


def _is_definite(value: str) -> bool:
    cleaned = value.strip()
    return bool(cleaned) and cleaned not in {"NOT_REPORTED_OR_UNCLEAR", "UNCLEAR"}


def _tri_counts(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    counts = Counter((row.get(field) or "").strip() or "BLANK" for row in rows)
    return {
        "YES": int(counts.get("YES", 0)),
        "NO": int(counts.get("NO", 0)),
        "NOT_REPORTED_OR_UNCLEAR": int(counts.get("NOT_REPORTED_OR_UNCLEAR", 0)),
        "BLANK": int(counts.get("BLANK", 0)),
    }


def _deployment_by_id(deployments: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {(row.get("deployment_id") or "").strip(): row for row in deployments}


def _provenance_parts(row: dict[str, str]) -> list[str]:
    return [part.strip() for part in (row.get("provenance_codes") or "").split("|") if part.strip()]


def _cross(
    pairs: list[tuple[str, str]],
) -> list[list[str]]:
    counts: dict[tuple[str, str], int] = Counter(pairs)
    return [
        [left, right, str(counts[(left, right)])]
        for left, right in sorted(counts)
    ]


def build_tables(layout: ReviewLayout) -> dict[str, list[list[str]]]:
    data = included_extraction(layout)
    publications = data["publications"]
    studies = data["studies"]
    deployments = data["deployments"]
    scenarios = data["scenarios"]
    studies_by_publication: dict[str, list[dict[str, str]]] = defaultdict(list)
    for study in studies:
        studies_by_publication[study.get("publication_id", "")].append(study)

    table_1: list[list[str]] = []
    if not publications:
        table_1.append(["", "", "", "", "", "No included publications are in the extraction tables."])
    for publication in publications:
        linked = studies_by_publication.get(publication.get("publication_id", ""), [])
        if not linked:
            table_1.append(
                [
                    publication.get("publication_id", ""),
                    publication.get("year", ""),
                    publication.get("authors", ""),
                    publication.get("title", ""),
                    "",
                    publication.get("venue", ""),
                ]
            )
            continue
        for study in linked:
            table_1.append(
                [
                    publication.get("publication_id", ""),
                    publication.get("year", ""),
                    publication.get("authors", ""),
                    publication.get("title", ""),
                    study.get("study_id", ""),
                    publication.get("venue", ""),
                ]
            )
    _write_pair(
        layout,
        "table_01_included_publications",
        "Table 1. Included publications and studies",
        "One publication can contain more than one study. An empty study id means no study row has been entered yet.",
        ["publication_id", "year", "authors", "title", "study_id", "venue"],
        table_1,
    )

    setting_counts = Counter((row.get("setting_type") or "").strip() or "BLANK" for row in deployments)
    table_2 = [
        [setting, str(setting_counts.get(setting, 0))]
        for setting in [*SETTING_TYPES, "BLANK"]
        if setting_counts.get(setting, 0) or setting in SETTING_TYPES
    ]
    _write_pair(
        layout,
        "table_02_settings",
        "Table 2. Primary deployment settings",
        (
            "Counts are deployments, not publications. "
            "additional_setting_types is not folded into this primary count. "
            "LABORATORY_REPEATED_EVERYDAY is an eligibility category, not a high-fidelity use setting."
        ),
        ["setting_type", "deployments"],
        table_2,
    )

    table_3 = [
        [
            row.get("deployment_id", ""),
            row.get("setting_type", ""),
            row.get("number_of_sessions", ""),
            row.get("total_period", ""),
            row.get("total_period_unit", ""),
            row.get("session_length", ""),
            row.get("continuous_vs_episodic", ""),
            row.get("novelty_or_habituation_reported", ""),
        ]
        for row in deployments
    ] or [["", "", "", "", "", "", "", "No included deployments."]]
    _write_pair(
        layout,
        "table_03_duration",
        "Table 3. Duration and exposure",
        "Duration is listed as reported. No short/long bins are applied.",
        [
            "deployment_id",
            "setting_type",
            "number_of_sessions",
            "total_period",
            "total_period_unit",
            "session_length",
            "continuous_vs_episodic",
            "novelty_or_habituation_reported",
        ],
        table_3,
    )

    table_4 = [
        [
            row.get("deployment_id", ""),
            row.get("robot_platform", ""),
            row.get("embodiment", ""),
            row.get("autonomy_reported", ""),
            row.get("autonomy_level", ""),
            row.get("single_or_multiple_embodiments", ""),
        ]
        for row in deployments
    ] or [["", "", "", "", "", "No included deployments."]]
    _write_pair(
        layout,
        "table_04_robot_autonomy",
        "Table 4. Robot platform and autonomy",
        "Autonomy is quoted from the extraction text. It is not recoded onto an invented scale.",
        [
            "deployment_id",
            "robot_platform",
            "embodiment",
            "autonomy_reported",
            "autonomy_level",
            "single_or_multiple_embodiments",
        ],
        table_4,
    )

    provenance_counts: Counter[str] = Counter()
    for scenario in scenarios:
        for part in _provenance_parts(scenario):
            provenance_counts[part] += 1
    table_5 = [[code, str(provenance_counts.get(code, 0))] for code in PROVENANCE_CODES]
    _write_pair(
        layout,
        "table_05_scenario_provenance",
        "Table 5. Scenario provenance",
        (
            f"Denominator is {len(scenarios)} included scenarios. "
            "A scenario with more than one provenance code is counted once in each listed code. "
            "The column does not sum to the number of scenarios."
        ),
        ["provenance_code", "scenarios"],
        table_5,
    )

    content_fields = [field for field in SCENARIO_TRI_STATE_FIELDS]
    table_6 = []
    for field in content_fields:
        counts = _tri_counts(scenarios, field)
        table_6.append(
            [
                field,
                str(counts["YES"]),
                str(counts["NO"]),
                str(counts["NOT_REPORTED_OR_UNCLEAR"]),
                str(counts["BLANK"]),
            ]
        )
    _write_pair(
        layout,
        "table_06_scenario_content",
        "Table 6. Scenario representational content",
        "NO and NOT_REPORTED_OR_UNCLEAR are separate. Blank means the cell was not coded.",
        ["field", "YES", "NO", "NOT_REPORTED_OR_UNCLEAR", "BLANK"],
        table_6,
    )

    measure_fields = (
        "observational_data",
        "log_data",
        "interviews",
        "qualitative_methods",
    )
    table_7 = []
    for field in measure_fields:
        counts = _tri_counts(deployments, field)
        table_7.append(
            [field, str(counts["YES"]), str(counts["NO"]), str(counts["NOT_REPORTED_OR_UNCLEAR"])]
        )
    _write_pair(
        layout,
        "table_07_measures",
        "Table 7. Evaluation measures and outcomes",
        (
            "The tri-state rows record whether that class of evidence was reported. "
            "Free-text constructs, instruments, and outcome descriptions stay on the deployment rows "
            "and are not scored."
        ),
        ["evidence_class", "YES", "NO", "NOT_REPORTED_OR_UNCLEAR"],
        table_7,
    )

    tradeoff_fields = (
        "safety_measures",
        "technician_oversight",
        "consent_shared_group_spaces",
        "private_setting_data_collection",
        "reported_fidelity_control_limitations",
        "physical_fidelity_reported",
        "contextual_fidelity_reported",
    )
    table_8 = []
    for field in tradeoff_fields:
        counts = _tri_counts(deployments, field)
        table_8.append(
            [field, str(counts["YES"]), str(counts["NO"]), str(counts["NOT_REPORTED_OR_UNCLEAR"])]
        )
    _write_pair(
        layout,
        "table_08_tradeoffs",
        "Table 8. Safety, control, and fidelity reporting",
        (
            "Physical fidelity and contextual fidelity are separate rows. "
            "They are not combined into a fidelity score. "
            "YES means the paper reports the topic. NO means the paper states the topic was absent. "
            "NOT_REPORTED_OR_UNCLEAR means the paper is silent or ambiguous."
        ),
        ["field", "YES", "NO", "NOT_REPORTED_OR_UNCLEAR"],
        table_8,
    )

    availability_fields = (
        "materials_available",
        "scripts_available",
        "code_available",
        "data_available",
    )
    table_9 = []
    for field in availability_fields:
        counts = _tri_counts(deployments, field)
        table_9.append(
            [field, str(counts["YES"]), str(counts["NO"]), str(counts["NOT_REPORTED_OR_UNCLEAR"])]
        )
    _write_pair(
        layout,
        "table_09_reporting_availability",
        "Table 9. Reporting and availability of reusable materials",
        "Availability is coded only from what the paper states. Silence is NOT_REPORTED_OR_UNCLEAR.",
        ["field", "YES", "NO", "NOT_REPORTED_OR_UNCLEAR"],
        table_9,
    )

    deployments_by_id = _deployment_by_id(deployments)
    cross_specs = [
        (
            "cross_provenance_by_setting",
            "Scenario provenance by primary setting",
            [
                (part, deployments_by_id.get(row.get("deployment_id", ""), {}).get("setting_type", ""))
                for row in scenarios
                for part in _provenance_parts(row)
            ],
        ),
        (
            "cross_provenance_by_duration",
            "Scenario provenance by continuous versus episodic exposure",
            [
                (
                    part,
                    deployments_by_id.get(row.get("deployment_id", ""), {}).get(
                        "continuous_vs_episodic", ""
                    ),
                )
                for row in scenarios
                for part in _provenance_parts(row)
            ],
        ),
        (
            "cross_autonomy_by_setting",
            "Autonomy text by primary setting",
            [
                ((row.get("autonomy_level") or "").strip(), (row.get("setting_type") or "").strip())
                for row in deployments
            ],
        ),
        (
            "cross_autonomy_by_duration",
            "Autonomy text by continuous versus episodic exposure",
            [
                (
                    (row.get("autonomy_level") or "").strip(),
                    (row.get("continuous_vs_episodic") or "").strip(),
                )
                for row in deployments
            ],
        ),
        (
            "cross_provenance_by_relationship_history",
            "Scenario provenance by relationship-history representation",
            [
                (part, (row.get("relationships_and_history") or "").strip())
                for row in scenarios
                for part in _provenance_parts(row)
            ],
        ),
        (
            "cross_setting_by_multiparty",
            "Primary setting by multi-party or group interaction",
            [
                (
                    deployments_by_id.get(row.get("deployment_id", ""), {}).get("setting_type", ""),
                    (row.get("multi_party_or_group_interaction") or "").strip(),
                )
                for row in scenarios
            ],
        ),
        (
            "cross_duration_by_temporal_dependencies",
            "Exposure by temporal dependencies",
            [
                (
                    deployments_by_id.get(row.get("deployment_id", ""), {}).get(
                        "continuous_vs_episodic", ""
                    ),
                    (row.get("temporal_dependencies") or "").strip(),
                )
                for row in scenarios
            ],
        ),
        (
            "cross_setting_by_touch",
            "Primary setting by touch or physical contact",
            [
                (
                    deployments_by_id.get(row.get("deployment_id", ""), {}).get("setting_type", ""),
                    (row.get("touch_and_physical_contact") or "").strip(),
                )
                for row in scenarios
            ],
        ),
    ]
    for stem, title, pairs in cross_specs:
        rows = _cross([(left or "BLANK", right or "BLANK") for left, right in pairs]) or [
            ["", "", "0"]
        ]
        _write_pair(
            layout,
            stem,
            title,
            "Multi-code provenance rows contribute to each code. NO is not merged with NOT_REPORTED_OR_UNCLEAR.",
            ["row_value", "column_value", "count"],
            rows,
        )

    arnold_rows: list[list[str]] = []
    for field, label in _ARNOLD_FIELDS:
        for setting in SETTING_TYPES:
            matched = [
                row
                for row in scenarios
                if deployments_by_id.get(row.get("deployment_id", ""), {}).get("setting_type")
                == setting
            ]
            counts = _tri_counts(matched, field)
            arnold_rows.append(
                [
                    label,
                    setting,
                    str(counts["YES"]),
                    str(counts["NO"]),
                    str(counts["NOT_REPORTED_OR_UNCLEAR"]),
                ]
            )
    _write_pair(
        layout,
        "table_arnold_scheutz",
        "Arnold and Scheutz dimensions",
        (
            "Embodiment and touch, competing interests inside one-to-one interaction, "
            "and group decision-making are tabulated separately. "
            "A NOT_REPORTED_OR_UNCLEAR cell is not evidence that the dimension was absent."
        ),
        ["dimension", "setting_type", "YES", "NO", "NOT_REPORTED_OR_UNCLEAR"],
        arnold_rows,
    )

    completeness: list[list[str]] = []
    denominator_deployments = len(deployments)
    denominator_scenarios = len(scenarios)
    for field in COMPLETENESS_DEPLOYMENT_FIELDS:
        if field in DEPLOYMENT_TRI_STATE_FIELDS:
            counts = _tri_counts(deployments, field)
            definite = counts["YES"] + counts["NO"]
            missing = counts["NOT_REPORTED_OR_UNCLEAR"] + counts["BLANK"]
        else:
            definite = sum(1 for row in deployments if _is_definite(row.get(field, "")))
            missing = denominator_deployments - definite
        proportion = "" if denominator_deployments == 0 else f"{definite / denominator_deployments:.4f}"
        completeness.append(
            [
                "deployment",
                field,
                str(denominator_deployments),
                str(definite),
                str(missing),
                proportion,
            ]
        )
    for field in COMPLETENESS_SCENARIO_FIELDS:
        if field in SCENARIO_TRI_STATE_FIELDS:
            counts = _tri_counts(scenarios, field)
            definite = counts["YES"] + counts["NO"]
            missing = counts["NOT_REPORTED_OR_UNCLEAR"] + counts["BLANK"]
        else:
            definite = sum(1 for row in scenarios if _is_definite(row.get(field, "")))
            missing = denominator_scenarios - definite
        proportion = "" if denominator_scenarios == 0 else f"{definite / denominator_scenarios:.4f}"
        completeness.append(
            [
                "scenario",
                field,
                str(denominator_scenarios),
                str(definite),
                str(missing),
                proportion,
            ]
        )
    _write_pair(
        layout,
        "table_reporting_completeness",
        "Reporting completeness",
        (
            "Each proportion is the share of included deployments or scenarios with a definite code "
            "or a non-empty free-text value other than NOT_REPORTED_OR_UNCLEAR. "
            "For tri-state fields, both YES and NO count as definite reports. "
            "These proportions are not added into a quality score."
        ),
        ["unit", "field", "denominator", "definite_reports", "not_definite", "proportion_definite"],
        completeness,
    )

    figure_dir = layout.path("outputs", "figures")
    figure_dir.mkdir(parents=True, exist_ok=True)
    (figure_dir / "settings.svg").write_text(_bar_svg(setting_counts, "Included deployments by primary setting"), encoding="utf-8")
    (figure_dir / "provenance.svg").write_text(
        _bar_svg(provenance_counts, "Included scenarios by provenance code"),
        encoding="utf-8",
    )
    return {"table_1": table_1, "completeness": completeness}


def _bar_svg(counts: Counter[str], title: str) -> str:
    items = [(key, counts[key]) for key in sorted(counts) if counts[key] > 0]
    if not items:
        items = [("No included rows", 0)]
    width = 760
    row_height = 28
    height = 70 + len(items) * row_height
    maximum = max(value for _key, value in items) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="20" y="28" font-family="sans-serif" font-size="16">{title}</text>',
    ]
    for index, (label, value) in enumerate(items):
        top = 48 + index * row_height
        bar = 0 if maximum == 0 else int(360 * value / maximum)
        safe_label = (
            label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        parts.append(
            f'<text x="20" y="{top + 16}" font-family="sans-serif" font-size="12">{safe_label}</text>'
        )
        parts.append(
            f'<rect x="280" y="{top}" width="{bar}" height="18" fill="#335C81"/>'
        )
        parts.append(
            f'<text x="{300 + bar}" y="{top + 14}" font-family="sans-serif" font-size="12">{value}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_synthesis(layout: ReviewLayout) -> None:
    build_tables(layout)
    index = layout.path("outputs", "tables", "README.md")
    index.write_text(
        "\n".join(
            [
                "# Descriptive synthesis tables",
                "",
                "These files are generated from included extraction rows.",
                "Regenerate them with `python -m inthewild_review synthesize`.",
                "Do not treat an empty table as a finding that no such studies exist.",
                "An empty table means no included rows have been entered.",
                "",
                "No table in this directory is a quality score.",
                "",
            ]
        ),
        encoding="utf-8",
    )
