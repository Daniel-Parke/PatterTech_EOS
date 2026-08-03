---
summary: When are tests written relative to the code, and is that a rule or a default?
kind: guide
scope: estate
authority: default
lifecycle: active
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0003, EV-0006, EV-0007, EV-0016, EV-0178, EV-0192, EV-0194]
review: 2028-03
type: wargame
status: active
tags: [delivery, testing, ci]
review_by: 2028-03
---

# WG-DEL-007: When are tests written?

## The question

Test-first is the most-argued question in the field and the
worst-evidenced. The temptation is to settle it with doctrine, and
doctrine is exactly what the evidence does not support in either
direction. The fork is whether timing is a universal rule, a per-class
default, or left to the author. Independence is settled separately in
WG-DEL-006 and binds regardless of what this guide rules.

## It depends on

- The change class. A FIX has a reproduction available before any code;
  a spike has nothing stateable at all.
- The tier. R2 and above already require the oracle frozen before
  implementation, which decides timing for those changes.
- Whether the author is a person or a model. For a person the test is
  partly a design aid; for a model it is mainly the only reliable
  oracle.
- Whether the class of change carries behaviour worth asserting. Docs
  and dependency bumps mostly do not.
- What the venture's capability profile has earned.

## Options

### A. Test-first everywhere
What it is: no production line lands before a failing test covering it.
Buys: an oracle the implementation cannot have contaminated, every
time, and a decomposition rhythm that keeps increments small.
Costs: it demands a stateable condition on changes that do not have
one, which produces ceremony tests written to satisfy the rule. The
best human evidence available finds the active ingredient is granular,
uniform increments rather than the sequencing, across 82 observations
from 39 professionals on short greenfield tasks (EV-0178).

### B. Timing by change class
What it is: the matrix in the pack body. Reproduction first for a FIX,
frozen oracle first at R2 and above, behaviour pinned first for a
REFACTOR, nothing behavioural for DOCS and MAINT.
Buys: the ceremony lands where it pays and stays away where it does
not, and each cell is a defensible claim rather than a slogan.
Costs: more to remember than one rule, and the cells are currently set
by judgement rather than measurement.

### C. End-stage testing
What it is: implement, then write the suite before the merge gate.
Buys: speed on exploratory work, and tests written against real
signatures rather than imagined ones.
Costs: this is the contaminated case. Tests written after faulty code
detected roughly half the faults of independently generated tests, 14%
against 25% (EV-0007). Legitimate only when the oracle comes from
somewhere other than the code just written.

### D. No behavioural tests for this class
What it is: link, snippet, schema and generated-doc checks carry the
class, with no behavioural suite at all.
Buys: honesty about documentation, configuration and mechanical bulk
change, where a behavioural test asserts nothing anyone cares about.
Costs: mistaking a class for one of these is how untested behaviour
gets in.

## Decision rule

- FIX: **B**, and the cell is reproduction first. The reproduction is
  kept forever.
- R2 or above: **B**, and the cell is the frozen oracle, which is the
  tier's own requirement.
- REFACTOR: **B**, behaviour pinned before structure moves, then the
  new condition.
- Exploratory spike on a spike branch: **C** is acceptable while the
  spike cannot merge; hardening re-enters through the router and gets
  its cell like any other change.
- DOCS, MAINT, dependency bumps: **D**, with a sampled oracle over the
  class rather than per change.
- **A** is available to any venture that wants it and is never imposed
  by this pack.

## Default

B, the matrix, read as a default set rather than as law. The test-timing
ablation in P7 sets these cells per capability profile from evidence;
until it reports, the conservative value stands, and an inconclusive
cell keeps whatever it has. No cell in the matrix is doctrine, and this
pack does not mandate test-driven development or end-stage testing
anywhere.

## What the evidence does and does not say

Every timing result available here comes from narrow populations.
EV-0007 is task-level programming problems and agentic workflows.
EV-0006 is SWE-bench Verified trajectories, where test-writing frequency
was similar in resolved and unresolved runs. EV-0003 is SWE-bench
Verified again, and its useful finding is about context rather than
procedure: surfacing test-impact context cut regressions from 6.08% to
1.82%, while generic test-first instructions without that context made
regressions worse at 9.94%. EV-0178 is 39 human professionals on short
greenfield tasks. None of these licenses a universal claim about how
software should be written, and this guide does not make one.

Selection interacts with timing: whatever gets written, requirement 6
in the pack body still holds, so a test written late is still a test
that runs against every changeset eventually (EV-0016, EV-0194), and
diff-scoped mutation at review time is where a thin suite shows up
(EV-0192).

## Worked rulings

- **PatterTech EOS delivery pack (2026-08, argued)**: B. The matrix
  ships as a default set with the ablation named as the mechanism that
  will replace judgement with measurement. Test-first was considered as
  a binding rule and rejected on the grounds that the evidence supports
  independence rather than ordering.
- **AutoWatt (2026, inherited)**: FIX starts from the failing
  reproduction and keeps it forever; a FEAT starts from its test
  specification with acceptance skips lifted only when green end to
  end. Inherited from the v1 delivery doctrine rather than argued
  fresh, and consistent with cells one and two of the matrix.
