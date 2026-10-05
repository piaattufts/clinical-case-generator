# Data dictionary

Empty cells in yes/no fields are invalid once a row exists. Use `NOT_REPORTED_OR_UNCLEAR`.

`origin` on a normalized record is `database` or `citation_chasing`. It is how PRISMA splits identification. It is not an eligibility label.

## Normalized records

`data/interim/normalized_records.csv`

| Field | Meaning |
| --- | --- |
| `record_id` | Stable id. Prefix `rec_` plus a hash. |
| `source_database` | Database or `citation_chasing`. |
| `source_record_id` | The source's own id, when the export has one. |
| `title` | Title as imported. |
| `normalized_title` | Comparison form. Not a replacement for `title`. |
| `abstract` | Abstract as imported. |
| `authors` | Author string as imported. |
| `year` | Four-digit year when one is present. |
| `journal_or_venue` | Journal, proceedings, or other venue. |
| `volume`, `issue`, `pages` | As imported. |
| `doi_raw` | DOI as imported. |
| `doi_normalized` | Lowercased DOI without a resolver prefix. |
| `url` | Link from the export. |
| `document_type` | As imported. |
| `keywords` | Author keywords. |
| `indexed_keywords` | Index or thesaurus terms. |
| `language` | As imported. |
| `source_file` | Export path. |
| `import_timestamp` | UTC timestamp of the import. |
| `origin` | `database` or `citation_chasing`. |
| `discovery_source` | Where the row entered. |

## Duplicate candidates

`data/interim/duplicate_candidates.csv`

| Field | Meaning |
| --- | --- |
| `duplicate_group_id` | Stable id for the DOI, title, or fuzzy pair. |
| `record_id_1`, `record_id_2` | The pair, sorted by id. |
| `match_type` | `EXACT_DOI`, `EXACT_TITLE`, `EXACT_DOI_AND_TITLE`, or `FUZZY_TITLE`. |
| `doi_match`, `exact_title_match` | `YES` or `NO`. |
| `fuzzy_title_score` | SequenceMatcher ratio, four decimals, when titles exist. |
| `recommended_review` | `YES` for every candidate the detector emits. |
| `human_decision` | Blank, `SAME_RECORD`, `DISTINCT_PUBLICATIONS`, `CONFERENCE_JOURNAL_PAIR`, or `UNCERTAIN`. |
| `human_reason`, `decision_by`, `decision_date` | The human review. |
| `retained_record_id` | Which record stays when the decision is `SAME_RECORD`. Blank means nothing is dropped. |

## Screening

Title/abstract and calibration files share `record_id`, `reviewer`, `decision`, `exclusion_code`, `notes`, `screened_at`, `criteria_version`.

`decision` is `INCLUDE`, `MAYBE`, or `EXCLUDE`.

Full text adds `full_text_available` and the eight criterion fields (`YES`, `NO`, `UNCLEAR`), plus `exclusion_reason`.

## Citation graph

`data/interim/citation_graph/edges.csv`: `edge_id`, `seed_record_id`, `citing_or_cited_record`, `direction` (`BACKWARD` or `FORWARD`), `iteration`, `parent_record`, `discovery_source`, `date_retrieved`, `notes`.

`BACKWARD` means the cited work was found from the parent's reference list. `FORWARD` means the record cites the parent.

`nodes.csv` records whether each id is a seed or was reached by a chase, and whether a bibliographic row exists. `in_bibliographic_set` is not eligibility.

## Extraction

Column lists and controlled values are in `protocol/extraction_codebook.md`. The CSV headers in `data/extraction/` match `src/inthewild_review/schemas.py`.

## Search validation

`data/search_validation.csv`: `validation_id`, `citation_label`, `database`, `expected_retrieval`, `retrieved`, `retrieval_date`, `failure_reason`, `search_version`, `notes`.

`expected_retrieval` YES means the item is a known item the search should find. `retrieved` blank means nobody has checked an export yet.

## AI suggestions

`data/screening/ai_suggestions.csv` is unused by the standard commands. Columns include the suggestion, the model provider, name, and version, a prompt id, a SHA-256 of the prompt text, and blank human-verification fields. `human_accepts` is not copied into a screening decision.

## Search log

`search/search_log.csv`: `search_id`, `database`, `platform`, `search_date`, `query_file`, `query_version`, `filters`, `result_count`, `export_filename`, `notes`, `performed_by`.
