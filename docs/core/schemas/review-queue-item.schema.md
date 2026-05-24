# Review Queue Item Schema

## Purpose

This document defines the P0 review queue item schema for Neon Ronin.

A review queue item is the core-owned record that holds risky, important, public-facing, customer-facing, paid, destructive, credential-related, privacy-sensitive, compliance-sensitive, or Observatory-intake work until a human decision is made.

Review queue items are the primary mechanism that keeps agents helpful without letting them become final decision-makers.

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

Review queue mechanics are a reusable Neon Ronin platform capability.

A review item may reference workspace-owned artifacts, workspace-owned signal candidates, integration-owned external references, or Observatory-owned records, but the review item itself is a core-owned governance record.

## Core Rule

```text
A review queue item requests human judgment.
It does not execute the action by existing.
```

Creating a review item must not automatically publish, deliver, spend, delete, message, approve, or submit data to the Observatory.

## What Enters The Review Queue

Review items should be created for:

- customer-facing deliverables
- public content drafts
- marketplace listing drafts
- publish requests
- paid action requests
- destructive action requests
- credential or permission changes
- external write requests
- rights, IP, policy, or compliance concerns
- privacy-sensitive outputs
- signal sanitization approvals
- escalation packets
- active workspace promotion decisions
- material workflow changes

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `review_item_id` | string | system-owned | Stable unique review item id |
| `workspace_id` | string | system-owned/reference | Workspace this item belongs to |
| `review_type` | enum | source/system-owned | Type of review being requested |
| `status` | enum | system-governed | Current review item status |
| `risk_categories` | array enum | source/system-owned | Why review is required |
| `source_actor_type` | enum | source/system-owned | Actor type that created/requested the item |
| `source_actor_id` | string | source/system-owned | Actor id that created/requested the item |
| `source_run_id` | string/null | system/reference | Agent run or process that produced the item if applicable |
| `title` | string | source-owned | Human-readable review title |
| `summary` | string | source-owned | Short summary of what requires review |
| `recommended_action` | string | source-owned | Proposed next action; not approval |
| `required_gates` | array enum | system/source-owned | Gates that must be satisfied |
| `linked_records` | array object | referenced-only | Related artifacts, signals, runs, external refs, or decisions |
| `decision` | object/null | human/system-owned | Human decision once made |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |
| `audit_record_id` | string/null | system-owned/reference | Audit record for review item creation or latest state change |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `description` | string | source-owned | Longer review context |
| `priority` | enum | source/system-owned | Review priority |
| `due_at` | datetime/null | human/system-owned | Optional target review time |
| `expires_at` | datetime/null | human/system-owned | Optional expiration time |
| `sensitivity_rating` | enum | source/system-owned | Data/privacy sensitivity |
| `confidence` | enum | source/system-owned | Evidence/output confidence if applicable |
| `evidence_summary` | string | source-owned | Summary of supporting evidence without private payload dump |
| `reviewer_actor_id` | string/null | human/system-owned | Human reviewer assigned or completing review |
| `escalation_reason` | string/null | human/source-owned | Reason deeper review is required |
| `revision_instructions` | string/null | human-owned | Instructions if revision is requested |
| `park_reason` | string/null | human-owned | Reason item was parked |
| `blocked_reason` | string/null | system/human-owned | Reason item cannot proceed |
| `version` | integer/string | system-owned | Version for future migration/change tracking |

## Valid Review Types

Canonical review types:

```text
quality_review
customer_delivery_review
publish_review
paid_action_review
destructive_action_review
credential_or_permission_review
privacy_review
rights_and_compliance_review
ip_common_sense_review
signal_sanitization_review
strategy_review
workspace_promotion_review
material_workflow_change_review
external_write_review
escalation_review
```

Review type describes what kind of judgment is requested.

Risk categories describe why the item is risky.

## Valid Statuses

Canonical statuses:

```text
open
in_review
approved
approved_with_changes
rejected
revision_requested
escalated
parked
blocked
cancelled
expired
```

## Status Transition Rules

Allowed transitions:

| From | To | Requirement |
|---|---|---|
| `open` | `in_review` | Human begins review |
| `open` | `cancelled` | Source/human cancels before decision |
| `open` | `blocked` | System or human blocks item |
| `open` | `expired` | Time-based expiration if configured |
| `in_review` | `approved` | Human approves |
| `in_review` | `approved_with_changes` | Human approves after changes |
| `in_review` | `rejected` | Human rejects |
| `in_review` | `revision_requested` | Human requests revision |
| `in_review` | `escalated` | Human escalates |
| `in_review` | `parked` | Human parks |
| `revision_requested` | `open` | Revised item is resubmitted |
| `escalated` | `in_review` | Escalated review resumes |
| `parked` | `open` | Human reopens parked item |
| `blocked` | `open` | Blocker resolved and item reopened |

Terminal statuses by default:

```text
approved
approved_with_changes
rejected
cancelled
expired
```

A future schema may allow reopen behavior with explicit audit and decision records.

## Valid Decisions

Human decision values:

```text
approve
approve_with_changes
reject
request_revision
escalate
park
block
cancel
```

Decisions must be made by a human actor where human review is required.

No agent may approve its own output.

## Risk Categories

Canonical risk categories:

```text
public_facing
customer_facing
paid_action
destructive_action
credential_related
permission_related
privacy_sensitive
compliance_sensitive
ip_or_rights_sensitive
external_write
observatory_intake
workspace_lifecycle
business_strategy
quality_sensitive
```

Multiple risk categories may apply.

## Required Gates

Common review gates:

```text
quality_gate
publish_gate
paid_action_gate
data_privacy_gate
customer_delivery_gate
rights_and_compliance_gate
signal_sanitization_gate
ip_common_sense_gate
strategy_review_gate
workspace_promotion_gate
external_write_gate
credential_permission_gate
```

A review item may require more than one gate.

A required gate must not be bypassed by permissions.

## Priority Values

Initial priority values:

```text
low
normal
high
urgent
```

Priority does not bypass review.

Urgent does not mean autonomous.

## Sensitivity Ratings

Initial sensitivity ratings:

```text
low
medium
high
restricted
unknown
```

A high or restricted sensitivity item should require extra care, privacy review, or escalation.

## Linked Records

`linked_records` is an array of references, not ownership transfer.

Allowed linked record types:

```text
artifact
agent_run
signal_candidate
sanitized_signal
workspace_config
audit_record
external_reference
observatory_query_result
human_decision
workflow
business_intake
```

Example:

```yaml
linked_records:
  - record_type: artifact
    record_id: art_123
    relationship: reviewed_output
  - record_type: agent_run
    record_id: run_456
    relationship: source_run
```

Linked records must preserve ownership boundaries.

A review item may reference a workspace-owned artifact, but it does not own the artifact content.

## Decision Object

When a decision is made, the review item should include or reference a decision object.

Recommended shape:

```yaml
decision:
  decision_type: approve | approve_with_changes | reject | request_revision | escalate | park | block | cancel
  reviewer_actor_id: human_operator
  decided_at: 2026-05-24T00:00:00Z
  decision_notes: string
  changed_fields:
    - field_name
  audit_record_id: audit_123
```

A future `human-decision.schema.md` may make this a separate P1 record.

Until then, review items must still preserve decision provenance.

## System-Owned Fields

The following fields should be system-owned:

- `review_item_id`
- `created_at`
- `updated_at`
- `audit_record_id`
- status transition timestamps when implemented
- lifecycle transition result fields
- system-computed blocked/expired state
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless a governed correction process allows change:

- `review_item_id`
- `workspace_id`
- original `source_actor_type`
- original `source_actor_id`
- original `source_run_id`
- original `created_at`

Revisions should create traceable updates, not rewrite origin history.

## Provenance Requirements

A review item must preserve:

- what produced the review request
- which workspace owns the work context
- which actor or run created the request
- which records are being reviewed
- why review is required
- what action is recommended
- what gates must be satisfied
- what decision was made
- who made the decision
- when the decision was made
- what audit records trace the process

## Audit Requirements

The following events must generate audit records:

- review item created
- review item assigned
- review status changed
- review decision made
- review item approved
- review item approved with changes
- review item rejected
- revision requested
- item escalated
- item parked
- item blocked
- item cancelled
- item expired
- linked record changed after review item creation

Rejected, parked, blocked, cancelled, and expired items remain auditable.

## Lifecycle Rules

Review items must obey workspace lifecycle state:

- `idea` workspaces should not generate operational review items.
- `onboarding` workspaces may generate planning/promotion review items only.
- `manual_test` workspaces may generate review items from manual workflows.
- `active` workspaces may generate configured review items.
- `paused` workspaces may not generate new review items.
- `retired` workspaces may not generate new review items.

If a workspace is paused or retired after review item creation, the review item should not proceed to external action without an explicit resume or revalidation decision.

## Action Rules

Review item creation never executes the recommended action.

Approval may authorize the next step only if:

1. the workspace lifecycle allows it
2. the runtime mode allows it
3. required gates are satisfied
4. permissions allow it
5. audit logging succeeds
6. the action is not forbidden by hard-no rules

## Signal Sanitization Review Rules

For `signal_sanitization_review`:

- linked record should include a signal candidate
- risk category should include `observatory_intake`
- required gates should include `signal_sanitization_gate`
- decision must be human-approved early
- approval permits Observatory intake only for the sanitized signal
- rejection prevents Observatory intake
- parking holds without intake

Signal review must not expose private source details through normal Observatory query surfaces.

## External Action Review Rules

For `publish_review`, `external_write_review`, `paid_action_review`, `customer_delivery_review`, `credential_or_permission_review`, or `destructive_action_review`:

- approval must not bypass workspace lifecycle
- approval must not bypass runtime rules
- approval must not bypass permissions
- approval must be audited
- approval should authorize a specific bounded action, not permanent broad authority

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
searchclarity_report_section
etsy_listing_payload
printify_product_payload
fiverr_message_text
custom_data
```

Use linked workspace-owned artifacts, external references, integration-owned records, or bounded evidence summaries instead.

## Bounded Metadata

Do not use unbounded metadata to store hidden review logic.

A future bounded metadata field must define:

- allowed keys
- value types
- owner
- whether it is queryable
- whether it is canonical meaning
- what must not be stored there

Until then, avoid generic `metadata` or `custom_data` fields.

## Example Record

```yaml
review_item_id: rev_001
workspace_id: ws_internal_research_001
review_type: signal_sanitization_review
status: open
risk_categories:
  - observatory_intake
  - privacy_sensitive
source_actor_type: agent
source_actor_id: signal_capture_agent
source_run_id: run_001
title: Review sanitized signal candidate for Observatory intake
summary: A signal candidate proposes a generalized pattern from internal research findings.
recommended_action: Approve sanitized signal if it contains no workspace-private details.
required_gates:
  - signal_sanitization_gate
linked_records:
  - record_type: signal_candidate
    record_id: sigcand_001
    relationship: reviewed_signal_candidate
  - record_type: agent_run
    record_id: run_001
    relationship: source_run
decision: null
sensitivity_rating: medium
confidence: medium
evidence_summary: Signal is based on internal research notes and contains no customer data.
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
audit_record_id: audit_001
version: 1
```

## Validation Questions

Before accepting a review item, answer:

1. Is the workspace id valid?
2. Is the workspace lifecycle status allowed to create this review item?
3. Is the review type valid?
4. Are risk categories defined?
5. Are required gates defined?
6. Is the source actor traceable?
7. Are linked records references rather than ownership transfers?
8. Does the item avoid private payload dumps?
9. Does the item avoid provider-specific payloads in core?
10. Does the recommended action stay bounded?
11. Does approval require a human where required?
12. Does the item preserve audit and provenance requirements?
13. Does this review item avoid executing the action by existing?

## Non-Goals

This schema does not define:

- full human decision schema
- artifact content schema
- customer records
- provider payload schemas
- signal schema details beyond references
- execution engine behavior
- database tables
- UI review screens
- notification system

## Final Rule

```text
A review item is a gate, not a green light.
```
