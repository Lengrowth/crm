import { env } from "@/lib/env";
import { getAuthTokenCookie } from "@/lib/auth";

function getResponseMessage(response: Response): Promise<string> {
  return response
    .json()
    .then(
      (payload: { detail?: string }) => payload.detail ?? response.statusText,
    )
    .catch(() => response.statusText);
}

async function requestJson<TResponse>(path: string, init: RequestInit = {}) {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");

  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    ...init,
    headers,
  });

  if (!response.ok) {
    throw new Error(await getResponseMessage(response));
  }

  return (await response.json()) as TResponse;
}

async function requestJsonAuth<TResponse>(
  path: string,
  init: RequestInit = {},
  includeAuth = true,
) {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");

  if (includeAuth) {
    const token = getAuthTokenCookie();
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
  }

  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    ...init,
    headers,
  });

  if (!response.ok) {
    throw new Error(await getResponseMessage(response));
  }

  return (await response.json()) as TResponse;
}

export type MarketingIntake = {
  name: string;
  email: string;
  message: string;
};

export function sendContact(payload: MarketingIntake) {
  return requestJson<{ detail: string }>("/marketing/contact", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function sendDemoRequest(payload: MarketingIntake) {
  return requestJson<{ detail: string }>("/marketing/demo", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function trackMarketingEvent(payload: Record<string, unknown>) {
  return fetch(`${env.apiBaseUrl}/marketing/analytics`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).catch(() => undefined);
}

export function fetchOrganizations() {
  return requestJsonAuth<any[]>("/organizations", { method: "GET" });
}

export function fetchOrganization(organizationId: string) {
  return requestJsonAuth<any>(`/organizations/${organizationId}`, {
    method: "GET",
  });
}

export function fetchOrganizationTenants(organizationId: string) {
  return requestJsonAuth<any[]>(`/organizations/${organizationId}/tenants`, {
    method: "GET",
  });
}

export function createOrganizationTenant(
  organizationId: string,
  payload: Record<string, unknown>,
) {
  return requestJsonAuth<any>(`/organizations/${organizationId}/tenants`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchTenants() {
  return requestJsonAuth<any[]>("/tenants", { method: "GET" });
}

export function fetchTenant(tenantId: string) {
  return requestJsonAuth<any>(`/tenants/${tenantId}`, { method: "GET" });
}

export function listTenantDomains(tenantId: string) {
  return requestJsonAuth<any[]>(`/tenants/${tenantId}/domains`, {
    method: "GET",
  });
}

export function manualActivateDomain(
  tenantId: string,
  domainId: string,
  payload: Record<string, unknown>,
) {
  return requestJsonAuth<any>(
    `/tenants/${tenantId}/domains/${domainId}/manual_activate`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export function provisionTenant(
  organizationId: string,
  tenantId: string,
  payload: Record<string, unknown>,
) {
  return requestJsonAuth<{ id: string }>(
    `/organizations/${organizationId}/tenants/${tenantId}/provision`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export function getProvisioningStatus(provisionId: string) {
  return requestJsonAuth<any>(`/provisioning/${provisionId}`, {
    method: "GET",
  });
}
