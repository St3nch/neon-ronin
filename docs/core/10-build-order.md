# 10 - Build Order

## Purpose

This document defines the recommended Neon Ronin implementation order.

The goal is to prevent building workspace-specific features before the core platform contracts exist.

## Core Principle

```text
Do not build automation before the runtime contract exists.
Do not onboard businesses before workspace boundaries exist.
Do not share signals before sanitization rules exist.
```

## Recommended Build Sequence

### Phase 1 - Platform Doctrine

Create and stabilize:

- platform doctrine
- workspace model
- business onboarding
- Observatory definition
- agent runtime contract
- review queue model
- permissions and audit rules

### Phase 2 - Core Schemas

Define:

- workspace config schema
- signal schema
- review queue item schema
- agent output schema
- artifact metadata schema

### Phase 3 - Manual Workspace Validation

Create one low-risk internal workspace.

Goals:

- validate workspace configs
- validate review queue flow
- validate signal intake flow
- validate audit logging
- validate workspace isolation

No autonomous actions should exist yet.

### Phase 4 - Controlled Agent Assistance

Introduce:

- research drafting
- queue generation
- structured outputs
- scheduled read-only monitoring

All risky actions remain human-gated.

### Phase 5 - Additional Workspace Types

Add:

- service business workspace
- marketplace store workspace
- digital product workspace
- content workspace

Only after core runtime rules are stable.

## Do Not Build Yet

```text
Autonomous publishing
Autonomous spending
Cross-agent self-orchestration
Direct marketplace write actions
Unreviewed customer messaging
```

## Final Rule

```text
Neon Ronin should earn complexity gradually.
```
