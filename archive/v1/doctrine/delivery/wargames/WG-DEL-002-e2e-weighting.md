---
summary: How much end-to-end, and which branch does it block?
type: wargame
tags: [delivery, testing, ci]
status: archived
review_by: 2027-07
---

# WG-DEL-002: How much end-to-end testing, and where does it gate?

## The question

End-to-end suites prove what unit tests cannot (the system, assembled,
against real services) and cost what unit tests never do (minutes per
run, environments, flake exposure). The fork is their weight in the
pyramid and the branch they are allowed to block.

## It depends on

- Whether a real local stack exists to run against (the harness
  decides the ceiling).
- Determinism: are external dependencies synthetic in CI?
- The cost of an escaped assembly bug (money, legal, trust) against
  the cost of a slower merge.

## Options

### A. Smoke only, advisory
A handful of route-loads and health checks, non-blocking. Cheap;
catches only catastrophe.

### B. Blocking on main, tiered below
Unit and integration gate every change; the full end-to-end suite
(smoke plus the acceptance journeys) blocks `main` merges only. Fast
inner loop, assembled proof before anything ships.

### C. End-to-end everywhere
The full suite on every push. Honest and slow; the queue it creates
becomes the reason it gets skipped.

## Decision rule

A real local stack and synthetic external modes exist: B, with the
acceptance journeys (the venture's §A5-style walk-through, where one
exists) encoded in the blocking set. No harness yet: A, and building
the harness is the standing foundation order. C only for ventures
whose merge rate is so low the queue cannot form.

## Default

B. Assembly proof gates the trunk; speed gates the loop.

## Worked rulings

- **WiseWattage (2026, argued)**: B. Python, node and docker jobs gate
  the dev branch; E2E smoke and the auth journeys against the local
  stack block `main` only, with synthetic weather for determinism.
- **Venture A (2026-07, argued by design)**: B mandated in its brief:
  the §A5 walk-through becomes the acceptance suite, failing first,
  skips lifted only as journeys go green end to end.
