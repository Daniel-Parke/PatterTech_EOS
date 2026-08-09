#!/usr/bin/env python3
"""Write dist/ from the sources.

Run it after any change to web/. Nothing else generates anything, so if
a file under dist/ disagrees with its source, the source is right and
this script has not been run.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "web", DIST)
    written = sorted(p.relative_to(DIST).as_posix()
                     for p in DIST.rglob("*") if p.is_file())
    for name in written:
        print("dist/%s" % name)
    return written


if __name__ == "__main__":
    build()
    sys.exit(0)
