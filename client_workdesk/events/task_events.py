# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import today
from frappe.utils.data import escape_html

from client_workdesk.utils.task_follow_up import sync_linked_follow_up_from_task
from client_workdesk.utils.workdesk_notify import cwd_notify_users, parse_assign_json


def task_validate(doc, method=None):
	meta = frappe.get_meta("Task")

	if doc.project:
		row = frappe.db.get_value(
			"Project",
			doc.project,
			["customer", "client_application"],
			as_dict=True,
		)
		if row:
			if row.get("customer"):
				doc.customer = row.customer
			if row.get("client_application"):
				doc.client_application = row.client_application

	if meta.get_field("completed_on") and (doc.work_status or "") == "Done":
		if not doc.completed_on:
			doc.completed_on = frappe.utils.today()

	if doc.get("blocked") and not (doc.blocked_reason or "").strip():
		frappe.throw(_("Blocked Reason is mandatory when Blocked is checked."))

	if doc.get("follow_up_required") and not doc.get("follow_up_date"):
		frappe.throw(_("Follow-up Date is mandatory when Follow-up Required is checked."))

	if doc.get("billing_status") == "Ready to Invoice":
		if not doc.project or not doc.customer:
			frappe.throw(
				_("Customer and Project are required when Billing Status is Ready to Invoice.")
			)


def task_after_insert(doc, method=None):
	sync_linked_follow_up_from_task(doc)


def task_on_update(doc, method=None):
	sync_linked_follow_up_from_task(doc)
	_notify_task_overdue_if_new(doc)


def _notify_task_overdue_if_new(doc):
	"""Notify assignees the moment a task crosses into overdue (save-time transition)."""
	if frappe.flags.in_install or getattr(doc.flags, "cwd_skip_overdue_notify", False):
		return
	prev = doc.get_doc_before_save()
	if not prev:
		return
	if not _is_open_task(doc) or not _is_overdue(doc):
		return
	if _was_overdue(prev):
		return
	assignees = parse_assign_json(doc._assign)
	if not assignees:
		return
	subj = _("Task is now overdue: {0}").format(escape_html(doc.subject or doc.name))
	cwd_notify_users(
		assignees,
		{
			"type": "Alert",
			"subject": subj,
			"document_type": "Task",
			"document_name": doc.name,
			"email_content": f"<p>{_('Due date: {0}').format(doc.exp_end_date)}</p>",
			"from_user": frappe.session.user if frappe.session.user != "Guest" else "Administrator",
		},
	)


def _is_open_task(doc) -> bool:
	if doc.status in ("Cancelled", "Completed"):
		return False
	if (doc.work_status or "") in ("Done", "Cancelled"):
		return False
	return True


def _is_overdue(doc) -> bool:
	if not doc.exp_end_date:
		return False
	return str(doc.exp_end_date) < today()


def _was_overdue(prev) -> bool:
	if not prev:
		return False
	return _is_overdue(prev)
