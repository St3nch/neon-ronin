# 16 - Error And Failure Handling

## Purpose

This document defines Neon Ronin's contract for errors, failures, blocked actions, rejected work, retries, escalations, and recovery behavior.

It exists to answer:

```text
When something fails, blocks, rejects, expires, cancels, or becomes uncertain, what state does Neon Ronin record, what happens next, who must review it, and what must never be hidden?
```

Failure handling is part of the platform safety model.

A system that hides failure cannot be trusted with agents, workspaces, signals, reviews, external actions, or future automation.

## Core Rule

```text
Failure must become explicit state.
```

Neon Ronin must not silently continue after a meaningful failure.

Neon Ronin must not pretend a failed, blocked, rejected, parked, expired, cancelled, or uncertain operation succeeded.

## Failure Is Not One Thing

Use precise states instead of vague failure language.

Common outcomes:

| Outcome | Meaning |
|---|---|
| `failed` | Work attempted and did not complete successfully |
| `blocked` | Work was prevented by rule, permission, lifecycle, safety, or missing requirement |
| `rejected` | Human or validation rejected the item/output/action |
| `revision_requested` | Human requested changes before work may proceed |
| `parked` | Human held the item for later without proceeding |
| `cancelled` | Human/system stopped the work before completion |
| `expired` | Work or approval timed out |
| `skipped` | Work was intentionally not run because it was no longer needed or disallowed |
| `unknown` | Outcome cannot be confirmed and must be treated carefully |

Do not collapse these into `error` unless the exact state is not yet known.

## Required Failure Posture

For meaningful work, Neon Ronin must preserve:

- what failed or blocked
- where it happened
- who or what caused it
- what workspace was involved
- what input/output was affected
- what rule or dependency was involved
- what state was recorded
- whether human review is required
- whether retry is allowed
- what audit record traces it
- what must not happen next

## Error Classes

Initial error/failure classes:

```text
validation_error
permission_denied
lifecycle_blocked
runtime_blocked
review_required
review_rejected
human_revision_requested
human_parked
human_cancelled
missing_input
missing_provenance
missing_artifact
missing_review_gate
missing_human_decision
secrets_or_credentials_blocked
credential_incident
external_integration_error
external_provider_error
observatory_permission_denied
observatory_sanitization_failed
signal_blocked
artifact_blocked
workflow_step_failed
agent_run_failed
agent_run_blocked
audit_logging_failed
schema_violation
unknown_field_rejected
rate_limited
timeout
dependency_unavailable
conflict_detected
stale_state
unsafe_output_detected
unknown_error
```

Error classes may expand later through schema authority.

Do not create provider-specific core error classes when a generic class plus external reference is enough.

## Severity Levels

Initial severity levels:

```text
info
warning
error
critical
incident
```

Meanings:

| Severity | Meaning |
|---|---|
| `info` | Expected non-harmful condition worth recording |
| `warning` | Work completed or stopped with caveats |
| `error` | Work failed or was blocked and needs attention |
| `critical` | Work may affect safety, data integrity, credentials, external state, or trust |
| `incident` | Security, credential, privacy, or serious external-action risk |

Severity must not bypass review.

Severity should influence escalation.

## Retry Policy

Retries must be explicit.

Default posture:

| Failure Class | Retry Default |
|---|---|
| validation error | do not retry until corrected |
| permission denied | do not retry until permission changes |
| lifecycle blocked | do not retry until lifecycle changes |
| runtime blocked | do not retry until runtime mode changes |
| review required | do not retry; create/reuse review item |
| review rejected | do not retry unless revised and resubmitted |
| missing provenance | do not retry until provenance is supplied |
| credential incident | do not retry until incident resolved |
| external provider timeout | may retry if bounded and audited |
| rate limited | may retry later if bounded and allowed |
| dependency unavailable | may retry later if safe |
| audit logging failed | do not proceed |
| unknown error | do not retry automatically |

Automated retries are deferred unless explicitly promoted later.

Early Neon Ronin should prefer human-started retries.

## No Silent Retry Rule

Neon Ronin must not silently retry meaningful state-changing operations.

Retries must preserve:

- original failed/blocked run or action
- retry trigger actor
- retry reason
- retry attempt number
- changed inputs if any
- linked audit records
- final result

A retry is a new traceable attempt, not a rewrite of history.

## Audit-First Rule

If an operation changes meaningful state or fails while attempting meaningful state, it must create an audit record.

If audit logging itself fails, Neon Ronin must not continue to perform external actions, live writes, destructive actions, credential changes, permission changes, or Observatory intake.

```text
audit_logging_failed -> block consequential action
```

Audit failure is a platform safety failure.

## Review-Required Failures

Some failures should create or update review items instead of proceeding.

Examples:

- missing required human decision
- output requires QA review
- customer-facing artifact not approved
- signal candidate requires sanitization review
- external write request requires approval
- credential scope change requires review
- unsafe output detected
- missing provenance for decision-grade output

Review-required state is not success.

It is controlled pause.

## Blocked Action Rules

A blocked action means Neon Ronin correctly prevented something from proceeding.

Blocked actions should be auditable when meaningful.

Common block reasons:

```text
workspace_lifecycle_disallows_action
runtime_mode_disallows_action
permission_scope_denied
review_gate_required
human_decision_missing
hard_no_rule_violation
credential_reference_missing
credential_scope_denied
observatory_permission_denied
sanitization_required
missing_provenance
schema_validation_failed
external_integration_not_promoted
```

A blocked action should not be treated as a system crash.

A blocked action is often the system working correctly.

## Failed Action Rules

A failed action means Neon Ronin attempted work and did not complete it successfully.

Failures should record:

- failure class
- severity
- affected record(s)
- actor/run/workflow involved
- safe error summary
- retry eligibility
- review/escalation need
- audit record

Failures must not store raw private data, credentials, full provider payloads, or unsafe output dumps.

## Unknown Outcome Rule

If Neon Ronin cannot confirm whether an operation succeeded, the result must be treated as `unknown` until reconciled.

Unknown outcomes are especially dangerous for external actions.

For unknown external action outcomes:

1. do not repeat the action automatically
2. create an audit record
3. create or update a review item
4. reconcile with external reference/provider state if possible
5. require human decision before retrying consequential action

## External Action Failure Rules

External action failures must be bounded and audited.

External action failure records should include:

- workspace id
- provider or external reference
- action class
- requested action
- triggering actor
- review item id if applicable
- human decision id if applicable
- result status
- safe error code
- safe error summary
- retry eligibility
- audit record id

External action failures must not include:

- raw credentials
- tokens
- full provider responses
- full customer payloads
- raw private artifact contents

## Credential Failure Rules

Credential-related failures may be normal errors or incidents.

Examples:

| Failure | Classification |
|---|---|
| credential reference not found | error |
| credential expired | error or warning depending context |
| credential scope denied | blocked |
| credential value found in artifact/log/docs | incident |
| provider auth failed | error |
| token suspected compromised | incident |
| credential used without approval | incident |

Credential incidents must follow `docs/core/15-secrets-and-credentials.md`.

## Signal Failure Rules

Signal failures must preserve the boundary between workspace-private data and Observatory-owned intelligence.

Common signal failures:

- raw signal contains private data
- signal candidate contains private data
- signal candidate missing provenance
- sanitization review rejected
- Observatory permission denied
- normalization failed
- derived intelligence missing source references

Rules:

- raw signals do not enter Observatory
- rejected candidates remain auditable
- parked candidates do not proceed
- missing provenance blocks decision-grade use
- failed normalization does not erase sanitized signal provenance

## Artifact Failure Rules

Artifact failures include:

- artifact missing
- storage reference invalid
- artifact contaminated with secret
- artifact contains private data not allowed for its scope
- artifact not delivery-ready
- artifact review rejected
- PDF/export generation failed
- public-use consent missing

Rules:

- contaminated artifacts are blocked
- customer-facing artifacts require review before delivery
- public-use artifacts require consent or fictional/sample status
- failed export does not approve the source artifact

## Workflow Failure Rules

Workflow step failures must not be hidden by later steps.

If a required step fails, downstream steps must block unless a human decision explicitly changes the path.

Workflow failures should record:

- workflow id
- step id
- step type
- actor
- input references
- output references if any
- error class
- blocked/failed status
- audit record
- required review/escalation

## Agent Run Failure Rules

Agent run failures must follow `docs/core/schemas/agent-run.schema.md`.

Agent runs may end as:

```text
completed
completed_with_warnings
failed
blocked
cancelled
expired
skipped
waiting_for_review
```

Agent failures must not approve outputs, hide missing provenance, or continue into external action without review.

If an agent produces unsafe, private, credential-bearing, or uncertain output, the run should be blocked or routed to review.

## Permission Failure Rules

Permission failures are usually blocked actions.

If permission scope denies an action:

1. do not perform the action
2. record blocked result if meaningful
3. create audit record
4. create review item only if a human decision could safely change scope
5. do not auto-expand permission

No actor may expand its own permission after denial.

## Validation Failure Rules

Validation failures should reject invalid records or transitions.

Validation failure examples:

- unknown field in core schema
- invalid lifecycle transition
- invalid status transition
- missing required field
- forbidden field present
- provider-specific field in core schema
- unbounded metadata used as semantic truth
- source references missing

Invalid records should not be silently corrected unless a schema explicitly defines safe normalization.

## Parking Rules

Parking is a deliberate human decision to hold work.

Parked items:

- remain visible
- remain auditable
- do not proceed
- do not expire unless explicitly configured
- may be reopened through governed action

Parking is not rejection.

Parking is not approval.

## Rejection Rules

Rejected work must not proceed unless revised and resubmitted through the appropriate path.

Rejected work remains auditable.

Rejected signal candidates do not enter the Observatory.

Rejected artifacts do not become delivery-ready.

Rejected permission changes do not change permissions.

Rejected external action requests do not execute.

## Cancellation Rules

Cancellation stops work before completion.

Cancelled work should record:

- who or what cancelled it
- why it was cancelled if known
- what records were affected
- whether partial outputs exist
- whether cleanup is required
- audit record

Cancellation is not failure if intentionally chosen.

Cancellation is not approval.

## Expiration Rules

Expiration means a record, approval, request, or action window is no longer valid.

Expired items must not proceed without revalidation.

Examples:

- review approval expires before external action
- credential scope expires
- queued run expires before starting
- stale workspace intake requires review

Expiration should be auditable when meaningful.

## Escalation Rules

Escalation routes uncertain or higher-risk items to human review or a stricter review path.

Escalate when:

- sensitivity is high or restricted
- confidence is low and action is consequential
- provenance is missing
- policy/compliance risk is unclear
- credential exposure is suspected
- external outcome is unknown
- agent output may be unsafe
- workspace boundary is unclear

Escalation is not approval.

## Recovery Rules

Recovery must be explicit and traceable.

Recovery may include:

- retrying with corrected input
- revising artifact
- resubmitting review item
- restoring prior safe state
- revoking or rotating credential
- reopening parked item
- creating superseding decision
- creating corrected record
- archiving contaminated output

Recovery must not rewrite the failure out of history.

## State Correction Rules

If a record was wrong, create a correction or superseding record when possible.

Do not silently mutate history.

Corrections should preserve:

- incorrect prior state
- corrected state
- reason
- actor
- audit record
- affected records

Audit records themselves should be append-friendly and effectively immutable.

## Error Summary Rules

Error summaries should be useful but safe.

They may include:

- error class
- safe reason
- affected record id
- provider error code if non-sensitive
- retry eligibility
- next required action

They must not include:

- secrets
- raw tokens
- passwords
- full customer payloads
- full provider responses
- private artifact content
- unsafe generated output dumps

## Example Failure Record Shape

This is a conceptual shape, not a new P1 schema.

```yaml
error_class: missing_provenance
severity: error
result_status: blocked
workspace_id: ws_internal_research_001
affected_record_type: signal_candidate
affected_record_id: sigcand_001
actor_type: agent
actor_id: signal_capture_agent
safe_summary: Signal candidate is missing source references required for sanitization review.
retry_allowed: false
next_required_action: Add source references or reject candidate.
review_item_id: rev_001
audit_record_id: audit_001
```

## Example External Unknown Outcome

```yaml
error_class: external_provider_error
severity: critical
result_status: unknown
workspace_id: ws_future_marketplace_001
external_reference_id: extref_provider_listing_001
action_class: live_write
safe_summary: Provider request timed out after submission; final external state is unknown.
retry_allowed: false
next_required_action: Human review and provider-state reconciliation required before retry.
review_item_id: rev_001
audit_record_id: audit_001
```

## Non-Goals

This document does not define:

- full exception classes in code
- database schema for error records
- alerting implementation
- retry scheduler
- provider-specific error mapping
- UI error display
- observability stack
- log aggregation system
- incident response runbook details

Those come later.

## Relationship To Other Docs

This document depends on:

- `docs/core/06-review-queue.md`
- `docs/core/07-permissions-and-audit.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/15-secrets-and-credentials.md`
- `docs/core/schemas/audit-record.schema.md`
- `docs/core/schemas/review-queue-item.schema.md`
- `docs/core/schemas/agent-run.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/core/schemas/permission-scope.schema.md`

This document informs:

- `docs/operations/review-queue-runbook.md`
- `docs/operations/emergency-stop-procedure.md`
- `docs/operations/manual-test-template.md`
- future runtime implementation
- future integration contracts
- future observability/logging design

## Final Rule

```text
Fail loud, fail safe, and leave a trace.
```
