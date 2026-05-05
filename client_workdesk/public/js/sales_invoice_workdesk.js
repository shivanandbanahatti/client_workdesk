// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Sales Invoice", {
	onload(frm) {
		if (!frm.is_new() || !frappe.route_options) {
			return;
		}
		const ro = frappe.route_options;
		if (ro.customer && frm.get_docfield("customer")) {
			frm.set_value("customer", ro.customer);
		}
		if (ro.project && frm.get_docfield("project")) {
			frm.set_value("project", ro.project);
		}
		frappe.route_options = null;
	},
});
