# 17 - Observatory Scoring Contract

## Purpose

This document defines how Neon Ronin's Observatory may score, rank, cluster, compare, and summarize sanitized cross-workspace intelligence.

It exists to answer:

```text
What may the Observatory score, what evidence may it use, how must scores explain themselves, and what must a score never be allowed to do?
```

The Observatory is allowed to support decisions.

The Observatory is not allowed to make decisions.

## Core Rule

```text
A score is decision support.
A score is not a decision.
```

Scores, rankings, clusters, and recommendations must remain derived intelligence.

They must not become approval, publishing authority, spending authority, customer delivery authority, credential authority, or external action authority.

## Scope

This contract applies to Observatory outputs such as:

- opportunity scores
- trend scores
- confidence scores
- data quality scores
- keyword clusters
- niche clusters
- prior signal checks
- competitor pattern summaries
- market gap summaries
- strategy queue suggestions
- research queue suggestions
- generalized recommendations

This contract does not define a final scoring formula.

It defines the rules any future formula must obey.

## Observatory Input Boundary

The Observatory may score only approved data that is eligible for shared intelligence.

Allowed input types:

- approved sanitized signals
- normalized Observatory records
- generalized signal aggregates
- prior derived intelligence with provenance
- approved public/reference data later
- data quality notes

Forbidden input types:

- raw workspace data
- raw customer data
- private workspace artifacts
- customer records
- credentials
- raw external provider payloads
- unreviewed signal candidates
- private drafts
- workspace-specific strategy unless explicitly generalized and approved

The Observatory must not score private workspace data directly.

## Derived Intelligence Rule

Every Observatory score is derived.

Derived scoring outputs must preserve:

- source signal references or aggregate references
- scoring method or scoring version
- scoring timestamp
- evidence count
- evidence quality notes
- confidence or uncertainty
- known limitations
- generated actor/process
- audit record reference where meaningful

A score without provenance is not decision-grade.

## Minimum Score Explanation

Any meaningful score should be explainable in plain language.

A score result should answer:

- what was scored?
- why was it scored?
- what source evidence contributed?
- how much evidence exists?
- how fresh is the evidence?
- how diverse is the evidence?
- what lowered confidence?
- what should a human review next?
- what the score does not prove?

## Score Types

Initial score types:

```text
opportunity_score
trend_score
confidence_score
data_quality_score
fit_score
risk_score
novelty_score
repeat_signal_score
priority_score
```

Score types may expand later through schema authority.

Do not create business-specific score types in core when a generic score plus workspace context is sufficient.

## Score Scale

Early Neon Ronin should prefer simple bounded score scales.

Recommended numeric scale:

```text
0.0 to 1.0
```

Recommended label scale:

```text
low
medium
high
unknown
```

Numeric scores should not be presented without labels, explanation, and caveats.

A score of `0.82` without explanation is not useful.

## Confidence Labels

Canonical confidence labels:

```text
low
medium
high
unknown
```

Confidence describes trust in the score based on evidence.

Confidence is not approval.

Confidence should decrease when:

- evidence is sparse
- evidence is stale
- evidence comes from one source only
- source provenance is weak
- signals conflict
- signals are too generalized
- data quality warnings exist
- scoring method is experimental

## Evidence Strength

Evidence strength should consider:

- count of supporting signals
- diversity of source workspace types
- recency of observations
- consistency across signals
- strength of provenance
- sensitivity/sanitization confidence
- whether sources are independent
- whether data quality warnings exist

Evidence strength should be visible in score summaries.

## Data Quality Notes

Scoring outputs should include data quality notes when relevant.

Examples:

```text
low evidence count
single-source pattern
stale signals
conflicting signals
highly generalized source data
missing comparison baseline
experimental scoring method
```

Data quality warnings must not be hidden because a score looks attractive.

## Recency Rules

Scores should account for signal freshness when relevant.

A fresh weak signal should not automatically beat older strong evidence.

An old strong pattern should not automatically remain relevant forever.

Scoring should preserve enough timing context for a human to understand freshness.

## Source Diversity Rules

The Observatory should distinguish between:

- many signals from one workspace
- similar signals from multiple workspaces
- similar signals from multiple workspace types
- signals from public/reference data only
- signals from weak or unknown provenance

Cross-workspace diversity may increase confidence only when privacy boundaries are preserved.

Normal query surfaces must not expose private source workspace details.

## Normal Query Surface Rules

Score outputs may expose generalized source context, such as:

- signal category
- workspace type
- approximate time period
- evidence count
- confidence band
- data quality note
- generalized reason

Score outputs must not expose:

- source customer identity
- raw signal text
- raw artifacts
- private workspace data
- exact customer text
- source workspace private strategy
- credentials
- exact provider payloads

## Score Output Shape

A future scoring output should conceptually include:

```yaml
score_id: score_001
score_type: opportunity_score
subject_type: keyword_cluster
subject_label: handmade soy candle wedding favors
score_value: 0.74
score_label: high
confidence: medium
evidence_count: 12
evidence_window: last_90_days
source_context:
  workspace_types:
    - marketplace_store
    - service
  signal_types:
    - keyword_pattern
    - customer_need_pattern
data_quality_notes:
  - Evidence is strongest in marketplace-style signals.
  - Few service-business signals support this pattern.
explanation: Multiple sanitized signals suggest recurring demand and keyword gaps, but source diversity is moderate.
recommended_next_step: Human review should decide whether to create a research packet.
derived_from:
  - obs_signal_group_001
scoring_method_version: observatory_scoring_v0
created_at: 2026-05-24T00:00:00Z
```

This is a conceptual shape, not a final schema.

## Ranking Rules

Rankings must preserve score explanations.

A ranked list should not show only order.

It should show:

- score label
- confidence
- evidence count
- data quality warning if any
- reason for ranking
- next human review step

A rank is not a decision.

## Clustering Rules

Clusters must remain explainable.

A cluster should preserve:

- cluster label
- included generalized signals or aggregate references
- similarity basis
- evidence count
- confidence
- data quality notes
- scoring method/version if scored

Clusters must not expose raw private evidence.

## Opportunity Score Rules

Opportunity scores may estimate whether something deserves attention.

Opportunity scores should consider:

- demand signal strength
- repeated observations
- source diversity
- recency
- competition or saturation notes where available
- operational fit if known
- risk notes
- confidence
- data quality warnings

Opportunity scores must not automatically create a workspace, publish content, spend money, message customers, or execute external actions.

## Risk Score Rules

Risk scores may flag privacy, compliance, IP, rights, operational, credential, external-action, or business-risk concerns.

Risk scores should increase review strictness.

Risk scores should not automatically reject work unless a separate rule or hard-no invariant applies.

High risk should usually create or update a review item.

## Fit Score Rules

Fit scores may estimate how well an opportunity matches a workspace type, adapter, agent capability, or current roadmap phase.

Fit scores must not override roadmap boundaries.

A high fit score does not promote a deferred domain.

A high fit score does not allow specific-business needs to enter core.

## Priority Score Rules

Priority scores may suggest which item a human should review first.

Priority scores must not reorder risky work in a way that bypasses required review gates.

Priority should consider urgency, evidence strength, risk, dependencies, and lifecycle status.

## Scoring Method Version

Every score should reference a scoring method/version.

The scoring method/version should explain:

- input types used
- weighting assumptions
- freshness handling
- confidence handling
- data quality handling
- known limitations

Changing scoring method should not silently rewrite old scores.

New scoring methods should create new derived outputs or preserve method version history.

## Human Review Rule

Scores can recommend review.

Scores cannot perform review.

A score may create a review queue item only if a workflow/agent is allowed to queue review items.

The human decision remains separate.

Examples:

```text
Score suggests: review this opportunity.
Human decides: approve research packet.
```

```text
Score suggests: high risk.
Human decides: reject, revise, park, or escalate.
```

## Automation Boundary

Scores must not trigger automation directly.

Forbidden:

- score automatically publishes
- score automatically spends money
- score automatically messages customer
- score automatically changes credential scope
- score automatically creates external listing
- score automatically submits raw signal to Observatory
- score automatically promotes workspace to active

Allowed later, if governed:

- score creates a review suggestion
- score adds item to research queue
- score informs human decision
- score updates a derived intelligence record
- score flags data quality issues

## Audit Requirements

Meaningful scoring events should generate audit records when they affect workflow state.

Audit when:

- score generated for a queued decision
- score changes strategy/research queue status
- high-risk score triggers review item
- scoring method changes
- score is used in human decision context
- score generation fails
- score output is blocked due to missing provenance

Audit records should reference score outputs and source aggregates, not raw private data.

## Failure Rules

Scoring should fail or block when:

- source provenance is missing
- input contains raw private data
- input contains credentials
- signal candidate is unapproved
- Observatory permission is missing
- scoring method is unknown
- source references are unavailable
- data quality is too poor for meaningful output

Failure should follow `docs/core/16-error-and-failure-handling.md`.

A failed score must not become a score of zero unless the method explicitly means zero.

Unknown is not zero.

Blocked is not low.

Rejected is not low.

## Score Visibility Rules

Score visibility should depend on permission scope and workspace relationship.

A workspace may see generalized Observatory score outputs if allowed.

A workspace must not see private details from another workspace through score explanations.

High-sensitivity scoring outputs may require stricter review or limited display.

## Future Service Workspace Boundary Example

A future service workspace may capture raw market observations during paid or manual service work.

Those observations may later become sanitized signals.

The Observatory may score generalized patterns derived from those sanitized signals.

The service workspace must not directly define the scoring formula.

Workspace-specific customer reports, customer history, service-platform copy, pricing, and report language remain workspace-owned.

Reusable lesson:

```text
A workspace may contribute sanitized evidence.
Neon Ronin may derive generalized intelligence.
A human decides what to do next.
```

## Forbidden Score Uses

Do not use scores as:

- approval
- proof
- truth
- publish permission
- customer delivery permission
- spending permission
- credential permission
- workspace promotion permission
- replacement for human review
- replacement for source evidence
- excuse to skip provenance
- reason to expose private data

## Example Good Score Summary

```text
Opportunity score: high
Confidence: medium
Evidence count: 12 sanitized signals over 90 days
Data quality: moderate source diversity, no raw customer data exposed
Reason: Multiple generalized signals suggest recurring demand and keyword gaps.
Next step: Human review should decide whether to create a research packet.
```

## Example Bad Score Summary

```text
Score: 92
Do this now.
```

Bad because it lacks provenance, confidence, data quality, limitations, and human review boundary.

## Relationship To Other Docs

This document depends on:

- `docs/core/04-observatory.md`
- `docs/core/08-sanitization.md`
- `docs/core/11-data-boundaries.md`
- `docs/core/12-system-invariants.md`
- `docs/core/13-provenance-and-evidence.md`
- `docs/core/16-error-and-failure-handling.md`
- `docs/core/schemas/signal.schema.md`
- `docs/core/schemas/review-queue-item.schema.md`
- `docs/core/schemas/human-decision.schema.md`
- `docs/decisions/adr-004-observatory-shared-intelligence-boundary.md`

This document informs:

- future Observatory record schemas
- future derived intelligence schemas
- future strategy queue docs
- future research queue docs
- future agent scoring behavior
- future UI display of scores

## Non-Goals

This document does not define:

- final scoring formula
- database tables
- machine learning model selection
- embedding/vector database design
- UI ranking display
- complete Observatory query API
- marketplace research automation
- specific-business scoring logic

## Final Rule

```text
Scores recommend attention; humans decide action.
```
