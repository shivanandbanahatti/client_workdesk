# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe.utils import flt, getdate, today


def sales_invoice_validate(doc, method=None):
	"""Payment follow-up visibility for reports; mark Paid when fully settled (submitted only)."""
	if getattr(doc.flags, "cwd_skip_payment_follow_up_hook", False):
		return
	if doc.docstatus != 1:
		return

	if flt(doc.outstanding_amount) <= 0:
		if doc.payment_follow_up_status and doc.payment_follow_up_status != "Paid":
			doc.payment_follow_up_status = "Paid"
		return

	td = getdate(today())
	if doc.due_date:
		dd = getdate(doc.due_date)
		days_to_due = (dd - td).days
		# Due today, overdue, or within the next 7 days → surface on payment follow-up flows
		if days_to_due <= 7:
			if not doc.invoice_follow_up_date:
				doc.invoice_follow_up_date = dd if days_to_due >= 0 else td
			if not doc.payment_follow_up_status or doc.payment_follow_up_status == "Not Required":
				doc.payment_follow_up_status = "Pending"
