export const env = {
  appName: process.env.NEXT_PUBLIC_APP_NAME ?? "LenERP",
  apiBaseUrl:
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    (process.env.NODE_ENV === "production"
      ? "/api"
      : process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"),
  siteUrl: process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000",
  authCookieName: process.env.NEXT_PUBLIC_AUTH_COOKIE_NAME ?? "crm-auth-token",
  authCookiePath: process.env.NEXT_PUBLIC_AUTH_COOKIE_PATH ?? "/",
  authCookieDomain: process.env.NEXT_PUBLIC_AUTH_COOKIE_DOMAIN ?? "",
  authCookieSameSite: process.env.NEXT_PUBLIC_AUTH_COOKIE_SAME_SITE ?? "Lax",
  authCookieSecure:
    process.env.NEXT_PUBLIC_AUTH_COOKIE_SECURE === "true" ||
    (process.env.NEXT_PUBLIC_AUTH_COOKIE_SECURE === undefined &&
      process.env.NODE_ENV === "production"),
  authCookieMaxAgeSeconds: Number.parseInt(
    process.env.NEXT_PUBLIC_AUTH_COOKIE_MAX_AGE_SECONDS ?? `${60 * 60 * 24 * 30}`,
    10,
  ),
} as const;
