// Client Workdesk — Follow-up calendar (datetime from due date/time; colors by type/priority)

frappe.views.calendar["Follow-up"] = {
	field_map: {
		start: "calendar_starts_on",
		end: "calendar_ends_on",
		id: "name",
		title: "subject",
	},
	fields: [
		"calendar_starts_on",
		"calendar_ends_on",
		"subject",
		"name",
		"follow_up_type",
		"priority",
		"status",
	],
	get_events_method: "frappe.desk.calendar.get_events",
	get_css_class(data) {
		const pr = (data.priority || "").trim();
		if (pr === "Critical") return "danger";
		if (pr === "High") return "warning";
		if (pr === "Medium") return "default";
		if (pr === "Low") return "gray";
		const ft = (data.follow_up_type || "").trim();
		if (ft === "Invoice" || ft === "Payment") return "purple";
		if (ft === "Deployment" || ft === "UAT") return "red";
		if (ft === "Client Call" || ft === "Client Email" || ft === "WhatsApp") return "blue";
		if (ft === "Internal") return "gray";
		if (ft === "Vendor") return "pink";
		return "default";
	},
};
