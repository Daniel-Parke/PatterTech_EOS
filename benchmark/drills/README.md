---
summary: What a pack acceptance drill is, how the runner grades one, and what is still missing before any of the twenty can return a verdict
type: example
tags: [eos, testing]
---

# Pack acceptance drills

A drill is one cold-agent scenario with deterministic criteria. The
spec is frozen with its sha256 in `MANIFEST.json` and never changes
without an ADR amendment. A failed drill routes to fixing the pack and
re-running; it never routes to editing the spec.

Run them with `python -m tools.eos drills`. The contract is the drills
section of `tools/CLI_CONTRACTS.md`.

## What is frozen, and how strongly

Twenty specs, one per pack. Read `frozen_before_authoring` on every
entry in `MANIFEST.json` before you read a result:

- The **Wave A eight** were frozen before any of their pack content was
  authored. Their spec could not have been written to the pack, so they
  are independent oracles.
- The **Wave B twelve** were frozen on 2026-08-03, after their packs
  were authored and in the same commit as them. That is a weaker
  guarantee: the spec could have been written to suit the pack. A pass
  on a Wave B drill is worth less than a pass on a Wave A drill, and the
  manifest says so on each entry rather than leaving a reader to guess.

The freeze is byte-identical. Each spec is a straight copy of the
pack's own `research/DRILL_PROPOSAL.md`, and the manifest records the
source path so the copy can be checked.

## The three things a drill needs to run

The runner grades; it does not think. For a drill to return anything
other than `manual` it needs all three:

1. `<pack>.md`, the frozen spec, matching its recorded hash. Present
   for all twenty.
2. `scenarios/<pack>/`, the fixture tree the drill materialises into a
   scratch directory. **Absent for all twenty.** Every spec describes
   one; none was built.
3. `graders/<pack>/cN.py`, one grader per numbered criterion. **Absent
   for all twenty.** Every spec calls its criteria machine-checkable;
   the scripts that would check them were never written.

A grader follows the frozen benchmark criteria contract: `argv[1]` is
the scratch directory, it prints one JSON object
`{"id", "pass", "reason"}` and exits 0 on pass, non-zero on fail.

## Why every drill currently reports no verdict

With no scenario and no graders, every criterion is prose a human must
judge. The runner reports it as `manual`, does not count it as a pass,
and gives the drill a `pass` of `null` with the reason stated. It exits
1, because a drill that did not run is not a drill that passed.

There is also a fourth thing a drill needs that no command supplies:
the cold-agent session that does the work. `drills run` materialises the
scenario and grades a tree. Handing the scenario to an agent and
capturing what it delivers is the harness's job, and the graded tree
comes back through `--attempt DIR`. Running the command with no
`--attempt` grades the untouched fixture, which is worth doing once per
drill to prove the criteria discriminate, and is worth nothing as
evidence about a pack.

## The results ledger

`RESULTS.json` is append-only: one entry per drill per run, holding the
date, the pack, the per-criterion verdicts and the reason. Rows are
never rewritten or removed, and a `pass` of `null` is recorded as
plainly as a `false`.
