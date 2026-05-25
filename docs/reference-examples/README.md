# Reference Examples

## Purpose

This folder is the non-core home for concrete worked examples, sample classifications, and scenario sketches that help humans and LLMs understand Neon Ronin.

Reference examples are explanatory support.

They are not canonical platform doctrine.

## Core Rule

```text
Reference examples may illustrate Neon Ronin.
Reference examples do not define Neon Ronin.
```

Canonical doctrine remains in:

- `AGENTS.md`
- `docs/README.md`
- `docs/core/`
- `docs/decisions/`
- `docs/operations/`
- `docs/workspace-adapters/`

## What Belongs Here

Use this folder for:

- concrete worked examples
- future workspace scenario sketches
- example business-intake classifications
- example artifact/reference shapes
- SearchClarity-aware planning examples
- realistic hammer-test scenario notes

## What Does Not Belong Here

Do not put these here as authority:

- core schema rules
- platform invariants
- ADR decisions
- real secrets or credentials
- raw customer data
- live provider payloads
- prompts from audit sessions
- ignored audit reports from `docs/claudeai-audits/`

## Promotion Rule

A reference example becomes canonical only when its reusable lesson is deliberately promoted into a core doc, schema doc, operations doc, adapter doc, or ADR.

Concrete business details should remain outside core unless rewritten as business-neutral platform capability.

## SearchClarity Examples

SearchClarity-aware examples may live here during Phase 5C cleanup.

They must be labeled as reference examples and must not define core doctrine, core schemas, platform authority, or workspace lifecycle rules.

## Final Rule

```text
Examples explain the platform; they do not become the platform.
```
