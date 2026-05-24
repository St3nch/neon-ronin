# ADR-004 - Observatory Shared Intelligence Boundary

## Status

Accepted

## Context

Neon Ronin will support multiple small-business workspaces over time.

Each workspace will have private data, private artifacts, private drafts, private customer or business context, and its own workflow history.

At the same time, workspaces should be able to benefit from generalized intelligence discovered across the system.

The Observatory is intended to be that shared intelligence layer.

This creates a structural risk:

```text
If the Observatory is too open, it becomes cross-workspace data leakage.
If the Observatory is too closed, it becomes useless duplication.
```

The project already defines that:

- workspaces are isolated by default
- the Observatory is business-neutral
- only sanitized signals may enter the Observatory
- private workspace data must not cross boundaries directly

However, Neon Ronin also needs explicit structural decisions for how many workspaces may submit to and query the Observatory without turning it into a shared private-data swamp.

## Decision

The Observatory is a shared, business-neutral intelligence layer built from sanitized, generalized signals.

It is not a shared workspace database.

It is not a backdoor into another workspace.

It is not a place for raw customer data, raw drafts, raw reports, credentials, private artifacts, or business-specific operating records.

Core rule:

```text
Workspaces contribute sanitized intelligence to the Observatory.
Workspaces query generalized intelligence from the Observatory.
Workspaces do not query each other.
```

## Structural Boundaries

### 1. Workspaces Own Private Data

Each workspace owns its private data, including:

- raw inputs
- customer data
- customer history
- private drafts
- private artifacts
- workspace-specific strategy
- credentials
- platform account details
- business-specific workflows
- delivery records
- exact report text
- marketplace listings or product drafts

This data stays in the workspace unless transformed into an approved sanitized signal.

### 2. The Observatory Owns Generalized Intelligence

The Observatory may own:

- sanitized signals
- normalized signal records
- keyword clusters
- market patterns
- trend profiles
- competitor-pattern summaries
- generalized recommendation patterns
- data quality notes
- opportunity scores
- strategy queue items
- research queue items

The Observatory should store patterns, not private operational records.

### 3. Sanitization Is The Only Ingestion Path

No workspace data may enter the Observatory directly.

Allowed path:

```text
workspace-private observation
-> raw signal inside workspace
-> signal candidate
-> sanitization gate
-> approved sanitized signal
-> Observatory inbox
-> normalized Observatory record
```

Forbidden paths:

```text
workspace artifact -> Observatory
workspace customer record -> Observatory
workspace draft -> Observatory
workspace database table -> Observatory
workspace credential -> Observatory
workspace report text -> Observatory
```

### 4. Observatory Queries Return Generalized Results

Workspace queries to the Observatory should return:

- summaries
- clusters
- scores
- generalized patterns
- data quality notes
- recommended research directions
- prior-signal existence checks

Workspace queries should not return:

- raw source signals
- source customer identity
- source workspace private data
- exact customer text
- exact private evidence
- credentials
- private artifacts
- source workspace operational records

### 5. Source Provenance Exists But Is Restricted

The system may keep source provenance for audit, debugging, deduplication, and quality control.

Provenance may include internal references such as:

- source workspace id
- source workspace type
- source artifact id
- source run id
- sanitization review id
- audit record id

Normal Observatory query results must not expose source workspace id or source artifact id unless explicitly allowed by a future permission rule.

The default query surface should expose source context only at generalized levels, such as:

- workspace type
- signal category
- approximate time period
- evidence count
- confidence band

### 6. Query Access Is Permissioned

A workspace may query the Observatory only if its workspace config allows it.

Required setting:

```yaml
observatory:
  can_query: true
```

A workspace may submit sanitized signals only if its workspace config allows it.

Required setting:

```yaml
observatory:
  can_submit_sanitized_signals: true
```

These are separate permissions.

A workspace may be allowed to query the Observatory without being allowed to submit signals, or allowed to submit signals without being allowed to query.

### 7. No Direct Cross-Workspace Reads

The Observatory does not allow workspace A to read workspace B.

Forbidden:

```text
Workspace A -> Workspace B private data
Workspace A -> Workspace B artifacts
Workspace A -> Workspace B customer history
Workspace A -> Workspace B drafts
Workspace A -> Workspace B credentials
```

Allowed:

```text
Workspace A -> Observatory generalized query result
Workspace B -> Observatory sanitized signal submission
```

### 8. Scoring Must Be Generic And Pluggable

The Observatory may produce opportunity scores or confidence scores.

Core must define the scoring contract, not one business-specific scoring algorithm.

A scoring model may consider:

- evidence quality
- signal recurrence
- signal freshness
- relevance to workspace type
- risk level
- opportunity strength
- strategic value

But a concrete business-specific scoring formula must not become core doctrine unless accepted through a core doc or ADR.

### 9. Derived Records Are Separate From Raw Signals

The Observatory may generate derived records from sanitized signals, such as:

- keyword clusters
- trend profiles
- opportunity scores
- strategy queue items
- data quality summaries

Derived records should preserve traceability to source sanitized signals internally, but should not expose private source details through normal queries.

### 10. Query Results Must Be Auditable

Every Observatory query should be auditable.

Audit records should capture:

- requesting workspace id
- requesting actor id
- query type
- query timestamp
- result type
- result count or summary
- whether restricted records were filtered
- linked workflow or agent run if applicable

This is necessary because Observatory outputs can influence business decisions.

## Observatory Data Zones

The Observatory should be conceptually divided into zones.

| Zone | Purpose | Access |
|---|---|---|
| Inbox | Approved sanitized signals waiting for normalization | Observatory process only |
| Normalized Signals | Structured sanitized signal records | Restricted internal use |
| Derived Intelligence | Clusters, scores, patterns, summaries | Queryable by permitted workspaces |
| Strategy Queues | Recommended research or action queues | Queryable according to workspace permissions |
| Audit Trail | Ingestion, query, scoring, and review records | Operator/admin/audit use |

This does not require separate databases yet.

It is a structural boundary that future schemas and storage design must respect.

## Minimum Query Types

Initial Observatory query types should remain narrow:

| Query Type | Returns | Must Not Return |
|---|---|---|
| `keyword_cluster` | related terms or themes | source customer data |
| `trend_profile` | generalized trend or seasonality notes | raw source records |
| `competitor_pattern` | generalized market weaknesses or patterns | exact private competitor/customer context |
| `opportunity_score` | score plus explanation and confidence | business-specific private formula unless approved |
| `prior_signal_check` | whether similar sanitized signals exist | raw matching signals by default |
| `data_quality_check` | evidence strength and caveats | private evidence |

## Re-Identification Guardrail

Even sanitized and derived data can become unsafe if it is too specific.

The Observatory should avoid returning results that could allow a workspace to infer another workspace's private customer, source event, or strategy.

High-risk query results should be:

- generalized further
- withheld
- parked for review
- returned only with lower specificity
- returned only after human approval if required

## Early Implementation Constraint

During early development, the Observatory should start simple.

Allowed early:

- manual sanitized signal intake
- human-approved signal submission
- simple normalized signal records
- simple prior-signal checks
- simple keyword or pattern summaries
- audit records for ingestion and query

Forbidden early:

- automatic cross-workspace learning without review
- raw signal search across workspaces
- source workspace exposure in query results
- automatic scoring that drives external action
- direct workspace-to-workspace reads
- external writes triggered by Observatory output

## Relationship To Sanitization

This ADR depends on `docs/core/08-sanitization.md`.

Sanitization defines what may enter the Observatory.

This ADR defines how the Observatory behaves once many workspaces submit and query generalized intelligence.

## Relationship To Future Schemas

Future schemas must support these boundaries.

Expected schema implications:

- workspace config must define Observatory query and submission permissions
- signal schema must distinguish raw signal, signal candidate, sanitized signal, and derived records
- audit schema must record Observatory ingestion and query events
- permission schema must control query access and source-provenance visibility
- scoring schema must separate generic score contract from business-specific scoring models

## Consequences

- Workspaces can learn from shared intelligence without directly seeing each other.
- The Observatory remains useful without becoming a private-data dump.
- Sanitized signals become the only cross-workspace contribution path.
- Query results must be designed as products of generalized intelligence, not raw data exports.
- Future database planning must preserve these boundaries.
- Future scoring models must remain configurable and generic unless promoted through ADR/core docs.

## Final Rule

```text
The Observatory is shared intelligence, not shared private memory.
```
