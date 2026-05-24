# AGENTS.md - Neon Ronin LLM Entry Point

This file is the first context document for any LLM, coding agent, or assistant working in this repository.

Read this before proposing architecture, writing code, changing docs, or onboarding a business idea.

## Project Identity

Neon Ronin is a business-neutral, multi-workspace agent operating system.

Core principle:

```text
Neon Ronin is the operating system.
Each small business is a workspace.
Each workspace has its own workflows, agents, rules, outputs, and review gates.
The Observatory is shared intelligence.
The human remains the final decision-maker.
```

Neon Ronin exists to orchestrate agents across many small-business workspaces. Any single business is only one use case.

## What Neon Ronin Is

Neon Ronin is:

- an agent orchestration app
- a multi-workspace system
- a shared Observatory
- a data core
- a strategy layer
- a human-reviewed execution platform
- a platform for onboarding, testing, operating, and learning from small-business workspaces

## What Neon Ronin Is Not

Neon Ronin is not:

- a backend for one business
- a marketplace bot
- an autonomous publishing machine
- a single-purpose report generator
- a brand-specific workflow hardcoded into software
- an Etsy-only, Fiverr-only, Printify-only, or service-business-only tool

## First-Business Containment Rule

The first onboarded business is necessary, but dangerous.

It is allowed to shape implementation priorities. It is not allowed to define the platform.

```text
Neon Ronin may learn from the first business.
Neon Ronin must not become the first business.
```

During early development, every feature requested by the first onboarded business must be classified as one of:

1. Core platform capability
2. Workspace adapter capability
3. Workspace-specific configuration
4. External integration
5. Out-of-scope distraction

Nothing belongs in core until it passes the reusable capability test.

Good core capability examples:

- workspace config schema
- review queue
- draft artifact system
- audit log
- signal capture
- publish gate
- managed schedule
- agent runtime contract

Bad core capability examples:

- Etsy T-shirt listing generator
- SearchClarity-only report flow
- Printify-only product wizard
- one brand's customer language
- one marketplace account's assumptions

## Anti-Drift Rule

Core Neon Ronin docs and code must avoid specific business names unless the document is explicitly about that business or workspace.

Use generic terms in core:

| Avoid In Core | Use Instead |
|---|---|
| a specific service brand | service business workspace |
| a specific store brand | marketplace store workspace |
| a specific product line | product workspace |
| a specific customer-facing offer | service workflow |
| a specific marketplace account | connected marketplace channel |

When a real business needs support:

```text
1. Define what the business needs in its own docs/config.
2. Extract the generic Neon Ronin capabilities required.
3. Add reusable capabilities to Neon Ronin core.
4. Implement the business through a workspace adapter/configuration.
5. Keep business-specific language outside core docs.
```

## Human Control Rules

Agents are scoped workers. They do not have unlimited authority.

Hard-no rules:

```text
No autonomous publishing.
No autonomous spending.
No autonomous customer messaging.
No autonomous credential changes.
No autonomous destructive actions.
No agent approves its own work.
```

If an action is public-facing, customer-facing, paid, risky, credential-related, compliance-sensitive, or destructive, it must enter human review before execution.

Agents may:

- read approved data within limits
- analyze approved data
- draft artifacts
- prepare packets
- queue review items
- propose recommendations
- submit sanitized signal candidates

Agents must not independently:

- publish content or listings
- activate marketplace items
- message customers
- spend money
- issue refunds
- delete or revoke assets
- change credentials or permissions
- make final legal/IP/compliance decisions

## Workspace Model

A workspace is a business or project operating area inside Neon Ronin.

Each workspace should define:

- workspace name
- workspace type
- business purpose
- supported channels
- inputs
- outputs
- workflows
- agents
- data access permissions
- Observatory access
- signal feedback rules
- human review gates
- storage rules
- audit requirements

Workspace types currently recognized by the docs:

- service business
- marketplace store
- digital products
- content
- internal research
- hybrid
- other

Core rule:

```text
Workspace-specific data stays in the workspace.
Generalized intelligence may flow to the Observatory after sanitization.
```

## Observatory Rule

The Observatory is the only sanctioned cross-workspace intelligence channel.

It may store sanitized, generalized intelligence such as:

- workspace signals
- keyword clusters
- trend profiles
- competitor or market patterns
- opportunity scores
- data quality notes
- generalized observations
- research queue items
- strategy queue items

It must not store:

- private customer data
- raw credentials
- unsanitized customer notes
- workspace-private drafts
- confidential business details
- personally identifying information unless explicitly approved and required

## Business Onboarding Rule

A business does not become Neon Ronin. A business becomes a workspace inside Neon Ronin.

Canonical onboarding flow:

```text
business idea
-> business definition
-> workspace adapter requirements
-> reusable Neon Ronin capabilities
-> workspace configuration
-> workflows
-> agents
-> review gates
-> launch readiness
```

Workspace creation flow:

1. Create business intake
2. Classify business type
3. Select starter adapter
4. Identify workflows
5. Identify agents
6. Identify data sources
7. Identify outputs
8. Identify review gates
9. Identify Observatory feedback rules
10. Identify hard-no automation rules
11. Create workspace config
12. Run manual test
13. Add automation gradually
14. Promote workspace to active

Manual test rule:

```text
Do not automate a workflow until the manual version is understood.
```

## Build Order

Do not build automation before the runtime contract exists.

Do not onboard businesses before workspace boundaries exist.

Do not share signals before sanitization rules exist.

Recommended build order:

1. Platform doctrine
2. Core schemas
3. Manual workspace validation
4. Controlled agent assistance
5. Additional workspace types

Do not build yet:

- autonomous publishing
- autonomous spending
- cross-agent self-orchestration
- direct marketplace write actions
- unreviewed customer messaging

Neon Ronin should earn complexity gradually.

## Repository Map

| Path | Purpose |
|---|---|
| `AGENTS.md` | LLM entry point and operating rules |
| `docs/README.md` | Documentation index and anti-drift summary |
| `docs/core/` | Business-neutral Neon Ronin platform doctrine and architecture |
| `docs/workspace-adapters/` | Generic workspace patterns for types of businesses |
| `docs/decisions/` | Architecture decision records |
| `research-docs/` | Supporting research, feasibility notes, policy research, and experiments |
| `research-docs/archive/` | Archived research snapshots |

## Important Files To Read First

Read these before making architectural changes:

1. `AGENTS.md`
2. `docs/README.md`
3. `docs/core/00-origin-and-north-star.md`
4. `docs/core/01-platform-doctrine.md`
5. `docs/core/02-workspace-model.md`
6. `docs/core/03-business-onboarding.md`
7. `docs/core/04-observatory.md`
8. `docs/core/05-agent-runtime.md`
9. `docs/core/06-review-queue.md`
10. `docs/core/07-permissions-and-audit.md`
11. `docs/core/10-build-order.md`
12. `docs/decisions/adr-001-workspaces-not-hardcoded-businesses.md`

Read workspace adapter docs when working on a specific workspace type:

- `docs/workspace-adapters/service-business-workspace.md`
- `docs/workspace-adapters/marketplace-store-workspace.md`
- `docs/workspace-adapters/digital-product-workspace.md`
- `docs/workspace-adapters/content-business-workspace.md`
- `docs/workspace-adapters/internal-research-workspace.md`

Research docs are supporting context, not automatically core doctrine. Use them to understand why decisions were made, but prefer `docs/core/` and `docs/decisions/` as canonical unless the user says otherwise.

## LLM Operating Instructions

When working in this repo:

1. Preserve the platform/workspace separation.
2. Push back on drift, premature automation, and business-specific core logic.
3. Classify proposed changes before implementing them.
4. Prefer reusable platform capabilities over one-off business features.
5. Keep risky actions human-gated.
6. Keep workspace-private data isolated.
7. Route cross-workspace learning through sanitized Observatory signals only.
8. Treat the first onboarded business as a test tenant, not the product identity.
9. Keep docs and code aligned.
10. Check repository status before editing.
11. Do not overwrite user work.
12. Prefer small, reviewable changes.
13. When unsure, document the assumption and choose the safer, more generic platform boundary.

## Classification Checklist For New Ideas

Before green-lighting an idea, answer:

| Question | Purpose |
|---|---|
| Is this a workspace, core feature, adapter feature, integration, or distraction? | Prevents drift |
| What reusable Neon Ronin capability does it require? | Keeps core clean |
| What parts are business-specific? | Keeps workspace logic contained |
| What needs human approval? | Preserves control |
| What data must stay private? | Preserves isolation |
| What sanitized signals can feed the Observatory? | Enables shared learning |
| Can this be manually tested first? | Prevents premature automation |
| What would green-light more automation? | Requires evidence |
| What would kill or park the idea? | Avoids sunk-cost drift |

Use these verdicts during planning:

- `GREEN LIGHT`: worth building or testing now
- `YELLOW LIGHT`: possible, but needs constraints or manual proof
- `RED LIGHT`: bad fit, premature, risky, or platform-drifting
- `PARK`: potentially good, wrong time

## Final Rule

```text
Business docs define use cases.
Workspace adapters translate use cases.
Neon Ronin core defines reusable capabilities.
Humans make final decisions.
```