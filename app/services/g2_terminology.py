"""Verified terminology used by Generation 2 episode facts.

Codes in this module were checked against NLM Clinical Tables LOINC and
ICD-10-CM searches. RxNorm product codes are copied from Synthea bundles and
are not listed here. A code that is not in this table and not copied from the
source bundle is rejected by the audit.
"""

from __future__ import annotations

from app.services.medication_regimens import (
    ClinicalRegimen,
    load_regimens,
    matching_regimens,
    token_in,
)

LOINC: dict[str, tuple[str, str]] = {
    "2160-0": ("Creatinine [Mass/volume] in Serum or Plasma", "mg/dL"),
    "2823-3": ("Potassium [Moles/volume] in Serum or Plasma", "mmol/L"),
    "2951-2": ("Sodium [Moles/volume] in Serum or Plasma", "mmol/L"),
    "718-7": ("Hemoglobin [Mass/volume] in Blood", "g/dL"),
    "6690-2": ("Leukocytes [#/volume] in Blood by Automated count", "10*3/uL"),
    "6301-6": ("INR in Platelet poor plasma by Coagulation assay", "[INR]"),
    "30934-4": ("Natriuretic peptide B [Mass/volume] in Serum or Plasma", "pg/mL"),
    "777-3": ("Platelets [#/volume] in Blood by Automated count", "10*3/uL"),
    "10839-9": ("Troponin I.cardiac [Mass/volume] in Serum or Plasma", "ng/mL"),
    "30246-3": (
        "Cytomegalovirus DNA [Presence] in Serum or Plasma by NAA with probe detection",
        "",
    ),
    "600-7": ("Bacteria identified in Blood by Culture", ""),
    "2345-7": ("Glucose [Mass/volume] in Serum or Plasma", "mg/dL"),
}

ICD10: dict[str, str] = {
    "I50.23": "Acute on chronic systolic (congestive) heart failure",
    "I50.21": "Acute systolic (congestive) heart failure",
    "I50.9": "Heart failure, unspecified",
    "I48.91": "Unspecified atrial fibrillation",
    "I48.0": "Paroxysmal atrial fibrillation",
    "I33.0": "Acute and subacute infective endocarditis",
    "B25.8": "Other cytomegaloviral diseases",
    "B25.9": "Cytomegaloviral disease, unspecified",
    "K92.2": "Gastrointestinal hemorrhage, unspecified",
    "K25.4": "Chronic or unspecified gastric ulcer with hemorrhage",
    "K26.4": "Chronic or unspecified duodenal ulcer with hemorrhage",
    "K57.31": "Diverticulosis of large intestine without perforation or abscess with bleeding",
    "K92.0": "Hematemesis",
    "K92.1": "Melena",
    "K20.90": "Esophagitis, unspecified without bleeding",
    "S72.001A": (
        "Fracture of unspecified part of neck of right femur, initial encounter "
        "for closed fracture"
    ),
    "Z94.0": "Kidney transplant status",
    "F05": "Delirium due to known physiological condition",
    "N17.9": "Acute kidney failure, unspecified",
    "E87.1": "Hypo-osmolality and hyponatremia",
    "E87.6": "Hypokalemia",
    "E86.0": "Dehydration",
    "I10": "Essential (primary) hypertension",
    "E11.9": "Type 2 diabetes mellitus without complications",
    "E78.5": "Hyperlipidemia, unspecified",
    "J18.9": "Pneumonia, unspecified organism",
    "N39.0": "Urinary tract infection, site not specified",
    "D62": "Acute posthemorrhagic anemia",
    "Z79.01": "Long term (current) use of anticoagulants",
    "Z95.2": "Presence of prosthetic heart valve",
    "R41.0": "Disorientation, unspecified",
}

UCUM_UNITS = frozenset(
    {
        "mg/dL",
        "mmol/L",
        "g/dL",
        "pg/mL",
        "ng/mL",
        "10*3/uL",
        "[INR]",
        "kg",
    }
)

ALLOWED_ACTIONS = frozenset(
    {"continue", "stop", "restart", "hold", "dose_change", "new_start"}
)

TIME_RANK = {
    "baseline": 0,
    "admission": 1,
    "hospital_day_1": 2,
    "peak": 3,
    "nadir": 3,
    "intermediate": 4,
    "hospital_day_3": 4,
    "hospital_day_4": 5,
    "pre_discharge": 6,
    "discharge": 7,
}


def regimen_by_id(regimen_id: str) -> ClinicalRegimen:
    for item in load_regimens():
        if item.id == regimen_id:
            return item
    raise KeyError(f"curated regimen {regimen_id} is not in medication_regimens.json")


def regimen_for_product(display: str) -> ClinicalRegimen | None:
    """Match a Synthea product only when a curated dose is the labeled strength.

    Combination products are skipped. A regimen whose milligram dose is not
    present in the product name is not applied, so a 100 MG tablet is not
    charted as a 25 MG regimen.
    """
    if "/" in display:
        return None
    hits = [
        item
        for item in matching_regimens(display)
        if token_in(item.dose, display) or item.dose.casefold() in {"individualized"}
    ]
    if not hits:
        return None
    hits.sort(key=lambda item: (item.selection_priority, -len(item.dose), item.id))
    return hits[0]
