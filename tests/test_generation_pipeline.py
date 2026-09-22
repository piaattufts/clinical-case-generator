"""Bootstrap, rule, generation, and validation tests. HTTP is mocked."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from app.models.cases import CaseMedication, ClinicalCase
from app.models.reference import (
    ClinicalRule,
    RefDiagnosis,
    RefLabTest,
    RefMedication,
    RefSymptom,
    RefUnit,
)
from app.repositories.cases import (
    list_answer_keys_for_case,
    list_medications_for_case,
    list_plans_for_case,
)
from app.repositories.reference import (
    get_diagnosis_by_icd10cm,
    get_lab_test_by_loinc,
    get_medication_by_rxcui,
    get_rule_by_code,
    get_unit_by_ucum,
)
from app.services.bootstrap import (
    SourceClients,
    bootstrap_reference_data,
    looks_like_combination_name,
    prefer_loinc_concept,
    token_match,
)
from app.services.generation import Scenario, generate_one_case
from app.services.rules import (
    CaseSnapshot,
    enable_rules_from_templates,
    evaluate_rules,
    hard_violations,
)
from app.services.validation import require_valid, validate_case
from app.sources.conditions import ConditionsClient
from app.sources.dailymed import DailyMedClient
from app.sources.exceptions import CaseValidationError, ReferenceResolutionError
from app.sources.hpo import HpoClient
from app.sources.icd10cm import Icd10CmClient
from app.sources.loinc import LoincClient, LoincConcept
from app.sources.rxclass import RxClassClient
from app.sources.rxnorm import RxNormClient
from app.sources.ucum import UcumClient
from app.utils.provenance import build_provenance
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tests.source_fixtures import (
    TEST_HPO_ID,
    TEST_HPO_NAME,
    TEST_ICD,
    TEST_LOINC,
    TEST_RXCUI,
    TEST_RXCUI_APIXABAN,
    TEST_RXCUI_COMBO,
    TEST_RXCUI_IBU,
    TEST_RXCUI_WARFARIN,
    TEST_SET_ID,
    TEST_SYMPTOM_NAME,
    TEST_UCUM,
    conditions_transport,
    dailymed_transport,
    hpo_transport,
    icd10cm_transport,
    loinc_transport,
    official_shaped_ucum_xml,
    rxclass_transport,
    rxnorm_transport,
    ucum_transport,
)


def _clients() -> SourceClients:
    xml_text = official_shaped_ucum_xml()
    return SourceClients(
        rxnorm=RxNormClient(
            client=httpx.Client(
                base_url="https://rxnav.nlm.nih.gov/REST", transport=rxnorm_transport()
            )
        ),
        icd10cm=Icd10CmClient(client=httpx.Client(transport=icd10cm_transport())),
        ucum=UcumClient(
            client=httpx.Client(transport=ucum_transport(xml_text)),
            essence_url="https://raw.githubusercontent.com/ucum-org/ucum/v2.2/ucum-essence.xml",
        ),
        loinc=LoincClient(
            username="TEST_USER",
            password="TEST_PASS",
            client=httpx.Client(base_url="https://fhir.loinc.org", transport=loinc_transport()),
        ),
        conditions=ConditionsClient(client=httpx.Client(transport=conditions_transport())),
        hpo=HpoClient(client=httpx.Client(transport=hpo_transport())),
        dailymed=DailyMedClient(client=httpx.Client(transport=dailymed_transport())),
        rxclass=RxClassClient(client=httpx.Client(transport=rxclass_transport())),
    )


def _write_manifest(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "medications": ["TEST_med"],
                "diagnoses": ["TEST"],
                "symptoms": ["TEST_symptom"],
                "labs": ["TEST_lab"],
                "units": ["TEST_U1"],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_bootstrap_is_idempotent_and_records_provenance(
    db_session: Session, tmp_path: Path
) -> None:
    manifest = _write_manifest(tmp_path / "manifest.json")
    clients = _clients()
    first = bootstrap_reference_data(db_session, manifest_path=manifest, clients=clients)
    assert TEST_RXCUI in first.upserted["medications"]
    assert TEST_ICD in first.upserted["diagnoses"]
    assert TEST_LOINC in first.upserted["labs"]
    assert TEST_UCUM in first.upserted["units"]
    assert TEST_SYMPTOM_NAME in first.upserted["symptoms"]
    assert TEST_SET_ID in first.upserted["labels"]
    med = get_medication_by_rxcui(db_session, TEST_RXCUI)
    assert med is not None
    assert med.source_system == "RXNORM"
    first_id = med.id
    diagnosis = get_diagnosis_by_icd10cm(db_session, TEST_ICD)
    assert diagnosis is not None
    assert diagnosis.preferred_name == "TEST_exact description from source"
    assert diagnosis.source_system == "ICD10CM"
    lab = get_lab_test_by_loinc(db_session, TEST_LOINC)
    assert lab is not None
    assert lab.source_system == "LOINC"
    unit = get_unit_by_ucum(db_session, TEST_UCUM)
    assert unit is not None
    assert unit.source_system == "UCUM"
    second = bootstrap_reference_data(db_session, manifest_path=manifest, clients=clients)
    again = get_medication_by_rxcui(db_session, TEST_RXCUI)
    assert again is not None
    assert again.id == first_id
    assert int(db_session.scalar(select(func.count()).select_from(RefMedication)) or 0) == 1
    assert not second.unresolved


def test_bootstrap_reports_unresolved_names(db_session: Session, tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "medications": ["unknown_manifest_query"],
                "diagnoses": ["unknown_diagnosis_query"],
                "symptoms": ["unknown_symptom_query"],
                "labs": ["unknown_lab_query"],
                "units": ["unknown_unit_query"],
            }
        ),
        encoding="utf-8",
    )
    result = bootstrap_reference_data(db_session, manifest_path=manifest, clients=_clients())
    kinds = {item.kind for item in result.unresolved}
    assert "medication" in kinds
    assert "diagnosis" in kinds
    assert "unit" in kinds


def test_token_match_rejects_embedded_words() -> None:
    assert token_match("Pulmonary edema", "edema")
    assert token_match("Dyspnea", "dyspnea")
    assert not token_match("Angioedema", "edema")
    assert not token_match("TEST_symptom_name", "ptom")


def test_loinc_unconfigured_is_skipped_not_fabricated(
    db_session: Session, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.config import Settings

    monkeypatch.setattr(
        "app.sources.loinc.get_settings",
        lambda: Settings(loinc_username="", loinc_password=""),
    )
    manifest = _write_manifest(tmp_path / "manifest.json")
    clients = _clients()
    clients.loinc = None
    result = bootstrap_reference_data(db_session, manifest_path=manifest, clients=clients)
    assert get_lab_test_by_loinc(db_session, TEST_LOINC) is None
    assert any(item.kind == "lab" for item in result.skipped)


def test_rules_require_source_evidence(db_session: Session, tmp_path: Path) -> None:
    provenance = build_provenance("RXNORM", "TEST_RXNORM_VERSION")
    db_session.add(
        RefMedication(
            rxcui=TEST_RXCUI_WARFARIN,
            concept_name="TEST_warfarin",
            generic_name="TEST_warfarin",
            ingredient="TEST_warfarin",
            **provenance,
        )
    )
    db_session.add(
        RefMedication(
            rxcui=TEST_RXCUI_APIXABAN,
            concept_name="TEST_apixaban",
            generic_name="TEST_apixaban",
            ingredient="TEST_apixaban",
            **provenance,
        )
    )
    db_session.flush()
    template = tmp_path / "rules.json"
    template.write_text(
        json.dumps(
            {
                "templates": [
                    {
                        "rule_code": "TEST_NO_DUAL_ANTICOAG",
                        "rule_type": "medication_incompatibility",
                        "severity": "hard",
                        "medication_names": ["warfarin", "apixaban"],
                        "evidence_needles": ["anticoagulant", "concomitant"],
                        "constraint": {"action": "prohibit_coadministration"},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    enabled = enable_rules_from_templates(
        db_session,
        dailymed=DailyMedClient(client=httpx.Client(transport=dailymed_transport())),
        rxclass=RxClassClient(client=httpx.Client(transport=rxclass_transport())),
        template_path=template,
    )
    assert "TEST_NO_DUAL_ANTICOAG" in enabled
    row = get_rule_by_code(db_session, "TEST_NO_DUAL_ANTICOAG")
    assert row is not None
    assert row.enabled is True
    assert row.source_identifier == TEST_SET_ID
    assert row.evidence_excerpt is not None
    hits = evaluate_rules(
        db_session,
        CaseSnapshot(
            age=70,
            sex="Female",
            care_context="inpatient",
            icd10cm_codes=frozenset(),
            rxcuis=frozenset({TEST_RXCUI_WARFARIN, TEST_RXCUI_APIXABAN}),
            loinc_codes=frozenset(),
        ),
    )
    assert hard_violations(hits)


def test_rule_stays_disabled_without_evidence(db_session: Session, tmp_path: Path) -> None:
    def empty_label(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/spls.json"):
            return httpx.Response(200, json={"data": []})
        return httpx.Response(404, json={})

    provenance = build_provenance("RXNORM", "TEST_RXNORM_VERSION")
    db_session.add(
        RefMedication(
            rxcui=TEST_RXCUI_WARFARIN,
            concept_name="TEST_warfarin",
            generic_name="TEST_warfarin",
            **provenance,
        )
    )
    db_session.flush()
    template = tmp_path / "rules.json"
    template.write_text(
        json.dumps(
            {
                "templates": [
                    {
                        "rule_code": "TEST_DISABLED_RULE",
                        "rule_type": "monitoring_dependency",
                        "severity": "hard",
                        "medication_names": ["warfarin"],
                        "lab_names": ["inr"],
                        "evidence_needles": ["inr", "prothrombin"],
                        "constraint": {"action": "require_lab"},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    enabled = enable_rules_from_templates(
        db_session,
        dailymed=DailyMedClient(client=httpx.Client(transport=httpx.MockTransport(empty_label))),
        rxclass=RxClassClient(client=httpx.Client(transport=rxclass_transport())),
        template_path=template,
    )
    assert enabled == []
    row = get_rule_by_code(db_session, "TEST_DISABLED_RULE")
    assert row is not None
    assert row.enabled is False


def _seed_generation_refs(session: Session) -> None:
    rx = build_provenance("RXNORM", "TEST_RXNORM_VERSION")
    icd = build_provenance("ICD10CM")
    loinc = build_provenance("LOINC", "TEST_LOINC_VERSION")
    ucum = build_provenance("UCUM", "TEST_UCUM_2")
    session.add(
        RefMedication(
            rxcui=TEST_RXCUI,
            concept_name="TEST_med branded product",
            generic_name="TEST_med",
            ingredient="TEST_ingredient",
            strength="TEST_strength",
            **rx,
        )
    )
    session.add(
        RefMedication(
            rxcui=TEST_RXCUI_WARFARIN,
            concept_name="TEST_warfarin",
            generic_name="TEST_warfarin",
            ingredient="TEST_warfarin",
            **rx,
        )
    )
    session.add(
        RefMedication(
            rxcui=TEST_RXCUI_APIXABAN,
            concept_name="TEST_apixaban",
            generic_name="TEST_apixaban",
            ingredient="TEST_apixaban",
            **rx,
        )
    )
    session.add(
        RefMedication(
            rxcui=TEST_RXCUI_IBU,
            concept_name="TEST_ibuprofen",
            generic_name="TEST_ibuprofen",
            ingredient="TEST_ibuprofen",
            **rx,
        )
    )
    session.add(
        RefDiagnosis(
            icd10cm_code=TEST_ICD,
            preferred_name="TEST_heart failure description",
            snomed_code=None,
            **icd,
        )
    )
    session.add(RefSymptom(preferred_name=TEST_SYMPTOM_NAME, snomed_code=None, **icd))
    session.add(
        RefLabTest(
            loinc_code=TEST_LOINC,
            long_common_name="TEST_lab long name",
            component="TEST_component",
            example_ucum_units=["TEST_mg/dL"],
            **loinc,
        )
    )
    session.add(RefUnit(ucum_code=TEST_UCUM, display_name="TEST unit one", **ucum))
    session.flush()


def _test_scenario() -> Scenario:
    return Scenario(
        code="TEST_HF",
        specialty="cardiology",
        care_context="inpatient",
        age_min=60,
        age_max=60,
        target_error_category="omission",
        diagnosis_queries=["TEST_heart"],
        symptom_queries=["TEST_symptom"],
        medication_queries=["TEST_med"],
        anticoagulant_mutex_queries=["warfarin", "apixaban"],
        lab_queries=["TEST_lab"],
    )


def test_seeded_generation_is_deterministic_and_injects_one_error(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    first = generate_one_case(
        db_session,
        sequence=1,
        seed=42,
        scenario=_test_scenario(),
        inject_error=True,
        use_openai=False,
    )
    assert first.case_id_code == "SYN-000001"
    assert first.clean_passed is True
    assert first.injected is not None
    case = db_session.get(ClinicalCase, first.case_id)
    assert case is not None
    keys = list_answer_keys_for_case(db_session, case.id)
    assert len(keys) == 1
    assert keys[0].error_category == "f1_omission"
    assert keys[0].error_family == "family_1"
    assert keys[0].is_primary_error is True
    targets = [plan for plan in list_plans_for_case(db_session, case.id) if plan.is_error_target]
    assert len(targets) == 1
    discharge = [
        item
        for item in list_medications_for_case(db_session, case.id)
        if item.context == "discharge"
    ]
    home = [
        item for item in list_medications_for_case(db_session, case.id) if item.context == "home"
    ]
    assert len(home) - len(discharge) == 1
    rxcuis: set[str] = set()
    for item in home:
        if item.ref_medication_id is None:
            continue
        linked = db_session.get(RefMedication, item.ref_medication_id)
        if linked is not None:
            rxcuis.add(linked.rxcui)
    assert TEST_RXCUI in rxcuis
    assert not ({TEST_RXCUI_WARFARIN, TEST_RXCUI_APIXABAN} <= rxcuis)
    age = case.patient_age
    gender = case.patient_gender
    omitted = first.injected.rxcui
    second = generate_one_case(
        db_session,
        sequence=1,
        seed=42,
        scenario=_test_scenario(),
        inject_error=True,
        use_openai=False,
    )
    again = db_session.get(ClinicalCase, second.case_id)
    assert again is not None
    assert again.patient_age == age
    assert again.patient_gender == gender
    assert second.injected is not None
    assert second.injected.rxcui == omitted


def test_clean_case_validation_and_invented_identifier_rejection(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    result = generate_one_case(
        db_session,
        sequence=2,
        seed=7,
        scenario=_test_scenario(),
        inject_error=False,
        use_openai=False,
    )
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    report = validate_case(db_session, case, expect_injected_error=False)
    require_valid(report)
    fake = RefMedication(rxcui="INVENTED_RXCUI", concept_name="not source backed")
    db_session.add(fake)
    db_session.flush()
    db_session.add(
        CaseMedication(
            case_id=case.id,
            medication_id="MED-SYN000002-099",
            ref_medication_id=fake.id,
            context="home",
            drug="invented",
            status="home",
            source_reference="RXCUI:INVENTED_RXCUI",
        )
    )
    db_session.flush()
    failed = validate_case(db_session, case, expect_injected_error=False)
    assert failed.passed is False
    assert any(
        "invented" in item.casefold() or "provenance" in item.casefold() for item in failed.errors()
    )
    with pytest.raises(CaseValidationError):
        require_valid(failed)


def test_clinical_conditional_rejects_dual_anticoagulant(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    db_session.add(
        ClinicalRule(
            rule_code="TEST_NO_DUAL_ANTICOAG",
            rule_type="medication_incompatibility",
            severity="hard",
            enabled=True,
            input_rxcui=TEST_RXCUI_WARFARIN,
            related_rxcui=TEST_RXCUI_APIXABAN,
            constraint_json={"action": "prohibit_coadministration"},
            source_system="DAILYMED",
            source_identifier=TEST_SET_ID,
        )
    )
    db_session.flush()
    hits = evaluate_rules(
        db_session,
        CaseSnapshot(
            age=80,
            sex="Male",
            care_context="inpatient",
            icd10cm_codes=frozenset({TEST_ICD}),
            rxcuis=frozenset({TEST_RXCUI_WARFARIN, TEST_RXCUI_APIXABAN}),
            loinc_codes=frozenset(),
        ),
    )
    assert any(item.rule_code == "TEST_NO_DUAL_ANTICOAG" for item in hard_violations(hits))
    result = generate_one_case(
        db_session,
        sequence=3,
        seed=99,
        scenario=_test_scenario(),
        inject_error=False,
        use_openai=False,
    )
    case = db_session.get(ClinicalCase, result.case_id)
    assert case is not None
    snapshot_rxcuis = set()
    for medication in list_medications_for_case(db_session, case.id):
        if medication.ref_medication_id is None:
            continue
        row = db_session.get(RefMedication, medication.ref_medication_id)
        if row is not None:
            snapshot_rxcuis.add(row.rxcui)
    assert not ({TEST_RXCUI_WARFARIN, TEST_RXCUI_APIXABAN} <= snapshot_rxcuis)


def test_combination_name_is_rejected_for_single_ingredient_query(
    db_session: Session, tmp_path: Path
) -> None:
    assert looks_like_combination_name("TEST_med / TEST_other Oral Tablet")
    assert not looks_like_combination_name("TEST_med branded product")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "medications": ["TEST_combo"],
                "diagnoses": [],
                "symptoms": [],
                "labs": [],
                "units": [],
            }
        ),
        encoding="utf-8",
    )
    result = bootstrap_reference_data(db_session, manifest_path=manifest, clients=_clients())
    assert TEST_RXCUI in result.upserted["medications"]
    assert TEST_RXCUI_COMBO not in result.upserted["medications"]


def test_hpo_fallback_resolves_orthopnea(db_session: Session, tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "medications": [],
                "diagnoses": [],
                "symptoms": ["orthopnea"],
                "labs": [],
                "units": [],
            }
        ),
        encoding="utf-8",
    )
    result = bootstrap_reference_data(db_session, manifest_path=manifest, clients=_clients())
    assert TEST_HPO_NAME in result.upserted["symptoms"]
    row = db_session.scalar(select(RefSymptom).where(RefSymptom.preferred_name == TEST_HPO_NAME))
    assert row is not None
    assert row.snomed_code is None
    assert row.source_system == "NLM_HPO"
    assert TEST_HPO_ID in (row.synonyms or [])


def test_supported_error_categories_inject_exactly_one(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.stop_medication_queries = ["ibuprofen"]
    dose = generate_one_case(
        db_session,
        sequence=11,
        seed=3,
        scenario=scenario,
        inject_error=True,
        use_openai=False,
        error_category="dose_mismatch",
    )
    assert dose.injected is not None
    assert dose.injected.category == "f1_dose_mismatch"
    freq = generate_one_case(
        db_session,
        sequence=12,
        seed=3,
        scenario=scenario,
        inject_error=True,
        use_openai=False,
        error_category="frequency_mismatch",
    )
    assert freq.injected is not None
    assert freq.injected.category == "f1_frequency_mismatch"
    cont = generate_one_case(
        db_session,
        sequence=13,
        seed=3,
        scenario=scenario,
        inject_error=True,
        use_openai=False,
        error_category="incorrect_continuation",
    )
    assert cont.injected is not None
    assert cont.injected.category == "f1_commission"
    case = db_session.get(ClinicalCase, cont.case_id)
    assert case is not None
    report = validate_case(
        db_session, case, expect_injected_error=True, expected_category="f1_commission"
    )
    require_valid(report)
    targets = [plan for plan in list_plans_for_case(db_session, case.id) if plan.is_error_target]
    assert len(targets) >= 1
    keys = list_answer_keys_for_case(db_session, case.id)
    assert len(keys) == 1
    assert keys[0].error_category == "f1_commission"


def test_prefer_loinc_ranks_query_match_ahead_of_code_order() -> None:
    panel = LoincConcept(
        loinc_code="TEST_10000-0",
        long_common_name="TEST_unrelated panel",
        status="ACTIVE",
    )
    inr = LoincConcept(
        loinc_code="TEST_20000-0",
        long_common_name="TEST_INR in Platelet poor plasma",
        component="TEST_INR",
        status="ACTIVE",
    )
    chosen = prefer_loinc_concept([panel, inr], "inr")
    assert chosen is not None
    assert chosen.loinc_code == "TEST_20000-0"


def test_prefer_loinc_ignores_part_codes() -> None:
    part = LoincConcept(loinc_code="LP15098-4", long_common_name="Potassium", status="ACTIVE")
    term = LoincConcept(
        loinc_code="TEST_2823-3",
        long_common_name="TEST_Potassium [Moles/volume] in Serum or Plasma",
        status="ACTIVE",
        example_ucum_units=["mmol/L"],
    )
    chosen = prefer_loinc_concept([part, term], "potassium")
    assert chosen is not None
    assert chosen.loinc_code == "TEST_2823-3"


def test_prefer_loinc_ranks_serum_over_timed_variant() -> None:
    dialysis = LoincConcept(
        loinc_code="TEST_11041-1",
        long_common_name="TEST_Creatinine [Mass/volume] in Serum or Plasma --post dialysis",
        status="ACTIVE",
        example_ucum_units=["mg/dL"],
    )
    serum = LoincConcept(
        loinc_code="TEST_2160-0",
        long_common_name="TEST_Creatinine [Mass/volume] in Serum or Plasma",
        status="ACTIVE",
        example_ucum_units=["mg/dL"],
    )
    chosen = prefer_loinc_concept([dialysis, serum], "creatinine")
    assert chosen is not None
    assert chosen.loinc_code == "TEST_2160-0"


def test_prefer_loinc_skips_ratio_fraction_hemoglobin() -> None:
    ratio = LoincConcept(
        loinc_code="TEST_35125-4",
        long_common_name="TEST_Hemoglobin Lepore/Hemoglobin.total in Blood",
        status="ACTIVE",
        example_ucum_units=["%"],
    )
    total = LoincConcept(
        loinc_code="TEST_718-7",
        long_common_name="TEST_Hemoglobin [Mass/volume] in Blood",
        status="ACTIVE",
        example_ucum_units=["g/dL"],
    )
    chosen = prefer_loinc_concept([ratio, total], "hemoglobin")
    assert chosen is not None
    assert chosen.loinc_code == "TEST_718-7"


def test_prefer_loinc_prefers_base_hemoglobin_over_a2() -> None:
    subtype = LoincConcept(
        loinc_code="TEST_4550-0",
        long_common_name="TEST_Hemoglobin A2 [Moles/volume] in Blood by Chromatography column",
        status="ACTIVE",
        example_ucum_units=["mmol/L"],
    )
    total = LoincConcept(
        loinc_code="TEST_718-7",
        long_common_name="TEST_Hemoglobin [Mass/volume] in Blood",
        status="ACTIVE",
        example_ucum_units=["g/dL"],
    )
    chosen = prefer_loinc_concept([subtype, total], "hemoglobin")
    assert chosen is not None
    assert chosen.loinc_code == "TEST_718-7"


def test_generation_rejects_unresolved_scenario_lab(db_session: Session) -> None:
    _seed_generation_refs(db_session)
    scenario = _test_scenario()
    scenario.lab_queries = ["TEST_lab", "missing_lab_query"]
    with pytest.raises(ReferenceResolutionError, match="missing_lab_query"):
        generate_one_case(
            db_session,
            sequence=31,
            seed=9,
            scenario=scenario,
            inject_error=False,
            use_openai=False,
        )
