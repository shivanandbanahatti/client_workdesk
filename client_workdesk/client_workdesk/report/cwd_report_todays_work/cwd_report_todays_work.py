# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import getdate, today
from frappe.utils.data import format_time, get_time_str

from client_workdesk.report.cwd_report_helpers import desk_link, format_assignees


def execute(filters=None):
	td = today()
	columns = [
		{"label": _("Type"), "fieldname": "row_type", "fieldtype": "Data", "width": 110},
		{"label": _("Subject"), "fieldname": "subject", "fieldtype": "Data", "width": 200},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 130},
		{"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 130},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": _("Due Time"), "fieldname": "due_time", "fieldtype": "Data", "width": 80},
		{"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 90},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Data", "width": 160},
		{"label": _("Link"), "fieldname": "doc_link", "fieldtype": "Data", "width": 200},
	]
	rows = []

	tasks = frappe.db.sql(
		"""
		SELECT name, subject, customer, project, exp_end_date, follow_up_date, due_time,
			task_priority, status, work_status, _assign
		FROM `tabTask`
		WHERE status NOT IN ('Cancelled', 'Completed')
			AND IFNULL(work_status, '') NOT IN ('Done', 'Cancelled')
			AND (exp_end_date = %(td)s OR follow_up_date = %(td)s)
		ORDER BY exp_end_date, name
		""",
		{"td": td},
		as_dict=True,
	)
	for t in tasks:
		due_d = t.exp_end_date or t.follow_up_date
		due_t = format_time(t.due_time) if t.due_time else ""
		st = " / ".join([x for x in [t.status, t.work_status] if x])
		rows.append(
			{
				"row_type": "Task",
				"subject": t.subject,
				"customer": t.customer,
				"project": t.project,
				"due_date": due_d,
				"due_time": due_t,
				"priority": t.task_priority or "",
				"status": st,
				"assigned_to": format_assignees(t._assign),
				"doc_link": desk_link("Task", t.name),
			}
		)

	fups = frappe.get_all(
		"Follow-up",
		filters={"due_date": td, "status": ["not in", ["Done", "Cancelled"]]},
		fields=["name", "subject", "customer", "project", "due_date", "due_time", "priority", "status", "owner_user"],
		order_by="due_time asc, name asc",
	)
	for f in fups:
		dt_str = format_time(f.due_time) if f.due_time else ""
		rows.append(
			{
				"row_type": "Follow-up",
				"subject": f.subject,
				"customer": f.customer,
				"project": f.project,
				"due_date": f.due_date,
				"due_time": dt_str,
				"priority": f.priority or "",
				"status": f.status,
				"assigned_to": frappe.db.get_value("User", f.owner_user, "full_name") if f.owner_user else "",
				"doc_link": desk_link("Follow-up", f.name),
			}
		)

	events = frappe.db.sql(
		"""
		SELECT name, subject, starts_on, event_type, status
		FROM `tabEvent`
		WHERE status = 'Open' AND DATE(starts_on) = %(td)s
		ORDER BY starts_on
		""",
		{"td": td},
		as_dict=True,
	)
	for e in events:
		rows.append(
			{
				"row_type": "Meeting",
				"subject": e.subject,
				"customer": None,
				"project": None,
				"due_date": getdate(e.starts_on) if e.starts_on else None,
				"due_time": get_time_str(e.starts_on) if e.starts_on else "",
				"priority": "",
				"status": e.event_type or _("Open"),
				"assigned_to": "",
				"doc_link": desk_link("Event", e.name),
			}
		)

	deps = frappe.db.sql(
		"""
		SELECT name, title, customer, project, deployment_datetime, deployment_environment, status
		FROM `tabDeployment Plan`
		WHERE DATE(deployment_datetime) = %(td)s
			AND status IN ('Planned', 'In Progress')
		ORDER BY deployment_datetime
		""",
		{"td": td},
		as_dict=True,
	)
	for d in deps:
		rows.append(
			{
				"row_type": "Deployment",
				"subject": d.title,
				"customer": d.customer,
				"project": d.project,
				"due_date": getdate(d.deployment_datetime),
				"due_time": get_time_str(d.deployment_datetime) if d.deployment_datetime else "",
				"priority": d.deployment_environment or "",
				"status": d.status,
				"assigned_to": "",
				"doc_link": desk_link("Deployment Plan", d.name),
			}
		)

	sis = frappe.get_all(
		"Sales Invoice",
		filters={
			"docstatus": 1,
			"outstanding_amount": [">", 0],
			"invoice_follow_up_date": td,
		},
		fields=[
			"name",
			"customer",
			"project",
			"invoice_follow_up_date",
			"outstanding_amount",
			"payment_follow_up_status",
		],
		order_by="name",
	)
	for s in sis:
		outst = frappe.format_value(s.outstanding_amount, {"fieldtype": "Currency"})
		rows.append(
			{
				"row_type": "Invoice Follow-up",
				"subject": f"{s.name} — {outst}",
				"customer": s.customer,
				"project": s.project,
				"due_date": s.invoice_follow_up_date,
				"due_time": "",
				"priority": "",
				"status": s.payment_follow_up_status or "",
				"assigned_to": "",
				"doc_link": desk_link("Sales Invoice", s.name),
			}
		)

	rows.sort(key=lambda r: (r.get("due_date") or td, r.get("due_time") or "", r.get("row_type") or ""))
	return columns, rows
