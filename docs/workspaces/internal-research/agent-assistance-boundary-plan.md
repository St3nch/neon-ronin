# Internal Research Agent-Assistance Boundary Plan

## Status

```text
draft_boundary_plan
```

This document defines the boundary for future agent-like assistance in the Internal Research workspace.

It exists because Manual Test 002 showed that LLM recommendations are useful as reviewable artifacts, but executable agent definitions are not yet authorized.

This is not an agent definition.

This is not an agent runtime configuration.

This does not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.

## Source Evidence

```yaml
source_workspace_config: docs/workspaces/internal-research/workspace-config.draft.md
source_manual_test_plan: docs/workspaces/internal-research/manual-test-002-llm-recommendation-assistance.md
source_manual_test_evidence: docs/workspaces/internal-research/manual-test-002-evidence.md
source_agent_runtime_doctrine: docs/core/05-agent-runtime.md
source_permissions_and_audit_doctrine: docs/core/07-permissions-and-audit.md
source_error_and_failure_doctrine: docs/core/16-error-and-failure-handling.md
schema_version: agent_assistance_boundary_plan_v1
record_revision: 1
```

## Core Rule

```text
Recommendation is not action.
Drafting is not permission.
A proposed action is not an approved action.
Human decision remains required before consequential work.
```

## Purpose

Define safe levels of LLM/agent-like assistance that Neon Ronin can test manually before any executable agent definitions are drafted.

The purpose is to preserve the value of LLM reasoning while preventing stealth runtime authority.

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

## Assistance Levels

| Level | Name | Description | Allowed Now? | Action Authority |
|---|---|---|---:|---|
| 0 | `no_assistance` | Human-only manual work | Yes | Human only |
| 1 | `recommend_only` | LLM produces recommendations as reviewable artifacts | Yes, in manual evidence passes | None |
| 2 | `draft_only` | LLM drafts internal artifacts, packets, notes, or checklists for review | Candidate for next manual test | None |
| 3 | `propose_action` | LLM proposes an action but cannot prepare or execute it | Candidate for later manual test | None |
| 4 | `prepare_action` | LLM prepares bounded action inputs for human execution | Not allowed yet | None without future approval |
| 5 | `execute_with_human_approval` | Agent executes a bounded action only after explicit human approval | Not allowed yet | Future governed action only |
| 6 | `autonomous_execution` | Agent executes without per-action human approval | Forbidden for current roadmap posture | Forbidden |

## Currently Allowed Assistance

Only Level 1 is validated by Manual Test 002:

```text
recommend_only
```

The LLM may:

- analyze provided project docs
- produce recommendation packets
- name risks and blocked actions
- suggest review gates
- propose future manual tests
- draft evidence summaries for human review

The LLM may not:

- assign agents
- change `allowed_agents`
- enable runtime modes
- create executable agent definitions
- invoke external tools as an agent
- create integrations
- perform scheduled work
- use watch mode
- submit live Observatory signals
- change workspace status
- make final approval decisions without the human operator

## Candidate Next Assistance To Test

The next assistance level worth testing manually is:

```text
draft_only
```

That test should prove whether an LLM can draft internal artifacts while remaining inside review/audit boundaries.

Candidate manual test:

```text
Manual Test 003 - LLM Draft Assistance
```

Expected scope:

- LLM drafts an internal research artifact
- human reviews artifact quality and boundaries
- human records approve/revise/reject/park decision
- blocked probes confirm no runtime action occurs
- optional signal candidate remains parked unless sanitized

## Agent Definition Gate

No executable agent definition may be drafted until all of the following are true:

- recommendation assistance boundary is documented
- at least one draft-only manual test is completed with human decision
- permission scopes for test-only agent behavior are specified
- audit expectations for agent-like assistance are specified
- failure/block behavior is specified
- review gates are specified
- workspace config explicitly allows a bounded test agent entry
- human operator approves the transition in a promotion/review document

## Test-Only Agent Candidate Boundary

A future test-only agent candidate, if later approved, must be constrained to:

```text
workspace: ws_internal_research_001
runtime: on_demand only
scheduled: false
watch_mode: false
external_integrations: none
external_writes: none
credentials: none
allowed_action_classes: read, analyze, draft
forbidden_action_classes: publish, spend, external_write, credential_change, destructive_action, live_observatory_ingestion
human_review_required: true
```

This boundary is planning guidance only.

It is not permission to create the agent definition yet.

## Required Review Gates Before Any Agent Definition Draft

Before drafting an executable agent definition, require:

- `quality_gate`
- `strategy_review_gate`
- `permission_review_gate`
- `audit_readiness_gate`
- `data_privacy_gate`
- `promotion_readiness_gate`

If any gate fails, the agent-definition draft must be blocked or parked.

## Required Audit Expectations

Future implementation must eventually audit:

- assistance request created
- LLM recommendation or draft produced
- review item created
- human decision recorded
- blocked action prevented
- runtime mode checked
- permission scope checked
- agent definition created if later authorized
- agent run started if later authorized
- agent run blocked/failed/completed if later authorized

This plan does not create real audit records in a database.

## Failure And Block Rules

| Situation | Required Result |
|---|---|
| LLM recommends action beyond current level | record recommendation; block action |
| LLM drafts executable config before approval | reject or park draft |
| LLM suggests external write | block and record as forbidden recommendation |
| LLM suggests scheduled/watch mode | block and record as forbidden recommendation |
| LLM suggests credential use | block and record as forbidden recommendation |
| Human decision missing | block progression |
| Audit expectation unclear | block progression |
| Workspace status not compatible | block progression |
| Runtime mode not compatible | block progression |

## Non-Goals

This plan does not define:

- executable agents
- agent ids
- agent prompts
- tool integrations
- external connectors
- background jobs
- database tables
- API routes
- UI screens
- live Observatory ingestion
- automation

## Validation Questions

- Does this plan preserve human decision authority? Yes.
- Does this plan allow useful LLM recommendations? Yes.
- Does this plan start agents? No.
- Does this plan draft executable agent definitions? No.
- Does this plan keep runtime off? Yes.
- Does this plan keep `allowed_agents: []` unchanged? Yes.
- Does this plan name the next safe manual test? Yes: LLM draft assistance.
- Does this plan block external actions, credentials, scheduled jobs, and watch mode? Yes.

## Next Allowed Step

Create Manual Test 003 for LLM draft assistance.

Do not draft executable agent definitions yet.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.