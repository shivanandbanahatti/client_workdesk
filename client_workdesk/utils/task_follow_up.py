# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

"""Create/update Follow-up documents linked from Tasks (task field)."""

from __future__ import annotations

import frappe
from frappe import _

from client_workdesk.utils.workdesk_notify import parse_assign_json


def sync_linked_follow_up_from_task(doc) -> None:
	"""One Follow-up per Task when follow_up_required and follow_up_date are set."""
	if getattr(doc.flags, "cwd_skip_linked_follow_up", False):
		return
	if not doc.get("follow_up_required") or not doc.get("follow_up_date"):
		return

	subject = (doc.subject or _("Follow-up"))[:140]
	ftype = _task_type_to_follow_up_type(doc.get("task_type"))

	existing = frappe.get_all("Follow-up", filters={"task": doc.name}, pluck="name", limit_page_length=1)
	owner = _default_follow_up_owner(doc)

	if existing:
		fup = frappe.get_doc("Follow-up", existing[0])
		fup.subject = subject
		fup.customer = doc.customer
		fup.project = doc.project
		fup.task = doc.name
		fup.due_date = doc.follow_up_date
		fup.due_time = doc.due_time
		if ftype:
			fup.follow_up_type = ftype
		if owner and not fup.owner_user:
			fup.owner_user = owner
		fup.flags.ignore_permissions = True
		fup.save()
		return

	fup = frappe.new_doc("Follow-up")
	fup.subject = subject
	fup.customer = doc.customer
	fup.project = doc.project
	fup.task = doc.name
	fup.due_date = doc.follow_up_date
	fup.due_time = doc.due_time
	fup.status = "Pending"
	fup.follow_up_type = ftype or "Client Follow-up"
	fup.owner_user = owner
	fup.flags.ignore_permissions = True
	fup.insert()


def _default_follow_up_owner(doc) -> str | None:
	u = frappe.session.user
	if u and u not in ("Guest", "Administrator"):
		return u
	assignees = parse_assign_json(doc._assign)
	return assignees[0] if assignees else None


def _task_type_to_follow_up_type(task_type: str | None) -> str | None:
	if not task_type:
		return None
	mapping = {
		"Client Follow-up": "Client Follow-up",
		"Invoice Follow-up": "Invoice",
		"Payment Follow-up": "Payment",
		"Deployment": "Deployment",
		"UAT": "UAT",
		"Meeting": "Client Call",
	}
	return mapping.get(task_type)
