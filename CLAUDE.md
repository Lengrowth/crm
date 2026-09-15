# LenERP — Project Operations Reference

## Phase 0 handover — read this first

This repository has a verified Phase 0 release-safety foundation. The current
result is **CONDITIONAL PASS**: staging is operational, production was not
promoted, credential rotation is intentionally deferred, and the public API
hostname still has a Cloudflare edge TLS problem.

Never print, paste, commit, or place credential values in logs, documentation,
patches, shell history, or chat. Retrieve secrets only from the approved secret
store/password manager. Do not rotate or invalidate credentials unless the
owner explicitly re-authorizes it; rotation remains mandatory before Champion
confidential data is received, restored, copied, or imported.

Preserve unrelated work. The current CRM checkout intentionally has an
uncommitted `frontend/tsconfig.tsbuildinfo` change. Do not run `git reset
--hard`, `git clean`, destructive checkout commands, or broad deletion.

Do not edit the production Frappe or ERPNext worktrees. They contain preserved
tracked and untracked drift and have no configured upstream remote. Never clean
or reset them to make a check pass. Do not perform production migrations,
database/schema changes, public DNS changes, or production pointer switches as
part of Phase 0.

## Repository and release state

- Workspace: `C:\Users\smikl\Desktop\Work\crm`
- Requested GitHub repository: `https://github.com/Lengrowth/crm`
- Local `origin`: `https://github.com/BuildGrowthNow/crm.git`
- Local `lengrowth` remote: `https://github.com/Lengrowth/crm.git`
- Branch: `main`; pushes to `main` deploy the exact commit to staging only.
- Production promotion is separate and protected: `.github/workflows/promote-saas-control-production.yml` and `scripts/deploy/promote_saas_control.sh`.
- Last verified staging candidate: `265a9047bb7b4d4cc034be3501b61c0f314cf83f`.
- Verified previous staging candidate: `b6e96b628513e7033949d711fd845f5a4fe4125b`.
- Successful exact-candidate runs: GitHub Actions `34970823140` (latest),
  `34968621678`, and repeat/idempotency run `34968811226`.

Useful local checks:

```powershell
git status --short                 # preserve existing changes
git remote -v
python scripts/release/secret_scan.py
git diff --check
```

## EC2 access and safety

- Instance: `i-0f54fba441caa7154`
- Public IP: `100.62.163.246`
- Region: `us-east-1`
- Key: `C:\Users\smikl\lenquant.pem`
- Key pair: `lenquant`
- Security group: `sg-0387e9287e4817700` (`lenerp-sg`)
- Existing approved SSH source: `188.169.243.84/32`
- The temporary workstation SSH rule was removed after Phase 0. If access is
  needed again, authorize only the current workstation public `/32`, use it,
  then revoke that exact rule:

```powershell
ssh -i "C:\Users\smikl\lenquant.pem" ubuntu@100.62.163.246
# after the work:
aws ec2 revoke-security-group-ingress --region us-east-1 `
  --group-id sg-0387e9287e4817700 --protocol tcp --port 22 `
  --cidr CURRENT_WORKSTATION_IP/32
```

Do not remove `188.169.243.84/32`. Keep the PEM private and never print it.
AWS CLI access is available for this EC2/security-group inspection and narrow
security-group changes. SSM was not authorized, so SSH is the approved access
path.

## Production as-built map — read-only by default

The same EC2 hosts both production systems:

| Component | Location/service | Production ports/routes |
|---|---|---|
| Control-plane source | `/opt/saas-control/repo` | backend `8001`, frontend `3000` |
| Control-plane env | `/opt/saas-control/shared/env/backend.env`, `frontend.env` | never print values |
| Control-plane services | `saas-backend.service`, `saas-frontend.service` | production only |
| Frappe bench | `/home/frappe/frappe-bench` | web `8000`, socketio `9000` |
| Production site | `/home/frappe/frappe-bench/sites/erp.lengrowth.com` | `erp.lengrowth.com`, `*.erp.lengrowth.com` |
| Frappe process manager | Supervisor groups `frappe-bench-web`, `frappe-bench-workers`, `frappe-bench-redis` | production only |
| Database | MariaDB 10.6.23 | production site database; do not alter casually |

Production source revisions are Frappe
`edae775dd36b6c4ad7acab10230262bd74040765` and ERPNext
`945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`. The production worktrees are
dirty by design from pre-existing changes. Clean detached reference clones are
available locally at:

- `C:\Users\smikl\Desktop\Work\phase0-upstreams\frappe`
- `C:\Users\smikl\Desktop\Work\phase0-upstreams\erpnext`

Safe production inspection:

```bash
sudo supervisorctl status
sudo ss -ltnp
curl -fsS https://lenerp.lengrowth.com/
curl -fsS https://erp.lengrowth.com/
curl -sS -o /dev/null -w '%{http_code}\n' \
  https://erp.lengrowth.com/api/method/frappe.auth.get_logged_user
```

Do not use the existing production bench as a staging bench. Any production
restart, migration, source edit, or database operation requires a separately
approved change and verified backup/rollback target.

## EC2 staging map — safe operational lane

Staging is isolated on the same EC2 by path, database, files, processes, ports,
Redis instances, environment files, and host-header policy. Use synthetic data
only.

### Control plane staging

- Root: `/opt/saas-control-staging`
- Releases: `/opt/saas-control-staging/releases/<commit>`
- Current/previous pointers: `/opt/saas-control-staging/current`,
  `/opt/saas-control-staging/previous`
- Database: `/opt/saas-control-staging/shared/data/control-plane-staging.db`
- Env: `/opt/saas-control-staging/shared/env/staging-backend.env` and
  `staging-frontend.env`; values must not be printed.
- Services: `saas-control-staging-backend.service`,
  `saas-control-staging-frontend.service`
- Ports: backend `127.0.0.1:18001`, frontend `127.0.0.1:13001`
- Host-header equivalent: `staging.example.test`
- Smoke: `scripts/release/smoke.sh`

The deploy script builds an immutable candidate, runs preflight/migrations,
switches the pointer atomically, runs authenticated smoke, and restores the
previous pointer after a failed health check:

```bash
DEPLOY_TARGET=staging ./scripts/deploy/deploy_saas_control.sh
```

The staging auth bearer is generated for a synthetic account, stored only under
`/run/saas-control-staging/smoke/auth-token`, and never printed or committed.

### ERP staging

- Bench: `/opt/frappe-staging-bench`
- Site: `erp-staging.example.test`
- Separate MariaDB schema: `erp_staging_example_test`
- Site files: `/opt/frappe-staging-bench/sites/erp-staging.example.test`
- Web: `127.0.0.1:28000`
- Redis cache/queue: `127.0.0.1:14100/14101`
- Services: `frappe-staging-web.service`,
  `frappe-staging-redis-cache.service`,
  `frappe-staging-redis-queue.service`,
  `frappe-staging-worker-short.service`,
  `frappe-staging-schedule.service`
- Installed apps: Frappe `15.119.1`, ERPNext `15.120.0`, `lenerp_core 0.1.0`
- Pinned Frappe commit: `edae775dd36b6c4ad7acab10230262bd74040765`
- Pinned ERPNext commit: `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`
- Smoke: `scripts/release/erp_staging_smoke.sh`

Run the ERP smoke from the EC2 after copying or checking out the repository:

```bash
sudo /opt/frappe-staging-bench/erp-staging-smoke.sh
```

The production site and production Redis ports must never be reused by this
lane.

## Backups and Cloudflare R2

The chosen off-host destination is Cloudflare R2, not S3.

- Account: Lengrowth
- Dedicated bucket: `lenerp-phase0-backups`
- ERP prefix: `erp/2026-09-15/erp.lengrowth.com/`
- Control-plane prefix: `control-plane/2026-09-15/`
- Contents: site-config backup, database dump, public files, private files,
  and `saas_control.db`
- All five objects were byte-hash verified against the EC2 sources.
- Restore rehearsal passed outside production: SQL imported into a disposable
  MariaDB schema with 707 tables; files/config validated; temporary targets
  were removed.

Wrangler is available through the project-local invocation; never expose its
OAuth/token material:

```powershell
npx --yes wrangler@latest whoami
npx --yes wrangler@latest r2 bucket list
npx --yes wrangler@latest r2 object list lenerp-phase0-backups
```

R2 lifecycle retention is configured for 90 days on both `erp/` and
`control-plane/` prefixes. Matt Newcomer approved that policy per the delivery
owner's instruction. Non-interactive backup automation credentials and a second
independent restore operator still need explicit operational confirmation.

## Known blockers and handoff actions

1. **Cloudflare API edge TLS:** `https://api.lenerp.lengrowth.com/health`
   fails at the Cloudflare edge while the EC2 origin is healthy. The connected
   Wrangler identity had only zone-read scope and could not inspect or change
   DNS/SSL settings. Wrangler has no DNS-record command for this zone. In the
   Cloudflare dashboard select account `Lengrowth` → zone `lengrowth.com`:
   verify `api.lenerp` is an `A` record for `100.62.163.246` with Proxy status
   enabled; under **SSL/TLS → Overview** use **Full (strict)**; under
   **SSL/TLS → Edge Certificates** verify Universal SSL is active and covers
   `*.lengrowth.com`, then use the certificate retry/refresh action if the
   certificate is pending or errored. If using a token instead of the
   dashboard, grant only zone-scoped `DNS:Edit`, `Zone Settings:Edit`, and
   `SSL/TLS Certificates:Edit` permissions for `lengrowth.com`. Verify from a
   terminal with `curl.exe -Iv https://api.lenerp.lengrowth.com/health` and
   expect HTTP 200 before repeating public authenticated smoke.
2. **Credential rotation:** intentionally not performed. It is mandatory before
   Champion confidential data; do not silently mark this complete.
3. **Production source ownership:** production Frappe/ERPNext drift was
   reviewed. White-label branding and removal of vendor-promotional banners
   were retained and committed locally; help/video/payment functionality and
   accidental backup artifacts were restored/deleted. Production trees are
   clean at Frappe `a5524bdb8c4df252bf0a76bcfdcdc9715c9c389b` and ERPNext
   `0fd1992505bd680432363134063d01b0c755008c`; do not push client changes to
   the official upstream remotes.
4. **`lenerp_core` ownership:** private remote is now
   `https://github.com/Len-OS/lenerp_core.git`, with clean `main` at
   `728de29176ddb9c05c78d734318406d57f10f205`.
5. **Production release rollback:** resolved for the control plane. Production
   `current` is `265a9047bb7b4d4cc034be3501b61c0f314cf83f` and `previous` is
   `1c3ea4d570e08443a8100acb1ecdf506c30a4ca5`; both are immutable release
   directories and services use the `current` pointer.
6. **Acceptance records:** the local six-page agreement PDF `FG-CWD-2026-0915-ONE`
   exists and names Matt Newcomer as final acceptance authority, but its extracted
   signature/date lines are blank and no cleared-payment or DocuSign completion
   certificate is available. Commencement and acceptance therefore remain open.

Primary records:

- `docs/champion_execution/releases/PLAT-P0.md`
- `docs/champion_execution/DECISION_BLOCKER_RISK_REGISTER.md`
- `docs/champion_execution/HANDOVER_INVENTORY.md`
- `ops/staging/README.md`

## Infrastructure Overview

| Service | URL | Notes |
|---|---|---|
| LenERP (ERPNext) | https://erp.lengrowth.com | ERPNext v15, Frappe v15 |
| LenERP Portal (Next.js) | https://lenerp.lengrowth.com | FastAPI + Next.js |
| Champion Forecast | deployed via Vercel | auto-deploy on push to main |

## SSH — EC2 Server

```bash
ssh -i "C:/Users/smikl/lenquant.pem" ubuntu@100.62.163.246
```

- OS: Ubuntu 22.04, region us-east-1
- Elastic IP: `100.62.163.246`
- ERPNext runs under user `frappe`
- Bench dir: `/home/frappe/frappe-bench/`
- Site: `erp.lengrowth.com`

**Switch to frappe user:**
```bash
sudo su - frappe
cd /home/frappe/frappe-bench
```

**Restart ERPNext services only after an approved production change:**
```bash
sudo supervisorctl restart all
# or specific:
sudo supervisorctl restart frappe-web:
sudo supervisorctl restart frappe-worker-default:
```

**Rebuild assets after code changes:**
```bash
sudo -u frappe bash -c "cd /home/frappe/frappe-bench && bench build --app erpnext"
```

**Run migrations after DB changes:**
```bash
sudo -u frappe bash -c "cd /home/frappe/frappe-bench && bench --site erp.lengrowth.com migrate"
```

**Clear cache:**
```bash
sudo -u frappe bash -c "cd /home/frappe/frappe-bench && bench --site erp.lengrowth.com clear-cache"
```

## ERPNext — Edit via Bench Console

These are legacy operational references, not Phase 0 instructions. Do not use
them to make unreproducible production customizations or change production
data during release-safety work. Prefer source, fixtures, patches, or staging.

```bash
sudo -u frappe bash -c "cd /home/frappe/frappe-bench && bench --site erp.lengrowth.com console"
```

Inside console:
```python
# Read a setting
frappe.db.get_single_value("System Settings", "app_name")

# Write a setting (always commit!)
frappe.db.set_single_value("System Settings", "app_name", "LenERP")
frappe.db.commit()

# Count records
frappe.db.count("Customer")
```

**Important:** bench console runs `frappe.db.rollback()` on exit. Always call `frappe.db.commit()` before exiting.

## ERPNext — Edit via MariaDB

Never obtain or print the production DB password from this document. Direct SQL
against production requires an approved change, verified backup, and rollback
or restore plan. Use the disposable staging schema for rehearsal.

```bash
mysql -u root -p <database-name-from-approved-runbook>
```

**Key tables:**
- `tabSingles` — site-wide settings (System Settings, Website Settings, Navbar Settings)
- `tabWorkspace` — sidebar menu items
- `tabOnboarding Step` — setup wizard steps
- `tabNavbar Item` — top-right dropdown items

**Update a setting (tabSingles has NO unique constraint — always UPDATE not INSERT):**
```sql
UPDATE tabSingles SET value='LenERP' WHERE doctype='System Settings' AND field='app_name';
```

## ERPNext — Edit Template Files

Do not edit files under the production Frappe/ERPNext app trees during Phase 0;
those trees already contain preserved drift. Make reproducible changes in a
custom app or explicitly approved source branch.

```
/home/frappe/frappe-bench/apps/erpnext/erpnext/templates/
/home/frappe/frappe-bench/apps/frappe/frappe/templates/
```

HTML/Jinja changes are live immediately (no restart needed).

Static assets (logos, SVGs):
```
/home/frappe/frappe-bench/apps/erpnext/erpnext/public/images/
/home/frappe/frappe-bench/sites/erp.lengrowth.com/public/files/
```

## ERPNext Credentials

Credential values are intentionally not stored in this document. Retrieve them
from the approved secret store or operator password manager only when needed.
Known exposed credentials remain deferred for this Phase 0 run and must be
rotated before any Champion confidential data is received, restored, copied, or
imported. Record only secret references and rotation evidence in release records.

DB name: retrieve from the approved runbook or secret store when authorized; do not record it here.

## Cloudflare

**Zone:** `lengrowth.com`

**Disable cache for live testing:**
Dashboard → Caching → Configuration → Development Mode → Enable (3 hours)

**DNS:**
- `erp.lengrowth.com` → `100.62.163.246` (proxied)
- `lenerp.lengrowth.com` → `100.62.163.246` (proxied)
- `api.lenerp.lengrowth.com` → proxied to the same EC2 origin; public TLS is
  currently failing at the Cloudflare edge and requires DNS/SSL-capable access.

**Purge specific URL:**
Dashboard → Caching → Cache Rules → Purge Cache → Custom Purge

## AWS

**EC2 instance:** AWS Console → EC2 → Instances → filter `100.62.163.246`
- Type: t3.large, Region: us-east-1
- Key pair: `lenquant.pem` at `C:\Users\smikl\lenquant.pem`
- Security group: inbound 22, 80, 443 required

SSH is restricted to approved source `/32` rules; never open port 22 broadly.
Do not change production DNS during a rehearsal.

## Champion Forecast (Vercel)

Repo: `github.com/guerra2fernando/champion-forecast`
Local: `C:\Users\smikl\Desktop\Work\champion-forecast`

Push to `main` auto-deploys. Proposal page: `src/app/proposal/page.tsx`

## Branding — LenERP (rebranded from ERPNext)

Branding locations:
1. **DB tabSingles:** System Settings, Website Settings, Navbar Settings — app_name, app_logo, favicon
2. **Logo files:** `/home/frappe/frappe-bench/sites/erp.lengrowth.com/public/files/lenerp-logo.png`
3. **SVG fallback:** `/home/frappe/frappe-bench/apps/erpnext/erpnext/public/images/erpnext-logo.svg` (replaced)
4. **Footer template:** `/home/frappe/frappe-bench/apps/erpnext/erpnext/templates/includes/footer/footer_powered.html` (cleared)
5. **JS injection:** Website Settings → website_script replaces remaining ERPNext text nodes at runtime
