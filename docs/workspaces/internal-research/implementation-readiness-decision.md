# Internal Research Implementation Readiness Decision

## Status

```text
approved
```

This document records the implementation-readiness decision for Neon Ronin after Internal Research Manual Tests 001-005 and the Prompt B schema/status audit cleanup.

It decides whether Neon Ronin may move from documentation-only manual evidence toward the smallest executable platform slice.

This decision does not implement code.

This decision does not create a database.

This decision does not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.

## Decision Metadata

```yaml
implementation_readiness_decision_id: decision_internal_research_implementation_readiness_001
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_decision_time: manual_test
decision_type: approve_with_changes
decision_status: recorded
created_at: 2026-05-26T00:00:00Z
updated_at: 2026-05-26T00:00:00Z
schema_version: implementation_readiness_decision_v1
record_revision: 1
```

## Decision

```text
Approve with changes: Neon Ronin may prepare for the smallest executable persistence proof, but implementation remains gated behind a separate implementation plan and explicit approval.
```

## Decision Summary

Manual Tests 001-005 have provided enough documentation-only evidence to stop adding meta-governance by default.

Neon Ronin may move from repeated manual evidence generation into implementation-readiness planning for a minimal executable platform slice.

The next work should define the smallest executable proof that validates core doctrine without overbuilding.

This decision does not approve implementation itself.

## Evidence Reviewed

| Evidence | Result | Notes |
|---|---|---|
| Phase 5C Core Example Separation | passed | SearchClarity examples moved out of core and core docs remain business-neutral |
| Phase 5D DB Reliability And Schema Clarification | passed | schema authority, record types, statuses, transactions, audit-first rule, and resolver hammer doctrine exist |
| Prompt B schema/status audit cleanup | passed | promotion-review drift and manual-test status vocabulary were fixed |
| Manual Test 001 | passed_with_notes | artifact/review/audit/human-decision/signal flow validated manually |
| Promotion Review 001 | approved | Internal Research moved to documentation-only `manual_test` posture |
| Manual Test 002 | passed_with_notes | LLM recommendation assistance stayed reviewable and non-executing |
| Manual Test 003 | passed_with_notes | LLM draft assistance stayed artifact-only and human-reviewed |
| Manual Test 004 | passed_with_notes | LLM propose-action assistance stayed proposal-only with no preparation/execution |
| Manual Test 005 | passed_with_notes | local/manual-test shape drift was classified without creating a local schema reference |
| Roadmap implementation-readiness checkpoint | present | roadmap now says no MT006 by default |

## Checkpoint Answers

### Are Prompt B Audit Findings Resolved?

```text
yes_for_P1_cleanup
```

Prompt B P1 findings have been fixed:

- promotion-review canonical human-decision drift repaired
- manual-test evidence statuses normalized to `passed_with_notes`
- timestamp posture added to schema authority
- resolver hammer checks strengthened
- reusable gate vocabulary updated
- workspace-local gate extensions documented for manual-test evidence

Remaining lower-priority items are not blockers for implementation-readiness planning.

### Are Manual Tests 001-005 Enough Evidence?

```text
yes_for_readiness_planning
```

Manual Tests 001-005 are sufficient to stop adding meta-governance by default.

They validate:

- manual artifact review flow
- audit expectation capture
- human decision capture
- signal candidate and sanitization posture
- LLM recommendation assistance
- LLM draft assistance
- LLM proposed-action assistance
- local shape drift detection

Do not create Manual Test 006 unless it answers a concrete implementation-readiness question.

### Are Adapter Or Workspace-Extension Docs Blockers Right Now?

```text
not_blockers_for_minimal_internal_persistence_proof
```

Adapter and workspace-extension docs are important before customer-facing workspace onboarding.

They are not blockers for a minimal Internal Research persistence proof limited to platform records.

They become blockers before:

- customer-facing workspace onboarding
- service-business order records
- customer/deliverable consent records
- adapter-level workspace records
- SearchClarity compatibility onboarding

### What Is The Smallest Executable Slice?

```text
minimal_internal_persistence_proof
```

Allowed scope for the first implementation plan, if separately approved:

- `workspace_configs`
- `audit_records`
- audit-first write path
- one transaction boundary
- one hammer probe

Preferred first transaction boundary:

```text
workspace_config_create
```

Preferred first hammer proof:

```text
attempt to create a workspace config without an audit record and verify the state change is blocked or rolled back
```

## Approved Conditions

This decision approves readiness planning only under these conditions:

1. The next document must be a minimal implementation plan, not code.
2. The implementation plan must name the exact first executable slice.
3. The implementation plan must name the authoritative docs for the slice.
4. The implementation plan must name the first transaction boundary.
5. The implementation plan must name the first hammer proof.
6. The implementation plan must explicitly keep agents, UI, integrations, scheduled jobs, watch mode, live Observatory ingestion, automation, and customer-facing workspace onboarding out of scope.
7. The implementation plan must not create a local schema reference from Manual Test 005 evidence alone.
8. The implementation plan must not promote local packet shapes into core schemas.
9. Actual code, database migration, or tool implementation requires a separate approval after the implementation plan is reviewed.

## Still Forbidden

This decision does not authorize:

- application code
- database implementation
- database migrations
- executable agents
- agent definitions
- agent runs
- integrations
- UI work
- scheduled jobs
- watch mode
- live Observatory ingestion
- automation
- customer-facing workspace onboarding
- SearchClarity onboarding
- local schema reference creation
- core schema promotion from local packet shapes
- workspace adapter implementation
- service-business order records
- consent record implementation

## Future Non-Blocking Backlog

The following are important, but they are not blockers for a minimal Internal Research persistence proof:

- expand service-business adapter contract before customer-facing workspace onboarding
- define adapter-level order lifecycle before any service-business workspace evidence creates order records
- define consent-record planning before public samples, testimonials, or case studies need tracked consent
- create workspace-local schema extension planning before many workspace-level extensions accumulate
- update `docs/workspaces/README.md` with second workspace slot conventions before a second workspace folder is created

## Human Decision Record

```yaml
human_decision_id: decision_internal_research_implementation_readiness_001
decision_type: approve_with_changes
decision_status: recorded
actor_type: human
actor_id: human_operator
decision_summary: Neon Ronin may prepare a minimal implementation plan for the first executable persistence proof, but implementation itself remains blocked until separately approved.
conditions:
  - next step is a minimal implementation plan only
  - first executable slice is limited to workspace_configs and audit_records unless separately approved
  - first transaction boundary should be workspace_config_create unless the implementation plan justifies another boundary
  - first hammer proof should verify audit-first write blocking or rollback
  - agents remain blocked
  - integrations remain blocked
  - UI remains blocked
  - scheduled jobs remain blocked
  - watch mode remains blocked
  - live Observatory ingestion remains blocked
  - customer-facing workspace onboarding remains blocked
  - SearchClarity onboarding remains blocked
  - local schema reference creation remains blocked
  - core schema promotion from local packet shapes remains blocked
source_references:
  - record_type: manual_note
    record_id: mt_internal_research_001_evidence
    relationship: evidence
  - record_type: manual_note
    record_id: mt_internal_research_002_evidence
    relationship: evidence
  - record_type: manual_note
    record_id: mt_internal_research_003_evidence
    relationship: evidence
  - record_type: manual_note
    record_id: mt_internal_research_004_evidence
    relationship: evidence
  - record_type: manual_note
    record_id: mt_internal_research_005_evidence
    relationship: evidence
  - record_type: manual_note
    record_id: roadmap_implementation_readiness_checkpoint
    relationship: roadmap_authority
schema_version: schema_v1
record_revision: 1
```

## Next Allowed Step

Create a minimal implementation plan for the first executable persistence proof.

The plan may name:

- proposed storage substrate candidates
- proposed first records
- authoritative docs
- first transaction boundary
- first hammer proof
- explicit non-goals
- approval requirements before implementation

The plan must not implement anything.

Do not write code.

Do not create database migrations.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.
