---
summary: How much discovery does this decision deserve, a gated phase, a standing cadence, outcome elicitation alone, or ship and instrument?
type: guide
tags: [product, testing, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0010, EV-0153]
review: 2028-06
---

# GD-DISC-001: How much discovery does this decision deserve?

## The question

Somebody wants something built. The fork is how much investigation to do
before committing, and the honest version of the question is: what would
it cost to be wrong, and how fast would you find out? Every named school
below answers that with a fixed shape, and the shapes were priced for
teams whose build step was the expensive part.

## It depends on

- Is the commitment reversible, and at what cost?
- Are there real users you can reach this week?
- Is there enough traffic to power a test on the metric that matters?
- Would a wrong problem statement cost days or months?
- Does anything here touch a regulatory, data or contractual boundary?

## Options

### A. Gated phase

A named, time-boxed investigation with no building inside it and defined
exit artefacts: a problem statement that is not a restatement of
somebody's solution, named hard and soft constraints, a map of what
already exists, and a stated measure of success
(`EV-0403`). Buys: a hard stop where a kill is
ordinary rather than embarrassing, and a written record before anybody
is emotionally committed. Costs: four to eight weeks of calendar, a
hand-off shape that a solo venture does not have, and a phase length
calibrated to public-sector funding.

### B. Standing cadence

No phase. One outcome at the root, opportunities admitted only when
grounded in a story from an actual interview, effort excluded from the
value comparison, several candidate solutions carried per opportunity
(`EV-0415`), with completion defined as retiring the
four risks (`EV-0416`). Buys: continuous contact with
reality, and a definition of done for discovery that is four
answerable questions rather than a document. Costs: it assumes weekly
access to real customers, and with one operator holding all four risks
the uninteresting two get assumed away.

### C. Outcome elicitation only

Skip the process and change the unit of analysis. Get underneath the
request to a measurable statement about a step in the user's job
(`EV-0418`). Buys: something that survives a change of
technology, and it is cheap. Costs: it settles what to aim at and
nothing about whether anyone will use it or pay for it. The scoring
arithmetic attached to this school is separately unsupported, see
`packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md`.

### D. Ship and instrument

Build the smallest real thing and read the instrument. Buys: the only
method that measures rather than predicts, and the base rate says
prediction is where teams are weakest, since roughly a third of ideas
moved the metric positively, a third were flat and a third negative,
with expert judgement failing to sort them
(`EV-0405`). Costs: it needs traffic. Below the power
floor the readout is theatre with statistics attached, and naive
experimentation manufactures confident wrong answers
(`EV-0406`).

## Decision rule

- `is_irreversible`, or a regulatory, data or contractual boundary is
  touched: A, time-boxed to the smallest box you can defend, and the
  exit artefacts are the point rather than the calendar.
- `has_live_traffic` above the power floor in
  `packs/product-discovery/refs/SAMPLE_AND_SIGNAL.md`, and the change is
  reversible: D. Fix the rules before the data arrives, per B7.
- `has_reachable_users` and the product is live but thin on traffic:
  B for the problem, then C to state the outcome, then a build with a
  named signal read by hand.
- Nothing live, nobody reachable, first version of anything: C alone,
  plus one named signal you will be able to read once it exists. Do not
  run A here. There is nothing to discover except your own assumptions,
  and four weeks of that produces a confident document.
- Mixed case, which is most cases: C is never wrong to do first, because
  it is an hour and it changes what the other three would investigate.

## Default

Depth set by reversibility, not by the size of the request. In practice
that means C for almost everything, D wherever there is traffic, A only
where undoing it is expensive, and B once there are users worth a
standing cadence.

## Why the inherited lengths do not transfer

The four-to-eight-week box, and the phase language around it, was
written for a funded multidisciplinary team handing over to a separate
build team (`EV-0403`). Under agentic development the
build is often the cheapest step in the chain, which inverts the
economics the box was priced against. No source located reprices
discovery for that world. The nearest structural analogue is that
boundaries are discovered under change rather than designed up front,
and the advice there is explicitly tentative and anecdotal (EV-0153).
Treat any confident claim about the right length, including this
guide's, as a working rule.

## Evidence boundary

`EV-0403` is a stable government standard, not a
study, and it predates agentic development. The base-rate result behind
D is a large industrial corpus on very high-traffic consumer surfaces
(`EV-0405`) and it says nothing about
agent-generated ideas. B rests on coaching practice with no controlled
evaluation. Do not report a build estimate from feel: self-reported
speed inverted the sign in the one randomised trial available (EV-0010).

## Worked rulings

- **PatterTech EOS product-discovery pack (2026-08, argued)**: depth by
  reversibility adopted as default D1. Argued from
  `EV-0403` for the exit artefacts and
  `EV-0405` for why prediction is weak.
- **Approvals inbox request (2026-08, argued)**: C then a hand-read
  signal, verdict TEST. Traffic was two orders of magnitude below the
  power floor, so D was refused. See
  `packs/product-discovery/exemplars/EX-DISC-001-approvals-inbox-request.md`.
- **Data-retention change on regulated records (2026-08, inherited)**:
  A, because the commitment is irreversible once records are deleted.
  The box was two days, not four weeks, and the exit artefacts were the
  same four.
