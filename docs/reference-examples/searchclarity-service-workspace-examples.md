# SearchClarity Service Workspace Examples

## Status

```text
Reference example only
```

This document preserves SearchClarity-aware worked examples outside `docs/core/`.

SearchClarity is useful planning pressure for Neon Ronin, but SearchClarity-specific details must not define Neon Ronin core doctrine, core schema, or platform authority.

## Boundary Rule

```text
Prepare Neon Ronin for SearchClarity.
Do not turn Neon Ronin into SearchClarity.
```

## Example Classification

| SearchClarity Item | Likely Classification |
|---|---|
| Professional PDF reports | Workspace output / artifact need |
| Customer delivery review | Reusable core review gate need |
| Fiverr gig copy | Workspace-specific artifact |
| Etsy Listing Visibility Audit template | Workspace-specific, or service-adapter pattern only after generic extraction |
| Raw market signal capture | Workspace-owned signal source |
| Observatory scoring | Neon Ronin core / Observatory concern |
| Customer/order/report tracker | Workspace-owned operational data |
| Pricing | Workspace-owned business detail |

## Example Business Intake Sketch

```yaml
business_intake_id: intake_searchclarity_example
idea_name: SearchClarity
intake_status: captured
proposed_workspace_type: service
summary: Service business concept producing evidence-based visibility reports for marketplace sellers.
purpose: Validate a manual service workflow that produces human-reviewed reports and captures safe market signals.
primary_offer_or_output: Customer-facing PDF visibility audit report.
private_data_expected: true
classification_verdict: YELLOW_LIGHT
reusable_capabilities:
  - artifact tracking
  - workflow tracking
  - customer delivery review
  - signal sanitization
  - audit trail
workspace_specific_items:
  - brand language
  - Fiverr copy
  - report template text
  - pricing
  - customer records
deferred_domains_touched:
  - Fiverr automation
  - external integrations
manual_test_goal: Model one manual report workflow from intake to QA to delivery-ready artifact without automation.
```

## Example Artifact Sketch

```yaml
artifact_id: art_searchclarity_sample_report_example
workspace_id: ws_searchclarity_future
artifact_type: sample_report
status: draft
content_scope: workspace_private
storage_reference:
  storage_type: repo_path
  reference: docs/samples/maplewood-candle-co-listing-visibility-audit.md
  external_reference_id: null
  content_stored_in_core: false
title: Maplewood Candle Co. Etsy Listing Visibility Audit Sample
summary: Fictional sample report source used as a SearchClarity proof asset and future workflow input.
public_use_allowed: false
```

This sketch does not authorize customer delivery automation, Fiverr automation, Etsy integration, or SearchClarity-specific core schema.

## Example Hammer Scenario Sources

SearchClarity may later provide realistic hammer scenarios for:

- report artifact ownership
- customer delivery review
- raw market signal capture
- sanitized signal handoff
- public sample and consent checks
- external service-platform boundaries

The hammer doctrine should remain generic.

## Final Rule

```text
SearchClarity can supply examples later; Neon Ronin core supplies the reusable laws.
```
