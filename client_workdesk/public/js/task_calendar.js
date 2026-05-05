// Client Workdesk — Task calendar (scheduled + expected dates, colors by type/status)

frappe.views.calendar["Task"] = {
	field_map: {
		start: "calendar_start",
		end: "calendar_end",
		id: "name",
		title: "subject",
		progress: "progress",
	},
	gantt: true,
	filters: [
		{
			fieldtype: "Link",
			fieldname: "project",
			options: "Project",
			label: __("Project"),
		},
	],
	get_events_method: "client_workdesk.desk.calendar.get_task_calendar_events",
	update_event_method: "client_workdesk.desk.calendar.update_task_calendar_event",
	options: {
		editable: true,
		selectable: true,
	},
	get_css_class(data) {
		const st = (data.work_status || "").trim();
		if (st === "Done") return "success";
		if (st === "Cancelled") return "default";
		if (st.includes("Waiting") || st === "Blocked") return "warning";
		if (st === "Testing" || st === "UAT") return "pink";
		const tt = (data.task_type || "").trim();
		if (tt === "Bug Fix") return "danger";
		if (tt.includes("Deployment")) return "red";
		if (tt.includes("Invoice") || tt.includes("Payment")) return "purple";
		if (tt === "Meeting" || tt.includes("Client Follow")) return "blue";
		if (tt === "Internal Review" || tt === "Research") return "gray";
		return "default";
	},
};
