// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Deployment Plan", {
	onload(frm) {
		if (!frm.is_new() || !frappe.route_options) {
			return;
		}
		const ro = frappe.route_options;
		if (ro.related_task) {
			frm.set_value("related_task", ro.related_task);
		}
		if (ro.project) {
			frm.set_value("project", ro.project);
		}
		if (ro.customer) {
			frm.set_value("customer", ro.customer);
		}
		if (ro.client_application) {
			frm.set_value("client_application", ro.client_application);
		}
		frappe.route_options = null;
	},
});
