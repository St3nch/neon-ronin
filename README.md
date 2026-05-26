# Neon Ronin Runtime Layout

This repository now uses a small app-ready layout while keeping the first implementation slice narrow.

## Top-Level Layout

```text
apps/              Future user-facing applications.
services/          Future local sidecars/services used by apps.
packages/          Reusable platform packages.
fixtures/          Test/proof fixtures derived from governed docs.
tools/             Developer and hammer-test tooling.
docs/              Canonical doctrine, schemas, operations, and workspace records.
research-docs/     Supporting research context, not canonical doctrine.
```

## Current Implementation Scope

Only the first local persistence proof is authorized.

Allowed implementation area:

```text
packages/neon-core/
fixtures/internal-research/
tools/hammers/
```

Deferred areas:

```text
apps/desktop/
services/local/
```

Those folders exist to reserve the app architecture shape. They do not authorize UI work, Tauri setup, a sidecar service, agents, integrations, scheduled jobs, watch mode, live Observatory ingestion, customer-facing onboarding, SearchClarity onboarding, or automation.

## Intended Future Desktop Shape

The current planning bias is:

```text
apps/desktop/      Future Tauri + web frontend shell.
services/local/    Future local sidecar/service boundary, likely for long-running workflows.
packages/neon-core/ Shared core platform rules and persistence behavior.
```

The first proof starts in `packages/neon-core` so the core persistence behavior can be reused later by a desktop shell or local service without tying it to UI framework choices.