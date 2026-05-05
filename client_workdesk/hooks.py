app_name = "client_workdesk"
app_title = "Client Workdesk"
app_publisher = "Shivanand Banahatti"
app_description = "Multi-client work desk for projects, tasks, and billing inside ERPNext"
app_email = "shivanandbanahatti@gmail.com"
app_license = "mit"

# Custom Field records live in `client_workdesk/fixtures/custom_field.json` and are
# imported on `bench migrate` / app install. Use `bench export-fixtures` to refresh.
fixtures = [
	{"dt": "Custom Field", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Property Setter", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Workspace", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Report", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Number Card", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Dashboard Chart", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Kanban Board", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Client Script", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Notification", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Role", "filters": [["name", "in", ["Client Work Manager", "Client Work User", "Billing User", "Implementation Reviewer"]]]},
	{"dt": "Workflow", "filters": [["module", "=", "Client Workdesk"]]},
	{"dt": "Print Format", "filters": [["module", "=", "Client Workdesk"]]},
]

# Apps
# ------------------

required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "client_workdesk",
# 		"logo": "/assets/client_workdesk/logo.png",
# 		"title": "Client Workdesk",
# 		"route": "/client_workdesk",
# 		"has_permission": "client_workdesk.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/client_workdesk/css/task_kanban.css"
# After ERPNext bundles (so `task_list.js` runs first); merges Task listview + Kanban UX.
app_include_js = "/assets/client_workdesk/js/task_kanban_listview.js"

# include js, css files in header of web template
# web_include_css = "/assets/client_workdesk/css/client_workdesk.css"
# web_include_js = "/assets/client_workdesk/js/client_workdesk.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "client_workdesk/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Task": "public/js/task_workdesk.js",
	"Project": "public/js/project_workdesk.js",
	"Customer": "public/js/customer_workdesk.js",
	"Follow-up": "public/js/follow_up_workdesk.js",
	"Deployment Plan": "public/js/deployment_plan_workdesk.js",
	"Sales Invoice": "public/js/sales_invoice_workdesk.js",
	"Client Application": "public/js/client_application_workdesk.js",
	"Implementation Note": "public/js/implementation_note_workdesk.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {
	"Task": "public/js/task_calendar.js",
	"Follow-up": "public/js/follow_up_calendar.js",
	"Deployment Plan": "public/js/deployment_plan_calendar.js",
	"Sales Invoice": "public/js/sales_invoice_follow_up_calendar.js",
}

# Desk calendar switcher (merged with other apps, e.g. ERPNext "Task")
calendars = [
	"Follow-up",
	"Deployment Plan",
	"Sales Invoice",
]

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "client_workdesk/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "client_workdesk.utils.jinja_methods",
# 	"filters": "client_workdesk.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "client_workdesk.install.before_install"
# Clear Jinja loader cache after install so website `www/index.html` from other apps still resolves.
after_install = "client_workdesk.install.after_migrate"
after_migrate = "client_workdesk.install.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "client_workdesk.uninstall.before_uninstall"
# after_uninstall = "client_workdesk.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "client_workdesk.utils.before_app_install"
# after_app_install = "client_workdesk.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "client_workdesk.utils.before_app_uninstall"
# after_app_uninstall = "client_workdesk.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "client_workdesk.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Task": {
		"validate": "client_workdesk.events.task_events.task_validate",
		"after_insert": "client_workdesk.events.task_events.task_after_insert",
		"on_update": "client_workdesk.events.task_events.task_on_update",
	},
	"Sales Invoice": {
		"validate": "client_workdesk.events.sales_invoice_events.sales_invoice_validate",
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"client_workdesk.scheduled_jobs.send_daily_work_summary",
		"client_workdesk.scheduled_jobs.notify_overdue_tasks_daily",
		"client_workdesk.scheduled_jobs.notify_followups_due_today",
		"client_workdesk.scheduled_jobs.notify_invoice_followups_due_today",
		"client_workdesk.scheduled_jobs.update_auto_project_health",
	],
}

# Testing
# -------

# before_tests = "client_workdesk.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "client_workdesk.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "client_workdesk.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "client_workdesk.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["client_workdesk.utils.before_request"]
# after_request = ["client_workdesk.utils.after_request"]

# Job Events
# ----------
# before_job = ["client_workdesk.utils.before_job"]
# after_job = ["client_workdesk.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"client_workdesk.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

