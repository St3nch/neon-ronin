# 12 - System Invariants

## Purpose

This document defines the non-negotiable conditions that must remain true for Neon Ronin to remain Neon Ronin.

An invariant is stronger than a preference.

An invariant is a boundary that protects the platform from drift, convenience shortcuts, first-business contamination, unsafe automation, and schema sprawl.

## Core Rule

```text
If a change violates a Neon Ronin invariant, the change is wrong until the invariant is explicitly revised through an ADR.
```

Implementation convenience is not a valid reason to violate an invariant.

A better demo is not a valid reason to violate an invariant.

A first-business need is not a valid reason to violate an invariant.

## Invariant Definition

A Neon Ronin invariant is a condition that must remain true across:

- docs
- schemas
- workflows
- workspace adapters
- agent behavior
- review gates
- Observatory behavior
- operations docs
- future code
- future database design
- future integrations

If an invariant appears inconvenient, the correct response is to redesign around it, not quietly bypass it.

## Invariant 1 - Neon Ronin Hosts Workspaces

Neon Ronin is the operating system.

Each small business, experiment, project, or research effort is a workspace.

Core must not become one workspace's backend.

```text
Neon Ronin hosts workspaces.
Neon Ronin does not become a workspace.
```

Violations include:

- adding one business's report language to core
- adding one marketplace's fields to core records
- adding SearchClarity-specific workflow assumptions to core
- treating a workspace adapter as the whole platform
- naming core schemas after one business or channel

## Invariant 2 - Workspaces Are Isolated By Default

Every workspace is isolated unless a specific, governed boundary allows data to move.

Workspaces must not directly access another workspace's:

- private data
- customer records
- drafts
- artifacts
- credentials
- customer history
- workspace-local strategy
- external account records

Allowed cross-workspace learning happens only through the Observatory and only through approved sanitized signals.

## Invariant 3 - The Observatory Is The Only Cross-Workspace Intelligence Channel

The Observatory is the sanctioned shared intelligence layer.

It receives sanitized signals and returns generalized intelligence.

It is not a backdoor into another workspace.

```text
Workspace A may query generalized Observatory intelligence.
Workspace A may not query Workspace B private data.
```

Any design that creates a second cross-workspace intelligence path must be rejected or promoted through an ADR.

## Invariant 4 - Private Workspace Data Does Not Enter The Observatory

The Observatory must not receive raw private workspace data.

Only sanitized, generalized intelligence may enter the Observatory.

Forbidden Observatory data includes:

- raw customer data
- credentials
- unsanitized customer notes
- private drafts
- confidential business details
- exact report text
- exact marketplace listing copy
- raw customer files
- raw payment/order data

Sanitization is not optional.

## Invariant 5 - Human Approval Gates Risky Actions

Humans remain the final decision-makers for risky actions.

Risky actions include:

- public-facing actions
- customer-facing actions
- paid actions
- credential changes
- destructive actions
- publishing
- customer messaging
- delivery to customers
- legal, IP, compliance, or rights decisions

Agents may prepare, recommend, draft, queue, and summarize.

Agents must not independently approve or execute risky actions.

## Invariant 6 - No Agent Approves Its Own Work

No agent may approve, publish, deliver, or finalize its own output.

Agent output requiring review must pass through a review gate.

This applies to:

- deliverables
- listing drafts
- content drafts
- sanitized signal candidates
- external action requests
- paid action requests
- credential or permission changes

Human review decisions must be auditable.

## Invariant 7 - Manual Workflow Proof Comes Before Automation

A workflow must be understood manually before Neon Ronin automates it.

```text
Manual first.
Assisted second.
Automated later.
```

Violations include:

- scheduled jobs before manual validation
- watch mode before manual validation
- external writes before manual workflow proof
- agent delegation chains before a single-agent/manual version works
- marketplace publishing before launch workflow proof

Automation is earned.

## Invariant 8 - Workspace Capability Follows Lifecycle Maturity

A workspace earns capability by passing lifecycle gates.

Workspace status controls what is allowed.

Examples:

- `idea` workspaces cannot run agents
- `onboarding` workspaces cannot execute external actions
- `manual_test` workspaces cannot run scheduled jobs or watch mode
- `paused` workspaces cannot start new work
- `retired` workspaces are read-only by default

A workflow cannot bypass lifecycle gates because it is convenient.

## Invariant 9 - Core Schemas Remain Business-Neutral

Core schemas must model reusable platform concepts.

They must not model one business, one channel, one marketplace, one provider, or one service offer as if it were universal.

Good core concepts:

- workspace
- agent
- run
- artifact
- review item
- human decision
- signal
- audit record
- permission scope
- external reference

Bad core concepts:

- SearchClarity report section
- Etsy listing draft field inside a generic artifact
- Printify product wizard state inside core workspace config
- Fiverr gig package baked into core schema
- one business's pricing tier as a platform enum

## Invariant 10 - Every Durable Record Has An Owner

Every durable record must be classified before it becomes schema.

Valid ownership categories include:

- core-owned data
- workspace-owned data
- Observatory-owned data
- adapter-owned pattern
- integration-owned record
- referenced-only data
- derived data
- forbidden-in-core data

If ownership is unclear, the record is not ready.

## Invariant 11 - Derived Output Does Not Replace Canonical Source Records

Derived outputs must remain labeled as derived.

A derived output may inform a human decision.

It must not replace the source records it summarizes or interprets.

Examples:

```text
A score is not a decision.
A recommendation is not approval.
A draft is not a deliverable.
A signal summary is not raw evidence.
A QA summary is not the review decision.
```

Derived output must preserve provenance back to source records.

## Invariant 12 - Provenance Must Remain Traceable

Important records must preserve enough provenance to explain:

- what the record is
- where it came from
- when it was created or captured
- who or what created it
- what workspace it belongs to
- whether it is raw, structured, sanitized, normalized, or derived
- what source artifacts, runs, decisions, or signals informed it

If provenance is lost, trust is lost.

## Invariant 13 - Auditability Is Required For Meaningful State Change

Meaningful state changes must create audit records.

This includes:

- agent runs
- review decisions
- workspace status changes
- runtime mode changes
- signal submissions
- signal approvals
- external API calls
- publish attempts
- paid action attempts
- credential changes
- permission changes
- workflow config changes
- emergency stop events

Rejected, failed, parked, or blocked actions remain auditable.

## Invariant 14 - Deferred Domains Do Not Get Ad Hoc Schema

Deferred domains must not appear in core schema as convenience fields, temporary tables, or speculative enums.

Deferred domains currently include:

- Etsy integration
- Printify integration
- Fiverr automation
- marketplace publishing
- Tauri UI
- LangGraph integration
- Hermes integration
- scheduled agents
- watch mode
- multi-user roles
- cloud sync
- plugin marketplaces

Deferred does not mean forgotten.

Deferred means not allowed to mutate core schema until promoted through the roadmap.

## Invariant 15 - Explicit Schema Beats JSON Sludge

Neon Ronin should prefer explicit schema for important meaning.

JSON fields may exist only when bounded and justified.

Bad pattern:

```text
custom_data: { anything goes }
```

Acceptable pattern:

```text
provider_payload_snapshot: bounded integration-owned payload, not core semantic truth
```

If important system meaning hides inside arbitrary JSON, the schema boundary has failed.

## Invariant 16 - External Integrations Are Subordinate To Core Rules

External integrations may connect Neon Ronin to outside systems.

They must not override Neon Ronin's rules.

External integrations must obey:

- workspace isolation
- workspace lifecycle
- runtime modes
- review gates
- permissions
- audit logging
- credential rules
- human approval requirements
- hard-no automation rules

An external platform's convenience does not determine Neon Ronin's safety model.

## Invariant 17 - Research Does Not Override Doctrine

Research docs are supporting context.

They do not define platform authority unless promoted through core docs, adapter docs, operations docs, schema docs, or ADRs.

```text
Use research as evidence.
Use core docs and ADRs as authority.
```

Concrete examples in research docs are examples, not platform doctrine.

## Invariant 18 - The First Business Is A Proving Ground, Not The Platform

The first real business may expose useful requirements.

It must not define Neon Ronin core.

Every first-business-driven feature must be classified as:

1. core platform capability
2. workspace adapter capability
3. workspace-specific configuration or documentation
4. external integration
5. out-of-scope distraction

```text
Neon Ronin may learn from the first business.
Neon Ronin must not become the first business.
```

## Invariant 19 - Review Gates Cannot Be Bypassed By Permissions

Permissions should enforce review gates, not route around them.

No agent, integration, workflow, or runtime mode should gain direct permission to execute an action that requires review.

If an action requires human approval, the permission system must preserve that requirement.

## Invariant 20 - Paused And Retired Workspaces Cannot Start New Work

Paused workspaces preserve state but block new work.

Retired workspaces are read-only by default.

No scheduled job, watch-mode job, agent run, review item generation, signal submission, or external action should start from a paused or retired workspace.

Emergency stop overrides all workspace activity.

## Invariant 21 - Cross-Workspace Query Results Must Be Generalized

Observatory query results must not expose another workspace's private details.

They should return:

- summaries
- clusters
- scores
- patterns
- confidence bands
- data quality notes
- generalized recommendations

They should not return:

- raw source signals
- source customer identity
- source workspace private data
- raw artifacts
- exact customer text
- exact private evidence

## Invariant 22 - Neon Ronin Must Remain Legible To Capable LLMs

The repo is LLM-first.

Future LLMs and coding agents must be able to understand:

- what Neon Ronin is
- what Neon Ronin is not
- which docs are canonical
- what belongs in core
- what belongs in workspaces
- what belongs in adapters
- what belongs in integrations
- what belongs in the Observatory
- what is forbidden or deferred

Docs, schemas, and naming should reduce ambiguity rather than require hidden context.

## Invariant Violation Response

When a proposed change appears to violate an invariant:

1. Stop.
2. Name the invariant at risk.
3. Classify the proposed change.
4. Redesign the change within the invariant if possible.
5. If the invariant itself may be wrong, create or update an ADR.
6. Do not normalize the violation as a temporary shortcut.

Temporary shortcuts become permanent architecture by accident.

## Relationship To Other Docs

This document depends on:

- `docs/core/01-platform-doctrine.md`
- `docs/core/02-workspace-model.md`
- `docs/core/03-business-onboarding.md`
- `docs/core/04-observatory.md`
- `docs/core/05-agent-runtime.md`
- `docs/core/06-review-queue.md`
- `docs/core/07-permissions-and-audit.md`
- `docs/core/08-sanitization.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/core/11-data-boundaries.md`
- `docs/decisions/adr-002-research-docs-are-supporting-context.md`
- `docs/decisions/adr-003-first-business-containment.md`
- `docs/decisions/adr-004-observatory-shared-intelligence-boundary.md`

Future schema, operations, and implementation docs must not contradict these invariants without an ADR.

## Final Rule

```text
If the shortcut makes Neon Ronin easier by making its boundaries weaker, reject the shortcut.
```
