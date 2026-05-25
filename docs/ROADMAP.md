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
Doctrine -> Structural Authority -> Schemas -> Manual Workspace Validation -> Controlled Agent Assistance -> Additional Workspace Types
```

This roadmap expands that sequence into practical planning phases.

## VEDA-Informed Planning Adjustment

A review of VEDA observatory/database specification docs showed several structural patterns Neon Ronin should adopt before glossary and schema work.

Neon Ronin should borrow VEDA's discipline, not VEDA's exact system boundaries.

Useful borrowed patterns:

- define data ownership before schema
- define system invariants before implementation
- preserve provenance and evidence before interpretation
- distinguish raw, structured, sanitized, normalized, and derived records
- make schema authority explicit before individual schema files
- prevent deferred domains from getting ad hoc tables or fields
- prefer explicit schema over unbounded JSON sludge
- keep derived outputs labeled as derived
- preserve read-without-ownership boundaries

Adapted Neon Ronin rule:

```text
Borrow structural rigor from VEDA.
Do not import VEDA's project assumptions, entity names, or pure-observatory role.
```

Neon Ronin is not a pure observatory. Neon Ronin orchestrates workspaces under human control, and the Observatory is one core subsystem inside that platform.

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
- provenance and evidence
- schema authority
- data ownership boundaries
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

### Status

Completed.

## Phase 1 - Core Boundary Specs

### Goal

Turn the doctrine into enforceable platform boundaries before structural authority docs, schemas, and code.

### Tasks

1. Define signal sanitization rules.
2. Define workspace lifecycle states and allowed transitions.
3. Define allowed runtime modes by workspace status.
4. Define what belongs in core vs adapter vs workspace-specific config vs external integration.
5. Define manual-test requirements and workspace promotion criteria.
6. Define the Observatory shared-intelligence boundary.

### Deliverables

- `docs/core/08-sanitization.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/decisions/adr-004-observatory-shared-intelligence-boundary.md`

### Exit Criteria

- A workspace cannot move from idea to active without explicit criteria.
- A signal cannot enter the Observatory without a defined sanitization path.
- The Observatory is structurally defined as shared intelligence, not shared private memory.
- Manual testing is operational, not just philosophical.

### Status

Completed.

## Phase 2 - Structural Authority Layer

### Goal

Add the VEDA-informed authority docs that must exist before glossary and schema work.

This phase defines ownership, invariants, provenance, and schema authority so individual schemas do not become ad hoc implementation guesses.

### Tasks

1. Define Neon Ronin data ownership boundaries.
2. Define system invariants that must always remain true.
3. Define provenance and evidence requirements.
4. Define schema authority and governed schema families.
5. Define canonical vocabulary after ownership and provenance are clear.

### Deliverables

1. `docs/core/11-data-boundaries.md`
2. `docs/core/12-system-invariants.md`
3. `docs/core/13-provenance-and-evidence.md`
4. `docs/core/14-schema-authority.md`
5. `docs/core/glossary.md`

### Data Boundary Topics

`docs/core/11-data-boundaries.md` should define:

- core-owned data
- workspace-owned data
- Observatory-owned data
- adapter-owned patterns
- integration-owned records
- referenced-only data
- forbidden-in-core data
- read-without-ownership rules
- derived-does-not-replace-canonical rules
- deferred domain rules

### System Invariant Topics

`docs/core/12-system-invariants.md` should define non-negotiables such as:

- Neon Ronin hosts workspaces; it does not become a workspace.
- Workspaces are isolated by default.
- The Observatory is the only cross-workspace intelligence channel.
- Human approval gates risky actions.
- No agent approves its own work.
- Manual workflow proof comes before automation.
- Core schemas remain business-neutral.
- Deferred domains do not get ad hoc schemas.
- Derived intelligence does not become approval or execution truth.
- The system remains legible to capable LLMs.

### Provenance And Evidence Topics

`docs/core/13-provenance-and-evidence.md` should define provenance requirements for:

- raw workspace observations
- signal candidates
- sanitized signals
- normalized Observatory records
- derived intelligence
- agent runs
- artifacts
- review queue items
- human decisions
- audit records

It should preserve the distinction between:

```text
raw data -> structured record -> sanitized record -> normalized record -> derived output -> human decision/action
```

### Schema Authority Topics

`docs/core/14-schema-authority.md` should define governed schema families before individual schema docs are written:

- workspace records
- workflow records
- agent records
- run/job records
- artifact records
- review records
- human decision records
- signal records
- Observatory records
- audit records
- permission records
- integration reference records
- operations records

It should also define what must not become schema yet, including deferred domains such as marketplace integrations, Printify, Fiverr automation, Tauri UI, LangGraph, Hermes, scheduled agents, watch mode, and multi-user roles.

### Exit Criteria

- Every future schema family has an ownership category.
- Every derived output can be distinguished from canonical source records.
- Every meaningful record has a provenance expectation.
- Deferred domains cannot sneak into schema through convenience fields.
- Glossary terms are grounded in ownership and provenance decisions.

## Phase 3 - P0 Platform Schemas

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
- ownership category
- required fields
- optional fields
- server/system-owned fields
- valid statuses or enums
- relationships to other records
- provenance requirements
- audit requirements
- lifecycle constraints
- example record
- non-goals

Where practical, schemas should be written so they can later become JSON Schema, Pydantic models, TypeScript types, or database tables.

### Exit Criteria

- A workspace config can be validated on paper.
- A review item can be created, reviewed, and audited on paper.
- A signal can be sanitized and accepted or rejected on paper.
- An agent run can be recorded and traced on paper.
- No schema depends on SearchClarity-specific assumptions.

### Status

Completed.

## Phase 4 - P1 Platform Schemas And Contracts

### Goal

Complete the first serious workflow contract layer.

### Deliverables

1. `docs/core/schemas/artifact.schema.md`
2. `docs/core/schemas/workflow.schema.md`
3. `docs/core/schemas/business-intake.schema.md`
4. `docs/core/schemas/human-decision.schema.md`
5. `docs/core/schemas/permission-scope.schema.md`
6. `docs/core/15-secrets-and-credentials.md`
7. `docs/core/16-error-and-failure-handling.md`
8. `docs/core/17-observatory-scoring-contract.md`
9. `docs/core/18-external-integration-contract.md`

### Exit Criteria

- Neon Ronin can describe a complete manual workflow without code.
- Neon Ronin can describe what an external integration is allowed to do.
- Secrets and credentials have a documented boundary before any real token is stored.
- Failed runs, rejected reviews, parked items, and blocked signals have defined behavior.

### Schema Status

Completed.

### Contract Status

Completed.

## Parallel Track - SearchClarity Business Readiness

### Goal

Make SearchClarity operationally ready as a real manual service business before Neon Ronin attempts full workspace onboarding or automation planning.

This is a parallel business-readiness track, not Neon Ronin core work.

SearchClarity artifacts may inform Neon Ronin compatibility work, but they must not become core doctrine or core schema.

Core rule:

```text
SearchClarity must prove its manual business workflow.
Neon Ronin must prepare to host that workflow without becoming it.
```

### Why This Track Exists

A review of `C:\dev\searchclarity\docs` showed that SearchClarity is strategically strong but still has launch-blocking business artifacts to finish.

SearchClarity should not be fully onboarded into Neon Ronin until there is enough real manual workflow evidence to model safely.

SearchClarity currently needs manual-business assets such as:

- public sample report
- report production pipeline
- branded report template
- tracker workbook
- Fiverr gig copy
- buyer intake forms
- first-order fulfillment SOP
- QC checklist
- pricing source of truth
- public proof assets

These are SearchClarity workspace inputs.

They are not Neon Ronin platform doctrine.

### SearchClarity Readiness Deliverables

Before full SearchClarity onboarding, SearchClarity should have:

1. `docs/samples/maplewood-candle-co-listing-visibility-audit.md` completed as a polished sample source.
2. A working PDF export pipeline from Markdown to customer-facing PDF.
3. A SearchClarity stylesheet or report styling system.
4. A delivery-ready sample PDF export.
5. A reusable Etsy Listing Visibility Audit report template.
6. A minimal tracker workbook with the eight required sheets:
   - Customers
   - Orders
   - Reports
   - Action Plan Items
   - Keyword Observations
   - Raw Market Signals
   - Generalized Observations
   - Consent Records
7. Fiverr gig copy for the first offer.
8. Buyer intake form copy for the first offer.
9. First-order fulfillment SOP.
10. One-page QC checklist or tracker tab.
11. Reconciled launch pricing source of truth.
12. Consent language for public examples, testimonials, or case studies.

### SearchClarity Evidence Needed By Neon Ronin

Neon Ronin should later use SearchClarity readiness artifacts to extract:

- service-business workspace requirements
- customer intake workflow
- report artifact types
- QA review gate needs
- customer delivery review gate needs
- privacy review needs
- signal capture workflow
- raw-to-sanitized signal handoff
- artifact storage requirements
- audit events required for fulfillment
- workspace-private data boundaries
- manual-test checklist items

### SearchClarity Must Stay Workspace-Owned

The following remain SearchClarity workspace-owned or SearchClarity business-owned:

- brand language
- service offers
- package names
- pricing
- Fiverr gig copy
- buyer-facing report language
- report templates
- customer intake forms
- customer/order/report records
- customer delivery messages
- client-specific recommendations
- client-specific report history
- raw client observations
- consent records

These must not enter `docs/core/` as Neon Ronin doctrine.

### Neon Ronin May Extract Reusable Capabilities

SearchClarity may reveal reusable platform needs, such as:

- artifact schema requirements
- workflow schema requirements
- business intake schema requirements
- human decision schema requirements
- permission scope requirements
- service-business adapter gaps
- review queue item types
- audit event types
- signal sanitization patterns
- Observatory scoring contract needs
- external integration boundaries

Only reusable capabilities may be promoted into Neon Ronin core.

### Readiness Gate For Phase 7

Phase 7 SearchClarity Compatibility Preparation should begin only when:

1. Neon Ronin has completed enough Phase 4 and Phase 5 structure to model manual workflows safely.
2. SearchClarity has completed enough business-readiness artifacts to provide real workspace input.
3. SearchClarity-specific details can be classified as workspace-owned, adapter-owned, reusable core capability, integration-owned, or out-of-scope.
4. SearchClarity can be inspected without turning SearchClarity's docs into Neon Ronin doctrine.

### Status

Not started in Neon Ronin.

SearchClarity docs have been inspected as WIP context.

## Phase 5 - Operations Layer

### Goal

Create the operational documents that prevent planning rules from becoming wishful thinking.

### Deliverables

- `docs/operations/first-workspace-decision-log.md`
- `docs/operations/workspace-onboarding-checklist.md`
- `docs/operations/manual-test-template.md`
- `docs/operations/workspace-promotion-checklist.md`
- `docs/operations/review-queue-runbook.md`
- `docs/operations/emergency-stop-procedure.md`
- `docs/operations/schema-change-checklist.md`

### Exit Criteria

- Every new workspace-driven feature can be classified before implementation.
- Every manual test can be recorded consistently.
- Every schema change can be reviewed for drift risk.
- Emergency stop is defined before background work exists.

### Status

Completed.

## Phase 5B - Hammer Testing Doctrine

### Goal

Define Neon Ronin's future hammer testing doctrine before implementation, database design, API design, agent runtime, or integration work begins.

This phase adapts VEDA, Project V, and V Forge hammer discipline to Neon Ronin's workspace, Observatory, review, audit, permission, artifact, signal, and integration model.

### Deliverable

- `docs/core/19-hammer-testing-doctrine.md`

### Exit Criteria

- Hammer testing is defined as stress verification, not ordinary unit testing.
- Future hammer categories are named for persistence, contracts, boundaries, workspace isolation, Observatory, review gates, audit, permissions, agent runs, artifacts, signals, rollback, schema drift, integrations, and emergency stop.
- Anti-fake-coverage rules are documented before tests exist.
- Future DB reliability probes are listed without prematurely choosing database architecture.
- Manual testing and hammer testing are clearly separated.

### Status

Completed.

## Phase 5C - Core Example Separation

### Goal

Separate concrete worked examples from core doctrine before Phase 6 Internal Research begins.

This phase exists because SearchClarity was useful as planning evidence, but SearchClarity-specific examples, IDs, and reminders should not live inside business-neutral core docs.

Core docs should contain generic platform doctrine.

Reference examples should contain concrete worked examples.

### Why This Phase Exists

A Claude architecture audit found that SearchClarity had leaked into multiple `docs/core/` files and schema examples.

A follow-up discussion clarified the cause: Neon Ronin needed concrete examples during planning, but the repository lacked a legal home for real-business worked examples that are useful without becoming doctrine.

This phase fixes that structure.

### Deliverables

- `docs/reference-examples/README.md`
- `docs/workspaces/README.md`
- SearchClarity-aware worked examples moved or rewritten outside `docs/core/`
- generic replacements for SearchClarity-specific examples in core docs and schemas
- status notes on unexercised operations docs where appropriate

### Exit Criteria

- `docs/core/` remains business-neutral.
- Core schemas do not use SearchClarity IDs, filenames, package names, or business examples as canonical examples.
- Concrete SearchClarity examples have a non-core home if they remain useful.
- `docs/reference-examples/` is clearly labeled as explanatory, not canonical doctrine.
- `docs/workspaces/` exists as the future home for actual workspace configs and notes.
- Phase 6 can begin without SearchClarity acting as the hidden reference model.

### Status

Completed.

## Phase 5D - DB Reliability And Schema Clarification

### Goal

Resolve the database-readiness and hammer-readiness clarification issues found by the Claude Prompt B audit before Phase 6 begins.

This phase does not design or implement the database.

This phase clarifies the schema, transaction, resolver, and reliability decisions that Phase 6 records would otherwise encode ambiguously.

### Why This Phase Exists

The Prompt B audit found that Neon Ronin is not at data-swamp risk, but several pre-implementation concepts are still too ambiguous for reliable future database design.

The highest-risk issues are:

- polymorphic references without a resolver contract
- ambiguous `version` field semantics
- unnamed transaction boundaries
- audit-first wording that needs transaction-aware clarification
- cross-schema status drift
- append-only audit/human-decision enforcement not yet specified
- workspace isolation enforcement posture not yet specified
- retention/deletion policy not yet specified

### Pre-Phase-6 Fixes

Before Phase 6 Internal Research begins, complete the following:

1. Split generic `version` semantics into `schema_version` and `record_revision` across governed schemas.
2. Add a canonical allowed `record_type` registry for polymorphic references.
3. Add canonical cross-schema status definitions for recurring statuses such as `blocked`, `parked`, `rejected`, `cancelled`, `expired`, `archived`, and `retired`.
4. Add a transaction-boundaries doc that names the Phase-6-relevant atomic operations.
5. Clarify the audit-first rule so in-transaction audit failure rolls back state changes, while audit subsystem unavailability blocks new consequential work.
6. Resolve the P0/P1 sanitization decision boundary if still ambiguous.
7. Complete Phase 5C core example separation so SearchClarity is not the hidden reference model.
8. Specify Internal Research's relationship to business intake before drafting its workspace config.
9. Add a resolver hammer module specification to `docs/core/19-hammer-testing-doctrine.md`.

### Future DB Planning Preconditions

Track, but do not necessarily complete before Phase 6:

- append-only enforcement posture for audit records and human decisions
- workspace isolation enforcement posture
- soft-delete, hard-delete, retention, and deletion policy
- timestamp posture, including UTC, precision, DB-set fields, and ordering tie-breakers
- system-owned field enforcement posture
- signal record decomposition decision
- workflow step storage decision
- sub-object shape enumeration requirements
- provider payload snapshot isolation rule
- future hammer coverage map enforcement rules

### Deliverables

- updates to `docs/core/14-schema-authority.md`
- updates to affected schema docs for `schema_version` and `record_revision`
- `docs/core/20-transaction-boundaries.md`
- updates to `docs/core/16-error-and-failure-handling.md`
- updates to `docs/core/19-hammer-testing-doctrine.md`
- any small supporting updates needed to preserve roadmap consistency

### Exit Criteria

- Version semantics are unambiguous before first Phase 6 records are drafted.
- Polymorphic reference vocabulary has a canonical registry.
- Phase-6-relevant transaction boundaries are named.
- Audit-first behavior is implementable later.
- Recurring statuses have canonical meanings.
- Phase 5C cleanup is complete before Phase 6 starts.
- Future DB planning preconditions are captured without prematurely choosing database technology.

### Status

Completed.

## Phase 6 - Workspace 1: Internal Research

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
- provenance requirements
- derived-vs-canonical record boundaries

### Allowed

- human-started research tasks
- internal research packets
- idea scoring packets
- review queue items
- sanitized signal candidates
- audit records
- documentation-only LLM recommendation assistance as reviewable artifacts
- documentation-only LLM draft assistance testing through manual evidence passes

### Current Progress

Internal Research has completed:

- lightweight intake/classification
- workspace config draft
- Manual Test 001 for artifact, review, audit, human-decision, and signal flow
- Manual Test 001 evidence and human decisions
- promotion to documentation-only `manual_test` posture
- Manual Test 002 for LLM recommendation assistance
- Manual Test 002 evidence and human decision
- agent-assistance boundary plan
- Manual Test 003 plan for LLM draft assistance

Current posture remains:

```text
status: manual_test
runtime.default_mode: off
allowed_agents: []
scheduled_allowed: false
watch_mode_allowed: false
external_references: []
```

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
7. Provenance is preserved across raw, structured, sanitized, and derived records.

## Phase 7 - SearchClarity Compatibility Preparation

### Goal

Prepare Neon Ronin to inspect and onboard SearchClarity without letting SearchClarity reshape core.

This phase begins only after Phases 0 through 6 are complete enough to enforce boundaries and the SearchClarity Business Readiness track has produced enough manual-business evidence to model safely.

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
13. Identify provenance and evidence requirements.
14. Identify any deferred domains that must not enter core yet.
15. Confirm which SearchClarity readiness artifacts exist and which are still missing.
16. Confirm whether SearchClarity is ready for workspace onboarding or should remain business-build-only.

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
- provenance requirements

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

## Phase 8 - Workspace 2: SearchClarity Manual Validation

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

## Phase 9 - Controlled Agent Assistance

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

## Phase 10 - Future Workspace Types

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

Deferred domains must not receive ad hoc schemas, fields, or tables before they are promoted through the roadmap.

## Roadmap Principle

```text
Neon Ronin earns automation by proving manual workflows.
Neon Ronin earns new workspace types by preserving core boundaries.
Neon Ronin earns schemas by proving ownership and provenance.
Neon Ronin earns complexity gradually.
```

## Immediate Next Actions

1. Execute Manual Test 003 for LLM draft assistance as a documented evidence pass.
2. Record the human decision for Manual Test 003 before treating `draft_only` as validated.
3. Keep executable agent definitions blocked until Manual Test 003 passes and a separate approval path says otherwise.
4. Keep runtime off, `allowed_agents: []`, scheduled jobs disabled, watch mode disabled, and live Observatory ingestion blocked.
5. Keep SearchClarity as future workspace pressure, not core doctrine.

## Final Rule

SearchClarity is allowed to be an early workspace.

SearchClarity is not allowed to become Neon Ronin.

```text
Smart and Optimal.
```



