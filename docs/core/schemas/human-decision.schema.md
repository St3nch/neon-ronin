# Human Decision Schema

## Purpose

This document defines the P1 human decision schema for Neon Ronin.

A human decision is a recorded operator judgment that approves, rejects, revises, escalates, parks, blocks, cancels, or otherwise governs a review item, workflow step, artifact, signal candidate, permission change, workspace lifecycle transition, or external action request.

Human decision records exist so Neon Ronin can preserve human authority, review provenance, and auditability.

## Schema Status

```text
P1 planning schema
```

This is an implementation-facing planning document.

It is not yet a database migration, JSON Schema file, Pydantic model, TypeScript type, or API contract.

## Ownership Category

```text
Core-owned data
```

Human decisions are platform governance records.

A human decision may reference workspace-owned artifacts, workspace-owned signal candidates, core-owned review items, integration-owned external references, or Observatory-owned records, but the decision record itself is core-owned.

## Core Rule

```text
Human decisions record authority.
They do not erase provenance or bypass future gates.
```

A human decision should authorize only the specific bounded next step it names.

A human decision is not permanent broad permission unless a future permission schema explicitly grants and audits that scope.

## What Requires A Human Decision

Human decisions are required for:

- customer-facing delivery approval
- public publishing approval
- paid action approval
- destructive action approval
- credential or permission change approval
- signal sanitization approval
- workspace promotion approval
- privacy-sensitive output approval
- rights/IP/compliance-sensitive output approval
- external write approval
- override or escalation decisions

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `human_decision_id` | string | system-owned | Stable unique decision id |
| `workspace_id` | string/null | system/reference | Workspace scope if applicable |
| `review_item_id` | string/null | referenced-only | Review item this decision resolves or updates |
| `decision_type` | enum | human/system-owned | Decision made |
| `decision_status` | enum | system-governed | Current decision record status |
| `decision_scope` | enum | human/system-owned | Scope of what the decision applies to |
| `reviewer_actor_id` | string | human/system-owned | Human actor who made the decision |
| `target_records` | array object | referenced-only | Records affected or reviewed |
| `decision_summary` | string | human-owned | Short human-readable decision summary |
| `decided_at` | datetime | system-owned | Decision timestamp |
| `audit_record_id` | string | system/reference | Audit record for this decision |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `decision_notes` | string/null | human-owned | Additional decision rationale or notes |
| `conditions` | array string | human-owned | Conditions required for approval to remain valid |
| `changed_fields` | array object | human/system-owned | Fields changed as part of approval-with-changes |
| `revision_instructions` | string/null | human-owned | Instructions if revision was requested |
| `escalation_reason` | string/null | human-owned | Reason for escalation |
| `park_reason` | string/null | human-owned | Reason item was parked |
| `block_reason` | string/null | human/system-owned | Reason item was blocked |
| `expires_at` | datetime/null | human/system-owned | Expiration for bounded approval if applicable |
| `supersedes_decision_id` | string/null | referenced-only | Prior decision superseded by this decision |
| `sensitivity_rating` | enum | human/system-owned | Sensitivity/privacy rating |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Decision Types

Canonical decision types:

```text
approve
approve_with_changes
reject
request_revision
escalate
park
block
cancel
resume
promote
retire
override
```

`override` should be rare, strongly audited, and narrowly scoped.

## Valid Decision Statuses

Canonical decision statuses:

```text
recorded
superseded
expired
revoked
invalidated
```

A decision should usually be immutable after recording.

If a decision changes, create a new decision that supersedes the old one rather than rewriting history.

## Decision Scopes

Canonical decision scopes:

```text
review_item
artifact
signal_candidate
sanitized_signal
workspace_lifecycle
workflow_step
external_action
permission_change
credential_change
publish_action
customer_delivery
paid_action
destructive_action
other
```

Decision scope defines what the decision applies to.

It must not be broader than necessary.

## Target Records

`target_records` is an array of thin references, not ownership transfer.

Allowed target record types:

```text
review_item
artifact
signal_candidate
sanitized_signal
workspace_config
workflow
agent_run
permission_scope
external_reference
audit_record
business_intake
```

Example:

```yaml
target_records:
  - record_type: review_item
    record_id: rev_001
    relationship: resolves_review
  - record_type: artifact
    record_id: art_001
    relationship: reviewed_output
```

## Changed Fields Object

For `approve_with_changes`, changed fields should be explicit.

Recommended shape:

```yaml
changed_fields:
  - record_type: artifact
    record_id: art_001
    field_name: delivery_ready
    previous_value: false
    new_value: true
```

Changed fields should not contain raw private payloads, credentials, or full provider responses.

## System-Owned Fields

System-owned fields should include:

- `human_decision_id`
- `decision_status`
- `decided_at`
- `created_at`
- `updated_at`
- `audit_record_id`
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation:

- `human_decision_id`
- `workspace_id`
- `review_item_id`
- `decision_type`
- `decision_scope`
- `reviewer_actor_id`
- `target_records`
- `decided_at`
- `created_at`

If correction is needed, create a new superseding decision and audit record.

## Provenance Requirements

A human decision must preserve:

- who made the decision
- when the decision was made
- what was reviewed
- what records were affected
- what review item triggered the decision if any
- what conditions or changes apply
- what audit record traces the decision
- whether the decision supersedes a prior decision

## Audit Requirements

The following events must generate audit records:

- human decision recorded
- decision superseded
- decision expired
- decision revoked
- decision invalidated
- approval with changes applied
- override decision recorded
- workspace promotion/retirement decision recorded
- permission/credential decision recorded

## Relationship To Review Queue

A human decision often resolves a review queue item.

Review item status should update according to the human decision, but the decision record should remain a separate authority record once this schema exists.

Review item creation is not approval.

Human decision recording is the approval/rejection/parking/escalation authority.

## Relationship To Permissions

A human decision may authorize a bounded next step.

It does not automatically create permanent permission.

If the decision changes permission scope, a permission-scope record or future permission event must represent that scope explicitly and auditably.

## Lifecycle Rules

Human decisions must obey workspace lifecycle and runtime limits.

Examples:

- a decision may approve a draft artifact but not deliver it if the workspace is paused
- a decision may approve signal sanitization but not submit if workspace permissions disallow Observatory submission
- a decision may promote a workspace only through allowed lifecycle transitions
- a decision cannot revive a retired workspace unless a future ADR defines controlled reactivation

## External Action Rules

Human decisions approving external actions must be specific and bounded.

They should identify:

- target action
- target record or external reference
- conditions
- expiration if needed
- review item id
- audit record id

They must not grant broad permanent external write authority by accident.

## Signal Decision Rules

For signal sanitization decisions:

- target record should include a signal candidate
- decision scope should be `signal_candidate` or `sanitized_signal`
- approval authorizes only the sanitized version under review
- rejection blocks Observatory intake
- parking holds without intake
- revision requires candidate update and resubmission

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
business_specific_report_text
etsy_listing_payload
printify_product_payload
fiverr_message_text
custom_data
```

Use target references, bounded notes, and workspace-owned artifacts instead.

## Example Record

```yaml
human_decision_id: hdec_001
workspace_id: ws_internal_research_001
review_item_id: rev_001
decision_type: approve
decision_status: recorded
decision_scope: signal_candidate
reviewer_actor_id: human_operator
target_records:
  - record_type: review_item
    record_id: rev_001
    relationship: resolves_review
  - record_type: signal_candidate
    record_id: sigcand_001
    relationship: approved_signal_candidate
decision_summary: Approved sanitized signal candidate for Observatory intake.
decided_at: 2026-05-24T00:00:00Z
audit_record_id: audit_001
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
decision_notes: Candidate contains no customer data, credentials, or workspace-private details.
conditions:
  - Submit only the reviewed sanitized signal text.
changed_fields: []
revision_instructions: null
escalation_reason: null
park_reason: null
block_reason: null
expires_at: null
supersedes_decision_id: null
sensitivity_rating: low
version: 1
```

## Validation Questions

Before accepting a human decision record, answer:

1. Is the reviewer a human actor?
2. Is the decision type valid?
3. Is the decision scope bounded?
4. Are target records explicit references?
5. Is the related review item linked where applicable?
6. Does the decision avoid raw private payloads?
7. Does the decision avoid credentials and provider payloads?
8. Are conditions explicit for approvals?
9. If approval changes state, are changed fields explicit?
10. Is an audit record linked?
11. Does the decision obey workspace lifecycle and runtime constraints?
12. Does it avoid creating permanent broad permission by accident?

## Non-Goals

This schema does not define:

- user identity management
- authentication
- full permission model
- UI review screens
- external action execution
- artifact content
- customer records
- database tables

## Final Rule

```text
Human decision is authority, but only within its recorded scope.
```
