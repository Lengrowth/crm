# `lenerp_core`

Private LenERP custom Frappe application boundary for Champion delivery.

All LenERP-owned DocTypes, hooks, fixtures, patches, roles, workspaces,
reports, print formats, styling, and tests belong here. Upstream Frappe and
ERPNext source trees are dependencies and must remain clean and pinned.

## C01 foundation status

The `0.2.0` implementation adds the value-free C01 configuration boundary
(`LenERP Branding Settings`). It stores no default Champion values and does not
change ERPNext branding until the approved company, product, asset, domain, and
ownership decisions are recorded. The package release identity is
`CHAMP-C01-R1`; it is not accepted or production-ready until those inputs,
clean staging installation/migration, browser/print evidence, and Champion
acceptance are complete.

The settings document is intentionally restricted to System Manager. It is a
configuration boundary, not a substitute for the standard ERPNext Company,
System Settings, Website Settings, or approved domain cutover runbooks.

## Phase 0 status

The local repository contains no Champion data, secrets, or brand assets.
The private remote destination is intentionally not configured until the
approved GitHub organization/account is recorded. Install, migrate, list, and
uninstall must be run on a disposable Frappe v15 bench before this app can be
treated as release-ready.

## Planned verification

```bash
bench --site <disposable-site> install-app lenerp_core
bench --site <disposable-site> migrate
bench --site <disposable-site> list-apps
bench --site <disposable-site> uninstall-app lenerp_core --yes
```

Do not place passwords, API keys, private keys, tokens, or Champion records in
this repository.

## Phase 04 role-based workspace

Version `0.3.0` adds the version-controlled Champion role/home registry and
the `/champion-home` presentation route. It is server-controlled and remains
off unless the ERP site configuration explicitly sets
`lenerp_phase4_workspace_enabled=1`. An optional JSON object in
`lenerp_phase4_role_rollout` enables named roles independently, for example
`{"Champion Dispatcher": true}`. With the flag off, the existing
`Champion ERP` Workspace remains the rollback surface.

The home API reads authorized ERPNext/HRMS records in place. It does not copy
operational records into LenERP or create a second task, employee, payroll, or
inventory system. Missing optional applications are rendered as
`Pending configuration`.
