# 20 - Transaction Boundaries

## Purpose

This document names Neon Ronin's Phase-6-relevant atomic operations before database design or implementation begins.

It exists to answer:

```text
Which state changes must succeed or fail together so Phase 6 does not fossilize ambiguous persistence behavior?
```

## Schema Status

```text
Phase 5D planning doctrine
```

This is not a database design.

This is not a migration plan.

This is not a choice of PostgreSQL, SQLite, ORM, API framework, queue, lock strategy, or storage layout.

## Core Rule

```text
Meaningful state change and its required audit trace succeed together or fail together.
```

A partial state change that loses its audit trail is not acceptable.

## Audit-First Transaction Rule

For operations that require audit:

```text
state change + audit record = one atomic unit
```

If the audit write fails inside that unit, the state change must roll back.

If the audit subsystem is unavailable before new consequential work begins, Neon Ronin must block the work.

Consequential work includes:

- workspace lifecycle changes
- workspace config changes
- review decisions
- human decisions
- artifact status changes
- signal sanitization decisions
- Observatory intake
- permission changes
- credential reference changes
- external action attempts
- emergency stop changes

## Named Atomic Operations

The following atomic operation names are planning names for future implementation and hammer testing.

### `workspace_config_create`

Creates a workspace config and its creation audit record.

Atomic writes:

- workspace config record
- creation audit record

Rollback rule:

- if audit creation fails, no workspace config is created

### `workspace_config_update`

Updates governed workspace config fields and records the change.

Atomic writes:

- workspace config update / revision
- audit record describing changed bounded fields

Rollback rule:

- if audit creation fails, the config update rolls back

### `workspace_status_transition`

Changes a workspace lifecycle status through an allowed transition.

Atomic writes:

- workspace status update
- human decision if required
- audit record

Rollback rule:

- invalid transition or audit failure leaves prior status intact

### `business_intake_classification_update`

Records intake classification, verdict, parking, rejection, or approval-for-onboarding state.

Atomic writes:

- business intake status/verdict update
- audit record

Rollback rule:

- if the update cannot be audited, intake state remains unchanged

### `business_intake_convert_to_workspace`

Converts an approved intake into a workspace config.

Atomic writes:

- business intake status update to `converted_to_workspace`
- workspace config creation
- source relationship/reference
- audit record or records

Rollback rule:

- if any required write fails, no partial workspace conversion remains

### `agent_run_start`

Creates or starts an agent run under lifecycle, runtime, permission, and audit checks.

Atomic writes:

- agent run status change to `started` or `running`
- audit record

Rollback rule:

- if audit creation fails, the run must not start

### `agent_run_finish`

Completes, blocks, fails, cancels, expires, or skips an agent run.

Atomic writes:

- agent run terminal or waiting status update
- output references if produced
- audit record or records

Rollback rule:

- result status and output references must not diverge from audit trail

### `artifact_metadata_create`

Creates artifact metadata without claiming ownership of artifact content.

Atomic writes:

- artifact metadata record
- audit record

Rollback rule:

- if audit creation fails, artifact metadata creation rolls back

### `artifact_status_transition`

Changes artifact status, such as draft to review, approved, rejected, delivery-ready, delivered, published, archived, or retired.

Atomic writes:

- artifact status update
- required human decision if applicable
- audit record

Rollback rule:

- no artifact may become delivery-ready, delivered, or published without its required decision and audit trail

### `review_item_create`

Creates a review item as a gate, not approval.

Atomic writes:

- review item record
- audit record

Rollback rule:

- if audit creation fails, review item creation rolls back

### `review_decision_record`

Records a human review decision and updates the review item accordingly.

Atomic writes:

- human decision record or embedded P0 decision shape
- review item status update
- audit record
- bounded target status update if the decision immediately changes one

Rollback rule:

- decision, review status, target status, and audit trail must not diverge

### `signal_candidate_create`

Creates a signal candidate from raw/source material.

Atomic writes:

- signal candidate record
- source references
- audit record
- review item if immediately routed to sanitization review

Rollback rule:

- candidate and review/audit references must not partially exist

### `signal_sanitization_decision`

Records the human sanitization decision for a signal candidate.

Atomic writes:

- human decision record or embedded P0 decision shape
- signal status update
- review item status update
- audit record

Rollback rule:

- a signal cannot become approved, rejected, or parked without the matching decision and audit trace

### `observatory_sanitized_signal_intake`

Submits an approved sanitized signal to the Observatory inbox.

Atomic writes:

- sanitized signal status update
- Observatory inbox/intake record or reference
- audit record

Rollback rule:

- if Observatory intake or audit fails, the signal must not appear as submitted

### `permission_scope_change`

Creates, activates, changes, pauses, revokes, expires, or retires a permission scope.

Atomic writes:

- permission scope change
- human decision when required
- audit record

Rollback rule:

- no permission expansion may exist without its required decision and audit trail

### `emergency_stop_change`

Triggers, escalates, narrows, resolves, or lifts emergency stop posture.

Atomic writes:

- emergency stop state/record
- affected workspace/integration/agent/runtime status changes if applicable
- human decision when lifting or narrowing stop
- audit record

Rollback rule:

- safety stop state and audit trail must not diverge

## Deferred But Named Future Operations

These operations are named for future consistency but remain deferred until the roadmap promotes them:

- `external_action_request`
- `external_action_attempt`
- `credential_reference_change`
- `scheduled_job_create`
- `watch_mode_event_intake`
- `provider_payload_snapshot_store`

Naming them does not authorize implementation.

## Transaction Failure Posture

When an atomic operation fails mid-operation:

1. Roll back all writes in the atomic unit when possible.
2. Do not leave partial state masquerading as success.
3. Preserve a safe failed-attempt audit record only if the operation explicitly models out-of-transaction attempt logging.
4. Return or record a precise failure status.
5. Require human review before retrying consequential work if outcome is unknown.

## Relationship To Hammer Testing

Future hammer tests must verify that these atomic operation boundaries are real.

Required future hammer probes include:

- failed audit write rolls back state change
- invalid status transition leaves prior status intact
- review decision and target status cannot diverge
- approved sanitized signal cannot appear in Observatory without decision and audit
- permission expansion cannot exist without human decision and audit
- emergency stop cannot be lifted without human decision and audit

## Non-Goals

This document does not define:

- database engine
- transaction isolation level
- lock strategy
- idempotency implementation
- ORM or query layer
- migration format
- table layout
- API route design
- queue implementation

## Final Rule

```text
No consequential state without its trace.
```
