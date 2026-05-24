# ADR-001 - Workspaces, Not Hardcoded Businesses

## Status

Accepted

## Context

Neon Ronin must support multiple future businesses. Designing around one specific business creates drift and makes the platform brittle.

## Decision

Core Neon Ronin docs and architecture will use generic workspace types. Business-specific needs will live in business docs or workspace adapter docs.

## Consequences

- Core remains reusable.
- Business-specific workflows require adapter docs.
- Workspace adapters translate real business needs into generic capabilities.
- Core docs may be less concrete, but they stay clean.
