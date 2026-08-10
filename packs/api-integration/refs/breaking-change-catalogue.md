---
summary: What counts as a breaking change, the compatibility tiers and modes available, and how the gate is wired
kind: fact
scope: estate
sources: [EV-0129, EV-0135, EV-0136, EV-0139, EV-0124]
volatility: slow
review: on-change-of:EV-0129
type: example
tags: [arch, ci, delivery]
---

# Reference: breaking changes, tiers and the gate

Level 3 detail behind BR-2, BR-3 and BR-6.

## Three guarantees, not one

Compatibility is source, wire and semantic, and each has to hold
independently (EV-0129). A change can pass a wire check and still break
a consumer's build, or pass both and still change what a value means.

## What is breaking

From AIP-180 (EV-0129), scoped as noted:

- Renaming a field or a method. A rename is a removal plus an addition.
- Removing anything.
- Changing a type, including widening or narrowing a numeric type.
- Changing a default value.
- Adding a required field to a request.
- Changing the format of a resource name or identifier.
- Moving a field into or out of a oneof, for protobuf.
- Changing how a value is constructed or what it means, even with the
  schema untouched. This is the semantic guarantee, it is the strictest
  bar in the list, and no gate detects it.

Adding an enum value is flagged as risky rather than forbidden, which
leaves a judgement call: a consumer switching exhaustively will fall
through on a value it has never seen.

Caveat on scope: AIP-180 is written for protobuf-shaped APIs at Google
scale, and its semantic bar is stricter than most estates can afford.
The list of what breaks a consumer generalises; the ceremony around it
does not.

## Tiers and modes

For protobuf, buf makes strictness a declared setting with a strict
default you relax deliberately (EV-0135):

| Tier | Protects |
| --- | --- |
| FILE | generated code layout, the default |
| PACKAGE | package-level source compatibility |
| WIRE_JSON | wire plus JSON field names, the minimum where JSON transports are used |
| WIRE | binary wire only |

For event schemas, the mode encodes an upgrade order (EV-0139):

| Mode | Meaning | Upgrade order |
| --- | --- | --- |
| BACKWARD | new schema reads old data, the default | consumers first |
| FORWARD | old schema reads new data | producers first |
| FULL | both | either |
| NONE | no check | lockstep |

Transitive variants check every prior version rather than only the last,
and are the only modes safe for a log a consumer can rewind. A
non-transitive mode on a replayable topic gives false comfort.

HTTP has no equivalent tier vocabulary. oasdiff supplies configurable
rules instead, so the estate encodes its own promise in the ruleset and
records the resulting tier name in DECISIONS.md (EV-0136).

## Wiring the gate

The gate runs in CI, against a committed baseline, and fails the build.
For an OpenAPI document:

```bash
oasdiff breaking api/baseline/openapi.yaml api/openapi.yaml --fail-on ERR
oasdiff changelog api/baseline/openapi.yaml api/openapi.yaml
```

The first command is the gate. The second reports consumer-visible but
non-breaking changes, which belong in release notes rather than in a
build failure (EV-0136).

Two limits worth stating plainly. The gate detects only what the
specification expresses, so a semantic break with an unchanged schema
passes silently. And it needs a reliable baseline, so it works only
where the specification is generated or authored with discipline
(EV-0136).

## Shipping a break anyway

When the change has to happen:

1. Add the new shape alongside the old.
2. Mark the old one deprecated in the specification, and announce it in
   band with a date (EV-0124).
3. Publish a sunset date, never earlier than the deprecation date
   (EV-0124).
4. Put anything that cannot coexist, such as a newly required request
   field, behind a version discriminator.
5. Remove only after the sunset date, as a separate change.

Deprecation headers are informational and change no behaviour, so they
work only if consumers instrument for them (EV-0124). Announce out of
band as well.
