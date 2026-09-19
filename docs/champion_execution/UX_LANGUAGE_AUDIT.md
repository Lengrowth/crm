# Customer-facing UX language audit

Status: **implemented in the pre-kickoff remediation branch; protected staging evidence required for independent re-review**

Scope: public marketing and onboarding pages, authentication and recovery, the
reseller/operator shell, company and ERP-site pages, module selection, account
settings, and the Champion ERP browser surfaces.

## Changes made

- Account Settings no longer exposes release identifiers, commit hashes, build
  environments, feature-flag state, or phase labels. It now uses customer terms
  such as Demo workspace, Live workspace, Service status, Security, and Support.
- Module selection no longer shows module codes, entitlement terminology,
  preview hashes, internal marketed/internal badges, or ERP verification
  language. It now uses Available modules, Selected modules, Included, Ready,
  Setup in progress, and Review your changes.
- Company module history now presents business-facing module choice updates
  without source types, internal codes, or before/after payloads.
- Public onboarding now uses Workspace setup, Requested capabilities, and Send
  for review. It no longer describes tenant, entitlement, invoice, or raw
  provisioning internals to applicants.
- The protected browser evidence script audits customer-facing route text for
  release IDs, package IDs, phase labels, feature-flag names, commit-hash,
  readback, isolated-synthetic-execution, and raw-JSON language.

## Route coverage

| Surface | Routes or screens | Result |
|---|---|---|
| Public marketing | Home, product, modules, industries, Champion well drilling, contact, privacy, terms | Reviewed; business language retained |
| Public intake | `/onboarding`, request confirmation, request access code | Updated; no setup is implied before review |
| Authentication | Login, sign-up, forgot password, reset password, verification, resend verification | Reviewed; protected browser capture includes login |
| Reseller/operator shell | Dashboard, companies, ERP sites, company details, module selection, settings, mobile navigation | Reviewed; customer-visible settings/module copy updated |
| Operator-only delivery | Implementation portfolio, onboarding queue, site setup history | Restricted operational terminology retained for authorized operators; non-admin denial is part of the protected browser gate |
| ERP browser | Login, authenticated Champion routes, responsive well/job/inventory/accounting/asset screens, print and export surfaces | Route-by-route accessibility and terminology evidence captured by the protected ERP browser script |
| States and overlays | Empty, loading, partial failure, denied, not-found, dialogs, mobile navigation | Exercised by the protected browser evidence workflow |

## Review rule

Platform diagnostics may contain deployment identity and operational detail only
when access is restricted to platform administrators. Customer and Champion
users should see business terms such as Companies, ERP workspaces, Available
modules, Setup progress, Customers, Wells and sites, Jobs, Inventory,
Equipment, Quotes and invoices, and Reports.

## Final audit result

Protected main run [35457401709](https://github.com/Lengrowth/crm/actions/runs/35457401709) found no technical/internal language findings on the audited customer-facing routes. The result is bound to CRM `dccff421027527860075c0c2de4ce08deccf5423` and LenERP Core `26f41e34deab5fc699224657d206bd6a9d7bf161`; restricted administrator diagnostics remain permitted only in restricted views.
