---
id: WG-MKTG-002
summary: Where does a lawful marketing address come from, and what may be sent to it?
kind: wargame
type: wargame
tags: [content, eos, forms, pii, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-MKTG-001]
applies_when: [collects_contact_details]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: binding
basis: law
evidence_grade: observational
volatility: fast
sources: [EV-0041, EV-0225, EV-0361]
review: on-change-of:PECR-reg-22-amendment
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-MKTG-002: Where does a lawful marketing address come from?

## Decision question and stakes

PACK.md B1 requires a lawful basis stored with every address. This Wargame
decides which basis a given capture route can honestly claim, and what
that basis then permits. Getting it wrong at capture is unrecoverable,
because the fact you needed to record was true only at the moment of
collection.

## Doctrines or coverage gap under pressure

- `DOC-MKTG-001` (binding): The lawful basis is stored with the address, not asserted about the list.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Whether the person is an individual subscriber**, which includes
  sole traders and most partnerships, or a corporate one. The
  distinction sits in regulator guidance rather than the regulation text
  (EV-0361).
- **Whether a sale or a negotiation actually happened** with that
  person, not with their employer and not nearly.
- **What you intend to send**, because the soft opt-in reaches similar
  products and services only.
- **Jurisdiction.** UK rules do not transfer to the US opt-out regime,
  and EU member states implement the parent directive with local
  variation.
- **Whether the venture can evidence the capture** a year later without
  the person's help.

Applicability is `collects_contact_details`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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
offered at collection and in every later message (EV-0361). Buys a
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

## Failure premises

### Premortem for A. Explicit opt-in at a form the person filled in

Assume `A. Explicit opt-in at a form the person filled in` was selected and the outcome failed. Test this option's stated failure mechanism first: conversion at the form, and it needs the capture wording stored, not just a boolean.

### Premortem for B. Soft opt-in from a prior sale or negotiation

Assume `B. Soft opt-in from a prior sale or negotiation` was selected and the outcome failed. Test this option's stated failure mechanism first: a stored reference to the transaction it rests on, and it narrows what may be sent. A record claiming this with no transaction reference is invalid, and should fail validation rather than warn.

### Premortem for C. Corporate subscriber

Assume `C. Corporate subscriber` was selected and the outcome failed. Test this option's stated failure mechanism first: certainty: the individual and corporate line, and the enforcement practice around it, live in regulator guidance rather than in the regulation, and data protection duties still apply to a named person at a company (EV-0041, EV-0225). Record the classification and the reason for it, never assume it from the domain.

### Premortem for D. A bought, rented or scraped list

Assume `D. A bought, rented or scraped list` was selected and the outcome failed. Test this option's stated failure mechanism first: Named to be excluded. The provenance you need cannot travel with an address you did not collect, the consent was not given to you, and B1 cannot be satisfied by a supplier's assurance. There is no configuration of this option that this pack permits.

## Decision rule

If the person acted at a form you control, record A with the wording
shown. If a sale or negotiation happened with that person and you intend
to send similar things only, record B with the transaction reference. If
the subscriber is corporate, record C with the reason for the
classification, and keep the refusal route anyway. Never D. Where two
routes could apply, record the stronger one, which is A.

## Safe default

A. It is the only route whose permission does not narrow over time, and
it is the one a machine can validate completely from the stored fields.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether the person is an individual subscriber**, which includes sole traders and most partnerships, or a corporate one. The distinction sits in regulator guidance rather than the regulation text (EV-0361).** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. It is the only route whose permission does not narrow over time, and it is the one a machine can validate completely from the stored fields.

**Exit condition:** Stop or roll back the selected branch when conversion at the form, and it needs the capture wording stored, not just a boolean, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether the person is an individual subscriber**, which includes sole traders and most partnerships, or a corporate one. The distinction sits in regulator guidance rather than the regulation text (EV-0361).

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Whether the person is an individual subscriber**, which includes sole traders and most partnerships, or a corporate one. The distinction sits in regulator guidance rather than the regulation text (EV-0361).** and ****Whether a sale or a negotiation actually happened** with that person, not with their employer and not nearly.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
