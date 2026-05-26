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
artifact_metadata
workflow_records
workspace_config_create
workspace_config_update
review_queue_item_create
human_decision_record
signal_candidate_create
artifact_metadata_create
workflow_record_create
audit-first transaction behavior
first-persistence-proof
```

The core invariants are:

```text
no audit record means no workspace config record
no audit record means no review queue item record
no audit record means no human decision record and no review item resolution
no audit record means no signal candidate record
no audit record means no artifact metadata record
no audit record means no workflow record
```

## Current Files

```text
common.py
constants.py
errors.py
results.py
schema.py
sqlite_store.py
validators.py
```

`sqlite_store.py` keeps the SQLite-backed transaction/read/write orchestration for `workspace_config_create`, `workspace_config_update`, `review_queue_item_create`, `human_decision_record`, `signal_candidate_create`, `artifact_metadata_create`, and `workflow_record_create`.

The supporting modules keep the proof readable:

- `common.py` contains shared timestamp, id factory, and JSON helpers.
- `constants.py` contains bounded proof constants and allowed values.
- `errors.py` contains persistence proof error types.
- `results.py` contains operation result dataclasses.
- `schema.py` contains SQLite schema initialization.
- `validators.py` contains bounded payload validators.

It uses Python stdlib `sqlite3` and no external dependencies.

## Tables Authorized In This Slice

Only these tables are authorized:

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
artifact_metadata
workflow_records
```

Adding any new persistence table or domain record requires a separate decision.

## Hammer Runner

Run the proof from the repository root:

```text
python tools/hammers/run_first_persistence_proof.py
```

Expected result:

```text
Ran 87 tests
OK
```

## What The Hammer Proves

The hammer currently verifies:

- valid workspace config creation writes exactly one workspace config and one audit record
- valid workspace config update preserves `created_at`, replaces `updated_at`, increments `record_revision`, and writes one update audit record
- valid review queue item creation writes exactly one review item and one audit record
- valid human decision recording writes exactly one human decision, resolves one review item, and writes one audit record
- valid signal candidate creation writes exactly one workspace-owned signal candidate and one audit record
- valid artifact metadata creation writes exactly one metadata-only artifact record and one audit record
- valid workflow record creation writes exactly one manual-test workflow definition and one audit record
- forced audit-write failure rolls back workspace config creation
- forced audit-write failure rolls back workspace config update
- forced audit-write failure rolls back review queue item creation
- forced audit-write failure rolls back human decision recording and review item resolution
- forced audit-write failure rolls back signal candidate creation
- forced audit-write failure rolls back artifact metadata creation
- forced audit-write failure rolls back workflow record creation
- no partial workspace config remains after forced audit failure
- no partial review queue item remains after forced audit failure
- no partial human decision or review item resolution remains after forced audit failure
- no partial signal candidate remains after forced audit failure
- no partial artifact metadata remains after forced audit failure
- no partial workflow record remains after forced audit failure
- file-backed SQLite persistence survives reconnect
- duplicate workspace id does not create a second audit record
- missing workspace update does not create an audit record
- review item creation requires an existing workspace
- human decision recording requires an existing unresolved review item
- signal candidate creation requires an existing workspace
- artifact metadata creation requires an existing workspace
- workflow record creation requires an existing workspace
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
- unsupported artifact types, content scopes, creator actor types, content formats, sensitivity ratings, confidence values, and source reference record types are rejected
- unsupported workflow types, scope types, runtime modes, triggers, step actors, step payload fields, and workflow I/O types are rejected
- signal candidates require `private_data_removed: true`
- artifact metadata requires `storage_reference.content_stored_in_core: false`
- artifact metadata rejects delivery-ready and public-use shortcuts
- artifact metadata rejects storage references containing credential or content payload fields
- workflow records are definitions only and reject scheduled/watch/external-event triggers
- workflow records reject agent and integration step actors
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
- artifact content storage
- blob storage
- artifact status transitions
- delivery-ready marking
- artifact delivery or publishing
- workflow execution
- workflow run records
- workflow status transitions
- external action execution
- provider payload snapshots
- credential handling

## Next Safe Direction

Before expanding persistence, keep this proof green and decide the next smallest boundary explicitly.

Preferred next work should audit the split persistence slice before adding another table.
