# Agent Definition Schema

## Purpose

This document defines the P0 agent definition schema for Neon Ronin.

An agent definition is the core-owned record that describes an agent's role, allowed workspace types, allowed action classes, allowed tools, output types, runtime constraints, review requirements, permission posture, and forbidden actions.

Agent definitions exist so Neon Ronin can use agents without granting them vague, unlimited, or self-approving authority.

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

Agent definitions are core-owned because agent capability boundaries are a platform responsibility.

Workspace-specific agent assignments or configuration overlays may be workspace-scoped later, but the reusable definition of what an agent is allowed to do belongs to core.

## Core Rule

```text
An agent definition grants bounded capability.
It does not grant final authority.
```

Agents may assist, analyze, draft, prepare, classify, summarize, and queue work within their allowed scope.

Agents must not approve their own work, bypass review gates, perform forbidden actions, or expand their own permissions.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `agent_id` | string | system-owned | Stable unique agent identifier |
| `agent_name` | string | human/config-owned | Human-readable agent name |
| `agent_role` | enum/string | human/config-owned | Primary role or function |
| `description` | string | human/config-owned | Short description of the agent's purpose |
| `allowed_workspace_types` | array enum | human/config-owned | Workspace types where this agent may operate |
| `allowed_action_classes` | array enum | human/config-owned | Action classes the agent may perform |
| `allowed_runtime_modes` | array enum | human/config-owned | Runtime modes the agent may run under |
| `allowed_tools` | array string | human/config-owned | Tool ids or tool classes the agent may use |
| `output_types` | array enum/string | human/config-owned | Outputs the agent may create |
| `required_review_gates` | array enum | human/config-owned | Review gates required for this agent's outputs/actions |
| `forbidden_actions` | array enum/string | human/config-owned | Actions this agent must never perform |
| `permission_scope` | object | human/config-owned | Bounded permission posture for the agent |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `agent_version` | string/integer | system-owned | Version of the agent definition |
| `status` | enum | system-governed | Whether the agent definition is active, draft, paused, retired, or deprecated |
| `owner_actor_id` | string/null | human/config-owned | Human owner or maintainer |
| `default_model_policy` | string/null | human/config-owned | Optional model/provider policy reference, not provider lock-in |
| `input_constraints` | array string | human/config-owned | Inputs the agent may accept |
| `data_access_rules` | object | human/config-owned | Workspace/Observatory/private-data access boundaries |
| `observatory_permissions` | object | human/config-owned | Whether agent may query or propose signals |
| `handoff_rules` | object | human/config-owned | Rules for routing outputs to review or another actor |
| `failure_behavior` | object | human/config-owned | What happens when the agent fails or is blocked |
| `audit_requirements` | array string | human/config-owned | Audit events required for the agent |
| `tags` | array string | bounded/human-owned | Bounded organizational tags |

## Valid Agent Statuses

Canonical values:

```text
draft
active
paused
deprecated
retired
```

Status meanings:

| Status | Meaning |
|---|---|
| `draft` | Agent is being defined and should not run |
| `active` | Agent may run within allowed workspace/runtime rules |
| `paused` | Agent definition exists but new runs are blocked |
| `deprecated` | Agent should not be used for new workflows but may remain for history |
| `retired` | Agent is closed for new use and preserved for audit/history |

## Valid Workspace Types

Canonical values:

```text
service
marketplace_store
digital_products
content
internal_research
hybrid
other
```

An agent may support multiple workspace types only if its role is truly reusable.

## Valid Action Classes

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

Early Neon Ronin should avoid granting `live_write` or `destructive` to agents.

If those action classes are ever allowed later, they must remain behind human approval gates and explicit permissions.

## Valid Runtime Modes

Canonical runtime modes:

```text
off
on_demand
scheduled
watch_mode
paused
emergency_stop
```

Agent runtime modes must also obey workspace lifecycle status.

Examples:

- agents may not run for `idea` workspaces
- manual-test workspaces may use only human-started on-demand agents if configured
- paused and retired workspaces cannot start new agent runs
- emergency stop blocks all new agent work

## Common Agent Roles

Initial generic roles:

```text
research_agent
pattern_analysis_agent
scoring_agent
queue_agent
qa_agent
signal_capture_agent
intake_agent
drafting_agent
delivery_prep_agent
publishing_prep_agent
product_brief_agent
listing_copy_agent
asset_prep_agent
editorial_planning_agent
```

Roles should remain generic.

Do not define specific-business, provider-specific, or marketplace-specific agent roles in core.

## Output Types

Initial output types:

```text
research_packet
analysis_summary
recommendation_packet
draft_artifact
review_queue_item
signal_candidate
qa_checklist
scoring_result
workflow_note
external_draft_request
blocked_action_report
```

Output type does not imply approval.

A draft remains a draft.

A recommendation remains a recommendation.

A review item remains a gate.

## Permission Scope Object

Required conceptual shape:

```yaml
permission_scope:
  workspace_scoped: true
  allowed_workspace_ids: []
  allowed_action_classes:
    - read
    - analyze
    - draft
    - queue
  can_access_workspace_private_data: boolean
  can_query_observatory: boolean
  can_submit_signal_candidates: boolean
  can_create_review_items: boolean
  can_execute_external_actions: false
  requires_human_review_for_outputs: true
```

Rules:

- permissions must be workspace-scoped unless explicitly global/core-owned
- permissions must not bypass review gates
- agents must not modify their own permission scope
- agents must not approve their own outputs
- agents must not gain access to another workspace's private data through permission shortcuts

## Data Access Rules Object

Recommended shape:

```yaml
data_access_rules:
  workspace_private_access: none | read_limited | read_allowed
  observatory_access: none | query_allowed | signal_candidate_allowed
  external_data_access: none | read_allowed | draft_allowed
  customer_data_access: none | redacted_only | workspace_scoped_allowed
  credential_access: none
```

Default posture should be restrictive.

Credential access should be `none` until a future secrets and credentials contract exists.

## Observatory Permissions Object

Recommended shape:

```yaml
observatory_permissions:
  can_query: boolean
  allowed_query_types:
    - keyword_cluster
    - trend_profile
    - prior_signal_check
    - data_quality_check
  can_create_signal_candidates: boolean
  can_submit_sanitized_signals: false
  signal_submission_requires_human_review: true
```

Agents may propose signal candidates.

Agents must not approve final Observatory intake.

## Required Review Gates

Common gates:

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
external_write_gate
credential_permission_gate
```

If an agent output can influence risky action, the output must route through review.

## Forbidden Actions

Global forbidden actions for agents:

```text
approve_own_work
autonomous_publishing
autonomous_spending
autonomous_customer_messaging
autonomous_customer_delivery
autonomous_credential_changes
autonomous_destructive_actions
bypass_review_gate
modify_own_permissions
read_other_workspace_private_data
submit_raw_data_to_observatory
store_credentials_in_output
```

Workspace-specific agent definitions may add stricter forbidden actions.

They must not remove global forbidden actions.

## Handoff Rules

Agent definitions should define what happens to outputs.

Recommended shape:

```yaml
handoff_rules:
  draft_outputs_go_to_review_queue: true
  signal_candidates_go_to_sanitization_review: true
  external_action_requests_go_to_review_queue: true
  failed_runs_create_audit_record: true
  blocked_actions_create_audit_record: true
```

Agents should hand off outputs through governed records, not side effects.

## Failure Behavior

Recommended shape:

```yaml
failure_behavior:
  on_error: create_audit_record
  on_permission_denied: create_blocked_action_report
  on_review_required: create_review_queue_item
  on_policy_uncertain: escalate_to_human
  on_missing_provenance: block_or_request_revision
```

Failure must not silently proceed.

## System-Owned Fields

The following fields should be system-owned:

- `agent_id`
- `created_at`
- `updated_at`
- `agent_version`
- status transition timestamps when implemented
- system-computed compatibility flags when implemented

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless a governed migration allows change:

- `agent_id`
- original `created_at`
- original creator/source reference when added later

Role, permissions, tools, and review gates may change through governed updates, but meaningful changes must generate audit records.

## Provenance Requirements

An agent definition should preserve or reference:

- who created the definition
- when it was created
- what platform need it serves
- which workspace types it supports
- why its action classes are allowed
- why its tools are allowed
- what review gates constrain it
- audit records for definition changes

## Audit Requirements

The following events must generate audit records:

- agent definition created
- agent definition updated
- agent status changed
- allowed action classes changed
- allowed tools changed
- permission scope changed
- review gate requirements changed
- forbidden actions changed
- agent paused
- agent retired
- agent run attempted while paused/retired/forbidden

## Lifecycle Rules

Agent definitions must obey both agent status and workspace lifecycle.

Examples:

- `draft` agents cannot run.
- `paused` agents cannot start new runs.
- `retired` agents cannot start new runs.
- active agents still cannot run in workspace statuses that disallow agent work.
- an agent allowed in one workspace type is not automatically allowed in all workspace types.

## Relationships To Other Records

Agent definitions may be referenced by:

- workspace configs
- agent runs
- review queue items
- audit records
- signal candidates
- artifacts
- workflow records
- permission records later

Agent definitions should not directly own agent run history.

Runs belong to the agent run schema.

## Forbidden Fields

Do not add fields such as:

```text
business_specific_secret_prompt
etsy_publish_permission
printify_api_key
fiverr_message_permission
raw_customer_data_global_access
all_workspace_access
self_approval_allowed
provider_token
api_key
oauth_refresh_token
custom_data
```

Use bounded permission scopes, integration-owned records, and future secrets/credentials contracts instead.

## Bounded Metadata

Do not use unbounded metadata to hide permissions, prompts, provider-specific payloads, or business-specific logic.

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
agent_id: agent_signal_capture
agent_name: Signal Capture Agent
agent_role: signal_capture_agent
description: Identifies reusable observations and drafts signal candidates for human sanitization review.
status: active
allowed_workspace_types:
  - internal_research
  - service
  - marketplace_store
  - digital_products
  - content
allowed_action_classes:
  - read
  - analyze
  - draft
  - queue
allowed_runtime_modes:
  - on_demand
allowed_tools:
  - workspace_artifact_reader
  - observatory_query_reader
output_types:
  - signal_candidate
  - review_queue_item
  - analysis_summary
required_review_gates:
  - signal_sanitization_gate
forbidden_actions:
  - approve_own_work
  - autonomous_publishing
  - autonomous_spending
  - autonomous_customer_messaging
  - autonomous_customer_delivery
  - autonomous_credential_changes
  - autonomous_destructive_actions
  - bypass_review_gate
  - modify_own_permissions
  - read_other_workspace_private_data
  - submit_raw_data_to_observatory
  - store_credentials_in_output
permission_scope:
  workspace_scoped: true
  allowed_workspace_ids: []
  allowed_action_classes:
    - read
    - analyze
    - draft
    - queue
  can_access_workspace_private_data: true
  can_query_observatory: true
  can_submit_signal_candidates: true
  can_create_review_items: true
  can_execute_external_actions: false
  requires_human_review_for_outputs: true
data_access_rules:
  workspace_private_access: read_limited
  observatory_access: signal_candidate_allowed
  external_data_access: none
  customer_data_access: redacted_only
  credential_access: none
observatory_permissions:
  can_query: true
  allowed_query_types:
    - keyword_cluster
    - trend_profile
    - prior_signal_check
    - data_quality_check
  can_create_signal_candidates: true
  can_submit_sanitized_signals: false
  signal_submission_requires_human_review: true
handoff_rules:
  draft_outputs_go_to_review_queue: true
  signal_candidates_go_to_sanitization_review: true
  external_action_requests_go_to_review_queue: true
  failed_runs_create_audit_record: true
  blocked_actions_create_audit_record: true
failure_behavior:
  on_error: create_audit_record
  on_permission_denied: create_blocked_action_report
  on_review_required: create_review_queue_item
  on_policy_uncertain: escalate_to_human
  on_missing_provenance: block_or_request_revision
audit_requirements:
  - agent_run_started
  - agent_run_completed
  - agent_run_failed
  - review_item_created
  - signal_candidate_created
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
agent_version: 1
```

## Validation Questions

Before accepting an agent definition, answer:

1. Is the agent role generic and business-neutral?
2. Are allowed workspace types explicit?
3. Are allowed action classes explicit?
4. Are runtime modes explicit and lifecycle-compatible?
5. Are tools bounded and justified?
6. Are output types defined?
7. Are review gates required for risky outputs?
8. Are global forbidden actions preserved?
9. Can the agent approve its own work? If yes, reject the definition.
10. Can the agent modify its own permissions? If yes, reject the definition.
11. Can the agent access other workspaces' private data? If yes, reject or redesign.
12. Can the agent submit raw data to the Observatory? If yes, reject the definition.
13. Does the definition avoid provider-specific credentials or payloads?
14. Does it preserve provenance and audit requirements?
15. Does it avoid unbounded metadata/custom data?

## Non-Goals

This schema does not define:

- agent run records
- prompts in full
- model provider contracts
- tool implementation contracts
- permission-scope schema details
- secrets or credentials
- external integration behavior
- autonomous scheduling
- watch mode behavior
- database tables

## Final Rule

```text
An agent is a bounded worker, not a decision owner.
```
