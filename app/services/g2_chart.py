"""Structured Generation 2 chart. Narrative is rendered from stored facts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.services.g2_terminology import (
    ALLOWED_ACTIONS,
    ICD10,
    LOINC,
    TIME_RANK,
    regimen_by_id,
)
from app.services.synthea_eligibility import MappedMedication
from app.sources.synthea import LongitudinalPatient

SYNTHEA = "synthea_longitudinal"
EPISODE = "cliniproof_episode_generated"
TERMINOLOGY = "reference_terminology"
REFERENCE = "investigator_derived_reference"


@dataclass
class Chart:
    patient: LongitudinalPatient
    scenario_code: str
    variant_id: str
    eligibility_tier: str
    episode_seed: str
    fingerprint: dict[str, str]
    physiology_expectations: list[str]
    synthea_meta: dict[str, str]
    chief_complaint: str = ""
    syndrome: str = ""
    symptom_duration: str = ""
    symptom_course: str = ""
    symptoms: list[str] = field(default_factory=list)
    disposition: str = "home"
    specialty: str = "internal medicine"
    facts: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    labs: list[dict[str, Any]] = field(default_factory=list)
    vitals: list[dict[str, Any]] = field(default_factory=list)
    weights: list[dict[str, Any]] = field(default_factory=list)
    diagnoses: list[dict[str, Any]] = field(default_factory=list)
    imaging: list[dict[str, Any]] = field(default_factory=list)
    procedures: list[dict[str, Any]] = field(default_factory=list)
    micro: list[dict[str, Any]] = field(default_factory=list)
    consults: list[dict[str, Any]] = field(default_factory=list)
    monitoring: list[dict[str, Any]] = field(default_factory=list)
    followup: list[dict[str, Any]] = field(default_factory=list)
    instructions: list[dict[str, Any]] = field(default_factory=list)
    intake: list[dict[str, Any]] = field(default_factory=list)
    medrec: list[dict[str, Any]] = field(default_factory=list)
    medications: list[dict[str, Any]] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    def fact(
        self,
        fact_id: str,
        domains: list[str],
        text: str,
        provenance: str,
        order: int,
        section: str,
    ) -> str:
        self.facts.append(
            {
                "fact_id": fact_id,
                "domains": domains,
                "text": text,
                "provenance": provenance,
                "time_order": order,
                "section": section,
                "resident_visible": True,
            }
        )
        return fact_id

    def event(
        self,
        event_id: str,
        event_type: str,
        order: int,
        provenance: str,
        summary: str,
        support_ids: list[str],
        *,
        empiric: bool = False,
    ) -> None:
        self.events.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "time_order": order,
                "provenance": provenance,
                "summary": summary,
                "supporting_data": support_ids,
                "empiric": empiric,
            }
        )

    def lab(
        self,
        loinc_code: str,
        points: list[tuple[str, float | str]],
        provenance: str,
    ) -> None:
        name, unit = LOINC[loinc_code]
        for timepoint, value in points:
            if timepoint not in TIME_RANK:
                raise KeyError(timepoint)
            row: dict[str, Any] = {
                "loinc_code": loinc_code,
                "test_name": name,
                "unit": unit,
                "timepoint": timepoint,
                "time_rank": TIME_RANK[timepoint],
                "provenance": provenance,
                "code_provenance": TERMINOLOGY,
            }
            if isinstance(value, str):
                row["value"] = None
                row["value_text"] = value
            else:
                row["value"] = value
                row["value_text"] = None
            self.labs.append(row)

    def vital(
        self,
        timepoint: str,
        *,
        temp_c: float,
        bp_systolic: int,
        bp_diastolic: int,
        heart_rate: int,
        resp_rate: int,
        spo2_percent: float,
        provenance: str,
    ) -> None:
        self.vitals.append(
            {
                "timepoint": timepoint,
                "time_rank": TIME_RANK[timepoint],
                "temp_c": temp_c,
                "bp_systolic": bp_systolic,
                "bp_diastolic": bp_diastolic,
                "heart_rate": heart_rate,
                "resp_rate": resp_rate,
                "spo2_percent": spo2_percent,
                "provenance": provenance,
            }
        )

    def weight(self, timepoint: str, weight_kg: float, provenance: str) -> None:
        self.weights.append(
            {
                "timepoint": timepoint,
                "time_rank": TIME_RANK[timepoint],
                "weight_kg": weight_kg,
                "provenance": provenance,
            }
        )

    def diagnosis(
        self,
        name: str,
        icd10cm: str | None,
        diagnosis_type: str,
        provenance: str,
        *,
        snomed_code: str | None = None,
        context: str = "inpatient",
    ) -> None:
        if icd10cm is not None and icd10cm not in ICD10:
            raise KeyError(f"ICD-10-CM {icd10cm} is not in the verified Generation 2 table")
        self.diagnoses.append(
            {
                "diagnosis": name,
                "icd10cm": icd10cm,
                "snomed_code": snomed_code,
                "diagnosis_type": diagnosis_type,
                "status": "active",
                "context": context,
                "provenance": provenance,
                "code_provenance": TERMINOLOGY if icd10cm or snomed_code else None,
            }
        )

    def image(self, timepoint: str, study_type: str, finding: str, provenance: str) -> None:
        self.imaging.append(
            {
                "timepoint": timepoint,
                "study_type": study_type,
                "body_site": "",
                "finding": finding,
                "provenance": provenance,
            }
        )

    def procedure(
        self,
        name: str,
        when: str,
        findings: str,
        provenance: str,
        *,
        complications: str = "none",
    ) -> None:
        self.procedures.append(
            {
                "procedure_name": name,
                "procedure_type": "inpatient",
                "time": when,
                "findings": findings,
                "complications": complications,
                "provenance": provenance,
            }
        )

    def microbiology(
        self,
        timepoint: str,
        specimen: str,
        test: str,
        result: str,
        provenance: str,
        *,
        organism: str = "",
        status: str = "final",
        notes: str = "",
    ) -> None:
        self.micro.append(
            {
                "timepoint": timepoint,
                "specimen": specimen,
                "test": test,
                "organism": organism,
                "result": result,
                "status": status,
                "notes": notes,
                "provenance": provenance,
            }
        )

    def consult(self, service: str, timepoint: str, assessment: str, recommendation: str) -> None:
        self.consults.append(
            {
                "service": service,
                "timepoint": timepoint,
                "assessment": assessment,
                "recommendation": recommendation,
                "provenance": EPISODE,
            }
        )

    def monitor(self, parameter: str, frequency: str, target: str, service: str) -> None:
        self.monitoring.append(
            {
                "parameter": parameter,
                "frequency": frequency,
                "target": target,
                "trigger_for_action": "",
                "duration": "until the first follow-up visit",
                "responsible_service": service,
                "provenance": EPISODE,
            }
        )

    def follow(self, item: str, timing: str, service: str) -> None:
        self.followup.append(
            {
                "item": item,
                "timing": timing,
                "with_service": service,
                "provenance": EPISODE,
            }
        )

    def instruction(self, category: str, text: str) -> None:
        self.instructions.append(
            {"category": category, "instruction_text": text, "provenance": EPISODE}
        )

    def intake_output(self, timepoint: str, intake_ml: int, output_ml: int, notes: str) -> None:
        self.intake.append(
            {
                "timepoint": timepoint,
                "intake_ml": intake_ml,
                "output_ml": output_ml,
                "net_ml": intake_ml - output_ml,
                "notes": notes,
                "provenance": EPISODE,
            }
        )

    def medrec_row(self, drug: str, source: str, status: str, note: str) -> None:
        self.medrec.append(
            {
                "drug": drug,
                "bpmh_source": source,
                "medrec_status": status,
                "notes": note,
                "provenance": EPISODE,
            }
        )

    def medication(
        self,
        *,
        drug: str,
        dose: str,
        route: str,
        frequency: str,
        indication: str,
        regimen_id: str,
        identity_provenance: str,
        rxcui: str | None,
        synthea_product: str | None,
        states: list[dict[str, Any]],
        discharge_action: str,
        evidence_ids: list[str],
        resident_note: str,
        rationale: str,
        monitoring: str,
        follow_up: str,
        alternatives: list[dict[str, str]] | None = None,
        hospital_only: bool = False,
    ) -> None:
        if discharge_action not in ALLOWED_ACTIONS:
            raise KeyError(discharge_action)
        regimen = regimen_by_id(regimen_id)
        if regimen.dose != dose or regimen.route != route or regimen.frequency != frequency:
            raise ValueError(
                f"{regimen_id} does not match charted {dose} {route} {frequency}"
            )
        self.medications.append(
            {
                "drug": drug,
                "dose": dose,
                "route": route,
                "frequency": frequency,
                "indication": indication,
                "regimen_id": regimen_id,
                "identity_provenance": identity_provenance,
                "regimen_provenance": TERMINOLOGY,
                "rxcui": rxcui,
                "synthea_product": synthea_product,
                "states": states,
                "discharge_action": discharge_action,
                "evidence_ids": evidence_ids,
                "resident_note": resident_note,
                "rationale": rationale,
                "monitoring": monitoring,
                "follow_up": follow_up,
                "acceptable_alternatives": alternatives or [],
                "hospital_only": hospital_only,
            }
        )

    def continue_mapped(
        self,
        mapped: MappedMedication,
        indication: str,
        evidence_ids: list[str],
        rationale: str,
        resident_note: str,
    ) -> None:
        self.medication(
            drug=regimen_by_id(mapped.regimen_id).query,
            dose=mapped.dose,
            route=mapped.route,
            frequency=mapped.frequency,
            indication=indication,
            regimen_id=mapped.regimen_id,
            identity_provenance=SYNTHEA,
            rxcui=mapped.rxcui,
            synthea_product=mapped.display,
            states=[
                {
                    "state": "home",
                    "time_order": 10,
                    "trigger": "recorded outpatient medication",
                    "evidence": evidence_ids[:1] or evidence_ids,
                    "provenance": SYNTHEA,
                },
                {
                    "state": "continued_inpatient",
                    "time_order": 70,
                    "trigger": "indication still present and no new contraindication",
                    "evidence": evidence_ids,
                    "provenance": EPISODE,
                },
            ],
            discharge_action="continue",
            evidence_ids=evidence_ids,
            resident_note=resident_note,
            rationale=rationale,
            monitoring="Routine follow-up. No new intensive monitoring is required for this continuation.",
            follow_up="Review at the scheduled follow-up visit.",
            hospital_only=False,
        )

    def section_text(self, section: str) -> str:
        rows = [item for item in self.facts if item["section"] == section and item["resident_visible"]]
        rows.sort(key=lambda item: int(item["time_order"]))
        return " ".join(str(item["text"]).strip() for item in rows)

    def to_episode(self, case_id: str | None = None) -> dict[str, Any]:
        signature = "|".join(
            f"{item['drug']}:{item['discharge_action']}"
            for item in sorted(self.medications, key=lambda item: str(item["drug"]))
        )
        self.fingerprint["med_signature"] = signature
        resident = self._resident(case_id or "UNASSIGNED")
        reference = self._reference()
        visible = {str(item["fact_id"]) for item in self.facts if item["resident_visible"]}
        return {
            "case_id": case_id,
            "scenario_code": self.scenario_code,
            "scenario_version": "g2-scenarios-v1",
            "variant_id": self.variant_id,
            "eligibility_tier": self.eligibility_tier,
            "fingerprint": self.fingerprint,
            "physiology_expectations": self.physiology_expectations,
            "synthea_patient_id": self.patient.synthea_patient_id,
            "episode_generation_seed": self.episode_seed,
            "facts": self.facts,
            "timeline": self.events,
            "medication_decisions": self.medications,
            "reference_discharge_plan": reference,
            "visible_fact_ids": sorted(visible),
            "source_rxcuis": sorted(self.patient.source_rxcuis()),
            "source_snomed": sorted(self.patient.source_snomed()),
            "control_error_status": "NO INTENTIONAL ERROR",
            "resident": resident,
            "provenance": self._provenance(),
        }

    def _provenance(self) -> dict[str, Any]:
        return {
            "generation_method": "synthea_cliniproof_g2",
            "synthea": {
                "repository": self.synthea_meta["repository"],
                "commit": self.synthea_meta["commit"],
                "version": self.synthea_meta["version"],
                "population_seed": self.synthea_meta["population_seed"],
                "reference_date": self.synthea_meta["reference_date"],
                "fhir_version": self.synthea_meta["fhir_version"],
                "java_version": self.synthea_meta["java_version"],
                "synthetic_patient_id": self.patient.synthea_patient_id,
            },
            "scenario": {"code": self.scenario_code, "version": "g2-scenarios-v1"},
            "episode_generation_seed": self.episode_seed,
            "source_classes": [SYNTHEA, EPISODE, TERMINOLOGY, REFERENCE],
            "generated_at": self.synthea_meta["generated_at"],
            "narrative": "template rendering of structured facts; no language model",
            "use_openai": False,
        }

    def _reference(self) -> dict[str, Any]:
        actions = []
        for med in self.medications:
            actions.append(
                {
                    "medication": med["drug"],
                    "regimen_id": med["regimen_id"],
                    "action": med["discharge_action"],
                    "dose": med["dose"],
                    "route": med["route"],
                    "frequency": med["frequency"],
                    "indication": med["indication"],
                    "rationale": med["rationale"],
                    "resident_visible_evidence": med["evidence_ids"],
                    "monitoring": med["monitoring"],
                    "follow_up": med["follow_up"],
                    "acceptable_alternatives": med["acceptable_alternatives"],
                    "provenance": REFERENCE,
                }
            )
        return {"actions": actions, "provenance": REFERENCE}

    def _resident(self, case_id: str) -> dict[str, Any]:
        history = [
            item["diagnosis"]
            for item in self.diagnoses
            if item["diagnosis_type"] == "past_history"
        ]
        weight_kg = self.patient.weight_kg
        for item in self.weights:
            if item["timepoint"] == "baseline":
                weight_kg = item["weight_kg"]
        hpi = self.section_text("hpi")
        course = self.section_text("course")
        one_liner = (
            f"{self.patient.age_years}-year-old {self.patient.sex_display} with {self.syndrome}"
        )
        meds: list[dict[str, Any]] = []
        counter = 1
        for med in self.medications:
            states = {str(item["state"]) for item in med["states"]}
            if "home" in states:
                meds.append(self._med_row(case_id, counter, med, "home", "home"))
                counter += 1
            inpatient_status = "held" if "held" in states and "restarted" not in states else "active"
            if med["hospital_only"] and inpatient_status == "active":
                inpatient_status = "completed_inpatient_course"
            meds.append(self._med_row(case_id, counter, med, "inpatient", inpatient_status))
            counter += 1
        return {
            "case_id_code": case_id,
            "ClinicalCase": {
                "title": f"{self.scenario_code} {case_id}",
                "case_id_code": case_id,
                "case_status": "candidate",
                "generation_source": "synthetic",
                "one_liner": one_liner,
                "admission_dx": next(
                    (
                        item["diagnosis"]
                        for item in self.diagnoses
                        if item["diagnosis_type"] == "admission"
                    ),
                    self.syndrome,
                ),
                "disposition_status": self.disposition,
                "chief_complaint": self.chief_complaint,
                "patient_name": case_id,
                "patient_age": self.patient.age_years,
                "patient_gender": self.patient.sex_display,
                "ethnicity": None,
                "weight_kg": weight_kg,
                "social_context": "Longitudinal social history was not required for this episode.",
                "is_active": True,
                "difficulty": "standard",
                "specialty": self.specialty,
                "allergies": self.patient.allergies,
                "medical_history": history or self.problems,
                "source_type": "synthea_cliniproof_g2",
                "source_file": None,
                "presentation": {
                    "chief_complaint": self.chief_complaint,
                    "hpi": hpi,
                    "review_of_systems": None,
                    "presenting_symptoms": self.symptoms,
                    "symptom_duration": self.symptom_duration,
                    "symptom_course": self.symptom_course,
                },
                "social_support": {
                    "living_situation": "community",
                    "caregiver_support": None,
                    "transportation": None,
                    "financial_barriers": None,
                    "health_literacy": None,
                    "language_preference": "English",
                    "substance_use": None,
                    "advance_directive": None,
                },
                "discharge_planning": {
                    "disposition": self.disposition,
                    "disposition_detail": None,
                    "transportation_needed": False,
                    "barriers_to_discharge": [],
                    "discharge_readiness": "ready for clinician review of the discharge medication plan",
                    "anticipated_discharge_date": None,
                    "medicaid_pending": None,
                    "home_health_ordered": self.disposition == "home",
                    "dme_needed": [],
                },
            },
            "CaseDiagnosis": [
                {
                    "diagnosis_id": f"DX-{case_id}-{index:03d}",
                    "case_id": case_id,
                    **{
                        key: item[key]
                        for key in (
                            "diagnosis",
                            "diagnosis_type",
                            "status",
                            "context",
                            "provenance",
                        )
                    },
                    "icd10cm": item["icd10cm"],
                    "snomed_code": item["snomed_code"],
                    "code_provenance": item["code_provenance"],
                }
                for index, item in enumerate(self.diagnoses, start=1)
            ],
            "CaseNote": [
                {
                    "note_id": f"NOTE-{case_id}-001",
                    "case_id": case_id,
                    "note_type": "admission",
                    "note_text": hpi,
                    "provenance": EPISODE,
                },
                {
                    "note_id": f"NOTE-{case_id}-002",
                    "case_id": case_id,
                    "note_type": "hospital_course",
                    "note_text": course,
                    "provenance": EPISODE,
                },
            ],
            "CaseVital": [
                {
                    "vital_id": f"VIT-{case_id}-{index:03d}",
                    "case_id": case_id,
                    **item,
                }
                for index, item in enumerate(self.vitals, start=1)
            ],
            "CaseLab": [
                {
                    "lab_id": f"LAB-{case_id}-{index:03d}",
                    "case_id": case_id,
                    "timepoint": item["timepoint"],
                    "test_name": item["test_name"],
                    "loinc_code": item["loinc_code"],
                    "value": item["value"],
                    "value_text": item["value_text"],
                    "unit": item["unit"],
                    "status": "final",
                    "provenance": item["provenance"],
                    "code_provenance": item["code_provenance"],
                }
                for index, item in enumerate(self.labs, start=1)
            ],
            "CaseWeight": [
                {
                    "weight_id": f"WT-{case_id}-{index:03d}",
                    "case_id": case_id,
                    "timepoint": item["timepoint"],
                    "weight_kg": item["weight_kg"],
                    "provenance": item["provenance"],
                }
                for index, item in enumerate(self.weights, start=1)
            ],
            "CaseImaging": [
                {"study_id": f"STUDY-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.imaging, start=1)
            ],
            "CaseProcedure": [
                {"procedure_id": f"PROC-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.procedures, start=1)
            ],
            "CaseConsult": [
                {"consult_id": f"CON-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.consults, start=1)
            ],
            "CaseMicrobiology": [
                {"micro_id": f"MICRO-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.micro, start=1)
            ],
            "CaseMedication": meds,
            "CaseMedicationReconciliation": [
                {"medrec_id": f"REC-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.medrec, start=1)
            ],
            "CaseMonitoring": [
                {"monitoring_id": f"MON-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.monitoring, start=1)
            ],
            "CaseFollowup": [
                {"followup_id": f"FU-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.followup, start=1)
            ],
            "CaseInstruction": [
                {"instruction_id": f"INS-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.instructions, start=1)
            ],
            "CaseIntakeOutput": [
                {"io_id": f"IO-{case_id}-{index:03d}", "case_id": case_id, **item}
                for index, item in enumerate(self.intake, start=1)
            ],
        }

    def _med_row(
        self,
        case_id: str,
        index: int,
        med: dict[str, Any],
        context: str,
        status: str,
    ) -> dict[str, Any]:
        held = status == "held"
        dose = med["dose"]
        frequency = med["frequency"]
        if context == "home" and med.get("home_dose"):
            dose = str(med["home_dose"])
            frequency = str(med["home_frequency"])
        return {
            "medication_id": f"MED-{case_id}-{index:03d}",
            "case_id": case_id,
            "context": context,
            "drug": med["drug"],
            "reported_name": med["drug"],
            "dose": dose,
            "route": med["route"],
            "frequency": frequency,
            "indication": med["indication"],
            "status": status,
            "held_reason": med["resident_note"] if held else None,
            "verification_status": "verified",
            "verification_source": "longitudinal_record_and_inpatient_course",
            "monitoring": None,
            "notes": med["resident_note"],
            "regimen_id": med["regimen_id"],
            "rxcui": med["rxcui"],
            "identity_provenance": med["identity_provenance"],
            "regimen_provenance": med["regimen_provenance"],
            "provenance": med["identity_provenance"],
        }


def net_from_weight(admission_kg: float, discharge_kg: float) -> tuple[int, int]:
    """Return intake and output volumes whose net matches the weight change."""
    delta_ml = int(round((admission_kg - discharge_kg) * 1000))
    intake = 8000
    output = intake + delta_ml
    return intake, output
