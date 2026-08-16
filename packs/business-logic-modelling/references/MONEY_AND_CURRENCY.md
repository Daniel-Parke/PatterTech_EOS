---
summary: The money type, the exponent table, rounding and allocation, and the adapter boundary with external systems
kind: fact
scope: estate
sources: [EV-0017, EV-0150, EV-0188, EV-0283, EV-0284, EV-0285]
volatility: slow
review: on-change-of:ISO-4217-amendment
type: implementation
tags: [money, data, tooling]
---

# Money and currency

Reference for PACK.md B1 and D7, and for WG-BLM-003.

## The type

A money value is two fields and no more:

- `minor_units`: a signed integer. Not a float, not a decimal string,
  not a fixed-point wrapper over a float.
- `currency`: an alphabetic code from the published lists (EV-0283).

Construction refuses anything else, per D9. There is no constructor
that takes a decimal amount without also taking the currency, because
the exponent is meaningless without it.

## The exponent

The published lists carry an alphabetic code, a numeric code and a
minor unit exponent per currency, and that exponent varies (EV-0283).
Two decimal places is common and it is not the rule. The consequences:

- Formatting divides by ten to the power of the currency's exponent.
- Parsing a human-entered decimal multiplies by the same power and
  refuses a value with more fractional digits than the currency has.
- A currency with an exponent of zero has no fractional part at all,
  and code that assumes it does will render an amount a hundred times
  too small.

Pin the table to a recorded version of the lists and record which
amendment you are on. The lists are versioned and currencies move to
the historical list, most recently on a euro adoption (EV-0283). A
stored amount keeps the code it was denominated in and is never
reinterpreted under a successor currency.

## Arithmetic

- Addition and subtraction between two amounts require equal currency
  codes and raise otherwise. There is no implicit conversion, because a
  conversion needs a rate, a time and a decision.
- Multiplication is by a scalar, never by another money value.
- Division of an amount is not a plain division. It goes through the
  allocation function below.
- Comparison across currencies raises for the same reason as addition.

## Rounding and allocation

The published lists give codes and exponents. They do not give rounding
rules, allocation rules or conversion (EV-0283), so this part is an
estate decision.

- Every division of an amount goes through one allocation function that
  takes an amount and a list of weights and returns parts that sum
  exactly to the original.
- The remainder is distributed deterministically. Which part receives
  the odd minor unit is a business decision recorded in the change
  record, not a property of the function's implementation.
- Rounding mode is declared once per venture and applied nowhere else.
  Half-up and banker's rounding are both defensible; silently taking
  the language default is not.
- The property worth testing is that allocation is exact: for any
  amount and any weights, the parts sum to the input (EV-0017, EV-0188
  in the delivery-testing pack own the mechanics).

## The adapter boundary

One adapter per external system owns the translation, per D7 and
EV-0150. What the adapter absorbs:

- Providers that want a zero-decimal currency sent in hundreds for
  backwards compatibility (EV-0284).
- Currencies charged with two decimals and paid out in whole units
  (EV-0284).
- Any accounting system with its own precision, and any tax engine with
  its own rounding step.

The domain never learns these quirks. A test that pins the adapter's
behaviour for each quirky currency is the cheapest way to keep them
there, and the provider's page changes without notice, so the pin is
what tells you when it moved.

## What this reference does not settle

Foreign-exchange conversion, multi-currency accounting, the choice of
rounding mode, and the treatment of tax-inclusive prices. None of the
sources here covers them, and all four are venture decisions recorded
in a lock-book rather than doctrine.
