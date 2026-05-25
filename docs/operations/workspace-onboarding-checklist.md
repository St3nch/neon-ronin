# Workspace Onboarding Checklist

## Purpose

This checklist defines the required operating steps before a business idea, project, or internal effort becomes a Neon Ronin workspace.

It exists to prevent workspace onboarding from becoming a shortcut around core boundaries, schema authority, review gates, privacy rules, or first-business containment.

## Core Rule

```text
No workspace enters Neon Ronin without classification, boundaries, review gates, and manual-test intent.
```

A workspace is not just a folder, idea, or business name.

A workspace is a governed operating area inside Neon Ronin.

## When To Use This Checklist

Use this checklist before:

- creating a workspace config
- converting business intake into onboarding
- creating workspace-owned folders or records
- assigning agents
- connecting integrations
- submitting signals to the Observatory
- running manual tests
- preparing SearchClarity compatibility work

## Required Inputs

Before onboarding, gather:

- business intake record or source docs
- workspace purpose
- proposed workspace type
- proposed adapter
- expected inputs
- expected outputs
- expected artifacts
- expected review gates
- expected private data
- external systems touched
- Observatory query/submission expectations
- hard-no automation rules
- manual-test goal

## Step 1 - Confirm Workspace Candidate

- [ ] Candidate has a clear name.
- [ ] Candidate has a clear purpose.
- [ ] Candidate has a human owner/operator.
- [ ] Candidate is not secretly trying to redefine Neon Ronin core.
- [ ] Candidate has enough source material to classify.
- [ ] Candidate has been recorded in the first-workspace decision log if strategically important.

Decision:

```text
Proceed | Needs More Info | Park | Reject
```

## Step 2 - Classify Workspace Type

Select one:

- [ ] `service`
- [ ] `marketplace_store`
- [ ] `digital_products`
- [ ] `content`
- [ ] `internal_research`
- [ ] `hybrid`
- [ ] `other`

Notes:

```text
Why this type?
```

If `hybrid` or `other`, explain why existing adapters do not fit cleanly.

## Step 3 - Classify Ownership Boundaries

Classify expected data:

| Data / Record | Classification | Notes |
|---|---|---|
| workspace config | core-owned | |
| customer/private data | workspace-owned | |
| artifacts | metadata core-tracked, content workspace-owned | |
| raw signals | workspace-owned | |
| sanitized signals | Observatory-owned after approval | |
| external provider records | integration-owned or referenced-only | |
| credentials | secret store later, reference only | |
| derived intelligence | derived / Observatory-owned | |

Required checks:

- [ ] Workspace-owned data is identified.
- [ ] Core-owned data is identified.
- [ ] Observatory-owned data is identified.
- [ ] Integration-owned data is identified.
- [ ] Referenced-only data is identified.
- [ ] Forbidden-in-core data is identified.

## Step 4 - Identify Forbidden-In-Core Details

List details that must not enter `docs/core/`:

- [ ] brand language
- [ ] pricing
- [ ] customer promises
- [ ] customer records
- [ ] report templates
- [ ] marketplace/provider payloads
- [ ] Fiverr/Etsy/Printify/provider-specific assumptions
- [ ] private strategy
- [ ] raw customer observations
- [ ] credentials/secrets

Workspace-specific forbidden-in-core notes:

```text
Add notes here.
```

## Step 5 - Identify Expected Artifacts

List expected artifacts:

- [ ] research packet
- [ ] recommendation packet
- [ ] draft report
- [ ] final report
- [ ] sample report
- [ ] report template
- [ ] QA checklist
- [ ] action plan
- [ ] keyword table
- [ ] spreadsheet deliverable
- [ ] PDF export
- [ ] markdown source
- [ ] delivery message
- [ ] signal support note
- [ ] other

For each artifact, identify:

- content owner
- storage reference expectation
- review requirement
- public-use/consent requirement
- lifecycle status

## Step 6 - Identify Expected Workflows

List workflows needed:

- [ ] business intake
- [ ] manual research
- [ ] report production
- [ ] artifact review
- [ ] customer delivery
- [ ] signal capture
- [ ] signal sanitization
- [ ] Observatory handoff
- [ ] workspace promotion
- [ ] QA review
- [ ] external action request
- [ ] internal strategy
- [ ] other

For each workflow, identify:

- trigger
- required inputs
- expected outputs
- required agents, if any
- review gates
- audit events
- failure behavior

## Step 7 - Identify Review Gates

Required review gate checks:

- [ ] quality gate
- [ ] publish gate
- [ ] paid action gate
- [ ] data privacy gate
- [ ] customer delivery gate
- [ ] rights and compliance gate
- [ ] signal sanitization gate
- [ ] IP/common-sense gate
- [ ] strategy review gate
- [ ] external write gate
- [ ] credential permission gate

Notes:

```text
Which gates are required and why?
```

No risky output may proceed without required gates.

## Step 8 - Identify Agent Eligibility

Before assigning agents:

- [ ] Workspace lifecycle allows agent assistance.
- [ ] Workspace config lists allowed agents.
- [ ] Agent definition allows this workspace type.
- [ ] Permission scope is defined or planned.
- [ ] Review gates are preserved.
- [ ] Agent cannot approve its own work.
- [ ] Agent cannot access other workspace private data.
- [ ] Agent cannot submit raw data to Observatory.
- [ ] Agent cannot perform external writes without human approval.

Initial agent posture should usually be:

```text
human-started on-demand assistance only
```

## Step 9 - Identify Observatory Fit

Observatory expectations:

- [ ] Workspace may query Observatory.
- [ ] Workspace may not query Observatory yet.
- [ ] Workspace may generate raw signals.
- [ ] Workspace may create signal candidates.
- [ ] Workspace may submit sanitized signals after human review.
- [ ] Workspace may not submit signals yet.

Required checks:

- [ ] Raw signals stay workspace-owned.
- [ ] Signal candidates require review.
- [ ] Sanitized signals require human approval before Observatory intake.
- [ ] Normal query surfaces do not reveal private source data.
- [ ] Score outputs are decision support only.

## Step 10 - Identify External Integration Touchpoints

List external systems touched:

```text
Provider/system:
Purpose:
Action classes:
Credential required? yes/no
Review gates required:
Deferred domain risk:
```

Required checks:

- [ ] No real secret values are stored in docs or configs.
- [ ] Credential references only.
- [ ] Provider capability is not treated as Neon Ronin permission.
- [ ] External write requires human decision.
- [ ] Destructive action requires human decision.
- [ ] Integration is not a deferred domain sneaking in early.

## Step 11 - Define Hard-No Rules

Global hard-no rules always apply:

- [ ] no autonomous publishing
- [ ] no autonomous spending
- [ ] no autonomous customer messaging
- [ ] no autonomous customer delivery
- [ ] no autonomous credential changes
- [ ] no autonomous destructive actions
- [ ] no agent self-approval
- [ ] no raw data to Observatory
- [ ] no credentials in artifacts/logs/prompts/docs

Workspace-specific hard-no rules:

```text
Add here.
```

## Step 12 - Define Manual-Test Goal

Manual-test goal:

```text
What exact workflow will be manually validated first?
```

Manual test must identify:

- [ ] start condition
- [ ] human actor
- [ ] inputs
- [ ] artifacts produced
- [ ] review items created
- [ ] human decisions recorded
- [ ] audit records expected
- [ ] signals captured, if any
- [ ] failure cases tested
- [ ] exit criteria

## Internal Research Intake Note

Internal Research is low-risk and internal, but it still needs a lightweight intake/classification record before a workspace config is drafted.

That intake should confirm `internal_research` type, no default customer data, no external action posture, human-started manual/on-demand runtime only, and a manual-test goal for artifact/review/audit/signal flow.

## Step 13 - Draft Workspace Config

Draft fields:

```yaml
workspace_id:
workspace_name:
workspace_type:
status: onboarding | manual_test
purpose:
channels:
adapter:
allowed_agents:
review_gates:
observatory:
  can_query:
  can_submit_sanitized_signals:
  allowed_query_types:
  signal_submission_requires_human_review: true
storage_rules:
runtime:
  default_mode:
  allowed_modes:
  scheduled_allowed: false
  watch_mode_allowed: false
  emergency_stop_supported: true
hard_no_rules:
audit_requirements:
manual_test_goal:
```

Do not include workspace-private customer data in the config.

## Step 14 - Onboarding Decision

Decision:

- [ ] Approve for onboarding
- [ ] Needs more information
- [ ] Park
- [ ] Reject
- [ ] Escalate to ADR

Reason:

```text
Add reason here.
```

Required before approval:

- [ ] Workspace type is valid.
- [ ] Ownership boundaries are clear.
- [ ] Review gates are clear.
- [ ] Manual-test goal is clear.
- [ ] Hard-no rules are clear.
- [ ] Deferred domains are not being promoted accidentally.
- [ ] SearchClarity-specific or business-specific details stay outside core.

## SearchClarity-Specific Reminder

SearchClarity is a likely future `service` workspace.

SearchClarity should not be fully onboarded until its business-readiness track has enough evidence:

- [ ] polished sample report source
- [ ] PDF export pipeline
- [ ] report style/template system
- [ ] delivery-ready sample PDF
- [ ] minimal tracker workbook
- [ ] Fiverr gig copy
- [ ] buyer intake form
- [ ] fulfillment SOP
- [ ] QC checklist
- [ ] pricing source of truth
- [ ] consent language

SearchClarity-specific business assets remain workspace-owned.

## Final Rule

```text
Onboard the workspace; do not smuggle the business into core.
```
