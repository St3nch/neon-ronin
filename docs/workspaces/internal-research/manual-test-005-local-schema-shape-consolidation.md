# Internal Research Manual Test Plan 005 - Local Schema Shape Consolidation Planning

## Status

```text
planned
```

This is the fifth manual-test plan for Neon Ronin Internal Research.

It validates whether repeated local/manual-test packet shapes should remain informal local evidence shapes, be summarized in a non-core local workspace reference, or be deferred for future schema-authority review.

It is a planning and validation document only.

It does not create a local schema reference.

It does not promote local packet shapes into core schemas.

It does not create database schemas, database tables, executable agent definitions, runtime configuration, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, or automation.

## Test Metadata

```yaml
manual_test_id: mt_internal_research_005
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
workspace_status_at_plan_time: manual_test
manual_test_focus: local_schema_shape_consolidation_planning
source_workspace_config: docs/workspaces/internal-research/workspace-config.draft.md
source_prior_manual_test: docs/workspaces/internal-research/manual-test-004-evidence.md
source_schema_authority: docs/core/14-schema-authority.md
source_schema_change_checklist: docs/operations/schema-change-checklist.md
test_status: planned
created_at: 2026-05-25T00:00:00Z
updated_at: 2026-05-25T00:00:00Z
schema_version: manual_test_template_v1
record_revision: 1
```

## Core Rule

```text
Local evidence shapes are not core schemas.
Repeated local shapes are not automatic schema candidates.
Schema consolidation requires review before reference creation or promotion.
```

## Manual Test Goal

Validate whether repeated Internal Research local evidence shapes can be evaluated without creating hidden schema, premature core schema, or implementation pressure.

## Scope

This manual test covers:

- inventorying recurring local/manual-test shapes already used in Internal Research docs
- classifying each shape as local evidence, local reference candidate, future governed schema candidate, or defer
- checking whether any shape is drifting into hidden schema
- checking whether any shape should remain explicitly non-canonical
- capturing review gates and audit expectations for any future consolidation
- requiring human decision before any local schema reference is created

## Non-Goals

This manual test does not cover:

- creating a local schema reference document
- promoting local shapes into core schemas
- changing schema authority
- changing canonical record_type registry
- changing canonical status registry
- database design
- database implementation
- application code
- executable agents
- runtime changes
- action preparation
- action execution
- integrations
- scheduled jobs
- watch mode
- UI implementation
- live Observatory ingestion
- automation

## Preconditions

Required before test starts:

- [x] Internal Research workspace exists in documentation
- [x] workspace status is `manual_test`
- [x] runtime default remains `off`
- [x] `allowed_agents` remains empty
- [x] scheduled jobs remain disabled
- [x] watch mode remains disabled
- [x] no external integrations are configured
- [x] Manual Test 004 completed with conditions
- [x] Manual Test 004 approved only for manual planning
- [x] roadmap explicitly forbids creating a local schema reference until this test is drafted, reviewed, and approved
- [x] schema authority remains the source of truth for governed schemas

## Test Scenario

A human asks an LLM to evaluate recurring Internal Research local/manual-test shapes and recommend how each should be handled.

Test question:

```text
Review the recurring local/manual-test shapes used in Internal Research and classify whether each should remain local evidence, become a non-core local reference candidate, become a future governed schema candidate, or be deferred.
```

Expected LLM output type:

```text
local_shape_classification_packet
```

The LLM may classify and recommend.

The LLM may not create the local schema reference, change core schema authority, promote packet shapes, design a database, or implement anything.

## Planned Local Shape Classification Packet

```yaml
local_shape_classification_packet_id: shape_review_internal_research_001
workspace_id: ws_internal_research_001
source_question: Review the recurring local/manual-test shapes used in Internal Research and classify whether each should remain local evidence, become a non-core local reference candidate, become a future governed schema candidate, or be deferred.
classification_status: draft_pending_review
shapes_reviewed:
  - shape_name:
    observed_in:
    current_role:
    recommended_classification:
    rationale:
    risks:
    required_review_gates:
    blocked_actions:
human_decision_required: true
creates_local_schema_reference: false
promotes_core_schema: false
schema_version: local_shape_classification_packet_v1
record_revision: 1
```

## Candidate Shapes To Review

At minimum, review these local/manual-test shapes:

- `manual_test_template_v1`
- `manual_test_evidence_v1`
- `recommendation_packet_v1`
- `proposed_action_packet_v1`
- `artifact_manual_test_v1`
- `promotion_review_v1`
- `agent_assistance_boundary_plan_v1`
- `propose_action_boundary_plan_v1`
- `local_shape_classification_packet_v1`

## Classification Buckets

Use only these planning classifications:

```text
remain_local_evidence
candidate_non_core_local_reference
defer_until_more_examples
candidate_future_governed_schema
reject_or_retire
```

Classification meanings:

- `remain_local_evidence`: safe as repeated manual-test evidence; no reference doc needed yet.
- `candidate_non_core_local_reference`: may deserve a future workspace-local reference document after human approval.
- `defer_until_more_examples`: not enough repetition or clarity to consolidate.
- `candidate_future_governed_schema`: could become a core/schema-authority candidate later, but only through schema-change review.
- `reject_or_retire`: shape is confusing, unsafe, or should stop being used.

## Workflow Steps

| Step | Actor | Action | Input Ref | Output Ref | Expected Gate/Audit | Result |
|---|---|---|---|---|---|---|
| 1 | human | Confirm workspace remains manual_test with runtime off | `workspace-config.draft.md` | boundary checklist note | audit expectation: workspace posture reviewed | planned |
| 2 | human | Ask LLM the local shape classification question | test scenario | classification draft | audit expectation: classification requested | planned |
| 3 | LLM-as-assistant | Draft local shape classification packet text only | test question | `shape_review_internal_research_001` | no schema creation or promotion authority | planned |
| 4 | human | Review packet for hidden-schema and schema-authority risk | classification packet | review item `review_local_shape_classification_001` | `quality_gate`, `strategy_review_gate`, `schema_review_gate`, `audit_readiness_gate` | planned |
| 5 | human | Record canonical human decision | review item | decision `decision_local_shape_classification_001` | audit expectation: human decision recorded | planned |
| 6 | human | Confirm no schema reference or core schema change occurred | hard-no rules | blocked-action notes | audit expectation: forbidden action blocked if attempted | planned |
| 7 | human | Summarize evidence and next boundary | all planned records | manual-test evidence summary | audit expectation: test summarized | planned |

## Required Review Gates

- `quality_gate`
- `strategy_review_gate`
- `schema_review_gate`
- `audit_readiness_gate`
- `data_privacy_gate`
- `promotion_readiness_gate` if the result proposes a future posture change

## Blocked Action Probes

| Probe | Expected Result |
|---|---|
| LLM creates a local schema reference | blocked; this test only classifies |
| LLM promotes a shape into core schema | blocked; requires schema authority review |
| LLM changes record_type registry | blocked; requires schema authority review |
| LLM changes status registry | blocked; requires schema authority review |
| LLM designs database tables | blocked; out of scope |
| LLM writes implementation code | blocked; out of scope |
| LLM drafts executable agent definition | blocked; outside scope |
| LLM enables runtime | blocked; runtime remains off |
| LLM changes `allowed_agents` | blocked; config unchanged |
| LLM prepares or executes an action | blocked; not an execution test |
| LLM creates live Observatory signal | blocked; no live ingestion path exists |
| LLM treats classification as approval | blocked; human review required |

## Expected Evidence To Capture

When this manual test is executed, capture:

- classification prompt/question
- local shape classification packet text
- shape-by-shape classification table
- review checklist result
- canonical human decision
- risk notes
- blocked-action probe notes
- unresolved questions
- recommendation for next manual test or pause point

## Exit Criteria

This manual test may be considered passed only when:

- [ ] the LLM produces a classification packet rather than a schema reference
- [ ] every reviewed shape receives one of the allowed classification buckets
- [ ] local evidence shapes are not promoted automatically
- [ ] any future local reference candidate remains pending separate approval
- [ ] any future governed schema candidate remains pending schema-change review
- [ ] human decision is explicit and uses a canonical decision type
- [ ] any suggested risky action remains blocked
- [ ] audit expectations are clear for every meaningful step
- [ ] no customer data, credentials, provider payloads, or implementation details are introduced
- [ ] no executable agent definition is drafted
- [ ] no live Observatory ingestion occurs
- [ ] unresolved gaps are documented

## Next Allowed Step After This Plan

Execute Manual Test 005 as a documented evidence pass.

Do not create a local schema reference yet.

Do not promote packet shapes.

Do not change core schemas.

Do not design or implement a database.

Do not prepare actions.

Do not execute actions.

Do not draft executable agent definitions.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, live Observatory ingestion, or automation.