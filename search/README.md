# Search strategy

The primary search has two concept blocks.

1. Social or companion robots.
2. Naturalistic, in-the-wild, or long-term settings.

There is not a third generic block for "evaluation" or "study." Adding one would change the search the protocol specified.

Scenario language is a sensitivity analysis. It lives in `scenario_sensitivity_searches/` and is logged as its own search, not as part of the primary query file.

## Why some familiar terms are absent

Bare `home*` was avoided because it matches unrelated words such as homework, homeostasis, and homepage. Home settings still need to be sought with phrases that point at a dwelling or a household, once the protocol query is pasted.

Paro, robotic seal, Pleo, and AIBO are low-ambiguity platform names and stay available to the search.

NAO and Pepper were considered higher-noise platform names. They are not added on top of the protocol query.

## Files

| File | Role |
| --- | --- |
| `scopus.txt` | Verbatim final Scopus query. Not yet pasted. |
| `web_of_science.txt` | Translation. Not validated. |
| `ieee_xplore.txt` | Translation. Not validated. |
| `acm_dl.txt` | Translation. Not validated. |
| `pubmed.txt` | Translation. Not validated. |
| `psycinfo.txt` | Translation. Not validated. |
| `google_scholar.md` | How to record a Scholar pass. The number screened is unresolved. |
| `search_log.csv` | One row per search actually run. |

Every translation file contains `# TODO: HUMAN VERIFICATION REQUIRED`. Leave that line in place until a person has compared the translation with the pasted Scopus query. Do not write in the log that a translation was validated before that check.

## Search log

Columns: `search_id`, `database`, `platform`, `search_date`, `query_file`, `query_version`, `filters`, `result_count`, `export_filename`, `notes`, `performed_by`.

The log is empty of searches. Do not enter a result count from memory. Enter it from the database's own hit display, and point `export_filename` at the file saved under `data/raw/`.

## Known-item check

`data/search_validation.csv` lists the known items named in the brief. `retrieved` stays blank until an export is compared with that list. `python -m inthewild_review search-validation-report` writes `outputs/reports/search_validation_report.md`. A blank cell is "not yet assessed." It is not a miss. A miss is a row where `retrieved` is `NO`.
