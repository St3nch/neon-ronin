# 08 - Sanitization

## Purpose

This document defines how workspace-private observations become Observatory-eligible signals without leaking private workspace, customer, credential, or confidential business data.

The Observatory is Neon Ronin's shared intelligence layer. It may learn from workspaces only through sanitized signals.

Sanitization is the boundary between private workspace data and shared platform intelligence.

## Core Rule

```text
Private workspace data does not enter the Observatory.
Only sanitized, generalized intelligence may enter the Observatory.
```

A signal is Observatory-eligible only when it contains reusable intelligence and no private workspace/customer details.

## Why Sanitization Exists

Workspaces may observe useful patterns during real work:

- repeated customer needs
- keyword patterns
- marketplace gaps
- weak competitor patterns
- common report findings
- product or service opportunity signals
- workflow problems
- quality issues
- recurring questions

Some of that information may help other workspaces.

But raw workspace observations may contain private, identifying, confidential, or business-specific details.

Sanitization converts raw observations into generalized intelligence that can safely support the broader Neon Ronin platform.

## Terms

| Term | Meaning |
|---|---|
| Raw Signal | An unsanitized observation created inside a workspace |
| Signal Candidate | A proposed sanitized version waiting for review or validation |
| Sanitized Signal | An approved generalized signal eligible for Observatory intake |
| Rejected Signal | A signal candidate blocked from Observatory intake |
| Parked Signal | A signal candidate held for later review or more evidence |
| Signal Source | The workspace, agent, human, artifact, or workflow that produced the observation |
| Sanitization Gate | The review or validation step that determines whether a signal may enter the Observatory |

## Signal Flow

```text
Workspace observes something useful
-> workspace creates raw signal
-> raw signal stays workspace-private
-> agent or human drafts signal candidate
-> signal candidate enters sanitization gate
-> human approves, edits, rejects, requests revision, escalates, or parks
-> approved sanitized signal enters Observatory inbox
-> Observatory normalizes, deduplicates, scores, or queues signal
```

## What May Become A Sanitized Signal

Sanitized signals may include generalized versions of:

- keyword clusters
- niche or topic patterns
- broad customer need patterns
- generalized competitor weaknesses
- repeated workflow problems
- content gaps
- service demand patterns
- market opportunity observations
- quality issues that apply across workspaces
- reusable recommendation patterns
- data quality notes

## What Must Never Enter The Observatory

The Observatory must not receive:

- raw customer names
- customer emails
- customer phone numbers
- customer addresses
- customer usernames or handles
- shop URLs tied to a specific customer
- private screenshots
- raw credentials
- API keys
- OAuth tokens
- refresh tokens
- payment data
- order IDs tied to customers
- private customer notes
- workspace-private drafts
- confidential strategy details
- private report text
- exact customer requests when identifying
- full source documents from a customer or workspace
- personally identifying information unless explicitly approved and required

## Business-Specific Data That Should Stay Out

The Observatory should not store business-specific details unless they have been generalized.

Avoid sending:

- specific brand language
- service package names
- customer-facing promises
- pricing assumptions from one business
- private customer delivery rules
- one store's product names
- one business's internal positioning
- one workspace's private strategy
- exact report templates
- exact marketplace listing copy

These belong in the workspace, not the Observatory.

## Sanitization Transformations

Sanitization should transform private observations into generalized intelligence.

| Raw Detail | Sanitized Form |
|---|---|
| Customer name | remove |
| Customer email or phone | remove |
| Shop URL | remove or replace with marketplace/category context |
| Exact customer request | summarize into generalized need pattern |
| Exact report text | summarize into abstract finding |
| Exact listing copy | summarize into listing pattern |
| Exact business name | replace with workspace type if needed |
| Exact product title | replace with product category or niche cluster |
| Exact date/time | reduce precision if exact timing is identifying |
| Private screenshot | do not send; summarize non-identifying pattern |
| Credentials or tokens | remove; reject if present |
| Payment/order data | remove; reject if not safely separable |

## Required Signal Candidate Fields

A signal candidate should include:

- signal candidate id
- source workspace id
- source workspace type
- source actor type
- source actor id
- source artifact or run reference if applicable
- created timestamp
- proposed signal type
- generalized summary
- evidence summary
- private data removed flag
- remaining sensitivity rating
- recommended Observatory destination
- recommended review gate
- audit log reference

The source workspace id is used for traceability and audit. It should not be exposed through normal Observatory query results unless explicitly allowed.

## Sanitization Review Decisions

Signal sanitization approvals use the review queue decision model.

| Decision | Meaning |
|---|---|
| approve | Candidate may enter the Observatory |
| approve_with_changes | Human edits candidate before Observatory intake |
| reject | Candidate is blocked and remains auditable |
| request_revision | Candidate must be revised before another review |
| escalate | Candidate requires deeper privacy, policy, legal, or business review |
| park | Candidate is held without Observatory intake |

## Default Approval Rule

Early Neon Ronin should require human approval before any signal enters the Observatory.

```text
Agent-proposed sanitization is allowed.
Human approval is required for Observatory intake.
```

A later system may support deterministic or bulk approval for low-risk signal categories only after the sanitization rules and audit process are proven.

## Rejection Rules

A signal candidate must be rejected if it contains:

- credentials
- raw customer contact details
- payment data
- private customer files
- unapproved personally identifying information
- confidential business information that cannot be generalized
- exact customer-owned text that should not be shared
- data from a workspace that does not allow Observatory submission

Rejected signals must remain auditable.

## Parking Rules

A signal candidate may be parked when:

- the evidence is weak
- the signal may be useful but needs more examples
- the privacy risk is unclear
- the signal is too specific but may be generalizable later
- the reviewer wants to wait before adding it to the Observatory

Parked signals do not enter the Observatory.

## Sanitization Gate Requirements

Every sanitization gate must record:

- signal candidate id
- reviewer or decision actor
- decision
- decision timestamp
- reason or note
- fields changed if approved with changes
- linked audit record

No agent may approve its own signal candidate.

## Audit Requirements

The following actions must generate audit records:

- raw signal creation
- signal candidate creation
- sanitization review decision
- approved signal intake into Observatory
- rejected signal decision
- parked signal decision
- signal revision request
- signal escalation
- Observatory normalization
- Observatory deduplication
- Observatory query returning a signal-derived result

## Observatory Query Boundary

The Observatory may return generalized intelligence.

It should not expose:

- source customer identity
- source workspace-private details
- raw source artifacts
- raw signal text
- exact private evidence
- credentials or secrets
- any data that would allow easy re-identification of a customer or private workspace event

The Observatory should prefer returning summaries, clusters, scores, and generalized patterns rather than raw signal records.

## Re-Identification Risk Rule

A sanitized signal may still be unsafe if it is so specific that a person could infer the source customer, source business, or private event.

Signals should be generalized further, parked, or rejected when they are too specific.

Examples of risky specificity:

- a niche plus exact date plus exact platform plus unique customer context
- a rare customer problem described in detail
- a quote that can be searched online
- a shop or business detail that uniquely identifies the source

## Workspace Consent Rule

A workspace may submit sanitized signals to the Observatory only if its workspace config allows it.

Required workspace setting:

```yaml
observatory:
  can_submit_sanitized_signals: true
```

If this setting is false, signals from that workspace must remain workspace-private.

## Signal Sensitivity Ratings

Signal candidates should use a simple sensitivity rating before Observatory intake.

| Rating | Meaning | Default Action |
|---|---|---|
| low | General market or workflow pattern, no identifying details | Human review required early; eligible for approval |
| medium | Some specificity or business context remains | Human review required; likely needs editing |
| high | Contains private, identifying, sensitive, or confidential details | Reject, revise, or escalate |

## Early Implementation Rule

During early development, all signal categories should default to human review.

Do not automate signal approval until:

1. signal schema exists
2. sanitization rules are tested manually
3. audit logs prove traceability
4. rejected and parked signals remain auditable
5. low-risk categories are clearly defined

## Examples

### Good Sanitized Signal

```text
Multiple service-business customers ask for help understanding Etsy keyword competition. This may indicate demand for a reusable Etsy keyword education asset or service add-on.
```

Why it is acceptable:

- no customer identity
- no customer URL
- no private report text
- reusable market/service insight

### Bad Raw Signal

```text
Customer Jane Doe at janedoe@example.com with shop https://example.etsy.com asked us to rewrite her listing for 'Blue Floral Nurse Retirement Shirt' because her conversion rate dropped after March 3.
```

Why it is not acceptable:

- customer name
- email
- shop URL
- exact listing
- exact business event
- private customer context

### Improved Sanitized Version

```text
A service-business workflow observed demand for listing optimization help in retirement-gift niches. The pattern may support future research into gift-niche keyword education or service add-ons.
```

## Relationship To Review Queue

Signal sanitization approvals are review queue items.

They are not casual background operations.

A signal does not enter the Observatory until the sanitization review gate allows it.

## Relationship To Workspace Isolation

Sanitization does not remove the workspace isolation rule.

Workspaces remain isolated by default.

The Observatory is the only sanctioned cross-workspace intelligence channel, and it receives only sanitized signals.

## Final Principle

```text
The workspace owns private data.
The Observatory owns generalized intelligence.
Sanitization is the gate between them.
```
