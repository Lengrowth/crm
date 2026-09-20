import { env } from "@/lib/env";
import { getAuthTokenCookie } from "@/lib/auth";
import type { DashboardSummary } from "@/features/dashboard/types";
import type { ImplementationPortfolio } from "@/features/implementation/types";
import type { DomainRecord, ProvisioningJobRecord, TenantRecord } from "@/features/tenants/types";
import type { OrganizationRecord } from "@/features/organizations/types";
import type { ModuleAudit, ModuleBundle, ModuleEffective, ModulePreview, ModuleSummary } from "@/features/modules/types";
import type { OperatorOnboardingRead, ProvisioningEventRead, ProvisioningJobDetailRead, PublicOnboardingRead, PublicOnboardingResult } from "@/features/onboarding/types";

export type SSOAuthorizationResponse = { code: string; state: string; redirect_uri: string; expires_in: number; tenant_id: string; organization_id: string };
export type SSOReadiness = { tenant_id: string; organization_id: string; organization_name: string; tenant_slug: string; environment: string; destination: string | null; enabled: boolean; ready: boolean; explanation: string };

export class ApiError extends Error {
  constructor(public readonly status: number, message: string) { super(message); this.name = "ApiError"; }
}

function safeMessage(status: number, detail: unknown): string {
  if (status === 401) return "Your session has expired. Sign in again to continue.";
  if (status === 403) return "You do not have permission to perform this action.";
  if (status === 404) return "The requested record was not found.";
  if (status >= 500) return "The service is temporarily unavailable. Try again shortly.";
  if (typeof detail === "string" && detail.length > 0 && detail.length < 240 && !(/[\r\n]|traceback|exception|secret|token|password/i.test(detail))) return detail;
  return "The request could not be completed. Check the highlighted fields and try again.";
}

async function requestJson<T>(path: string, init: RequestInit = {}, includeAuth = true): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  if (includeAuth) {
    const token = getAuthTokenCookie();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(`${env.apiBaseUrl}${path}`, { ...init, headers });
  if (!response.ok) {
    let detail: unknown;
    try { detail = (await response.json() as { detail?: unknown }).detail; } catch { /* use generic message */ }
    throw new ApiError(response.status, safeMessage(response.status, detail));
  }
  if (response.status === 204) return undefined as T;
  return await response.json() as T;
}

export type MarketingIntake = { name: string; email: string; message: string };
export function sendContact(payload: MarketingIntake) { return requestJson<{ detail: string }>("/marketing/contact", { method: "POST", body: JSON.stringify(payload) }, false); }
export function sendDemoRequest(payload: MarketingIntake) { return requestJson<{ detail: string }>("/marketing/demo", { method: "POST", body: JSON.stringify(payload) }, false); }
export function trackMarketingEvent(payload: Record<string, unknown>) { return fetch(`${env.apiBaseUrl}/marketing/analytics`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }).catch(() => undefined); }

export function fetchDashboardSummary() { return requestJson<DashboardSummary>("/dashboard/summary"); }
export function fetchImplementationPortfolio() { return requestJson<ImplementationPortfolio>("/implementation/portfolio"); }
export function fetchOrganizations(limit?: number) { return requestJson<OrganizationRecord[]>(`/organizations${limit ? `?limit=${limit}` : ""}`); }
export function createOrganization(payload: Record<string, unknown>) { return requestJson<OrganizationRecord>("/organizations", { method: "POST", body: JSON.stringify(payload) }); }
export function fetchOrganization(organizationId: string) { return requestJson<OrganizationRecord>(`/organizations/${organizationId}`); }
export function updateOrganization(organizationId: string, payload: Record<string, unknown>) { return requestJson<OrganizationRecord>(`/organizations/${organizationId}`, { method: "PATCH", body: JSON.stringify(payload) }); }
export function fetchOrganizationTenants(organizationId: string) { return requestJson<TenantRecord[]>(`/organizations/${organizationId}/tenants`); }
export function createOrganizationTenant(organizationId: string, payload: Record<string, unknown>) { return requestJson<TenantRecord>(`/organizations/${organizationId}/tenants`, { method: "POST", body: JSON.stringify(payload) }); }
export function fetchTenants(limit?: number) { return requestJson<TenantRecord[]>(`/tenants${limit ? `?limit=${limit}` : ""}`); }
export function createTenant(payload: Record<string, unknown>) { return requestJson<TenantRecord>("/tenants", { method: "POST", body: JSON.stringify(payload) }); }
export function fetchTenant(tenantId: string) { return requestJson<TenantRecord>(`/tenants/${tenantId}`); }
export function fetchSsoReadiness(tenantId: string) { return requestJson<SSOReadiness>(`/sso/readiness/${tenantId}`); }
export function authorizeSso(payload: Record<string, unknown>) { return requestJson<SSOAuthorizationResponse>("/sso/authorize", { method: "POST", body: JSON.stringify(payload) }); }
export function updateTenant(tenantId: string, payload: Record<string, unknown>) { return requestJson<TenantRecord>(`/tenants/${tenantId}`, { method: "PATCH", body: JSON.stringify(payload) }); }
export function suspendTenant(tenantId: string, reason?: string) { return requestJson<TenantRecord>(`/tenants/${tenantId}/suspend`, { method: "POST", body: JSON.stringify({ reason }) }); }
export function reactivateTenant(tenantId: string, reason?: string) { return requestJson<TenantRecord>(`/tenants/${tenantId}/reactivate`, { method: "POST", body: JSON.stringify({ reason }) }); }
export function listTenantDomains(tenantId: string) { return requestJson<DomainRecord[]>(`/tenants/${tenantId}/domains`); }
export function manualActivateDomain(tenantId: string, domainId: string, payload: Record<string, unknown>) { return requestJson<DomainRecord>(`/tenants/${tenantId}/domains/${domainId}/manual_activate`, { method: "POST", body: JSON.stringify(payload) }); }
export function getProvisioningStatus(provisionId: string) { return requestJson<{ id: string; status: string }>(`/provisioning/${provisionId}`); }
export function listProvisioningJobs(tenantId: string) { return requestJson<ProvisioningJobRecord[]>(`/tenants/${tenantId}/provisioning_jobs`); }
export function fetchModuleCatalog() { return requestJson<ModuleSummary[]>("/catalog/modules"); }
export function fetchPublicModuleCatalog() { return requestJson<Array<{ code: string; name: string; category: string | null; description: string; display_order: number }>>("/public/modules", {}, false); }
export function fetchModuleBundles() { return requestJson<ModuleBundle[]>("/module-bundles"); }
export function fetchOrganizationModules(organizationId: string) { return requestJson<ModuleEffective>(`/organizations/${organizationId}/modules`); }
export function previewOrganizationModules(organizationId: string, payload: Record<string, unknown>) { return requestJson<ModulePreview>(`/organizations/${organizationId}/modules/preview`, { method: "POST", body: JSON.stringify({ ...payload, organization_id: organizationId }) }); }
export function applyOrganizationModules(organizationId: string, payload: Record<string, unknown>) { return requestJson<{ operation: string; replayed: boolean; audit_id: string | null; effective: ModuleEffective }>(`/organizations/${organizationId}/modules/apply`, { method: "POST", body: JSON.stringify({ ...payload, organization_id: organizationId }) }); }
export function fetchOrganizationModuleAudit(organizationId: string) { return requestJson<ModuleAudit[]>(`/organizations/${organizationId}/modules/audit`); }

export type PublicOnboardingPayload = {
  company_name: string; legal_name?: string; industry?: string; country?: string; timezone?: string;
  billing_email?: string; administrator_name: string; administrator_email: string; requested_modules: string[];
  bundle_key?: string; bundle_version?: number; branding: Record<string, string>; expected_users: Array<Record<string, string>>;
  data_import_needs?: string; desired_domain?: string; desired_infrastructure: "isolated_staging" | "isolated_synthetic";
  billing_contact?: string; implementation_notes?: string; applicant_revision: number;
};
export function createPublicOnboarding(idempotencyKey: string, payload: PublicOnboardingPayload) { return requestJson<PublicOnboardingResult>("/public/onboarding-requests", { method: "POST", body: JSON.stringify({ idempotency_key: idempotencyKey, payload }) }, false); }
export function fetchPublicOnboarding(requestId: string, token: string) { return requestJson<PublicOnboardingRead>(`/public/onboarding-requests/${requestId}`, { headers: { "X-Onboarding-Token": token } }, false); }
export function revisePublicOnboarding(requestId: string, token: string, idempotencyKey: string, payload: PublicOnboardingPayload) { return requestJson<PublicOnboardingResult>(`/public/onboarding-requests/${requestId}/revisions`, { method: "POST", headers: { "X-Onboarding-Token": token }, body: JSON.stringify({ idempotency_key: idempotencyKey, payload }) }, false); }
export function submitPublicOnboarding(requestId: string, token: string) { return requestJson<PublicOnboardingResult>(`/public/onboarding-requests/${requestId}/submit`, { method: "POST", headers: { "X-Onboarding-Token": token } }, false); }
export function fetchOperatorOnboarding(state?: string) { return requestJson<OperatorOnboardingRead[]>(`/operator/onboarding-requests${state ? `?state=${encodeURIComponent(state)}` : ""}`); }
export function beginOperatorOnboardingReview(requestId: string, version: number, reason: string) { return requestJson<OperatorOnboardingRead>(`/operator/onboarding-requests/${requestId}/under-review`, { method: "POST", body: JSON.stringify({ version, reason }) }); }
export function approveOperatorOnboarding(requestId: string, version: number, reason: string) { return requestJson<OperatorOnboardingRead>(`/operator/onboarding-requests/${requestId}/approve`, { method: "POST", body: JSON.stringify({ version, reason }) }); }
export function convertOperatorOnboarding(requestId: string) { return requestJson<OperatorOnboardingRead>(`/operator/onboarding-requests/${requestId}/convert`, { method: "POST" }); }
export function authorizeOperatorOnboarding(requestId: string, version: number, reason: string) { return requestJson<OperatorOnboardingRead>(`/operator/onboarding-requests/${requestId}/authorize-execution`, { method: "POST", body: JSON.stringify({ version, confirmation: "authorize_isolated_synthetic_execution", reason }) }); }
export function fetchOperatorProvisioningJob(jobId: string) { return requestJson<ProvisioningJobDetailRead>(`/operator/provisioning-jobs/${jobId}`); }
export function fetchOperatorProvisioningEvents(jobId: string) { return requestJson<ProvisioningEventRead[]>(`/operator/provisioning-jobs/${jobId}/events`); }
export function retryOperatorProvisioningStep(jobId: string, stepKey: string, confirmation: "retry_safe_step" | "confirm_irreversible_step", reason: string) { return requestJson<ProvisioningJobDetailRead>(`/operator/provisioning-jobs/${jobId}/retry`, { method: "POST", body: JSON.stringify({ step_key: stepKey, confirmation, reason }) }); }
