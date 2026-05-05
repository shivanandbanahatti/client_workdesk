# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import today
from frappe.utils.data import format_time

from client_workdesk.report.cwd_report_helpers import desk_link


def execute(filters=None):
	td = today()
	columns = [
		{"label": _("Follow-up"), "fieldname": "name", "fieldtype": "Link", "options": "Follow-up", "width": 130},
		{"label": _("Subject"), "fieldname": "subject", "fieldtype": "Data", "width": 200},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": _("Due Time"), "fieldname": "due_time", "fieldtype": "Data", "width": 80},
		{"label": _("Type"), "fieldname": "follow_up_type", "fieldtype": "Data", "width": 120},
		{"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 90},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Owner"), "fieldname": "owner_user", "fieldtype": "Link", "options": "User", "width": 140},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = frappe.get_all(
		"Follow-up",
		filters={"due_date": td, "status": ["not in", ["Done", "Cancelled"]]},
		fields=[
			"name",
			"subject",
			"customer",
			"project",
			"due_date",
			"due_time",
			"follow_up_type",
			"priority",
			"status",
			"owner_user",
		],
		order_by="due_time asc, name asc",
		limit_page_length=1000,
	)
	for r in rows:
		r["due_time"] = format_time(r["due_time"]) if r.get("due_time") else ""
		r["doc_link"] = desk_link("Follow-up", r["name"])
	return columns, rows
