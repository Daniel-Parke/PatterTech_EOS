---
id: GD-BMP-001
summary: What information the price is anchored to, and the condition that makes that anchor right here
kind: wargame
type: wargame
tags: [eos, money, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-BMP-005]
applies_when: [sets_a_price]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0287, EV-0288, EV-0289, EV-0290, EV-0292, EV-0197]
review: 2028-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-BMP-001: what is this price anchored to?

## Decision question and stakes

A venture has to put a number on a thing. The fork is which information
that number is derived from: what it costs to serve, what the nearest
comparable product charges, or what the buyer's benefit is worth. The
usual framing treats this as a ranking with value at the top. The
evidence does not support a ranking.

## Doctrines or coverage gap under pressure

- `DOC-BMP-005` (default): Open on a named practice with its condition and a revisit date.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can the buyer compare this against something like it, easily?
- Does the product change a number in the buyer's world that either side
  can measure?
- Do segments differ enough that one price is leaving money behind?
- Does anyone here own building the value case, and have they got the
  access to build it?
- Is there any willingness-to-pay evidence at all yet, or only opinion?

Applicability is `sets_a_price`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Cost-informed

Take the allocated cost to serve one unit (EV-0197) and add a margin.
Buys: a number you can defend to a customer and to yourself, available
on day one, and a fairness story that survives a price rise, because a
cost-justified increase reads as fair
(EV-0292). Costs: it is blind to what the buyer
would have paid, and it caps you at whatever margin you had the nerve to
write.

### B. Competition-informed

Anchor on comparable products. Buys: instant credibility in a market
where buyers already know the going rate, and no research bill. Costs:
you inherit a stranger's cost base and funding position, and you learn
nothing about your own buyer. It is a legitimate practice under its
conditions and a bad habit outside them
(EV-0288).

### C. Value-informed

Price from a quantified before-and-after in one buyer segment. Buys: the
only anchor that can price segments differently, and the one
practitioners and academics agree works. Costs: it is an operational
build, not a decision. The reported blockers were value assessment,
value communication, segmentation, sales incentives and sponsorship, all
capability problems (EV-0287). For a small
venture the affordable form is narrow: one segment, one measured number,
one price.

### D. Hybrid, cost floor and value ceiling

Set a floor from allocated cost plus the margin you will not go under,
set a ceiling from the best value or willingness-to-pay evidence you
have, and pick inside the band with a stated reason. Buys: it makes both
the floor and the ceiling explicit and testable. Costs: two pieces of
work instead of one, and the band is only as good as the ceiling
evidence.

## Failure premises

### Premortem for A. Cost-informed

Assume `A. Cost-informed` was selected and the outcome failed. Test this option's stated failure mechanism first: to serve one unit (EV-0197) and add a margin. Buys: a number you can defend to a customer and to yourself, available on day one, and a fairness story that survives a price rise, because a cost-justified increase reads as fair (EV-0292). Costs: it is blind to what the buyer would have paid, and it caps you at whatever margin you had the nerve to write.

### Premortem for B. Competition-informed

Assume `B. Competition-informed` was selected and the outcome failed. Test this option's stated failure mechanism first: you inherit a stranger's cost base and funding position, and you learn nothing about your own buyer. It is a legitimate practice under its conditions and a bad habit outside them (EV-0288).

### Premortem for C. Value-informed

Assume `C. Value-informed` was selected and the outcome failed. Test this option's stated failure mechanism first: it is an operational build, not a decision. The reported blockers were value assessment, value communication, segmentation, sales incentives and sponsorship, all capability problems (EV-0287). For a small venture the affordable form is narrow: one segment, one measured number, one price.

### Premortem for D. Hybrid, cost floor and value ceiling

Assume `D. Hybrid, cost floor and value ceiling` was selected and the outcome failed. Test this option's stated failure mechanism first: plus the margin you will not go under, set a ceiling from the best value or willingness-to-pay evidence you have, and pick inside the band with a stated reason. Buys: it makes both the floor and the ceiling explicit and testable. Costs: two pieces of work instead of one, and the band is only as good as the ceiling evidence.

## Decision rule

- No willingness-to-pay evidence, and a buyer who can compare easily: B,
  with A as the floor check.
- No comparable product and no value measurement yet: A, and set a date.
- A measurable change in the buyer's world and someone to own the value
  case: C, for one segment first.
- Anything beyond the first few months, once both a cost allocation and
  some real transaction evidence exist: D.

Whichever you pick, write the practice and the condition into the
decision record. A practice with no condition next to it is an opinion
that will not survive its author.

## Safe default

A or B as an opening position, with a dated review to move toward value
evidence. The reason is availability rather than merit: a venture in its
first months has an allocated cost and a competitor page, and no
willingness-to-pay evidence worth the name.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can the buyer compare this against something like it, easily?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A or B as an opening position, with a dated review to move toward value evidence. The reason is availability rather than merit: a venture in its first months has an allocated cost and a competitor page, and no willingness-to-pay evidence worth the name.

**Exit condition:** Stop or roll back the selected branch when to serve one unit (EV-0197) and add a margin. Buys: a number you can defend to a customer and to yourself, available on day one, and a fairness story that survives a price rise, because a cost-justified increase reads as fair (EV-0292). Costs: it is blind to what the buyer would have paid, and it caps you at whatever margin you had the nerve to write, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can the buyer compare this against something like it, easily?

## Counter-evidence and transfer limits

### Evidence boundary

EV-0287 is executive self-report from 2008,
mid-size and large firms, pre-SaaS, and its eighty per cent figure is a
survey-era snapshot rather than a current fact.
EV-0288 was read at abstract level only, so its
moderator coefficients are not available and must not be quoted. Neither
identifies a causal effect. Willingness-to-pay evidence gathered by
survey is an upper bound, because hypothetical answers overstate what
people pay (EV-0289), and the price sensitivity
meter is a screening bracket by its own vendor's account
(EV-0290).
### Preserved reasoning: Related

The unit the anchor applies to is a separate fork, in
`packs/business-model-pricing/guides/GD-BMP-002-charging-unit.md`. When
the anchor moves, the change is governed by
`packs/business-model-pricing/guides/GD-BMP-004-repricing-trigger.md`.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
