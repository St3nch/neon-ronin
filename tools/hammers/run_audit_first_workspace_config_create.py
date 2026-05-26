"""Compatibility wrapper for the renamed first persistence proof hammer.

Prefer `python tools/hammers/run_first_persistence_proof.py`.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
HAMMERS_DIR = ROOT / "tools" / "hammers"

text_path = str(HAMMERS_DIR)
if text_path not in sys.path:
    sys.path.insert(0, text_path)

from run_first_persistence_proof import main


if __name__ == "__main__":
    raise SystemExit(main())
