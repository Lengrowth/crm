"""add Phase 4 onboarding state and durable provisioning workflow

Revision ID: 20260918_0010
Revises: 20260918_0009
"""

from alembic import op
import sqlalchemy as sa


revision = "20260918_0010"
down_revision = "20260918_0009"
branch_labels = None
depends_on = None


def _json_list() -> sa.TextClause:
    return sa.text("'[]'")


def _json_object() -> sa.TextClause:
    return sa.text("'{}'")


def upgrade() -> None:
    op.create_table(
        "onboarding_requests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        sa.Column("management_token_hash", sa.String(length=64), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("applicant_visible_status", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("submitted_version", sa.Integer(), nullable=True),
        sa.Column("approved_version", sa.Integer(), nullable=True),
        sa.Column("approved_bundle_key", sa.String(length=64), nullable=True),
        sa.Column("approved_bundle_version", sa.Integer(), nullable=True),
        sa.Column("approved_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("execution_authorized_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("execution_authorized_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("converted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("organization_id", sa.String(length=36), nullable=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=True),
        sa.Column("implementation_project_id", sa.String(length=36), nullable=True),
        sa.Column("provisioning_job_id", sa.String(length=36), nullable=True),
        sa.Column("rejection_reason", sa.String(length=500), nullable=True),
        sa.Column("cancellation_reason", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["approved_by_user_id"], ["saas_users.id"]),
        sa.ForeignKeyConstraint(["execution_authorized_by_user_id"], ["saas_users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["implementation_project_id"], ["implementation_projects.id"]),
        sa.ForeignKeyConstraint(["provisioning_job_id"], ["provisioning_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key", name="uq_onboarding_request_idempotency"),
    )
    op.create_index("ix_onboarding_requests_state", "onboarding_requests", ["state"], unique=False)
    op.create_index("ix_onboarding_requests_organization_id", "onboarding_requests", ["organization_id"], unique=False)
    op.create_index("ix_onboarding_requests_tenant_id", "onboarding_requests", ["tenant_id"], unique=False)

    op.create_table(
        "onboarding_request_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("version_idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False, server_default=_json_object()),
        sa.Column("requested_module_codes_json", sa.JSON(), nullable=False, server_default=_json_list()),
        sa.Column("bundle_key", sa.String(length=64), nullable=True),
        sa.Column("bundle_version", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=32), nullable=False, server_default="public"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("supersedes_version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["request_id"], ["onboarding_requests.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_id", "version", name="uq_onboarding_request_version"),
        sa.UniqueConstraint("request_id", "version_idempotency_key", name="uq_onboarding_version_idempotency"),
    )
    op.create_index("ix_onboarding_request_versions_request_id", "onboarding_request_versions", ["request_id"], unique=False)

    op.create_table(
        "onboarding_management_credentials",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["request_id"], ["onboarding_requests.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_onboarding_management_credentials_request_id", "onboarding_management_credentials", ["request_id"], unique=False)

    op.create_table(
        "onboarding_decisions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("actor_user_id", sa.String(length=36), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=False),
        sa.Column("bundle_key", sa.String(length=64), nullable=True),
        sa.Column("bundle_version", sa.Integer(), nullable=True),
        sa.Column("execution_authorized", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["request_id"], ["onboarding_requests.id"]),
        sa.ForeignKeyConstraint(["actor_user_id"], ["saas_users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_onboarding_decisions_request_id", "onboarding_decisions", ["request_id"], unique=False)
    op.create_index("ix_onboarding_decisions_actor_user_id", "onboarding_decisions", ["actor_user_id"], unique=False)

    for column in (
        sa.Column("onboarding_request_id", sa.String(length=36), nullable=True),
        sa.Column("onboarding_version", sa.Integer(), nullable=True),
        sa.Column("workflow_version", sa.String(length=32), nullable=False, server_default="legacy-1"),
        sa.Column("worker_id", sa.String(length=128), nullable=True),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("cancel_requested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("external_refs_json", sa.JSON(), nullable=False, server_default=_json_object()),
        sa.Column("target_environment", sa.String(length=32), nullable=False, server_default="staging"),
        sa.Column("target_isolation_json", sa.JSON(), nullable=False, server_default=_json_object()),
    ):
        op.add_column("provisioning_jobs", column)
    op.create_index("ix_provisioning_jobs_onboarding_request_id", "provisioning_jobs", ["onboarding_request_id"], unique=False)

    op.create_table(
        "provisioning_steps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=64), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("worker_id", sa.String(length=128), nullable=True),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_category", sa.String(length=32), nullable=True),
        sa.Column("sanitized_error", sa.String(length=500), nullable=True),
        sa.Column("evidence_json", sa.JSON(), nullable=False, server_default=_json_object()),
        sa.Column("external_ref", sa.String(length=255), nullable=True),
        sa.Column("rollback_state", sa.String(length=32), nullable=False, server_default="not_started"),
        sa.Column("dependency_keys_json", sa.JSON(), nullable=False, server_default=_json_list()),
        sa.ForeignKeyConstraint(["job_id"], ["provisioning_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id", "step_key", name="uq_provisioning_step_job_key"),
    )
    op.create_index("ix_provisioning_steps_job_id", "provisioning_steps", ["job_id"], unique=False)

    op.create_table(
        "provisioning_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("step_id", sa.String(length=36), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("event_code", sa.String(length=64), nullable=False),
        sa.Column("public_message", sa.String(length=500), nullable=False),
        sa.Column("context_json", sa.JSON(), nullable=False, server_default=_json_object()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["step_id"], ["provisioning_steps.id"]),
        sa.ForeignKeyConstraint(["job_id"], ["provisioning_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_provisioning_events_step_id", "provisioning_events", ["step_id"], unique=False)
    op.create_index("ix_provisioning_events_job_id", "provisioning_events", ["job_id"], unique=False)

    op.create_table(
        "provisioning_outbox_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("aggregate_type", sa.String(length=64), nullable=False),
        sa.Column("aggregate_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False, server_default=_json_object()),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key", name="uq_provisioning_outbox_idempotency"),
    )
    op.create_index("ix_provisioning_outbox_events_aggregate_id", "provisioning_outbox_events", ["aggregate_id"], unique=False)

    op.create_table(
        "first_login_handoffs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=True),
        sa.Column("token_secret_ref", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="prepared"),
        sa.Column("delivery_status", sa.String(length=32), nullable=False, server_default="disabled"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivery_reference", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["request_id"], ["onboarding_requests.id"]),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["saas_users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_first_login_handoffs_request_id", "first_login_handoffs", ["request_id"], unique=False)
    op.create_index("ix_first_login_handoffs_tenant_id", "first_login_handoffs", ["tenant_id"], unique=False)
    op.create_index("ix_first_login_handoffs_user_id", "first_login_handoffs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_first_login_handoffs_user_id", table_name="first_login_handoffs")
    op.drop_index("ix_first_login_handoffs_tenant_id", table_name="first_login_handoffs")
    op.drop_index("ix_first_login_handoffs_request_id", table_name="first_login_handoffs")
    op.drop_table("first_login_handoffs")
    op.drop_index("ix_provisioning_outbox_events_aggregate_id", table_name="provisioning_outbox_events")
    op.drop_table("provisioning_outbox_events")
    op.drop_index("ix_provisioning_events_job_id", table_name="provisioning_events")
    op.drop_index("ix_provisioning_events_step_id", table_name="provisioning_events")
    op.drop_table("provisioning_events")
    op.drop_index("ix_provisioning_steps_job_id", table_name="provisioning_steps")
    op.drop_table("provisioning_steps")
    op.drop_index("ix_provisioning_jobs_onboarding_request_id", table_name="provisioning_jobs")
    for name in ("target_isolation_json", "target_environment", "external_refs_json", "cancel_requested_at", "max_attempts", "next_attempt_at", "heartbeat_at", "lease_expires_at", "worker_id", "workflow_version", "onboarding_version", "onboarding_request_id"):
        op.drop_column("provisioning_jobs", name)
    op.drop_index("ix_onboarding_decisions_actor_user_id", table_name="onboarding_decisions")
    op.drop_index("ix_onboarding_decisions_request_id", table_name="onboarding_decisions")
    op.drop_table("onboarding_decisions")
    op.drop_index("ix_onboarding_management_credentials_request_id", table_name="onboarding_management_credentials")
    op.drop_table("onboarding_management_credentials")
    op.drop_index("ix_onboarding_request_versions_request_id", table_name="onboarding_request_versions")
    op.drop_table("onboarding_request_versions")
    op.drop_index("ix_onboarding_requests_tenant_id", table_name="onboarding_requests")
    op.drop_index("ix_onboarding_requests_organization_id", table_name="onboarding_requests")
    op.drop_index("ix_onboarding_requests_state", table_name="onboarding_requests")
    op.drop_table("onboarding_requests")
