from __future__ import annotations

from typing import Any


class TenantOnboardingService:
    """Compatibility facade for callers migrating to the Phase 4 workflow.

    Tenant onboarding is intentionally not started from a tenant id. The public
    intake creates an :class:`OnboardingRequest`, and an approved operator action
    performs conversion and separately authorized execution. Keeping this facade
    side-effect-free prevents older callers from recreating the retired direct
    provisioning bypass.
    """

    def start_onboarding(self, tenant_id: str, **_: Any) -> dict[str, str]:
        if not tenant_id or not tenant_id.strip():
            raise ValueError("tenant_id is required")
        return {
            "tenant_id": tenant_id,
            "status": "requires_approved_onboarding",
            "message": "Create and approve an onboarding request before execution.",
        }
