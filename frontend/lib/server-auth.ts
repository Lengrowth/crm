import { cookies } from "next/headers";
import { env } from "@/lib/env";
import type { AuthMeResponse, AuthUser } from "@/features/auth/types";

export function canAccessImplementation(user: AuthUser | null): boolean {
  return user?.is_platform_admin === true;
}

function backendUrl(path: string): string | null {
  const configured = process.env.SAAS_BACKEND_INTERNAL_URL ?? env.apiBaseUrl;
  if (!configured || configured.startsWith("/")) return null;
  return `${configured.replace(/\/$/, "")}${path}`;
}

export async function getServerAuthUser(): Promise<AuthUser | null> {
  const token = (await cookies()).get(env.authCookieName)?.value;
  const url = backendUrl("/auth/me");
  if (!token || !url) return null;

  try {
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!response.ok) return null;
    const payload = (await response.json()) as AuthMeResponse;
    return payload.user ?? null;
  } catch {
    return null;
  }
}
