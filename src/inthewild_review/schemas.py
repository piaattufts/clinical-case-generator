"""Controlled values and column orders.

Categorical lists are operational vocabularies for fields named in the
implementation brief. Where the protocol text was not available, lists that
go beyond the brief are marked in the extraction codebook and are not treated
as protocol amendments.
"""

from __future__ import annotations

SCREENING_DECISIONS = ("INCLUDE", "MAYBE", "EXCLUDE")

EXCLUSION_CODES = (
    "N1_NOT_NATURALISTIC",
    "N2_NOT_SOCIAL_ROBOT",
    "N3_NON_PRIMARY",
    "N4_TECHNICAL_NO_SITUATED_HRI",
    "N5_NOT_A_RECORD",
)

EXCLUSION_CODE_DESCRIPTIONS = {
    "N1_NOT_NATURALISTIC": (
        "The record does not meet the naturalistic or repeated everyday-use "
        "definition. Do not use this code only because the authors call the "
        "location a laboratory."
    ),
    "N2_NOT_SOCIAL_ROBOT": (
        "The record does not concern a physically embodied social or companion robot."
    ),
    "N3_NON_PRIMARY": (
        "The record is not a primary report of an evaluation. Reviews, commentaries, "
        "editorials, and protocol-only papers are examples."
    ),
    "N4_TECHNICAL_NO_SITUATED_HRI": (
        "The record is a technical paper without a situated human-robot interaction "
        "that can be screened as an evaluation."
    ),
    "N5_NOT_A_RECORD": (
        "The item is not a screenable publication record, for example an empty export "
        "row or a record with no usable bibliographic identity."
    ),
}

FULL_TEXT_CRITERION_FIELDS = (
    "physically_embodied_robot",
    "substantive_social_interaction",
    "human_participants",
    "naturalistic_or_repeated_longterm",
    "identifiable_interaction_situation",
    "setting_extractable",
    "duration_extractable",
    "interaction_structure_extractable",
)

FULL_TEXT_RESPONSES = ("YES", "NO", "UNCLEAR")

FULL_TEXT_EXCLUSION_REASONS = (
    "NOT_PHYSICALLY_EMBODIED_ROBOT",
    "NO_SUBSTANTIVE_SOCIAL_INTERACTION",
    "NO_HUMAN_PARTICIPANTS",
    "NOT_NATURALISTIC_OR_REPEATED_LONGTERM",
    "NO_IDENTIFIABLE_INTERACTION_SITUATION",
    "SETTING_NOT_EXTRACTABLE",
    "DURATION_NOT_EXTRACTABLE",
    "INTERACTION_STRUCTURE_NOT_EXTRACTABLE",
    "FULL_TEXT_UNAVAILABLE",
)

# Maps a full-text exclusion reason to the criterion that must be NO,
# except FULL_TEXT_UNAVAILABLE which is checked against full_text_available.
FULL_TEXT_REASON_TO_FIELD = {
    "NOT_PHYSICALLY_EMBODIED_ROBOT": "physically_embodied_robot",
    "NO_SUBSTANTIVE_SOCIAL_INTERACTION": "substantive_social_interaction",
    "NO_HUMAN_PARTICIPANTS": "human_participants",
    "NOT_NATURALISTIC_OR_REPEATED_LONGTERM": "naturalistic_or_repeated_longterm",
    "NO_IDENTIFIABLE_INTERACTION_SITUATION": "identifiable_interaction_situation",
    "SETTING_NOT_EXTRACTABLE": "setting_extractable",
    "DURATION_NOT_EXTRACTABLE": "duration_extractable",
    "INTERACTION_STRUCTURE_NOT_EXTRACTABLE": "interaction_structure_extractable",
    "FULL_TEXT_UNAVAILABLE": "full_text_available",
}

TRI_STATE = ("YES", "NO", "NOT_REPORTED_OR_UNCLEAR")

DUPLICATE_DECISIONS = (
    "SAME_RECORD",
    "DISTINCT_PUBLICATIONS",
    "CONFERENCE_JOURNAL_PAIR",
    "UNCERTAIN",
)

SCENARIO_EXPLICITNESS = ("EXPLICIT", "IMPLICIT", "UNCLEAR")

PROVENANCE_CODES = (
    "RESEARCHER_AUTHORED",
    "PERSONA_BASED",
    "NARRATIVE_FRAMING",
    "USAGE_SCENARIO_DERIVED",
    "CO_DESIGNED_PARTICIPATORY",
    "FIELD_OBSERVATION",
    "PRIOR_PARADIGM",
    "FICTION_DERIVED",
    "IMPLICIT_EVERYDAY_ACTIVITY",
    "HYBRID",
    "NOT_REPORTED_OR_UNCLEAR",
)

SETTING_TYPES = (
    "PRIVATE_HOME",
    "CARE_HOME",
    "HOSPITAL",
    "SCHOOL",
    "MUSEUM",
    "SHOP",
    "WORKPLACE",
    "PUBLIC_SPACE",
    "TEST_HOUSE",
    "LABORATORY_REPEATED_EVERYDAY",
    "OTHER",
    "NOT_REPORTED_OR_UNCLEAR",
)

CONTINUOUS_VS_EPISODIC = (
    "CONTINUOUS",
    "EPISODIC",
    "MIXED",
    "NOT_REPORTED_OR_UNCLEAR",
)

EMBODIMENT_COUNT = ("SINGLE", "MULTIPLE", "NOT_REPORTED_OR_UNCLEAR")

CITATION_DIRECTIONS = ("BACKWARD", "FORWARD")

CRITERIA_VERSION = "brief-pending-protocol-file"

DEFAULT_CALIBRATION_N = 100
DEFAULT_CALIBRATION_SEED = 20261005
DEFAULT_FUZZY_THRESHOLD = 0.92

SAMPLING_METHOD = (
    "stratified_without_replacement_by_year_and_source_database;"
    "largest_remainder_allocation;"
    "within_stratum_order_shuffled_with_fixed_seed;"
    "stable_pre_shuffle_order_by_record_id"
)

NORMALIZED_FIELDS = [
    "record_id",
    "source_database",
    "source_record_id",
    "title",
    "normalized_title",
    "abstract",
    "authors",
    "year",
    "journal_or_venue",
    "volume",
    "issue",
    "pages",
    "doi_raw",
    "doi_normalized",
    "url",
    "document_type",
    "keywords",
    "indexed_keywords",
    "language",
    "source_file",
    "import_timestamp",
    "origin",
    "discovery_source",
]

IMPORT_MANIFEST_FIELDS = [
    "batch_id",
    "source_database",
    "source_format",
    "source_file",
    "import_timestamp",
    "record_count",
    "notes",
]

SEARCH_LOG_FIELDS = [
    "search_id",
    "database",
    "platform",
    "search_date",
    "query_file",
    "query_version",
    "filters",
    "result_count",
    "export_filename",
    "notes",
    "performed_by",
]

SEARCH_VALIDATION_FIELDS = [
    "validation_id",
    "citation_label",
    "database",
    "expected_retrieval",
    "retrieved",
    "retrieval_date",
    "failure_reason",
    "search_version",
    "notes",
]

DUPLICATE_FIELDS = [
    "duplicate_group_id",
    "record_id_1",
    "record_id_2",
    "match_type",
    "doi_match",
    "exact_title_match",
    "fuzzy_title_score",
    "recommended_review",
    "human_decision",
    "human_reason",
    "decision_by",
    "decision_date",
    "retained_record_id",
]

SCREENING_FIELDS = [
    "record_id",
    "reviewer",
    "decision",
    "exclusion_code",
    "notes",
    "screened_at",
    "criteria_version",
]

CALIBRATION_SAMPLE_FIELDS = [
    "record_id",
    "year",
    "source_database",
    "stratum",
    "sample_order",
    "random_seed",
    "sample_size",
    "sampling_method",
]

FULL_TEXT_FIELDS = [
    "record_id",
    "full_text_available",
    "physically_embodied_robot",
    "substantive_social_interaction",
    "human_participants",
    "naturalistic_or_repeated_longterm",
    "identifiable_interaction_situation",
    "setting_extractable",
    "duration_extractable",
    "interaction_structure_extractable",
    "decision",
    "exclusion_reason",
    "reviewer",
    "notes",
    "screened_at",
]

PUBLICATION_FIELDS = [
    "publication_id",
    "record_id",
    "doi",
    "title",
    "authors",
    "year",
    "venue",
    "publication_type",
    "source_database",
    "notes",
]

STUDY_FIELDS = [
    "study_id",
    "publication_id",
    "study_label",
    "study_design",
    "country",
    "population_description",
    "participant_count",
    "recruitment",
    "notes",
]

DEPLOYMENT_FIELDS = [
    "deployment_id",
    "study_id",
    "setting_type",
    "additional_setting_types",
    "setting_detail",
    "physical_fidelity_reported",
    "physical_fidelity",
    "contextual_fidelity_reported",
    "contextual_fidelity",
    "participant_role",
    "researcher_presence",
    "number_of_sessions",
    "total_period",
    "total_period_unit",
    "session_length",
    "continuous_vs_episodic",
    "novelty_or_habituation_reported",
    "novelty_or_habituation_notes",
    "population",
    "participant_count",
    "recruitment",
    "interaction_configuration",
    "robot_platform",
    "embodiment",
    "autonomy_reported",
    "autonomy_level",
    "single_or_multiple_embodiments",
    "failure_handling",
    "safety_measures",
    "safety_measures_notes",
    "technician_oversight",
    "technician_oversight_notes",
    "consent_shared_group_spaces",
    "consent_shared_group_spaces_notes",
    "private_setting_data_collection",
    "private_setting_data_collection_notes",
    "reported_fidelity_control_limitations",
    "reported_fidelity_control_limitations_notes",
    "materials_available",
    "scripts_available",
    "code_available",
    "data_available",
    "constructs_measured",
    "instruments",
    "observational_data",
    "log_data",
    "interviews",
    "qualitative_methods",
    "interaction_level_outcomes",
    "relationship_level_outcomes",
    "source_pages",
    "extractor",
    "extraction_notes",
]

DEPLOYMENT_TRI_STATE_FIELDS = (
    "physical_fidelity_reported",
    "contextual_fidelity_reported",
    "novelty_or_habituation_reported",
    "autonomy_reported",
    "safety_measures",
    "technician_oversight",
    "consent_shared_group_spaces",
    "private_setting_data_collection",
    "reported_fidelity_control_limitations",
    "materials_available",
    "scripts_available",
    "code_available",
    "data_available",
    "observational_data",
    "log_data",
    "interviews",
    "qualitative_methods",
)

SCENARIO_FIELDS = [
    "scenario_id",
    "deployment_id",
    "study_id",
    "publication_id",
    "scenario_explicitness",
    "provenance_codes",
    "provenance_notes",
    "task_represented",
    "task_notes",
    "events_represented",
    "events_notes",
    "goals_represented",
    "goals_notes",
    "relationships_and_history",
    "relationships_and_history_notes",
    "affect_represented",
    "affect_notes",
    "norms_represented",
    "norms_notes",
    "norms_examples",
    "competing_interests_or_obligations",
    "competing_interests_notes",
    "competing_interests_in_one_to_one",
    "competing_interests_in_one_to_one_notes",
    "touch_and_physical_contact",
    "touch_notes",
    "temporal_dependencies",
    "temporal_dependencies_notes",
    "multi_party_or_group_interaction",
    "multi_party_notes",
    "group_decision_making",
    "group_decision_making_notes",
    "source_pages",
    "extractor",
    "extraction_notes",
]

SCENARIO_TRI_STATE_FIELDS = (
    "task_represented",
    "events_represented",
    "goals_represented",
    "relationships_and_history",
    "affect_represented",
    "norms_represented",
    "competing_interests_or_obligations",
    "competing_interests_in_one_to_one",
    "touch_and_physical_contact",
    "temporal_dependencies",
    "multi_party_or_group_interaction",
    "group_decision_making",
)

EXTRACTION_NOTE_FIELDS = [
    "note_id",
    "entity_level",
    "entity_id",
    "field_name",
    "note",
    "page_reference",
    "extractor",
    "noted_at",
]

DECISION_LOG_FIELDS = [
    "decision_id",
    "date",
    "stage",
    "issue",
    "original_protocol",
    "decision",
    "rationale",
    "made_by",
    "prospective_or_retrospective",
    "affected_files",
    "notes",
]

CITATION_NODE_FIELDS = [
    "record_id",
    "seed_record_id",
    "title",
    "doi_normalized",
    "year",
    "entry_route",
    "discovery_source",
    "date_retrieved",
    "in_bibliographic_set",
]

CITATION_EDGE_FIELDS = [
    "edge_id",
    "seed_record_id",
    "citing_or_cited_record",
    "direction",
    "iteration",
    "parent_record",
    "discovery_source",
    "date_retrieved",
    "notes",
]

AI_SUGGESTION_FIELDS = [
    "suggestion_id",
    "record_id",
    "task",
    "suggested_value",
    "model_provider",
    "model_name",
    "model_version",
    "prompt_id",
    "prompt_sha256",
    "created_at",
    "human_verifier",
    "human_verified_at",
    "human_accepts",
    "notes",
]

KNOWN_ITEM_LABELS = (
    "Syrdal et al. (2014)",
    "Koay et al. (2009)",
    "Walters et al. (2011)",
    "Koay et al. (2007)",
    "Kidd & Breazeal (2008)",
    "de Graaf et al. (2014)",
    "Fernaeus et al. (2010)",
    "Kanda et al. (2004)",
    "Šabanović et al. (2006)",
    "Chang & Šabanović (2015)",
)

# Reporting-completeness items. These are descriptive proportions, not a score.
COMPLETENESS_DEPLOYMENT_FIELDS = (
    "setting_type",
    "number_of_sessions",
    "total_period",
    "participant_role",
    "autonomy_level",
    "materials_available",
    "scripts_available",
    "code_available",
    "data_available",
)

COMPLETENESS_SCENARIO_FIELDS = (
    "provenance_codes",
    "relationships_and_history",
    "temporal_dependencies",
)
