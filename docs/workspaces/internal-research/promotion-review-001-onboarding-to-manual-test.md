# Internal Research Promotion Review 001

## Status

```text
approved
```

This document records the documentation-only promotion review for Neon Ronin Internal Research from `onboarding` to `manual_test` posture.

It does not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.

## Promotion Header

```yaml
promotion_review_id: promo_internal_research_001
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_type: internal_research
current_status: onboarding
proposed_status: manual_test
promotion_status: approved
review_date: 2026-05-25T00:00:00Z
source_intake: docs/workspaces/internal-research/intake-classification.md
source_workspace_config: docs/workspaces/internal-research/workspace-config.draft.md
source_manual_test_plan: docs/workspaces/internal-research/manual-test-001-artifact-review-audit-signal-flow.md
source_manual_test_evidence: docs/workspaces/internal-research/manual-test-001-evidence.md
schema_version: promotion_review_v1
record_revision: 1
```

## Decision Summary

Internal Research may move from `onboarding` to `manual_test` posture in documentation.

The move is approved with conditions because Manual Test 001 passed with conditions and the remaining boundaries are explicit.

This does not make the workspace active.

This does not enable runtime execution.

This does not assign agents.

This does not authorize automation.

## Evidence Reviewed

| Evidence | Result |
|---|---|
| Lightweight intake/classification exists | passed |
| Workspace config draft exists | passed |
| Manual-test goal is clear | passed |
| Manual-test plan exists | passed |
| Manual-test evidence exists | passed_with_notes |
| Artifact review decision recorded | approve_with_changes |
| Sanitization decision recorded | approve_with_changes |
| No customer data involved | passed |
| No external writes involved | passed |
| No agents assigned | passed |
| No scheduled jobs/watch mode | passed |
| No credentials/provider payloads | passed |
| Audit expectations documented | passed |
| Review gates identified and exercised manually | passed_with_notes |

## Promotion Checklist

| Requirement | Status | Evidence |
|---|---|---|
| Workspace id is known | passed | `ws_internal_research_001` |
| Workspace type is valid | passed | `internal_research` |
| Current status is known | passed | `onboarding` |
| Proposed status is valid | passed | `manual_test` |
| Transition is allowed | passed | `onboarding -> manual_test` is allowed by lifecycle doctrine |
| Draft workspace config exists | passed | `workspace-config.draft.md` |
| Review gates are defined | passed | quality, data privacy, strategy, signal sanitization, promotion readiness |
| Audit requirements are defined | passed | config/evidence docs list audit expectations |
| Manual-test goal is clear | passed | artifact/review/audit/human-decision/signal flow |
| Hard-no rules remain intact | passed | no agents, no schedules, no watch mode, no credentials, no external writes |
| Blockers are absent or documented | passed_with_notes | conditions listed below |

## Conditions

The `manual_test` posture is approved only under these conditions:

- runtime default remains `off`
- `allowed_agents` remains empty
- scheduled jobs remain disabled
- watch mode remains disabled
- external integrations remain absent
- no live Observatory ingestion occurs
- no customer data is introduced
- no provider credentials are introduced
- Manual Test 001 artifact remains manual-test evidence only unless separately promoted through schema/ADR/core-doc review
- signal candidate remains concise and provenance-linked if later used

## Human Decision Record

```yaml
human_decision_id: decision_internal_research_promotion_001
decision_type: promote
actor_type: human
actor_id: human_operator
decision_status: recorded
from_status: onboarding
to_status: manual_test
decision_summary: Internal Research may move to manual_test posture in documentation while runtime remains off and all automation/integration boundaries remain blocked.
conditions:
  - runtime default remains off
  - allowed_agents remains empty
  - scheduled jobs remain disabled
  - watch mode remains disabled
  - external integrations remain absent
  - live Observatory ingestion remains blocked
  - all work remains documentation-only manual testing
source_references:
  - record_type: manual_note
    record_id: mt_internal_research_001_evidence
    relationship: evidence
  - record_type: manual_note
    record_id: ws_internal_research_001_config_draft
    relationship: promotion_target
schema_version: schema_v1
record_revision: 1
```

## Audit Expectations

Future implementation should audit:

- promotion review started
- human decision recorded
- workspace status changed from `onboarding` to `manual_test`
- conditions attached to promotion
- runtime remained `off`
- agent list remained empty
- scheduled/watch modes remained disabled

This document does not create real audit records in a database.

## Resulting Workspace Posture

```text
status: manual_test
runtime.default_mode: off
allowed_agents: []
scheduled_allowed: false
watch_mode_allowed: false
external_references: []
```

## Next Allowed Step

Continue manual-test work by creating a second documented manual evidence pass or revising Manual Test 001 evidence if needed.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.
