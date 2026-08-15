---
id: GD-DISC-001
summary: How much discovery does this decision deserve, a gated phase, a standing cadence, outcome elicitation alone, or ship and instrument?
kind: wargame
type: wargame
tags: [eos, product, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DISC-002, DOC-DISC-009]
applies_when: [runs_experiment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0010, EV-0153, EV-0579]
review: 2028-06
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DISC-001: How much discovery does this decision deserve?

## Decision question and stakes

Somebody wants something built. The fork is how much investigation to do
before committing, and the honest version of the question is: what would
it cost to be wrong, and how fast would you find out? Every named school
below answers that with a fixed shape, and the shapes were priced for
teams whose build step was the expensive part.

## Doctrines or coverage gap under pressure

- `DOC-DISC-002` (binding): An experiment fixes its stopping rule, metric, segmentation and sample before data arrives.
- `DOC-DISC-009` (default): Depth is set by reversibility, not by the size of the request.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is the commitment reversible, and at what cost?
- Are there real users you can reach this week?
- Is there enough traffic to power a test on the metric that matters?
- Would a wrong problem statement cost days or months?
- Does anything here touch a regulatory, data or contractual boundary?

Applicability is `runs_experiment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Gated phase

Assume `A. Gated phase` was selected and the outcome failed. Test this option's stated failure mechanism first: four to eight weeks of calendar, a hand-off shape that a solo venture does not have, and a phase length calibrated to public-sector funding.

### Premortem for B. Standing cadence

Assume `B. Standing cadence` was selected and the outcome failed. Test this option's stated failure mechanism first: it assumes weekly access to real customers, and with one operator holding all four risks the uninteresting two get assumed away.

### Premortem for C. Outcome elicitation only

Assume `C. Outcome elicitation only` was selected and the outcome failed. Test this option's stated failure mechanism first: it settles what to aim at and nothing about whether anyone will use it or pay for it. The scoring arithmetic attached to this school is separately unsupported, see `packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md`.

### Premortem for D. Ship and instrument

Assume `D. Ship and instrument` was selected and the outcome failed. Test this option's stated failure mechanism first: it needs traffic. Below the power floor the readout is theatre with statistics attached, and naive experimentation manufactures confident wrong answers (`EV-0406`).

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

## Safe default

Depth set by reversibility, not by the size of the request. In practice
that means C for almost everything, D wherever there is traffic, A only
where undoing it is expensive, and B once there are users worth a
standing cadence.

## Cheapest discriminating test

Build the narrowest representative path and list the assumptions it can actually test. Name its deletion or promotion boundary, then list the hardening evidence required before any retained artefact reaches users.

## Fallback, exit and revisit

**Fallback `safe-default`:** Depth set by reversibility, not by the size of the request. In practice that means C for almost everything, D wherever there is traffic, A only where undoing it is expensive, and B once there are users worth a standing cadence.

**Exit condition:** Stop or roll back the selected branch when four to eight weeks of calendar, a hand-off shape that a solo venture does not have, and a phase length calibrated to public-sector funding, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is the commitment reversible, and at what cost?

## Counter-evidence and transfer limits

### Evidence boundary

`EV-0403` is a stable government standard, not a
study, and it predates agentic development. The base-rate result behind
D is a large industrial corpus on very high-traffic consumer surfaces
(`EV-0405`) and it says nothing about
agent-generated ideas. B rests on coaching practice with no controlled
evaluation. Do not report a build estimate from feel: self-reported
speed inverted the sign in the one randomised trial available (EV-0010).
### Preserved reasoning: Why the inherited lengths do not transfer

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
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Current research boundary

EV-0579 supports a narrow exploratory path only while its deletion or promotion boundary remains explicit. Copying or retaining the result moves it back through the normal evidence gate.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
