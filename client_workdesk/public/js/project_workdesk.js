// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Project", {
	onload(frm) {
		if (!frm.is_new() || !frappe.route_options) {
			return;
		}
		const ro = frappe.route_options;
		if (ro.customer && frm.get_docfield("customer")) {
			frm.set_value("customer", ro.customer);
		}
		frappe.route_options = null;
	},

	refresh(frm) {
		if (frm.is_new()) {
			return;
		}
		const grp = __("Workdesk");

		if (frappe.model.can_create("Task")) {
			frm.add_custom_button(
				__("New Task"),
				() => {
					frappe.route_options = {
						project: frm.doc.name,
						customer: frm.doc.customer,
						client_application: frm.doc.client_application,
					};
					frappe.new_doc("Task");
				},
				grp
			);
		}

		if (frappe.model.can_create("Follow-up")) {
			frm.add_custom_button(
				__("New Follow-up"),
				() => {
					frappe.route_options = {
						project: frm.doc.name,
						customer: frm.doc.customer,
					};
					frappe.new_doc("Follow-up");
				},
				grp
			);
		}

		if (frappe.model.can_create("Implementation Note")) {
			frm.add_custom_button(
				__("New Implementation Note"),
				() => {
					frappe.route_options = { project: frm.doc.name };
					frappe.new_doc("Implementation Note");
				},
				grp
			);
		}

		if (frappe.model.can_create("Deployment Plan")) {
			frm.add_custom_button(
				__("New Deployment Plan"),
				() => {
					frappe.route_options = {
						project: frm.doc.name,
						customer: frm.doc.customer,
						client_application: frm.doc.client_application,
					};
					frappe.new_doc("Deployment Plan");
				},
				grp
			);
		}

		if (frappe.model.can_read("Task")) {
			frm.add_custom_button(
				__("Open Tasks"),
				() => {
					frappe.route_options = {
						project: frm.doc.name,
						status: ["in", ["Open", "Working", "Overdue"]],
					};
					frappe.set_route("List", "Task");
				},
				grp
			);
		}

		frm.add_custom_button(
			__("Billing status"),
			() => {
				frappe.set_route("query-report", "CWD Report Billable Not Invoiced");
			},
			grp
		);
	},
});
