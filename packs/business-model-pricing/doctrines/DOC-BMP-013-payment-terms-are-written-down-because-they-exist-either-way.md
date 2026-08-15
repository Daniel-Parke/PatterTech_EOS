---
summary: Payment terms are written down, because they exist either way.
type: doctrine
tags: [eos]
id: DOC-BMP-013
statement: Payment terms are written down, because they exist either way.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [sets_a_price]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0301, EV-0302]
review: on-change-of:DMCC-Part-4-Chapter-2-commencement
lifecycle: active
verification_refs: [packs/business-model-pricing/CHECKS.md]
migration_sources: [packs/business-model-pricing/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-BMP-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Predicates: sets_a_price, sells_to_public_sector. Where nothing is
agreed, a commercial payment is late thirty days after the later of
invoice receipt and delivery; terms may run to sixty days between
businesses where fair, and public authorities pay within thirty
(EV-0301). Every public contract carries an implied thirty-day term that
no clause can override, and a valid invoice needs the supplier name, a
description, the amount and a unique identifier (EV-0302). Those are the
law and they apply whatever this pack says. What is a default is writing
the term into the quote, and the reason is that a quote shipped with no
term invites the belief that nothing is therefore late. Departing means
recording that the statutory default is the term you are relying on.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-model-pricing/PACK.md:defaults:009`, lines 220-231, SHA-256 `718370afb1f8a47b97b1598f0561ec7879ef96579f7bf4dcf73052e646134593`.
