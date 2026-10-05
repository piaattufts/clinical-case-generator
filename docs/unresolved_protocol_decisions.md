# Unresolved protocol decisions

This file lists choices that must stay open. It is not a set of decisions.

## Source of this list

`InTheWild_Review_Methods.docx` was named as the authoritative protocol. It was not in the repository, not on `origin/main`, and not elsewhere on the machine when this infrastructure was built. A later message named the same filename and did not include the file.

Because the file could not be read:

- bracketed placeholders inside the protocol were not inventoried
- none of those placeholders were resolved
- the final Scopus query was not reconstructed
- database translations were not marked as validated
- no result count, DOI, screening decision, kappa, or PRISMA number was filled in as a finding

The items below are of two kinds.

1. Gaps created by the missing protocol file.
2. Examples named in the implementation brief as the sort of choice that must not be resolved silently. They are listed as open items. They are not a claim that the protocol document uses those exact brackets.

When the protocol file is added, replace section A with a line-by-line inventory of the bracketed text. Do not delete an item until the protocol text actually settles it.

## A. Missing protocol text

| ID | Open item | Why it is unresolved | What the code does meanwhile |
| --- | --- | --- | --- |
| U1 | Verbatim protocol text | The docx is absent | Summaries in `protocol/` are taken from the implementation brief and are marked as such |
| U2 | Final Scopus Boolean query | The brief says to copy it exactly and not rewrite it | `search/scopus.txt` contains no query |
| U3 | Translated queries for Web of Science, IEEE Xplore, ACM Digital Library, PubMed, and PsycINFO | Translation cannot be checked against a missing source query | Each file says human verification is required |
| U4 | Verbatim exclusion-code prose | Codes were named in the brief; the protocol sentences were not | Code descriptions are labeled provisional in the screening manual |
| U5 | Full known-item list and the database expected to retrieve each item | The brief names ten citation labels and says "including" | Only those ten labels are in `data/search_validation.csv`, with `retrieved` blank |
| U6 | Controlled vocabularies that the protocol may define for autonomy, participant role, researcher presence, and fidelity levels | The brief names the variables and forbids an aggregate fidelity score | Those fields are free text, plus a separate reported / not-reported code. No ordinal scale was invented |
| U7 | Whether full-text screening uses MAYBE | The brief requires MAYBE at title/abstract and does not say to drop it later | Full-text decisions also allow MAYBE. Confirm against the protocol |

## B. Choices the brief said not to resolve silently

| ID | Open item | Current behavior |
| --- | --- | --- |
| U8 | Whether conceptual scenario contributions are included separately or excluded | No rule was added. A record is included only when a human enters that decision |
| U9 | Final database search dates | `search/search_log.csv` has headers and no search rows |
| U10 | Final result counts | PRISMA output is computed from files. With no imports, the counts are zero because the files are empty |
| U11 | Number of Google Scholar results to screen | `search/google_scholar.md` does not set a number |
| U12 | Exact stopping rule for citation chasing | The importer accepts every supplied iteration. It does not stop the chain |
| U13 | Whether AI-assisted screening is used | The standard commands do not call a model. A separate suggestion file exists and is unused unless someone writes to it |
| U14 | Unresolved translated search-string details | See U3 |

## C. Operational rules recorded because the workflow needs them

These are not protocol amendments. They are logged in `protocol/decision_log.csv` as provisional.

- INCLUDE and MAYBE both enter the full-text queue. EXCLUDE does not.
- A duplicate is dropped from the PRISMA "removed" count only when a person has set `human_decision` to `SAME_RECORD` and filled `retained_record_id`.
- DOI comparison also strips `https://dx.doi.org/` and `http://dx.doi.org/` in addition to the prefixes named in the brief.

If the protocol contradicts any of these, change the code and add a prospective decision-log row. Do not edit historical screening files to match the new rule without saying so in that row.

## D. Observed review data

No observed search results, screening decisions, or extractions are stored yet. Do not copy counts from this file into a paper.
