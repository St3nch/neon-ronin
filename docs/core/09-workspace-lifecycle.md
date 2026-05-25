# 09 - Workspace Lifecycle

## Purpose

This document defines the lifecycle states, allowed transitions, runtime limits, and promotion rules for Neon Ronin workspaces.

A workspace is not active just because it exists.

A workspace earns more capability only after boundaries, workflows, review gates, audit requirements, and manual tests are proven.

## Core Rule

```text
Workspace capability increases only when workspace maturity increases.
```

Neon Ronin should not allow high-risk runtime modes, external actions, customer-facing work, or marketplace-changing actions until the workspace has passed the required lifecycle gates.

## Workspace Statuses

| Status | Meaning |
|---|---|
| `idea` | A possible business or project concept has been captured but not yet structured |
| `onboarding` | The workspace is being defined, classified, scoped, and configured |
| `manual_test` | The workspace workflow is being tested manually before automation |
| `active` | The workspace is approved for normal controlled operation |
| `paused` | The workspace state is preserved, but no new work may start |
| `retired` | The workspace is closed for new work and kept only for history, audit, or export |

These statuses are part of the core workspace model.

## Status Definitions

### `idea`

The workspace is only a captured idea.

Allowed:

- record business idea
- classify possible workspace type
- draft rough notes
- compare against roadmap
- park or reject idea

Forbidden:

- agent runs
- external integrations
- customer work
- marketplace work
- Observatory submissions
- scheduled jobs
- watch mode

Exit paths:

- `idea -> onboarding`
- `idea -> retired`

### `onboarding`

The workspace is being shaped into a real workspace configuration.

Allowed:

- define purpose
- classify workspace type
- choose adapter
- identify workflows
- identify agents
- identify data sources
- identify outputs
- identify review gates
- identify hard-no rules
- identify Observatory permissions
- draft workspace config

Forbidden:

- autonomous agent runs
- scheduled jobs
- watch mode
- customer-facing delivery
- public publishing
- paid actions
- destructive actions
- external writes

Exit paths:

- `onboarding -> manual_test`
- `onboarding -> paused`
- `onboarding -> retired`

### `manual_test`

The workspace has enough structure to test workflows manually.

This is the default state for a new real workspace before automation.

Allowed:

- human-started manual workflow runs
- draft artifacts
- review queue items
- audit records
- signal candidates
- human-approved sanitized signal submission if configured
- on-demand agent assistance only if explicitly allowed

Forbidden by default:

- scheduled runtime
- watch mode
- autonomous external writes
- autonomous customer messaging
- autonomous customer delivery
- autonomous publishing
- autonomous spending
- autonomous destructive actions
- multi-agent delegation chains

Exit paths:

- `manual_test -> active`
- `manual_test -> paused`
- `manual_test -> retired`
- `manual_test -> onboarding` if the workspace needs redesign

### `active`

The workspace has passed manual validation and may operate under controlled rules.

Allowed, if configured:

- on-demand work
- approved scheduled jobs
- approved watch-mode jobs
- draft artifacts
- review queue workflows
- sanitized signal submission
- Observatory queries
- external draft actions behind gates

Still forbidden without explicit human approval:

- publishing
- customer messaging
- customer delivery
- spending
- credential changes
- destructive actions
- final legal, IP, compliance, or rights decisions

Exit paths:

- `active -> paused`
- `active -> retired`
- `active -> manual_test` if the workflow changes materially and needs revalidation

### `paused`

The workspace is temporarily stopped.

Allowed:

- view workspace records
- view audit logs
- export workspace data if permitted
- resume planning
- update configuration if approved
- move to retired

Forbidden:

- new agent runs
- new scheduled jobs
- new watch-mode jobs
- new review queue items
- new external actions
- new Observatory submissions

Exit paths:

- `paused -> active`
- `paused -> manual_test`
- `paused -> onboarding`
- `paused -> retired`

### `retired`

The workspace is closed for new operations.

Allowed:

- read historical records
- read audit logs
- export if permitted
- archive
- inspect lessons learned

Forbidden:

- new workflows
- new agent runs
- new review items
- new signals
- new external actions
- scheduled jobs
- watch mode
- reactivation without explicit decision

Exit paths:

- none by default

A future ADR may define a controlled reactivation process.

## Allowed Transitions

| From | To | Requirement |
|---|---|---|
| `idea` | `onboarding` | Human decides idea is worth structuring |
| `idea` | `retired` | Human rejects or archives idea |
| `onboarding` | `manual_test` | Workspace config draft and review gates exist |
| `onboarding` | `paused` | Human pauses onboarding |
| `onboarding` | `retired` | Human cancels onboarding |
| `manual_test` | `active` | Manual validation criteria passed |
| `manual_test` | `onboarding` | Workspace needs redesign |
| `manual_test` | `paused` | Human pauses testing |
| `manual_test` | `retired` | Human ends test |
| `active` | `paused` | Human pauses operations or system safety requires pause |
| `active` | `manual_test` | Material workflow change requires revalidation |
| `active` | `retired` | Human closes workspace |
| `paused` | `active` | Human resumes previously active workspace |
| `paused` | `manual_test` | Human resumes in test mode |
| `paused` | `onboarding` | Human resumes redesign |
| `paused` | `retired` | Human closes workspace |

Any transition not listed is forbidden by default.

## Runtime Modes By Workspace Status

| Workspace Status | Off | On-Demand | Scheduled | Watch Mode | Paused | Emergency Stop |
|---|---:|---:|---:|---:|---:|---:|
| `idea` | Yes | No | No | No | No | Yes |
| `onboarding` | Yes | Setup only | No | No | Yes | Yes |
| `manual_test` | Yes | Yes, human-started only | No | No | Yes | Yes |
| `active` | Yes | Yes | Yes, if approved | Yes, if approved | Yes | Yes |
| `paused` | Yes | No | No | No | Yes | Yes |
| `retired` | Yes | No | No | No | No | Yes |

## Runtime Rules

```text
Manual-test workspaces may not run scheduled jobs.
Manual-test workspaces may not run watch mode.
Paused workspaces may not start new work.
Retired workspaces are read-only by default.
Emergency stop overrides all workspace statuses.
```

## Promotion To Manual Test

A workspace may move from `onboarding` to `manual_test` only when it has:

- workspace name
- workspace type
- purpose
- basic workspace config
- supported channels listed
- expected inputs
- expected outputs
- initial workflows
- expected agents or human roles
- review gates
- hard-no automation rules
- data privacy notes
- Observatory query/submission settings
- audit requirements
- manual test goal

## Promotion To Active

A workspace may move from `manual_test` to `active` only when:

1. The manual workflow has been run enough times to be understood.
2. Required review gates have been used at least once where applicable.
3. Audit records can trace the work.
4. Workspace-private data boundaries are understood.
5. Observatory signal rules are tested if the workspace submits signals.
6. Rejected or parked review items remain auditable.
7. The human operator approves active status.
8. Any new automation is explicitly scoped.
9. Hard-no rules remain intact.

A workspace must not become active merely because it has a business idea or a draft config.

## Material Workflow Change Rule

A material workflow change should move an active workspace back to `manual_test` or `onboarding`.

Material changes include:

- new external integration
- new customer-facing deliverable type
- new marketplace or channel
- new agent with expanded permissions
- new data source containing private or customer data
- new Observatory signal category
- new paid action path
- new publishing path
- new automation mode
- major change to review gates

## Pause Rules

A workspace should be paused when:

- the human operator requests pause
- emergency stop affects the workspace
- cost caps are exceeded
- credentials are invalid or compromised
- audit logging fails
- review queue is blocked
- privacy boundary is uncertain
- external platform rules change materially
- a dangerous or unexpected agent behavior occurs

Paused means:

```text
state is preserved
new work is blocked
history remains auditable
```

## Retirement Rules

A workspace should be retired when:

- the business idea is rejected
- the experiment is complete
- the business is closed
- the workspace is replaced
- the workspace is no longer safe or useful
- the human decides it should not continue

Retired workspaces should remain auditable.

Retirement is not deletion.

## Review Gate Requirements By Lifecycle

| Status | Review Gate Behavior |
|---|---|
| `idea` | No operational review gates; planning only |
| `onboarding` | Review gates are designed but not exercised |
| `manual_test` | Review gates are exercised manually |
| `active` | Review gates enforce risky actions |
| `paused` | Existing review records remain visible; no new review items |
| `retired` | Review history remains visible; no new review items |

## Observatory Rules By Lifecycle

| Status | Observatory Query | Signal Submission |
|---|---:|---:|
| `idea` | No | No |
| `onboarding` | Planning only if approved | No |
| `manual_test` | Yes, if configured | Yes, human-approved only if configured |
| `active` | Yes, if configured | Yes, through sanitization gate if configured |
| `paused` | Read-only if needed | No |
| `retired` | Read-only historical/audit only | No |

## External Integration Rules By Lifecycle

| Status | External Reads | External Drafts | External Writes |
|---|---:|---:|---:|
| `idea` | No | No | No |
| `onboarding` | Planning only | No | No |
| `manual_test` | Human-approved only | Human-approved dry run only | No |
| `active` | If configured | If gated | Human-approved only if explicitly allowed |
| `paused` | No new reads | No | No |
| `retired` | No new reads | No | No |

## Audit Requirements

The following lifecycle events must generate audit records:

- workspace created
- status changed
- runtime mode changed
- workspace paused
- workspace resumed
- workspace retired
- workspace config changed
- manual test started
- manual test completed
- active promotion approved
- active promotion rejected
- material workflow change detected
- emergency stop triggered

## Workspace Lifecycle Record

Every lifecycle change should record:

- workspace id
- previous status
- new status
- actor type
- actor id
- timestamp
- reason
- linked review item if applicable
- linked audit record

## Default First Workspace Rule

The first real Neon Ronin workspace should be low-risk and internal.

Recommended first workspace:

```yaml
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
status: manual_test
```

Real business workspaces should wait until Neon Ronin has enough lifecycle, review, audit, and sanitization structure to contain them.

## Final Principle

```text
A workspace earns trust by passing gates.
More capability requires more proof.
```