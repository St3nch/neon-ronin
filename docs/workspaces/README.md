# Workspaces

## Purpose

This folder is the future home for real Neon Ronin workspace configs, workspace notes, manual-test records, and workspace-specific operating material.

It exists so real workspace details do not leak into `docs/core/`.

## Current Status

```text
Internal Research has documentation-only manual_test records.
No workspace configs are active runtime configs yet.
```

Phase 5C and Phase 5D cleanup are complete.

Phase 6 preparation has moved Internal Research into documentation-only `manual_test` posture with `internal-research/intake-classification.md`, `internal-research/workspace-config.draft.md`, `internal-research/manual-test-001-artifact-review-audit-signal-flow.md`, `internal-research/manual-test-001-evidence.md`, `internal-research/promotion-review-001-onboarding-to-manual-test.md`, `internal-research/manual-test-002-llm-recommendation-assistance.md`, `internal-research/manual-test-002-evidence.md`, `internal-research/agent-assistance-boundary-plan.md`, `internal-research/manual-test-003-llm-draft-assistance.md`, `internal-research/manual-test-003-evidence.md`, `internal-research/propose-action-boundary-plan.md`, `internal-research/manual-test-004-llm-propose-action-assistance.md`, `internal-research/manual-test-004-evidence.md`, `internal-research/manual-test-005-local-schema-shape-consolidation.md`, `internal-research/manual-test-005-evidence.md`, `internal-research/implementation-readiness-decision.md`, `internal-research/minimal-implementation-plan-persistence-001.md`, `internal-research/first-proof-parameters-persistence-001.md`, `internal-research/implementation-start-decision-persistence-001.md`, and `internal-research/persistence-proof-001-evidence.md`.

Do not create active workspace configs here until the intake/classification step and workspace config draft are reviewed.

Implementation readiness is the next checkpoint before any executable platform slice, local schema reference, or customer-facing workspace onboarding.

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
