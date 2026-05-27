export const AUTH_TOKEN_COOKIE = "crm-auth-token";

export function getAuthTokenCookie(): string | null {
  if (typeof document === "undefined") {
    return null;
  }

  const match = document.cookie.match(new RegExp(`(?:^|; )${AUTH_TOKEN_COOKIE}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

export function setAuthTokenCookie(token: string, maxAgeSeconds = 60 * 60 * 24 * 30): void {
  if (typeof document === "undefined") {
    return;
  }

  document.cookie = [
    `${AUTH_TOKEN_COOKIE}=${encodeURIComponent(token)}`,
    "Path=/",
    `Max-Age=${maxAgeSeconds}`,
    "SameSite=Lax",
  ].join("; ");
}

export function clearAuthTokenCookie(): void {
  if (typeof document === "undefined") {
    return;
  }

  document.cookie = `${AUTH_TOKEN_COOKIE}=; Path=/; Max-Age=0; SameSite=Lax`;
}
