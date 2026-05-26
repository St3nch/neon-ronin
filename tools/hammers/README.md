# tools/hammers

Hammer proof tooling.

Current authorized hammer:

```text
first-persistence-proof
```

This folder may contain focused verification scripts/tests for the first local persistence proof.

It must not introduce agents, integrations, UI, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.
## Runner

Run the current hammer proof from the repository root:

```text
python tools/hammers/run_first_persistence_proof.py
```



The runner only sets local import paths and executes the existing unittest proof. It must not introduce agents, integrations, UI, scheduled jobs, watch mode, live Observatory ingestion, customer-facing workspace onboarding, SearchClarity onboarding, or automation.
