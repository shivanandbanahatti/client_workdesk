import re

from frappe.model.document import Document
from frappe.model.naming import append_number_if_name_exists


class ClientApplication(Document):
	def autoname(self):
		customer = (self.customer or "").strip()
		app_name = (self.application_name or "").strip()
		if not customer or not app_name:
			return

		def slug(text: str) -> str:
			text = re.sub(r"[^\w\-.]+", "-", text.strip())
			text = re.sub(r"-{2,}", "-", text).strip("-")
			return text or "application"

		base = f"{customer}-{slug(app_name)}"
		if len(base) > 140:
			base = base[:140]
		self.name = append_number_if_name_exists("Client Application", base)
