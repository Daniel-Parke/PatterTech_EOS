---
summary: Frozen benchmark protocol for the EOS v1 versus v2 comparison, session counts, gates, custody and budget
type: example
tags: [eos, testing]
---

# Benchmark protocol (frozen)

This protocol is frozen before any scored run. Changes after the first
scored session require a new protocol version and a restart of the
affected slots. The point of freezing is simple: if we tune the test
while running it, the result tells us nothing.

## Model and tool settings

- Model pin: `claude-fable-5` for every scored session, both variants.
- Fresh session per run. No carried context, no resumed conversations.
- Default permission mode. No extra MCP servers beyond the stock set.
- One task per session. The session ends when the agent declares done
  or the operator stops it.

## How a variant reaches the scratch tree

Added 2026-08-08. Until then this protocol said nothing about it, and
neither did any code: `--variant` was a free-text label `score.py`
wrote onto a ledger row, and nothing upstream read it. Ten of the
fourteen tasks use a fixture that carries no process files at all, so a
v1 session and a v2 session on those tasks received a byte-identical
tree and a byte-identical prompt. The sessions behind the 2026-08-03
rows were driven by an orchestration wrapper that was never committed,
so those rows cannot be reproduced from this repository.

A run is now prepared by `benchmark/harness.py prepare`, and the
variant reaches the tree one of two ways, recorded per run in
`<run_id>.run.json` beside the tree:

- **paired**: the fixture is a seeded venture that already carries its
  own EOS, so the two arms are two fixtures. `seed-v1-S` pairs with
  `seed-v2-S`, `seed-v1-M` with `seed-v2-ORG`.
- **overlaid**: the fixture is a bare application, so the variant's
  process surface is copied onto it from `benchmark/surfaces/<variant>/`.

The surfaces are not authored for the benchmark. They are the frozen
paired seeds copied verbatim, with the venture identity replaced by a
slot, and the seeds are compiled output of each version's own kernel
templates. The ceremony difference between the arms is therefore
whatever the two kernels already produce, not a choice made by whoever
built the harness. That matters because the ceremony gate measures
exactly that difference. Venture content is excluded and written
identically into both arms, so nothing about the venture can differ.

The donors are the M and ORG scale seeds, decided by measurement: on
the S-scale seeds a pilot of T04 wrote nine ceremony lines under v1
where the 2026-08-03 ledger recorded a median of 206. S carries one
running log; M carries `org/roles/PLAN`, `WORK` and `VERIFY` with
`org/logs`, `org/STATE` and `org/QUEUE`, which is the three-session
ceremony v2 claims to collapse.

Two slots cannot be run as comparisons and are not pretended to be.
`T09-doctrine` uses `eos-mini`, a v1-shaped miniature EOS with no v2
counterpart, so it runs on one arm; it is also the slot where both
arms spend zero ceremony lines, whose handling decides the ceremony
gate. `T10-inception` names its fixture in prose rather than as a
directory and cannot be materialised.

## Counterbalancing in practice

`harness.py grid` emits the whole run in a seeded shuffle and records
the seed with the plan. The requirement below was not met by the
2026-08-03 batch: every v1 run happened, then every v2, then the
corrected v2 arm, which is why that batch's wall-clock figure cannot
be attributed to the system rather than to machine load.

## Planned session counts

- Critical tasks T03, T04, T06 and T07 run at k=5 per variant.
- The six other tasks run at k=3 per variant.
- Probes P1 to P3 run at k=5 per variant.
- That gives 53 sessions under v1 and 50 under v2, 103 across the two,
  because T09-doctrine has no v2 arm.
- Policy ablations: 4 ablations x 4 tasks x 3 trials = 48 sessions.
- Timing ablation: 3 timings x tasks T02, T03, T04 and T11 x k=3 = 36
  sessions.
- Roughly 20 pack drills come later, after the main grid.
- Corrective reruns are additional and are counted against the budget.

## Minimum release-qualifying floor

Three valid trials per slot per variant is the floor. The kernel
minimum is 78 sessions. Any slot below its minimum means the benchmark
is incomplete and no release decision can be made from it.

## Counterbalancing

Task order is split across trials between forward and reverse order,
and v1 and v2 sessions alternate, so drift in the environment or the
operator lands on both variants evenly.

## Early stopping

A slot may stop at 3 trials when both conditions hold:

1. All trials passed their criteria.
2. For every metric, the range across trials is at most
   max(15 percent of the median, floor), where the floors are 10k
   tokens, 3 minutes wall clock, 5 ceremony lines and 1 operator event.

Otherwise the slot runs to its planned k.

## Budget

The cap is 65M tokens, inclusive of corrective reruns and scoring.
At 80 percent spend, the remaining budget is reserved for critical
minima only. If the budget runs out with any slot below minimum, the
benchmark is incomplete and there is no release.

## v1 baseline discipline

v1 failures are recorded unchanged and never fixed. Fix-and-restart
applies to v2 runs only. The baseline is the baseline; patching it
mid-benchmark would make the comparison worthless.

## Release gates

Per the ADR-0002 plan, all eight gates must pass:

1. Ceremony: at least 60 percent median reduction in ceremony lines.
2. Tokens: at least 30 percent median reduction.
3. Wall clock: at least 25 percent median reduction.
4. Per-task no-regression on T03, T04, T06 and T07 and the probes,
   scored with the sealed evaluation.
5. Aggregate pass rate within 3 percentage points, with gate 4 holding.
6. Safety gates pass.
7. Completeness: every slot at or above its minimum.
8. Pack drills pass.

## Sealed custody

- A separate evaluator-author session writes the sealed suite.
- The suite is encrypted with public-key encryption. the operator holds the
  private key and provides it only to the final evaluator, after
  implementation and diagnostic correction are complete.
- Only the ciphertext hash and an opaque handle are committed.
- The sealed suite runs once against frozen v1 and once against final
  v2 in the same window. Neither result is exposed until both are
  scored.
- A failed sealed run means stop, or freeze a replacement unseen suite.
  Never tune and re-run against a suite that has been seen.

## Diagnostic holdout

`benchmark/holdout/` is excluded from materialisation. It is used for
timing-ablation scoring and diagnostic regression detection. It is
visible to the build side, and that visibility is recorded as a known
limitation of the diagnostic results.

## Operator interaction and the METR caveat

Operator interaction is counted from harness events only, never from
recollection. Perceived speed is never accepted as evidence; only
measured wall clock and token counts count, following the METR finding
that developers misjudge their own speed-up.

## Assumptions to replace with actuals

- Token pricing is assumed, to be replaced with billed figures.
- Per-session token bands are estimates until the first scored batch.
