export type TenantStatus = "planned" | "provisioning" | "ready" | "suspended" | "failed" | "archived";

export interface TenantSummary {
  id: string;
  organizationId: string;
  organizationName: string;
  tenantSlug: string;
  environment: "demo" | "staging" | "production";
  status: TenantStatus;
  primaryDomain: string | null;
  customDomain: string | null;
  erpnextSiteName: string | null;
  erpnextBaseUrl: string | null;
  provisioningStatus: "pending" | "queued" | "running" | "ready" | "failed";
}
