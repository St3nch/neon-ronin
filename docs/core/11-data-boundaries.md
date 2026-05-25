# 11 - Data Boundaries

## Purpose

This document defines Neon Ronin's data ownership boundaries before schema design begins.

It exists to answer:

```text
What data does Neon Ronin core own, what data belongs to workspaces, what data belongs to the Observatory, what data may only be referenced, and what must never become core platform data?
```

Neon Ronin must support many future workspaces without turning the core platform into one business's private database.

## Core Rule

```text
Every durable record must have a clear owner.
If ownership is unclear, the schema is not ready.
```

A cleaner dashboard, easier query, or faster implementation is not a valid reason to erase ownership boundaries.

## Boundary Categories

Every proposed data class must be classified into one of these categories before it becomes a schema, table, document family, or durable record.

| Category | Meaning |
|---|---|
| Core-Owned Data | Business-neutral platform records Neon Ronin owns directly |
| Workspace-Owned Data | Private records owned by one workspace |
| Observatory-Owned Data | Sanitized shared intelligence owned by the Observatory |
| Adapter-Owned Pattern | Business-type workflow pattern, not one workspace's private data |
| Integration-Owned Record | External-service-specific connection, token, payload, or platform reference |
| Referenced-Only Data | Data Neon Ronin may point to without owning or copying as canonical truth |
| Derived Data | Data computed from other records and labeled as derived |
| Forbidden-In-Core Data | Data that must not become core platform data |

## Core-Owned Data

Core-owned data belongs to Neon Ronin as a business-neutral platform.

Core may own records such as:

- workspace registry records
- workspace lifecycle records
- workspace configuration records
- agent definitions
- agent run records
- workflow definitions
- task or job records
- artifact metadata
- review queue items
- human decision records
- audit records
- permission scope records
- runtime mode records
- system settings
- schema/version metadata

Core-owned data must be reusable across workspace types.

Core-owned data must not contain business-specific customer content unless that content is represented only as workspace-scoped private data or safely summarized metadata.

## Workspace-Owned Data

Workspace-owned data belongs to one workspace.

Workspace-owned data may include:

- raw business inputs
- customer data
- customer history
- customer requests
- private notes
- workspace-private drafts
- workspace artifacts
- workspace deliverables
- workspace strategy
- workspace-specific templates
- workspace-specific prompts
- workspace-specific brand language
- workspace-specific service offers
- workspace-specific product details
- workspace-specific pricing assumptions
- workspace-specific channel rules
- workspace-local workflow state

Workspace-owned data is isolated by default.

Other workspaces must not read it directly.

The Observatory must not receive it unless it has been transformed into an approved sanitized signal.

## Observatory-Owned Data

Observatory-owned data is shared intelligence derived from sanitized signals.

The Observatory may own:

- approved sanitized signals
- normalized signal records
- derived keyword clusters
- trend profiles
- generalized competitor or market patterns
- opportunity scores
- confidence scores
- data quality notes
- generalized observations
- research queue items
- strategy queue items
- Observatory ingestion records
- Observatory query audit records

The Observatory owns generalized intelligence, not private workspace memory.

The Observatory must not become a dumping ground for raw workspace data.

## Adapter-Owned Patterns

Workspace adapters describe reusable patterns for a class of workspaces.

Adapters may define:

- expected workflows
- common agent roles
- common review gates
- common output types
- common artifact categories
- common data-source types
- common hard-no rules
- common Observatory signal patterns

Adapters must not own private records for a real business.

Adapters are templates and patterns, not operating databases.

Examples:

| Adapter Pattern | Belongs In |
|---|---|
| service business intake pattern | service business adapter |
| marketplace listing draft pattern | marketplace store adapter |
| content editorial workflow | content adapter |
| internal research scoring packet pattern | internal research adapter |

## Integration-Owned Records

Integration-owned records are specific to external systems or providers.

Examples:

- OAuth connection records
- external account references
- provider identifiers
- external object ids
- API request/response metadata
- rate limit state
- provider capability flags
- provider-specific payload snapshots where allowed
- token storage references
- webhook event metadata

Integration-owned records must remain subordinate to Neon Ronin core rules.

They must obey:

- workspace isolation
- permissions
- review gates
- runtime modes
- audit requirements
- credential rules
- external integration contracts

External integration data must not leak provider-specific assumptions into core schemas.

Example:

```text
Bad core field: etsy_listing_id
Better pattern: external_reference { provider, resource_type, provider_resource_id }
```

Specific provider fields may exist inside integration-specific schemas later, but not in generic core records.

## Referenced-Only Data

Referenced-only data is data Neon Ronin may point to without owning as canonical truth.

Examples:

- external platform ids
- source URLs
- file paths
- local asset paths
- external report references
- marketplace resource references
- provider request ids
- workspace artifact references from an audit record
- Observatory signal references from a workspace decision record

Referencing data does not transfer ownership.

```text
Reading or referencing a record does not make Neon Ronin core the owner of that record.
```

A reference should preserve enough context to trace the source without copying private or provider-specific data into the wrong owner.

## Derived Data

Derived data is produced from one or more source records.

Examples:

- opportunity score derived from sanitized signals
- QA result derived from an artifact
- recommendation packet derived from research notes
- trend summary derived from Observatory records
- workspace health score derived from audit and review records
- agent confidence assessment derived from run output

Derived data must be labeled as derived.

Derived data must preserve provenance back to its source records.

Derived data must not replace canonical source records.

Core rule:

```text
A derived recommendation is not approval.
A score is not a decision.
A draft is not a deliverable.
A signal summary is not raw evidence.
```

## Forbidden-In-Core Data

The following must not become core platform data:

- one workspace's report language
- one business's service packages
- one business's customer promises
- one business's pricing assumptions
- one business's private customer history
- one store's product niche
- one marketplace account's assumptions
- one platform's publish payload shape
- raw customer content
- raw customer files
- raw credentials
- raw OAuth tokens
- customer payment details
- unsanitized customer notes
- workspace-private drafts
- confidential workspace strategy
- exact marketplace listing copy from one workspace
- exact report templates from one business

These may belong in workspace-private records, integration-specific records, or external systems, but not in Neon Ronin core.

## Read-Without-Ownership Rule

A system component may read or reference data without owning it.

Examples:

- a workspace may query Observatory intelligence without owning Observatory records
- an agent run may reference an artifact without owning the artifact content
- an audit record may reference a review item without becoming the review item
- a workflow may reference an integration connection without owning credentials
- a workspace decision may cite a signal without absorbing the Observatory source record

Read access does not imply ownership.

Write access does not imply schema authority.

Convenience copying must be avoided unless explicitly justified.

## Derived-Does-Not-Replace-Canonical Rule

Derived outputs must remain subordinate to their source records.

A derived record may inform human decisions.

It must not become the canonical truth for the thing it summarizes unless an explicit schema or ADR says so.

Examples:

| Derived Output | Must Not Replace |
|---|---|
| opportunity score | underlying signals and evidence |
| QA summary | original artifact and review decision |
| agent recommendation | human approval |
| market pattern | source sanitized signals |
| workspace health score | audit records and review records |

## Deferred Domain Rule

Deferred domains must not receive ad hoc core schemas, fields, or tables.

Deferred domains currently include:

- Etsy integration
- Printify integration
- Fiverr automation
- marketplace publishing
- Tauri UI
- LangGraph integration
- Hermes integration
- scheduled agents
- watch mode
- multi-user roles
- cloud sync
- plugin marketplaces

A deferred domain may be discussed in research or roadmap docs.

It must not appear in core schemas as a convenience shortcut before it is promoted through the roadmap.

## JSON Sludge Rule

JSON fields may be useful for bounded provider payloads, metadata, or future-proofing.

But JSON must not be used to avoid schema design.

Bad use of JSON:

```text
custom_data: { anything goes }
```

Acceptable use of JSON:

```text
provider_payload_snapshot: bounded provider-specific payload, integration-owned, not core semantic truth
```

If a JSON field becomes the main way the system stores important meaning, the boundary is too weak.

## Boundary Classification Test

Before adding a new schema, table, field, or durable document type, answer:

1. Who owns this data?
2. Is it core-owned, workspace-owned, Observatory-owned, adapter-owned, integration-owned, referenced-only, derived, or forbidden in core?
3. Is it business-neutral?
4. Is it private to one workspace?
5. Is it sanitized enough for Observatory use?
6. Is it provider-specific?
7. Is it derived from other records?
8. What provenance must it keep?
9. What review or audit rules apply?
10. Is this domain deferred?
11. Would adding this create a shortcut around workspace isolation?
12. Would adding this make core depend on a specific business or first-business candidate?

If these questions cannot be answered, do not add the data structure yet.

## Examples

### Example 1 - Workspace-Specific Report Template

Classification:

```text
Workspace-owned data
```

Reason:

A specific business report template is workspace-owned. It may inform reusable artifact patterns, but the exact template must not become core.

Reusable extraction may produce:

```text
service deliverable artifact pattern
QA review gate
customer delivery gate
```

### Example 2 - Review Queue Item

Classification:

```text
Core-owned data
```

Reason:

Many workspace types need human review gates. The review item is business-neutral, even if the linked artifact is workspace-specific.

### Example 3 - Etsy Listing ID

Classification:

```text
Integration-owned record or referenced-only data
```

Reason:

An Etsy listing id is provider-specific. It must not become a generic core field.

### Example 4 - Sanitized Market Pattern

Classification:

```text
Observatory-owned data
```

Reason:

A sanitized generalized market pattern can support multiple workspaces and has passed the Observatory boundary.

### Example 5 - Opportunity Score

Classification:

```text
Derived data
```

Reason:

The score is produced from source signals or evidence. It must preserve provenance and must not replace the underlying records.

## Relationship To Other Docs

This document informs future schema design.

Related docs:

- `docs/core/01-platform-doctrine.md`
- `docs/core/02-workspace-model.md`
- `docs/core/04-observatory.md`
- `docs/core/07-permissions-and-audit.md`
- `docs/core/08-sanitization.md`
- `docs/core/09-workspace-lifecycle.md`
- `docs/decisions/adr-003-first-business-containment.md`
- `docs/decisions/adr-004-observatory-shared-intelligence-boundary.md`

## Final Rule

```text
Ownership before schema.
Boundaries before convenience.
Provenance before interpretation.
```
