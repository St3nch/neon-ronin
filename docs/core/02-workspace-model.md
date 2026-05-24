# 02 - Workspace Model

## Purpose

This document defines the generic workspace model for Neon Ronin.

A workspace is a business or project operating area inside Neon Ronin.

## Workspace Requirements

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

## Workspace Types

| Workspace Type | Typical Needs | Example Outputs |
|---|---|---|
| Service Business | Customer intake, research, deliverable drafting, QA, delivery, customer history | Reports, audits, recommendations, customer notes |
| Marketplace Store | Product research, listing drafts, asset management, policy checks, publishing gates | Listing drafts, product ideas, mockups, launch packets |
| Digital Product Business | Topic validation, product packaging, copywriting, asset creation, launch prep | Templates, PDFs, guides, sales pages |
| Content Business | Research queue, editorial planning, drafting, SEO review, publishing prep | Articles, briefs, content calendars |
| Internal Research Lab | Market monitoring, experiments, scoring, notes, decision logs | Research packets, opportunity scores, strategy notes |

## Generic Workspace Schema

```yaml
workspace_id: string
workspace_name: string
workspace_type: service | marketplace_store | digital_products | content | internal_research | hybrid | other
status: idea | onboarding | manual_test | active | paused | retired

purpose: string
channels:
  - marketplace
  - service_platform
  - direct_site
  - social_platform
  - content_platform
  - other

allowed_agents:
  - string

review_gates:
  - string

observatory:
  can_query: boolean
  can_submit_sanitized_signals: boolean

storage_rules:
  workspace_private_data: true
  generalized_signals_allowed_after_sanitization: true
```

## Rule

```text
Workspace-specific data stays in the workspace.
Generalized intelligence may flow to the Observatory after sanitization.
```
