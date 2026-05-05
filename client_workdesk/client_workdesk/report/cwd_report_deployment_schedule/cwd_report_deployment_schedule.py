# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils.data import format_datetime

from client_workdesk.report.cwd_report_helpers import desk_link


def execute(filters=None):
	columns = [
		{"label": _("Deployment"), "fieldname": "name", "fieldtype": "Link", "options": "Deployment Plan", "width": 140},
		{"label": _("Title"), "fieldname": "title", "fieldtype": "Data", "width": 200},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Application"), "fieldname": "client_application", "fieldtype": "Link", "options": "Client Application", "width": 140},
		{"label": _("Environment"), "fieldname": "deployment_environment", "fieldtype": "Data", "width": 110},
		{"label": _("Deployment Date/Time"), "fieldname": "deployment_datetime", "fieldtype": "Data", "width": 160},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = frappe.get_all(
		"Deployment Plan",
		filters={},
		fields=[
			"name",
			"title",
			"customer",
			"project",
			"client_application",
			"deployment_environment",
			"deployment_datetime",
			"status",
		],
		order_by="deployment_datetime asc",
		limit_page_length=2000,
	)
	for r in rows:
		dt = r.get("deployment_datetime")
		r["deployment_datetime"] = format_datetime(dt) if dt else ""
		r["doc_link"] = desk_link("Deployment Plan", r.name)
	return columns, rows
