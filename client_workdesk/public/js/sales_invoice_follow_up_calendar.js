// Client Workdesk — unpaid invoices pending payment follow-up (by invoice_follow_up_date)

frappe.views.calendar["Sales Invoice"] = {
	field_map: {
		start: "invoice_follow_up_date",
		end: "invoice_follow_up_date",
		id: "name",
		title: "calendar_title",
	},
	get_events_method: "client_workdesk.desk.calendar.get_sales_invoice_follow_up_events",
	get_css_class(data) {
		const ps = (data.payment_follow_up_status || "").trim();
		const st = (data.si_status || "").trim();
		if (st === "Overdue" || ps === "Escalated") return "danger";
		if (ps === "Pending") return "warning";
		if (ps === "Followed Up") return "orange";
		return "default";
	},
};
