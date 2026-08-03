---
summary: Single-run cold-agent acceptance drill for the business logic and modelling pack, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# DRILL-BLM-001: the invariant holds, in money and in time

## Scenario

A cold agent gets the pack and an empty Python repository holding a
frozen harness at `harness/` and an empty package `booking/`. The
prompt is one line: "Model a room booking. It has a nightly rate in a
currency, a check-in and check-out date, and a status. It can be held,
confirmed, cancelled or completed. A held booking expires after 30
minutes. Total price is nights times rate. Expose `booking.api` and
nothing else."

Single run, no follow-up prompts. Pass requires all nine criteria, each
an exit code or a file check run by the frozen harness.

## Deterministic criteria

1. `python -m pytest harness/` exits 0 on the delivered tree.
2. Grep of `booking/**/*.py` finds no `float` annotation and no
   `float(` call, and the harness asserts the money type's internal
   amount is an `int`.
3. Money built from `(1099, "GBP")` and `(1099, "JPY")` renders
   `10.99` and `1099`, proving the minor-unit exponent is per currency
   and not fixed at two.
4. Arithmetic between a `GBP` and a `JPY` amount raises.
5. Constructing a booking with check-out on or before check-in raises
   at construction. A `validate` or `is_valid` method fails this.
6. Driving every ordered pair of statuses through the public API, only
   these succeed: held to confirmed, held to cancelled, held to
   expired, confirmed to cancelled, confirmed to completed. Every other
   pair raises, and none silently no-ops.
7. A hold created at `2026-10-25T01:40:00` in `Europe/London`, ten
   minutes before the clocks go back, is still held twenty wall-clock
   minutes later and expired after forty. Naive datetimes fail this.
8. `import booking.api` succeeds and re-exports the money, booking and
   status types; no other `booking.*` submodule is importable.
9. The dependency manifest lists nothing beyond the standard library
   and the harness pins: no rule engine, no state machine library.

## Fail conditions worth logging separately

- 5 fails while 1 to 4 pass: taught money, not invariant placement.
- 7 fails alone: taught currency, not time.
- 9 fails: taught the tool, not the threshold, since four statuses do
  not warrant an engine.
- All pass but the tree holds an aggregate root, a repository interface
  and an event bus: over-modelling, logged as a warning and counted.

## Freeze note

Criteria 1 to 9, the harness, the two currencies, the clock-change
instant and the transition matrix in criterion 6 are frozen before
content authoring and stored with the drill.
