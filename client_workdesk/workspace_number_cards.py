# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

"""Number card methods (type Custom) for Client Work Desk workspace."""

import frappe
from frappe.utils import today
from frappe.utils.data import get_datetime


@frappe.whitelist()
def cwd_my_tasks_due_today(filters=None):
	user = frappe.session.user
	td = today()
	n = frappe.db.count(
		"Task",
		{
			"exp_end_date": td,
			"_assign": ["like", f"%{user}%"],
			"work_status": ["not in", ["Done", "Cancelled"]],
		},
	)
	return {
		"value": n,
		"fieldtype": "Int",
		"route": ["List", "Task", "List"],
		"route_options": {"exp_end_date": td},
	}


@frappe.whitelist()
def cwd_my_overdue_tasks(filters=None):
	user = frappe.session.user
	td = today()
	n = frappe.db.count(
		"Task",
		{
			"exp_end_date": ["<", td],
			"_assign": ["like", f"%{user}%"],
			"work_status": ["not in", ["Done", "Cancelled"]],
		},
	)
	return {
		"value": n,
		"fieldtype": "Int",
		"route": ["List", "Task", "List"],
		"route_options": {},
	}


@frappe.whitelist()
def cwd_followups_due_today_count(filters=None):
	td = today()
	n = frappe.db.count(
		"Follow-up",
		{
			"due_date": td,
			"status": ["not in", ["Done", "Cancelled"]],
		},
	)
	return {
		"value": n,
		"fieldtype": "Int",
		"route": ["List", "Follow-up", "List"],
		"route_options": {"due_date": td},
	}


@frappe.whitelist()
def cwd_payment_followups_due_count(filters=None):
	td = today()
	n = frappe.db.count(
		"Sales Invoice",
		{
			"docstatus": 1,
			"outstanding_amount": [">", 0],
			"payment_follow_up_status": "Pending",
			"invoice_follow_up_date": td,
		},
	)
	return {
		"value": n,
		"fieldtype": "Int",
		"route": ["List", "Sales Invoice", "List"],
		"route_options": {
			"invoice_follow_up_date": td,
			"payment_follow_up_status": "Pending",
		},
	}


@frappe.whitelist()
def cwd_deployments_today_count(filters=None):
	td = today()
	start = get_datetime(f"{td} 00:00:00")
	end = get_datetime(f"{td} 23:59:59")
	n = frappe.db.sql(
		"""
		SELECT COUNT(*) FROM `tabDeployment Plan`
		WHERE deployment_datetime >= %s AND deployment_datetime <= %s
		""",
		(start, end),
	)[0][0]
	return {
		"value": int(n),
		"fieldtype": "Int",
		"route": ["List", "Deployment Plan", "List"],
		"route_options": {},
	}
