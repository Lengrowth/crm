# Phase Deployment Gate

Copy this checklist into the phase release record. All required items must be checked or explicitly waived with an owner and reason.

## Release identity

- Phase:
- Release type: Platform / Champion package / Data / Final
- Release/commit:
- Champion package IDs:
- Data stage/source/batch IDs:
- Database revision before/after:
- Upstream Frappe/ERPNext commits:
- Custom-app version before/after:
- Feature flags changed:
- Data/import batch IDs affected:
- Operator:
- Approver:
- Planned production window:
- Previous known-good release:
- Temporary/final hostname affected:
- Commercial classification and approval, when applicable:

## Before implementation

- [ ] Acceptance scenarios and rollback triggers are written.
- [ ] Package/stage IDs, owners, dependencies, and commercial classification are recorded.
- [ ] Current production health and key route/API responses are recorded.
- [ ] Work is isolated on a branch; no direct production edits are required.
- [ ] Database change is additive/backward compatible or has a separately rehearsed recovery plan.
- [ ] Code rollback and data recovery/correction are documented separately.
- [ ] Upstream `frappe` and `erpnext` worktrees are clean; LenERP changes exist only in approved repositories/apps.
- [ ] New functionality defaults off when incomplete.
- [ ] No undocumented production-only configuration is required for this release.
- [ ] Hostnames, product name, callbacks, cookies, generated links, and service URLs are configuration rather than hardcoded assumptions.
- [ ] If Champion data is affected, secure receipt/access/retention are approved and exposed credentials have been rotated.

## Local and CI validation

- [ ] Backend tests pass.
- [ ] Frontend typecheck and production build pass.
- [ ] New automated tests cover success, authorization failure, validation failure, and retry where relevant.
- [ ] Secret/dependency scan finds no newly committed secrets or unacceptable dependency change.
- [ ] Migration upgrade and downgrade/restore strategy is reviewed.

## Staging validation

- [ ] Staging uses the exact candidate commit/artifacts.
- [ ] Staging configuration matches production structure without copying unsafe secrets.
- [ ] Database migration succeeds on a recent restored or representative database.
- [ ] Existing phase smoke tests still pass.
- [ ] New phase acceptance tests pass.
- [ ] Old URLs/APIs still work or redirect as documented.
- [ ] Temporary and final hostname behavior is tested when domain configuration is affected.
- [ ] Role and tenant-isolation negative tests pass.
- [ ] Logs contain no new repeated errors or sensitive values.
- [ ] Rollback to the previous release is rehearsed when release mechanics or schema behavior changed.

## Production promotion

- [ ] Full application/database/files backup completed and off-host copy verified.
- [ ] Backup contains the ERP database, site configuration, public files, and private files when the ERP site is affected.
- [ ] Previous release artifact and exact rollback procedure are available.
- [ ] Maintenance/communication plan is active if any interruption is possible.
- [ ] Candidate is built and health-checked before receiving production traffic.
- [ ] Database migration completed without destructive cleanup.
- [ ] Traffic/service pointer switched to the candidate.
- [ ] nginx configuration test passes before reload.
- [ ] DNS/TLS/cookie/CSRF/CORS/callback/webhook changes have an exact rollback when the domain is affected.

## Production smoke tests

- [ ] Public website and login load through Cloudflare.
- [ ] Authenticated `/app` loads and session behavior works.
- [ ] Backend health and ERP runtime checks pass.
- [ ] Existing organization, tenant, module, implementation, and settings routes work.
- [ ] One read and one authorized write succeed for affected features.
- [ ] Unauthorized access remains denied.
- [ ] Background/provisioning jobs remain healthy when affected.
- [ ] Origin/systemd/nginx/application logs remain healthy during observation.
- [ ] External monitoring confirms availability from outside the server.
- [ ] Module state is reported accurately as marketed/requested/entitled/applied/verified when modules are affected.
- [ ] Import counts, reconciliation, retry, and correction evidence is saved when data is affected.

## Rollback triggers

Rollback immediately for any of the following unless the approved operator records a safer action:

- login or authenticated app unavailable;
- repeated 5xx responses or failed health checks;
- migration corruption or unexplained data loss;
- authorization or tenant-isolation regression;
- background jobs repeatedly failing or duplicating irreversible actions;
- frontend cannot complete the existing critical path;
- origin, nginx, backend, or frontend fails to remain healthy.

## Completion

- [ ] Release record and evidence links saved.
- [ ] Production observation completed.
- [ ] Feature flag left in the intended state.
- [ ] Decision/blocker/defect registers updated.
- [ ] Next phase baseline updated from the actual deployed state.
- [ ] Champion solution and data migration registers updated from the actual result.
- [ ] Handover inventory updated for new code, configuration, dependency/license, operational, or known-limitation changes.
