# 05 — Custom Frappe App Development Runbook

**Project:** ERPNext/Frappe SaaS custom app development  
**Audience:** Fernando / developers building LenGrowth FieldOps modules  
**Last updated:** 2026-05-21  
**Status:** Technical development runbook

---

## 1. Purpose

This document explains how to build your own product on top of ERPNext/Frappe without modifying ERPNext core.

Your custom app should contain the reusable SaaS modules:

```txt
Field Operations
Drilling
Fleet
Maintenance
Client Portal
QuickBooks Integration
White Label Settings
SaaS Module Entitlements
Reports and dashboards
```

The most important principle:

```txt
Do not edit ERPNext core unless absolutely unavoidable.
Build your product as a separate Frappe app.
```

Why:

```txt
ERPNext updates remain easier
Your code is version-controlled separately
You can install your app on multiple client sites
You can enable/disable modules per client
You can sell your product as SaaS
```

---

## 2. Development environments

You need at least three environments.

### 2.1 Local development

Purpose:

```txt
Build DocTypes
Write Python logic
Write reports
Create fixtures
Test workflows
```

Use Docker or a local bench. Docker is cleaner if production uses Frappe Docker.

### 2.2 Staging

Purpose:

```txt
Test production-like deployment
Test migrations
Test upgrades
Test sample tenant provisioning
Test backups/restores
```

Example:

```txt
staging.yourdomain.com
demo-staging.yourdomain.com
```

### 2.3 Production

Purpose:

```txt
Real clients
Stable releases only
Backups always enabled
Strict change control
```

Never develop directly on production.

---

## 3. App creation

In a bench environment:

```bash
cd ~/frappe-bench
bench new-app lengrowth_fieldops
```

During prompts:

```txt
App Title: LenGrowth FieldOps
App Description: Field operations modules for ERPNext
App Publisher: LenGrowth / LenQuant
App Email: support@yourdomain.com
App License: MIT or GPL-compatible depending on your legal strategy
```

Install on a dev site:

```bash
bench --site dev.yourdomain.local install-app lengrowth_fieldops
bench --site dev.yourdomain.local migrate
```

Verify:

```bash
bench --site dev.yourdomain.local list-apps
```

Expected:

```txt
frappe
erpnext
lengrowth_fieldops
```

---

## 4. Repository structure

Recommended repository:

```txt
lengrowth_fieldops/
  lengrowth_fieldops/
    __init__.py
    hooks.py
    modules.txt

    field_operations/
      doctype/
        field_ops_settings/
        crew/
        crew_assignment/
        daily_field_report/
        field_photo_log/

    drilling/
      doctype/
        drilling_job/
        borehole/
        depth_log/
        daily_drilling_report/
        rig_assignment/
        safety_checklist/
        job_signoff/

    fleet/
      doctype/
        fleet_settings/
        vehicle_assignment/
        fuel_log_extension/
        maintenance_alert/

    integrations/
      doctype/
        quickbooks_settings/
        stripe_settings/
      api/
        quickbooks.py
        stripe.py

    saas/
      doctype/
        tenant_module_settings/
        tenant_branding_settings/
      api/
        entitlements.py
        health.py
        branding.py

    public/
      js/
      css/

    templates/
    patches/
    fixtures/
    config/
    tests/
```

Better to separate modules clearly from day one.

---

## 5. Naming conventions

Use clear, singular DocType names.

Good:

```txt
Drilling Job
Borehole
Depth Log
Daily Drilling Report
Crew Assignment
Rig Assignment
Job Sign-off
Tenant Branding Settings
```

Avoid:

```txt
Jobs
Data
Drilling Info
Client Thing
Work Stuff
```

Frappe DocTypes are normally singular. Keep names business-friendly.

---

## 6. Developer mode

When creating DocTypes that should become part of your app code, enable developer mode in development.

```bash
bench set-config -g developer_mode true
bench restart
```

Then create DocTypes in the UI. Frappe will generate JSON files in your app.

Do not enable developer mode casually on production.

---

## 7. Creating DocTypes

You can create DocTypes through the Desk UI:

```txt
Search → New DocType
```

For each custom DocType define:

```txt
Module
Is Submittable?
Is Child Table?
Naming rule
Fields
Permissions
Track changes
Search fields
Title field
```

### 7.1 Standard DocType example: Drilling Job

Settings:

```txt
DocType Name: Drilling Job
Module: Drilling
Is Submittable: Yes, if you need approval/finalization
Track Changes: Yes
Allow Rename: No, usually
Autoname: naming_series:
```

Fields:

```txt
naming_series
customer
project
site_address
job_type
status
expected_start_date
expected_end_date
assigned_crew
assigned_rig
estimated_depth
actual_depth
safety_risk_level
signoff_status
invoice_status
notes
```

### 7.2 Child table example: Crew Member Row

Child table fields:

```txt
employee
role_on_crew
skill
is_lead
notes
```

Used inside:

```txt
Crew
Crew Assignment
Daily Drilling Report
```

### 7.3 Single DocType example: Field Ops Settings

Use Single DocType for tenant-specific settings.

Fields:

```txt
default_job_status
require_customer_signoff
require_photos_before_completion
default_warehouse
default_job_naming_series
enable_drilling_module
enable_fleet_module
enable_quickbooks_sync
```

---

## 8. Linking to ERPNext objects

Your custom app should use ERPNext records instead of duplicating them.

Use Link fields:

```txt
Customer → Customer
Project → Project
Sales Order → Sales Order
Sales Invoice → Sales Invoice
Item → Item
Warehouse → Warehouse
Employee → Employee
Asset → Asset
Address → Address
Contact → Contact
```

Bad design:

```txt
Custom Customer Name text field
Custom Employee text field
Custom Item name text field
```

Good design:

```txt
Link field to Customer
Link field to Employee
Link field to Item
```

This allows reporting, permissions, and accounting to stay connected.

---

## 9. Custom fields vs custom DocTypes

Use **custom fields** when you need small extra info on ERPNext records.

Examples:

```txt
Add "Default Rig Operator" to Asset
Add "Preferred Crew" to Customer
Add "Site Access Instructions" to Address
Add "Drilling Job" link to Project
```

Use **custom DocTypes** when the concept has its own lifecycle.

Examples:

```txt
Drilling Job
Daily Drilling Report
Depth Log
Crew Assignment
Safety Checklist
Job Sign-off
```

Rule:

```txt
If it has statuses, approvals, reports, child tables, or many records, create a DocType.
If it is just one extra attribute on an existing object, use a custom field.
```

---

## 10. Fixtures

Fixtures let you export configuration from development into your app so it can be installed on other sites.

Use fixtures for:

```txt
Custom Fields
Property Setters
Roles
Role Profiles
Workflows
Workflow States
Print Formats
Email Templates
Notification Templates
Workspace definitions
```

Example in `hooks.py`:

```python
fixtures = [
    "Custom Field",
    "Property Setter",
    "Role",
    "Role Profile",
    "Workflow",
    "Workflow State",
    "Print Format",
    "Email Template"
]
```

Then export:

```bash
bench --site dev.yourdomain.local export-fixtures
```

Commit fixtures to git.

---

## 11. Permissions

Define custom roles:

```txt
Field Ops Manager
Field Ops User
Drilling Manager
Drilling Supervisor
Field Worker
Fleet Manager
SaaS Integration
Client Portal User
```

Permission principles:

```txt
Workers should not see accounting
Dispatchers should not edit invoices
Finance should not necessarily edit drilling logs
Client portal users should see only their own jobs/reports
SaaS integration user should only run specific integration actions
```

Use:

```txt
Role Permission Manager
User Permissions
Custom permission checks in Python
```

For client portal access, always enforce record-level restrictions.

---

## 12. Workflows

Example Drilling Job workflow:

```txt
Draft
  ↓ submit
Approved
  ↓ schedule
Scheduled
  ↓ start
In Progress
  ↓ complete field work
Completed
  ↓ customer signs
Signed Off
  ↓ invoice
Invoiced
  ↓ close
Closed
```

Roles:

```txt
Operations Manager can approve
Dispatcher can schedule
Crew Leader can start/complete field work
Client Portal User can sign off
Accounts User can invoice
```

Keep workflows simple at first. Complex workflows slow implementation.

---

## 13. Server-side logic

Each DocType can have a Python controller.

Example:

```python
import frappe
from frappe.model.document import Document

class DrillingJob(Document):
    def validate(self):
        self.validate_required_links()
        self.validate_dates()

    def on_submit(self):
        self.create_project_if_missing()

    def validate_dates(self):
        if self.expected_end_date and self.expected_start_date:
            if self.expected_end_date < self.expected_start_date:
                frappe.throw("Expected end date cannot be before start date.")
```

Use controller methods for:

```txt
Validation
Auto-creating linked records
Updating statuses
Computing totals
Enforcing module entitlements
Triggering background jobs
```

Do not put critical business logic only in client-side JS.

---

## 14. Client-side scripts

Use client-side JS for UI convenience:

```txt
Show/hide fields
Auto-fill fields
Filter link fields
Set defaults
Show warnings
Improve form workflow
```

Example:

```javascript
frappe.ui.form.on('Drilling Job', {
  customer(frm) {
    if (frm.doc.customer) {
      frappe.db.get_value('Customer', frm.doc.customer, 'customer_group')
        .then(r => {
          frm.set_value('customer_group', r.message.customer_group);
        });
    }
  }
});
```

Never rely on JS for security. Always validate server-side too.

---

## 15. APIs

Frappe exposes standard REST APIs for documents, but you should also create specific methods for SaaS and integrations.

Example files:

```txt
lengrowth_fieldops/saas/api/health.py
lengrowth_fieldops/saas/api/entitlements.py
lengrowth_fieldops/integrations/api/quickbooks.py
```

Example method:

```python
import frappe

@frappe.whitelist()
def health():
    return {
        "ok": True,
        "site": frappe.local.site,
        "installed_apps": frappe.get_installed_apps()
    }
```

Protect APIs with:

```txt
API key/secret
Role checks
Rate limits where needed
Input validation
Audit logs
```

---

## 16. Background jobs

Frappe supports background jobs using RQ/Redis.

Use background jobs for:

```txt
QuickBooks sync
Stripe webhook processing
Report generation
Large imports
PDF generation
Daily digest emails
Backup status checks
GPS/device data ingestion
Maintenance due notifications
```

Example:

```python
import frappe

def enqueue_quickbooks_sync(company):
    frappe.enqueue(
        "lengrowth_fieldops.integrations.quickbooks.sync_company",
        queue="long",
        company=company,
        timeout=600
    )
```

Queues:

```txt
short: quick actions
default: normal jobs
long: imports/syncs/reports
```

---

## 17. Scheduled jobs

Use `hooks.py`:

```python
scheduler_events = {
    "daily": [
        "lengrowth_fieldops.fleet.tasks.create_maintenance_alerts",
        "lengrowth_fieldops.reports.tasks.send_daily_operations_digest"
    ],
    "hourly": [
        "lengrowth_fieldops.integrations.quickbooks.tasks.sync_pending"
    ],
    "cron": {
        "0 2 * * *": [
            "lengrowth_fieldops.saas.tasks.collect_usage_metrics"
        ]
    }
}
```

Use scheduled jobs for:

```txt
Maintenance alerts
Daily reports
Billing usage metrics
Subscription state sync
Backup verification
```

---

## 18. Reports and dashboards

Recommended reports:

```txt
Drilling Jobs by Status
Daily Drilling Progress
Materials Used by Job
Crew Utilization
Rig Utilization
Job Profitability
Maintenance Due
Delayed Jobs
Unsigned Completed Jobs
Unbilled Completed Jobs
```

Start with Query Reports or Script Reports.

Example report columns:

```txt
Job ID
Customer
Status
Start Date
Crew
Rig
Quoted Amount
Actual Cost
Margin
Invoice Status
```

Create workspaces:

```txt
Field Operations
Drilling
Fleet
Management
Finance
```

---

## 19. Print formats

Create print formats for:

```txt
Drilling Quotation
Daily Drilling Report
Safety Checklist
Customer Sign-off
Completion Report
Invoice
```

For white-label:

```txt
Logo from Tenant Branding Settings
Company address
Client-specific footer
Terms and conditions
```

Avoid hardcoding logos into templates. Use settings.

---

## 20. Notifications

Examples:

```txt
New job assigned to crew leader
Job scheduled for tomorrow
Daily report missing
Safety issue reported
Customer sign-off required
Invoice overdue
Maintenance due
Payment failed / tenant in grace period
```

Notification channels:

```txt
Email
In-app notification
SMS/WhatsApp later
Slack/Teams later
```

---

## 21. Tests

At minimum, test:

```txt
Create Drilling Job
Create Project from Drilling Job
Assign crew
Assign rig
Submit Daily Drilling Report
Record Material Usage
Generate Customer Sign-off
Block invoice until sign-off, if configured
Enable/disable module entitlements
API health endpoint
Background job enqueues
```

Do not skip tests for migrations and permissions.

---

## 22. Patches and migrations

Use patches for data changes that must run across all sites.

Examples:

```txt
Create default statuses
Backfill job status
Create default roles
Update old field values
Create default settings records
```

Patch file:

```txt
lengrowth_fieldops/patches/v1_0/create_default_drilling_statuses.py
```

Add to:

```txt
patches.txt
```

Then run:

```bash
bench --site site-name migrate
```

---

## 23. Versioning and releases

Use semantic versioning:

```txt
0.1.0 internal prototype
0.2.0 first drilling MVP
0.3.0 field ops beta
1.0.0 first production client
1.1.0 fleet module
1.2.0 QuickBooks module
```

Each release should include:

```txt
Migration notes
New DocTypes
Changed fields
Breaking changes
Rollback notes
Testing notes
```

---

## 24. Deployment process

If using custom Docker images:

```txt
Update app repo
Build new image
Tag image with version
Push image to registry
Deploy to staging
Run migrations
Test
Deploy to production
Run migrations per site
```

Staging checklist:

```txt
[ ] Image built
[ ] Staging site backup created
[ ] Migration ran
[ ] Workflows tested
[ ] Reports tested
[ ] Permissions tested
[ ] Background jobs tested
[ ] No critical logs
```

Production checklist:

```txt
[ ] Release notes written
[ ] Backups verified
[ ] Maintenance window chosen, if needed
[ ] Deploy image
[ ] Run migrate on internal/demo tenant
[ ] Test
[ ] Run migrate on first client
[ ] Test
[ ] Roll out to remaining tenants
[ ] Monitor logs
```

---

## 25. Security rules

```txt
Do not use Administrator for integrations
Do not give workers accounting access
Do not store plaintext secrets
Do not trust client-side JS
Do not expose provisioning commands to public users
Do not allow arbitrary command execution
Do not enable server scripts on shared production benches unless you understand the risk
Do not skip backups before migrations
```

---

## 26. What to build first

Recommended build order:

```txt
1. Custom app skeleton
2. Field Ops Settings
3. Drilling Job
4. Crew and Crew Assignment
5. Rig Assignment
6. Daily Drilling Report
7. Safety Checklist
8. Field Photo Log
9. Job Sign-off
10. Basic reports
11. Module Entitlements
12. Tenant Branding Settings
13. SaaS health endpoint
14. Provisioning helper methods
15. QuickBooks/Stripe later
```

---

## 27. References

```txt
Frappe create app:
https://docs.frappe.io/framework/user/en/tutorial/create-an-app
https://docs.frappe.io/framework/user/en/basics/apps

Frappe DocTypes:
https://docs.frappe.io/framework/user/en/basics/doctypes
https://docs.frappe.io/framework/user/en/tutorial/create-a-doctype

Frappe customizations:
https://docs.frappe.io/framework/user/en/basics/doctypes/customize

Frappe users and permissions:
https://docs.frappe.io/framework/user/en/basics/users-and-permissions
https://docs.frappe.io/framework/permission-types

Frappe background jobs:
https://docs.frappe.io/framework/user/en/api/background_jobs
https://docs.frappe.io/framework/user/en/guides/app-development/running-background-jobs

Frappe reports:
https://docs.frappe.io/framework/user/en/desk/reports/query-report

Frappe REST/document API:
https://docs.frappe.io/framework/user/en/api/document
```
