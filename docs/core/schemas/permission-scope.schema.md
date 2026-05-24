# Permission Scope Schema

## Purpose

This document defines the P1 permission scope schema for Neon Ronin.

A permission scope is a bounded record describing what an actor, agent, workflow, integration, runtime process, or future user role may do within Neon Ronin.

Permission scopes exist so capability is explicit, workspace-scoped, review-aware, auditable, and unable to bypass lifecycle or human approval gates.

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

Permission scopes are core-owned because authorization boundaries are a platform responsibility.

A permission scope may reference workspace config, agent definitions, workflows, integrations, review gates, and human decisions, but the scope itself is a core governance record.

## Core Rule

```text
Permissions enforce boundaries.
Permissions do not bypass review gates.
```

A permission scope that allows a risky action must still require the appropriate lifecycle status, runtime mode, review gate, human decision, and audit record.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `permission_scope_id` | string | system-owned | Stable unique permission scope id |
| `scope_name` | string | human/config-owned | Human-readable scope name |
| `scope_status` | enum | system-governed | Current scope status |
| `actor_type` | enum | human/system-owned | Type of actor this scope applies to |
| `actor_id` | string | human/system-owned | Actor id this scope applies to |
| `workspace_scope` | object | human/system-owned | Workspace boundary for this permission |
| `allowed_action_classes` | array enum | human/system-owned | Action classes permitted by this scope |
| `allowed_resource_types` | array enum/string | human/system-owned | Resource types this scope may act on |
| `allowed_runtime_modes` | array enum | human/system-owned | Runtime modes where this scope applies |
| `required_review_gates` | array enum | human/system-owned | Gates required before risky actions |
| `audit_requirements` | array string | human/system-owned | Audit events required when scope is used/changed |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `description` | string | human/config-owned | Longer permission scope description |
| `expires_at` | datetime/null | human/system-owned | Expiration timestamp if temporary |
| `granted_by_human_decision_id` | string/null | referenced-only | Human decision that granted or changed this scope |
| `revoked_by_human_decision_id` | string/null | referenced-only | Human decision that revoked this scope |
| `allowed_workspace_types` | array enum | human/system-owned | Workspace types this permission may apply to |
| `denied_action_classes` | array enum | human/system-owned | Explicit action class denials |
| `denied_resource_types` | array enum/string | human/system-owned | Explicit resource denials |
| `external_provider_scope` | object/null | integration-owned/reference | Bounded external provider scope, if any |
| `observatory_scope` | object/null | human/system-owned | Observatory query/submission permissions |
| `data_access_rules` | object | human/system-owned | Private/customer/credential/data rules |
| `conditions` | array string | human/system-owned | Conditions that must remain true |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Scope Statuses

Canonical values:

```text
draft
active
paused
revoked
expired
retired
```

Status meanings:

| Status | Meaning |
|---|---|
| `draft` | Scope is being defined and grants no capability |
| `active` | Scope may be used if all other gates pass |
| `paused` | Scope exists but may not be used for new work |
| `revoked` | Scope has been explicitly removed |
| `expired` | Scope is no longer valid due to time/condition |
| `retired` | Scope is closed and kept for history |

## Actor Types

Canonical actor types:

```text
human
agent
system
workflow
integration
scheduled_job
external_provider
unknown
```

Early Neon Ronin should mainly use human, agent, system, workflow, and integration.

Scheduled jobs and external provider delegated scopes are deferred unless promoted later.

## Action Classes

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

Early permission scopes should avoid `live_write` and `destructive` unless explicitly review-gated and human-approved.

## Workspace Scope Object

Recommended shape:

```yaml
workspace_scope:
  scope_type: all | workspace_ids | workspace_type | none
  workspace_ids:
    - ws_001
  workspace_types:
    - internal_research
  cross_workspace_private_data_access: false
```

Rules:

- default scope should be one workspace or no workspace
- cross-workspace private data access must be false by default
- Observatory queries are not direct cross-workspace private access
- all-workspace scopes should be rare and strongly justified

## Observatory Scope Object

Recommended shape:

```yaml
observatory_scope:
  can_query: boolean
  allowed_query_types:
    - keyword_cluster
    - trend_profile
    - prior_signal_check
    - data_quality_check
  can_submit_signal_candidates: boolean
  can_submit_sanitized_signals: boolean
  signal_submission_requires_human_review: true
```

Rules:

- querying and submission are separate permissions
- agents may create signal candidates only if allowed
- early agents must not approve final Observatory intake
- raw workspace data must not enter the Observatory

## Data Access Rules Object

Recommended shape:

```yaml
data_access_rules:
  workspace_private_data: none | read_limited | read_allowed
  customer_data: none | redacted_only | workspace_scoped_allowed
  credentials: none
  external_payloads: none | bounded_references_only | integration_scoped
  artifact_content: none | metadata_only | workspace_scoped_allowed
```

Default posture should be restrictive.

Credentials should remain `none` until secrets and credentials rules are implemented.

## External Provider Scope Object

Recommended shape:

```yaml
external_provider_scope:
  provider: string
  allowed_resource_types:
    - listing
    - draft
  allowed_action_classes:
    - read
    - external_draft
  live_write_requires_human_decision: true
```

Provider-specific details belong in integration-specific contracts later.

A generic permission scope must not store provider tokens, raw API keys, or full provider payloads.

## Required Review Gate Rule

Permission scopes must list required review gates for risky actions.

Risky action classes include:

- `external_draft` in many early contexts
- `live_write`
- `destructive`
- paid actions
- credential changes
- permission changes
- customer-facing outputs
- public publishing
- Observatory intake

Permissions should route through gates, not around them.

## Human Decision Rule

Human approval may grant or change a permission scope only when represented by a linked human decision and audit record.

A human decision may authorize a bounded scope.

It should not accidentally create permanent broad permission.

## Deny-First Rule

If an action is not explicitly allowed, it is denied.

If an action is both allowed and denied, denial wins.

If workspace lifecycle, runtime mode, review gate, or hard-no rule forbids an action, permission scope cannot override it.

## System-Owned Fields

System-owned fields should include:

- `permission_scope_id`
- `scope_status`
- `created_at`
- `updated_at`
- expiration/revocation computed fields when implemented
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless governed migration allows change:

- `permission_scope_id`
- original `actor_type`
- original `actor_id`
- original `created_at`

Permission changes should be versioned, superseded, or audited rather than silently overwritten.

## Provenance Requirements

Permission scopes must preserve:

- who or what the scope applies to
- why the scope exists
- who approved it, if approval is required
- what human decision granted or changed it
- what workspace or workspace type it applies to
- what actions and resources are allowed
- what gates remain required
- when it expires or was revoked
- audit records for creation/change/revocation/use

## Audit Requirements

The following events must generate audit records:

- permission scope created
- permission scope activated
- permission scope changed
- permission scope paused
- permission scope revoked
- permission scope expired
- permission scope retired
- permission denied action
- permission allowed action used for meaningful state change
- permission attempted to bypass review gate
- permission attempted to access forbidden workspace/private data

## Lifecycle And Runtime Rules

Permission scopes must obey workspace lifecycle and runtime mode.

Examples:

- permission cannot allow new runs in paused workspaces
- permission cannot allow operations in retired workspaces
- permission cannot allow scheduled work when scheduled mode is not approved
- permission cannot allow watch mode when watch mode is deferred or disallowed
- permission cannot override emergency stop

## Relationship To Agent Definitions

Agent definitions may include conceptual permission posture.

Permission scopes are the more explicit governance record for actual allowed capability.

An agent run is valid only when both the agent definition and applicable permission scope allow the action, and all lifecycle/review/audit requirements pass.

## Relationship To Review Queue

Permission scopes should require review queue items for risky actions.

A permission scope that allows creating review items does not allow approving those review items.

No agent permission scope may include self-approval.

## Relationship To External Integrations

External provider permissions must remain bounded and subordinate to Neon Ronin rules.

External platform permissions do not define Neon Ronin authority.

Provider-specific fields belong in future integration contracts, not generic permission scope fields.

## Forbidden Fields

Do not add fields such as:

```text
api_key
provider_token
oauth_refresh_token
password
secret_value
all_workspace_private_data_access
self_approval_allowed
ignore_review_gates
bypass_lifecycle
raw_customer_data_global_access
etsy_publish_token
printify_api_key
fiverr_message_token
custom_data
```

Use future secrets/credentials contracts, external references, and explicit bounded scopes instead.

## Example Record

```yaml
permission_scope_id: perm_signal_capture_internal_001
scope_name: Signal Capture Agent Internal Research Scope
scope_status: active
actor_type: agent
actor_id: agent_signal_capture
workspace_scope:
  scope_type: workspace_ids
  workspace_ids:
    - ws_internal_research_001
  workspace_types:
    - internal_research
  cross_workspace_private_data_access: false
allowed_action_classes:
  - read
  - analyze
  - draft
  - queue
allowed_resource_types:
  - workspace_config
  - artifact
  - signal_candidate
  - review_item
  - audit_record
allowed_runtime_modes:
  - on_demand
required_review_gates:
  - signal_sanitization_gate
audit_requirements:
  - permission_allowed_action_used
  - permission_denied_action
  - review_item_created
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
description: Allows the Signal Capture Agent to read internal research artifacts, draft signal candidates, and queue sanitization review items.
expires_at: null
granted_by_human_decision_id: hdec_001
revoked_by_human_decision_id: null
allowed_workspace_types:
  - internal_research
denied_action_classes:
  - live_write
  - destructive
denied_resource_types:
  - credential_reference
external_provider_scope: null
observatory_scope:
  can_query: true
  allowed_query_types:
    - keyword_cluster
    - prior_signal_check
    - data_quality_check
  can_submit_signal_candidates: true
  can_submit_sanitized_signals: false
  signal_submission_requires_human_review: true
data_access_rules:
  workspace_private_data: read_limited
  customer_data: none
  credentials: none
  external_payloads: bounded_references_only
  artifact_content: workspace_scoped_allowed
conditions:
  - Workspace must remain in manual_test or active status.
  - Signal candidates must go to human sanitization review.
  - Agent may not approve its own work.
version: 1
```

## Validation Questions

Before accepting a permission scope, answer:

1. Is the actor explicit and traceable?
2. Is workspace scope bounded?
3. Is cross-workspace private data access false unless explicitly justified by a future governance rule?
4. Are action classes explicit?
5. Are denied action classes explicit where needed?
6. Are required review gates preserved?
7. Does the scope obey workspace lifecycle and runtime constraints?
8. Does the scope avoid self-approval?
9. Does the scope avoid credentials, tokens, and raw secrets?
10. Does it avoid provider-specific payloads in core?
11. Is a human decision linked when approval is required?
12. Are audit requirements explicit?
13. Does denial win over allowance?
14. Does it avoid unbounded metadata/custom data?

## Non-Goals

This schema does not define:

- authentication
- user accounts
- secrets storage
- OAuth implementation
- provider permission APIs
- role-based access control UI
- database tables
- multi-user organization model

## Final Rule

```text
Permission grants capability only inside every other boundary.
```
