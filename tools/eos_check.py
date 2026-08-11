#!/usr/bin/env python3
"""Deprecation shim: forwards to python -m tools.eos.

This path is the v1 checker's, and `org/decisions/ADR-0001` still names
it as the single sanctioned executable. That record is accepted and
append-only, so the path has to keep resolving. The shim is what makes
it resolve, and it forwards rather than pretending: the v1 checker
itself is at archive/v1-final:tools/eos_check.py and cannot validate a
v2 tree, because it looks for doctrine modules and a wargame index the
pack restructure retired.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main() -> int:
    print("tools/eos_check.py is deprecated: use python -m tools.eos check",
          file=sys.stderr)
    args = sys.argv[1:]
    forwarded = ["check"] + args if args else ["check", "--repo"]
    return subprocess.run(
        [sys.executable, "-m", "tools.eos", *forwarded], cwd=str(REPO)).returncode


if __name__ == "__main__":
    sys.exit(main())
