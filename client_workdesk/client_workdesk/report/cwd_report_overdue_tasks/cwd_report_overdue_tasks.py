# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import today

from client_workdesk.report.cwd_report_helpers import desk_link, format_assignees


def execute(filters=None):
	td = today()
	columns = [
		{"label": _("Task"), "fieldname": "name", "fieldtype": "Link", "options": "Task", "width": 120},
		{"label": _("Subject"), "fieldname": "subject", "fieldtype": "Data", "width": 200},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Due Date"), "fieldname": "exp_end_date", "fieldtype": "Date", "width": 100},
		{"label": _("Priority"), "fieldname": "task_priority", "fieldtype": "Data", "width": 90},
		{"label": _("Work Status"), "fieldname": "work_status", "fieldtype": "Data", "width": 120},
		{"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Data", "width": 160},
		{"label": _("Blocked"), "fieldname": "blocked", "fieldtype": "Check", "width": 70},
		{"label": _("Blocked Reason"), "fieldname": "blocked_reason", "fieldtype": "Small Text", "width": 200},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = frappe.db.sql(
		"""
		SELECT name, subject, customer, project, exp_end_date, task_priority, work_status,
			_assign, blocked, blocked_reason
		FROM `tabTask`
		WHERE exp_end_date IS NOT NULL
			AND exp_end_date < %(td)s
			AND status NOT IN ('Cancelled', 'Completed')
			AND IFNULL(work_status, '') NOT IN ('Done', 'Cancelled')
		ORDER BY exp_end_date ASC, name
		""",
		{"td": td},
		as_dict=True,
	)
	for r in rows:
		r["assigned_to"] = format_assignees(r.pop("_assign", None))
		r["doc_link"] = desk_link("Task", r.name)
	return columns, rows
