"""Lookups for synthetic cases. Terminology identifiers are not created here."""

from __future__ import annotations

import uuid

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models.cases import (
    CaseAnswerKey,
    CaseDiagnosis,
    CaseLab,
    CaseMedication,
    CaseSymptom,
    ClinicalCase,
)
from app.models.generation import (
    CaseBlueprint,
    CaseGenerationRun,
    CaseMedicationPlan,
    ValidationBatchCase,
)
from app.sources.exceptions import FrozenValidationCaseError
from app.utils.identifiers import CASE_CODE_RE


def get_case_by_id(session: Session, case_id: uuid.UUID) -> ClinicalCase | None:
    return session.get(ClinicalCase, case_id)


def get_case_by_code(session: Session, case_id_code: str) -> ClinicalCase | None:
    return session.scalar(select(ClinicalCase).where(ClinicalCase.case_id_code == case_id_code))


def list_cases(session: Session) -> list[ClinicalCase]:
    rows = session.scalars(select(ClinicalCase).order_by(ClinicalCase.case_id_code)).all()
    return list(rows)


def list_medications_for_case(session: Session, case_id: uuid.UUID) -> list[CaseMedication]:
    rows = session.scalars(
        select(CaseMedication)
        .where(CaseMedication.case_id == case_id)
        .order_by(CaseMedication.context.nulls_last(), CaseMedication.drug.nulls_last())
    ).all()
    return list(rows)


def list_diagnoses_for_case(session: Session, case_id: uuid.UUID) -> list[CaseDiagnosis]:
    rows = session.scalars(
        select(CaseDiagnosis)
        .where(CaseDiagnosis.case_id == case_id)
        .order_by(CaseDiagnosis.diagnosis_id.nulls_last())
    ).all()
    return list(rows)


def list_labs_for_case(session: Session, case_id: uuid.UUID) -> list[CaseLab]:
    rows = session.scalars(
        select(CaseLab).where(CaseLab.case_id == case_id).order_by(CaseLab.lab_id.nulls_last())
    ).all()
    return list(rows)


def list_symptoms_for_case(session: Session, case_id: uuid.UUID) -> list[CaseSymptom]:
    rows = session.scalars(
        select(CaseSymptom)
        .where(CaseSymptom.case_id == case_id)
        .order_by(CaseSymptom.symptom_id.nulls_last())
    ).all()
    return list(rows)


def list_plans_for_case(session: Session, case_id: uuid.UUID) -> list[CaseMedicationPlan]:
    rows = session.scalars(
        select(CaseMedicationPlan)
        .where(CaseMedicationPlan.case_id == case_id)
        .order_by(CaseMedicationPlan.plan_id.nulls_last())
    ).all()
    return list(rows)


def list_answer_keys_for_case(session: Session, case_id: uuid.UUID) -> list[CaseAnswerKey]:
    rows = session.scalars(
        select(CaseAnswerKey)
        .where(CaseAnswerKey.case_id == case_id)
        .order_by(CaseAnswerKey.answer_id.nulls_last())
    ).all()
    return list(rows)


def next_case_sequence(session: Session) -> int:
    codes = session.scalars(select(ClinicalCase.case_id_code)).all()
    highest = 0
    for code in codes:
        if CASE_CODE_RE.fullmatch(code) is None:
            continue
        highest = max(highest, int(code.split("-")[1]))
    return highest + 1


def get_frozen_case_for_clinical_id(
    session: Session, case_id: uuid.UUID
) -> ValidationBatchCase | None:
    return session.scalar(
        select(ValidationBatchCase).where(ValidationBatchCase.case_id == case_id)
    )


def get_frozen_case_by_validation_id(
    session: Session, validation_case_id: str
) -> ValidationBatchCase | None:
    return session.scalar(
        select(ValidationBatchCase).where(
            ValidationBatchCase.validation_case_id == validation_case_id
        )
    )


def list_frozen_batch(session: Session, batch_code: str) -> list[ValidationBatchCase]:
    rows = session.scalars(
        select(ValidationBatchCase)
        .where(ValidationBatchCase.batch_code == batch_code)
        .order_by(ValidationBatchCase.validation_case_id)
    ).all()
    return list(rows)


def delete_case_graph(session: Session, case: ClinicalCase) -> None:
    """Remove a case, generation runs, plans, and associated blueprints.

    Child case rows cascade from clinical_cases. Generation runs reference
    blueprints with ON DELETE RESTRICT, so runs are removed first. Deterministic
    blueprint and run business ids for this case code are also cleared so a
    later generate of SYN-000001 can reuse BP-SYN000001-001.
    """
    frozen = get_frozen_case_for_clinical_id(session, case.id)
    if frozen is not None and frozen.immutable:
        raise FrozenValidationCaseError(
            frozen.validation_case_id,
            f"underlying case {case.case_id_code} is frozen",
        )
    compact = _compact_case_token(case.case_id_code)
    blueprint_ids = list(
        session.scalars(
            select(CaseGenerationRun.blueprint_id).where(CaseGenerationRun.case_id == case.id)
        )
    )
    session.execute(delete(CaseGenerationRun).where(CaseGenerationRun.case_id == case.id))
    if compact is not None:
        extra_run_blueprints = list(
            session.scalars(
                select(CaseGenerationRun.blueprint_id).where(
                    CaseGenerationRun.run_id.like(f"RUN-{compact}-%")
                )
            )
        )
        blueprint_ids.extend(extra_run_blueprints)
        session.execute(
            delete(CaseGenerationRun).where(CaseGenerationRun.run_id.like(f"RUN-{compact}-%"))
        )
    session.execute(delete(CaseMedicationPlan).where(CaseMedicationPlan.case_id == case.id))
    session.delete(case)
    session.flush()
    _delete_blueprints(session, blueprint_ids, compact)
    session.expire_all()


def delete_generation_artifacts_for_case_code(session: Session, case_id_code: str) -> None:
    """Remove leftover runs and blueprints for a case code when no case row exists."""
    compact = _compact_case_token(case_id_code)
    if compact is None:
        return
    blueprint_ids = list(
        session.scalars(
            select(CaseGenerationRun.blueprint_id).where(
                CaseGenerationRun.run_id.like(f"RUN-{compact}-%")
            )
        )
    )
    session.execute(
        delete(CaseGenerationRun).where(CaseGenerationRun.run_id.like(f"RUN-{compact}-%"))
    )
    session.flush()
    _delete_blueprints(session, blueprint_ids, compact)


def _delete_blueprints(
    session: Session, blueprint_ids: list[uuid.UUID], compact: str | None
) -> None:
    ids = list(dict.fromkeys(blueprint_ids))
    if compact is not None:
        named = list(
            session.scalars(
                select(CaseBlueprint.id).where(CaseBlueprint.blueprint_id.like(f"BP-{compact}-%"))
            )
        )
        ids.extend(item for item in named if item not in ids)
    if ids:
        session.execute(delete(CaseBlueprint).where(CaseBlueprint.id.in_(ids)))
        session.flush()


def _compact_case_token(case_id_code: str) -> str | None:
    if CASE_CODE_RE.fullmatch(case_id_code) is None:
        return None
    return "SYN" + case_id_code.removeprefix("SYN-")


def count_blueprints(session: Session) -> int:
    return int(session.scalar(select(func.count()).select_from(CaseBlueprint)) or 0)
