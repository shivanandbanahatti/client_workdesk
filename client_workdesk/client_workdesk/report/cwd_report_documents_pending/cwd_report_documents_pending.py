# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _

from client_workdesk.report.cwd_report_helpers import desk_link


def execute(filters=None):
	columns = [
		{"label": _("Checklist"), "fieldname": "name", "fieldtype": "Link", "options": "Client Document Checklist", "width": 160},
		{"label": _("Document Name"), "fieldname": "document_name", "fieldtype": "Data", "width": 180},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Direction"), "fieldname": "direction", "fieldtype": "Data", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = frappe.get_all(
		"Client Document Checklist",
		filters={},
		or_filters=[
			["status", "=", "Pending"],
			["direction", "in", ["To Be Shared", "To Be Received"]],
		],
		fields=["name", "document_name", "customer", "project", "direction", "status", "due_date"],
		order_by="due_date asc, customer asc",
		limit_page_length=1000,
	)
	for r in rows:
		r["doc_link"] = desk_link("Client Document Checklist", r.name)
	return columns, rows
