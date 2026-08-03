---
summary: How do you choose between candidate opportunities, score them, rank by outcome contribution, test them all, or sequence by reversibility?
type: guide
tags: [product, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0059, EV-0153]
review: 2027-08
review_by: 2027-08
---

# GD-DISC-003: How do you choose between candidate opportunities?

## The question

Several things could be built and one of them goes first. The fork is
what settles the order. Start from the finding that makes this hard: the
team's own estimate of impact is close to uninformative at the idea
level, so any method that ranks by predicted value is calibrating
against a signal that measurably is not there
(`FRAG-PRODUCT-DISCOVERY-03`).

## It depends on

- Can you test them cheaply, or does each one cost weeks?
- Are they reversible?
- Do any of them foreclose the others?
- Is the constraint capacity, or is it learning?

## Options

### A. Score them

A formula over reach, impact, confidence and effort, or importance and
satisfaction ratings combined by an opportunity algorithm. Buys: a
number that stops the loudest voice winning, an audit trail, and, in the
RICE case, an explicit confidence multiplier that forces the team to
write down how much of the score is guesswork
(`FRAG-PRODUCT-DISCOVERY-15`). Costs: the arithmetic multiplies three
subjective estimates into a precise-looking number with invisible error
bars, and the impact term it depends on most is the term the base rate
says nobody can estimate (`FRAG-PRODUCT-DISCOVERY-03`). The
outcome-driven variant adds an importance rating to a difference of two
subjective ratings on the same scale with no stated justification, and
needs 180 to 600 survey respondents
(`FRAG-PRODUCT-DISCOVERY-16`). Neither has been evaluated against any
alternative by anyone who does not sell it.

### B. Rank by contribution to one outcome, effort excluded

One business outcome at the root, opportunities beneath it admitted only
when grounded in a story from an actual interview, and effort
deliberately kept out of the comparison so cheapness cannot pose as
value (`FRAG-PRODUCT-DISCOVERY-13`). Buys: a comparison that is about
the user rather than about the team's calendar, and a hard filter on
invented opportunities. Costs: coaching practice with no controlled
evaluation, it assumes weekly access to customers, and excluding effort
means the ordering it produces is not yet a plan.

### C. Test them all

Stop ranking and raise throughput. If a test is cheap, running three is
cheaper than arguing about which one to run
(`FRAG-PRODUCT-DISCOVERY-03`). Buys: the only option that produces
evidence rather than opinion, and the one the base rate favours. Costs:
it needs traffic and it needs the discipline of B7, because a cheap test
read badly is worse than no test (`FRAG-PRODUCT-DISCOVERY-04`).

### D. Sequence by reversibility and foreclosure

Order the list by what each choice takes away. Do the reversible things
now, do the things that foreclose other options last, and treat the
irreversible ones as their own decision with their own record. Buys: it
uses the one input that is not a guess, since reversibility is a
property of the change rather than a prediction about users. Costs: it
says nothing about value, so it orders the queue without telling you
whether anything in it is worth doing.

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

## Default

Sequence by reversibility, test cheaply where there is traffic, do not
score. Where a stakeholder wants a number, give them the confidence
multiplier alone: how much of this is guesswork, on the record.

## Why the scepticism, stated plainly

No prioritisation framework in the sources located has a controlled
evaluation. RICE is one company's internal tool published as a blog post
(`FRAG-PRODUCT-DISCOVERY-15`). Outcome-driven innovation's effectiveness
claims all come from the consultancy that owns the method, and its own
owner has said exact ordering is not the point
(`FRAG-PRODUCT-DISCOVERY-16`). Opportunity solution trees are coaching
practice (`FRAG-PRODUCT-DISCOVERY-13`). None of this makes them wrong.
It means a team that adopts one has chosen a shared vocabulary, not
acquired evidence, and should not present the output as a finding. The
elicitation halves of these methods are the parts worth keeping, and
they are defaults D2 and D3 in `packs/product-discovery/PACK.md`.

## Evidence boundary

The base rate that undercuts scoring comes from very high-traffic
consumer search and portal surfaces where a powered experiment finishes
in days (`FRAG-PRODUCT-DISCOVERY-03`). It is a strong result about that
population and a prior everywhere else. It predates model-assisted
ideation entirely, so whether agent-generated candidates share the base
rate is unknown. EV-0059 supplies the asymmetric gate shape for option
C and is vendor documentation, so its thresholds are conventions.
EV-0153 supplies the reversibility instinct behind D and is explicitly
anecdotal, with the author stating he lacks the cases to decide when it
applies.

## Worked rulings

- **PatterTech EOS product-discovery pack (2026-08, argued)**: no
  prioritisation formula carried at estate level. Argued from
  `FRAG-PRODUCT-DISCOVERY-03` against the impact term and from the
  absence of any controlled evaluation of a framework.
- **Approvals inbox request (2026-08, argued)**: D, because the
  requested build would have set a permissions model that the two
  cheaper candidates did not need. See
  `packs/product-discovery/exemplars/EX-DISC-001-approvals-inbox-request.md`.
- **Quarterly roadmap ordering (2026-08, inherited)**: D for the order,
  with the confidence tier written beside each item and no composite
  score anywhere in the document.
