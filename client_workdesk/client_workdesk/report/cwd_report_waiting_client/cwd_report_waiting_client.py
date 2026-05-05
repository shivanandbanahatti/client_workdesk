# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _

from client_workdesk.report.cwd_report_helpers import desk_link, format_assignees


def execute(filters=None):
	columns = [
		{"label": _("Type"), "fieldname": "row_type", "fieldtype": "Data", "width": 100},
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Data", "width": 130},
		{"label": _("Subject"), "fieldname": "subject", "fieldtype": "Data", "width": 200},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Work Status"), "fieldname": "work_status", "fieldtype": "Data", "width": 120},
		{"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Data", "width": 160},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = []

	tasks = frappe.get_all(
		"Task",
		filters={"work_status": "Waiting for Client"},
		fields=["name", "subject", "customer", "project", "status", "work_status", "_assign"],
		order_by="modified desc",
		limit_page_length=500,
	)
	for t in tasks:
		rows.append(
			{
				"row_type": "Task",
				"name": t.name,
				"subject": t.subject,
				"customer": t.customer,
				"project": t.project,
				"status": t.status,
				"work_status": t.work_status or "",
				"assigned_to": format_assignees(t._assign),
				"doc_link": desk_link("Task", t.name),
			}
		)

	fups = frappe.get_all(
		"Follow-up",
		filters={"status": "Waiting for Client"},
		fields=["name", "subject", "customer", "project", "status", "owner_user"],
		order_by="modified desc",
		limit_page_length=500,
	)
	for f in fups:
		rows.append(
			{
				"row_type": "Follow-up",
				"name": f.name,
				"subject": f.subject,
				"customer": f.customer,
				"project": f.project,
				"status": f.status,
				"work_status": "",
				"assigned_to": frappe.db.get_value("User", f.owner_user, "full_name") if f.owner_user else "",
				"doc_link": desk_link("Follow-up", f.name),
			}
		)

	return columns, rows
