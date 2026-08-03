---
summary: The kernel in v2, the law files and the compile contract
type: kernel
tags: [eos]
---

# Kernel

The organisational machinery Session 0 compiles into each venture.
Ventures get compiled copies stamped with the EOS version they came
from; nothing here is read by a venture at runtime.

## What lives here

- Law the templates instantiate: `kernel/POLICY_SPEC.md` (the risk
  model and factor table), `kernel/GUARD_SPEC.md` (the action-time
  guard), `kernel/METADATA_SPEC.md` (the metadata axes).
- Schemas under kernel/schemas/ for every machine file: policy, task
  records, claims, guard actions, capability profiles, coverage,
  evidence, benchmark, migration.
- Templates under kernel/templates/: the router, operators guide,
  brief, lock-book, compile report and feedback file at every scale;
  the constitution, the three charters (EXECUTOR, ORACLE, REVIEWER),
  the policy and cadence instances, the testing law, the artefact
  shapes, the playbooks and the boot file for the ORG seed; the task
  list for S.
- `kernel/SEED_RUBRIC.md`, the pass gate a compiled seed must clear.

## Scale in v2

Two seeds: S at nine files and ORG at nineteen; v1's M and L merge
into ORG. `kernel/SCALE_MATRIX.md` holds the v2 law and the seed check
parses it there. The swap happened once the v1 baseline scoring that
depended on the old matrix completed; the v1 matrix, with its S, M and
L columns, is at `archive/v1-final:kernel/SCALE_MATRIX.md`. A seed
resolves whichever matrix its pinned commit carries, so a venture
pinned before the swap still checks against v1's.

## The compile contract

- Templates are hand-written. The compiler (an agent following
  `inception/COMPILE.md`) fills slots and prunes fences; it never
  authors.
- Slots look like `{{PRODUCT_DOCTRINE}}` and are filled from the
  brief and lock-book; a compiled file with an unfilled slot fails
  the seed check.
- Scale fences are `<!-- scale: S -->` and `<!-- scale: ORG -->`,
  closed by `<!-- scale: end -->`. The compiler keeps a fenced body
  only for the ruled scale and always removes the marker lines; a
  leftover marker of either kind fails the seed check.
- JSON seed files follow the same contract: the policy and cadence
  files compile from their templates, the claims file is seeded
  empty per its schema, and every one gets an ancestry row in the
  compile report.
- Every compiled file traces to a template, a schema or an authored
  row in the compile report; anything untraceable is a compile
  failure.

## Concurrency doctrine

One mechanism: claims assigned by the integrator and committed
before worker dispatch. No live mutable coordination file, no
check-then-acquire, no lock files in a shared tree. Liveness comes
from harness task state or a recorded PID; a timestamp alone never
authorises taking a claim. Unscheduled concurrent sessions are
refused and their work is quarantined for the integrator to adopt or
discard.

## Status

The v2 kernel content is staged on the integration branch. It is not
released law until the benchmark gates pass and Daniel approves
release; ADR-0002 records what was approved for implementation. The
v1 template set this replaces is preserved in git history.
