# Business Intake Schema

## Purpose

This document defines the P1 business intake schema for Neon Ronin.

Business intake captures a proposed business, project, gig, service, store, content operation, internal research effort, or hybrid idea before it becomes a configured workspace.

Business intake exists so Neon Ronin can evaluate and classify ideas without letting one idea mutate core platform doctrine or schema.

## Schema Status

```text
P1 planning schema
```

This is an implementation-facing planning document.

It is not yet a database migration, JSON Schema file, Pydantic model, TypeScript type, or API contract.

## Ownership Category

```text
Workspace-owned data or core-tracked intake metadata
```

Business intake records are usually workspace-candidate records.

Core may track intake metadata and classification results, but the business-specific details remain candidate/workspace-owned until promoted through the correct boundary.

## Core Rule

```text
Business intake turns ideas into classified workspace candidates.
It does not turn business-specific details into core doctrine.
```

A strong business idea may become a workspace.

It does not become Neon Ronin.

## Required Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `business_intake_id` | string | system-owned | Stable unique intake id |
| `idea_name` | string | human-owned | Human-readable idea/business name |
| `intake_status` | enum | system-governed | Current intake status |
| `proposed_workspace_type` | enum | human/system-owned | Proposed workspace type |
| `summary` | string | human-owned | Short business idea summary |
| `purpose` | string | human-owned | What the business/project is for |
| `target_customer_or_user` | string | human-owned | Intended customer/user group |
| `primary_offer_or_output` | string | human-owned | Main offer, deliverable, product, or output |
| `channels` | array enum | human-owned | Expected operating channels |
| `expected_inputs` | array string | human-owned | Inputs the workspace would receive |
| `expected_outputs` | array string | human-owned | Outputs the workspace would produce |
| `private_data_expected` | boolean | human/system-owned | Whether private/customer data is expected |
| `external_systems_expected` | array string | human-owned | External systems likely involved |
| `initial_risk_notes` | string | human-owned | Known risk/privacy/compliance/rights notes |
| `classification_verdict` | enum | human/system-owned | Green/yellow/red/park classification |
| `created_at` | datetime | system-owned | Creation timestamp |
| `updated_at` | datetime | system-owned | Last update timestamp |
| `audit_record_ids` | array string | system/reference | Audit records related to intake |

## Optional Fields

| Field | Type | Owner | Description |
|---|---|---|---|
| `description` | string | human-owned | Longer business description |
| `source_actor_type` | enum | system/human-owned | Actor type that submitted the intake |
| `source_actor_id` | string | system/human-owned | Actor id that submitted the intake |
| `source_references` | array object | referenced-only | Docs, notes, artifacts, or research supporting the idea |
| `proposed_adapter` | string/null | human/system-owned | Candidate adapter |
| `known_workflows` | array string | human-owned | Likely workflows needed |
| `known_review_gates` | array enum | human/system-owned | Likely review gates needed |
| `hard_no_rules` | array string | human/system-owned | Known action prohibitions |
| `observatory_fit` | object | human/system-owned | Query/submission expectations |
| `reusable_capabilities` | array string | human/system-owned | Capabilities possibly reusable across Neon Ronin |
| `workspace_specific_items` | array string | human/system-owned | Items that must stay workspace-owned |
| `deferred_domains_touched` | array string | human/system-owned | Deferred domains touched by the idea |
| `manual_test_goal` | string/null | human/system-owned | Goal for first manual test |
| `promotion_recommendation` | enum/null | human/system-owned | Recommended next step |
| `tags` | array string | bounded/human-owned | Bounded organizational tags |
| `version` | integer/string | system-owned | Schema/version tracking |

## Valid Intake Statuses

Canonical values:

```text
captured
classifying
needs_more_info
parked
rejected
approved_for_onboarding
converted_to_workspace
archived
```

## Status Transition Rules

Allowed transitions:

| From | To | Requirement |
|---|---|---|
| `captured` | `classifying` | Human/system begins classification |
| `captured` | `parked` | Human parks before classification |
| `classifying` | `needs_more_info` | Required information missing |
| `classifying` | `approved_for_onboarding` | Human approves for onboarding |
| `classifying` | `parked` | Human parks idea |
| `classifying` | `rejected` | Human rejects idea |
| `needs_more_info` | `classifying` | Missing info supplied |
| `approved_for_onboarding` | `converted_to_workspace` | Workspace config created |
| any non-terminal | `archived` | Human/system archives |

Terminal statuses by default:

```text
rejected
converted_to_workspace
archived
```

## Proposed Workspace Types

Canonical values:

```text
service
marketplace_store
digital_products
content
internal_research
hybrid
other
```

If workspace type is unclear, use `other` or keep status as `needs_more_info`.

## Classification Verdicts

Canonical values:

```text
GREEN_LIGHT
YELLOW_LIGHT
RED_LIGHT
PARK
UNKNOWN
```

Meanings:

| Verdict | Meaning |
|---|---|
| `GREEN_LIGHT` | Worth onboarding/testing now |
| `YELLOW_LIGHT` | Possible but needs constraints or manual proof |
| `RED_LIGHT` | Bad fit, too risky, premature, or platform-drifting |
| `PARK` | Potentially useful but wrong time |
| `UNKNOWN` | Not enough information |

## Channels

Initial channel values:

```text
marketplace
service_platform
direct_site
social_platform
content_platform
internal_research
external_provider
other
```

A channel is not automatically an integration.

## Observatory Fit Object

Recommended shape:

```yaml
observatory_fit:
  may_query_observatory: boolean
  may_generate_signals: boolean
  likely_signal_types:
    - market_gap
    - keyword_pattern
  private_data_risk: low | medium | high | restricted | unknown
  sanitization_notes: string
```

Business intake may identify potential signal value, but it does not approve Observatory submission.

## Reusable Capability Extraction

Business intake should classify needs as:

```text
core_platform_capability
adapter_capability
workspace_specific
integration_specific
out_of_scope
```

Example:

| Business Need | Classification |
|---|---|
| customer delivery approval | core_platform_capability |
| service report template | workspace_specific or adapter_capability |
| Fiverr gig copy | workspace_specific |
| generic artifact review | core_platform_capability |
| provider-specific API payload | integration_specific |

## Future Service Workspace Example Classification

A concrete service-workspace candidate should classify like this:

| Item | Classification |
|---|---|
| Professional PDF reports | workspace output / artifact need |
| Customer delivery review | reusable core review gate need |
| Service-platform profile copy | workspace-specific |
| Service report template | workspace-specific or service adapter pattern after extraction |
| Raw market signal capture | workspace-owned signal source |
| Observatory scoring | Neon Ronin core / Observatory concern |
| Customer/order/report tracker | workspace-owned operational data |

This example does not make a specific service business core doctrine.

## System-Owned Fields

System-owned fields should include:

- `business_intake_id`
- `intake_status`
- `created_at`
- `updated_at`
- `audit_record_ids`
- system-computed classification aids if added later
- `version`

Agents and callers must not forge system-owned fields.

## Immutable Fields

Likely immutable after creation unless governed correction allows change:

- `business_intake_id`
- original `source_actor_type`
- original `source_actor_id`
- original `created_at`

Classification can change as more evidence arrives, but changes must be auditable.

## Provenance Requirements

Business intake must preserve:

- who submitted the idea
- when it was submitted
- source notes/docs/artifacts
- classification reasoning
- workspace type reasoning
- reusable capability extraction
- workspace-specific boundary notes
- promotion/rejection/parking decision
- audit records

## Audit Requirements

The following events must generate audit records:

- business intake created
- intake classification started
- intake status changed
- verdict assigned
- verdict changed
- intake approved for onboarding
- intake rejected
- intake parked
- intake converted to workspace
- reusable capability extracted

## Lifecycle Rules

Business intake sits before workspace lifecycle or at the `idea` stage.

A business intake record may create a workspace config only when approved for onboarding.

Creating intake does not permit agent runs, external actions, customer work, or Observatory submission.

## Relationships To Other Records

Business intake may reference:

- source artifacts
- research packets
- audit records
- review items
- human decisions
- workspace config after conversion
- signal candidates later if manual testing produces them

Business intake should not own customer records, credentials, provider payloads, or workspace operating history.

## Forbidden Fields

Do not add fields such as:

```text
customer_email
customer_phone
payment_details
provider_token
api_key
oauth_refresh_token
full_report_template_body
etsy_listing_payload
printify_product_payload
fiverr_message_text
custom_data
```

Use source references, workspace docs, integration records, or future governed schemas instead.

## Example Record

```yaml
business_intake_id: intake_future_service_workspace_001
idea_name: Future Service Workspace
intake_status: captured
proposed_workspace_type: service
summary: Professional service business concept producing evidence-based, human-reviewed customer deliverables.
purpose: Validate a manual service workflow that produces reviewed deliverables and captures safe market signals.
target_customer_or_user: Small-business operators who need structured recommendations.
primary_offer_or_output: Customer-facing PDF report.
channels:
  - service_platform
  - direct_site
expected_inputs:
  - customer intake answers
  - source URLs or files provided by customer
  - optional screenshots provided by customer
expected_outputs:
  - draft report
  - final PDF report
  - action plan
  - generalized observations
private_data_expected: true
external_systems_expected:
  - service platform
  - marketplace reference source
  - research tool
initial_risk_notes: Customer data, platform terms, public sample consent, no unsupported guarantees, no credential storage.
classification_verdict: YELLOW_LIGHT
created_at: 2026-05-24T00:00:00Z
updated_at: 2026-05-24T00:00:00Z
audit_record_ids:
  - audit_001
source_actor_type: human
source_actor_id: human_operator
source_references:
  - record_type: artifact
    record_id: art_future_service_docs_review
    relationship: source_context
proposed_adapter: service-business-workspace
known_workflows:
  - customer intake
  - report production
  - QA review
  - customer delivery
  - signal capture
known_review_gates:
  - quality_gate
  - customer_delivery_gate
  - data_privacy_gate
  - rights_and_compliance_gate
  - signal_sanitization_gate
hard_no_rules:
  - no_autonomous_customer_delivery
  - no_autonomous_customer_messaging
  - no_autonomous_publishing
  - no_platform_credentials
observatory_fit:
  may_query_observatory: true
  may_generate_signals: true
  likely_signal_types:
    - market_gap
    - keyword_pattern
    - customer_need_pattern
  private_data_risk: medium
  sanitization_notes: Raw client details must remain workspace-owned; only generalized sanitized signals may be handed off.
reusable_capabilities:
  - artifact tracking
  - workflow tracking
  - customer delivery review
  - signal sanitization
  - audit trail
workspace_specific_items:
  - brand language
  - service-platform copy
  - report template text
  - pricing
  - customer records
deferred_domains_touched:
  - service-platform automation
  - external integrations
manual_test_goal: Model one manual report workflow from intake to QA to delivery-ready artifact without automation.
promotion_recommendation: continue_business_build_before_full_onboarding
tags:
  - service
  - future-workspace
version: 1
```

## Validation Questions

Before accepting a business intake record, answer:

1. Is the idea clearly described?
2. Is proposed workspace type identified or marked unknown?
3. Are expected inputs and outputs clear?
4. Is private data risk identified?
5. Are external systems identified without becoming core fields?
6. Are reusable capabilities separated from workspace-specific details?
7. Are deferred domains identified?
8. Is the classification verdict justified?
9. Is there enough provenance to understand where the idea came from?
10. Does intake avoid granting operational permissions?
11. Does it avoid turning business-specific details into core doctrine?
12. Does it avoid unbounded metadata/custom data?

## Non-Goals

This schema does not define:

- customer intake forms for a specific business
- customer records
- workspace config details after conversion
- report templates
- provider integrations
- marketplace automation
- scoring formulas
- database tables

## Final Rule

```text
Intake classifies the business idea; it does not promote the business into core.
```
