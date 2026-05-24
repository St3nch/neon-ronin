# ADR-002 - Research Docs Are Supporting Context

## Status

Accepted

## Context

Neon Ronin contains two kinds of project knowledge:

1. Canonical platform doctrine and architecture in `docs/core/` and `docs/decisions/`
2. Supporting research, feasibility notes, policy research, experiments, and historical reasoning in `research-docs/`

The research documents are valuable because they explain why certain ideas, risks, and architecture directions were considered.

However, research documents may use concrete business examples, dated platform details, vendor-specific assumptions, or exploratory recommendations.

If future humans or LLMs treat research documents as canonical platform doctrine, Neon Ronin could drift toward one business, one marketplace, one service workflow, or one old research conclusion.

This is especially risky because some research docs discuss concrete examples such as service business workspaces or marketplace store workspaces in more specific terms than the core docs.

## Decision

`research-docs/` are supporting context, not canonical doctrine.

Canonical Neon Ronin doctrine lives in:

- `AGENTS.md`
- `docs/README.md`
- `docs/core/`
- `docs/workspace-adapters/`
- `docs/decisions/`

When there is a conflict between research documents and core doctrine, core doctrine wins unless a new ADR explicitly changes the decision.

Research findings may become canonical only after they are promoted into:

- a core doc
- a workspace adapter doc
- a schema doc
- an operations doc
- an ADR

## Rules

```text
Research informs Neon Ronin.
Research does not define Neon Ronin.
```

```text
Concrete examples in research docs are examples.
They are not platform doctrine.
```

```text
A research recommendation becomes binding only when promoted through core docs or ADRs.
```

## Consequences

- Future LLMs should read `research-docs/` for context, not as the source of truth.
- Core platform docs remain business-neutral.
- Business-specific examples in research docs cannot silently become core architecture.
- Old research can remain useful without creating architectural drift.
- Research conclusions must be deliberately promoted before they guide implementation.

## Implementation Notes

When using research docs during planning:

1. Identify the relevant research finding.
2. Classify whether it is generic platform capability, workspace adapter guidance, workspace-specific detail, external integration detail, or obsolete context.
3. Promote only reusable or intentionally accepted conclusions into canonical docs.
4. Use an ADR when the promoted conclusion changes architecture, build order, or platform doctrine.

## Final Rule

```text
Use research as evidence.
Use core docs and ADRs as authority.
```
