# Client Workdesk Documentation

This document provides:

1. An implementation summary of what is available in `client_workdesk`.
2. A practical user guide for day-to-day operations.
3. Guidance on adding images/screenshots in documentation.

## 1) Implementation Summary

### App Scope

`client_workdesk` adds a Jira-like project operations layer inside ERPNext for:

- Multi-client work tracking
- Follow-ups and reminders
- Deployment planning
- Implementation documentation
- Billing follow-up visibility

### Standard DocTypes Used

- `Customer`
- `Project`
- `Task`
- `Event`
- `Timesheet`
- `Sales Invoice`

### Custom DocTypes

- `Follow-up`
- `Implementation Note`
- `Client Application`
- `Client Document Checklist`
- `Deployment Plan`

### Workspace

- Workspace: **Client Work Desk**
- Includes shortcuts, list/calendar links, number cards, and charts for operational visibility.

### Calendar Views

- Task Calendar
- Follow-up Calendar
- Deployment Calendar
- Sales Invoice Follow-up Calendar

### Kanban

- Task board configured on `work_status` with Jira-like columns and color indicators.

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

### Number Cards / Dashboard Charts

- Number cards and dashboard charts are included for daily monitoring in the workspace.

### Client Scripts

Custom form scripts are available for:

- Task
- Project
- Customer
- Follow-up
- Deployment Plan
- Sales Invoice
- Client Application
- Implementation Note

### Server-Side Hooks

- Task validation and follow-up sync logic
- Follow-up event sync / chaining logic
- Deployment plan event + task block handling
- Sales invoice follow-up status automation
- Scheduler jobs for reminders and summary notifications

### Scheduler Notifications

Daily scheduler tasks include:

- Daily work summary
- Overdue task reminder
- Follow-up due reminder
- Invoice follow-up reminder
- Auto project health evaluation (if enabled)

### Roles

- Client Work Manager
- Client Work User
- Billing User
- Implementation Reviewer

### Fixtures

Fixtures are configured for:

- Custom Field
- Property Setter
- Workspace
- Report
- Number Card
- Dashboard Chart
- Kanban Board
- Client Script
- Notification
- Role
- Workflow
- Print Format

## 2) User Guide

### A. Getting Started

1. Open ERPNext Desk.
2. Search and open **Client Work Desk** workspace.
3. Use shortcuts for quick creation:
   - New Task
   - New Follow-up
   - New Deployment Plan
   - New Implementation Note
   - New Sales Invoice

### B. Daily Workflow

1. Check **My Tasks Due Today** and **My Overdue Tasks** cards.
2. Open **CWD Report Todays Work** for a unified day plan.
3. Update Task `work_status`, due dates, and blockers.
4. Add follow-ups where client communication is pending.
5. Review payment follow-up cards/reports for billing actions.

### C. Task Handling

- Link Task to `Project`, `Customer`, and `Client Application`.
- Use Task custom buttons for related actions:
  - Create Follow-up
  - Create Implementation Note
  - Create Deployment Plan
  - Create Timesheet
  - Create Sales Invoice (when billing status is Ready to Invoice)

### D. Follow-up Handling

- Create Follow-up with due date and owner.
- Optional: enable calendar event.
- Mark done when completed; last-followed-up timestamp auto-updates.
- Use next follow-up date to spawn the next follow-up cycle.

### E. Deployment Handling

- Plan deployment with date/time, environment, and related task.
- Completed deployments can store completion notes.
- Failed / rolled-back deployments can block related tasks for visibility.

### F. Billing and Invoice Follow-up

- Use billable and pending payment reports for finance operations.
- Invoice follow-up status is tracked and reminders are generated.

### G. Project Health Monitoring

- Review **CWD Report Project Health** regularly.
- If auto health is enabled on project, status can be derived from overdue/waiting/billing signals.

## 3) How to Add Images in Documentation

You can add images in two common ways.

### Option 1: Markdown documentation in repository

1. Put image files in:
   - `apps/client_workdesk/docs/images/`
2. Reference in markdown:

```md
![Task Kanban](images/task-kanban.png)
```

For this file specifically, use:

```md
![Task Kanban](images/task-kanban.png)
![Today Report](images/todays-work-report.png)
```

### Option 2: Frappe Wiki / Website / Knowledge Base pages

1. Upload image via Attach or the editor image uploader.
2. Insert image in rich text editor (it stores file URL).
3. Keep image names descriptive (`client-work-desk-overview.png`, etc.).

### Recommended Image List

- Workspace overview
- Task Kanban board
- Task calendar
- Follow-up form
- Deployment plan form
- Today’s Work report
- Invoices Pending Payment report

## 4) Post-Deployment Checklist

After updates:

1. `bench --site <site> migrate`
2. `bench --site <site> clear-cache`
3. `bench --site <site> clear-website-cache`
4. Hard refresh browser.

If a custom DocType is visible in filesystem but not in UI/database, run migrate and verify module path/doctype sync before testing.
