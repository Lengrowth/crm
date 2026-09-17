import { env } from "@/lib/env";
import { getAuthTokenCookie } from "@/lib/auth";
import type { DashboardSummary } from "@/features/dashboard/types";
import type { ImplementationPortfolio } from "@/features/implementation/types";
import type { DomainRecord, ProvisioningJobRecord, TenantRecord } from "@/features/tenants/types";
import type { OrganizationRecord } from "@/features/organizations/types";

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
export function fetchOrganizations() { return requestJson<OrganizationRecord[]>("/organizations"); }
export function createOrganization(payload: Record<string, unknown>) { return requestJson<OrganizationRecord>("/organizations", { method: "POST", body: JSON.stringify(payload) }); }
export function fetchOrganization(organizationId: string) { return requestJson<OrganizationRecord>(`/organizations/${organizationId}`); }
export function updateOrganization(organizationId: string, payload: Record<string, unknown>) { return requestJson<OrganizationRecord>(`/organizations/${organizationId}`, { method: "PATCH", body: JSON.stringify(payload) }); }
export function fetchOrganizationTenants(organizationId: string) { return requestJson<TenantRecord[]>(`/organizations/${organizationId}/tenants`); }
export function createOrganizationTenant(organizationId: string, payload: Record<string, unknown>) { return requestJson<TenantRecord>(`/organizations/${organizationId}/tenants`, { method: "POST", body: JSON.stringify(payload) }); }
export function fetchTenants() { return requestJson<TenantRecord[]>("/tenants"); }
export function createTenant(payload: Record<string, unknown>) { return requestJson<TenantRecord>("/tenants", { method: "POST", body: JSON.stringify(payload) }); }
export function fetchTenant(tenantId: string) { return requestJson<TenantRecord>(`/tenants/${tenantId}`); }
export function updateTenant(tenantId: string, payload: Record<string, unknown>) { return requestJson<TenantRecord>(`/tenants/${tenantId}`, { method: "PATCH", body: JSON.stringify(payload) }); }
export function suspendTenant(tenantId: string, reason?: string) { return requestJson<TenantRecord>(`/tenants/${tenantId}/suspend`, { method: "POST", body: JSON.stringify({ reason }) }); }
export function reactivateTenant(tenantId: string, reason?: string) { return requestJson<TenantRecord>(`/tenants/${tenantId}/reactivate`, { method: "POST", body: JSON.stringify({ reason }) }); }
export function listTenantDomains(tenantId: string) { return requestJson<DomainRecord[]>(`/tenants/${tenantId}/domains`); }
export function manualActivateDomain(tenantId: string, domainId: string, payload: Record<string, unknown>) { return requestJson<DomainRecord>(`/tenants/${tenantId}/domains/${domainId}/manual_activate`, { method: "POST", body: JSON.stringify(payload) }); }
export function provisionTenant(organizationId: string, tenantId: string, payload: Record<string, unknown>) { return requestJson<{ id: string }>(`/organizations/${organizationId}/tenants/${tenantId}/provision`, { method: "POST", body: JSON.stringify(payload) }); }
export function getProvisioningStatus(provisionId: string) { return requestJson<{ id: string; status: string }>(`/provisioning/${provisionId}`); }
export function listProvisioningJobs(tenantId: string) { return requestJson<ProvisioningJobRecord[]>(`/tenants/${tenantId}/provisioning_jobs`); }
