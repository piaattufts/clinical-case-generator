"""clinical rules table

Revision ID: 7b9e4c21d6a0
Revises: 1c236aeaadc7
Create Date: 2026-09-21 23:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "7b9e4c21d6a0"
down_revision: str | None = "1c236aeaadc7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "clinical_rules",
        sa.Column("rule_code", sa.String(length=64), nullable=False),
        sa.Column("rule_type", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("input_icd10cm_code", sa.String(length=16), nullable=True),
        sa.Column("input_rxcui", sa.String(length=64), nullable=True),
        sa.Column("input_loinc_code", sa.String(length=64), nullable=True),
        sa.Column("related_rxcui", sa.String(length=64), nullable=True),
        sa.Column("age_min", sa.Integer(), nullable=True),
        sa.Column("age_max", sa.Integer(), nullable=True),
        sa.Column("sex", sa.String(length=32), nullable=True),
        sa.Column("care_context", sa.String(length=64), nullable=True),
        sa.Column("constraint_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("logic_notes", sa.Text(), nullable=True),
        sa.Column("source_identifier", sa.String(length=128), nullable=True),
        sa.Column("source_url", sa.String(length=512), nullable=True),
        sa.Column("evidence_excerpt", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("source_system", sa.String(length=128), nullable=True),
        sa.Column("source_version", sa.String(length=64), nullable=True),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("btrim(rule_code) <> ''", name="ck_clinical_rules_rule_code_not_blank"),
        sa.CheckConstraint(
            "severity IN ('hard', 'soft')", name="ck_clinical_rules_severity_values"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_clinical_rules"),
        sa.UniqueConstraint("rule_code", name="uq_clinical_rules_rule_code"),
    )


def downgrade() -> None:
    op.drop_table("clinical_rules")
