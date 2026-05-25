# Glossary

## Purpose

This glossary defines canonical Neon Ronin vocabulary for humans, LLMs, coding agents, docs, schemas, operations, and future implementation work.

It exists to reduce ambiguity before schema design begins.

If a term is defined here, use this meaning unless a more specific core doc, schema doc, operations doc, workspace adapter doc, or ADR intentionally narrows it.

## Core Rule

```text
Use canonical Neon Ronin terms consistently.
Do not invent new names for existing platform concepts without updating this glossary.
```

A vague term becomes schema drift later.

## Authority

This glossary is informed by:

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
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/14-schema-authority.md`
- `docs/decisions/`
- `docs/workspace-adapters/`

Research docs may inform vocabulary, but they do not override canonical terms unless promoted through core docs or ADRs.

## Quick Mental Model

```text
Neon Ronin = the operating system
Workspace = a business or project tenant
Workspace adapter = reusable pattern for a type of workspace
Agent = scoped worker
Review queue = human control gate
Artifact = produced output or file reference
Signal = useful observation that may become shared intelligence
Sanitization = privacy/generalization gate
Observatory = shared intelligence layer
Audit log = trace of meaningful state changes
Human = final decision-maker
```

---

# A

## Action Class

A category of action an agent, workflow, integration, or runtime operation may perform.

Canonical action classes:

| Action Class | Meaning |
|---|---|
| `read` | Fetch or inspect approved data |
| `analyze` | Transform, compare, summarize, or classify data |
| `draft` | Create internal drafts, packets, artifacts, or candidates |
| `queue` | Create or update review queue items |
| `external_draft` | Prepare or create a draft in an external system, gated early |
| `live_write` | Change public, customer-facing, marketplace-facing, or live external state |
| `destructive` | Delete, cancel, refund, revoke, remove, or otherwise damage/undo state |

`live_write` and `destructive` actions require human approval.

## Active

A workspace lifecycle status meaning the workspace passed manual validation and may operate under controlled rules.

Active does not mean autonomous.

Active workspaces may use on-demand work and approved scheduled/watch modes only if configured and gated.

## Adapter-Owned Pattern

A reusable workflow, agent-role, artifact, or review-gate pattern that applies to a class of workspaces, not to one real business.

Examples:

- service business intake pattern
- marketplace listing draft pattern
- content editorial workflow
- internal research scoring packet pattern

Adapter-owned patterns are not private workspace records.

## Agent

A scoped worker inside Neon Ronin.

Agents may read approved data, analyze, draft, prepare packets, create review items, and submit signal candidates within their permissions.

Agents do not have unlimited authority.

Agents must not approve their own work.

## Agent Definition

A core-owned record or schema family describing an agent's identity, role, allowed action classes, allowed tools, workspace scope, output types, runtime constraints, review requirements, and forbidden actions.

## Agent Run

A traceable execution attempt by an agent.

An agent run should record:

- workspace id
- agent id
- triggering actor
- trigger type
- runtime mode
- input references
- output references
- status
- timestamps
- linked audit records

## Agent Runtime

The platform contract that governs how agents run, what they may access, what actions they may take, what outputs they produce, and which review gates they trigger.

## Approved Record

A reviewed record that has received approval for its intended next step.

Approval must be traceable to a human decision where human review is required.

## Artifact

An output, file, packet, draft, note, deliverable, asset, report, checklist, or reference produced by a human, agent, workflow, or integration.

Artifact metadata may be core-owned.

Artifact content is usually workspace-owned.

An artifact draft is not a final deliverable.

## Audit Log

The append-friendly or immutable history of meaningful system activity and state changes.

Audit logs should record agent runs, review decisions, external API calls, workspace status changes, signal submissions, signal approvals, paid action attempts, publish attempts, credential changes, and emergency stop events.

## Audit Record

A single audit entry describing who or what did what, when, against which target, in which workspace if applicable, and with what result.

Audit records should not contain raw credentials or private payload dumps.

## Automation

System-driven execution without a human manually performing each step.

Automation is earned only after manual workflow proof.

Do not confuse automation with agent assistance. Agent assistance may still require human review.

---

# B

## Business

A real or proposed small-business idea, service, store, content operation, digital product effort, internal research effort, or hybrid project that may become a Neon Ronin workspace.

A business does not become Neon Ronin.

A business becomes a workspace inside Neon Ronin.

## Business Idea

A captured concept that may or may not become a workspace.

Business ideas begin at the `idea` lifecycle status and must be classified before onboarding.

## Business Intake

The process or future schema family used to capture and structure a business idea before it becomes a configured workspace.

Business intake should identify purpose, type, channels, workflows, data sources, outputs, review gates, hard-no rules, and Observatory permissions.

## Business-Neutral

Not tied to one real business, brand, marketplace, customer, product line, service offer, or provider.

Core Neon Ronin docs and schemas should be business-neutral.

---

# C

## Capability Extraction

The planning process of turning a real business need into reusable Neon Ronin platform capabilities.

Example:

| Business Need | Reusable Capability |
|---|---|
| customer submits request | intake workflow |
| output needs approval | review queue |
| insight may help other workspaces | signal capture and sanitization |
| public release is needed | publish gate |

Only reusable capabilities belong in core.

## Channel

A place or medium where a workspace operates or publishes.

Examples:

- marketplace
- service platform
- direct site
- social platform
- content platform
- internal research
- other

A channel is not automatically an integration.

## Confidence

A simple indication of evidence strength or uncertainty on a record, signal, score, or derived output.

Recommended labels:

| Label | Meaning |
|---|---|
| `low` | Weak evidence, high uncertainty, or speculative output |
| `medium` | Some supporting evidence with caveats |
| `high` | Strong supporting evidence and few caveats |
| `unknown` | Confidence not assessed |

Confidence is not approval.

## Content Business Workspace

A workspace type for publishing articles, videos, newsletters, media, or similar content.

Typical needs include topic research, editorial planning, drafting, content review, publishing preparation, calendar management, and signal capture.

## Core

The business-neutral Neon Ronin platform layer.

Core owns reusable platform capabilities such as workspace registry, lifecycle, agent runtime, review queue, audit, permissions, schema authority, and the Observatory boundary.

Core must not contain one business's private workflows, report templates, customer data, marketplace assumptions, or provider-specific payload shape.

## Core-Owned Data

Business-neutral platform data Neon Ronin owns directly.

Examples include workspace config, agent definitions, review queue items, audit records, permission scopes, runtime modes, and schema/version metadata.

## Customer-Facing Action

An action visible to or delivered to a customer.

Examples:

- sending a message
- delivering a report
- publishing customer-visible output
- issuing a refund
- changing a customer order

Customer-facing actions require human review unless explicitly governed otherwise later.

---

# D

## Data Boundary

A rule defining who owns a data class, where it may live, what may reference it, and what must not become canonical platform data.

Every durable record must have a clear data boundary.

## Data Quality Note

A note describing the strength, weakness, freshness, uncertainty, or limitation of evidence, signals, queries, or derived intelligence.

Data quality notes may appear in Observatory records, research packets, scores, and review items.

## Deferred Domain

A future capability area that is not allowed to mutate core schema, docs, or implementation yet.

Current deferred domains include Etsy integration, Printify integration, Fiverr automation, marketplace publishing, Tauri UI, LangGraph, Hermes, scheduled agents, watch mode, multi-user roles, cloud sync, and plugin marketplaces.

Deferred does not mean forgotten. It means not yet promoted.

## Deliverable

A customer-facing or public-facing output prepared by a workspace.

A draft deliverable is an artifact.

A final deliverable requires appropriate review and approval.

## Derived Data

Data computed, summarized, scored, clustered, transformed, or interpreted from one or more source records.

Derived data must be labeled as derived and preserve provenance.

A derived output does not replace canonical source records.

## Derived Intelligence

Observatory or strategy output derived from sanitized signals or other approved sources.

Examples:

- keyword cluster
- trend profile
- opportunity score
- data quality summary
- generalized recommendation

Derived intelligence is not approval and must not trigger external action by itself.

## Digital Product Workspace

A workspace type for downloadable, packaged, or otherwise digitally delivered products.

Typical needs include topic validation, product briefs, asset drafting, QA, launch preparation, delivery preparation, version tracking, and signal capture.

## Draft

An unfinished or unapproved output.

Drafts may be produced by agents or humans, but they are not final deliverables, publications, or approved actions.

---

# E

## Emergency Stop

A runtime mode or platform state that stops active runs and blocks new work.

Emergency stop overrides all workspace statuses and runtime modes.

## Evidence

Source material or records that support later work, interpretation, review, or decisions.

Evidence may include raw input, structured records, artifacts, audit records, external references, signals, and reviewed outputs.

Evidence must preserve provenance.

## External Action

An action involving a system outside Neon Ronin.

Examples:

- external API call
- marketplace draft creation
- publishing request
- customer message
- payment/refund action
- file upload to a provider

External actions must follow integration, permission, runtime, review, and audit rules.

## External Draft

An action class where Neon Ronin prepares or creates a draft in an external system.

External drafts are gated early and must not imply live publishing.

## External Integration

A connection to an outside platform, provider, API, marketplace, service, LLM provider, file store, payment processor, or communication system.

External integrations are subordinate to Neon Ronin core rules.

## External Reference

A provider/resource pointer that lets Neon Ronin refer to external data without making provider-specific fields part of core schema.

Example shape:

```yaml
provider: etsy
resource_type: shop
provider_resource_id: abc123
```

Provider-specific details belong in integration-specific schemas later, not generic core records.

---

# F

## First Business

The first real business workspace used to validate Neon Ronin.

The first business may shape priorities, but it must not define the platform.

```text
The first business is a proving ground.
It is not the platform.
```

## Forbidden-In-Core Data

Data that must not become Neon Ronin core platform data.

Examples include one business's customer history, report templates, marketplace listing copy, product niche, customer promises, pricing assumptions, raw customer files, credentials, and provider-specific payload shapes.

## Foundation Lock

The roadmap phase that stabilizes foundational docs, LLM entrypoint, north star, research authority boundary, and first-business containment before further planning.

---

# G

## Gate

A control point requiring review, approval, validation, or explicit decision before work may continue.

See Review Gate.

## Generalized Intelligence

Information transformed so it is useful across workspaces without exposing private workspace or customer details.

Generalized intelligence may live in the Observatory if it passes sanitization.

## Glossary

This file.

The canonical vocabulary reference for Neon Ronin.

---

# H

## Hard-No Rule

A non-negotiable action prohibition.

Current hard-no rules:

```text
No autonomous publishing.
No autonomous spending.
No autonomous customer messaging.
No autonomous credential changes.
No autonomous destructive actions.
No agent approves its own work.
```

## Human

The operator or reviewer who remains the final decision-maker for risky, public-facing, customer-facing, paid, destructive, credential-related, legal, IP, compliance, and publishing actions.

## Human Decision

A recorded approval, approval with changes, rejection, revision request, escalation, parking decision, publish approval, delivery approval, or other operator decision.

Human decisions must preserve review provenance and auditability.

## Human-In-The-Loop

A design posture where agents may assist but humans approve risky or consequential actions.

Human-in-the-loop is not optional decoration. It is part of Neon Ronin's safety model.

## Hybrid Workspace

A workspace type combining multiple workspace patterns, such as service plus content, marketplace plus digital product, or research plus service.

Hybrid workspaces require extra care to avoid adapter confusion and schema drift.

---

# I

## Idea

A workspace lifecycle status representing a captured concept that has not yet been structured.

Idea-stage workspaces cannot run agents, submit signals, use integrations, or perform operational work.

## Immutable Field

A schema field that cannot change after creation unless a governed migration or special transition allows it.

Examples may include record id, original source reference, source workspace id, created timestamp, original actor id, and immutable audit event fields.

## Internal Research Workspace

A low-risk workspace type for research, hypothesis tracking, opportunity scoring, strategy notes, market observation, and decision support.

The recommended first Neon Ronin workspace is:

```yaml
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
status: manual_test
```

## Integration-Owned Record

A record owned by an external integration domain, such as provider references, request ids, response status, OAuth connection records, webhook metadata, or provider-specific payload snapshots where allowed.

Integration-owned records must not leak provider-specific semantics into generic core records.

---

# J

## Job

A planned, queued, scheduled, or managed unit of work.

Job schema is not P0 unless required by early agent-run schema design.

Scheduled jobs and watch-mode jobs are deferred domains until promoted.

## JSON Sludge

Unbounded JSON or metadata used to avoid proper schema design.

Bad pattern:

```text
custom_data: { anything goes }
```

Acceptable JSON must be bounded, justified, and not used as hidden core semantic truth.

---

# K

## Keyword Cluster

A group of related terms, queries, topics, or themes returned by the Observatory as generalized intelligence.

Keyword clusters must not expose private source records through normal query surfaces.

---

# L

## Lifecycle Status

The state of a workspace.

Canonical workspace statuses:

```text
idea
onboarding
manual_test
active
paused
retired
```

Workspace status controls allowed runtime modes, review behavior, Observatory access, and external integration permissions.

## Live Write

An action class that changes public, customer-facing, marketplace-visible, or live external state.

Live writes require human approval.

## LLM-First

The repository is designed so future LLMs and coding agents can quickly understand the project, canonical docs, rules, boundaries, and roadmap.

LLM-first does not mean prompts belong in the repo by default.

Stable doctrine belongs in the repo. Temporary model-specific prompts do not.

---

# M

## Manual Test

A workspace lifecycle status and validation practice where a workflow is tested manually before automation.

Manual test workspaces may use human-started workflows and explicitly allowed on-demand agent assistance, but cannot run scheduled jobs or watch mode.

## Marketplace Store Workspace

A workspace type for selling products/listings on marketplaces.

Typical needs include trend research, product idea intake, niche validation, design/product briefs, IP/common-sense review packets, listing drafts, asset prep, publish gates, and signal capture.

Marketplace store agents may draft and prepare. They may not publish listings or change live marketplace state without human approval.

## Material Workflow Change

A change significant enough that an active workspace may need to return to `manual_test` or `onboarding`.

Examples:

- new external integration
- new customer-facing deliverable type
- new marketplace or channel
- new agent with expanded permissions
- new private data source
- new Observatory signal category
- new paid action path
- new publishing path
- new automation mode
- major review gate change

## Metadata

Secondary data about a record.

Metadata must be bounded and justified.

Unbounded metadata becomes JSON sludge.

## Multi-Workspace System

A system designed to host many isolated workspaces while allowing shared learning only through governed paths such as the Observatory.

Neon Ronin is a multi-workspace system.

---

# N

## Neon Ronin

A human-controlled, business-neutral, multi-workspace agent orchestration platform for onboarding, testing, operating, and learning from multiple small-business workspaces.

Neon Ronin is the operating system, not a single business.

## Non-Goal

A thing a doc, schema, workflow, or subsystem explicitly does not define or must not become.

Every schema should define non-goals.

## Normalization

The process of converting an approved record into a standard platform or Observatory shape.

Normalization must not erase provenance or silently upgrade weak evidence into strong evidence.

## Normalized Record

A record converted into a standard Neon Ronin or Observatory format.

Normalized records must remain traceable to source records.

---

# O

## Observatory

Neon Ronin's shared intelligence layer.

The Observatory receives approved sanitized signals from workspaces, normalizes them, scores or clusters them if allowed, and returns generalized intelligence to permitted workspaces.

The Observatory is shared intelligence, not shared private memory.

## Observatory Inbox

The conceptual zone where approved sanitized signals wait for normalization.

The inbox is for Observatory processing, not general workspace browsing.

## Observatory-Owned Data

Data owned by the Observatory, such as sanitized signals, normalized signal records, derived intelligence, keyword clusters, trend profiles, opportunity scores, data quality notes, research queue items, strategy queue items, and Observatory query audit records.

## Observatory Query

A request from a permitted workspace or actor for generalized Observatory intelligence.

Canonical early query types:

- `keyword_cluster`
- `trend_profile`
- `competitor_pattern`
- `opportunity_score`
- `prior_signal_check`
- `data_quality_check`

Observatory queries must not expose private workspace data.

## Observatory Signal

A sanitized, generalized signal accepted into or owned by the Observatory.

Use `sanitized signal` when referring to the approved signal itself. Use `normalized Observatory record` when referring to the standardized Observatory representation.

## On-Demand

A runtime mode where agents or workflows run only when started by a human.

On-demand does not mean ungated.

## Onboarding

A workspace lifecycle status and process where a business idea is defined, classified, scoped, configured, and prepared for manual testing.

Onboarding workspaces cannot run autonomous operations or external writes.

## Opportunity Score

A derived score representing potential opportunity strength based on approved signals, evidence, criteria, or research.

An opportunity score is derived data.

A score is not a decision.

## Out-Of-Scope Distraction

A proposed feature, schema, workflow, integration, or idea that does not support the current roadmap, creates premature complexity, or weakens platform boundaries.

Out-of-scope distractions should be rejected or parked.

---

# P

## Park

A review or planning decision meaning hold without further action for now.

Parked items remain visible and auditable but do not proceed.

## Parked Signal

A signal candidate held for later review or more evidence.

Parked signals do not enter the Observatory.

## Paused

A workspace lifecycle status and runtime mode indicating state is preserved but new work is blocked.

Paused workspaces may not start new agent runs, scheduled jobs, watch-mode jobs, external actions, review items, or Observatory submissions.

## Permission Scope

A bounded permission definition for an actor, agent, integration, workflow, or runtime process.

Permissions should be scoped by workspace, actor, action class, external service, review state, and runtime mode.

Permissions must enforce review gates, not bypass them.

## Platform Capability

A reusable Neon Ronin capability that supports multiple workspace types.

Examples:

- workspace config schema
- review queue
- audit log
- draft artifact system
- signal capture
- sanitization gate
- agent runtime contract
- permission scope model
- workspace lifecycle model

## Provenance

Traceable context describing origin, scope, actor, time, source, evidence, and transformation history.

Provenance should answer where a record came from and what supports it.

If provenance is lost, trust is lost.

## Publish Gate

A review gate requiring human approval before public, marketplace, content, product, or customer-visible publishing.

Agents may prepare publish packets, but they may not publish by themselves.

---

# Q

## QA Agent

A generic agent role that checks quality, completeness, consistency, evidence, policy concerns, and review readiness.

QA agents may recommend, flag, and queue review items. They do not approve their own work.

## Quality Gate

A review gate focused on completeness, accuracy, consistency, evidence quality, claims, and output readiness.

## Query Result

The response to an Observatory or system query.

Query results must preserve appropriate provenance, avoid private data leakage, and indicate confidence or data quality where useful.

---

# R

## Raw Data

Unprocessed input or observation retained in its original or closest available form.

Raw data is usually workspace-owned or integration-owned.

Raw private data must not enter the Observatory.

## Raw Record

A record preserving raw or near-raw input.

Raw records must not be confused with sanitized, normalized, or derived records.

## Raw Signal

An unsanitized observation created inside a workspace.

Raw signals are workspace-owned and do not enter the Observatory directly.

## Read-Without-Ownership

A boundary rule meaning a component may read or reference data without becoming the owner of that data.

Examples:

- a workspace queries Observatory intelligence without owning Observatory records
- an audit record references a run without becoming the run
- a review item references an artifact without owning the artifact content

## Recommendation Packet

A structured draft output containing a suggested action, rationale, evidence summary, uncertainty, and review needs.

A recommendation packet is not approval.

## Rejected Signal

A signal candidate blocked from Observatory intake.

Rejected signals remain auditable.

## Retired

A workspace lifecycle status meaning the workspace is closed for new operations and kept only for history, audit, archive, or export.

Retirement is not deletion.

## Review Gate

A human control point that must be passed before risky, public-facing, customer-facing, paid, destructive, credential-related, compliance-sensitive, or publishing actions proceed.

Examples:

- quality gate
- publish gate
- paid action gate
- data privacy gate
- customer delivery gate
- rights and compliance gate
- signal sanitization gate
- IP/common-sense gate
- strategy review gate

## Review Item

A unit of work awaiting human review.

Review items should include workspace id, source actor, output type, risk category, required gates, linked artifacts or signal candidates, recommended action, decision status, and audit references.

## Review Queue

The platform queue where risky or important outputs wait for human decision.

The review queue keeps humans in control while allowing agents to assist with research, drafting, organization, and preparation.

## Reviewed Record

A record that has passed through a human review gate.

Reviewed does not necessarily mean approved.

## Risk Category

A classification describing why an item needs review.

Risk categories may include public-facing, customer-facing, paid, destructive, credential-related, compliance-sensitive, privacy-sensitive, IP/rights-sensitive, or external-write-sensitive.

## Runtime Mode

The operating mode controlling how work may start or run.

Canonical runtime modes:

| Mode | Meaning |
|---|---|
| `off` | No background work runs |
| `on_demand` | Work starts only when started by a human |
| `scheduled` | Approved jobs run on schedules |
| `watch_mode` | Approved monitors run within limits |
| `paused` | State saved; no new work starts |
| `emergency_stop` | Active runs stop and new work is blocked |

Runtime modes are constrained by workspace lifecycle status.

---

# S

## Sanitization

The process of removing, redacting, or generalizing private, identifying, confidential, or business-specific details so a signal may safely become Observatory-eligible.

Sanitization is the gate between workspace-private data and shared intelligence.

## Sanitization Gate

The review or validation step that determines whether a signal candidate may enter the Observatory.

Early Neon Ronin requires human approval before Observatory intake.

## Sanitized Signal

An approved generalized signal eligible for Observatory intake.

Sanitized signals must not contain private workspace/customer details.

## Schema

A structured definition of a record family, fields, statuses, transitions, relationships, provenance, audit requirements, ownership, and non-goals.

Schema docs are planning docs before implementation.

They are not database migrations yet.

## Schema Authority

The governed decision layer defining which schema families Neon Ronin may define, what each owns, and what must not become schema yet.

Schema authority is defined in `docs/core/14-schema-authority.md`.

## Schema Family

A related group of records modeling one governed platform concept.

Examples:

- workspace records
- agent records
- signal records
- review records
- audit records
- Observatory records

## Specific Business Candidate

A real or future business idea that may become a workspace.

Specific business candidates are allowed to provide concrete planning pressure.

They are not allowed to become Neon Ronin core doctrine.

Specific-business details must stay outside core unless extracted as reusable platform capabilities.

## Service Business Workspace

A workspace type for customer-specific service work.

Typical needs include customer intake, research, deliverable drafting, QA, delivery preparation, customer-safe storage, raw signal capture, and signal sanitization.

Service business agents may draft and prepare. They may not deliver customer-facing outputs without human approval.

## Signal

A useful observation from a workspace, workflow, agent, human, artifact, market, customer pattern, or research process that may inform future decisions or shared intelligence.

Signals move through lifecycle forms such as raw signal, signal candidate, sanitized signal, normalized Observatory record, and derived intelligence.

## Signal Candidate

A proposed sanitized version of a raw signal waiting for review or validation.

Signal candidates do not enter the Observatory until approved through the sanitization gate.

## Signal Capture

The process of identifying and recording useful observations that may become signal candidates or remain workspace-local.

## Signal Source

The workspace, agent, human, artifact, workflow, integration, or source record that produced the observation behind a signal.

## Source Context

The origin information that explains where a record came from, including workspace, actor, source artifact, source run, external provider, or input event.

## Source Reference

A thin reference to a source record, artifact, run, review item, external resource, or signal.

A source reference is a pointer, not ownership transfer.

## Structured Record

A record extracted or organized from raw input into defined fields.

Structured records should preserve references back to source context.

## System Invariant

A non-negotiable condition that must remain true for Neon Ronin to remain Neon Ronin.

If a change violates an invariant, the change is wrong unless the invariant is revised through an ADR.

## System-Owned Field

A field that callers, agents, workspace configs, or integrations may not set directly.

Examples may include created timestamp, audit id, approval status, lifecycle transition result, normalized Observatory id, and system-computed score.

---

# T

## Task

A unit of work to be performed by a human, agent, workflow, or system process.

Task and job concepts should remain bounded and not become hidden execution ledgers before schema authority allows them.

## Tenant

A metaphor for a workspace inside Neon Ronin.

Businesses are tenants.

Neon Ronin is the building.

## Trend Profile

A generalized Observatory output describing seasonality, trend direction, market movement, or observed pattern over time.

Trend profiles are derived intelligence and must preserve provenance.

---

# U

## Unknown Field

A field not defined by a schema.

Future implementation contracts should reject unknown fields for core schemas unless a schema explicitly allows bounded metadata.

Unknown fields must not be allowed to smuggle business-specific meaning into core.

## Uncertainty

Known limitation, confidence gap, missing evidence, data quality issue, or unresolved question attached to a record or derived output.

Uncertainty should be preserved, not smoothed away.

---

# V

## Validation

The process of checking that a record, transition, action, signal, schema, or workflow follows Neon Ronin rules.

Validation may apply to structure, lifecycle, ownership, provenance, permissions, review state, and data boundaries.

## VEDA

A separate project whose observatory/database specification docs informed Neon Ronin's structural authority phase.

Neon Ronin borrows structural discipline from VEDA, not VEDA's exact system boundaries, entity names, or pure-observatory role.

## Verdict

A planning classification for ideas and proposals.

Canonical planning verdicts:

| Verdict | Meaning |
|---|---|
| `GREEN LIGHT` | Worth building or testing now |
| `YELLOW LIGHT` | Possible, but needs constraints or manual proof |
| `RED LIGHT` | Bad fit, premature, risky, or platform-drifting |
| `PARK` | Potentially good, wrong time |

---

# W

## Watch Mode

A runtime mode where approved monitoring jobs run within defined limits.

Watch mode is deferred and must not be used by manual-test workspaces.

## Workflow

A structured sequence of steps inside a workspace or adapter.

Workflows may involve humans, agents, artifacts, review gates, signals, audit records, and future integrations.

A workflow should not bypass review gates or lifecycle limits.

## Workspace

A business or project operating area inside Neon Ronin.

Each workspace has its own purpose, type, workflows, agents, rules, outputs, review gates, data access permissions, storage rules, audit requirements, and Observatory settings.

Workspaces are isolated by default.

## Workspace Adapter

A generic pattern for a type of workspace.

Adapters define common needs, workflows, agent roles, review gates, and rules for workspace types such as service business, marketplace store, digital product, content business, and internal research.

Adapters do not own private records for real businesses.

## Workspace Config

The structured configuration describing a workspace's identity, type, status, purpose, channels, allowed agents, review gates, Observatory permissions, storage rules, hard-no rules, and runtime constraints.

Workspace config is a P0 schema.

## Workspace Lifecycle

The status model and transition rules for workspaces.

Canonical statuses:

```text
idea -> onboarding -> manual_test -> active -> paused -> retired
```

Only listed transitions are allowed by default.

## Workspace-Owned Data

Private records owned by one workspace.

Examples include customer data, raw inputs, private drafts, artifacts, deliverables, workspace strategy, workspace-specific prompts, templates, offers, product details, and customer history.

Workspace-owned data does not cross boundaries directly.

## Workspace Type

A classification describing the kind of workspace.

Canonical workspace types:

| Workspace Type | Meaning |
|---|---|
| `service` | Customer-specific service business |
| `marketplace_store` | Product/listing marketplace business |
| `digital_products` | Downloadable or packaged digital product business |
| `content` | Publishing/media/content business |
| `internal_research` | Research/lab/strategy workspace |
| `hybrid` | Multiple workspace patterns combined |
| `other` | Not otherwise classified |

---

# X

No canonical X terms yet.

---

# Y

No canonical Y terms yet.

---

# Z

No canonical Z terms yet.

---

## Naming Rules

Use existing terms before inventing new ones.

Prefer:

| Prefer | Avoid |
|---|---|
| workspace | business backend |
| workspace adapter | business-specific core mode |
| artifact | random output blob |
| review item | approval todo |
| human decision | vague approval flag |
| signal candidate | maybe-useful note |
| sanitized signal | shared insight |
| Observatory query | cross-workspace lookup |
| external reference | provider-specific core field |
| derived intelligence | magic answer |
| provenance | source vibes |
| deferred domain | later maybe thing |

## Final Rule

```text
Clear words now prevent cursed schemas later.
```
