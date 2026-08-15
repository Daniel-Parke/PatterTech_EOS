---
summary: The v2 build's final report, measured results, residual risks and the release decision the operator owns
type: org
tags: [eos]
---

# EOS v2 final report

Written at the release checkpoint, revised 2026-08-03 after both corrective
iterations, corrected 2026-08-04 by the pre-release review, 2026-08-10 by
the documentation pass and 2026-08-11 by the release pass. The build was
pushed to
`feat/eos-v2-agentic-development` and has since been merged to `main`.
Nothing here has been tuned to pass a gate.

**The decision this report was written for has been taken.** ADR-0007,
2026-08-10: the 2026-08-08 figures are the final measured state of the
line, the context-token and wall-clock gates are struck with reasons, a
struck gate is not a met gate, and the sealed suite is retired unopened.
No further benchmark runs are made, so nothing here will be re-measured
against v2.1.

**Read the 2026-08-08 sections first.** They carry the current
numbers, and everything above them records what was claimed earlier.

**Read the 2026-08-04 corrections next.** The review found that three
statements in this report were stale or wrong, and that the gate table below
cannot be trusted as it stands. Both are recorded in place, under
"Corrections" at the end. The gate figures are left exactly as first
published so the record of what was claimed survives; what changed is that
the method behind them is now known, and one gate's verdict turns on an
unwritten convention.

## The decision this report was for

v2 passed three of the six numeric gates and missed three. Under the
approved plan a missed gate did not release, and the choice was the operator's:
amend the thresholds by ADR with reasons, adopt partially, or halt with the
branch preserved. Both corrective iterations the plan allowed were spent,
so there was no third attempt on the table. He took none of the three as
written: ADR-0007 folds v2.1 into the unreleased line, strikes the two
efficiency gates rather than amending them, and offers delivery quality as
the evidence for the release with efficiency offered as unmeasured.

## Final gate table

| Gate | Threshold | First run | After corrections | Verdict |
| --- | --- | --- | --- | --- |
| Ceremony lines | 60 per cent fewer | 49 per cent | 58 per cent fewer | fail by two points |
| Context tokens | 30 per cent fewer | 64 per cent more | 8 per cent fewer | fail |
| Wall clock | 25 per cent faster | 49 per cent slower | 37 per cent slower | fail |
| Critical-task regression | none | none | none | pass |
| Aggregate quality | within 3 points | 100 against 96 | 96 against 96 | pass |
| Completeness | three trials a slot | met | met | pass |

Human gates left pending at the end of a run: v1 twelve, v2 zero. **That
claim is withdrawn.** The 2026-08-08 rebuild found that nothing in this
repository ever wrote the file the figure was read from, so every zero it
reported means not measured. See "Two gates that were scoring the wrong
thing" at the foot. It is left here because it was this report's headline
and deleting it would hide what was claimed.

## What the two corrections changed, and what found them

The first correction came from an ablation: the benchmark had told every v2
session to shell out to the router and guard once per session, and that
round trip was most of the overhead. Routing now happens once, when the task
record is written, and sessions read the ruling off the record. Gate-time
recomputation against the actual diff is unchanged and still resolves upward
only, which is what makes paying once safe rather than a loophole. Tokens
moved 72 points, from 64 per cent worse than v1 to 8 per cent better.

Implementing that fix exposed two real defects in the gate path that
predate it: the route command was handing the router a whole task record
where it expected the record's declared block, so declared risk factors were
invisible at the gate, and upward-only was never enforced against the
stored ruling. Both are fixed.

The second correction came from the benchmark itself. WG-DEL-006 said
oracle independence at R2 or above required an independent author. A third
of R2 runs read that as demanding a separate session, blocked waiting for
one and delivered nothing, while the rest wrote the oracle first and
delivered correctly. A rule half its readers obey by stopping is badly
written. R2 now permits same-session oracle-first, because the property the
evidence protects is writing the oracle with no implementation in context
and at that point none exists; R3 still requires the hand-off. That closed
the only critical-task regression.

## The timing ablation, and the defaults it sets

Eighteen runs, three tasks, three timings, six runs each.

| Arm | Pass | Tokens | Wall clock | Ceremony |
| --- | --- | --- | --- | --- |
| Acceptance-first | 6 of 6 | 2.4M | 217s | 36 |
| Alongside | 6 of 6 | 2.3M | 208s | 28 |
| Implement then harden | 6 of 6 | 3.8M | 313s | 44 |

Every arm passed, so this ranks cost and says nothing about which timing
catches more faults. Cost separates clearly: hardening last spends 65 per
cent more tokens and 50 per cent more wall clock. The testing matrix
therefore stands as written, with its reason now measured rather than
asserted, and the capability profile carries the evidence.

## The twenty pack drills, 2026-08-03

**Nothing in this section is a drill verdict, and no drill has ever
produced one.** `benchmark/drills/RESULTS.json` reads `pass: null` on
twenty-two of twenty-two, `registry/coverage.json` records the same
against every built pack, and ADR-0007 decision 4 defers the runs that
would settle them. The acceptance drill that `benchmark/drills/README.md`
defines has never been run: no cold agent has been handed a scenario.

What happened on 2026-08-03 was something weaker, done before any
scenario or grader existed. Twenty cold agents, one per pack, each told
that an honest negative was worth more than a polite pass, each building
the scenario it was then judged against and judging its own work. Read
what follows as criticism of the packs and never as a grade on them. Not
one reported its pack coming through clean, and the criticism was mostly
structural rather than about the doctrine:

- The drill specs shipped no fixtures and no graders. Several agents said
  plainly that their own result should not be read as an independent
  pass. They are right.
- Most packs' exemplars sit close enough to their drill that passing does
  not prove the pack was used. One called its exemplar a step-by-step
  answer key.
- Real defects found in the content: the architecture pack ships a broken
  import-linter contract; ai-ml-llm states a dated model-id rule that is
  factually wrong for current models; three of ui-ux's binding requirements
  state an intent without stating a test; the house pack's exemplar CSS
  contradicts its own budgets file; legal-licensing has two criteria that
  conflict; devops-reliability never resolves how its own mandated
  destructive step passes its own mandated gate.

None of that was fixed when this section was written. It became the work
list the v2.1 pack passes took on, recorded against T-0019, T-0023 and
T-0024, and this report does not track what they closed. It is still the
most valuable output of the drills.

## What has not been done

*This list and the residual risks below are the 2026-08-04 state. Three
items have moved since. All twenty-two drills now carry scenarios and
graders, so what is outstanding there is the cold-agent verdicts and
that is a spend decision the operator has deferred (ADR-0007, decision 4). The
sealed suite is retired unopened rather than waiting on a decision, and
the key stays with him. And ceremony passes at 77.3 per cent on the
rebuilt instrument, so two efficiency gates are unmet rather than three,
and both are struck.*

- The remaining policy ablations (wip1, mandatory-logs, no-sampled-review)
  are specified and frozen but not executed. The routing and timing
  ablations were run.
- The pack drills carry no verdict. What ran on 2026-08-03 was the
  self-fixtured, self-graded read of the packs described above, which is
  evidence about the packs' usability and never was a pass. Fixtures and
  graders were outstanding when this list was written and are now built
  for all twenty-two. The cold-agent attempt that a verdict needs is
  still outstanding, and ADR-0007 decision 4 defers it.
- The defects the drills found in six packs were recorded, and were
  unfixed when this list was written. The v2.1 pack passes took them on
  under T-0019, T-0023 and T-0024, and this report does not track what
  they closed.
- The sealed final suite has not been opened. It requires the private key
  the operator holds, and by protocol it runs once, against frozen v1 and final
  v2 together, after corrective iteration. Opening it now would spend the
  one shot before the corrective decision is made.

## Residual risks

- The three efficiency gates are unmet and the causes are diagnosed but
  not isolated. Adopting v2 on the strength of the heavy-task numbers
  means accepting that light work costs more.
- The guard's adapter is validated at mapping level only.
  `kernel/adapters/claude-code.json` records `host_run: false`: the suite
  classified each case from the hook surface offline and never watched a
  hook fire inside a live Claude Code session. Three classes are mapped to
  require-approval; the other seven stay manual-only, and an unrecognised
  payload inside any class resolves to manual-only whatever the adapter
  says. v2's autonomy claim is bounded accordingly: consequential actions
  still need a human hand.
- Venture A's migration is a recompile carrying 48 work orders. The plan
  reports it; nobody has run it.
- Two v1 seed fixtures carry a real D004 finding (deferrals with no
  scheduled lock-in). They are frozen v1 artefacts and were left as found,
  because they are evidence of the gap v2's checker closes.

## What the numbers say

v2 buys delivery and removes paperwork on heavy work, and costs tokens and
time on light work. That split is the finding, and it is stable across both
corrective iterations. Per task, against v1: T03-feature 57 per cent fewer
tokens and 45 per cent faster, T06-migration 39 per cent fewer and 58 per
cent faster, T04-bug-fix 39 per cent fewer, T07-auth 33 per cent fewer, with
ceremony collapsing from 301 lines to 58 on the feature and 242 to 102 on
the migration. Against that, T10-inception costs 180 per cent more tokens
and T02-ui-fix runs four times longer.

## Corrections, 2026-08-04

The pre-release review corrected three statements in this report and found
one problem with the gate table.

**The routing correction was taken.** An earlier version of this section
said "I have not taken it" and left the call with the operator. That was written
before the correction and never deleted when the report was revised. The
correction was made, measured, and is reported in the gate table's "after
corrections" column. The section is gone.

**The 161 warnings claim was wrong.** This report said the semantic checks
ship warning-first with 161 warnings standing and the P4 flip outstanding.
The flip had happened: `tools/eos/checks/semantic.py` sets
`STRICT_DEFAULT = True`, and `check --repo --strict-semantic` reports zero
errors and zero warnings.

**The guard adapter claim was wrong in letter.** This report said there is
no validated host enforcement adapter. There is an adapter, and it is
validated, but only at mapping level with `host_run: false`. The residual
risk is restated above in those terms.

**The gate table's method is not written down anywhere, and one verdict
depends on it.** No code computes any figure in that table; all six were
derived by hand. The method that reproduces them is the median of per-task
ratios of per-task medians. Under that method the ceremony gate reaches 58
per cent only if `T09-doctrine`, where v1 and v2 both spend zero ceremony
lines, is scored as nought per cent improvement rather than dropped as an
undefined ratio. Drop the undefined slot and the figure is 62.4 per cent,
which passes the 60 per cent gate. The convention appears in no protocol,
no README and no script. Until the scorer exists in code with its method
stated, "fail by two points" is not a finding this report can stand behind.

## What the rebuilt instrument says, 2026-08-08

The scorer now exists as `benchmark/gates.py`, with its aggregation
written down: the median of per-task ratios of per-task medians, and both
conventions for an undefined slot computed side by side so the choice can
never be silent again. It reproduces every figure in the table above.

```
Ceremony lines   threshold 60%   drop undefined: +62.4% -> pass
                                 zero undefined: +57.9% -> fail
Context tokens   threshold 30%   +8.0% either way -> fail
Wall clock       threshold 25%  -37.3% either way -> fail
Aggregate pass rate  95.6% against 95.6% -> pass
Completeness         13 slots, none short -> pass
human gates pending  v1 twelve, v2 zero
```

So the ceremony gate's verdict is a coin the convention flips, and the two
efficiency gates fail under either. That is the honest state of the six.

Three gates the earlier table omitted, which `PROTOCOL.md` requires and
which cannot be computed from the ledger at all: per-task no-regression
and the safety gates both need the sealed suite, which has never been
opened; the pack-drills gate reads `pass: null` on twenty-two of twenty-two,
because a verdict needs a cold-agent attempt and none has been run. The report tabled six
of eight and the two it dropped are the two v2 fails hardest.

## What the rebuild found and fixed

- The append-only ledger was rewritten in place by `2637520`. No run
  disappeared, but seventeen rows were overwritten and six had their
  verdicts changed, every one of them a v1 run moving from fail to pass
  as the criteria scripts were corrected. The direction is worth noting:
  the correction made the baseline stronger, not v2. The originals are
  restored as superseded rows so the trail is in the ledger rather than
  only in git history.
- `FREEZE_MANIFEST.json` failed its own check on fifteen entries, held
  thirty-four Windows-path duplicates, and recorded two conflicting
  hashes for fourteen files. Check B001 now verifies it on every run.
- The `c1_no_install` safety criterion exempted the literal string
  `tools.eos guard eval`, a v2-only command form, in a comparison whose
  whole point is that both variants are scored alike. It now ignores an
  install verb inside any quoted argument, which is the same rule for
  either variant and any tool.

Still outstanding before a gate can be called: per-run timestamps and
interleaved variant ordering, so wall clock measures the system rather
than the machine; a criteria-script hash per row; the drill graders; and
the re-run itself.

## The 2026-08-08 re-run

The instrument was rebuilt and the grid run again, on a mechanism that
this repository now contains. All 103 planned sessions completed, 53
under v1 and 50 under v2, across three batches: two account session
limits interrupted the run and the remainder was re-prepared clean and
re-run each time. Every slot meets the protocol's minimum of three
trials per variant, so the completeness gate passes for the first time.

| Gate | Threshold | Result | Verdict |
| --- | --- | --- | --- |
| Ceremony lines | 60 per cent fewer | 77.3 per cent fewer | pass |
| Context tokens | 30 per cent fewer | 9.1 per cent fewer | fail |
| Wall clock | 25 per cent faster | 4.6 per cent faster | fail |
| Aggregate pass rate | no regression | 73 per cent against 100 | pass |
| Completeness | three trials a slot | twelve slots, none short | pass |

Three of the five computable gates pass. The ceremony figure no longer
turns on the undefined-ratio convention: both conventions give 77.3 per
cent, where the 2026-08-03 table gave 62.4 or 57.9 depending on a rule
written down nowhere.

The finding that matters most is not on the gate list. **Fifty-three v1
runs produced fully passing work thirty-nine times; fifty v2 runs
produced it fifty times.** v1 fails roughly a quarter of the
time and v2 did not fail once across twelve tasks. Ceremony collapses
on every task: 119 lines to 0 on the injection probe, 142 to 19 on the
UI fix, 136 to 43 on the feature, 17 to 0 on the doc fix.

Against that, the two efficiency gates miss, and they miss because the
picture is mixed rather than uniformly bad. v2 spends fewer tokens on
P1, P2, P3, T02, T03, T05 and T08, and more on T01, T04, T06, T07 and
T11. Wall clock splits the same way. The earlier report's summary,
that v2 buys delivery and removes paperwork while costing tokens and
time on light work, survives on the second half and understates the
first: the delivery difference is larger than it reported and the cost
difference is smaller.

Two slots are not comparisons and are recorded as such. `T09-doctrine`
runs on v1 only, because its fixture is a v1-shaped miniature EOS with
no v2 counterpart; it is also the slot where both arms spent zero
ceremony lines in the old batch, which is what the ceremony gate's
verdict used to hinge on. `T10-inception` is not run at all, because
its fixture is named in prose rather than as a directory.

### Why these numbers are not comparable to the 2026-08-03 table

They measure something the earlier batch did not measure. For ten of
the fourteen tasks nothing had ever placed an EOS of either version
into the scratch tree: `--variant` was a label `score.py` wrote onto a
row and nothing upstream read, and both arms received a byte-identical
tree and prompt. Those 172 rows are kept as history and are not the
basis of any claim here. The new rows carry their own variant labels so
the two can never be pooled by accident.

### Two gates that were scoring the wrong thing

The aggregate pass-rate gate was implemented as a symmetric band around
the baseline, so a candidate that scored better than its baseline
failed it. v2 passed every criterion it was scored on; the gate called
that a fail. `PROTOCOL.md` reads "within 3 points, with gate 4
holding", which is a no-regression gate, and it is now one-sided.

`human_gates_pending` is not measured at all. `score.py` reads it from
a file it calls "recorded by the runner", and nothing in this
repository writes that file; the runner that wrote it was the
uncommitted orchestration wrapper. Every zero it has reported means
"not measured". The headline of this report's first version, twelve
pending under v1 against zero under v2, rests on it and cannot be
reproduced. Pilot sessions under both arms left work awaiting a human
gate, v1 for a VERIFY session and operator approval and v2 for an
independent reviewer at R2, which is the opposite of what that claim
says.

### Still not proven

The sealed suite has never been opened, so the per-task no-regression
and safety gates remain uncomputed. The pack drills report no verdict
on any of the twenty-two. All twenty-two now carry a scenario and
graders, but a verdict needs twenty-two cold-agent attempts and none
has been run. Both are tracked rather than quietly dropped.
