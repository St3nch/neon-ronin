# Neon Ronin Roadmap Phase History

## Purpose

This file preserves condensed historical roadmap detail so `docs/ROADMAP.md` can stay readable and action-oriented.

It is supporting roadmap history, not a replacement for canonical doctrine, schema docs, ADRs, operations docs, or workspace evidence.

## Phase 0 - Foundation Lock

Status: completed.

Outcome:

- Canonical LLM/project entry point established in `AGENTS.md`.
- Origin and north-star doctrine added.
- Docs index corrected to point at `research-docs/` as supporting context.
- Research docs and first-business containment decisions captured in ADRs.

Primary references:

- `AGENTS.md`
- `docs/core/00-origin-and-north-star.md`
- `docs/README.md`
- `docs/decisions/adr-002-research-docs-are-supporting-context.md`
- `docs/decisions/adr-003-first-business-containment.md`

## Phase 1 - Core Boundary Specs

Status: completed.

Outcome:

- Signal sanitization, workspace lifecycle, runtime-by-status, manual-test promotion, and Observatory shared-intelligence boundaries were defined.
- Observatory was established as shared intelligence, not shared private memory.

Primary references:

- `docs/core/08-sanitization.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/decisions/adr-004-observatory-shared-intelligence-boundary.md`

## Phase 2 - Structural Authority Layer

Status: completed.

Outcome:

- Ownership, invariants, provenance, schema authority, and canonical vocabulary were defined before implementation.
- Deferred domains were blocked from receiving ad hoc schemas or convenience fields.

Primary references:

- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/14-schema-authority.md`
- `docs/core/glossary.md`

## Phase 3 - P0 Platform Schemas

Status: completed.

Outcome:

- Minimum platform schema docs were created for workspace config, review queue items, audit records, signals, agent definitions, and agent runs.
- Schemas remained business-neutral and SearchClarity-free.

Primary references:

- `docs/core/schemas/workspace-config.schema.md`
- `docs/core/schemas/review-queue-item.schema.md`
- `docs/core/schemas/audit-record.schema.md`
- `docs/core/schemas/signal.schema.md`
- `docs/core/schemas/agent-definition.schema.md`
- `docs/core/schemas/agent-run.schema.md`

## Phase 4 - P1 Platform Schemas And Contracts

Status: completed.

Outcome:

- First serious manual-workflow contract layer completed.
- Artifact, workflow, business intake, human decision, permission, secrets, error/failure, Observatory scoring, and external integration boundaries were defined before runtime work.

Primary references:

- `docs/core/schemas/artifact.schema.md`
- `docs/core/schemas/workflow.schema.md`
- `docs/core/schemas/business-intake.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/core/schemas/permission-scope.schema.md`
- `docs/core/15-secrets-and-credentials.md`
- `docs/core/16-error-and-failure-handling.md`
- `docs/core/17-observatory-scoring-contract.md`
- `docs/core/18-external-integration-contract.md`

## Parallel Track - SearchClarity Business Readiness

Status: not started in Neon Ronin.

Outcome so far:

- SearchClarity has been identified as future workspace pressure and supporting context, not core doctrine.
- SearchClarity remains blocked from Neon Ronin onboarding until both Neon Ronin Phase 6 and SearchClarity business-readiness evidence are sufficient.

SearchClarity artifacts that must remain workspace-owned or business-owned include brand language, offers, pricing, Fiverr copy, buyer-facing report language, templates, customer intake forms, customer/order/report records, delivery messages, client-specific recommendations, raw client observations, and consent records.

## Phase 5 - Operations Layer

Status: completed.

Outcome:

- Operational documents were added so manual tests, workspace promotion, review queue operations, emergency stop, and schema changes can be recorded consistently.

Primary references:

- `docs/operations/first-workspace-decision-log.md`
- `docs/operations/workspace-onboarding-checklist.md`
- `docs/operations/manual-test-template.md`
- `docs/operations/workspace-promotion-checklist.md`
- `docs/operations/review-queue-runbook.md`
- `docs/operations/emergency-stop-procedure.md`
- `docs/operations/schema-change-checklist.md`

## Phase 5B - Hammer Testing Doctrine

Status: completed.

Outcome:

- Hammer testing was defined as stress verification, separate from ordinary unit testing.
- Future hammer categories were named for persistence, contracts, boundaries, workspace isolation, Observatory, review gates, audit, permissions, agent runs, artifacts, signals, rollback, schema drift, integrations, and emergency stop.

Primary reference:

- `docs/core/19-hammer-testing-doctrine.md`

## Phase 5C - Core Example Separation

Status: completed.

Outcome:

- Concrete examples were separated from core doctrine.
- SearchClarity-specific examples, IDs, filenames, package names, and business assumptions were removed from canonical core posture or given non-core homes.

Primary references:

- `docs/reference-examples/README.md`
- `docs/workspaces/README.md`
- `docs/core/`
- `docs/core/schemas/`

## Phase 5D - DB Reliability And Schema Clarification

Status: completed.

Outcome:

- Generic `version` semantics were split into `schema_version` and `record_revision`.
- Polymorphic record-type vocabulary and recurring status semantics were clarified.
- Phase-6-relevant transaction boundaries were named.
- Audit-first behavior was clarified as transaction-aware.
- Future DB planning concerns were captured without choosing a production database architecture.

Primary references:

- `docs/core/14-schema-authority.md`
- `docs/core/16-error-and-failure-handling.md`
- `docs/core/19-hammer-testing-doctrine.md`
- `docs/core/20-transaction-boundaries.md`
- `docs/core/schemas/`

## Phase 6 - Workspace 1: Internal Research

Status: active.

Outcome so far:

- Internal Research intake/classification completed.
- Workspace config draft created.
- Manual Tests 001 through 005 completed as documentation/manual evidence.
- Internal Research promoted to documentation-only `manual_test` posture.
- Implementation readiness checkpoint completed.
- Minimal persistence proof plan and first proof parameters approved with conditions.
- First local SQLite audit-first persistence proof implemented.
- Next persistence boundary options recorded without automatically authorizing implementation.
- Current executable proof expanded through the authorized persistence boundaries listed below.

Implemented persistence operations:

- `workspace_config_create`
- `workspace_config_update`
- `review_queue_item_create`
- `human_decision_record`
- `signal_candidate_create`
- `artifact_metadata_create`
- `workflow_record_create`

Authorized tables in the current proof:

- `workspace_configs`
- `audit_records`
- `review_queue_items`
- `human_decisions`
- `signal_candidates`
- `artifact_metadata`
- `workflow_records`

Current validation:

```text
python tools/dev/check_first_proof.py
Ran 92 tests
OK
```

The tests-only cross-boundary proof now verifies the existing authorized records can compose into:

- a manual workflow -> metadata-only artifact -> review item -> human decision chain
- a signal candidate -> sanitization review item -> human rejection decision chain without Observatory ingestion
- business-neutrality rejection tests for customer-facing, SearchClarity-shaped, and external-action shortcuts

Important proof limits:

- signal candidate persistence only; no raw signal persistence, sanitized signal persistence, or Observatory submission
- artifact metadata only; no blob/content storage, delivery-ready marking, or public-use approval
- workflow definition only; no execution, scheduling, watch mode, agents, or integrations
- no new persistence table or domain record without a separate implementation-start decision

Primary references:

- `docs/workspaces/internal-research/`
- `docs/workspaces/internal-research/persistence-proof-001-evidence.md`
- `docs/workspaces/internal-research/next-persistence-boundary-decision.md`
- `packages/neon-core/src/neon_ronin_core/persistence/README.md`
- `tools/hammers/run_first_persistence_proof.py`
- `tools/dev/check_first_proof.py`

## Phase 6A - Post-Claude Audit Cleanup And Stabilization

Status: completed.

Outcome:

- External Claude audit returned `PASS WITH FINDINGS` with no blockers, no high-severity findings, no doctrine breach, no forbidden runtime surfaces, and no audit-first invariant failure.
- Dead split debris was removed from `validators.py`.
- Unused imports were removed from split persistence modules.
- ROADMAP and hammer command references were synchronized with the current proof runner.
- Manual-test promotion statuses were normalized from `passed_with_conditions` to `passed_with_notes` where appropriate.
- Immediate cleanup finished with a green proof; later tests-only Phase 6 tightening raised the current proof to `Ran 92 tests / OK`.

Deferred cleanup, still not required before moving on:

- decide whether shared test helper adoption should expand beyond authorized-table assertions
- shared test payloads were moved out of test modules after cross-boundary proof coupling grew
- consider package export cleanup only when there is a real consumer need
- revisit audit-first orchestration helper extraction only if another persistence boundary adds enough repetition to justify it

Phase 6A did not authorize new persistence tables, new domain records, UI, agents, integrations, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Phase 7 - SearchClarity Compatibility Preparation

Status: blocked.

Phase 7 begins only after:

1. Phase 6 is complete enough to enforce boundaries.
2. SearchClarity has enough manual-business evidence to model safely.
3. SearchClarity-specific details can be classified without becoming core doctrine.
4. Neon Ronin can inspect SearchClarity without becoming SearchClarity.

Expected future work:

- read SearchClarity docs as business/workspace input
- classify SearchClarity as a workspace type
- extract reusable Neon Ronin capabilities
- identify adapter/core/schema gaps
- draft a workspace config only when readiness gates are satisfied
- identify hard-no automation rules and privacy boundaries

No SearchClarity onboarding is currently authorized.
