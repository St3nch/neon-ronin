# Internal Research First Proof Parameters - Persistence Proof 001

## Status

```text
planned
```

This document records exact first proof parameters for the approved minimal implementation plan.

It chooses the proposed storage substrate, fixture strategy, transaction boundary, and hammer proof for review.

It does not write code.

It does not create database migrations.

It does not implement storage.

It does not create database tables.

It does not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Parameter Metadata

```yaml
first_proof_parameter_record_id: first_proof_params_internal_research_persistence_001
implementation_plan_id: impl_plan_internal_research_persistence_001
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_parameter_time: manual_test
source_implementation_plan: docs/workspaces/internal-research/minimal-implementation-plan-persistence-001.md
parameter_status: planned
created_at: 2026-05-26T00:00:00Z
updated_at: 2026-05-26T00:00:00Z
schema_version: first_proof_parameter_record_v1
record_revision: 1
```

## Parameter Decision Summary

Proposed first proof parameters:

```yaml
storage_substrate: sqlite
execution_surface: direct_service_module_call
fixture_strategy: hand-authored_minimal_fixture_extracted_from_internal_research_workspace_config
transaction_boundary: workspace_config_create
hammer_proof: hammer-audit-first-workspace-config-create
audit_failure_strategy: injectable_audit_write_failure
failed_attempt_audit_logging: deferred
human_decision_record_required_for_first_proof: false
```

## Storage Substrate

Chosen proposed substrate:

```text
SQLite
```

Rationale:

- local-first
- low setup cost
- supports real atomic transactions
- enough to prove audit-first write behavior
- avoids production database architecture gravity
- avoids cloud services and integrations
- deterministic enough for the first hammer proof

Non-goals:

- this does not choose Neon Ronin's final production database
- this does not design the full database architecture
- this does not create migrations
- this does not forbid future Postgres adoption

SQLite is selected only as the proposed substrate for the first local persistence proof.

## Execution Surface

Chosen proposed execution surface:

```text
direct_service_module_call
```

Rationale:

- avoids premature API/server design
- keeps the first proof focused on persistence and audit-first behavior
- still allows a real transaction boundary and real hammer probe
- avoids UI, agents, integrations, and routing concerns

Non-goals:

- no HTTP API
- no CLI contract
- no MCP tool
- no agent-accessible surface
- no user-facing interface

## Fixture Strategy

Chosen proposed fixture strategy:

```text
hand-authored_minimal_fixture_extracted_from_internal_research_workspace_config
```

Fixture source:

```text
docs/workspaces/internal-research/workspace-config.draft.md
```

Fixture rule:

```text
The markdown file is not a database import source.
```

A minimal fixture should be hand-authored from the governed example while preserving only the fields necessary to validate `workspace_config_create` and audit-first behavior.

Required fixture properties:

```yaml
workspace_id: ws_internal_research_001
workspace_type: internal_research
status: manual_test
runtime:
  default_mode: off
  scheduled_allowed: false
  watch_mode_allowed: false
allowed_agents: []
external_references: []
schema_version: schema_v1
record_revision: 1
```

Fixture must not include:

- provider payloads
- credentials
- customer data
- SearchClarity-specific fields
- unbounded `metadata`
- `custom_data`
- executable agent definitions
- integration references

## Transaction Boundary

Chosen transaction boundary:

```text
workspace_config_create
```

Expected atomic write unit:

```text
workspace config record + creation audit record
```

Required invariant:

```text
no audit record means no workspace config record
```

Positive case expectation:

- workspace config persists
- exactly one creation audit record persists
- audit target points to created workspace config
- deterministic success result is returned
- no extra hidden records are created

Negative case expectation:

- forced audit-write failure blocks or rolls back workspace config creation
- no partial workspace config remains durable
- deterministic failure result is returned
- retry posture is clean

## Hammer Proof

Chosen hammer proof:

```text
hammer-audit-first-workspace-config-create
```

Required checks:

1. valid workspace config creation creates exactly one workspace config and one audit record
2. forced audit creation failure blocks or rolls back workspace config creation
3. no partial workspace config remains after failure
4. caller cannot forge system-owned fields
5. unknown fields are rejected
6. forbidden fields such as unbounded `metadata` or `custom_data` are rejected
7. timestamps are UTC ISO 8601 with `Z` suffix
8. `schema_version` and `record_revision` are present and correctly owned
9. result is deterministic and not mock-only

Explicitly insufficient:

- mocked happy path only
- checking only that a return object exists
- audit record created outside the transaction without rollback proof
- workspace config persisted first and audit record attempted later

## Audit Failure Strategy

Chosen proposed audit failure strategy:

```text
injectable_audit_write_failure
```

The first proof should include an implementation seam that lets the hammer proof force audit-record creation to fail during the transaction.

The failure should happen after workspace config validation but before the atomic unit commits.

Expected result:

```text
transaction rolls back and no workspace config remains durable
```

## Failed-Attempt Audit Logging

Chosen proposed handling:

```text
deferred
```

Rationale:

The first proof should focus on the core invariant:

```text
no audit record means no workspace config record
```

Out-of-transaction failed-attempt audit logging can be planned later after the core transaction behavior is proven.

## Human Decision Record Requirement

Chosen proposed handling:

```text
not_required_for_first_proof
```

Rationale:

The first proof validates `workspace_config_create`, not review-decision recording.

Human-decision persistence should remain future work.

The first proof may reference the existing documentation decision as planning context, but it should not implement human-decision records yet.

## Scope Locked For First Proof

Allowed:

- local SQLite-backed persistence proof, if separately approved
- direct service/module call surface
- workspace config record persistence
- audit record persistence
- `workspace_config_create` transaction boundary
- `hammer-audit-first-workspace-config-create`
- minimal fixture extracted from Internal Research workspace config draft

Still blocked:

- code until separate approval
- database migrations until separate approval
- storage implementation until separate approval
- full DB architecture
- Postgres production planning
- API server
- CLI surface
- MCP tool surface
- UI
- agents
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing workspace onboarding
- SearchClarity onboarding
- local schema reference creation
- core schema promotion from local packet shapes
- consent records
- order records
- service-business adapter implementation

## Review Questions

1. Is SQLite acceptable for the first local proof?
2. Is a direct service/module call the right first execution surface?
3. Is fixture extraction from `workspace-config.draft.md` narrow enough?
4. Is `workspace_config_create` still the right first transaction boundary?
5. Is `hammer-audit-first-workspace-config-create` the right first hammer proof?
6. Should failed-attempt audit logging remain deferred?
7. Should human-decision record persistence remain out of scope?

## Recommended Human Decision

Recommended canonical decision:

```text
approve_with_changes
```

Recommended conditions:

```text
Approve the first proof parameters for implementation approval review only. Actual code, migrations, and storage implementation remain blocked until a separate implementation-start decision is recorded.
```

## Next Allowed Step

Record the human review decision for this first proof parameter record.

Do not write code.

Do not create database migrations.

Do not implement storage.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.