# 05 - Agent Runtime

## Purpose

This document defines the Neon Ronin agent runtime contract.

Agents are scoped workers. They do not have unlimited authority.

## Agent Contract

Every agent must define:

- agent id
- agent name
- workspace scope
- allowed inputs
- allowed outputs
- allowed tools
- allowed external calls
- forbidden actions
- review gates triggered by its output
- audit requirements

## Action Classes

| Class | Description | Autonomous? |
|---|---|---:|
| Read | Fetch or inspect approved data | Yes, within limits |
| Analyze | Transform, compare, or summarize data | Yes |
| Draft | Create internal drafts or packets | Yes, within limits |
| Queue | Add item to review queue | Yes |
| External Draft | Create a draft in an external system | Gated early |
| Live Write | Change public/customer/marketplace-visible state | No |
| Destructive | Delete, cancel, refund, revoke, remove | No |

## Runtime Modes

| Mode | Meaning |
|---|---|
| Off | No background work runs |
| On-Demand | Agents run only when started by the human |
| Scheduled | Approved jobs run on schedules |
| Watch Mode | Approved monitoring jobs run within limits |
| Paused | Existing state is saved, no new work starts |
| Emergency Stop | Active runs stop and new work is blocked |

## Hard-No Rules

```text
No autonomous publishing.
No autonomous spending.
No autonomous customer messaging.
No autonomous credential changes.
No autonomous destructive actions.
No agent approves its own work.
```

## Agent Output Rule

Agents should produce structured outputs:

- draft artifact
- research note
- review queue item
- signal candidate
- recommendation packet
- error report

## Review Gate Rule

If an output is public-facing, customer-facing, paid, risky, credential-related, or compliance-sensitive, it must enter human review before action.
