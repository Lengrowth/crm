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

export interface TenantRecord {
  id: string;
  organization_id: string;
  tenant_slug: string;
  environment: "demo" | "staging" | "production";
  status: TenantStatus;
  primary_domain: string | null;
  custom_domain: string | null;
  erpnext_site_name: string | null;
  erpnext_base_url: string | null;
  provisioning_status: "pending" | "queued" | "running" | "ready" | "failed";
  created_at: string;
  updated_at: string;
}

export interface DomainRecord {
  id: string;
  tenant_id: string;
  domain: string;
  type: string;
  status: string;
  is_active: boolean;
  manual_activation_required: boolean;
  ssl_status: string;
  notes_json: Record<string, unknown>;
}

export interface ProvisioningJobRecord {
  id: string;
  tenant_id: string;
  job_type: string;
  status: string;
  started_at: string | null;
  finished_at: string | null;
  attempt_count: number;
  logs_json: Array<Record<string, unknown>>;
  error_message: string | null;
}
