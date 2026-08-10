---
summary: What a reviewer or a script can verify about domain modelling work, split into executable today and judgement
kind: fact
scope: estate
sources: [EV-0017, EV-0157, EV-0188, EV-0269, EV-0270, EV-0277, EV-0281, EV-0283, EV-0284, EV-0285]
volatility: slow
review: 2027-11
type: implementation
tags: [testing, money, data]
---

# CHECKS

Evaluation criteria for work in this domain. Each row says what is
verified, against which requirement, and whether a machine can settle
it today. "Executable" means a script decides it with no human reading
the output. "Judgement" means a person rules and the record is the
evidence.

## Executable today

| # | Check | Verifies | How |
| --- | --- | --- | --- |
| C1 | No float or bare number holds an amount | B1 | scan the domain tree for float annotations, float constructors and float division on money |
| C2 | The money type's amount is an integer | B1 | construct one and assert the internal type |
| C3 | Formatting is exponent-driven, not fixed at two | B1 | the same integer renders differently in a two-decimal and a zero-decimal currency |
| C4 | Cross-currency arithmetic raises | B1 | add, subtract and compare two different codes, expect a raise each time |
| C5 | Allocation is exact | GD-BLM-003 | property test: for any amount and weights, the parts sum to the input (EV-0017, EV-0188) |
| C6 | Currency table version is recorded | ref MONEY_AND_CURRENCY | the pinned list version exists in the repo and is referenced by the lookup |
| C7 | External money quirks live only in an adapter | D7 | the domain tree contains no provider-specific currency case |
| C8 | No naive datetime in the domain tree | B2 | scan for datetime construction without a zone, and for storage of an offset where a zone was meant |
| C9 | Elapsed durations survive a clock change | B2 | property test across a daylight-saving boundary in a real zone, both directions |
| C10 | Calendar arithmetic happens in the zone | B2 | one month later at a clock change lands on the same local time, not the same offset |
| C11 | Illegal values cannot be constructed | D9 | construct each declared invalid case, expect a raise from the constructor |
| C12 | No validate-only path | D9 | the type exposes no `validate` or `is_valid` that a caller may skip in place of construction |
| C13 | Transition matrix is exhaustive and refusing | D3 | drive every ordered pair of statuses; only declared pairs succeed, every other raises, none returns quietly |
| C14 | Outbox and state share a transaction | D10 | roll the transaction back, assert no message is relayed |
| C15 | Consumers are idempotent | D10 | deliver the same message twice, assert one effect |
| C16 | Decision tables are complete | D6 | evaluate every input combination, fail on a gap or an undeclared overlap (EV-0277) |
| C17 | No rule engine or state machine dependency without a recorded decision | D6, D1 | scan the dependency manifest against the change record |
| C18 | Every EV id cited in this pack exists | pack hygiene | lookup against `registry/evidence.json` |

C1 and C8 are the two cheapest checks in the pack and they catch the
two commonest defects, so they run on every change set rather than at
review. C13 is written as a matrix on purpose: a check that only walks
the legal path proves nothing about what the lifecycle refuses.

## Judgement, recorded not automated

| # | Check | Verifies | What good looks like |
| --- | --- | --- | --- |
| J1 | The invariant is a real invariant | D2 | one sentence, no "usually", spanning more than one object (EV-0269) |
| J2 | The boundary is written up | D2 | the field set is filled in and dated, and the corrective policy list is short (EV-0270) |
| J3 | The model grew against a named trigger | D1 | the change record names what forced the step, not a preference |
| J4 | The odd minor unit rule is a business decision | GD-BLM-003 | somebody who sells the product answered it, and the answer is in the change record |
| J5 | Each duration is declared elapsed or wall-clock | D5 | the declaration sits next to the rule, not in a library default |
| J6 | The event pattern is named | D11 | one of notification, state transfer, sourcing, CQRS, named in the change record |
| J7 | The rule lives on the right clock | D6 | who edits it and how often, stated, and the home follows |
| J8 | An event log holding personal data has an erasure story | GD-BLM-005 | the story exists and `packs/security-privacy/PACK.md` has seen it |
| J9 | Departures from a default carry a reason | defaults | the reason is in the task record, not in a commit message alone |

## Not verifiable here

- Whether the model shape was right. No source in this pack measures
  aggregate sizing against defect or contention rates, so no check
  claims it.
- Whether the modelling method improved anything. The strongest review
  available finds demonstrated value in decomposition and thin support
  for the rest.
- Whether a rule is correct as a business rule. That is a question for
  the person who owns the product, and the checks only establish that
  the rule is where somebody can find and argue with it.

## Cadence

C1 to C4, C8, C11, C12 and C18 run on every change set. C5, C9, C10,
C13, C14, C15 and C16 run on any change touching money, time,
lifecycle or a decision table. C6, C7 and C17 run on any dependency or
adapter change. The judgement rows run at review, and J1 to J3 run once
per boundary at the point the model grows, then again when the
invariant changes.
