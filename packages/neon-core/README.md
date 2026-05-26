# packages/neon-core

Reusable Neon Ronin core package.

This package is the home for the first local persistence proof and future reusable platform-domain logic.

Current authorized scope:

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
workspace_config_create
workspace_config_update
review_queue_item_create
human_decision_record
signal_candidate_create
audit-first write behavior
hammer-audit-first-workspace-config-create
```

Current forbidden scope:

```text
UI
Tauri commands
HTTP API
CLI contract unless required by hammer proof
MCP tool surface
agents
integrations
scheduled jobs
watch mode
live Observatory ingestion
customer-facing workspace onboarding
SearchClarity onboarding
automation
```

Use this package to keep the platform core reusable by future app shells and services.