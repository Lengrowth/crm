import { env } from "@/lib/env";

export const AUTH_TOKEN_COOKIE = env.authCookieName;

export function getAuthTokenCookie(): string | null {
  if (typeof document === "undefined") {
    return null;
  }

  const match = document.cookie.match(new RegExp(`(?:^|; )${AUTH_TOKEN_COOKIE}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

function cookieAttributes(maxAgeSeconds: number): string[] {
  const attributes = [
    `Path=${env.authCookiePath}`,
    `Max-Age=${maxAgeSeconds}`,
    `SameSite=${env.authCookieSameSite}`,
  ];
  if (env.authCookieDomain) {
    attributes.push(`Domain=${env.authCookieDomain}`);
  }
  if (env.authCookieSecure) {
    attributes.push("Secure");
  }
  return attributes;
}

export function setAuthTokenCookie(token: string, maxAgeSeconds = env.authCookieMaxAgeSeconds): void {
  if (typeof document === "undefined") {
    return;
  }

  document.cookie = [`${AUTH_TOKEN_COOKIE}=${encodeURIComponent(token)}`, ...cookieAttributes(maxAgeSeconds)].join("; ");
}

export function clearAuthTokenCookie(): void {
  if (typeof document === "undefined") {
    return;
  }

  document.cookie = `${AUTH_TOKEN_COOKIE}=; ${cookieAttributes(0).join("; ")}`;
}
