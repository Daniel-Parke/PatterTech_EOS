---
summary: Which register does this surface speak in?
type: wargame
tags: [voice, content, brand]
status: active
review_by: 2027-07
---

# WG-VOX-001: Which register does this surface speak in?

## The question

The voice law (doctrine/voice/DOCTRINE.md) fixes how every PatterTech
surface is written. It does not fix who the writing talks to. A page
for an insurer, a peer engineer and an anxious first-time customer can
all obey the law and still need different registers: how much is
assumed, how much is scaffolded, how the stakes are handled. Every
venture rules its register per surface family before copy is written.

## It depends on

- Audience expertise: can they fill gaps themselves, or does a gap read
  as a wall?
- Cost of misreading: money, legal exposure or safety raise the bar for
  explicitness.
- Brand identity: what the lock-book's narrative brief says the visitor
  should feel.
- Regulatory constraints: some surfaces must carry defined wording
  (caveats, complaints routes) verbatim.

## Options

### A. Peer-expert
Dense, technical, no hand-holding. Assumes the reader shares the
vocabulary. Buys speed and credibility with experts; costs everyone
else. Right for developer docs, internal doctrine, technical appendices.

### B. Professional-calm
Plain, confident, evidence-led. States facts and shows records rather
than making claims. Buys trust across mixed professional audiences;
costs a little colour. The register of an organisation that expects to
be audited.

### C. Warm-guide
Second person, stepwise, anticipates anxiety. Buys comfort for
consumers at high-stakes moments; costs authority with experts and
length everywhere.

## Decision rule

If the surface faces insurers, assessors or professional buyers, choose
B. If the readers are peers of the writer (developer docs, internal
technical material), choose A. If the reader is a consumer at a moment
of uncertainty (onboarding, an error, money leaving their account),
choose C for that surface family only. Where wording is regulated,
the regulated text is verbatim regardless of register. Mixed audiences
take B with A-density appendices linked, never blended in place.

## Default

B, professional-calm. The estate sells trust in records; the register
that shows evidence without raising its voice serves every venture
until a trigger says otherwise.

## Worked rulings

- **PatterTech_Website (2026-07, argued)**: B for the site body with A
  moments in the technical build notes; the narrative brief ("a calm
  vessel around an undeniable source") rejects both hand-holding and
  showing off. Landed in the v0.1 lock-in, now
  examples/pattertech-website.md.
