# Internal Research Manual Test Plan 001

## Status

```text
planned
```

This is the first manual-test plan for Neon Ronin Internal Research.

It is a planning and validation document only.

It does not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.

## Test Metadata

```yaml
manual_test_id: mt_internal_research_001
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_plan_time: onboarding
source_intake: docs/workspaces/internal-research/intake-classification.md
source_workspace_config: docs/workspaces/internal-research/workspace-config.draft.md
test_status: planned
created_at: 2026-05-25T00:00:00Z
updated_at: 2026-05-25T00:00:00Z
schema_version: manual_test_template_v1
record_revision: 1
```

## Manual Test Goal

Validate artifact, review, audit, human-decision, and sanitized-signal flow using internal research artifacts without customer data, external writes, agents, scheduled jobs, watch mode, UI work, database implementation, or automation.

## Scope

This manual test covers:

- workspace config assumptions
- artifact creation as a referenced internal research artifact
- review queue item creation as a planned/manual record
- human decision capture as a planned/manual record
- audit record expectations as planned trace entries
- signal candidate drafting from generalized internal research findings
- sanitization review decision posture
- failure/block behavior for forbidden actions

## Non-Goals

This manual test does not cover:

- application code
- database tables
- API routes
- UI screens
- real agent runs
- automated workflows
- scheduled jobs
- watch mode
- external integrations
- live Observatory ingestion
- SearchClarity onboarding
- customer-facing delivery

## Preconditions

Required before test starts:

- [x] workspace type is known: `internal_research`
- [x] workspace config draft exists
- [x] workspace status is `onboarding`
- [x] workflow being tested is defined in this document
- [x] expected artifacts are identified
- [x] expected review gates are identified
- [x] expected audit events are identified
- [x] hard-no rules are preserved
- [x] no agents are assigned
- [x] no external integrations are configured
- [x] no customer data is required
- [x] no database implementation is required

## Test Scenario

A human operator performs a small internal research workflow:

```text
Research question -> internal research artifact -> review item -> human decision -> audit expectation -> signal candidate -> sanitization review -> planned outcome
```

Example research question:

```text
What repeatable criteria should Neon Ronin use to decide whether a future business idea is ready for workspace intake?
```

The output should be an internal research artifact and one generalized signal candidate.

## Planned Records

These are planned/manual records, not database records.

| Planned Record | Purpose | Storage Target |
|---|---|---|
| `art_internal_research_workspace_readiness_001` | Internal research artifact summarizing readiness criteria | future manual-test evidence doc |
| `review_internal_research_artifact_001` | Review item for artifact quality and boundary safety | future manual-test evidence doc |
| `decision_internal_research_artifact_001` | Human decision on artifact approval/revision | future manual-test evidence doc |
| `audit_internal_research_manual_test_001` | Planned audit trace for the manual flow | future manual-test evidence doc |
| `signal_candidate_workspace_readiness_001` | Generalized signal candidate from the internal research finding | future manual-test evidence doc |
| `review_signal_candidate_workspace_readiness_001` | Sanitization review item | future manual-test evidence doc |

## Workflow Steps

| Step | Actor | Action | Input Ref | Output Ref | Expected Gate/Audit | Result |
|---|---|---|---|---|---|---|
| 1 | human | Confirm workspace config boundaries | `workspace-config.draft.md` | boundary checklist note | audit expectation: workspace config reviewed | planned |
| 2 | human | Draft internal research artifact from research question | manual research question | `art_internal_research_workspace_readiness_001` | audit expectation: artifact drafted | planned |
| 3 | human | Check artifact for business-neutral language and no private/customer data | artifact draft | review item `review_internal_research_artifact_001` | `quality_gate`, `data_privacy_gate`, `strategy_review_gate` | planned |
| 4 | human | Record human decision for artifact | review item | decision `decision_internal_research_artifact_001` | audit expectation: human decision recorded | planned |
| 5 | human | Extract one generalized signal candidate from approved artifact | artifact and decision | `signal_candidate_workspace_readiness_001` | audit expectation: signal candidate drafted | planned |
| 6 | human | Review signal candidate for sanitization | signal candidate | `review_signal_candidate_workspace_readiness_001` | `signal_sanitization_gate` | planned |
| 7 | human | Record sanitization decision | sanitization review | planned sanitized-signal outcome or rejection/park decision | audit expectation: signal submission reviewed | planned |
| 8 | human | Check forbidden action probes | hard-no rules | blocked-action notes | audit expectation: forbidden action blocked if attempted | planned |
| 9 | human | Summarize test evidence and unresolved gaps | all planned records | manual-test evidence summary | audit expectation: test summarized | planned |

## Expected Artifact Shape

The internal research artifact should include:

- artifact id
- workspace id
- title
- research question
- short findings summary
- recommendation summary
- source references
- review gate references
- sensitivity rating
- delivery/public status
- schema version and record revision if represented as a structured record

Artifact content should remain workspace-owned.

The artifact must not contain:

- customer data
- external provider payloads
- credentials
- SearchClarity-specific core doctrine
- unbounded metadata/custom data

## Expected Review Behavior

The artifact review should check:

- business-neutral language
- source/provenance clarity
- no customer/private data
- no core doctrine mutation
- no hidden implementation decision
- no automation authorization
- reusable lesson is generalized enough for Internal Research

Possible decisions:

- approve
- approve_with_changes
- request_revision
- reject
- park

A human decision is required before the artifact can be treated as test evidence.

## Expected Audit Behavior

The manual test should identify audit expectations for:

- workspace config reviewed
- artifact drafted
- artifact review item created
- human decision recorded
- signal candidate drafted
- sanitization review item created
- sanitization decision recorded
- forbidden action blocked if attempted
- manual test summarized

This plan does not create real audit records in a database.

It defines what audit records future implementation must preserve.

## Expected Signal Candidate Behavior

The signal candidate should be generalized from internal research and should not include private workspace details beyond allowed provenance references.

Example candidate:

```text
Future workspace promotion should require clear purpose, known inputs/outputs, explicit review gates, hard-no rules, and a manual-test goal before runtime permissions are considered.
```

Expected signal type:

```text
workspace_readiness_signal
```

The candidate may only become Observatory-eligible after human sanitization review.

## Sanitization Review Expectations

The sanitization review should verify:

- no private/customer data
- no raw artifact text copied into shared intelligence
- no specific future business details that create hidden doctrine
- generalized value for future workspace intake
- provenance retained through safe references
- human decision recorded

Expected default outcome for this first test:

```text
approve_with_changes or park
```

Reason: the first test should favor caution until evidence format and review flow are proven.

## Failure And Block Probes

The manual test should include planned checks that the following remain blocked:

| Probe | Expected Result |
|---|---|
| Try to assign an agent | blocked; `allowed_agents: []` |
| Try to enable scheduled mode | blocked; `scheduled_allowed: false` |
| Try to enable watch mode | blocked; `watch_mode_allowed: false` |
| Try to add provider credential | blocked; `external_credentials_allowed: false` and `no_provider_credentials` |
| Try to submit raw artifact text to Observatory | blocked; sanitization required |
| Try to mark signal as approved without human decision | blocked; human review required |
| Try to treat this plan as DB implementation permission | blocked; non-goal |

## Evidence To Capture Later

When this manual test is executed, capture:

- completed workflow table
- final artifact text or artifact reference
- review decision note
- human decision note
- audit expectation checklist result
- signal candidate text
- sanitization decision note
- blocked-action probe notes
- unresolved questions
- recommendation for next manual test or config revision

## Exit Criteria

This manual test may be considered passed only when:

- [ ] the workflow can be completed manually from artifact draft to sanitization decision
- [ ] review gates are used before evidence is accepted
- [ ] human decisions are explicit
- [ ] audit expectations are clear for every meaningful step
- [ ] signal candidate does not enter Observatory without sanitization review
- [ ] hard-no probes remain blocked
- [ ] no customer data, credentials, provider payloads, or implementation details are introduced
- [ ] unresolved gaps are documented

## Next Allowed Step After This Plan

Execute this manual test as a documented manual evidence pass.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, or automation.