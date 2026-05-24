# 13 - Provenance And Evidence

## Purpose

This document defines how Neon Ronin preserves provenance, evidence, source context, derivation boundaries, and uncertainty across workspaces, agents, artifacts, signals, review items, Observatory records, and audit logs.

It exists to answer:

```text
Where did this record come from, what supports it, who or what created it, and is it raw, structured, sanitized, normalized, derived, reviewed, or approved?
```

Without provenance, Neon Ronin cannot be trusted.

## Core Rule

```text
Important records must remain traceable to their source context.
```

A record that influences a workflow, review decision, signal, score, recommendation, external action, or human decision must preserve enough provenance to be reviewed later.

## Why Provenance Matters

Neon Ronin will use agents to draft, summarize, transform, score, and recommend.

Those actions can make information look cleaner and more confident than the underlying evidence deserves.

Provenance prevents that.

Provenance makes it possible to answer:

- what is this record?
- where did it come from?
- who or what created it?
- when was it created or captured?
- what workspace does it belong to?
- what evidence supports it?
- what transformations were applied?
- what review gates touched it?
- what was approved, rejected, revised, or parked?
- what uncertainty remains?

## Terms

| Term | Meaning |
|---|---|
| Evidence | Source material or record that supports later work, interpretation, review, or decision |
| Provenance | Traceable context describing origin, scope, actor, time, source, and transformation history |
| Source Context | The workspace, artifact, run, human, agent, integration, or external source that produced or introduced a record |
| Raw Record | Unprocessed input or observation retained in its original or closest available form |
| Structured Record | A record extracted or organized from raw input into defined fields |
| Sanitized Record | A record with private or identifying details removed or generalized |
| Normalized Record | A record converted into a standard Observatory or platform format |
| Derived Record | A record computed, summarized, scored, or interpreted from source records |
| Reviewed Record | A record that has passed through a human review gate |
| Approved Record | A reviewed record that has received approval for its intended next step |

## Representation Levels

Neon Ronin must preserve the distinction between levels of representation.

```text
raw data
-> structured record
-> sanitized record
-> normalized record
-> derived output
-> human decision or action
```

Each level has a different trust posture.

A later level must not erase the existence or importance of earlier levels.

## Level Definitions

### Raw Data

Raw data is the closest available form of the original input or observation.

Examples:

- customer request text
- uploaded file
- manually entered business idea
- external API payload
- local note
- raw workspace observation
- source screenshot metadata

Raw data is usually workspace-owned or integration-owned.

Raw private data must not enter the Observatory.

### Structured Record

A structured record organizes raw data into defined fields.

Examples:

- intake record extracted from a customer request
- agent run record
- review queue item
- artifact metadata
- external reference record

Structured records must preserve references back to the raw or source context where practical.

### Sanitized Record

A sanitized record has private, identifying, confidential, or business-specific details removed or generalized.

Examples:

- signal candidate after sensitive details are removed
- approved sanitized signal
- generalized market observation

Sanitized records must preserve internal provenance while hiding private details from normal query surfaces.

### Normalized Record

A normalized record is converted into a standard platform or Observatory shape.

Examples:

- normalized Observatory signal
- normalized artifact metadata
- normalized external reference

Normalization must not silently upgrade uncertain or weak evidence into strong evidence.

### Derived Output

A derived output is created by analyzing, summarizing, scoring, clustering, transforming, or interpreting source records.

Examples:

- opportunity score
- research packet
- QA summary
- strategy recommendation
- keyword cluster
- trend profile
- workspace health score
- agent confidence label

Derived outputs must be labeled as derived and must preserve provenance to source records.

### Human Decision Or Action

A human decision or action is a review outcome, approval, rejection, revision, escalation, parking decision, publish approval, delivery approval, or other human-controlled decision.

Human decisions must record what was reviewed and what was decided.

## Minimum Provenance Fields

Every important record should preserve enough context to answer the provenance questions.

At minimum, important records should include or reference:

- record id
- record type
- ownership category
- workspace id if workspace-scoped
- source actor type
- source actor id
- created timestamp
- source record references where applicable
- source artifact references where applicable
- source run references where applicable
- source review item references where applicable
- transformation level
- derivation status
- confidence or uncertainty where applicable
- audit record reference

Exact field names will be defined in schema docs.

This document defines the required posture.

## Actor Provenance

Records should distinguish who or what created or changed them.

Actor types may include:

- human
- agent
- system
- integration
- external provider
- scheduled job
- imported file

Actor identity should be specific enough for audit.

Examples:

```text
human:operator
agent:trend_research_agent
system:observatory_normalizer
integration:etsy
external_provider:anthropic
```

## Workspace Provenance

Workspace-scoped records must preserve their workspace context.

A workspace-scoped record should not become global merely because another component reads it.

Examples:

- a workspace artifact remains workspace-owned
- a workspace customer request remains workspace-owned
- a workspace signal candidate remains workspace-owned until approved as sanitized
- a sanitized signal may enter Observatory ownership while keeping restricted internal source provenance

## Source Reference Rules

Source references should be thin and purposeful.

A record may reference another record without owning or copying it.

Examples:

- review item references artifact metadata
- audit record references agent run
- sanitized signal references source signal candidate
- derived opportunity score references sanitized signals
- workspace decision references Observatory query result

References must not become secret ownership transfers.

```text
A reference is a pointer, not a takeover.
```

## Evidence Preservation Rule

Neon Ronin should preserve enough evidence context that later review remains possible.

This means:

- source records should remain distinguishable from summaries
- raw inputs should remain distinguishable from extracted fields
- sanitized records should remain distinguishable from raw records
- derived outputs should remain distinguishable from source records
- review decisions should remain distinguishable from recommendations

Convenience summaries must not make the source disappear.

## Derivation Honesty Rule

Derived records must clearly state that they are derived.

Derived records should preserve:

- source record references
- derivation method or process
- generated timestamp
- generating actor or process
- confidence or uncertainty
- limitations or caveats where applicable

A derived record must not pretend to be raw evidence.

## Confidence And Uncertainty

Agent and system outputs should not erase uncertainty.

Where useful, records should capture:

- confidence level
- evidence strength
- known limitations
- missing data
- unresolved questions
- quality warnings

Recommended simple confidence labels:

| Label | Meaning |
|---|---|
| low | Weak evidence, high uncertainty, or speculative output |
| medium | Some supporting evidence but notable caveats |
| high | Strong supporting evidence and few caveats |
| unknown | Confidence not assessed |

Confidence is not approval.

## Review Provenance

Review decisions must preserve what was reviewed and what was decided.

A review decision should reference:

- review item id
- reviewer actor id
- reviewed artifact or signal id
- decision
- timestamp
- decision notes
- fields changed if approved with changes
- linked audit record

Review provenance is required because a human decision may change the status, safety, or external readiness of a record.

## Signal Provenance

Signals must preserve source continuity across their lifecycle.

Signal lifecycle provenance should connect:

```text
raw signal
-> signal candidate
-> sanitization review
-> sanitized signal
-> normalized Observatory record
-> derived intelligence
-> query result or strategy queue item
```

Normal query surfaces should not expose private source details.

Internal provenance should remain available for audit and debugging.

## Artifact Provenance

Artifacts should preserve origin and transformation context.

Artifact provenance should answer:

- which workspace owns this artifact?
- who or what created it?
- what workflow produced it?
- what agent run or human action created it?
- what inputs informed it?
- what review gates touched it?
- is it draft, reviewed, approved, delivered, archived, or rejected?

An artifact draft is not a final deliverable.

## Agent Run Provenance

Agent runs must be traceable.

Agent run provenance should include:

- run id
- workspace id
- agent id
- triggering actor
- trigger type
- runtime mode
- input references
- output references
- model or provider reference if applicable
- tool or integration references if applicable
- start timestamp
- end timestamp
- result status
- linked audit records

Agent runs that create review items, artifacts, signals, or external action requests must link to those outputs.

## Observatory Provenance

The Observatory may store restricted internal provenance for audit and quality control.

This may include:

- source workspace id
- source workspace type
- source signal candidate id
- sanitization review id
- source artifact id
- source run id
- normalization process
- derived output references

Normal Observatory query responses should expose generalized provenance only, such as:

- workspace type
- signal category
- approximate time period
- evidence count
- confidence band
- data quality note

## External Integration Provenance

External integration records must preserve provider context without leaking provider-specific assumptions into core schemas.

External integration provenance may include:

- provider name
- provider resource type
- provider resource id
- request id
- response status
- timestamp
- workspace id
- triggering actor or run
- linked review item if applicable
- audit record reference

Credentials and raw secrets must never be treated as normal evidence.

Credential handling belongs to the future secrets and credentials doc.

## Audit Provenance

Audit records are themselves provenance infrastructure.

They should preserve meaningful state changes and link to the affected records.

Audit records should not be rewritten to make history cleaner.

Rejected, failed, parked, blocked, or revised actions remain part of the evidence trail.

## Provenance Gaps

Sometimes provenance will be incomplete.

Incomplete provenance must be marked, not hidden.

Examples:

- imported file with unknown original source
- copied note from an old system
- manual observation without source artifact
- external provider response missing expected metadata
- agent output generated from incomplete inputs

A provenance gap should lower confidence or require review.

Do not normalize incomplete provenance into complete-looking records.

## Provenance Failure Examples

Bad patterns:

```text
Agent says this niche is promising, but no source signals are linked.
```

```text
A review item exists, but no artifact or run is linked.
```

```text
A sanitized signal is in the Observatory, but no sanitization decision is linked.
```

```text
A score exists, but source signals are not referenced.
```

```text
A customer-facing deliverable is marked approved, but no human decision record exists.
```

These are provenance failures.

## Human-In-The-Loop Rule

Human review does not erase provenance requirements.

Human approval should add provenance, not replace it.

A human may approve a derived recommendation, but the recommendation should still trace to its supporting records.

## LLM Use Rule

LLMs working in Neon Ronin must preserve provenance in their outputs when making recommendations, summaries, classifications, or schema proposals.

LLM-generated content should identify:

- source docs or records used
- assumptions made
- uncertainty or gaps
- whether the output is a summary, recommendation, schema proposal, or decision support artifact

An LLM summary is not canonical unless promoted through the appropriate doc, schema, review, or ADR path.

## Early Implementation Rule

Before code, Neon Ronin docs and schemas should assume provenance is required even if the exact storage model is not yet chosen.

During schema design, every schema should define:

- ownership category
- provenance fields
- source references
- audit relationship
- derivation status if applicable
- confidence or uncertainty field if applicable

## Relationship To Other Docs

This document depends on:

- `docs/core/07-permissions-and-audit.md`
- `docs/core/08-sanitization.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/decisions/adr-004-observatory-shared-intelligence-boundary.md`

This document informs:

- `docs/core/14-schema-authority.md`
- `docs/core/glossary.md`
- future schema docs under `docs/core/schemas/`
- future operations docs
- future database planning

## Final Rule

```text
If a record cannot explain where it came from, do not trust it as decision-grade evidence.
```
