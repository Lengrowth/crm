class ERPNextProvisioningService:
    """Coordinates provisioning actions for ERPNext tenant sites."""

    def build_plan(self, tenant_id: str) -> list[str]:
        return [
            "create_site",
            "install_erpnext",
            "install_custom_app",
            "configure_branding",
            "create_admin_user",
            "enable_modules",
            "configure_domain",
            "issue_ssl",
        ]
