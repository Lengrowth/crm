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
