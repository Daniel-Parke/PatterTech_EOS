---
summary: The stored shape of a lawful marketing basis, the closed enum, the soft opt-in tests and the suppression store
kind: fact
scope: estate
sources: [EV-0041, EV-0225]
volatility: fast
review: on-change-of:PECR-reg-22-amendment
type: implementation
tags: [pii, forms, tooling]
---

# Consent record

Reference for PACK.md B1 and B3, and for
`packs/marketing-growth/guides/GD-MKTG-002-consent-route.md`. This is
the field shape, not the law. The law is PECR regulation 22 as amended
(FRAG-MKTG-09) with UK data protection duties beside it (EV-0225,
EV-0041), and it is cited rather than restated because the statutory
text moves.

## The record

Every contact carries these fields, written at capture and never
back-filled.

| Field | Type | Rule |
| --- | --- | --- |
| address | string | the electronic contact point |
| subscriber_type | enum: individual, corporate | recorded with a reason, never inferred from the domain |
| lawful_basis | closed enum, below | one value, true at the moment of capture |
| captured_at | timestamp | when, not when the row was written |
| source | string | the form, import or integration that produced it |
| capture_wording | string | the words the person saw, for basis explicit_opt_in |
| transaction_ref | string | required when basis is soft_opt_in, otherwise absent |
| similar_products_scope | string | required when basis is soft_opt_in |

## The closed enum

Three values, and no others.

- `explicit_opt_in`: the person took a deliberate action at a form under
  your control. Requires capture_wording.
- `soft_opt_in`: all three PECR conditions held together. Requires
  transaction_ref and similar_products_scope.
- `corporate_subscriber`: the subscriber is not an individual. Requires
  a recorded reason in source.

Legitimate interests is deliberately absent. It is not an escape from
the regulation 22 consent requirement for marketing mail to an
individual subscriber, and a schema that offers it will collect it.

## The three soft opt-in tests

A soft_opt_in record is valid only when all three hold. Any one missing
invalidates the basis, and the validator rejects rather than warns.

1. The details were obtained in the course of a sale or a negotiation
   for a sale with that person. Not with their employer, not an
   enquiry that went nowhere.
2. What is sent is a similar product or service. The stored
   similar_products_scope is what that claim is checked against later.
3. A simple free refusal route was offered at collection and appears in
   every subsequent message. The second half is PACK.md B2's job.

## Suppression

The suppression store is a separate artefact from the contact table, and
it outranks it. Rules:

- A valid unsubscribe request writes to it before returning success.
- The send path reads it and fails closed on any address in it. Failing
  closed means a non-zero exit, not a logged warning.
- It survives list re-import: an address in suppression that reappears
  in an import stays suppressed, and the import records the collision.
- It survives a change of sending provider, because it lives with the
  venture and not with the provider.
- Removal from suppression happens only through a fresh capture that
  writes a new record under this schema.

## What this file does not settle

How long a consent stays fresh before it should be re-taken. The
regulation does not put a number on it and the pack refuses to invent
one. Jurisdiction beyond the UK: the US regime is opt-out and EU member
states vary (FRAG-MKTG-09), so a venture sending outside the UK adds
routes rather than reinterpreting these.
