"""Clinical-structure constraints for synthetic cases.

These checks encode implemented chart-coherence rules: lab value/unit coupling,
symptom versus diagnosis granularity, medication route/form compatibility,
indication-to-problem mapping, and resident-facing leak phrases. They do not
establish clinical truth or replace clinician validation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from app.models.reference import RefLabTest, RefMedication, RefSymptom


@dataclass(frozen=True)
class LabSpec:
    """One internally coherent numeric representation for a laboratory analyte."""

    name: str
    keywords: tuple[str, ...]
    preferred_units: tuple[str, ...]
    conventional_unit: str
    conventional_low: float
    conventional_high: float
    molar_unit: str | None = None
    conventional_to_molar: float | None = None
    exclude_keywords: tuple[str, ...] = ()


LAB_SPECS: tuple[LabSpec, ...] = (
    LabSpec(
        name="creatinine",
        keywords=("creatinine",),
        preferred_units=("mg/dL", "mg/dl"),
        conventional_unit="mg/dL",
        conventional_low=0.6,
        conventional_high=3.5,
        molar_unit="umol/L",
        conventional_to_molar=88.4,
        exclude_keywords=("clearance", "ratio", "urine", "dialysis"),
    ),
    LabSpec(
        name="glucose",
        keywords=("glucose",),
        preferred_units=("mg/dL", "mg/dl"),
        conventional_unit="mg/dL",
        conventional_low=60.0,
        conventional_high=450.0,
        molar_unit="mmol/L",
        conventional_to_molar=1.0 / 18.0182,
        exclude_keywords=("csf", "tolerance", "challenge"),
    ),
    LabSpec(
        name="potassium",
        keywords=("potassium",),
        preferred_units=("mmol/L", "meq/L", "mmol/l"),
        conventional_unit="mmol/L",
        conventional_low=2.8,
        conventional_high=6.2,
    ),
    LabSpec(
        name="sodium",
        keywords=("sodium",),
        preferred_units=("mmol/L", "meq/L", "mmol/l"),
        conventional_unit="mmol/L",
        conventional_low=120.0,
        conventional_high=155.0,
    ),
    LabSpec(
        name="inr",
        keywords=("inr", "international normalized"),
        preferred_units=("{INR}", "1", ""),
        conventional_unit="{INR}",
        conventional_low=0.8,
        conventional_high=4.5,
    ),
    LabSpec(
        name="hemoglobin",
        keywords=("hemoglobin", "haemoglobin"),
        preferred_units=("g/dL", "g/dl"),
        conventional_unit="g/dL",
        conventional_low=6.5,
        conventional_high=17.0,
        exclude_keywords=("a1c", "a2", "fraction", "fetal", "ratio"),
    ),
    LabSpec(
        name="natriuretic peptide",
        keywords=("natriuretic", "bnp", "nt-probnp"),
        preferred_units=("pg/mL", "ng/L"),
        conventional_unit="pg/mL",
        conventional_low=10.0,
        conventional_high=5000.0,
    ),
)

SYMPTOM_DISEASE_MARKERS = (
    "syndrome",
    "disease",
    "disorder",
    "angina pectoris",
    "chronic fatigue",
    "myalgic encephalomyelitis",
    "heart failure",
    "pneumonia",
    "diabetes mellitus",
    "hypertension",
    "endocarditis",
    "atrial fibrillation",
)

INDICATION_BY_QUERY: dict[str, str] = {
    "lisinopril": "hypertension",
    "enalapril": "hypertension",
    "amlodipine": "hypertension",
    "hydrochlorothiazide": "hypertension",
    "furosemide": "heart failure",
    "spironolactone": "heart failure",
    "metoprolol": "heart failure",
    "carvedilol": "heart failure",
    "atorvastatin": "hyperlipidemia",
    "metformin": "type 2 diabetes mellitus",
    "warfarin": "atrial fibrillation",
    "apixaban": "atrial fibrillation",
    "azithromycin": "pneumonia",
    "pantoprazole": "gastro-esophageal reflux",
    "ceftriaxone": "endocarditis",
    "tacrolimus": "kidney transplant",
    "mycophenolate mofetil": "kidney transplant",
    "valganciclovir": "cytomegaloviral",
    "enoxaparin": "atrial fibrillation",
}

PARENTERAL_QUERIES = frozenset({"ceftriaxone", "enoxaparin", "vancomycin"})
INHALED_QUERIES = frozenset({"albuterol"})

ORAL_FORM_MARKERS = ("tablet", "capsule", "oral solution", "oral suspension", "chewable")
INJECTION_FORM_MARKERS = (
    "injection",
    "injectable",
    "intravenous",
    "intramuscular",
    "iv ",
    "prefilled syringe",
)
INHALATION_FORM_MARKERS = ("inhalation", "inhaler", "nebulizer", "aerosol", "powder for inhalation")
TOPICAL_FORM_MARKERS = ("cream", "ointment", "gel", "topical", "patch")

ORAL_ROUTES = frozenset({"oral", "po", "by mouth", "enteral"})
PARENTAL_ROUTES = frozenset(
    {
        "intravenous",
        "iv",
        "i.v.",
        "intramuscular",
        "im",
        "i.m.",
        "subcutaneous",
        "sq",
        "sc",
        "parenteral",
    }
)
INHALED_ROUTES = frozenset({"inhaled", "inhalation", "nebulized", "respiratory"})
TOPICAL_ROUTES = frozenset({"topical", "transdermal", "cutaneous"})

TABLET_DOSE_MARKERS = ("tablet", "capsule", "caplet")

RESIDENT_LEAK_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bclean case\b",
        r"\bclean discharge plan\b",
        r"\bclean list\b",
        r"\bplanted error\b",
        r"\bplanted\b",
        r"\bseed document\b",
        r"\bseed-derived\b",
        r"\bsoftware rules?\b",
        r"\bunsupported dosing rule\b",
        r"\bnot encoded as software\b",
        r"\bcase generator\b",
        r"\bgenerator_version\b",
        r"\bgenerator_name\b",
        r"\btarget medication\b",
        r"\bprofile id\b",
        r"\banswer key\b",
        r"\berror categor(?:y|ies)\b",
        r"\bassessment target\b",
        r"\binvestigator\b",
        r"\bblueprint\b",
        r"\bgeneration_strategy\b",
        r"\bclinical profile\b",
        r"\bis_error_target\b",
        r"\bsynthetic_model_generated\b",
        r"\bsource-backed inpatient therapy\b",
    )
)


def lab_blob(lab: RefLabTest | None, extra: str = "") -> str:
    if lab is None:
        return extra.casefold()
    parts = [
        lab.long_common_name,
        lab.short_name,
        lab.component,
        lab.loinc_code,
        extra,
    ]
    return " ".join(part for part in parts if part).casefold()


def spec_for_lab(lab: RefLabTest | None, extra: str = "") -> LabSpec | None:
    blob = lab_blob(lab, extra)
    for spec in LAB_SPECS:
        if any(token in blob for token in spec.exclude_keywords):
            continue
        if any(token in blob for token in spec.keywords):
            return spec
    return None


def normalize_unit(unit: str | None) -> str:
    if not unit:
        return ""
    text = unit.strip()
    replacements = {
        "mg/dl": "mg/dL",
        "g/dl": "g/dL",
        "mmol/l": "mmol/L",
        "umol/l": "umol/L",
        "µmol/l": "umol/L",
        "meq/l": "mmol/L",
        "pg/ml": "pg/mL",
        "ng/l": "ng/L",
    }
    return replacements.get(text.casefold(), text)


def preferred_lab_unit(lab: RefLabTest) -> str | None:
    examples = [normalize_unit(str(item)) for item in (lab.example_ucum_units or []) if item]
    spec = spec_for_lab(lab)
    if spec is None:
        return examples[0] if examples else None
    preferred = {item.casefold() for item in spec.preferred_units if item}
    for unit in examples:
        if unit.casefold() in preferred:
            return unit
    if spec.molar_unit:
        for unit in examples:
            if unit.casefold() == spec.molar_unit.casefold():
                return unit
    return examples[0] if examples else spec.conventional_unit


def convert_conventional(spec: LabSpec, conventional_value: float, unit: str | None) -> float:
    actual = normalize_unit(unit)
    if not actual or actual.casefold() in {item.casefold() for item in spec.preferred_units}:
        return conventional_value
    if (
        spec.molar_unit
        and spec.conventional_to_molar is not None
        and actual.casefold() == spec.molar_unit.casefold()
    ):
        return round(conventional_value * spec.conventional_to_molar, 1)
    return conventional_value


def lab_value_in_range(value: float, unit: str | None, spec: LabSpec) -> bool:
    actual = normalize_unit(unit)
    low = spec.conventional_low
    high = spec.conventional_high
    if (
        spec.molar_unit
        and spec.conventional_to_molar is not None
        and actual.casefold() == spec.molar_unit.casefold()
    ):
        low *= spec.conventional_to_molar
        high *= spec.conventional_to_molar
    return low <= value <= high


def lab_unit_rank(lab_like: Any, query: str) -> int:
    spec = None
    for item in LAB_SPECS:
        if any(token in query.casefold() for token in item.keywords):
            spec = item
            break
    if spec is None:
        return 1
    units = []
    if hasattr(lab_like, "example_ucum_units"):
        units = [normalize_unit(str(part)) for part in (lab_like.example_ucum_units or [])]
    preferred = {item.casefold() for item in spec.preferred_units if item}
    if any(unit.casefold() in preferred for unit in units):
        return 0
    return 1


def implausible_lab_errors(
    test_name: str | None, value: float | None, unit: str | None
) -> list[str]:
    if value is None:
        return []
    spec = spec_for_lab(None, extra=test_name or "")
    if spec is None:
        return []
    if not lab_value_in_range(float(value), unit, spec):
        return [
            f"{spec.name} value {value} {normalize_unit(unit) or '(no unit)'} is not coherent "
            f"with the generation range for that unit"
        ]
    return []


def is_symptom_level_concept(name: str | None, query: str) -> bool:
    text = (name or "").strip()
    if not text:
        return False
    lowered = text.casefold()
    needle = query.casefold().strip()
    if not needle:
        return False
    if any(marker in lowered for marker in SYMPTOM_DISEASE_MARKERS) and lowered != needle:
        return False
    return needle in lowered


def symptom_rank_key(item: RefSymptom, query: str) -> tuple[int, int, str, str]:
    name = item.preferred_name or ""
    exact = 0 if name.casefold() == query.casefold() else 1
    disease = 0 if is_symptom_level_concept(name, query) else 1
    return (disease, exact, name, str(item.id))


def medication_form_blob(medication: RefMedication) -> str:
    return " ".join(
        part
        for part in (
            medication.dose_form,
            medication.concept_name,
            medication.generic_name,
            medication.route,
        )
        if part
    ).casefold()


def inferred_route(medication: RefMedication, query: str | None = None) -> str:
    stored = (medication.route or "").strip()
    blob = medication_form_blob(medication)
    needle = (query or medication.ingredient or medication.generic_name or "").casefold()
    if any(marker in blob for marker in INJECTION_FORM_MARKERS):
        if "intramuscular" in blob or "im " in blob:
            return "intramuscular"
        if "subcutaneous" in blob or "sq" in blob:
            return "subcutaneous"
        return stored if stored.casefold() in PARENTAL_ROUTES else "intravenous"
    if any(marker in blob for marker in INHALATION_FORM_MARKERS):
        return "inhaled"
    if any(marker in blob for marker in TOPICAL_FORM_MARKERS):
        return "topical"
    if any(marker in blob for marker in ORAL_FORM_MARKERS):
        return stored if stored.casefold() in ORAL_ROUTES else "oral"
    if stored:
        return stored
    if needle in PARENTERAL_QUERIES:
        return "intravenous"
    if needle in INHALED_QUERIES:
        return "inhaled"
    return "oral"


def route_compatible_with_form(route: str | None, medication: RefMedication) -> bool:
    blob = medication_form_blob(medication)
    actual = (route or "").casefold().strip()
    if not actual:
        return True
    if any(marker in blob for marker in INJECTION_FORM_MARKERS):
        return actual in PARENTAL_ROUTES
    if any(marker in blob for marker in INHALATION_FORM_MARKERS):
        return actual in INHALED_ROUTES
    if any(marker in blob for marker in TOPICAL_FORM_MARKERS):
        return actual in TOPICAL_ROUTES
    if any(marker in blob for marker in ORAL_FORM_MARKERS):
        return actual in ORAL_ROUTES
    return True


def formulation_preference_rank_blob(blob: str, query: str) -> int:
    lowered = blob.casefold()
    needle = query.casefold().strip()
    if needle in PARENTERAL_QUERIES or "injection" in needle or needle == "iv":
        return 0 if any(marker in lowered for marker in INJECTION_FORM_MARKERS) else 2
    if needle in INHALED_QUERIES or "inhal" in needle:
        return 0 if any(marker in lowered for marker in INHALATION_FORM_MARKERS) else 2
    if any(marker in lowered for marker in ("tablet", "capsule")):
        return 0
    if any(marker in lowered for marker in INJECTION_FORM_MARKERS):
        return 2
    return 1


def formulation_preference_rank(medication: RefMedication, query: str) -> int:
    return formulation_preference_rank_blob(medication_form_blob(medication), query)


def synthetic_dose_for(medication: RefMedication) -> str:
    strength = (medication.strength or "").strip()
    blob = medication_form_blob(medication)
    if strength:
        return strength
    if any(marker in blob for marker in INJECTION_FORM_MARKERS):
        return "as labeled"
    if any(marker in blob for marker in INHALATION_FORM_MARKERS):
        return "1 inhalation"
    if any(marker in blob for marker in ("solution", "suspension")):
        return "as labeled"
    return "1 tablet"


def dose_compatible_with_form(dose: str | None, medication: RefMedication) -> bool:
    text = (dose or "").casefold()
    blob = medication_form_blob(medication)
    if "tablet" in text and any(marker in blob for marker in INJECTION_FORM_MARKERS):
        return False
    if "tablet" in text and any(marker in blob for marker in INHALATION_FORM_MARKERS):
        return False
    if (
        "tablet" in text
        and "solution" in blob
        and not any(marker in blob for marker in TABLET_DOSE_MARKERS)
    ):
        return False
    return True


def indication_query_for(medication_query: str) -> str | None:
    return INDICATION_BY_QUERY.get(medication_query.casefold().strip())


def indication_matches_problems(indication: str | None, problem_names: list[str]) -> bool:
    text = (indication or "").casefold()
    if not text:
        return False
    for name in problem_names:
        if not name:
            continue
        lowered = name.casefold()
        if lowered in text or text in lowered:
            return True
        tokens = [part for part in re.split(r"[^a-z0-9]+", lowered) if len(part) > 3]
        if tokens and all(token in text for token in tokens[:2]):
            return True
    return False


def resident_leak_hits(text: str) -> list[str]:
    found: list[str] = []
    for pattern in RESIDENT_LEAK_PATTERNS:
        match = pattern.search(text)
        if match is not None:
            found.append(match.group(0))
    return found
