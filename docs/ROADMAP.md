# Neon Ronin Roadmap

## Purpose

This roadmap is the compact, canonical navigation document for Neon Ronin's build sequence.

It answers:

- where the project is now
- what phases are complete
- what phase is active
- what is blocked or deferred
- what evidence documents hold the detail

Detailed phase history lives in `docs/roadmap/phase-history.md`.

Core rule:

```text
Prepare Neon Ronin for SearchClarity.
Do not turn Neon Ronin into SearchClarity.
```

## Roadmap Doctrine

Neon Ronin follows the build order defined in `docs/core/10-build-order.md`:

```text
Doctrine -> Structural Authority -> Schemas -> Manual Workspace Validation -> Controlled Agent Assistance -> Additional Workspace Types
```

Borrow structural rigor from prior systems, but do not import their project assumptions, entity names, or boundaries.

Neon Ronin is the multi-workspace agent operating system. SearchClarity and any other business are future workspaces, not core doctrine.

## Current Status

Neon Ronin is in Phase 6: Internal Research validation and first local persistence proof work.

Current implementation posture:

```text
status: manual_test
runtime.default_mode: off
allowed_agents: []
scheduled_allowed: false
watch_mode_allowed: false
external_references: []
```

Current proof command:

```text
python tools/dev/check_first_proof.py
```

Expected result:

```text
Ran 87 tests
OK
```

## Current Constraints

Do not add or start any of the following without a separate explicit decision:

- new persistence tables
- new domain records
- new schemas
- UI or desktop shell work
- agents or agent runtime
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing onboarding
- SearchClarity onboarding
- automation
- external writes
- marketplace actions
- customer delivery
- autonomous spending or publishing

Planning docs do not need fake canonical human-decision records for every low-risk refinement.

Canonical human-decision records are required for meaningful gates, including implementation start, schema authority changes, runtime enablement, agent enablement, integrations, external actions, customer-facing work, workspace promotion, SearchClarity onboarding, and local packet-shape promotion.

## Phase Summary

| Phase | Name | Status | Current Outcome | Detail Source |
|---|---|---|---|---|
| 0 | Foundation Lock | Completed | Canonical doctrine base stabilized. | `AGENTS.md`, `docs/core/00-origin-and-north-star.md`, ADRs |
| 1 | Core Boundary Specs | Completed | Lifecycle, sanitization, onboarding, and Observatory boundaries established. | `docs/core/08-sanitization.md`, `docs/core/09-workspace-lifecycle.md`, ADR 004 |
| 2 | Structural Authority Layer | Completed | Data ownership, invariants, provenance, schema authority, and glossary defined. | `docs/core/11-data-boundaries.md` through `docs/core/14-schema-authority.md`, `docs/core/glossary.md` |
| 3 | P0 Platform Schemas | Completed | Workspace, review, audit, signal, agent definition, and agent-run schema docs created. | `docs/core/schemas/` |
| 4 | P1 Platform Schemas And Contracts | Completed | Artifact, workflow, business intake, human decision, permission, error, scoring, secrets, and integration contracts defined. | `docs/core/schemas/`, `docs/core/15-secrets-and-credentials.md` through `docs/core/18-external-integration-contract.md` |
| 5 | Operations Layer | Completed | Operational checklists and runbooks created. | `docs/operations/` |
| 5B | Hammer Testing Doctrine | Completed | Hammer testing posture defined before serious implementation. | `docs/core/19-hammer-testing-doctrine.md` |
| 5C | Core Example Separation | Completed | Concrete business examples separated from core doctrine. | `docs/reference-examples/`, `docs/workspaces/` |
| 5D | DB Reliability And Schema Clarification | Completed | Version semantics, transaction boundaries, status vocabulary, and resolver concerns clarified. | `docs/core/14-schema-authority.md`, `docs/core/20-transaction-boundaries.md`, schema docs |
| 6 | Workspace 1: Internal Research | Active | Manual validation and first executable persistence proof are underway. | `docs/workspaces/internal-research/`, `packages/neon-core/` |
| 6A | Post-Claude Audit Cleanup And Stabilization | Completed | Immediate audit cleanup completed; proof remains green. | `docs/roadmap/phase-history.md`, persistence proof docs |
| 7 | SearchClarity Compatibility Preparation | Blocked | Waits for Phase 6 sufficiency and SearchClarity business-readiness evidence. | Future workspace planning |

## Active Phase: Phase 6 - Internal Research

Goal:

Validate Neon Ronin using a low-risk internal workspace before onboarding SearchClarity or any customer-facing workspace.

Internal Research is allowed to exercise:

- human-started research tasks
- internal research packets
- idea scoring packets
- review queue items
- sanitized signal candidates
- audit records
- documentation-only LLM recommendation assistance as reviewable artifacts
- documentation-only LLM draft/propose-action assistance through manual evidence passes

Internal Research must not introduce customer pressure, marketplace pressure, paid delivery pressure, business-specific report formats, or SearchClarity-specific core assumptions.

## Phase 6 Current Proof State

The first executable persistence proof exists and remains local/constrained.

Authorized tables:

- `workspace_configs`
- `audit_records`
- `review_queue_items`
- `human_decisions`
- `signal_candidates`
- `artifact_metadata`
- `workflow_records`

Implemented operations:

- `workspace_config_create`
- `workspace_config_update`
- `review_queue_item_create`
- `human_decision_record`
- `signal_candidate_create`
- `artifact_metadata_create`
- `workflow_record_create`

Core audit-first invariant:

```text
No required audit record means no consequential persisted record or state change.
```

The proof is intentionally not a production database layer, UI, service, agent runtime, integration layer, scheduler, watch system, Observatory ingestion path, customer-facing workspace, SearchClarity onboarding path, or automation surface.

## Phase 6 Exit Criteria

Before SearchClarity enters Neon Ronin planning, Internal Research should prove that:

1. A workspace can be created from config.
2. A manual workflow can produce artifacts.
3. A review queue item can be created and resolved.
4. An audit record can trace the work.
5. A signal candidate can be sanitized or rejected.
6. A platform decision can be recorded without business-specific contamination.
7. Provenance is preserved across raw, structured, sanitized, and derived records.

## Current Decision Point

Phase 6 is healthy but not closed.

Recommended next action:

- complete a docs-only Phase 6 checkpoint review
- map current evidence against the Phase 6 exit criteria
- decide whether remaining gaps require docs-only cleanup, tests-only proof, new implementation, or pause

No new persistence boundary is currently authorized.

## SearchClarity Readiness Track

SearchClarity remains a parallel business-readiness track, not Neon Ronin core work.

SearchClarity-specific brand language, offers, pricing, report templates, customer intake forms, customer/order/report records, delivery messages, client-specific observations, and consent records must remain SearchClarity workspace-owned or business-owned.

SearchClarity Compatibility Preparation begins only when:

1. Neon Ronin has completed enough Phase 6 validation to enforce boundaries.
2. SearchClarity has enough manual-business evidence to model safely.
3. SearchClarity-specific needs can be classified as workspace-owned, adapter-owned, reusable core capability, integration-owned, or out-of-scope.
4. SearchClarity can be inspected without turning its docs into Neon Ronin doctrine.

## Historical References

Use these files for details instead of expanding this roadmap:

- `docs/roadmap/phase-history.md`
- `docs/core/`
- `docs/core/schemas/`
- `docs/operations/`
- `docs/workspaces/internal-research/`
- `packages/neon-core/src/neon_ronin_core/persistence/README.md`
- `tools/hammers/README.md`
