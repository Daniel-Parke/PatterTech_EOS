---
summary: Flake sources, the determinism budget, the quarantine record and why retries are not a policy
kind: recipe
scope: estate
sources: [EV-0015, EV-0090, EV-0093, EV-0195, EV-0196]
type: example
tags: [delivery, testing, ci]
---

# Flake and determinism, in practice

Reference material for binding requirement 4. The argument is in
WG-DEL-004; this is the mechanics.

## Where flake comes from

Flakiness tracks test size and dependency count more than author
discipline. Across roughly 4.2 million tests, likelihood of flaking
rose broadly with binary size and with the number of dependencies, and
heavy harnesses such as device emulators were worst (EV-0196). The
cheapest control is a smaller test that touches less, before any
tooling is considered.

The recurring sources, and the fix that removes the class rather than
the instance:

| Source | Fix |
| --- | --- |
| Wall clock, timezones, month ends | Inject the clock; freeze it in tests |
| Randomness, unordered iteration | Seed it; sort before asserting |
| Live external calls | A synthetic or offline mode built into the adapter |
| Shared state between tests | Isolation per test, fresh fixtures |
| Fixed sleeps waiting for readiness | Wait for the condition, not the clock |
| Downloads at test time | Pin and cache the artefact in the image |
| Shared long-lived environments | A throwaway container per run (EV-0093) |
| Unseeded generated inputs in a gate | Pin the seed in the gate |

Each fix lands once, in infrastructure, so every test inherits it. A
fix applied per test is a fix you will apply again next month.

## Retries

Blocking gates run zero retries. Retry-on-failure can mask a genuine
race condition, and a runner that reports passed, flaky and failed as
separate states gives you the honest picture without hiding anything
(EV-0015). Flaky is a reported outcome, not a silent one.

A scheduled job may retry to keep a signal readable. A gate may not,
because a gate that sometimes means try again stops meaning anything.

## The quarantine record

When a flake cannot be root-caused this week, it leaves the blocking
path with a record. Bare quarantine is worse than no quarantine,
because it looks like a decision.

```yaml
# tests/QUARANTINE.yaml
- test: tests/test_schedule.py::test_next_run_crosses_midnight
  reason: asserts against the wall clock; needs the clock injected
  owner: daniel
  quarantined: 2026-08-03
  expires: 2026-08-24
  issue: T-0042
```

Required fields: the test, the reason, a named human owner, the date it
entered, and an ISO expiry no more than thirty days out. An expired
record, an unowned record or a record with no reason is a finding. The
list is reviewed at retro, and a test that has been quarantined twice
gets deleted or rewritten rather than quarantined a third time.

## What quarantine costs

It suppresses signal along with noise. One Google team found that when
a previously stable test turned flaky, the cause was a genuine
production defect roughly one time in six (EV-0195). So the first
question about a newly flaky test is whether the product broke, and
quarantine is the answer only after that question has been asked.

Quarantine also presumes somebody is funded to drain the queue. Where
nobody is, the expiry date is doing all the work, which is why it is
required rather than suggested.
