# Workspace Promotion Checklist

## Purpose

This checklist defines how a Neon Ronin workspace moves from one lifecycle status to another.

It exists to prevent workspace promotion from becoming a vibes-based shortcut around manual proof, review gates, auditability, data boundaries, or hard-no rules.

## Core Rule

```text
A workspace earns promotion by evidence, not enthusiasm.
```

Promotion must be based on documented workflow proof, review outcomes, audit coverage, and boundary checks.

## Applies To

Workspace lifecycle statuses:

```text
idea
onboarding
manual_test
active
paused
retired
```

This checklist is especially important for:

- promoting Internal Research into manual test
- later promoting SearchClarity into onboarding/manual test
- pausing workspaces safely
- retiring workspaces without deleting history
- preventing premature active status

## Required References

Before using this checklist, read or reference:

- `docs/core/09-workspace-lifecycle.md`
- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/schemas/workspace-config.schema.md`
- `docs/core/schemas/review-queue-item.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/core/schemas/audit-record.schema.md`
- `docs/operations/workspace-onboarding-checklist.md`
- `docs/operations/manual-test-template.md`

## Promotion Header

```yaml
promotion_review_id:
workspace_id:
workspace_name:
workspace_type:
current_status:
proposed_status:
review_date:
reviewer_actor_id:
promotion_status: proposed | approved | rejected | parked | blocked
```

## Allowed Promotion Paths

Default lifecycle path:

```text
idea -> onboarding -> manual_test -> active -> paused -> retired
```

Other allowed operational transitions may include:

```text
active -> paused
paused -> active
manual_test -> paused
paused -> manual_test
onboarding -> parked/rejected outside lifecycle if intake fails
```

Retired should be treated as closed for new work.

Reactivation from retired is forbidden unless a future ADR defines a controlled process.

## Universal Promotion Requirements

Before any promotion:

- [ ] Workspace id is known.
- [ ] Workspace type is valid.
- [ ] Current status is known.
- [ ] Proposed status is valid.
- [ ] Transition is allowed.
- [ ] Human reviewer is identified.
- [ ] Audit record will be created.
- [ ] Human decision will be recorded.
- [ ] Open blockers are listed.
- [ ] Deferred domains are checked.
- [ ] Hard-no rules remain intact.

## Idea To Onboarding

Use when a business idea becomes an onboarding candidate.

Required evidence:

- [ ] Business intake exists or source docs are available.
- [ ] Workspace type is proposed.
- [ ] Candidate purpose is clear.
- [ ] Expected inputs are described.
- [ ] Expected outputs are described.
- [ ] Private data expectations are identified.
- [ ] External systems are identified.
- [ ] Forbidden-in-core details are identified.
- [ ] Initial hard-no rules are defined.
- [ ] Manual-test goal is drafted.

Decision:

- [ ] approve onboarding
- [ ] request more information
- [ ] park
- [ ] reject

## Onboarding To Manual Test

Use when a workspace is ready to validate a workflow manually.

Required evidence:

- [ ] Draft workspace config exists.
- [ ] Workspace purpose is clear.
- [ ] Adapter fit is identified.
- [ ] Expected artifacts are identified.
- [ ] Expected workflows are identified.
- [ ] Required review gates are identified.
- [ ] Audit requirements are identified.
- [ ] Storage/data boundaries are identified.
- [ ] Observatory permissions are explicit.
- [ ] External integration touchpoints are deferred or bounded.
- [ ] Permission/hard-no rules are explicit.
- [ ] Manual-test template is prepared.
- [ ] Manual-test success criteria are defined.

Runtime requirements:

- [ ] Default runtime mode is `on_demand` or `off`.
- [ ] Scheduled mode is disabled.
- [ ] Watch mode is disabled.
- [ ] Emergency stop is supported.

Decision:

- [ ] approve manual test
- [ ] request revision
- [ ] park
- [ ] block

## Manual Test To Active

Use only after manual workflows have been validated.

Required evidence:

- [ ] Manual test was completed.
- [ ] Manual test result was passed or passed with acceptable notes.
- [ ] Artifacts were produced and tracked.
- [ ] Review queue items were created where required.
- [ ] Human decisions were recorded.
- [ ] Audit records trace meaningful state changes.
- [ ] Failure/block cases were tested or explicitly deferred with reason.
- [ ] Signal handling was tested if signals are in scope.
- [ ] Sanitization gate was tested if Observatory submission is in scope.
- [ ] Permission boundaries held.
- [ ] No hard-no rules were violated.
- [ ] No external live writes occurred without explicit approval.
- [ ] No secrets entered docs/artifacts/logs/prompts.
- [ ] Reusable capability gaps are recorded.
- [ ] Workspace-specific details stayed out of core.

Active-mode requirements:

- [ ] Active runtime modes are explicitly configured.
- [ ] On-demand behavior is defined.
- [ ] Scheduled/watch mode remains disabled unless future roadmap allows.
- [ ] Agents, if any, are bounded by agent definitions and permission scopes.
- [ ] Review gates remain active.

Decision:

- [ ] approve active
- [ ] repeat manual test
- [ ] request revisions
- [ ] park
- [ ] block

## Active To Paused

Use when a workspace should stop new work while preserving state.

Reasons may include:

- business pause
- safety concern
- credential concern
- external integration concern
- unresolved review backlog
- data boundary concern
- incident
- operator decision

Required actions:

- [ ] Reason is recorded.
- [ ] New runs are blocked.
- [ ] New review items are blocked unless needed for incident/recovery.
- [ ] New external actions are blocked.
- [ ] New Observatory submissions are blocked.
- [ ] Open work is triaged.
- [ ] Audit record is created.
- [ ] Human decision is recorded.

Decision:

- [ ] pause workspace
- [ ] emergency stop instead
- [ ] continue active with restrictions

## Paused To Active

Use when resuming a paused workspace.

Required evidence:

- [ ] Pause reason is resolved or accepted.
- [ ] Open review items are triaged.
- [ ] Credential/integration risks are resolved if relevant.
- [ ] Workspace config is still valid.
- [ ] Runtime modes are still valid.
- [ ] Hard-no rules are intact.
- [ ] Audit record is created.
- [ ] Human decision is recorded.

Decision:

- [ ] resume active
- [ ] resume manual test
- [ ] remain paused
- [ ] retire

## Any Status To Retired

Use when a workspace should close for new operations.

Required actions:

- [ ] Retirement reason is recorded.
- [ ] New runs are blocked.
- [ ] New workflows are blocked.
- [ ] New external actions are blocked.
- [ ] New Observatory submissions are blocked.
- [ ] Open review items are resolved, cancelled, parked, or archived.
- [ ] Artifacts are archived according to ownership rules.
- [ ] Audit records remain preserved.
- [ ] Credential references are revoked/retired if applicable.
- [ ] External integrations are paused/retired if applicable.
- [ ] Human decision is recorded.
- [ ] Audit record is created.

Decision:

- [ ] retire workspace
- [ ] pause instead
- [ ] park retirement decision

## Promotion Blockers

Block promotion if any are true:

- [ ] workspace type is unclear
- [ ] ownership boundaries are unclear
- [ ] review gates are missing
- [ ] audit requirements are missing
- [ ] manual-test goal is vague
- [ ] hard-no rules are weakened
- [ ] external integration is being smuggled in
- [ ] provider-specific fields enter core
- [ ] secrets appear in docs/artifacts/logs/prompts
- [ ] raw workspace data would enter Observatory
- [ ] agent could approve its own work
- [ ] active status is requested without manual proof
- [ ] SearchClarity-specific business logic is entering core

Blocker notes:

```text
Add blocker notes here.
```

## Required Human Decision

Every promotion requires a human decision record.

Decision shape:

```yaml
human_decision_id:
decision_type: promote | reject | request_revision | park | block | retire | resume
decision_scope: workspace_lifecycle
reviewer_actor_id:
target_records:
  - record_type: workspace_config
    record_id:
    relationship: promotion_target
decision_summary:
audit_record_id:
```

## Required Audit Events

Promotion should create audit records for:

- workspace promotion review started
- workspace status changed
- human decision recorded
- blockers found
- promotion rejected
- promotion parked
- workspace paused
- workspace resumed
- workspace retired

## Internal Research Promotion Notes

Internal Research may enter manual test when:

- [ ] workspace config draft exists
- [ ] manual-test goal is clear
- [ ] no external writes are needed
- [ ] no customer data is involved
- [ ] artifacts/review/audit/signal flow can be tested safely

Internal Research should not be active until manual-test proof exists.

## SearchClarity Promotion Notes

SearchClarity should not enter full Neon Ronin onboarding until the parallel SearchClarity readiness track has enough evidence.

SearchClarity should not enter manual test until:

- [ ] sample report/source is sufficiently complete
- [ ] report workflow is clear
- [ ] tracker or equivalent records exist
- [ ] buyer intake is defined
- [ ] QA checklist exists
- [ ] no customer delivery automation is planned
- [ ] SearchClarity-specific details stay workspace-owned

## Final Rule

```text
Promotion is a controlled transition, not a mood.
```
