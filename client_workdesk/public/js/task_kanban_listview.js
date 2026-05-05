// Client Workdesk — Task Kanban (work_status): card styling + quick filters.
// Loaded via app_include_js so it runs after ERPNext `task_list.js`.

(function () {
	const base = frappe.listview_settings.Task || {};

	function setup_task_kanban(listview) {
		if (listview._cw_kanban_setup) {
			return;
		}
		listview._cw_kanban_setup = true;

		const orig_refresh = listview.refresh.bind(listview);
		listview.refresh = function (refresh_header) {
			return orig_refresh(refresh_header).then(() => {
				frappe.next_tick(() => decorate_task_kanban_cards(listview));
			});
		};

		const group = __("Client Workdesk");
		listview.page.add_inner_button(__("Waiting for Client"), () => {
			listview.filter_area
				.clear(false)
				.then(() =>
					listview.filter_area.add([["Task", "work_status", "=", "Waiting for Client"]]),
				);
		}, group);

		listview.page.add_inner_button(__("Overdue (open)"), () => {
			const today = frappe.datetime.get_today();
			listview.filter_area
				.clear(false)
				.then(() =>
					listview.filter_area.add([
						["Task", "exp_end_date", "<", today],
						["Task", "work_status", "not in", ["Done", "Cancelled"]],
					]),
				);
		}, group);
	}

	function decorate_task_kanban_cards(listview) {
		if (listview.view_name !== "Kanban" || !listview.$result || !listview.$result.length) {
			return;
		}
		const data = listview.data || [];
		listview.$result.find(".kanban-card-wrapper").each(function () {
			const $w = $(this);
			const enc = $w.attr("data-name");
			if (!enc) {
				return;
			}
			let name;
			try {
				name = decodeURIComponent(enc);
			} catch (e) {
				name = enc;
			}
			const row = data.find((r) => r.name === name);
			const cls =
				"cw-kanban-card cw-kanban-priority-low cw-kanban-priority-medium cw-kanban-priority-high cw-kanban-priority-critical cw-kanban-overdue cw-kanban-blocked";
			$w.find(".kanban-card").first().removeClass(cls);
			if (!row) {
				return;
			}
			const $card = $w.find(".kanban-card").first();
			const $target = $card.length ? $card : $w;
			$target.addClass("cw-kanban-card");

			const pr = (row.task_priority || "").trim();
			if (pr === "Critical") {
				$target.addClass("cw-kanban-priority-critical");
			} else if (pr === "High") {
				$target.addClass("cw-kanban-priority-high");
			} else if (pr === "Medium") {
				$target.addClass("cw-kanban-priority-medium");
			} else if (pr === "Low") {
				$target.addClass("cw-kanban-priority-low");
			}

			if (cint(row.blocked)) {
				$target.addClass("cw-kanban-blocked");
				if (row.blocked_reason) {
					$w.attr("title", row.blocked_reason);
				}
			} else {
				$w.removeAttr("title");
			}

			if (is_task_row_overdue(row)) {
				$target.addClass("cw-kanban-overdue");
			}
		});
	}

	function is_task_row_overdue(row) {
		if (!row.exp_end_date) {
			return false;
		}
		if (["Done", "Cancelled"].includes((row.work_status || "").trim())) {
			return false;
		}
		return frappe.datetime.get_diff(frappe.datetime.get_today(), row.exp_end_date) > 0;
	}

	frappe.listview_settings.Task = Object.assign({}, base, {
		add_fields: [
			...new Set([
				...(base.add_fields || []),
				"work_status",
				"task_priority",
				"blocked",
				"blocked_reason",
			]),
		],
		onload(listview) {
			base.onload && base.onload(listview);
			if (listview.doctype === "Task" && listview.view_name === "Kanban") {
				setup_task_kanban(listview);
			}
		},
	});
})();
