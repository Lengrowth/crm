"""Opt-in, idempotent synthetic Champion demonstration data.

Run from an ERPNext bench:

    bench --site <staging-site> execute lenerp_core.demo_seed.seed
    bench --site <staging-site> execute lenerp_core.demo_seed.status
    bench --site <staging-site> execute lenerp_core.demo_seed.reset

The seed uses clearly fictitious records and never reads external files or
credentials. It is deliberately separate from install/migrate hooks so a
normal app deployment cannot create demo data by accident.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import frappe
from frappe.utils import add_days, today


DEMO_COMPANY = "DEMO Champion Well Drilling"
DEMO_PREFIX = "DEMO-CHAMPION-"


def _exists(doctype: str, name: str) -> bool:
    return bool(frappe.db.exists(doctype, name))


def _insert(doctype: str, name: str, values: dict[str, Any]) -> str:
    if _exists(doctype, name):
        # Reconcile scalar fields so rerunning the seed upgrades an earlier
        # synthetic snapshot without touching unrelated records. Child-table
        # payloads are intentionally left intact because their parent
        # documents may already be submitted.
        for field, value in values.items():
            if isinstance(value, (list, dict)):
                continue
            frappe.db.set_value(doctype, name, field, value, update_modified=False)
        return name
    doc = frappe.get_doc({"doctype": doctype, "name": name, **values})
    doc.insert(ignore_permissions=True)
    return doc.name


def _ensure_warehouse_types() -> None:
    """Provide the standard ERPNext link used by a new company's transit warehouse."""
    if not _exists("Warehouse Type", "Transit"):
        _insert(
            "Warehouse Type",
            "Transit",
            {"description": "Standard ERPNext transit warehouse type for synthetic demo setup."},
        )


def _ensure_party_defaults() -> None:
    """Provide the minimal ERPNext party masters used by synthetic customers."""
    if not _exists("Customer Group", "All Customer Groups"):
        _insert(
            "Customer Group",
            "All Customer Groups",
            {"customer_group_name": "All Customer Groups", "is_group": 1},
        )
    if not _exists("Customer Group", "Commercial"):
        _insert(
            "Customer Group",
            "Commercial",
            {
                "customer_group_name": "Commercial",
                "parent_customer_group": "All Customer Groups",
                "is_group": 0,
            },
        )
    if not _exists("Territory", "All Territories"):
        _insert(
            "Territory",
            "All Territories",
            {"territory_name": "All Territories", "is_group": 1},
        )
    if not _exists("Supplier Group", "All Supplier Groups"):
        _insert(
            "Supplier Group",
            "All Supplier Groups",
            {"supplier_group_name": "All Supplier Groups", "is_group": 1},
        )
    if not _exists("UOM", "Nos"):
        _insert("UOM", "Nos", {"uom_name": "Nos", "must_be_whole_number": 0})
    if not _exists("Item Group", "All Item Groups"):
        _insert(
            "Item Group",
            "All Item Groups",
            {"item_group_name": "All Item Groups", "is_group": 1},
        )
    if not _exists("Item Group", "Products"):
        _insert(
            "Item Group",
            "Products",
            {"item_group_name": "Products", "is_group": 0, "parent_item_group": "All Item Groups"},
        )
    if not _exists("Item Group", "Fixed Assets"):
        _insert(
            "Item Group",
            "Fixed Assets",
            {"item_group_name": "Fixed Assets", "is_group": 0, "parent_item_group": "All Item Groups"},
        )
    if not _exists("Sales Stage", "Prospecting"):
        _insert("Sales Stage", "Prospecting", {"stage_name": "Prospecting"})


def _company() -> str:
    _ensure_warehouse_types()
    _ensure_party_defaults()
    return _insert(
        "Company",
        DEMO_COMPANY,
        {
            "company_name": DEMO_COMPANY,
            "abbr": "DCH",
            "default_currency": "USD",
            "country": "United States",
            "is_group": 0,
        },
    )


def _core_records(company: str) -> dict[str, list[str]]:
    customers = [
        ("DEMO-CHAMPION-CUSTOMER-01", "DEMO-CHAMPION-North Ridge Farm", "Commercial"),
        ("DEMO-CHAMPION-CUSTOMER-02", "DEMO-CHAMPION-Pine Creek Estates", "Commercial"),
        ("DEMO-CHAMPION-CUSTOMER-03", "DEMO-CHAMPION-Red Mesa Utilities", "Commercial"),
    ]
    customer_names: list[str] = []
    for name, customer_name, customer_type in customers:
        customer_names.append(
            _insert(
                "Customer",
                name,
                {
                    "customer_name": customer_name,
                    "customer_type": "Company",
                    "customer_group": "Commercial",
                    "territory": "All Territories",
                },
            )
        )

    contact_names: list[str] = []
    for name, first_name, last_name, customer in (
        ("DEMO-CHAMPION-CONTACT-01", "DEMO-CHAMPION-Maya", "Ellis", customer_names[0]),
        ("DEMO-CHAMPION-CONTACT-02", "DEMO-CHAMPION-Jonah", "Reed", customer_names[1]),
        ("DEMO-CHAMPION-CONTACT-03", "DEMO-CHAMPION-Ari", "Santos", customer_names[2]),
    ):
        contact_names.append(
            _insert(
                "Contact",
                name,
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "links": [{"link_doctype": "Customer", "link_name": customer}],
                },
            )
        )

    well_names: list[str] = []
    well_values = (
        ("DEMO-WELL-NR-01", "North Ridge Well 01", customer_names[0], "North Ridge", "7", "10.00", "-84.00", "118", "6-inch submersible pump; 30 m rising main"),
        ("DEMO-WELL-PC-02", "Pine Creek Well 02", customer_names[1], "Pine Creek", "8", "10.02", "-84.03", "96", "5-inch pump; pressure tank service"),
        ("DEMO-WELL-RM-03", "Red Mesa Test Well", customer_names[2], "Red Mesa", "2", "31.50", "-110.10", "142", "Monitoring well; water-quality sample pending"),
    )
    for name, site_name, customer, city, status, lat, lon, depth, pump in well_values:
        well_names.append(
            _insert(
                "LenERP Well Site",
                name,
                {
                    "well_id": name.replace("DEMO-WELL-", "WELL-"),
                    "site_name": site_name,
                    "customer": customer,
                    "contact": contact_names[customer_names.index(customer)],
                    "status": "Active" if status != "2" else "Needs review",
                    "city": city,
                    "state": "Synthetic region",
                    "postal_code": "00000",
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "depth_m": float(depth),
                    "pump_specification": pump,
                    "operational_notes": "Fictitious demonstration record. Replace during Project Start.",
                },
            )
        )

    job_names: list[str] = []
    jobs = (
        ("DEMO-JOB-001", customer_names[0], well_names[0], "New well drilling", "Completed", -12, "Crew Atlas", "Completed synthetic drilling workflow; completion notes recorded."),
        ("DEMO-JOB-002", customer_names[1], well_names[1], "Pump installation", "In Progress", 1, "Crew Beacon", "Pump and pressure system inspection underway."),
        ("DEMO-JOB-003", customer_names[2], well_names[2], "Water testing", "Scheduled", 4, "Crew Cedar", "Collect sample and attach laboratory result after review."),
        ("DEMO-JOB-004", customer_names[0], well_names[0], "Maintenance", "Planned", 10, "Unassigned", "Routine annual service; confirm parts before scheduling."),
    )
    for name, customer, well, job_type, status, offset, crew, notes in jobs:
        job_name = _insert(
            "LenERP Drilling Job",
            name,
            {
                "customer": customer,
                "well_site": well,
                "job_type": job_type,
                # Workflow validation requires a new document to start in its
                # configured initial state. The final synthetic snapshot is
                # applied below through the database API, preserving the
                # production workflow transitions for interactive edits.
                "status": "Planned",
                "workflow_state": "Planned",
                "scheduled_date": add_days(today(), offset),
                "assigned_personnel": crew,
                "priority": "High" if status == "In Progress" else "Routine",
                "work_notes": notes,
                "completion_details": notes if status == "Completed" else None,
                "completed_on": add_days(today(), offset) if status == "Completed" else None,
            },
        )
        if status != "Planned":
            frappe.db.set_value(
                "LenERP Drilling Job",
                job_name,
                {"status": status, "workflow_state": status},
                update_modified=False,
            )
        job_names.append(job_name)

    return {"customers": customer_names, "contacts": contact_names, "wells": well_names, "jobs": job_names}


def _ensure_warehouse(company: str) -> str:
    return _insert(
        "Warehouse",
        "DEMO-CHAMPION-YARD-WAREHOUSE",
        {"warehouse_name": "DEMO-CHAMPION-Yard Warehouse", "company": company},
    )


def _ensure_asset_category(company: str) -> str:
    # ERPNext versions differ on whether Company exposes a default fixed-asset
    # account.  The Asset Category child table is stable, so resolve a valid
    # company leaf account without querying an optional Company column.
    account = frappe.db.get_value("Account", {"company": company, "is_group": 0}, "name")
    if not account:
        raise RuntimeError(f"No leaf account is available for synthetic Asset Category in {company}")
    return _insert(
        "Asset Category",
        "DEMO-CHAMPION-FIELD-EQUIPMENT",
        {
            "asset_category_name": "DEMO-CHAMPION Field Equipment",
            "non_depreciable_category": 1,
            "accounts": [{"company_name": company, "fixed_asset_account": account}],
        },
    )


def _commercial_records(company: str, customer: str, warehouse: str) -> dict[str, list[str]]:
    lead = _insert(
        "Lead",
        "DEMO-CHAMPION-LEAD-001",
        {"lead_name": "DEMO-CHAMPION-Avery Cole", "company_name": "DEMO-CHAMPION-Summit Springs HOA", "status": "Lead"},
    )
    opportunity = _insert(
        "Opportunity",
        "DEMO-CHAMPION-OPPORTUNITY-001",
        {"opportunity_from": "Customer", "party_name": customer, "status": "Open", "opportunity_amount": 1850, "transaction_date": today(), "company": company},
    )
    supplier = _insert(
        "Supplier",
        "DEMO-CHAMPION-SUPPLIER-01",
        {"supplier_name": "DEMO-CHAMPION-Blue Basin Supply", "supplier_group": "All Supplier Groups", "supplier_type": "Company"},
    )
    asset_category = _ensure_asset_category(company)
    item = _insert(
        "Item",
        "DEMO-CHAMPION-ITEM-PUMP",
        {"item_code": "DEMO-CHAMPION-ITEM-PUMP", "item_name": "DEMO-CHAMPION-Submersible Pump 6in", "description": "Synthetic pump for the Champion demo workflow.", "item_group": "Products", "stock_uom": "Nos", "is_stock_item": 1, "is_sales_item": 1, "is_purchase_item": 1},
    )
    fixed_asset_item = _insert(
        "Item",
        "DEMO-CHAMPION-ITEM-RIG",
        {"item_code": "DEMO-CHAMPION-ITEM-RIG", "item_name": "DEMO-CHAMPION-Drilling Rig", "description": "Synthetic fixed asset for the Champion demo workflow.", "item_group": "Fixed Assets", "stock_uom": "Nos", "is_stock_item": 0, "is_fixed_asset": 1, "asset_category": asset_category, "is_sales_item": 0, "is_purchase_item": 1},
    )
    quotation = _insert(
        "Quotation",
        "DEMO-CHAMPION-QUOTE-001",
        {"quotation_to": "Customer", "party_name": customer, "company": company, "transaction_date": today(), "items": [{"item_code": item, "qty": 1, "rate": 1850, "description": "Synthetic pump replacement quote"}]},
    )
    invoice = _insert(
        "Sales Invoice",
        "DEMO-CHAMPION-INVOICE-001",
        {"customer": customer, "company": company, "posting_date": today(), "due_date": add_days(today(), 30), "items": [{"item_code": item, "qty": 1, "rate": 1850, "description": "Synthetic pump replacement"}], "remarks": "Synthetic demonstration invoice; accounting settings remain provisional."},
    )
    invoice_doc = frappe.get_doc("Sales Invoice", invoice)
    if invoice_doc.docstatus == 0:
        invoice_doc.submit()
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

    payment = "DEMO-CHAMPION-PAYMENT-001"
    if not _exists("Payment Entry", payment):
        payment_doc = get_payment_entry("Sales Invoice", invoice)
        payment_doc.name = payment
        payment_doc.posting_date = today()
        payment_doc.insert(ignore_permissions=True)
        payment_doc.submit()
    receipt = _insert(
        "Purchase Receipt",
        "DEMO-CHAMPION-PURCHASE-RECEIPT-001",
        {"supplier": supplier, "company": company, "posting_date": today(), "items": [{"item_code": item, "qty": 5, "rate": 250, "warehouse": warehouse, "description": "Synthetic pump receipt"}]},
    )
    receipt_doc = frappe.get_doc("Purchase Receipt", receipt)
    if receipt_doc.docstatus == 0:
        receipt_doc.submit()
    return {
        "leads": [lead] if lead else [],
        "opportunities": [opportunity] if opportunity else [],
        "suppliers": [supplier] if supplier else [],
        "items": [item] if item else [],
        "fixed_asset_items": [fixed_asset_item],
        "asset_categories": [asset_category],
        "quotations": [quotation] if quotation else [],
        "invoices": [invoice] if invoice else [],
        "payments": [payment] if payment else [],
        "purchase_receipts": [receipt],
    }


def _inventory_records(company: str, item: str, fixed_asset_item: str, warehouse: str, supplier: str) -> dict[str, list[str]]:
    stock_entry = _insert(
        "Stock Entry",
        "DEMO-CHAMPION-STOCK-ISSUE-001",
        {"stock_entry_type": "Material Issue", "company": company, "posting_date": today(), "items": [{"item_code": item, "qty": 1, "s_warehouse": warehouse, "description": "Synthetic pump issued to drilling crew"}]},
    )
    stock_entry_doc = frappe.get_doc("Stock Entry", stock_entry)
    if stock_entry_doc.docstatus == 0:
        stock_entry_doc.submit()
    cost_center = frappe.db.get_value("Cost Center", {"company": company, "is_group": 0}, "name")
    if not cost_center:
        parent = frappe.db.get_value("Cost Center", {"company": company, "is_group": 1}, "name")
        cost_center = _insert("Cost Center", "DEMO-CHAMPION-COST-CENTER", {"cost_center_name": "DEMO-CHAMPION Field Operations", "company": company, "parent_cost_center": parent, "is_group": 0})
    assets: list[str] = []
    for name, asset_name in (
        ("DEMO-CHAMPION-ASSET-RIG-01", "DEMO-CHAMPION-Rig Atlas"),
        ("DEMO-CHAMPION-ASSET-TRUCK-01", "DEMO-CHAMPION-Service Truck Beacon"),
    ):
        asset = _insert(
            "Asset",
            name,
            {"asset_name": asset_name, "item_code": fixed_asset_item, "asset_category": frappe.db.get_value("Item", fixed_asset_item, "asset_category"), "company": company, "gross_purchase_amount": 1, "purchase_date": today(), "available_for_use_date": today(), "is_existing_asset": 1, "calculate_depreciation": 0, "cost_center": cost_center, "maintenance_required": 1},
        )
        assets.append(asset)
    team = _insert(
        "Asset Maintenance Team",
        "DEMO-CHAMPION-MAINTENANCE-TEAM",
        {"maintenance_team_name": "DEMO-CHAMPION Maintenance Team", "company": company, "maintenance_team_members": [{"team_member": "Administrator", "maintenance_role": "System Manager"}]},
    )
    maintenance: list[str] = []
    for asset in assets:
        maintenance_doc = _insert(
            "Asset Maintenance",
            f"DEMO-CHAMPION-MAINTENANCE-{asset.rsplit('-', 1)[-1]}",
            {"asset_name": asset, "company": company, "maintenance_team": team, "asset_maintenance_tasks": [{"maintenance_task": "Inspect drilling rig and service records", "maintenance_status": "Planned", "start_date": today(), "periodicity": "Monthly", "description": "Synthetic preventive maintenance task."}]},
        )
        maintenance.append(maintenance_doc)
    return {"warehouses": [warehouse], "stock_entries": [stock_entry], "assets": assets, "asset_maintenance": maintenance}


def seed() -> dict[str, Any]:
    """Create or reconcile all synthetic demo records and return exact counts."""
    company = _company()
    core = _core_records(company)
    warehouse = _ensure_warehouse(company)
    commercial = _commercial_records(company, core["customers"][0], warehouse)
    inventory = _inventory_records(company, commercial["items"][0], commercial["fixed_asset_items"][0], warehouse, commercial["suppliers"][0])
    frappe.db.commit()
    result = {"company": company, **core, **commercial, **inventory}
    result["counts"] = {key: len(value) if isinstance(value, list) else 1 for key, value in result.items() if key != "company"}
    print(f"{DEMO_PREFIX} synthetic seed complete counts={frappe.as_json(result['counts'])}")
    return result


def _delete_names(doctype: str, names: Iterable[str]) -> int:
    deleted = 0
    for name in names:
        if _exists(doctype, name):
            frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)
            deleted += 1
    return deleted


def reset() -> dict[str, int]:
    """Remove only records created by this seed; never touch non-demo data."""
    targets = (
        ("Payment Entry", "DEMO-%"),
        ("Stock Entry", "DEMO-%"),
        ("Purchase Receipt", "DEMO-%"),
        ("Asset Maintenance", "DEMO-%"),
        ("Asset Maintenance Team", "DEMO-%"),
        ("Sales Invoice", "DEMO-%"),
        ("Quotation", "DEMO-%"),
        ("Opportunity", "DEMO-%"),
        ("Lead", "DEMO-%"),
        ("LenERP Drilling Job", "DEMO-%"),
        ("LenERP Well Site", "DEMO-%"),
        ("Contact", "DEMO-%"),
        ("Customer", "DEMO-%"),
        ("Item", "DEMO-%"),
        ("Supplier", "DEMO-%"),
        ("Warehouse", "DEMO-%"),
        ("Asset", "DEMO-%"),
        ("Asset Category", "DEMO-%"),
        ("Cost Center", "DEMO-%"),
        ("Item Group", "DEMO-%"),
        ("Supplier Group", "DEMO-%"),
        ("UOM", "DEMO-%"),
        ("Company", DEMO_COMPANY),
    )
    deleted: dict[str, int] = {}
    for doctype, pattern in targets:
        names = [row.name for row in frappe.get_all(doctype, filters={"name": ["like", pattern]}, fields=["name"])]
        deleted[doctype] = _delete_names(doctype, names)
    frappe.db.commit()
    return deleted


def status() -> dict[str, Any]:
    """Read persisted demo counts without creating or mutating records."""
    doctypes = (
        ("Company", {"name": DEMO_COMPANY}),
        ("Customer", {"name": ["like", "DEMO-%"]}),
        ("Contact", {"name": ["like", "DEMO-%"]}),
        ("Lead", {"name": ["like", "DEMO-%"]}),
        ("Opportunity", {"name": ["like", "DEMO-%"]}),
        ("LenERP Well Site", {"name": ["like", "DEMO-%"]}),
        ("LenERP Drilling Job", {"name": ["like", "DEMO-%"]}),
        ("Supplier", {"name": ["like", "DEMO-%"]}),
        ("Item", {"name": ["like", "DEMO-%"]}),
        ("Warehouse", {"name": ["like", "DEMO-%"]}),
        ("Quotation", {"name": ["like", "DEMO-%"]}),
        ("Sales Invoice", {"name": ["like", "DEMO-%"]}),
        ("Payment Entry", {"name": ["like", "DEMO-%"]}),
        ("Purchase Receipt", {"name": ["like", "DEMO-%"]}),
        ("Stock Entry", {"name": ["like", "DEMO-%"]}),
        ("Asset", {"name": ["like", "DEMO-%"]}),
        ("Asset Maintenance", {"name": ["like", "DEMO-%"]}),
    )
    return {doctype: len(frappe.get_all(doctype, filters=filters, fields=["name"], limit_page_length=10000)) for doctype, filters in doctypes}
