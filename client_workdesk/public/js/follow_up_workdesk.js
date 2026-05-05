// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Follow-up", {
	onload(frm) {
		if (!frm.is_new() || !frappe.route_options) {
			return;
		}
		const ro = frappe.route_options;
		if (ro.task) {
			frm.set_value("task", ro.task);
		}
		if (ro.customer) {
			frm.set_value("customer", ro.customer);
		}
		if (ro.project) {
			frm.set_value("project", ro.project);
		}
		if (ro.owner_user) {
			frm.set_value("owner_user", ro.owner_user);
		}
		frappe.route_options = null;
	},
});
