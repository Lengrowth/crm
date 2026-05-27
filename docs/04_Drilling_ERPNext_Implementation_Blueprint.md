# 04 — Drilling ERPNext Implementation Blueprint

**Project:** ERPNext/Frappe-based SaaS for drilling and field operations businesses  
**Audience:** Fernando / LenGrowth implementation and product team  
**Last updated:** 2026-05-21  
**Status:** Detailed implementation blueprint

---

## 1. Purpose

This document explains how to configure ERPNext for the first drilling/manual field operations company, and what you should build as custom functionality.

The goal is to avoid two mistakes:

1. Building things ERPNext already does.
2. Forcing drilling-specific operations into generic ERPNext fields where they do not belong.

ERPNext should provide the business backbone:

```txt
CRM
Sales
Quotations
Invoices
Purchasing
Suppliers
Stock/inventory
Warehouses
Projects
Tasks
Employees
Assets/equipment
Maintenance
Accounting
Reports
Permissions
Documents/attachments
```

Your custom app should provide the vertical field-operations layer:

```txt
Drilling Job
Borehole / Well
Rig Assignment
Crew Assignment
Daily Drilling Report
Depth Log
Safety Checklist
Field Photos
Customer Sign-off
Material Usage per Job
Rig/Fleet Dispatch
Job Costing Extensions
```

---

## 2. Implementation principle

Do not build a “drilling ERP” from scratch.

Build:

```txt
ERPNext base
  + Field Operations shared module
  + Drilling-specific module
  + Client-specific configuration
```

The product should later support other industries by reusing the same base:

```txt
Construction = ERPNext + Field Ops + Construction Pack
Drilling = ERPNext + Field Ops + Drilling Pack
Maintenance = ERPNext + Field Ops + Service Work Pack
Warehouse = ERPNext + Inventory + Warehouse Pack
Logistics = ERPNext + Fleet + Dispatch Pack
```

---

## 3. Discovery checklist for the first drilling client

### 3.1 Company/legal

```txt
Legal company name
Trading name
Tax ID
Country
Currency
Fiscal year start
Address
Phone/email
Bank details
Invoice terms
Payment terms
Taxes
Accounting requirements
Existing accounting system
QuickBooks usage
```

### 3.2 Sales/CRM

```txt
How leads arrive
Who qualifies leads
Sales pipeline stages
Quotation approval process
Typical quotation format
Price list or manual pricing
Discount rules
Deposit requirements
Customer contract process
```

### 3.3 Jobs/operations

```txt
Types of drilling jobs
Typical job lifecycle
Who schedules jobs
Who assigns crews
Who assigns rigs/equipment
How site surveys work
How daily work is reported
How job completion is confirmed
How customer sign-off happens
What causes job delays
What data must be captured in the field
```

### 3.4 Drilling-specific

```txt
Do they drill wells, boreholes, geotechnical holes, utility holes, or other?
Do they track depth?
Do they track soil/rock layers?
Do they need geological logs?
Do they need rig hours?
Do they need water levels?
Do they need GPS coordinates?
Do they need permits?
Do they need safety inspections?
Do they need before/after photos?
Do they need final drilling reports for clients?
```

### 3.5 Crew/workforce

```txt
Employees
Contractors
Crew leaders
Roles
Skills/certifications
Shift patterns
Timesheets
Overtime
Travel time
Per diem
```

### 3.6 Equipment/fleet

```txt
Rigs
Vehicles
Trailers
Generators
Compressors
Tools
Maintenance schedule
Fuel tracking
Equipment assignment
Equipment damage
Vehicle logs
GPS devices
```

### 3.7 Inventory/materials

```txt
Materials used on jobs
Consumables
Pipes/casings
Drilling mud/additives
Fuel
Bits/tools
Warehouse locations
Mobile stock in vehicles
Purchase process
Stock adjustment process
```

### 3.8 Reporting

```txt
Daily job report
Job profitability
Crew utilization
Rig utilization
Open jobs
Delayed jobs
Materials used per job
Revenue by customer
Maintenance due
Outstanding invoices
```

---

## 4. ERPNext module mapping

| Business need | ERPNext area | Notes |
|---|---|---|
| Leads and prospects | CRM | Use Lead and Opportunity |
| Customer records | Selling/CRM | Use Customer, Contact, Address |
| Quotations | Selling | Customize print format for drilling |
| Sales Orders | Selling | Use when customer approves quotation |
| Invoices | Accounts/Selling | Standard Sales Invoice |
| Suppliers | Buying | Standard Supplier |
| Purchase Orders | Buying | Standard PO flow |
| Materials | Stock | Item, Item Group, UOM |
| Warehouses | Stock | Main warehouse, vehicle warehouses |
| Stock movements | Stock | Stock Entry / Material Transfer |
| Employees | HR | Standard Employee |
| Projects/jobs backbone | Projects | Use Project as business job container |
| Tasks | Projects | Use for operational tasks/subtasks |
| Equipment | Assets | Use Asset for rigs, vehicles, tools |
| Maintenance | Assets/Maintenance | Standard maintenance can be extended |
| Accounting | Accounts | Company, accounts, taxes, ledgers |
| Permissions | Users/Roles | Use role-based permissions |
| Attachments | Core Frappe | Attach photos, PDFs, permits |

Custom app should add:

| Need | Custom DocType | Why custom? |
|---|---|---|
| Drilling operation record | Drilling Job | More specific than generic Project |
| Borehole/well data | Borehole | Specific technical record |
| Daily site report | Daily Drilling Report | Repeated field report structure |
| Depth measurements | Depth Log | Technical drilling data |
| Crew assignment | Crew Assignment | Field scheduling concept |
| Rig assignment | Rig Assignment | Link rig to job/date/operator |
| Safety inspection | Safety Checklist | Field compliance |
| Customer sign-off | Job Sign-off | Operational approval before invoice |
| Photos with categories | Field Photo Log | Better metadata than generic attachments |
| Job material usage | Job Material Usage | Link inventory to job and report |
| Field issue/delay | Job Incident | Operations-specific problem tracking |
| Final report | Drilling Completion Report | Client-facing output |

---

## 5. Recommended data model

### 5.1 ERPNext base objects

```txt
Customer
Contact
Address
Lead
Opportunity
Quotation
Sales Order
Sales Invoice
Supplier
Purchase Order
Item
Warehouse
Stock Entry
Project
Task
Employee
Asset
Maintenance Schedule
Company
Account
Cost Center
```

### 5.2 Custom app objects

```txt
Drilling Job
Borehole
Rig
Crew
Crew Assignment
Rig Assignment
Daily Drilling Report
Depth Log
Safety Checklist
Field Photo Log
Material Usage Record
Job Incident
Job Sign-off
Drilling Completion Report
```

### 5.3 Link model

```txt
Drilling Job
  ├── Customer
  ├── Project
  ├── Opportunity
  ├── Quotation
  ├── Sales Order
  ├── Sales Invoice
  ├── Site Address
  ├── Assigned Crew
  ├── Assigned Rig
  ├── Boreholes
  ├── Daily Reports
  ├── Material Usage
  ├── Safety Checklists
  ├── Field Photos
  └── Final Report
```

### 5.4 Naming series

```txt
Drilling Job: DJ-.YYYY.-.#####
Borehole: BH-.YYYY.-.#####
Daily Report: DDR-.YYYY.-.#####
Crew Assignment: CA-.YYYY.-.#####
Rig Assignment: RA-.YYYY.-.#####
Job Sign-off: JSO-.YYYY.-.#####
```

---

## 6. ERPNext setup sequence

### 6.1 Company setup

Configure:

```txt
Company name
Abbreviation
Default currency
Country
Fiscal year
Chart of accounts
Default receivable account
Default payable account
Default income account
Default expense account
Default warehouse
Default cost center
```

Chart of accounts is foundational. Choose carefully because accounting cleanup later can be painful.

### 6.2 Users and roles

Create internal roles:

```txt
Company Owner
Operations Manager
Dispatcher
Crew Leader
Field Worker
Inventory Manager
Fleet Manager
Sales Manager
Sales User
Accounts Manager
Accounts User
Project Manager
Executive Viewer
```

Custom roles:

```txt
Field Ops Manager
Field Ops User
Drilling Manager
Drilling Field Supervisor
Drilling Field Worker
Fleet Operations User
Client Sign-off User
```

Do not give normal workers access to accounting.

### 6.3 Customers and contacts

Set up:

```txt
Customer groups
Territories
Customer naming rule
Contact types
Address types
```

Example customer groups:

```txt
Residential
Commercial
Industrial
Government
Contractor
Partner
```

### 6.4 Items and materials

Create item groups:

```txt
Drilling Materials
Consumables
Fuel
Pipes/Casing
Tools
Safety Equipment
Services
Equipment Rental
Labor
Travel
Subcontracted Work
```

Examples:

```txt
Drilling Service - Standard
Site Survey Service
Rig Mobilization
Fuel
Casing Pipe
Drilling Bit
Concrete/Grout
Safety Kit
```

### 6.5 Warehouses

Recommended structure:

```txt
Main Warehouse
  ├── Consumables
  ├── Tools
  ├── Parts
  └── Safety Equipment

Vehicle Warehouses
  ├── Truck 01
  ├── Truck 02
  └── Service Van 01

Rig Warehouses
  ├── Rig 01 Stock
  └── Rig 02 Stock

Job Site Temporary
  ├── Job Site - ABC
  └── Job Site - XYZ
```

Vehicle warehouses help track what is physically in trucks.

### 6.6 Assets/equipment

Create asset categories:

```txt
Drilling Rig
Truck
Trailer
Generator
Compressor
Heavy Tool
Survey Equipment
Safety Equipment
```

Each rig/vehicle should have:

```txt
Asset ID
Serial/VIN
Purchase date
Maintenance schedule
Current status
Assigned operator
Current location
Insurance/registration details
```

### 6.7 Projects

Use Project as the financial/business container for a job.

Project fields:

```txt
Customer
Expected start date
Expected end date
Status
Cost center
Sales order
Budget
Project manager
```

Custom Drilling Job links to Project.

Do not rely only on Project if you need field-specific data. Use Project + Drilling Job.

---

## 7. Core business workflows

### 7.1 Lead to job workflow

```txt
Lead
  ↓
Opportunity
  ↓
Site Survey Task, if required
  ↓
Quotation
  ↓
Customer approval
  ↓
Sales Order
  ↓
Project created
  ↓
Drilling Job created
  ↓
Crew/Rig assigned
  ↓
Daily reports submitted
  ↓
Customer sign-off
  ↓
Sales Invoice
  ↓
Payment
  ↓
Job closed
```

### 7.2 Quote to invoice workflow

```txt
Quotation
  ├── Mobilization fee
  ├── Drilling service line
  ├── Materials estimate
  ├── Equipment/rental line
  ├── Labor line
  └── Taxes/terms

Approved Quotation
  ↓
Sales Order
  ↓
Project/Drilling Job
  ↓
Actual material/labor usage
  ↓
Invoice
```

### 7.3 Field execution workflow

```txt
Drilling Job: Scheduled
  ↓
Crew Assignment
  ↓
Rig Assignment
  ↓
Daily Drilling Report
  ↓
Depth Logs
  ↓
Material Usage
  ↓
Safety Checklist
  ↓
Field Photos
  ↓
Incident/delay report if needed
  ↓
Completion Report
  ↓
Customer Sign-off
```

### 7.4 Inventory usage workflow

```txt
Material loaded from Main Warehouse to Truck Warehouse
  ↓
Material used on Drilling Job
  ↓
Job Material Usage record created
  ↓
Stock Entry created
  ↓
Cost linked to Project/Job
  ↓
Report shows material cost per job
```

### 7.5 Maintenance workflow

```txt
Rig/Vehicle maintenance schedule
  ↓
Maintenance due notification
  ↓
Maintenance task/work order
  ↓
Parts consumed
  ↓
Downtime recorded
  ↓
Asset maintenance history updated
```

---

## 8. Custom DocTypes in detail

### 8.1 Drilling Job

Purpose: central field operations record.

Fields:

```txt
Job ID
Customer
Project
Opportunity
Quotation
Sales Order
Site Address
GPS coordinates
Job type
Job status
Priority
Expected start date
Expected end date
Actual start date
Actual end date
Operations manager
Dispatcher
Crew leader
Assigned rig
Assigned crew
Estimated depth
Actual depth
Number of boreholes
Permit required
Permit status
Safety risk level
Invoice status
Sign-off status
Notes
```

Statuses:

```txt
Draft
Quoted
Approved
Scheduled
Crew Assigned
In Progress
Paused
Completed
Awaiting Sign-off
Ready To Invoice
Invoiced
Closed
Cancelled
```

### 8.2 Borehole

Fields:

```txt
Borehole ID
Drilling Job
Borehole number
GPS coordinates
Planned depth
Actual depth
Diameter
Start date/time
End date/time
Water level
Soil/rock notes
Completion status
```

### 8.3 Depth Log

Fields:

```txt
Drilling Job
Borehole
Depth from
Depth to
Material/soil type
Rock type
Water encountered
Tool/bit used
Notes
Photo attachment
Recorded by
Recorded at
```

### 8.4 Daily Drilling Report

Fields:

```txt
Report date
Drilling Job
Crew leader
Weather
Start time
End time
Rig hours
Crew hours
Progress summary
Depth achieved today
Materials used
Equipment used
Delays
Incidents
Safety notes
Photos
Customer notes
Submitted by
Approved by
```

### 8.5 Crew

Fields:

```txt
Crew name
Crew leader
Members
Skills
Default vehicle
Default rig
Active/inactive
```

### 8.6 Crew Assignment

Fields:

```txt
Drilling Job
Crew
Date
Start time
End time
Crew leader
Members
Status
Notes
```

### 8.7 Rig Assignment

Fields:

```txt
Drilling Job
Rig asset
Operator
Date/time from
Date/time to
Expected hours
Actual hours
Status
Notes
```

### 8.8 Safety Checklist

Fields:

```txt
Drilling Job
Date
Checklist template
Completed by
PPE checked
Site hazards checked
Equipment inspected
Emergency plan reviewed
Customer/site contact briefed
Issues found
Corrective actions
Signature
```

### 8.9 Field Photo Log

Fields:

```txt
Drilling Job
Borehole, optional
Report, optional
Photo category
Photo
Caption
Taken by
Taken at
GPS coordinates, optional
```

Categories:

```txt
Before work
During work
After work
Damage
Safety issue
Equipment
Material
Completion proof
```

### 8.10 Job Sign-off

Fields:

```txt
Drilling Job
Customer representative
Customer email
Sign-off date/time
Work accepted?
Comments
Signature image
Signed document PDF
Ready to invoice flag
```

---

## 9. Reports and dashboards

### 9.1 Operations dashboard

```txt
Jobs scheduled today
Jobs in progress
Jobs delayed
Crews assigned
Unassigned jobs
Rigs available
Rigs under maintenance
Safety issues
```

### 9.2 Job profitability dashboard

```txt
Quoted amount
Actual labor cost
Actual material cost
Equipment cost
Travel/fuel cost
Gross margin
Unbilled work
```

### 9.3 Fleet/equipment dashboard

```txt
Rig utilization
Vehicle utilization
Maintenance due
Fuel logs
Downtime
Repairs
```

### 9.4 Executive dashboard

```txt
Revenue this month
Open receivables
Jobs completed
Average job margin
Top customers
Delayed jobs
Crew utilization
```

---

## 10. Implementation phases

### Phase 1 — ERPNext base setup

```txt
Company
Users
Roles
CRM
Customers
Items
Warehouses
Projects
Quotations
Invoices
Basic reports
```

Goal: the client can manage sales, customers, inventory, and invoices.

### Phase 2 — Field operations module

```txt
Work orders/jobs
Crew assignments
Daily reports
Photos
Job statuses
Customer sign-off
```

Goal: the client can run jobs operationally.

### Phase 3 — Drilling-specific module

```txt
Boreholes
Depth logs
Rig assignment
Drilling reports
Safety checklists
Completion reports
```

Goal: the system fits drilling work.

### Phase 4 — Costing and automation

```txt
Material usage per job
Labor hours per job
Equipment hours
Job margin reports
Notifications
Approval workflows
```

Goal: the client sees profitability and control.

### Phase 5 — Mobile/offline and integrations

```txt
Mobile-friendly forms
Offline sync, if needed
QuickBooks integration
GPS integrations
Client portal
```

Goal: mature SaaS product.

---

## 11. MVP scope for first client

Recommended MVP:

```txt
ERPNext setup
Customers
CRM
Quotations
Invoices
Items/materials
Warehouses
Employees
Assets
Projects
Drilling Job
Crew Assignment
Rig Assignment
Daily Drilling Report
Safety Checklist
Field Photos
Job Sign-off
Basic dashboards
```

Delay:

```txt
Full offline mobile
Advanced GPS tracking
Full QuickBooks sync
Complex payroll
AI reports
Predictive maintenance
Advanced route optimization
```

---

## 12. Data migration plan

Import sequence:

```txt
Companies/settings
Users
Customers
Contacts
Suppliers
Items
Warehouses
Opening stock
Employees
Assets/equipment
Open opportunities
Open quotations
Open jobs/projects
Outstanding invoices, if needed
```

Required CSV templates:

```txt
Customers
Contacts
Suppliers
Items
Warehouses
Employees
Assets
Vehicles
Open jobs
Materials opening balance
```

Validation rules:

```txt
No duplicate customer names
Valid emails
Valid phone formats where possible
Required addresses present
Items have UOM
Stock items have warehouses
Assets have categories
Employees have names and roles
```

---

## 13. Go-live checklist

```txt
[ ] ERPNext base configured
[ ] Company setup complete
[ ] Chart of accounts reviewed
[ ] Users created
[ ] Roles assigned
[ ] Customer data imported
[ ] Items/materials configured
[ ] Warehouses configured
[ ] Assets/equipment configured
[ ] Drilling Job workflow tested
[ ] Quotation flow tested
[ ] Invoice flow tested
[ ] Inventory usage flow tested
[ ] Daily report flow tested
[ ] Customer sign-off tested
[ ] Backup tested
[ ] Email sending tested
[ ] Training completed
[ ] Support channel established
[ ] First real job entered under supervision
```

---

## 14. Product rule for SaaS growth

Every new client request should be classified as:

### Configuration

```txt
Different logo
Different checklist
Different invoice template
Different job statuses
Different roles
```

Implement through settings/templates.

### Reusable module

```txt
Rig maintenance
Fleet dispatch
Equipment certification
Customer portal
QuickBooks sync
```

Build as product modules.

### One-off customization

```txt
Very specific report only one client wants
Unique approval process for one client
Legacy import from strange software
```

Charge implementation fees. Do not pollute the core SaaS.

---

## 15. References

```txt
ERPNext company setup:
https://docs.frappe.io/erpnext/company-setup

ERPNext/Frappe users and permissions:
https://docs.frappe.io/framework/user/en/basics/users-and-permissions

Frappe DocTypes:
https://docs.frappe.io/framework/user/en/basics/doctypes

Frappe customize DocTypes:
https://docs.frappe.io/framework/user/en/basics/doctypes/customize

ERPNext assets:
https://docs.frappe.io/erpnext/v14/user/manual/en/asset

ERPNext vehicle / vehicle log:
https://docs.frappe.io/erpnext/v12/user/manual/en/human-resources/vehicle
https://docs.frappe.io/erpnext/v12/user/manual/en/human-resources/vehicle-log
```
