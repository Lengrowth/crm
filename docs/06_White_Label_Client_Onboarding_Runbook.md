# 06 — White Label Client Onboarding Runbook

**Project:** ERPNext/Frappe SaaS onboarding and white-label delivery  
**Audience:** Fernando / LenGrowth sales, implementation, and support team  
**Last updated:** 2026-05-21  
**Status:** Client-facing and internal onboarding process

---

## 1. Purpose

This document defines how to onboard a new client into your ERPNext/Frappe SaaS in a repeatable way.

The goal is to prevent every implementation from becoming chaotic.

A client onboarding should produce:

```txt
A working ERP tenant
Correct branding
Correct domain
Correct users
Correct modules
Correct permissions
Basic data imported
Workflows configured
Training completed
First real process tested
Support channel created
```

---

## 2. Onboarding stages

Use this repeatable process:

```txt
1. Sales qualification
2. Discovery
3. Proposal and plan selection
4. Contract/payment/trial
5. Technical onboarding
6. ERP configuration
7. Data import
8. Workflow setup
9. User training
10. UAT/testing
11. Go-live
12. Hypercare
13. Ongoing support
```

---

## 3. Client onboarding record

Your SaaS admin should have a record for each onboarding.

Fields:

```txt
Client name
Legal company name
Primary contact
Technical contact
Billing contact
Industry
Plan
Modules
Implementation status
Tenant site
Custom domain
Branding status
DNS status
Email status
Data import status
Training status
Go-live date
Support channel
Notes
```

Statuses:

```txt
new
discovery
waiting_for_client_info
provisioning
configuration
data_import
training
uat
ready_for_go_live
live
hypercare
completed
paused
cancelled
```

---

## 4. Discovery questionnaire

### 4.1 Business basics

```txt
Company legal name:
Trading name:
Country:
Currency:
Timezone:
Fiscal year start:
Tax ID:
Number of users:
Number of field workers:
Number of locations/warehouses:
Current software:
Reason for switching:
```

### 4.2 Modules needed

```txt
CRM / leads
Quotations
Sales invoices
Accounting
Inventory
Warehouses
Purchasing
Projects/jobs
Field operations
Crew scheduling
Vehicles/fleet
Equipment maintenance
Drilling-specific records
Customer portal
QuickBooks integration
Stripe/payment collection
Advanced reporting
White-label domain
```

### 4.3 Current process questions

```txt
How do you receive leads?
How do you quote customers?
Who approves jobs?
How do you schedule field work?
Who assigns crews?
Who assigns equipment?
How do field workers report progress?
How do you capture photos?
How does the customer approve completion?
How do you invoice?
How do you track materials?
How do you handle maintenance?
What reports do managers need weekly?
```

### 4.4 Pain points

```txt
What causes the most errors today?
Where do you lose money?
Where do employees duplicate work?
What is still done in spreadsheets?
Which reports take too long?
Which process breaks when someone is absent?
```

---

## 5. Branding collection

Collect:

```txt
Company logo, preferably SVG/PNG
Square logo or icon
Favicon
Primary brand color
Secondary brand color
Invoice footer text
Email signature
Terms and conditions
Company address
Support email
Website URL
```

Logo requirements:

```txt
Main logo: transparent PNG or SVG
Minimum width: 600px recommended
Favicon: square 512x512 PNG
Invoice logo: high-resolution PNG/SVG
Avoid low-quality JPG screenshots
```

---

## 6. Domain setup

### 6.1 Subdomain on your domain

Fastest option:

```txt
client.yourdomain.com
```

You control DNS. Good for MVP.

### 6.2 Client-owned white-label domain

Example:

```txt
ops.clientcompany.com
erp.clientcompany.com
portal.clientcompany.com
```

Ask client to create:

```txt
CNAME ops.clientcompany.com → client.yourdomain.com
```

or:

```txt
A ops.clientcompany.com → your VM static IP
```

Recommended client instruction:

```txt
Please create a DNS record:

Type: CNAME
Name/Host: ops
Value/Target: client.yourdomain.com
Proxy: DNS only at first, if using Cloudflare
TTL: Auto or 300 seconds
```

After it resolves, configure the domain on the Frappe site and issue SSL.

### 6.3 DNS verification checklist

```txt
[ ] Domain points to correct server
[ ] No old A/CNAME conflict
[ ] DNS propagation confirmed
[ ] Site loads on HTTP/HTTPS
[ ] SSL issued
[ ] No wrong tenant appears
```

---

## 7. SSL checklist

Your infrastructure should handle SSL through Traefik, Nginx + Certbot, or your reverse proxy.

For every domain:

```txt
[ ] DNS points to server
[ ] Reverse proxy knows the domain
[ ] Certificate issued
[ ] HTTP redirects to HTTPS
[ ] Certificate auto-renewal enabled
[ ] Test in incognito browser
```

Do not onboard a client with browser certificate warnings.

---

## 8. Email setup

### 8.1 Basic sender

MVP:

```txt
notifications@yourdomain.com
```

Use a reliable provider:

```txt
Google Workspace SMTP
Postmark
SendGrid
Mailgun
Amazon SES
```

### 8.2 White-label sender

For enterprise/white-label clients:

```txt
notifications@clientcompany.com
erp@clientcompany.com
```

Requires DNS records from the provider:

```txt
SPF
DKIM
DMARC
Return-path/bounce domain
```

### 8.3 Email test checklist

```txt
[ ] Password reset email works
[ ] User invite email works
[ ] Invoice email works
[ ] Daily report email works
[ ] Notification email works
[ ] Emails do not land in spam
[ ] Reply-to address is correct
```

---

## 9. Data collection templates

Provide CSV templates for:

```txt
Customers
Contacts
Suppliers
Items/materials
Warehouses
Employees
Assets/equipment
Vehicles
Open jobs
Opening inventory
Open invoices, if importing
```

### 9.1 Customer CSV fields

```txt
Customer Name
Customer Type
Customer Group
Territory
Tax ID
Billing Address
Shipping/Site Address
Contact Name
Contact Email
Contact Phone
Notes
```

### 9.2 Employee CSV fields

```txt
Employee Name
Email
Phone
Role
Department
Manager
Active
Default Crew
Skills/Certifications
```

### 9.3 Asset/equipment CSV fields

```txt
Asset Name
Asset Category
Serial Number/VIN
Purchase Date
Current Location
Assigned Operator
Maintenance Frequency
Notes
```

### 9.4 Item/material CSV fields

```txt
Item Code
Item Name
Item Group
UOM
Is Stock Item
Opening Quantity
Opening Warehouse
Valuation Rate
Supplier
Notes
```

---

## 10. Plan/module setup

Before provisioning, confirm:

```txt
Plan
Billing cycle
Trial length
User limit
Storage limit
Modules
White-label domain included?
Implementation package included?
Support level
```

Example modules:

```txt
CRM
Sales/Invoicing
Inventory
Projects
Field Ops
Drilling
Fleet
Maintenance
QuickBooks
Advanced Reports
Client Portal
White Label
```

Your SaaS admin should save these before tenant creation.

---

## 11. Provisioning checklist

```txt
[ ] Tenant record created
[ ] Plan selected
[ ] Stripe subscription/trial created
[ ] Domain selected
[ ] DNS configured
[ ] Site created
[ ] ERPNext installed
[ ] Custom app installed
[ ] Modules enabled
[ ] Company configured
[ ] Branding applied
[ ] Users created
[ ] Email configured
[ ] Backup tested
[ ] Health check passed
```

---

## 12. ERP configuration checklist

### 12.1 Company

```txt
[ ] Company name
[ ] Currency
[ ] Fiscal year
[ ] Chart of accounts
[ ] Tax setup
[ ] Bank/cash accounts
[ ] Default cost center
[ ] Default warehouse
[ ] Address/contact
```

### 12.2 Sales

```txt
[ ] Customer groups
[ ] Territories
[ ] Lead sources
[ ] Sales pipeline stages
[ ] Quotation template
[ ] Terms and conditions
[ ] Taxes
[ ] Invoice template
```

### 12.3 Operations

```txt
[ ] Job statuses
[ ] Workflows
[ ] Crew roles
[ ] Crew assignment rules
[ ] Equipment assignment rules
[ ] Daily report template
[ ] Safety checklist template
[ ] Customer sign-off template
```

### 12.4 Inventory

```txt
[ ] Item groups
[ ] UOMs
[ ] Warehouses
[ ] Opening stock
[ ] Material usage workflow
[ ] Purchase flow
```

### 12.5 Fleet/equipment

```txt
[ ] Asset categories
[ ] Vehicles
[ ] Rigs/equipment
[ ] Maintenance schedule
[ ] Operators
[ ] Fuel log process
```

---

## 13. Roles and access setup

Recommended user groups:

```txt
Owner/Admin
Operations Manager
Dispatcher
Crew Leader
Field Worker
Sales User
Finance User
Inventory User
Fleet Manager
Executive Viewer
Client Portal User
```

Access principles:

```txt
System Manager only for trusted admins
Field workers should see only assigned work
Finance users should control invoices/accounting
Client portal users should only see their own records
Executives can view dashboards but not edit operations
```

User checklist:

```txt
[ ] User email verified
[ ] Correct role assigned
[ ] Password reset/invite sent
[ ] Login tested
[ ] Access to correct workspace
[ ] No excessive permissions
```

---

## 14. Training plan

### 14.1 Admin training

```txt
Users and roles
Company settings
Customers
Items
Warehouses
Reports
Basic troubleshooting
Support process
```

### 14.2 Sales training

```txt
Leads
Opportunities
Quotations
Sales orders
Customer follow-up
```

### 14.3 Operations training

```txt
Creating jobs
Scheduling jobs
Assigning crews
Assigning rigs
Daily reports
Safety checklists
Field photos
Customer sign-off
```

### 14.4 Finance training

```txt
Invoices
Payments
Receivables
Reports
Exporting data
Accounting review
```

### 14.5 Field worker training

```txt
Login
View assigned jobs
Submit daily report
Upload photos
Complete checklist
Report issues
```

---

## 15. User acceptance testing

### Scenario 1 — Sales to job

```txt
Create lead
Create opportunity
Create quotation
Approve quotation
Create sales order
Create project
Create drilling job
```

### Scenario 2 — Field execution

```txt
Assign crew
Assign rig
Submit daily report
Add photos
Record depth log
Complete safety checklist
Submit customer sign-off
```

### Scenario 3 — Inventory

```txt
Transfer material to vehicle warehouse
Use material on job
Confirm stock decreased
Review job material usage
```

### Scenario 4 — Invoice

```txt
Mark job completed
Generate invoice
Email invoice
Record payment
```

### Scenario 5 — Permissions

```txt
Field worker cannot access accounting
Client portal user sees only own jobs
Dispatcher can schedule but not edit accounting
Finance can invoice but not edit drilling logs
```

---

## 16. Go-live checklist

```txt
[ ] UAT completed
[ ] Critical issues fixed
[ ] Users trained
[ ] Production data imported
[ ] Email tested
[ ] Backup tested
[ ] Domain/SSL tested
[ ] First real process tested
[ ] Client admin accepts setup
[ ] Go-live date confirmed
[ ] Support channel open
```

---

## 17. Hypercare process

For the first 1–2 weeks after go-live:

```txt
Daily check-in
Review open issues
Review failed emails
Review user login problems
Review job/invoice flow
Review backup status
Fix urgent workflow problems
Document feature requests
```

Classify issues:

```txt
Bug
Configuration
Training issue
New feature request
Data cleanup
Permission issue
```

---

## 18. Support process

Create support tiers.

### Basic support

```txt
Email support
Response within 1–2 business days
Bug fixes
Documentation
```

### Pro support

```txt
Priority support
Implementation help
Monthly review call
Minor configuration changes
```

### Enterprise support

```txt
Dedicated channel
Custom domain/email
Advanced onboarding
Dedicated infrastructure optional
SLA
Custom development
```

Support ticket fields:

```txt
Client
Tenant/site
Reported by
Module
Priority
Issue type
Description
Screenshots
Steps to reproduce
Assigned to
Status
Resolution
```

---

## 19. Change request process

When client asks for a new thing:

```txt
1. Understand the business reason
2. Decide: configuration, reusable module, or one-off customization
3. Estimate effort
4. Decide if included in plan or paid implementation
5. Document acceptance criteria
6. Build in staging
7. Test with client
8. Release to production
```

Never allow random client requests to silently become core product changes.

---

## 20. Client handover package

At go-live, send:

```txt
Login URL
Admin user list
Support contact
Training notes
Basic how-to guide
Known limitations
Backup policy summary
Billing/plan summary
Change request process
```

Do not send root/server credentials.

---

## 21. Internal implementation notes

For every client, keep an internal page:

```txt
Tenant/site name
Server
Domains
Plan
Modules
Special settings
Custom fields
Custom reports
Integrations
Data import notes
Known issues
Backup path
Support history
```

---

## 22. Red flags during onboarding

Watch for:

```txt
Client does not know their process
Client wants everything customized before using anything
Client has dirty data but expects perfect migration
Client refuses to assign internal owner
Client wants enterprise white label on starter budget
Client asks for one-off custom work but wants SaaS pricing
Client has no person responsible for accounting/process decisions
```

Pause and clarify before proceeding.

---

## 23. References

```txt
Frappe users and permissions:
https://docs.frappe.io/framework/user/en/basics/users-and-permissions

Frappe sites:
https://docs.frappe.io/framework/user/en/basics/sites

ERPNext company setup:
https://docs.frappe.io/erpnext/company-setup

Frappe DocTypes/customization:
https://docs.frappe.io/framework/user/en/basics/doctypes
https://docs.frappe.io/framework/user/en/basics/doctypes/customize
```
