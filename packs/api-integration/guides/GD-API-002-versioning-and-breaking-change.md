---
summary: How is a boundary allowed to change: add only, declared tier plus gate, explicit version parameter, or pinned date with transformers?
kind: guide
authority: advisory
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0129, EV-0131, EV-0132, EV-0134, EV-0135, EV-0136, EV-0139, EV-0061, EV-0140]
review: on-change-of:EV-0129
type: guide
tags: [arch, ci, delivery]
---

# GD-API-002: how is the boundary allowed to change?

## The question

Something has to give when the shape of a published boundary must
change. Either the change is forbidden, or it is absorbed somewhere:
in the server, in a version selector, or in the consumer's upgrade
schedule. The fork is where you put that cost. The failure that decides
it is the rename that ships on a Tuesday and takes a consumer down on
the Wednesday.

## It depends on

- Can you make every consumer upgrade, and how quickly?
- Are consumers inside the estate, or people you will never meet?
- Does the boundary carry business semantics, or is it a wire format?
- Can a consumer rewind and replay old messages?

## Options

### A. Never remove, only add

Commit publicly to additive change and drop version negotiation
entirely, as JSON:API does by keeping its version field optional
(EV-0134). GraphQL is the same bet with a stronger mechanism, since a
client receives only what it selected (EV-0140). Buys: no version
machinery at all. Costs: the surface accretes forever, deprecation
without a sunset date is not removal, and most of a mature additive
surface ends up unexercised. Additions are free; type, nullability and
argument changes are not.

### B. Declare a compatibility tier and machine-check it

Pick the strictness explicitly and gate it. Buf makes the tier a setting
with a strict default you relax deliberately (EV-0135); Confluent makes
the mode an upgrade order, where BACKWARD means consumers first, FORWARD
means producers first, and only the transitive variants are safe for a
replayable log (EV-0139); oasdiff brings the same to HTTP with
configurable rules and a separate changelog for consumer-visible but
non-breaking changes (EV-0136). Buys: the promise is written down and
enforced by a machine, and breaks surface at build time. Costs: needs a
committed baseline, and it detects only what the specification
expresses.

### C. An explicit version selector on every call

Azure mandates a required `api-version` query parameter with a dated
value and rejects a call without one; error codes are contract, so a new
top-level code needs a version bump (EV-0132). Zalando forbids URL
versioning and mandates media-type versioning instead (EV-0131). Buys: a
consumer's version is unambiguous and observable. Costs: the two mature
positions contradict each other, media-type versioning is poorly served
by browsers, caches and casual clients, and rejecting a call for a
missing version is hostile to exploration.

### D. Pin the consumer to a date and transform in the server

Stripe pins each account to a dated version and encapsulates every
incompatible change as a self-contained transformation module, which
kept roughly a hundred breaking changes invisible to callers (EV-0061).
Buys: the server absorbs everything and consumers upgrade when they
choose. Costs: real engineering in the version machinery, and by its own
account it pays off only at high consumer count.

## Decision rule

- Consumers inside the estate you can upgrade in one release train: B.
- Public boundary, many external consumers, none of whom you can make
  upgrade: D, once consumer count justifies the machinery, with B still
  underneath it.
- Platform or ecosystem mandate: C, in whichever form the platform
  requires, with B still underneath it.
- Wire format with no business semantics, or a selection-based surface:
  A is honest, provided a sunset policy exists for deprecated fields.

B is not exclusive with the others: it is the floor. Whatever the
selector, the tier is declared before the first change (D10) and the
gate runs in CI (BR-2). Renames and new required request fields are
breaking in every option (EV-0129): ship the new name alongside the old,
mark the old deprecated with a sunset date, and put a new required field
behind a version discriminator.

## Default

B, with `compatibility: BACKWARD` for HTTP boundaries and
`BACKWARD_TRANSITIVE` for any topic a consumer can rewind. The line goes
in DECISIONS.md or an ADR, in a form a checker can parse.

## Worked rulings

- **WiseWattage (2026, inherited)**: B in effect. The committed,
  drift-checked contract from
  `packs/architecture/guides/WG-ARCH-005-contract-seam.md` gives
  the baseline a gate needs; the tier itself was never written down,
  which is exactly the gap D10 closes.
- **No venture has argued D.** Stripe's approach is read as an exemplar
  in `packs/api-integration/exemplars/stripe-versioning.md`, not adopted.
- **No venture has argued C.** The three mature estates disagree
  (EV-0131, EV-0132, EV-0061), so there is no default to inherit.
