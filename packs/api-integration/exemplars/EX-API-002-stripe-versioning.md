---
summary: Stripe's pinned-date versioning read as an exemplar, what it actually costs, and the conditions under which copying it is right
kind: exemplar
scope: estate
sources: [EV-0061, EV-0133, EV-0132, EV-0134, EV-0136]
type: example
tags: [arch, money, delivery]
---

# EX-API-002: reading Stripe's versioning

Stripe is the most cited answer to breaking-change management, and it is
routinely copied by estates that have none of the conditions that make
it work. This is the exemplar read properly: what the approach is, what
it buys, what it costs, and when it is the right answer.

## What they do

Each account is pinned to a dated API version. Every incompatible change
is written as a self-contained transformation module that converts
between the current internal representation and the older responses. A
caller sees the shape it was pinned to until it deliberately upgrades.
Roughly a hundred breaking changes have gone out this way while callers
saw none (EV-0061).

## What it buys

- Consumers upgrade on their own schedule, individually, not on the
  provider's release train.
- The server keeps one current internal model rather than branching the
  codebase per version.
- Each incompatible change is one reviewable, testable unit rather than
  a scattered set of conditionals.
- Old integrations built by people who have left the company keep
  working.

## What it costs

The version machinery is real engineering, permanently staffed. Every
transformation module is code that must keep working forever, or until
the version it serves is retired, and retiring one means chasing the
long tail of accounts still pinned to it. Stripe's own account concedes
the approach pays off at high consumer count and not below it (EV-0061).

There is a second, quieter cost. A pinned consumer never sees the
current shape, so bug reports arrive in dialects the current team has to
translate, and every support conversation begins by establishing which
version the caller is on.

## Conditions that make it right

All four, not some of them:

- Many external consumers you cannot contact, let alone make upgrade.
- Long-lived integrations, often built by third parties and then
  abandoned.
- Incompatible change is genuinely unavoidable and recurring, not a
  symptom of a boundary that was never designed.
- Enough engineering capacity to keep the transformation layer honest,
  with tests per version, forever.

Miss any one and a cheaper option fits better: a declared compatibility
tier with a machine gate (EV-0136), an explicit version parameter as
Azure mandates (EV-0132), or an add-only promise as JSON:API makes
(EV-0134).

## What we copy without copying the machinery

Three habits transfer cleanly to a two-consumer internal service:

1. **Treat an incompatible change as a named, self-contained unit.**
   Even without transformation modules, the change gets a record, a
   date and an owner rather than being one line inside a feature
   branch.
2. **Make the consumer's version explicit and observable.** Know which
   consumer is on which shape before deciding what is safe to remove.
3. **Settle idempotency parameters at the same time as versioning.**
   Stripe's idempotency documentation (EV-0133) is the clearest
   specification of the four decisions in the field, and it is
   independent of the versioning approach.

## Our ruling

The estate does not meet the conditions. No venture has an external
consumer base of the size that pays for the machinery, so the default in
`packs/api-integration/guides/GD-API-002-versioning-and-breaking-change.md`
stays a declared tier plus a gate. Stripe is read here as an exemplar
and a target for the day a venture does meet the conditions, not as
doctrine to adopt now.
