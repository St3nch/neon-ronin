# 14 - Schema Authority

## Purpose

This document defines the governed schema authority for Neon Ronin before individual schema files are written.

It exists to answer:

```text
What schema families may Neon Ronin define, what does each family own, what must each family preserve, and what must not become schema yet?
```

Schema authority prevents ad hoc tables, business-specific core fields, provider-specific leakage, and JSON sludge from becoming the platform architecture.

## Core Rule

```text
A schema family is not allowed until its owner, purpose, boundaries, provenance, and non-goals are clear.
```

Do not create schemas because they seem useful.

Create schemas because they are governed platform records with clear ownership and boundaries.

## Relationship To Prior Docs

This document depends on:

- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`

Those docs define ownership, invariants, and provenance posture.

This doc applies those rules to schema families.

## Schema Authority Rule

The schema docs under `docs/core/schemas/` are implementation-facing planning docs.

They are not database migrations yet.

They should be precise enough to become:

- JSON Schema
- Pydantic models
- TypeScript types
- database tables
- API request/response contracts
- CLI validation contracts

But they should not pretend that storage technology has already been chosen.

## Schema Family Requirements

Every schema family must define:

- purpose
- ownership category
- scope
- required fields
- optional fields
- server/system-owned fields
- valid statuses or enums
- lifecycle rules
- provenance requirements
- audit requirements
- relationships to other records
- forbidden fields
- example record
- non-goals

If a schema cannot define those items yet, it is not ready.

## Governed Schema Families

The first governed Neon Ronin schema families are:

1. Workspace records
2. Workflow records
3. Agent records
4. Run and job records
5. Artifact records
6. Review records
7. Human decision records
8. Signal records
9. Observatory records
10. Audit records
11. Permission records
12. Integration reference records
13. Operations records

Each family is described below.

## 1. Workspace Records

### Purpose

Workspace records define the business or project containers Neon Ronin operates.

### Ownership

```text
Core-owned data
```

Workspace records are core-owned because Neon Ronin must know what workspaces exist, what lifecycle state they are in, what rules apply, and which adapters/configs they use.

### May Model

- workspace identity
- workspace type
- lifecycle status
- purpose
- channels
- adapter selection
- allowed agents
- review gates
- Observatory permissions
- storage rules
- runtime limits
- hard-no automation rules

### Must Not Model

- private customer records
- business-specific report text
- business-specific templates
- marketplace-specific payloads
- one workspace's detailed operating database
- specific-business service logic

### First Schema

```text
docs/core/schemas/workspace-config.schema.md
```

## 2. Workflow Records

### Purpose

Workflow records define reusable or workspace-scoped sequences of work.

### Ownership

Usually:

```text
Core-owned data or Workspace-owned data
```

A generic workflow definition may be core-owned. A concrete workspace workflow configuration is workspace-owned or workspace-scoped.

### May Model

- workflow name
- workflow type
- workspace scope
- allowed steps
- required review gates
- expected artifacts
- allowed agents
- trigger types
- lifecycle constraints
- runtime mode constraints

### Must Not Model

- provider-specific API behavior
- customer-private content
- channel-specific publishing payloads
- hidden bypasses around review gates

### Future Schema

```text
docs/core/schemas/workflow.schema.md
```

## 3. Agent Records

### Purpose

Agent records define scoped workers and their allowed capabilities.

### Ownership

```text
Core-owned data
```

Agent definitions are core platform records. Workspace-specific agent assignments are workspace-scoped configuration.

### May Model

- agent id
- agent role
- allowed action classes
- allowed workspace types
- allowed tools
- permission scopes
- review requirements
- runtime constraints
- output types

### Must Not Model

- unlimited authority
- self-approval rights
- hidden external write permissions
- provider-specific prompt hacks as core behavior
- business-specific promises

### First Schema

```text
docs/core/schemas/agent-definition.schema.md
```

## 4. Run And Job Records

### Purpose

Run and job records capture execution attempts, whether human-started, agent-started, scheduled later, or system-managed.

### Ownership

```text
Core-owned data
```

Runs and jobs are part of the platform runtime/audit surface.

### May Model

- run id
- job id
- workspace id
- triggering actor
- runtime mode
- input references
- output references
- status
- timestamps
- errors
- linked audit records

### Must Not Model

- raw customer payloads as generic run data
- unbounded arbitrary logs as canonical truth
- hidden cross-workspace inputs
- scheduled/watch behavior before those domains are promoted

### First Schema

```text
docs/core/schemas/agent-run.schema.md
```

Future:

```text
docs/core/schemas/job.schema.md
```

## 5. Artifact Records

### Purpose

Artifact records describe outputs or files produced by humans, agents, workflows, or integrations.

### Ownership

Metadata may be:

```text
Core-owned data
```

Artifact content is usually:

```text
Workspace-owned data
```

### May Model

- artifact id
- workspace id
- artifact type
- storage reference
- creator actor
- source run
- review status
- lifecycle status
- provenance references

### Must Not Model

- all artifact content in core by default
- customer-private deliverables as global data
- one business's report sections as core fields
- one marketplace's listing fields as generic artifact fields

### Future Schema

```text
docs/core/schemas/artifact.schema.md
```

## 6. Review Records

### Purpose

Review records define items awaiting human approval, rejection, revision, escalation, or parking.

### Ownership

```text
Core-owned data
```

Review queue mechanics are a platform capability.

### May Model

- review item id
- workspace id
- source actor
- risk category
- required gates
- linked artifacts
- linked signal candidates
- recommended action
- current decision status
- audit reference

### Must Not Model

- automatic approval by the source agent
- unreviewed risky actions as approved
- private artifact content directly in the review item unless workspace-scoped
- external execution as a side effect of item creation

### First Schema

```text
docs/core/schemas/review-queue-item.schema.md
```

## 7. Human Decision Records

### Purpose

Human decision records capture approvals, rejections, revisions, escalations, parking decisions, and other operator choices.

### Ownership

```text
Core-owned data
```

Human decisions are platform governance records.

### May Model

- decision id
- review item id
- actor id
- decision type
- decision timestamp
- decision notes
- changed fields
- linked audit record

### Must Not Model

- vague approval without a reviewed target
- agent approval pretending to be human approval
- hidden action execution without audit

### Future Schema

```text
docs/core/schemas/human-decision.schema.md
```

## 8. Signal Records

### Purpose

Signal records model observations that may become shared intelligence after sanitization.

### Ownership

Raw and candidate signals are usually:

```text
Workspace-owned data
```

Approved sanitized signals are:

```text
Observatory-owned data
```

### May Model

- raw signal
- signal candidate
- sanitization review
- sanitized signal
- sensitivity rating
- source references
- evidence summary
- decision status
- Observatory destination

### Must Not Model

- raw customer data in Observatory-owned records
- private workspace drafts in shared records
- unreviewed signal candidates as approved signals
- source workspace details exposed through normal query surfaces

### First Schema

```text
docs/core/schemas/signal.schema.md
```

## 9. Observatory Records

### Purpose

Observatory records model shared generalized intelligence derived from sanitized signals.

### Ownership

```text
Observatory-owned data
```

### May Model

- normalized signals
- derived intelligence
- keyword clusters
- trend profiles
- opportunity scores
- data quality notes
- prior signal checks
- strategy queue items
- research queue items
- query audit records

### Must Not Model

- raw workspace data
- raw customer data
- workspace-private artifacts
- direct cross-workspace reads
- hidden source workspace exposure
- business-specific private strategy

### Future Schemas

```text
docs/core/schemas/observatory-record.schema.md
docs/core/schemas/observatory-query.schema.md
docs/core/schemas/derived-intelligence.schema.md
```

These are not P0 unless needed earlier by signal schema design.

## 10. Audit Records

### Purpose

Audit records capture meaningful state changes and system activity.

### Ownership

```text
Core-owned data
```

### May Model

- audit id
- workspace id if applicable
- actor type
- actor id
- action type
- target resource
- result status
- timestamp
- linked review item
- linked run
- linked signal
- linked external reference

### Must Not Model

- editable history
- private payload dumps as audit detail
- credentials
- unaudited state-changing actions

### First Schema

```text
docs/core/schemas/audit-record.schema.md
```

## 11. Permission Records

### Purpose

Permission records define what actors, agents, integrations, or workflows may do.

### Ownership

```text
Core-owned data
```

### May Model

- permission scope
- actor type
- workspace scope
- action class
- allowed tools
- allowed runtime modes
- required review gates
- expiration or revocation status

### Must Not Model

- review bypasses
- broad unscoped permissions
- permanent secrets
- external platform permissions that override Neon Ronin gates

### Future Schema

```text
docs/core/schemas/permission-scope.schema.md
```

## 12. Integration Reference Records

### Purpose

Integration reference records let Neon Ronin refer to external systems without leaking provider-specific shape into core records.

### Ownership

```text
Integration-owned record or Referenced-only data
```

### May Model

- provider
- provider resource type
- provider resource id
- workspace id
- linked local record
- request id
- response status
- timestamp
- audit reference

### Must Not Model

- provider-specific fields in generic core records
- raw credentials
- one provider's semantics as platform semantics
- external write permission without review gates

### Future Schema

```text
docs/core/schemas/external-reference.schema.md
```

This is not P0 unless needed by early manual workflows.

## 13. Operations Records

### Purpose

Operations records support internal process discipline, manual tests, promotion decisions, emergency stops, and schema governance.

### Ownership

Usually:

```text
Core-owned data
```

Some operational notes may be documentation-only until implementation.

### May Model

- manual test records
- workspace promotion checklist records
- emergency stop events
- schema change review records
- first-workspace decision log entries

### Must Not Model

- execution truth as informal notes only
- bypass decisions without audit
- unapproved schema exceptions

### Future Schemas

```text
docs/core/schemas/manual-test.schema.md
docs/core/schemas/schema-change-review.schema.md
```

These are not P0.

## P0 Schema Set

The first schema set must stay small.

P0 schemas are:

1. `workspace-config.schema.md`
2. `review-queue-item.schema.md`
3. `audit-record.schema.md`
4. `signal.schema.md`
5. `agent-definition.schema.md`
6. `agent-run.schema.md`

These are enough to validate the initial core platform shape on paper.

Do not add additional P0 schemas unless one of these cannot be defined without it.

## P1 Schema Set

P1 schemas are:

1. `artifact.schema.md`
2. `workflow.schema.md`
3. `business-intake.schema.md`
4. `human-decision.schema.md`
5. `permission-scope.schema.md`

These are needed before a serious manual workflow is fully specified.

## Deferred Schema Domains

The following must not receive schema files, fields, or tables yet:

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
- plugin marketplace
- billing/subscription system
- marketplace account management

They may be discussed in roadmap or research docs.

They must not mutate core schema until promoted through an ADR, roadmap phase, or schema authority update.

## Provider-Specific Field Rule

Provider-specific fields must stay in provider-specific integration schemas or referenced-only records.

Do not add provider-specific fields to generic core schemas.

Bad:

```yaml
workspace:
  etsy_shop_id: abc123
```

Better:

```yaml
external_references:
  - provider: etsy
    resource_type: shop
    provider_resource_id: abc123
```

Even better later:

```text
integration-specific Etsy connection schema behind core external reference contract
```

## Server/System-Owned Field Rule

Schema docs must identify fields that callers, agents, or workspace configs may not set directly.

Examples:

- created timestamp
- updated timestamp
- audit id
- derived status
- approval status
- lifecycle transition result
- normalized Observatory id
- system-computed score

Server/system-owned fields prevent callers and agents from forging state.

## Immutable Field Rule

Schema docs must identify fields that cannot change after creation unless a governed migration or special transition allows it.

Examples may include:

- record id
- original source reference
- source workspace id
- created timestamp
- original actor id
- immutable audit event fields

Immutability protects provenance and auditability.

## Status And Transition Rule

Schemas with statuses must define valid statuses and valid transitions.

A status enum without transition rules is incomplete.

Examples:

- workspace lifecycle statuses
- review decision statuses
- signal lifecycle statuses
- agent run statuses
- artifact lifecycle statuses

Invalid transitions must be rejected, not silently corrected.

## Unknown Field Rule

Future implementation contracts should reject unknown fields for core schemas unless a schema explicitly allows bounded metadata.

This avoids silent schema drift.

A caller should not be able to smuggle business-specific or provider-specific meaning into core through unknown fields.

## Bounded Metadata Rule

Metadata fields may exist only when bounded and justified.

A metadata field must define:

- purpose
- owner
- allowed value types
- whether it is queryable
- whether it is canonical meaning
- what must not be stored there

Unbounded metadata is JSON sludge with a nicer hat.

## Relationship Rule

Schema relationships must preserve ownership boundaries.

Allowed:

- core review item references workspace artifact metadata
- audit record references source run
- sanitized signal references source signal candidate internally
- workspace decision references Observatory query output
- external reference links local record to provider resource id

Forbidden:

- workspace A directly references workspace B private record
- core record stores raw provider payload as platform truth
- Observatory query result exposes raw source workspace data
- business-specific table becomes FK target from core records

## Schema Promotion Rule

A new schema family may be added only when:

1. ownership is clear
2. scope is clear
3. provenance expectations are clear
4. non-goals are clear
5. deferred-domain risk has been checked
6. business-specific drift risk has been checked
7. affected docs are updated
8. the change is small enough to review

Major schema-family additions should use an ADR.

## Schema Review Questions

Before writing or changing a schema, answer:

1. What system concept does this schema model?
2. Who owns this data?
3. Is it core, workspace, Observatory, adapter, integration, referenced-only, or derived?
4. Is this schema business-neutral?
5. Does this schema depend on a specific business or first-business candidate?
6. Does this schema introduce a deferred domain?
7. What provenance must be preserved?
8. What audit events touch it?
9. What statuses and transitions exist?
10. Which fields are system-owned?
11. Which fields are immutable?
12. What must not be stored here?
13. What would be JSON sludge if added?
14. What future schema should this not try to pre-solve?

## Non-Goals

This document does not define:

- exact database tables
- exact SQL types
- exact indexes
- migration sequence
- API route contracts
- UI forms
- provider-specific payload contracts
- specific-business schema

Those come later if and when the roadmap allows them.

## Relationship To Operations

Future operations docs should enforce this schema authority through:

- schema change checklist
- first-workspace decision log
- workspace onboarding checklist
- manual test template
- promotion checklist

Schema authority is not just documentation. It is planning governance.

## Final Rule

```text
No schema without ownership.
No field without purpose.
No derived record without provenance.
No deferred domain by accident.
```
