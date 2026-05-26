# Internal Research Implementation Start Decision - Persistence Proof 006

## Status

```text
approved
```

This document authorizes the next roadmap-aligned implementation slice: `artifact_metadata_create`.

It exists because this slice adds one new persistence boundary and one new table. It is not a broad planning document.

## Decision

```text
Approve implementation start for `artifact_metadata_create`, limited to creating bounded artifact metadata records with audit-first transaction behavior.
```

## Why This Slice Is Next

Phase 6 has now proven workspace config create/update, review queue create/resolve with human authority, and workspace-owned signal candidate creation.

The next manual-workflow proof should let Neon Ronin track produced or referenced outputs without storing private content in core.

`artifact_metadata_create` is the smallest useful artifact boundary because it creates metadata only. It does not store artifact content, blobs, generated files, customer deliverables, public publishing state, or external delivery actions.

## Authorized Scope

This decision authorizes only:

- `artifact_metadata_create`
- one new table: `artifact_metadata`
- audit-first transaction behavior for artifact metadata creation
- bounded validation for the first executable artifact metadata shape
- hammer coverage for success, validation rejection, missing workspace, and forced audit-write rollback

## Authorized Tables

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
artifact_metadata
```

No other tables are authorized.

## Transaction Boundary

```text
artifact_metadata_create
```

A successful create must write the artifact metadata and its audit record in the same transaction.

Required invariant:

```text
no audit record means no artifact metadata record
```

## Initial Allowed Artifact Metadata Shape

The first executable shape must stay small and bounded:

- `workspace_id`
- `artifact_type`
- `content_scope`
- `storage_reference`
- `title`
- `summary`
- `creator_actor_type`
- `creator_actor_id`
- `source_references`
- optional `workflow_id`
- optional `agent_run_id`
- optional `review_item_ids`
- optional `human_decision_ids`
- optional `parent_artifact_id`
- optional `version_label`
- optional `content_format`
- optional `file_hash`
- optional `sensitivity_rating`
- optional `confidence`
- optional `delivery_ready`
- optional `public_use_allowed`
- optional `tags`

The persistence layer owns:

- `artifact_id`
- `status`
- `audit_record_ids`
- `created_at`
- `updated_at`
- `schema_version`
- `record_revision`

## Required Initial Constraints

The first proof must:

- require the workspace config to already exist
- require `status` to be system-owned as `draft`
- require `audit_record_ids` to be system-owned
- require `storage_reference.content_stored_in_core` to be `false`
- reject caller-supplied system-owned fields
- reject unknown fields
- reject forbidden unbounded `metadata` or `custom_data`
- reject unsupported artifact types
- reject unsupported content scopes
- reject unsupported creator actor types
- reject unsupported source reference record types
- reject storage references containing credentials or private payload bodies
- write exactly one audit record for successful artifact metadata creation
- roll back artifact metadata if audit write fails

## Explicitly Not Authorized

This decision does not authorize:

- artifact content storage
- blob storage
- generated file creation
- artifact status transitions
- review submission
- delivery-ready marking
- delivery or publishing
- public-use approval
- external action execution
- workflow persistence
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
Ran 59 or more tests
OK
```

The count should increase if artifact metadata coverage is added.
