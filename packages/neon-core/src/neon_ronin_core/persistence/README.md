# Neon Ronin Persistence Proof

This folder contains the first executable Neon Ronin persistence proof.

## Current Status

```text
proof_slice_only
```

This is not the full Neon Ronin database layer.

This is not a production persistence architecture.

This is not a desktop app, local service, agent runtime, integration layer, scheduled job system, watch mode, live Observatory ingestion path, customer-facing workspace, SearchClarity onboarding path, or automation surface.

## Authorized Scope

The current implementation is limited to:

```text
workspace_configs
audit_records
workspace_config_create
audit-first transaction behavior
hammer-audit-first-workspace-config-create
```

The core invariant is:

```text
no audit record means no workspace config record
```

## Current Files

```text
sqlite_store.py
```

`sqlite_store.py` implements a tiny SQLite-backed direct module/service proof for `workspace_config_create`.

It uses Python stdlib `sqlite3` and no external dependencies.

## Tables Authorized In This Slice

Only these tables are authorized:

```text
workspace_configs
audit_records
```

Adding any new persistence table or domain record requires a separate decision.

## Hammer Runner

Run the proof from the repository root:

```text
python tools/hammers/run_audit_first_workspace_config_create.py
```

Expected result:

```text
Ran 11 tests
OK
```

## What The Hammer Proves

The hammer currently verifies:

- valid workspace config creation writes exactly one workspace config and one audit record
- forced audit-write failure rolls back workspace config creation
- no partial workspace config remains after forced audit failure
- file-backed SQLite persistence survives reconnect
- duplicate workspace id does not create a second audit record
- caller-supplied system-owned fields are rejected
- unknown fields are rejected
- missing required fields are rejected
- forbidden `metadata` and `custom_data` are rejected
- non-empty `allowed_agents` is rejected
- non-empty `external_references` is rejected
- scheduled or watch runtime flags are rejected
- timestamps are UTC ISO 8601 strings with a `Z` suffix
- `schema_version` and `record_revision` are present and owned by the persistence layer

## Still Forbidden

Do not add any of the following in this persistence slice:

- UI code
- Tauri commands
- HTTP API
- CLI contract unless separately approved
- MCP tool surface
- executable agents
- agent definitions
- agent runs
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing workspace onboarding
- SearchClarity onboarding
- automation
- service-business adapter implementation
- order records
- consent records
- human-decision persistence
- signal persistence
- review queue persistence
- artifact persistence
- provider payload snapshots
- credential handling

## Next Safe Direction

Before expanding persistence, keep this proof green and decide the next smallest boundary explicitly.

Preferred next work should either:

1. improve the current hammer coverage without adding new tables, or
2. record a separate decision for the next persistence boundary.
