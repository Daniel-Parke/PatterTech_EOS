---
id: GD-RESEARCH-003
summary: Wait for something to break, sweep on a calendar, supersede on a named event, or keep the answer continuously live?
kind: wargame
type: wargame
tags: [content, data, eos, migrations, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-RESEARCH-004]
applies_when: [supersedes_a_source]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0536, EV-0539, EV-0541, EV-0542, EV-0543, EV-0124, EV-0171, EV-0259, EV-0260, EV-0331]
review: 2029-06
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-RESEARCH-003: how is a source superseded when it changes version or dies?

## Decision question and stakes

A claim was true of what was read on the day it was read. The source
then does one of three things: it stops resolving, it moves, or it stays
at the same address and says something different. The third matters most
and is hardest to notice, because nothing breaks. A knowledge base whose
claims are true of a world that has moved is worse than an empty one,
because it reads as current.

The two failures have separate names and separate rates. Link rot is the
reference no longer resolving; content drift is the reference resolving
to something changed (EV-0541). Only the first is mechanically
detectable, and for a venture reading vendor documentation the second is
the common case, because the documentation site keeps the URL and
rewrites the page.

## Doctrines or coverage gap under pressure

- `DOC-RESEARCH-004` (binding): A dead or changed source is superseded, not left.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Does the source publish version signals? A semantic version, a
  deprecation header, a changelog and a retirement date are all offers
  to be told (EV-0171, EV-0124, EV-0260).
- Does it change on an event or on a clock? A supplier shipping a
  release is event-driven; a standards body is closer to periodic.
- Can the same address change what it says? A model endpoint behind a
  stable name is the sharpest instance of this, where behaviour moved
  substantially in months (EV-0259).
- Is there an archive that holds a prior state, and does anybody run a
  time gate for it (EV-0542)?

Applicability is `supersedes_a_source`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Wait for something to break
No sweep, no trigger. The claim is re-checked when a build fails or
somebody notices. Buys zero maintenance cost, which is the right price
for a claim nothing rests on. Costs the whole class of silent failure:
content drift breaks nothing, so nothing tells you, and the older the
claim the worse the odds. In the one measured corpus, references aged
fifteen years failed to resolve at rates between fifty-nine and
eighty-nine per cent (EV-0541).

### B. A calendar sweep
Every source carries a review date and somebody works the queue. Buys a
bounded, predictable cost and catches drift as well as death, because a
person reads the page again. Costs being wrong twice: an event-driven
fact on a calendar is reviewed too late when the supplier ships and too
early when it does not. A queue that is mostly no-change trains people
to stamp it.

### C. Event-driven supersession on a named trigger
Each record carries `on-change-of:<the thing that moves>` rather than a
date, and the trigger is the supplier's own signal: a release, a
deprecation notice, a retirement date, a new edition. Buys review at the
moment the answer could have changed and at no other moment. Costs a
dependency on the supplier publishing a signal, which the good ones do
(EV-0124, EV-0260) and the rest do not. Costs nothing against the source
that quietly rewrites a page, so it needs the frozen copy underneath it
to be worth anything.

### D. Keep the answer continuously live
Standing surveillance, searches on a short cycle, new material folded in
as it arrives. Buys an answer that is current by construction, and it is
the right shape where the question is high priority, current certainty
is low, and new evidence is genuinely likely. Costs continuous effort
for a question that may not move, and the handbook that defines the
approach names those three conditions together as the test for using it
at all (EV-0536).

## Failure premises

### Premortem for A. Wait for something to break

Assume `A. Wait for something to break` was selected and the outcome failed. Test this option's stated failure mechanism first: , which is the right price for a claim nothing rests on. Costs the whole class of silent failure: content drift breaks nothing, so nothing tells you, and the older the claim the worse the odds. In the one measured corpus, references aged fifteen years failed to resolve at rates between fifty-nine and eighty-nine per cent (EV-0541).

### Premortem for B. A calendar sweep

Assume `B. A calendar sweep` was selected and the outcome failed. Test this option's stated failure mechanism first: and catches drift as well as death, because a person reads the page again. Costs being wrong twice: an event-driven fact on a calendar is reviewed too late when the supplier ships and too early when it does not. A queue that is mostly no-change trains people to stamp it.

### Premortem for C. Event-driven supersession on a named trigger

Assume `C. Event-driven supersession on a named trigger` was selected and the outcome failed. Test this option's stated failure mechanism first: a dependency on the supplier publishing a signal, which the good ones do (EV-0124, EV-0260) and the rest do not. Costs nothing against the source that quietly rewrites a page, so it needs the frozen copy underneath it to be worth anything.

### Premortem for D. Keep the answer continuously live

Assume `D. Keep the answer continuously live` was selected and the outcome failed. Test this option's stated failure mechanism first: continuous effort for a question that may not move, and the handbook that defines the approach names those three conditions together as the test for using it at all (EV-0536).

## Decision rule

- Underneath all four: freeze a copy at first read and record where it
  is. Without it nothing can tell drift from a misremembering, and the
  record cannot outlive the source (EV-0539).
- Nothing rests on the claim, or it is definitional on a frozen
  standard: A, plus a scheduled link check so death is noticed (EV-0331).
- The source publishes a version, a deprecation or a retirement signal:
  C, with the trigger named as the thing that moves rather than as a
  month.
- No signal to subscribe to and something real rests on it: B, with a
  date set by how fast that source has moved, not by a house default.
- The three conditions hold together, high priority, low certainty, new
  material likely: D, and write the cadence into the plan rather than
  deciding it each time.
- Whichever is chosen, supersession is a dated ruling and not a link
  update: every claim on the source is marked still standing, narrowed
  or withdrawn.

## Safe default

C with a frozen copy at first read, falling back to B where the source
publishes nothing to subscribe to. Most of what a venture reads is
published by somebody who announces changes, and reviewing on their
event rather than on our calendar spends the attention where it can
change an answer.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Does the source publish version signals? A semantic version, a deprecation header, a changelog and a retirement date are all offers to be told (EV-0171, EV-0124, EV-0260).** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C with a frozen copy at first read, falling back to B where the source publishes nothing to subscribe to. Most of what a venture reads is published by somebody who announces changes, and reviewing on their event rather than on our calendar spends the attention where it can change an answer.

**Exit condition:** Stop or roll back the selected branch when , which is the right price for a claim nothing rests on. Costs the whole class of silent failure: content drift breaks nothing, so nothing tells you, and the older the claim the worse the odds. In the one measured corpus, references aged fifteen years failed to resolve at rates between fifty-nine and eighty-nine per cent (EV-0541), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Does the source publish version signals? A semantic version, a deprecation header, a changelog and a retirement date are all offers to be told (EV-0171, EV-0124, EV-0260).

## Counter-evidence and transfer limits

The link-rot half of the evidence is measured and the content-drift half
is modelled: the authors had no real data on how often the referenced
resources actually changed and had to assume representativeness
thresholds (EV-0541). The direction is well established; the rate is
not, and this guide rests on the direction.

That corpus is scholarly web references from 1997 to 2012. Vendor
documentation, most of what a venture reads, fails differently: it keeps
its URL and rewrites the page, so the measured rates understate the risk
that matters here and overstate the one that does not.

D reads as the safest option and is the one its own source is most
cautious about. Three conditions have to hold together, and a review
kept current on a settled question spends effort forever and never
changes an answer (EV-0536).

Finally, a maintained official source can be wrong at a pinned version
and correct it later: the injection taxonomy this pack cites carries a
planning note recording an error on a numbered page three months after
publication (EV-0543). Supersession also covers sources that were wrong
and said so, which only a record carrying an edition and a date catches.
### Historical ruling boundary

The baseline file carried 4 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
