# Internal Research Implementation Start Decision - Persistence Proof 002

## Status

```text
approved
```

This document records the implementation-start decision for the next roadmap-aligned local persistence proof.

It authorizes one tiny executable Neon Ronin implementation slice: `workspace_config_update`.

It does not authorize a new persistence table, new domain record, full database architecture, UI work, agents, integrations, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Decision Metadata

```yaml
implementation_start_decision_id: decision_internal_research_implementation_start_persistence_002
prior_options_doc: docs/workspaces/internal-research/next-persistence-boundary-decision.md
prior_pushed_commit: fb9a0f3
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_decision_time: manual_test
decision_type: approve_with_constraints
decision_status: recorded
schema_version: implementation_start_decision_v1
record_revision: 1
```

## Decision

```text
Approve implementation start for `workspace_config_update`, limited to updating an existing workspace config using the existing `workspace_configs` and `audit_records` tables with audit-first transaction behavior.
```

This is the next smallest roadmap-aligned persistence boundary because it extends the existing workspace config proof without adding a new domain record.

## Why This Is The Right Next Slice

Phase 6 is validating Internal Research through low-risk workspace mechanics before SearchClarity onboarding.

The first proof demonstrated `workspace_config_create` and audit-first creation behavior.

The next useful proof should strengthen the same platform foundation before jumping into review queue, human decision, signal, or artifact persistence.

`workspace_config_update` is preferred because it:

- reuses the existing `workspace_configs` table
- reuses the existing `audit_records` table
- tests `record_revision` behavior
- tests update transaction behavior
- keeps audit-first behavior central
- avoids new tables
- avoids new domain records
- avoids pretending the review queue or human-decision layer is executable before its own boundary is approved

## Authorized Implementation Scope

This decision authorizes implementation of only:

- `workspace_config_update`
- update behavior for an existing workspace config record
- audit-first transaction behavior for the update path
- `record_revision` increment from 1 to 2 on successful update
- `updated_at` replacement on successful update
- `created_at` preservation on successful update
- rejection of caller-supplied system-owned fields
- rejection of forbidden `metadata` and `custom_data`
- rejection of unknown fields
- rejection of non-empty `allowed_agents`
- rejection of non-empty `external_references`
- rejection of scheduled/watch runtime enablement
- hammer coverage for success, validation failure, missing target, and forced audit-write failure rollback

## Authorized Tables

Only these existing tables are authorized:

```text
workspace_configs
audit_records
```

No new table is authorized by this decision.

## Authorized Files And Folders

Implementation may touch only the existing first-proof implementation areas:

```text
packages/neon-core/src/neon_ronin_core/persistence/sqlite_store.py
packages/neon-core/tests/test_workspace_config_create.py
fixtures/internal-research/workspace_config_fixture.py
tools/hammers/run_audit_first_workspace_config_create.py
tools/dev/check_first_proof.py
packages/neon-core/src/neon_ronin_core/persistence/README.md
packages/neon-core/README.md
tools/hammers/README.md
```

Doc updates may touch only directly relevant Internal Research or current-proof docs if needed.

## Transaction Boundary

The transaction boundary is:

```text
workspace_config_update
```

A successful update must write the workspace config update and the corresponding audit record in the same transaction.

A forced audit-write failure must roll back the workspace config update.

Required invariant:

```text
no update audit record means no durable workspace config update
```

## Required Positive Case

A valid update operation must:

- require the target workspace config to already exist
- update only allowed human/config-owned fields
- preserve `workspace_id`
- preserve `created_at`
- replace `updated_at`
- increment `record_revision`
- preserve `schema_version`
- create exactly one update audit record
- not create a second workspace config record
- not create any extra hidden records

## Required Negative Cases

The hammer must prove:

1. missing target workspace id does not create an audit record
2. forced audit-write failure rolls back the workspace config update
3. validation failure does not update workspace config
4. caller cannot forge system-owned fields
5. forbidden fields such as `metadata` or `custom_data` are rejected
6. unknown fields are rejected
7. non-empty `allowed_agents` is rejected
8. non-empty `external_references` is rejected
9. scheduled or watch runtime enablement is rejected

## Audit Behavior

The update audit record should identify:

- event type: workspace updated/config updated using current local proof vocabulary
- action type: `workspace_config_update`
- target type: `workspace_config`
- target id: workspace id
- result status: `succeeded`
- actor type and actor id
- timestamp fields in UTC ISO 8601 with `Z` suffix
- schema version
- record revision

The audit record should remain a bounded summary, not a payload dump.

Failed-attempt audit logging remains deferred unless separately approved.

## System-Owned Fields

Callers must not forge or directly supply:

- `workspace_id`
- `created_at`
- `updated_at`
- `schema_version`
- `record_revision`

The persistence layer owns these fields.

## Explicitly Not Authorized

This decision does not authorize:

- new tables
- new domain records
- review queue persistence
- human-decision persistence
- signal persistence
- artifact persistence
- lifecycle transition engine
- status transition authority
- runtime enablement
- agent enablement
- external references
- unbounded `metadata`
- unbounded `custom_data`
- provider payload snapshots
- credential handling
- UI
- Tauri commands
- HTTP API
- local service
- MCP tool surface
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing workspace onboarding
- SearchClarity onboarding
- automation

## Required Validation Command

Before commit, run:

```text
python tools/dev/check_first_proof.py
```

Expected result after implementation:

```text
Ran 12 or more tests
OK
```

The test count may increase because this decision authorizes new hammer coverage for update behavior.

## Next Allowed Step

Begin the `workspace_config_update` implementation in the narrow scope above.

Do not add review queue, human-decision, signal, artifact, UI, agent, integration, scheduling, watch mode, Observatory ingestion, customer-facing onboarding, SearchClarity onboarding, or automation behavior without a separate decision.
