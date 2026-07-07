---
summary: When a test flakes: retry, quarantine, or root-cause now?
type: wargame
tags: [delivery, testing, ci]
status: active
review_by: 2027-07
---

# WG-DEL-004: What happens when a test flakes?

## The question

A flaking test is a gate lying some of the time, and every response
teaches the organisation something. Retries teach that red sometimes
means try again; deletion teaches that gates are negotiable. The fork
is the sanctioned response, decided before the first flake rather than
during it.

## It depends on

- Whether the flake source is the venture's own determinism debt
  (live external calls, unpinned rendering, time and randomness) or
  genuine environmental noise.
- The gate it sits in: a blocking main gate can afford zero lies.
- Whether an owner exists to fix root causes this week.

## Options

### A. Automatic retries
Run it again until green. Masks the signal, normalises the lie, and
the flake population only grows.

### B. Quarantine with a deadline
The flaking test moves to a non-blocking quarantine list with an order
filed and a deadline; the gate stays honest, the test stays visible,
and quarantine is shameful enough to shrink.

### C. Determinism first, zero retries
Retries set to zero; every flake is treated as a determinism bug and
root-caused now: synthetic modes for external calls, pinned renderers,
no CDN downloads in CI, seeded randomness, frozen clocks.

## Decision rule

C is the posture: build the determinism budget in (the stack profiles
carry the estate's known fixes) and keep retries at zero on blocking
gates. When a flake cannot be root-caused this week, B contains it:
quarantine, order, deadline, never silence. A is forbidden on blocking
gates; a scheduled job may retry, a gate may not.

## Default

C with B as the containment valve. A red gate means something is
wrong; keeping that sentence true is worth real engineering.

## Worked rulings

- **WiseWattage (2026, argued)**: C. Playwright retries zero, CI on
  the runner's preinstalled Chrome after the CDN download stalled
  whole job budgets, synthetic weather mode for offline determinism;
  each fix landed as infrastructure, not as a retry count.
