import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from client_workdesk.utils.event_sync import sync_follow_up_calendar_fields, sync_follow_up_event


class FollowUp(Document):
	def validate(self):
		sync_follow_up_calendar_fields(self)
		if self.status == "Done" and not self.last_followed_up_on:
			self.last_followed_up_on = now_datetime()

	def after_insert(self):
		self._sync_event()

	def on_update(self):
		self._sync_event()
		self._sync_linked_event_status()
		self._spawn_next_follow_up_if_needed()

	def _spawn_next_follow_up_if_needed(self):
		if not self.next_follow_up_date or self.flags.get("cwd_skip_chain_spawn"):
			return
		try:
			child = frappe.new_doc("Follow-up")
			child.subject = (f"Follow-up: {self.subject or self.name}")[:200]
			child.customer = self.customer
			child.project = self.project
			child.task = self.task
			child.due_date = self.next_follow_up_date
			child.status = "Pending"
			child.follow_up_type = self.follow_up_type or "Client Follow-up"
			child.owner_user = self.owner_user
			child.flags.ignore_permissions = True
			child.insert()
			frappe.db.set_value("Follow-up", self.name, "next_follow_up_date", None, update_modified=False)
		except Exception:
			frappe.log_error(frappe.get_traceback(), "Follow-up: spawn next from next_follow_up_date")

	def _sync_event(self):
		if not self.get("create_calendar_event"):
			return
		try:
			sync_follow_up_event(self)
		except Exception:
			frappe.log_error(frappe.get_traceback(), "Follow-up Event Sync")

	def _sync_linked_event_status(self):
		if not self.get("calendar_event") or not frappe.db.exists("Event", self.calendar_event):
			return
		if self.status == "Done":
			frappe.db.set_value("Event", self.calendar_event, "status", "Completed", update_modified=False)
		elif self.status == "Cancelled":
			frappe.db.set_value("Event", self.calendar_event, "status", "Cancelled", update_modified=False)
		else:
			frappe.db.set_value("Event", self.calendar_event, "status", "Open", update_modified=False)
