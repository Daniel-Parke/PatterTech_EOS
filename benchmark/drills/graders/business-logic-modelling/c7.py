#!/usr/bin/env python3
"""Criterion 7: a hold taken across the clock change expires on real time.

01:40 on 2026-10-25 in Europe/London is ten minutes before the clocks
go back. Twenty real minutes later the wall clock reads 01:00 and forty
real minutes later it reads 01:20, both earlier than the moment the
hold was taken. A model that subtracts local labels therefore sees a
negative age and never expires the hold, which is the failure this
criterion exists to catch.

The same instant is asked again in UTC. A model whose answer depends on
how the caller happened to label the time fails there.

Without the IANA time zone database the criterion is left unsettled
rather than failed: nothing looked at the work.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BOOKING_SETUP, UNSETTLED, emit,  # noqa: E402
                     require_implementation, scratch_dir, settle,
                     zoneinfo_available)

CID = "c7"

PROBE = BOOKING_SETUP + '''
from zoneinfo import ZoneInfo

LONDON = ZoneInfo("Europe/London")
TAKEN = dt.datetime(2026, 10, 25, 1, 40, tzinfo=LONDON)


def later(minutes):
    """The instant `minutes` real minutes on, expressed in London time."""
    absolute = TAKEN.astimezone(dt.timezone.utc) + dt.timedelta(minutes=minutes)
    return absolute.astimezone(LONDON)


twenty, forty = later(20), later(40)
stay = a_hold(held_at=TAKEN)

early = stay.is_expired(twenty)
if early:
    fail("a hold taken at 01:40 on 2026-10-25 in London reports expired "
         "twenty real minutes later (%s), before the thirty minutes are up"
         % twenty.isoformat())

late = stay.is_expired(forty)
if not late:
    fail("a hold taken at 01:40 on 2026-10-25 in London is still unexpired "
         "forty real minutes later (%s). The clocks went back in between, "
         "so the wall clock reads %s, earlier than 01:40: the model is "
         "subtracting local labels rather than measuring elapsed time"
         % (forty.isoformat(), forty.strftime("%H:%M")))

as_utc = forty.astimezone(dt.timezone.utc)
if not stay.is_expired(as_utc):
    fail("the same instant handed over as %s does not report expired, so "
         "the answer depends on which zone the caller used to say it"
         % as_utc.isoformat())

ok("still held after twenty real minutes and expired after forty across "
   "the 2026-10-25 clock change, where the wall clock reads %s and %s"
   % (twenty.strftime("%H:%M"), forty.strftime("%H:%M")))
'''


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)
    if not zoneinfo_available():
        emit(CID, UNSETTLED,
             "the Europe/London zone is not available to this interpreter, "
             "so the clock change was never put to the model. That is a gap "
             "in the environment, not a finding against the delivered tree.")
    settle(CID, scratch, PROBE)


if __name__ == "__main__":
    main()
