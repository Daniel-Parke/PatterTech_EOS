---
summary: Where does a lawful marketing address come from, and what may be sent to it?
kind: guide
authority: binding
lifecycle: active
basis: law
evidence_grade: observational
scope: estate
applies_when: [collects_contact_details, sends_marketing_message]
volatility: fast
review: on-change-of:PECR-reg-22-amendment
sources: [EV-0041, EV-0225]
type: guide
tags: [pii, forms, content]
review_by: 2027-04
---

# GD-MKTG-002: Where does a lawful marketing address come from?

## The question

PACK.md B1 requires a lawful basis stored with every address. This guide
decides which basis a given capture route can honestly claim, and what
that basis then permits. Getting it wrong at capture is unrecoverable,
because the fact you needed to record was true only at the moment of
collection.

## It depends on

- **Whether the person is an individual subscriber**, which includes
  sole traders and most partnerships, or a corporate one. The
  distinction sits in regulator guidance rather than the regulation text
  (FRAG-MKTG-09).
- **Whether a sale or a negotiation actually happened** with that
  person, not with their employer and not nearly.
- **What you intend to send**, because the soft opt-in reaches similar
  products and services only.
- **Jurisdiction.** UK rules do not transfer to the US opt-out regime,
  and EU member states implement the parent directive with local
  variation.
- **Whether the venture can evidence the capture** a year later without
  the person's help.

## Options

### A. Explicit opt-in at a form the person filled in
An unticked box or a deliberate action, with the wording, timestamp and
source stored on the record. Buys the widest permission and the simplest
story to a regulator. Costs conversion at the form, and it needs the
capture wording stored, not just a boolean.

### B. Soft opt-in from a prior sale or negotiation
Permitted only where all three conditions hold together: details
obtained in the course of a sale or negotiation with that person,
similar products and services only, and a simple free refusal route
offered at collection and in every later message (FRAG-MKTG-09). Buys a
lawful route to existing customers without a second consent step. Costs
a stored reference to the transaction it rests on, and it narrows what
may be sent. A record claiming this with no transaction reference is
invalid, and should fail validation rather than warn.

### C. Corporate subscriber
The regulation's consent requirement for electronic mail bites on
individual subscribers, so a corporate address sits differently. Buys
reach into business contacts. Costs certainty: the individual and
corporate line, and the enforcement practice around it, live in
regulator guidance rather than in the regulation, and data protection
duties still apply to a named person at a company (EV-0041, EV-0225).
Record the classification and the reason for it, never assume it from
the domain.

### D. A bought, rented or scraped list
Named to be excluded. The provenance you need cannot travel with an
address you did not collect, the consent was not given to you, and B1
cannot be satisfied by a supplier's assurance. There is no configuration
of this option that this pack permits.

## Decision rule

If the person acted at a form you control, record A with the wording
shown. If a sale or negotiation happened with that person and you intend
to send similar things only, record B with the transaction reference. If
the subscriber is corporate, record C with the reason for the
classification, and keep the refusal route anyway. Never D. Where two
routes could apply, record the stronger one, which is A.

## Default

A. It is the only route whose permission does not narrow over time, and
it is the one a machine can validate completely from the stored fields.

## Worked rulings

- **marketing-growth pack exemplar (2026-08, argued)**: A for the launch
  sequence, with the soft opt-in enum value present in the schema and
  unused, so the validator that rejects a soft opt-in with no
  transaction reference is exercised by a fixture rather than by live
  data. See
  `packs/marketing-growth/exemplars/EX-MKTG-001-launch-and-first-sequence.md`.
- **Estate default (2026-08, argued)**: the basis enum is closed and
  legitimate interests is not in it for marketing mail to an individual.
  A venture wanting a route this guide does not list argues it as an RFC
  against the regulation text, not in a lock-book note. The field shape
  is in `packs/marketing-growth/refs/CONSENT_RECORD.md`.
