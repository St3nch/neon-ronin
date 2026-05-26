"""Run the first Neon Ronin persistence proof hammer suite.

This runner exists only to make the approved local persistence proof repeatable
without manual PYTHONPATH setup. It does not introduce new runtime behavior.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CORE_SRC = ROOT / "packages" / "neon-core" / "src"
FIXTURE_SRC = ROOT / "fixtures" / "internal-research"
TESTS_DIR = ROOT / "packages" / "neon-core" / "tests"

for path in (CORE_SRC, FIXTURE_SRC, TESTS_DIR):
    text_path = str(path)
    if text_path not in sys.path:
        sys.path.insert(0, text_path)


def main() -> int:
    """Run the first persistence proof hammer suite."""

    print("hammer: first-persistence-proof")
    print(f"core_src: {CORE_SRC}")
    print(f"fixtures: {FIXTURE_SRC}")
    print(f"tests: {TESTS_DIR}")

    suite = unittest.defaultTestLoader.discover(str(TESTS_DIR))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
