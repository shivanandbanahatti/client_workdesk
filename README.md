### Client Workdesk

Multi-client work desk for projects, tasks, and billing inside ERPNext

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app client_workdesk
```

### Documentation

- Implementation + User Guide: `docs/CLIENT_WORKDESK_DOCUMENTATION.md`
- Add screenshots under: `docs/images/`

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/client_workdesk
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
