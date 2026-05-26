# Internal Research Implementation Start Decision - Persistence Proof 005

## Status

```text
approved
```

This document authorizes the next roadmap-aligned implementation slice: `signal_candidate_create`.

It exists because this slice adds one new persistence boundary and one new table. It is not a broad planning document.

## Decision

```text
Approve implementation start for `signal_candidate_create`, limited to creating workspace-owned signal candidate records with audit-first transaction behavior.
```

## Why This Slice Is Next

Phase 6 has now proven workspace config create/update and review queue create/resolve with human authority.

The next manual-workflow proof should exercise signal intake without crossing into Observatory ingestion.

`signal_candidate_create` is the smallest useful signal boundary because it creates a workspace-owned candidate only. It does not create sanitized signals, submit anything to the Observatory, normalize records, generate derived intelligence, or automate review.

## Authorized Scope

This decision authorizes only:

- `signal_candidate_create`
- one new table: `signal_candidates`
- audit-first transaction behavior for signal candidate creation
- bounded validation for the first executable signal candidate shape
- hammer coverage for success, validation rejection, missing workspace, and forced audit-write rollback

## Authorized Tables

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
```

No other tables are authorized.

## Transaction Boundary

```text
signal_candidate_create
```

A successful create must write the signal candidate and its audit record in the same transaction.

Required invariant:

```text
no audit record means no signal candidate record
```

## Initial Allowed Signal Candidate Shape

The first executable shape must stay small and bounded:

- `workspace_id`
- `workspace_type`
- `signal_type`
- `source_actor_type`
- `source_actor_id`
- `source_references`
- `summary`
- `evidence_summary`
- `sensitivity_rating`
- `confidence`
- `private_data_removed`
- `remaining_sensitivity_notes`
- optional `parent_signal_id`
- optional `raw_signal_id`
- optional `tags`

The persistence layer owns:

- `signal_id`
- `signal_form`
- `status`
- `audit_record_id`
- `created_at`
- `updated_at`
- `schema_version`
- `record_revision`

## Required Initial Constraints

The first proof must:

- require the workspace config to already exist
- require `signal_form` to be system-owned as `signal_candidate`
- require `status` to be system-owned as `candidate`
- require `private_data_removed` to be `true`
- reject caller-supplied system-owned fields
- reject unknown fields
- reject forbidden unbounded `metadata` or `custom_data`
- reject unsupported signal types
- reject unsupported source actor types
- reject unsupported source reference record types
- reject high, restricted, or unknown sensitivity for this first low-risk candidate proof
- write exactly one audit record for successful signal candidate creation
- roll back the signal candidate if audit write fails

## Explicitly Not Authorized

This decision does not authorize:

- raw signal persistence
- sanitized signal persistence
- signal status transitions
- sanitization review creation
- Observatory submission
- Observatory inbox
- Observatory normalization
- derived intelligence
- live Observatory ingestion
- external action execution
- artifact persistence
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
Ran 47 or more tests
OK
```

The count should increase if signal candidate coverage is added.
