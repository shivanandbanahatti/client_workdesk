# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

"""Scheduler entry points for Client Workdesk (see hooks.scheduler_events)."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import add_days, formatdate, getdate, today
from frappe.utils.data import escape_html

from client_workdesk.utils.workdesk_notify import (
	cwd_notify_users,
	html_li_link,
	parse_assign_json,
	recipients_for_deployment_plan,
	recipients_for_invoice_followup,
	section_html,
)


def _has_doctype(doctype: str) -> bool:
	return bool(frappe.db.exists("DocType", doctype))


def _task_open_sql_filters(alias: str | None = None) -> str:
	col = f"{alias}." if alias else ""
	return f"""
		{col}status NOT IN ('Cancelled', 'Completed')
		AND IFNULL({col}work_status, '') NOT IN ('Done', 'Cancelled')
	"""


def send_daily_work_summary():
	"""Morning digest: tasks due / overdue, follow-ups, deployments, invoice follow-ups (per user)."""
	td = today()

	# --- Load pools
	tasks_due = frappe.db.sql(
		f"""
		SELECT name, subject, exp_end_date, follow_up_date, _assign
		FROM `tabTask`
		WHERE {_task_open_sql_filters()}
			AND (exp_end_date = %(td)s OR follow_up_date = %(td)s)
		""",
		{"td": td},
		as_dict=True,
	)
	tasks_overdue = frappe.db.sql(
		f"""
		SELECT name, subject, exp_end_date, _assign
		FROM `tabTask`
		WHERE {_task_open_sql_filters()}
			AND exp_end_date IS NOT NULL
			AND exp_end_date < %(td)s
		""",
		{"td": td},
		as_dict=True,
	)
	followups = []
	if _has_doctype("Follow-up"):
		followups = frappe.get_all(
			"Follow-up",
			filters={"due_date": td, "status": ["not in", ["Done", "Cancelled"]]},
			fields=["name", "subject", "owner_user"],
		)

	deployments = []
	if _has_doctype("Deployment Plan"):
		deployments = frappe.db.sql(
			"""
			SELECT name, title, deployment_datetime, status, deployed_by, project, customer
			FROM `tabDeployment Plan`
			WHERE status IN ('Planned', 'In Progress')
				AND DATE(deployment_datetime) = %(td)s
			""",
			{"td": td},
			as_dict=True,
		)
	invoices = frappe.get_all(
		"Sales Invoice",
		filters={
			"docstatus": 1,
			"outstanding_amount": [">", 0],
			"invoice_follow_up_date": td,
		},
		fields=["name", "customer", "project", "outstanding_amount"],
	)

	# --- Build per-user buckets
	user_rows: dict[str, dict] = {}

	def bucket(user: str, key: str, html_line: str):
		if not user:
			return
		user_rows.setdefault(user, {k: [] for k in ("due", "overdue", "fup", "depl", "inv")})
		user_rows[user][key].append(html_line)

	for t in tasks_due:
		label = t.subject or t.name
		line = html_li_link("Task", t.name, label)
		for u in parse_assign_json(t._assign):
			bucket(u, "due", line)

	for t in tasks_overdue:
		label = f"{t.subject or t.name} ({formatdate(t.exp_end_date)})"
		line = html_li_link("Task", t.name, label)
		for u in parse_assign_json(t._assign):
			bucket(u, "overdue", line)

	for f in followups:
		if not f.owner_user:
			continue
		label = f.subject or f.name
		bucket(f.owner_user, "fup", html_li_link("Follow-up", f.name, label))

	for d in deployments:
		for u in recipients_for_deployment_plan(d):
			label = d.title or d.name
			bucket(u, "depl", html_li_link("Deployment Plan", d.name, label))

	for inv in invoices:
		si = inv
		for u in recipients_for_invoice_followup(si):
			label = f"{inv.name} ({inv.outstanding_amount})"
			bucket(u, "inv", html_li_link("Sales Invoice", inv.name, label))

	# --- Send
	desk_url = frappe.utils.get_url() + "/app"
	subject_date = formatdate(getdate(td))
	for user, parts in user_rows.items():
		if not any(parts[k] for k in parts):
			continue
		html = "".join(
			[
				section_html(_("Tasks due today"), parts["due"]),
				section_html(_("Overdue tasks"), parts["overdue"]),
				section_html(_("Follow-ups due today"), parts["fup"]),
				section_html(_("Deployments today"), parts["depl"]),
				section_html(_("Invoice follow-ups today"), parts["inv"]),
			]
		)
		if not html.strip():
			continue
		cwd_notify_users(
			[user],
			{
				"type": "Alert",
				"subject": _("Client Workdesk — Your work summary ({0})").format(subject_date),
				"email_content": html,
				"link": desk_url,
				"from_user": "Administrator",
			},
		)


def notify_overdue_tasks_daily():
	"""Notify assignees for tasks that became overdue since yesterday (calendar)."""
	td = today()
	yesterday = add_days(td, -1)
	tasks = frappe.db.sql(
		f"""
		SELECT name, subject, exp_end_date, _assign
		FROM `tabTask`
		WHERE {_task_open_sql_filters()}
			AND exp_end_date = %(yd)s
		""",
		{"yd": yesterday},
		as_dict=True,
	)
	for t in tasks:
		assignees = parse_assign_json(t._assign)
		if not assignees:
			continue
		subj = _("Task overdue: {0}").format(escape_html(t.subject or t.name))
		cwd_notify_users(
			assignees,
			{
				"type": "Alert",
				"subject": subj,
				"document_type": "Task",
				"document_name": t.name,
				"email_content": f"<p>{_('Due date was {0}').format(formatdate(t.exp_end_date))}</p>",
				"from_user": "Administrator",
			},
		)


def notify_followups_due_today():
	"""Remind Follow-up owner_user when due_date is today."""
	if not _has_doctype("Follow-up"):
		return
	td = today()
	rows = frappe.get_all(
		"Follow-up",
		filters={"due_date": td, "status": ["not in", ["Done", "Cancelled"]]},
		fields=["name", "subject", "owner_user"],
	)
	for r in rows:
		if not r.owner_user:
			continue
		cwd_notify_users(
			[r.owner_user],
			{
				"type": "Alert",
				"subject": _("Follow-up due today: {0}").format(escape_html(r.subject or r.name)),
				"document_type": "Follow-up",
				"document_name": r.name,
				"from_user": "Administrator",
			},
		)


def notify_invoice_followups_due_today():
	td = today()
	rows = frappe.get_all(
		"Sales Invoice",
		filters={
			"docstatus": 1,
			"outstanding_amount": [">", 0],
			"invoice_follow_up_date": td,
		},
		fields=["name", "customer", "project", "outstanding_amount"],
	)
	for r in rows:
		recipients = recipients_for_invoice_followup(r)
		if not recipients:
			continue
		cwd_notify_users(
			recipients,
			{
				"type": "Alert",
				"subject": _("Invoice payment follow-up: {0}").format(r.name),
				"document_type": "Sales Invoice",
				"document_name": r.name,
				"email_content": f"<p>{_('Outstanding')}: {r.outstanding_amount}</p>",
				"from_user": "Administrator",
			},
		)


def update_auto_project_health():
	"""When Project.auto_project_health is set, derive Green / Yellow / Red."""
	if not _has_doctype("Project") or not _has_doctype("Task"):
		return
	projects = frappe.get_all(
		"Project",
		filters={"status": "Open", "auto_project_health": 1},
		pluck="name",
	)
	for name in projects:
		threshold = frappe.db.get_value("Project", name, "health_payment_overdue_days") or 7
		try:
			threshold = int(threshold)
		except (TypeError, ValueError):
			threshold = 7

		overdue_count = frappe.db.sql(
			f"""
			SELECT COUNT(*) FROM `tabTask` t
			WHERE t.project = %(p)s
				AND {_task_open_sql_filters('t')}
				AND t.exp_end_date IS NOT NULL
				AND t.exp_end_date < %(td)s
			""",
			{"p": name, "td": today()},
		)[0][0]

		critical_overdue = frappe.db.sql(
			f"""
			SELECT COUNT(*) FROM `tabTask` t
			WHERE t.project = %(p)s
				AND {_task_open_sql_filters('t')}
				AND IFNULL(t.task_priority, '') = 'Critical'
				AND t.exp_end_date IS NOT NULL
				AND t.exp_end_date < %(td)s
			""",
			{"p": name, "td": today()},
		)[0][0]

		waiting_client = frappe.db.sql(
			f"""
			SELECT COUNT(*) FROM `tabTask` t
			WHERE t.project = %(p)s
				AND {_task_open_sql_filters('t')}
				AND t.work_status = 'Waiting for Client'
			""",
			{"p": name},
		)[0][0]

		any_overdue = overdue_count > 0

		uat_pending = 0
		if _has_doctype("Follow-up"):
			uat_pending = frappe.db.sql(
				"""
				SELECT COUNT(*) FROM `tabFollow-up` f
				WHERE f.project = %(p)s
					AND f.follow_up_type = 'UAT'
					AND f.status = 'Pending'
				""",
				{"p": name},
			)[0][0]

		payment_cutoff = add_days(today(), -threshold)
		payment_overdue = frappe.db.sql(
			"""
			SELECT COUNT(*) FROM `tabSales Invoice` si
			WHERE si.docstatus = 1
				AND si.outstanding_amount > 0
				AND si.project = %(p)s
				AND si.due_date IS NOT NULL
				AND si.due_date < %(cutoff)s
			""",
			{"p": name, "cutoff": payment_cutoff},
		)[0][0]

		reasons: list[str] = []
		health = "Green"

		if overdue_count > 3 or critical_overdue > 0 or payment_overdue > 0:
			health = "Red"
			if overdue_count > 3:
				reasons.append(_("More than 3 overdue tasks ({0})").format(overdue_count))
			if critical_overdue:
				reasons.append(_("Critical task(s) overdue"))
			if payment_overdue:
				reasons.append(
					_("Payment overdue (>{0} days past invoice due)").format(threshold)
				)
		elif any_overdue or waiting_client > 0 or uat_pending > 0:
			health = "Yellow"
			if any_overdue:
				reasons.append(_("There are overdue tasks"))
			if waiting_client:
				reasons.append(_("Client waiting for response"))
			if uat_pending:
				reasons.append(_("UAT follow-up pending"))

		reason = "; ".join(reasons) if reasons else _("No blocking signals")

		frappe.db.set_value(
			"Project",
			name,
			{"project_health": health, "project_health_reason": reason},
			update_modified=False,
		)
