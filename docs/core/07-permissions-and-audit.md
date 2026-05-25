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
