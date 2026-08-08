#!/usr/bin/env python3
"""Deprecation shim: forwards to python -m tools.eos.

The v1 checker was the parity anchor for the v2 port and is kept at
archive/v1-final:tools/eos_check.py as history. It cannot validate the v2
tree: it looks for doctrine modules and a wargame index that the pack
restructure retired. Every caller should move to the package.
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
