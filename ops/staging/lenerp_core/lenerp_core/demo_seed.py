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
        return name
    doc = frappe.get_doc({"doctype": doctype, "name": name, **values})
    doc.insert(ignore_permissions=True)
    return doc.name


def _try_insert(doctype: str, name: str, values: dict[str, Any]) -> str | None:
    """Insert optional ERPNext records without hiding required demo records."""
    try:
        return _insert(doctype, name, values)
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Synthetic demo: {doctype} {name}")
        frappe.db.rollback()
        return None


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
        ("DEMO-CHAMPION-CUSTOMER-01", "North Ridge Farm", "Commercial"),
        ("DEMO-CHAMPION-CUSTOMER-02", "Pine Creek Estates", "Commercial"),
        ("DEMO-CHAMPION-CUSTOMER-03", "Red Mesa Utilities", "Commercial"),
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
        ("DEMO-CHAMPION-CONTACT-01", "Maya", "Ellis", customer_names[0]),
        ("DEMO-CHAMPION-CONTACT-02", "Jonah", "Reed", customer_names[1]),
        ("DEMO-CHAMPION-CONTACT-03", "Ari", "Santos", customer_names[2]),
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
        job_names.append(
            _insert(
                "LenERP Drilling Job",
                name,
                {
                    "customer": customer,
                    "well_site": well,
                    "job_type": job_type,
                    "status": status,
                    "workflow_state": status,
                    "scheduled_date": add_days(today(), offset),
                    "assigned_personnel": crew,
                    "priority": "High" if status == "In Progress" else "Routine",
                    "work_notes": notes,
                    "completion_details": notes if status == "Completed" else None,
                    "completed_on": add_days(today(), offset) if status == "Completed" else None,
                },
            )
        )

    return {"customers": customer_names, "contacts": contact_names, "wells": well_names, "jobs": job_names}


def _commercial_records(company: str, customer: str) -> dict[str, list[str]]:
    lead = _try_insert(
        "Lead",
        "DEMO-CHAMPION-LEAD-001",
        {"lead_name": "Avery Cole (Demo)", "company_name": "Summit Springs HOA (Demo)", "status": "Lead", "source": "Website"},
    )
    opportunity = _try_insert(
        "Opportunity",
        "DEMO-CHAMPION-OPPORTUNITY-001",
        {"opportunity_from": "Customer", "party_name": customer, "status": "Open", "opportunity_amount": 1850, "transaction_date": today(), "company": company},
    )
    supplier = _try_insert(
        "Supplier",
        "DEMO-CHAMPION-SUPPLIER-01",
        {"supplier_name": "Blue Basin Supply (Demo)", "supplier_group": "All Supplier Groups", "supplier_type": "Company"},
    )
    item = _try_insert(
        "Item",
        "DEMO-CHAMPION-ITEM-PUMP",
        {"item_code": "DEMO-CHAMPION-ITEM-PUMP", "item_name": "Submersible Pump 6in (Demo)", "item_group": "Products", "stock_uom": "Nos", "is_stock_item": 1},
    )
    quotation = None
    invoice = None
    payment = None
    if item:
        quotation = _try_insert(
            "Quotation",
            "DEMO-CHAMPION-QUOTE-001",
            {"quotation_to": "Customer", "party_name": customer, "company": company, "transaction_date": today(), "items": [{"item_code": item, "qty": 1, "rate": 1850, "description": "Synthetic pump replacement quote"}]},
        )
        invoice = _try_insert(
            "Sales Invoice",
            "DEMO-CHAMPION-INVOICE-001",
            {"customer": customer, "company": company, "posting_date": today(), "due_date": add_days(today(), 30), "items": [{"item_code": item, "qty": 1, "rate": 1850, "description": "Synthetic pump replacement"}], "remarks": "Synthetic demonstration invoice; accounting settings remain provisional."},
        )
        if invoice:
            try:
                invoice_doc = frappe.get_doc("Sales Invoice", invoice)
                invoice_doc.submit()
                from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

                payment_doc = get_payment_entry("Sales Invoice", invoice)
                payment_doc.name = "DEMO-CHAMPION-PAYMENT-001"
                payment_doc.posting_date = today()
                payment_doc.insert(ignore_permissions=True)
                payment_doc.submit()
                payment = payment_doc.name
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Synthetic demo: payment entry")
                frappe.db.rollback()
    return {
        "leads": [lead] if lead else [],
        "opportunities": [opportunity] if opportunity else [],
        "suppliers": [supplier] if supplier else [],
        "items": [item] if item else [],
        "quotations": [quotation] if quotation else [],
        "invoices": [invoice] if invoice else [],
        "payments": [payment] if payment else [],
    }


def _inventory_records(company: str, item: str | None) -> dict[str, list[str]]:
    warehouse = _try_insert(
        "Warehouse",
        "DEMO-CHAMPION-YARD-WAREHOUSE",
        {"warehouse_name": "Demo Yard Warehouse", "company": company, "parent_warehouse": None},
    )
    assets: list[str] = []
    if item:
        for name, asset_name in (
            ("DEMO-CHAMPION-ASSET-RIG-01", "Rig Atlas (Demo)"),
            ("DEMO-CHAMPION-ASSET-TRUCK-01", "Service Truck Beacon (Demo)"),
        ):
            asset = _try_insert(
                "Asset",
                name,
                {"asset_name": asset_name, "item_code": item, "company": company, "gross_purchase_amount": 1, "available_for_use_date": today()},
            )
            if asset:
                assets.append(asset)
    return {"warehouses": [warehouse] if warehouse else [], "assets": assets}


def seed() -> dict[str, Any]:
    """Create or reconcile all synthetic demo records and return exact counts."""
    company = _company()
    core = _core_records(company)
    commercial = _commercial_records(company, core["customers"][0])
    inventory = _inventory_records(company, commercial["items"][0] if commercial["items"] else None)
    frappe.db.commit()
    result = {"company": company, **core, **commercial, **inventory}
    result["counts"] = {key: len(value) if isinstance(value, list) else 1 for key, value in result.items() if key != "company"}
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
        ("Company", DEMO_COMPANY),
    )
    deleted: dict[str, int] = {}
    for doctype, pattern in targets:
        names = [row.name for row in frappe.get_all(doctype, filters={"name": ["like", pattern]}, fields=["name"])]
        deleted[doctype] = _delete_names(doctype, names)
    frappe.db.commit()
    return deleted


def status() -> dict[str, Any]:
    """Return persisted demo counts for runbook evidence."""
    doctypes = ("Company", "Customer", "Contact", "LenERP Well Site", "LenERP Drilling Job", "Supplier", "Item", "Quotation", "Sales Invoice", "Payment Entry", "Asset")
    result = {doctype: frappe.db.count(doctype, {"name": ["like", DEMO_PREFIX + "%"]}) for doctype in doctypes}
    result["Company"] = int(_exists("Company", DEMO_COMPANY))
    return result
