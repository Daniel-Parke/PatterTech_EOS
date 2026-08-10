---
summary: The pack applied end to end to a subscription that renews monthly, prorates a mid-period upgrade and publishes a renewal event
type: example
tags: [money, data, arch]
kind: exemplar
scope: estate
---

# EX-BLM-001: The subscription that renewed on the wrong day

A worked run of this pack against one concrete situation, from the
first read of the requirement to the merge. Every rule that fires is
named where it fires.

## The situation

A venture sells a monthly subscription. Customers are in the United
Kingdom, Iceland and Japan. Three defects arrive in the same week.

A customer upgraded mid-period and the proration came out a penny short
of the invoice total. An Icelandic customer was charged an amount a
hundred times too small. And in late October a handful of UK renewals
fired an hour early, which nobody noticed until a customer was billed
twice in one calendar day.

The existing code stores the price as a float, the renewal date as a
naive local datetime, and the subscription status as three booleans.

## Step 1: activation and routing

Predicates `models_money`, `models_time`, `has_lifecycle_state` and
`encodes_domain_rule` are all true, so the pack loads in full. The task
touches money, so `kernel/POLICY_SPEC.md` rules the tier, and money
movement stays a guarded action under `kernel/GUARD_SPEC.md` whatever
this pack says about modelling it. The pack advises; it grants nothing.

## Step 2: how much model

Guide GD-BLM-001. The rules are thin: a price, a period, a status and
a proration. There is exactly one sentence that qualifies as an
invariant spanning more than one object: a subscription's ledger
entries must never sum to something other than what the customer was
charged for the period.

So the ruling is A plus B, with C for that one invariant only. No
repository interface, no event bus, no domain service layer. The
subscription and its ledger entries form one boundary, written up in
the field set from
`packs/business-logic-modelling/refs/BOUNDARY_WRITE_UP.md`. Everything
else stays a function.

## Step 3: money

Requirement B1 and guide GD-BLM-003. The float goes. Money becomes an
integer count of minor units plus a currency code, with the exponent
read from a table pinned to a recorded version of the published lists.

That fixes the Icelandic defect immediately: the currency's exponent is
zero, and the old code divided by a hundred on the way out. The
provider wants that same currency sent in hundreds for backwards
compatibility, so that quirk goes in the provider adapter and nowhere
else, per D7. The domain holds the standard exponent. A pin test
records the adapter's behaviour for each quirky currency, so the next
change to the provider's contract is visible.

The penny defect is the allocation function. A part-period upgrade
divides a monthly price by days, and the old code rounded each part
independently. Now the division goes through one allocation function
that returns parts summing exactly to the original amount, with the odd
minor unit going to the earlier period by recorded decision. That
decision is a business decision and it sits in the change record, not
in a comment.

## Step 4: time

Requirement B2 and guide GD-BLM-004. The naive local datetime goes. The
renewal instant becomes a zoned date-time carrying Europe/London,
Atlantic/Reykjavik or Asia/Tokyo, not an offset, because an offset is a
number and only a zone identifier answers what one month later means.

The rule is written down explicitly for the first time: a monthly
renewal is a calendar operation in the customer's zone, then resolved
to an instant. It is not thirty days added to a timestamp. On the
morning the UK clocks go back, the renewal lands at the same local time
it always did, which is what the customer expects and what the old code
got wrong.

The trial period is the other kind. A fourteen-day trial is elapsed
time, so it is arithmetic on the instant and a clock change does not
move it. Both rules are declared at the point they are written, per
`packs/business-logic-modelling/refs/TIME_TYPES.md`.

The customer's zone is stored on the subscription. It was previously
inferred from the billing address, which is how a customer who moved
started renewing on the wrong day.

## Step 5: lifecycle

Default D3 and guide GD-BLM-002. The three booleans go. Trialling,
active, past due, cancelled and expired become one closed status type
with a hand-written transition table listing the seven legal
transitions.

An illegal transition raises. It does not return false and it does not
quietly do nothing, because a silent no-op leaves the caller believing
the change happened. Five states and seven transitions is well inside
what one person holds in their head, so there is no state machine
library and no engine here. That is the threshold in GD-BLM-002, not a
preference about dependencies.

## Step 6: the price bands

Five price bands that marketing changes on its own clock, previously a
chain of conditionals edited by a developer every time. Guide
GD-BLM-002 rules B: a flat decision table with declared inputs,
declared outputs and declared overlap handling, evaluated in process.

No rule engine. No second runtime. No chaining, so no rule's output
feeds another rule's condition, which is the property that makes a rule
set unpredictable. A completeness check over the table runs in the test
suite and fails on a gap.

## Step 7: the outbox

Default D10 and guide GD-BLM-005. The renewal event was previously
published after commit, in a separate call, which is why one customer
saw a renewal email for a charge that had been rolled back.

The event now goes to an outbox table written in the same transaction
as the ledger entries, relayed afterwards. The consumer is keyed on the
renewal identity, so a redelivery is a no-op. The pattern buys
at-least-once delivery and nothing more, which is why the idempotence
half is not optional.

The change record names the pattern: event notification through an
outbox. It does not say "we went event-driven", because that phrase
covers four different things and settles no argument.

## Step 8: what the checks caught

C1 found two remaining float annotations in a reporting helper. C4
found one place still comparing a naive datetime. C7 found the
transition table missing the past-due to cancelled pair, which was
legal in the old booleans and had been lost in translation. All three
were fixed before review. The judgement rows added one finding: the odd
penny decision had been made in code review rather than by anyone who
sells the product, so it went back and got a real answer.

## What it would have looked like without the pack

The Icelandic defect fixed with a special case in the formatter. The
penny defect fixed by rounding the last part differently. The renewal
defect fixed by adding an hour of tolerance. All three fixes local, all
three plausible, and all three still wrong the next time a currency, a
zone or a clock change arrives.
