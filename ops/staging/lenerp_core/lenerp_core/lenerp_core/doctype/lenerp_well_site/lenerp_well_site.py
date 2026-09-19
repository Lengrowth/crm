from __future__ import annotations

import frappe
from frappe.model.document import Document


class LenERPWellSite(Document):
    """Customer-owned well/site record used by drilling and service jobs."""

    def validate(self) -> None:
        if self.latitude is not None and not -90 <= float(self.latitude) <= 90:
            frappe.throw("Latitude must be between -90 and 90.")
        if self.longitude is not None and not -180 <= float(self.longitude) <= 180:
            frappe.throw("Longitude must be between -180 and 180.")
        if self.depth_m is not None and float(self.depth_m) < 0:
            frappe.throw("Depth cannot be negative.")
