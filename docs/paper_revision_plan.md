# Manuscript revision plan

Source manuscript: the September 16 draft supplied for this revision (`CliniProof_sept16_highlighted(1).docx` / uploaded `CliniProof_sept16_7488.docx`). That file is not overwritten.

Working repository state: `main` after the matched Generation 2 cohort and the de-identified reviewer comparison. Method statements below are labeled IMPLEMENTED, PLANNED, PROPOSED, or VALIDATED. VALIDATED is not used for Generation 2 or for the revised Generation 1 charts. Clinician review of the original charts occurred; acceptance of the revised charts has not.

## Title alternatives

The title is not locked. The September title is:

> CliniProof: A Framework for Generating and Validating Synthetic Cases for Medication Reconciliation Assessment

Alternatives, shown before any title is treated as final:

1. CliniProof: A Framework for Generating and Validating Synthetic Cases for Discharge Medication Reasoning
2. CliniProof: Clinician-Informed Generation and Validation of Synthetic Discharge Medication Reasoning Cases
3. Keep the September title and change only the subtitle or abstract.

The Markdown draft and the DOCX use alternative 1 as a working title so the file has a heading. It can be replaced without changing the method text.

## Section plan

| Section | Current problem | Required conceptual change | Evidence/source in repository | Proposed new content | Implementation status |
| --- | --- | --- | --- | --- | --- |
| Title and abstract | Title and opening frame a planted-error assessment library. There is no abstract for the current method. | Center provenance, clean cases, hidden references, and two generation strategies. Report only completed implementation and review facts. | README.md current status; docs/methodology.md; docs/methodology_synthea_g2.md; data/case_sets/synthea_g2/manifest.json | Structured abstract. G2 clinician outcomes stated as not yet collected. | Drafted |
| Introduction | Ends by proposing one-shot generation of cases with known planted errors and a validation hunt for those errors. | Keep safety, training, and case-based learning. Replace the closing problem with evidence-sufficient discharge reasoning and four aims. Do not claim superiority. | README.md aims-equivalent status; docs/methodology.md | Aims 1–4 as specified. Status: framework IMPLEMENTED; comparison PROPOSED. | Drafted |
| Background | Treats LLM vignettes plus Delphi as the technical path. | Keep medication-safety, training-gap, simulation, and expert-review subsections. Add longitudinal synthetic records. Retain LLM papers as comparison. | Existing bibliography; Walonoski et al., JAMIA 2018 (verified); docs/methodology_synthea_g2.md | New subsection and a three-way distinction: vignette, synthetic patient, assessment case. | Drafted |
| Expert review | Calls the dominant validation method a classical Delphi and the manuscript later implies two primary raters plus a naive third rater for all cases. | Call the completed review structured iterative clinician review. State incomplete coverage and no consensus threshold. | docs/clinical_feedback/reviewer_comparison.md; docs/methodology.md | Coverage table. Silence is not agreement. | Drafted |
| Conceptual framework | Layer 2 is a planted exclusive error. The resident sees discharge medications. | Two layers: resident-visible chart without a completed discharge list; hidden reference derived afterward. | docs/revision/revision_framework.md; resident JSON in REVISED/ and synthea_g2/cases/resident/ | Tables 1 and 2 replaced. | Drafted |
| Error taxonomy | Defines the base case. | Move to a future perturbation layer after base-case acceptance. | docs/methodology.md historical 20-and-4 freeze; error taxonomy code remains in the repository as historical provenance | Supplementary-style section in the draft, not the base method. | Drafted |
| Validity requirements | Six error-centered gates. | Use the ten frozen Generation 1 revision domains and the Generation 2 audit columns actually stored. | docs/revision/revision_framework.md; reports/validation_report.csv | Table of implemented domain names. | Drafted |
| Generation 1 construction | One-shot schema-completion prompt is the method. | Six resident examples abstracted to six families, four profiles each, terminology-backed structured generation, OpenAI not used for the freeze. | docs/methodology.md; data/seed_cases/blueprints/archetypes.json; data/case_sets/seed_guided/batch_plan.json | IMPLEMENTED construction. Historical planted-error freeze labeled historical. | Drafted |
| Review coverage | Two primary raters rate every case; a third naive rater rates plausibility. | Reviewer 1: 6/24. Reviewer 2: 4/24. Overlap: VAL-801, VAL-805, VAL-809, VAL-813. No names in the method narrative. | reviewer_comparison.csv | Exact coverage. | Drafted |
| Four-case revision | Not described. | Clinician-informed candidate revisions, pending re-review. Not validated. | docs/revision/overlap_4_revision_log.md | Case-level concern summary. | Drafted |
| Frozen framework and remaining 20 | Not described. | Ten domains frozen from the four overlap cases, then applied by investigators. VAL-802 and VAL-803 also use Reviewer 1 comments. The other 18 do not. | revision_framework.md; revision_framework_application.csv; remaining_20_revision_log.md | Explicit non-validation statement. | Drafted |
| Generation 2 | Absent. | Synthea longitudinal context plus CliniProof inpatient episode, sufficiency gates, hidden reference after the chart, 24 matched clean cases. | methodology_synthea_g2.md; manifest.json; g2_episode and g2_audit code | Full method section. | Drafted |
| Synthea role | Would be over-claimed if Synthea were said to write the hospitalization. | Synthea: age, sex, conditions, outpatient medicines, prior encounters when present. CliniProof: acute episode. Provenance labels. | config/synthea.yml; methodology_synthea_g2.md | Bounded description. Endocarditis and most heart-failure episodes are episode-generated. | Drafted |
| Matched design | Absent. | VAL-801→G2-001 through VAL-824→G2-024. Match reasoning task, not the patient or the answer. | matched_pairs.csv; matched_pair_audit.md | 24/24 core pass; 0 copied facts; 0 copied references. | Drafted |
| Quality by design | Absent. | Round 1 deficiencies become prospective gates. Gates are not themselves clinician-validated. | methodology_synthea_g2.md “Round 1 design requirements”; revision_framework.md triggers | Table 4. | Drafted |
| Trajectories and medication state | Not in the old prompt method. | Longitudinal labs/vitals and temporal medication states. | g2 methodology; medication_regimens.json | IMPLEMENTED for Generation 2. | Drafted |
| Hidden reference and alternatives | Answer key is the planted error and one correct action, written before the vignette. | Reference is derived after the resident chart. Alternatives are allowed. | methodology_synthea_g2.md; evaluator JSON `reference_discharge_plan` | IMPLEMENTED. | Drafted |
| Candidate selection | First schema-complete JSON is accepted. | 96 matched attempts, 24 selected. Automated pass is not clinical validation. | manifest.json `candidate_attempts`: 96; validation_report.csv 24/24 true on every audit column | Counts from files only. | Drafted |
| Validation instrument | Five error-fidelity gates, two primary raters, and a third naive rater. | Current C1–C5 clean-case wording from the template. | docs/validation/CODEBOOK.md; CliniProof_Clinical_Validation_Template.docx | Table 7 quotes the clean-case questions. | Drafted |
| Validation order | Not separated from seeing the answer key. | Written casebook protocol: complete C1 before the validation reference. Not a software lock. | validation casebook instructions | IMPLEMENTED as instructions; not a technical blind. | Drafted |
| G1/G2 comparison | Attrition of planted-error generation. | Paired question stated as PROPOSED. No statistics. | README.md; matched_pair_audit.md | Outcomes listed as potential, not measured. | Drafted |
| Blinding | Not applicable to the old design. | Neutral-identifier casebook exists. The comparison has not been run. | blinding_map.json; CliniProof_Paired_Blinded_Casebook.docx; unblinding key marked investigator-only | IMPLEMENTED artifact; PROPOSED study. | Drafted |
| Old error-injection analysis | Primary result. | Future layer after a locked clean reference. | methodology.md historical freeze note | Sequence diagram in the draft. | Drafted |
| Workflow | Five stages around planted-error generation and a naive rater. | Construction, automated checks, clinician validation, resident administration, scoring. Last two are not the current implemented study. | word_export.py dashboard wording: planned, not implemented | Stages 1–3 IMPLEMENTED for case production and review materials. Stages 4–5 PLANNED. | Drafted |
| Dashboard | Resident compares a supplied discharge list with home and inpatient lists. | Resident builds the discharge plan. No correct list before submission. | word_export.py: “A resident review dashboard is planned. It is not implemented.” | PLANNED interface. | Drafted |
| Scoring | Detect and classify the planted discrepancy; argumentation graph. | Agreement with the hidden reference. Categories are a sketch, not an implemented scorer. | No resident-administration scorer in the current study path | PLANNED. Argumentation-graph scoring not claimed as built. | Drafted |
| Results | Proposed attrition, not observed results. | Only completed construction and review-coverage facts. | manifest.json; reviewer_comparison.csv; revision logs | No G2 clinician outcomes. | Drafted |
| Discussion and conclusion | Contribution is a constrained LLM prompt plus an error rubric. | Contribution is separation of synthetic patient, evidence-sufficient case, and validation. Next question is empirical. | README limitations | No superiority claim. | Drafted |
| Limitations | “Specified but not evaluated,” still about the prompt pipeline. | Small panel, incomplete coverage, investigator framework application, Synthea limits, pending G2 review, no resident data. | README limitations; methodology.md | Replaced. | Drafted |
| Figures | Figure 3 is planted-error attrition. Figure 1 is the frozen prompt. | Four figures for the current architecture. | This plan | Specified as text figures, not implied empirical plots. | Drafted |
| References | Adequate for background; overweight LLM vignette generation; no Synthea source. | Keep background citations. Move LLM papers to the comparison subsection. Add Walonoski et al. 2018. Do not invent the rest. | Existing bibliography; JAMIA 2018;25(3):230–238, doi:10.1093/jamia/ocx079 | Citation-status list below. | Drafted |

## Citation status

### KEEP

Background citations that still support unchanged safety, training, simulation, or expert-review claims: Barnsteiner 2008; Joint Commission 2006; Kwan et al. 2013; Coleman et al. 2005; Alqenae et al. 2020; Bishop et al. 2015; Killin et al. 2021; Boockvar et al. 2011; Ramjaun et al. 2015; McShane and Stark 2018; Mueller et al. 2012; Lindquist et al. 2008; Barrows and Tamblyn 1980; Norman and Schmidt 1992; Komperda and Lempicki 2019; Thomas et al. 2015; Gonzales et al. 2023; Desai et al. 2024; Triola and Burk-Rafel 2023; Nasa et al. 2021; Hernandez et al. 2020; Arthur et al. 2012; Cumyn and Harris 2012.

Taxonomy citations, kept only for the future perturbation layer: NCC MERP; Gleason et al. 2012 (MATCH); Bajorek and McElroy 2020; Forster et al. 2003.

### MOVE

Keep in the manuscript, but only inside the subsection that contrasts LLM vignettes with the current pipeline: Rao et al. 2025; Emekli et al. 2026; Cayres Ribeiro et al. 2026; Chung et al. 2023; Bakkum et al. 2024; Ruggiano et al. 2026; Takahashi et al. 2024; Yanagita et al. 2024; Abidi et al. 2026; Gorenshtein et al. 2025; Zhang et al. 2025.

These citations were already in the September draft. This revision does not re-verify every one of them. They are retained as the draft’s existing literature, not as new evidence that the current generator is an LLM.

### ADD

Walonoski J, Kramer M, Nichols J, Quina A, Moesel C, Hall D, Duffett C, Dube K, Gallagher T, McLachlan S, et al. Synthea: an approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record. J Am Med Inform Assoc. 2018;25(3):230–238. doi:10.1093/jamia/ocx079. Verified against the journal record for this revision.

### REMOVE / OPTIONAL

None of the September citations are deleted. The one-shot prompt, response schema, and planted-error attrition figure are removed from the base-case method. They can sit in a historical supplement if a later version needs them. No new unverified papers were inserted to fill that gap.

### CITATION NEEDED, not invented

A methods paper on content validation other than the Delphi citations already in the draft; a citation for matched-pair comparative designs in education; any paper claiming Synthea generates complete inpatient diagnostic hospitalizations. Those claims are not made.

## Claim control

| Concept in the September draft | Disposition |
| --- | --- |
| Planted error as the base case | Historical freeze and future perturbation layer only |
| One-shot LLM prompt as the generator | Not the current method. OpenAI was not used for the frozen Generation 1 set or for Generation 2 |
| Resident-visible discharge medication list | Removed from the base task |
| Hidden answer key as the planted discrepancy | Replaced by a hidden reference discharge plan |
| Error fidelity, detectability of a planted error, two primary raters, third naive rater | Obsolete for the completed review |
| Classical Delphi | Removed as a description of this review |
| Validated library | Not claimed |
| Dashboard and argumentation-graph scoring | PLANNED, not implemented |
