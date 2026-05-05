# Client Workdesk

Jira-like operations workspace inside ERPNext for managing multiple client projects, tasks, follow-ups, deployments, implementation notes, document checklists, and invoice reminders.

## What it provides

- Unified **Client Work Desk** workspace
- Task, Follow-up, Deployment, and Invoice Follow-up calendar views
- Task Kanban board on `work_status`
- Operational reports (today's work, overdue, waiting for client, billing, project health)
- Number cards and dashboard charts for daily visibility
- Task-linked follow-up automation and deployment/event sync
- Daily scheduler reminders and summary notifications

## Key Features

### Workspace and views

- Workspace: **Client Work Desk**
- Shortcuts for creating Task, Follow-up, Implementation Note, Deployment Plan, Sales Invoice
- Task list/kanban/calendar quick access

### Custom DocTypes

- Follow-up
- Implementation Note
- Deployment Plan
- Client Application
- Client Document Checklist

### Reports

- CWD Report Todays Work
- CWD Report Overdue Tasks
- CWD Report Followups Due Today
- CWD Report Waiting Client
- CWD Report Clientwise Open Tasks
- CWD Report Project Health
- CWD Report Billable Not Invoiced
- CWD Report Invoices Pending Payment
- CWD Report Documents Pending
- CWD Report Deployment Schedule

### Automation

- Task-side sync for linked follow-ups
- Follow-up calendar/event sync and chaining
- Deployment event sync and related-task blocking on failure/rollback
- Invoice follow-up status handling for outstanding/paid transitions
- Daily notifications for work summary and reminders

## Compatibility

Designed for Frappe / ERPNext v16 benches.

## Getting Started (Production)

### Self-hosted (existing bench)

```bash
cd /path/to/frappe-bench
bench get-app <repo-url> --branch version-16
bench --site <site-name> install-app client_workdesk
bench --site <site-name> migrate
```

## Getting Started (Development)

1. [Set up Bench](https://docs.frappe.io/framework/user/en/installation).
2. In `frappe-bench`, keep `bench start` running.
3. In another terminal:

```bash
cd /path/to/frappe-bench
bench get-app <repo-url> --branch version-16
bench new-site <site-name> --install-app client_workdesk
```

## Documentation

- Implementation + User Guide: `docs/CLIENT_WORKDESK_DOCUMENTATION.md`
- Store screenshots at: `docs/images/`

Example image usage in markdown:

```md
![Client Work Desk](images/workspace-overview.png)
```

## Contributing

This app uses `pre-commit` for formatting and linting.

```bash
cd apps/client_workdesk
pre-commit install
```

Configured tools include:

- ruff
- eslint
- prettier
- pyupgrade

## License

MIT
