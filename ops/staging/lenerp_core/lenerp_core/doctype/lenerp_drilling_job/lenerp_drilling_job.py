from __future__ import annotations

import frappe
from frappe.model.document import Document


class LenERPDrillingJob(Document):
    """Persisted field job with controlled status changes and assignments."""

    def validate(self) -> None:
        if self.scheduled_date and self.completed_on and self.completed_on < self.scheduled_date:
            frappe.throw("Completion date cannot be before the scheduled date.")
        if self.status == "Completed" and not self.completion_details:
            frappe.throw("Completion details are required before a job is completed.")

