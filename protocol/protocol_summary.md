# Protocol summary

Status: this summary was compiled from the implementation brief. `InTheWild_Review_Methods.docx` was not available to transcribe. It is not a substitute for that file.

Title: Evaluating Social Robots in the Wild: A Scoping Review of Naturalistic Evaluation Settings and the Scenarios That Structure Them.

## Review questions

RQ1. In which settings, over what durations, and with which people are social robots evaluated outside the laboratory?

RQ2. How are the scenarios used in these evaluations sourced and constructed, including researcher-authored, persona-based, narrative-framed, co-designed, observation-derived, fiction-derived, implicit everyday activity, and hybrid forms?

RQ3. What social, relational, normative, and temporal information do the scenarios represent, including multi-party interaction, competing interests, embodiment and touch, relationship development, affect, norms, and temporal dependencies?

RQ4. What aspects of robot or interaction performance do these evaluations allow researchers to assess, and with which measures?

RQ5. How do studies report and manage trade-offs among setting fidelity, robot autonomy, participant safety, and experimental control?

## Definitions carried into the repository

An in-the-wild or naturalistic evaluation includes interaction with a physically embodied social robot in the intended use setting, in a purpose-built high-fidelity environment used as the target setting, or across repeated sessions with the same participants when the work is explicitly framed as everyday use. Calling a place a laboratory is not, by itself, a reason to exclude.

Physical fidelity and contextual fidelity are recorded at extraction. They do not decide eligibility.

A scenario is a structured representation or enactment of a human–robot situation with enough contextual information to situate robot behaviour. The word "scenario" is not required. Explicit and implicit scenarios are both in scope.

## Bibliographic sources named for the workflow

Scopus, Web of Science, IEEE Xplore, ACM Digital Library, PubMed, PsycINFO, and Google Scholar. Citation chasing runs backward and forward from seed studies and then enters the same pipeline as database records.

The primary search has two concept blocks: social or companion robots, and naturalistic, in-the-wild, or long-term settings. There is no generic evaluation block. A scenario block is a sensitivity analysis and stays in `search/scenario_sensitivity_searches/`.

## Screening and extraction levels

Title/abstract decisions are INCLUDE, MAYBE, and EXCLUDE. MAYBE is kept.

The data model is publication, then study, then deployment, then scenario. Those units are not forced to be one-to-one.

Missing information is `NOT_REPORTED_OR_UNCLEAR`. It is not coded `NO`.

Synthesis is descriptive. The protocol does not prespecify an aggregate quality or fidelity score, and this repository does not add one.

## Known-item labels named in the brief

Syrdal et al. (2014); Koay et al. (2009); Walters et al. (2011); Koay et al. (2007); Kidd & Breazeal (2008); de Graaf et al. (2014); Fernaeus et al. (2010); Kanda et al. (2004); Šabanović et al. (2006); Chang & Šabanović (2015).

They are listed in `data/search_validation.csv` with retrieval left blank. No DOI was added.

## What this summary does not contain

Search dates, hit counts, the final Boolean string, translated strings, a citation-chasing stop rule, and any bracket the protocol still has open. See `docs/unresolved_protocol_decisions.md`.
