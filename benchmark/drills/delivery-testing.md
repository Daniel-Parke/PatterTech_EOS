---
summary: Cold-agent acceptance drill for the delivery, testing and quality pack, checking double choice, contract verification and flake handling
type: example
tags: [eos]
---

# DRILL: delivery-testing acceptance

Single run, one cold agent, no human turns. Frozen before content
authoring.

## Setup

A small Python service with three seeded problems:

- `pricing.py` computes a discounted total; the rounding branch is wrong
  for one input class, and an example test passes over it.
- `gateway.py` reaches a payment API through `FakeGateway` in
  `fakes.py`. The fake returns a field the real client no longer
  returns, so it has drifted. No contract suite exists.
- `tests/test_schedule.py` asserts on the wall clock and fails roughly
  one run in four.

## Task given to the agent

"Fix the pricing defect and make the suite trustworthy. Follow the
delivery, testing and quality pack."

## Machine-checkable criteria

All checks run by `tools/drill_delivery_testing.py` against the working
tree after the run. Pass requires all nine.

1. `pytest -q` exits zero on a clean checkout of the agent's tree.
2. The pricing fault is fixed: the hidden oracle suite in
   `.drill/oracle/test_pricing_oracle.py` passes.
3. A new test exists that fails against the original `pricing.py`
   (checked by reverting the file and rerunning the agent's tests, which
   must exit non-zero).
4. That new test does not import from or reference `pricing.py`
   internals beyond the public function name (AST check: no attribute
   access on private names, no monkeypatching inside the module).
5. A contract suite file matching `tests/contract/test_*gateway*.py`
   exists and is parameterised over both `FakeGateway` and the real
   client class (AST check for both symbols reachable from the same
   parameterisation).
6. Run against the recorded real-client responses in
   `.drill/oracle/real_gateway_recording.json`, that suite fails for
   `FakeGateway` as committed, proving it detects the drift.
7. The temporal flake is fixed by controlling time, not by retry: zero
   additions of `flaky`, `rerun`, `retries` or `--reruns` in the diff or
   config, and `tests/test_schedule.py` passes twenty runs in a row.
8. Any quarantine record names an owner and an ISO expiry within 30
   days; no quarantine also passes, a bare quarantine fails.
9. No new commercial or hosted-service dependency in `pyproject.toml`
   or CI config.

On failure the harness logs the failed criterion number, the diff and
the pytest output.
