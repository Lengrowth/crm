# Phase 08 — End-to-End UX Certification and Matt Demo

## AI goal

Certify the exact staging candidate and produce a concise, reliable Matt demonstration showing one login, one product, all promised modules, role-aware navigation and the current Champion operational foundation.

## Required demonstration journey

1. Sign in once through the LenERP control plane.
2. Open Champion’s organization and show the module profile with honest Requested/Entitled/Applied/Verified states.
3. Select `Open ERP`; arrive in the authorized Champion ERP workspace without a second password.
4. Demonstrate the Administrator module home and role switch using separate synthetic users rather than permission impersonation.
5. Show Office Board task creation, assignment, comment and Kanban movement.
6. Show Customer → Well → Drilling Job → Materials → Completion/report context.
7. Show Inventory, Buying, Assets, CRM/Selling and Accounting entry points with representative synthetic records.
8. Submit a Support request and a product-update request.
9. Record and progress a Callback/Quality case.
10. Show synthetic Employee/time-off/hours and restricted Payroll access.
11. Return from the ERP user dropdown to the matching control-plane tenant.
12. Show mobile/tablet navigation and one field-oriented form.
13. End with an explicit decision slide/list: what is demonstrated, what needs Matt’s approval, and what is future/advisory.

## Certification matrix

- Exact CRM and `lenerp_core` commits, HRMS/Frappe/ERPNext revisions and database migrations.
- Installed-app readback.
- Module requested/entitled/applied/verified reconciliation.
- SSO success and denial/replay cases.
- Role navigation plus direct-route/API denial.
- Desktop, tablet, mobile, 200% zoom, keyboard and light/dark review.
- Automated accessibility results with manual review of incomplete findings.
- Empty, partial, loading, provider-failure and access-denied states.
- Synthetic seed and exact reset.
- Backup, rollback and break-glass access rehearsal.
- Secret/log scan and confirmation that no real Champion or payroll data is present.

## Demo UX rules

- Use a seeded scenario and deterministic accounts; never troubleshoot live during the meeting.
- Keep the primary walkthrough under 20 minutes and reserve detailed module exploration for questions.
- Avoid technical framework names unless Matt asks.
- Do not call a module complete because its menu exists.
- Keep a static evidence pack and screenshots available if staging connectivity fails.
- Every pending decision names the expected owner: Matt, Pedro/Team or Fernando.

## Acceptance tests

- The exact candidate completes the entire journey without a second password, broken link, dead action or permission bypass.
- All promised modules are visible to the appropriate demonstration role and hidden/denied to others.
- HRMS-dependent modules are verified against installed-app readback.
- Cross-navigation returns to the correct organization and tenant.
- Synthetic reset returns all affected record counts to the manifest baseline.
- Break-glass ERP access works when central SSO is disabled.
- The evidence pack names known limitations and contains no secrets.

## Production boundary

Passing this phase means `PRE-KICKOFF SYNTHETIC MODULE SHOWCASE: READY`. It does not mean Champion acceptance, production identity cutover, real-data authorization, final payroll configuration, Field App delivery or completion of the full proposal.

## Gate and rollback

Record the exact candidate through the generic deployment gate. The demo must run in staging or another approved synthetic environment. Rollback restores the previous control-plane and custom-app candidates, disables SSO/module-showcase flags, verifies break-glass login and runs exact synthetic cleanup.

## Execution prompt

> Certify the exact staging candidate and produce the Matt demo/evidence pack described here. Run the complete one-login, cross-navigation, module, Office Board, Well/Job, Support, Quality, HR and restricted Payroll journey; validate role denials, responsive accessibility, installed-app/module reconciliation, reset and rollback; disclose every pending decision; and do not promote to production or claim Champion acceptance.
