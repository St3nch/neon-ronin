# Internal Research Propose-Action Boundary Plan

## Status

```text
draft_boundary_plan
```

This document defines the boundary for future `propose_action` assistance in the Internal Research workspace.

It exists because Manual Test 003 showed that LLM draft assistance can produce reviewable artifacts safely, but proposing actions introduces a stronger risk: a proposed action may be mistaken for approved action, prepared action, or executable agent work.

This is not an agent definition.

This is not an agent runtime configuration.

This does not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.

## Source Evidence

```yaml
source_workspace_config: docs/workspaces/internal-research/workspace-config.draft.md
source_agent_assistance_boundary_plan: docs/workspaces/internal-research/agent-assistance-boundary-plan.md
source_manual_test_003_evidence: docs/workspaces/internal-research/manual-test-003-evidence.md
source_agent_runtime_doctrine: docs/core/05-agent-runtime.md
source_permissions_and_audit_doctrine: docs/core/07-permissions-and-audit.md
source_error_and_failure_doctrine: docs/core/16-error-and-failure-handling.md
source_transaction_boundaries: docs/core/20-transaction-boundaries.md
schema_version: propose_action_boundary_plan_v1
record_revision: 1
```

## Core Rule

```text
A proposed action is not an approved action.
A proposed action is not a prepared action.
A proposed action is not an executed action.
Human decision remains required before consequential work.
```

## Purpose

Define how Neon Ronin can safely test LLM-generated action proposals without granting permission to prepare, execute, automate, or delegate those actions.

The purpose is to preserve useful LLM judgment while preventing action-language from becoming stealth runtime authority.

## Current Workspace Posture

Internal Research currently remains:

```text
status: manual_test
runtime.default_mode: off
allowed_agents: []
scheduled_allowed: false
watch_mode_allowed: false
external_references: []
```

This boundary plan does not change that posture.

## Assistance Level Under Boundary

```text
propose_action
```

Definition:

```text
An LLM may propose a bounded next action as a reviewable artifact, but may not prepare action inputs, execute tools, change records, assign agents, change runtime, or contact external systems.
```

## Difference From Prior Levels

| Level | What It Allows | What It Does Not Allow |
|---|---|---|
| `recommend_only` | Suggest general next steps | No draft artifact or action proposal required |
| `draft_only` | Draft internal artifacts for review | No action proposal treated as pending execution |
| `propose_action` | Propose a bounded action for human review | No preparation, execution, scheduling, tool use, or runtime change |

## Allowed Proposal Types For Manual Testing

A `propose_action` test may propose only internal, non-executing actions such as:

- create another manual-test plan
- revise a documentation artifact
- request human review
- park a signal candidate
- add a risk note
- create a future boundary-plan draft
- update roadmap text after review

These proposals remain proposals only.

They do not authorize the proposed work.

## Forbidden Proposal Types

A `propose_action` test must block or park proposals involving:

- external writes
- customer messaging
- marketplace actions
- spending
- publishing
- credential use
- credential changes
- destructive actions
- live Observatory ingestion
- executable agent definitions
- agent runs
- scheduled jobs
- watch mode
- database implementation
- UI implementation
- integrations or provider API use

A forbidden proposal may be recorded as evidence, but the action remains blocked.

## Proposed Action Packet Shape

A proposed action should be represented as a reviewable packet:

```yaml
proposed_action_packet_id:
workspace_id:
source_question:
proposed_action_title:
proposed_action_summary:
action_class:
risk_level:
why_now:
expected_benefit:
required_review_gates:
blocked_action_checks:
human_decision_required: true
execution_allowed: false
preparation_allowed: false
schema_version: proposed_action_packet_v1
record_revision: 1
```

## Required Review Gates

Every proposed action packet must pass through:

- `quality_gate`
- `strategy_review_gate`
- `permission_review_gate`
- `audit_readiness_gate`
- `data_privacy_gate`

If the proposal touches signal flow, also require:

- `signal_sanitization_gate`

If the proposal could affect workspace posture, also require:

- `promotion_readiness_gate`

## Required Human Decision

A human operator must decide one of:

```text
approve_for_manual_planning
approve_with_changes
request_revision
reject
park
block
```

Important:

```text
approve_for_manual_planning does not mean execute.
```

It means the proposed action may become a future manual planning task or document update under separate review.

## Required Audit Expectations

Future implementation must eventually audit:

- action proposal requested
- proposed action packet created
- review item created
- human decision recorded
- blocked proposal recorded if applicable
- transition from proposal to planning task if later approved
- rejection/parking/blocking if not approved

This plan does not create real audit records in a database.

## Failure And Block Rules

| Situation | Required Result |
|---|---|
| LLM proposes allowed internal planning action | record packet and route to human review |
| LLM proposes external action | block or park; do not prepare or execute |
| LLM proposes credential use | block; record as forbidden proposal |
| LLM proposes executable agent definition | block; requires separate future approval path |
| LLM proposes runtime change | block; runtime remains off |
| LLM proposes scheduled/watch mode | block; scheduled/watch remain disabled |
| LLM proposes live Observatory ingestion | block; no live ingestion path exists |
| Human decision missing | block progression |
| Audit expectations unclear | block progression |
| Proposal has unclear action class | request revision or park |

## Test-Only Scope

A future Manual Test 004 for `propose_action` should use an internal, non-executing proposal such as:

```text
Propose the next safest manual-test plan for Internal Research after draft assistance.
```

The expected output should be a proposed action packet, not an executed task.

## Validation Questions

- Does this plan preserve human decision authority? Yes.
- Does this plan permit useful LLM action proposals? Yes, as reviewable packets only.
- Does this plan allow action preparation? No.
- Does this plan allow execution? No.
- Does this plan start agents? No.
- Does this plan change `allowed_agents`? No.
- Does this plan change runtime mode? No.
- Does this plan allow external writes, credentials, scheduled jobs, watch mode, or live Observatory ingestion? No.
- Does this plan name the next safe manual test? Yes: Manual Test 004 for propose-action assistance.

## Non-Goals

This plan does not define:

- executable agents
- agent ids
- agent prompts
- tool integrations
- action execution APIs
- provider connectors
- background jobs
- database tables
- API routes
- UI screens
- live Observatory ingestion
- automation

## Next Allowed Step

Create Manual Test 004 for `propose_action` assistance.

Do not draft executable agent definitions.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.