# Neon Ronin Docs Index

Neon Ronin is a business-neutral, multi-workspace agent operating system.

Core docs must not be written around any one specific business, brand, store, or service.

## Folder Map

| Folder | Purpose |
|---|---|
| `core` | Business-neutral Neon Ronin platform doctrine and architecture |
| `workspace-adapters` | Generic workspace patterns for types of businesses |
| `reference-examples` | Non-canonical concrete examples and scenario sketches |
| `workspaces` | Future home for real workspace configs, notes, and manual-test records |
| `research-docs/` | Supporting research, feasibility notes, policy research, and experiments |
| `decisions` | Architecture decision records |

## Anti-Drift Rule

```text
Neon Ronin core defines reusable capabilities.
Business docs define business-specific needs.
Workspace adapters translate business needs into Neon Ronin capabilities.
```

If a document depends on a specific business name, it does not belong in `docs/core`.
