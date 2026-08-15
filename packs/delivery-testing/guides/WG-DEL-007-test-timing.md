---
id: WG-DEL-007
summary: What has to exist before work fans out, and when checks get written relative to the code
kind: wargame
type: wargame
tags: [ci, delivery, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DISC-009, DOC-DISC-013, DOC-DEL-008]
applies_when: [ships_code]
engages_when: [riskiest_assumption_is_unproved]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0003, EV-0006, EV-0007, EV-0016, EV-0053, EV-0178, EV-0192, EV-0194, EV-0579]
review: 2028-03
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DEL-007: What has to exist before work starts?

## Decision question and stakes

This guide used to ask when tests get written. That was the wrong
question at the top. Ordering is the least load-bearing thing test-first
was doing. What decides whether work can be judged at all is who holds
the verifier and when it came into being, so the fork is verifier-first
and timing is a per-class default further down. Independence is settled
in WG-DEL-006 and binds regardless of anything ruled here.

## Doctrines or coverage gap under pressure

- `DOC-DISC-009` (default): Depth is set by reversibility, not by the size of the request.
- `DOC-DISC-013` (default): Prefer throughput of cheap reversible tests over accuracy of ranking, where there is traffic to read.
- `DOC-DEL-008` (default): Verification staged by risk and stability.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether work will fan out. One lane can repair a bad oracle as it
  goes. Several cannot: by the time anyone notices, the wrong thing has
  been built in parallel.
- Whether an oracle exists that no lane authored.
- The change class. A FIX has a reproduction before any code; a spike
  has nothing stateable; docs carry no behaviour worth asserting.
- The tier. R2 and above already require the oracle frozen before
  implementation, which decides timing for those changes.

Applicability is `ships_code`. Engagement is `riskiest_assumption_is_unproved`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Checks first everywhere

Nothing lands before a failing check
covering it. Buys a clean authoring context and a rhythm that keeps
increments small. Costs: it demands a stateable condition on changes
that have none, which produces ceremony checks. The best human evidence
finds the ingredient is granular, uniform increments rather than the
sequencing (EV-0178, 82 observations, 39 professionals).

### B. Timing by change class

The matrix in the pack body. Buys
ceremony where it pays and none where it does not, and costs more to
remember than one rule does.

### C. Checks last

Implement, then write the suite before the gate.
Buys speed on exploratory work. Costs: this is the contaminated case
whenever the author is also the implementer, and tests written after
faulty code detected roughly half the faults of independently generated
ones, 14% against 25% (EV-0007). Legitimate only where the oracle comes
from somewhere other than the code just written.

### D. No behavioural checks for this class

Link, snippet, schema and
generated-doc checks carry it. Buys honesty about documentation and
mechanical bulk change. Costs: mistaking a class for one of these is
how untested behaviour gets in.

## Failure premises

### Premortem for A. Checks first everywhere

Assume `A. Checks first everywhere` was selected and the outcome failed. Test this option's stated failure mechanism first: it demands a stateable condition on changes that have none, which produces ceremony checks. The best human evidence finds the ingredient is granular, uniform increments rather than the sequencing (EV-0178, 82 observations, 39 professionals).

### Premortem for B. Timing by change class

Assume `B. Timing by change class` was selected and the outcome failed. Test this option's stated failure mechanism first: more to remember than one rule does.

### Premortem for C. Checks last

Assume `C. Checks last` was selected and the outcome failed. Test this option's stated failure mechanism first: this is the contaminated case whenever the author is also the implementer, and tests written after faulty code detected roughly half the faults of independently generated ones, 14% against 25% (EV-0007). Legitimate only where the oracle comes from somewhere other than the code just written.

### Premortem for D. No behavioural checks for this class

Assume `D. No behavioural checks for this class` was selected and the outcome failed. Test this option's stated failure mechanism first: mistaking a class for one of these is how untested behaviour gets in.

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

## Safe default

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

## Cheapest discriminating test

Build the narrowest end-to-end path. List the deletion or hardening work required before any artefact reaches users, then use that list to decide whether the slice remains a spike or enters the normal gate.

## Fallback, exit and revisit

**Fallback `safe-default`:** The verifier rule, then B. The matrix is a default set, not law. Our own timing ablation ran on 2026-08-03: eighteen runs, three tasks, three timings, six runs each. Every arm passed six of six, so timing did not separate quality on that work, and implement-then-harden cost about 65 per cent more tokens and 50 per cent more wall clock than the other two. The cells stand on cost and on independence, not on fault-finding. Results in `org/reports/V2_FINAL_REPORT.md`. A policy setting `test_timing` to `per-profile` resolves to the matrix in the pack body; the capability-profile record, ours being.

**Exit condition:** Stop or roll back the selected branch when it demands a stateable condition on changes that have none, which produces ceremony checks. The best human evidence finds the ingredient is granular, uniform increments rather than the sequencing (EV-0178, 82 observations, 39 professionals), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether work will fan out. One lane can repair a bad oracle as it goes. Several cannot: by the time anyone notices, the wrong thing has been built in parallel.

## Counter-evidence and transfer limits

### Preserved reasoning: The verifier rule

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
### Preserved reasoning: What the evidence does and does not say

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
### Current research boundary

EV-0579 separates exploratory code from software that reaches users. It does not make every small change reversible: a spike still needs a named deletion or hardening boundary.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
