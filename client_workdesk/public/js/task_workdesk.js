// Copyright (c) 2026, Client Workdesk contributors
// License: MIT

frappe.ui.form.on("Task", {
	onload(frm) {
		if (!frm.is_new() || !frappe.route_options) {
			return;
		}
		const ro = frappe.route_options;
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

	project(frm) {
		cwd_task_sync_from_project(frm);
	},

	follow_up_required(frm) {
		cwd_task_toggle_follow_up(frm);
	},

	blocked(frm) {
		cwd_task_toggle_blocked(frm);
	},

	work_status(frm) {
		if ((frm.doc.work_status || "") === "Done") {
			cwd_task_prompt_done_extras(frm);
		}
	},

	refresh(frm) {
		cwd_task_toggle_follow_up(frm);
		cwd_task_toggle_blocked(frm);
		cwd_task_add_workdesk_buttons(frm);
	},
});

function cwd_task_sync_from_project(frm) {
	if (!frm.doc.project) {
		frm.set_value("customer", "");
		frm.set_value("client_application", "");
		return;
	}
	frappe.db.get_value("Project", frm.doc.project, ["customer", "client_application"]).then((r) => {
		const row = r.message;
		if (!row) {
			return;
		}
		if (row.customer) {
			frm.set_value("customer", row.customer);
		}
		if (row.client_application) {
			frm.set_value("client_application", row.client_application);
		} else {
			frm.set_value("client_application", "");
		}
	});
}

function cwd_task_toggle_follow_up(frm) {
	const on = !!frm.doc.follow_up_required;
	if (frm.get_docfield("follow_up_date")) {
		frm.set_df_property("follow_up_date", "hidden", !on);
		frm.set_df_property("follow_up_date", "reqd", on);
	}
}

function cwd_task_toggle_blocked(frm) {
	const on = !!frm.doc.blocked;
	if (frm.get_docfield("blocked_reason")) {
		frm.set_df_property("blocked_reason", "hidden", !on);
		frm.set_df_property("blocked_reason", "reqd", on);
	}
}

function cwd_task_prompt_done_extras(frm) {
	const need_hours = frm.get_docfield("actual_hours") && !frm.doc.actual_hours;
	const need_note = frm.get_docfield("implementation_note") && !frm.doc.implementation_note;
	if (!need_hours && !need_note) {
		return;
	}
	frappe.confirm(
		__(
			"Work status is Done. Add actual hours and/or link an Implementation Note before saving?"
		),
		() => {
			if (need_hours) {
				frm.scroll_to_field("actual_hours");
			} else if (need_note) {
				frm.scroll_to_field("implementation_note");
			}
		},
		() => {}
	);
}

function cwd_task_add_workdesk_buttons(frm) {
	const grp = __("Workdesk");

	if (frappe.model.can_create("Implementation Note")) {
		frm.add_custom_button(
			__("Create Implementation Note"),
			() => {
				const opts = {};
				if (!frm.is_new()) {
					opts.related_task = frm.doc.name;
					opts.project = frm.doc.project;
				}
				frappe.route_options = opts;
				frappe.new_doc("Implementation Note");
			},
			grp
		);
	}

	if (frappe.model.can_create("Follow-up")) {
		frm.add_custom_button(
			__("Create Follow-up"),
			() => {
				if (frm.is_new()) {
					frappe.msgprint(__("Save the Task first to link a Follow-up."));
					return;
				}
				frappe.route_options = {
					task: frm.doc.name,
					customer: frm.doc.customer,
					project: frm.doc.project,
					owner_user: frappe.session.user,
				};
				frappe.new_doc("Follow-up");
			},
			grp
		);
	}

	if (frappe.model.can_create("Deployment Plan")) {
		frm.add_custom_button(
			__("Create Deployment Plan"),
			() => {
				if (frm.is_new()) {
					frappe.msgprint(__("Save the Task first to link a Deployment Plan."));
					return;
				}
				frappe.route_options = {
					related_task: frm.doc.name,
					project: frm.doc.project,
					customer: frm.doc.customer,
					client_application: frm.doc.client_application,
				};
				frappe.new_doc("Deployment Plan");
			},
			grp
		);
	}

	if (frappe.model.can_create("Timesheet")) {
		frm.add_custom_button(
			__("Create Timesheet"),
			() => {
				if (frm.is_new()) {
					frappe.msgprint(__("Save the Task first to log time against it."));
					return;
				}
				cwd_open_new_timesheet_for_task(frm);
			},
			grp
		);
	}

	if (
		(frm.doc.billing_status || "") === "Ready to Invoice" &&
		frappe.model.can_create("Sales Invoice")
	) {
		frm.add_custom_button(
			__("Create Sales Invoice"),
			() => {
				if (frm.is_new()) {
					frappe.msgprint(__("Save the Task first."));
					return;
				}
				frappe.route_options = {
					customer: frm.doc.customer,
					project: frm.doc.project,
				};
				frappe.new_doc("Sales Invoice");
			},
			grp
		);
	}
}

function cwd_open_new_timesheet_for_task(frm) {
	frappe.model.with_doctype("Timesheet", () => {
		const doc = frappe.model.get_new_doc("Timesheet");
		doc.customer = frm.doc.customer;
		doc.project = frm.doc.project;
		doc.time_logs = [];
		const row = frappe.model.add_child(doc, "Timesheet Detail", "time_logs");
		row.project = frm.doc.project;
		row.task = frm.doc.name;
		frappe.set_route("Form", "Timesheet", doc.name);
	});
}
