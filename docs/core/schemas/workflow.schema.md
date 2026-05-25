# Workflow Schema

## Purpose

This document defines the P1 workflow schema for Neon Ronin.

A workflow is a structured sequence of steps used to move work from an input or trigger to one or more outputs, review gates, decisions, artifacts, signals, or audit records.

Workflow records exist so Neon Ronin can describe repeatable manual and assisted work before automation is introduced.

## Schema Status

```text
P1 planning schema
```

This is an implementation-facing planning document.

It is not yet a database migration, JSON Schema file, Pydantic model, TypeScript type, or API contract.

## Ownership Category

Workflow ownership may vary by scope:

| Workflow Layer | Ownership |
|---|---|
| Generic platform workflow pattern | Core-owned data |
| Workspace-specific workflow config | Workspace-owned or workspace-scoped data |
| Adapter workflow pattern | Adapter-owned pattern |
| External provider workflow details | Integration-owned record later |

## Core Rule

```text
A workflow describes controlled work.
It does not bypass lifecycle, runtime, permissions, review gates, or audit rules.
```

Workflow definition is not automation permission.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `workflow_id` | string | system-owned | Stable unique workflow id |
| `workflow_name` | string | human/config-owned | Human-readable workflow name |
| `workflow_type` | enum | human/config-owned | Type/category of workflow |
| `scope_type` | enum | human/config-owned | core, adapter, workspace, or integration scope |
| `workspace_id` | string/null | referenced-only | Workspace id if workspace-scoped |
| `adapter_id` | string/null | referenced-only | Adapter id if adapter-scoped |
| `status` | enum | system-governed | Workflow definition status |
| `allowed_workspace_types` | array enum | human/config-owned | Workspace types this workflow supports |
| `allowed_lifecycle_statuses` | array enum | human/config-owned | Workspace lifecycle statuses where this workflow may run |
| `allowed_runtime_modes` | array enum | human/config-owned | Runtime modes where this workflow may run |
| `steps` | array object | human/config-owned | Ordered workflow steps |
| `required_review_gates` | array enum | human/config-owned | Gates required by this workflow |
| `expected_inputs` | array object | human/config-owned | Inputs required or accepted |
| `expected_outputs` | array object | human/config-owned | Outputs expected from the workflow |
| `audit_requirements` | array string | human/config-owned | Audit events required |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `description` | string | human/config-owned | Longer workflow description |
| `version_label` | string/null | system/human-owned | Human-readable workflow version |
| `trigger_types` | array enum | human/config-owned | Allowed triggers |
| `allowed_agents` | array string | human/config-owned | Agents allowed to participate |
| `forbidden_actions` | array string | human/config-owned | Workflow-specific hard-no actions |
| `handoff_rules` | object | human/config-owned | Rules for handoff between steps/review/outputs |
| `failure_behavior` | object | human/config-owned | Failure/block behavior |
| `provenance_requirements` | array string | human/config-owned | Required provenance links |
| `tags` | array string | bounded/human-owned | Bounded organizational tags |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Workflow Types

Initial workflow types:

```text
business_intake
manual_research
report_production
artifact_review
customer_delivery
signal_capture
signal_sanitization
observatory_handoff
workspace_promotion
qa_review
external_action_request
internal_strategy
other
```

Workflow types should remain business-neutral.

Do not create specific-business, provider-specific, or marketplace-specific workflow types in core.

## Scope Types

Canonical values:

```text
core
adapter
workspace
integration
```

Rules:

- `core` workflows must be reusable platform workflows
- `adapter` workflows belong to workspace-type patterns
- `workspace` workflows are specific to one workspace
- `integration` workflows belong to future integration-specific contracts

## Valid Statuses

Canonical workflow statuses:

```text
draft
manual_test
active
paused
deprecated
retired
```

A workflow marked `active` still must obey workspace lifecycle, runtime, permission, and review constraints.

## Workflow Step Object

Recommended step shape:

```yaml
steps:
  - step_id: step_001
    step_name: Capture intake
    step_type: human_task | agent_task | review_gate | artifact_creation | signal_capture | external_reference | decision | audit_event
    required: true
    actor_type: human | agent | system | integration
    allowed_agent_ids: []
    input_refs:
      - business_intake
    output_refs:
      - artifact
    review_gate: null
    audit_event_type: workflow_step_completed
```

A workflow step defines expected structure.

It must not embed raw private payloads or provider-specific API bodies.

## Step Types

Canonical step types:

```text
human_task
agent_task
review_gate
artifact_creation
signal_capture
signal_sanitization
external_action_request
external_draft
human_decision
audit_event
handoff
blocked_or_escalated
```

Step types do not grant permission.

## Trigger Types

Canonical trigger types:

```text
human_started
workspace_created
business_intake_completed
review_requested
agent_run_completed
signal_candidate_created
manual_test_started
scheduled
watch_mode
external_event
unknown
```

Early workflows should primarily be `human_started`.

`scheduled`, `watch_mode`, and `external_event` remain deferred unless promoted later.

## Expected Inputs

Expected input objects should define input type and owner boundary.

Example:

```yaml
expected_inputs:
  - input_type: business_intake
    required: true
    ownership: workspace_owned
  - input_type: artifact
    required: false
    ownership: workspace_owned
```

Inputs are references, not payload dumps.

## Expected Outputs

Expected output objects should define output type and review needs.

Example:

```yaml
expected_outputs:
  - output_type: artifact
    artifact_type: draft_report
    requires_review: true
  - output_type: review_queue_item
    review_type: quality_review
    requires_review: true
```

Outputs are not automatically approved.

## Review Rules

Workflows must declare review gates for risky outputs/actions.

Review gates are required for:

- customer-facing outputs
- public-facing outputs
- publishing
- paid actions
- destructive actions
- credential or permission changes
- privacy-sensitive outputs
- rights/IP/compliance-sensitive outputs
- signal submission to the Observatory

## Runtime And Lifecycle Rules

A workflow may run only when:

1. workspace status allows it
2. runtime mode allows it
3. workflow status allows it
4. required agents are active and allowed
5. permissions allow it
6. hard-no rules are preserved
7. audit logging is available

Manual-test workflows may not use scheduled jobs or watch mode.

Paused or retired workspaces may not start new workflows.

## Handoff Rules

Workflow handoffs should be explicit.

Recommended shape:

```yaml
handoff_rules:
  artifacts_requiring_review_go_to_review_queue: true
  signal_candidates_go_to_sanitization_review: true
  external_action_requests_go_to_review_queue: true
  failed_steps_create_audit_record: true
  blocked_steps_escalate_to_human: true
```

## Failure Behavior

Recommended shape:

```yaml
failure_behavior:
  on_missing_input: block_or_request_revision
  on_permission_denied: block_and_audit
  on_review_required: create_review_item
  on_failed_step: create_audit_record
  on_missing_provenance: block_or_escalate
```

Failure must not silently proceed.

## System-Owned Fields

System-owned fields should include:

- `workflow_id`
- `created_at`
- `updated_at`
- system-computed status transition timestamps
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless governed migration allows change:

- `workflow_id`
- original `scope_type`
- original `created_at`

Workflow changes should be versioned or audited rather than silently overwritten.

## Provenance Requirements

Workflow records should preserve:

- creator actor
- why the workflow exists
- workspace/adapter/core scope
- supported workspace types
- required inputs and outputs
- review gates
- audit requirements
- version/change history

Workflow runs are captured by agent runs, audit records, and future job/run records.

## Audit Requirements

The following events must generate audit records:

- workflow created
- workflow updated
- workflow status changed
- workflow started
- workflow completed
- workflow failed
- workflow blocked
- workflow review gate triggered
- workflow output created
- workflow permission/runtime violation blocked

## Relationships To Other Records

Workflows may reference:

- workspace config
- workspace adapters
- agent definitions
- agent runs
- artifacts
- review queue items
- human decisions
- signals
- audit records
- business intake records
- external references

Workflows should not own artifact content, customer records, provider payloads, or human decisions.

## Forbidden Fields

Do not add fields such as:

```text
full_customer_request
private_report_text
provider_token
api_key
oauth_refresh_token
etsy_publish_payload
fiverr_message_text
business_specific_report_template_body
custom_data
```

Use references and future governed schemas instead.

## Example Record

```yaml
workflow_id: wf_service_report_manual_test
workflow_name: Service Report Manual Test Workflow
workflow_type: report_production
scope_type: adapter
workspace_id: null
adapter_id: service-business-workspace
status: manual_test
allowed_workspace_types:
  - service
allowed_lifecycle_statuses:
  - manual_test
  - active
allowed_runtime_modes:
  - on_demand
steps:
  - step_id: step_001
    step_name: Capture customer intake
    step_type: human_task
    required: true
    actor_type: human
    allowed_agent_ids: []
    input_refs:
      - business_intake
    output_refs:
      - intake_summary
    review_gate: null
    audit_event_type: workflow_step_completed
  - step_id: step_002
    step_name: Draft report artifact
    step_type: artifact_creation
    required: true
    actor_type: human
    allowed_agent_ids: []
    input_refs:
      - intake_summary
    output_refs:
      - draft_report
    review_gate: null
    audit_event_type: artifact_created
  - step_id: step_003
    step_name: Human QA review
    step_type: review_gate
    required: true
    actor_type: human
    allowed_agent_ids: []
    input_refs:
      - draft_report
    output_refs:
      - review_queue_item
    review_gate: quality_gate
    audit_event_type: review_item_created
required_review_gates:
  - quality_gate
  - customer_delivery_gate
expected_inputs:
  - input_type: business_intake
    required: true
    ownership: workspace_owned
expected_outputs:
  - output_type: artifact
    artifact_type: draft_report
    requires_review: true
  - output_type: review_queue_item
    review_type: quality_review
    requires_review: true
audit_requirements:
  - workflow_started
  - artifact_created
  - review_item_created
  - workflow_completed
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
version: 1
```

## Validation Questions

Before accepting a workflow record, answer:

1. Is the workflow type business-neutral?
2. Is ownership/scope clear?
3. Are lifecycle and runtime constraints explicit?
4. Are steps ordered and bounded?
5. Are expected inputs and outputs references rather than payload dumps?
6. Are review gates declared for risky outputs/actions?
7. Are audit requirements defined?
8. Does the workflow avoid provider-specific fields in core?
9. Does it avoid business-specific report/template content in core?
10. Does it avoid unbounded metadata/custom data?

## Non-Goals

This schema does not define:

- workflow engine implementation
- scheduler implementation
- watch mode implementation
- UI workflow builder
- provider API contracts
- artifact content schemas
- customer records
- database tables

## Final Rule

```text
A workflow is a controlled path, not an automation permission slip.
```
