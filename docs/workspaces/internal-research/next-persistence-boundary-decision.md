# Internal Research Next Persistence Boundary Decision

## Status

```text
decision_options_only
```

This document records options for the next possible persistence boundary after the first local SQLite audit-first proof.

It is not an implementation-start decision.

It does not authorize new code, new tables, new schemas, new domain records, UI, agents, integrations, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Current Proof Baseline

The first local SQLite audit-first proof is complete and pushed.

```yaml
latest_pushed_commit: f63e1d8
latest_pushed_commit_summary: Add first proof developer check
proof_scope:
  - workspace_configs
  - audit_records
  - workspace_config_create
  - audit-first transaction behavior
current_hammer_command: python tools/dev/check_first_proof.py
current_hammer_result: Ran 12 tests / OK
```

The implementation remains intentionally tiny:

- Python stdlib `sqlite3` only
- direct module/service call only
- `packages/neon-core` proof slice only
- no external dependencies
- no UI
- no local service
- no agents
- no integrations
- no scheduled jobs
- no watch mode
- no live Observatory ingestion
- no customer-facing workspace onboarding
- no SearchClarity onboarding
- no automation

Core invariant already proven:

```text
no audit record means no workspace config record
```

## Boundary Decision Rule

No new persistence boundary is authorized yet.

Before adding any selected next boundary, Neon Ronin must record a separate implementation-start decision that names:

- selected operation
- authorized tables
- authorized files or folders
- transaction boundary
- audit behavior
- system-owned fields
- validation rules
- hammer command and expected result
- explicit forbidden scope
- rollback/failure expectations

Until that implementation-start decision exists, this document is only planning context.

## Candidate Next Boundaries

### 1. `workspace_config_update`

Possible scope:

- update an existing workspace config through a governed direct module/service call
- increment `record_revision`
- preserve `created_at`
- update `updated_at`
- write a corresponding audit record in the same transaction
- reject caller-supplied system-owned fields
- keep first-proof runtime restrictions intact unless separately changed by decision

Why it is small:

- reuses the existing `workspace_configs` and `audit_records` tables
- tests `record_revision` behavior without adding a new domain record
- extends the current proof instead of widening the platform surface
- keeps audit-first behavior central

Main risks:

- accidentally turning config updates into lifecycle/runtime enablement
- allowing status changes without lifecycle authority
- treating config patch shape as a hidden schema
- weakening first-proof runtime and agent restrictions

Required guardrails if selected:

- no new tables
- no lifecycle status transition support unless explicitly authorized
- no agent enablement
- no scheduled/watch runtime enablement
- no external references
- no unbounded `metadata` or `custom_data`
- audit record must be written in the same transaction as the update

### 2. `review_queue_item_create`

Possible scope:

- create a review queue item record
- validate required review fields
- write audit-first creation behavior

Why it matters:

- review queue is central to human-in-loop runtime doctrine
- it moves Neon Ronin closer to meaningful gated workflow records

Why it is not the smallest next step:

- likely requires a new `review_queue_items` table
- introduces a new core domain record
- raises status transition and human-decision linkage questions
- should probably wait for a separate boundary decision with sharper schema authority review

### 3. `human_decision_record`

Possible scope:

- create append-friendly human decision records
- link decisions to review items, workspace changes, or signal sanitization
- preserve decision provenance and audit behavior

Why it matters:

- human decisions are canonical authority for meaningful gates
- prevents agents or derived outputs from becoming approval truth

Why it is not the smallest next step:

- likely requires a new `human_decisions` table
- raises append-only enforcement questions
- needs clear relationship to review queue items and audit records
- could become paperwork theater if added before a concrete gated operation needs it

### 4. `signal_candidate_create`

Possible scope:

- create workspace-scoped signal candidates before sanitization
- preserve provenance and sensitivity posture
- block live Observatory ingestion

Why it matters:

- signal flow is core to the Observatory boundary
- validates raw-to-candidate-to-sanitized discipline

Why it is not the smallest next step:

- likely requires new signal persistence
- risks confusing workspace-private signal candidates with Observatory-owned records
- must not enable live Observatory ingestion
- sanitization review and human-decision authority need sharper implementation sequencing

### 5. `artifact_metadata_create`

Possible scope:

- create metadata for workspace artifacts without storing full private artifact content
- link artifact metadata to review/audit expectations later

Why it matters:

- artifacts are a natural output of manual and assisted workflows
- metadata can support review without introducing content storage too early

Why it is not the smallest next step:

- likely requires a new artifact record/table
- risks sneaking artifact content storage into metadata
- review queue linkage is not implemented yet
- storage rules need a tighter executable boundary before content-adjacent persistence begins

## Recommendation

Recommended next persistence boundary:

```text
workspace_config_update
```

Reason:

`workspace_config_update` is the smallest useful next boundary because it can reuse the existing `workspace_configs` and `audit_records` tables while testing record revision behavior and audit-first update semantics.

It extends the current proof without adding a new domain record.

It also keeps Neon Ronin focused on platform governance rather than jumping into review queue, human decision, signal, or artifact persistence too early.

## Recommended Scope If Later Approved

If a separate implementation-start decision approves `workspace_config_update`, the implementation should stay limited to:

- existing `workspace_configs` table
- existing `audit_records` table
- one update operation
- one focused hammer path
- revision increment behavior
- audit-first transaction rollback on audit-write failure
- validation that blocks system-owned field forgery and forbidden fields

It should not include:

- new tables
- review queue persistence
- human-decision persistence
- signal persistence
- artifact persistence
- lifecycle transition engine
- runtime enablement
- agent enablement
- external references
- UI
- local service
- integrations
- scheduled jobs
- watch mode
- live Observatory ingestion
- customer-facing workspace onboarding
- SearchClarity onboarding
- automation

## Required Next Gate

Before implementation, create a separate implementation-start decision document for the selected boundary.

Suggested document if `workspace_config_update` is selected:

```text
docs/workspaces/internal-research/implementation-start-decision-persistence-002.md
```

That document should explicitly authorize the selected operation and repeat the forbidden scope.

This options document alone is not enough to begin implementation.
