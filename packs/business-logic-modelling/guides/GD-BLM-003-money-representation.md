---
summary: How is money represented, rounded, allocated and converted at the edges?
kind: guide
authority: binding
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0150, EV-0283, EV-0284, EV-0285]
review: on-change-of:ISO-4217-amendment
type: guide
tags: [money, data, arch]
---

# GD-BLM-003: How is money represented?

## The question

The representation itself is settled and binds as B1 in PACK.md: an
integer count of minor units carrying its currency code. The live forks
are the ones underneath it. Where does the exponent come from, what
happens at the boundary with an external system, and who owns rounding
and allocation when a division does not come out even.

## It depends on

- **How many currencies.** One currency for the life of the venture is
  a different problem from several, and the single-currency system that
  later adds a second is the expensive case.
- **Which external systems handle the money.** A payment provider, an
  accounting ledger and a tax engine can each disagree about the same
  currency's minor units (EV-0284).
- **Whether amounts get split.** Proration, tax and discounts all
  divide, and division is where pennies get lost or invented.
- **Whether historical amounts must stay readable.** Currencies retire,
  so a stored amount keeps the code it was denominated in (EV-0283).

## Options

### A. Integer minor units, currency code alongside, exponent from a pinned table
The money type holds an integer and a code; the exponent is looked up
in a table pinned to a recorded version of the published lists
(EV-0283). Buys correctness with no runtime cost and a single place to
update when an amendment lands. Costs a table to maintain and a version
to record.

### B. A, plus a decimal type at the analytical edges
Domain arithmetic stays in integers; reporting and forecasting convert
once, deliberately, into an arbitrary-precision decimal. Buys
readable analytics without letting inexact arithmetic near a total that
somebody is charged. Costs one conversion boundary to police.

### C. A, plus an allocation function for every division
Any division of an amount goes through one function that distributes
the remainder deterministically and returns parts that sum exactly to
the original. Buys the guarantee that proration and split invoices
reconcile. Costs a decision about who gets the odd penny, which is a
business decision and belongs in the change record.

### D. Floats or bare numbers
Named here to be refused. Binary fractions do not represent most
decimal amounts, sums drift, and every test with round numbers passes.
The published lists and the largest provider both say otherwise
(EV-0283, EV-0284).

## Decision rule

A always. Add C the first time an amount is divided, which for anything
with subscriptions, tax or discounts is immediately. Add B only when a
reporting surface genuinely needs fractional units, and put the
conversion in one place. Never D, and no exception exists for "it is
only a display value", because display values become inputs.

Conversion to and from any external system's money happens in one
adapter per system, per default D7 in PACK.md, because the exponent is
a property of a currency in a context: the same provider charges some
currencies with two decimals and pays them out whole (EV-0284, EV-0150).
The domain never learns the provider's quirks.

## Default

A plus C, with the currency table version recorded in the repository
and the adapter owning every external quirk. Arithmetic between two
currencies raises rather than converting silently: a conversion needs a
rate, a time and a decision, and none of those belong in an addition
operator.

## Worked rulings

- **Zero-decimal currencies (external, inherited)**: the published
  lists give some currencies an exponent of zero, and the provider
  wants two of those sent in hundreds for backwards compatibility
  (EV-0283, EV-0284). The domain holds the standard exponent, the
  adapter holds the provider's. Neither leaks into the other.
- **Subscription proration (2026-08, argued)**: a monthly price split
  across a part month went through the allocation function; the parts
  summed to the original amount exactly and the odd penny went to the
  first period by recorded decision. See
  `packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md`.
- **Retired currency (external, inherited)**: an amendment moved a
  currency to the historical list on a euro adoption (EV-0283). Stored
  amounts keep their original code and are not reinterpreted, so
  historical invoices still say what they said.

## Counter-evidence

No single currency table is authoritative across a whole system. The
standard lists and the provider's contract disagree on specific
currencies, and the provider's page changes without notice (EV-0283,
EV-0284). That disagreement is the argument for the adapter, not an
argument for picking a favourite. Neither source gives rounding rules
or allocation rules, so C is this estate's decision, argued from the
requirement that parts sum to the whole.
