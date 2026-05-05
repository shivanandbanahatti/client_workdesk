# Copyright (c) 2026, Client Workdesk contributors
# License: MIT

import json
import re

import frappe
from frappe.desk.calendar import get_event_conditions
from frappe.desk.reportview import get_match_cond
from frappe.utils import get_datetime, getdate

_SQL_IDENT = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")


def _sql_alias(name: str, default: str) -> str:
	if name and _SQL_IDENT.match(name):
		return name
	return default


def _parse_filters(filters):
	if not filters:
		return []
	return json.loads(filters) if isinstance(filters, str) else filters


@frappe.whitelist()
def get_task_calendar_events(doctype, start, end, field_map, filters=None, fields=None):
	"""Task calendar: COALESCE(scheduled_start, exp_start_date, exp_end_date) for start; end prefers scheduled_end."""
	del doctype, fields
	filters = _parse_filters(filters)
	field_map = frappe._dict(json.loads(field_map))
	conditions = get_event_conditions("Task", filters)
	if not conditions:
		conditions = get_match_cond("Task")

	start_f = _sql_alias(field_map.get("start"), "calendar_start")
	end_f = _sql_alias(field_map.get("end"), "calendar_end")

	return frappe.db.sql(
		f"""
		SELECT * FROM (
			SELECT
				`tabTask`.name,
				`tabTask`.subject,
				IFNULL(`tabTask`.task_type, '') AS task_type,
				IFNULL(`tabTask`.work_status, '') AS work_status,
				COALESCE(
					`tabTask`.scheduled_start,
					IFNULL(TIMESTAMP(`tabTask`.exp_start_date), NULL),
					IFNULL(TIMESTAMP(`tabTask`.exp_end_date), NULL)
				) AS `{start_f}`,
				COALESCE(
					`tabTask`.scheduled_end,
					IF(`tabTask`.scheduled_start IS NOT NULL, DATE_ADD(`tabTask`.scheduled_start, INTERVAL 1 HOUR), NULL),
					IF(
						COALESCE(`tabTask`.exp_end_date, `tabTask`.exp_start_date) IS NOT NULL,
						TIMESTAMP(DATE_ADD(COALESCE(`tabTask`.exp_end_date, `tabTask`.exp_start_date), INTERVAL 1 DAY))
							- INTERVAL 1 SECOND,
						NULL
					),
					DATE_ADD(
						COALESCE(
							`tabTask`.scheduled_start,
							IFNULL(TIMESTAMP(`tabTask`.exp_start_date), NULL),
							IFNULL(TIMESTAMP(`tabTask`.exp_end_date), NULL)
						),
						INTERVAL 1 HOUR
					)
				) AS `{end_f}`
			FROM `tabTask`
			WHERE
				COALESCE(
					`tabTask`.scheduled_start,
					IFNULL(TIMESTAMP(`tabTask`.exp_start_date), NULL),
					IFNULL(TIMESTAMP(`tabTask`.exp_end_date), NULL)
				) IS NOT NULL
				{conditions}
		) cal
		WHERE cal.`{start_f}` <= %(end)s
			AND cal.`{end_f}` >= %(start)s
		""",
		{"start": start, "end": end},
		as_dict=True,
	)


@frappe.whitelist()
def update_task_calendar_event(args, field_map):
	args = frappe._dict(json.loads(args))
	field_map = frappe._dict(json.loads(field_map))
	doc = frappe.get_doc("Task", args.name)
	start = get_datetime(args[field_map.start])
	end = get_datetime(args[field_map.end])
	if not start or not end:
		frappe.throw(frappe._("Invalid start or end"))
	if end < start:
		end = start

	doc.scheduled_start = start
	doc.scheduled_end = end
	doc.exp_start_date = getdate(start)
	doc.exp_end_date = getdate(end)
	doc.save()


@frappe.whitelist()
def get_sales_invoice_follow_up_events(doctype, start, end, field_map, filters=None, fields=None):
	del doctype, fields
	filters = _parse_filters(filters)
	field_map = frappe._dict(json.loads(field_map))

	conditions = get_event_conditions("Sales Invoice", filters)
	if not conditions:
		conditions = get_match_cond("Sales Invoice")

	start_f = _sql_alias(field_map.get("start"), "invoice_follow_up_date")
	end_f = _sql_alias(field_map.get("end"), "invoice_follow_up_date")
	title_f = _sql_alias(field_map.get("title"), "calendar_title")

	return frappe.db.sql(
		f"""
		SELECT
			`tabSales Invoice`.name,
			CONCAT_WS(' — ', NULLIF(`tabSales Invoice`.customer_name, ''), `tabSales Invoice`.name) AS `{title_f}`,
			`tabSales Invoice`.invoice_follow_up_date AS `{start_f}`,
			`tabSales Invoice`.invoice_follow_up_date AS `{end_f}`,
			IFNULL(`tabSales Invoice`.payment_follow_up_status, '') AS payment_follow_up_status,
			IFNULL(`tabSales Invoice`.status, '') AS si_status
		FROM `tabSales Invoice`
		WHERE
			`tabSales Invoice`.docstatus = 1
			AND IFNULL(`tabSales Invoice`.outstanding_amount, 0) > 0
			AND IFNULL(`tabSales Invoice`.payment_follow_up_status, '') = 'Pending'
			AND `tabSales Invoice`.invoice_follow_up_date IS NOT NULL
			AND `tabSales Invoice`.invoice_follow_up_date <= %(end)s
			AND `tabSales Invoice`.invoice_follow_up_date >= %(start)s
			{conditions}
		""",
		{"start": getdate(start), "end": getdate(end)},
		as_dict=True,
		update={"doctype": "Sales Invoice"},
	)
