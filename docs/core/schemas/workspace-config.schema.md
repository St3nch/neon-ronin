# Workspace Config Schema

## Purpose

This document defines the P0 workspace configuration schema for Neon Ronin.

A workspace config is the core-owned record that describes a workspace's identity, type, lifecycle status, permissions, runtime limits, review gates, Observatory access, storage posture, and hard-no rules.

Workspace config is the first P0 schema because every workflow, agent run, review item, audit record, signal, artifact, and future integration must be scoped to a workspace.

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

Neon Ronin core owns workspace configuration because the platform must know:

- which workspaces exist
- what type each workspace is
- what lifecycle status each workspace is in
- what runtime modes are allowed
- what agents may operate
- what review gates are required
- whether the workspace may query or submit to the Observatory
- what storage and privacy rules apply
- what hard-no rules apply

Workspace config must remain business-neutral.

It must not contain detailed customer records, business-specific report text, marketplace-specific payloads, or one workspace's private operating database.

## Core Rule

```text
A workspace config defines platform boundaries for a workspace.
It does not contain the workspace's private business data.
```

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `workspace_id` | string | system-owned | Stable unique workspace identifier |
| `workspace_name` | string | human/config-owned | Human-readable workspace name |
| `workspace_type` | enum | human/config-owned | Type of workspace |
| `status` | enum | system-governed | Workspace lifecycle status |
| `purpose` | string | human/config-owned | Short business-neutral purpose statement |
| `channels` | array enum | human/config-owned | Channels the workspace may operate in |
| `adapter` | string | human/config-owned | Workspace adapter id or name |
| `allowed_agents` | array string | human/config-owned | Agent ids or roles allowed in this workspace |
| `review_gates` | array string | human/config-owned | Required review gates for this workspace |
| `observatory` | object | human/config-owned | Observatory query/submission permissions |
| `storage_rules` | object | human/config-owned | Workspace storage and privacy posture |
| `runtime` | object | system-governed/config-owned | Runtime mode constraints |
| `hard_no_rules` | array string | human/config-owned | Workspace-specific hard-no automation rules |
| `audit_requirements` | array string | human/config-owned | Required audit events or audit posture |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `description` | string | human/config-owned | Longer workspace description |
| `workspace_slug` | string | system-owned or human/config-owned | Stable readable identifier if needed |
| `owner_actor_id` | string | human/config-owned | Human owner/operator actor id |
| `data_classification` | enum | human/config-owned | Overall sensitivity posture |
| `manual_test_goal` | string | human/config-owned | Manual test objective for onboarding/manual_test workspaces |
| `promotion_notes` | string | human/config-owned | Notes about readiness or promotion blockers |
| `external_references` | array object | integration-owned/referenced-only | External provider/resource references, not provider-specific fields |
| `tags` | array string | human/config-owned | Bounded organizational tags |
| `version` | integer/string | system-owned | Config version for future migration/change tracking |

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

Definitions live in `docs/core/glossary.md` and workspace adapter docs.

## Valid Workspace Statuses

Canonical values:

```text
idea
onboarding
manual_test
active
paused
retired
```

Status transitions are governed by `docs/core/09-workspace-lifecycle.md`.

A config may store current status, but status changes must follow lifecycle transition rules and generate audit records.

## Valid Channels

Initial channel values:

```text
marketplace
service_platform
direct_site
social_platform
content_platform
internal_research
external_provider
other
```

A channel is not automatically an integration.

A channel describes where the workspace operates. An integration describes a governed external system connection.

## Observatory Object

Required shape:

```yaml
observatory:
  can_query: boolean
  can_submit_sanitized_signals: boolean
  allowed_query_types:
    - keyword_cluster
    - trend_profile
    - competitor_pattern
    - opportunity_score
    - prior_signal_check
    - data_quality_check
  signal_submission_requires_human_review: true
```

Rules:

- `can_query` and `can_submit_sanitized_signals` are separate permissions.
- Early workspaces should require human review for all signal submissions.
- A workspace may query the Observatory only if `can_query` is true.
- A workspace may submit sanitized signals only if `can_submit_sanitized_signals` is true.
- Raw workspace data must never enter the Observatory.

## Storage Rules Object

Required shape:

```yaml
storage_rules:
  workspace_private_data: true
  generalized_signals_allowed_after_sanitization: boolean
  raw_customer_data_allowed: boolean
  external_credentials_allowed: boolean
  artifact_content_scope: workspace_private
```

Rules:

- `workspace_private_data` should default to true.
- `artifact_content_scope` should not imply global/core ownership of artifact contents.
- Credentials require future secrets/credentials rules before implementation.
- Customer data remains workspace-owned.

## Runtime Object

Required shape:

```yaml
runtime:
  default_mode: off | on_demand | paused
  allowed_modes:
    - off
    - on_demand
  scheduled_allowed: false
  watch_mode_allowed: false
  emergency_stop_supported: true
```

Rules:

- Runtime modes must obey workspace lifecycle status.
- `manual_test` workspaces may not use scheduled or watch mode.
- `paused` and `retired` workspaces may not start new work.
- Emergency stop overrides all runtime modes.

## Review Gates

Review gates should reference canonical review gate terms.

Common values:

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
```

A workspace config may define which gates apply, but review queue schemas define review item details.

## Hard-No Rules

Global hard-no rules always apply:

```text
no_autonomous_publishing
no_autonomous_spending
no_autonomous_customer_messaging
no_autonomous_credential_changes
no_autonomous_destructive_actions
no_agent_self_approval
```

Workspace-specific hard-no rules may add stricter limits.

Workspace-specific hard-no rules must not weaken global hard-no rules.

## System-Owned Fields

The following fields should be system-owned:

- `workspace_id`
- `created_at`
- `updated_at`
- `version`
- lifecycle transition audit references when implemented

Agents and workspace configs must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless a governed migration allows change:

- `workspace_id`
- original `created_at`
- original source/intake reference when added later

Other fields may change through governed config updates, but meaningful changes must generate audit records.

## Lifecycle Rules

Workspace config must obey lifecycle rules from `docs/core/09-workspace-lifecycle.md`.

Examples:

- `idea` workspaces cannot run agents.
- `onboarding` workspaces cannot execute external writes.
- `manual_test` workspaces cannot use scheduled jobs or watch mode.
- `active` workspaces may use approved modes only if configured.
- `paused` workspaces cannot start new work.
- `retired` workspaces are read-only by default.

## Provenance Requirements

Workspace config should preserve or reference:

- who created the workspace config
- when it was created
- what business idea or intake led to it, once business intake schema exists
- what adapter was selected
- why the workspace type was chosen
- any promotion/review records related to lifecycle changes
- audit records for config updates

## Audit Requirements

The following events must generate audit records:

- workspace config created
- workspace config updated
- workspace status changed
- workspace runtime mode changed
- Observatory permission changed
- allowed agent list changed
- review gate list changed
- storage/privacy rule changed
- hard-no rule changed
- workspace paused
- workspace retired
- workspace promoted to manual test or active

## Relationships To Other Records

Workspace config will be referenced by:

- agent definitions and assignments
- agent runs
- review queue items
- audit records
- signal records
- artifact metadata
- workflow records
- Observatory query audit records
- future integration references

Other records must not operate without workspace scope unless explicitly global/core-owned.

## Forbidden Fields

Do not add fields such as:

```text
business_specific_report_template
etsy_shop_id
etsy_listing_id
printify_product_id
fiverr_gig_package
customer_email
customer_name
customer_order_history
raw_customer_notes
private_report_text
marketplace_listing_payload
provider_token
api_key
custom_data
```

Use workspace-owned records, integration-owned records, external references, or future governed schemas instead.

## Bounded Metadata

Workspace config may eventually allow bounded metadata, but not as a dumping ground.

Any metadata field must define:

- purpose
- allowed keys or value types
- whether it is queryable
- whether it is canonical meaning
- what must not be stored there

Until then, avoid generic `metadata` or `custom_data` fields.

## Example Record

```yaml
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
status: manual_test
purpose: Research and evaluate business ideas, platform decisions, and opportunity signals before onboarding real business workspaces.
channels:
  - internal_research
adapter: internal-research-workspace
allowed_agents:
  - research_agent
  - pattern_analysis_agent
  - scoring_agent
  - qa_agent
  - signal_capture_agent
review_gates:
  - quality_gate
  - strategy_review_gate
  - signal_sanitization_gate
observatory:
  can_query: true
  can_submit_sanitized_signals: true
  allowed_query_types:
    - keyword_cluster
    - trend_profile
    - prior_signal_check
    - data_quality_check
  signal_submission_requires_human_review: true
storage_rules:
  workspace_private_data: true
  generalized_signals_allowed_after_sanitization: true
  raw_customer_data_allowed: false
  external_credentials_allowed: false
  artifact_content_scope: workspace_private
runtime:
  default_mode: on_demand
  allowed_modes:
    - off
    - on_demand
    - paused
  scheduled_allowed: false
  watch_mode_allowed: false
  emergency_stop_supported: true
hard_no_rules:
  - no_autonomous_publishing
  - no_autonomous_spending
  - no_autonomous_customer_messaging
  - no_autonomous_credential_changes
  - no_autonomous_destructive_actions
  - no_agent_self_approval
audit_requirements:
  - workspace_config_created
  - workspace_status_changed
  - agent_run_created
  - review_decision_recorded
  - signal_submission_reviewed
manual_test_goal: Validate workspace config, artifacts, review queue, audit records, and sanitized signal flow without external writes.
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
version: 1
```

## Validation Questions

Before accepting a workspace config, answer:

1. Is the workspace type valid?
2. Is the lifecycle status valid?
3. Are runtime modes allowed for the lifecycle status?
4. Are Observatory permissions explicit?
5. Are review gates defined?
6. Are hard-no rules at least as strict as global rules?
7. Does the config avoid business-specific private data?
8. Does it avoid provider-specific fields?
9. Does it preserve enough provenance and audit posture?
10. Could another workspace type use the same core schema?

## Non-Goals

This schema does not define:

- customer records
- artifact content
- specific-business report formats
- marketplace listing payloads
- provider credentials
- external integration details
- workflow step schemas
- agent run details
- review item details
- signal lifecycle details
- database tables

## Final Rule

```text
A workspace config is a boundary contract, not a business database.
```
