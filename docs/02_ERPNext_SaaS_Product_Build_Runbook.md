# 02 — SaaS/Product Build Runbook for ERPNext/Frappe Vertical SaaS

**Project:** ERPNext/Frappe-based SaaS platform for drilling, field operations, construction, fleet, warehouse, and manual services  
**Owner:** Fernando Guerra / LenGrowth-LenQuant context  
**Last reviewed:** 2026-05-21  
**Goal:** define what you need to build on top of ERPNext/Frappe to turn it into a SaaS, not just a custom ERP implementation.

---

## 0. Simple explanation

ERPNext gives you the generic ERP foundation:

```txt
CRM
Customers
Quotations
Sales Orders
Invoices
Accounting
Inventory
Warehouses
Suppliers
Purchasing
Employees
Projects
Tasks
Assets
Permissions
Reports
Files
Print formats
```

Frappe gives you the framework:

```txt
Users
Roles
DocTypes / data models
Forms
Reports
REST API
Background jobs
Scheduler
Workflows
File attachments
Print/PDF formats
Custom apps
Multi-site setup
```

Your SaaS layer gives you the product/business wrapper:

```txt
Tenant signup
Billing
Plans
Module enable/disable
White-label settings
Domain mapping
Provisioning automation
Client onboarding
Implementation templates
Support/admin tools
Backups/status visibility
```

Your custom field-operations app gives you the vertical value:

```txt
Work Orders
Crew Scheduling
Dispatch
Vehicle/Fleet Tracking
Drilling Jobs
Borehole Logs
Daily Reports
Safety Checklists
Field Photos
Material Usage
Customer Sign-off
QuickBooks/Stripe integrations
```

---

## 1. The product you are building

Do not position it as “generic ERPNext hosting.” That is weak.

Position it as:

```txt
A field operations ERP/SaaS for manual businesses that need CRM, jobs, crews, assets, inventory, vehicles, reports, invoices, and industry-specific workflows.
```

First vertical:

```txt
Drilling business / field service / manual jobs
```

Later verticals:

```txt
Construction
Field maintenance
Warehouses
Fleet/logistics
Equipment rental
Industrial services
Oil/gas service companies
Utilities/service crews
```

The product architecture:

```txt
ERPNext Base
  + Field Operations Core
  + Industry Modules
  + SaaS Control Layer
  + White-label/implementation layer
```

---

## 2. What ERPNext already gives you

For a drilling company, ERPNext already covers much of the administrative side.

```txt
Need                              ERPNext coverage
----------------------------------------------------------
Leads                             Yes
Customers                         Yes
Contacts                          Yes
Quotations                        Yes
Sales Orders                      Yes
Invoices                          Yes
Payments                          Yes
Accounting                        Yes
Items/materials                   Yes
Warehouses                        Yes
Purchase Orders                   Yes
Suppliers                         Yes
Employees                         Yes
Projects                          Yes
Tasks                             Yes
Assets/equipment                  Yes
Basic maintenance                 Mostly
Attachments/files                 Yes
Reports                           Yes
Roles/permissions                 Yes
Email templates                   Yes
Print formats                     Yes
```

Do not rebuild these unless there is a very strong reason.

---

## 3. What you need to build

You build what ERPNext does not handle well out of the box for field/manual operations.

```txt
Custom field operations app
  ├── Work Orders
  ├── Job Scheduling
  ├── Crew Assignment
  ├── Dispatch Board
  ├── Field Daily Reports
  ├── Safety Checklists
  ├── Field Photos
  ├── Customer Sign-off
  ├── Material Usage per Job
  ├── Equipment/Rig Assignment
  ├── Vehicle Logs
  ├── Drilling-specific logs
  ├── Dashboards
  └── Integrations
```

For drilling specifically:

```txt
Drilling Job
Borehole / Well / Site
Rig Assignment
Crew Assignment
Depth Log
Daily Drilling Report
Safety Checklist
Material Consumption
Downtime Log
Equipment Maintenance Log
Client Approval
Job Completion Report
```

---

## 4. SaaS layers: keep them separate mentally

There are three products/layers:

```txt
1. Marketing/main website
2. SaaS control/admin/customer portal
3. Client ERP sites
```

### 4.1 Marketing/main website

This sells the product.

Example:

```txt
yourdomain.com
www.yourdomain.com
```

Built with:

```txt
Next.js
Tailwind
Framer Motion / animations
SEO pages
Pricing pages
Contact/demo forms
```

### 4.2 SaaS control/admin/customer portal

This controls clients, billing, plans, modules, and provisioning.

Example:

```txt
app.yourdomain.com
```

Can be built as:

```txt
Option A: Frappe custom app/site
Option B: Next.js + backend/API
```

For MVP, Option A is simpler. For a polished SaaS product later, Option B may be better.

### 4.3 Client ERP sites

Each client gets an ERPNext/Frappe site:

```txt
client1.yourdomain.com
client2.yourdomain.com
ops.clientdomain.com
```

Each one has separate:

```txt
Database
Users
Settings
Files
Logo
Company records
Enabled modules
Custom domain
```

---

## 5. Recommended build order

Do not build the full SaaS layer first.

Build in this order:

```txt
Phase 1: ERPNext online
Phase 2: One drilling/client workflow manually configured
Phase 3: Custom Frappe app for field ops
Phase 4: Repeatable implementation template
Phase 5: SaaS admin/control layer
Phase 6: Stripe billing + provisioning automation
Phase 7: White-label automation
Phase 8: Multi-client scaling
```

This avoids building a beautiful SaaS shell around a workflow that is not proven yet.

---

## 6. Main website requirements

Your main site should not be too generic.

Suggested sitemap:

```txt
/
  Hero
  Pain points
  Product modules
  Drilling use case
  Field operations use case
  Screenshots / demo video
  Integrations
  Pricing
  CTA

/industries/drilling
/industries/field-service
/industries/construction
/industries/fleet
/industries/warehouse

/product/crm
/product/jobs
/product/dispatch
/product/fleet
/product/inventory
/product/reporting
/product/accounting
/product/white-label

/pricing
/demo
/contact
/login
/privacy
/terms
/security
/status
```

### 6.1 Main site CTAs

Use these CTAs:

```txt
Book a demo
Start a pilot
Request field operations audit
See drilling workflow
Login
```

### 6.2 Demo form fields

```txt
Name
Company
Email
Phone/WhatsApp
Industry
Number of field workers
Number of vehicles/equipment
Current software
Main problem
Timeline
```

### 6.3 Main site auth

The marketing site does not need deep auth.

The `/login` page should ask:

```txt
Company subdomain or email
```

Then redirect to the right ERP site:

```txt
client1.yourdomain.com/login
```

At the start, avoid building central SSO. Use each ERPNext site’s own login.

---

## 7. Authentication architecture

You will have two authentication layers.

### 7.1 SaaS admin/customer portal auth

Used by:

```txt
You
Support team
Implementation team
Client billing admins
Possibly client owner/admin users
```

This controls:

```txt
Tenant account
Billing
Plan
Modules
Domains
Implementation status
Support
```

For MVP, this can be a Frappe site because Frappe already has users, roles, sessions, and permissions.

### 7.2 ERP site auth

Used by each client’s staff:

```txt
Owner
Admin
Manager
Dispatcher
Field worker
Accountant
Customer portal user
```

Each client ERP site handles its own users.

Example:

```txt
client1.yourdomain.com
  admin@client1.com
  dispatcher@client1.com
  worker1@client1.com

client2.yourdomain.com
  admin@client2.com
  manager@client2.com
```

### 7.3 Initial decision

For MVP:

```txt
No central SSO.
Each ERP site has its own login.
The SaaS/admin layer stores tenant metadata.
```

Later:

```txt
Use OAuth/SSO so users can log in once and access their ERP site.
```

Frappe supports normal user sessions, role-based permissions, API key/secret authentication, OAuth, and social login options.

---

## 8. Tenant model

Your SaaS layer should store tenants separately from ERPNext site data.

### 8.1 Tenant record

Create a DocType/model/table:

```txt
Tenant
```

Fields:

```txt
Tenant Name
Company Legal Name
Slug
Primary Domain
White-label Domain
Frappe Site Name
Database Name
Status
Plan
Billing Status
Stripe Customer ID
Stripe Subscription ID
Owner Name
Owner Email
Industry
Implementation Status
Created At
Go-live Date
Suspended At
Notes
```

Statuses:

```txt
lead
trial
provisioning
active
past_due
suspended
cancelled
archived
```

### 8.2 Tenant Domain record

```txt
Tenant Domain
```

Fields:

```txt
Tenant
Domain
Type: platform_subdomain / white_label
DNS Status: pending / verified / failed
SSL Status: pending / issued / failed
Primary: yes/no
Created At
Verified At
```

### 8.3 Tenant Module record

```txt
Tenant Module
```

Fields:

```txt
Tenant
Module
Enabled
Plan Source
Enabled By
Enabled At
Config JSON
```

### 8.4 Provisioning Job record

```txt
Provisioning Job
```

Fields:

```txt
Tenant
Job Type
Status
Command/Action
Started At
Finished At
Logs
Error
Retry Count
```

This gives you a history of every site creation, domain change, module install, backup, and migration.

---

## 9. SaaS module system

Do not customize each client completely from zero.

Build reusable modules.

### 9.1 Base modules

```txt
Core ERP
  CRM
  Customers
  Sales
  Inventory
  Accounting
  Projects
  Employees
  Assets
```

### 9.2 Your product modules

```txt
Field Operations Core
  Work Orders
  Crews
  Dispatch
  Field Reports
  Photos
  Signatures
  Checklists

Fleet Module
  Vehicles
  Drivers
  Fuel Logs
  GPS Events
  Maintenance

Drilling Module
  Drilling Jobs
  Boreholes
  Rigs
  Depth Logs
  Safety Logs
  Downtime Logs

Warehouse Module
  Warehouse Ops
  Picking/Packing
  Stock Movement
  Cycle Counts

Construction Module
  Job Sites
  Subcontractors
  Daily Reports
  Materials
  Progress Tracking

Reporting Module
  Dashboards
  Client reports
  KPI reports
  Export tools

Integrations Module
  QuickBooks
  Stripe
  Email
  Webhooks
  Import/Export
```

### 9.3 Client combinations

```txt
Drilling client:
  Core ERP + Field Ops + Fleet + Drilling + Reporting

Manual service client:
  Core ERP + Field Ops + Reporting

Warehouse client:
  Core ERP + Inventory + Warehouse + Reporting

Construction client:
  Core ERP + Field Ops + Construction + Fleet
```

---

## 10. Feature/module gating

You need a way to say:

```txt
Client A can use Drilling Module.
Client B cannot.
```

### 10.1 MVP approach

In your custom Frappe app, create:

```txt
SaaS Settings
Tenant Module Settings
```

Then in code/UI:

```txt
If Drilling enabled -> show Drilling workspace, DocTypes, reports
If Fleet disabled -> hide Fleet workspace, block routes/API actions
```

### 10.2 Roles

Create roles:

```txt
Field Ops Admin
Dispatcher
Crew Manager
Field Worker
Fleet Manager
Drilling Manager
Accounting User
Client Portal User
```

Use roles to control permissions.

### 10.3 Workspaces

Use workspaces per module:

```txt
Field Operations Workspace
Fleet Workspace
Drilling Workspace
Reports Workspace
```

Only show relevant workspaces to users with the correct roles/modules.

---

## 11. Site provisioning workflow

This is what your SaaS layer eventually automates.

### 11.1 Manual MVP version

For a new client:

```txt
1. Create Tenant record in SaaS/admin layer
2. Create DNS record clientslug.yourdomain.com -> static IP
3. Add domain to SITES_RULE
4. Create new Frappe site
5. Install ERPNext
6. Install your custom app
7. Apply industry template
8. Set company name, logo, country, currency
9. Create client admin user
10. Enable modules
11. Test login
12. Send welcome email
13. Run backup
```

### 11.2 Future automated version

Trigger:

```txt
Stripe checkout completed
or admin clicks Create Tenant
```

System actions:

```txt
Create Tenant record
Create provisioning job
Create site
Install apps
Run migrations
Apply template
Create admin user
Generate password/reset link
Configure domain
Check SSL
Send welcome email
Mark tenant active
```

### 11.3 Example provisioning command pattern

Inside Docker:

```bash
docker compose exec backend bench new-site clientslug.yourdomain.com \
  --admin-password 'ADMIN_PASSWORD' \
  --db-root-password 'DB_ROOT_PASSWORD' \
  --install-app erpnext

docker compose exec backend bench --site clientslug.yourdomain.com install-app lengrowth_fieldops

docker compose exec backend bench --site clientslug.yourdomain.com migrate
```

Then run a custom setup function:

```bash
docker compose exec backend bench --site clientslug.yourdomain.com execute \
  "lengrowth_fieldops.setup.apply_template" \
  --kwargs '{"template":"drilling","company_name":"Client Company"}'
```

Your custom app should include this setup function later.

---

## 12. White-label system

White label should be mostly configuration, not custom code per client.

### 12.1 White-label settings

Create:

```txt
Tenant Branding Settings
```

Fields:

```txt
Company display name
Logo
Favicon
Primary color
Accent color
Login page background
Email sender name
Support email
Custom domain
Invoice/print letterhead
Portal welcome text
Footer text
Hide platform branding yes/no
```

### 12.2 What to automate

```txt
Set logo
Set website/app name
Set letterhead
Set email templates
Set print formats
Set custom domain
Set portal colors/text
```

### 12.3 What not to promise early

Do not promise each client a totally custom UI unless they pay implementation fees.

Offer levels:

```txt
Basic white label:
  logo, domain, letterhead, email name

Pro white label:
  custom colors, portal copy, print formats

Enterprise white label:
  custom workflow, custom dashboards, dedicated infra
```

---

## 13. Billing with Stripe

ERPNext has Stripe integration for payment gateway use, but your SaaS billing should be controlled by your SaaS layer.

### 13.1 Stripe products

Create products/plans:

```txt
Starter
Professional
Business
Enterprise
Implementation Fee
Additional Module Add-on
Additional User Add-on
Dedicated Infrastructure Add-on
```

### 13.2 Basic pricing model

Example:

```txt
Starter
  5 users
  CRM + Jobs + Invoicing
  shared infra

Professional
  20 users
  Field Ops + Fleet + Reports
  shared infra

Business
  50 users
  Field Ops + Fleet + Drilling/Construction
  custom workflows

Enterprise
  dedicated infra
  SSO
  custom contract
```

### 13.3 Required Stripe webhooks

Implement webhooks for:

```txt
checkout.session.completed
customer.subscription.created
customer.subscription.updated
customer.subscription.deleted
invoice.paid
invoice.payment_failed
payment_method.attached
```

### 13.4 Webhook rules

Every Stripe webhook handler must:

```txt
Verify Stripe signature
Be idempotent
Log the event ID
Never trust client-side data alone
Update Tenant billing status
Trigger provisioning only once
```

### 13.5 Billing status behavior

```txt
trialing       -> tenant active
active         -> tenant active
past_due       -> warn client, keep active for grace period
unpaid         -> restrict/suspend after grace period
cancelled      -> schedule deactivation/archive
enterprise     -> manual contract handling
```

### 13.6 Customer billing portal

Use Stripe Customer Portal so clients can:

```txt
Update payment method
Download invoices
Change subscription if allowed
Cancel if allowed
Update billing details
```

This saves you from building billing UI from zero.

---

## 14. SaaS admin panel requirements

The admin panel is for you and your team.

### 14.1 Dashboard

Show:

```txt
Active tenants
Trial tenants
Past due tenants
Failed provisioning jobs
Backup status
Sites requiring migration
Monthly recurring revenue
Implementation pipeline
Support issues
```

### 14.2 Tenant detail page

Show:

```txt
Company
Owner/admin user
Domains
Plan
Enabled modules
Billing status
ERP site URL
White-label settings
Provisioning jobs
Backup history
Implementation notes
Support notes
```

Actions:

```txt
Create site
Install module
Run migrate
Run backup
Suspend tenant
Reactivate tenant
Add domain
Check DNS
Check SSL
Send password reset
Open ERP site
```

### 14.3 Plan/module page

Manage:

```txt
Plan name
Price
User limit
Enabled modules
Storage limit
White-label level
Support level
Dedicated infra yes/no
```

### 14.4 Implementation page

Track onboarding tasks:

```txt
Discovery call
Data import
Company setup
User setup
Workflow mapping
Role permissions
Training
Go-live
Post-go-live support
```

---

## 15. Customer portal requirements

For client owners/admins:

```txt
View plan
View billing status
Open Stripe portal
Request module
Request support
Invite admin users, later
View implementation status
View backup/status summary, later
Access ERP login
```

Do not give them low-level infrastructure controls.

---

## 16. ERP client site requirements

Each client ERP site needs:

```txt
Company setup
Chart of accounts
Users and roles
Customers
Items/materials
Warehouses
Assets/equipment
Projects/jobs
Invoice/quotation templates
Letterhead
Email settings
Enabled modules
Custom workflows
Reports
```

For drilling, initial DocTypes/customizations should be:

```txt
Drilling Job
Borehole Log
Rig Assignment
Crew Assignment
Daily Field Report
Safety Checklist
Material Usage
Customer Sign-off
```

Link them to ERPNext:

```txt
Drilling Job -> Customer
Drilling Job -> Project
Drilling Job -> Sales Order
Material Usage -> Stock Entry
Rig -> Asset
Crew Member -> Employee
Invoice -> Sales Invoice
```

---

## 17. Data import tools

Clients will have old data.

Build/import support for:

```txt
Customers CSV
Contacts CSV
Items/materials CSV
Vehicles/equipment CSV
Employees/users CSV
Open jobs CSV
Inventory opening balance
Invoices/accounting migration, later
```

MVP approach:

```txt
Use ERPNext Data Import Tool manually.
Create templates per industry.
Later add your own onboarding/import wizard.
```

---

## 18. Reporting and dashboards

Initial dashboards:

```txt
Open jobs
Jobs by status
Jobs by crew
Jobs by customer
Revenue by month
Material usage by job
Vehicle/equipment utilization
Delayed jobs
Safety checklist completion
Invoices pending
```

For drilling:

```txt
Drilling jobs active
Depth progress
Rig utilization
Downtime by cause
Crew productivity
Material usage by drilling job
Field report completion
```

---

## 19. Background jobs / async tasks

Frappe does not use Celery by default. It has its own background job system.

Use background jobs for:

```txt
Provisioning sites
Installing apps
Running backups
Uploading backups to GCS
Stripe webhook follow-up
QuickBooks sync
Email notifications
Large CSV imports
Report generation
PDF generation
Daily summary emails
Usage metering
```

For scheduled jobs, use Frappe scheduler events in your app.

Example future jobs:

```txt
hourly:
  sync_stripe_statuses
  check_failed_provisioning_jobs

daily:
  upload_site_backups
  check_dns_ssl_status
  send_daily_ops_summary
  sync_quickbooks

weekly:
  generate_client_health_reports
```

---

## 20. Security requirements

### 20.1 Tenant isolation

Use separate Frappe sites per tenant.

This gives:

```txt
Separate database
Separate users
Separate files
Separate settings
Cleaner backup/restore
Cleaner deletion/archive
```

### 20.2 Admin access

Your team should not use the same admin password everywhere.

Rules:

```txt
Unique Administrator password per site
Store in password manager
Prefer named admin users for your staff
Disable/remove staff access when no longer needed
Use roles, not shared accounts
```

### 20.3 Secrets

Never commit:

```txt
DB passwords
Stripe keys
Webhook secrets
OAuth client secrets
API keys
Administrator passwords
```

Store secrets in:

```txt
.env on server with proper permissions for MVP
Password manager
Later: Secret Manager
```

### 20.4 Audit

Enable/use:

```txt
Frappe document versioning/audit
Login history
Role permissions
Backup logs
Provisioning job logs
Stripe event logs
```

### 20.5 Public pages

You need:

```txt
Privacy Policy
Terms of Service
Security page
Data Processing Agreement, later
Subprocessors page, later
Status page, later
```

---

## 21. Support and operations workflows

Create a support process from day one.

### 21.1 Support ticket fields

```txt
Tenant
User
Issue type
Severity
ERP site URL
Module
Screenshot/files
Status
Assigned to
Resolution notes
```

### 21.2 Severity

```txt
P0: site down / cannot work
P1: billing/invoicing/job operations blocked
P2: important workflow broken
P3: bug with workaround
P4: feature request
```

### 21.3 Support admin actions

```txt
Impersonation: avoid if possible; use controlled support access
Password reset
Check logs
Check background jobs
Run backup before manual data changes
Record all fixes in support notes
```

---

## 22. Implementation/onboarding template

Each new client should follow a repeatable onboarding process.

### 22.1 Discovery

Ask:

```txt
How many employees?
How many field workers?
How many vehicles/equipment?
What is the sales process?
What is the job lifecycle?
What documents/forms are used?
What reports are required?
What accounting system is used?
What inventory/materials are tracked?
Do they need offline mobile?
Do they need GPS/fleet tracking?
```

### 22.2 Setup

```txt
Create tenant
Create ERP site
Set company info
Set logo/domain
Create users/roles
Import customers/items/equipment
Configure workflows
Enable modules
Train admin
Run test job
Go live
```

### 22.3 First drilling workflow MVP

```txt
Lead
  -> Customer
  -> Quotation
  -> Approved Job / Project
  -> Crew Assignment
  -> Rig/Vehicle Assignment
  -> Daily Field Reports
  -> Material Usage
  -> Customer Sign-off
  -> Invoice
  -> Payment
  -> Job closeout report
```

---

## 23. Development workflow

Use three environments:

```txt
Local dev
Staging site
Production site
```

### 23.1 Local dev

Build custom app:

```txt
lengrowth_fieldops
```

Do not experiment directly on production.

### 23.2 Staging

Create:

```txt
staging.yourdomain.com
```

Use it to test:

```txt
ERPNext updates
Custom app migrations
New DocTypes
New workflows
Stripe test mode
QuickBooks sandbox
```

### 23.3 Production

Only deploy tested changes.

Before production changes:

```txt
Backup
Snapshot
Deploy
Migrate
Smoke test
```

---

## 24. Git repository structure

Suggested repos:

```txt
lengrowth-main-site
  Next.js marketing site

lengrowth-saas-admin
  Optional Next.js SaaS/customer portal, if not using Frappe for admin

lengrowth-fieldops-frappe-app
  Custom Frappe app

lengrowth-infra
  Docker compose files, scripts, provisioning scripts, docs
```

If using one monorepo:

```txt
lengrowth-platform/
  apps/
    marketing/
    saas-admin/
    frappe-fieldops/
  infra/
    gcp/
    docker/
    scripts/
  docs/
    01_GCP_ERPNext_Frappe_Infrastructure_Runbook.md
    02_ERPNext_SaaS_Product_Build_Runbook.md
```

Never commit production `.env` files.

---

## 25. Minimal MVP scope

Do this first:

```txt
1. Plain ERPNext online
2. Demo site online
3. One drilling client site online
4. Basic company setup
5. CRM -> quotation -> project/job -> invoice flow
6. Equipment/assets configured
7. Inventory/material usage configured
8. Custom fields for drilling-specific data
9. Simple daily field report DocType
10. Basic dashboard
11. Manual billing/plan tracking
12. Manual backups
```

This is enough to test the product with a real client.

---

## 26. MVP SaaS layer scope

Do not build everything at once.

For MVP, SaaS layer only needs:

```txt
Tenant list
Tenant detail
Plan field
Enabled modules field
Billing status field
Domain fields
Provisioning status
Manual action checklist
Stripe customer/subscription IDs, even if manual
Backup status notes
Implementation notes
```

It can start as a Frappe admin app/site.

---

## 27. Phase 2 SaaS automation

After the first client works, automate:

```txt
Create site button
Install modules button
Run migration button
Backup button
Suspend/reactivate button
DNS/SSL check
Stripe webhook sync
Customer portal link
```

---

## 28. Phase 3 SaaS automation

After multiple clients:

```txt
Automated signup
Stripe Checkout
Auto-provision trial site
Self-serve billing portal
Module marketplace/add-ons
Usage limits
In-app upgrade prompts
White-label domain self-serve flow
Automated implementation templates
Automated backups status page
```

---

## 29. What to charge separately

Charge monthly SaaS for product access.

Charge one-time implementation fees for client-specific setup.

Examples:

```txt
SaaS subscription
  recurring product access

Implementation fee
  data import, setup, training, workflow mapping

Customization fee
  special workflow or custom report

White-label fee
  custom domain, logo, branded portal

Dedicated infrastructure fee
  separate VM/database/backups
```

This prevents custom work from destroying the SaaS margin.

---

## 30. Red lines / avoid these mistakes

Avoid:

```txt
Editing ERPNext core directly
One-off custom code for every client
Building the full billing system before workflow validation
Opening SSH to 0.0.0.0/0 permanently
Skipping backups
Using latest tags in production without testing
Mixing all tenants in one database manually
Promising offline mobile too early
Promising full white-label custom UI too early
```

Prefer:

```txt
Custom Frappe app
Reusable modules
Separate site per tenant
Manual implementation first
Automate repeated steps later
Charge for custom work
```

---

## 31. First 30-day execution plan

### Week 1 — Infrastructure

```txt
Create GCP project
Create VM
Deploy Frappe Docker
Create demo site
Enable HTTPS
Create backup bucket
Run first backup
```

### Week 2 — ERPNext base workflow

```txt
Configure company
Configure CRM
Configure quotation/invoice
Configure project/job workflow
Configure items/materials
Configure assets/equipment
Create demo data
```

### Week 3 — Drilling MVP customization

```txt
Add custom fields
Create Daily Field Report DocType
Create Drilling Job DocType if needed
Create Crew Assignment DocType if needed
Create simple dashboard
Create print format/report
```

### Week 4 — SaaS/admin structure

```txt
Create Tenant records
Create Module records
Create Plan records
Create manual provisioning checklist
Document first implementation template
Prepare demo/pilot offer
```

---

## 32. References

- Frappe Framework: https://frappe.io/framework
- ERPNext: https://erpnext.com
- Frappe Docker: https://github.com/frappe/frappe_docker
- Frappe Docker getting started: https://github.com/frappe/frappe_docker/blob/main/docs/getting-started.md
- Frappe users and permissions: https://docs.frappe.io/framework/user/en/basics/users-and-permissions
- Frappe REST API/auth: https://docs.frappe.io/framework/user/en/api/rest
- Frappe OAuth2: https://docs.frappe.io/framework/oauth2
- Frappe social login: https://docs.frappe.io/framework/user/en/guides/integration/social_login_key
- Frappe background jobs: https://docs.frappe.io/framework/user/en/api/background_jobs
- Frappe custom domains: https://docs.frappe.io/framework/user/en/bench/guides/adding-custom-domains
- Stripe Customer Portal: https://docs.stripe.com/customer-management
- Stripe Webhooks: https://docs.stripe.com/webhooks
- ERPNext Stripe integration: https://docs.frappe.io/erpnext/stripe-integration
