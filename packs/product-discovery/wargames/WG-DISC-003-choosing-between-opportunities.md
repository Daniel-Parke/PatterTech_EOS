---
id: WG-DISC-003
summary: How do you choose between candidate opportunities, score them, rank by outcome contribution, test them all, or sequence by reversibility?
kind: wargame
type: wargame
tags: [eos, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DISC-002, DOC-DISC-010, DOC-DISC-011]
applies_when: [runs_experiment]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0059, EV-0153]
review: 2028-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DISC-003: How do you choose between candidate opportunities?

## Decision question and stakes

Several things could be built and one of them goes first. The fork is
what settles the order. Start from the finding that makes this hard: the
team's own estimate of impact is close to uninformative at the idea
level, so any method that ranks by predicted value is calibrating
against a signal that measurably is not there
(`EV-0405`).

## Doctrines or coverage gap under pressure

- `DOC-DISC-002` (binding): An experiment fixes its stopping rule, metric, segmentation and sample before data arrives.
- `DOC-DISC-010` (default): Elicit outcomes, not features.
- `DOC-DISC-011` (default): Carry more than one candidate solution before committing.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can you test them cheaply, or does each one cost weeks?
- Are they reversible?
- Do any of them foreclose the others?
- Is the constraint capacity, or is it learning?

Applicability is `runs_experiment`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Score them

A formula over reach, impact, confidence and effort, or importance and
satisfaction ratings combined by an opportunity algorithm. Buys: a
number that stops the loudest voice winning, an audit trail, and, in the
RICE case, an explicit confidence multiplier that forces the team to
write down how much of the score is guesswork
(`EV-0417`). Costs: the arithmetic multiplies three
subjective estimates into a precise-looking number with invisible error
bars, and the impact term it depends on most is the term the base rate
says nobody can estimate (`EV-0405`). The
outcome-driven variant adds an importance rating to a difference of two
subjective ratings on the same scale with no stated justification, and
needs 180 to 600 survey respondents
(`EV-0418`). Neither has been evaluated against any
alternative by anyone who does not sell it.

### B. Rank by contribution to one outcome, effort excluded

One business outcome at the root, opportunities beneath it admitted only
when grounded in a story from an actual interview, and effort
deliberately kept out of the comparison so cheapness cannot pose as
value (`EV-0415`). Buys: a comparison that is about
the user rather than about the team's calendar, and a hard filter on
invented opportunities. Costs: coaching practice with no controlled
evaluation, it assumes weekly access to customers, and excluding effort
means the ordering it produces is not yet a plan.

### C. Test them all

Stop ranking and raise throughput. If a test is cheap, running three is
cheaper than arguing about which one to run
(`EV-0405`). Buys: the only option that produces
evidence rather than opinion, and the one the base rate favours. Costs:
it needs traffic and it needs the discipline of B7, because a cheap test
read badly is worse than no test (`EV-0406`).

### D. Sequence by reversibility and foreclosure

Order the list by what each choice takes away. Do the reversible things
now, do the things that foreclose other options last, and treat the
irreversible ones as their own decision with their own record. Buys: it
uses the one input that is not a guess, since reversibility is a
property of the change rather than a prediction about users. Costs: it
says nothing about value, so it orders the queue without telling you
whether anything in it is worth doing.

## Failure premises

### Premortem for A. Score them

Assume `A. Score them` was selected and the outcome failed. Test this option's stated failure mechanism first: the arithmetic multiplies three subjective estimates into a precise-looking number with invisible error bars, and the impact term it depends on most is the term the base rate says nobody can estimate (`EV-0405`). The outcome-driven variant adds an importance rating to a difference of two subjective ratings on the same scale with no stated justification, and needs 180 to 600 survey respondents (`EV-0418`). Neither has been evaluated against any alternative by anyone who does not sell it.

### Premortem for B. Rank by contribution to one outcome, effort excluded

Assume `B. Rank by contribution to one outcome, effort excluded` was selected and the outcome failed. Test this option's stated failure mechanism first: coaching practice with no controlled evaluation, it assumes weekly access to customers, and excluding effort means the ordering it produces is not yet a plan.

### Premortem for C. Test them all

Assume `C. Test them all` was selected and the outcome failed. Test this option's stated failure mechanism first: it needs traffic and it needs the discipline of B7, because a cheap test read badly is worse than no test (`EV-0406`).

### Premortem for D. Sequence by reversibility and foreclosure

Assume `D. Sequence by reversibility and foreclosure` was selected and the outcome failed. Test this option's stated failure mechanism first: it says nothing about value, so it orders the queue without telling you whether anything in it is worth doing.

## Decision rule

- The candidates are cheap and reversible and there is traffic: C.
- The candidates are cheap and reversible and there is no traffic: D for
  the order, and one named signal per candidate so that shipping teaches
  you something.
- Any candidate is irreversible or forecloses another: D, and that
  candidate leaves the queue and gets its own discovery record.
- You have real users and a live outcome metric: B for the shortlist,
  then C or D for the order.
- A is never the deciding input. If a score is written down, it is
  written as an estimate with its confidence attached, and the record
  says what it would take to overturn it.

## Safe default

Sequence by reversibility, test cheaply where there is traffic, do not
score. Where a stakeholder wants a number, give them the confidence
multiplier alone: how much of this is guesswork, on the record.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can you test them cheaply, or does each one cost weeks?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** Sequence by reversibility, test cheaply where there is traffic, do not score. Where a stakeholder wants a number, give them the confidence multiplier alone: how much of this is guesswork, on the record.

**Exit condition:** Stop or roll back the selected branch when the arithmetic multiplies three subjective estimates into a precise-looking number with invisible error bars, and the impact term it depends on most is the term the base rate says nobody can estimate (`EV-0405`). The outcome-driven variant adds an importance rating to a difference of two subjective ratings on the same scale with no stated justification, and needs 180 to 600 survey respondents (`EV-0418`). Neither has been evaluated against any alternative by anyone who does not sell it, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can you test them cheaply, or does each one cost weeks?

## Counter-evidence and transfer limits

### Evidence boundary

The base rate that undercuts scoring comes from very high-traffic
consumer search and portal surfaces where a powered experiment finishes
in days (`EV-0405`). It is a strong result about that
population and a prior everywhere else. It predates model-assisted
ideation entirely, so whether agent-generated candidates share the base
rate is unknown. EV-0059 supplies the asymmetric gate shape for option
C and is vendor documentation, so its thresholds are conventions.
EV-0153 supplies the reversibility instinct behind D and is explicitly
anecdotal, with the author stating he lacks the cases to decide when it
applies.
### Preserved reasoning: Why the scepticism, stated plainly

No prioritisation framework in the sources located has a controlled
evaluation. RICE is one company's internal tool published as a blog post
(`EV-0417`). Outcome-driven innovation's effectiveness
claims all come from the consultancy that owns the method, and its own
owner has said exact ordering is not the point
(`EV-0418`). Opportunity solution trees are coaching
practice (`EV-0415`). None of this makes them wrong.
It means a team that adopts one has chosen a shared vocabulary, not
acquired evidence, and should not present the output as a finding. The
elicitation halves of these methods are the parts worth keeping, and
they are defaults D2 and D3 in `packs/product-discovery/PACK.md`.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
