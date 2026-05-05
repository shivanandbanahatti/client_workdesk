# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

"""Desk + email notifications (Notification Log) by User name."""

from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _
from frappe.desk.doctype.notification_settings.notification_settings import is_notifications_enabled
from frappe.utils.data import escape_html


def parse_assign_json(assign_json: str | None) -> list[str]:
	if not assign_json:
		return []
	try:
		data = json.loads(assign_json)
	except (TypeError, ValueError):
		return []
	if not isinstance(data, list):
		return []
	return [str(u) for u in data if u]


def cwd_notify_users(user_names: list[str] | None, doc: dict[str, Any]) -> None:
	"""Insert Notification Log per user (by User.name). Respects notification settings."""
	if frappe.flags.in_install:
		return
	doc = dict(doc)
	from_user = doc.get("from_user") or "Administrator"
	doc["from_user"] = from_user
	for un in {u for u in (user_names or []) if u and u != "Guest"}:
		if not frappe.db.get_value("User", un, "enabled"):
			continue
		if not is_notifications_enabled(un):
			continue
		notification = frappe.new_doc("Notification Log")
		notification.update(doc)
		notification.for_user = un
		if notification.for_user != notification.from_user or doc.get("type") == "Alert":
			notification.insert(ignore_permissions=True)


def html_li_link(doctype: str, name: str, label: str | None) -> str:
	url = frappe.utils.get_url_to_form(doctype, name)
	return f'<li><a href="{url}">{escape_html(label or "")}</a></li>'


def section_html(title: str, items: list[str]) -> str:
	if not items:
		return ""
	body = "".join(items)
	return f"<p><strong>{escape_html(title)}</strong></p><ul>{body}</ul>"


def recipients_for_deployment_plan(row: dict) -> list[str]:
	out: list[str] = []
	if row.get("deployed_by"):
		out.append(row["deployed_by"])
	if row.get("project"):
		users = frappe.db.sql(
			"""
			SELECT DISTINCT user FROM `tabProject User`
			WHERE parenttype = 'Project' AND parent = %(p)s AND user IS NOT NULL
			""",
			{"p": row["project"]},
			pluck=True,
		)
		out.extend(users or [])
		owner = frappe.db.get_value("Project", row["project"], "owner")
		if owner:
			out.append(owner)
	return list({u for u in out if u})


def recipients_for_invoice_followup(si: dict) -> list[str]:
	out: list[str] = []
	if si.get("customer"):
		am = frappe.db.get_value("Customer", si["customer"], "account_manager")
		if am:
			out.append(am)
	if si.get("project"):
		owner = frappe.db.get_value("Project", si["project"], "owner")
		if owner:
			out.append(owner)
		users = frappe.db.sql(
			"""
			SELECT DISTINCT user FROM `tabProject User`
			WHERE parenttype = 'Project' AND parent = %(p)s AND user IS NOT NULL
			LIMIT 5
			""",
			{"p": si["project"]},
			pluck=True,
		)
		out.extend(users or [])
	return list({u for u in out if u})
