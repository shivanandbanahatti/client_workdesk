# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import json

import frappe


def format_assignees(assign_json: str | None) -> str:
	if not assign_json:
		return ""
	try:
		users = json.loads(assign_json)
	except (TypeError, ValueError):
		return ""
	names = []
	for u in users:
		names.append(frappe.db.get_value("User", u, "full_name") or u)
	return ", ".join(names)


def desk_link(doctype: str, name: str) -> str:
	if not name:
		return ""
	return frappe.utils.get_url_to_form(doctype, name)
