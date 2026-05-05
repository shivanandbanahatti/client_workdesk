// Client Workdesk — Deployment plan calendar (colors by environment/status)

frappe.views.calendar["Deployment Plan"] = {
	field_map: {
		start: "deployment_datetime",
		end: "deployment_calendar_end",
		id: "name",
		title: "title",
	},
	fields: [
		"deployment_datetime",
		"deployment_calendar_end",
		"title",
		"name",
		"deployment_environment",
		"status",
	],
	get_events_method: "frappe.desk.calendar.get_events",
	get_css_class(data) {
		const env = (data.deployment_environment || "").trim();
		const st = (data.status || "").trim();
		if (st === "Failed" || st === "Rolled Back") return "danger";
		if (st === "Completed") return "success";
		if (st === "Cancelled") return "gray";
		if (st === "In Progress") return "warning";
		if (env === "Production") return "red";
		if (env === "Staging") return "orange";
		if (env === "Development") return "blue";
		return "default";
	},
};
