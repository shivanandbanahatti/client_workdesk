import frappe
from frappe.model.document import Document

from client_workdesk.utils.datetime_utils import add_hours
from client_workdesk.utils.event_sync import sync_deployment_plan_event


class DeploymentPlan(Document):
	def validate(self):
		if self.deployment_datetime:
			self.deployment_calendar_end = add_hours(self.deployment_datetime, 1.0)

	def after_insert(self):
		self._sync_event()
		self._block_related_task_if_needed()

	def on_update(self):
		self._sync_event()
		self._sync_linked_event_status()
		self._block_related_task_if_needed()

	def _sync_event(self):
		if not self.deployment_datetime:
			return
		try:
			sync_deployment_plan_event(self)
		except Exception:
			frappe.log_error(frappe.get_traceback(), "Deployment Plan Event Sync")

	def _block_related_task_if_needed(self):
		if self.status not in ("Failed", "Rolled Back") or not self.related_task:
			return
		reason = f"{self.title or self.name} — {self.status}"
		try:
			frappe.db.set_value(
				"Task",
				self.related_task,
				{"blocked": 1, "blocked_reason": reason[:280]},
				update_modified=True,
			)
		except Exception:
			frappe.log_error(frappe.get_traceback(), "Deployment Plan: block related Task")

	def _sync_linked_event_status(self):
		if not self.get("calendar_event") or not frappe.db.exists("Event", self.calendar_event):
			return
		if self.status in ("Completed", "Cancelled", "Rolled Back"):
			frappe.db.set_value("Event", self.calendar_event, "status", "Closed", update_modified=False)
		elif self.status == "Failed":
			frappe.db.set_value("Event", self.calendar_event, "status", "Cancelled", update_modified=False)
		else:
			frappe.db.set_value("Event", self.calendar_event, "status", "Open", update_modified=False)
