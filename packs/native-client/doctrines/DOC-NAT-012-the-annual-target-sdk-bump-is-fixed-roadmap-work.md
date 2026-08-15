---
summary: The annual target SDK bump is fixed roadmap work.
type: doctrine
tags: [eos]
id: DOC-NAT-012
statement: The annual target SDK bump is fixed roadmap work.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0376]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-NAT-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

From 31
August 2026 Play requires API 36 for new submissions and API 35 for an
existing app to stay visible to new users on current devices
(EV-0376). Reason: an unmaintained client goes quietly
invisible.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:defaults:005`, lines 229-233, SHA-256 `0daace0990fafe95eb9d2f1ccb2c8f10ece984e58f3a4ec49082f8d0e2056c7d`.
