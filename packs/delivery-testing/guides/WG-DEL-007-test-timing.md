---
summary: What has to exist before work fans out, and when checks get written relative to the code
kind: guide
scope: estate
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0003, EV-0006, EV-0007, EV-0016, EV-0053, EV-0178, EV-0192, EV-0194]
review: 2028-03
type: wargame
status: active
tags: [delivery, testing, ci]
---

# WG-DEL-007: What has to exist before work starts?

## The question

This guide used to ask when tests get written. That was the wrong
question at the top. Ordering is the least load-bearing thing test-first
was doing. What decides whether work can be judged at all is who holds
the verifier and when it came into being, so the fork is verifier-first
and timing is a per-class default further down. Independence is settled
in WG-DEL-006 and binds regardless of anything ruled here.

## It depends on

- Whether work will fan out. One lane can repair a bad oracle as it
  goes. Several cannot: by the time anyone notices, the wrong thing has
  been built in parallel.
- Whether an oracle exists that no lane authored.
- The change class. A FIX has a reproduction before any code; a spike
  has nothing stateable; docs carry no behaviour worth asserting.
- The tier. R2 and above already require the oracle frozen before
  implementation, which decides timing for those changes.

## The verifier rule

No fan-out without a verifier that predates the lanes and was not
written by the agents it judges. Three parts, each of which fails alone.

**Predates the lanes.** The acceptance conditions exist before the work
is split. An oracle written after the lanes are running has already seen
their output: that is the contamination WG-DEL-006 is about, applied to
a whole batch at once.

**External to the lanes.** The verifier belongs above the fan-out, with
the integrator. A lane may not decide its own work is done, and lanes
agreeing with each other is no substitute: agreement between generated
implementations is not independence.

**Lane count is gated on oracle strength, not on how much work there
is.** The number of lanes a batch can carry is the number the verifier
can judge. Where the oracle is near-perfect and machine-readable, agents
can self-direct in large numbers against it and verifier quality, not
coordination, is the binding constraint (EV-0053, one run of sixteen
parallel agents on a shared repository, so read it as an existence proof
and not a measurement). Where the oracle is thin, cut the lanes until
each one has something that can tell it no. `packs/agentic-swarm/PACK.md`
owns the fan-out mechanics; this guide owns the condition on them.

## Timing options

**A. Checks first everywhere.** Nothing lands before a failing check
covering it. Buys a clean authoring context and a rhythm that keeps
increments small. Costs: it demands a stateable condition on changes
that have none, which produces ceremony checks. The best human evidence
finds the ingredient is granular, uniform increments rather than the
sequencing (EV-0178, 82 observations, 39 professionals).

**B. Timing by change class.** The matrix in the pack body. Buys
ceremony where it pays and none where it does not, and costs more to
remember than one rule does.

**C. Checks last.** Implement, then write the suite before the gate.
Buys speed on exploratory work. Costs: this is the contaminated case
whenever the author is also the implementer, and tests written after
faulty code detected roughly half the faults of independently generated
ones, 14% against 25% (EV-0007). Legitimate only where the oracle comes
from somewhere other than the code just written.

**D. No behavioural checks for this class.** Link, snippet, schema and
generated-doc checks carry it. Buys honesty about documentation and
mechanical bulk change. Costs: mistaking a class for one of these is
how untested behaviour gets in.

## Decision rule

- Work about to fan out: the verifier rule, before any timing question.
- FIX: **B**, reproduction first, kept forever.
- Invariants, money, security, personal data, irreversible operations,
  public contracts: **B**, independent acceptance frozen first, at any
  tier. These are risk floors and staging never defers them.
- R2 or above: **B**, the frozen oracle, which is the tier's own
  requirement.
- REFACTOR: **B**, behaviour pinned before structure moves.
- Exploratory spike on a spike branch: **C** while the spike cannot
  merge; hardening re-enters through the router.
- DOCS, MAINT, dependency bumps: **D**, with a sampled oracle over the
  class.
- **A** is available to any venture that wants it and is never imposed.

## Default

The verifier rule, then B. The matrix is a default set, not law.

Our own timing ablation ran on 2026-08-03: eighteen runs, three tasks,
three timings, six runs each. Every arm passed six of six, so timing did
not separate quality on that work, and implement-then-harden cost about
65 per cent more tokens and 50 per cent more wall clock than the other
two. The cells stand on cost and on independence, not on fault-finding.
Results in `org/reports/V2_FINAL_REPORT.md`. A policy setting
`test_timing` to `per-profile` resolves to the matrix in the pack body;
the capability-profile record, ours being
`org/capability-profile.json`, decides only the level and its expiry.

## What the evidence does and does not say

Every timing result here comes from a narrow population. EV-0007 is
task-level programming problems. EV-0006 is SWE-bench Verified, 500
tasks, where prompting for more tests changed test-writing behaviour on
most tasks and left the number resolved statistically unchanged. EV-0003
is SWE-bench Verified again, and its useful finding is about context
rather than procedure: surfacing test-impact context cut regressions
from 6.08% to 1.82%, while generic test-first instructions without that
context made regressions worse at 9.94%. EV-0178 is 39 human
professionals on short greenfield tasks. None of these licenses a
universal claim about how software should be written.

Requirement 6 in the pack body holds whatever gets written, so a late
check still runs against every changeset eventually (EV-0016, EV-0194),
and diff-scoped mutation at review time is where a thin suite shows
up (EV-0192).

## Worked rulings

- **PatterTech EOS delivery pack (2026-08-03, argued, superseded)**: B,
  with the ablation named as the thing that would replace judgement with
  measurement. Test-first was considered as a binding rule and rejected
  because the evidence supports independence rather than ordering.
- **PatterTech EOS delivery pack (2026-08-10, argued, ADR-0006)**: the
  verifier rule first, then B, with personal data and irreversible
  operations added to the risk row. The ablation is no longer a future
  event and its result is that timing ranks on cost.
- **Venture A (2026, inherited)**: FIX starts from the failing
  reproduction and keeps it forever; a FEAT starts from its test
  specification, with acceptance skips lifted only when green end to
  end. Inherited from the v1 delivery doctrine, and consistent with
  cells one and two of the matrix.
