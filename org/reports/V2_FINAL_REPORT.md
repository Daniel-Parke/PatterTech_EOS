---
summary: The v2 build's final report, measured results, residual risks and the release decision Daniel owns
type: org
tags: [eos]
---

# EOS v2 final report

Written at the release checkpoint, 2026-08-03. The build is complete and
pushed to `feat/eos-v2-agentic-development`. `main` is untouched. Nothing
here has been tuned to pass a gate.

## The decision this report is for

v2 misses three of the six numeric release gates. Under the approved plan
that means it does not release, and the choice is Daniel's: amend the
thresholds by ADR with reasons, adopt v2 partially, or halt with the
branch preserved. The evidence follows so the choice can be made on
numbers rather than on the fact that the work is finished.

## What was measured

Two variants, thirteen tasks each, three valid trials per slot, the same
fixtures and the same frozen criteria. 84 scored runs: 45 v1, 39 v2. The
v1 baseline ran before any v2 code existed, and its failures were
recorded unchanged.

| Gate | Threshold | Measured | Verdict |
| --- | --- | --- | --- |
| Ceremony lines | at least 60 per cent fewer | 49 per cent fewer | fail |
| Context tokens | at least 30 per cent fewer | 64 per cent more | fail |
| Wall clock | at least 25 per cent faster | 49 per cent slower | fail |
| Critical-task regression | none | none | pass |
| Aggregate quality | within 3 points of v1 | 100 per cent against 96 | pass |
| Completeness | three trials per slot | met on both sides | pass |

Human gates left pending at the end of a run: v1 twelve, v2 zero.

## What the ceremony median hides

The median is taken across all thirteen tasks, and it is dragged down by
tasks where v1 had almost no ceremony to remove.

- Heavy work, where v1 wrote 90 lines of paperwork or more: ceremony down
  65 per cent, tokens down 41 per cent. v2 wins on both.
- Light work, where v1 wrote under 20 lines: ceremony 7 per cent worse,
  tokens 107 per cent worse. v2 loses on both.

Per task, v2 removed 68 per cent of the paperwork on the feature, 69 per
cent on the bug fix, 62 per cent on the migration and 54 per cent on the
authorisation change, and took the spike and the trivial documentation
fix to zero. It added paperwork on the small UI fix and on inception.

## The finding that matters most

On every task above the ordinary risk line, v1 did not deliver. The work
reached VERIFY-approved on a branch and stopped, waiting for an operator
gate that never arrives in an autonomous run. That is v1's constitution
working exactly as written: a session may not merge its own R2-or-above
work. Across the baseline v1 left twelve outstanding human gates; v2 left
none, at equal or better quality.

This is not a small difference in convenience. It is the difference
between a process that finishes and one that queues.

## Why v2 costs more, honestly

v2 sessions read fewer files than v1 (a median of one or two against five
to twenty-two), so progressive disclosure is doing its job. They spend
more turns and more tokens anyway. Three causes, in the order I believe
they matter:

1. The benchmark instructed v2 sessions to route the task and consult the
   guard through the tooling. v1 sessions had no such instruction because
   v1 has no such tooling. Some of the measured cost is a real property of
   v2 (routing is not free) and some is an asymmetry the harness
   introduced. I have not separated the two, and I will not claim a number
   I have not measured.
2. Shell exploration replaced file reads. Fewer Read calls, more command
   output flowing back into context.
3. The v2 seeds and packs are larger than the v1 seeds, so the venture a
   session boots into carries more material even when little of it loads.

Cause 1 is testable with an ablation that runs v2 without the routing
instruction. That ablation has not been run.

## What has not been done

- The policy ablations (no-router, wip1, mandatory-logs, no-sampled-
  review) and the test-timing ablation are specified and frozen but not
  executed. The timing ablation is what sets the capability-profile
  testing defaults, so those defaults remain unset and the testing matrix
  stands as a default set rather than an evidence-set one.
- The pack acceptance drills are frozen with hashes but have not been run
  against the twenty built packs.
- The sealed final suite has not been opened. It requires the private key
  Daniel holds, and by protocol it runs once, against frozen v1 and final
  v2 together, after corrective iteration. Opening it now would spend the
  one shot before the corrective decision is made.

## Residual risks

- The three efficiency gates are unmet and the causes are diagnosed but
  not isolated. Adopting v2 on the strength of the heavy-task numbers
  means accepting that light work costs more.
- The semantic checks ship warning-first. 161 warnings stand, most of them
  metadata that predates v2 or archived v1 material. Flipping them to
  errors is a P4 intention that has not happened.
- The guard has no validated host enforcement adapter, so every guarded
  class is manual-only. That is the fail-closed state working as designed,
  but it means v2's autonomy claim is bounded: consequential actions still
  need a human hand.
- Venture A's migration is a recompile carrying 48 work orders. The plan
  reports it; nobody has run it.
- Two v1 seed fixtures carry a real D004 finding (deferrals with no
  scheduled lock-in). They are frozen v1 artefacts and were left as found,
  because they are evidence of the gap v2's checker closes.

## What I would do next

Run the routing ablation first. It is the cheapest experiment that could
change the decision, because it separates the cost of v2's design from the
cost of the way the benchmark asked for it. If routing is most of the
overhead, the honest options widen: route only above a tier floor, or
cache the routing verdict per task rather than per session.

If the ablation does not move the numbers, the finding stands as measured:
v2 buys delivery and removes paperwork on heavy work, and costs tokens and
time on light work.
