# Internal Research Workspace Config Draft

## Status

```text
Draft workspace config
```

This document drafts the workspace config for Neon Ronin Internal Research after the lightweight intake/classification record.

It is a manual_test posture draft with runtime default still off.

It is not application code.

It does not authorize agents, scheduled jobs, watch mode, external integrations, database implementation, UI work, or automation.

## Source Intake

```text
docs/workspaces/internal-research/intake-classification.md
```

## Workspace Config Record

```yaml
workspace_id: ws_internal_research_001
workspace_name: Neon Ronin Internal Research
workspace_slug: internal-research
workspace_type: internal_research
status: manual_test
purpose: Research and evaluate business ideas, platform decisions, opportunity signals, and workspace onboarding plans before customer-facing or business-specific workspaces are promoted.
channels:
  - internal_research
adapter: internal-research-workspace
allowed_agents: []
review_gates:
  - quality_gate
  - data_privacy_gate
  - strategy_review_gate
  - signal_sanitization_gate
  - promotion_readiness_gate
observatory:
  can_query: true
  can_submit_sanitized_signals: true
  allowed_query_types:
    - prior_signal_check
    - data_quality_check
    - opportunity_score
    - trend_profile
  signal_submission_requires_human_review: true
storage_rules:
  workspace_private_data: true
  generalized_signals_allowed_after_sanitization: true
  raw_customer_data_allowed: false
  external_credentials_allowed: false
  artifact_content_scope: workspace_private
runtime:
  default_mode: off
  allowed_modes:
    - off
    - on_demand
  scheduled_allowed: false
  watch_mode_allowed: false
  emergency_stop_supported: true
hard_no_rules:
  - no_autonomous_publishing
  - no_autonomous_spending
  - no_autonomous_customer_messaging
  - no_autonomous_customer_delivery
  - no_autonomous_credential_changes
  - no_autonomous_destructive_actions
  - no_agent_self_approval
  - no_external_writes
  - no_customer_data_by_default
  - no_scheduled_jobs
  - no_watch_mode
  - no_provider_credentials
  - no_database_implementation_from_workspace_config
audit_requirements:
  - workspace_config_created
  - workspace_config_updated
  - workspace_status_changed
  - workspace_runtime_mode_changed
  - observatory_permission_changed
  - review_gate_list_changed
  - hard_no_rule_changed
  - artifact_reviewed
  - human_decision_recorded
  - signal_submission_reviewed
owner_actor_id: human_operator
data_classification: internal_low_risk
manual_test_goal: Validate artifact, review, audit, human-decision, and sanitized-signal flow using internal research artifacts without customer data, external writes, agents, scheduled jobs, watch mode, or automation.
promotion_notes: Promoted to manual_test posture in documentation by promotion review 001. Runtime default remains off; allowed_agents remains empty; scheduled jobs and watch mode remain disabled.
external_references: []
tags:
  - internal-research
  - workspace-1
  - phase-6
  - config-draft
created_at: 2026-05-25T00:00:00Z
updated_at: 2026-05-25T00:00:00Z
schema_version: schema_v1
record_revision: 2
```

## Boundary Notes

This draft establishes workspace boundaries only.

It does not start the workspace.

It does not grant agent execution rights.

It does not create integrations.

It does not create database tables, API routes, UI screens, scheduled jobs, watch mode, or automation.

## Validation Questions

- Is the workspace type valid? Yes: `internal_research`.
- Is the lifecycle status valid? Yes: `manual_test`.
  - Note: the prior revision used `onboarding`; the status change is recorded in `promotion-review-001-onboarding-to-manual-test.md`.
- Are runtime modes allowed for the lifecycle status? Yes: default is `off`, with only `off` and `on_demand` listed for future manual use.
- Are Observatory permissions explicit? Yes: query and sanitized signal submission are explicit, and signal submission requires human review.
- Are review gates defined? Yes.
- Are hard-no rules at least as strict as global rules? Yes.
- Does the config avoid business-specific private data? Yes.
- Does it avoid provider-specific fields? Yes.
- Does it preserve enough provenance and audit posture? Yes: source intake is named and audit requirements are explicit.
- Could another workspace type use the same core schema? Yes.

## Next Allowed Step

Continue manual-test work through documented manual evidence passes.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, database implementation, live Observatory ingestion, or automation.
