# Review Queue Runbook

## Purpose

This runbook defines how humans operate the Neon Ronin review queue.

The review queue is where risky, important, customer-facing, public-facing, paid, destructive, credential-related, privacy-sensitive, compliance-sensitive, or Observatory-intake work waits for human judgment.

## Core Rule

```text
The review queue is a control gate, not a rubber stamp.
```

A review item requests human judgment.

It does not execute the action by existing.

## Applies To

Use this runbook for review items involving:

- artifact quality review
- customer delivery review
- publish review
- paid action review
- destructive action review
- credential or permission review
- privacy review
- rights/IP/compliance review
- signal sanitization review
- strategy review
- workspace promotion review
- external write review
- escalation review

## Required References

This runbook depends on:

- `docs/core/06-review-queue.md`
- `docs/core/07-permissions-and-audit.md`
- `docs/core/08-sanitization.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/16-error-and-failure-handling.md`
- `docs/core/schemas/review-queue-item.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/core/schemas/audit-record.schema.md`

## Review Queue Statuses

Canonical review item statuses:

```text
open
in_review
approved
approved_with_changes
rejected
revision_requested
escalated
parked
blocked
cancelled
expired
```

Do not invent casual status names like `done-ish`, `looks fine`, or `probably okay`.

Tiny ambiguity goblins live there.

## Reviewer Responsibilities

A reviewer must:

- confirm workspace scope
- confirm review type
- confirm risk categories
- inspect linked records
- confirm required gates
- verify provenance
- check privacy and credential safety
- check lifecycle/runtime constraints
- decide within recorded scope
- create or trigger audit record
- avoid broad accidental approval

A reviewer must not:

- approve their own agent output as an agent
- approve without checking target records
- approve external action without scope
- approve raw data into Observatory
- approve credentials appearing in normal records
- treat score/rank/recommendation as decision authority

## Review Intake Steps

When a review item appears:

1. Confirm `review_item_id` exists.
2. Confirm `workspace_id` exists and is valid.
3. Confirm workspace lifecycle allows review to proceed.
4. Confirm `review_type` is valid.
5. Confirm `risk_categories` are present.
6. Confirm `required_gates` are present.
7. Confirm `linked_records` are references, not payload dumps.
8. Confirm source actor/run is traceable.
9. Confirm audit record exists or will be created.
10. Decide whether to begin review, block, park, or request revision.

## Begin Review

Move review item:

```text
open -> in_review
```

Only begin review if:

- item has enough context
- reviewer is a human actor where human review is required
- linked records can be inspected
- there is no obvious credential/private-data incident
- workspace is not paused/retired in a way that blocks review

If context is missing, request revision or block.

## Standard Review Checklist

For every item:

- [ ] Workspace id is valid.
- [ ] Workspace lifecycle allows this review.
- [ ] Review type is valid.
- [ ] Risk categories are correct.
- [ ] Required gates are correct.
- [ ] Source actor is traceable.
- [ ] Linked records are references, not ownership transfers.
- [ ] Provenance is sufficient.
- [ ] No credentials or raw secrets are present.
- [ ] No forbidden private payload dump is present.
- [ ] Recommended action is bounded.
- [ ] Decision will be scoped.
- [ ] Audit record will be created.

## Decision Options

Allowed human decisions:

```text
approve
approve_with_changes
reject
request_revision
escalate
park
block
cancel
```

Use the most precise decision.

Approval is not the only useful outcome.

Blocking bad work means the system is functioning.

## Approval Rules

Approve only when:

- all required gates are satisfied
- provenance is sufficient
- privacy boundary is safe
- credential boundary is safe
- target action is bounded
- workspace lifecycle allows next step
- runtime mode allows next step
- permission scope allows next step
- hard-no rules are not violated
- audit logging is available

Approval should state exactly what is approved.

Bad approval:

```text
Looks good.
```

Good approval:

```text
Approve artifact art_001 as delivery-ready for this manual-test workflow only. No external delivery action is approved.
```

## Approve With Changes

Use `approve_with_changes` when small bounded changes are required and the reviewer can specify them clearly.

Required:

- changed fields or required edits listed
- scope of approval stated
- audit record created
- no private payloads added to decision notes

If changes are substantial, request revision instead.

## Request Revision

Use `request_revision` when the item may become acceptable after changes.

Common reasons:

- missing provenance
- unclear recommendation
- incomplete artifact
- missing QA notes
- weak evidence summary
- private details need removal
- signal candidate needs better generalization
- review gate mismatch

Revision instructions should be specific and actionable.

## Reject

Use `reject` when the item should not proceed.

Common reasons:

- violates hard-no rule
- contains secrets
- contains private data that cannot be safely generalized
- unsupported external action
- bad fit for workspace lifecycle
- too risky for current phase
- no valid provenance
- provider-specific payload trying to enter core

Rejected items remain auditable.

Rejected does not mean deleted.

## Park

Use `park` when the item is not wrong but should not proceed now.

Common reasons:

- good idea, wrong phase
- waiting for SearchClarity readiness
- waiting for schema/contract support
- waiting for more evidence
- lower priority than current roadmap

Parked items do not proceed.

Parked is not approval.

## Escalate

Use `escalate` when higher scrutiny is needed.

Escalate if:

- privacy risk is unclear
- credential exposure is suspected
- external outcome is unknown
- legal/IP/compliance concern exists
- workspace boundary is unclear
- score/recommendation conflicts with evidence
- action could affect customers/public/external accounts
- reviewer lacks enough authority or context

Escalation should identify what must be reviewed next.

## Block

Use `block` when Neon Ronin must prevent progress.

Common blockers:

- lifecycle disallows action
- runtime mode disallows action
- permission scope denies action
- required human decision is missing
- required review gate is missing
- credential reference is missing or unsafe
- raw data would enter Observatory
- external integration is deferred
- audit logging is unavailable
- unknown/forbidden field appears in core record

Blocked items require explicit resolution before reopening.

## Cancel

Use `cancel` when work is intentionally stopped before a final approval/rejection decision.

Cancellation should record:

- who cancelled
- why cancelled if known
- affected records
- whether partial outputs exist
- audit record

## Review Type Procedures

## Quality Review

Check:

- [ ] artifact/output is complete
- [ ] claims are supported
- [ ] evidence summary is clear
- [ ] formatting/structure is acceptable
- [ ] no missing sections needed for current phase
- [ ] no unsafe certainty or fake guarantee

Allowed decisions:

```text
approve
approve_with_changes
request_revision
reject
park
```

## Customer Delivery Review

Check:

- [ ] artifact is delivery-ready
- [ ] customer/private data is handled correctly
- [ ] no unsupported promises
- [ ] no hidden credentials/provider details
- [ ] delivery message is appropriate if in scope
- [ ] customer-facing action is bounded

Customer delivery must not be autonomous.

Approval should specify whether it approves the artifact only or the delivery action too.

## Publish Review

Check:

- [ ] public-facing content is approved
- [ ] rights/IP concerns checked
- [ ] privacy concerns checked
- [ ] provider/platform constraints considered
- [ ] public-use consent exists if required
- [ ] no customer-private data leaks

No autonomous publishing.

## Paid Action Review

Check:

- [ ] amount or cost boundary is explicit
- [ ] payment/refund/provider context is explicit
- [ ] human approval is explicit
- [ ] credential/payment references are safe
- [ ] audit requirement is clear

No autonomous spending.

## Destructive Action Review

Check:

- [ ] target is explicit
- [ ] reason is explicit
- [ ] reversibility is understood
- [ ] human approval is explicit
- [ ] external reference is explicit if applicable
- [ ] audit record is required

Autonomous destructive actions are forbidden.

## Credential Or Permission Review

Check:

- [ ] no raw secret value appears
- [ ] credential reference only
- [ ] permission scope is bounded
- [ ] denied actions are explicit
- [ ] review gates remain required
- [ ] expiration/revocation behavior is clear
- [ ] human decision is linked

Approval does not reveal secret values.

Approval does not create broad permanent permission unless explicitly scoped and audited.

## Signal Sanitization Review

Check:

- [ ] linked signal candidate exists
- [ ] source provenance exists
- [ ] private data was removed/generalized
- [ ] no customer identifiers remain
- [ ] no credentials remain
- [ ] no workspace-private strategy leaks
- [ ] signal type is business-neutral
- [ ] Observatory submission is allowed by workspace config
- [ ] confidence/data quality notes are reasonable

Allowed outcomes:

- approve sanitized signal
- request revision
- reject
- park
- block

Approval permits only the reviewed sanitized signal to proceed.

It does not approve raw signal sharing.

## Workspace Promotion Review

Use `docs/operations/workspace-promotion-checklist.md`.

Do not promote a workspace from manual test to active without manual-test evidence.

Do not promote SearchClarity before readiness evidence exists.

## External Write Review

Check:

- [ ] external provider/resource is explicit
- [ ] external reference is explicit
- [ ] action class is explicit
- [ ] provider capability is not confused with permission
- [ ] permission scope allows request
- [ ] credential reference is valid
- [ ] human decision is scoped
- [ ] audit logging is available
- [ ] idempotency/unknown outcome risks considered

No autonomous external live writes.

## Audit Requirements

Review queue events that require audit:

- review item created
- review item opened/in review
- review decision made
- approval recorded
- approval with changes recorded
- revision requested
- rejection recorded
- escalation recorded
- parking recorded
- blocking recorded
- cancellation recorded
- expiration recorded
- linked record changed after review creation

Audit records should include safe summaries, not payload dumps.

## Safe Decision Notes

Decision notes may include:

- decision reason
- target record ids
- safe evidence summary
- conditions
- revision instructions
- blocker reason

Decision notes must not include:

- raw customer data
- private artifact body
- credentials
- provider tokens
- full provider responses
- raw external payloads
- exact private report text when unnecessary

## Reopening Items

Only reopen if the prior blocker/reason is resolved.

Reopening should be audited.

Common reopen paths:

```text
revision_requested -> open
parked -> open
blocked -> open
escalated -> in_review
```

Do not reopen rejected items casually.

Create a new review item if the revised work is materially different.

## Review Backlog Hygiene

Regularly check for:

- stale open items
- parked items that need revisiting
- blocked items without resolution path
- expired approvals
- items missing provenance
- items tied to paused/retired workspaces
- items touching deferred domains
- items waiting on SearchClarity readiness

Backlog hygiene is operational safety.

## Example Review Decision

```yaml
human_decision_id: hdec_001
workspace_id: ws_internal_research_001
review_item_id: rev_001
decision_type: approve
decision_status: recorded
decision_scope: signal_candidate
reviewer_actor_id: human_operator
target_records:
  - record_type: signal_candidate
    record_id: sigcand_001
    relationship: approved_signal_candidate
decision_summary: Approved sanitized signal candidate for Observatory intake.
decision_notes: Candidate contains no customer data, credentials, or workspace-private details.
conditions:
  - Submit only the reviewed sanitized signal text.
audit_record_id: audit_001
```

## Emergency Stop Link

If review reveals active risk involving credentials, external writes, customer data leakage, uncontrolled agents, or destructive actions, use the emergency stop procedure when available.

Until then:

1. pause the workspace or integration if possible
2. block related review items
3. create audit records
4. escalate to human/operator decision
5. do not proceed with external actions

## SearchClarity Reminder

SearchClarity-related review items should preserve the boundary:

- SearchClarity report text is workspace-owned
- SearchClarity customer data is workspace-owned
- Fiverr copy is workspace-owned
- raw market signals are workspace-owned
- sanitized generalized signals may be reviewed for Observatory intake later
- no customer delivery automation early
- no Fiverr automation early

## Final Rule

```text
Review is where Neon Ronin slows down on purpose.
```
