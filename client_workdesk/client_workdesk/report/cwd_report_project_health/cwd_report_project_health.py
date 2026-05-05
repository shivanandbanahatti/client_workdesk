# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import today


def execute(filters=None):
	td = today()
	columns = [
		{"label": _("Project"), "fieldname": "name", "fieldtype": "Link", "options": "Project", "width": 140},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project Health"), "fieldname": "project_health", "fieldtype": "Data", "width": 100},
		{"label": _("Health Reason"), "fieldname": "project_health_reason", "fieldtype": "Small Text", "width": 200},
		{"label": _("Open Tasks"), "fieldname": "open_tasks", "fieldtype": "Int", "width": 100},
		{"label": _("Overdue Tasks"), "fieldname": "overdue_tasks", "fieldtype": "Int", "width": 110},
		{"label": _("Waiting for Client Count"), "fieldname": "waiting_client", "fieldtype": "Int", "width": 160},
		{"label": _("Billing Status"), "fieldname": "billing_status", "fieldtype": "Data", "width": 130},
		{"label": _("Next Invoice Date"), "fieldname": "next_invoice_date", "fieldtype": "Date", "width": 120},
	]
	rows = frappe.db.sql(
		f"""
		SELECT
			p.name,
			p.customer,
			p.project_health,
			p.project_health_reason,
			p.billing_status,
			p.next_invoice_date,
			(
				SELECT COUNT(*) FROM `tabTask` t
				WHERE t.project = p.name
					AND t.status IN ('Open', 'Working', 'Overdue')
					AND IFNULL(t.work_status, '') NOT IN ('Done', 'Cancelled')
			) AS open_tasks,
			(
				SELECT COUNT(*) FROM `tabTask` t
				WHERE t.project = p.name
					AND t.exp_end_date IS NOT NULL
					AND t.exp_end_date < %(td)s
					AND t.status NOT IN ('Cancelled', 'Completed')
					AND IFNULL(t.work_status, '') NOT IN ('Done', 'Cancelled')
			) AS overdue_tasks,
			(
				SELECT COUNT(*) FROM `tabTask` t
				WHERE t.project = p.name
					AND t.work_status = 'Waiting for Client'
			) AS waiting_client
		FROM `tabProject` p
		WHERE p.status = 'Open'
		ORDER BY p.modified DESC
		""",
		{"td": td},
		as_dict=True,
	)
	for r in rows:
		for k in ("open_tasks", "overdue_tasks", "waiting_client"):
			r[k] = int(r[k] or 0)
	return columns, rows
