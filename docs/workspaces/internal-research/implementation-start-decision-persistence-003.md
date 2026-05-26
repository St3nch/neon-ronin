# Internal Research Implementation Start Decision - Persistence Proof 003

## Status

```text
approved
```

This document authorizes the next roadmap-aligned implementation slice: `review_queue_item_create`.

It exists because this slice adds one new persistence boundary and one new table. It is not a broad planning document.

## Decision

```text
Approve implementation start for `review_queue_item_create`, limited to creating bounded review queue item records with audit-first transaction behavior.
```

## Why This Slice Is Next

Phase 6 requires Internal Research to prove that a review queue item can be created and later resolved.

The previous persistence proofs covered workspace config create and update. The next smallest roadmap-valid boundary is review item creation.

## Authorized Scope

This decision authorizes only:

- `review_queue_item_create`
- one new table: `review_queue_items`
- audit-first transaction behavior for review item creation
- bounded validation for the first executable review item shape
- hammer coverage for success, validation rejection, and forced audit-write rollback

## Authorized Tables

```text
workspace_configs
audit_records
review_queue_items
```

No other tables are authorized.

## Transaction Boundary

```text
review_queue_item_create
```

A successful create must write the review queue item and its audit record in the same transaction.

Required invariant:

```text
no audit record means no review queue item record
```

## Initial Allowed Review Shape

The first executable shape must stay small and bounded:

- `workspace_id`
- `review_type`
- `risk_categories`
- `source_actor_type`
- `source_actor_id`
- `title`
- `summary`
- `required_gates`
- `linked_records`
- optional `description`
- optional `priority`
- optional `sensitivity_rating`
- optional `confidence`

The persistence layer owns:

- `review_item_id`
- `status`
- `decision`
- `audit_record_id`
- `created_at`
- `updated_at`
- `schema_version`
- `record_revision`

## Required Initial Constraints

The first proof must:

- require the workspace config to already exist
- create review items with initial status `open`
- keep `decision` as null
- reject caller-supplied system-owned fields
- reject unknown fields
- reject forbidden unbounded `metadata` or `custom_data`
- reject unsupported review types
- reject unsupported risk categories
- reject unsupported required gates
- reject invalid linked record types
- write exactly one audit record for successful creation
- roll back the review item if audit write fails

## Explicitly Not Authorized

This decision does not authorize:

- review item resolution
- embedded decision recording
- human-decision persistence
- signal persistence
- artifact persistence
- lifecycle transition engine
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
Ran 23 or more tests
OK
```

The count should increase if review queue item create coverage is added.
