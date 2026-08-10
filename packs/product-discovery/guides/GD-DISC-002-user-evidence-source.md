---
summary: Where does the evidence about users come from, existing behaviour, talking to people, a controlled experiment, or a model standing in for them?
type: guide
tags: [product, testing, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0059]
review: 2028-06
---

# GD-DISC-002: Where does the evidence about users come from?

## The question

You need to say something about what people want or do, and the record
has to name where that came from (B5). The fork is which instrument you
point at the question. Each instrument answers a different question, and
most bad discovery comes from using one to answer another's.

## It depends on

- Are you asking whether a problem exists, or whether a design works,
  or whether a change moves a number?
- Can you reach real users this week, and which users?
- How much traffic does the surface carry?
- What does being wrong cost, and when would you find out?

## Options

### A. Existing behaviour already recorded

Support tickets, session records, telemetry, sales notes, churn
reasons. Buys: it is real, it is already there, and it costs an hour. It
is the only instrument available before you have users to interview.
Costs: it is a record of the people who spoke, not of the population; it
tells you what people hit and never what they wanted; and the filter you
applied to get a count becomes part of the claim, so the record has to
state it.

### B. Talking to and watching real people

Interviews, contextual observation, moderated task sessions. Buys: the
only instrument that finds a problem you did not already suspect, and
the only source that grounds an opportunity in a story rather than an
assumption (`EV-0415`). Costs: recruitment is slow,
and the recruitment frame decides whether the whole discovery is wrong
(`EV-0404`). Small samples are wildly variable rather
than merely thin: across random sets of five participants the share of
known problems found ran from 99 per cent down to 55, ten raised the
floor to about 80, twenty to about 95
(`EV-0407`).

### C. A controlled experiment

Change behaviour for some users and read a metric. Buys: it measures
instead of predicting, which matters because expert judgement does not
sort ideas into the third that work and the two thirds that do not
(`EV-0405`). Costs: it needs enough traffic to power
the metric, and without a platform enforcing guardrails the known
failure modes get more likely, not less
(`EV-0406`). Asymmetric gating is the usable default:
goal metrics drive the ship decision, guardrails block only on
significant harm (EV-0059, vendor documentation of its own feature, so
the thresholds are conventions).

### D. A model standing in for users

Synthetic personas, simulated survey respondents, model-generated
requirements. Buys: instant, free, and available before you have anyone
to ask. Costs: on the segment-targeting task, which is the thing product
teams actually want from it, models inflated between-segment gaps two to
fourfold and would have pointed a team at the wrong segment in half the
US cases, and no tested model beat the strongest non-LLM baseline at the
individual level (`EV-0413`). Scope note: that
benchmark is attitudinal survey prediction, not interview rehearsal.

## Decision rule

- "Does this problem exist and who has it": A first, because it is an
  hour, then B. Never D.
- "Does this design work": B, moderated, with the worst-case sample
  reasoning of D7 rather than the average.
- "Does this change move the number": C if the surface clears the power
  floor in `packs/product-discovery/refs/SAMPLE_AND_SIGNAL.md`,
  otherwise a named signal read by hand and a stated waiting period.
- "What should we ask them": D is legitimate here. Drafting an
  interview guide, generating candidate questions, or synthesising a
  transcript you collected is the structuring job, which is where
  model assistance measured best (`EV-0412`).
- Any use of D that reaches the record is labelled unverified at the
  point of use, per B6, and never carries a decision alone.

## Default

A then B for problem questions, C for metric questions above the power
floor, D only for structuring real input. Where two instruments
disagree, the one that observed behaviour wins over the one that asked.

## Sample size, honestly

Two sources are usually presented as contradicting each other. The
five-user convention argues that three rounds of five beat one round of
fifteen on a fixed budget, because each round changes the design and so
changes the problem set (`EV-0408`). The resampling
study measures what that average hides
(`EV-0407`). They optimise different things: expected
yield per pound against the variance of a single draw. This pack takes
the worst case, because you only ever run one sample and cannot tell
which one you drew. Two further cautions: the five-user article is
twenty-six years old and never revised, and it models usability defect
finding, not whether a problem is worth solving. Citing it to justify
five customer interviews is citing it for something it does not cover.

## Evidence boundary

`EV-0407` is one interface, one problem set, a 2003
web application, and its denominator is problems found by the full
sixty, so problems nobody found are invisible to it. The exact
percentages do not transfer to another interface class; the shape of the
variance does. `EV-0412` is a preprint on a single
platform with participants rather than real stakeholders, scored against
a documentation standard that rewards well-formed prose and cannot
detect a well-written requirement for the wrong thing.
`EV-0413` moves as models move; the direction is the
durable part, not the margins.

## Worked rulings

- **PatterTech EOS product-discovery pack (2026-08, argued)**: worst
  case over average adopted as D7, and the label rule bound as B6.
- **Approvals inbox request (2026-08, argued)**: A only, because there
  were no reachable users and the ticket export was the sole real
  source. The three supplied personas were refused as decision evidence
  and cited as unverified. See
  `packs/product-discovery/exemplars/EX-DISC-001-approvals-inbox-request.md`.
- **Onboarding copy variant (2026-08, inherited)**: C, because the
  signup surface was the one place with enough traffic to power a test
  inside a fortnight.
