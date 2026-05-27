export const env = {
  appName: process.env.NEXT_PUBLIC_APP_NAME ?? "SaaS Control Platform",
  apiBaseUrl:
    process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000",
  siteUrl: process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000",
} as const;
