---
summary: Deliverability is a preflight gate before a first send.
type: doctrine
tags: [eos]
id: DOC-MKTG-012
statement: Deliverability is a preflight gate before a first send.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [publishes_public_content]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0360]
review: on-change-of:PECR-reg-22-amendment
lifecycle: active
verification_refs: [packs/marketing-growth/CHECKS.md]
migration_sources: [packs/marketing-growth/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-MKTG-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

SPF or
DKIM, forward and reverse DNS, TLS and RFC 5322 conformance for every
sender; above five thousand messages a day, SPF and DKIM and DMARC with
From alignment plus one-click unsubscribe; spam rate under 0.30 per
cent (EV-0360). Reason: published numbers a machine can assert
before anything ships. Scope note: one mailbox provider's rules for its
own inboxes. Others publish overlapping but different thresholds, and
at least one computes the spam-rate denominator differently, so no
single number is universal. See
`packs/marketing-growth/refs/SEND_PREFLIGHT.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/marketing-growth/PACK.md:defaults:009`, lines 214-223, SHA-256 `1f4e72a94d045959d3c1cb03d5028ced64d7ca0226e265084ceb0f9c98cc72b2`.
