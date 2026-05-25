# Schema Change Checklist

## Purpose

This checklist defines how Neon Ronin changes schemas, schema-like contracts, and implementation-facing planning records without creating drift, hidden breaking changes, or business-specific core contamination.

It exists because schema changes are architecture changes.

## Core Rule

```text
No schema change without ownership, purpose, provenance, and boundary review.
```

A schema change must not be made only because one workspace, provider, report, marketplace, or agent happens to need a field.

## Applies To

Use this checklist before changing:

- `docs/core/schemas/*.schema.md`
- schema authority docs
- data boundary docs
- provenance/evidence docs
- workspace lifecycle docs
- review/audit/permission contracts
- future database schemas
- future API contracts
- future validation models
- future migration files

## Required References

Before changing a schema, review:

- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/14-schema-authority.md`
- `docs/core/glossary.md`
- `docs/core/16-error-and-failure-handling.md`
- relevant schema file
- relevant ADRs

## Change Header

```yaml
schema_change_id:
proposed_at:
proposed_by:
affected_schema:
change_type: add_field | remove_field | rename_field | change_status | change_transition | add_schema | deprecate_schema | clarify_text | other
status: proposed | accepted | rejected | parked | implemented | superseded
```

## Step 1 - Define The Change

What is changing?

```text
Proposed change:
```

Why is it needed?

```text
Reason:
```

What problem does it solve?

```text
Problem solved:
```

If the answer is vague, stop.

## Step 2 - Identify Source Pressure

What triggered the change?

- [ ] core platform need
- [ ] adapter pattern need
- [ ] workspace-specific need
- [ ] integration-specific need
- [ ] Observatory need
- [ ] SearchClarity readiness finding
- [ ] Internal Research manual-test finding
- [ ] implementation discovery
- [ ] bug/failure/incident
- [ ] other

Notes:

```text
Source pressure notes:
```

## Step 3 - Classify Ownership

Classify the proposed change:

- [ ] core-owned data
- [ ] workspace-owned data
- [ ] adapter-owned pattern
- [ ] integration-owned record
- [ ] Observatory-owned data
- [ ] derived data
- [ ] referenced-only data
- [ ] forbidden-in-core data
- [ ] deferred domain

If ownership is unclear, park the change.

## Step 4 - Check Core Contamination

Does the proposed change include:

- [ ] business-specific naming
- [ ] SearchClarity-specific field
- [ ] Etsy/Fiverr/Printify/provider-specific field
- [ ] report-template-specific field
- [ ] customer-specific field
- [ ] credential or secret field
- [ ] raw provider payload field
- [ ] unbounded metadata/custom data
- [ ] raw private data field

If yes, reject or move to workspace/integration-owned boundary unless a core abstraction is justified.

## Step 5 - Reusability Test

Answer:

1. Would at least two different workspace types plausibly use this concept?
2. Is the concept business-neutral?
3. Can it be named without provider/workspace-specific language?
4. Does it preserve ownership boundaries?
5. Does it avoid unbounded JSON sludge?
6. Does it fit existing schema family ownership?

Decision:

```text
Reusable core | Adapter pattern | Workspace-specific | Integration-specific | Park | Reject
```

## Step 6 - Field-Level Review

For each new or changed field:

| Field | Purpose | Owner | Type | Required? | System-Owned? | Immutable? | Notes |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

Each field must have:

- [ ] clear purpose
- [ ] clear owner
- [ ] clear type
- [ ] clear required/optional status
- [ ] clear system-owned/human-owned/source-owned status
- [ ] clear immutability expectation
- [ ] clear non-goal if drift-prone

No field without purpose.

## Step 7 - Status And Transition Review

If statuses or transitions change:

- [ ] status names are canonical and business-neutral
- [ ] transitions are explicit
- [ ] terminal statuses are clear
- [ ] blocked/failed/rejected/parked states are not collapsed incorrectly
- [ ] lifecycle rules are preserved
- [ ] human decision requirements are preserved
- [ ] audit requirements are updated

Do not add casual ambiguous states like:

```text
maybe
sorta_done
good_enough
readyish
```

## Step 8 - Provenance Review

Does the change preserve or improve provenance?

- [ ] source actor remains traceable
- [ ] source records remain referenced
- [ ] derived data remains labeled
- [ ] human decisions remain linked
- [ ] audit records remain linked
- [ ] external references remain references
- [ ] private source details are not exposed through normal query surfaces

If provenance weakens, reject or revise.

## Step 9 - Review Gate Impact

Does the change affect review gates?

- [ ] quality gate
- [ ] publish gate
- [ ] paid action gate
- [ ] data privacy gate
- [ ] customer delivery gate
- [ ] rights and compliance gate
- [ ] signal sanitization gate
- [ ] strategy review gate
- [ ] external write gate
- [ ] credential permission gate

If yes:

- [ ] review queue schema/runbook still works
- [ ] human decision schema still works
- [ ] audit requirements updated
- [ ] no self-approval path introduced

## Step 10 - Permission And Secrets Review

Confirm:

- [ ] no raw secret fields added
- [ ] credential references only
- [ ] permission scope remains bounded
- [ ] no lifecycle bypass
- [ ] no review-gate bypass
- [ ] no emergency-stop bypass
- [ ] denied actions still win over allowed actions

If secrets are involved, follow `docs/core/15-secrets-and-credentials.md`.

## Step 11 - Observatory Review

If the change affects signals, scoring, or Observatory:

- [ ] raw workspace data remains workspace-owned
- [ ] signal candidates still require review
- [ ] sanitized signals are clearly separated
- [ ] normal query surfaces hide private source details
- [ ] scores remain decision support only
- [ ] provenance/data quality remains visible

If raw data could enter Observatory, reject the change.

## Step 12 - External Integration Review

If the change affects external systems:

- [ ] provider-specific fields stay out of generic core schema
- [ ] external references are used
- [ ] credentials are references only
- [ ] live writes require human approval
- [ ] destructive actions require human approval
- [ ] unknown external outcomes are handled
- [ ] integration remains deferred if not promoted

If provider capability becomes Neon Ronin permission, reject the change.

## Step 13 - Backward Compatibility Review

For future implementation schemas, ask:

- [ ] Does this break existing records?
- [ ] Is a migration needed?
- [ ] Are old records still readable?
- [ ] Does validation need updating?
- [ ] Are examples updated?
- [ ] Are operations docs updated?
- [ ] Is an ADR needed?

Current planning docs may not need migrations yet, but compatibility thinking starts now.

## Step 14 - Documentation Update Checklist

If accepted, update as needed:

- [ ] affected schema doc
- [ ] `docs/core/glossary.md`
- [ ] `docs/core/14-schema-authority.md`
- [ ] data boundary docs
- [ ] provenance/evidence docs
- [ ] review queue runbook
- [ ] onboarding checklist
- [ ] manual-test template
- [ ] roadmap
- [ ] ADRs

## Step 15 - ADR Decision

Create an ADR if the change:

- changes platform authority
- changes workspace isolation
- changes Observatory boundary
- changes review/human decision model
- changes permission model
- promotes deferred domain
- introduces external integration authority
- changes lifecycle model
- changes core ownership assumptions

ADR needed?

```text
Yes | No
```

Proposed ADR title:

```text
Title:
```

## Step 16 - Decision

Decision:

- [ ] accept
- [ ] accept with changes
- [ ] request revision
- [ ] reject
- [ ] park
- [ ] escalate to ADR

Decision summary:

```text
Summary:
```

Required records:

- [ ] human decision record
- [ ] audit record
- [ ] decision log entry if strategically important
- [ ] ADR if required

## Step 17 - Implementation Notes

If implementing the change:

- [ ] make smallest safe change
- [ ] update examples
- [ ] update validation questions
- [ ] update forbidden fields if needed
- [ ] preserve final rule
- [ ] run manual review
- [ ] commit separately where practical

## Common Rejection Reasons

Reject schema changes when:

- field is business-specific
- field is provider-specific in core
- field stores a secret
- field stores raw private data in core
- field duplicates existing concept
- purpose is unclear
- owner is unclear
- provenance is weakened
- review gate is bypassed
- permission boundary is bypassed
- unbounded metadata is used as hidden schema
- deferred domain is promoted accidentally
- SearchClarity need is not yet proven reusable

## SearchClarity Reminder

SearchClarity may reveal useful requirements.

But SearchClarity-specific details must not enter core schemas unless extracted as reusable capabilities.

Examples:

| SearchClarity Need | Likely Classification |
|---|---|
| report artifact | reusable artifact concept |
| customer delivery review | reusable review gate |
| Fiverr gig copy | workspace-owned artifact |
| Etsy audit report template | workspace-owned or adapter pattern after extraction |
| raw market signal | workspace-owned signal source |
| pricing | workspace-owned business detail |
| customer order tracker | workspace-owned operational data |

## Final Rule

```text
A schema change is not small if it changes ownership, authority, or trust.
```
