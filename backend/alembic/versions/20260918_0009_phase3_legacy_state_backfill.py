"""backfill Phase 3 state from legacy organization module status

Revision ID: 20260918_0009
Revises: 20260917_0008
"""

from alembic import op
import sqlalchemy as sa


revision = "20260918_0009"
down_revision = "20260917_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Idempotent and deliberately status-derived so deployments that already
    # ran 0008 receive the same safe behavior as a fresh 0007 -> head upgrade.
    op.execute(
        sa.text(
            """
            UPDATE organization_modules
            SET explicit_state = CASE WHEN lower(status) = 'enabled' THEN 'enabled' ELSE 'disabled' END,
                requested_state = CASE WHEN lower(status) = 'enabled' THEN 'enabled' ELSE 'disabled' END,
                entitled_state = CASE WHEN lower(status) = 'enabled' THEN 'entitled' ELSE 'not_entitled' END
            """
        )
    )


def downgrade() -> None:
    # State columns remain part of 0008; this migration has no independent
    # destructive downgrade.
    pass
