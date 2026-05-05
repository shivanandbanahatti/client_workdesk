# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

"""Default Task Kanban board on `work_status` (Jira-style columns)."""

import json

import frappe
from frappe.desk.doctype.kanban_board.kanban_board import get_order_for_column

TASK_WORK_STATUS_BOARD = "Task Work Status"

# Column order matches Task `work_status` select options; indicators are column header colours.
TASK_KANBAN_COLUMNS: list[tuple[str, str]] = [
	("Backlog", "Gray"),
	("To Do", "Light Blue"),
	("In Progress", "Green"),
	("Waiting for Client", "Orange"),
	("Waiting for Internal Team", "Yellow"),
	("Waiting for Third Party", "Pink"),
	("Testing", "Purple"),
	("UAT", "Cyan"),
	("Ready for Deployment", "Red"),
	("Done", "Gray"),
	("Cancelled", "Gray"),
]

# Shown under the title on each card (fieldnames on Task).
TASK_KANBAN_CARD_FIELDS = [
	"project",
	"task_priority",
	"exp_end_date",
	"status",
	"blocked",
]


def ensure_default_task_kanban_board():
	"""Create or refresh the default Task Kanban board (idempotent)."""
	if frappe.db.exists("Kanban Board", TASK_WORK_STATUS_BOARD):
		doc = frappe.get_doc("Kanban Board", TASK_WORK_STATUS_BOARD)
		changed = False
		if doc.field_name != "work_status":
			doc.field_name = "work_status"
			changed = True
		target_fields = json.dumps(TASK_KANBAN_CARD_FIELDS)
		if (doc.fields or "[]") != target_fields:
			doc.fields = target_fields
			changed = True
		if doc.show_labels != 1:
			doc.show_labels = 1
			changed = True
		existing = {c.column_name: c for c in doc.columns}
		for col_name, indicator in TASK_KANBAN_COLUMNS:
			if col_name not in existing:
				row = doc.append(
					"columns",
					{"column_name": col_name, "status": "Active", "indicator": indicator},
				)
				row.order = get_order_for_column(doc, col_name)
				changed = True
			elif existing[col_name].indicator != indicator:
				existing[col_name].indicator = indicator
				changed = True
		if changed:
			doc.save(ignore_permissions=True)
		return

	doc = frappe.new_doc("Kanban Board")
	doc.kanban_board_name = TASK_WORK_STATUS_BOARD
	doc.reference_doctype = "Task"
	doc.field_name = "work_status"
	doc.private = 0
	doc.show_labels = 1
	doc.filters = "[]"
	doc.fields = json.dumps(TASK_KANBAN_CARD_FIELDS)
	for col_name, indicator in TASK_KANBAN_COLUMNS:
		doc.append("columns", {"column_name": col_name, "status": "Active", "indicator": indicator})
	doc.insert(ignore_permissions=True)
