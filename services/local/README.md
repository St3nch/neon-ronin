# services/local

Future local sidecar/service boundary.

This folder is reserved for a later local service or sidecar process, potentially used by the desktop app for long-running workflows.

Current status:

```text
deferred
```

Do not add FastAPI, LangGraph runtime, daemon behavior, agent runtime, scheduled jobs, watch mode, or service packaging here until a separate decision authorizes local-service work.

The first persistence proof must remain a direct module/service call in `packages/neon-core`.