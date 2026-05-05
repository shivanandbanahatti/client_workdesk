# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _

from client_workdesk.report.cwd_report_helpers import desk_link


def execute(filters=None):
	columns = [
		{"label": _("Sales Invoice"), "fieldname": "name", "fieldtype": "Link", "options": "Sales Invoice", "width": 130},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 140},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 120},
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 110},
		{"label": _("Outstanding"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Payment Follow-up"), "fieldname": "payment_follow_up_status", "fieldtype": "Data", "width": 130},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = frappe.get_all(
		"Sales Invoice",
		filters={"docstatus": 1, "outstanding_amount": [">", 0]},
		fields=[
			"name",
			"customer",
			"project",
			"posting_date",
			"due_date",
			"grand_total",
			"outstanding_amount",
			"status",
			"payment_follow_up_status",
		],
		order_by="due_date asc, outstanding_amount desc",
		limit_page_length=1000,
	)
	for r in rows:
		r["doc_link"] = desk_link("Sales Invoice", r.name)
	return columns, rows
