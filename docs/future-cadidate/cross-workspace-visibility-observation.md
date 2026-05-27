# Cross-Workspace Visibility Observation Candidate

## Status

```text
candidate_only
```

## Purpose

This document captures a future Neon Ronin capability candidate for provider-agnostic visibility observations across owned websites, marketplace assets, customer assets, SERP results, GEO/LLM visibility, analytics sources, and similar external visibility signals.

This is parked future context.

It is not active roadmap work.

It does not authorize implementation.

It does not authorize database migrations.

It does not authorize new schemas, new persistence tables, runtime behavior, integrations, agents, scheduled jobs, watch mode, Observatory ingestion, SearchClarity onboarding, customer-facing work, automation, or external actions.

## Current Recommendation

Wait.

Do not implement this yet.

The concept is important, but Neon Ronin needs more evidence before designing persistence or integration boundaries.

Near-term work should remain manual and evidence-driven:

- define what SearchClarity and future workspaces need to observe
- collect examples manually or through workspace-owned planning docs
- identify repeated patterns across more than one workspace
- keep DataForSEO and any other provider as possible adapters, not core doctrine
- avoid database design until request/result/observation shapes are proven by real use cases

## Origin

This candidate was identified while discussing future support for SearchClarity-owned website visibility and customer marketplace ranking data.

SearchClarity may eventually want visibility support for:

- `searchclarity.co` owned website SERP/GEO/LLM visibility
- Fiverr gig visibility
- Etsy listing visibility for customer reports
- marketplace ranking checks
- blog/content opportunity monitoring
- analytics and search console observations

The reusable Neon Ronin concept is broader than SearchClarity and broader than any one provider.

## Core Principle

Neon Ronin should eventually model visibility observations and provenance, not provider-specific API shapes.

Good abstraction:

```text
visibility_data_request
provider_payload_reference
visibility_observation
visibility_signal_candidate
```

Bad abstraction:

```text
dataforseo_results
searchclarity_serp_rankings
fiverr_rank_tracker_table
etsy_customer_rankings_table
```

Provider APIs should not become Neon Ronin database design.

## Provider-Agnostic Rule

DataForSEO may be a useful future provider, but it is only one possible source.

Possible future sources include:

| Source Type | Possible Providers Or Methods |
|---|---|
| Google SERP | DataForSEO, SerpApi, manual checks, approved search APIs |
| Bing SERP | DataForSEO, Bing Webmaster Tools, manual checks |
| Etsy search | marketplace-specific adapter, manual workflow, provider if available |
| Fiverr search | manual workflow, future adapter, provider if available |
| Google Search Console | Google Search Console API |
| Analytics | GA4, Plausible, Vercel Analytics, server logs |
| LLM visibility | manual prompts, approved APIs, third-party visibility tools |
| Website health | Lighthouse, crawler tools, custom approved checks |
| Mentions/citations | search APIs, monitoring tools, manual research |

Neon Ronin should record the source, provider, request context, observation, and provenance separately enough that providers can change later.

## Ownership Categories

Visibility data has different ownership and privacy levels.

### Owned Website Visibility

Example:

```text
searchclarity.co ranks for "etsy listing visibility audit" in Google results.
```

Likely sensitivity:

```text
workspace_owned_public_signal
```

This is usually lower risk because it concerns a workspace-owned public asset.

### Marketplace Gig Visibility

Example:

```text
SearchClarity's Fiverr gig appears for "etsy seo audit".
```

Likely sensitivity:

```text
workspace_owned_marketplace_signal
```

This still needs source, query, time, marketplace, account/asset boundaries, and review before public use.

### Customer Marketplace Ranking Data

Example:

```text
A customer Etsy listing ranks for a buyer query during a paid report.
```

Likely sensitivity:

```text
customer_or_workspace_private_signal
```

This needs stricter handling:

- customer/order linkage
- consent and retention rules
- workspace boundaries
- private data handling
- report linkage
- sanitization before any Observatory or cross-workspace use

### LLM/GEO Visibility

Example:

```text
A model answer mentions a workspace or competitor for a target query.
```

Likely sensitivity:

```text
public_or_mixed_signal
```

This requires careful evidence capture, prompt/source metadata, model/provider context, timestamp, and uncertainty notes.

## Candidate Conceptual Layers

These are conceptual layers only, not approved tables.

### 1. Visibility Data Request

A request says what should be checked and why.

Candidate fields later:

```text
request_id
workspace_id
target_type
target_ref
source_type
provider
queries
location
language
device
requested_by
purpose
status
created_at
```

### 2. Provider Payload Reference

A provider payload reference records what was fetched without forcing provider JSON into core tables.

Candidate fields later:

```text
payload_id
request_id
provider
provider_endpoint
payload_hash
storage_reference
retrieved_at
cost_units
status
```

Raw payload storage should be bounded and deliberate.

Core should not blindly store large provider JSON blobs without retention, privacy, and cost rules.

### 3. Visibility Observation

A normalized observation captures the reusable visibility fact.

Candidate fields later:

```text
observation_id
workspace_id
request_id
source_type
observed_at
query
target_type
target_ref
observed_url_or_entity
position
page
result_type
matched_entity
confidence
source_reference
private_data_removed
sensitivity_rating
```

### 4. Visibility Signal Candidate

A derived signal candidate turns observations into possible action, without treating the action as approved.

Example:

```text
SearchClarity's Fiverr landing page appears for the target query, but the canonical service page does not.
Recommend reviewing internal links and service page metadata.
```

This should map to existing Neon Ronin patterns where possible:

- signal candidate
- review queue item
- artifact metadata or repo diff reference
- human decision
- audit record

## Relationship To Current Proof Tables

Current first-proof tables are:

```text
workspace_configs
audit_records
review_queue_items
human_decisions
signal_candidates
artifact_metadata
workflow_records
```

These support review, audit, human decision, artifact reference, workflow definition, and signal-candidate control.

They are not enough for recurring visibility data at scale.

Future visibility support may eventually require new persistence boundaries, but only after a separate implementation-start decision.

## Possible Future Records

Candidate records later:

- visibility_data_request
- provider_payload_reference
- visibility_observation
- visibility_signal_candidate
- external_data_request
- external_data_result
- website_asset
- marketplace_asset
- customer_asset_reference
- analytics_observation
- llm_visibility_observation
- serp_observation
- marketplace_ranking_observation

These are candidate concepts only.

Do not create schemas or tables from this document.

## Asset Modeling Direction

Own websites and marketplace profiles should likely be treated as workspace-owned assets later.

Candidate examples:

```text
owned_website: searchclarity.co
marketplace_profile: SearchClarity Fiverr seller profile
marketplace_gig: Etsy Listing Visibility Audit on Fiverr
service_page: /services/etsy-listing-visibility-audit
channel_landing_page: /fiverr/etsy-listing-visibility-audit
```

A generic `workspace_asset` concept may be more reusable than a website-only model, but this is not decided.

Do not add `website_assets` or `workspace_assets` yet.

## Integration Boundary Direction

Provider-specific logic belongs in adapters or integration layers later.

DataForSEO, Google Search Console, Bing Webmaster Tools, GA4, Fiverr, Etsy, and future providers should not become core Neon Ronin assumptions.

Future adapter responsibilities may include:

- authentication
- provider request formatting
- rate limits
- quota and cost tracking
- retries and error handling
- raw payload references
- provider-specific normalization
- provider-specific availability limits

Core responsibilities may later include:

- workspace ownership
- request purpose
- provenance
- normalized observation rules
- review gates
- audit records
- human decisions
- derived signal candidates

## Candidate Review Gates Later

Possible gates:

- data_source_approval_gate
- provider_cost_gate
- data_privacy_gate
- customer_data_boundary_gate
- observation_quality_gate
- signal_sanitization_gate
- workspace_owner_approval_gate
- content_or_action_recommendation_gate
- publish_or_merge_approval_gate

Some may map to existing review queue and human decision patterns.

Some may remain workspace-local.

Some may become future schema-authority candidates.

None are approved as new core gate types by this document.

## Anti-Drift Rules

Do not let this candidate:

- make DataForSEO a core dependency
- make SearchClarity's website visibility needs universal Neon Ronin doctrine
- mix customer-private ranking data with public owned-site visibility data
- store raw provider payloads without retention and privacy rules
- treat SERP/GEO/LLM observations as decisions
- let agents act on visibility observations without human review
- create provider-shaped tables
- create SearchClarity-shaped tables
- skip source, query, time, location, device, and provider provenance
- ingest customer data into Observatory without sanitization and approval
- authorize integrations before integration boundaries exist

## Evidence Needed Before Promotion

Before this candidate can move toward active planning, Neon Ronin would need evidence such as:

- SearchClarity or another workspace defining concrete visibility questions
- repeated owned-site visibility observation examples
- repeated marketplace visibility observation examples
- clear distinction between workspace-owned public data and customer/private data
- provider comparison or source options beyond one vendor
- sample request/result/observation packets
- privacy and retention expectations
- cost/quota expectations
- review gates for derived recommendations
- proof that this belongs in Neon Ronin rather than only in one workspace

## Possible First Safe Proof Later

If this ever becomes active, the first safe proof should be tiny and local.

Possible future proof shape:

```text
manual visibility observation create
-> bounded validation
-> audit record
-> no provider API call
-> no integration
-> no agent
-> no scheduler
-> no Observatory ingestion
```

This would prove the record boundary before any provider integration.

Even that proof is not authorized by this document.

## Current Recommendation

Keep this candidate parked.

Do not implement now.

Do not design migrations now.

Do not wire DataForSEO now.

Let SearchClarity and future workspaces produce manual evidence first.
