---
summary: The kernel in v2, the law files and the compile contract
type: kernel
tags: [eos]
---

# Kernel

The law and the seed material. Session 0 compiles a venture out of this
directory and stops; the venture then owns its copies. Nothing here is
edited by a venture, and nothing here runs: the code that reads these
files lives in `tools/eos/`.

A venture does keep reaching back. Its lock-book pins `eos_root` and
`eos_commit`, and it resolves the schemas, the scale matrix and the
packs it adopted at that commit, which is what makes an upgrade a diff
against a pin rather than a guess.

## What lives here

- The law the templates instantiate: `POLICY_SPEC.md` (the risk model
  and the factor table the router rules from), `GUARD_SPEC.md` (the
  action-time guard), `METADATA_SPEC.md` (the knowledge metadata axes).
- `SCALE_MATRIX.md`, the file list per scale, and `SEED_RUBRIC.md`, the
  gate a compiled seed must clear.
- `schemas/`, one JSON Schema per machine file or command output:
  policy, task record, claims, guard action, capability profile,
  coverage, evidence, lesson, migration state, and two that document
  the frozen benchmark.
- `templates/`, every file a seed can contain, plus `adapters/`, the
  host enforcement mappings the guard reads.

`SCALE_MATRIX.md` is the only place that says which template lands
where, at which scale, and how many files a seed comes to. It is not
restated here, because the copy that used to live here went stale.

## Scale in v2

Two seeds, S and ORG; v1's M and L merge into ORG. The seed check
parses the matrix out of `SCALE_MATRIX.md`. The v1 matrix, with its S,
M and L columns, is at `archive/v1-final:kernel/SCALE_MATRIX.md`, and a
seed resolves whichever matrix its pinned commit carries, so a venture
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

This content is unreleased law until Daniel approves the release.
ADR-0002 records what was approved for implementation. ADR-0007 settles
what the release gate now is, and strikes the two benchmark gates that
can no longer be computed. The v1 template set this replaces is
preserved in git history.
