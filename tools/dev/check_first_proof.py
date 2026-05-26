"""Run developer checks for the first Neon Ronin persistence proof.

This script is intentionally limited to the already-authorized first proof.
It does not introduce agents, UI, integrations, scheduled jobs, watch mode,
live Observatory ingestion, customer-facing onboarding, SearchClarity
onboarding, automation, new persistence tables, or new domain records.
"""

from __future__ import annotations

import compileall
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
HAMMER = ROOT / "tools" / "hammers" / "run_first_persistence_proof.py"
COMPILE_TARGETS = (
    ROOT / "packages" / "neon-core" / "src",
    ROOT / "packages" / "neon-core" / "tests",
    ROOT / "fixtures" / "internal-research",
    ROOT / "tools" / "hammers",
)


def run_hammer() -> int:
    """Run the current audit-first workspace config hammer."""

    print("check: first-persistence-proof", flush=True)
    completed = subprocess.run([sys.executable, str(HAMMER)], cwd=ROOT, check=False)
    return completed.returncode


def run_compileall() -> int:
    """Compile the current proof modules and tests."""

    print("check: compileall", flush=True)
    failed_targets: list[pathlib.Path] = []
    for target in COMPILE_TARGETS:
        print(f"compile: {target.relative_to(ROOT)}")
        if not compileall.compile_dir(str(target), quiet=1):
            failed_targets.append(target)

    if failed_targets:
        print("compileall failed for:", file=sys.stderr)
        for target in failed_targets:
            print(f"- {target.relative_to(ROOT)}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    """Run all first-proof developer validation checks."""

    hammer_status = run_hammer()
    if hammer_status != 0:
        return hammer_status
    return run_compileall()


if __name__ == "__main__":
    raise SystemExit(main())
