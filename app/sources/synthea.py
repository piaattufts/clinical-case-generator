"""Parse a Synthea FHIR R4 transaction bundle into a longitudinal patient.

Only resources that can support discharge-reconciliation eligibility are kept.
The parser does not create inpatient episodes and does not invent codes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

REFERENCE_DATE = date(2026, 10, 8)

KEEP_LOINC = frozenset(
    {
        "2160-0",
        "2823-3",
        "2951-2",
        "718-7",
        "29463-7",
        "8480-6",
        "8462-4",
        "8867-4",
        "8310-5",
        "59408-5",
        "9279-1",
    }
)

SYNTHEA_LONGITUDINAL = "synthea_longitudinal"
RXNORM_SYSTEM = "rxnorm"


@dataclass(frozen=True)
class ConditionFact:
    text: str
    status: str
    snomed_code: str | None
    onset: str | None
    provenance: str = SYNTHEA_LONGITUDINAL


@dataclass(frozen=True)
class MedicationFact:
    display: str
    status: str
    rxcui: str | None
    authored_on: str | None
    synthea_frequency: str | None
    provenance: str = SYNTHEA_LONGITUDINAL


@dataclass(frozen=True)
class ObservationFact:
    loinc_code: str
    display: str
    value: float
    unit: str | None
    effective: str | None
    provenance: str = SYNTHEA_LONGITUDINAL


@dataclass(frozen=True)
class EncounterFact:
    encounter_class: str | None
    text: str
    start: str | None
    provenance: str = SYNTHEA_LONGITUDINAL


@dataclass(frozen=True)
class ProcedureFact:
    text: str
    performed: str | None
    snomed_code: str | None
    provenance: str = SYNTHEA_LONGITUDINAL


@dataclass(frozen=True)
class CarePlanFact:
    text: str
    status: str | None
    provenance: str = SYNTHEA_LONGITUDINAL


@dataclass
class LongitudinalPatient:
    """Study-relevant longitudinal view of one Synthea patient."""

    synthea_patient_id: str
    birth_date: str
    age_years: int
    sex: str
    sex_display: str
    deceased: bool
    weight_kg: float | None
    conditions: list[ConditionFact] = field(default_factory=list)
    medications: list[MedicationFact] = field(default_factory=list)
    observations: list[ObservationFact] = field(default_factory=list)
    encounters: list[EncounterFact] = field(default_factory=list)
    procedures: list[ProcedureFact] = field(default_factory=list)
    careplans: list[CarePlanFact] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)

    def active_condition_text(self) -> list[str]:
        return [item.text for item in self.conditions if item.status == "active" and item.text]

    def condition_blob(self) -> str:
        return " ".join(text.casefold() for text in self.active_condition_text())

    def active_medications(self) -> list[MedicationFact]:
        return [item for item in self.medications if item.status == "active"]

    def source_rxcuis(self) -> set[str]:
        return {item.rxcui for item in self.medications if item.rxcui}

    def source_snomed(self) -> set[str]:
        codes = {item.snomed_code for item in self.conditions if item.snomed_code}
        codes.update(item.snomed_code for item in self.procedures if item.snomed_code)
        return codes

    def latest_lab(self, loinc_code: str, *, unit: str | None = None) -> ObservationFact | None:
        matches = [
            item
            for item in self.observations
            if item.loinc_code == loinc_code and (unit is None or item.unit == unit)
        ]
        if not matches:
            return None
        return matches[-1]


def age_on(birth_date: str, on: date = REFERENCE_DATE) -> int:
    year_text, month_text, day_text = birth_date.split("-", 2)
    born = date(int(year_text), int(month_text), int(day_text))
    return on.year - born.year - ((on.month, on.day) < (born.month, born.day))


def _coding(resource_code: dict[str, Any] | None, system_token: str) -> str | None:
    if not isinstance(resource_code, dict):
        return None
    for coding in resource_code.get("coding") or []:
        if not isinstance(coding, dict):
            continue
        system = str(coding.get("system") or "")
        code = coding.get("code")
        if code and system_token.casefold() in system.casefold():
            return str(code)
    return None


def _code_text(resource_code: dict[str, Any] | None) -> str:
    if not isinstance(resource_code, dict):
        return ""
    text = resource_code.get("text")
    if isinstance(text, str) and text.strip():
        return text.strip()
    for coding in resource_code.get("coding") or []:
        if isinstance(coding, dict) and coding.get("display"):
            return str(coding["display"]).strip()
    return ""


def _status_code(node: dict[str, Any] | None) -> str:
    if not isinstance(node, dict):
        return ""
    for coding in node.get("coding") or []:
        if isinstance(coding, dict) and coding.get("code"):
            return str(coding["code"])
    return ""


def _frequency(dosage: object) -> str | None:
    if not isinstance(dosage, list) or not dosage or not isinstance(dosage[0], dict):
        return None
    repeat = (dosage[0].get("timing") or {}).get("repeat") or {}
    if not isinstance(repeat, dict):
        return None
    frequency = repeat.get("frequency")
    period = repeat.get("period")
    unit = repeat.get("periodUnit")
    if frequency == 1 and period == 1 and unit == "d":
        return "once daily"
    if frequency == 2 and period == 1 and unit == "d":
        return "twice daily"
    if frequency == 1 and period == 12 and unit == "h":
        return "every 12 hours"
    return None


def parse_bundle(payload: dict[str, Any], *, on: date = REFERENCE_DATE) -> LongitudinalPatient:
    """Parse one Synthea bundle. Raises ValueError if the patient resource is absent."""
    entries = payload.get("entry")
    if payload.get("resourceType") != "Bundle" or not isinstance(entries, list):
        raise ValueError("Synthea export is not a FHIR Bundle")
    patient_resource: dict[str, Any] | None = None
    conditions: list[ConditionFact] = []
    medications: list[MedicationFact] = []
    observations: dict[str, ObservationFact] = {}
    encounters: list[EncounterFact] = []
    procedures: list[ProcedureFact] = []
    careplans: list[CarePlanFact] = []
    allergies: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        resource = entry.get("resource")
        if not isinstance(resource, dict):
            continue
        kind = resource.get("resourceType")
        if kind == "Patient" and patient_resource is None:
            patient_resource = resource
        elif kind == "Condition":
            text = _code_text(resource.get("code"))
            if not text:
                continue
            conditions.append(
                ConditionFact(
                    text=text,
                    status=_status_code(resource.get("clinicalStatus")) or "unknown",
                    snomed_code=_coding(resource.get("code"), "snomed"),
                    onset=resource.get("onsetDateTime")
                    if isinstance(resource.get("onsetDateTime"), str)
                    else None,
                )
            )
        elif kind == "MedicationRequest":
            concept = resource.get("medicationCodeableConcept")
            display = _code_text(concept if isinstance(concept, dict) else None)
            if not display:
                continue
            medications.append(
                MedicationFact(
                    display=display,
                    status=str(resource.get("status") or ""),
                    rxcui=_coding(concept if isinstance(concept, dict) else None, RXNORM_SYSTEM),
                    authored_on=resource.get("authoredOn")
                    if isinstance(resource.get("authoredOn"), str)
                    else None,
                    synthea_frequency=_frequency(resource.get("dosageInstruction")),
                )
            )
        elif kind == "MedicationStatement":
            concept = resource.get("medicationCodeableConcept")
            display = _code_text(concept if isinstance(concept, dict) else None)
            if not display:
                continue
            medications.append(
                MedicationFact(
                    display=display,
                    status=str(resource.get("status") or ""),
                    rxcui=_coding(concept if isinstance(concept, dict) else None, RXNORM_SYSTEM),
                    authored_on=None,
                    synthea_frequency=_frequency(resource.get("dosage")),
                )
            )
        elif kind == "Observation":
            code = resource.get("code")
            loinc = _coding(code if isinstance(code, dict) else None, "loinc")
            quantity = resource.get("valueQuantity")
            if loinc not in KEEP_LOINC or not isinstance(quantity, dict):
                continue
            value = quantity.get("value")
            if not isinstance(value, int | float):
                continue
            effective = resource.get("effectiveDateTime")
            observations[loinc] = ObservationFact(
                loinc_code=loinc,
                display=_code_text(code if isinstance(code, dict) else None) or loinc,
                value=float(value),
                unit=str(quantity["unit"]) if quantity.get("unit") else None,
                effective=effective if isinstance(effective, str) else None,
            )
        elif kind == "Encounter":
            raw_period = resource.get("period")
            period = raw_period if isinstance(raw_period, dict) else {}
            raw_class = resource.get("class")
            raw_type = resource.get("type")
            type_text = ""
            if isinstance(raw_type, list) and raw_type and isinstance(raw_type[0], dict):
                type_text = _code_text(raw_type[0])
            start = period.get("start")
            encounters.append(
                EncounterFact(
                    encounter_class=raw_class.get("code")
                    if isinstance(raw_class, dict)
                    else None,
                    text=type_text,
                    start=start if isinstance(start, str) else None,
                )
            )
        elif kind == "Procedure":
            text = _code_text(resource.get("code"))
            if not text:
                continue
            performed_value = resource.get("performedDateTime")
            performed: str | None
            if isinstance(performed_value, str):
                performed = performed_value
            else:
                raw_performed = resource.get("performedPeriod")
                performed_period = raw_performed if isinstance(raw_performed, dict) else {}
                start = performed_period.get("start")
                performed = start if isinstance(start, str) else None
            procedures.append(
                ProcedureFact(
                    text=text,
                    performed=performed,
                    snomed_code=_coding(resource.get("code"), "snomed"),
                )
            )
        elif kind == "CarePlan":
            careplans.append(
                CarePlanFact(
                    text=_code_text(None)
                    or _careplan_text(resource),
                    status=str(resource.get("status") or "") or None,
                )
            )
        elif kind == "AllergyIntolerance":
            text = _code_text(resource.get("code"))
            if text:
                allergies.append(text)
    if patient_resource is None:
        raise ValueError("Bundle has no Patient resource")
    birth = patient_resource.get("birthDate")
    if not isinstance(birth, str):
        raise ValueError("Patient has no birthDate")
    gender = str(patient_resource.get("gender") or "unknown")
    sex_display = {"male": "Male", "female": "Female"}.get(gender, gender)
    deceased = bool(
        patient_resource.get("deceasedDateTime") or patient_resource.get("deceasedBoolean") is True
    )
    weight = observations.get("29463-7")
    weight_kg = None
    if weight is not None and weight.unit in {None, "kg"} and 30 <= weight.value <= 250:
        weight_kg = weight.value
    encounters.sort(key=lambda item: item.start or "")
    procedures.sort(key=lambda item: item.performed or "")
    return LongitudinalPatient(
        synthea_patient_id=str(patient_resource.get("id") or ""),
        birth_date=birth,
        age_years=age_on(birth, on),
        sex=gender,
        sex_display=sex_display,
        deceased=deceased,
        weight_kg=weight_kg,
        conditions=conditions,
        medications=_dedupe_meds(medications),
        observations=list(observations.values()),
        encounters=encounters[-6:],
        procedures=procedures[-8:],
        careplans=careplans[:6],
        allergies=allergies,
    )


def _careplan_text(resource: dict[str, Any]) -> str:
    for category in resource.get("category") or []:
        if isinstance(category, dict):
            text = _code_text(category)
            if text:
                return text
    return ""


def _dedupe_meds(medications: list[MedicationFact]) -> list[MedicationFact]:
    seen: set[tuple[str, str]] = set()
    kept: list[MedicationFact] = []
    for item in medications:
        key = (item.status, item.display.casefold())
        if key in seen:
            continue
        seen.add(key)
        kept.append(item)
    return kept
