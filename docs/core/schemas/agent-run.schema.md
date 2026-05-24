# Agent Run Schema

## Purpose

This document defines the P0 agent run schema for Neon Ronin.

An agent run is the core-owned execution record for one attempt by an agent to perform scoped work inside a workspace.

Agent runs exist so Neon Ronin can answer:

```text
Which agent ran, why did it run, what inputs did it use, what outputs did it create, what review gates were triggered, what audit records trace it, and did it stay within its allowed boundaries?
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

Agent runs are core-owned because runtime traceability is a platform responsibility.

An agent run may reference workspace-owned artifacts, workspace-owned inputs, Observatory-owned query results, integration-owned references, review queue items, signal candidates, and audit records, but the run record itself is part of Neon Ronin core runtime governance.

## Core Rule

```text
An agent run records scoped execution.
It does not grant authority beyond the agent definition, workspace config, lifecycle status, runtime mode, permissions, and review gates.
```

An agent run must not be used as a backdoor for external writes, publishing, customer messaging, spending, credential changes, destructive actions, or Observatory intake.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `agent_run_id` | string | system-owned | Stable unique run id |
| `workspace_id` | string | system/reference | Workspace where the run occurred |
| `agent_id` | string | system/reference | Agent definition used for the run |
| `agent_role` | enum/string | system/reference | Agent role at time of run |
| `status` | enum | system-governed | Current run status |
| `trigger_type` | enum | system/source-owned | What started the run |
| `trigger_actor_type` | enum | system/source-owned | Actor type that triggered the run |
| `trigger_actor_id` | string | system/source-owned | Actor id that triggered the run |
| `runtime_mode` | enum | system-governed | Runtime mode used for the run |
| `input_references` | array object | referenced-only | Inputs used by the run |
| `output_references` | array object | referenced-only | Outputs created by the run |
| `action_classes_used` | array enum | system-owned | Action classes actually used during the run |
| `started_at` | datetime | system-owned | Run start timestamp |
| `ended_at` | datetime/null | system-owned | Run end timestamp |
| `audit_record_ids` | array string | system/reference | Audit records linked to the run |
| `created_at` | datetime | system-owned | Run record creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `correlation_id` | string/null | system-owned | Groups related records across workflow/request |
| `parent_run_id` | string/null | referenced-only | Parent run if this run was spawned from another governed run |
| `workflow_id` | string/null | referenced-only | Workflow this run belongs to, if applicable |
| `review_item_ids` | array string | referenced-only | Review items created or updated by the run |
| `signal_candidate_ids` | array string | referenced-only | Signal candidates created by the run |
| `artifact_ids` | array string | referenced-only | Artifacts created or updated by the run |
| `observatory_query_ids` | array string | referenced-only | Observatory queries made during the run |
| `external_reference_ids` | array string | referenced-only/integration-owned | External references touched or created |
| `model_policy_reference` | string/null | referenced-only | Optional model/provider policy reference, not provider lock-in |
| `tool_usage` | array object | bounded/system-owned | Bounded record of tools used |
| `result_summary` | string/null | system/source-owned | Human-readable run result summary |
| `error_code` | string/null | system-owned | Machine-readable error code if failed/blocked |
| `error_summary` | string/null | system-owned | Human-readable error summary without private payload dump |
| `blocked_reason` | string/null | system/human-owned | Reason run was blocked |
| `confidence` | enum/null | source/system-owned | Confidence of run output if applicable |
| `provenance_level` | enum | system-owned | Run is usually event/structured provenance |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Statuses

Canonical run statuses:

```text
queued
started
running
waiting_for_review
completed
completed_with_warnings
failed
blocked
cancelled
expired
skipped
```

## Status Transition Rules

Allowed transitions:

| From | To | Requirement |
|---|---|---|
| `queued` | `started` | Runtime begins run |
| `started` | `running` | Agent begins work |
| `running` | `waiting_for_review` | Run creates output requiring review |
| `running` | `completed` | Run finishes successfully with no required pending review |
| `running` | `completed_with_warnings` | Run finishes but warnings remain |
| `running` | `failed` | Run fails |
| `running` | `blocked` | Permissions, lifecycle, policy, validation, or safety blocks run |
| `running` | `cancelled` | Human/system cancels run |
| `queued` | `cancelled` | Human/system cancels before start |
| `queued` | `expired` | Run expires before starting |
| `queued` | `skipped` | Run skipped because no longer needed |
| `waiting_for_review` | `completed` | Required review outcome resolves run's pending state if applicable |
| any non-terminal | `blocked` | Safety/lifecycle/permission issue blocks progress |

Terminal statuses by default:

```text
completed
completed_with_warnings
failed
blocked
cancelled
expired
skipped
```

A terminal run should not be rewritten into another terminal result. Create a new run or correction/audit record if needed.

## Trigger Types

Canonical trigger types:

```text
human_started
workflow_started
review_requested
system_started
scheduled
watch_mode
retry
imported
unknown
```

Early Neon Ronin should primarily use `human_started`.

`scheduled` and `watch_mode` remain deferred except where explicitly promoted later.

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

Trigger actor must be traceable.

## Runtime Modes

Canonical runtime modes:

```text
off
on_demand
scheduled
watch_mode
paused
emergency_stop
```

Agent runs must obey workspace lifecycle and runtime constraints.

Examples:

- `idea` workspaces cannot start agent runs.
- `manual_test` workspaces may use human-started on-demand runs only if configured.
- `paused` workspaces cannot start new runs.
- `retired` workspaces cannot start new runs.
- `emergency_stop` blocks all new runs and should cancel/stop active runs where possible.

## Input References

`input_references` is an array of thin references.

Allowed input reference types:

```text
workspace_config
artifact
review_item
signal
signal_candidate
observatory_query_result
external_reference
workflow
manual_note
business_intake
human_decision
audit_record
```

Example:

```yaml
input_references:
  - record_type: workspace_config
    record_id: ws_internal_research_001
    relationship: workspace_scope
  - record_type: artifact
    record_id: art_001
    relationship: source_material
```

Input references must not copy raw private payloads into the run record.

## Output References

`output_references` is an array of thin references.

Allowed output reference types:

```text
artifact
review_item
signal_candidate
audit_record
external_reference
blocked_action_report
analysis_summary
recommendation_packet
qa_checklist
```

Example:

```yaml
output_references:
  - record_type: signal_candidate
    record_id: sigcand_001
    relationship: created_output
  - record_type: review_item
    record_id: rev_001
    relationship: required_review
```

Output references must not imply approval.

A draft output remains a draft.

A review item remains a gate.

A signal candidate remains unapproved until sanitization review.

## Action Classes Used

Canonical action classes:

```text
read
analyze
draft
queue
external_draft
live_write
destructive
```

Agent run action classes must be a subset of the agent definition's allowed action classes and the workspace config/runtime permissions.

Early agent runs should avoid `live_write` and `destructive`.

## Tool Usage

`tool_usage` may record bounded tool activity.

Recommended shape:

```yaml
tool_usage:
  - tool_id: workspace_artifact_reader
    action_class: read
    result_status: succeeded
    audit_record_id: audit_123
```

Tool usage must not store full prompts, raw private customer data, credentials, or full provider payloads unless a future bounded schema allows it.

## System-Owned Fields

The following fields should be system-owned:

- `agent_run_id`
- `status`
- `started_at`
- `ended_at`
- `created_at`
- `updated_at`
- `audit_record_ids`
- `correlation_id`
- system-computed error/block fields
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless a governed correction process allows change:

- `agent_run_id`
- `workspace_id`
- `agent_id`
- original `trigger_type`
- original `trigger_actor_type`
- original `trigger_actor_id`
- original `runtime_mode`
- original `started_at`
- original `created_at`

If a run needs correction, create audit/correction records rather than rewriting origin history.

## Provenance Requirements

An agent run must preserve enough provenance to answer:

- which workspace scoped the run?
- which agent definition was used?
- who or what triggered the run?
- what runtime mode was used?
- what inputs were referenced?
- what tools were used?
- what outputs were created?
- what review items were created?
- what signals or artifacts resulted?
- what audit records trace the run?
- why did it fail or get blocked, if applicable?

## Audit Requirements

The following run events must generate audit records:

- agent run queued
- agent run started
- agent run completed
- agent run completed with warnings
- agent run failed
- agent run blocked
- agent run cancelled
- agent run expired
- agent used tool
- agent created artifact
- agent created signal candidate
- agent created review item
- agent requested external action
- agent attempted forbidden action
- agent run skipped due to lifecycle/runtime/permission rules

Failed, blocked, cancelled, expired, and skipped runs remain auditable.

## Lifecycle Rules

Agent runs must obey workspace lifecycle status:

- `idea` workspaces cannot start agent runs.
- `onboarding` workspaces may allow setup/planning assistance only if explicitly configured.
- `manual_test` workspaces may allow human-started on-demand runs only.
- `active` workspaces may run according to configured runtime modes and review gates.
- `paused` workspaces cannot start new runs.
- `retired` workspaces cannot start new runs.

If workspace status changes during a run, the run should obey the new stricter state.

Example:

- if workspace becomes paused, active run should stop, block, or wait for human decision
- if emergency stop triggers, active run should stop or be marked blocked/cancelled according to future runtime implementation

## Permission Rules

A run is valid only if:

1. the agent definition is active
2. the workspace config allows the agent
3. the workspace lifecycle allows agent work
4. runtime mode is allowed for the workspace
5. requested action classes are allowed by the agent definition
6. requested action classes are allowed by permissions
7. required review gates are preserved
8. hard-no rules are not violated
9. audit logging succeeds

If any check fails, the run should be blocked or rejected and audited.

## Review Rules

An agent run must create or link review items when outputs require human judgment.

Examples requiring review:

- customer-facing deliverable draft
- publish packet
- external write request
- paid action request
- destructive action request
- credential/permission change request
- signal candidate intended for Observatory intake
- rights/IP/compliance-sensitive output

A run cannot approve its own review item.

## Signal Rules

An agent run may create a signal candidate if allowed.

An agent run must not:

- approve its own signal candidate
- submit raw data to the Observatory
- bypass signal sanitization review
- expose private source details through Observatory query surfaces

Signal candidate outputs should link to review queue items for sanitization review.

## External Action Rules

An agent run may request or prepare external actions only if allowed by agent definition, workspace config, lifecycle, permissions, and review gates.

Even if an agent creates an external draft request, the run itself must not imply final external execution.

Forbidden early without explicit later promotion:

- autonomous publishing
- autonomous customer messaging
- autonomous customer delivery
- autonomous spending
- autonomous credential changes
- autonomous destructive actions

## Error And Block Rules

Runs should fail or block explicitly.

Common block reasons:

```text
workspace_lifecycle_disallows_run
runtime_mode_disallows_run
agent_status_disallows_run
agent_not_allowed_in_workspace
permission_scope_denied
review_gate_required
hard_no_rule_violation
missing_provenance
observatory_permission_denied
external_action_not_allowed
audit_logging_failed
unknown_field_rejected
```

Failure or block must create audit records.

## Relationships To Other Records

Agent runs may reference:

- workspace config
- agent definition
- artifacts
- review queue items
- audit records
- signal records
- Observatory query results
- external references
- workflows
- human decisions

Agent runs should not own artifact content, signal approval decisions, human decisions, or external provider resources.

## Forbidden Fields

Do not add fields such as:

```text
full_prompt_dump
full_model_response_dump
customer_email
customer_phone
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
fiverr_message_text
custom_data
```

Use bounded summaries, references, future provider contracts, and workspace-owned artifacts instead.

## Bounded Metadata

Do not use unbounded metadata to hide prompts, private payloads, provider responses, tool payloads, or business-specific logic.

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
agent_run_id: run_001
workspace_id: ws_internal_research_001
agent_id: agent_signal_capture
agent_role: signal_capture_agent
status: waiting_for_review
trigger_type: human_started
trigger_actor_type: human
trigger_actor_id: human_operator
runtime_mode: on_demand
input_references:
  - record_type: workspace_config
    record_id: ws_internal_research_001
    relationship: workspace_scope
  - record_type: artifact
    record_id: art_research_notes_001
    relationship: source_material
output_references:
  - record_type: signal_candidate
    record_id: sigcand_001
    relationship: created_output
  - record_type: review_item
    record_id: rev_001
    relationship: required_sanitization_review
action_classes_used:
  - read
  - analyze
  - draft
  - queue
started_at: 2026-05-24T00:00:00Z
ended_at: 2026-05-24T00:01:00Z
audit_record_ids:
  - audit_run_started_001
  - audit_signal_candidate_created_001
  - audit_review_item_created_001
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:01:00Z
correlation_id: corr_001
parent_run_id: null
workflow_id: null
review_item_ids:
  - rev_001
signal_candidate_ids:
  - sigcand_001
artifact_ids: []
observatory_query_ids: []
external_reference_ids: []
model_policy_reference: local_default_model_policy
tool_usage:
  - tool_id: workspace_artifact_reader
    action_class: read
    result_status: succeeded
    audit_record_id: audit_tool_001
result_summary: Signal Capture Agent drafted a signal candidate and created a review item for sanitization approval.
error_code: null
error_summary: null
blocked_reason: null
confidence: medium
provenance_level: event
version: 1
```

## Validation Questions

Before accepting an agent run record, answer:

1. Is the workspace id valid?
2. Is the agent id valid and active?
3. Is the agent allowed in this workspace?
4. Does workspace lifecycle allow this run?
5. Does runtime mode allow this run?
6. Are action classes used allowed by the agent definition?
7. Are action classes used allowed by permissions and hard-no rules?
8. Are input references thin references rather than payload dumps?
9. Are output references clear and bounded?
10. Did the run create review items where required?
11. Did the run avoid approving its own work?
12. Did the run avoid raw Observatory submission?
13. Are audit records linked?
14. If failed/blocked, is the reason explicit?
15. Does the record avoid credentials, raw customer data, provider payload dumps, and unbounded metadata?

## Non-Goals

This schema does not define:

- full workflow schema
- scheduler implementation
- watch mode implementation
- prompt storage
- model provider API contracts
- full tool execution logs
- artifact content
- human decision schema details
- external integration schemas
- database tables
- UI run timeline

## Final Rule

```text
An agent run is execution evidence, not execution permission.
```
