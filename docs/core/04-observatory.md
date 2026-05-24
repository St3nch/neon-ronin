# 04 - Observatory

## Purpose

The Observatory is Neon Ronin's shared intelligence layer.

It receives sanitized signals from workspaces, normalizes them, scores them, and routes them into research or strategy queues.

The Observatory is business-neutral. It does not belong to any one workspace.

## What The Observatory Stores

- sanitized workspace signals
- normalized signal records
- keyword clusters
- trend profiles
- competitor or market patterns
- opportunity scores
- data quality notes
- generalized observations
- research queue items
- strategy queue items

## What The Observatory Must Not Store

- private customer data
- raw credentials
- unsanitized customer notes
- workspace-private drafts
- confidential business details
- personally identifying information unless explicitly approved and required

## Signal Intake Flow

```text
Workspace observes something useful
-> workspace creates raw signal
-> signal is sanitized
-> signal passes sanitization gate
-> signal enters Observatory inbox
-> Observatory normalizes signal
-> Observatory checks duplicates
-> Observatory enriches signal if allowed
-> Observatory scores or queues signal
```

## Workspace Query Types

| Query Type | Purpose |
|---|---|
| keyword_cluster | Return related terms or themes |
| trend_profile | Return seasonality or trend notes |
| competitor_pattern | Return generalized market patterns |
| opportunity_score | Return scored opportunity context |
| prior_signal_check | Check whether similar signals exist |
| data_quality_check | Evaluate evidence quality |

## Sanitization Rule

A signal is Observatory-eligible only when it contains generalized market intelligence and no private workspace/customer details.

## Core Rule

```text
The Observatory is the only sanctioned cross-workspace intelligence channel.
Private workspace data does not cross boundaries directly.
```
