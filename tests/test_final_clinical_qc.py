"""Regimen provenance and active-batch clinical QC regressions."""

from __future__ import annotations

import json
import re
from pathlib import Path
from types import SimpleNamespace

from app.services.medication_regimens import (
    administration_for,
    beta_blocker_frequency_conflicts,
    echo_course_statement,
    endocarditis_microbiology_conflicts,
    imaging_timepoint_conflict,
    living_disposition_conflict,
    regimen_field_conflicts,
)
from scripts.check_docs import main as check_docs_main

ROOT = Path(__file__).resolve().parents[1]
BATCHES = (
    ROOT / "data" / "validation_balanced_v4",
    ROOT / "data" / "validation_seedcases_v3",
)
LEAK = re.compile(
    r"clean case|planted error|seed document|temporal_role|profile id|answer key",
    re.IGNORECASE,
)


def _med(name: str, rxcui: str = "100") -> SimpleNamespace:
    return SimpleNamespace(
        ingredient=name,
        generic_name=name,
        concept_name=name,
        dose_form=None,
        rxcui=rxcui,
    )


def _cases() -> list[tuple[str, dict[str, object]]]:
    found: list[tuple[str, dict[str, object]]] = []
    for directory in BATCHES:
        resident = json.loads((directory / "resident_validation_cases.json").read_text())
        investigator = json.loads((directory / "investigator_answer_key.json").read_text())
        keys = {row["validation_case_id"]: row for row in investigator["cases"]}
        for case in resident["cases"]:
            found.append(
                (
                    case["case_id_code"],
                    {"resident": case, "key": keys[case["case_id_code"]]},
                )
            )
    return found


def test_apixaban_standard_regimen_is_not_once_daily_2_5() -> None:
    admin = administration_for(
        _med("apixaban 2.5 MG Oral Tablet"),
        fallback_frequency="once daily",
    )
    assert admin.dose == "5 MG"
    assert admin.route == "oral"
    assert admin.frequency == "twice daily"
    assert regimen_field_conflicts(
        _med("apixaban 5 MG Oral Tablet"),
        dose="2.5 MG",
        route="oral",
        frequency="once daily",
    )


def test_product_strength_is_not_copied_as_administered_dose() -> None:
    admin = administration_for(
        _med("ceftriaxone 500 MG Injection"),
        fallback_frequency="once daily",
    )
    assert admin.dose == "2000 MG"
    assert admin.route == "intravenous"
    assert "500" not in admin.dose


def test_beta_blocker_formulation_matches_frequency() -> None:
    succinate = administration_for(
        _med("24 HR metoprolol succinate 25 MG Extended Release Oral Tablet"),
        fallback_frequency="twice daily",
    )
    tartrate = administration_for(
        _med("metoprolol tartrate 25 MG Oral Tablet"),
        fallback_frequency="once daily",
    )
    assert succinate.frequency == "once daily"
    assert tartrate.frequency == "twice daily"
    assert beta_blocker_frequency_conflicts("metoprolol tartrate 25 MG", "once daily")
    assert not beta_blocker_frequency_conflicts("metoprolol succinate 25 MG", "once daily")
    assert beta_blocker_frequency_conflicts("carvedilol 6.25 MG Oral Tablet", "once daily")


def test_spironolactone_heart_failure_dose_is_25() -> None:
    admin = administration_for(
        _med("spironolactone 100 MG Oral Tablet"),
        fallback_frequency="once daily",
    )
    assert admin.dose == "25 MG"
    assert admin.frequency == "once daily"


def test_imaging_timepoint_rejects_admission_comparison() -> None:
    assert imaging_timepoint_conflict(
        "admission",
        "Improving pulmonary edema compared with admission.",
    )
    assert (
        imaging_timepoint_conflict(
            "discharge",
            "Improved pulmonary edema compared with admission.",
        )
        is None
    )


def test_endocarditis_helpers_require_chronology_and_an_imaging_finding() -> None:
    assert echo_course_statement("Vegetation treatment course in progress")
    assert not echo_course_statement(
        "Mobile echodensity consistent with a vegetation; ventricular function preserved."
    )
    assert endocarditis_microbiology_conflicts(
        [
            {
                "timepoint": "admission",
                "result": "no growth",
                "organism": "",
                "status": "",
                "notes": "",
            }
        ]
    )
    assert not endocarditis_microbiology_conflicts(
        [
            {
                "timepoint": "admission",
                "result": "growth",
                "organism": "gram-positive cocci",
                "status": "final",
                "notes": "",
            },
            {
                "timepoint": "inpatient",
                "result": "no growth",
                "organism": "",
                "status": "final",
                "notes": "cultures cleared",
            },
        ]
    )


def test_living_situation_must_be_labeled_baseline_when_disposition_leaves_home() -> None:
    assert living_disposition_conflict("Lives at home", "inpatient rehabilitation")
    assert living_disposition_conflict(
        "Baseline living situation: lives at home",
        "inpatient rehabilitation",
    ) is None


def test_active_cases_keep_curated_regimens_and_temporal_roles() -> None:
    cases = _cases()
    assert len(cases) == 48
    for case_id, payload in cases:
        resident = payload["resident"]
        key = payload["key"]
        assert isinstance(resident, dict)
        assert isinstance(key, dict)
        meds = resident["CaseMedication"]
        assert isinstance(meds, list)
        hpi = ((resident["ClinicalCase"]["presentation"] or {}).get("hpi")) or ""
        assert not LEAK.search(hpi), case_id
        for medication in meds:
            assert isinstance(medication, dict)
            blob = " ".join(
                str(medication.get(field) or "")
                for field in ("drug", "dose", "route", "frequency", "notes", "indication")
            )
            assert not LEAK.search(blob), case_id
            drug = str(medication.get("drug") or "").casefold()
            if "apixaban" in drug:
                assert medication["dose"] == "5 MG", case_id
                assert medication["frequency"] == "twice daily", case_id
            if "spironolactone" in drug:
                assert medication["dose"] == "25 MG", case_id
            if "ceftriaxone" in drug:
                assert medication["context"] != "home", case_id
                assert medication["route"] == "intravenous", case_id
                if medication.get("context") != "discharge":
                    assert medication["dose"] == "2000 MG", case_id
            if "azithromycin" in drug:
                assert medication["context"] != "home", case_id
            if "enoxaparin" in drug:
                assert medication["dose"] == "40 MG", case_id
                assert medication["route"] == "subcutaneous", case_id
                assert medication["context"] != "home", case_id
        for image in resident.get("CaseImaging") or []:
            assert isinstance(image, dict)
            assert imaging_timepoint_conflict(image.get("timepoint"), image.get("finding")) is None
        dx = str(resident["ClinicalCase"].get("admission_dx") or "").casefold()
        if "endocarditis" in dx:
            micros = resident.get("CaseMicrobiology") or []
            assert not endocarditis_microbiology_conflicts(
                [
                    {
                        "timepoint": str(row.get("timepoint") or ""),
                        "result": str(row.get("result") or ""),
                        "organism": str(row.get("organism") or ""),
                        "status": str(row.get("status") or ""),
                        "notes": str(row.get("notes") or ""),
                    }
                    for row in micros
                ]
            ), case_id
            for image in resident.get("CaseImaging") or []:
                study = str(image.get("study_type") or "").casefold()
                if "echo" in study:
                    assert not echo_course_statement(str(image.get("finding") or "")), case_id
        if any("ceftriaxone" in str(item.get("drug") or "").casefold() for item in meds):
            assert resident.get("CaseMonitoring"), case_id
        category = str((key.get("error") or {}).get("error_category") or "none")
        warfarin_discharge = any(
            "warfarin" in str(item.get("drug") or "").casefold()
            and item.get("context") == "discharge"
            for item in meds
        )
        if warfarin_discharge and category != "f2_monitoring_not_arranged":
            assert resident.get("CaseMonitoring"), case_id
        social = resident["ClinicalCase"].get("social_context") or ""
        disposition = resident["ClinicalCase"].get("disposition_status") or ""
        assert living_disposition_conflict(str(social), str(disposition)) is None
        final = key["post_injection_validation"]
        assert isinstance(final, dict)
        assert final["passed"] is True, case_id
        assert final["errors"] == [], case_id


def test_documentation_checks_pass() -> None:
    assert check_docs_main() == 0


_REVEALING = re.compile(
    r"stop at discharge|no outpatient continuation|not intended for outpatient|"
    r"should not be continued|standard labeled dose|not a universal dose|"
    r"correct dose|appropriate dose|intended discharge state|"
    r"hospital-only medication that must be stopped|inpatient-only indication|"
    r"do not restart|resume home therapy",
    re.IGNORECASE,
)


def _resident_text(case: dict[str, object]) -> str:
    chunks: list[str] = []
    clinical = case["ClinicalCase"]
    assert isinstance(clinical, dict)
    presentation = clinical.get("presentation") or {}
    assert isinstance(presentation, dict)
    chunks.append(str(presentation.get("hpi") or ""))
    for key in ("CaseNote", "CaseInstruction", "CaseMedication", "CaseConsult"):
        rows = case.get(key) or []
        assert isinstance(rows, list)
        for row in rows:
            if isinstance(row, dict):
                chunks.extend(str(value or "") for value in row.values())
    return "\n".join(chunks)


def test_resident_charts_do_not_reveal_the_answer() -> None:
    for case_id, payload in _cases():
        resident = payload["resident"]
        assert isinstance(resident, dict)
        assert _REVEALING.search(_resident_text(resident)) is None, case_id
        assert "decision_reason" not in json.dumps(resident), case_id


def test_hospital_only_reason_stays_on_the_investigator_plan() -> None:
    found = 0
    for case_id, payload in _cases():
        key = payload["key"]
        resident = payload["resident"]
        assert isinstance(key, dict)
        assert isinstance(resident, dict)
        error = key["error"]
        assert isinstance(error, dict)
        if error.get("error_category") in (None, "none"):
            state = error
        else:
            state = error.get("clean_expected_state") or {}
        assert isinstance(state, dict)
        plans = state.get("plans") or []
        assert isinstance(plans, list)
        meds = resident["CaseMedication"]
        assert isinstance(meds, list)
        for plan in plans:
            assert isinstance(plan, dict)
            reason = str(plan.get("decision_reason") or "")
            if "inpatient-only indication" not in reason.casefold():
                continue
            found += 1
            assert plan.get("correct_discharge_state") == "stop", case_id
            drug = str(plan.get("drug") or "").casefold()
            for medication in meds:
                assert isinstance(medication, dict)
                if drug and drug in str(medication.get("drug") or "").casefold():
                    blob = " ".join(
                        str(medication.get(field) or "")
                        for field in ("notes", "indication", "held_reason")
                    )
                    assert "inpatient-only indication" not in blob.casefold(), case_id
                    assert "hospital-only" not in blob.casefold(), case_id
    assert found > 0


def test_val_823_hold_matches_the_pending_decision() -> None:
    _case_id, payload = next(item for item in _cases() if item[0] == "VAL-823")
    resident = payload["resident"]
    key = payload["key"]
    assert isinstance(resident, dict)
    assert isinstance(key, dict)
    error = key["error"]
    assert isinstance(error, dict)
    assert error["error_category"] == "f2_pending_decision_followup_missing"
    meds = resident["CaseMedication"]
    assert isinstance(meds, list)
    discharge = [
        item
        for item in meds
        if isinstance(item, dict)
        and "apixaban" in str(item.get("drug") or "").casefold()
        and item.get("context") == "discharge"
    ]
    assert len(discharge) == 1
    assert discharge[0]["status"] == "held"
    assert resident["CaseFollowup"] == []
    text = _resident_text(resident).casefold()
    assert "pending" in text
    assert "restart versus continued hold" in text
    plans = error["clean_expected_state"]["plans"]
    apixaban = next(plan for plan in plans if "apixaban" in plan["drug"].casefold())
    assert apixaban["decision"] == "hold"
    assert apixaban["correct_discharge_state"] == "hold"
    followup = error["clean_expected_state"]["diversity"]["fingerprint"]["followup"]
    assert followup
    assert "cardiology" in followup[0]


def test_warfarin_monitoring_matches_the_answer_key() -> None:
    seen: set[str] = set()
    for case_id, payload in _cases():
        resident = payload["resident"]
        key = payload["key"]
        assert isinstance(resident, dict)
        assert isinstance(key, dict)
        meds = resident["CaseMedication"]
        assert isinstance(meds, list)
        if not any("warfarin" in str(item.get("drug") or "").casefold() for item in meds):
            continue
        seen.add(case_id)
        category = str((key.get("error") or {}).get("error_category") or "none")
        discharge = any(
            "warfarin" in str(item.get("drug") or "").casefold()
            and item.get("context") == "discharge"
            and item.get("status") != "held"
            for item in meds
        )
        monitoring = resident.get("CaseMonitoring") or []
        followup = json.dumps(resident.get("CaseFollowup") or []).casefold()
        if category == "f2_monitoring_not_arranged":
            assert discharge, case_id
            assert monitoring == [], case_id
            assert "anticoagulation" in followup, case_id
        elif category == "f1_omission":
            assert not discharge, case_id
            assert monitoring, case_id
        else:
            assert discharge, case_id
            assert monitoring, case_id
    assert seen == {"VAL-703", "VAL-707", "VAL-710", "VAL-817", "VAL-818", "VAL-819", "VAL-820"}


def test_active_batches_keep_one_intended_discrepancy() -> None:
    for case_id, payload in _cases():
        key = payload["key"]
        assert isinstance(key, dict)
        final = key["post_injection_validation"]
        assert isinstance(final, dict)
        assert final["passed"] is True, case_id
        assert final["errors"] == [], case_id
        error = key["error"]
        assert isinstance(error, dict)
        category = error.get("error_category")
        status = error.get("control_error_status")
        if status == "clean_control":
            assert category in (None, "none"), case_id
        else:
            assert status == "error_bearing", case_id
            assert category not in (None, "none"), case_id


def test_root_readme_explains_both_methods_and_validation() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    lowered = readme.casefold()
    assert "two active prospective validation datasets" in lowered
    assert "balanced structured generation" in lowered
    assert "resident-seed-guided generation" in lowered
    assert "CLINIPROOF_BALANCED_V4" in readme
    assert "CLINIPROOF_SEEDCASES_V3" in readme
    assert "VAL-701" in readme and "VAL-724" in readme
    assert "VAL-801" in readme and "VAL-824" in readme
    assert "not** the current study set" in lowered or "not the current study set" in lowered
    for heading in (
        "### C1 — Clinical plausibility",
        "### C2 — Intended assessment problem",
        "### C3 — Detectability",
        "### C4 — No unintended clinically meaningful problem",
        "### C5 — Difficulty",
    ):
        assert heading in readme
    assert "Accept." in readme and "Revise." in readme and "Exclude." in readme
    assert (
        "A source-backed terminology concept is not automatically a clinically appropriate choice"
        in readme
    )
    assert "Passing automated validation does not establish clinical validity." in readme
    assert "`f1_omission`" in readme and "`f2_monitoring_not_arranged`" in readme
    assert "f2_coprescription_omitted" in readme
    assert "data/validation_balanced_v4/readable/all_cases.md" in readme
    assert "data/validation_seedcases_v3/readable/all_cases.md" in readme
    assert "does not treat product strength as the administered dose" in readme
    for batch, first, last, family_1, family_2 in (
        (ROOT / "data" / "validation_balanced_v4" / "README.md", "VAL-701", "VAL-724", "11", "9"),
        (ROOT / "data" / "validation_seedcases_v3" / "README.md", "VAL-801", "VAL-824", "7", "13"),
    ):
        text = batch.read_text(encoding="utf-8")
        manifest = json.loads((batch.parent / "validation_manifest.json").read_text())
        assert manifest["batch_code"] in text
        assert first in text and last in text
        assert "24" in text
        assert family_1 in text and family_2 in text
        assert len(manifest["cases"]) == 24
