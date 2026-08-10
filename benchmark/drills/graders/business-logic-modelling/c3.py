#!/usr/bin/env python3
"""Criterion 3: the minor-unit exponent is per currency, not fixed at two.

`Money(1099, "GBP")` renders `10.99` and `Money(1099, "JPY")` renders
`1099`. The yen is the whole criterion: a model that divides by a
hundred renders `10.99` for both and is wrong in a way no sterling test
can see.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import settle, require_implementation, scratch_dir  # noqa: E402

CID = "c3"

PROBE = '''
from booking.api import Money

sterling = str(Money(1099, "GBP"))
yen = str(Money(1099, "JPY"))

if sterling != "10.99" and yen != "1099":
    fail("Money(1099, 'GBP') renders %r and Money(1099, 'JPY') renders %r; "
         "wanted '10.99' and '1099'" % (sterling, yen))
if sterling != "10.99":
    fail("Money(1099, 'GBP') renders %r, not '10.99'" % (sterling,))
if yen != "1099":
    if yen == sterling:
        fail("Money(1099, 'JPY') renders %r, the same as sterling, so the "
             "exponent is fixed at two rather than read off the currency"
             % (yen,))
    fail("Money(1099, 'JPY') renders %r, not '1099'" % (yen,))
ok("1099 renders as 10.99 in GBP and 1099 in JPY, so the exponent comes "
   "from the currency")
'''


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)
    settle(CID, scratch, PROBE)


if __name__ == "__main__":
    main()
