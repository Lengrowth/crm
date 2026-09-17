# Frontend

This is the Next.js App Router frontend for the SaaS control platform.

## Purpose

- Public marketing pages.
- Auth placeholder pages.
- Dashboard shell pages.
- SaaS entity pages for organizations, tenants, modules, billing, and settings.
- A simple light/dark theme shell built with Tailwind and local CSS tokens.
- A responsive operator shell gated by the server-controlled
  `platform_phase1_shell` runtime flag. Set `NEXT_PUBLIC_APP_NAME`,
  `NEXT_PUBLIC_ENVIRONMENT_LABEL`, `NEXT_PUBLIC_STATUS_LABEL`, `NEXT_PUBLIC_SUPPORT_URL`, and
  `NEXT_PUBLIC_STATUS_URL` per deployment; do not bake deployment hostnames
  into shell code.

## Folder Layout

- `app/` - route groups and pages.
- `components/` - reusable UI placeholders.
- `features/` - feature-level types and future UI logic.
- `lib/` - shared frontend helpers.
- `styles/` - theme tokens and shared styling.

## Local Development

```bash
npm install
npm run dev
```

## Environment

Copy `./.env.example` to `.env.local` before running the app.

## Notes

- The frontend is intentionally a shell in Phase 01.
- `npm test` runs navigation, permission, flag, nested-route, and breadcrumb
  unit coverage.
- Phase 03 adds a local auth-aware login page, a session badge, and middleware-based route protection scaffolding.
- Phase 04 adds the public marketing pages and the canonical `/app` shell for logged-in navigation.
- Phase 05 adds organization and tenant route scaffolds under `/app`, including list, detail, and create screens.
- ERPNext/Frappe is not required for local development.
- The current UI does not rely on shadcn; it uses Tailwind plus local theme variables so light and dark layouts stay under our control.
- Phase 20 expands auth UX with dedicated forgot-password, reset-password, verify-email, and resend-verification screens while keeping the `/login` sign-in/register toggle.
