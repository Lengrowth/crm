# LenERP — Project Operations Reference

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

**Restart ERPNext services:**
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

**Purge specific URL:**
Dashboard → Caching → Cache Rules → Purge Cache → Custom Purge

## AWS

**EC2 instance:** AWS Console → EC2 → Instances → filter `100.62.163.246`
- Type: t3.large, Region: us-east-1
- Key pair: `lenquant.pem` at `C:\Users\smikl\lenquant.pem`
- Security group: inbound 22, 80, 443 required

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
