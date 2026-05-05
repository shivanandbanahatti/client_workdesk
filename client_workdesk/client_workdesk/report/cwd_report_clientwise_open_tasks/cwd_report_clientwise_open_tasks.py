# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _


def execute(filters=None):
	columns = [
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 160},
		{"label": _("Open Tasks"), "fieldname": "task_count", "fieldtype": "Int", "width": 110},
	]
	rows = frappe.db.sql(
		"""
		SELECT customer, project, COUNT(*) AS task_count
		FROM `tabTask`
		WHERE status IN ('Open', 'Working', 'Overdue')
			AND IFNULL(work_status, '') NOT IN ('Done', 'Cancelled')
		GROUP BY customer, project
		HAVING IFNULL(customer, '') != '' OR IFNULL(project, '') != ''
		ORDER BY customer, project
		""",
		as_dict=True,
	)
	return columns, rows
