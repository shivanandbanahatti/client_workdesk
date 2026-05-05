// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Client Application", {
	onload(frm) {
		if (!frm.is_new() || !frappe.route_options) {
			return;
		}
		const ro = frappe.route_options;
		if (ro.customer) {
			frm.set_value("customer", ro.customer);
		}
		frappe.route_options = null;
	},
});
