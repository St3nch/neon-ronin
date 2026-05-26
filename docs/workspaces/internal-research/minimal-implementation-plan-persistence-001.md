# Internal Research Minimal Implementation Plan - Persistence Proof 001

## Status

```text
approved
```

This document defines the first minimal executable persistence proof Neon Ronin may prepare for after the implementation-readiness decision.

It is an implementation plan only.

It does not write code.

It does not create database migrations.

It does not choose a final database architecture.

It does not implement an API, UI, agent runtime, integration, scheduled job, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Plan Metadata

```yaml
implementation_plan_id: impl_plan_internal_research_persistence_001
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_plan_time: manual_test
source_implementation_readiness_decision: docs/workspaces/internal-research/implementation-readiness-decision.md
plan_status: approved
created_at: 2026-05-26T00:00:00Z
updated_at: 2026-05-26T00:00:00Z
schema_version: implementation_plan_v1
record_revision: 2
```

## Decision Inherited

The implementation-readiness decision approved planning for a minimal persistence proof only.

It did not approve implementation.

This plan therefore defines the proposed proof and the approval requirements before any code or migration work begins.

## Goal

Prove the smallest useful Neon Ronin executable invariant:

```text
A workspace config cannot be durably created without its required audit record.
```

The proof should validate the audit-first transaction doctrine with the least possible implementation surface.

## Proposed Slice

```text
minimal_internal_persistence_proof
```

Included records:

```text
workspace_configs
audit_records
```

Included behavior:

```text
audit-first write path
workspace_config_create transaction boundary
one hammer proof for audit-first blocking or rollback
```

## Authoritative Docs

The first implementation proof must treat these docs as authoritative:

| Area | Authoritative Doc |
|---|---|
| schema authority | `docs/core/14-schema-authority.md` |
| workspace config schema | `docs/core/schemas/workspace-config.schema.md` |
| audit record schema | `docs/core/schemas/audit-record.schema.md` |
| transaction boundary | `docs/core/20-transaction-boundaries.md` |
| audit/error behavior | `docs/core/16-error-and-failure-handling.md` |
| permissions/audit doctrine | `docs/core/07-permissions-and-audit.md` |
| hammer doctrine | `docs/core/19-hammer-testing-doctrine.md` |
| workspace lifecycle | `docs/core/09-workspace-lifecycle.md` |
| current workspace example | `docs/workspaces/internal-research/workspace-config.draft.md` |

If these docs conflict, pause and resolve the doctrine conflict before implementation.

## Proposed Storage Substrate Candidates

This plan may evaluate storage substrates but does not choose one.

Candidate set:

```text
SQLite
Postgres
file-backed JSON/NDJSON prototype
```

Selection criteria for the implementation approval step:

- supports atomic multi-write transaction or an equivalent proof mechanism
- can enforce required fields and reject unknown/forbidden fields at the application/service boundary
- can support append-friendly audit records
- can support deterministic tests
- does not require a large framework or production architecture decision
- does not introduce integrations, cloud services, or customer-facing exposure

Preferred planning bias:

```text
Choose the smallest local substrate that can honestly prove audit-first behavior.
```

The implementation approval may choose SQLite, Postgres, or another local substrate, but must justify the choice against the criteria above.

## First Transaction Boundary

Preferred transaction boundary:

```text
workspace_config_create
```

From `docs/core/20-transaction-boundaries.md`, the operation creates:

- workspace config record
- creation audit record

Required rollback behavior:

```text
If audit creation fails, workspace config creation rolls back.
```

## Minimal Positive Case

A valid create request should produce exactly:

- one workspace config record
- one linked audit record
- deterministic success result
- no extra hidden records
- no provider payloads
- no unbounded metadata
- no executable agent/run records

The audit record should reference the created workspace config with:

```yaml
target_type: workspace_config
target_id: <created workspace_id>
result_status: succeeded
```

## Minimal Negative Case

A forced audit-write failure during `workspace_config_create` should produce:

- no durable workspace config record
- no partial success result
- deterministic failure result
- clean retry posture

A failed transaction may preserve a failed-attempt audit only if the implementation explicitly models out-of-transaction attempt logging.

The first proof should prefer the simpler rule:

```text
no audit record means no workspace config record
```

## First Hammer Proof

Proposed first hammer proof:

```text
hammer-audit-first-workspace-config-create
```

It must verify:

1. valid workspace config creation creates exactly one workspace config and one audit record
2. forced audit creation failure prevents or rolls back workspace config creation
3. no partial workspace config remains after failure
4. system-owned fields cannot be forged by caller input
5. unknown fields are rejected
6. forbidden fields such as unbounded `metadata` or `custom_data` are rejected
7. timestamps are UTC ISO 8601 with `Z` suffix
8. `schema_version` and `record_revision` are present and correctly owned
9. result is deterministic and not mock-only

This hammer proof should be real enough to exercise the actual persistence boundary chosen later.

A mocked happy-path-only test is not sufficient.

## Candidate Initial Workspace Config Fixture

Use the Internal Research workspace as a low-risk fixture.

Candidate fixture source:

```text
docs/workspaces/internal-research/workspace-config.draft.md
```

The implementation plan must not treat that markdown file as a database import source without a separate fixture extraction step.

The fixture should preserve these boundaries:

- `workspace_id: ws_internal_research_001`
- `workspace_type: internal_research`
- `status: manual_test`
- `runtime.default_mode: off`
- `allowed_agents: []`
- `scheduled_allowed: false`
- `watch_mode_allowed: false`
- `external_references: []`

## Non-Goals

This plan explicitly excludes:

- full database design
- production database architecture
- migrations
- API server implementation
- UI implementation
- agent runtime
- executable agent definitions
- agent runs
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing workspace onboarding
- SearchClarity onboarding
- service-business adapter implementation
- order records
- consent records
- local schema reference creation
- core schema promotion from local packet shapes
- provider payload snapshots
- credential handling
- authentication/authorization system design

## Approval Required Before Implementation

Before code, database migration, or executable test work begins, a human decision must approve the implementation plan.

Required canonical decision type:

```text
approve_with_changes
```

Required minimum conditions:

- implementation remains local-only
- scope remains limited to `workspace_configs` and `audit_records`
- first transaction remains `workspace_config_create` unless explicitly changed
- first hammer proof remains audit-first blocking/rollback unless explicitly changed
- no agents
- no integrations
- no UI
- no scheduled jobs
- no watch mode
- no live Observatory ingestion
- no customer-facing workspace onboarding
- no SearchClarity onboarding
- no local schema reference creation
- no core schema promotion from local packet shapes

## Open Questions For Review

1. Which local storage substrate should be selected for the first proof?
2. Should the first proof use a direct service/module call instead of an HTTP/API surface?
3. Should audit failure be simulated by dependency injection, transaction hook, or validation failure?
4. Should failed-attempt audit logging be deferred until after the first proof?
5. What is the minimum fixture extraction format from the Internal Research workspace config draft?
6. Does the first proof need a human-decision record, or is workspace config + audit record sufficient?

## Recommended Review Decision

Recommended decision:

```text
approve_with_changes
```

Recommended condition:

```text
Approve planning only for a local minimal persistence proof. Implementation may begin only after a separate human approval records the storage substrate, fixture strategy, transaction boundary, and hammer proof.
```

## Human Review Decision

```yaml
human_decision_id: decision_minimal_implementation_plan_persistence_001
decision_type: approve_with_changes
decision_status: recorded
actor_type: human
actor_id: human_operator
decision_summary: Approve the minimal implementation plan for planning only. The next step may record exact first proof parameters, but code, migrations, storage implementation, agents, integrations, UI, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, and automation remain blocked.
conditions:
  - planning only
  - storage substrate must be recorded before code
  - fixture strategy must be recorded before code
  - transaction boundary remains workspace_config_create unless separately changed
  - first hammer proof remains audit-first blocking or rollback unless separately changed
  - scope remains limited to workspace_configs and audit_records unless separately changed
  - no code until separate approval
  - no database migrations until separate approval
  - no storage implementation until separate approval
  - no agents
  - no integrations
  - no UI
  - no scheduled jobs
  - no watch mode
  - no live Observatory ingestion
  - no customer-facing workspace onboarding
  - no SearchClarity onboarding
  - no automation
source_references:
  - record_type: manual_note
    record_id: impl_plan_internal_research_persistence_001
    relationship: approved_plan
schema_version: schema_v1
record_revision: 1
```
## Next Allowed Step

Record exact first proof parameters for the approved minimal implementation plan.

Do not write code.

Do not create database migrations.

Do not implement storage.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.
