"""CliniProof error taxonomy columns and RxClass membership.

Revision ID: d4e8b17c6a91
Revises: c3f8a91b2e47
Create Date: 2026-09-22 15:00:00.000000

Adds investigator error_family on frozen batch rows and a source-backed
medication-class table. Does not rewrite Phase 1 or historical VAL rows.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d4e8b17c6a91"
down_revision: str | None = "c3f8a91b2e47"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "validation_batch_cases",
        sa.Column("error_family", sa.String(length=64), nullable=True),
    )
    op.create_table(
        "ref_medication_classes",
        sa.Column("rxcui", sa.String(length=64), nullable=False),
        sa.Column("class_id", sa.String(length=64), nullable=False),
        sa.Column("class_name", sa.String(length=512), nullable=False),
        sa.Column("class_type", sa.String(length=64), nullable=True),
        sa.Column("rela", sa.String(length=128), nullable=True),
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("source_system", sa.String(length=128), nullable=True),
        sa.Column("source_version", sa.String(length=64), nullable=True),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("btrim(rxcui) <> ''", name="ck_ref_medication_classes_rxcui_not_blank"),
        sa.CheckConstraint(
            "btrim(class_id) <> ''", name="ck_ref_medication_classes_class_id_not_blank"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_ref_medication_classes"),
        sa.UniqueConstraint(
            "rxcui",
            "class_id",
            "class_type",
            "rela",
            name="uq_ref_medication_classes_membership",
            postgresql_nulls_not_distinct=True,
        ),
    )
    op.create_index(
        "ix_ref_medication_classes_rxcui",
        "ref_medication_classes",
        ["rxcui"],
        unique=False,
    )
    op.create_index(
        "ix_ref_medication_classes_class_id",
        "ref_medication_classes",
        ["class_id"],
        unique=False,
    )
    op.execute(
        """
        INSERT INTO data_source_registry (
            source_code, source_name, provider, source_category, access_type,
            requires_credentials, enabled, sync_status, records_imported,
            license_or_terms, metadata
        )
        SELECT
            'RXCLASS',
            'RxClass',
            'U.S. National Library of Medicine',
            'medication_class',
            'public',
            false,
            true,
            'never_synced',
            0,
            'NLM RxClass terms apply. Class membership is copied from RxNav, not inferred.',
            '{"required_env": []}'::jsonb
        WHERE NOT EXISTS (
            SELECT 1 FROM data_source_registry WHERE source_code = 'RXCLASS'
        )
        """
    )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM data_source_registry WHERE source_code = 'RXCLASS'"))
    op.drop_index("ix_ref_medication_classes_class_id", table_name="ref_medication_classes")
    op.drop_index("ix_ref_medication_classes_rxcui", table_name="ref_medication_classes")
    op.drop_table("ref_medication_classes")
    op.drop_column("validation_batch_cases", "error_family")
    _ = postgresql
