"""Lookups for synthetic cases. Phase 1 does not create cases."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cases import CaseMedication, ClinicalCase


def get_case_by_id(session: Session, case_id: uuid.UUID) -> ClinicalCase | None:
    return session.get(ClinicalCase, case_id)


def get_case_by_code(session: Session, case_id_code: str) -> ClinicalCase | None:
    return session.scalar(select(ClinicalCase).where(ClinicalCase.case_id_code == case_id_code))


def list_medications_for_case(session: Session, case_id: uuid.UUID) -> list[CaseMedication]:
    rows = session.scalars(
        select(CaseMedication).where(CaseMedication.case_id == case_id)
    ).all()
    return list(rows)
