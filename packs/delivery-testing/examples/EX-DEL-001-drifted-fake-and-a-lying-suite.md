---
summary: A worked run of the pack: a rounding defect, a drifted fake and a clock-dependent test, fixed in order
kind: example
scope: estate
type: example
tags: [delivery, testing, ci]
---

# EX-DEL-001: a drifted fake and a suite that lies

A composed example, not a venture record. It shows the pack applied end
to end on one task.

## The situation

A tariff sync service. Three things are wrong at once.

1. Standing charges are wrong by a penny for one class of tariff. The
   existing example test passes over it, because the expected value in
   the test was copied from what the code produced.
2. The service reaches a supplier API through a hand-written fake. The
   real API stopped returning a legacy `unit_price` field two releases
   ago; the fake still returns it, and code paths still read it. No
   contract suite exists.
3. One scheduling test asserts against the wall clock and fails about
   one run in four, most often after 23:00 and around the end of a
   month.

The task: fix the charge defect and make the suite trustworthy.

## Routing

Declared facts: touches money paths, no schema change, no external
sends. The router rules R2 on the money factor
(`kernel/POLICY_SPEC.md`). R2 means an independent oracle authored
before implementation and frozen, so WG-DEL-006 is decided before any
code is read: option C, and the oracle comes from the published tariff
rules rather than from the current output.

## What the pack said, fork by fork

| Fork | Wargame | Ruling here |
| --- | --- | --- |
| Oracle | WG-DEL-006 | C, plus D: rounding has an invariant |
| Timing | WG-DEL-007 | FIX cell, reproduction first |
| Double for the supplier API | WG-DEL-005 | C, verified fake with a contract suite |
| Flake response | Requirement 4 | Determinism first, no retries |

## The work, in order

1. **Reproduction first.** A failing test derived from the published
   tariff rules, asserting the charge for the affected class. It uses
   the public function only, no private attributes, no patching inside
   the module. Committed red, before the fix.
2. **The invariant, because one was available.** A property test over
   generated tariff inputs asserting the charge never rounds away from
   the customer, with a pinned seed in the gate. The property found a
   second input class the example test would have missed.
3. **The fix.** One rounding branch. The reproduction goes green and
   the property holds.
4. **The lying test.** The old example test asserted the wrong value.
   It was corrected against the published rules, and the correction is
   noted in the commit message. This is not weakening a check: the
   check was wrong about the specification, and the new oracle is
   independent of the code.
5. **The contract suite.** One file under `tests/contract/`,
   parameterised over the fake and the real client, running the same
   cases against both. Against recorded real responses it goes red for
   the fake immediately, on the case asserting that no legacy field
   comes back. The fake is corrected, then the reading code, then the
   suite goes green both ways. Cadence: nightly against the recording,
   with the recording refreshed monthly.
6. **The clock.** The scheduling test flakes because time is an ambient
   dependency. The clock becomes a port, injected, frozen in the test,
   with cases pinned at 23:59 and at a month end. Zero retries added.
   Twenty consecutive runs pass.
7. **No quarantine.** Nothing needed containing, so no quarantine
   record was written. Had the clock fix not landed this week, the
   record would carry an owner and an expiry inside thirty days.

## What was refused, and why

- Adding a retry to the scheduling test. Requirement 4, and it would
  have hidden the timezone bug that the frozen clock exposed.
- Deleting the old example test to make the suite green. Requirement 2.
  It was corrected against the specification instead.
- Mocking the supplier client in the unit tests to skip the fake
  problem. WG-DEL-005: mocking your own port hides drift rather than
  finding it.
- Raising the coverage floor because coverage happened to rise.
  Ratchets move in the change that earned the movement, and this change
  earned a rounding fix, not a floor.
- Adding a hosted flake-detection service. Nothing in the pack requires
  a vendor, and the fixes above are infrastructure the venture owns.

## What a reviewer checks

Revert the pricing file: the new test must go red. Point the contract
suite at the pre-fix fake: it must go red. Grep the diff for retries,
reruns and flaky markers: none. Confirm the new test reaches the code
through its public interface only. That is four mechanical checks, and
they are the ones in `packs/delivery-testing/CHECKS.md`.
