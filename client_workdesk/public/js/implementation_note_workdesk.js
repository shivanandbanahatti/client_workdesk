frappe.ui.form.on("Implementation Note", {
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
		frappe.route_options = null;
	},
});
