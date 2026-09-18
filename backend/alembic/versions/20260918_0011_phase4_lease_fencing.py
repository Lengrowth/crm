"""add durable lease fencing for Phase 4 workers

Revision ID: 20260918_0011
Revises: 20260918_0010
"""

from alembic import op
import sqlalchemy as sa


revision = "20260918_0011"
down_revision = "20260918_0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "provisioning_jobs",
        sa.Column("lease_token", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("provisioning_jobs", "lease_token")
