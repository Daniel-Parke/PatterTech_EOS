---
summary: The lawful basis is stored with the address, not asserted about the list.
type: doctrine
tags: [eos]
id: DOC-MKTG-001
statement: The lawful basis is stored with the address, not asserted about the list.
kind: doctrine
authority: binding
basis: law
evidence_grade: observational
scope: estate
applies_when: [collects_contact_details]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0225, EV-0361]
review: on-change-of:PECR-reg-22-amendment
lifecycle: active
verification_refs: [packs/marketing-growth/CHECKS.md]
migration_sources: [packs/marketing-growth/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-MKTG-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`collects_contact_details`. Every contact record carries a
basis from a closed enum, a timestamp and the collection source,
written at capture; a record claiming soft opt-in also carries a
reference to the sale or negotiation it rests on. Prevents the one
failure that cannot be repaired afterwards. PECR regulation 22 requires
prior consent for marketing mail to an individual subscriber, with a
single narrow escape needing all three of details obtained in the
course of a sale or negotiation, similar products only, and a free
refusal route at collection and in every later message (EV-0361).
Provenance cannot be rebuilt from a table of addresses six months on,
and UK statute now expects a recorded lawful basis rather than a
privacy notice (EV-0225). Basis: law. See
`packs/marketing-growth/refs/CONSENT_RECORD.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/marketing-growth/PACK.md:requirements:001`, lines 106-119, SHA-256 `e6a1208c7b260bfb1156c8537a02cf2abdd233c6b426e60b25ddfa42b1771ff8`.
