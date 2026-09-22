"""External source clients.

Phase 2 talks to RxNorm, LOINC, official UCUM essence XML, ICD-10-CM,
NLM conditions, NLM HPO, DailyMed, and RxClass. It does not invent identifiers and
does not send MIMIC or other patient rows to OpenAI.
"""

from app.sources.conditions import ConditionsClient
from app.sources.dailymed import DailyMedClient
from app.sources.exceptions import (
    CaseValidationError,
    FrozenValidationCaseError,
    ReferenceResolutionError,
    SourceError,
    SourceHttpError,
    SourceNotConfigured,
    SourceParseError,
    SourceUnavailable,
)
from app.sources.hpo import HpoClient
from app.sources.icd10cm import Icd10CmClient
from app.sources.loinc import LoincClient
from app.sources.rxclass import RxClassClient
from app.sources.rxnorm import RxNormClient
from app.sources.ucum import UcumClient

__all__ = [
    "CaseValidationError",
    "ConditionsClient",
    "DailyMedClient",
    "FrozenValidationCaseError",
    "HpoClient",
    "Icd10CmClient",
    "LoincClient",
    "ReferenceResolutionError",
    "RxClassClient",
    "RxNormClient",
    "SourceError",
    "SourceHttpError",
    "SourceNotConfigured",
    "SourceParseError",
    "SourceUnavailable",
    "UcumClient",
]
