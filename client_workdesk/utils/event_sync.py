import frappe
from frappe import _

from client_workdesk.utils.datetime_utils import add_hours, combine_date_time


def create_or_update_event_for_doc(
	doc,
	*,
	subject: str,
	starts_on,
	ends_on,
	reference_doctype: str,
	description_html: str | None = None,
):
	"""Create or update a single Event linked to ``doc`` via ``doc.calendar_event``."""
	if not starts_on:
		frappe.throw(_("Start datetime is required to create a calendar event."))

	desc = description_html or ""

	if doc.get("calendar_event") and frappe.db.exists("Event", doc.calendar_event):
		ev = frappe.get_doc("Event", doc.calendar_event)
		ev.subject = subject[:140]
		ev.starts_on = starts_on
		ev.ends_on = ends_on or add_hours(starts_on, 1.0)
		ev.description = desc
		ev.reference_doctype = reference_doctype
		ev.reference_docname = doc.name
		ev.flags.ignore_permissions = True
		ev.save()
		return ev.name

	ev = frappe.new_doc("Event")
	ev.subject = subject[:140]
	ev.event_type = "Public"
	ev.event_category = "Other"
	ev.status = "Open"
	ev.starts_on = starts_on
	ev.ends_on = ends_on or add_hours(starts_on, 1.0)
	ev.description = desc
	ev.reference_doctype = reference_doctype
	ev.reference_docname = doc.name
	ev.flags.ignore_permissions = True
	ev.insert()

	return ev.name


def sync_follow_up_calendar_fields(doc):
	"""Keep hidden calendar datetime in sync with due_date + due_time."""
	doc.calendar_starts_on = combine_date_time(doc.due_date, doc.due_time)
	if doc.calendar_starts_on:
		doc.calendar_ends_on = add_hours(doc.calendar_starts_on, 1.0)


def sync_follow_up_event(doc):
	if not doc.get("create_calendar_event"):
		return

	sync_follow_up_calendar_fields(doc)
	if not doc.calendar_starts_on:
		return

	subject = doc.subject or _("Follow-up")
	desc = doc.notes or ""
	starts = doc.calendar_starts_on
	ends = doc.calendar_ends_on or add_hours(starts, 1.0)

	name = create_or_update_event_for_doc(
		doc,
		subject=subject,
		starts_on=starts,
		ends_on=ends,
		reference_doctype=doc.doctype,
		description_html=desc,
	)
	if doc.get("calendar_event") != name:
		frappe.db.set_value(doc.doctype, doc.name, "calendar_event", name, update_modified=False)


def sync_deployment_plan_event(doc):
	"""Show Deployment Plan on desk calendar whenever deployment_datetime is set."""
	if not doc.deployment_datetime:
		return

	starts = doc.deployment_datetime
	ends = doc.deployment_calendar_end or add_hours(starts, 1.0)
	subject = doc.title or _("Deployment")
	parts = []
	if doc.pre_deployment_checklist:
		parts.append(doc.pre_deployment_checklist)
	if doc.deployment_steps:
		parts.append(doc.deployment_steps)
	desc = "<br><br>".join(parts)

	name = create_or_update_event_for_doc(
		doc,
		subject=subject[:140],
		starts_on=starts,
		ends_on=ends,
		reference_doctype=doc.doctype,
		description_html=desc,
	)
	if doc.get("calendar_event") != name:
		frappe.db.set_value(doc.doctype, doc.name, "calendar_event", name, update_modified=False)
