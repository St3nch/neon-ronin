# Signal Schema

## Purpose

This document defines the P0 signal schema for Neon Ronin.

A signal is a useful observation that may inform workspace decisions or shared Observatory intelligence.

Signal records must preserve the boundary between workspace-private observations and Observatory-owned generalized intelligence.

## Schema Status

```text
P0 planning schema
```

This is an implementation-facing planning document.

It is not yet a database migration, JSON Schema file, Pydantic model, TypeScript type, or API contract.

## Ownership Category

Signal ownership changes by lifecycle stage.

| Signal Form | Ownership |
|---|---|
| Raw signal | Workspace-owned data |
| Signal candidate | Workspace-owned data |
| Sanitization review | Core-owned review record |
| Sanitized signal | Observatory-owned data after approval |
| Normalized Observatory signal | Observatory-owned data |
| Derived intelligence | Derived data / Observatory-owned data |

## Core Rule

```text
Raw workspace observations do not enter the Observatory.
Only approved sanitized signals may enter the Observatory.
```

A signal is not safe because it is useful.

A signal is safe only after sanitization and review.

## Signal Lifecycle

Canonical signal lifecycle:

```text
raw_signal
-> signal_candidate
-> sanitization_review
-> sanitized_signal
-> observatory_inbox
-> normalized_observatory_record
-> derived_intelligence
```

Not every raw signal becomes a sanitized signal.

Not every sanitized signal becomes derived intelligence.

## Signal Forms

### Raw Signal

An unsanitized observation created inside a workspace.

Raw signals are workspace-owned and may contain private, identifying, confidential, or business-specific context.

Raw signals must not enter the Observatory.

### Signal Candidate

A proposed sanitized/generalized version of a raw signal.

Signal candidates are reviewable but not yet Observatory-owned.

Signal candidates must pass a sanitization review before Observatory intake.

### Sanitized Signal

An approved generalized signal eligible for Observatory intake.

Sanitized signals must not contain private workspace/customer details.

### Normalized Observatory Record

A sanitized signal converted into a standard Observatory format.

Normalization must preserve restricted internal provenance and must not expose private details through normal query surfaces.

### Derived Intelligence

A derived output generated from sanitized/normalized Observatory records.

Examples:

- keyword cluster
- trend profile
- opportunity score
- data quality note
- generalized recommendation

Derived intelligence is not approval and must not directly trigger external action.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `signal_id` | string | system-owned | Stable unique signal id for the current signal form |
| `signal_form` | enum | system-owned | Current form of the signal lifecycle |
| `workspace_id` | string | system/reference | Source workspace id for raw/candidate signals; restricted provenance for sanitized signals |
| `workspace_type` | enum | system/source-owned | Source workspace type for generalized context |
| `status` | enum | system-governed | Current signal status |
| `signal_type` | enum | source/system-owned | Type/category of signal |
| `source_actor_type` | enum | source/system-owned | Actor type that observed or created the signal |
| `source_actor_id` | string | source/system-owned | Actor id that observed or created the signal |
| `source_references` | array object | referenced-only | Source records/artifacts/runs supporting the signal |
| `summary` | string | source-owned | Signal summary appropriate to current lifecycle form |
| `evidence_summary` | string | source-owned | Evidence summary without private payload dump |
| `sensitivity_rating` | enum | source/system-owned | Sensitivity/privacy rating |
| `confidence` | enum | source/system-owned | Evidence confidence level |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |
| `audit_record_id` | string/null | system/reference | Audit record for creation or latest state change |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `parent_signal_id` | string/null | system/reference | Prior signal form this record was derived from |
| `raw_signal_id` | string/null | restricted/reference | Original raw signal id, restricted after sanitization |
| `sanitization_review_item_id` | string/null | referenced-only | Review item that approved/rejected/parked sanitization |
| `sanitization_decision` | enum/null | human/system-owned | Outcome of sanitization review |
| `private_data_removed` | boolean | source/system-owned | Whether private data was removed/generalized |
| `remaining_sensitivity_notes` | string/null | source/human-owned | Notes about residual sensitivity or risk |
| `observatory_destination` | string/null | system/human-owned | Target Observatory zone/category if approved |
| `normalized_record_id` | string/null | system/reference | Resulting normalized Observatory record id |
| `derived_from_signal_ids` | array string | referenced-only | Source signals for derived intelligence |
| `tags` | array string | bounded/source-owned | Bounded classification tags |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Signal Forms

Canonical values:

```text
raw_signal
signal_candidate
sanitized_signal
normalized_observatory_record
derived_intelligence
```

`sanitization_review` is represented by a review queue item, not by the signal record itself.

## Valid Statuses

Canonical signal statuses:

```text
draft
candidate
in_review
approved_sanitized
rejected
revision_requested
parked
submitted_to_observatory
normalized
derived
archived
blocked
```

## Status Transition Rules

Allowed transitions:

| From | To | Requirement |
|---|---|---|
| `draft` | `candidate` | Raw signal is converted into a candidate |
| `candidate` | `in_review` | Signal candidate enters sanitization review |
| `in_review` | `approved_sanitized` | Human approves sanitization |
| `in_review` | `rejected` | Human rejects candidate |
| `in_review` | `revision_requested` | Human requests revision |
| `in_review` | `parked` | Human parks candidate |
| `revision_requested` | `candidate` | Candidate is revised and resubmitted |
| `approved_sanitized` | `submitted_to_observatory` | Approved sanitized signal is submitted |
| `submitted_to_observatory` | `normalized` | Observatory normalizes signal |
| `normalized` | `derived` | Derived intelligence is produced |
| any non-terminal | `blocked` | System/human blocks due to safety, lifecycle, or validation issue |
| any terminal or completed | `archived` | Human/system archives without deletion |

Terminal statuses by default:

```text
rejected
parked
blocked
archived
```

A parked signal may later be reopened through a governed review process.

## Valid Signal Types

Initial signal types:

```text
customer_need_pattern
keyword_pattern
market_gap
competitor_pattern
workflow_problem
quality_issue
content_gap
service_demand_pattern
product_opportunity
policy_or_rights_risk
data_quality_note
research_finding
strategy_observation
other
```

Signal type should remain business-neutral.

Do not create SearchClarity-specific, Etsy-specific, Printify-specific, or Fiverr-specific signal types in core.

## Sensitivity Ratings

Canonical sensitivity ratings:

```text
low
medium
high
restricted
unknown
```

Default posture:

- `low`: potentially eligible after human review
- `medium`: likely requires edits or extra review
- `high`: reject, revise, or escalate
- `restricted`: reject or escalate by default
- `unknown`: treat as medium or high until clarified

## Confidence Values

Canonical confidence values:

```text
low
medium
high
unknown
```

Confidence describes evidence strength.

Confidence is not approval.

## Sanitization Decisions

Canonical sanitization decisions:

```text
approve
approve_with_changes
reject
request_revision
escalate
park
block
```

These decisions should come from a review queue item.

No agent may approve its own signal candidate.

## Source References

`source_references` is an array of thin references.

Allowed source reference types:

```text
artifact
agent_run
review_item
human_decision
audit_record
workflow
external_reference
observatory_query_result
manual_note
business_intake
```

Example:

```yaml
source_references:
  - record_type: artifact
    record_id: art_001
    relationship: source_note
  - record_type: agent_run
    record_id: run_001
    relationship: observed_by
```

Source references must not copy raw private data into the signal record.

## Required Sanitization Properties

A signal candidate should make sanitization explicit:

```yaml
private_data_removed: true
remaining_sensitivity_notes: No customer names, URLs, emails, or exact private report text remain.
```

A signal candidate must be rejected or revised if it contains:

- customer names
- customer emails
- customer phone numbers
- customer addresses
- customer usernames or handles when identifying
- shop URLs tied to a specific customer
- private screenshots
- raw credentials
- API keys
- OAuth tokens
- payment data
- exact customer-owned text that should not be shared
- confidential workspace strategy
- exact report templates from one business
- exact marketplace listing copy from one workspace

## Observatory Submission Rules

A signal may be submitted to the Observatory only when:

1. workspace config allows `can_submit_sanitized_signals`
2. signal is approved through sanitization review
3. signal contains no private workspace/customer details
4. signal has enough provenance for audit
5. audit record creation succeeds
6. workspace lifecycle allows submission

Early Neon Ronin requires human approval before Observatory intake.

## Normal Query Surface Rules

Normal Observatory query responses must not expose:

- raw signal text
- raw source artifacts
- source customer identity
- source workspace-private details
- exact private evidence
- source workspace id unless explicitly allowed by future permission rules

Allowed generalized context may include:

- workspace type
- signal category
- approximate time period
- evidence count
- confidence band
- data quality note

## System-Owned Fields

The following fields should be system-owned:

- `signal_id`
- `signal_form`
- lifecycle status changes
- `created_at`
- `updated_at`
- `audit_record_id`
- `normalized_record_id`
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless a governed correction process allows change:

- `signal_id`
- original `workspace_id`
- original `source_actor_type`
- original `source_actor_id`
- original source references for raw signal creation
- original `created_at`

Later forms should reference prior forms rather than rewrite origin history.

## Provenance Requirements

A signal must preserve enough provenance to trace:

- source workspace
- source workspace type
- source actor
- source run or artifact if applicable
- raw signal origin if applicable
- sanitization review item
- human decision if approved/rejected/parked
- audit records for lifecycle changes
- Observatory normalization if applicable
- derived intelligence if applicable

Restricted internal provenance may exist for audit and debugging.

Normal query surfaces must hide private source details.

## Audit Requirements

The following signal events must generate audit records:

- raw signal created
- signal candidate created
- signal candidate submitted for review
- sanitization decision made
- signal approved as sanitized
- signal rejected
- signal revision requested
- signal parked
- signal blocked
- sanitized signal submitted to Observatory
- Observatory normalization completed
- derived intelligence generated from signal

Rejected, parked, blocked, and revised signals remain auditable.

## Lifecycle Rules

Signals must obey workspace lifecycle status:

- `idea` workspaces cannot submit signals.
- `onboarding` workspaces should not submit operational signals.
- `manual_test` workspaces may create candidates and submit human-approved sanitized signals if configured.
- `active` workspaces may submit through configured sanitization gates.
- `paused` workspaces may not submit new signals.
- `retired` workspaces may not submit new signals.

If a workspace is paused after candidate creation, the candidate should not proceed to Observatory intake without explicit revalidation.

## Relationships To Other Records

Signals may reference:

- workspace config
- agent runs
- artifacts
- review queue items
- human decisions
- audit records
- external references
- Observatory query results
- normalized Observatory records
- derived intelligence records

Signals must not directly create cross-workspace reads.

## Forbidden Fields

Do not add fields such as:

```text
customer_name
customer_email
customer_phone
customer_address
customer_shop_url
full_customer_request
private_report_text
raw_customer_file
api_key
provider_token
oauth_refresh_token
payment_details
searchclarity_report_template
etsy_listing_payload
printify_product_payload
fiverr_message_text
custom_data
```

Use source references, workspace-owned records, bounded evidence summaries, and sanitized generalized summaries instead.

## Bounded Metadata

Do not use generic metadata as a place to hide private details or provider-specific payloads.

A future bounded metadata field must define:

- allowed keys
- value types
- owner
- whether it is queryable
- whether it is canonical meaning
- what must not be stored there

Until then, avoid generic `metadata` or `custom_data` fields.

## Example Raw Signal

```yaml
signal_id: sig_raw_001
signal_form: raw_signal
workspace_id: ws_internal_research_001
workspace_type: internal_research
status: draft
signal_type: research_finding
source_actor_type: human
source_actor_id: human_operator
source_references:
  - record_type: manual_note
    record_id: note_001
    relationship: source_observation
summary: Internal research observed repeated need for clearer schema ownership rules before DB planning.
evidence_summary: Based on planning notes and VEDA-inspired structural review.
sensitivity_rating: low
confidence: high
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
audit_record_id: audit_001
```

## Example Signal Candidate

```yaml
signal_id: sigcand_001
signal_form: signal_candidate
parent_signal_id: sig_raw_001
raw_signal_id: sig_raw_001
workspace_id: ws_internal_research_001
workspace_type: internal_research
status: candidate
signal_type: workflow_problem
source_actor_type: agent
source_actor_id: signal_capture_agent
source_references:
  - record_type: agent_run
    record_id: run_001
    relationship: created_candidate
summary: Early platform planning benefits from defining data ownership boundaries before schema design.
evidence_summary: Repeated planning docs and VEDA review showed that schema work depends on ownership clarity.
sensitivity_rating: low
confidence: high
private_data_removed: true
remaining_sensitivity_notes: No customer, credential, provider, or workspace-private business data included.
observatory_destination: normalized_signals
sanitization_review_item_id: rev_001
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
audit_record_id: audit_002
version: 1
```

## Example Sanitized Signal

```yaml
signal_id: sig_sanitized_001
signal_form: sanitized_signal
parent_signal_id: sigcand_001
raw_signal_id: sig_raw_001
workspace_id: ws_internal_research_001
workspace_type: internal_research
status: approved_sanitized
signal_type: workflow_problem
source_actor_type: human
source_actor_id: human_operator
source_references:
  - record_type: review_item
    record_id: rev_001
    relationship: sanitization_approval
  - record_type: audit_record
    record_id: audit_003
    relationship: approval_audit
summary: Platform schema planning should define data ownership before individual schemas are written.
evidence_summary: Multiple planning steps showed schema definitions depend on clear ownership and provenance boundaries.
sensitivity_rating: low
confidence: high
private_data_removed: true
sanitization_decision: approve
observatory_destination: normalized_signals
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
audit_record_id: audit_003
version: 1
```

## Validation Questions

Before accepting a signal record, answer:

1. Is the signal form valid?
2. Is the signal status valid for that form?
3. Is the workspace id valid when required?
4. Does workspace lifecycle allow this signal action?
5. Does workspace config allow Observatory submission if applicable?
6. Is the signal type business-neutral?
7. Are source references thin references rather than ownership transfers?
8. Does the signal avoid private payload dumps?
9. Does the signal avoid credentials and raw secrets?
10. Does the signal preserve provenance?
11. If Observatory-bound, has sanitization review approved it?
12. If derived, does it reference source signals?
13. Does it avoid provider-specific fields in core?
14. Does it avoid unbounded metadata/custom data?

## Non-Goals

This schema does not define:

- full Observatory record schema
- derived intelligence schema
- customer records
- artifact content
- provider payload schemas
- external integration behavior
- database tables
- scoring formula
- query API behavior
- UI display rules

## Final Rule

```text
A signal earns reach by passing sanitization.
```
