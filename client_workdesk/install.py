"""Install / migrate hooks for Client Workdesk."""

import os

import frappe

from client_workdesk.setup.default_kanban import ensure_default_task_kanban_board


def after_migrate():
	"""Clear cached Jinja loaders so `www/index.html` from other apps (e.g. consulting site) resolves.

	After installing a new app, Frappe's site-cached Jinja `ChoiceLoader` can still miss templates
	that exist on disk, which surfaces as ``TemplateNotFound: www/index.html`` on the home route.
	"""
	try:
		from frappe.utils.jinja import _get_jloader

		_get_jloader.clear_cache()
	except Exception:
		pass

	# Remove empty boilerplate `www/` so PackageLoader does not treat this app as owning a home page.
	www = frappe.get_app_path("client_workdesk", "www")
	try:
		if os.path.isdir(www) and not any(name for name in os.listdir(www) if name not in (".", "..")):
			os.rmdir(www)
	except OSError:
		pass

	try:
		ensure_default_task_kanban_board()
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Client Workdesk: default Task Kanban board")

	frappe.clear_cache()
