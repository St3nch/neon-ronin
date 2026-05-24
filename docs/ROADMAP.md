# Neon Ronin Roadmap

## Purpose

This roadmap defines the official Neon Ronin-first build plan before any specific business workspace, including SearchClarity, is onboarded.

The goal is to make Neon Ronin structurally ready to host SearchClarity without allowing SearchClarity to define the platform.

SearchClarity may be an important early workspace, but Neon Ronin must remain the multi-workspace agent operating system.

Core rule:

```text
Prepare Neon Ronin for SearchClarity.
Do not turn Neon Ronin into SearchClarity.
```

## Roadmap Doctrine

Neon Ronin must follow the build order already defined in `docs/core/10-build-order.md`:

```text
Doctrine -> Schemas -> Manual Workspace Validation -> Controlled Agent Assistance -> Additional Workspace Types
```

This roadmap expands that sequence into practical planning phases.

## Current Status

Neon Ronin is currently in the doctrine and architecture-planning stage.

The project has strong conceptual docs, but it is not ready for application code.

Before coding begins, Neon Ronin needs concrete contracts for:

- workspace configuration
- workspace lifecycle
- business idea intake
- review queue items
- audit records
- agent definitions
- agent runs
- artifacts
- signals
- signal sanitization
- Observatory ingestion
- permissions
- external integration boundaries

## Near-Term Rule

Do not introduce SearchClarity docs, assumptions, schemas, report formats, customer workflows, or business-specific language into Neon Ronin core until the platform contracts below exist.

SearchClarity will be onboarded later through:

```text
business docs -> workspace adapter requirements -> reusable Neon Ronin capabilities -> workspace config
```

## Phase 0 - Foundation Lock

### Goal

Stabilize the current doctrine so future planning has a clean base.

### Tasks

1. Commit `AGENTS.md`.
2. Commit `docs/core/00-origin-and-north-star.md`.
3. Fix `docs/README.md` so it references `research-docs/`, not `research/`.
4. Add an ADR stating that `research-docs/` are supporting context, not canonical doctrine.
5. Add an ADR stating that first-business requirements must pass the reusable capability test before entering core.

### Deliverables

- `AGENTS.md`
- `docs/core/00-origin-and-north-star.md`
- updated `docs/README.md`
- `docs/decisions/adr-002-research-docs-are-supporting-context.md`
- `docs/decisions/adr-003-first-business-containment.md`

### Exit Criteria

- Any LLM or human can identify the canonical docs.
- Research docs cannot accidentally override core doctrine.
- First-business containment is documented as an accepted architecture decision.

## Phase 1 - Core Boundary Specs

### Goal

Turn the doctrine into enforceable platform boundaries before schemas and code.

### Tasks

1. Define signal sanitization rules.
2. Define workspace lifecycle states and allowed transitions.
3. Define allowed runtime modes by workspace status.
4. Define what belongs in core vs adapter vs workspace-specific config vs external integration.
5. Define manual-test requirements and workspace promotion criteria.

### Deliverables

- `docs/core/08-sanitization.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/core/glossary.md`
- `docs/operations/manual-test-template.md`
- `docs/operations/workspace-promotion-checklist.md`

### Exit Criteria

- A workspace cannot move from idea to active without explicit criteria.
- A signal cannot enter the Observatory without a defined sanitization path.
- Manual testing is operational, not just philosophical.

## Phase 2 - P0 Platform Schemas

### Goal

Define the minimum concrete records Neon Ronin needs before implementation.

### Required Folder

Create:

```text
docs/core/schemas/
```

### P0 Schema Deliverables

1. `docs/core/schemas/workspace-config.schema.md`
2. `docs/core/schemas/review-queue-item.schema.md`
3. `docs/core/schemas/audit-record.schema.md`
4. `docs/core/schemas/signal.schema.md`
5. `docs/core/schemas/agent-definition.schema.md`
6. `docs/core/schemas/agent-run.schema.md`

### Schema Requirements

Each schema doc should define:

- purpose
- required fields
- optional fields
- valid statuses or enums
- relationships to other records
- audit requirements
- example record
- non-goals

Where practical, schemas should be written so they can later become JSON Schema, Pydantic models, TypeScript types, or database tables.

### Exit Criteria

- A workspace config can be validated on paper.
- A review item can be created, reviewed, and audited on paper.
- A signal can be sanitized and accepted or rejected on paper.
- An agent run can be recorded and traced on paper.

## Phase 3 - P1 Platform Schemas And Contracts

### Goal

Complete the first serious workflow contract layer.

### Deliverables

1. `docs/core/schemas/artifact.schema.md`
2. `docs/core/schemas/workflow.schema.md`
3. `docs/core/schemas/business-intake.schema.md`
4. `docs/core/schemas/human-decision.schema.md`
5. `docs/core/schemas/permission-scope.schema.md`
6. `docs/core/11-secrets-and-credentials.md`
7. `docs/core/12-error-and-failure-handling.md`
8. `docs/core/13-observatory-scoring-contract.md`
9. `docs/core/14-external-integration-contract.md`

### Exit Criteria

- Neon Ronin can describe a complete manual workflow without code.
- Neon Ronin can describe what an external integration is allowed to do.
- Secrets and credentials have a documented boundary before any real token is stored.
- Failed runs, rejected reviews, parked items, and blocked signals have defined behavior.

## Phase 4 - Operations Layer

### Goal

Create the operational documents that prevent planning rules from becoming wishful thinking.

### Deliverables

- `docs/operations/first-workspace-decision-log.md`
- `docs/operations/workspace-onboarding-checklist.md`
- `docs/operations/review-queue-runbook.md`
- `docs/operations/emergency-stop-procedure.md`
- `docs/operations/schema-change-checklist.md`

### Exit Criteria

- Every new workspace-driven feature can be classified before implementation.
- Every manual test can be recorded consistently.
- Every schema change can be reviewed for drift risk.
- Emergency stop is defined before background work exists.

## Phase 5 - Workspace 1: Internal Research

### Goal

Validate Neon Ronin using a low-risk internal workspace before onboarding SearchClarity.

### Workspace

```yaml
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
status: manual_test
```

### Purpose

Use Neon Ronin to research and evaluate business ideas, platform decisions, opportunity signals, and workspace onboarding plans.

### Why This Comes Before SearchClarity

Internal Research exercises core platform mechanics without introducing customer pressure, marketplace pressure, paid delivery pressure, or business-specific report formats.

This workspace should validate:

- workspace configs
- artifacts
- review queue items
- audit logs
- signal candidates
- sanitization gates
- Observatory ingestion rules
- manual workflow discipline

### Allowed

- human-started research tasks
- internal research packets
- idea scoring packets
- review queue items
- sanitized signal candidates
- audit records

### Forbidden

- external writes
- marketplace actions
- customer delivery
- scheduled jobs
- watch mode
- autonomous spending
- autonomous publishing
- multi-agent delegation chains

### Exit Criteria

Before SearchClarity enters Neon Ronin planning, Internal Research should prove that:

1. A workspace can be created from config.
2. A manual workflow can produce artifacts.
3. A review queue item can be created and resolved.
4. An audit record can trace the work.
5. A signal candidate can be sanitized or rejected.
6. A platform decision can be recorded without business-specific contamination.

## Phase 6 - SearchClarity Compatibility Preparation

### Goal

Prepare Neon Ronin to inspect and onboard SearchClarity without letting SearchClarity reshape core.

This phase begins only after Phases 0 through 5 are complete enough to enforce boundaries.

### Tasks

1. Read the SearchClarity docs as business/workspace input, not platform doctrine.
2. Classify SearchClarity as a workspace type.
3. Identify SearchClarity-specific needs.
4. Extract reusable Neon Ronin capabilities.
5. Identify existing adapter coverage.
6. Identify gaps in core schemas.
7. Identify gaps in service-business adapter docs.
8. Create a SearchClarity workspace draft config.
9. Create a manual-test plan.
10. Identify hard-no automation rules.
11. Identify Observatory signal candidates.
12. Identify data that must remain private.

### Expected Classification

SearchClarity will likely be a service business workspace.

That assumption must be confirmed by reading the SearchClarity docs later.

### SearchClarity Must Stay Out Of Core

SearchClarity-specific items must not enter Neon Ronin core directly, including:

- customer-facing report language
- service brand language
- package names
- pricing assumptions
- customer promises
- report templates
- delivery rules
- Fiverr-specific gig copy
- customer history
- client-specific observations

These belong in SearchClarity workspace docs/config or a future business-specific folder, not in `docs/core/`.

### Reusable Capabilities That May Belong In Core

SearchClarity may reveal reusable needs such as:

- customer intake workflow
- service deliverable draft artifact
- QA review gate
- delivery gate
- customer-safe storage rules
- signal sanitization rules
- audit requirements
- review queue item types

Only these reusable capabilities should be promoted into Neon Ronin core.

### Deliverables

- SearchClarity intake summary
- SearchClarity workspace classification
- SearchClarity capability extraction table
- SearchClarity manual-test plan
- SearchClarity draft workspace config
- list of core gaps found during onboarding
- list of adapter gaps found during onboarding

### Exit Criteria

- SearchClarity can be described as a workspace without changing Neon Ronin identity.
- SearchClarity-specific language is isolated outside core.
- Any reusable requirements are documented as generic capabilities.
- A manual test can be run before any automation.

## Phase 7 - Workspace 2: SearchClarity Manual Validation

### Goal

Validate a service business workspace using SearchClarity as the first real business tenant.

### Allowed

- manual customer/request intake modeling
- report artifact drafting
- QA review packets
- human delivery approval gates
- customer-safe storage modeling
- sanitized signal candidates
- audit records

### Forbidden At First

- autonomous customer delivery
- autonomous customer messaging
- autonomous publishing
- autonomous pricing changes
- autonomous platform/account changes
- autonomous use of customer-private data in Observatory
- scheduled customer-facing workflows

### Exit Criteria

SearchClarity can move toward active only when:

1. Manual workflow has been run several times.
2. Review queue has handled customer-facing draft approval.
3. Audit logs trace each deliverable step.
4. Signal sanitization has been validated.
5. Customer-private data boundaries are enforced.
6. The service-business adapter remains generic.
7. No SearchClarity-specific logic has entered core.

## Phase 8 - Controlled Agent Assistance

### Goal

Add limited agent assistance after manual workflows are understood.

### Allowed Agent Work

- research drafting
- intake normalization
- outline/deliverable draft preparation
- QA checklists
- review queue generation
- sanitized signal candidate drafting
- internal recommendation packets

### Still Forbidden

- autonomous customer messaging
- autonomous customer delivery
- autonomous external writes
- autonomous paid actions
- autonomous credential changes
- autonomous destructive actions

### Exit Criteria

Agents improve speed or consistency without bypassing human review gates.

## Phase 9 - Future Workspace Types

### Goal

Only after Neon Ronin supports Internal Research and SearchClarity cleanly should additional workspace types enter serious planning.

Possible future workspaces:

- marketplace store workspace
- digital product workspace
- content business workspace
- hybrid workspace

### Rule

Each new workspace must go through the same onboarding process:

```text
business idea
-> business definition
-> adapter requirements
-> reusable capability extraction
-> workspace config
-> manual test
-> gradual automation
```

## Do Not Build Yet

Until the earlier phases are complete, do not build:

- Tauri UI
- marketplace integrations
- Printify integration
- Etsy integration
- Fiverr automation
- LangGraph integration
- Hermes integration
- scheduled agents
- watch mode
- multi-agent delegation
- autonomous publishing
- autonomous spending
- customer messaging automation
- cross-workspace direct queries

## Roadmap Principle

```text
Neon Ronin earns automation by proving manual workflows.
Neon Ronin earns new workspace types by preserving core boundaries.
Neon Ronin earns complexity gradually.
```

## Immediate Next Actions

1. Commit the current foundational docs.
2. Fix `docs/README.md` folder map.
3. Add ADR-002 for research-docs status.
4. Add ADR-003 for first-business containment.
5. Write `docs/core/08-sanitization.md`.
6. Write `docs/core/09-workspace-lifecycle.md`.
7. Create `docs/core/schemas/`.
8. Write the six P0 schemas.
9. Create `docs/operations/`.
10. Prepare Internal Research as Workspace 1.

## Final Rule

SearchClarity is allowed to be an early workspace.

SearchClarity is not allowed to become Neon Ronin.
