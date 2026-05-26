# Internal Research Implementation Start Decision - Persistence Proof 004

## Status

```text
approved
```

This document authorizes the next roadmap-aligned implementation slice: `human_decision_record` resolving an existing review queue item.

It exists because this slice adds one new persistence boundary and one new table. It is not a broad planning document.

## Decision

```text
Approve implementation start for `human_decision_record`, limited to recording a bounded human decision that resolves one existing review queue item with audit-first transaction behavior.
```

## Why This Slice Is Next

Phase 6 requires Internal Research to prove that a review queue item can be created and resolved.

The previous proof created review queue items. The next smallest useful boundary is recording the human decision that resolves an existing review item.

## Authorized Scope

This decision authorizes only:

- `human_decision_record`
- one new table: `human_decisions`
- update of the existing `review_queue_items` record status as part of the same transaction
- audit-first transaction behavior for decision recording and review item resolution
- bounded validation for the first executable human decision shape
- hammer coverage for success, validation rejection, missing review item, already-resolved review item, non-human reviewer rejection, and forced audit-write rollback

## Authorized Tables

```text
workspace_configs
audit_records
review_queue_items
human_decisions
```

No other tables are authorized.

## Transaction Boundary

```text
human_decision_record
```

A successful decision record must write the human decision, update the review item, and write the corresponding audit record in the same transaction.

Required invariant:

```text
no audit record means no human decision record and no review item resolution
```

## Initial Allowed Decision Shape

The first executable shape must stay small and bounded:

- `review_item_id`
- `decision_type`
- `decision_scope`
- `reviewer_actor_id`
- `target_records`
- `decision_summary`
- optional `decision_notes`
- optional `conditions`
- optional `revision_instructions`
- optional `park_reason`
- optional `block_reason`
- optional `sensitivity_rating`

The persistence layer owns:

- `human_decision_id`
- `workspace_id`
- `decision_status`
- `audit_record_id`
- `decided_at`
- `created_at`
- `updated_at`
- `schema_version`
- `record_revision`

## Required Initial Constraints

The first proof must:

- require the review item to already exist
- require reviewer actor ids to start with `human:`
- reject caller-supplied system-owned fields
- reject unknown fields
- reject forbidden unbounded `metadata` or `custom_data`
- reject unsupported decision types
- reject unsupported decision scopes
- reject invalid target record types
- reject decisions for already-resolved review items
- update the review item status according to the decision
- store the decision on the review item as a bounded object/reference
- write exactly one audit record for successful decision recording
- roll back the human decision and review item status update if audit write fails

## Explicitly Not Authorized

This decision does not authorize:

- external action execution
- artifact delivery
- signal ingestion
- workspace promotion transition engine
- permission grants
- agent enablement
- runtime enablement
- UI
- local service
- HTTP API
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

Expected result:

```text
Ran 35 or more tests
OK
```

The count should increase if human decision coverage is added.
