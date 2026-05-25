# First Workspace Decision Log

## Purpose

This operations document records major decisions made while preparing and validating the first Neon Ronin workspaces.

It exists so Neon Ronin does not make quiet architecture decisions through vibes, momentum, or first-business pressure.

## Core Rule

```text
If a workspace teaches Neon Ronin something important, record the decision before changing the platform.
```

This log is especially important for:

- Internal Research as Workspace 1
- SearchClarity as an early real business workspace
- any reusable capability extracted from a specific workspace
- any rejected or parked idea that might return later

## Relationship To Core Docs

This log must obey:

- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/14-schema-authority.md`
- `docs/core/glossary.md`
- `docs/core/schemas/business-intake.schema.md`
- `docs/core/schemas/human-decision.schema.md`

This log does not override ADRs or core docs.

Major architecture decisions still require ADRs.

## When To Add An Entry

Add an entry when deciding:

- whether an idea becomes a workspace candidate
- whether a workspace enters onboarding
- whether a workspace enters manual test
- whether a workspace becomes active
- whether a workspace should pause or retire
- whether a workspace-specific need is reusable
- whether a reusable need belongs in core, adapter, operations, or a workspace
- whether a deferred domain is being touched
- whether SearchClarity-specific details must stay isolated
- whether a schema or contract gap exists
- whether an ADR is needed

## Decision Entry Template

Copy this block for each decision.

```markdown
## Decision YYYY-MM-DD - Short Title

### Status

Proposed | Accepted | Rejected | Parked | Superseded

### Decision

What was decided?

### Context

What situation or workspace raised this decision?

### Workspace Involved

- Workspace name:
- Workspace type:
- Lifecycle status:

### Classification

- Core capability:
- Adapter pattern:
- Workspace-owned detail:
- Integration-owned detail:
- Observatory-owned detail:
- Deferred domain:
- Out of scope:

### Reasoning

Why is this the smart and optimal decision?

### Risks

What could go wrong if this is wrong?

### Boundaries Preserved

- Workspace isolation:
- Human review:
- Auditability:
- Provenance:
- Sanitization:
- Secret/credential safety:
- Provider-specific isolation:

### Follow-Up Actions

- [ ] Action 1
- [ ] Action 2

### Related Records Or Docs

- Link/path:

### ADR Needed?

Yes | No

If yes, proposed ADR title:
```

## Initial Decisions

## Decision 2026-05-24 - Use Internal Research Before SearchClarity

### Status

Accepted

### Decision

Neon Ronin should validate core platform mechanics with an Internal Research workspace before fully onboarding SearchClarity.

### Context

SearchClarity is a useful early business workspace candidate, but it is still a work in progress and contains business-specific service/report/customer-delivery details.

Internal Research exercises platform mechanics with less customer, marketplace, delivery, credential, and external-action risk.

### Workspace Involved

- Workspace name: Neon Ronin Internal Research
- Workspace type: internal_research
- Lifecycle status: planned/manual_test candidate

### Classification

- Core capability: workspace validation, artifacts, review queue, audit, signals, human decisions
- Adapter pattern: internal research workspace pattern
- Workspace-owned detail: specific research notes and platform planning artifacts
- Integration-owned detail: none
- Observatory-owned detail: sanitized/generalized platform signals only after review
- Deferred domain: scheduled agents, watch mode, external integrations
- Out of scope: customer-facing delivery

### Reasoning

Internal Research lets Neon Ronin validate its contracts before customer-facing business pressure distorts core.

### Risks

If skipped, SearchClarity may accidentally define core platform behavior before boundaries are operational.

### Boundaries Preserved

- Workspace isolation: yes
- Human review: yes
- Auditability: yes
- Provenance: yes
- Sanitization: yes
- Secret/credential safety: yes
- Provider-specific isolation: yes

### Follow-Up Actions

- [ ] Create Internal Research workspace draft config later.
- [ ] Run manual-test template against Internal Research.
- [ ] Record any reusable capability gaps.

### Related Records Or Docs

- `docs/ROADMAP.md`
- `docs/core/schemas/workspace-config.schema.md`
- `docs/core/schemas/artifact.schema.md`
- `docs/core/schemas/review-queue-item.schema.md`

### ADR Needed?

No. Existing roadmap and first-business containment ADR cover this posture.

## Decision 2026-05-24 - Treat SearchClarity Readiness As Parallel Business Track

### Status

Accepted

### Decision

SearchClarity business-readiness work should be tracked as a parallel dependency, not as Neon Ronin core work.

### Context

SearchClarity docs show a strong service-business concept but launch assets still need completion: sample report, PDF pipeline, tracker workbook, Fiverr copy, intake forms, SOP, QC checklist, pricing source of truth, and consent language.

### Workspace Involved

- Workspace name: SearchClarity
- Workspace type: service candidate
- Lifecycle status: business-build/pre-onboarding

### Classification

- Core capability: artifact/workflow/business-intake/review/audit/signal contracts
- Adapter pattern: service-business workspace adapter
- Workspace-owned detail: brand, offer, pricing, templates, Fiverr copy, customer records
- Integration-owned detail: future service-platform/marketplace references only
- Observatory-owned detail: sanitized generalized signals only
- Deferred domain: Fiverr automation, external integrations, marketplace publishing
- Out of scope: SearchClarity-specific schema in core

### Reasoning

SearchClarity should provide real workspace input later, but it must not hijack Neon Ronin core before manual business evidence exists.

### Risks

If SearchClarity is onboarded too early, report templates, service language, Fiverr assumptions, or customer-delivery details could leak into core.

### Boundaries Preserved

- Workspace isolation: yes
- Human review: yes
- Auditability: yes
- Provenance: yes
- Sanitization: yes
- Secret/credential safety: yes
- Provider-specific isolation: yes

### Follow-Up Actions

- [ ] Keep SearchClarity readiness visible in roadmap.
- [ ] Do not create SearchClarity-specific core schema.
- [ ] Revisit SearchClarity after Phase 5 and Internal Research validation.

### Related Records Or Docs

- `docs/ROADMAP.md`
- `docs/core/schemas/business-intake.schema.md`
- `docs/core/schemas/artifact.schema.md`
- `docs/core/18-external-integration-contract.md`

### ADR Needed?

No for now. Escalate to ADR if SearchClarity requires core authority changes.

## Maintenance Rule

This log should stay short enough to remain useful.

If a decision changes architecture, create an ADR.

If a decision is merely task tracking, put it in the relevant checklist instead.

## Final Rule

```text
Record the fork in the road before building the road.
```
