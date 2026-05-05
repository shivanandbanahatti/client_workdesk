import datetime

from frappe.utils import get_time, getdate


def combine_date_time(d, t) -> datetime.datetime | None:
	"""Combine ERPNext Date and Time into a datetime for Events and calendar."""
	if not d:
		return None
	date_val = getdate(d)
	if t:
		tm = get_time(t)
		return datetime.datetime.combine(date_val, tm)
	return datetime.datetime.combine(date_val, datetime.time(9, 0))


def add_hours(dt: datetime.datetime, hours: float) -> datetime.datetime:
	return dt + datetime.timedelta(hours=hours)
