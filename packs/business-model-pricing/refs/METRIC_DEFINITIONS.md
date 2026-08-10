---
summary: Why commercial metrics carry their own definitions, the house definitions, and the honest weakness in this rule
type: foundation
tags: [money, data]
kind: fact
scope: estate
sources: [EV-0296, EV-0297, EV-0199, EV-0210]
volatility: slow
review: 2028-08
---

# Commercial metric definitions

Level three material behind default D5. Read this before a commercial
number leaves the venture.

## Why the definitions live here

No primary source was found at the cutoff that fixes what annual
recurring revenue, net revenue retention or churn mean. Public filings
say openly that annual recurring revenue has no standardised meaning,
which is itself the finding. So the venture writes its own definitions
and keeps them.

The discipline is borrowed rather than invented. The delivery metric
work insists that a metric without its definition is a number people
argue past, and that the definition moving is itself an event to report
(EV-0199, EV-0210). Honest weakness: an attempt to anchor this in the
securities regulator's release on key performance indicator disclosure
failed at the cutoff because the source could not be fetched. D5 rests
on internal reasoning and stays a default for that reason.

## The rule

1. Every metric named in a decision record or a commercial report
   appears in the venture's definitions file with a formula.
2. The formula sits next to the number wherever the number is shown, or
   one click away with the link in the same view.
3. A definition change is stated in the report where it happens, with
   the old and the new formula and the date.
4. The name diff between the metrics used and the metrics defined is
   empty. A metric with no definition is not reportable.

## House definitions

These are the starting set. A venture may replace any of them with a
recorded reason, and then owns keeping the replacement true.

| Metric | Formula | Notes |
| --- | --- | --- |
| Recognised revenue, period | Sum of transaction price allocated to performance obligations satisfied in the period | Cash collected is not this (EV-0297) |
| Deferred revenue | Cash received for obligations not yet satisfied | The other half of the same entry |
| Average revenue per account | Recognised revenue in period divided by accounts active at any point in the period | State the denominator; averaging over month-end accounts gives a different number |
| Cohort retention at age n | Accounts from the cohort still active at age n divided by accounts in the cohort at age zero | Reported as a curve, never as one blended rate (EV-0296) |
| Blended churn | Accounts lapsing in a period divided by accounts active at the start | Reportable as an operational number, refused as a lifetime value input |
| Lifetime value | Sum over projected cohort ages of retention at age n times contribution per account at age n | Contribution uses allocated cost to serve, not price |
| Allocated unit cost | Cost to serve one unit under the venture's FinOps allocation | Owned by the devops-reliability pack |
| Gross margin per unit | Price minus allocated unit cost, over price | Meaningless without the allocation |
| Rolling twelve-month taxable turnover | Taxable supplies over the trailing twelve months, recomputed monthly | A VAT threshold watch metric, not an accounting one |
| Trial adoption | Trials started divided by eligible new users | One of three trial stages, reported separately |
| Immediate conversion | Paid within the trial window divided by trials started | Never the sole readout of a trial test |
| Delayed conversion | Paid after the trial window divided by trials started | The stage that moved in the trial evidence |

## Anti-patterns this prevents

- The same word meaning two things in two reports in the same quarter.
- A metric definition quietly widening so that a number improves.
- Reporting one blended churn figure and calling it retention.
- Judging a trial-length experiment on immediate conversion alone,
  because that was the only stage in the report. See
  `packs/business-model-pricing/guides/GD-BMP-003-try-before-paying.md`.
- A margin figure computed from price against unallocated cost.

## The one-person venture problem

Segregation of duties is not available when one person books the
revenue, sets the price and writes the report. Nothing was found at the
cutoff on financial controls proportionate to that situation, and this
pack does not invent one. The partial substitute that these definitions
provide is a written, dated definition that a future reader can check
the numbers against. That is a weaker control than a second person, and
it should be named as weaker rather than presented as sufficient.
