# Workspaces

## Purpose

This folder is the future home for real Neon Ronin workspace configs, workspace notes, manual-test records, and workspace-specific operating material.

It exists so real workspace details do not leak into `docs/core/`.

## Current Status

```text
No workspace configs are active yet.
```

Neon Ronin is still completing Phase 5C and Phase 5D cleanup before Phase 6 Internal Research begins.

Do not create Phase 6 workspace records here until Phase 5C and Phase 5D are complete.

## What Belongs Here Later

Use this folder for:

- actual workspace config drafts
- workspace-specific notes
- workspace-owned operating decisions
- workspace manual-test records
- workspace promotion notes
- workspace-specific artifact references
- workspace-specific intake summaries

## What Does Not Belong Here

Do not put these here:

- business-neutral core doctrine
- generic schema authority
- platform invariants
- ADRs that change platform authority
- raw secrets or credentials
- ignored audit reports
- prompts from audit sessions

## Internal Research Relationship To Business Intake

Internal Research is the planned first Neon Ronin workspace, but it is still a workspace candidate.

Because it is internal and low-risk, its intake may be lightweight, but it should still be represented as an intake/classification step before a workspace config is drafted.

The intake should establish:

- workspace type: `internal_research`
- purpose: evaluate business ideas, platform decisions, and opportunity signals
- private data posture: no customer data by default
- external action posture: none
- runtime posture: human-started manual/on-demand only
- Observatory posture: query and sanitized signal submission only if reviewed
- manual-test goal: validate artifact, review, audit, and signal flow without automation

## SearchClarity Relationship To This Folder

SearchClarity may later become a real workspace here only after Neon Ronin completes earlier roadmap gates and SearchClarity has enough manual-business evidence to model safely.

Until then, SearchClarity-aware worked examples belong in `docs/reference-examples/`, not `docs/core/`.

## Final Rule

```text
Real workspace details live with workspaces, not in core doctrine.
```
