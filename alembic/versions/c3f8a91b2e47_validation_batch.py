"""validation batch freeze table

Revision ID: c3f8a91b2e47
Revises: 7b9e4c21d6a0
Create Date: 2026-09-22 00:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c3f8a91b2e47"
down_revision: str | None = "7b9e4c21d6a0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "validation_batch_cases",
        sa.Column("validation_case_id", sa.String(length=16), nullable=False),
        sa.Column("batch_code", sa.String(length=64), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("scenario_code", sa.String(length=64), nullable=False),
        sa.Column("master_seed", sa.Integer(), nullable=False),
        sa.Column("case_seed", sa.String(length=128), nullable=False),
        sa.Column("is_clean_control", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("error_category", sa.String(length=64), nullable=True),
        sa.Column("generator_version", sa.String(length=32), nullable=True),
        sa.Column(
            "reference_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("rule_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("clean_validation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("final_validation", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("clean_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("resident_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("answer_key_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "frozen_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("immutable", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.CheckConstraint(
            "validation_case_id ~ '^VAL-[0-9]{3}$'",
            name="ck_validation_batch_cases_validation_case_id_format",
        ),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["clinical_cases.id"],
            name="fk_validation_batch_cases_case_id_clinical_cases",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_validation_batch_cases"),
        sa.UniqueConstraint("validation_case_id", name="uq_validation_batch_cases_validation_case_id"),
    )
    op.create_index(
        "ix_validation_batch_cases_batch_code",
        "validation_batch_cases",
        ["batch_code"],
        unique=False,
    )
    op.create_index(
        "ix_validation_batch_cases_case_id",
        "validation_batch_cases",
        ["case_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_validation_batch_cases_case_id", table_name="validation_batch_cases")
    op.drop_index("ix_validation_batch_cases_batch_code", table_name="validation_batch_cases")
    op.drop_table("validation_batch_cases")
