// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Customer", {
	refresh(frm) {
		if (frm.is_new()) {
			return;
		}
		const grp = __("Workdesk");

		if (frappe.model.can_create("Project")) {
			frm.add_custom_button(
				__("New Project"),
				() => {
					frappe.route_options = { customer: frm.doc.name };
					frappe.new_doc("Project");
				},
				grp
			);
		}

		if (frappe.model.can_create("Client Application")) {
			frm.add_custom_button(
				__("New Client Application"),
				() => {
					frappe.route_options = { customer: frm.doc.name };
					frappe.new_doc("Client Application");
				},
				grp
			);
		}

		if (frappe.model.can_read("Task")) {
			frm.add_custom_button(
				__("Open Tasks"),
				() => {
					frappe.route_options = {
						customer: frm.doc.name,
						status: ["in", ["Open", "Working", "Overdue"]],
					};
					frappe.set_route("List", "Task");
				},
				grp
			);
		}

		if (frappe.model.can_read("Follow-up")) {
			frm.add_custom_button(
				__("Follow-ups"),
				() => {
					frappe.route_options = { customer: frm.doc.name };
					frappe.set_route("List", "Follow-up");
				},
				grp
			);
		}

		frm.add_custom_button(
			__("Pending Invoices"),
			() => {
				frappe.set_route("query-report", "CWD Report Invoices Pending Payment");
			},
			grp
		);
	},
});
