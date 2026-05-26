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
review_queue_items
human_decisions
signal_candidates
workspace_config_create
workspace_config_update
review_queue_item_create
human_decision_record
signal_candidate_create
audit-first transaction behavior
hammer-audit-first-workspace-config-create
```

The core invariants are:

```text
no audit record means no workspace config record
no audit record means no review queue item record
no audit record means no human decision record and no review item resolution
no audit record means no signal candidate record
```

## Current Files

```text
sqlite_store.py
```

`sqlite_store.py` implements a tiny SQLite-backed direct module/service proof for `workspace_config_create`, `workspace_config_update`, `review_queue_item_create`, `human_decision_record`, and `signal_candidate_create`.

It uses Python stdlib `sqlite3` and no external dependencies.

## Tables Authorized In This Slice

Only these tables are authorized:

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
```

Adding any new persistence table or domain record requires a separate decision.

## Hammer Runner

Run the proof from the repository root:

```text
python tools/hammers/run_audit_first_workspace_config_create.py
```

Expected result:

```text
Ran 59 tests
OK
```

## What The Hammer Proves

The hammer currently verifies:

- valid workspace config creation writes exactly one workspace config and one audit record
- valid workspace config update preserves `created_at`, replaces `updated_at`, increments `record_revision`, and writes one update audit record
- valid review queue item creation writes exactly one review item and one audit record
- valid human decision recording writes exactly one human decision, resolves one review item, and writes one audit record
- valid signal candidate creation writes exactly one workspace-owned signal candidate and one audit record
- forced audit-write failure rolls back workspace config creation
- forced audit-write failure rolls back workspace config update
- forced audit-write failure rolls back review queue item creation
- forced audit-write failure rolls back human decision recording and review item resolution
- forced audit-write failure rolls back signal candidate creation
- no partial workspace config remains after forced audit failure
- no partial review queue item remains after forced audit failure
- no partial human decision or review item resolution remains after forced audit failure
- no partial signal candidate remains after forced audit failure
- file-backed SQLite persistence survives reconnect
- duplicate workspace id does not create a second audit record
- missing workspace update does not create an audit record
- review item creation requires an existing workspace
- human decision recording requires an existing unresolved review item
- signal candidate creation requires an existing workspace
- non-human reviewer actors are rejected for human decisions
- schema initialization creates only the authorized tables
- caller-supplied system-owned fields are rejected
- unknown fields are rejected
- missing required fields are rejected
- forbidden `metadata` and `custom_data` are rejected
- non-empty `allowed_agents` is rejected
- non-empty `external_references` is rejected
- scheduled or watch runtime flags are rejected
- update attempts cannot change workspace status or runtime shape
- unsupported review types, risk categories, required gates, and linked record types are rejected
- unsupported decision types, decision scopes, and target record types are rejected
- unsupported signal types, sensitivity ratings, and source reference record types are rejected
- signal candidates require `private_data_removed: true`
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
- raw signal persistence
- sanitized signal persistence
- signal status transitions
- Observatory submission
- Observatory normalization
- derived intelligence
- artifact persistence
- external action execution
- provider payload snapshots
- credential handling

## Next Safe Direction

Before expanding persistence, keep this proof green and decide the next smallest boundary explicitly.

Preferred next work should either:

1. pause and audit the current persistence slice, or
2. implement a separately approved artifact or workflow boundary.
