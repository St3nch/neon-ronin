# 03 - Business Onboarding

## Purpose

This document defines how Neon Ronin onboards a new business without allowing that business to distort the core platform.

Neon Ronin must support multiple future businesses, experiments, service workflows, marketplace stores, and digital products.

A business does not become Neon Ronin.

A business becomes a workspace inside Neon Ronin.

## Core Onboarding Flow

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

## Onboarding Principle

When adding a new business, do not start by building random features.

Start by answering:

- What does this business need to do?
- Which parts are business-specific?
- Which parts are reusable Neon Ronin capabilities?
- What needs human approval?
- What data must stay private?
- What signals can feed the Observatory?

Neon Ronin should only absorb reusable capabilities.

Business-specific branding, offers, product names, customer language, listings, templates, and delivery details stay inside the workspace or business docs.

## Business Type Classification

| Business Type | Description |
|---|---|
| Service Business | Produces customer-specific deliverables |
| Marketplace Store | Sells products/listings on marketplaces |
| Digital Product Business | Sells downloadable or packaged digital products |
| Content Business | Publishes articles, videos, newsletters, or media |
| Internal Research Project | Produces strategy, research, or internal decisions |
| Hybrid Business | Combines multiple types |

## Workspace Creation Flow

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

## Capability Extraction

| Business Need | Generic Neon Ronin Capability |
|---|---|
| customer submits request | intake workflow |
| product idea needs validation | idea review workflow |
| agent researches keywords | Observatory query |
| agent drafts output | draft artifact system |
| human reviews output | review queue |
| public publishing needed | publish gate |
| customer delivery needed | delivery gate |
| market insight found | signal capture |
| agent work runs repeatedly | managed schedule |
| output needs traceability | audit logs |

If a capability is only useful to one business, keep it in the workspace.

If it is reusable, add it to Neon Ronin core.

## Manual Test Requirement

Every new business should prove its workflow manually before Neon Ronin automates it.

Rule:

```text
Do not automate a workflow until the manual version is understood.
```

## Final Principle

```text
Neon Ronin does not absorb businesses.
Neon Ronin hosts workspaces.
```
