---
id: WG-BLM-003
summary: How is money represented, rounded, allocated and converted at the edges?
kind: wargame
type: wargame
tags: [arch, data, eos, money, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-BLM-001, DOC-BLM-009]
applies_when: [models_money]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: binding
basis: standard
evidence_grade: observational
sources: [EV-0150, EV-0283, EV-0284, EV-0285]
review: on-change-of:ISO-4217-amendment
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-BLM-003: How is money represented?

## Decision question and stakes

The representation itself is settled and binds as B1 in PACK.md: an
integer count of minor units carrying its currency code. The live forks
are the ones underneath it. Where does the exponent come from, what
happens at the boundary with an external system, and who owns rounding
and allocation when a division does not come out even.

## Doctrines or coverage gap under pressure

- `DOC-BLM-001` (binding): Money is an integer count of minor units carrying its currency code.
- `DOC-BLM-009` (default): Conversion between domain money and any external money happens in one adapter.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `models_money`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Integer minor units, currency code alongside, exponent from a pinned table

Assume `A. Integer minor units, currency code alongside, exponent from a pinned table` was selected and the outcome failed. Test this option's stated failure mechanism first: and a single place to update when an amendment lands. Costs a table to maintain and a version to record.

### Premortem for B. A, plus a decimal type at the analytical edges

Assume `B. A, plus a decimal type at the analytical edges` was selected and the outcome failed. Test this option's stated failure mechanism first: one conversion boundary to police.

### Premortem for C. A, plus an allocation function for every division

Assume `C. A, plus an allocation function for every division` was selected and the outcome failed. Test this option's stated failure mechanism first: a decision about who gets the odd penny, which is a business decision and belongs in the change record.

### Premortem for D. Floats or bare numbers

Assume `D. Floats or bare numbers` was selected and the outcome failed. Test this option's stated failure mechanism first: Named here to be refused. Binary fractions do not represent most decimal amounts, sums drift, and every test with round numbers passes. The published lists and the largest provider both say otherwise (EV-0283, EV-0284).

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

## Safe default

A plus C, with the currency table version recorded in the repository
and the adapter owning every external quirk. Arithmetic between two
currencies raises rather than converting silently: a conversion needs a
rate, a time and a decision, and none of those belong in an addition
operator.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****How many currencies.** One currency for the life of the venture is a different problem from several, and the single-currency system that later adds a second is the expensive case.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A plus C, with the currency table version recorded in the repository and the adapter owning every external quirk. Arithmetic between two currencies raises rather than converting silently: a conversion needs a rate, a time and a decision, and none of those belong in an addition operator.

**Exit condition:** Stop or roll back the selected branch when and a single place to update when an amendment lands. Costs a table to maintain and a version to record, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **How many currencies.** One currency for the life of the venture is a different problem from several, and the single-currency system that later adds a second is the expensive case.

## Counter-evidence and transfer limits

No single currency table is authoritative across a whole system. The
standard lists and the provider's contract disagree on specific
currencies, and the provider's page changes without notice (EV-0283,
EV-0284). That disagreement is the argument for the adapter, not an
argument for picking a favourite. Neither source gives rounding rules
or allocation rules, so C is this estate's decision, argued from the
requirement that parts sum to the whole.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
