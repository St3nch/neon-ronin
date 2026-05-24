# ADR-003 - First-Business Containment

## Status

Accepted

## Context

Neon Ronin must eventually support many small-business workspaces.

However, the first real onboarded business will naturally influence early implementation priorities because it will expose concrete workflows, data needs, review gates, artifacts, and operational pain points.

This is useful and necessary.

It is also dangerous.

If the first business is allowed to directly define Neon Ronin core, the platform can drift into a one-business backend instead of remaining a reusable multi-workspace agent operating system.

The first business may be SearchClarity or another early workspace. Regardless of which business comes first, it must be treated as a tenant and test case, not as the identity of Neon Ronin.

## Decision

The first onboarded business may shape implementation priorities, but it must not define Neon Ronin core.

Core rule:

```text
Neon Ronin may learn from the first business.
Neon Ronin must not become the first business.
```

Every feature, schema, workflow, agent, integration, or document requested because of the first business must be classified before it is added.

Classification categories:

1. Core platform capability
2. Workspace adapter capability
3. Workspace-specific configuration or documentation
4. External integration
5. Out-of-scope distraction

Only reusable capabilities belong in Neon Ronin core.

Business-specific branding, customer language, service promises, report templates, package names, marketplace listings, pricing assumptions, customer history, delivery details, and channel-specific tactics must remain outside core.

## Classification Rules

### Core Platform Capability

A capability belongs in core only if it can reasonably support multiple workspace types.

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

### Workspace Adapter Capability

A capability belongs in a workspace adapter when it applies to a class of businesses but not all of Neon Ronin.

Examples:

- service business intake pattern
- marketplace store listing draft pattern
- digital product launch packet pattern
- content business editorial workflow
- internal research scoring packet pattern

### Workspace-Specific Configuration Or Documentation

A detail belongs in workspace-specific config or docs when it applies to one real business.

Examples:

- SearchClarity report language
- one service offer's package structure
- one store's product niche
- one business's customer delivery rules
- one brand's tone or positioning
- one workspace's private customer history

### External Integration

A capability belongs in an integration module when it depends on a specific external platform or API.

Examples:

- Etsy API draft listing creation
- Printify product publishing
- Fiverr order intake
- OpenAI or Anthropic API calls
- payment processor callbacks
- marketplace OAuth flows

External integrations must obey Neon Ronin core review gates, audit rules, permissions, and runtime modes.

### Out-Of-Scope Distraction

An idea should be parked or rejected when it does not support the current roadmap, creates premature complexity, or weakens the platform boundary.

Examples:

- autonomous publishing before manual validation
- marketplace automation before review gates exist
- multi-user SaaS features before single-operator workflows work
- UI polish before schemas exist
- business-specific shortcuts in core

## Required Mechanism

During early development, every first-business-driven change must answer:

1. What business need triggered this?
2. Is the need reusable across workspaces?
3. Which classification category does it belong to?
4. What review gates are required?
5. What data must remain workspace-private?
6. What sanitized signals may flow to the Observatory?
7. Can this be manually tested before automation?
8. What would prove this deserves automation?
9. What would cause this to be rejected or parked?

If the answer is unclear, choose the safer and more generic boundary.

## Consequences

- Neon Ronin can use the first business to discover real platform requirements.
- The first business cannot silently smuggle business-specific assumptions into core.
- Future workspaces remain possible because core stays reusable.
- Workspace adapters carry business-type patterns without polluting the platform.
- Business-specific docs and configs remain isolated.
- External integrations remain subordinate to Neon Ronin's review, audit, permission, and runtime rules.

## Implementation Notes

A future operations document should maintain a first-workspace decision log.

The decision log should record first-business-driven changes and their classification.

Recommended future file:

```text
docs/operations/first-workspace-decision-log.md
```

Until that file exists, planning discussions and ADRs must explicitly classify first-business-driven ideas.

## Final Rule

```text
The first business is a proving ground.
It is not the platform.
```
