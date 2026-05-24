# Audit Record Schema

## Purpose

This document defines the P0 audit record schema for Neon Ronin.

An audit record is the core-owned trace of meaningful system activity, state change, review decision, agent run, signal movement, permission change, runtime change, workspace lifecycle change, or external action attempt.

Audit records exist so humans, LLMs, agents, and future code can answer:

```text
What happened, when did it happen, who or what did it, what did it affect, what was the result, and what evidence links to it?
```

## Schema Status

```text
P0 planning schema
```

This is an implementation-facing planning document.

It is not yet a database migration, JSON Schema file, Pydantic model, TypeScript type, or API contract.

## Ownership Category

```text
Core-owned data
```

Audit records are core-owned because auditability is a platform responsibility.

Audit records may reference workspace-owned, Observatory-owned, integration-owned, or derived records, but audit records themselves are platform governance records.

## Core Rule

```text
Meaningful state changes must be auditable.
```

Rejected, failed, parked, blocked, cancelled, expired, or partially completed actions remain auditable.

## Audit Record Is Not A Payload Dump

An audit record should capture what happened and link to relevant records.

It should not become a dumping ground for private payloads, raw customer data, full external API responses, credentials, or arbitrary logs.

Use references, summaries, and bounded metadata.

## What Must Generate Audit Records

Audit records should be created for:

- workspace created
- workspace config changed
- workspace status changed
- workspace runtime mode changed
- workspace paused
- workspace resumed
- workspace retired
- agent run started
- agent run completed
- agent run failed
- review item created
- review status changed
- human decision recorded
- signal created
- signal candidate created
- signal sanitization decision made
- sanitized signal submitted to Observatory
- Observatory signal normalized
- Observatory query executed
- external API call attempted
- external draft created
- publish attempt
- paid action attempt
- destructive action attempt
- credential or permission change requested
- credential or permission change approved/rejected
- emergency stop triggered
- schema/config migration later

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `audit_record_id` | string | system-owned | Stable unique audit record id |
| `event_type` | enum | system-owned | Type of audited event |
| `workspace_id` | string/null | system/reference | Workspace scope if applicable |
| `actor_type` | enum | system/source-owned | Actor type that caused the event |
| `actor_id` | string | system/source-owned | Actor id that caused the event |
| `action_type` | enum/string | system-owned | Action performed or attempted |
| `target_type` | enum/string | system-owned/reference | Type of record/resource affected |
| `target_id` | string/null | system-owned/reference | Id of affected record/resource if applicable |
| `result_status` | enum | system-owned | Outcome of the event |
| `occurred_at` | datetime | system-owned | Event timestamp |
| `source_references` | array object | referenced-only | Records, runs, review items, signals, or external refs that explain the event |
| `summary` | string | system/source-owned | Human-readable event summary |
| `created_at` | datetime | system-owned | Audit record creation timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `correlation_id` | string/null | system-owned | Groups related records across a workflow/run/request |
| `request_id` | string/null | system-owned/integration-owned | Request id if event came from an API/CLI/provider call |
| `review_item_id` | string/null | referenced-only | Linked review item if applicable |
| `agent_run_id` | string/null | referenced-only | Linked agent run if applicable |
| `human_decision_id` | string/null | referenced-only | Linked human decision if applicable |
| `external_reference_id` | string/null | referenced-only/integration-owned | Linked external provider/resource reference |
| `previous_state` | object/null | bounded/system-owned | Previous state summary, not private payload dump |
| `new_state` | object/null | bounded/system-owned | New state summary, not private payload dump |
| `reason` | string/null | human/system-owned | Reason for change if provided |
| `error_code` | string/null | system-owned | Machine-readable error code if failed/blocked |
| `error_summary` | string/null | system-owned | Human-readable error summary without private payload dump |
| `sensitivity_rating` | enum | system/source-owned | Sensitivity rating for the audit event |
| `provenance_level` | enum | system-owned | Raw/structured/sanitized/normalized/derived/decision/event posture |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Event Types

Initial canonical event types:

```text
workspace_created
workspace_config_updated
workspace_status_changed
workspace_runtime_mode_changed
workspace_paused
workspace_resumed
workspace_retired
agent_run_started
agent_run_completed
agent_run_failed
review_item_created
review_item_status_changed
human_decision_recorded
signal_raw_created
signal_candidate_created
signal_sanitization_decided
sanitized_signal_submitted
observatory_signal_normalized
observatory_query_executed
external_api_call_attempted
external_draft_created
external_write_requested
publish_attempted
paid_action_attempted
destructive_action_attempted
credential_change_requested
credential_change_decided
permission_change_requested
permission_change_decided
emergency_stop_triggered
validation_failed
schema_or_config_migration
```

Event types may expand later through schema authority.

Do not create provider-specific event types in core if a generic event type plus external reference is sufficient.

## Actor Types

Canonical actor types:

```text
human
agent
system
integration
external_provider
scheduled_job
imported_file
unknown
```

Actor id should be specific enough to support review and debugging.

Examples:

```text
human:operator
agent:signal_capture_agent
system:workspace_lifecycle_manager
integration:etsy
external_provider:anthropic
```

## Result Statuses

Canonical result statuses:

```text
started
succeeded
failed
blocked
rejected
approved
approved_with_changes
revision_requested
escalated
parked
cancelled
expired
skipped
unknown
```

A failed or blocked event is still an audit event.

## Target Types

Initial target types:

```text
workspace_config
workspace_status
runtime_mode
agent_run
review_item
human_decision
artifact
signal
signal_candidate
sanitized_signal
observatory_record
observatory_query
permission_scope
external_reference
external_provider_resource
credential_reference
workflow
schema
system
```

Target type should describe the affected record or resource without forcing provider-specific schemas into core.

## Source References

`source_references` is an array of thin references, not ownership transfer.

Example:

```yaml
source_references:
  - record_type: review_item
    record_id: rev_001
    relationship: decision_source
  - record_type: agent_run
    record_id: run_001
    relationship: generated_output
```

Source references should preserve provenance while avoiding private payload copies.

## Previous And New State Objects

`previous_state` and `new_state` may be useful for lifecycle or config changes.

They must be bounded summaries.

Allowed examples:

```yaml
previous_state:
  status: manual_test
new_state:
  status: active
```

Forbidden examples:

```yaml
previous_state:
  full_customer_record: ...
new_state:
  provider_token: ...
```

State snapshots must not store credentials, raw customer data, private artifact content, or full provider payloads.

## System-Owned Fields

The following fields should be system-owned:

- `audit_record_id`
- `event_type`
- `occurred_at`
- `created_at`
- `result_status`
- `correlation_id`
- system-generated request ids
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Audit records should be append-friendly and effectively immutable after creation.

Immutable fields should include:

- `audit_record_id`
- `event_type`
- `workspace_id`
- `actor_type`
- `actor_id`
- `action_type`
- `target_type`
- `target_id`
- `occurred_at`
- `created_at`
- `source_references`

If an audit record needs correction, create a correction/superseding audit record rather than rewriting history.

## Provenance Requirements

An audit record must preserve enough provenance to answer:

- what happened?
- when did it happen?
- who or what caused it?
- what workspace was involved?
- what target was affected?
- what source records explain it?
- what was the result?
- what review item or human decision authorized it, if applicable?
- what error or blocker occurred, if applicable?

## Audit Relationships

Audit records may be referenced by:

- workspace config changes
- workspace lifecycle changes
- agent runs
- review queue items
- human decisions
- signal lifecycle events
- Observatory ingestion and query events
- external integration events
- permission changes
- emergency stop events

Audit records should be linkable from the records they describe.

## Lifecycle Rules

Audit records must be created regardless of workspace lifecycle status when meaningful state changes or blocked attempts occur.

Examples:

- If a paused workspace blocks a new run, create an audit record for the blocked attempt.
- If a retired workspace rejects a new review item, create an audit record for the rejection/block.
- If emergency stop blocks external action, create an audit record.

## External Action Audit Rules

External action audit records must include:

- workspace id
- actor id
- action type
- provider or external reference if applicable
- review item id if approval was required
- result status
- error code/summary if failed
- request id if available

They must not include:

- raw credentials
- OAuth tokens
- full customer-private payloads
- full provider responses unless bounded and allowed by a future integration schema

## Review Decision Audit Rules

Review decision audit records must include:

- review item id
- reviewer actor id
- decision type
- decision timestamp
- target record references
- result status
- decision summary or reason

No agent may create an audit record claiming to be a human approval.

## Signal And Observatory Audit Rules

Signal-related audit records must link the lifecycle:

```text
raw signal
-> signal candidate
-> sanitization review decision
-> sanitized signal submission
-> Observatory normalization
-> Observatory query result
```

Normal Observatory audit records must not expose private source details through query surfaces.

Internal audit references may preserve restricted provenance for debugging and governance.

## Error And Validation Audit Rules

Validation failures should be auditable when they matter.

Examples:

- invalid lifecycle transition attempted
- review gate bypass attempted
- workspace tried to query Observatory without permission
- signal submitted without sanitization approval
- external write attempted from manual_test workspace
- unknown field rejected during future schema validation

These events should use `validation_failed` or a more specific future event type.

## Sensitivity Ratings

Initial sensitivity ratings:

```text
low
medium
high
restricted
unknown
```

High or restricted audit records may require limited visibility in future UI/API layers.

Sensitivity does not remove auditability.

## Provenance Levels

Initial provenance levels:

```text
raw
structured
sanitized
normalized
derived
decision
event
unknown
```

Most audit records are `event` records, but they may reference records at other provenance levels.

## Forbidden Fields

Do not add fields such as:

```text
raw_customer_email
raw_customer_phone
full_customer_request
private_report_text
provider_token
api_key
oauth_refresh_token
full_external_payload
full_provider_response
searchclarity_report_text
etsy_listing_payload
printify_product_payload
custom_data
```

Use bounded summaries and references instead.

## Bounded Metadata

A future bounded metadata field may exist only if it defines:

- allowed keys
- allowed value types
- owner
- whether it is queryable
- whether it is canonical meaning
- what must not be stored there

Until then, avoid generic `metadata` or `custom_data` fields.

## Example Record

```yaml
audit_record_id: audit_001
event_type: review_item_created
workspace_id: ws_internal_research_001
actor_type: agent
actor_id: signal_capture_agent
action_type: create_review_item
target_type: review_item
target_id: rev_001
result_status: succeeded
occurred_at: 2026-05-24T00:00:00Z
source_references:
  - record_type: agent_run
    record_id: run_001
    relationship: source_run
  - record_type: signal_candidate
    record_id: sigcand_001
    relationship: review_subject
summary: Signal capture agent created a review item for sanitized signal candidate approval.
correlation_id: corr_001
request_id: null
review_item_id: rev_001
agent_run_id: run_001
human_decision_id: null
external_reference_id: null
previous_state: null
new_state:
  review_item_status: open
reason: Human review required before Observatory intake.
error_code: null
error_summary: null
sensitivity_rating: medium
provenance_level: event
created_at: 2026-05-24T00:00:00Z
version: 1
```

## Validation Questions

Before accepting an audit record, answer:

1. Is the event type valid?
2. Is the actor traceable?
3. Is the target type clear?
4. Is the result status valid?
5. Is the workspace id present when workspace-scoped?
6. Are source references thin references rather than ownership transfers?
7. Does the record avoid private payload dumps?
8. Does the record avoid credentials and raw secrets?
9. Does the record preserve enough context for future review?
10. Does the event need a linked review item or human decision?
11. Does it avoid provider-specific fields in core?
12. If it failed or was blocked, is that result explicit?

## Non-Goals

This schema does not define:

- full log storage architecture
- database indexing
- full external provider payload storage
- credential storage
- customer history records
- UI audit timeline design
- retention policy
- export/import format
- human decision schema details
- agent run schema details

## Final Rule

```text
If Neon Ronin changes meaningful state, Neon Ronin leaves a trace.
```
