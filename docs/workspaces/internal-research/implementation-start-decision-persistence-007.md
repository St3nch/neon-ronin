# Internal Research Implementation Start Decision - Persistence Proof 007

## Status

```text
approved
```

This document authorizes the next roadmap-aligned implementation slice: `workflow_record_create`.

It exists because this slice adds one new persistence boundary and one new table. It is not a broad planning document.

## Decision

```text
Approve implementation start for `workflow_record_create`, limited to creating bounded workflow definition records with audit-first transaction behavior.
```

## Why This Slice Is Next

Phase 6 has now proven workspace config create/update, review queue create/resolve with human authority, signal candidate creation, and metadata-only artifact creation.

The next manual-workflow proof should let Neon Ronin describe repeatable controlled work without introducing a workflow engine.

`workflow_record_create` is the smallest useful workflow boundary because it creates a workflow definition only. It does not start, execute, schedule, watch, run, automate, or advance workflow work.

## Authorized Scope

This decision authorizes only:

- `workflow_record_create`
- one new table: `workflow_records`
- audit-first transaction behavior for workflow record creation
- bounded validation for the first executable workflow definition shape
- hammer coverage for success, validation rejection, missing workspace, and forced audit-write rollback

## Authorized Tables

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
artifact_metadata
workflow_records
```

No other tables are authorized.

## Transaction Boundary

```text
workflow_record_create
```

A successful create must write the workflow record and its audit record in the same transaction.

Required invariant:

```text
no audit record means no workflow record
```

## Initial Allowed Workflow Record Shape

The first executable shape must stay small and bounded:

- `workflow_name`
- `workflow_type`
- `scope_type`
- `workspace_id`
- `adapter_id`
- `allowed_workspace_types`
- `allowed_lifecycle_statuses`
- `allowed_runtime_modes`
- `steps`
- `required_review_gates`
- `expected_inputs`
- `expected_outputs`
- `audit_requirements`
- optional `description`
- optional `version_label`
- optional `trigger_types`
- optional `allowed_agents`
- optional `forbidden_actions`
- optional `handoff_rules`
- optional `failure_behavior`
- optional `provenance_requirements`
- optional `tags`

The persistence layer owns:

- `workflow_id`
- `status`
- `audit_record_id`
- `created_at`
- `updated_at`
- `schema_version`
- `record_revision`

## Required Initial Constraints

The first proof must:

- require workspace-scoped workflows to reference an existing workspace config
- require `status` to be system-owned as `manual_test`
- reject caller-supplied system-owned fields
- reject unknown fields
- reject forbidden unbounded `metadata` or `custom_data`
- reject unsupported workflow types
- reject unsupported scope types
- reject unsupported lifecycle statuses
- reject runtime modes other than `on_demand`
- reject scheduled, watch-mode, and external-event triggers
- reject non-empty `allowed_agents`
- reject workflow steps with agent or integration actors
- reject workflow steps with provider payload or private content fields
- write exactly one audit record for successful workflow record creation
- roll back workflow record creation if audit write fails

## Explicitly Not Authorized

This decision does not authorize:

- workflow run records
- workflow execution
- workflow engine behavior
- workflow status transitions
- scheduling
- watch mode
- external events
- agent enablement
- integration enablement
- runtime enablement
- UI
- local service
- HTTP API
- MCP tool surface
- customer-facing workspace onboarding
- SearchClarity onboarding
- automation

## Required Validation Command

Before commit, run:

```text
python tools/dev/check_first_proof.py
```

Expected result:

```text
Ran 72 or more tests
OK
```

The count should increase if workflow record coverage is added.
