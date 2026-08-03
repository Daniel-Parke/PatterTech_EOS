---
summary: The v2 build's final report, measured results, residual risks and the release decision Daniel owns
type: org
tags: [eos]
---

# EOS v2 final report

Written at the release checkpoint, revised 2026-08-03 after both corrective
iterations, and corrected 2026-08-04 by the pre-release review. The build is
pushed to `feat/eos-v2-agentic-development`. `main` is untouched. Nothing
here has been tuned to pass a gate.

**Read the 2026-08-04 corrections first.** The review found that three
statements in this report were stale or wrong, and that the gate table below
cannot be trusted as it stands. Both are recorded in place, under
"Corrections" at the end. The gate figures are left exactly as first
published so the record of what was claimed survives; what changed is that
the method behind them is now known, and one gate's verdict turns on an
unwritten convention.

## The decision this report is for

v2 passes three of the six numeric gates and misses three. Under the
approved plan a missed gate does not release, and the choice is Daniel's:
amend the thresholds by ADR with reasons, adopt partially, or halt with the
branch preserved. Both corrective iterations the plan allowed have now been
spent, so there is no third attempt on the table.

## Final gate table

| Gate | Threshold | First run | After corrections | Verdict |
| --- | --- | --- | --- | --- |
| Ceremony lines | 60 per cent fewer | 49 per cent | 58 per cent fewer | fail by two points |
| Context tokens | 30 per cent fewer | 64 per cent more | 8 per cent fewer | fail |
| Wall clock | 25 per cent faster | 49 per cent slower | 37 per cent slower | fail |
| Critical-task regression | none | none | none | pass |
| Aggregate quality | within 3 points | 100 against 96 | 96 against 96 | pass |
| Completeness | three trials a slot | met | met | pass |

Human gates left pending at the end of a run: v1 twelve, v2 zero. That
number did not move across any correction, and it is the finding I would
put above the rest.

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

## The twenty pack drills

Twenty cold agents, one per pack, each told that an honest negative was
worth more than a polite pass. Not one returned a clean pass, and the
criticism was mostly structural rather than about the doctrine:

- The drill specs ship no fixtures and no graders, so every agent built the
  scenario it was then judged against. Several said plainly that their own
  result should not be read as an independent pass. They are right.
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

None of that is fixed. It is a work list, and it is the most valuable
output of the drills.

## What has not been done

- The remaining policy ablations (wip1, mandatory-logs, no-sampled-review)
  are specified and frozen but not executed. The routing and timing
  ablations were run.
- The twenty pack drills were run by cold agents, but self-fixtured and
  self-graded, so they are evidence about the packs' usability and not an
  independent pass. Building real fixtures and graders for them is
  outstanding.
- The defects the drills found in six packs are recorded and unfixed.
- The sealed final suite has not been opened. It requires the private key
  Daniel holds, and by protocol it runs once, against frozen v1 and final
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
said "I have not taken it" and left the call with Daniel. That was written
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

The benchmark is being rebuilt before any gate is reported again: the
scorer written in code, the freeze manifest verified, the fourteen ledger
rows deleted by `2c7468d` restored as superseded, and the grid re-run
interleaved and timestamped. Nothing in the table above should be quoted
until that lands.
