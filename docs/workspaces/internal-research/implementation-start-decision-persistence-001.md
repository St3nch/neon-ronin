# Internal Research Implementation Start Decision - Persistence Proof 001

## Status

```text
approved
```

This document records the implementation-start decision for the first local persistence proof.

It authorizes the first tiny executable Neon Ronin implementation slice under strict scope controls.

It does not authorize a full database architecture.

It does not authorize UI work, agents, integrations, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Decision Metadata

```yaml
implementation_start_decision_id: decision_internal_research_implementation_start_persistence_001
implementation_plan_id: impl_plan_internal_research_persistence_001
first_proof_parameter_record_id: first_proof_params_internal_research_persistence_001
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_decision_time: manual_test
decision_type: approve_with_changes
decision_status: recorded
created_at: 2026-05-26T00:00:00Z
updated_at: 2026-05-26T00:00:00Z
schema_version: implementation_start_decision_v1
record_revision: 1
```

## Decision

```text
Approve implementation start for the first local persistence proof, limited to SQLite-backed workspace config and audit record persistence through workspace_config_create plus one audit-first hammer proof.
```

## Confirmed First Proof Parameters

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

## Authorized Implementation Scope

This decision authorizes implementation of only the following:

- local SQLite-backed persistence proof
- direct service/module call surface
- minimal `workspace_configs` persistence shape
- minimal `audit_records` persistence shape
- `workspace_config_create` transaction behavior
- audit-first write behavior for the create path
- fixture extracted from `docs/workspaces/internal-research/workspace-config.draft.md`
- hammer proof named `hammer-audit-first-workspace-config-create`

## Required Invariant

```text
no audit record means no workspace config record
```

The first proof must demonstrate that workspace config creation and creation audit recording succeed or fail together.

## Required Positive Case

A valid first-proof create operation must produce:

- exactly one workspace config record
- exactly one creation audit record
- deterministic success result
- no extra hidden records
- no provider payloads
- no unbounded metadata
- no executable agent/run records

## Required Negative Case

A forced audit-write failure must produce:

- no durable workspace config record
- no partial success result
- deterministic failure result
- clean retry posture

## Required Hammer Checks

The first hammer proof must verify:

1. valid workspace config creation creates exactly one workspace config and one audit record
2. forced audit creation failure blocks or rolls back workspace config creation
3. no partial workspace config remains after failure
4. caller cannot forge system-owned fields
5. unknown fields are rejected
6. forbidden fields such as unbounded `metadata` or `custom_data` are rejected
7. timestamps are UTC ISO 8601 with `Z` suffix
8. `schema_version` and `record_revision` are present and correctly owned
9. result is deterministic and not mock-only

## Implementation Constraints

- Keep the implementation local-only.
- Prefer the smallest direct module/service shape that proves the invariant.
- Do not introduce an HTTP API.
- Do not introduce a CLI contract unless necessary for the hammer proof.
- Do not introduce MCP tools.
- Do not introduce an agent-accessible surface.
- Do not create production database architecture.
- Do not create broad migrations beyond what the first proof requires.
- Do not add tables/entities outside `workspace_configs` and `audit_records`.
- Do not implement human-decision persistence in this slice.
- Do not implement signal persistence in this slice.
- Do not implement review queue persistence in this slice.
- Do not implement artifact persistence in this slice.

## Still Forbidden

This decision does not authorize:

- UI work
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
- external writes
- marketplace actions
- customer delivery
- paid actions
- credential handling
- service-business adapter implementation
- order records
- consent records
- local schema reference creation
- core schema promotion from local packet shapes
- provider payload snapshots

## Authoritative Inputs

| Area | Authoritative Doc |
|---|---|
| schema authority | `docs/core/14-schema-authority.md` |
| workspace config schema | `docs/core/schemas/workspace-config.schema.md` |
| audit record schema | `docs/core/schemas/audit-record.schema.md` |
| transaction boundary | `docs/core/20-transaction-boundaries.md` |
| audit/error behavior | `docs/core/16-error-and-failure-handling.md` |
| permissions/audit doctrine | `docs/core/07-permissions-and-audit.md` |
| hammer doctrine | `docs/core/19-hammer-testing-doctrine.md` |
| implementation plan | `docs/workspaces/internal-research/minimal-implementation-plan-persistence-001.md` |
| proof parameters | `docs/workspaces/internal-research/first-proof-parameters-persistence-001.md` |

If implementation reveals a conflict between these docs, stop and resolve the doctrine conflict before continuing.

## Human Gate Meaning

This decision is the meaningful human gate for implementation start.

The human-in-loop product rule remains focused on preventing future agents and automation from self-approving consequential work.

This implementation-start decision does not imply that every low-risk planning refinement requires a canonical human-decision record.

## Next Allowed Step

Begin the first local persistence proof implementation in the narrow scope above.

Allowed next implementation work:

```text
create the smallest local SQLite-backed module/service needed to prove workspace_config_create creates or rolls back workspace config and audit records together
```

Do not expand scope without a new decision.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.