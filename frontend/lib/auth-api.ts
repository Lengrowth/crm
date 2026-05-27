import { env } from "@/lib/env";
import { getAuthTokenCookie } from "@/lib/auth";
import type {
  AuthLoginPayload,
  AuthMeResponse,
  AuthRegisterPayload,
  AuthTokenResponse,
} from "@/features/auth/types";

function getResponseMessage(response: Response): Promise<string> {
  return response
    .json()
    .then((payload: { detail?: string }) => payload.detail ?? response.statusText)
    .catch(() => response.statusText);
}

async function requestJson<TResponse>(
  path: string,
  init: RequestInit = {},
  includeAuth = false,
): Promise<TResponse> {
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

export function loginLocalUser(payload: AuthLoginPayload): Promise<AuthTokenResponse> {
  return requestJson<AuthTokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function registerLocalUser(payload: AuthRegisterPayload): Promise<AuthTokenResponse> {
  return requestJson<AuthTokenResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchLocalSession(): Promise<AuthMeResponse> {
  return requestJson<AuthMeResponse>("/auth/me", { method: "GET" }, true);
}

export function logoutLocalUser(): Promise<{ detail: string }> {
  return requestJson<{ detail: string }>("/auth/logout", { method: "POST" }, true);
}
