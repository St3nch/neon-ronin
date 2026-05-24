# 06 - Review Queue

## Purpose

This document defines the Neon Ronin human review queue model.

The review queue is where risky, public-facing, customer-facing, paid, or compliance-sensitive outputs wait for human approval.

## What Enters The Review Queue

- customer-facing deliverables
- public content drafts
- marketplace listing drafts
- publish requests
- paid action requests
- rights and compliance review items
- signal sanitization approvals
- credential or permission changes
- escalation packets

## Review Queue Item Structure

Every review item should include:

- review item id
- workspace id
- source agent
- output type
- created timestamp
- risk category
- required review gates
- linked artifacts
- recommended action
- human decision status
- audit log reference

## Human Decisions

| Decision | Meaning |
|---|---|
| approve | Item may proceed |
| approve_with_changes | Human modified item before approval |
| reject | Item is blocked |
| request_revision | Agent or operator must revise item |
| escalate | Requires deeper review |
| park | Hold without further action |

## Queue Rules

```text
No agent may approve its own output.
Review decisions must be logged.
Rejected items remain auditable.
Paused workspaces may not generate new review items.
```

## Review Queue Goal

The review queue exists to keep humans in control of risky actions while still allowing agents to assist with drafting, organizing, and research.
