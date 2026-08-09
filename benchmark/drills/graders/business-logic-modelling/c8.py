#!/usr/bin/env python3
"""Criterion 8: `booking.api` is the way in, and the only way in.

Two halves. The module must import and carry the three types, and the
package must hold no other submodule that a caller could reach for. A
private helper module still counts: `booking._money` imports, so it is
exposed whatever its name suggests.

A file that is present but cannot be imported is reported separately.
It is still a fail, because the package was asked to hold one submodule
and holds two, but the reason should not claim the second one is
reachable when it is not.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import require_implementation, scratch_dir, settle  # noqa: E402

CID = "c8"

PROBE = '''
import importlib
import pkgutil

import booking
import booking.api

absent = [name for name in ("Money", "Booking", "Status")
          if not hasattr(booking.api, name)]
if absent:
    fail("booking.api imports but does not re-export %s" % ", ".join(absent))

others = sorted({info.name
                 for info in pkgutil.iter_modules(list(booking.__path__))
                 if info.name != "api"})

reachable, broken = [], []
for name in others:
    try:
        importlib.import_module("booking." + name)
    except Exception:
        broken.append(name)
    else:
        reachable.append(name)

if reachable:
    fail("booking exposes %s besides booking.api, and %s import cleanly"
         % (", ".join("booking." + n for n in others),
            "they" if len(reachable) > 1 else "booking." + reachable[0]))
if broken:
    fail("booking holds %s besides booking.api; %s does not import here, "
         "but the package was asked to carry one submodule and carries %d"
         % (", ".join("booking." + n for n in broken),
            "none of them" if len(broken) > 1 else "it", len(others) + 1))

ok("booking.api imports, re-exports Money, Booking and Status, and is the "
   "only submodule of booking")
'''


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)
    settle(CID, scratch, PROBE)


if __name__ == "__main__":
    main()
