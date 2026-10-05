# Extraction codebook

Status: field definitions for this repository. Where the protocol file was not available, free-text fields are used instead of an invented scale. Confirm labels against `InTheWild_Review_Methods.docx` before coding a batch.

## Levels

```text
publication
   ↓ may report
one or more studies
   ↓ may contain
one or more deployments
   ↓ may contain
one or more scenarios
```

Identifiers: `publication_id`, `study_id`, `deployment_id`, `scenario_id`.

A paper that reports two deployments gets two deployment rows. A deployment with two scenarios gets two scenario rows. Do not copy a scenario onto a second row just to make the counts match.

`publication.record_id` points at the normalized bibliographic record that survived screening. A publication row is valid only when that record has a full-text INCLUDE decision.

## Missing information

Yes/no fields use three values:

| Value | Meaning |
| --- | --- |
| `YES` | The paper supports the claim |
| `NO` | The paper states the claim is not the case |
| `NOT_REPORTED_OR_UNCLEAR` | The paper is silent or too ambiguous to choose YES or NO |

`NOT_REPORTED_OR_UNCLEAR` is not `NO`. Validation rejects a blank cell on these fields. It does not rewrite one value into the other.

Scenario explicitness uses a different trio: `EXPLICIT`, `IMPLICIT`, `UNCLEAR`. `UNCLEAR` there means the coder cannot tell whether the scenario is explicit or implicit.

Full-text criterion fields use `YES`, `NO`, and `UNCLEAR`. Those columns are on the screening sheet, not on the scenario sheet.

## Publication

`publications.csv`: `publication_id`, `record_id`, `doi`, `title`, `authors`, `year`, `venue`, `publication_type`, `source_database`, `notes`.

Copy bibliographic values from the normalized record. Do not invent a DOI.

## Study

`studies.csv`: `study_id`, `publication_id`, `study_label`, `study_design`, `country`, `population_description`, `participant_count`, `recruitment`, `notes`.

`study_design`, `country`, and `recruitment` are free text taken from the paper. This codebook does not add a design taxonomy.

## Deployment

One row is one evaluation deployment.

### Setting

`setting_type` is the primary setting. Allowed values:

`PRIVATE_HOME`, `CARE_HOME`, `HOSPITAL`, `SCHOOL`, `MUSEUM`, `SHOP`, `WORKPLACE`, `PUBLIC_SPACE`, `TEST_HOUSE`, `LABORATORY_REPEATED_EVERYDAY`, `OTHER`, `NOT_REPORTED_OR_UNCLEAR`.

`LABORATORY_REPEATED_EVERYDAY` is the repeated everyday-use laboratory case from the eligibility definition. It is not a claim of high physical fidelity.

These labels are not assumed to be mutually exclusive. Put the main setting in `setting_type`. Put any further settings in `additional_setting_types`, separated by `|`. Describe the place in `setting_detail`.

### Fidelity

Physical fidelity: how closely the physical environment resembles intended use.

Contextual fidelity: how closely the participant's role, goals, and activities resemble actual use.

Each has a reported flag (`physical_fidelity_reported`, `contextual_fidelity_reported`) using YES / NO / NOT_REPORTED_OR_UNCLEAR, and a free-text description (`physical_fidelity`, `contextual_fidelity`).

There is no numeric fidelity score and no combined score. Do not add one.

### People, time, robot

Free text unless a controlled list is named here:

- `participant_role`
- `researcher_presence`
- `number_of_sessions`
- `total_period` and `total_period_unit`
- `session_length`
- `population`
- `participant_count`
- `recruitment`
- `interaction_configuration`
- `robot_platform`
- `embodiment`
- `autonomy_level` with `autonomy_reported`
- `failure_handling`

`continuous_vs_episodic`: `CONTINUOUS`, `EPISODIC`, `MIXED`, `NOT_REPORTED_OR_UNCLEAR`.

`single_or_multiple_embodiments`: `SINGLE`, `MULTIPLE`, `NOT_REPORTED_OR_UNCLEAR`.

`novelty_or_habituation_reported`: YES means the paper discusses novelty or habituation. It does not mean habituation occurred. Put what the paper says in `novelty_or_habituation_notes`.

No duration bins are applied. Table 3 lists the values as entered.

### Trade-offs, ethics, and availability

These are YES / NO / NOT_REPORTED_OR_UNCLEAR, with a notes column for the words the paper uses:

- `safety_measures`
- `technician_oversight`
- `consent_shared_group_spaces`
- `private_setting_data_collection`
- `reported_fidelity_control_limitations`
- `materials_available`
- `scripts_available`
- `code_available`
- `data_available`

YES means the paper reports the topic. NO means the paper says it was absent or unavailable. Silence is `NOT_REPORTED_OR_UNCLEAR`.

### Measures

`observational_data`, `log_data`, `interviews`, and `qualitative_methods` use the same three values: whether that class of evidence is reported.

`constructs_measured`, `instruments`, `interaction_level_outcomes`, and `relationship_level_outcomes` are free text. They are not scored.

Evaluation fields sit on the deployment. If two scenarios in one deployment were measured differently, either split the deployment or explain the split in `extraction_notes.csv`.

## Scenario

Identifiers: `scenario_id`, `deployment_id`, `study_id`, `publication_id`.

`scenario_explicitness`: `EXPLICIT`, `IMPLICIT`, or `UNCLEAR`.

### Provenance

`provenance_codes` may contain more than one code, separated by `|`. Do not force a single code when the paper describes a hybrid.

| Code | Use |
| --- | --- |
| `RESEARCHER_AUTHORED` | Written by the research team |
| `PERSONA_BASED` | Built from a persona |
| `NARRATIVE_FRAMING` | Framed as a narrative |
| `USAGE_SCENARIO_DERIVED` | Taken from a usage scenario |
| `CO_DESIGNED_PARTICIPATORY` | Co-designed or participatory |
| `FIELD_OBSERVATION` | Derived from observation |
| `PRIOR_PARADIGM` | Taken from a prior paradigm |
| `FICTION_DERIVED` | Derived from fiction |
| `IMPLICIT_EVERYDAY_ACTIVITY` | The everyday activity is the scenario |
| `HYBRID` | The paper combines forms. Keep the specific codes as well |
| `NOT_REPORTED_OR_UNCLEAR` | Provenance is not reported. Do not combine this with another code |

### Content

Each content field is YES, NO, or NOT_REPORTED_OR_UNCLEAR, plus a notes column:

- `task_represented`
- `events_represented`
- `goals_represented`
- `relationships_and_history`
- `affect_represented`
- `norms_represented`
- `competing_interests_or_obligations`
- `competing_interests_in_one_to_one`
- `touch_and_physical_contact`
- `temporal_dependencies`
- `multi_party_or_group_interaction`
- `group_decision_making`

`norms_examples` is free text. Privacy, confidentiality, consent, authority, and politeness are examples, not a closed list.

Arnold and Scheutz dimensions are coded separately from the broader RQ3 fields:

- embodiment and touch: `touch_and_physical_contact`
- competing interests inside one-to-one interaction: `competing_interests_in_one_to_one`
- multi-party or group decision-making: `group_decision_making`

`multi_party_or_group_interaction` can be YES when people interact as a group even if `group_decision_making` is NO or NOT_REPORTED_OR_UNCLEAR. Keep those apart.

## Notes sheet

`extraction_notes.csv` holds quotations, page numbers, and coder comments that do not fit a cell: `note_id`, `entity_level`, `entity_id`, `field_name`, `note`, `page_reference`, `extractor`, `noted_at`.

`entity_level` is `publication`, `study`, `deployment`, or `scenario`.

## What this codebook does not contain

An overall quality score. A combined fidelity score. A rule that conference and journal versions are the same publication. A rule that an empty cell means no.
