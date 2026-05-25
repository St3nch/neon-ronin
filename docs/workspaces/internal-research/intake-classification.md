# Internal Research Intake Classification

## Status

```text
Phase 6 preparation
```

This document is the lightweight business intake/classification record for Neon Ronin's first planned workspace: Internal Research.

It is not a workspace config.

It is not application code.

It does not authorize agents, scheduled jobs, external integrations, watch mode, automation, database implementation, or UI work.

## Intake Record

```yaml
business_intake_id: intake_internal_research_001
idea_name: Neon Ronin Internal Research
intake_status: approved_for_onboarding
proposed_workspace_type: internal_research
summary: Internal workspace for evaluating business ideas, platform decisions, opportunity signals, and future workspace onboarding plans.
purpose: Validate Neon Ronin's workspace, artifact, review, audit, and sanitized-signal flow using low-risk internal research before onboarding external/customer-facing businesses.
target_customer_or_user: Neon Ronin operator and future workspace planning process.
primary_offer_or_output: Internal research notes, decision packets, recommendation packets, artifact drafts, review items, and sanitized opportunity signals.
channels:
  - internal_docs
  - manual_research
expected_inputs:
  - operator questions
  - business idea notes
  - platform planning notes
  - public research summaries
  - prior Neon Ronin docs
expected_outputs:
  - research artifacts
  - recommendation packets
  - review queue items
  - audit-friendly decision notes
  - signal candidates
  - sanitized signals for Observatory review
private_data_expected: false
external_systems_expected:
  - none by default
initial_risk_notes: Internal-only planning workspace. No customer data, no credentialed provider access, no external writes, no automation, no scheduled jobs, and no watch mode by default.
classification_verdict: GREEN_LIGHT
created_at: 2026-05-25T00:00:00Z
updated_at: 2026-05-25T00:00:00Z
source_actor_type: human
source_actor_id: human_operator
source_references:
  - record_type: manual_note
    record_id: docs_ROADMAP_phase_6
    relationship: roadmap_context
proposed_adapter: internal-research-workspace
known_workflows:
  - research intake
  - artifact drafting
  - recommendation drafting
  - review queue validation
  - decision capture
  - signal candidate drafting
  - sanitization review
known_review_gates:
  - artifact_quality_gate
  - data_boundary_gate
  - signal_sanitization_gate
  - promotion_readiness_gate
hard_no_rules:
  - no_external_writes
  - no_customer_data_by_default
  - no_autonomous_actions
  - no_scheduled_jobs
  - no_watch_mode
  - no_provider_credentials
  - no_workspace_config_before_intake
observatory_fit:
  may_query_observatory: true
  may_generate_signals: true
  likely_signal_types:
    - opportunity_signal
    - platform_decision_signal
    - workspace_readiness_signal
    - reusable_process_signal
  private_data_risk: low
  sanitization_notes: Only generalized internal research findings may become signal candidates. Any specific future business details remain workspace-owned or reference-example material until generalized.
reusable_capabilities:
  - artifact tracking
  - review queue validation
  - audit trail validation
  - human decision capture
  - signal candidate drafting
  - signal sanitization
workspace_specific_items:
  - internal research notes
  - workspace planning notes
  - opportunity evaluation notes
  - operator decision context
deferred_domains_touched:
  - none by default
manual_test_goal: Validate artifact, review, audit, human-decision, and sanitized-signal flow without customer data, external writes, agents, scheduled jobs, watch mode, or automation.
promotion_recommendation: draft_workspace_config_next
tags:
  - internal-research
  - phase-6-prep
schema_version: schema_v1
record_revision: 1
```

## Classification Rationale

Internal Research is appropriate as Workspace 1 because it exercises the platform mechanics with the lowest practical external risk.

It can validate:

- workspace-specific artifact handling
- review queue flow
- audit trail expectations
- human decision posture
- signal candidate drafting
- sanitization boundaries
- Observatory interaction rules

It avoids, by default:

- customer data
- paid delivery pressure
- external writes
- provider credentials
- marketplace automation
- scheduled jobs
- watch mode
- business-specific core leakage

## Onboarding Boundary

This intake permits the next planning step:

```text
Draft Internal Research workspace config.
```

It does not permit runtime execution, agents, automation, database implementation, UI work, external integrations, or live Observatory ingestion.

## Validation Questions

- Is the idea clearly described? Yes.
- Is proposed workspace type identified? Yes: `internal_research`.
- Are expected inputs and outputs clear? Yes.
- Is private data risk identified? Yes: no customer data by default, low risk.
- Are external systems identified without becoming core fields? Yes: none by default.
- Does this intake create a workspace config? No.
- Does this intake authorize automation? No.
- Does this intake preserve business-neutral Neon Ronin core? Yes.

## Next Allowed Step

Draft the Internal Research workspace config as a separate reviewed document.

Do not start agents, integrations, scheduled jobs, watch mode, UI work, or database implementation.
