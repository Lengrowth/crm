# 03 — ERPNext Tenant Provisioning And SaaS Connection Runbook

**Project:** ERPNext/Frappe-based vertical SaaS for field operations, drilling, fleet, service work, warehouses, logistics, and similar manual operations businesses  
**Audience:** Fernando / LenGrowth technical and operations team  
**Last updated:** 2026-05-21  
**Status:** MVP-to-production implementation runbook

---

## 1. Purpose

This document explains the missing bridge between the infrastructure runbook and the SaaS/product runbook.

The main question answered here is:

> When a new client pays or starts a trial, how does that become a real ERPNext tenant with its own domain, users, branding, modules, database, backups, and support process?

The desired flow is:

```txt
Client signs up or you manually create client
  ↓
SaaS layer creates a Tenant record
  ↓
Stripe trial/payment/subscription is attached
  ↓
Provisioning process creates a new Frappe site
  ↓
ERPNext is installed on that site
  ↓
Your custom app is installed/enabled
  ↓
Company, logo, users, modules, domain, email, and roles are configured
  ↓
SSL is active
  ↓
Client receives login details
  ↓
Ongoing billing, backups, updates, and support begin
```

At MVP stage, some steps can be manual. Over time, the SaaS layer should automate them.

---

## 2. Key concepts

### 2.1 Frappe

Frappe is the framework. It provides the application runtime, database models, DocTypes, permissions, background jobs, REST APIs, users, roles, workflows, desk UI, reports, and site management.

### 2.2 ERPNext

ERPNext is the ERP application built on Frappe. It provides CRM, sales, purchasing, accounting, inventory, projects, employees, assets, maintenance, reports, and business workflows.

### 2.3 Your custom app

Your app is where your SaaS product lives.

Example names:

```txt
lengrowth_fieldops
fieldops_core
drilling_ops
ops_platform
```

It should contain reusable modules:

```txt
Field Operations
Drilling
Fleet
Service Work Orders
Warehouse Operations
QuickBooks Integration
SaaS Module Entitlements
Tenant Branding Settings
White Label Settings
```

### 2.4 Frappe site

A client/tenant is normally represented by a **Frappe site**.

Example:

```txt
demo.lengrowth.com
drilling-client-1.lengrowth.com
ops.clientcompany.com
```

Each site has:

```txt
Own database
Own site_config.json
Own company setup
Own users
Own ERPNext data
Own logo/settings
Own domain(s)
```

This is good for SaaS because clients are isolated at database/site level.

### 2.5 SaaS control layer

The SaaS layer is your central control system.

It does **not** replace ERPNext. It controls ERPNext tenants.

It stores metadata such as:

```txt
Client name
Tenant/site name
Custom domain
Billing status
Stripe customer ID
Stripe subscription ID
Plan
Enabled modules
Provisioning status
Deployment server
Backup status
Health status
Support status
```

---

## 3. Recommended MVP architecture

At the beginning, one VM is enough.

```txt
Google Cloud VM
  ├── Reverse proxy / Traefik / Nginx
  ├── ERPNext/Frappe stack
  ├── MariaDB
  ├── Redis
  ├── Workers
  ├── Scheduler
  ├── SaaS control app or admin scripts
  └── Backups to Google Cloud Storage
```

Sites/domains:

```txt
app.yourdomain.com              → SaaS admin/control panel
demo.yourdomain.com             → demo ERP tenant
drilling-client.yourdomain.com  → first real ERP tenant
clientdomain.com                → white-label custom domain
```

Later, split into:

```txt
VM 1: SaaS admin/app
VM 2: ERP tenants 1–20
VM 3: ERP tenants 21–40
VM 4: dedicated enterprise client
Managed Redis
Dedicated MariaDB or HA database layer
```

Do not split too early. First prove the workflow.

---

## 4. Tenant lifecycle states

Your SaaS layer should track each tenant with a clear lifecycle.

Recommended full state list:

```txt
lead
trial_requested
payment_pending
provisioning_queued
provisioning_started
site_created
apps_installed
setup_pending
setup_complete
active
grace_period
suspended
cancelled
archived
failed
deleted
```

Minimum MVP states:

```txt
pending
provisioning
active
suspended
failed
cancelled
```

Suggested table if the SaaS layer is built outside Frappe:

```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY,
  client_name TEXT NOT NULL,
  legal_company_name TEXT,
  site_name TEXT UNIQUE NOT NULL,
  primary_domain TEXT UNIQUE NOT NULL,
  custom_domain TEXT UNIQUE,
  status TEXT NOT NULL,
  plan_code TEXT NOT NULL,
  enabled_modules JSONB,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  admin_email TEXT NOT NULL,
  admin_full_name TEXT,
  deployment_server TEXT,
  frappe_db_name TEXT,
  last_backup_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);
```

If you build the SaaS admin layer in Frappe itself, use DocTypes instead:

```txt
SaaS Tenant
SaaS Plan
SaaS Module
SaaS Subscription
SaaS Provisioning Job
SaaS Deployment Server
SaaS Domain Mapping
SaaS Backup Record
SaaS Incident
```

---

## 5. Manual MVP provisioning flow

Manual provisioning is acceptable for the first 1–3 clients if it is documented and repeatable.

### 5.1 Collect information before provisioning

Collect:

```txt
Client display name
Legal company name
Admin full name
Admin email
Primary phone
Desired subdomain
Desired custom domain, if any
Logo file
Company address
Country and currency
Fiscal year start
Chart of accounts preference
Modules purchased
Implementation template
Plan
Trial or paid status
```

Example:

```txt
Client: ABC Drilling LLC
Site: abc-drilling.yourdomain.com
Custom domain: ops.abcdrilling.com
Admin: Maria Silva <maria@abcdrilling.com>
Plan: Pro
Modules: CRM, Field Ops, Drilling, Fleet, Inventory, QuickBooks
Template: Drilling Company Basic
```

### 5.2 Prepare DNS

For your own subdomain:

```txt
abc-drilling.yourdomain.com → A record → VM static IP
```

For a white-label client domain:

```txt
ops.abcdrilling.com → CNAME → abc-drilling.yourdomain.com
```

or:

```txt
ops.abcdrilling.com → A record → VM static IP
```

If the client uses Cloudflare:

```txt
Set record to DNS Only while testing SSL.
After SSL works, enable Cloudflare proxy if desired.
```

### 5.3 Create the Frappe site

Standard bench example:

```bash
cd ~/frappe-bench

bench new-site abc-drilling.yourdomain.com \
  --admin-password 'CHANGE_THIS_STRONG_PASSWORD' \
  --mariadb-root-password 'MARIADB_ROOT_PASSWORD'
```

Frappe Docker example pattern:

```bash
docker compose exec backend bench new-site abc-drilling.yourdomain.com \
  --admin-password 'CHANGE_THIS_STRONG_PASSWORD' \
  --mariadb-root-password 'MARIADB_ROOT_PASSWORD'
```

The site name should normally match the primary hostname.

Good:

```txt
abc-drilling.yourdomain.com
demo.yourdomain.com
ops.clientdomain.com
```

Avoid:

```txt
client1
test123
new-site-final
```

### 5.4 Install ERPNext

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com install-app erpnext
```

Verify:

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com list-apps
```

Expected:

```txt
frappe
erpnext
```

### 5.5 Install your custom app

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com install-app lengrowth_fieldops
```

Verify:

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com list-apps
```

Expected:

```txt
frappe
erpnext
lengrowth_fieldops
```

### 5.6 Run migration

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com migrate
```

This applies schema changes, custom DocTypes, fixtures, roles, patches, and app updates.

### 5.7 Add custom domain

If the client uses:

```txt
ops.abcdrilling.com
```

Add domain to the site.

Pattern:

```bash
docker compose exec backend bench setup add-domain ops.abcdrilling.com \
  --site abc-drilling.yourdomain.com
```

Depending on your proxy setup, you may need to regenerate Nginx or update Traefik labels/config.

With Nginx/bench:

```bash
docker compose exec backend bench setup nginx
docker compose restart frontend
```

With Traefik/wildcard routing, the Docker labels may already handle routing. Still test carefully.

### 5.8 Confirm site routing

Open:

```txt
https://abc-drilling.yourdomain.com
https://ops.abcdrilling.com
```

Check:

```txt
Login page loads
Correct site loads
No wrong tenant appears
No certificate warning
No 502/503 errors
```

### 5.9 Complete ERPNext setup wizard

Set:

```txt
Country
Timezone
Currency
Company name
Chart of accounts
Fiscal year
Admin user
Language
```

For MVP, this can be manual. Later, automate it through scripts/API/fixtures.

### 5.10 Configure company profile

Inside ERPNext:

```txt
Company name
Abbreviation
Default currency
Tax ID
Address
Contact details
Letterhead
Logo
Default bank/cash accounts
Fiscal year
Terms and conditions
```

### 5.11 Configure white-label basics

Minimum:

```txt
Website Settings logo
Company logo
Letterhead logo
Print format logo
Email header/footer logo
Favicon, if supported in your theme/customization
```

For deeper white label, create a **Tenant Branding Settings** DocType:

```txt
Tenant name
Primary logo
Small logo
Favicon
Primary color
Secondary color
Login background
Support email
Sender name
Custom domain
Hide ERPNext branding flag
```

### 5.12 Create users

Create:

```txt
Client Owner / System Manager
Operations Manager
Dispatcher
Field Supervisor
Field Worker
Finance User
Inventory User
Read-only Executive
```

Do not give every user System Manager.

Recommended roles:

```txt
System Manager: only 1–2 trusted admins
Accounts User/Manager: finance people
Sales User/Manager: CRM/sales
Stock User/Manager: warehouse/inventory
Projects User/Manager: jobs/projects
HR User/Manager: employee data
Field Ops Manager: custom role
Field Worker: custom role
Fleet Manager: custom role
Client Portal User: external users
```

### 5.13 Enable modules

There are two layers:

```txt
ERPNext/Frappe module visibility
Your SaaS business module entitlements
```

Recommended model:

```txt
SaaS layer says tenant has: Drilling + Fleet
  ↓
Your custom app stores module entitlements in Tenant Module Settings
  ↓
UI/workspaces/buttons/features are shown or hidden
  ↓
Permissions prevent access to disabled modules
```

Do not rely only on hiding buttons. Enforce access in server logic and permissions too.

### 5.14 Apply implementation template

For drilling:

```txt
Create default roles
Create default workspaces
Create default drilling workflow
Create default job statuses
Create default checklists
Create default item groups
Create default warehouses
Create sample reports/dashboards
Create default print formats
Create default notification templates
```

Example job statuses:

```txt
Lead
Site Survey Required
Quote Sent
Approved
Scheduled
Crew Assigned
In Progress
Paused
Completed
Awaiting Client Sign-off
Ready to Invoice
Invoiced
Closed
Cancelled
```

### 5.15 Configure email

You need transactional email for:

```txt
User invitations
Password resets
Notifications
Invoices
Payment reminders
Daily reports
Approvals
```

MVP options:

```txt
Use Google Workspace SMTP
Use SendGrid/Postmark/Mailgun
Use client SMTP for white-label clients
```

White-label sender requires DNS records:

```txt
SPF
DKIM
DMARC
Return-path/bounce domain if using provider
```

### 5.16 Configure backups

For each tenant, verify backup works:

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com backup --with-files
```

Then copy/upload to cloud storage.

Recommended path:

```txt
gs://your-backup-bucket/frappe/sites/abc-drilling.yourdomain.com/YYYY/MM/DD/
```

Include:

```txt
Database backup
Public files
Private files
site_config.json copy, encrypted or handled carefully
Version metadata
Apps list
```

### 5.17 Provisioning completion checklist

```txt
[ ] DNS resolves
[ ] HTTPS works
[ ] Correct site loads
[ ] ERPNext setup wizard completed
[ ] Company settings completed
[ ] Logo/letterhead configured
[ ] Admin user created
[ ] User roles configured
[ ] Purchased modules enabled
[ ] Default workflows applied
[ ] Email sending tested
[ ] Backup tested
[ ] Restore point created
[ ] Client login tested in incognito browser
[ ] Support/admin access documented
[ ] Tenant marked active in SaaS admin
```

---

## 6. Automated provisioning design

Manual steps are fine for the first clients. After that, automate.

### 6.1 Provisioning job model

Create a provisioning job when a client signs up or an admin clicks **Create Tenant**.

Fields:

```txt
job_id
tenant_id
status
requested_by
site_name
custom_domain
plan_code
enabled_modules
current_step
error_message
started_at
completed_at
logs
retry_count
```

Steps:

```txt
validate_input
validate_dns
create_site
install_erpnext
install_custom_apps
migrate
apply_template
create_company
create_admin_user
apply_branding
configure_modules
configure_email
create_backup
run_health_check
send_welcome_email
mark_active
```

### 6.2 Provisioning must be asynchronous

Provisioning can take time and can fail. Do not run it inside a normal HTTP request.

Use:

```txt
Frappe background job
RQ worker
Separate worker container
Small Python/Node service
```

The SaaS UI should show:

```txt
Provisioning queued
Provisioning started
Creating site
Installing ERPNext
Configuring tenant
Ready
Failed: reason
```

### 6.3 Provisioning pseudo-code

```python
def provision_tenant(tenant_id):
    tenant = get_tenant(tenant_id)

    mark_step(tenant, "validate_input")
    validate_tenant_payload(tenant)

    mark_step(tenant, "validate_dns")
    validate_domain_points_to_server(tenant.primary_domain)

    mark_step(tenant, "create_site")
    run_command([
        "bench", "new-site", tenant.site_name,
        "--admin-password", tenant.generated_admin_password,
        "--mariadb-root-password", get_secret("MARIADB_ROOT_PASSWORD")
    ])

    mark_step(tenant, "install_erpnext")
    run_command(["bench", "--site", tenant.site_name, "install-app", "erpnext"])

    mark_step(tenant, "install_custom_app")
    run_command(["bench", "--site", tenant.site_name, "install-app", "lengrowth_fieldops"])

    mark_step(tenant, "migrate")
    run_command(["bench", "--site", tenant.site_name, "migrate"])

    mark_step(tenant, "apply_template")
    apply_template(tenant.site_name, tenant.template_code)

    mark_step(tenant, "create_admin_user")
    create_admin_user(tenant.site_name, tenant.admin_email)

    mark_step(tenant, "apply_branding")
    apply_branding(tenant.site_name, tenant.branding)

    mark_step(tenant, "configure_modules")
    configure_modules(tenant.site_name, tenant.enabled_modules)

    mark_step(tenant, "backup")
    create_initial_backup(tenant.site_name)

    mark_step(tenant, "health_check")
    assert_site_healthy(tenant.primary_domain)

    mark_active(tenant)
    send_welcome_email(tenant)
```

### 6.4 Command execution safety

Never do this:

```python
os.system("bench new-site " + user_input)
```

Do this:

```python
subprocess.run(["bench", "new-site", safe_site_name], check=True)
```

Validate:

```txt
site_name only uses approved domain/subdomain
custom_domain is DNS-valid
email is valid
plan exists
modules exist
no shell metacharacters
```

### 6.5 Store secrets securely

Do not store these in plain text:

```txt
MariaDB root password
Frappe admin password
Stripe secrets
Email provider secrets
OAuth secrets
QuickBooks tokens
Google Cloud service account keys
```

Use:

```txt
Google Secret Manager
Environment variables
Encrypted fields
Restricted IAM
```

---

## 7. SaaS ↔ ERPNext connection model

### 7.1 SaaS layer owns

```txt
Plan
Subscription
Payment status
Tenant status
Provisioning status
Enabled modules
Custom domain
Deployment server
Billing contact
Support tier
```

### 7.2 ERPNext tenant owns

```txt
Users
Customers
Suppliers
Sales
Purchasing
Inventory
Accounting
Projects
Field jobs
Drilling logs
Vehicles
Reports
Attachments
Daily work data
```

### 7.3 Sync direction

```txt
SaaS → ERPNext:
  plan changes
  module entitlements
  suspension/reactivation
  branding
  support metadata

ERPNext → SaaS:
  health status
  usage metrics
  backup status
  module usage
  storage usage
  user count
```

### 7.4 Minimum API endpoints

Create protected methods in your custom app:

```txt
GET /api/method/lengrowth_fieldops.api.health
POST /api/method/lengrowth_fieldops.api.apply_plan
POST /api/method/lengrowth_fieldops.api.apply_branding
POST /api/method/lengrowth_fieldops.api.enable_modules
POST /api/method/lengrowth_fieldops.api.suspend_tenant
POST /api/method/lengrowth_fieldops.api.reactivate_tenant
GET /api/method/lengrowth_fieldops.api.usage_summary
```

### 7.5 Authentication between SaaS and tenant sites

Options:

```txt
Per-tenant API key/secret
OAuth client
Internal service token
Signed webhook payloads
```

MVP:

```txt
Create one integration user per tenant:
  integration@yourdomain.com

Assign limited role:
  SaaS Integration

Store API key/secret in the SaaS control layer securely.
```

Do not use Administrator credentials for ongoing automation.

---

## 8. Stripe billing connection

Stripe controls billing. Your SaaS controls tenant status.

### 8.1 Signup flow

```txt
User selects plan
  ↓
Stripe Checkout creates subscription/trial
  ↓
Stripe webhook confirms checkout.session.completed
  ↓
SaaS creates tenant record
  ↓
Provisioning job starts
  ↓
Tenant becomes active
```

### 8.2 Important webhooks

```txt
checkout.session.completed
customer.subscription.created
customer.subscription.updated
customer.subscription.deleted
invoice.payment_succeeded
invoice.payment_failed
customer.updated
```

### 8.3 Billing states

```txt
Stripe trialing       → tenant active/trial
Stripe active         → tenant active
Stripe past_due       → tenant grace_period
Stripe unpaid         → tenant suspended
Stripe canceled       → tenant cancelled
Stripe incomplete     → payment_pending
```

### 8.4 Grace period

Recommended:

```txt
Day 0: payment failed → notify
Day 3: remind
Day 7: restrict admin/banner
Day 14: suspend login or restrict writes
Day 30: archive/export discussion
Day 60+: deletion according to contract
```

### 8.5 Suspension behavior

```txt
Block normal user logins or show billing lock screen
Keep data intact
Keep backups running for retention period
Allow owner/admin to access billing/export page if possible
Do not delete data automatically
```

---

## 9. Module entitlement design

Each module should be controlled by configuration, not by creating different codebases.

Example modules:

```txt
crm
sales
inventory
field_ops
drilling
fleet
maintenance
quickbooks
advanced_reporting
client_portal
white_label
```

Example plans:

```txt
Starter:
  crm
  sales
  field_ops_basic

Pro:
  crm
  sales
  inventory
  field_ops
  fleet
  reports

Drilling Pro:
  crm
  sales
  inventory
  field_ops
  fleet
  drilling
  maintenance
  reports

Enterprise:
  everything
  custom_domain
  white_label
  dedicated support
```

Enforce modules at three layers:

```txt
1. UI visibility:
   Hide workspaces, buttons, dashboards, and reports for disabled modules.

2. Permissions:
   Remove role permissions for disabled modules.

3. Server-side validation:
   Critical API/methods check tenant entitlement before executing.
```

Example:

```python
def require_module(module_code):
    if not tenant_has_module(module_code):
        frappe.throw("This module is not enabled for your subscription.")
```

---

## 10. Updating tenants

When you release a new version:

```txt
Build new image
Deploy to staging
Run migrations on staging tenant
Test workflows
Backup production tenants
Deploy image to production
Run bench migrate per site
Smoke test each site
Monitor errors
```

For many tenants, do not blindly migrate all at once. Use waves:

```txt
Wave 1: internal demo
Wave 2: first friendly client
Wave 3: remaining small clients
Wave 4: enterprise/heavy clients
```

---

## 11. Deleting / archiving tenants

Never delete immediately.

### 11.1 Cancelled tenant process

```txt
[ ] Confirm cancellation
[ ] Disable billing renewal
[ ] Export final data if required
[ ] Take final backup
[ ] Mark tenant cancelled
[ ] Restrict access
[ ] Keep backups for contractual retention period
[ ] Delete site only after retention period and written confirmation
```

### 11.2 Archive site

```bash
docker compose exec backend bench --site abc-drilling.yourdomain.com backup --with-files
```

Copy backup to:

```txt
gs://your-backup-bucket/archived-sites/abc-drilling.yourdomain.com/
```

Record:

```txt
Archive date
Backup file names
Apps version
Frappe version
ERPNext version
Custom app version
Who approved deletion
Retention end date
```

### 11.3 Delete site

Only after confirmation:

```bash
docker compose exec backend bench drop-site abc-drilling.yourdomain.com
```

Use extreme caution. Dropping a site deletes data.

---

## 12. Operational checklists

### 12.1 New tenant checklist

```txt
[ ] Tenant record created
[ ] Stripe subscription/trial attached
[ ] Subdomain selected
[ ] DNS configured
[ ] Site created
[ ] ERPNext installed
[ ] Custom app installed
[ ] Migration completed
[ ] Company configured
[ ] Branding configured
[ ] Admin user created
[ ] Roles configured
[ ] Modules enabled
[ ] Email tested
[ ] SSL tested
[ ] Backup tested
[ ] Client welcome email sent
[ ] Tenant marked active
```

### 12.2 Tenant health checklist

```txt
[ ] Site responds with 200
[ ] Login page loads
[ ] Workers running
[ ] Scheduler running
[ ] Redis healthy
[ ] MariaDB healthy
[ ] Disk usage below threshold
[ ] Last backup successful
[ ] SSL certificate valid
[ ] No repeated errors in logs
[ ] Subscription active
```

### 12.3 Failed provisioning checklist

```txt
[ ] Read provisioning logs
[ ] Identify failed step
[ ] Check DNS
[ ] Check MariaDB credentials
[ ] Check apps installed in image
[ ] Check Redis/worker health
[ ] Check disk space
[ ] If site partially created, decide repair vs drop/recreate
[ ] Retry from failed step
[ ] Update tenant status
```

---

## 13. What to automate first

### Phase 1 — Manual but documented

```txt
Manual site creation
Manual setup wizard
Manual users
Manual logo/domain
Manual checklist
Manual backup verification
```

### Phase 2 — Scripted provisioning

```txt
Script creates site
Script installs apps
Script runs migration
Script creates admin user
Script applies basic template
```

### Phase 3 — SaaS admin provisioning

```txt
Admin panel button: Create Tenant
Provisioning job queue
Status UI
Logs
Retry support
```

### Phase 4 — Self-service signup

```txt
Public plan page
Stripe Checkout
Automatic tenant creation
Welcome email
Billing portal
```

---

## 14. Minimum MVP definition

Your MVP tenant provisioning is acceptable when you can reliably do this:

```txt
Create a new tenant in under 1 hour
Client can log in
Company data is configured
Modules are visible correctly
Email works
SSL works
Backup works
Client can create job/customer/invoice
You can suspend/reactivate access
You can restore from backup in a test environment
```

Do not launch paid clients before backup/restore is tested.

---

## 15. References

```txt
Frappe Bench new-site command:
https://docs.frappe.io/framework/user/en/bench/reference/new-site

Frappe multitenancy / sites:
https://docs.frappe.io/framework/user/en/basics/sites
https://docs.frappe.io/framework/user/en/bench/guides/setup-multitenancy

Frappe Docker:
https://github.com/frappe/frappe_docker

Frappe users and permissions:
https://docs.frappe.io/framework/user/en/basics/users-and-permissions

Frappe background jobs:
https://docs.frappe.io/framework/user/en/api/background_jobs
https://docs.frappe.io/framework/user/en/guides/app-development/running-background-jobs

ERPNext company setup:
https://docs.frappe.io/erpnext/company-setup
```
