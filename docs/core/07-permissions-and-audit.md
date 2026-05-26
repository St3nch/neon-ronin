# 07 - Permissions And Audit

## Purpose

This document defines workspace isolation, permission boundaries, and audit logging requirements for Neon Ronin.

## Workspace Isolation Rule

Every workspace is isolated by default.

Workspaces may not directly access:

- another workspace's private data
- another workspace's credentials
- another workspace's drafts
- another workspace's customer history
- another workspace's artifacts

The Observatory is the only sanctioned cross-workspace intelligence channel.

## Permission Scope

Permissions should be scoped to:

- workspace
- agent
- action class
- external service
- review state
- runtime mode

## Least Privilege Rule

```text
Agents receive the minimum permissions required to complete their task.
```

Agents should receive scoped tokens or temporary permissions where possible.

## Runtime Human-In-Loop Rule

Human-in-loop requirements apply to consequential runtime and workflow actions.

Future agents, workflows, and automation must not finalize, approve, publish, deliver, spend, submit, execute external actions, or move consequential work forward without the required human review gate.

Agents must not mark their own work as correct, final, approved, delivered, or safe to execute.

Planning documents may be assistant-drafted and operator-reviewed without requiring a canonical human-decision record for every low-risk refinement.

Canonical human-decision records are required for meaningful gates, including implementation start, schema authority changes, runtime enablement, agent enablement, integrations, external actions, customer-facing work, workspace promotion, and any action that would let automation move consequential work forward.

## Audit Requirements

The following actions must generate audit records:

- agent runs
- external API calls
- review decisions
- publish attempts
- paid actions
- credential changes
- workspace configuration changes
- signal submissions
- signal approvals

## Audit Record Fields

Every audit record should include:

- audit id
- workspace id
- actor type
- actor id
- action type
- timestamp
- target resource
- result status
- linked review item if applicable

## Relationship To Transaction Boundaries

Audit requirements are enforced through the transaction posture named in `docs/core/20-transaction-boundaries.md`.

The permissions layer must not allow actors to perform consequential state changes when required audit records cannot be created.

## Core Rules

```text
Audit logs should be immutable.
Rejected actions remain auditable.
Paused workspaces may not execute new actions.
No agent should bypass review gates through direct permissions.
Meaningful state changes and required audit records succeed or fail together.
```

If audit logging is unavailable, Neon Ronin must block new consequential work rather than create unaudited state changes.
