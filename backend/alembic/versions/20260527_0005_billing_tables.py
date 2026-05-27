"""billing tables

Revision ID: 20260527_0005_billing_tables
Revises: 20260527_0004_erpnext_integration
Create Date: 2026-05-27 00:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260527_0005_billing_tables"
down_revision = "20260527_0004_erpnext_integration"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "billing_plans",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False, default=0),
        sa.Column("currency", sa.String(length=3), nullable=False, default="USD"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        op.f("ix_billing_plans_name"), "billing_plans", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_billing_plans_slug"), "billing_plans", ["slug"], unique=False
    )

    op.create_table(
        "billing_subscriptions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.String(length=36),
            sa.ForeignKey("tenants.id"),
            nullable=True,
        ),
        sa.Column(
            "plan_id",
            sa.String(length=36),
            sa.ForeignKey("billing_plans.id"),
            nullable=False,
        ),
        sa.Column(
            "status", sa.String(length=32), nullable=False, server_default="active"
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'")
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        op.f("ix_billing_subscriptions_organization_id"),
        "billing_subscriptions",
        ["organization_id"],
        unique=False,
    )

    op.create_table(
        "billing_invoices",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.String(length=36),
            sa.ForeignKey("tenants.id"),
            nullable=True,
        ),
        sa.Column("amount_cents", sa.Integer(), nullable=False, default=0),
        sa.Column("currency", sa.String(length=3), nullable=False, default="USD"),
        sa.Column(
            "status", sa.String(length=32), nullable=False, server_default="draft"
        ),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lines", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column(
            "metadata", sa.JSON(), nullable=False, server_default=sa.text("'{}'")
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        op.f("ix_billing_invoices_organization_id"),
        "billing_invoices",
        ["organization_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_billing_invoices_organization_id"), table_name="billing_invoices"
    )
    op.drop_table("billing_invoices")
    op.drop_index(
        op.f("ix_billing_subscriptions_organization_id"),
        table_name="billing_subscriptions",
    )
    op.drop_table("billing_subscriptions")
    op.drop_index(op.f("ix_billing_plans_slug"), table_name="billing_plans")
    op.drop_index(op.f("ix_billing_plans_name"), table_name="billing_plans")
    op.drop_table("billing_plans")
