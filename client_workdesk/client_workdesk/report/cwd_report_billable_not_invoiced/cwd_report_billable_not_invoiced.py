# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _

from client_workdesk.report.cwd_report_helpers import desk_link, format_assignees


def execute(filters=None):
	columns = [
		{"label": _("Type"), "fieldname": "row_type", "fieldtype": "Data", "width": 100},
		{"label": _("ID"), "fieldname": "name", "fieldtype": "Data", "width": 130},
		{"label": _("Subject / Title"), "fieldname": "title", "fieldtype": "Data", "width": 200},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Billable Hours"), "fieldname": "billable_hours", "fieldtype": "Float", "width": 110},
		{"label": _("Billing / Billed %"), "fieldname": "billing_note", "fieldtype": "Data", "width": 160},
		{"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Data", "width": 140},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = []

	tasks = frappe.get_all(
		"Task",
		filters={
			"status": ["in", ["Open", "Working", "Overdue"]],
			"billing_status": ["in", ["Billable", "Ready to Invoice"]],
		},
		fields=[
			"name",
			"subject",
			"customer",
			"project",
			"actual_hours",
			"billing_status",
			"_assign",
		],
		order_by="project asc, name asc",
		limit_page_length=500,
	)
	for t in tasks:
		rows.append(
			{
				"row_type": "Task",
				"name": t.name,
				"title": t.subject,
				"customer": t.customer,
				"project": t.project,
				"billable_hours": t.actual_hours or 0,
				"billing_note": t.billing_status or "",
				"assigned_to": format_assignees(t._assign),
				"doc_link": desk_link("Task", t.name),
			}
		)

	tss = frappe.get_all(
		"Timesheet",
		filters={
			"docstatus": 1,
			"total_billable_hours": [">", 0],
			"per_billed": ["<", 100],
		},
		fields=[
			"name",
			"customer",
			"project",
			"total_billable_hours",
			"total_billed_hours",
			"per_billed",
			"sales_invoice",
			"employee",
		],
		order_by="project asc, name asc",
		limit_page_length=500,
	)
	for ts in tss:
		note = f"{ts.per_billed or 0}% billed"
		if ts.sales_invoice:
			note += f" ({ts.sales_invoice})"
		emp_name = frappe.db.get_value("Employee", ts.employee, "employee_name") if ts.employee else ""
		rows.append(
			{
				"row_type": "Timesheet",
				"name": ts.name,
				"title": ts.name,
				"customer": ts.customer,
				"project": ts.project,
				"billable_hours": ts.total_billable_hours or 0,
				"billing_note": note,
				"assigned_to": emp_name,
				"doc_link": desk_link("Timesheet", ts.name),
			}
		)

	return columns, rows
