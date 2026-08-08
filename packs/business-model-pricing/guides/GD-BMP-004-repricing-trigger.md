---
summary: What opens a price change, what cause is announced with it, and who is protected from the change
type: guide
tags: [money, product]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0292, EV-0298, EV-0303, EV-0096, EV-0197]
review: 2028-06
---

# GD-BMP-004: when and how does the price change?

## The question

A price set once is a price that decays. The fork is what opens a
change, because the trigger decides whether the change is a decision or
a panic.

## It depends on

- How volatile is the allocated cost to serve (EV-0197)?
- Does the venture have contracts with existing customers, and what did
  they promise?
- Is there a threshold event coming, such as VAT registration
  (EV-0303)?
- Can you state a cause the buyer can check?
- How many customers would have to leave before the rise loses money?

## Options

### A. Never, until something breaks

No trigger. Buys: nothing to maintain, and no awkward conversations.
Costs: the change eventually happens under pressure, at the worst
moment, with no argument prepared.

### B. Scheduled review

A fixed calendar review, quarterly or annually, that may or may not
change the price. Buys: the decision gets made when nobody is panicking,
and customers can be told when reviews happen. Costs: a review with no
threshold turns into a rubber stamp, and it misses a fast cost move
between dates.

### C. Cost-indexed trigger

A written movement in allocated unit cost, above a stated band, opens a
change. Buys: the cause is already established when the change fires,
which is the framing buyers accept
(EV-0292). It is the same shape as a pre-agreed
error budget policy: the threshold and the response are both agreed
before the pressure arrives (EV-0096). Costs: it needs a real cost
allocation, and it only covers cost causes.

### D. Contract-indexed

The contract states the mechanism, such as an annual uplift against a
published index or a capped percentage. Buys: no negotiation at all, and
the buyer priced the risk when they signed. Costs: it binds you as well
as them, and an index can move against you.

## Decision rule

- Volatile input costs and a real allocation: C, with B as the backstop
  for causes that are not cost.
- Business contracts of a year or more: D, agreed at signature.
- Everything else, and any venture without a cost allocation yet: B, at
  a stated cadence, with the first review dated in the decision record.
- A is not a default. Take it only for a price you intend to retire.

## Default

C where a cost allocation exists, B where it does not, and both write
the threshold down before it fires.

## How a change is announced

The cause is stated, and the cause is a cost movement or a change in
delivered value. Buyers accept a rise that protects an existing margin
against a cost increase and judge a rise that exploits a demand shift to
be unfair (EV-0292). The operational form:

1. Name the cause and its type, cost or value. A demand cause is not one
   of the two.
2. Give the size, the date and what stays the same.
3. Say what existing customers get. Grandfathering is a choice and
   costs money; make it deliberately.
4. For consumer subscriptions, the change rides on the statutory notice
   machinery rather than beside it: reminder notices and the cooling-off
   duties apply (EV-0298).
5. Record the change and its cause in the decision record so the next
   change can be argued against the last one.

## Evidence boundary

EV-0292 is stated fairness judgement from 1986
telephone surveys, not observed churn. It puts no number on what a
fairness violation costs, fairness norms vary by market, and firms
routinely raise prices on demand shifts without visible collapse. So
this is a constraint with an unmeasured price, carried as a default and
not as a rule. If your own cohorts show the retention consequence, that
observation beats the survey.

## Worked rulings

- **PatterTech EOS business-model-pricing pack (2026-08, argued)**: C
  where a cost allocation exists, B otherwise, and a cause type of cost
  or value on every announcement. Argued from
  EV-0292 with its 1986 provenance stated.
- **First UK consumer subscription, composed (2026-08, inherited)**:
  C, with a band of plus or minus ten per cent on allocated unit cost
  over a rolling quarter, and a cause type recorded on the change. See
  `packs/business-model-pricing/exemplars/EX-BMP-001-first-consumer-subscription.md`.

## Related

The anchor that the new number is derived from is
`packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md`. The
dated legal and tax triggers that can force a change sit in
`packs/business-model-pricing/refs/UK_OBLIGATIONS.md`.
