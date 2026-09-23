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
