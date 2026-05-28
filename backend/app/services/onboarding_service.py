from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.schemas.control import OrganizationCreateRequest, TenantCreateRequest
from app.services.billing_service import BillingService
from app.services.control_plane_service import ControlPlaneService
from app.services.provisioning_service import provisioning_service
from app.workers.provisioning_worker import run_next_job


class OnboardingService:
    """Orchestrates a pilot onboarding flow across control plane, billing, and provisioning.

    Methods are deterministic and use existing app services. Network provider calls are
    best-effort and do not fail the local flow.
    """

    def __init__(self, billing_provider: Optional[Any] = None) -> None:
        self.control = ControlPlaneService()
        self.billing = BillingService(provider=billing_provider)

    def onboard_pilot_organization(
        self,
        session: Session,
        current_user: object,
        org_payload: dict[str, Any],
        tenant_payload: dict[str, Any],
        plan_slug: str,
        site_options: Optional[dict[str, Any]] = None,
        run_provision_now: bool = False,
        provisioning_client: Optional[Any] = None,
    ) -> dict[str, Any]:
        """Run the pilot onboarding orchestration.

        Steps:
        - create Organization
        - create Tenant under the organization
        - subscribe the organization to `plan_slug` (creates a BillingSubscription)
        - generate an invoice for the subscription
        - queue a provisioning job for the tenant (payload includes organization_id and site_options)

        If `run_provision_now` is True the worker will be invoked synchronously using
        `run_next_job` so tests can execute the full flow in-memory.

        Returns a dict with keys: organization, tenant, subscription, invoice, provisioning_job
        (each value is the SQLAlchemy ORM object as returned by the underlying services).
        """
        # create organization
        org_req = OrganizationCreateRequest(**org_payload)
        organization = self.control.create_organization(session, current_user, org_req)

        # create tenant
        # ensure tenant_payload references organization
        tenant_payload = dict(tenant_payload or {})
        tenant_payload["organization_id"] = organization.id
        tenant_req = TenantCreateRequest(**tenant_payload)
        tenant = self.control.create_tenant(session, current_user, tenant_req)

        # subscribe organization
        subscription = self.billing.subscribe_organization(
            session, organization.id, plan_slug, tenant_id=tenant.id
        )

        # generate invoice
        invoice = self.billing.generate_invoice_for_subscription(
            session, subscription.id
        )

        # queue provisioning job
        payload = {
            "organization_id": organization.id,
            "site_options": site_options or {},
        }
        job = provisioning_service.queue_provisioning_job(
            session, tenant_id=tenant.id, job_type="initial_provision", payload=payload
        )

        result = {
            "organization": organization,
            "tenant": tenant,
            "subscription": subscription,
            "invoice": invoice,
            "provisioning_job": job,
        }

        # optionally run provisioning synchronously for in-memory tests
        if run_provision_now:
            # run worker once; it will pick queued job(s) and process them
            run_next_job(session, client=provisioning_client)
            # refresh job and tenant state from DB
            session.refresh(job)
            session.refresh(tenant)

        return result


onboarding_service = OnboardingService()
