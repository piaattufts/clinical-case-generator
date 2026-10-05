# Evaluating Social Robots in the Wild

A scoping review of naturalistic evaluation settings and the scenarios that structure them.

This repository is the infrastructure for conducting that review. It does not contain completed screening decisions, extracted study data, or PRISMA results. Those files stay empty until a person imports real database exports and records human decisions.

The authoritative methods text is `InTheWild_Review_Methods.docx`. That file was not in this workspace when the infrastructure was built. Place it at `protocol/InTheWild_Review_Methods.docx`. Until that happens, `docs/unresolved_protocol_decisions.md` is the list of choices this code deliberately does not make.

This branch also still contains the CliniProof clinical-case project. Its previous root README is `CLINIPROOF.md`. The review commands do not modify that project.

## 1. What this review is

The review asks how social robots are evaluated outside the laboratory, and how the scenarios in those evaluations are built and what they represent. The synthesis is descriptive. There is no meta-analysis and no overall study-quality score.

## 2. Research questions

RQ1. In which settings, over what durations, and with which people are social robots evaluated outside the laboratory?

RQ2. How are the scenarios used in these evaluations sourced and constructed, including researcher-authored, persona-based, narrative-framed, co-designed, observation-derived, fiction-derived, implicit everyday activity, and hybrid forms?

RQ3. What social, relational, normative, and temporal information do the scenarios represent, including multi-party interaction, competing interests, embodiment and touch, relationship development, affect, norms, and temporal dependencies?

RQ4. What aspects of robot or interaction performance do these evaluations allow researchers to assess, and with which measures?

RQ5. How do studies report and manage trade-offs among setting fidelity, robot autonomy, participant safety, and experimental control?

## 3. What counts as naturalistic or in the wild

An in-the-wild or naturalistic evaluation includes interaction with a physically embodied social robot in:

- the intended use setting, such as a private home, care home, hospital, school, museum, shop, workplace, or public space
- or a purpose-built high-fidelity environment used as the target setting, such as a furnished test house
- or repeated interaction in a laboratory when there is more than one session with the same participants and the work is explicitly framed as everyday use

Do not exclude a study only because the authors call the location a laboratory.

Physical fidelity and contextual fidelity are extraction variables. They are not eligibility cutoffs.

A scenario is a structured representation or enactment of a human–robot situation that contains enough contextual information to situate robot behaviour within a use or evaluation context. The paper does not need to use the word "scenario." Record both explicit scenarios and implicit scenarios based on everyday activities or deployments.

## 4. Workflow

```text
Protocol
   ↓
Database searches
   +
Citation chasing
   ↓
Raw bibliographic exports
   ↓
Normalization
   ↓
Duplicate candidate detection
   ↓
Title/abstract screening
   ↓
Full-text screening
   ↓
Included publications
   ↓
Study / deployment / scenario extraction
   ↓
Validation
   ↓
Descriptive synthesis
   ↓
PRISMA + tables + figures
```

Human work and automated processing are separate. See the next two sections.

## 5. What you do manually

- Paste the protocol file into `protocol/InTheWild_Review_Methods.docx`.
- Paste the final Scopus query, unchanged, into `search/scopus.txt`.
- Translate that query for the other databases and remove the human-verification line only after a person has checked the translation.
- Run the searches and save the exports under `data/raw/`. Do not edit those files later.
- Decide whether each duplicate candidate is the same record, two publications, a conference/journal pair, or uncertain.
- Screen titles and abstracts. The decisions are INCLUDE, MAYBE, and EXCLUDE.
- Complete the calibration sample as two independent reviewers, then record consensus in a third file.
- Screen full texts. Do not turn a missing detail into NO.
- Enter publication, study, deployment, and scenario rows.
- Record citation-chasing links.
- Log any later change to search, eligibility, coding, extraction, or analysis in `protocol/decision_log.csv`.

The scripts will not include or exclude a paper for you.

## 6. What the scripts automate

From the repository root:

```bash
PYTHONPATH=src python -m inthewild_review import-records --database scopus --input data/raw/scopus/export.csv
PYTHONPATH=src python -m inthewild_review normalize
PYTHONPATH=src python -m inthewild_review duplicates
PYTHONPATH=src python -m inthewild_review calibration --n 100 --seed 20261005
PYTHONPATH=src python -m inthewild_review agreement
PYTHONPATH=src python -m inthewild_review prepare-fulltext
PYTHONPATH=src python -m inthewild_review validate
PYTHONPATH=src python -m inthewild_review prisma
PYTHONPATH=src python -m inthewild_review synthesize
PYTHONPATH=src python -m inthewild_review search-validation-report
PYTHONPATH=src python -m inthewild_review citation-import --input path/to/citation_edges.csv
```

The same commands are available as `python scripts/import_records.py` and the other files in `scripts/`. After `pip install -e .`, the `PYTHONPATH=src` prefix is unnecessary.

No API key is required. Optional machine suggestions, if you later choose to store them, go to `data/screening/ai_suggestions.csv` and do not overwrite reviewer decisions.

## 7. How screening works

Title and abstract decisions are only `INCLUDE`, `MAYBE`, and `EXCLUDE`. MAYBE is stored as MAYBE.

Every EXCLUDE needs exactly one of these codes:

| Code | Meaning used by this repository |
| --- | --- |
| `N1_NOT_NATURALISTIC` | Not an intended-use setting, test house, or repeated everyday-use laboratory interaction |
| `N2_NOT_SOCIAL_ROBOT` | Not a physically embodied social or companion robot |
| `N3_NON_PRIMARY` | Not a primary evaluation report |
| `N4_TECHNICAL_NO_SITUATED_HRI` | Technical paper without a situated interaction to screen |
| `N5_NOT_A_RECORD` | Not a screenable publication record |

The wording of these codes is provisional until the protocol file is added. Details are in `protocol/screening_manual.md`.

Put the review's title/abstract decisions in `data/screening/title_abstract_screening.csv`. The calibration files are separate and are not counted as the review's PRISMA screening sheet.

INCLUDE and MAYBE are copied into the full-text queue by `prepare-fulltext`. EXCLUDE is not. This routing is recorded as a provisional operational rule in the decision log because the protocol file could not be checked.

## 8. How extraction works

One publication can report more than one study. One study can contain more than one deployment. One deployment can contain more than one scenario. Do not collapse those levels.

Enter rows in:

- `data/extraction/publications.csv`
- `data/extraction/studies.csv`
- `data/extraction/deployments.csv`
- `data/extraction/scenarios.csv`
- `data/extraction/extraction_notes.csv`

For a yes/no/missing field, the allowed values are `YES`, `NO`, and `NOT_REPORTED_OR_UNCLEAR`. Leaving the cell blank fails validation. Coding silence as `NO` is a different claim and will be counted separately. The codebook is `protocol/extraction_codebook.md`.

`data/processed/` is regenerated. Edit the extraction files, not the processed copies.

## 9. How PRISMA counts are generated

`python -m inthewild_review prisma` reads the normalized records, duplicate decisions, screening files, and extraction tables. It writes:

- `outputs/prisma/prisma_counts.json`
- `outputs/prisma/prisma_counts.csv`
- `outputs/prisma/prisma_summary.md`
- `outputs/prisma/prisma_flow.svg`

A record is removed as a duplicate only after a person has marked `SAME_RECORD` and named `retained_record_id`. Candidate pairs stay in the set until then.

Publication, study, deployment, and scenario counts are reported as different units.

A zero means the corresponding file has no rows yet. It does not mean a database search found nothing.

## 10. How descriptive synthesis is generated

`python -m inthewild_review synthesize` writes the protocol tables under `outputs/tables/` and two bar charts under `outputs/figures/`. The tables cover settings, duration, robot and autonomy, scenario provenance, scenario content, measures, trade-offs, material availability, the Arnold and Scheutz dimensions, reporting completeness, and the requested cross-tabulations.

Completeness proportions are not added into a quality score. `NO` is not merged with `NOT_REPORTED_OR_UNCLEAR`.

## 11. How protocol deviations are documented

After the protocol date, a change to the search, eligibility, coding, extraction, or analysis is written to `protocol/decision_log.csv` before it is applied. The columns are `decision_id`, `date`, `stage`, `issue`, `original_protocol`, `decision`, `rationale`, `made_by`, `prospective_or_retrospective`, `affected_files`, and `notes`.

Do not resolve a bracketed protocol placeholder inside the code. Add it to `docs/unresolved_protocol_decisions.md` and leave the behavior unchanged until you decide.

## Where to put database exports

| Database | Directory |
| --- | --- |
| Scopus | `data/raw/scopus/` |
| Web of Science | `data/raw/web_of_science/` |
| IEEE Xplore | `data/raw/ieee/` |
| ACM Digital Library | `data/raw/acm/` |
| PubMed | `data/raw/pubmed/` |
| PsycINFO | `data/raw/psycinfo/` |
| Google Scholar notes or exports | `data/raw/scholar/` |
| Citation-chasing source files | `data/raw/citation_chasing/` |

Supported inputs include Scopus CSV, Web of Science CSV or tab-separated text, IEEE CSV, ACM CSV or BibTeX, PubMed CSV or NBIB, RIS, BibTeX, and a generic CSV with recognizable column names.

## How two reviewers run the calibration sample

```bash
PYTHONPATH=src python -m inthewild_review calibration --n 100 --seed 20261005
```

The default size is 100 and the default seed is `20261005`. Both are arguments. The draw is stratified by year and source. It is not the first 100 rows. The seed and the sampling method are stored in `data/screening/calibration_sampling.json` and on each sample row.

Reviewer 1 edits only `data/screening/calibration_reviewer_1.csv`.
Reviewer 2 edits only `data/screening/calibration_reviewer_2.csv`.
Consensus, after both files exist, goes in `data/screening/calibration_consensus.csv`.

Running calibration again appends new sample identifiers. It does not replace a row that already has a decision. `agreement` reads the two reviewer files and writes `outputs/reports/calibration_report.md`. It calculates three-category agreement and kappa, collapsed INCLUDE-or-MAYBE versus EXCLUDE agreement and kappa, a confusion matrix, and a disagreement table.

## How citation chasing is imported

Put one row per link in a CSV with `seed_record_id`, `citing_or_cited_record`, `direction` (`BACKWARD` or `FORWARD`), `iteration`, `parent_record`, `discovery_source`, and `date_retrieved`. Optional bibliographic columns such as `title` and `doi` are copied onto a new normalized record when that work is not already in the set.

```bash
PYTHONPATH=src python -m inthewild_review citation-import --input data/raw/citation_chasing/edges.csv
PYTHONPATH=src python -m inthewild_review duplicates
```

Those records then use the same screening sheets as database records. Nothing in the chain is eligible until a person includes it. No stopping rule is coded, because that rule is unresolved.

## Tests

The tests use synthetic bibliographic rows labeled `SYNTHETIC TEST FIXTURE`. They do not add studies to the review data.

```bash
PYTHONPATH=src python -m pytest tests/test_normalization.py tests/test_deduplication.py tests/test_screening.py tests/test_agreement.py tests/test_extraction.py tests/test_prisma.py
```

Further detail is in `docs/workflow.md`, `docs/reproducibility.md`, `docs/data_dictionary.md`, and `docs/methods_traceability.md`.
